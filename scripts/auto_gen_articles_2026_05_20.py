#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成公考SEO文章 - 2026-05-20 执行
生成 8 篇文章，带图片配图
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
TODAY = datetime.now().strftime("%Y-%m-%d")

# 文章定义 - 使用关键词池中的angles字段生成不同角度的文章
ARTICLES = [
    {
        "filename": f"beikao-zhinan/2026-shegong-k Cory-aomen-baoming.md",
        "title": "2026年社工考试报名流程详解：从注册到缴费的完整指南",
        "keyword": "社工招聘报名流程",
        "category": "beikao-zhinan",
        "tags": ["社工报名流程", "社区工作者报名", "2026社工报名", "报名流程图解"],
        "description": "2026年社工考试报名流程全详解，从用户注册、信息填写、照片上传到缴费确认，一步步教您完成报名。",
        "headings": ["社工考试报名整体流程", "用户注册与账号激活", "个人信息填写注意事项", "照片上传要求与处理工具", "缴费确认与报名成功确认"],
    },
    {
        "filename": f"gangwei-fenxi/2026-shegong-xinzi-goucheng-yanjing.md",
        "title": "社区工作者薪资构成详解：基本工资、绩效与补贴全解析",
        "keyword": "社区工作者工资多少",
        "category": "gangwei-fenxi",
        "tags": ["社区工作者薪资", "社工工资构成", "基本工资", "绩效奖金"],
        "description": "详细解析社区工作者的薪资构成，包括基本工资、绩效奖金、岗位补贴、工龄工资等部分，帮助考生了解实际收入情况。",
        "headings": ["社区工作者薪资的整体构成", "基本工资：岗位等级决定基础待遇", "绩效奖金：月度与年度考核结果", "补贴部分：交通、餐补、高温补贴等", "各地社区工作者薪资差异分析"],
    },
    {
        "filename": f"zhengce-jiedu/2026-shegong-hukou-yiju-zhengce.md",
        "title": "2026年社区工作者户籍政策解读：外地人报考需要居住证吗",
        "keyword": "社区工作者户籍要求",
        "category": "zhengce-jiedu",
        "tags": ["社工户籍政策", "外地人考社工", "居住证报考", "2026新政"],
        "description": "2026年社区工作者户籍政策最新解读，分析外地人报考是否需要居住证，哪些地区已放宽户籍限制。",
        "headings": ["社区工作者户籍要求的政策背景", "2026年各地户籍政策最新变化", "居住证 vs 本地户籍：报考差异", "无需户籍限制的地区案例分析", "外地考生报考的准备工作"],
    },
    {
        "filename": f"shang-an-jingyan/2026-shegong-mianshi-yingdu-yingdu.md",
        "title": "社区工作者面试应急预案：常见问题与应对技巧全攻略",
        "keyword": "社区工作者面试技巧",
        "category": "shang-an-jingyan",
        "tags": ["社工面试技巧", "面试应急预案", "社区工作者面试", "面试高分攻略"],
        "description": "社区工作者面试应急预案与应对技巧全攻略，涵盖常见问题、语言表达、仪态仪表等核心要点，帮助考生提升面试得分。",
        "headings": ["社区工作者面试的整体流程回顾", "面试中常见的突发情况与应对", "语言表达技巧：逻辑清晰与重点突出", "仪态仪表：着装与肢体语言", "模拟练习：如何提高面试应变能力"],
    },
    {
        "filename": f"zhenti-jiexi/2026-shegong-gongji-shiti-fenxi.md",
        "title": "2026年社区工作者公基试题解析：高频考点与答题技巧",
        "keyword": "社区工作者公共基础知识",
        "category": "zhenti-jiexi",
        "tags": ["公基试题解析", "社区工作者公基", "高频考点", "答题技巧"],
        "description": "2026年社区工作者公共基础知识试题解析，分析高频考点、命题规律和答题技巧，帮助考生高效备考公基科目。",
        "headings": ["公共基础知识考试特点分析", "法律常识：高频考点与典型例题", "政治理论：时政热点与基本理论", "社区专业知识：基层治理与政策法规", "公基答题技巧与时间分配策略"],
    },
    {
        "filename": f"baokao-gonggao/2026-shegong-zaixian-pay-jiufen.md",
        "title": "社工考试报名缴费常见问题：支付失败、退费政策一站式解答",
        "keyword": "社区工作者考试报名费",
        "category": "baokao-gonggao",
        "tags": ["社工报名缴费", "支付问题", "退费政策", "报名常见问题"],
        "description": "社工考试报名缴费常见问题一站式解答，包括支付失败处理方法、退费政策规定、发票申请流程等实用信息。",
        "headings": ["社工考试报名缴费的整体流程", "常见支付失败原因与解决方法", "退费政策：什么条件可以退费", "发票申请：是否需要及如何申请", "缴费确认：确保报名成功的检查清单"],
    },
    {
        "filename": f"beikao-zhinan/2026-shegong-zhengshen-cailiao.md",
        "title": "社区工作者政审材料准备清单：需要哪些证明文件",
        "keyword": "社区工作者政审要求",
        "category": "beikao-zhinan",
        "tags": ["社工政审材料", "政审证明", "无犯罪记录证明", "政审流程"],
        "description": "社区工作者政审材料准备清单，详细列出需要哪些证明文件，如何办理无犯罪记录证明、征信报告等政审材料。",
        "headings": ["社区工作者政审的整体流程", "无犯罪记录证明：办理地点与流程", "征信报告：是否需要及如何获取", "学历学位证明：验证与认证", "其他可能需要的证明材料清单"],
    },
    {
        "filename": f"gangwei-fenxi/2026-shegong-zhuanbian-bianzhi.md",
        "title": "社区工作者转编机会分析：哪些地区有转编政策，如何准备",
        "keyword": "社区工作者能转编制吗",
        "category": "gangwei-fenxi",
        "tags": ["社工转编", "社区工作者编制", "转编政策", "如何准备转编"],
        "description": "社区工作者转编机会全面分析，介绍哪些地区有转编政策，转编条件和程序，以及如何提前准备增加转编成功率。",
        "headings": ["社区工作者转编的政策背景", "各地转编政策差异：典型案例", "转编的基本条件与优先情形", "如何提前准备：工作表现与资格考试", "转编后的编制性质与待遇变化"],
    },
]

def pick_images(category, count=2):
    """调用 image_picker.py 选取图片"""
    try:
        import subprocess
        cmd = [sys.executable, "scripts/image_picker.py", "--category", category, "--count", str(count), "--update", "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"选取图片失败: {e}")
    return []

def generate_article_content(article):
    """生成文章内容"""
    title = article["title"]
    keyword = article["keyword"]
    category = article["category"]
    headings = article["headings"]
    tags = article["tags"]
    description = article["description"]
    
    # 生成文章内容
    content = f"""---
title: "{title}"
date: "{TODAY}"
description: "{description}"
category: "{category}"
tags: {tags}
author: "公考助手"
---

# {title}

{description}

"""
    
    # 添加各个段落
    for i, heading in enumerate(headings, 1):
        content += f"\n## {i}. {heading}\n\n"
        # 生成段落内容 - 实际应用中这里应该调用LLM生成高质量内容
        # 这里先生成占位符，实际执行时应该替换为LLM生成的内容
        content += f"在此处添加关于「{heading}」的详细内容。包含{keyword}的相关信息，确保内容详实、有价值。\n\n"
    
    # 添加总结
    content += f"\n## 总结\n\n"
    content += f"通过以上分析，我们对{keyword}有了更全面的了解。希望本文能帮助考生们更好地备考社区工作者考试，顺利通过各环节挑战。\n"
    
    return content

def main():
    """主函数"""
    print(f"开始生成 {TODAY} 的 SEO 文章...")
    
    for article in ARTICLES:
        filename = article["filename"]
        filepath = CONTENT_DIR / filename
        
        # 确保目录存在
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成文章内容
        content = generate_article_content(article)
        
        # 选取图片
        images = pick_images(article["category"], count=2)
        
        # 在内容中插入图片
        if images:
            image_md = "\n\n"
            for img in images:
                img_path = img.get("path", "")
                alt_text = img.get("alt", article["keyword"])
                image_md += f"![{alt_text}]({img_path})\n\n"
            
            # 在第一个标题前插入图片
            first_heading_pos = content.find("## 1.")
            if first_heading_pos > 0:
                content = content[:first_heading_pos] + image_md + content[first_heading_pos:]
        
        # 写入文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 已生成: {filename}")
    
    print(f"\n{TODAY} 的 SEO 文章生成完成！共 {len(ARTICLES)} 篇")

if __name__ == "__main__":
    main()
