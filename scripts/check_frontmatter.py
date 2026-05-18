#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单frontmatter检查器 - 检查文章frontmatter格式
"""

import os
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"

def check_frontmatter(filepath):
    """检查单个文件的frontmatter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有frontmatter
        if not content.startswith('---'):
            return False, "缺少frontmatter开始标记"
        
        # 提取frontmatter
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return False, "frontmatter格式错误"
        
        fm_text = match.group(1)
        
        # 检查必需字段
        required_fields = ['title', 'date', 'category', 'tags', 'author', 'description']
        for field in required_fields:
            if f'{field}:' not in fm_text:
                return False, f"缺少必需字段: {field}"
        
        # 检查description中是否有英文双引号
        desc_match = re.search(r'description:\s*"([^"]*)"', fm_text)
        if desc_match:
            desc = desc_match.group(1)
            if '"' in desc:
                return False, "description中包含未转义的英文双引号"
        
        return True, "格式正确"
    
    except Exception as e:
        return False, f"检查出错: {str(e)}"

def main():
    """主函数"""
    print("开始检查frontmatter格式...")
    
    # 获取所有今天生成的文章
    today = datetime.now().strftime('%Y-%m-%d')
    problem_files = []
    
    for md_file in CONTENT_DIR.rglob('*.md'):
        if today in md_file.name:
            is_valid, message = check_frontmatter(md_file)
            if not is_valid:
                problem_files.append((md_file, message))
    
    # 输出结果
    if problem_files:
        print(f"\n发现 {len(problem_files)} 个问题文件:")
        for filepath, message in problem_files[:10]:  # 只显示前10个
            print(f"  {filepath.name}: {message}")
    else:
        print("\n所有今天生成的文章frontmatter格式正确！")
    
    print(f"\n检查完成。共检查了今天生成的文章。")

if __name__ == "__main__":
    main()
