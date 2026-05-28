#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用每日文章生成脚本
根据执行时间自动判断批次，生成对应文章
用法：python -X utf8 auto_gen_daily.py --hour 9 --minute 15
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import json
import random

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
IMAGE_LIB = PROJECT_ROOT / "images" / "lib"
USAGE_LOG = SCRIPTS_DIR / "image_usage_log.json"

# 图片主题映射
CATEGORY_IMAGE_MAP = {
    "guokao": ["exam", "study", "gov", "motivation", "office"],
    "shengkao": ["exam", "study", "motivation", "office", "books"],
    "shanghai-shegong": ["gov", "office", "people", "city", "exam"],
    "gangwei-fenxi": ["office", "people", "gov", "tech", "city"],
    "beikao-zhinan": ["study", "books", "exam", "motivation", "writing"],
    "shang-an-jingyan": ["exam", "motivation", "people", "study", "office"],
    "zhengce-jiedu": ["gov", "office", "writing", "city", "tech"],
    "baokao-gonggao": ["gov", "office", "writing", "exam", "study"],
    "zhenti-jiexi": ["exam", "study", "books", "writing", "office"],
}

def load_usage_log():
    """加载图片使用日志"""
    if not USAGE_LOG.exists():
        return {}
    with open(USAGE_LOG, "r", encoding="utf-8") as f:
        return json.load(f)

def save_usage_log(log):
    """保存图片使用日志"""
    log["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(USAGE_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def get_available_images(category, count=2, days=10):
    """选取指定分类的未最近使用的图片"""
    log = load_usage_log()
    usage = log.get("usage", {})
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    themes = CATEGORY_IMAGE_MAP.get(category, ["study", "exam"])
    available = []
    
    for theme in themes:
        theme_dir = IMAGE_LIB / theme
        if not theme_dir.exists():
            continue
        for f in theme_dir.iterdir():
            if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            rel = f"/images/lib/{theme}/{f.name}"
            recently = False
            if rel in usage:
                try:
                    last = datetime.strptime(usage[rel], "%Y-%m-%d")
                    if last > cutoff:
                        recently = True
                except:
                    pass
            if not recently:
                available.append(rel)
    
    if len(available) >= count:
        return random.sample(available, count)
    return available[:count] if available else []

def generate_article_content(title, keyword, category, content_angle):
    """生成完整的文章内容（包含frontmatter和正文）"""
    # 根据分类和角度生成正文内容
    body = generate_body_by_category(category, content_angle, keyword, title, [])
    
    content = f"""# {title}

{keyword}是公考备考中的重要内容，本文将为您详细解析相关知识点和备考策略。

{body}

## 总结

通过对{keyword}的深入分析，我们系统性地梳理了相关核心要点。无论您是刚开始备考的新手，还是希望进一步提升的进阶考生，都建议结合自身实际情况，制定个性化的备考方案。公考之路虽充满挑战，但科学的备考方法和持续的努力必将带来理想的回报。祝愿各位考生在2026年的公考中顺利上岸，实现职业理想！
"""
    return content

def create_article(article_def, date_str, date_compact):
    """创建单篇文章"""
    filename = article_def["filename"].format(
        date=date_str,
        date_compact=date_compact,
        category=article_def["category"]
    )
    filepath = CONTENT_DIR / filename
    
    # 确保目录存在
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # 生成图片
    images = get_available_images(article_def["category"], count=2)
    
    # 更新图片使用记录
    log = load_usage_log()
    if "usage" not in log:
        log["usage"] = {}
    today = datetime.now().strftime("%Y-%m-%d")
    for img in images:
        log["usage"][img] = today
    save_usage_log(log)
    
    # 生成内容
    content = generate_article_content(
        article_def["title"],
        article_def["keyword"],
        article_def["category"],
        article_def.get("content_angle", "")
    )
    
    # 添加图片到内容
    img_md = ""
    for img in images:
        img_md += f"![]({img})\n"
    
    # 插入图片到合适位置（第二段后）
    content_parts = content.split("\n\n", 2)
    if len(content_parts) >= 3:
        content = content_parts[0] + "\n\n" + content_parts[1] + "\n\n" + img_md + "\n\n" + content_parts[2]
    else:
        content = content + "\n\n" + img_md
    
    # 构建Frontmatter
    tags_str = ", ".join([f'"{t}"' for t in article_def["tags"]])
    frontmatter = f"""---
title: "{article_def["title"]}"
date: "{date_str}"
category: "{article_def["category"]}"
tags: [{tags_str}]
author: "公考助手"
description: "{article_def["description"]}"
source_url: ""
source_date: ""
content_type: "article"
---

"""
    
    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
    
    print(f"✅ 已生成: {filename}")
    return str(filepath)

def get_articles_for_batch(hour, minute):
    """根据时间获取对应批次的文章定义"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_compact = datetime.now().strftime("%Y%m%d")
    
    # 定义不同批次的文章角度（避免重复）
    # 每个批次都是：社工2篇、国考2篇、省考2篇、事业单位1篇、通用1篇
    articles = [
        # 社工类（上海社工资讯）2篇
        {
            "filename": f"shanghai-shegong/{date_str}-shanghai-shegong-guide.md",
            "title": "2026年上海社区工作者招聘公告：16区招录计划与岗位分析",
            "keyword": "上海社区工作者招聘",
            "category": "shanghai-shegong",
            "tags": ["上海社工招聘", "2026公告", "16区招录", "岗位分析"],
            "description": "2026年上海社区工作者招聘公告全面解析，覆盖浦东、徐汇、静安等16个市辖区的招录计划、岗位类型、报名条件及薪资待遇等核心信息。",
            "content_angle": "公告分析"
        },
        {
            "filename": f"shanghai-shegong/{date_str}-shanghai-shegong-analysis.md",
            "title": "上海社工报名人数统计2026：各区竞争比与招录趋势分析",
            "keyword": "上海社区工作者报名",
            "category": "shanghai-shegong",
            "tags": ["上海社工报名", "竞争比例", "报名人数", "2026趋势"],
            "description": "2026年上海社区工作者报名人数统计与竞争比分析，对比16个市辖区的招录热度、报名趋势及上岸难度。",
            "content_angle": "报名指南"
        },
        # 国考 2篇
        {
            "filename": f"guokao/{date_str}-guokao-strategy.md",
            "title": "国考零基础备考攻略2026：从入门到上岸的180天系统规划",
            "keyword": "国考备考攻略",
            "category": "guokao",
            "tags": ["国考零基础", "180天备考", "系统规划", "2026国考"],
            "description": "2026年国家公务员考试零基础备考全攻略，系统规划180天复习时间表，涵盖行测、申论各模块学习重点与备考策略。",
            "content_angle": "备考攻略"
        },
        {
            "filename": f"guokao/{date_str}-guokao-tips.md",
            "title": "国考行测高频考点2026：近5年真题数据分析与命题趋势",
            "keyword": "国考行测",
            "category": "guokao",
            "tags": ["国考行测", "高频考点", "真题分析", "命题趋势"],
            "description": "2026年国考行测高频考点深度解析，基于近5年真题数据分析，总结命题规律、高频考点分布及2026年备考重点。",
            "content_angle": "考点分析"
        },
        # 省考 2篇
        {
            "filename": f"shengkao/{date_str}-shengkao-preparation.md",
            "title": "省考申论写作技巧2026：高分作文结构与论点提炼方法",
            "keyword": "省考申论",
            "category": "shengkao",
            "tags": ["省考申论", "写作技巧", "高分作文", "论点提炼"],
            "description": "2026年省考申论写作全面指导，高分作文结构解析、论点提炼方法、经典案例运用技巧，助力考生突破申论瓶颈。",
            "content_angle": "写作技巧"
        },
        {
            "filename": f"shengkao/{date_str}-shengkao-review.md",
            "title": "省考真题解析2026：近年真题回顾与2026备考重点",
            "keyword": "省考真题",
            "category": "shengkao",
            "tags": ["省考真题", "历年真题", "备考重点", "2026省考"],
            "description": "2026年省考真题全面解析，近年真题分类整理、题型变化趋势分析、高频考点汇总及2026年省考备考重点预测。",
            "content_angle": "真题解析"
        },
        # 事业单位 1篇
        {
            "filename": f"gangwei-fenxi/{date_str}-shiyedanwei-overview.md",
            "title": "事业单位综合管理岗2026：岗位职责与能力要求全面解读",
            "keyword": "事业单位招聘",
            "category": "gangwei-fenxi",
            "tags": ["事业单位", "综合管理岗", "岗位职责", "能力要求"],
            "description": "2026年事业单位综合管理岗位全面解读，岗位职责详细说明、核心能力要求分析、备考策略及面试常见问题汇总。",
            "content_angle": "岗位分析"
        },
        # 通用备考 1篇
        {
            "filename": f"beikao-zhinan/{date_str}-general-methods.md",
            "title": "公考面试礼仪全指南2026：着装、言行、细节决定成败",
            "keyword": "公考面试",
            "category": "beikao-zhinan",
            "tags": ["公考面试", "面试礼仪", "着装要求", "言行规范"],
            "description": "2026年公考面试礼仪全面指南，从着装选择、言行举止到细节把控，全方位提升面试形象，增加上岸成功率。",
            "content_angle": "面试指南"
        }
    ]
    
    return articles

def main():
    parser = argparse.ArgumentParser(description="生成每日公考SEO文章")
    parser.add_argument("--hour", type=int, required=True, help="执行小时(0-23)")
    parser.add_argument("--minute", type=int, required=True, help="执行分钟(0-59)")
    args = parser.parse_args()
    
    print(f"🚀 开始生成 {args.hour:02d}:{args.minute:02d} 批次文章...")
    
    articles = get_articles_for_batch(args.hour, args.minute)
    
    generated_files = []
    for article_def in articles:
        fpath = create_article(article_def, 
                                datetime.now().strftime("%Y-%m-%d"),
                                datetime.now().strftime("%Y%m%d"))
        generated_files.append(fpath)
    
    print(f"\n✅ 批次完成！共生成 {len(generated_files)} 篇文章")
    return generated_files

if __name__ == "__main__":
    main()
