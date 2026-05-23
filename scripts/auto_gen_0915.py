#!/usr/bin/env python3
"""
自动生成09:15批次8篇SEO文章
- 社工2篇、国考2篇、省考2篇、事业单位1篇、通用备考1篇
- 每篇带2张配图
- 自动写入frontmatter
"""

import sys
import json
import random
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"
IMAGE_LIB = ROOT / "images" / "lib"
USAGE_LOG = ROOT / "scripts" / "image_usage_log.json"

# 文章分类 → 内容目录映射
CAT_DIR = {
    "shanghai-shegong": "shanghai-shegong",
    "guokao": "guokao",
    "shengkao": "shengkao",
    "gangwei-fenxi": "gangwei-fenxi",
    "beikao-zhinan": "beikao-zhinan",
}

# 图片主题映射（同image_picker.py）
CATEGORY_IMAGE_MAP = {
    "guokao":           ["exam", "study", "gov", "motivation", "office"],
    "shengkao":         ["exam", "study", "motivation", "office", "books"],
    "shanghai-shegong": ["gov", "office", "people", "city", "exam"],
    "gangwei-fenxi":    ["office", "people", "gov", "tech", "city"],
    "beikao-zhinan":    ["study", "books", "exam", "motivation", "writing"],
}

def load_usage_log():
    if not USAGE_LOG.exists():
        return {}
    with open(USAGE_LOG, "r", encoding="utf-8") as f:
        return json.load(f)

def save_usage_log(log):
    log["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(USAGE_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def get_available_images(category, count=2, days=10):
    """选取指定分类的未最近使用的图片"""
    log = load_usage_log()
    usage = log.get("usage", {})
    today = datetime.now().strftime("%Y-%m-%d")
    
    from datetime import datetime as dt, timedelta
    cutoff = dt.now() - timedelta(days=days)
    
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
            # 检查是否最近使用
            recently = False
            if rel in usage:
                try:
                    last = dt.strptime(usage[rel], "%Y-%m-%d")
                    if last > cutoff:
                        recently = True
                except:
                    pass
            if not recently:
                available.append(rel)
    
    # 去重
    available = list(dict.fromkeys(available))
    
    if len(available) < count:
        # 放宽到5天
        cutoff5 = dt.now() - timedelta(days=5)
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
                        last = dt.strptime(usage[rel], "%Y-%m-%d")
                        if last > cutoff5:
                            recently = True
                    except:
                        pass
                if not recently:
                    available.append(rel)
        available = list(dict.fromkeys(available))
    
    if not available:
        # 全部图片任选
        for theme in themes:
            theme_dir = IMAGE_LIB / theme
            if not theme_dir.exists():
                continue
            for f in theme_dir.iterdir():
                if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                    continue
                available.append(f"/images/lib/{theme}/{f.name}")
        available = list(dict.fromkeys(available))
    
    selected = random.sample(available, min(count, len(available)))
    
    # 更新使用记录
    for img in selected:
        usage[img] = today
    log["usage"] = usage
    save_usage_log(log)
    
    return selected

def gen_article_md(article_info, images):
    """
    生成文章内容（1500-2500字SEO文章）
    article_info: dict with title, description, category, tags, keyword
    images: list of image paths
    """
    title = article_info["title"]
    description = article_info["description"]
    category = article_info["category"]
    tags = article_info["tags"]
    keyword = article_info["keyword"]
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 生成正文内容（基于关键词和分类）
    content = gen_body_content(article_info, images)
    
    md = f"""---
title: "{title}"
description: "{description}"
date: "{date_str}"
category: {category}
tags: [{", ".join([f'"{t}"' for t in tags])}]
author: 公考助手
---

{content}
"""
    return md

def gen_body_content(article_info, images):
    """根据文章信息生成正文内容"""
    title = article_info["title"]
    category = article_info["category"]
    keyword = article_info["keyword"]
    
    # 图片Markdown
    img1 = f"![]({images[0]})" if images else ""
    img2 = f"![]({images[1]})" if len(images) > 1 else ""
    
    # 根据不同分类生成不同的正文模板
    templates = {
        "shanghai-shegong": [
            f"# {title}\n\n",
            f"随着上海社区工作者招聘规模的持续扩大，越来越多的考生开始关注「{keyword}」这一热点话题。",
            "本文将从报考条件、考试内容、备考策略等多个维度，为广大考生提供全面、实用的参考信息。\n\n",
            f"{img1}\n\n" if img1 else "",
            "## 一、上海社区工作者招聘现状\n\n",
            "近年来，上海市各区政府持续加大社区工作者招聘力度，",
            "岗位覆盖街道、社区服务中心、综合治理中心等多个方向。",
            "根据往年公告数据，全市年均招聘人数保持在较高规模，竞争比例因地而异。\n\n",
            "## 二、报名条件详解\n\n",
            "上海社区工作者报名条件主要包括以下几个方面：\n\n",
            "1. **户籍要求**：大部分岗位要求具有上海市常住户口，部分岗位接受持有上海市居住证的考生。\n",
            "2. **学历要求**：大多数岗位要求大专及以上学历，部分岗位要求本科及以上。\n",
            "3. **年龄要求**：一般要求18-35周岁，部分岗位可放宽至40周岁。\n",
            "4. **专业要求**：大部分岗位不限专业，少数岗位要求社会工作、法学、管理学等相关专业。\n\n",
            "## 三、考试内容与科目\n\n",
            "上海社区工作者考试通常包含以下科目：\n\n",
            "- **《综合能力测试》**：考察行政职业能力，包括言语理解、判断推理、资料分析等。\n",
            "- **《社区工作专业知识》**：考察社区工作相关法律法规、社区治理、社会工作方法等。\n",
            "- **面试**：结构化面试，重点考察综合素质、应变能力、岗位匹配度。\n\n",
            f"{img2}\n\n" if img2 else "",
            "## 四、备考策略建议\n\n",
            "### 4.1 笔试备考\n\n",
            "1. 提前3-6个月开始系统复习，重点攻克行测各模块。\n",
            "2. 社区专业知识需重点关注本市社区治理政策和法规文件。\n",
            "3. 多做真题，熟悉考试题型和难度。\n\n",
            "### 4.2 面试备考\n\n",
            "1. 熟悉结构化面试常见题型，如自我介绍、综合分析、应急应变等。\n",
            "2. 关注上海本地社区治理热点话题，积累答题素材。\n",
            "3. 进行模拟面试训练，提升临场应变能力。\n\n",
            "## 五、常见问题解答\n\n",
            "**Q1：非上海户籍可以报考吗？**\n",
            "A：大部分岗位要求上海户籍，但持有上海市居住证满一定年限的考生也可报考部分岗位。\n\n",
            "**Q2：社工证对报考有帮助吗？**\n",
            "A：持有社会工作者职业水平证书在招聘中通常可获得加分，建议在岗前或岗后考取。\n\n",
            "**Q3：社区工作者有编制吗？**\n",
            "A：目前上海社区工作者多为合同制，部分区试行员额制管理，具体情况以各区公告为准。\n\n",
            "## 六、总结\n\n",
            f"「{keyword}」是每位上海社区工作者考生必须认真准备的重要话题。",
            "希望本文能为您提供有价值的参考信息，祝您备考顺利、成功上岸！\n\n",
            "---\n\n",
            "*本文内容仅供参考，具体政策以各区官方公告为准。*\n",
        ],
        "guokao": [
            f"# {title}\n\n",
            f"国家公务员考试（国考）作为每年公考领域的重头戏，关于「{keyword}」的关注度持续攀升。",
            "本文将为考生全面解析相关考点、备考策略及注意事项，助力高效备考。\n\n",
            f"{img1}\n\n" if img1 else "",
            "## 一、国考基本概况\n\n",
            "国家公务员考试由中央公务员主管部门组织实施，每年举行一次。",
            "考试分为笔试和面试两个阶段，笔试包括《行政职业能力测验》和《申论》两科。\n\n",
            "## 二、报考条件解读\n\n",
            "1. **基本条件**：具有中华人民共和国国籍，年龄一般为18-35周岁。\n",
            "2. **学历条件**：大专及以上学历，部分岗位要求本科及以上。\n",
            "3. **专业条件**：不同岗位有不同专业要求，考生需仔细比对职位表。\n",
            "4. **其他条件**：部分岗位有政治面貌、基层工作经历等要求。\n\n",
            "## 三、考试科目深度解析\n\n",
            "### 3.1 行政职业能力测验\n\n",
            "行测包括言语理解与表达、数量关系、判断推理、资料分析、常识判断五大模块，",
            "满分100分，考试时长120分钟（省级以上）或120分钟（市地以下）。\n\n",
            "### 3.2 申论\n\n",
            "申论主要考察阅读理解能力、综合分析能力、提出和解决问题能力、文字表达能力。",
            "考生需根据给定材料进行分析、概括、提炼、加工，作答要求包括归纳概括、综合分析、提出对策、应用文写作、文章写作等。\n\n",
            f"{img2}\n\n" if img2 else "",
            "## 四、备考时间规划\n\n",
            "| 阶段 | 时间 | 重点任务 |\n",
            "|------|------|----------|\n",
            "| 基础阶段 | 考前6-4个月 | 系统学习各科目基础知识 |\n",
            "| 强化阶段 | 考前4-2个月 | 专项突破，刷题训练 |\n",
            "| 冲刺阶段 | 考前2个月 | 模拟考试，查漏补缺 |\n\n",
            "## 五、高分策略\n\n",
            "1. **行测策略**：优先做自己的优势模块，资料分析和判断推理是得分重点。\n",
            "2. **申论策略**：注重材料阅读，答案要点尽量从材料中提炼。\n",
            "3. **面试策略**：提前准备自我介绍、综合分析等常考题型，关注时政热点。\n\n",
            "## 六、总结\n\n",
            f"掌握「{keyword}」的核心要点，是国考备考的关键一步。",
            "希望本文的解析能为您的备考之路提供有力支持，预祝各位考生金榜题名！\n\n",
            "---\n\n",
            "*本文内容仅供参考，具体考试政策以国家公务员局官方公告为准。*\n",
        ],
        "shengkao": [
            f"# {title}\n\n",
            f"各省公务员考试（省考）与国考既有联系又有区别，关于「{keyword}」的各类问题，",
            "是每位省考考生都必须了解的重要内容。本文将从多个角度为考生详细解读。\n\n",
            f"{img1}\n\n" if img1 else "",
            "## 一、省考与国考的主要区别\n\n",
            "| 对比项 | 国考 | 省考 |\n",
            "|--------|------|------|\n",
            "| 组织单位 | 国家公务员局 | 各省公务员局 |\n",
            "| 考试时间 | 每年11月底 | 每年3-4月（多省联考） |\n",
            "| 户籍限制 | 大多数岗位无限制 | 部分岗位限本省户籍 |\n",
            "| 考试内容 | 行测+申论 | 行测+申论（部分省份加试专业科目） |\n\n",
            "## 二、省考报名条件\n\n",
            "1. **户籍要求**：大部分省份对本省户籍考生开放所有岗位，部分岗位面向全国招录。\n",
            "2. **学历要求**：大专及以上，部分偏远地区可放宽至高中/中专。\n",
            "3. **年龄要求**：18-35周岁，硕博可放宽至40周岁。\n",
            "4. **专业要求**：各岗位专业要求差异较大，需仔细比对职位表。\n\n",
            "## 三、省考笔试内容详解\n\n",
            "### 3.1 行测\n\n",
            "各省行测考试时间、题量略有差异，一般在90-120分钟之间，题量100-135道。",
            "主要模块与国考类似，但难度通常略低于国考。\n\n",
            "### 3.2 申论\n\n",
            "省考申论通常分为A类（省级机关）和B类（市县级机关），",
            "A类更侧重综合分析能力，B类更侧重解决实际问题能力。\n\n",
            f"{img2}\n\n" if img2 else "",
            "## 四、各省省考特点分析\n\n",
            "- **山东省考**：题量较大，竞争较为激烈，注重考察考生综合素质。\n",
            "- **广东省考**：分为县级以上和乡镇两套试卷，乡镇卷更侧重基层工作实际。\n",
            "- **浙江省考**：注重创新题型，考察考生灵活应变能力。\n",
            "- **四川省考**：分上、下半年两次考试，下半年招录人数较少。\n\n",
            "## 五、省考备考建议\n\n",
            "1. 提前了解本省省考特点，选择适合的备考资料。\n",
            "2. 关注本省公务员局官网，及时获取最新招考信息。\n",
            "3. 行测注重刷题训练，申论注重素材积累和写作训练。\n",
            "4. 面试提前准备，省考面试竞争同样激烈。\n\n",
            "## 六、总结\n\n",
            f"「{keyword}」作为省考备考的重要参考内容，值得每位考生深入研究。",
            "希望本文能帮助您更好地备战省考，顺利实现公考梦想！\n\n",
            "---\n\n",
            "*本文内容仅供参考，具体政策以各省公务员局官方公告为准。*\n",
        ],
        "gangwei-fenxi": [
            f"# {title}\n\n",
            f"事业单位作为公共管理服务体系的重要组成部分，其岗位设置和招聘要求一直是考生关注的焦点。",
            f"关于「{keyword}」，本文将从岗位类别、职责要求、待遇发展等多个维度进行深入分析。\n\n",
            f"{img1}\n\n" if img1 else "",
            "## 一、事业单位岗位分类\n\n",
            "根据《事业单位岗位设置管理试行办法》，事业单位岗位分为以下三类：\n\n",
            "1. **管理岗位**：担负领导职责或管理任务，共10个等级。\n",
            "2. **专业技术岗位**：从事专业技术工作，共13个等级（含高级、中级、初级）。\n",
            "3. **工勤技能岗位**：承担技能操作、维护服务等职责，共5个等级。\n\n",
            "## 二、各类岗位报考要求\n\n",
            "| 岗位类别 | 学历要求 | 专业要求 | 其他要求 |\n",
            "|----------|----------|----------|----------|\n",
            "| 管理岗位 | 大专及以上 | 视具体岗位而定 | 部分岗位要求中共党员 |\n",
            "| 专业技术岗位 | 大专及以上 | 与岗位相关专业技术专业 | 部分要求相应专业技术资格 |\n",
            "| 工勤技能岗位 | 高中/中专及以上 | 技能型专业 | 需具备相应技能等级证书 |\n\n",
            "## 三、事业单位考试内容\n\n",
            "事业单位招聘考试通常分为笔试和面试两个环节：\n\n",
            "### 3.1 笔试内容\n\n",
            "- **《公共基础知识》**：政治、法律、经济、管理、公文写作等。\n",
            "- **《职业能力倾向测验》**：与公考行测类似，但难度略低。\n",
            "- **《综合应用能力》**：与公考申论类似，但更侧重实际工作能力。\n",
            "- **专业科目**：部分专业技术岗位加试专业科目。\n\n",
            f"{img2}\n\n" if img2 else "",
            "### 3.2 面试内容\n\n",
            "事业单位面试通常采用结构化面试方式，部分岗位加试专业技能测试。",
            "面试重点考察综合素质、专业能力、岗位匹配度等。\n\n",
            "## 四、事业单位与公务员的区别\n\n",
            "| 对比项 | 事业单位 | 公务员 |\n",
            "|--------|----------|--------|\n",
            "| 编制类型 | 事业编制 | 行政编制 |\n",
            "| 考试难度 | 相对较低 | 相对较高 |\n",
            "| 晋升路径 | 专业技术职称/管理等级 | 行政职务晋升 |\n",
            "| 工作稳定性 | 较高 | 最高 |\n\n",
            "## 五、备考建议\n\n",
            "1. 明确报考岗位类别，针对性备考笔试科目。\n",
            "2. 关注本地人社局官网，及时获取招聘公告信息。\n",
            "3. 笔试注重公共基础知识积累，面试注重综合素质提升。\n",
            "4. 有条件者可参加事业单位定向培训班，提高备考效率。\n\n",
            "## 六、总结\n\n",
            f"深入分析「{keyword}」，有助于考生更科学地选择报考岗位、制定备考计划。",
            "事业单位考试竞争日益激烈，提早准备、系统复习是通过考试的关键。祝您备考顺利！\n\n",
            "---\n\n",
            "*本文内容仅供参考，具体招聘政策以各地人社局官方公告为准。*\n",
        ],
        "beikao-zhinan": [
            f"# {title}\n\n",
            f"公考备考是一场持久战，科学的备考方法和合理的时间规划是成功的关键。",
            f"本文围绕「{keyword}」这一主题，为广大考生提供一套系统、实用的备考指南。\n\n",
            f"{img1}\n\n" if img1 else "",
            "## 一、公考备考的整体规划\n\n",
            "公考备考通常分为三个阶段：基础阶段、强化阶段、冲刺阶段。",
            "每个阶段的重点任务不同，考生需根据自身情况合理安排。\n\n",
            "### 1.1 基础阶段（考前6-4个月）\n\n",
            "- 系统学习行测各模块基础知识\n",
            "- 熟悉申论考试要求和评分标准\n",
            "- 建立各科目知识框架\n",
            "- 做少量基础题目巩固知识\n\n",
            "### 1.2 强化阶段（考前4-2个月）\n\n",
            "- 专项突破，针对薄弱模块强化训练\n",
            "- 大量刷题，提高解题速度和准确率\n",
            "- 申论素材积累，关注时政热点\n",
            "- 定期模拟考试，检验学习效果\n\n",
            "### 1.3 冲刺阶段（考前2个月）\n\n",
            "- 全真模拟考试，调整应试状态\n",
            "- 查漏补缺，针对性复习重点难点\n",
            "- 面试提前准备，了解面试流程和题型\n",
            "- 调整心态，保持良好身心状态\n\n",
            f"{img2}\n\n" if img2 else "",
            "## 二、各科目备考要点\n\n",
            "### 2.1 行测备考要点\n\n",
            "| 模块 | 备考重点 | 时间分配建议 |\n",
            "|------|----------|----------------|\n",
            "| 言语理解 | 提高阅读速度，掌握解题技巧 | 25-30分钟 |\n",
            "| 数量关系 | 掌握常考题型，学会放弃难题 | 10-15分钟 |\n",
            "| 判断推理 | 熟悉规律，提高解题速度 | 30-35分钟 |\n",
            "| 资料分析 | 掌握速算技巧，确保高正确率 | 20-25分钟 |\n",
            "| 常识判断 | 广泛积累，不必过度投入 | 5-10分钟 |\n\n",
            "### 2.2 申论备考要点\n\n",
            "1. **材料阅读**：学会快速阅读，准确提炼要点。\n",
            "2. **归纳概括**：用简洁语言概括材料内容。\n",
            "3. **综合分析**：多角度分析问题，提出合理对策。\n",
            "4. **文章写作**：结构清晰，论点明确，论据充分。\n\n",
            "## 三、备考常见问题解答\n\n",
            "**Q1：零基础备考需要多长时间？**\n",
            "A：一般建议提前6个月以上开始系统备考，每天保证3-5小时有效学习时间。\n\n",
            "**Q2：在职人员如何安排备考时间？**\n",
            "A：建议利用早晚时间学习，工作日每天2-3小时，周末每天6-8小时。\n\n",
            "**Q3：备考资料如何选择？**\n",
            "A：选择权威机构出版的教材和真题，配合高质量网课效果更佳。\n\n",
            "## 四、总结\n\n",
            f"「{keyword}」是每位公考考生都会面临的重要课题。",
            "希望本文的备考指南能为您的公考之路提供有益参考，祝您成功上岸！\n\n",
            "---\n\n",
            "*本文内容仅供参考，具体备考计划请结合个人实际情况制定。*\n",
        ],
    }
    
    # 获取对应模板，如果没有则用通用模板
    template_lines = templates.get(category, templates["beikao-zhinan"])
    return "".join(template_lines)

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 定义8篇文章
    articles = [
        {
            "title": "上海社区工作者薪资待遇详解及2026年最新政策解读",
            "description": "全面解读上海社区工作者薪资待遇构成，包括基本工资、绩效奖金、五险一金等，并分析2026年最新政策变化及各区待遇差异。",
            "category": "shanghai-shegong",
            "tags": ["上海社区工作者", "薪资待遇", "2026年", "社区工作者工资"],
            "keyword": "上海社区工作者薪资待遇",
            "filename": f"{today}-shanghai-shegong-xinzi-daiyu-2026.md",
        },
        {
            "title": "上海社工考试面试分数线及录取规则全面解析",
            "description": "详细解析上海社工考试面试分数线划定规则、录取原则及历年分数线变化趋势，为考生提供面试备考参考。",
            "category": "shanghai-shegong",
            "tags": ["上海社工", "面试分数线", "录取规则", "社区工作者面试"],
            "keyword": "上海社工面试分数线",
            "filename": f"{today}-shanghai-shegong-mianshi-fenshuxian.md",
        },
        {
            "title": "国考行测资料分析高频考点与速算技巧全攻略",
            "description": "系统梳理国考行测资料分析模块高频考点，传授实用速算技巧，帮助考生在考试中快速准确解题，提高得分率。",
            "category": "guokao",
            "tags": ["国考", "行测", "资料分析", "速算技巧", "高频考点"],
            "keyword": "国考行测资料分析",
            "filename": f"{today}-guokao-xingce-ziliaofenxi-gaodian.md",
        },
        {
            "title": "国考申论大作文立意提炼与论证结构优化指南",
            "description": "深入讲解国考申论大作文的立意提炼方法、论证结构优化技巧，结合实际例题分析，帮助考生提升文章写作水平。",
            "category": "guokao",
            "tags": ["国考", "申论", "大作文", "立意提炼", "论证结构"],
            "keyword": "国考申论大作文",
            "filename": f"{today}-guokao-shenlun-dazuowen-linian.md",
        },
        {
            "title": "省考行测判断推理图形推理规律总结与解题技巧",
            "description": "全面总结省考行测判断推理模块中图形推理的规律类型，提供系统解题技巧和实战训练方法，助力考生高效备考。",
            "category": "shengkao",
            "tags": ["省考", "行测", "判断推理", "图形推理", "解题技巧"],
            "keyword": "省考行测判断推理",
            "filename": f"{today}-shengkao-xingce-panduan-tuixing.md",
        },
        {
            "title": "省考申论应用文写作格式规范与高分模板汇总",
            "description": "汇总省考申论应用文写作各类题型格式规范，提供高分写作模板和实战示例，帮助考生掌握应用文写作核心要领。",
            "category": "shengkao",
            "tags": ["省考", "申论", "应用文写作", "格式规范", "写作模板"],
            "keyword": "省考申论应用文写作",
            "filename": f"{today}-shengkao-shenlun-yingyongwen-xiezuo.md",
        },
        {
            "title": "事业单位综合管理类岗位的职责与发展路径分析",
            "description": "深入分析事业单位综合管理类岗位的主要职责、任职要求及职业发展路径，为考生报考和职业规划提供参考依据。",
            "category": "gangwei-fenxi",
            "tags": ["事业单位", "综合管理", "岗位职责", "职业发展", "事业编"],
            "keyword": "事业单位综合管理岗位",
            "filename": f"{today}-shiyedanwei-zongheguanli-gangwei.md",
        },
        {
            "title": "公考备考常见误区及科学避坑指南（2026年版）",
            "description": "总结公考备考过程中常见的学习误区、心态误区和策略误区，提供科学的避坑方法和备考建议，帮助考生少走弯路。",
            "category": "beikao-zhinan",
            "tags": ["公考备考", "备考误区", "避坑指南", "2026年", "科学备考"],
            "keyword": "公考备考误区",
            "filename": f"{today}-beikao-zhinan-beikao-wuqu-bikeng.md",
        },
    ]
    
    print(f"计划生成 {len(articles)} 篇文章")
    
    for i, article in enumerate(articles, 1):
        category = article["category"]
        dir_name = CAT_DIR.get(category, category)
        out_dir = CONTENT / dir_name
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 选取图片
        images = get_available_images(category, count=2)
        print(f"[{i}/{len(articles)}] {article['title']}")
        print(f"  分类: {category}, 图片: {images}")
        
        # 生成文章内容
        md_content = gen_article_md(article, images)
        
        # 写入文件
        out_file = out_dir / article["filename"]
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"  ✅ 已写入: {out_file}")
    
    print(f"\n全部 {len(articles)} 篇文章生成完毕！")

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    main()
