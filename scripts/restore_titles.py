#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量恢复被 d20f2d4 提交损坏的文章 frontmatter。
从 2123db8 (d20f2d4^) 版本中提取正确的 title 和 description，恢复到当前版本。
"""

import subprocess
import re
import os
from pathlib import Path
from collections import Counter

GOOD_COMMIT = "2123db8ae0d372f312c7b4b16888515434108732"  # d20f2d4^
CONTENT_DIR = Path("content")

def find_bad_files():
    """找到所有标题长度小于10的文章"""
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANG'] = 'en_US.UTF-8'

    result = subprocess.run(
        ["grep", "-rn", '^title: "', str(CONTENT_DIR)],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        env=env
    )
    if result.returncode != 0 and not result.stdout:
        print(f"grep stderr: {result.stderr}")
        return []

    bad_files = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        # line format: filepath:lineno:content
        # Find first two colons to split filepath and content
        first_colon = line.find(":")
        if first_colon == -1:
            continue
        second_colon = line.find(":", first_colon + 1)
        if second_colon == -1:
            continue
        filepath = line[:first_colon]
        content = line[second_colon + 1:]

        m = re.search(r'title:\s*"([^"]*)"', content)
        if m:
            title = m.group(1)
            if len(title) < 10:
                bad_files.append(filepath)
    return list(set(bad_files))  # 去重


def get_file_from_commit(filepath, commit):
    """从指定提交获取文件内容"""
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{filepath}"],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        if result.returncode == 0:
            return result.stdout
    except Exception as e:
        print(f"git show error for {filepath}: {e}")
    return None


def extract_frontmatter(content):
    """提取 frontmatter 中的 title 和 description"""
    title_match = re.search(r'^title:\s*"([^"]*)"', content, re.MULTILINE)
    desc_match = re.search(r'^description:\s*"([^"]*)"', content, re.MULTILINE)
    title = title_match.group(1) if title_match else None
    desc = desc_match.group(1) if desc_match else None
    return title, desc


def replace_frontmatter_field(content, field, new_val):
    """替换 frontmatter 中的某个字段值"""
    if not content.startswith("---\n"):
        return content
    end = content.find("\n---", 4)
    if end == -1:
        return content
    fm = content[:end+4]
    body = content[end+4:]

    # Escape quotes in new_val for regex replacement
    escaped_val = new_val.replace('"', '\\"')
    pattern = rf'(^|\n)({field}:\s*)"[^"]*"'
    replacement = rf'\1\2"{escaped_val}"'
    new_fm = re.sub(pattern, replacement, fm, count=1)
    return new_fm + body


def main():
    bad_files = find_bad_files()
    print(f"找到 {len(bad_files)} 篇标题异常的文章")

    cats = [f.split("/")[1] for f in bad_files if len(f.split("/")) > 1]
    for cat, cnt in Counter(cats).most_common():
        print(f"  {cat}: {cnt}")

    restored = 0
    skipped = 0
    failed = 0

    for filepath in bad_files:
        # 读取当前文件
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                current = f.read()
        except Exception as e:
            print(f"ERROR reading {filepath}: {e}")
            failed += 1
            continue

        # 从旧提交获取文件
        old_content = get_file_from_commit(filepath, GOOD_COMMIT)
        if old_content is None:
            print(f"SKIP {filepath}: not found in {GOOD_COMMIT}")
            skipped += 1
            continue

        old_title, old_desc = extract_frontmatter(old_content)
        cur_title, cur_desc = extract_frontmatter(current)

        if not old_title or len(old_title) < 10:
            print(f"SKIP {filepath}: old title also bad: '{old_title}'")
            skipped += 1
            continue

        new_content = current
        # 替换 title
        new_content = replace_frontmatter_field(new_content, "title", old_title)
        # 替换 description（如果旧的也有且比当前好）
        if old_desc and len(old_desc) > 10 and cur_desc and len(cur_desc) < 10:
            new_content = replace_frontmatter_field(new_content, "description", old_desc)

        # 写回文件
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            restored += 1
            if restored % 50 == 0:
                print(f"  Progress: {restored}/{len(bad_files)} restored...")
        except Exception as e:
            print(f"ERROR writing {filepath}: {e}")
            failed += 1

    print(f"\nDone! Restored: {restored}, Skipped: {skipped}, Failed: {failed}")


if __name__ == "__main__":
    main()
