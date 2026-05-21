#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片插入脚本 - 为生成的文章自动插入配图
"""

import json
import subprocess
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "content"

# 文章与分类映射
ARTICLE_CATEGORIES = [
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
    """调用image_picker.py选取图片"""
    cmd = ["python", "scripts/image_picker.py", "--category", category, "--count", "2", "--update", "--json"]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    
    # 解析输出的JSON部分
    output = result.stdout
    # 查找JSON数组
    json_match = re.search(r'\[\s*\{.*?\}\s*\]', output, re.DOTALL)
    if json_match:
        try:
            images = json.loads(json_match.group())
            return images
        except:
            pass
    
    # 如果解析失败，返回空列表
    print(f"  警告：无法解析图片选择结果")
    return []


def insert_images_to_article(article_path, images):
    """将图片插入文章内容"""
    if not article_path.exists():
        print(f"  文件不存在: {article_path}")
        return False
    
    content = article_path.read_text(encoding="utf-8")
    
    # 准备图片Markdown
    img_md = "\n\n".join([f"![]({img['path']})" for img in images])
    
    # 在第一个##标题后插入图片
    lines = content.split('\n')
    insert_pos = None
    
    for i, line in enumerate(lines):
        if line.startswith('## ') and i > 5:  # 跳过frontmatter
            insert_pos = i
            break
    
    if insert_pos:
        lines.insert(insert_pos, '\n' + img_md + '\n')
        new_content = '\n'.join(lines)
        
        # 写回文件
        article_path.write_text(new_content, encoding="utf-8")
        return True
    
    return False


def main():
    print("=" * 60)
    print("图片插入脚本")
    print("=" * 60)
    print()
    
    success_count = 0
    
    for category, filename in ARTICLE_CATEGORIES:
        print(f"处理: {filename}")
        
        # 选取图片
        print(f"  选取图片 (category={category})...")
        images = pick_images(category)
        
        if not images:
            print(f"  ⚠️  未获取到图片")
            continue
        
        print(f"  获取到 {len(images)} 张图片")
        for img in images:
            print(f"    - {img['path']}")
        
        # 插入图片
        article_path = CONTENT_DIR / category / filename
        if insert_images_to_article(article_path, images):
            print(f"  ✅ 图片已插入")
            success_count += 1
        else:
            print(f"  ❌ 插入失败")
        print()
    
    print("=" * 60)
    print(f"完成: {success_count}/{len(ARTICLE_CATEGORIES)} 篇")
    print("=" * 60)


if __name__ == "__main__":
    main()
