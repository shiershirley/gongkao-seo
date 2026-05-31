#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""运行SEO收录检查并输出到日志文件"""
import sys
import os
import time

# 设置日志文件
log_file = "d:/AI/task/gongkao-seo/reports/check_log.txt"
f = open(log_file, "w", encoding="utf-8")

class Tee:
    def __init__(self, stdout, file):
        self.stdout = stdout
        self.file = file
    def write(self, data):
        self.stdout.write(data)
        self.stdout.flush()
        self.file.write(data)
        self.file.flush()
    def flush(self):
        self.stdout.flush()
        self.file.flush()

sys.stdout = Tee(sys.stdout, f)
sys.stderr = Tee(sys.stderr, f)

sys.path.insert(0, os.path.dirname(__file__))

# 使用修复后的脚本
from seo_indexing_checker_fixed import SEOIndexingChecker, compute_target_date

print(f"[{time.strftime('%H:%M:%S')}] Starting check...", flush=True)

c = SEOIndexingChecker()
target = compute_target_date(10)
print(f"[{time.strftime('%H:%M:%S')}] Target date: {target}", flush=True)

articles = c.extract_articles_from_content(date_str=target)
print(f"[{time.strftime('%H:%M:%S')}] Found {len(articles)} articles", flush=True)

if not articles:
    print("No articles found", flush=True)
    f.close()
    sys.exit(1)

print(f"[{time.strftime('%H:%M:%S')}] Starting batch check...", flush=True)
results = c.batch_check(articles)
print(f"[{time.strftime('%H:%M:%S')}] Check complete, {len(results)} results", flush=True)

report = c.generate_report(articles, results, target, 10)

from datetime import datetime
from pathlib import Path
REPORTS_DIR = Path("d:/AI/task/gongkao-seo/reports")
REPORTS_DIR.mkdir(exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
date_label = target.replace("-", "")
report_file = REPORTS_DIR / f"indexing_check_{date_label}_{ts}.md"
report_file.write_text(report, encoding="utf-8")

print(f"[{time.strftime('%H:%M:%S')}] Report saved: {report_file}", flush=True)
f.close()
