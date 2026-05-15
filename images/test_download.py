# ============================================================
# 测试下载脚本 - 无需 API Key
# 使用 Lorem Picsum 获取随机真实照片进行测试
# ============================================================

# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import time
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

# ========== 配置 ==========
SAVE_ROOT = Path(__file__).parent / "test_images"
SAVE_ROOT.mkdir(parents=True, exist_ok=True)

# Lorem Picsum 测试图片列表（真实照片，横向）
TEST_IMAGES = [
    # 通用风景/建筑类（测试用）
    "https://picsum.photos/1920/1080",
    "https://picsum.photos/1920/1280",
    "https://picsum.photos/1600/900",
    "https://picsum.photos/1440/810",
    "https://picsum.photos/1920/1080",
    "https://picsum.photos/1600/900",
    "https://picsum.photos/1920/1280",
    "https://picsum.photos/1440/810",
    "https://picsum.photos/1920/1080",
    "https://picsum.photos/1600/900",
]


def download_test_image(url, filename):
    """下载测试图片"""
    filepath = SAVE_ROOT / filename

    try:
        print(f"⬇️  下载中: {filename}...")
        response = requests.get(url, timeout=30, stream=True)

        if response.status_code == 200:
            # 验证图片
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            print(f"   尺寸: {width}x{height}, 格式: {img.format}")

            # 保存
            img.save(filepath, quality=90)
            print(f"   ✅ 保存成功: {filepath}")
            return True
        else:
            print(f"   ❌ 下载失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return False


def main():
    """主函数"""
    print("="*60)
    print("🧪 图片下载测试脚本")
    print("="*60)

    print(f"\n📁 保存位置: {SAVE_ROOT}")
    print(f"🖼️  测试数量: {len(TEST_IMAGES)} 张\n")

    success_count = 0
    for i, url in enumerate(TEST_IMAGES, 1):
        filename = f"test_{i:03d}.jpg"
        if download_test_image(url, filename):
            success_count += 1
        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"📊 测试完成: {success_count}/{len(TEST_IMAGES)} 成功")

    # 列出所有下载的图片
    if SAVE_ROOT.exists():
        files = list(SAVE_ROOT.glob("*.jpg")) + list(SAVE_ROOT.glob("*.png"))
        print(f"\n📋 已下载文件:")
        for f in files:
            size_kb = f.stat().st_size // 1024
            print(f"   • {f.name} ({size_kb} KB)")


if __name__ == "__main__":
    main()
