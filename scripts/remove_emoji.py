#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量移除文章中的emoji表情符号，替换为纯文本标记
避免Windows GBK编码问题
"""

import os
import re
from pathlib import Path

# emoji替换映射
EMOJI_MAP = {
    '🎯': '[专属]',
    '📄': '[资料]',
    '📚': '[书籍]',
    '🎥': '[视频]',
    '✅': '[成功]',
    '⚠️': '[提示]',
    '❌': '[失败]',
    '⏭️': '[跳过]',
    '📊': '[数据]',
    '📈': '[上升]',
    '📉': '[下降]',
    '💡': '[建议]',
    '🔥': '[热门]',
    '⭐': '[星级]',
    '🌟': '[明星]',
}

def remove_emoji(text):
    """移除或替换emoji"""
    # 先替换已知emoji
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    
    # 移除其他emoji（Unicode范围）
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def process_file(md_path):
    """处理单个文件"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = remove_emoji(content)
        
        if new_content != content:
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "已移除emoji"
        return False, "无需修改"
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    base_dir = Path("content")
    if not base_dir.exists():
        print(f"[失败] 目录不存在: {base_dir}")
        return
    
    print("=" * 70)
    print("批量移除文章Emoji表情符号")
    print("=" * 70)
    
    processed = 0
    modified = 0
    
    for category_dir in base_dir.iterdir():
        if not category_dir.is_dir():
            continue
        
        for md_file in category_dir.glob("*.md"):
            processed += 1
            is_modified, msg = process_file(md_file)
            if is_modified:
                modified += 1
                if modified <= 10 or modified % 100 == 0:
                    print(f"[{modified}] {md_file.name}")
    
    print("\n" + "=" * 70)
    print(f"处理完成")
    print(f"  扫描: {processed} 篇")
    print(f"  修改: {modified} 篇")
    print("=" * 70)

if __name__ == "__main__":
    main()
