#!/usr/bin/env python3
"""
修复13:00批次文章的frontmatter格式问题
主要修复：
1. tags从Python列表格式改为YAML列表格式
2. description过长的问题（超过150字）
"""
import os
import re
from datetime import datetime

ROOT = 'd:/AI/task/gongkao-seo'
TODAY = '2026-05-19'
TIMESTAMP = '13-00'

def fix_tags_in_content(content):
    """修复tags格式：从Python列表改为YAML列表"""
    # 匹配 tags: ['...', '...'] 格式
    pattern = r'^tags:\s*\[\s*\'([^\']*)\'\s*,\s*\'([^\']*)\'\s*,\s*\'([^\']*)\'\s*,\s*\'([^\']*)\'\s*,\s*\'([^\']*)\'\s*\]'
    
    def replace_tags(match):
        tags = [match.group(i) for i in range(1, 6)]
        yaml_tags = 'tags:\n'
        for tag in tags:
            yaml_tags += f'  - {tag}\n'
        return yaml_tags.rstrip()
    
    fixed = re.sub(pattern, replace_tags, content, flags=re.MULTILINE)
    return fixed

def fix_description(content):
    """修复description过长的问题，截断到150字以内"""
    def truncate_desc(match):
        desc = match.group(1)
        if len(desc) > 140:
            desc = desc[:137] + '...'
        # 确保使用日文引号
        desc = desc.replace('"', '「').replace('"', '」')
        return f'description: "{desc}"'
    
    fixed = re.sub(r'description:\s*"([^"]*)"', truncate_desc, content)
    return fixed

def process_file(filepath):
    """处理单个文件"""
    print(f'处理: {os.path.basename(filepath)}')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复tags格式
    content = fix_tags_in_content(content)
    
    # 修复description
    content = fix_description(content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  -> 已修复')
        return True
    else:
        print(f'  -> 无需修复')
        return False

def main():
    print('=== 修复13:00批次文章格式 ===')
    print()
    
    # 查找今天13:00批次的文章
    import glob
    pattern = os.path.join(ROOT, 'content', '*', f'{TODAY}-*-{TIMESTAMP}.md')
    files = glob.glob(pattern)
    
    print(f'找到 {len(files)} 个文件:')
    for f in files:
        print(f'  {f}')
    print()
    
    fixed_count = 0
    for f in files:
        if process_file(f):
            fixed_count += 1
        print()
    
    print(f'=== 修复完成 ===')
    print(f'修复文件数: {fixed_count}/{len(files)}')

if __name__ == '__main__':
    main()
