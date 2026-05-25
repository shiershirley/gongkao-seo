#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Chinese slugs - rename files with Chinese characters to English slugs.
This fixes 500 errors on Vercel for static generation.
"""

import os
import re
import shutil
from datetime import datetime

# Mapping table for problematic Chinese phrases in filenames
SLUG_MAPPING = {
    '社区工作者准考证打印指南': 'shegong-zkz-dayin-zhinan',
    '社区工作者常识判断高分策略': 'shegong-changshi-gaofen-celue',
    '社区工作者数量关系技巧': 'shegong-shuliang-guanxi-jiqiao',
    '社区工作者与事业单位区别': 'shegong-vs-shiyedanwei',
    '社区工作者与省考国考区别': 'shegong-vs-shengkao-guokao',
    '社区工作者持证上岗政策': 'shegong-chizheng-shanggang',
    '社区工作者面试真题解析': 'shegong-mianshi-zhenti-jiexi',
    '宝妈考社区工作者成功经验': 'bama-shegong-chenggong',
    '社区工作者宝妈备考经验': 'shegong-bama-beikao',
}

def contains_chinese(text):
    """Check if string contains Chinese characters"""
    return any('\u4e00' <= c <= '\u9fff' for c in text)

def convert_filename(old_filename):
    """
    Convert filename with Chinese characters to English slug.
    Returns new_filename or None if no conversion needed.
    """
    # Remove extension
    name_without_ext = re.sub(r'\.(md|mdx)$', '', old_filename)
    ext = old_filename[len(name_without_ext):]
    
    if not contains_chinese(name_without_ext):
        return None
    
    # Try to find matching key in mapping (try longest match first)
    matched_key = None
    for key in sorted(SLUG_MAPPING.keys(), key=len, reverse=True):
        if key in name_without_ext:
            matched_key = key
            new_name = name_without_ext.replace(key, SLUG_MAPPING[key])
            return new_name + ext
    
    # If no mapping found, return None (skip this file)
    return None

def rename_file_safely(old_path, new_path):
    """Safely rename file, checking for conflicts"""
    if os.path.exists(new_path):
        print(f"  Warning: Target file already exists: {os.path.basename(new_path)}")
        return False
    try:
        shutil.move(old_path, new_path)
        return True
    except Exception as e:
        print(f"  Error renaming: {e}")
        return False

def main():
    content_dir = "content"
    renamed = []
    skipped = []
    
    print("=" * 70)
    print("Chinese Slug Fixer for Next.js SSG on Vercel")
    print("=" * 70)
    print()
    
    # Walk through all content files
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            if not (filename.endswith('.md') or filename.endswith('.mdx')):
                continue
            
            filepath = os.path.join(root, filename)
            new_filename = convert_filename(filename)
            
            if new_filename is None:
                continue
            
            new_filepath = os.path.join(root, new_filename)
            print(f"Processing: {filename}")
            print(f"  -> {new_filename}")
            
            if rename_file_safely(filepath, new_filepath):
                renamed.append((filepath, new_filepath))
                print(f"  Successfully renamed")
            print()
    
    # Summary
    print("=" * 70)
    print(f"Total files renamed: {len(renamed)}")
    print("=" * 70)
    
    # Save log
    if renamed:
        log_file = f"slug_fix_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Chinese Slug Fix Log\n")
            f.write("=" * 70 + "\n\n")
            for old, new in renamed:
                f.write(f"OLD: {old}\n")
                f.write(f"NEW: {new}\n")
                f.write("-" * 70 + "\n")
        print(f"\nLog saved to: {log_file}")

if __name__ == "__main__":
    main()
