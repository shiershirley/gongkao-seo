#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章发布后验证脚本
验证本地文件内容完整性 + 在线页面可访问性 + 配图加载
"""

import sys
import json
import urllib.request
import re
import argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"

def verify_local_file(filepath, min_words=1500, min_headings=3):
    """验证本地文章内容"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查字数
        word_count = len(content.replace(" ", "").replace("\n", ""))
        if word_count < min_words:
            return False, f"字数不足（{word_count}字 < {min_words}字）"

        # 检查frontmatter
        if not content.startswith("---"):
            return False, "缺少frontmatter"

        # 检查标题
        if "# " not in content:
            return False, "缺少文章标题"

        # 检查章节
        heading_count = content.count("\n## ")
        if heading_count < min_headings:
            return False, f"章节不足（{heading_count} < {min_headings}）"

        # 检查配图
        img_count = content.count("![")
        if img_count < 2:
            return False, f"配图不足（{img_count}张 < 2张）"

        # 检查总结
        if "## 总结" not in content:
            return False, "缺少总结章节"

        return True, f"验证通过（{word_count}字，{heading_count}章节，{img_count}张图）"
    except Exception as e:
        return False, f"验证失败: {e}"

def verify_online_article(url, check_images=True):
    """验证在线文章"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            status_code = resp.getcode()
            if status_code != 200:
                return False, f"HTTP {status_code}"

            html = resp.read().decode("utf-8", errors="ignore")

            # 检查标题
            title_match = re.search(r'<title>(.*?)</title>', html)
            if not title_match:
                return False, "页面标题缺失"

            # 检查日期格式（不应是时间戳）
            date_pattern = r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})'
            date_match = re.search(date_pattern, html)
            if date_match:
                date_str = date_match.group(1)
                if "T" in date_str or len(date_str) > 10:
                    return False, f"日期格式异常（{date_str}）"

            # 检查配图
            img_count = len(re.findall(r'<img[^>]+src="[^"]*images[^"]*"', html))
            if check_images and img_count < 2:
                return False, f"配图不足（{img_count}张 < 2张）"

            return True, f"在线验证通过（HTTP {status_code}，{img_count}张配图）"
    except Exception as e:
        return False, f"在线验证失败: {e}"

def main():
    parser = argparse.ArgumentParser(description="验证文章发布状态")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="验证指定日期的文章")
    parser.add_argument("--local-only", action="store_true", help="仅验证本地文件")
    parser.add_argument("--online-only", action="store_true", help="仅验证在线状态")
    parser.add_argument("--site-url", default="https://gk.edu-sjtu.cn", help="网站URL")
    args = parser.parse_args()

    date = args.date
    print(f"开始验证 {date} 的文章...")
    print("=" * 60)

    # 查找当日文章
    articles = []
    for category_dir in CONTENT_DIR.iterdir():
        if not category_dir.is_dir():
            continue
        for md_file in category_dir.glob(f"{date}*.md"):
            rel_path = md_file.relative_to(CONTENT_DIR)
            url_path = str(rel_path).replace(".md", "").replace("\\", "/")
            online_url = f"{args.site_url}/{url_path}"
            articles.append((md_file, rel_path, online_url))

    if not articles:
        print(f"未找到 {date} 的文章")
        return

    print(f"找到 {len(articles)} 篇文章，开始验证...\n")

    local_pass = 0
    local_fail = 0
    online_pass = 0
    online_fail = 0

    for idx, (filepath, rel_path, online_url) in enumerate(articles, 1):
        print(f"[{idx}/{len(articles)}] {rel_path}")

        # 本地验证
        if not args.online_only:
            is_valid, msg = verify_local_file(filepath)
            if is_valid:
                print(f"  ✅ 本地验证: {msg}")
                local_pass += 1
            else:
                print(f"  ❌ 本地验证失败: {msg}")
                local_fail += 1

        # 在线验证
        if not args.local_only:
            is_valid, msg = verify_online_article(online_url)
            if is_valid:
                print(f"  ✅ 在线验证: {msg}")
                online_pass += 1
            else:
                print(f"  ❌ 在线验证失败: {msg}")
                online_fail += 1

        print()

    # 统计
    print("=" * 60)
    print("验证结果统计:")
    if not args.online_only:
        print(f"  本地验证: 通过 {local_pass} 篇，失败 {local_fail} 篇")
    if not args.local_only:
        print(f"  在线验证: 通过 {online_pass} 篇，失败 {online_fail} 篇")

    # 生成报告
    report = {
        "date": date,
        "total": len(articles),
        "local_pass": local_pass,
        "local_fail": local_fail,
        "online_pass": online_pass,
        "online_fail": online_fail
    }

    report_file = PROJECT_ROOT / f"reports/verify_report_{date.replace('-', '')}.json"
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n验证报告已保存: {report_file}")

if __name__ == "__main__":
    main()
