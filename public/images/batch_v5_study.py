# -*- coding: utf-8 -*-
"""批次5 - 学习备考扩展（2nd batch）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'lib' / 'study'
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# 更多学习相关图片URL
URLS = [
    # 图书馆
    ('https://images.unsplash.com/photo-1526243741027-444d633d7365?w=1920&q=80', 'library_1'),
    ('https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1920&q=80', 'library_books_2'),
    ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'library_3'),
    # 学生学习
    ('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920&q=80', 'students_1'),
    ('https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920&q=80', 'students_2'),
    ('https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1920&q=80', 'students_3'),
    # 书桌学习
    ('https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920&q=80', 'desk_study_1'),
    ('https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1920&q=80', 'desk_study_2'),
    ('https://images.unsplash.com/photo-1589998059171-988d887df646?w=1920&q=80', 'desk_study_3'),
    # 电脑学习
    ('https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1920&q=80', 'laptop_study_1'),
    ('https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1920&q=80', 'laptop_study_2'),
    ('https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1920&q=80', 'laptop_study_3'),
    # 阅读
    ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80', 'reading_1'),
    ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=80', 'reading_2'),
    # 笔记本/笔记
    ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'notebook_1'),
    ('https://images.unsplash.com/photo-1517842645767-c639042777db?w=1920&q=80', 'notebook_2'),
    # 课堂
    ('https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1920&q=80', 'classroom_1'),
    ('https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1920&q=80', 'classroom_2'),
    # 考试准备
    ('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&q=80', 'prep_1'),
    ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=80', 'prep_2'),
    # Pexels补充
    ('https://images.pexels.com/photos/1203801/pexels-photo-1203801.jpeg?w=1920&auto=compress', 'lib_px_1'),
    ('https://images.pexels.com/photos/1370298/pexels-photo-1370298.jpeg?w=1920&auto=compress', 'study_px_1'),
    ('https://images.pexels.com/photos/2676096/pexels-photo-2676096.jpeg?w=1920&auto=compress', 'read_px_1'),
    ('https://images.pexels.com/photos/301920/pexels-photo-301920.jpeg?w=1920&auto=compress', 'book_px_1'),
    ('https://images.pexels.com/photos/2747449/pexels-photo-2747449.jpeg?w=1920&auto=compress', 'laptop_px_2'),
]

def download(url, name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        w, h = img.size
        if w <= h:
            return False, f'{name}: Not horizontal ({w}x{h})'

        safe_name = f'{name}.jpg'
        path = IMAGE_DIR / safe_name
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(path, 'JPEG', quality=85, optimize=True)
        return True, f'{name}: {w}x{h} ({len(r.content)//1024}KB)'
    except Exception as e:
        return False, f'{name}: {str(e)[:40]}'

def main():
    print('='*50)
    print('批次5 - 学习备考扩展（第2批）')
    print('='*50)
    print(f'任务数: {len(URLS)}')

    success, failed = 0, []
    for i, (url, name) in enumerate(URLS, 1):
        ok, msg = download(url, name)
        if ok:
            success += 1
            print(f'[{i}/{len(URLS)}] ✓ {msg}')
        else:
            failed.append((url, name, msg))
            print(f'[{i}/{len(URLS)}] ✗ {msg}')
        time.sleep(0.5)

    print('\n' + '='*50)
    print(f'完成: {success}成功, {len(failed)}失败')
    print(f'保存至: {IMAGE_DIR}')

if __name__ == '__main__':
    main()
