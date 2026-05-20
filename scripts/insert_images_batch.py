#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量插入图片到文章，并进行Frontmatter校验
"""

import sys
import json
import random
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"

# 文章列表 (文件路径, 分类)
ARTICLES = [
    ("beikao-zhinan/2026-shegong-baoming-liucheng-xiangjie.md", "beikao-zhinan"),
    ("gangwei-fenxi/2026-shegong-xinzi-goucheng-yanjing.md", "gangwei-fenxi"),
    ("zhengce-jiedu/2026-shegong-hukou-zhengce-jiedu.md", "zhengce-jiedu"),
    ("shang-an-jingyan/2026-shegong-mianshi-yingdu-yingbian.md", "shang-an-jingyan"),
    ("zhenti-jiexi/2026-shegong-gongji-shiti-fenxi.md", "zhenti-jiexi"),
    ("baokao-gonggao/2026-shegong-baoming-jiaofei-wenti.md", "baokao-gonggao"),
    ("beikao-zhinan/2026-shegong-zhengshen-cailiao.md", "beikao-zhinan"),
    ("gangwei-fenxi/2026-shegong-zhuanbian-bianzhi.md", "gangwei-fenxi"),
]

# 图片主题映射（模拟 image_picker.py 的功能）
CATEGORY_THEME_MAP = {
    "beikao-zhinan": ["study", "books", "exam", "motivation", "writing"],
    "gangwei-fenxi": ["office", "people", "gov", "tech", "city"],
    "zhengce-jiedu": ["gov", "office", "writing", "city", "tech"],
    "shang-an-jingyan": ["exam", "motivation", "people", "study", "office"],
    "zhenti-jiexi": ["exam", "study", "books", "writing", "office"],
    "baokao-gonggao": ["gov", "office", "writing", "exam", "study"],
}

def pick_images_mock(category, count=2):
    """模拟图片选取（实际应用中应调用 image_picker.py）"""
    themes = CATEGORY_THEME_MAP.get(category, ["exam", "study"])
    selected_themes = random.sample(themes, min(count, len(themes)))
    
    images = []
    for theme in selected_themes:
        # 模拟图片路径
        image_path = f"/images/lib/{theme}/{theme}_example.jpg"
        images.append({"path": image_path, "alt": f"{category}相关图片", "theme": theme})
    
    return images

def insert_images_to_article(filepath, category):
    """为文章插入图片"""
    full_path = CONTENT_DIR / filepath
    if not full_path.exists():
        print(f"文件不存在: {full_path}")
        return False
    
    # 读取文件内容
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 选取图片
    images = pick_images_mock(category, count=2)
    
    # 生成图片 Markdown
    image_md = "\n\n"
    for img in images:
        image_path = img.get("path", "")
        alt_text = img.get("alt", "相关图片")
        image_md += f"![{alt_text}]({image_path})\n\n"
    
    # 在第一个标题前插入图片
    first_heading_pos = content.find("\n## ")
    if first_heading_pos > 0:
        content = content[:first_heading_pos] + image_md + content[first_heading_pos:]
    
    # 写回文件
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 已为 {filepath} 插入图片")
    return True

def validate_frontmatter(filepath):
    """简单的Frontmatter校验"""
    full_path = CONTENT_DIR / filepath
    if not full_path.exists():
        return False, "文件不存在"
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否有 frontmatter
    if not content.startswith("---"):
        return False, "缺少 frontmatter 开始标记"
    
    # 查找结束的 ---
    end_pos = content.find("---", 3)
    if end_pos == -1:
        return False, "缺少 frontmatter 结束标记"
    
    frontmatter = content[3:end_pos].strip()
    
    # 检查必需字段
    required_fields = ["title", "date", "description", "category", "tags", "author"]
    missing_fields = []
    
    for field in required_fields:
        if field not in frontmatter:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"缺少必需字段: {missing_fields}"
    
    # 检查 description 中是否有未转义的双引号
    desc_start = frontmatter.find("description:")
    if desc_start > -1:
        desc_end = frontmatter.find("\n", desc_start)
        if desc_end == -1:
            desc_end = len(frontmatter)
        desc_content = frontmatter[desc_start:desc_end]
        
        # 检查是否有未转义的双引号（不是日文引号的）
        if '"' in desc_content and "「" not in desc_content and "」" not in desc_content:
            return False, "description 中可能含有未转义的双引号"
    
    return True, "Frontmatter 校验通过"

def main():
    """主函数"""
    print(f"开始为文章插入图片并进行 Frontmatter 校验...")
    
    success_count = 0
    for filepath, category in ARTICLES:
        print(f"\n处理: {filepath}")
        
        # 插入图片
        if insert_images_to_article(filepath, category):
            # 校验 Frontmatter
            is_valid, message = validate_frontmatter(filepath)
            if is_valid:
                print(f"   ✅ Frontmatter 校验通过")
                success_count += 1
            else:
                print(f"   ❌ Frontmatter 校验失败: {message}")
    
    print(f"\n处理完成！成功: {success_count}/{len(ARTICLES)}")

if __name__ == "__main__":
    main()
