#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面恢复 frontmatter 被损坏的文章。
处理以下异常情况：
- title 为空值（title: 后面无内容）
- title 为异常短字符串
- description 为空或异常短
"""

import subprocess
import re
import os
from pathlib import Path
from collections import Counter

GOOD_COMMIT = "2123db8ae0d372f312c7b4b16888515434108732"
CONTENT_DIR = Path("content")

def get_all_md_files():
    """获取所有 markdown 文件"""
    files = []
    for root, _, filenames in os.walk(CONTENT_DIR):
        for f in filenames:
            if f.endswith(".md"):
                files.append(os.path.join(root, f))
    return files


def get_file_from_commit(filepath, commit):
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{filepath}"],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass
    return None


def extract_frontmatter(content):
    """提取 frontmatter 字段"""
    if not content.startswith("---\n"):
        return None, None, None, None, None
    end = content.find("\n---", 4)
    if end == -1:
        return None, None, None, None, None
    fm = content[:end+4]

    title_match = re.search(r'^title:\s*(.*)', fm, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.*)', fm, re.MULTILINE)
    date_match = re.search(r'^date:\s*(.*)', fm, re.MULTILINE)
    cat_match = re.search(r'^category:\s*(.*)', fm, re.MULTILINE)
    author_match = re.search(r'^author:\s*(.*)', fm, re.MULTILINE)

    def clean(v):
        if v is None:
            return None
        v = v.strip()
        v = v.strip('"').strip("'")
        return v if v else None

    return clean(title_match.group(1) if title_match else None), \
           clean(desc_match.group(1) if desc_match else None), \
           clean(date_match.group(1) if date_match else None), \
           clean(cat_match.group(1) if cat_match else None), \
           clean(author_match.group(1) if author_match else None)


def rebuild_frontmatter(title, desc, date, category, author, tags, body):
    """重建完整的 frontmatter"""
    # 确保 tags 是列表格式
    if isinstance(tags, str):
        tags = [t.strip().strip('"').strip("'") for t in tags.split(",") if t.strip()]
    tags_str = ", ".join(f'"{t}"' for t in tags if t)

    fm_lines = ["---"]
    fm_lines.append(f'title: "{title}"')
    if desc:
        fm_lines.append(f'description: "{desc}"')
    if date:
        fm_lines.append(f'date: "{date}"')
    if category:
        fm_lines.append(f'category: "{category}"')
    if tags_str:
        fm_lines.append(f'tags: [{tags_str}]')
    if author:
        fm_lines.append(f'author: "{author}"')
    fm_lines.append("---")

    return "\n".join(fm_lines) + "\n" + body


def main():
    files = get_all_md_files()
    print(f"共 {len(files)} 篇文章")

    bad_files = []
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                current = f.read()
        except Exception:
            continue

        title, desc, date, category, author = extract_frontmatter(current)

        # 判断是否需要修复
        needs_fix = False
        if not title or len(title) < 10:
            needs_fix = True
        if not desc or len(desc) < 10:
            needs_fix = True

        if needs_fix:
            bad_files.append(filepath)

    print(f"找到 {len(bad_files)} 篇 frontmatter 异常的文章")

    cats = [f.split("/")[1] for f in bad_files if len(f.split("/")) > 1]
    for cat, cnt in Counter(cats).most_common():
        print(f"  {cat}: {cnt}")

    restored = 0
    skipped = 0
    failed = 0
    no_old = 0

    for filepath in bad_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                current = f.read()
        except Exception as e:
            print(f"ERROR reading {filepath}: {e}")
            failed += 1
            continue

        # 获取旧版本
        old_content = get_file_from_commit(filepath, GOOD_COMMIT)
        if old_content is None:
            no_old += 1
            # 尝试从文件名生成标题
            title, desc, date, category, author = extract_frontmatter(current)
            slug = Path(filepath).stem
            # 从 slug 生成标题
            generated_title = slug.replace("-", " ").replace("_", " ")
            if len(generated_title) > 5 and (not title or len(title) < 3):
                # 简单替换 frontmatter 中的 title
                new_fm = re.sub(
                    r'(^title:\s*)"?[^"\n]*"?',
                    rf'\1"{generated_title}"',
                    current,
                    count=1,
                    flags=re.MULTILINE
                )
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_fm)
                restored += 1
            else:
                skipped += 1
            continue

        old_title, old_desc, old_date, old_cat, old_author = extract_frontmatter(old_content)
        cur_title, cur_desc, cur_date, cur_cat, cur_author = extract_frontmatter(current)

        # 提取正文
        body_match = re.search(r'\n---\n(.*)', current, re.DOTALL)
        body = body_match.group(1) if body_match else ""

        # 提取当前 tags
        tags_match = re.search(r'^tags:\s*(.*)', current, re.MULTILINE)
        tags = tags_match.group(1) if tags_match else ""

        # 使用旧值或当前值中更好的
        final_title = old_title if old_title and len(old_title) >= 10 else cur_title
        final_desc = old_desc if old_desc and len(old_desc) >= 10 else cur_desc
        final_date = old_date if old_date else cur_date
        final_cat = old_cat if old_cat else cur_cat
        final_author = old_author if old_author else (cur_author or "公考助手")

        if not final_title or len(final_title) < 5:
            # 从文件名生成
            slug = Path(filepath).stem
            final_title = slug.replace("-", " ").replace("_", " ")

        new_content = rebuild_frontmatter(
            final_title, final_desc, final_date, final_cat, final_author, tags, body
        )

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            restored += 1
            if restored % 50 == 0:
                print(f"  Progress: {restored}/{len(bad_files)} restored...")
        except Exception as e:
            print(f"ERROR writing {filepath}: {e}")
            failed += 1

    print(f"\nDone! Restored: {restored}, No old version: {no_old}, Skipped: {skipped}, Failed: {failed}")


if __name__ == "__main__":
    main()
