#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO收录快速检查脚本 - 先全量Sitemap，再抽查搜索引擎
"""

import sys
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

import os
import re
import urllib.request
import urllib.parse
import time
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List, Dict, Optional

WEBSITE_URL = "https://gk.edu-sjtu.cn"
SITEMAP_URL = f"{WEBSITE_URL}/sitemap.xml"
CONTENT_DIR = Path("d:/AI/task/gongkao-seo/content")
REPORTS_DIR = Path("d:/AI/task/gongkao-seo/reports")


def parse_frontmatter(content: str) -> Optional[Dict]:
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    yaml_content = parts[1]
    result = {}
    for line in yaml_content.strip().split("\n"):
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key == "tags":
            if value.startswith("["):
                value = value.strip("[]")
            result[key] = [t.strip().strip('"').strip("'") for t in value.split(",") if t.strip()]
        else:
            result[key] = value
    return result


def get_articles(target_date: str) -> List[Dict]:
    articles = []
    for category_dir in sorted(CONTENT_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        for md_file in sorted(category_dir.glob("*.md")):
            if not md_file.name.startswith(target_date):
                continue
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                frontmatter = parse_frontmatter(content)
                if not frontmatter:
                    continue
                slug = md_file.stem
                category = category_dir.name
                articles.append({
                    "title": frontmatter.get("title", slug),
                    "url": f"{WEBSITE_URL}/{category}/{slug}",
                    "category": category,
                    "date": frontmatter.get("date", ""),
                })
            except Exception as e:
                print(f"⚠️  读取失败 {md_file}: {e}")
    return articles


def get_sitemap_urls() -> set:
    try:
        req = urllib.request.Request(SITEMAP_URL, headers={"User-Agent": "SEO-Checker/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            sitemap = resp.read().decode("utf-8", errors="ignore")
        urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
        print(f"📡 Sitemap 包含 {len(urls)} 条 URL")
        return urls
    except Exception as e:
        print(f"⚠️  无法获取 sitemap: {e}")
        return set()


def check_engine(url: str, engine: str) -> Dict:
    query = f"site:{url}"
    if engine == "Bing":
        search_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    elif engine == "百度":
        search_url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}"
    elif engine == "Google":
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    else:
        return {"indexed": None, "note": f"未知引擎: {engine}"}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    domain = "gk.edu-sjtu.cn"
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            final_url = resp.geturl()

        captcha_hints = ["wappass.baidu.com", "百度安全验证", "请输入验证码", "captcha", "access denied", "请点击下方图形"]
        if any(h in final_url.lower() or h in html for h in captcha_hints):
            return {"indexed": None, "note": f"{engine}: 反爬拦截"}

        no_result_hints = ["no results", "没有与此相关的结果", "未找到结果", "没有找到结果", "did not match any documents", "没有找到和查询"]
        if any(h in html.lower() for h in no_result_hints):
            return {"indexed": False, "note": f"{engine}: 无结果"}

        if domain in html:
            return {"indexed": True, "note": f"{engine}: 已收录"}
        else:
            return {"indexed": False, "note": f"{engine}: 未出现"}
    except Exception as e:
        err = str(e)[:60]
        return {"indexed": None, "note": f"{engine}: 失败({err})"}


def icon(val):
    if val is True: return "✅"
    if val is False: return "❌"
    return "⚠️"


def generate_report(articles, engine_results, sitemap_urls, target_date, days_ago):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# SEO收录检查报告 — {target_date}",
        "",
        f"**检查时间**: {now_str}",
        f"**目标日期**: {target_date}（{days_ago}天前发布）",
        f"**网站地址**: {WEBSITE_URL}",
        f"**检查文章数**: {len(articles)}",
        f"**搜索引擎检查**: 抽查 {len(engine_results)} 篇（每篇 Bing + 百度 + Google）",
        "",
        "## 详细检查结果",
        "",
        "| 标题 | 分类 | Sitemap | Bing | 百度 | Google |",
        "|------|------|---------|------|------|--------|",
    ]

    sitemap_indexed = 0
    bing_indexed = 0
    baidu_indexed = 0
    google_indexed = 0
    not_in_sitemap = []

    for article in articles:
        url = article["url"]
        in_sitemap = url in sitemap_urls
        # 兼容 path 匹配
        if not in_sitemap:
            path = url.replace(WEBSITE_URL, "").strip("/")
            in_sitemap = any(path in u or url in u for u in sitemap_urls)

        result = engine_results.get(url, {})
        bing = result.get("bing", {}).get("indexed")
        baidu = result.get("baidu", {}).get("indexed")
        google = result.get("google", {}).get("indexed")

        if in_sitemap:
            sitemap_indexed += 1
        else:
            not_in_sitemap.append(article)
        if bing is True: bing_indexed += 1
        if baidu is True: baidu_indexed += 1
        if google is True: google_indexed += 1

        title = article['title'][:28] + "..." if len(article['title']) > 28 else article['title']
        title_link = f"[{title}]({url})"
        lines.append(f"| {title_link} | {article['category']} | {icon(in_sitemap)} | {icon(bing)} | {icon(baidu)} | {icon(google)} |")

    lines.append("")

    if not_in_sitemap:
        lines.append("## ⚠️ 未出现在 Sitemap 的文章")
        lines.append("")
        lines.append("> 这些文章需要确认 Vercel 部署是否成功、sitemap.xml 是否已更新。")
        lines.append("")
        for a in not_in_sitemap:
            lines.append(f"- [{a['title']}]({a['url']})")
        lines.append("")

    total = len(articles)
    pct = lambda n: f"{round(n/total*100)}%" if total else "0%"

    def count_results(key, value):
        return sum(1 for a in articles if engine_results.get(a["url"], {}).get(key, {}).get("indexed") is value)

    lines.append("## 📊 收录统计汇总")
    lines.append("")
    lines.append("| 搜索引擎 | 已收录 ✅ | 未收录 ❌ | 无法判断 ⚠️ | 收录率 |")
    lines.append("|---------|----------|----------|------------|--------|")
    lines.append(f"| Sitemap | {sitemap_indexed} 篇 | {total - sitemap_indexed} 篇 | 0 篇 | {pct(sitemap_indexed)} |")
    lines.append(f"| Bing    | {bing_indexed} 篇 | {count_results('bing', False)} 篇 | {count_results('bing', None)} 篇 | {pct(bing_indexed)} |")
    lines.append(f"| 百度    | {baidu_indexed} 篇 | {count_results('baidu', False)} 篇 | {count_results('baidu', None)} 篇 | {pct(baidu_indexed)} |")
    lines.append(f"| Google  | {google_indexed} 篇 | {count_results('google', False)} 篇 | {count_results('google', None)} 篇 | {pct(google_indexed)} |")
    lines.append("")
    lines.append("> **图例说明**：✅ 确认已收录 | ❌ 确认未收录 | ⚠️ 反爬拦截/网络限制，无法判断，需手动确认")
    lines.append("")

    lines.append("## 💡 优化建议")
    lines.append("")
    suggest_no = 1
    if not_in_sitemap:
        lines.append(f"{suggest_no}. **{len(not_in_sitemap)} 篇未出现在 Sitemap**：检查 Vercel 部署日志，确认对应页面已成功生成。")
        suggest_no += 1
    if bing_indexed < len(engine_results):
        lines.append(f"{suggest_no}. **Bing 收录率 {pct(bing_indexed)}**：可登录 Bing Webmaster Tools 手动提交 sitemap，或使用 IndexNow 协议加速收录。")
        suggest_no += 1
    if baidu_indexed < len(engine_results):
        lines.append(f"{suggest_no}. **百度收录率 {pct(baidu_indexed)}**：百度对新站收录较慢（通常7-30天），建议开通百度搜索资源平台并主动推送 URL。注意：百度反爬较强，⚠️ 不代表一定未收录，建议手动在百度搜索 `site:gk.edu-sjtu.cn` 二次确认。")
        suggest_no += 1
    if google_indexed < len(engine_results):
        lines.append(f"{suggest_no}. **Google 收录率 {pct(google_indexed)}**：登录 Google Search Console 提交 sitemap，可使用 URL 检查工具请求收录。注意：Google 在国内访问受限，⚠️ 可能为网络原因导致，非真实未收录。")
        suggest_no += 1
    lines.append(f"{suggest_no}. **持续监测**：建议在发布后 7、14、30 天各做一次收录检查，追踪趋势。")
    lines.append("")

    return "\n".join(lines)


def main():
    target_date = (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")
    days_ago = 10

    print(f"\n🔍 SEO收录检查启动")
    print(f"   目标日期：{target_date}（{days_ago} 天前发布）")
    print(f"   网站地址：{WEBSITE_URL}\n")

    articles = get_articles(target_date)

    if not articles:
        print(f"⚠️  未找到 {target_date} 发布的文章")
        available = set()
        cutoff = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        for category_dir in CONTENT_DIR.iterdir():
            if not category_dir.is_dir():
                continue
            for md_file in category_dir.glob("*.md"):
                name = md_file.stem
                if name[:10] >= cutoff and name[:10].replace('-', '').isdigit():
                    available.add(name[:10])
        if available:
            fallback = min(sorted(available, reverse=True), key=lambda d: abs((datetime.strptime(d, "%Y-%m-%d").date() - datetime.strptime(target_date, "%Y-%m-%d").date()).days))
            days_ago = (date.today() - datetime.strptime(fallback, "%Y-%m-%d").date()).days
            print(f"📅 回退到最近可用日期：{fallback}（{days_ago}天前）")
            articles = get_articles(fallback)
            target_date = fallback
        else:
            print("❌ 未找到任何文章")
            return

    print(f"📄 找到 {len(articles)} 篇文章")
    print("📡 获取 sitemap.xml...")

    sitemap_urls = get_sitemap_urls()

    # 检查所有文章是否在sitemap中
    sitemap_count = 0
    for article in articles:
        url = article["url"]
        path = url.replace(WEBSITE_URL, "").strip("/")
        in_sitemap = url in sitemap_urls or any(path in u or url in u for u in sitemap_urls)
        if in_sitemap:
            sitemap_count += 1
    print(f"   {sitemap_count}/{len(articles)} 篇文章在 Sitemap 中\n")

    # 抽查搜索引擎：每类选最多3篇，总共不超过15篇
    print("🔍 抽查搜索引擎收录（每分类最多3篇）...")
    sampled = []
    by_category = {}
    for a in articles:
        by_category.setdefault(a["category"], []).append(a)

    for cat, items in by_category.items():
        sampled.extend(items[:3])

    # 如果总样本超过20篇，随机采样
    if len(sampled) > 20:
        import random
        random.seed(42)
        sampled = random.sample(sampled, 20)

    print(f"   选中 {len(sampled)} 篇文章进行搜索引擎检查\n")

    engine_results = {}
    for i, article in enumerate(sampled, 1):
        url = article["url"]
        print(f"  [{i}/{len(sampled)}] {article['title'][:30]}...")

        bing = check_engine(url, "Bing")
        time.sleep(1)
        baidu = check_engine(url, "百度")
        time.sleep(1)
        google = check_engine(url, "Google")
        time.sleep(1)

        engine_results[url] = {"bing": bing, "baidu": baidu, "google": google}
        print(f"         Bing:{icon(bing['indexed'])} 百度:{icon(baidu['indexed'])} Google:{icon(google['indexed'])}")

    print("\n📊 生成报告...")
    report = generate_report(articles, engine_results, sitemap_urls, target_date, days_ago)

    REPORTS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_label = target_date.replace("-", "")
    report_file = REPORTS_DIR / f"indexing_check_{date_label}_{ts}.md"
    report_file.write_text(report, encoding="utf-8")

    print(f"\n✅ 报告已保存：{report_file}")
    print(f"\n📋 报告预览（前20行）：")
    for line in report.split("\n")[:20]:
        print(line)


if __name__ == "__main__":
    main()
