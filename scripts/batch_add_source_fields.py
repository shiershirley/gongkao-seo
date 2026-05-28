#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新现有文章的frontmatter，添加信源标注字段
为所有文章添加 source_url、source_date、content_type 三个字段

使用方法:
  python scripts/batch_add_source_fields.py           # 预览模式，只显示会修改什么
  python scripts/batch_add_source_fields.py --apply    # 实际执行修改
  python scripts/batch_add_source_fields.py --dry-run  # 同预览模式
"""

import os
import re
import sys
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "content"

# 分类到栏目页URL的映射
CATEGORY_URL_MAP = {
    "guokao": "https://gk.edu-sjtu.cn/guokao/",
    "shengkao": "https://gk.edu-sjtu.cn/shengkao/",
    "shanghai-shegong": "https://gk.edu-sjtu.cn/shanghai-shegong/",
    "baokao-gonggao": "https://gk.edu-sjtu.cn/baokao-gonggao/",
    "zhengce-jiedu": "https://gk.edu-sjtu.cn/zhengce-jiedu/",
    "beikao-zhinan": "https://gk.edu-sjtu.cn/beikao-zhinan/",
    "zhenti-jiexi": "https://gk.edu-sjtu.cn/zhenti-jiexi/",
    "gangwei-fenxi": "https://gk.edu-sjtu.cn/gangwei-fenxi/",
    "shang-an-jingyan": "https://gk.edu-sjtu.cn/shang-an-jingyan/",
    "shiyedanwei": "https://gk.edu-sjtu.cn/shiyedanwei/",
    "shiye-dan-wei": "https://gk.edu-sjtu.cn/shiye-dan-wei/",
}

# 需要标记为"转载"的分类（通常是公告类）
BAOKAO_CATEGORIES = {"baokao-gonggao", "zhengce-jiedu"}


def extract_frontmatter(content: str) -> tuple:
    """提取frontmatter和正文"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), content[match.end():]


def parse_frontmatter_yaml(fm_text: str) -> dict:
    """简单解析YAML格式的frontmatter"""
    result = {}
    lines = fm_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        
        # 列表项（tags等）
        if line.startswith('  - ') or line.startswith('    - '):
            i += 1
            continue
            
        kv_match = re.match(r'^(\w+):\s*(.*)$', line)
        if kv_match:
            key = kv_match.group(1)
            raw_val = kv_match.group(2).strip()
            
            if not raw_val:
                result[key] = ""
            elif raw_val.startswith('[') and raw_val.endswith(']'):
                # 列表格式
                inner = raw_val[1:-1]
                items = [x.strip().strip('"\'') for x in inner.split(',')]
                result[key] = [x for x in items if x]
            else:
                result[key] = raw_val.strip('"\'')
            i += 1
            continue
        i += 1
    return result


def has_source_fields(fm: dict) -> bool:
    """检查是否已有source字段"""
    return 'source_url' in fm and 'source_date' in fm and 'content_type' in fm


def determine_content_type(fm: dict, filepath: Path) -> str:
    """判断文章类型：原创/转载/学员分享"""
    category = fm.get('category', '')
    
    # 公告类文章通常是转载
    if category in BAOKAO_CATEGORIES:
        return "转载"
    
    # 根据文件名或路径判断
    filename = filepath.name.lower()
    if 'jingyan' in filename or '分享' in fm.get('title', ''):
        return "学员分享"
    
    # 默认为原创
    return "原创"


def add_source_fields_to_frontmatter(content: str, filepath: Path) -> tuple:
    """
    添加source字段到frontmatter
    
    Returns:
        (new_content, changed: bool, fields_added: list)
    """
    fm_text, body = extract_frontmatter(content)
    if fm_text is None:
        return content, False, []
    
    fm = parse_frontmatter_yaml(fm_text)
    
    if has_source_fields(fm):
        return content, False, []
    
    fields_added = []
    
    # 1. source_url
    if 'source_url' not in fm:
        category = fm.get('category', '')
        source_url = CATEGORY_URL_MAP.get(category, "https://gk.edu-sjtu.cn/")
        fm['source_url'] = source_url
        fields_added.append('source_url')
    
    # 2. source_date
    if 'source_date' not in fm:
        # 使用文章的date字段
        source_date = fm.get('date', datetime.now().strftime('%Y-%m-%d'))
        # 去掉可能的引号
        if isinstance(source_date, str):

            source_date = source_date.strip('"\'')
        fm['source_date'] = source_date
        fields_added.append('source_date')
    
    # 3. content_type
    if 'content_type' not in fm:
        content_type = determine_content_type(fm, filepath)
        fm['content_type'] = content_type
        fields_added.append('content_type')
    
    # 重新构建frontmatter
    new_fm_lines = ['---']
    
    # 按原始顺序保留字段，然后添加新字段
    original_order = ['title', 'description', 'date', 'category', 'tags', 'author']
    for key in original_order:
        if key in fm:
            val = fm[key]
            if isinstance(val, list):
                tags_str = ', '.join(f'"{t}"' for t in val)
                new_fm_lines.append(f'{key}: [{tags_str}]')
            else:
                new_fm_lines.append(f'{key}: "{val}"')
    
    # 添加新字段（在author之后）
    for key in ['source_url', 'source_date', 'content_type']:
        if key in fm:
            new_fm_lines.append(f'{key}: "{fm[key]}"')
    
    new_fm_lines.append('---')
    
    new_content = '\n'.join(new_fm_lines) + '\n' + body
    
    return new_content, True, fields_added


def process_file(filepath: Path, apply: bool = False) -> dict:
    """处理单个文件"""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return {"file": str(filepath), "status": "error", "message": str(e)}
    
    new_content, changed, fields_added = add_source_fields_to_frontmatter(content, filepath)
    
    if changed:
        if apply:
            try:
                filepath.write_text(new_content, encoding='utf-8')
                return {"file": str(filepath), "status": "updated", "fields": fields_added}
            except Exception as e:
                return {"file": str(filepath), "status": "error", "message": str(e)}
        else:
            return {"file": str(filepath), "status": "would_update", "fields": fields_added}
    else:
        return {"file": str(filepath), "status": "skipped", "reason": "already_has_fields"}


def main():
    apply_mode = '--apply' in sys.argv
    dry_run = '--dry-run' in sys.argv or ('--apply' not in sys.argv)
    
    if dry_run:
        print("=" * 70)
        print("批量添加信源字段 - 预览模式")
        print("=" * 70)
        print("提示：添加 --apply 参数来实际执行修改")
        print()
    else:
        print("=" * 70)
        print("批量添加信源字段 - 执行模式")
        print("=" * 70)
        print()
    
    # 收集所有md文件
    all_files = []
    for ext in ['*.md', '**/*.md']:
        all_files.extend(CONTENT_DIR.rglob(ext))
    
    # 去重
    all_files = list(set(all_files))
    
    print(f"找到 {len(all_files)} 个Markdown文件")
    print()
    
    stats = {"updated": 0, "skipped": 0, "error": 0, "would_update": 0}
    updated_files = []
    
    for i, filepath in enumerate(sorted(all_files), 1):
        if i % 100 == 0:
            print(f"处理进度: {i}/{len(all_files)}...")
        
        result = process_file(filepath, apply=apply_mode)
        
        if result["status"] == "updated":
            stats["updated"] += 1
            updated_files.append(result)
        elif result["status"] == "would_update":
            stats["would_update"] += 1
            if len(updated_files) < 10:  # 只显示前10个预览
                print(f"  [预览] {result['file']}")
                print(f"      将添加字段: {', '.join(result['fields'])}")
        elif result["status"] == "skipped":
            stats["skipped"] += 1
        else:
            stats["error"] += 1
            print(f"  [错误] {result['file']}: {result.get('message', '')}")
    
    print()
    print("=" * 70)
    print("处理完成！")
    print("-" * 70)
    print(f"需要更新: {stats['would_update'] if dry_run else stats['updated']}")
    print(f"已跳过:   {stats['skipped']}")
    print(f"错误:     {stats['error']}")
    print("=" * 70)
    
    if dry_run and stats['would_update'] > 0:
        print()
        print("提示：确认无误后，运行以下命令实际执行修改：")
        print(f"  python {sys.argv[0]} --apply")
    
    return 0 if stats['error'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
