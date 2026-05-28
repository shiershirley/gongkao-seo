#!/usr/bin/env python3
"""
图片选取器 - 公考SEO文章配图自动化
功能：
  - 按文章分类选取匹配主题的图片
  - 10天内不重复选同一张图
  - 每篇文章选取1-2张图
  - 更新使用记录

用法：
  python scripts/image_picker.py --category shang-an-jingyan --count 2
  python scripts/image_picker.py --category beikao-zhinan --count 1 --update
"""

import json
import random
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 项目根目录
ROOT = Path(__file__).parent.parent
USAGE_LOG = ROOT / "scripts" / "image_usage_log.json"
IMAGE_LIB = ROOT / "images" / "lib"

# 文章分类 → 适合的图片主题（优先顺序）
CATEGORY_IMAGE_MAP = {
    "guokao":           ["exam", "study", "gov", "motivation", "office"],
    "shengkao":         ["exam", "study", "motivation", "office", "books"],
    "shanghai-shegong": ["gov", "office", "people", "city", "exam"],
    "baokao-gonggao":   ["gov", "office", "writing", "exam", "study"],
    "zhengce-jiedu":    ["gov", "office", "writing", "city", "tech"],
    "beikao-zhinan":    ["study", "books", "exam", "motivation", "writing"],
    "zhenti-jiexi":     ["exam", "study", "books", "writing", "office"],
    "gangwei-fenxi":    ["office", "people", "gov", "tech", "city"],
    "shang-an-jingyan": ["exam", "motivation", "people", "study", "office"],
}

# 图片库各分类的完整文件列表（懒加载）
_IMAGE_CACHE: dict[str, list[str]] = {}


def get_images_by_theme(theme: str) -> list[str]:
    """获取指定主题的所有图片路径（相对项目根）"""
    if theme in _IMAGE_CACHE:
        return _IMAGE_CACHE[theme]

    theme_dir = IMAGE_LIB / theme
    if not theme_dir.exists():
        return []

    images = []
    for f in theme_dir.iterdir():
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            # 使用相对于public的路径（用于Markdown插入）
            rel = f"/images/lib/{theme}/{f.name}"
            images.append(rel)

    _IMAGE_CACHE[theme] = images
    return images


def load_usage_log() -> dict:
    """加载图片使用记录"""
    if not USAGE_LOG.exists():
        return {"last_updated": "", "usage": {}}
    with open(USAGE_LOG, "r", encoding="utf-8") as f:
        return json.load(f)


def save_usage_log(log: dict):
    """保存图片使用记录"""
    log["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(USAGE_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def is_recently_used(img_path: str, usage: dict, days: int = 10) -> bool:
    """判断图片是否在最近N天内被使用过"""
    if img_path not in usage:
        return False
    last_used = datetime.strptime(usage[img_path], "%Y-%m-%d")
    cutoff = datetime.now() - timedelta(days=days)
    return last_used > cutoff


def pick_images(category: str, count: int = 2, update: bool = False, article_info: dict = None) -> list[dict]:
    """
    为指定分类文章选取图片

    Args:
        category: 文章分类
        count: 选取图片数量
        update: 是否更新使用记录
        article_info: 文章信息字典（包含title, tags等），用于优化alt文本

    Returns:
        list of {"path": "/images/lib/...", "theme": "exam", "alt": "..."}
    """
    log = load_usage_log()
    usage = log.get("usage", {})
    today = datetime.now().strftime("%Y-%m-%d")

    # 获取该分类适合的主题列表
    themes = CATEGORY_IMAGE_MAP.get(category, ["study", "exam", "motivation"])

    # 收集所有可用图片（未在10天内使用）
    available = []
    for theme in themes:
        imgs = get_images_by_theme(theme)
        for img in imgs:
            if not is_recently_used(img, usage):
                available.append({"path": img, "theme": theme})

    # 如果可用图片不足，放宽限制（降到5天）
    if len(available) < count:
        print(f"[警告] 可用图片不足（{len(available)}张），放宽到5天限制", file=sys.stderr)
        available = []
        for theme in themes:
            imgs = get_images_by_theme(theme)
            for img in imgs:
                if not is_recently_used(img, usage, days=5):
                    available.append({"path": img, "theme": theme})

    # 仍然不足则不限制
    if len(available) < count:
        print("[警告] 图片几乎全部近期使用，不限制时间", file=sys.stderr)
        for theme in themes:
            imgs = get_images_by_theme(theme)
            for img in imgs:
                available.append({"path": img, "theme": theme})

    # 去重（路径去重）
    seen = set()
    deduped = []
    for item in available:
        if item["path"] not in seen:
            seen.add(item["path"])
            deduped.append(item)
    available = deduped

    if not available:
        return []

    # 随机选取
    count = min(count, len(available))
    selected = random.sample(available, count)

    # 添加alt文字（根据文章信息优化SEO关键词）
    if article_info:
        for item in selected:
            item["alt"] = generate_contextual_alt(item, article_info)
    else:
        theme_alt_map = {
            "study": "备考学习",
            "exam": "考试上岸",
            "books": "备考资料",
            "motivation": "励志备考",
            "office": "职场工作",
            "gov": "政府政务",
            "people": "职业人物",
            "city": "城市景观",
            "tech": "科技数字",
            "nature": "自然风景",
            "writing": "笔记文档",
        }
        for item in selected:
            item["alt"] = theme_alt_map.get(item["theme"], "公考备考")

    # 更新使用记录
    if update:
        for item in selected:
            usage[item["path"]] = today
        log["usage"] = usage
        save_usage_log(log)
        print(f"[已更新] {len(selected)}张图片使用记录已写入", file=sys.stderr)

    return selected


def mark_used(img_paths: list[str]):
    """标记图片为已使用"""
    log = load_usage_log()
    usage = log.get("usage", {})
    today = datetime.now().strftime("%Y-%m-%d")
    for p in img_paths:
        usage[p] = today
    log["usage"] = usage
    save_usage_log(log)


def generate_contextual_alt(item: dict, article_info: dict = None) -> str:
    """
    根据文章信息生成包含关键词的alt文本（利于SEO）
    
    Args:
        item: 图片信息字典 {"path": "...", "theme": "exam", "alt": "..."}
        article_info: 文章信息字典，包含 title, tags, category 等
    
    Returns:
        优化后的alt文本
    """
    base_alt = item.get("alt", "公考备考")
    
    if not article_info:
        return base_alt
    
    # 提取文章关键词
    title = article_info.get("title", "")
    tags = article_info.get("tags", [])
    
    # 从标题中提取核心词（去掉年份等）
    core_title = title.replace("2026年", "").replace("2026", "").strip()
    
    # 构造包含关键词的alt文本
    # 格式：主题词 + 文章核心词 + 标签词
    keywords = []
    
    # 添加主题词
    theme_keyword_map = {
        "study": "备考学习",
        "exam": "考试",
        "books": "学习资料",
        "motivation": "励志备考",
        "office": "职场",
        "gov": "政务",
        "people": "人物",
        "city": "城市",
        "tech": "科技",
        "writing": "笔记"
    }
    if item.get("theme") in theme_keyword_map:
        keywords.append(theme_keyword_map[item["theme"]])
    
    # 添加文章核心词（限制长度）
    if core_title:
        keywords.append(core_title[:10])
    
    # 添加第一个标签（如果有）
    if tags and isinstance(tags, list) and len(tags) > 0:
        keywords.append(tags[0])
    
    # 合并去重
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    
    # 生成最终alt文本
    if len(unique_keywords) >= 2:
        return "".join(unique_keywords[:3])  # 最多取前3个关键词
    else:
        return base_alt


def generate_markdown_img(item: dict, caption: str = "", article_info: dict = None) -> str:
    """生成Markdown图片语法，支持根据文章信息优化alt"""
    alt = item["alt"]
    if article_info:
        alt = generate_contextual_alt(item, article_info)
    if caption:
        alt = caption
    return f'![{alt}]({item["path"]})'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="公考SEO文章图片选取器")
    parser.add_argument("--category", required=True, help="文章分类")
    parser.add_argument("--count", type=int, default=2, help="选取图片数量(1-2)")
    parser.add_argument("--update", action="store_true", help="更新使用记录")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    images = pick_images(args.category, args.count, args.update)

    if args.json:
        print(json.dumps(images, ensure_ascii=False, indent=2))
    else:
        print(f"\n为分类 [{args.category}] 选取了 {len(images)} 张图片：\n")
        for i, img in enumerate(images, 1):
            print(f"  {i}. {img['path']}")
            print(f"     主题: {img['theme']} | ALT: {img['alt']}")
            print(f"     Markdown: {generate_markdown_img(img)}\n")
