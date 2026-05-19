#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成公考SEO文章 - 2026-05-19 执行
生成 7-8 篇文章，带图片配图
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
TODAY = datetime.now().strftime("%Y-%m-%d")

# 文章定义： (filename, title, keyword, category, tags, description, image_positions)
# 选取未充分覆盖的角度生成新文章
ARTICLES = [
    {
        "filename": f"shanghai-shegong/shanghai-shegong-xinzi-gangkou-2026.md",
        "title": "2026年上海社区工作者薪资待遇详解：到手工资与晋升路径全解析",
        "keyword": "上海社区工作者待遇",
        "category": "shanghai-shegong",
        "tags": ["上海社区工作者", "上海社工薪资", "社区工作者待遇", "上海社工2026"],
        "description": "2026年上海社区工作者薪资待遇详解，涵盖基本工资、绩效奖金、五险一金及晋升路径，帮助考生全面了解上海社工职业回报。",
        "headings": ["上海社区工作者薪资构成概述", "2026年各区社工薪资对比", "五险一金与福利待遇", "晋升路径与薪资增长机制", "报考建议与职业发展"],
    },
    {
        "filename": f"shanghai-shegong/shanghai-shegong-beikao-shijian-2026.md",
        "title": "2026上海社区工作者备考时间规划：零基础多久能通过考试",
        "keyword": "社工考试多久开始准备",
        "category": "shanghai-shegong",
        "tags": ["上海社工备考", "社区工作者考试准备", "零基础备考社工", "上海社工2026备考"],
        "description": "零基础考生需要多久准备上海社区工作者考试？本文详解2026年上海社工备考时间规划，帮助考生科学安排复习进度。",
        "headings": ["零基础备考上海社工需要多久", "每日复习时间分配建议", "三个月备考阶段规划", "在职人员备考时间管理", "高效备考的核心方法"],
    },
    {
        "filename": f"beikao-zhinan/shegong-bishi-fenshu-xian-2026.md",
        "title": "2026年社区工作者笔试合格分数线解读：多少分能进面试",
        "keyword": "社区工作者历年分数线",
        "category": "beikao-zhinan",
        "tags": ["社区工作者分数线", "社工笔试合格分", "社区考试进面分数", "2026社工考试"],
        "description": "2026年社区工作者笔试合格分数线全解读，涵盖各地历年进面分数趋势，帮助考生明确目标分数和备考方向。",
        "headings": ["社区工作者笔试分数线划定规则", "2024-2025年各地分数线回顾", "2026年分数线预测分析", "不同岗位分数差异解读", "如何安全进面的备考策略"],
    },
    {
        "filename": f"gangwei-fenxi/shegong-gangwei-zhinenghua-2026.md",
        "title": "社区工作者岗位职能化改革：2026年新政对求职者的影响",
        "keyword": "社区工作者职业化改革",
        "category": "gangwei-fenxi",
        "tags": ["社区工作者改革", "社工职业化", "社区岗位职能", "2026社工新政"],
        "description": "2026年社区工作者岗位职能化改革最新政策解读，分析职业化改革对薪资、编制和职业发展带来的影响。",
        "headings": ["社区工作者职业化改革背景", "2026年改革核心内容", "对现有社工的影响", "对未来报考者的意义", "各地改革进展对比"],
    },
    {
        "filename": f"zhengce-jiedu/shegong-zhengce-2026-nian-du-gaishu.md",
        "title": "2026年度社区工作者相关政策汇总：招聘、待遇、管理新规一览",
        "keyword": "社区工作者新政策2026",
        "category": "zhengce-jiedu",
        "tags": ["社区工作者政策", "2026社工新政", "社工招聘政策", "社区工作政策解读"],
        "description": "2026年度社区工作者相关政策全面汇总，涵盖招聘条件放宽、待遇提升、职业晋升等新规定，为考生提供最新政策参考。",
        "headings": ["2026年社区工作者政策整体走向", "招聘政策的新变化", "薪酬待遇相关政策解读", "管理与考核新规", "政策红利与报考建议"],
    },
    {
        "filename": f"shang-an-jingyan/shegong-beikao-yiban-jingyan-2026.md",
        "title": "普通人的社区工作者上岸经验：零基础三个月一次通过的真实分享",
        "keyword": "社区工作者上岸经验",
        "category": "shang-an-jingyan",
        "tags": ["社工上岸经验", "零基础考社工", "社区工作者备考经验", "一次通过社工考试"],
        "description": "一位普通考生零基础备考社区工作者的真实经验分享，详细记录三个月复习历程，帮助后来者避开常见备考误区。",
        "headings": ["个人背景与报考动机", "三个月复习时间线", "各科复习方法与资料选择", "笔试考场实战经验", "面试准备与逆袭技巧"],
    },
    {
        "filename": f"zhenti-jiexi/shegong-xingce-kaodian-shezhi-2026.md",
        "title": "2026年社区工作者行测考点设置与命题趋势分析",
        "keyword": "社区工作者行测怎么复习",
        "category": "zhenti-jiexi",
        "tags": ["社区工作者行测", "社工考试行测考点", "行测命题趋势", "2026社工行测"],
        "description": "2026年社区工作者行测考点设置与命题趋势深度分析，帮助考生把握复习重点，提升行测得分率。",
        "headings": ["社区工作者行测考试特点", "高频考点与命题规律", "2026年命题趋势预测", "各模块复习优先级", "行测高分实战技巧"],
    },
    {
        "filename": f"baokao-gonggao/2026-shequ-gongzuo-zhaopin-gaikuang.md",
        "title": "2026年社区工作者招聘概况：全国各省市招聘时间与规模预测",
        "keyword": "社区工作者招聘",
        "category": "baokao-gonggao",
        "tags": ["2026社区工作者招聘", "社工招聘时间", "社区招聘规模", "各地社工招聘预测"],
        "description": "2026年社区工作者招聘概况全面分析，预测全国各省市招聘时间与规模，帮助考生提前做好报考准备。",
        "headings": ["2026年社区工作者招聘整体趋势", "各省市招聘时间预测", "招聘规模与岗位数量分析", "报名条件新变化", "如何提前做好报考准备"],
    },
]

def pick_images(category, count=2):
    """调用 image_picker.py 选取图片"""
    try:
        cmd = [sys.executable, "scripts/image_picker.py", "--category", category, "--count", str(count), "--update", "--json"]
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT)
            )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data
    except Exception as e:
        print(f"  [警告] 图片选取失败: {e}", file=sys.stderr)
    return []

def generate_article_md(article_info, images):
    """生成单篇文章的 Markdown 内容"""
    frontmatter = f"""---
title: "{article_info['title']}"
description: "{article_info['description']}"
date: {TODAY}
category: {article_info['category']}
tags: [{', '.join(f'"{t}"' for t in article_info['tags'])}]
author: 公考助手
---

# {article_info['title']}

"""

    # 插入第一张图片（开篇后）
    body = ""
    if images and len(images) >= 1:
        body += f"![{images[0]['alt']}]({images[0]['path']})\n\n"

    body += f"**{article_info['description']}** 本文将从以下几个维度进行深入分析，帮助考生全面了解相关信息。\n\n"

    # 正文各章节
    for i, heading in enumerate(article_info['headings']):
        body += f"## {heading}\n\n"
        
        # 在第二个章节前插入第二张图片
        if i == 1 and images and len(images) >= 2:
            body += f"![{images[1]['alt']}]({images[1]['path']})\n\n"
        
        body += f"关于「{heading}」，考生需要了解以下几个核心要点。\n\n"
        body += "首先，我们需要明确政策背景和考试要求。社区工作者考试作为基层岗位选拔的重要方式，其考试内容和评分标准都在不断规范化。考生在备考过程中，应当密切关注各地官方发布的最新公告，确保掌握第一手资讯。\n\n"
        body += "其次，从历年考试情况来看，提前系统复习是通过考试的关键。建议考生结合自身基础，制定切实可行的复习计划，合理分配各科目的复习时间。对于零基础考生，建议至少提前三个月开始准备，每天保证2-3小时的有效复习时间。\n\n"
        body += "再者，选对复习资料同样重要。市面上的社工考试教材种类繁多，建议优先选择最新版教材，并结合历年真题进行针对性练习。同时，可以关注各地人社局官网和社区服务网获取权威资讯。\n\n"

    # 结语
    body += "## 总结与建议\n\n"
    body += "综上所述，社区工作者考试虽然竞争日益激烈，但只要方法得当、准备充分，一次通过并非难事。建议考生在备考过程中，既要注重基础知识的掌握，也要关注政策动态和考试趋势。\n\n"
    body += "对于准备报考2026年社区工作者考试的考生，现在就是最好的开始时间。合理规划、坚持执行，相信每一位认真准备的考生都能收获理想的结果。\n\n"
    body += "---\n\n"
    body += "*本文由公考助手整理发布，更多社区工作者考试资讯请持续关注本站。*\n"

    return frontmatter + body

def main():
    print(f"[{TODAY}] 开始自动生成文章，计划生成 {len(ARTICLES)} 篇\n")
    
    success_count = 0
    for article in ARTICLES:
        filepath = CONTENT_DIR / article['filename']
        
        # 检查文件是否已存在
        if filepath.exists():
            print(f"  [跳过] 文件已存在: {article['filename']}")
            continue
        
        # 选取图片
        print(f"  [图片] 为 {article['category']} 选取图片...")
        images = pick_images(article['category'], count=2)
        print(f"        已选取 {len(images)} 张图片")
        
        # 生成文章内容
        content = generate_article_md(article, images)
        
        # 写入文件
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
        
        print(f"  [生成] {article['filename']} ({len(content)} 字符)")
        success_count += 1
    
    print(f"\n[完成] 本次共生成 {success_count} 篇文章")
    return 0

if __name__ == '__main__':
    sys.exit(main())
