#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为正文添加内容类型标签和时效性提示
功能：
1. 在标题后添加【原创/转载/学员分享】标签
2. 对超过90天的文章添加时效性提示
支持预览模式（默认）和执行模式（--apply）
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "content"

def has_content_type_badge(content):
    """检查文章是否已添加内容类型标签"""
    return bool(re.search(r'#\s*.+?\s*【(?:原创|转载|学员分享)】', content))

def has_timeliness_warning(content):
    """检查文章是否已有时效性提示"""
    return bool(re.search(r'⚠️\s*\*\*时效性提示\*\*', content))

def calculate_days_old(date_str):
    """计算文章发布天数"""
    try:
        article_date = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - article_date).days
    except:
        return 0

def add_content_type_and_timeliness(filepath, dry_run=True):
    """为单篇文章添加内容类型标签和时效性提示"""
    try:
        content = filepath.read_text(encoding='utf-8')
        
        # 解析frontmatter获取信息
        fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not fm_match:
            return {'status': 'error', 'reason': '无法解析frontmatter'}
        
        fm_text = fm_match.group(1)
        fm = {}
        for line in fm_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                key, _, value = line.partition(':')
                key = key.strip()
                value = value.strip()
                
                if key == 'tags' and value.startswith('['):
                    try:
                        fm[key] = json.loads(value)
                    except:
                        fm[key] = []
                else:
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    fm[key] = value
        
        content_type = fm.get('content_type', '原创')
        source_date = fm.get('date', '')
        
        new_content = content
        modifications = []
        
        # 1. 添加内容类型标签（如果还没有）
        if not has_content_type_badge(content):
            # 在标题行后添加标签
            title_pattern = r'(#\s*.+?)(\s*\n)'
            title_match = re.search(title_pattern, content)
            if title_match:
                original = title_match.group(0)
                badge = f" 【{content_type}】" if content_type in ['原创', '转载', '学员分享'] else ""
                new_title = title_match.group(1) + badge + title_match.group(2)
                new_content = new_content.replace(original, new_title, 1)
                modifications.append(f"添加【{content_type}】标签")
        
        # 2. 添加时效性提示（如果超过90天且没有提示）
        days_old = calculate_days_old(source_date)
        if days_old > 90 and not has_timeliness_warning(new_content):
            # 在描述引用后添加时效性提示
            desc_pattern = r'(>\s*.+?\n)'
            desc_match = re.search(desc_pattern, new_content)
            if desc_match:
                timeliness_warning = f"\n<div class=\"timeliness-warning\">\n⚠️ **时效性提示**：本文发布于 {source_date}，距今已 {days_old} 天，部分信息可能已过时。建议您同时参考最新公告和资料。\n</div>\n\n"
                pos = desc_match.end()
                new_content = new_content[:pos] + timeliness_warning + new_content[pos:]
                modifications.append(f"添加时效性提示（{days_old}天前）")
        
        if not modifications:
            return {'status': 'skipped', 'reason': '已包含标签和提示'}
        
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
            return {'status': 'updated', 'modifications': modifications}
        else:
            return {'status': 'would_update', 'modifications': modifications}
    
    except Exception as e:
        return {'status': 'error', 'reason': str(e)}

def main():
    import argparse
    parser = argparse.ArgumentParser(description='批量为正文添加内容类型标签和时效性提示')
    parser.add_argument('--apply', action='store_true', help='实际执行修改（默认仅预览）')
    args = parser.parse_args()
    
    print("=" * 60)
    print("批量添加内容类型标签和时效性提示")
    print("=" * 60)
    print()
    
    # 扫描所有文章
    print("正在扫描文章...")
    md_files = list(CONTENT_DIR.rglob("*.md"))
    print(f"找到 {len(md_files)} 篇文章")
    print()
    
    # 统计
    stats = {'updated': 0, 'would_update': 0, 'skipped': 0, 'error': 0}
    details = []
    
    for i, md_file in enumerate(md_files, 1):
        if i % 100 == 0:
            print(f"处理进度: {i}/{len(md_files)}")
        
        result = add_content_type_and_timeliness(
            md_file, 
            dry_run=not args.apply
        )
        
        status = result['status']
        stats[status] = stats.get(status, 0) + 1
        
        if status in ('updated', 'would_update'):
            details.append({
                'file': md_file.name,
                'modifications': result.get('modifications', [])
            })
    
    print()
    print("=" * 60)
    print("处理完成")
    print("=" * 60)
    print()
    print(f"总文章数: {len(md_files)}")
    if args.apply:
        print(f"已更新: {stats['updated']}")
    else:
        print(f"可更新: {stats['would_update']}")
    print(f"已跳过: {stats['skipped']}")
    print(f"错误: {stats['error']}")
    print()
    
    # 显示部分详情
    if details:
        print("示例更新（前5条）：")
        print("-" * 60)
        for i, detail in enumerate(details[:5], 1):
            print(f"{i}. {detail['file']}")
            for mod in detail['modifications']:
                print(f"   - {mod}")
            print()
    
    if not args.apply:
        print("提示：使用 --apply 参数实际执行修改")

if __name__ == "__main__":
    main()
