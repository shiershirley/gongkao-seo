# -*- coding: utf-8 -*-
"""批次17 - 综合扩展10"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=1920&q=80', 's7_1'),
        ('https://images.unsplash.com/photo-1529408632839-a54952c491e5?w=1920&q=80', 's7_2'),
        ('https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=1920&q=80', 's7_3'),
        ('https://images.pexels.com/photos/3660204/pexels-photo-3660204.jpeg?w=1920&auto=compress', 'sp7_1'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1556761175-4b46a572b786?w=1920&q=80', 'o7_1'),
        ('https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1920&q=80', 'o7_2'),
        ('https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1920&q=80', 'o7_3'),
        ('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=1920&auto=compress', 'op7_1'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=1920&q=80', 'b7_1'),
        ('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920&q=80', 'b7_2'),
        ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=80', 'b7_3'),
        ('https://images.pexels.com/photos/159868/pexels-photo-159868.jpeg?w=1920&auto=compress', 'bp7_1'),
    ],
    'city': [
        ('https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=1920&q=80', 'c7_1'),
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'c7_2'),
        ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'c7_3'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'g7_1'),
        ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'g7_2'),
        ('https://images.pexels.com/photos/3739120/pexels-photo-3739120.jpeg?w=1920&auto=compress', 'gp7_1'),
    ],
    'nature': [
        ('https://images.unsplash.com/photo-1470071459604-3a5ec3aed4de?w=1920&q=80', 'n7_1'),
        ('https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920&q=80', 'n7_2'),
        ('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80', 'n7_3'),
    ],
    'tech': [
        ('https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80', 't7_1'),
        ('https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1920&q=80', 't7_2'),
        ('https://images.pexels.com/photos/1181316/pexels-photo-1181316.jpeg?w=1920&auto=compress', 'tp7_1'),
    ],
    'motivation': [
        ('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&q=80', 'm7_1'),
        ('https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=1920&q=80', 'm7_2'),
        ('https://images.pexels.com/photos/1365421/pexels-photo-1365421.jpeg?w=1920&auto=compress', 'mp7_1'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920&q=80', 'e7_1'),
        ('https://images.unsplash.com/photo-1529408686214-b48b8532f72c?w=1920&q=80', 'e7_2'),
        ('https://images.pexels.com/photos/267885/pexels-photo-267885.jpeg?w=1920&auto=compress', 'ep7_1'),
    ],
    'writing': [
        ('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&q=80', 'w7_1'),
        ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'w7_2'),
        ('https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?w=1920&auto=compress', 'wp7_1'),
    ],
    'people': [
        ('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&q=80', 'p7_1'),
        ('https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=1920&q=80', 'p7_2'),
        ('https://images.pexels.com/photos/7125133/pexels-photo-7125133.jpeg?w=1920&auto=compress', 'pp7_1'),
    ],
}

def download(url, name, cat):
    headers = {'User-Agent': 'Mozilla/5.0'}
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
    except:
        return False, f'{name}: Error'

def main():
    print('批次17 - 综合扩展10')
    total_ok = 0
    for cat, urls in URLS_BY_CAT.items():
        ok = 0
        for url, name in urls:
            ok_f, msg = download(url, name, cat)
            if ok_f:
                ok += 1
                print(f'  ✓ {msg}')
            else:
                print(f'  ✗ {msg}')
            time.sleep(0.3)
        print(f'  -> {ok}/{len(urls)}')
        total_ok += ok
    print(f'总计: {total_ok}成功')

if __name__ == '__main__':
    main()
