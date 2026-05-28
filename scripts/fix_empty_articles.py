#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复内容为空的文章"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from auto_gen_daily import generate_article_content

fixes = [
    {
        "path": PROJECT_ROOT / "content/guokao/2026-05-28-guokao-strategy.md",
        "title": "国考零基础备考攻略2026：从入门到上岸的180天系统规划",
        "keyword": "国考备考攻略",
        "category": "guokao",
        "angle": "零基础"
    },
    {
        "path": PROJECT_ROOT / "content/guokao/2026-05-28-guokao-tips.md",
        "title": "国考行测高频考点2026：近5年真题数据分析与命题趋势",
        "keyword": "国考行测",
        "category": "guokao",
        "angle": "高分"
    },
    {
        "path": PROJECT_ROOT / "content/shengkao/2026-05-28-shengkao-preparation.md",
        "title": "省考申论写作技巧2026：高分作文结构与论点提炼方法",
        "keyword": "省考申论",
        "category": "shengkao",
        "angle": "面试"
    },
    {
        "path": PROJECT_ROOT / "content/shengkao/2026-05-28-shengkao-review.md",
        "title": "省考真题解析2026：近年真题回顾与2026备考重点",
        "keyword": "省考真题",
        "category": "shengkao",
        "angle": "差异"
    }
]

for fix in fixes:
    fpath = fix["path"]
    if not fpath.exists():
        print(f"❌ 文件不存在: {fpath}")
        continue
    
    # 读取原文件保留frontmatter
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        frontmatter = "---" + parts[1] + "---\n"
    else:
        frontmatter = ""
    
    # 生成新正文
    new_body = generate_article_content(
        fix["title"],
        fix["keyword"],
        fix["category"],
        fix["angle"]
    )
    
    # 写入文件
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(frontmatter + "\n" + new_body)
    
    print(f"✅ 已修复: {fpath.name}")

print("\n修复完成！")
