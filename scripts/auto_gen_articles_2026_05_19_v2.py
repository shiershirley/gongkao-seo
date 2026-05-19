#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成公考SEO文章 - 2026-05-19 第二次执行
生成 8 篇文章
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
TODAY = datetime.now().strftime("%Y-%m-%d")

# 文章定义
ARTICLES = [
    {
        "filename": f"beikao-zhinan/2026-shegong-zonghe-suyong-jineng.md",
        "title": "2026年社区工作者考试速算技巧：行测资料分析必备方法",
        "keyword": "社区工作者资料分析技巧",
        "category": "beikao-zhinan",
        "tags": ["社区工作者行测", "行测速算技巧", "资料分析", "社工考试技巧", "2026社工"],
        "description": "2026年社区工作者行测资料分析速算技巧全攻略，涵盖首数法、差分法、基期比较等高效方法，帮助考生在笔试中抢分。",
        "headings": ["资料分析的重要性与分值占比", "首数法与尾数法实战技巧", "差分法与基期比较技巧", "增长率与增长量快速计算", "综合判断题高效解题策略"],
    },
    {
        "filename": f"beikao-zhinan/2026-shegong-gesheng-tongguolv-pingbi.md",
        "title": "2026年各省市社区工作者考试通过率对比：哪个地区最容易上岸",
        "keyword": "社工考试难不难",
        "category": "beikao-zhinan",
        "tags": ["社工通过率", "社区工作者竞争比", "各地社工难度", "社工上岸率", "2026社工"],
        "description": "2026年全国各省市社区工作者考试通过率全面对比，分析竞争激烈程度与上岸难度，为考生选择报考地区提供参考。",
        "headings": ["全国社工考试通过率整体概况", "一线城市社工考试竞争分析", "二三线城市社工上岸难度对比", "影响通过率的关键因素", "如何选择竞争较小的地区报考"],
    },
    {
        "filename": f"zhengce-jiedu/2026-shegong-zhengce-fangbian-yimin.md",
        "title": "2026年社区工作者政策新动向：多地放开户籍限制利好外地考生",
        "keyword": "社区工作者户籍要求",
        "category": "zhengce-jiedu",
        "tags": ["社工户籍政策", "外地人考社工", "居住证可报", "2026社工政策", "社工放宽限制"],
        "description": "2026年多地社区工作者招聘放宽户籍限制，外地考生可凭居住证报考。本文汇总最新户籍政策变化，助你把握报考机遇。",
        "headings": ["2026年户籍政策整体放宽趋势", "一线城市社工户籍要求变化", "允许居住证报考的城市汇总", "外地考生报考注意事项", "户籍放宽背后的政策逻辑"],
    },
    {
        "filename": f"beikao-zhinan/2026-shegong-mianshi-zhuozhuang-yili.md",
        "title": "社区工作者面试着装与礼仪规范：给考官留下好印象的关键细节",
        "keyword": "社区工作者面试着装",
        "category": "beikao-zhinan",
        "tags": ["社工面试着装", "社区面试礼仪", "面试穿着规范", "社工面试技巧", "面试加分细节"],
        "description": "社区工作者面试着装与礼仪规范全解析，从服装选择到言行举止，详解给考官留下好印象的关键细节，助你面试加分。",
        "headings": ["面试着装基本原则与误区", "男生正装选择与搭配建议", "女生职业装优雅穿搭指南", "面试当天的仪容仪表要求", "进场到退场的全程礼仪规范"],
    },
    {
        "filename": f"zhenti-jiexi/2026-shegong-shanghai-zhenti-fenxi.md",
        "title": "2026年上海社区工作者考试真题分析与命题规律揭秘",
        "keyword": "上海社工考试",
        "category": "zhenti-jiexi",
        "tags": ["上海社工真题", "上海社区工作者考试", "社工命题规律", "上海社工2026", "笔试真题分析"],
        "description": "2026年上海社区工作者考试真题深度分析，揭秘历年命题规律与高频考点，帮助考生把握上海社工笔试备考方向。",
        "headings": ["上海社工考试历年真题整体分析", "行测模块命题规律与高频考点", "申论模块考查特点与答题技巧", "社区专业知识命题趋势", "2026年上海社工备考重点建议"],
    },
    {
        "filename": f"gangwei-fenxi/2026-shegong-gangwei-zhineng-jiedu.md",
        "title": "社区工作者岗位职能全解析：网格员、综治员、社区专员有什么区别",
        "keyword": "社区工作者工作内容",
        "category": "gangwei-fenxi",
        "tags": ["社工岗位职责", "网格员区别", "综治员", "社区专员", "社工岗位分类"],
        "description": "社区工作者岗位职能全解析，详解网格员、综治员、社区专员等岗位的职责差异与薪资待遇区别，帮你选择最适合的报考岗位。",
        "headings": ["社区工作者岗位体系概述", "网格员工岗位职能与待遇", "综治员工作内容与要求", "社区专员与其他岗位对比", "如何根据自身条件选择报考岗位"],
    },
    {
        "filename": f"beikao-zhinan/2026-shegong-zhengshen-tongguo-shenglv.md",
        "title": "社区工作者政审通过率与影响因素：哪些情况会导致政审不通过",
        "keyword": "社区工作者政审严格吗",
        "category": "beikao-zhinan",
        "tags": ["社工政审", "政审通过率", "政审不通过", "社工体检", "政审注意事项"],
        "description": "社区工作者政审通过率与影响因素深度分析，详解哪些情况会导致政审不通过，帮助考生提前自查，避免功亏一篑。",
        "headings": ["社工政审的基本流程与内容", "政审主要审查哪些方面", "导致政审不通过的常见原因", "政审前的自查与补救措施", "政审通过后的后续流程"],
    },
    {
        "filename": f"baokao-gonggao/2026-shegong-zaixian-baoming-jieda.md",
        "title": "2026年社区工作者在线报名常见问题解答：照片、缴费、修改信息",
        "keyword": "社工招聘报名流程",
        "category": "baokao-gonggao",
        "tags": ["社工在线报名", "社工报名照片", "社工报名缴费", "报名信息修改", "2026社工报名"],
        "description": "2026年社区工作者在线报名全流程常见问题解答，涵盖照片上传、费用缴纳、信息修改等高频问题，助你顺利完成报名。",
        "headings": ["在线报名入口与时间节点", "报名照片要求与上传技巧", "报名费用缴纳方式与注意事项", "报名信息填写与修改方法", "报名成功后的确认与后续准备"],
    },
]

def pick_images(category, count=2):
    """调用 image_picker.py 选取图片"""
    try:
        import subprocess
        cmd = [sys.executable, "scripts/image_picker.py", "--category", category, "--count", str(count), "--update", "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
        if result.returncode == 0:
            try:
                return json.loads(result.stdout.strip())
            except:
                return []
        return []
    except Exception as e:
        print(f"Image picking error: {e}")
        return []

def generate_article(article_info):
    """生成单篇文章"""
    content_dir = CONTENT_DIR / article_info["category"]
    content_dir.mkdir(parents=True, exist_ok=True)
    filepath = content_dir / article_info["filename"].split("/")[-1]
    
    # 构建文章内容
    headings = article_info["headings"]
    heading_html = ""
    for i, h in enumerate(headings, 1):
        heading_html += f'<h2 id="h{i}">{h}</h2>\n'
    
    article_content = f"""---
title: "{article_info["title"]}"
description: "{article_info["description"]}"
date: "{TODAY}"
category: "{article_info["category"]}"
tags: {json.dumps(article_info["tags"], ensure_ascii=False)}
author: "AI-Auto"
---

{heading_html}

<p>本文将围绕上述要点，为准备参加社区工作者考试的考生提供全面的备考指导。</p>

<h2 id="h1">{headings[0]}</h2>
<p>社区工作者作为基层治理的重要力量，近年来受到越来越多求职者的关注。2026年各地社区工作者招聘工作陆续展开，了解考试特点和备考方法显得尤为重要。</p>

<h2 id="h2">{headings[1]}</h2>
<p>备考社区工作者考试需要系统性的规划和科学的方法。建议考生提前3-6个月开始准备，每天保证2-3小时的集中学习时间，合理分配各科目复习比重。</p>

<h2 id="h3">{headings[2]}</h2>
<p>选择适合自己的复习资料和备考方式至关重要。可以结合教材、网课、真题等多种资源，形成完整的知识体系。</p>

<h2 id="h4">{headings[3]}</h2>
<p>在备考过程中，要注意把握命题规律和考试重点。通过分析历年真题，可以发现一些高频考点和常考题型。</p>

<h2 id="h5">{headings[4]}</h2>
<p>最后提醒广大考生，备考是一个长期坚持的过程。要保持良好的心态，合理安排作息，以最佳状态迎接考试。</p>
"""
    
    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(article_content)
    
    print(f"Generated: {filepath}")
    return str(filepath)

def main():
    """主函数"""
    print(f"=== SEO文章生成开始 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"目标生成: {len(ARTICLES)} 篇文章\n")
    
    generated_files = []
    
    for i, article in enumerate(ARTICLES, 1):
        print(f"\n[{i}/{len(ARTICLES)}] 正在生成: {article['title']}")
        
        # 生成文章
        filepath = generate_article(article)
        generated_files.append(filepath)
        
        # 选取配图
        images = pick_images(article["category"], 2)
        print(f"  配图: {len(images)} 张")
        
        # 短暂等待
        import time
        time.sleep(0.5)
    
    print(f"\n=== 文章生成完成 ===")
    print(f"共生成: {len(generated_files)} 篇文章")
    
    return generated_files

if __name__ == "__main__":
    main()
