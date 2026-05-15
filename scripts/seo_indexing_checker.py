#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO收录检查脚本 - 用于检查文章在各搜索引擎的收录情况

使用方法:
    python scripts/seo_indexing_checker.py                    # 检查10天前发布的文章
    python scripts/seo_indexing_checker.py --days-ago 7       # 检查7天前发布的文章
    python scripts/seo_indexing_checker.py --date 2026-05-05  # 检查指定日期文章
    python scripts/seo_indexing_checker.py --all              # 检查全部文章（慎用）
    python scripts/seo_indexing_checker.py --check-only       # 仅检查不生成报告

说明:
    - 新文章通常需要 3-14 天被收录，因此默认检查 10 天前的文章
    - 收录检查通过 Bing IndexNow API + 模拟 site: 查询实现
    - 报告保存在 reports/ 目录下，文件名带时间戳
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import urllib.request
import urllib.parse
import time

# 配置
WEBSITE_URL = "https://gk.edu-sjtu.cn"
SITEMAP_URL = f"{WEBSITE_URL}/sitemap.xml"
CONTENT_DIR = Path("d:/AI/task/gongkao-seo/content")
REPORTS_DIR = Path("d:/AI/task/gongkao-seo/reports")
DEFAULT_DAYS_AGO = 10  # 默认检查N天前发布的文章


# 搜索引擎检查配置
SEARCH_ENGINES = {
    "Bing": {
        "search_url": "https://www.bing.com/search?q={query}",
        "site_query": "site:gk.edu-sjtu.cn {keyword}",
        "check_regex": r"gk\.edu-sjtu\.cn[^\s<>\"']*"
    },
    "Google": {
        "search_url": "https://www.google.com/search?q={query}",
        "site_query": "site:gk.edu-sjtu.cn {keyword}",
        "check_regex": r"gk\.edu-sjtu\.cn[^\s<>\"']*"
    },
    "百度": {
        "search_url": "https://www.baidu.com/s?wd={query}",
        "site_query": "site:gk.edu-sjtu.cn {keyword}",
        "check_regex": r"gk\.edu-sjtu\.cn[^\s<>\"']*"
    },
}


def compute_target_date(days_ago: int) -> str:
    """计算 N 天前的日期字符串 YYYY-MM-DD"""
    target = date.today() - timedelta(days=days_ago)
    return target.strftime("%Y-%m-%d")


class SEOIndexingChecker:
    def __init__(self, website_url: str = WEBSITE_URL):
        self.website_url = website_url
        self.results = []

    def extract_articles_from_content(
        self,
        date_str: Optional[str] = None,
        check_all: bool = False
    ) -> List[Dict]:
        """
        从 content 目录提取文章信息。
        - date_str: 精确日期（YYYY-MM-DD），只匹配该日期发布的文章
        - check_all: 如果为 True，提取全部文章（忽略 date_str）
        """
        articles = []

        if not CONTENT_DIR.exists():
            print(f"❌ 内容目录不存在: {CONTENT_DIR}")
            return articles

        for category_dir in sorted(CONTENT_DIR.iterdir()):
            if not category_dir.is_dir():
                continue

            for md_file in sorted(category_dir.glob("*.md")):
                # 日期过滤（文件名以 YYYY-MM-DD- 开头）
                if not check_all and date_str:
                    if not md_file.name.startswith(date_str):
                        continue

                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    frontmatter = self._parse_frontmatter(content)
                    if not frontmatter:
                        continue

                    slug = md_file.stem
                    category = category_dir.name
                    article_url = f"{self.website_url}/{category}/{slug}"

                    articles.append({
                        "title": frontmatter.get("title", slug),
                        "url": article_url,
                        "category": category,
                        "file_path": str(md_file),
                        "date": frontmatter.get("date", ""),
                        "description": frontmatter.get("description", ""),
                        "tags": frontmatter.get("tags", []),
                    })
                except Exception as e:
                    print(f"⚠️  读取文件失败 {md_file}: {e}")

        return articles

    def _parse_frontmatter(self, content: str) -> Optional[Dict]:
        """解析 YAML frontmatter（简单版，满足本项目需求）"""
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
                # 支持 [tag1, tag2] 和 - tag1 两种格式
                if value.startswith("["):
                    value = value.strip("[]")
                result[key] = [t.strip().strip('"').strip("'")
                               for t in value.split(",") if t.strip()]
            else:
                result[key] = value

        return result

    def check_indexing_bing(self, article_url: str) -> Dict:
        """通过 Bing site: 查询判断收录（返回 indexed=True/False）"""
        query = f"site:{article_url}"
        search_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        try:
            req = urllib.request.Request(search_url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            # Bing 没有收录时会返回 "没有与此相关的结果" 等提示
            no_result_hints = [
                "no results", "没有与此相关的结果",
                "未找到结果", "没有找到结果",
            ]
            if any(h in html.lower() for h in no_result_hints):
                return {"indexed": False, "note": "Bing: 明确无结果"}

            # 检查页面中是否出现目标域名
            domain = "gk.edu-sjtu.cn"
            if domain in html:
                return {"indexed": True, "note": "Bing: 域名出现在结果页"}
            else:
                return {"indexed": False, "note": "Bing: 域名未出现在结果页（可能未收录或反爬）"}

        except Exception as e:
            return {"indexed": False, "note": f"Bing 查询失败: {e}"}

    def check_sitemap(self, article_url: str) -> bool:
        """检查文章 URL 是否出现在 sitemap.xml 中"""
        try:
            req = urllib.request.Request(
                SITEMAP_URL,
                headers={"User-Agent": "SEO-Checker/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                sitemap_content = resp.read().decode("utf-8", errors="ignore")

            # 去掉 WEBSITE_URL 前缀，只比较 path 部分
            path = article_url.replace(WEBSITE_URL, "").strip("/")
            return path in sitemap_content or article_url in sitemap_content
        except Exception:
            return False

    def batch_check(self, articles: List[Dict]) -> Dict[str, Dict]:
        """批量检查文章收录状态"""
        results = {}
        total = len(articles)

        # 先一次性获取 sitemap（只请求一次）
        print("📡 获取 sitemap.xml...")
        sitemap_urls: set = set()
        try:
            req = urllib.request.Request(
                SITEMAP_URL,
                headers={"User-Agent": "SEO-Checker/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                sitemap_content = resp.read().decode("utf-8", errors="ignore")
            # 提取所有 <loc>...</loc>
            sitemap_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap_content))
            print(f"   sitemap 包含 {len(sitemap_urls)} 条 URL")
        except Exception as e:
            print(f"⚠️  无法获取 sitemap: {e}")

        for i, article in enumerate(articles, 1):
            url = article["url"]
            print(f"  [{i}/{total}] 检查: {article['title'][:35]}...")

            # sitemap 收录（精确匹配）
            in_sitemap = url in sitemap_urls

            # Bing 搜索引擎收录（采样检查，避免被封）
            if i <= 20:  # 只对前20篇做实时搜索检查，避免IP被限
                bing_result = self.check_indexing_bing(url)
                time.sleep(1.5)  # 避免频繁请求
            else:
                bing_result = {"indexed": None, "note": "超出实时检查限额（仅 sitemap 检查）"}

            results[url] = {
                "in_sitemap": in_sitemap,
                "bing": bing_result,
            }

        return results

    def generate_report(
        self,
        articles: List[Dict],
        check_results: Dict[str, Dict],
        target_date: str,
        days_ago: int,
    ) -> str:
        """生成 Markdown 格式收录检查报告"""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = []
        lines.append(f"# SEO收录检查报告 — {target_date}")
        lines.append("")
        lines.append(f"**检查时间**: {now_str}")
        lines.append(f"**目标日期**: {target_date}（{days_ago}天前发布）")
        lines.append(f"**网站地址**: {self.website_url}")
        lines.append(f"**检查文章数**: {len(articles)}")
        lines.append("")

        # ---- 详细列表 ----
        lines.append("## 详细检查结果")
        lines.append("")
        lines.append("| 标题 | 分类 | Sitemap | Bing | 备注 |")
        lines.append("|------|------|---------|------|------|")

        sitemap_indexed = 0
        bing_indexed = 0
        not_in_sitemap = []

        for article in articles:
            url = article["url"]
            result = check_results.get(url, {})

            in_sitemap = result.get("in_sitemap", False)
            bing = result.get("bing", {})
            bing_status = bing.get("indexed")

            sitemap_icon = "✅" if in_sitemap else "❌"
            if bing_status is True:
                bing_icon = "✅"
                bing_indexed += 1
            elif bing_status is False:
                bing_icon = "❌"
            else:
                bing_icon = "—"

            if in_sitemap:
                sitemap_indexed += 1
            else:
                not_in_sitemap.append(article)

            note = bing.get("note", "")
            title_link = f"[{article['title'][:28]}]({url})"
            lines.append(
                f"| {title_link} | {article['category']} | {sitemap_icon} | {bing_icon} | {note[:30]} |"
            )

        lines.append("")

        # ---- 未收录清单 ----
        if not_in_sitemap:
            lines.append("## ⚠️ 未出现在 Sitemap 的文章")
            lines.append("")
            lines.append("> 这些文章需要确认 Vercel 部署是否成功、sitemap.xml 是否已更新。")
            lines.append("")
            for a in not_in_sitemap:
                lines.append(f"- [{a['title']}]({a['url']})")
            lines.append("")

        # ---- 统计汇总 ----
        total = len(articles)
        sitemap_rate = f"{sitemap_indexed}/{total}" if total else "0/0"
        bing_rate = f"{bing_indexed}/min({total},20)" if total else "0/0"

        lines.append("## 📊 收录统计汇总")
        lines.append("")
        lines.append(f"| 指标 | 数值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 检查文章总数 | {total} 篇 |")
        lines.append(f"| Sitemap 已收录 | {sitemap_indexed} 篇（{round(sitemap_indexed/total*100) if total else 0}%）|")
        lines.append(f"| Sitemap 未收录 | {len(not_in_sitemap)} 篇 |")
        lines.append(f"| Bing 实时检查（前20篇）| {bing_indexed} 篇已收录 |")
        lines.append("")

        # ---- 优化建议 ----
        lines.append("## 💡 优化建议")
        lines.append("")
        if len(not_in_sitemap) > 0:
            lines.append(f"1. **{len(not_in_sitemap)} 篇未出现在 Sitemap**：检查 Vercel 部署日志，确认对应页面已成功生成。")
        if bing_indexed < min(total, 10):
            lines.append("2. **Bing 收录率偏低**：可登录 Bing Webmaster Tools 手动提交 sitemap，或使用 IndexNow 协议加速收录。")
        lines.append("3. **百度收录延迟**：百度对新站收录较慢（通常7-30天），建议开通百度搜索资源平台并主动推送 URL。")
        lines.append("4. **持续监测**：建议在发布后 7、14、30 天各做一次收录检查。")
        lines.append("")

        return "\n".join(lines)

    def run(
        self,
        date_str: Optional[str] = None,
        days_ago: int = DEFAULT_DAYS_AGO,
        check_all: bool = False,
        check_only: bool = False,
    ) -> str:
        """执行收录检查主流程"""

        # 确定目标日期
        if date_str:
            target_date = date_str
            # 反推 days_ago（仅用于报告展示）
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
                days_ago = (date.today() - d).days
            except Exception:
                days_ago = 0
        elif check_all:
            target_date = "全部"
        else:
            target_date = compute_target_date(days_ago)

        print(f"\n🔍 SEO收录检查启动")
        print(f"   目标日期：{target_date}（{days_ago} 天前发布）")
        print(f"   网站地址：{self.website_url}\n")

        # 提取文章
        articles = self.extract_articles_from_content(
            date_str=target_date if not check_all else None,
            check_all=check_all,
        )

        if not articles:
            msg = f"❌ 未找到 {target_date} 发布的文章，检查结束。"
            print(msg)
            return msg

        print(f"📄 找到 {len(articles)} 篇文章，开始检查...\n")

        # 执行检查
        check_results = self.batch_check(articles)

        if check_only:
            print("✅ 检查完成（--check-only 模式，不生成报告）")
            return ""

        # 生成报告
        report = self.generate_report(articles, check_results, target_date, days_ago)

        # 保存报告
        REPORTS_DIR.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        date_label = target_date.replace("-", "") if target_date != "全部" else "all"
        report_file = REPORTS_DIR / f"indexing_check_{date_label}_{ts}.md"
        report_file.write_text(report, encoding="utf-8")

        print(f"\n✅ 收录检查报告已保存：{report_file}")
        return report


def main():
    parser = argparse.ArgumentParser(
        description="SEO收录检查工具 — 检查文章在 Bing/sitemap 的收录状态"
    )
    parser.add_argument(
        "--days-ago", type=int, default=DEFAULT_DAYS_AGO,
        help=f"检查 N 天前发布的文章（默认 {DEFAULT_DAYS_AGO} 天）"
    )
    parser.add_argument(
        "--date", type=str,
        help="精确指定日期，格式: YYYY-MM-DD（优先于 --days-ago）"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="检查全部文章（慎用，数量很大时耗时较长）"
    )
    parser.add_argument(
        "--check-only", action="store_true",
        help="仅执行检查，不生成报告文件"
    )

    args = parser.parse_args()

    checker = SEOIndexingChecker()
    checker.run(
        date_str=args.date,
        days_ago=args.days_ago,
        check_all=args.all,
        check_only=args.check_only,
    )


if __name__ == "__main__":
    main()
