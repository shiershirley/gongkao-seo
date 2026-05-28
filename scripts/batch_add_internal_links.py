#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为正文添加内链网络
功能：为现有文章添加"相关阅读"章节，包含2-3个内链
支持预览模式（默认）和执行模式（--apply）
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "content"

# 导入内链模块
sys.path.insert(0, str(Path(__file__).parent))
from internal_linker import build_article_index, find_related_articles, generate_related_links_section

def has_related_links_section(content):
    """检查文章是否已有相关阅读章节"""
    return bool(re.search(r'##\s*相关阅读', content))

def remove_related_links_section(content):
    """移除已有的相关阅读章节"""
    # 移除从"## 相关阅读"到下一个"##"或文件结尾的内容
    pattern = r'\n##\s*相关阅读\s*\n.*?(?=\n##|\Z)'
    return re.sub(pattern, '', content, flags=re.DOTALL)

def add_internal_links_to_article(filepath, index, max_links=3, dry_run=True):
    """为单篇文章添加内链"""
    try:
        content = filepath.read_text(encoding='utf-8')
        
        # 检查是否已有相关阅读章节
        if has_related_links_section(content):
            return {'status': 'skipped', 'reason': '已有相关阅读章节'}
        
        # 解析文章信息
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
        
        # 构造文章信息
        article_info = {
            'title': fm.get('title', filepath.stem),
            'category': fm.get('category', ''),
            'tags': fm.get('tags', []),
            'date': fm.get('date', ''),
            'path': str(filepath)
        }
        
        # 找相关文章
        related = find_related_articles(article_info, index, max_links=max_links)
        
        if not related:
            return {'status': 'skipped', 'reason': '未找到相关文章'}
        
        # 生成相关阅读章节
        related_section = generate_related_links_section(article_info, related)
        
        # 插入位置：在总结章节前，或追加到末尾
        patterns = [
            r'(##\s*四、总结与建议)',
            r'(##\s*三、总结与建议)',
            r'(##\s*总结)',
            r'(---\n\*本文仅供参考)',
        ]
        
        inserted = False
        new_content = content
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                pos = match.start()
                new_content = content[:pos] + related_section + "\n" + content[pos:]
                inserted = True
                break
        
        if not inserted:
            # 追加到末尾
            new_content = content.rstrip() + "\n" + related_section + "\n"
        
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
            return {'status': 'updated', 'related_count': len(related), 'related': [a['title'] for a in related]}
        else:
            return {'status': 'would_update', 'related_count': len(related), 'related': [a['title'] for a in related]}
    
    except Exception as e:
        return {'status': 'error', 'reason': str(e)}

def main():
    import argparse
    parser = argparse.ArgumentParser(description='批量为正文添加内链网络')
    parser.add_argument('--apply', action='store_true', help='实际执行修改（默认仅预览）')
    parser.add_argument('--max-links', type=int, default=3, help='每篇文章最多添加的内链数（默认3）')
    args = parser.parse_args()
    
    print("=" * 60)
    print("批量添加内链网络")
    print("=" * 60)
    print()
    
    # 构建索引
    print("正在构建文章索引...")
    index = build_article_index()
    print(f"索引完成，共 {len(index)} 篇文章")
    print()
    
    if len(index) < 2:
        print("文章数量不足，无法生成内链")
        return
    
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
        
        result = add_internal_links_to_article(
            md_file, 
            index, 
            max_links=args.max_links,
            dry_run=not args.apply
        )
        
        status = result['status']
        stats[status] = stats.get(status, 0) + 1
        
        if status in ('updated', 'would_update'):
            details.append({
                'file': md_file.name,
                'related': result.get('related', []),
                'related_count': result.get('related_count', 0)
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
            print(f"   添加 {detail['related_count']} 篇相关阅读")
            for title in detail['related']:
                print(f"   - {title}")
            print()
    
    if not args.apply:
        print("提示：使用 --apply 参数实际执行修改")

if __name__ == "__main__":
    main()
