# ============================================================
# 公考图片库下载脚本
# 用于 gk.edu-sjtu.cn 网站图片库建设
# 使用 Pexels API 获取真实、非AI生成的高质量图片
# ============================================================

import os
import sys
import json
import time
import random
import requests
from pathlib import Path
from urllib.parse import urlparse

# ========== 配置区 ==========
# ⚠️ 请填入你的 Pexels API Key（免费注册：https://www.pexels.com/api/）
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"

# 图片保存根目录
SAVE_ROOT = Path(__file__).parent / "downloads"

# 每个主题下载数量
PER_THEME_COUNT = 50

# 图片质量：large2x, large, medium, small
IMAGE_SIZE = "large2x"

# 请求间隔（秒），避免触发限流
REQUEST_DELAY = 3

# ========== 图片主题配置 ==========
THEMES = {
    "study": {
        "name": "学习备考",
        "keywords": [
            "student studying", "library books", "reading books",
            "notebook writing", "study notes", "online learning",
            "desk workspace", "textbook education", "home study room",
            "person reading", "writing notes", "open book"
        ]
    },
    "exam": {
        "name": "考试上岸",
        "keywords": [
            "graduation ceremony", "confident person", "success achievement",
            "exam room", "university campus", "test preparation",
            "young professional", "job interview", "certificate diploma",
            "career success", "goal achieved", "aspirational person"
        ]
    },
    "career": {
        "name": "职场政府",
        "keywords": [
            "office building", "government office", "business meeting",
            "professional work", "workplace teamwork", "business person",
            "civil servant", "corporate office", "conference room",
            "computer work", "desk job", "professional attire"
        ]
    },
    "city": {
        "name": "城市政策",
        "keywords": [
            "modern city skyline", "government building china",
            "urban architecture", "city planning", "public service",
            "beijing china", "shanghai skyline", "chinese architecture",
            "government office china", "city hall", "public institution",
            "office building exterior"
        ]
    },
    "motivation": {
        "name": "励志奋斗",
        "keywords": [
            "sunrise mountains", "mountain hiking", "sunrise horizon",
            "overcoming challenges", "running exercise", "fitness determination",
            "early morning motivation", "perseverance", "growth mindset",
            "sunset landscape", "nature adventure", "peak climbing"
        ]
    },
    "books": {
        "name": "书籍资料",
        "keywords": [
            "stack of books", "old books collection", "bookshelf library",
            "knowledge wisdom", "reading lamp", "vintage books",
            "book store", "exam books", "textbook stack",
            "library interior", "literature books", "book pages"
        ]
    }
}

# ========== Pexels API 函数 ==========
def search_photos(query, per_page=15, page=1):
    """搜索 Pexels 图片"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": per_page,
        "page": page,
        "orientation": "landscape"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"  ⚠️ API 请求受限，等待 60 秒...")
            time.sleep(60)
            return search_photos(query, per_page, page)
        else:
            print(f"  ❌ API 错误: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"  ❌ 请求异常: {e}")
        return None


def download_image(photo, save_dir):
    """下载单张图片"""
    url = photo["src"].get(IMAGE_SIZE) or photo["src"].get("large") or photo["src"].get("original")

    photo_id = photo["id"]
    extension = urlparse(url).path.split('.')[-1]
    if extension not in ['jpg', 'jpeg', 'png', 'webp']:
        extension = 'jpg'
    filename = f"{photo_id}.{extension}"
    filepath = save_dir / filename

    if filepath.exists():
        print(f"  ⏭️  已存在，跳过: {filename}")
        return "skipped"

    try:
        response = requests.get(url, timeout=60, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            try:
                from PIL import Image
                with Image.open(filepath) as img:
                    width, height = img.size
                    if width < 800:
                        filepath.unlink()
                        print(f"  ⚠️ 图片过小({width}x{height})，已删除")
                        return "rejected"
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                        filepath_jpg = filepath.with_suffix('.jpg')
                        img.save(filepath_jpg, 'JPEG', quality=90)
                        filepath.unlink()
                        filepath = filepath_jpg
                        filename = filepath.name

                    if width > 1920:
                        ratio = 1920 / width
                        new_height = int(height * ratio)
                        img = img.resize((1920, new_height), Image.Resampling.LANCZOS)
                        img.save(filepath, quality=90)
                        print(f"  ✅ 下载成功: {filename} ({width}x{height})")
                    else:
                        print(f"  ✅ 下载成功: {filename} ({width}x{height})")
            except Exception as e:
                print(f"  ⚠️ 图片验证失败: {e}")
                if filepath.exists():
                    filepath.unlink()
                return "rejected"

            return "success"
        else:
            print(f"  ❌ 下载失败: HTTP {response.status_code}")
            return "failed"
    except Exception as e:
        print(f"  ❌ 下载异常: {e}")
        return "failed"


def download_theme_images(theme_key, theme_config):
    """下载某个主题的图片"""
    theme_name = theme_config["name"]
    keywords = theme_config["keywords"]

    print(f"\n{'='*60}")
    print(f"📁 主题: {theme_name} ({theme_key})")
    print(f"{'='*60}")

    save_dir = SAVE_ROOT / theme_key
    save_dir.mkdir(parents=True, exist_ok=True)

    stats = {"success": 0, "skipped": 0, "failed": 0}

    current_count = len(list(save_dir.glob("*.jpg"))) + len(list(save_dir.glob("*.png")))
    target_count = PER_THEME_COUNT
    needed = max(0, target_count - current_count)

    print(f"当前已有: {current_count} 张，需要下载: {needed} 张")

    if needed == 0:
        print("✅ 已达到目标数量，跳过")
        return stats

    page = 1
    while stats["success"] + stats["skipped"] < target_count and page <= 10:
        keyword = random.choice(keywords)
        print(f"\n🔍 搜索关键词: {keyword} (第{page}页)")

        result = search_photos(keyword, per_page=15, page=page)
        if not result or result.get("photos") is None:
            page += 1
            continue

        photos = result["photos"]
        total_results = result.get("total_results", 0)
        print(f"   找到 {len(photos)} 张图片 (总计: {total_results})")

        for photo in photos:
            if stats["success"] >= target_count:
                break

            status = download_image(photo, save_dir)
            stats[status] = stats.get(status, 0) + 1

            if status == "success":
                time.sleep(random.uniform(1, REQUEST_DELAY))
            elif status == "failed":
                time.sleep(2)

        page += 1

    total_final = len(list(save_dir.glob("*.jpg"))) + len(list(save_dir.glob("*.png")))
    print(f"\n📊 {theme_name} 统计:")
    print(f"   成功: {stats.get('success', 0)}, 跳过: {stats.get('skipped', 0)}, 失败: {stats.get('failed', 0)}")
    print(f"   当前总计: {total_final} 张")

    return stats


def main():
    """主函数"""
    print("="*60)
    print("🏛️  公考图片库下载工具")
    print("    gk.edu-sjtu.cn 专用")
    print("="*60)

    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY":
        print("\n❌ 错误: 请先配置 PEXELS_API_KEY")
        print("   1. 访问 https://www.pexels.com/api/ 免费注册")
        print("   2. 获取 API Key")
        print("   3. 修改脚本中的 PEXELS_API_KEY 配置")
        return

    SAVE_ROOT.mkdir(parents=True, exist_ok=True)

    print(f"\n📋 图片主题列表:")
    for key, config in THEMES.items():
        print(f"   • {config['name']} ({key})")

    print(f"\n🎯 目标: 每个主题 {PER_THEME_COUNT} 张横向图片")
    print(f"📁 保存位置: {SAVE_ROOT}")

    print(f"\n{'='*60}")
    response = input("确认开始下载？(y/n): ").strip().lower()
    if response != 'y':
        print("已取消")
        return

    all_stats = {}
    for theme_key, theme_config in THEMES.items():
        try:
            download_theme_images(theme_key, theme_config)
            all_stats[theme_key] = "success"
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户中断")
            break
        except Exception as e:
            print(f"\n❌ 主题 {theme_key} 出错: {e}")
            all_stats[theme_key] = "failed"

        print(f"\n⏳ 休息 5 秒后继续下一个主题...")
        time.sleep(5)

    print(f"\n{'='*60}")
    print("📊 下载完成！总览:")
    total_images = 0
    for theme_key, theme_config in THEMES.items():
        theme_dir = SAVE_ROOT / theme_key
        count = len(list(theme_dir.glob("*.jpg"))) + len(list(theme_dir.glob("*.png")))
        total_images += count
        status_icon = "✅" if all_stats.get(theme_key) == "success" else "⚠️"
        print(f"   {status_icon} {theme_config['name']}: {count} 张")
    print(f"\n🏆 总计: {total_images} 张图片")
    print(f"📁 位置: {SAVE_ROOT}")


if __name__ == "__main__":
    try:
        from PIL import Image
    except ImportError:
        print("请先安装依赖: pip install requests Pillow")
        sys.exit(1)

    main()
