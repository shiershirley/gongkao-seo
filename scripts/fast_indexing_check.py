#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速SEO收录检查 - 仅检查Sitemap和Bing"""
import sys
import os
import re
import urllib.request
import urllib.parse
from datetime import datetime, date, timedelta
from pathlib import Path

# 全局socket超时
import socket
socket.setdefaulttimeout(5)

WEBSITE_URL = "https://gk.edu-sjtu.cn"
SITEMAP_URL = f"{WEBSITE_URL}/sitemap.xml"
CONTENT_DIR = Path("d:/AI/task/gongkao-seo/content")
REPORTS_DIR = Path("d:/AI/task/gongkao-seo/reports")

def compute_target_date(days_ago):
    target = date.today() - timedelta(days=days_ago)
    return target.strftime("%Y-%m-%d")

def extract_articles(date_str):
    articles = []
    for category_dir in sorted(CONTENT_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        for md_file in sorted(category_dir.glob("*.md")):
            if not md_file.name.startswith(date_str):
                continue
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if not content.startswith("---"):
                    continue
                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue
                yaml_content = parts[1]
                frontmatter = {}
                for line in yaml_content.strip().split("\n"):
                    if ":" not in line:
                        continue
                    key, _, value = line.partition(":")
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")
                
                slug = md_file.stem
                category = category_dir.name
                article_url = f"{WEBSITE_URL}/{category}/{slug}"
                articles.append({
                    "title": frontmatter.get("title", slug),
                    "url": article_url,
                    "category": category,
                    "date": frontmatter.get("date", ""),
                })
            except Exception as e:
                print(f"  Error reading {md_file}: {e}")
    return articles

def check_bing(url):
    try:
        query = f"site:{url}"
        search_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        if "gk.edu-sjtu.cn" in html:
            return True, "域名出现在结果页"
        return False, "未出现"
    except Exception as e:
        return None, f"查询失败({str(e)[:40]})"

def main():
    target = compute_target_date(10)
    print(f"Target date: {target}")
    
    articles = extract_articles(target)
    print(f"Found {len(articles)} articles")
    
    if not articles:
        print("No articles found")
        return
    
    # 获取sitemap
    print("Fetching sitemap...")
    sitemap_urls = set()
    try:
        req = urllib.request.Request(SITEMAP_URL, headers={"User-Agent": "SEO-Checker/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            sitemap_content = resp.read().decode("utf-8", errors="ignore")
        sitemap_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap_content))
        print(f"Sitemap has {len(sitemap_urls)} URLs")
    except Exception as e:
        print(f"Sitemap error: {e}")
    
    # 检查每篇文章
    results = []
    for i, article in enumerate(articles, 1):
        url = article["url"]
        title = article["title"][:30]
        print(f"  [{i}/{len(articles)}] {title}...", end=" ", flush=True)
        
        in_sitemap = url in sitemap_urls
        bing_status, bing_note = check_bing(url)
        
        s_icon = "Y" if in_sitemap else "N"
        b_icon = "Y" if bing_status is True else ("N" if bing_status is False else "?")
        print(f"S:{s_icon} B:{b_icon}")
        
        results.append({
            "article": article,
            "in_sitemap": in_sitemap,
            "bing": bing_status,
            "bing_note": bing_note,
        })
    
    # 生成报告
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append(f"# SEO收录检查报告 — {target}")
    lines.append("")
    lines.append(f"**检查时间**: {now_str}")
    lines.append(f"**目标日期**: {target}（10天前发布）")
    lines.append(f"**网站地址**: {WEBSITE_URL}")
    lines.append(f"**检查文章数**: {len(articles)}")
    lines.append("")
    lines.append("## 详细检查结果")
    lines.append("")
    lines.append("| 标题 | 分类 | Sitemap | Bing |")
    lines.append("|------|------|---------|------|")
    
    sitemap_ok = 0
    bing_ok = 0
    not_in_sitemap = []
    
    for r in results:
        a = r["article"]
        s = "✅" if r["in_sitemap"] else "❌"
        b = "✅" if r["bing"] is True else ("❌" if r["bing"] is False else "⚠️")
        if r["in_sitemap"]:
            sitemap_ok += 1
        else:
            not_in_sitemap.append(a)
        if r["bing"] is True:
            bing_ok += 1
        
        title = a["title"]
        if len(title) > 28:
            title = title[:28] + "..."
        lines.append(f"| [{title}]({a['url']}) | {a['category']} | {s} | {b} |")
    
    lines.append("")
    
    if not_in_sitemap:
        lines.append("## ⚠️ 未出现在 Sitemap 的文章")
        lines.append("")
        for a in not_in_sitemap:
            lines.append(f"- [{a['title']}]({a['url']})")
        lines.append("")
    
    lines.append("## 📊 收录统计汇总")
    lines.append("")
    lines.append(f"| 搜索引擎 | 已收录 | 未收录 | 无法判断 | 收录率 |")
    lines.append(f"|----------|--------|--------|----------|--------|")
    lines.append(f"| Sitemap | {sitemap_ok} 篇 | {len(articles)-sitemap_ok} 篇 | 0 篇 | {round(sitemap_ok/len(articles)*100)}% |")
    lines.append(f"| Bing | {bing_ok} 篇 | {sum(1 for r in results if r['bing'] is False)} 篇 | {sum(1 for r in results if r['bing'] is None)} 篇 | {round(bing_ok/len(articles)*100)}% |")
    lines.append("")
    
    # 保存报告
    REPORTS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_label = target.replace("-", "")
    report_file = REPORTS_DIR / f"indexing_check_{date_label}_{ts}.md"
    report_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport saved: {report_file}")

if __name__ == "__main__":
    main()
