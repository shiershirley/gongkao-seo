#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文章生成器 - 为未覆盖关键词生成文章
"""

import os
import re
from pathlib import Path
from datetime import datetime
import random

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
KEYWORD_POOL_FILE = PROJECT_ROOT / "scripts" / "keywords_pool.md"

# 文章模板
ARTICLE_TEMPLATE = """---
title: "{title}"
date: "{date}"
category: "{category}"
tags: {tags}
author: "公考SEO"
description: "{description}"
---

# {title}

## 概述

{keyword}是许多考生关注的热点问题。本文将详细解答这个问题，帮助考生更好地了解社区工作者考试相关信息。

## 详细内容

### 基本信息

{content_section1}

### 重要注意事项

{content_section2}

### 常见问题解答

**Q1：{question1}**
A：{answer1}

**Q2：{question2}**
A：{answer2}

**Q3：{question3}**
A：{answer3}

## 总结

以上就是关于{keyword}的详细介绍。希望本文能帮助考生更好地了解相关信息，顺利通过考试。

---

*本文仅供参考，具体信息以官方公告为准。*
"""

def load_uncovered_keywords():
    """加载未覆盖的关键词"""
    keywords = []
    
    if not KEYWORD_POOL_FILE.exists():
        return keywords
    
    with open(KEYWORD_POOL_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单的正则提取关键词
    pattern = r'- keyword:\s*(.+?)\s*\n\s*priority:\s*(\w+)\s*\n\s*type:\s*(\w+)\s*\n\s*covered:\s*(true|false)'
    
    for match in re.finditer(pattern, content):
        keyword = match.group(1).strip()
        priority = match.group(2).strip()
        kw_type = match.group(3).strip()
        covered = match.group(4).strip().lower() == 'true'
        
        if not covered:
            keywords.append({
                'keyword': keyword,
                'priority': priority,
                'type': kw_type,
                'category': suggest_category(keyword)
            })
    
    return keywords

def suggest_category(keyword):
    """根据关键词推断分类"""
    keyword_lower = keyword.lower()
    
    if any(w in keyword for w in ['上海', '社工', '社区工作者']):
        return 'shanghai-shegong'
    elif any(w in keyword for w in ['国考', '公务员']):
        return 'guokao'
    elif any(w in keyword for w in ['省考', '事业单位']):
        return 'shengkao'
    elif any(w in keyword for w in ['备考', '复习', '技巧']):
        return 'beikao-zhinan'
    elif any(w in keyword for w in ['岗位', '职位']):
        return 'gangwei-fenxi'
    elif any(w in keyword for w in ['招聘', '公告', '报名']):
        return 'baokao-gonggao'
    elif any(w in keyword for w in ['真题', '解析']):
        return 'zhenti-jiexi'
    else:
        return 'beikao-zhinan'

def generate_article_content(keyword_info):
    """生成文章内容"""
    keyword = keyword_info['keyword']
    category = keyword_info['category']
    
    # 生成标题
    title = f"{keyword}2026年最新详情"
    if len(title) > 25:
        title = f"{keyword}详解"
    
    # 生成描述
    description = f"本文详细介绍{keyword}的相关信息，包括报名条件、考试内容、薪资待遇等，帮助考生全面了解。"
    
    # 生成标签
    tags = [keyword, keyword[:4], "社区工作者", "2026年"]
    
    # 生成内容章节
    content_section1 = f"{keyword}是社区工作者考试中的重要内容。根据往年经验，考生需要重点关注以下几个方面：\n\n1. 政策变化：2026年相关政策有所调整，考生需及时关注。\n2. 考试内容：主要包括综合能力测试和专业知识。\n3. 报名条件：各地略有不同，需仔细阅读公告。"
    
    content_section2 = f"在准备{keyword}相关考试时，考生需要注意以下几点：\n\n1. 时间安排：合理规划复习时间，避免临时抱佛脚。\n2. 资料选择：选择权威的教材和辅导资料。\n3. 模拟练习：多做真题和模拟题，熟悉考试形式。"
    
    # 生成问题
    question1 = f"{keyword}的报名条件是什么？"
    answer1 = f"{keyword}的报名条件因地区而异，一般要求大专及以上学历，年龄在18-35周岁之间，部分岗位有专业限制。"
    
    question2 = f"{keyword}的考试内容有哪些？"
    answer2 = f"{keyword}的考试内容包括综合基础知识、社区工作专业知识和行政职业能力测试三个部分。"
    
    question3 = f"{keyword}的薪资待遇如何？"
    answer3 = f"{keyword}的薪资待遇因地区而异，一般包括基本工资、绩效奖金和年终奖，综合月薪在5000-8000元之间。"
    
    # 组合文章
    article = ARTICLE_TEMPLATE.format(
        title=title,
        date=datetime.now().strftime('%Y-%m-%d'),
        category=category,
        tags=str(tags),
        description=description,
        keyword=keyword,
        content_section1=content_section1,
        content_section2=content_section2,
        question1=question1,
        answer1=answer1,
        question2=question2,
        answer2=answer2,
        question3=question3,
        answer3=answer3
    )
    
    return article

def generate_articles(num_articles=100):
    """生成指定数量的文章"""
    # 加载未覆盖关键词
    uncovered_keywords = load_uncovered_keywords()
    
    if not uncovered_keywords:
        print("所有关键词都已覆盖！")
        return
    
    print(f"找到 {len(uncovered_keywords)} 个未覆盖关键词")
    
    # 如果未覆盖关键词不足，则重复使用并添加角度
    articles_to_generate = []
    
    while len(articles_to_generate) < num_articles:
        for kw_info in uncovered_keywords:
            if len(articles_to_generate) >= num_articles:
                break
            
            # 添加角度变体
            angle = random.choice(['最新详情', '全面解析', '报考指南', '备考攻略'])
            article_info = {
                'keyword_info': kw_info,
                'angle': angle
            }
            articles_to_generate.append(article_info)
    
    # 生成文章
    generated_count = 0
    
    for article_info in articles_to_generate[:num_articles]:
        kw_info = article_info['keyword_info']
        angle = article_info['angle']
        
        # 生成文章内容
        article_content = generate_article_content(kw_info)
        
        # 修改标题以包含角度
        article_content = article_content.replace(
            f"{kw_info['keyword']}2026年最新详情",
            f"{kw_info['keyword']}{angle}"
        )
        
        # 确定文件路径
        category_dir = CONTENT_DIR / kw_info['category']
        category_dir.mkdir(exist_ok=True, parents=True)
        
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{kw_info['keyword'][:20].replace(' ', '-')}-{angle[:4]}.md"
        filepath = category_dir / filename
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        generated_count += 1
        print(f"已生成 {generated_count}/{num_articles}：{filepath.name}")
    
    print(f"\n完成！共生成 {generated_count} 篇文章")

if __name__ == "__main__":
    import sys
    
    num_articles = 100
    if len(sys.argv) > 1:
        num_articles = int(sys.argv[1])
    
    print(f"开始生成 {num_articles} 篇文章...")
    generate_articles(num_articles)
