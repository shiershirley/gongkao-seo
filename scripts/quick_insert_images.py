#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速图片插入 - 直接调用image_picker并插入图片
"""

import subprocess
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

# 文章列表 (category, filename)
ARTICLES = [
    ("guokao", "2026-05-21-国考笔试成绩查询时间及入口.md"),
    ("guokao", "2026-05-21-国考面试礼仪全攻略：考官第一印象加分项.md"),
    ("shengkao", "2026-05-21-省考联考省份及考试时间汇总.md"),
    ("shengkao", "2026-05-21-省考申论大作文万能框架及高分技巧.md"),
    ("shanghai-shegong", "2026-05-21-上海社区工作者各区招聘计划解读.md"),
    ("shanghai-shegong", "2026-05-21-上海社工考试行测模块备考策略及真题分析.md"),
    ("gangwei-fenxi", "2026-05-21-事业单位联考《职业能力倾向测验》考情分析.md"),
    ("beikao-zhinan", "2026-05-21-零基础跨专业考生3个月公考上岸复习计划.md"),
]

def pick_images(category):
    """调用image_picker选取图片"""
    cmd = f'python scripts/image_picker.py --category {category} --count 2 --update --json'
    result = subprocess.run(cmd, shell=True, cwd=str(ROOT), capture_output=True, text=True)
    
    # 从输出中提取JSON
    output = result.stdout
    try:
        # 查找JSON数组
        start = output.find('[')
        end = output.rfind(']') + 1
        if start >= 0 and end > start:
            json_str = output[start:end]
            images = json.loads(json_str)
            return images
    except Exception as e:
        print(f"  解析图片JSON失败: {e}")
    
    return []


def insert_images(article_path, images):
    """插入图片到文章"""
    if not article_path.exists():
        print(f"  文件不存在")
        return False
    
    content = article_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 在第一个##标题后插入
    insert_idx = None
    for i, line in enumerate(lines):
        if line.startswith('## ') and i > 5:
            insert_idx = i
            break
    
    if insert_idx is None:
        print(f"  未找到插入位置")
        return False
    
    # 生成图片markdown
    img_lines = []
    for img in images:
        img_path = img.get('path', '')
        if img_path:
            img_lines.append(f"![]({img_path})")
    
    if not img_lines:
        print(f"  无有效图片")
        return False
    
    # 插入
    img_block = '\n'.join(img_lines)
    lines.insert(insert_idx, '\n' + img_block + '\n')
    
    # 写回
    new_content = '\n'.join(lines)
    article_path.write_text(new_content, encoding='utf-8')
    return True


def main():
    print("=" * 60)
    print("快速图片插入脚本")
    print("=" * 60)
    print()
    
    ok = 0
    for category, filename in ARTICLES:
        print(f"处理: {filename}")
        
        # 选取图片
        images = pick_images(category)
        if not images:
            print(f"  [跳过] 未获取到图片")
            continue
        
        print(f"  选取到 {len(images)} 张图片:")
        for img in images:
            print(f"    - {img.get('path', '')}")
        
        # 插入
        article_path = CONTENT / category / filename
        if insert_images(article_path, images):
            print(f"  [成功] 图片已插入")
            ok += 1
        else:
            print(f"  [失败] 插入出错")
        print()
    
    print("=" * 60)
    print(f"完成: {ok}/{len(ARTICLES)} 篇")
    print("=" * 60)


if __name__ == '__main__':
    main()
