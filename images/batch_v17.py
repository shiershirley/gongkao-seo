# -*- coding: utf-8 -*-
"""批次19 - 综合扩展12"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920&q=80', 's9_1'),
        ('https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1920&q=80', 's9_2'),
        ('https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920&q=80', 's9_3'),
        ('https://images.pexels.com/photos/1203801/pexels-photo-1203801.jpeg?w=1920&auto=compress', 'sp9_1'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80', 'o9_1'),
        ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=80', 'o9_2'),
        ('https://images.unsplash.com/photo-1556761175-4b46a572b786?w=1920&q=80', 'o9_3'),
        ('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=1920&auto=compress', 'op9_1'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'b9_1'),
        ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=80', 'b9_2'),
        ('https://images.pexels.com/photos/159868/pexels-photo-159868.jpeg?w=1920&auto=compress', 'bp9_1'),
    ],
    'city': [
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'c9_1'),
        ('https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80', 'c9_2'),
        ('https://images.pexels.com/photos/2067278/pexels-photo-2067278.jpeg?w=1920&auto=compress', 'cp9_1'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'g9_1'),
        ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'g9_2'),
        ('https://images.pexels.com/photos/3739120/pexels-photo-3739120.jpeg?w=1920&auto=compress', 'gp9_1'),
    ],
    'nature': [
        ('https://images.unsplash.com/photo-1470071459604-3a5ec3aed4de?w=1920&q=80', 'n9_1'),
        ('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80', 'n9_2'),
        ('https://images.pexels.com/photos/1223648/pexels-photo-1223648.jpeg?w=1920&auto=compress', 'np9_1'),
    ],
    'tech': [
        ('https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80', 't9_1'),
        ('https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1920&q=80', 't9_2'),
        ('https://images.pexels.com/photos/1181316/pexels-photo-1181316.jpeg?w=1920&auto=compress', 'tp9_1'),
    ],
    'motivation': [
        ('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&q=80', 'm9_1'),
        ('https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=1920&q=80', 'm9_2'),
        ('https://images.pexels.com/photos/1365421/pexels-photo-1365421.jpeg?w=1920&auto=compress', 'mp9_1'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=80', 'e9_1'),
        ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=80', 'e9_2'),
        ('https://images.pexels.com/photos/3762800/pexels-photo-3762800.jpeg?w=1920&auto=compress', 'ep9_1'),
    ],
    'writing': [
        ('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&q=80', 'w9_1'),
        ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'w9_2'),
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
    print('批次19 - 综合扩展12')
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
