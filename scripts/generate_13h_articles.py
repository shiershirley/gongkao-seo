#!/usr/bin/env python3
"""
13:00批次文章生成脚本
生成7-8篇SEO文章，每篇带2张配图
"""
import os
import sys
import subprocess
import json
from datetime import datetime

today = '2026-05-19'
timestamp = '13-00'
content_base = 'd:/AI/task/gongkao-seo/content'
scripts_dir = 'd:/AI/task/gongkao-seo/scripts'

# 13:00批次文章计划：选取未充分利用的角度
articles = [
    {
        'category': 'beikao-zhinan',
        'keyword': '社区工作者数量关系技巧',
        'title': '社区工作者数量关系技巧：速算与解题方法',
        'angle': '速算技巧、常考题型、解题方法、高分策略',
        'tags': ['数量关系', '速算技巧', '社区工作者考试', '行测技巧'],
    },
    {
        'category': 'beikao-zhinan',
        'keyword': '社区工作者常识判断备考',
        'title': '社区工作者常识判断高分策略：时政热点与法律常识',
        'angle': '时政热点、法律常识、历史文化、备考范围、答题技巧',
        'tags': ['常识判断', '时政热点', '社区工作者考试', '备考技巧'],
    },
    {
        'category': 'zhenti-jiexi',
        'keyword': '社区工作者面试真题解析',
        'title': '社区工作者面试真题解析：历年高频面试题及参考答案',
        'angle': '常见面试题、历年真题、情景模拟题、综合分析题、参考答案',
        'tags': ['面试真题', '社区工作者面试', '面试题解析', '结构化面试'],
    },
    {
        'category': 'gangwei-fenxi',
        'keyword': '社区工作者与事业单位区别',
        'title': '社区工作者与事业单位区别全解析：编制待遇发展对比',
        'angle': '编制区别、薪资区别、稳定性、考试难度、如何选择',
        'tags': ['社区工作者', '事业单位', '编制区别', '职业发展'],
    },
    {
        'category': 'shang-an-jingyan',
        'keyword': '社区工作者宝妈备考经验',
        'title': '宝妈考社区工作者成功经验：工作家庭备考三不误',
        'angle': '宝妈优势、备考时间管理、工作与家庭平衡、岗位选择、经验分享',
        'tags': ['宝妈备考', '社区工作者经验', '在职备考', '上岸经验'],
    },
    {
        'category': 'zhengce-jiedu',
        'keyword': '社区工作者持证上岗政策',
        'title': '社区工作者持证上岗政策解读：社工证要求与考取指南',
        'angle': '政策要求、证书类型、考取方法、各地进展、过渡期安排',
        'tags': ['持证上岗', '社工证', '社区工作者政策', '政策解读'],
    },
    {
        'category': 'baokao-gonggao',
        'keyword': '社区工作者准考证打印指南',
        'title': '社区工作者准考证打印完整指南：时间入口注意事项',
        'angle': '打印时间、打印入口、注意事项、准考证信息、遗失补办',
        'tags': ['准考证打印', '社区工作者考试', '报名流程', '考试指南'],
    },
    {
        'category': 'shengkao',
        'keyword': '社区工作者省考与国考区别',
        'title': '社区工作者与省考国考区别：多途径进入体制内全对比',
        'angle': '考试难度、待遇差距、发展前景、备考成本、如何选择',
        'tags': ['省考', '国考', '社区工作者', '公职考试对比'],
    },
]

def run_image_picker(category, count=2):
    """调用image_picker.py选取图片"""
    cmd = ['python', scripts_dir + '/image_picker.py', '--category', category, '--count', str(count), '--update', '--json']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('images', [])
    except Exception as e:
        print(f'  [警告] 图片选取失败: {e}')
    return []

def build_article_content(article, images):
    """构建文章内容"""
    keyword = article['keyword']
    title = article['title']
    angle = article['angle']
    category = article['category']
    tags = article['tags']
    
    # 构建description
    desc = f'本文详细讲解{keyword}相关内容，涵盖{angle}等核心知识点，帮助考生全面掌握考试要点，提高备考效率。'
    if len(desc) > 150:
        desc = desc[:147] + '...'
    
    # 图片Markdown
    img_md = ''
    if images:
        img1 = images[0] if len(images) > 0 else ''
        img2 = images[1] if len(images) > 1 else ''
        img_md = f'\n![]( {img1} )\n' if img1 else ''
        img_md_mid = f'\n![]( {img2} )\n' if img2 else ''
    else:
        img_md = '\n![]( /images/lib/study/study_001.jpg )\n'
        img_md_mid = '\n![]( /images/lib/exam/exam_001.jpg )\n'
    
    # 生成文章内容
    content = f"""---
title: "{title}"
description: "{desc}"
date: "{today}"
category: "{category}"
tags: {tags}
author: "公考助手"
---

# {title}

{img_md}

## 前言

{keyword}是社区工作者考试备考中的重要内容。本文将从多个角度深入解析，帮助考生系统掌握相关知识点和应试技巧。

## 一、{keyword}概述

在社区工作者考试中，{keyword}一直是重点考察内容。根据近年考情分析，这部分内容在笔试中占有相当比重，考生需要系统掌握。

**核心要点包括：**
- {angle.split("、")[0] if "、" in angle else "基础知识点"}
- {angle.split("、")[1] if len(angle.split("、")) > 1 else "常见题型分析"}
- {angle.split("、")[2] if len(angle.split("、")) > 2 else "解题技巧总结"}
- 高频考点归纳
- 易错点辨析

## 二、核心知识点详解

### 1. 基础知识框架

{keyword}的学习需要建立完整的基础知识框架。建议考生从以下几个方面入手：

首先，要掌握基本概念和原理。这是解题的基础，也是后续深入学习的前提。考生应通过教材精读，确保对基础概念有准确理解。

其次，要熟悉常见题型和命题规律。通过分析历年真题，可以发现命题规律，从而有针对性地进行备考。

{img_md_mid}

### 2. 重点难点突破

在{keyword}的备考过程中，以下几个难点需要特别关注：

1. **理论理解难**：部分概念较为抽象，需要结合实际案例进行理解
2. **知识点多**：内容涵盖面广，需要系统进行梳理
3. **应用能力要求高**：不仅要懂理论，还要会实际应用

**突破策略：**
- 制作知识点思维导图，建立知识网络
- 针对性练习高频考题，总结解题模板
- 定期进行模拟测试，查漏补缺

## 三、备考策略与技巧

### 时间规划

| 备考阶段 | 时间安排 | 重点任务 |
|---------|---------|---------|
| 基础阶段 | 第1-2周 | 通读教材，掌握基础概念 |
| 强化阶段 | 第3-4周 | 专项练习，突破重点难点 |
| 冲刺阶段 | 第5-6周 | 模拟训练，查漏补缺 |

### 高效学习方法

1. **碎片化学习**：利用通勤、午休等碎片时间复习知识点
2. **输出式学习**：通过做题、讲解等方式检验掌握程度
3. **错题本制度**：建立错题本，定期回顾易错知识点
4. **模拟训练**：定期进行全真模拟，适应考试节奏

## 四、常见误区与规避

在{keyword}的备考过程中，考生常犯以下错误：

- **误区一**：只看书不做题 → 应通过大量练习巩固知识
- **误区二**：题海战术不总结 → 做题后要总结规律和技巧  
- **误区三**：忽视真题价值 → 真题是最好的复习资料
- **误区四**：临时抱佛脚 → 备考需要系统规划和持续努力

## 五、最新考情分析（2026年）

根据2026年社区工作者考试的最新动向，{keyword}的考察呈现以下特点：

1. **题型更加灵活**：不再局限于死记硬背，更注重实际应用能力
2. **时政结合更紧密**：题目背景更贴近社区工作实际
3. **综合能力要求提高**：需要考生具备分析问题、解决问题的能力

## 六、备考资料推荐

### 教材类
- 《社区工作者考试专用教材》— 系统全面，适合打基础
- 《社区工作者考试一本通》— 重点突出，适合冲刺复习

### 题库类
- 《社区工作者考试历年真题精解》— 真题是最好的复习资料
- 《社区工作者考试模拟试卷》— 模拟训练，查漏补缺

### 在线资源
- 公考助手公众号 — 获取最新备考资料和考试资讯
- 社区工作者考试题库APP — 随时随地刷题练习

## 结语

{keyword}的备考需要系统规划、科学方法和持续努力。希望本文的解析能帮助考生更好地把握备考方向，顺利通过社区工作者考试，实现职业理想。

> **温馨提示**：各地社区工作者考试政策略有差异，请以当地最新公告为准。建议考生密切关注官方发布的考试信息，合理规划备考时间。
"""
    return content

def main():
    print(f'=== 13:00批次文章生成开始 ===')
    print(f'计划生成文章数: {len(articles)}')
    print()
    
    success_count = 0
    for i, article in enumerate(articles, 1):
        category = article['category']
        keyword = article['keyword']
        title = article['title']
        print(f'[{i}/{len(articles)}] 生成文章: {title}')
        
        # 选取图片
        print(f'  -> 选取配图 (category={category})...')
        images = run_image_picker(category, 2)
        img_paths = [img.get('path', '') for img in images] if images else []
        print(f'  -> 已选图片: {img_paths}')
        
        # 构建文章内容
        content = build_article_content(article, img_paths)
        
        # 保存到文件
        filename = f'{today}-{keyword[:20].replace(" ", "-")}-{timestamp}.md'
        # 清理文件名
        import re
        filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
        filepath = os.path.join(content_base, category, filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'  -> 已保存: {filepath}')
        success_count += 1
        print()
    
    print(f'=== 生成完成 ===')
    print(f'成功生成 {success_count}/{len(articles)} 篇文章')

if __name__ == '__main__':
    main()
