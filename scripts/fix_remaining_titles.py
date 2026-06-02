#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复剩余11篇标题异常的文章"""

import re

fixes = {
    "content/beikao-zhinan/2026-05-19-shanghai-shegong-mianshi-qingjing-moniti.md": {
        "title": "上海社区工作者面试情景模拟题解析与答题技巧",
        "desc": "上海社区工作者面试中情景模拟题是重点考查题型，本文精选典型模拟题，提供完整的答题思路和参考答案，帮助考生掌握答题技巧，提升面试通过率。"
    },
    "content/beikao-zhinan/2026-05-27-零基础跨专业考生3个月公考上岸复习计划.md": {
        "title": "零基础跨专业考生3个月公考上岸复习计划",
        "desc": "针对零基础跨专业考生，本文制定详细的3个月公考复习计划，从行测、申论到面试，分阶段安排学习任务，帮助考生高效备考，实现上岸目标。"
    },
    "content/guokao/2026-05-19-guokao-shegong-gangwei-tiaojian-jingzheng.md": {
        "title": "2026国考社工岗位报考条件与竞争分析",
        "desc": "2026年国考中社会工作相关岗位的报考条件、招录人数及竞争比全面分析，帮助考生了解岗位要求，合理选择报考职位，提高上岸概率。"
    },
    "content/guokao/2026-05-20-guokao-mianshi-beikao-zhinan.md": {
        "title": "2026国考面试备考指南：结构化面试高分技巧",
        "desc": "2026年国家公务员考试面试备考全攻略，涵盖结构化面试题型分析、答题框架、高分技巧及实战演练，助力考生面试脱颖而出。"
    },
    "content/guokao/2026-05-27-国考笔试成绩查询时间及入口.md": {
        "title": "2026国考笔试成绩查询时间及官方入口",
        "desc": "2026年国家公务员考试笔试成绩查询时间、官方查询入口及后续面试安排说明，帮助考生及时获取成绩信息，做好面试准备。"
    },
    "content/shanghai-shegong/2026-05-19-shanghai-shegong-xingce-30days.md": {
        "title": "上海社区工作者行测30天速成备考方案",
        "desc": "针对上海社区工作者招聘考试行测科目，制定30天速成备考方案，涵盖言语理解、数量关系、判断推理等模块的高效复习策略。"
    },
    "content/shanghai-shegong/2026-05-20-shanghai-shegong-daiku-fulishui.md": {
        "title": "上海社区工作者贷款、福利及税费待遇详解",
        "desc": "全面解读上海社区工作者的住房公积金贷款政策、福利待遇及个人所得税缴纳情况，帮助考生了解真实的工作待遇。"
    },
    "content/shanghai-shegong/2026-05-27-上海社区工作者各区招聘计划解读.md": {
        "title": "2026上海社区工作者各区招聘计划解读",
        "desc": "2026年上海市各区社区工作者招聘计划汇总解读，包括招录人数、报名条件、考试时间及薪资待遇，帮助考生选择合适区域报考。"
    },
    "content/shengkao/2026-05-19-shengkao-shegong-gangwei-xuanze.md": {
        "title": "2026省考社工岗位选择指南：条件与竞争分析",
        "desc": "2026年各省公务员考试中社会工作相关岗位的选择策略，分析报考条件、岗位特点及竞争情况，帮助考生做出最优报考决策。"
    },
    "content/shengkao/2026-05-27-省考联考省份及考试时间汇总.md": {
        "title": "2026省考联考省份及考试时间汇总",
        "desc": "2026年参加公务员联考省份名单及笔试时间汇总，帮助考生了解各省考试安排，合理规划跨省报考策略，把握每一次上岸机会。"
    },
    "content/zhenti-jiexi/2026-05-19-shegong-gongji-falv-changshi.md": {
        "title": "社区工作者公基法律常识高频考点解析",
        "desc": "社区工作者招聘考试中公共基础知识法律部分的高频考点解析，精选历年真题，帮助考生掌握法律常识重点，提升笔试成绩。"
    },
}

def replace_field(content, field, new_val):
    escaped = new_val.replace('"', '\\"')
    pattern = rf'(^|\n)({field}:\s*)"[^"]*"'
    replacement = rf'\1\2"{escaped}"'
    new_content = re.sub(pattern, replacement, content, count=1)
    # Also handle unquoted values
    if new_content == content:
        pattern2 = rf'(^|\n)({field}:\s*)([^\n]*)'
        replacement2 = rf'\1\2"{escaped}"'
        new_content = re.sub(pattern2, replacement2, new_content, count=1)
    return new_content

def fix_description(content, new_desc):
    escaped = new_desc.replace('"', '\\"')
    # Handle quoted description
    pattern = r'(^|\n)(description:\s*)"[^"]*"'
    replacement = rf'\1\2"{escaped}"'
    new_content = re.sub(pattern, replacement, content, count=1)
    if new_content == content:
        # Handle unquoted or partial description
        pattern2 = r'(^|\n)(description:\s*)([^\n]*)'
        replacement2 = rf'\1\2"{escaped}"'
        new_content = re.sub(pattern2, replacement2, new_content, count=1)
    return new_content

for filepath, data in fixes.items():
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = replace_field(content, "title", data["title"])
        new_content = fix_description(new_content, data["desc"])

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"FIXED: {filepath}")
    except Exception as e:
        print(f"ERROR: {filepath}: {e}")

print("\nDone!")
