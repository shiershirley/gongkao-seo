# -*- coding: utf-8 -*-
"""批次7 - 书籍资料扩展（2nd batch）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'lib' / 'books'
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

URLS = [
    # 书架
    ('https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=1920&q=80', 'bookshelf_1'),
    ('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920&q=80', 'bookshelf_2'),
    ('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920&q=80', 'bookshelf_3'),
    # 书堆
    ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=80', 'bookstack_1'),
    ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=80', 'bookstack_2'),
    # 打开的书
    ('https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=1920&q=80', 'openbook_1'),
    ('https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=1920&q=80', 'openbook_2'),
    # 阅读场景
    ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'reading_book_1'),
    ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80', 'reading_book_2'),
    # 教科书/备考
    ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'textbook_1'),
    ('https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=1920&q=80', 'textbook_2'),
    # Pexels
    ('https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?w=1920&auto=compress', 'books_px_1'),
    ('https://images.pexels.com/photos/261857/pexels-photo-261857.jpeg?w=1920&auto=compress', 'books_px_2'),
    ('https://images.pexels.com/photos/207662/pexels-photo-207662.jpeg?w=1920&auto=compress', 'books_px_3'),
    ('https://images.pexels.com/photos/159711/pexels-photo-159711.jpeg?w=1920&auto=compress', 'books_px_4'),
    ('https://images.pexels.com/photos/46505/pexels-photo-46505.jpeg?w=1920&auto=compress', 'books_px_5'),
    ('https://images.pexels.com/photos/159868/pexels-photo-159868.jpeg?w=1920&auto=compress', 'books_px_6'),
]

def download(url, name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        w, h = img.size
        if w <= h:
            return False, f'{name}: Not horizontal'
        path = IMAGE_DIR / f'{name}.jpg'
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(path, 'JPEG', quality=85, optimize=True)
        return True, f'{name}: {w}x{h}'
    except Exception as e:
        return False, f'{name}: {str(e)[:40]}'

def main():
    print('='*50)
    print('批次7 - 书籍资料扩展（第2批）')
    print('='*50)
    success, failed = 0, []
    for i, (url, name) in enumerate(URLS, 1):
        ok, msg = download(url, name)
        if ok:
            success += 1
            print(f'[{i}/{len(URLS)}] ✓ {msg}')
        else:
            failed.append(msg)
            print(f'[{i}/{len(URLS)}] ✗ {msg}')
        time.sleep(0.5)
    print(f'\n完成: {success}成功, {len(failed)}失败')

if __name__ == '__main__':
    main()
