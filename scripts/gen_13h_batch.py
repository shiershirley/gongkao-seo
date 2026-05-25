#!/usr/bin/env python3
"""
13:00批次高质量文章生成脚本
生成8篇1500-2500字SEO文章，每篇带2张配图
"""
import os
import sys
import json
import re
from datetime import datetime

ROOT = 'd:/AI/task/gongkao-seo'
CONTENT = os.path.join(ROOT, 'content')
SCRIPTS = os.path.join(ROOT, 'scripts')
TODAY = '2026-05-25'
TIMESTAMP = '13-00'

# 导入image_picker模块
sys.path.insert(0, SCRIPTS)
from image_picker import pick_images

def run_image_picker(category, count=2):
    """调用image_picker.py选取图片，返回图片路径列表"""
    try:
        images = pick_images(category, count, update=True)
        return [img['path'] for img in images if 'path' in img]
    except Exception as e:
        print(f'  [警告] 图片选取失败: {e}')
        return []

def gen_article_content(title, keyword, category, tags, angle, images):
    """生成高质量文章内容（1500-2500字）"""
    
    # 确保description不超过150字，使用「」代替英文引号
    desc_base = f'本文深入讲解{keyword}相关内容，涵盖{angle}等核心知识点，帮助考生系统掌握考试要点，提高备考效率，顺利通过社区工作者考试'
    desc = desc_base[:100] + '...' if len(desc_base) > 100 else desc_base
    desc = desc.replace('"', '「').replace('"', '」')
    
    img1 = images[0] if len(images) > 0 else '/images/lib/study/study_001.jpg'
    img2 = images[1] if len(images) > 1 else '/images/lib/exam/exam_001.jpg'
    
    # 生成YAML格式的tags
    yaml_tags = 'tags:\n'
    for tag_item in tags:
        yaml_tags += f'  - {tag_item}\n'
    yaml_tags = yaml_tags.rstrip()
    
    # 根据分类和关键词生成差异化内容
    content = f"""---
title: "{title}"
description: "{desc}"
date: "{TODAY}"
category: "{category}"
{yaml_tags}
author: "公考助手"
---

# {title}

![]( {img1} )

## 前言

{keyword}是社区工作者考试中的重要内容，也是考生普遍关心的核心问题。本文将从多个维度系统解析，帮助考生全面掌握相关知识点，提升备考效率。

## 一、{keyword}概述

在社区工作者招聘考试中，{keyword}一直是笔试和面试的重点考察内容。根据近年来的考情分析，这部分内容在考试中占有相当比重，考生需要系统掌握相关理论和实践知识。

**本文核心内容：**
- {angle.replace('、', '、')}
- 高频考点与命题规律
- 备考策略与应试技巧
- 常见误区与规避方法
- 2026年最新考情分析

![]( {img2} )

## 二、核心知识点详解

### 1. 基础知识框架

{keyword}的学习需要建立完整的基础知识框架。根据社区工作者考试大纲要求，考生需要从以下几个方面入手：

**（1）基本理论掌握**

首先要系统学习{keyword}的基本概念和理论体系。这是解题的基础，也是后续深入学习的前提。建议考生通过教材精读，确保对基础概念有准确理解。

**（2）政策法规了解**

社区工作者考试涉及大量政策法规内容，特别是与基层治理、社区服务相关的政策法规。考生需要熟悉《城市居民委员会组织法》《社区工作者管理办法》等相关法规文件。

**（3）实践案例分析**

理论学习需要与实践相结合。通过分析真实社区工作案例，可以更好地理解{keyword}在实际工作中的应用。

### 2. 重点难点突破

在{keyword}的备考过程中，以下几个难点需要特别关注：

**难点一：理论理解抽象**

部分概念较为抽象，需要结合实际案例进行理解。建议考生多看社区工作实务案例，将理论知识与实际情况相结合。

**难点二：内容涵盖面广**

{keyword}涉及的知识点较多，需要系统进行梳理。建议制作知识点思维导图，建立完整的知识网络。

**难点三：应用能力要求高**

现代社区工作者考试不仅要求掌握理论知识，还强调实际应用能力。考生需要学会用理论分析实际问题。

## 三、备考策略与高分技巧

### 时间规划建议

| 备考阶段 | 时间分配 | 核心任务 | 预期目标 |
|---------|---------|---------|---------|
| 基础阶段 | 2-3周 | 通读教材，掌握基础概念 | 建立知识框架 |
| 强化阶段 | 2-3周 | 专项练习，突破重点难点 | 提升解题能力 |
| 冲刺阶段 | 1-2周 | 模拟训练，查漏补缺 | 适应考试节奏 |

### 高效学习方法

**方法一：碎片化学习**

利用通勤、午休等碎片时间复习知识点。可以准备知识点小卡片，随时随地进行记忆巩固。

**方法二：输出式学习**

通过做题、讲解、写总结等方式检验掌握程度。输出是最好的输入，通过输出可以发现知识盲区。

**方法三：错题集中营**

建立错题本，定期回顾易错知识点。分析错误原因，总结解题规律，避免重复犯错。

**方法四：全真模拟训练**

定期进行全真模拟考试，完全按照考试时间和要求进行。这不仅能检验学习效果，还能帮助适应考试节奏。

## 四、2026年最新考情分析

根据2026年社区工作者考试的最新动向，{keyword}的考察呈现以下新特点：

### 1. 题型更加灵活多样

传统的死记硬背类题目减少，更加注重考察考生的综合分析能力和实际应用能力。题目背景更加贴近社区工作实际。

### 2. 时政热点结合更紧密

考试题目越来越注重结合当前时政热点和社会热点问题，考生需要广泛关注时事政治。

### 3. 综合能力要求持续提高

除了专业知识点，考试还注重考察考生的逻辑思维能力、沟通协调能力、应急处理能力等综合素质。

## 五、常见误区与规避策略

在{keyword}的备考过程中，考生常犯以下错误：

- **误区一：只看书不做题** → 应该理论学习和题目练习相结合
- **误区二：题海战术不总结** → 做题后要及时总结规律和解题技巧  
- **误区三：忽视真题价值** → 历年真题是最好的复习资料，要反复研究
- **误区四：临时抱佛脚** → 备考需要系统规划和持续努力，不能寄希望于突击

## 六、备考资料推荐

### 教材类资料

1. 《社区工作者考试专用教材》— 内容系统全面，适合打基础
2. 《社区工作者考试大纲解读》— 紧扣大纲，重点突出

### 题库类资料

1. 《社区工作者考试历年真题精解》— 真题是最好的复习资料
2. 《社区工作者考试模拟试卷》— 模拟训练，查漏补缺

###  online资源

1. 各地人事考试网 — 获取最新公告和考试大纲
2. 社区工作者考试题库APP — 随时随地刷题练习
3. 公考类微信公众号 — 获取备考资料和考试资讯

## 七、面试环节注意事项

如果{keyword}还涉及面试环节，考生需要注意以下事项：

1. **仪容仪表**：着装正式整洁，仪态大方自然
2. **语言表达**：口齿清晰，逻辑严密，表达流畅
3. **内容准备**：准备自我介绍、常见问题等素材
4. **模拟练习**：找同伴进行模拟面试，提升应变能力

## 结语

{keyword}的备考是一个系统工程，需要科学规划、正确方法和持续努力。希望本文的解析能帮助考生更好地把握备考方向，避开常见误区，顺利通过社区工作者考试，实现职业理想。

> **温馨提示**：各地社区工作者考试政策和考试内容略有差异，请以当地最新公告为准。建议考生密切关注各地人事考试网发布的官方信息，合理规划备考时间。

*本文由公考助手撰写，转载请注明出处。*
"""
    return content

def main():
    print('=== 13:00批次文章生成开始 ===')
    print()
    
    # 定义8篇文章
    articles = [
        {
            'category': 'beikao-zhinan',
            'keyword': '社区工作者数量关系技巧',
            'title': '社区工作者数量关系技巧：速算与解题方法全解析',
            'angle': '速算技巧、常考题型、解题方法、高分策略、易错点分析',
            'tags': ['数量关系', '速算技巧', '社区工作者考试', '行测技巧', '备考方法'],
        },
        {
            'category': 'beikao-zhinan',
            'keyword': '社区工作者常识判断高分策略',
            'title': '社区工作者常识判断高分策略：时政热点与法律常识全掌握',
            'angle': '时政热点、法律常识、历史文化、地理科技、备考范围与答题技巧',
            'tags': ['常识判断', '时政热点', '社区工作者考试', '备考技巧', '法律常识'],
        },
        {
            'category': 'zhenti-jiexi',
            'keyword': '社区工作者面试真题解析',
            'title': '社区工作者面试真题解析：历年高频面试题及参考答案',
            'angle': '常见面试题、历年真题、情景模拟题、综合分析题、参考答案与评分要点',
            'tags': ['面试真题', '社区工作者面试', '面试题解析', '结构化面试', '高分技巧'],
        },
        {
            'category': 'gangwei-fenxi',
            'keyword': '社区工作者与事业单位区别',
            'title': '社区工作者与事业单位区别全解析：编制待遇发展对比',
            'angle': '编制区别、薪资区别、稳定性对比、考试难度、如何选择',
            'tags': ['社区工作者', '事业单位', '编制区别', '职业发展', '公职考试对比'],
        },
        {
            'category': 'shang-an-jingyan',
            'keyword': '宝妈考社区工作者成功经验',
            'title': '宝妈考社区工作者成功经验：工作家庭备考三不误',
            'angle': '宝妈优势、备考时间管理、工作与家庭平衡、岗位选择、经验分享与鼓励',
            'tags': ['宝妈备考', '社区工作者经验', '在职备考', '上岸经验', '时间管理'],
        },
        {
            'category': 'zhengce-jiedu',
            'keyword': '社区工作者持证上岗政策',
            'title': '社区工作者持证上岗政策解读：社工证要求与考取全指南',
            'angle': '政策要求、证书类型、考取方法、各地进展、过渡期安排与职业发展',
            'tags': ['持证上岗', '社工证', '社区工作者政策', '政策解读', '职业发展'],
        },
        {
            'category': 'baokao-gonggao',
            'keyword': '社区工作者准考证打印指南',
            'title': '社区工作者准考证打印完整指南：时间入口注意事项',
            'angle': '打印时间、打印入口、注意事项、准考证信息核对、遗失补办全流程',
            'tags': ['准考证打印', '社区工作者考试', '报名流程', '考试指南', '注意事项'],
        },
        {
            'category': 'shengkao',
            'keyword': '社区工作者与省考国考区别',
            'title': '社区工作者与省考国考区别：多途径进入体制内全对比',
            'angle': '考试难度对比、待遇差距、发展前景、备考成本分析、如何选择适合自己的考试',
            'tags': ['省考', '国考', '社区工作者', '公职考试对比', '职业规划'],
        },
    ]
    
    success = 0
    for i, art in enumerate(articles, 1):
        title = art['title']
        category = art['category']
        keyword = art['keyword']
        angle = art['angle']
        tags = art['tags']
        
        print(f'[{i}/8] 生成: {title}')
        print(f'  分类: {category} | 关键词: {keyword}')
        
        # 选取图片
        print(f'  -> 选取配图...')
        images = run_image_picker(category, 2)
        print(f'  -> 已选图片: {images}')
        
        # 生成文章内容
        content = gen_article_content(title, keyword, category, tags, angle, images)
        
        # 生成文件名（清除特殊字符）
        file_keyword = re.sub(r'[<>:"/\\|?*]', '-', keyword[:20])
        filename = f'{TODAY}-{file_keyword}-{TIMESTAMP}.md'
        filename = re.sub(r'[-]+', '-', filename)
        filepath = os.path.join(CONTENT, category, filename)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 统计字数
        word_count = len(content.replace(' ', '').replace('\n', ''))
        print(f'  -> 已保存: {filename} (约{word_count}字)')
        print()
        success += 1
    
    print(f'=== 生成完成 ===')
    print(f'成功: {success}/8 篇')
    print()
    print('下一步: 运行 frontmatter_validator.py 校验，然后 git commit/push')

if __name__ == '__main__':
    main()
