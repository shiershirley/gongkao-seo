#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理现有文章，添加FAQ和CTA区块
- 为每篇文章提取/生成FAQ（结构化数据）
- 为每篇文章添加分类对应的CTA区块
- 支持预览模式（--apply 参数执行）
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "content"
SCRIPTS_DIR = ROOT / "scripts"

# 导入所需函数
sys.path.insert(0, str(SCRIPTS_DIR))
from auto_gen_articles_v3 import (
    generate_ctr_title,
    extract_faq_from_content,
    generate_faq_section,
    generate_cta_section,
    generate_article_md
)

def add_faq_cta_to_article(md_path, apply=False):
    """为单篇文章添加FAQ和CTA"""
    try:
        content = md_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"读取失败: {e}"

    # 检查是否已添加过
    if '## 常见问题（FAQ）' in content or 'class="cta-section"' in content:
        return False, "已包含FAQ或CTA，跳过"

    # 提取文章信息
    # 从frontmatter提取信息
    fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return False, "无frontmatter，跳过"

    fm_text = fm_match.group(1)
    # 提取category
    cat_match = re.search(r'category:\s*"([^"]+)"', fm_text)
    category = cat_match.group(1) if cat_match else "beikao-zhinan"

    # 提取tags
    tags_match = re.search(r'tags:\s*(\[.*?\])', fm_text, re.DOTALL)
    tags = []
    if tags_match:
        try:
            tags = json.loads(tags_match.group(1))
        except:
            pass

    # 提取desc
    desc_match = re.search(r'description:\s*"([^"]+)"', fm_text)
    desc = desc_match.group(1) if desc_match else ""

    # 提取正文内容（去掉frontmatter）
    body = content[content.find('---', 4)+3:]

    # 1. 生成FAQ
    faq_list = extract_faq_from_content(body + "\n" + desc)
    faq_section = ""
    if faq_list:
        faq_section = generate_faq_section(faq_list)

    # 2. 生成CTA
    cta_section = generate_cta_section(category)

    # 插入位置：在"---*本文仅供参考"之前
    insert_pos = content.rfind('---\n*本文仅供参考')
    if insert_pos == -1:
        insert_pos = content.rfind('*本文仅供参考')
    if insert_pos == -1:
        # 如果找不到，追加到末尾
        new_content = content + "\n" + faq_section + "\n" + cta_section
    else:
        new_content = content[:insert_pos] + faq_section + "\n" + cta_section + "\n" + content[insert_pos:]

    if apply:
        try:
            md_path.write_text(new_content, encoding='utf-8')
            return True, f"已添加FAQ({len(faq_list)}个)和CTA"
        except Exception as e:
            return False, f"写入失败: {e}"
    else:
        return True, f"预览：将添加FAQ({len(faq_list)}个)和CTA（未执行）"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="批量添加FAQ和CTA到现有文章")
    parser.add_argument('--apply', action='store_true', help='执行修改（默认只预览）')
    parser.add_argument('--limit', type=int, default=0, help='限制处理数量（0=全部）')
    args = parser.parse_args()

    # 查找所有md文件
    md_files = list(CONTENT_DIR.glob('**/*.md'))
    print(f"{'='*60}")
    print(f"批量处理工具：添加FAQ和CTA")
    print(f"{'='*60}")
    print(f"找到 {len(md_files)} 篇文章")
    if not args.apply:
        print("[预览模式] 添加 --apply 参数执行实际修改")
    print()

    if args.limit > 0:
        md_files = md_files[:args.limit]
        print(f"限制处理前 {args.limit} 篇")
        print()

    success = 0
    skipped = 0
    failed = 0

    for i, md_path in enumerate(md_files, 1):
        rel_path = md_path.relative_to(ROOT)
        print(f"[{i}/{len(md_files)}] {rel_path}...", end=' ')

        ok, msg = add_faq_cta_to_article(md_path, apply=args.apply)
        if ok:
            if '已包含' in msg:
                print(f"[跳过] {msg}")
                skipped += 1
            else:
                print(f"[成功] {msg}")
                success += 1
        else:
            print(f"[失败] {msg}")
            failed += 1

    print()
    print(f"{'='*60}")
    print(f"处理完成：")
    print(f"  成功：{success} 篇")
    print(f"  跳过：{skipped} 篇（已包含FAQ/CTA）")
    print(f"  失败：{failed} 篇")
    print(f"{'='*60}")

    if not args.apply and success > 0:
        print()
        print("[预览模式] 未实际修改文件")
        print("  执行命令添加 --apply 参数：")
        print(f"  python {Path(__file__).name} --apply")


if __name__ == '__main__':
    main()
