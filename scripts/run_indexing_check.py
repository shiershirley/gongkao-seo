#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接运行SEO收录检查（绕过stdout重定向问题）"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# 先禁用原脚本的编码修复
import seo_indexing_checker
seo_indexing_checker.sys.stdout = sys.stdout
seo_indexing_checker.sys.stderr = sys.stderr

from seo_indexing_checker import SEOIndexingChecker, compute_target_date

c = SEOIndexingChecker()
target = compute_target_date(10)
print(f'Target date: {target}', flush=True)

articles = c.extract_articles_from_content(date_str=target)
print(f'Found {len(articles)} articles', flush=True)

if not articles:
    print("No articles found, trying fallback...", flush=True)
    available_dates = c._find_available_dates()
    print(f"Available dates: {available_dates[:10]}", flush=True)
    sys.exit(1)

print(f"\nChecking {len(articles)} articles...", flush=True)
results = c.batch_check(articles)
print(f"\nCheck complete, {len(results)} results", flush=True)

report = c.generate_report(articles, results, target, 10)

# 保存报告
from datetime import datetime
from pathlib import Path
REPORTS_DIR = Path("d:/AI/task/gongkao-seo/reports")
REPORTS_DIR.mkdir(exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
date_label = target.replace("-", "")
report_file = REPORTS_DIR / f"indexing_check_{date_label}_{ts}.md"
report_file.write_text(report, encoding="utf-8")

print(f"\nReport saved: {report_file}", flush=True)
