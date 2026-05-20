#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版图片插入器 v2 - 为文章插入图片
"""

import os
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"

# 文章列表 (文件路径, 分类, 图片主题1, 图片主题2)
ARTICLES = [
    ("beikao-zhinan/2026-shegong-baoming-liucheng-xiangjie.md", "beikao-zhinan", "study", "exam"),
    ("gangwei-fenxi/2026-shegong-xinzi-goucheng-yanjing.md", "gangwei-fenxi", "office", "people"),
    ("zhengce-jiedu/2026-shegong-hukou-zhengce-jiedu.md", "zhengce-jiedu", "gov", "office"),
    ("shang-an-jingyan/2026-shegong-mianshi-yingdu-yingbian.md", "shang-an-jingyan", "exam", "motivation"),
    ("zhenti-jiexi/2026-shegong-gongji-shiti-fenxi.md", "zhenti-jiexi", "exam", "study"),
    ("baokao-gonggao/2026-shegong-baoming-jiaofei-wenti.md", "baokao-gonggao", "gov", "office"),
    ("beikao-zhinan/2026-shegong-zhengshen-cailiao.md", "beikao-zhinan", "study", "books"),
    ("gangwei-fenxi/2026-shegong-zhuanbian-bianzhi.md", "gangwei-fenxi", "office", "gov"),
]

def get_random_image(theme):
    """从指定主题文件夹中随机选择一张图片"""
    theme_dir = PROJECT_ROOT / "images" / "lib" / theme
    if not theme_dir.exists():
        print(f"主题文件夹不存在: {theme_dir}")
        return f"/images/lib/{theme}/{theme}_example.jpg"
    
    # 获取所有 jpg 文件
    images = list(theme_dir.glob("*.jpg"))
    if not images:
        return f"/images/lib/{theme}/{theme}_example.jpg"
    
    # 随机选择一张图片
    selected = random.choice(images)
    # 返回相对于项目根目录的路径
    rel_path = selected.relative_to(PROJECT_ROOT / "public")
    return f"/{rel_path}"

def insert_images_to_article(filepath, theme1, theme2):
    """为文章插入图片"""
    full_path = CONTENT_DIR / filepath
    if not full_path.exists():
        print(f"文件不存在: {full_path}")
        return False
    
    # 读取文件内容
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 如果已经有图片，跳过
    if "![" in content and "/images/lib/" in content:
        print(f"  文章已有图片，跳过: {filepath}")
        return True
    
    # 获取两张图片
    img1_path = get_random_image(theme1)
    img2_path = get_random_image(theme2)
    
    # 生成图片 Markdown
    img1_alt = f"{theme1}相关图片"
    img2_alt = f"{theme2}相关图片"
    
    image_md = f"\n\n![{img1_alt}]({img1_path})\n\n![{img2_alt}]({img2_path})\n\n"
    
    # 在第一个标题前插入图片
    first_heading_pos = content.find("\n## ")
    if first_heading_pos > 0:
        content = content[:first_heading_pos] + image_md + content[first_heading_pos:]
    
    # 写回文件
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 已为 {filepath} 插入图片")
    return True

def main():
    """主函数"""
    print("开始为文章插入图片...")
    
    success_count = 0
    for filepath, category, theme1, theme2 in ARTICLES:
        print(f"处理: {filepath}")
        if insert_images_to_article(filepath, theme1, theme2):
            success_count += 1
    
    print(f"图片插入完成！成功: {success_count}/{len(ARTICLES)}")

if __name__ == "__main__":
    main()
