# -*- coding: utf-8 -*-
"""批次10 - 综合扩展3"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

BASE_DIR = Path(__file__).parent

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'study_more_1'),
        ('https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920&q=80', 'study_more_2'),
        ('https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1920&q=80', 'study_more_3'),
        ('https://images.unsplash.com/photo-1476659360475-4369e475abc2?w=1920&q=80', 'study_more_4'),
        ('https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=1920&q=80', 'study_more_5'),
        ('https://images.unsplash.com/photo-1497636577773-f1233cc34d71?w=1920&q=80', 'study_more_6'),
        ('https://images.unsplash.com/photo-1542626991-cbc4e32524cc?w=1920&q=80', 'study_more_7'),
        ('https://images.unsplash.com/photo-1583468982228-19f19164aee2?w=1920&q=80', 'study_more_8'),
        ('https://images.pexels.com/photos/301920/pexels-photo-301920.jpeg?w=1920&auto=compress', 'study_px_1'),
        ('https://images.pexels.com/photos/3660204/pexels-photo-3660204.jpeg?w=1920&auto=compress', 'study_px_2'),
        ('https://images.pexels.com/photos/4050315/pexels-photo-4050315.jpeg?w=1920&auto=compress', 'study_px_3'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1920&q=80', 'office_more_1'),
        ('https://images.unsplash.com/photo-1531545514256-b1400bc00f31?w=1920&q=80', 'office_more_2'),
        ('https://images.unsplash.com/photo-1553028826-f4804a6dba3b?w=1920&q=80', 'office_more_3'),
        ('https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1920&q=80', 'office_more_4'),
        ('https://images.pexels.com/photos/3182730/pexels-photo-3182730.jpeg?w=1920&auto=compress', 'office_px_5'),
        ('https://images.pexels.com/photos/3183177/pexels-photo-3183177.jpeg?w=1920&auto=compress', 'office_px_6'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=80', 'books_more_1'),
        ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=80', 'books_more_2'),
        ('https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=1920&q=80', 'books_more_3'),
        ('https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=1920&q=80', 'books_more_4'),
        ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80', 'books_more_5'),
        ('https://images.pexels.com/photos/2676096/pexels-photo-2676096.jpeg?w=1920&auto=compress', 'books_px_7'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=80', 'exam_more_1'),
        ('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1920&q=80', 'exam_more_2'),
        ('https://images.pexels.com/photos/5668859/pexels-photo-5668859.jpeg?w=1920&auto=compress', 'exam_px_1'),
        ('https://images.pexels.com/photos/8612937/pexels-photo-8612937.jpeg?w=1920&auto=compress', 'exam_px_2'),
    ],
}

def download(url, name, cat):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    cat_path = Path('lib') / cat
    cat_path.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        w, h = img.size
        if w <= h:
            return False, f'{name}: Not horizontal'
        path = cat_path / f'{name}.jpg'
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(path, 'JPEG', quality=85, optimize=True)
        return True, f'{name}: {w}x{h}'
    except Exception as e:
        return False, f'{name}: {str(e)[:40]}'

def main():
    print('='*50)
    print('批次10 - 综合扩展3')
    print('='*50)
    total_ok, total_fail = 0, 0
    for cat, urls in URLS_BY_CAT.items():
        print(f'\n[{cat}]')
        ok, fail = 0, 0
        for i, (url, name) in enumerate(urls, 1):
            ok_f, msg = download(url, name, cat)
            if ok_f:
                ok += 1
                print(f'  ✓ {msg}')
            else:
                fail += 1
                print(f'  ✗ {msg}')
            time.sleep(0.3)
        print(f'  -> {ok}成功, {fail}失败')
        total_ok += ok
        total_fail += fail
    print(f'\n总计: {total_ok}成功, {total_fail}失败')

if __name__ == '__main__':
    main()
