#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公考SEO文章自动生成脚本 v3
- 按内容比例生成文章（社工2、国考2、省考2、事业单位1、通用1）
- 集成内链网络：自动为每篇文章添加2-3个相关阅读链接
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import re
import random

ROOT = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "content"

# 导入内链模块
sys.path.insert(0, str(Path(__file__).parent))
try:
    from internal_linker import build_article_index, find_related_articles, generate_related_links_section
    INTERNAL_LINK_ENABLED = True
except ImportError:
    print("警告：无法导入 internal_linker 模块，内链功能将禁用")
    INTERNAL_LINK_ENABLED = False

# ========== CTR标题生成函数 ==========
def generate_ctr_title(article_info):
    """
    生成高点击率标题，使用4种公式：
    1. 数字+痛点："2026国考分数线：这3个省分数暴涨"
    2. 疑问+解决方案："国考面试怎么准备？这份7天冲刺计划帮你"
    3. 对比+数据："省考vs国考：同样努力，为什么省考上岸率高30%？"
    4. 时效性+紧迫感："紧急通知：2026上海社工报名明天截止"
    """
    title = article_info.get("title", "")
    category = article_info.get("category", "")
    tags = article_info.get("tags", [])
    article_type = article_info.get("type", "info")
    
    # 提取核心关键词
    keywords = tags + [category.replace("-", "")]
    main_keyword = keywords[0] if keywords else "公考"
    
    # 数字池
    numbers = ["3", "5", "7", "10", "30%", "50%", "100+", "2倍"]
    # 情绪词池
    emotion_words = ["暴涨", "暴跌", "秘诀", "揭秘", "必看", "紧急", "重磅", "直呼没想到", 
                     "完蛋了", "稳了", "太简单了", "原来如此", "震惊"]
    # 疑问词池
    question_words = ["怎么", "为什么", "如何", "哪些", "什么时候", "哪里", "多少", "真的吗"]
    
    # 随机选择标题公式
    formula = random.choice([1, 2, 3, 4])
    
    if formula == 1:  # 数字+痛点
        num = random.choice(numbers)
        emotion = random.choice(emotion_words)
        return f"{title}：这{num}个{main_keyword}要点{emotion}"
    
    elif formula == 2:  # 疑问+解决方案
        q_word = random.choice(question_words)
        solutions = ["这份攻略", "这个秘诀", "这篇指南", "这个方法", "这份计划"]
        solution = random.choice(solutions)
        return f"{main_keyword}{q_word}{title.split('怎么')[-1] if '怎么' in title else '备考'}？{solution}帮你上岸"
    
    elif formula == 3:  # 对比+数据
        comparisons = {
            "guokao": ("省考", "竞争小3倍"),
            "shengkao": ("国考", "上岸率高30%"),
            "shanghai-shegong": ("国考", "压力小5倍"),
            "gangwei-fenxi": ("公务员", "待遇更稳定"),
            "beikao-zhinan": ("裸考", "通过率高2倍"),
        }
        if category in comparisons:
            comp, data = comparisons[category]
            return f"{main_keyword} vs {comp}：同样努力，为什么{main_keyword}{data}？"
        return f"{title}：为什么有人轻松上岸，有人却失败？"
    
    else:  # 时效性+紧迫感
        urgency_words = ["紧急通知", "最后3天", "明天截止", "马上开始", "最新消息", "刚刚发布"]
        urgency = random.choice(urgency_words)
        return f"{urgency}：{title}，考生必看！"
    
    return title  # 默认返回原标题


# ========== FAQ生成函数 ==========
def extract_faq_from_content(content, max_faq=5):
    """
    从文章正文中提取FAQ（常见问题）
    根据标题、小标题、关键词生成FAQ
    """
    faq_list = []
    lines = content.split('\n')
    
    # 从文章中提取可能的问题（包含问号、是/否、如何等关键词的句子）
    question_indicators = ['？', '吗', '如何', '怎么', '为什么', '哪些', '什么', '多少']
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检测是否为标题（## 或 ### 开头）
        if line.startswith('##') or line.startswith('###'):
            # 将标题转换为问题
            heading = re.sub(r'^#+\s*', '', line).strip()
            if heading and 'FAQ' not in heading and '相关阅读' not in heading:
                question = heading + '？'
                answer = f"关于{heading}的详细解析，请参考本文正文内容。"
                faq_list.append({"question": question, "answer": answer})
        
        # 检测包含问号的句子
        elif '？' in line and len(line) < 100:
            question = line.rstrip('？？')
            if question and len(faq_list) < max_faq:
                answer = f"关于「{question}」的详细解答，请参考本文相关章节。"
                faq_list.append({"question": question + "？", "answer": answer})
    
    # 如果提取的FAQ不足，根据关键词生成
    if len(faq_list) < 3:
        keywords = []
        for line in lines[:20]:  # 从前20行提取关键词
            for indicator in question_indicators[1:]:  # 跳过问号
                if indicator in line and len(line) < 80:
                    keywords.append(line.strip())
        
        default_questions = [
            f"{main_keyword if 'main_keyword' in dir() else '公考'}报名条件是什么？",
            f"{main_keyword if 'main_keyword' in dir() else '公考'}考试科目有哪些？",
            f"{main_keyword if 'main_keyword' in dir() else '公考'}如何高效备考？",
            f"{main_keyword if 'main_keyword' in dir() else '公考'}分数线是多少？",
            f"{main_keyword if 'main_keyword' in dir() else '公考'}什么时候出成绩？",
        ]
        
        for q in default_questions:
            if len(faq_list) >= max_faq:
                break
            if not any(f['question'] == q for f in faq_list):
                faq_list.append({"question": q, "answer": f"关于{q.rstrip('？')}的详细信息，请参考本文正文。"})
    
    return faq_list[:max_faq]


def generate_faq_section(faq_list, article_url=""):
    """生成FAQ章节的Markdown和JSON-LD结构化数据"""
    if not faq_list:
        return ""
    
    # Markdown部分
    md_section = "\n## 常见问题（FAQ）\n\n"
    for i, faq in enumerate(faq_list, 1):
        md_section += f"### {i}. {faq['question']}\n\n{faq['answer']}\n\n"
    
    # JSON-LD结构化数据
    json_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    for faq in faq_list:
        json_ld["mainEntity"].append({
            "@type": "Question",
            "name": faq['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq['answer']
            }
        })
    
    json_ld_str = json.dumps(json_ld, ensure_ascii=False, indent=2)
    
    # 将JSON-LD嵌入到script标签中
    script_tag = f"""
<script type="application/ld+json">
{json_ld_str}
</script>
"""
    
    return md_section + "\n" + script_tag + "\n"


# ========== CTA生成函数 ==========
def generate_cta_section(category, content_type="原创"):
    """
    根据文章分类生成对应的CTA（行动号召）区块
    """
    cta_templates = {
        "guokao": {
            "title": "🎯 国考备考资料领取",
            "items": [
                "📄 [2026国考职位表完整版下载 →](https://gk.edu-sjtu.cn/guokao/)",
                "📚 [申论高分范文100篇免费领 →](https://gk.edu-sjtu.cn/guokao/)",
                "🎥 [国考面试1对1辅导预约 →](https://gk.edu-sjtu.cn/beikao-zhinan/)",
            ]
        },
        "shengkao": {
            "title": "📌 省考备考资源",
            "items": [
                "📋 [2026省考职位表汇总下载 →](https://gk.edu-sjtu.cn/shengkao/)",
                "📝 [省考申论万能框架模板 →](https://gk.edu-sjtu.cn/shengkao/)",
                "💡 [省考历年真题及解析 →](https://gk.edu-sjtu.cn/zhenti-jiexi/)",
            ]
        },
        "shanghai-shegong": {
            "title": "🏙️ 上海社工专属福利",
            "items": [
                "📬 [加入上海社工备考群 →](https://gk.edu-sjtu.cn/shanghai-shegong/)",
                "📖 [上海社工考试大纲解读 →](https://gk.edu-sjtu.cn/shanghai-shegong/)",
                "💼 [上海各区社工待遇对比表 →](https://gk.edu-sjtu.cn/shanghai-shegong/)",
            ]
        },
        "gangwei-fenxi": {
            "title": "🏢 事业单位考试助手",
            "items": [
                "📊 [事业单位职测考情分析 →](https://gk.edu-sjtu.cn/gangwei-fenxi/)",
                "📚 [事业单位历年真题下载 →](https://gk.edu-sjtu.cn/zhenti-jiexi/)",
                "🎯 [事业单位面试技巧大全 →](https://gk.edu-sjtu.cn/beikao-zhinan/)",
            ]
        },
        "beikao-zhinan": {
            "title": "📚 备考指南精选",
            "items": [
                "⏰ [3个月高效备考计划表 →](https://gk.edu-sjtu.cn/beikao-zhinan/)",
                "📖 [零基础备考全攻略 →](https://gk.edu-sjtu.cn/beikao-zhinan/)",
                "💪 [公考高分学员经验分享 →](https://gk.edu-sjtu.cn/shang-an-jingyan/)",
            ]
        },
        "zhengce-jiedu": {
            "title": "📜 最新政策解读",
            "items": [
                "📰 [2026公考最新政策汇总 →](https://gk.edu-sjtu.cn/zhengce-jiedu/)",
                "🔍 [政策变化对备考的影响 →](https://gk.edu-sjtu.cn/zhengce-jiedu/)",
                "💡 [如何根据政策调整备考策略 →](https://gk.edu-sjtu.cn/beikao-zhinan/)",
            ]
        },
        "baokao-gonggao": {
            "title": "📢 报考公告速递",
            "items": [
                "📋 [2026最新报考公告汇总 →](https://gk.edu-sjtu.cn/baokao-gonggao/)",
                "🔔 [报名入口及流程详解 →](https://gk.edu-sjtu.cn/baokao-gonggao/)",
                "✅ [报考条件自测工具 →](https://gk.edu-sjtu.cn/beikao-zhinan/)",
            ]
        },
        "zhenti-jiexi": {
            "title": "📝 真题解析专区",
            "items": [
                "📚 [近5年公考真题汇总 →](https://gk.edu-sjtu.cn/zhenti-jiexi/)",
                "🔍 [真题解析及答题技巧 →](https://gk.edu-sjtu.cn/zhenti-jiexi/)",
                "💯 [高频考点及命题规律 →](https://gk.edu-sjtu.cn/beikao-zhinan/)",
            ]
        },
        "shang-an-jingyan": {
            "title": "🏆 上岸经验分享",
            "items": [
                "📖 [100+学员上岸经验合集 →](https://gk.edu-sjtu.cn/shang-an-jingyan/)",
                "💬 [面试逆袭成功经验 →](https://gk.edu-sjtu.cn/shang-an-jingyan/)",
                "🎯 [零基础3个月上岸计划 →](https://gk.edu-sjtu.cn/beikao-zhinan/)",
            ]
        },
    }
    
    # 默认CTA（如果没有匹配的分类）
    default_cta = {
        "title": "🎓 公考备考资料",
        "items": [
            "📚 [公考备考全攻略 →](https://gk.edu-sjtu.cn/)",
            "📝 [历年真题及解析 →](https://gk.edu-sjtu.cn/zhenti-jiexi/)",
            "💪 [高分学员经验分享 →](https://gk.edu-sjtu.cn/shang-an-jingyan/)",
        ]
    }
    
    cta = cta_templates.get(category, default_cta)
    
    cta_html = f"""
<div class="cta-section" style="background: #f8f9fa; border-left: 4px solid #1890ff; padding: 20px; margin: 30px 0; border-radius: 4px;">
  <h3 style="margin-top: 0; color: #1890ff;">{cta['title']}</h3>
  <ul style="list-style: none; padding-left: 0;">
"""
    for item in cta['items']:
        cta_html += f"    <li style='margin: 10px 0;'>{item}</li>\n"
    
    cta_html += "  </ul>\n</div>\n"
    
    return cta_html

# 文章主题库
ARTICLES = [
    # 国考2篇
    {
        "title": "2026年国考笔试成绩查询时间及入口",
        "category": "guokao",
        "type": "info",
        "tags": ["国考", "笔试成绩", "成绩查询"],
        "desc": "2026年国考笔试结束后，考生最关心的就是成绩查询。本文详解2026年国考笔试成绩查询时间、查询入口、成绩计算方法、合格分数线预测。",
        "source_url": "https://gk.edu-sjtu.cn/guokao/",  # 原创文章填网站栏目页
        "source_date": "2026-05-27",
        "content_type": "原创"
    },
    {
        "title": "国考面试礼仪全攻略：考官第一印象加分项",
        "category": "guokao", 
        "type": "guide",
        "tags": ["国考", "面试礼仪", "面试技巧"],
        "desc": "国考面试中，礼仪细节往往决定第一印象。本文从着装、举止、语言表达等多方面，全面解析国考面试礼仪要点，帮助考生在面试中脱颖而出。",
        "source_url": "https://gk.edu-sjtu.cn/guokao/",
        "source_date": "2026-05-27",
        "content_type": "原创"
    },
    # 省考2篇
    {
        "title": "2026年省考联考省份及考试时间汇总",
        "category": "shengkao",
        "type": "info",
        "tags": ["省考", "联考", "考试时间"],
        "desc": "2026年省考联考有哪些省份参加？考试时间如何安排？本文汇总2026年参加联考的各省份考试时间、报名入口、笔试科目安排。",
        "source_url": "https://gk.edu-sjtu.cn/shengkao/",
        "source_date": "2026-05-27",
        "content_type": "原创"
    },
    {
        "title": "省考申论大作文万能框架及高分技巧",
        "category": "shengkao",
        "type": "guide", 
        "tags": ["省考", "申论", "作文技巧"],
        "desc": "省考申论大作文是拉开分差的关键。本文分享省考申论大作文的万能框架结构、高分写作技巧、常见话题预测及范文参考。",
        "source_url": "https://gk.edu-sjtu.cn/shengkao/",
        "source_date": "2026-05-27",
        "content_type": "原创"
    },
    # 上海社工2篇
    {
        "title": "2026年上海社区工作者各区招聘计划解读",
        "category": "shanghai-shegong",
        "type": "info",
        "tags": ["上海社工", "招聘计划", "各区招聘"],
        "desc": "2026年上海各区社区工作者招聘计划陆续发布。本文解读浦东、徐汇、静安、杨浦等区的招聘人数、报名条件、考试时间安排。",
        "source_url": "https://gk.edu-sjtu.cn/shanghai-shegong/",
        "source_date": "2026-05-27",
        "content_type": "原创"
    },
    {
        "title": "上海社工考试行测模块备考策略及真题分析",
        "category": "shanghai-shegong",
        "type": "study",
        "tags": ["上海社工", "行测", "备考策略"],
        "desc": "上海社工考试行测模块是重点考察内容。本文分析上海社工行测考试的题型分布、重点知识点、历年真题规律及高效备考策略。",
        "source_url": "https://gk.edu-sjtu.cn/shanghai-shegong/",
        "source_date": "2026-05-27",
        "content_type": "原创"
    },
    # 事业单位1篇
    {
        "title": "事业单位联考《职业能力倾向测验》考情分析",
        "category": "gangwei-fenxi",
        "type": "info",
        "tags": ["事业单位", "职测", "考情分析"],
        "desc": "事业单位联考《职业能力倾向测验》与公务员考试《行测》有何区别？本文详细分析事业单位职测的考试题型、难度特点、备考要点。",
        "source_url": "https://gk.edu-sjtu.cn/gangwei-fenxi/",
        "source_date": "2026-05-27",
        "content_type": "原创"
    },
    # 通用备考1篇  
    {
        "title": "零基础跨专业考生3个月公考上岸复习计划",
        "category": "beikao-zhinan",
        "type": "guide",
        "tags": ["零基础", "跨专业", "复习计划"],
        "desc": "零基础、跨专业考生如何在3个月内高效备考公考并成功上岸？本文提供详细的每日复习计划、资料选择建议、刷题策略及心态调整方法。",
        "source_url": "https://gk.edu-sjtu.cn/beikao-zhinan/",
        "source_date": "2026-05-27",
        "content_type": "原创"
    },
]

def generate_article_md(article_info):
    """生成单篇文章的Markdown内容"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 使用CTR标题生成函数生成高点击率标题
    title = generate_ctr_title(article_info)
    desc = article_info["desc"]
    category = article_info["category"]
    tags = article_info["tags"]
    article_type = article_info["type"]

    # 新增字段：信源标注和文章类型（补救质量短板）
    source_url = article_info.get("source_url", "https://gk.edu-sjtu.cn")
    source_date = article_info.get("source_date", today)
    content_type = article_info.get("content_type", "原创")

    # 生成文件名（使用原标题的safe版本，避免CTR标题中的特殊字符）
    original_title = article_info["title"]
    safe_title = original_title.replace("2026年", "").replace(" ", "-")[:40]
    filename = f"{today}-{safe_title}.md"
    
    # Frontmatter (注意description使用日文引号避免YAML错误)
    frontmatter = f"""---
title: "{title}"
description: "{desc[:120]}..."
date: "{today}"
category: "{category}"
tags: {json.dumps(tags, ensure_ascii=False)}
author: "公考助手"
source_url: "{source_url}"
source_date: "{source_date}"
content_type: "{content_type}"
---

"""
    
    # 正文内容 (1500+字)
    # 添加内容类型标签和时效性提示
    content_type_badge = ""
    if content_type == "原创":
        content_type_badge = "【原创】"
    elif content_type == "转载":
        content_type_badge = "【转载】"
    elif content_type == "学员分享":
        content_type_badge = "【学员分享】"
    
    content = f"""# {title} {content_type_badge}

> {desc}

"""
    
    # 添加时效性提示（超过90天的文章）
    try:
        from datetime import datetime as dt
        article_date = dt.strptime(source_date, "%Y-%m-%d")
        days_old = (dt.now() - article_date).days
        if days_old > 90:
            content += f"""<div class="timeliness-warning">
⚠️ **时效性提示**：本文发布于 {source_date}，距今已 {days_old} 天，部分信息可能已过时。建议您同时参考最新公告和资料。
</div>

"""
    except:
        pass
    
    content += f"""## 一、核心概述

公考备考是一个系统性工程，需要考生从多个维度进行充分准备。无论是国考、省考还是事业单位考试，都有其独特的命题规律和备考策略。本文将围绕「{title.replace('2026年', '')}」这一主题，为考生提供全面、深入的解析。

## 二、详细解析

### 2.1 考试基本情况

"""
    
    # 根据不同类型添加内容
    if "成绩查询" in title or "笔试" in title:
        content += """公务员及事业单位考试成绩查询是考生关注的焦点。通常情况下，笔试成绩会在考试结束后30-45天内公布。

**成绩查询注意事项：**
1. **查询时间**：一般集中在早上9:00-10:00开通查询入口
2. **查询入口**：官方网站、人事考试网、人社厅官网
3. **查询材料**：准考证号、身份证号
4. **成绩复核**：对成绩有异议可在规定时间内申请复核

"""
    elif "面试" in title:
        content += """面试是公考中至关重要的环节，往往决定最终能否成功上岸。面试不仅考察考生的知识储备，更考察综合素质、应变能力、语言表达能力。

**面试核心考察要素：**
1. **综合分析能力**：对问题的深度思考和分析
2. **计划组织能力**：活动策划和组织协调能力  
3. **人际关系处理能力**：职场人际问题的处理
4. **应变能力**：突发事件的应急处理
5. **语言表达能力**：逻辑清晰、表达流畅

"""
    elif "省考" in title and "联考" in title:
        content += """省考联考是指多个省份在同一天举行公务员笔试，统一时间、统一命题（部分省份自主命题）。参加联考的省份可以共享考官资源、降低考试成本。

**2026年省考联考预计时间：**
- 公告发布：2026年2月中下旬
- 报名时间：2026年3月初  
- 笔试时间：2026年3月下旬（预计3月28日）
- 成绩公布：2026年5月上旬

**参加联考的常见省份：**
广东、湖南、湖北、安徽、福建、江西、陕西、山西、四川、重庆、河北、浙江等。

"""
    elif "申论" in title:
        content += """申论是公务员考试的重要科目，主要考察考生的阅读理解能力、综合分析能力、提出和解决问题能力、文字表达能力。

**申论大作文万能框架：**

**开头段（约150字）：**
- 引出话题：使用引言、数据或社会现象引出
- 分析现状：简要分析该话题的社会背景
- 提出论点：明确表达自己观点

**主体段（约600字，分3段）：**
- 分论点1 + 论据（案例/数据/理论）
- 分论点2 + 论据  
- 分论点3 + 论据

**结尾段（约150字）：**
- 总结全文：重申核心观点
- 升华主题：从个人到社会、国家层面
- 号召行动：提出建设性建议

"""
    elif "上海社工" in title:
        content += """上海作为中国经济最发达的城市之一，社区工作者岗位一直备受关注。上海社工考试相对国考、省考来说，竞争压力较小，且对户籍限制相对宽松。

**上海社工考试特点：**
1. **考试科目**：通常为《综合能力测验》和《专业知识》
2. **题型分布**：客观题+主观题相结合
3. **合格分数线**：一般按1:3比例确定面试人员
4. **薪资待遇**：月薪6000-9000元（各区有差异）

"""
    elif "事业单位" in title:
        content += """事业单位联考是指各事业单位在同一时间段举行联合招聘考试。与公务员考试相比，事业单位考试更注重专业技术能力。

**《职业能力倾向测验》考试特点：**
- **考试时长**：90分钟
- **题量**：100-120题  
- **模块**：言语理解、数量关系、判断推理、资料分析、常识判断
- **难度**：略低于公务员《行测》

**与公务员《行测》的主要区别：**
1. 题量相对较少
2. 难度相对较低
3. 更侧重实际应用能力
4. 部分岗位有专业测试

"""
    else:
        content += """公考备考需要科学合理的规划，尤其是零基础、跨专业考生，更需要制定详细的学习计划。

**3个月备考时间分配建议：**
- **第1个月**：基础理论学习，系统学习各科目知识点
- **第2个月**：强化训练，大量刷题，查漏补缺
- **第3个月**：模拟冲刺，全真模拟，调整心态

"""
    
    content += """### 2.2 备考策略建议

**（1）科学规划时间**
公考备考是一个长跑，需要合理分配时间。建议每天保证4-6小时高效学习时间，周末可适当增加。

**（2）精选学习资料**
- 教材：选择权威出版社的教材
- 真题：近5年真题是最好资料
- 题库：分模块进行针对性训练
- 网课：选择口碑好的名师课程

**（3）注重方法技巧**
公考不仅考察知识储备，更考察解题技巧。行测要注重速算技巧、答题顺序；申论要注重写作框架、逻辑思维。

**（4）保持良好心态**
备考过程漫长而艰辛，保持积极乐观的心态至关重要。可以适当运动、听音乐等方式缓解压力。

### 2.3 常见误区提醒

1. **只刷题不总结**：刷题后要善于总结规律，避免重复犯错
2. **忽视真题**：真题是最好的复习资料，要反复研究
3. **盲目报班**：根据自身基础选择，不要盲目跟风
4. **临时抱佛脚**：公考需要长期积累，不可能一蹴而就

## 三、实用技巧分享

### 3.1 行测答题技巧

- **言语理解**：先读问题再看文段，抓住关键词
- **数量关系**：掌握速算技巧，学会合理放弃
- **判断推理**：熟悉各类题型解题套路
- **资料分析**：优先看图标题眼，掌握速算方法

### 3.2 申论写作技巧

- **字迹工整**：卷面分很重要
- **结构清晰**：采用"总-分-总"结构
- **论点明确**：每段开头明确表达分论点
- **论据充分**：使用案例、数据、理论等支撑论点

### 3.3 面试备考技巧

- **多练习**：找同伴模拟面试场景
- ** recordings**：录下自己的回答，反复改进
- **关注时事**：积累热点话题素材
- **模拟训练**：进行全真模拟面试

## 四、总结与建议

公考之路充满挑战，但只要方法得当、坚持努力，成功上岸并非遥不可及。

**核心建议：**
1. 尽早开始备考，不要临时抱佛脚
2. 制定合理计划，并严格执行
3. 重视真题训练，掌握命题规律
4. 保持良好心态，积极应对挑战
5. 关注官方信息，避免错过重要时间节点

希望本文对各位考生有所帮助，祝愿大家都能成功上岸！

---
*本文仅供参考，具体信息以官方公告为准。*
"""

    # ========== 添加FAQ章节（结构化数据）==========
    faq_list = extract_faq_from_content(content + " " + desc)
    if faq_list:
        faq_section = generate_faq_section(faq_list)
        content += "\n" + faq_section

    # ========== 添加CTA行动号召区块 ==========
    cta_section = generate_cta_section(category, content_type)
    content += "\n" + cta_section

    return filename, frontmatter + content


def main():
    print("=" * 60)
    print("公考SEO文章自动生成脚本 v3")
    print("=" * 60)
    print()
    
    # 构建文章索引（用于内链匹配）
    article_index = []
    if INTERNAL_LINK_ENABLED:
        print("正在构建文章索引...")
        article_index = build_article_index()
        print(f"索引完成，共 {len(article_index)} 篇文章")
        print()
    
    generated = []
    
    for i, article in enumerate(ARTICLES):
        print(f"[{i+1}/8] 生成文章: {article['title']}")
        
        filename, content = generate_article_md(article)
        
        # 确定输出目录
        category_dir = CONTENT_DIR / article["category"]
        category_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = category_dir / filename
        
        # 检查是否已存在
        if output_path.exists():
            print(f"  跳过（已存在）: {filename}")
            continue
        
        # 如果启用了内链功能，添加相关阅读链接
        if INTERNAL_LINK_ENABLED and article_index:
            # 构造新文章信息
            new_article_info = {
                'title': article['title'],
                'category': article['category'],
                'tags': article['tags'],
                'date': datetime.now().strftime("%Y-%m-%d"),
                'path': str(output_path)
            }
            
            # 找到相关文章（排除自己）
            related = find_related_articles(
                new_article_info, 
                article_index, 
                max_links=3,
                exclude_path=str(output_path)
            )
            
            if related:
                # 生成相关阅读章节
                related_section = generate_related_links_section(new_article_info, related)
                
                # 插入到文章内容中（在总结章节前）
                patterns = [
                    r'(## 四、总结与建议)',
                    r'(## 三、总结与建议)',
                    r'(## 总结)',
                    r'(---\n\*本文仅供参考)',
                ]
                
                inserted = False
                for pattern in patterns:
                    match = re.search(pattern, content)
                    if match:
                        pos = match.start()
                        content = content[:pos] + related_section + "\n" + content[pos:]
                        inserted = True
                        break
                
                # 如果没找到合适位置，追加到末尾
                if not inserted:
                    content += "\n" + related_section
                
                print(f"  已添加 {len(related)} 篇相关阅读链接")
        
        # 写入文件
        output_path.write_text(content, encoding="utf-8")
        print(f"  已生成: {output_path.relative_to(ROOT)}")
        generated.append(output_path)
    
    print()
    print("=" * 60)
    print(f"共生成 {len(generated)} 篇文章")
    print("=" * 60)
    
    return generated


if __name__ == "__main__":
    main()
