# -*- coding: utf-8 -*-
"""批次12 - 综合扩展5"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920&q=80', 's2_1'),
        ('https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1920&q=80', 's2_2'),
        ('https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920&q=80', 's2_3'),
        ('https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1920&q=80', 's2_4'),
        ('https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=1920&q=80', 's2_5'),
        ('https://images.pexels.com/photos/3762800/pexels-photo-3762800.jpeg?w=1920&auto=compress', 'sp2_1'),
        ('https://images.pexels.com/photos/267885/pexels-photo-267885.jpeg?w=1920&auto=compress', 'sp2_2'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=80', 'o2_1'),
        ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=80', 'o2_2'),
        ('https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920&q=80', 'o2_3'),
        ('https://images.unsplash.com/photo-1600880292089-90a7e086ee0c?w=1920&q=80', 'o2_4'),
        ('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=1920&auto=compress', 'op2_1'),
        ('https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?w=1920&auto=compress', 'op2_2'),
        ('https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?w=1920&auto=compress', 'op2_3'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'b2_1'),
        ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=80', 'b2_2'),
        ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80', 'b2_3'),
        ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=80', 'b2_4'),
        ('https://images.pexels.com/photos/207662/pexels-photo-207662.jpeg?w=1920&auto=compress', 'bp2_1'),
        ('https://images.pexels.com/photos/261857/pexels-photo-261857.jpeg?w=1920&auto=compress', 'bp2_2'),
    ],
    'city': [
        ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'c2_1'),
        ('https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=1920&q=80', 'c2_2'),
        ('https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80', 'c2_3'),
        ('https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=1920&q=80', 'c2_4'),
        ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'c2_5'),
        ('https://images.pexels.com/photos-2067278?w=1920&auto=compress', 'cp_1'),
        ('https://images.pexels.com/photos/585419/pexels-photo-585419.jpeg?w=1920&auto=compress', 'cp_2'),
    ],
    'people': [
        ('https://images.unsplash.com/photo-1560250097-0b93528c311a?w=1920&q=80', 'p2_1'),
        ('https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1920&q=80', 'p2_2'),
        ('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1920&q=80', 'p2_3'),
        ('https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?w=1920&auto=compress', 'pp_1'),
        ('https://images.pexels.com/photos-1681010?w=1920&auto=compress', 'pp_2'),
    ],
    'writing': [
        ('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&q=80', 'w2_1'),
        ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'w2_2'),
        ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=80', 'w2_3'),
        ('https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?w=1920&auto=compress', 'wp_1'),
    ],
    'tech': [
        ('https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80', 't2_1'),
        ('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1920&q=80', 't2_2'),
        ('https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80', 't2_3'),
        ('https://images.pexels.com/photos/1181316/pexels-photo-1181316.jpeg?w=1920&auto=compress', 'tp_1'),
        ('https://images.pexels.com/photos/270348/pexels-photo-270348.jpeg?w=1920&auto=compress', 'tp_2'),
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
    except:
        return False, f'{name}: Error'

def main():
    print('='*50)
    print('批次12 - 综合扩展5')
    print('='*50)
    total_ok = 0
    for cat, urls in URLS_BY_CAT.items():
        print(f'\n[{cat}]')
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
    print(f'\n总计: {total_ok}成功')

if __name__ == '__main__':
    main()
