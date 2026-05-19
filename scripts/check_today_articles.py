#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查今天生成文章的 frontmatter 格式"""
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"

today = datetime.now().strftime("%Y-%m-%d")
errors = []
warnings = []

print(f"检查 {today} 生成的文章...")

for md_file in CONTENT_DIR.rglob(f"{today}-*.md"):
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            errors.append(f"[格式错误] {md_file.name}: 缺少 frontmatter")
            continue
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            errors.append(f"[格式错误] {md_file.name}: frontmatter 不完整")
            continue
        
        fm_text = parts[1]
        
        # 检查必填字段
        for field in ['title', 'date', 'category', 'tags', 'author']:
            pattern = re.compile(rf'^{field}\s*:', re.MULTILINE)
            if not pattern.search(fm_text):
                errors.append(f"[缺少字段] {md_file.name}: 缺少 {field}")
        
        # 检查 description 内嵌英文双引号
        desc_match = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE | re.DOTALL)
        if desc_match:
            desc = desc_match.group(1)
            if '"' in desc:
                errors.append(f"[引号错误] {md_file.name}: description 包含未转义英文双引号")
        
        # 检查日期格式
        date_match = re.search(r'^date:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)
        if date_match:
            date_val = date_match.group(1).strip()
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
                errors.append(f"[日期格式] {md_file.name}: 日期格式错误 {date_val}")
        
        print(f"  ✓ {md_file.name}")
        
    except Exception as e:
        errors.append(f"[读取失败] {md_file.name}: {e}")

print(f"\n检查完成，共发现 {len(errors)} 个问题，{len(warnings)} 个警告")
for e in errors:
    print(f"  ❌ {e}")
for w in warnings:
    print(f"  ⚠️ {w}")

if not errors and not warnings:
    print("✅ 所有文章 frontmatter 格式正确！")
