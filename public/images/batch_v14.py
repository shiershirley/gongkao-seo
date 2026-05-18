# -*- coding: utf-8 -*-
"""批次16 - 综合扩展9"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1497636577773-f1233cc34d71?w=1920&q=80', 's6_1'),
        ('https://images.unsplash.com/photo-1542626991-cbc4e32524cc?w=1920&q=80', 's6_2'),
        ('https://images.unsplash.com/photo-1583468982228-19f19164aee2?w=1920&q=80', 's6_3'),
        ('https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=1920&q=80', 's6_4'),
        ('https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920&q=80', 's6_5'),
        ('https://images.pexels.com/photos/5082579/pexels-photo-5082579.jpeg?w=1920&auto=compress', 'sp6_1'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1920&q=80', 'o6_1'),
        ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80', 'o6_2'),
        ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=80', 'o6_3'),
        ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=80', 'o6_4'),
        ('https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920&q=80', 'o6_5'),
        ('https://images.pexels.com/photos/3182730/pexels-photo-3182730.jpeg?w=1920&auto=compress', 'op6_1'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=80', 'b6_1'),
        ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80', 'b6_2'),
        ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=80', 'b6_3'),
        ('https://images.pexels.com/photos/2676096/pexels-photo-2676096.jpeg?w=1920&auto=compress', 'bp6_1'),
    ],
    'city': [
        ('https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=1920&q=80', 'c6_1'),
        ('https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80', 'c6_2'),
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'c6_3'),
        ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'c6_4'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'g6_1'),
        ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80', 'g6_2'),
        ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'g6_3'),
        ('https://images.pexels.com/photos/585419/pexels-photo-585419.jpeg?w=1920&auto=compress', 'gp6_1'),
    ],
    'nature': [
        ('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&q=80', 'n6_1'),
        ('https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=1920&q=80', 'n6_2'),
        ('https://images.unsplash.com/photo-1470071459604-3a5ec3aed4de?w=1920&q=80', 'n6_3'),
        ('https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg?w=1920&auto=compress', 'np6_1'),
    ],
    'tech': [
        ('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1920&q=80', 't6_1'),
        ('https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80', 't6_2'),
        ('https://images.pexels.com/photos/270348/pexels-photo-270348.jpeg?w=1920&auto=compress', 'tp6_1'),
    ],
    'motivation': [
        ('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80', 'm6_1'),
        ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'm6_2'),
        ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80', 'm6_3'),
        ('https://images.pexels.com/photos/1287142/pexels-photo-1287142.jpeg?w=1920&auto=compress', 'mp6_1'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=80', 'e6_1'),
        ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=80', 'e6_2'),
        ('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1920&q=80', 'e6_3'),
        ('https://images.pexels.com/photos/3762800/pexels-photo-3762800.jpeg?w=1920&auto=compress', 'ep6_1'),
    ],
    'writing': [
        ('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&q=80', 'w6_1'),
        ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=80', 'w6_2'),
        ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'w6_3'),
    ],
    'people': [
        ('https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1920&q=80', 'p6_1'),
        ('https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1920&q=80', 'p6_2'),
        ('https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?w=1920&auto=compress', 'pp6_1'),
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
    print('批次16 - 综合扩展9')
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
