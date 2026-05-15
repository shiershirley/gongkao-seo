#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_article_generator.py
公考SEO批量文章生成脚本

每次执行选取 N 个未覆盖关键词（含角度），输出文章生成任务列表（JSON格式）
供自动化任务读取后逐篇生成文章。

使用方法:
  python scripts/batch_article_generator.py --count 8          # 输出8篇生成任务
  python scripts/batch_article_generator.py --count 8 --dry-run  # 仅预览，不更新状态
  python scripts/batch_article_generator.py --list-uncovered   # 列出所有未覆盖关键词（含角度数）

角度轮换策略:
  - 每个关键词在 keywords_pool.md 中定义 angles 字段（多写作角度）
  - 同一关键词可被生成多篇文章，每次取不同角度
  - 角度用完后才重置（避免重复内容）
  - 角度消耗状态记录在 scripts/angle_coverage.json
"""

import json
import os
import re
import sys
import random
from datetime import datetime
from pathlib import Path
from typing import Optional

# ========== 配置 ==========
SCRIPTS_DIR = Path(__file__).parent
CONTENT_DIR = SCRIPTS_DIR.parent / 'content'
KEYWORDS_FILE = SCRIPTS_DIR / 'keywords_pool.md'
ANGLE_COVERAGE_FILE = SCRIPTS_DIR / 'angle_coverage.json'

CATEGORY_MAP = {
    'info': 'shanghai-shegong',
    'guide': 'beikao-zhinan',
    'question': 'beikao-zhinan',
    'study': 'beikao-zhinan',
    'compare': 'gangwei-fenxi',
}

# 特殊关键词分类覆盖
KEYWORD_CATEGORY_OVERRIDE = {
    '招聘': 'baokao-gonggao',
    '公告': 'baokao-gonggao',
    '报名时间': 'baokao-gonggao',
    '报名入口': 'baokao-gonggao',
    '政策': 'zhengce-jiedu',
    '新政策': 'zhengce-jiedu',
    '改革': 'zhengce-jiedu',
    '职业化': 'zhengce-jiedu',
    '真题': 'zhenti-jiexi',
    '模拟题': 'zhenti-jiexi',
    '历年': 'zhenti-jiexi',
    '分数线': 'zhenti-jiexi',
    '答案': 'zhenti-jiexi',
    '题库': 'zhenti-jiexi',
    '岗位': 'gangwei-fenxi',
    '发展前景': 'gangwei-fenxi',
    '编制': 'gangwei-fenxi',
    '转编': 'gangwei-fenxi',
    '稳定性': 'gangwei-fenxi',
    '上岸经验': 'shang-an-jingyan',
    '经验': 'shang-an-jingyan',
    '攻略': 'beikao-zhinan',
    '技巧': 'beikao-zhinan',
    '怎么复习': 'beikao-zhinan',
    '复习计划': 'beikao-zhinan',
    '网课': 'beikao-zhinan',
    '培训': 'beikao-zhinan',
    '社工证': 'zhengce-jiedu',
    '持证': 'zhengce-jiedu',
}


def load_angle_coverage() -> dict:
    """加载角度消耗记录"""
    if ANGLE_COVERAGE_FILE.exists():
        return json.loads(ANGLE_COVERAGE_FILE.read_text(encoding='utf-8'))
    return {}


def save_angle_coverage(coverage: dict):
    """保存角度消耗记录"""
    ANGLE_COVERAGE_FILE.write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


def parse_keywords_pool() -> list[dict]:
    """解析关键词池，返回关键词列表（含 angles）"""
    if not KEYWORDS_FILE.exists():
        return []

    content = KEYWORDS_FILE.read_text(encoding='utf-8')
    keywords = []

    yaml_blocks = re.findall(r'```yaml(.*?)```', content, re.DOTALL)
    for block in yaml_blocks:
        # 跳过动态关键词块（含 trigger 字段）
        if 'trigger:' in block:
            continue

        # 解析每个 - keyword: 条目
        entries = re.split(r'\n(?=- keyword:)', block.strip())
        for entry in entries:
            if not entry.strip():
                continue

            kw_match = re.search(r'- keyword:\s*(.+)', entry)
            if not kw_match:
                continue
            keyword = kw_match.group(1).strip()

            priority_match = re.search(r'priority:\s*(\w+)', entry)
            priority = priority_match.group(1).strip() if priority_match else 'P3'

            type_match = re.search(r'type:\s*(\w+)', entry)
            ktype = type_match.group(1).strip() if type_match else 'info'

            covered_match = re.search(r'covered:\s*(\w+)', entry)
            covered = covered_match.group(1).strip().lower() == 'true' if covered_match else False

            note_match = re.search(r'note:\s*(.+)', entry)
            note = note_match.group(1).strip() if note_match else ''

            # 解析 angles（格式: angles: [角度1, 角度2, ...]）
            angles_match = re.search(r'angles:\s*\[(.+?)\]', entry)
            if angles_match:
                angles_raw = angles_match.group(1)
                angles = [a.strip() for a in angles_raw.split(',') if a.strip()]
            else:
                angles = []

            keywords.append({
                'keyword': keyword,
                'priority': priority,
                'type': ktype,
                'covered': covered,
                'note': note,
                'angles': angles,
            })

    return keywords


def get_category(keyword: str, ktype: str) -> str:
    """根据关键词和类型判断分类"""
    for kw_hint, cat in KEYWORD_CATEGORY_OVERRIDE.items():
        if kw_hint in keyword:
            return cat
    return CATEGORY_MAP.get(ktype, 'shanghai-shegong')


def priority_order(p: str) -> int:
    return {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}.get(p, 9)


def generate_slug(keyword: str, angle: str, timestamp: str) -> str:
    """生成文件名 slug"""
    # 简单拼音化（仅ASCII字符）
    date_part = timestamp[:10]  # YYYY-MM-DD
    # 移除特殊字符，保留中文（通过 hash 方式生成短 id）
    import hashlib
    key = f"{keyword}_{angle}"
    hash_id = hashlib.md5(key.encode('utf-8')).hexdigest()[:6]
    # 根据时间+hash生成唯一slug
    time_id = timestamp[11:16].replace(':', '')  # HHMM
    return f"{date_part}-shegong-{hash_id}-{time_id}"


def build_tasks(count: int, dry_run: bool = False) -> list[dict]:
    """
    构建文章生成任务列表。
    每个任务包含：keyword, angle, category, slug, publish_datetime
    """
    keywords = parse_keywords_pool()
    angle_coverage = load_angle_coverage()

    # 按优先级排序
    keywords_sorted = sorted(keywords, key=lambda k: priority_order(k['priority']))

    tasks = []
    now = datetime.now()

    for kw_item in keywords_sorted:
        if len(tasks) >= count:
            break

        keyword = kw_item['keyword']
        ktype = kw_item['type']
        angles = kw_item['angles']

        # 当前关键词已消耗的角度
        used_angles = angle_coverage.get(keyword, [])

        if not angles:
            # 没有定义 angles，当 covered=False 时生成一篇基础文章
            if not kw_item['covered'] and keyword not in used_angles:
                angle = '综合版'
            else:
                continue
        else:
            # 找未使用的角度
            available = [a for a in angles if a not in used_angles]
            if not available:
                # 所有角度已消耗，重置（允许复用）
                if not dry_run:
                    angle_coverage[keyword] = []
                available = angles[:]

            if not available:
                continue

            angle = available[0]

        category = get_category(keyword, ktype)

        # 生成文章发布时间（在7:00-20:00之间，随机分布）
        # 每次执行时任务按顺序排列，各任务发布时间基于当前时间
        minute_offset = random.randint(0, 5) * 10  # 0/10/20/30/40/50分
        pub_datetime = now.strftime(f"%Y-%m-%dT{now.hour:02d}:{minute_offset:02d}:00")

        slug = generate_slug(keyword, angle, now.strftime('%Y-%m-%dT%H:%M:%S'))
        filename = f"{slug}.md"

        tasks.append({
            'keyword': keyword,
            'angle': angle,
            'category': category,
            'slug': slug,
            'filename': filename,
            'filepath': str(CONTENT_DIR / category / filename),
            'publish_datetime': pub_datetime,
            'priority': kw_item['priority'],
            'type': ktype,
        })

        # 标记角度已使用
        if not dry_run:
            angle_coverage.setdefault(keyword, []).append(angle)

    if not dry_run and tasks:
        save_angle_coverage(angle_coverage)

    return tasks


def list_uncovered():
    """列出所有未覆盖/有剩余角度的关键词"""
    keywords = parse_keywords_pool()
    angle_coverage = load_angle_coverage()

    print(f"\n{'='*60}")
    print(f"未覆盖/有剩余角度的关键词列表")
    print(f"{'='*60}")

    total_available = 0
    for p in ['P0', 'P1', 'P2', 'P3']:
        items = [k for k in keywords if k['priority'] == p]
        if not items:
            continue
        print(f"\n## {p} 级关键词")
        for kw in items:
            angles = kw['angles']
            used = angle_coverage.get(kw['keyword'], [])
            if angles:
                available = [a for a in angles if a not in used]
                remaining = len(available)
            else:
                remaining = 0 if kw['covered'] else 1

            if remaining > 0:
                total_available += remaining
                print(f"  [{kw['priority']}] {kw['keyword']} — 剩余 {remaining} 个角度")

    print(f"\n{'='*60}")
    print(f"合计可生成文章数：{total_available}")
    print(f"{'='*60}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='批量文章生成任务构建器')
    parser.add_argument('--count', type=int, default=8, help='本次生成篇数（默认8篇）')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不更新角度消耗记录')
    parser.add_argument('--list-uncovered', action='store_true', help='列出所有未覆盖关键词')
    parser.add_argument('--output', choices=['json', 'text'], default='json', help='输出格式')
    args = parser.parse_args()

    if args.list_uncovered:
        list_uncovered()
        return 0

    tasks = build_tasks(args.count, dry_run=args.dry_run)

    if args.output == 'json':
        print(json.dumps(tasks, ensure_ascii=False, indent=2))
    else:
        print(f"\n本次生成任务（共 {len(tasks)} 篇）：")
        for i, t in enumerate(tasks, 1):
            print(f"  {i}. [{t['priority']}] {t['keyword']} | 角度：{t['angle']}")
            print(f"     分类：{t['category']} | 文件：{t['filename']}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
