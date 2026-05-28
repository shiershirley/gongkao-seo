#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片Sitemap生成脚本
- 扫描 images/lib/ 目录，生成图片sitemap.xml
- 包含所有图片的URL、标题、描述（从文件名提取）
- 可直接提交到百度/Google站长平台
"""

import sys
from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).parent.parent
IMAGES_DIR = ROOT / "public" / "images" / "lib"
SITEMAP_PATH = ROOT / "public" / "image-sitemap.xml"

# 如果public/images不存在，尝试从images目录
if not IMAGES_DIR.exists():
    IMAGES_DIR = ROOT / "images" / "lib"
    SITEMAP_PATH = ROOT / "public" / "image-sitemap.xml"

# 确保public目录存在
PUBLIC_DIR = ROOT / "public"
PUBLIC_DIR.mkdir(exist_ok=True)

def get_image_info(image_path):
    """从图片路径提取信息"""
    # 获取相对路径
    rel_path = image_path.relative_to(ROOT / "public") if "public" in str(image_path) else image_path.relative_to(ROOT)

    # 生成URL
    url = f"https://gk.edu-sjtu.cn/{rel_path.as_posix()}"

    # 从文件名提取标题（去掉扩展名，替换连字符为空格）
    title = image_path.stem.replace('-', ' ').replace('_', ' ')
    title = ' '.join(word.capitalize() for word in title.split())

    # 尝试从所在目录名推断分类
    parent_dir = image_path.parent.name
    category_map = {
        'exam': '考试相关',
        'study': '学习场景',
        'people': '人物场景',
        'office': '办公场景',
        'nature': '自然风景',
        'city': '城市建筑',
        'books': '书籍阅读',
        'tech': '科技元素',
        'gov': '政府相关',
        'motivation': '励志激励',
        'writing': '写作场景',
    }
    category = category_map.get(parent_dir, '通用')

    # 生成描述
    description = f"{title} - 公考备考相关图片，适用于{category}场景"

    return {
        'url': url,
        'title': title,
        'caption': title,
        'description': description,
        'license': 'https://creativecommons.org/licenses/by/4.0/',
    }


def generate_image_sitemap(images):
    """生成图片sitemap XML"""
    now = datetime.now().strftime("%Y-%m-%d")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
<!-- 图片Sitemap 生成时间：{now} -->
<!-- 共 {len(images)} 张图片 -->

"""

    # 按目录分组（每个页面包含该目录下的图片）
    from collections import defaultdict
    dir_images = defaultdict(list)

    for img in images:
        parent_dir = img.parent.name
        dir_images[parent_dir].append(img)

    # 为每个目录生成一个URL条目
    base_url = "https://gk.edu-sjtu.cn"

    for dir_name, dir_imgs in sorted(dir_images.items()):
        page_url = f"{base_url}/{dir_name}/" if dir_name != 'lib' else f"{base_url}/"

        xml += f"  <url>\n"
        xml += f"    <loc>{page_url}</loc>\n"

        for img in dir_imgs[:50]:  # 每个页面最多50张图片（sitemap限制）
            info = get_image_info(img)
            xml += f"    <image:image>\n"
            xml += f"      <image:loc>{info['url']}</image:loc>\n"
            xml += f"      <image:caption>{info['caption']}</image:caption>\n"
            xml += f"      <image:title>{info['title']}</image:title>\n"
            xml += f"      <image:license>{info['license']}</image:license>\n"
            xml += f"    </image:image>\n"

        xml += f"  </url>\n\n"

    xml += "</urlset>\n"
    return xml


def main():
    print("=" * 60)
    print("图片Sitemap生成工具")
    print("=" * 60)
    print()

    # 检查图片目录
    if not IMAGES_DIR.exists():
        print(f"[错误] 图片目录不存在: {IMAGES_DIR}")
        print("请确认图片目录路径是否正确")
        sys.exit(1)

    print(f"图片目录: {IMAGES_DIR}")

    # 扫描图片文件
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    images = []

    for ext in image_extensions:
        images.extend(IMAGES_DIR.rglob(f"*{ext}"))
        images.extend(IMAGES_DIR.rglob(f"*{ext.upper()}"))

    print(f"找到 {len(images)} 张图片")
    print()

    if len(images) == 0:
        print("[警告] 未找到图片文件")
        sys.exit(0)

    # 生成sitemap
    print("正在生成图片sitemap...")
    sitemap_xml = generate_image_sitemap(images)

    # 写入文件
    SITEMAP_PATH.write_text(sitemap_xml, encoding='utf-8')

    print(f"[成功] 已生成: {SITEMAP_PATH.relative_to(ROOT)}")
    print(f"   包含 {len(images)} 张图片的索引信息")
    print()

    # 输出提交提示
    print("=" * 60)
    print("提交到站长平台：")
    print("=" * 60)
    print()
    print("百度站长平台：")
    print("  1. 登录 https://ziyuan.baidu.com/")
    print(f"  2. 进入「链接提交」->「sitemap」")
    print(f"  3. 提交: https://gk.edu-sjtu.cn/image-sitemap.xml")
    print()
    print("Google Search Console：")
    print("  1. 登录 https://search.google.com/search-console")
    print(f"  2. 进入「站点地图」")
    print(f"  3. 提交: https://gk.edu-sjtu.cn/image-sitemap.xml")
    print()
    print("=" * 60)

    # 在robots.txt中添加sitemap引用
    robots_path = ROOT / "public" / "robots.txt"
    if robots_path.exists():
        robots_content = robots_path.read_text(encoding='utf-8')
        if 'image-sitemap.xml' not in robots_content:
            robots_content += "\nSitemap: https://gk.edu-sjtu.cn/image-sitemap.xml\n"
            robots_path.write_text(robots_content, encoding='utf-8')
            print("[成功] 已更新 robots.txt，添加 sitemap 引用")
    else:
        print("[提示]  robots.txt 不存在，请手动添加:")
        print("   Sitemap: https://gk.edu-sjtu.cn/image-sitemap.xml")


if __name__ == '__main__':
    main()
