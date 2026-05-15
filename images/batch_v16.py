# -*- coding: utf-8 -*-
"""批次18 - 综合扩展11"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1920&q=80', 's8_1'),
        ('https://images.unsplash.com/photo-1589998059171-988d887df646?w=1920&q=80', 's8_2'),
        ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 's8_3'),
        ('https://images.pexels.com/photos/301920/pexels-photo-301920.jpeg?w=1920&auto=compress', 'sp8_1'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=80', 'o8_1'),
        ('https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920&q=80', 'o8_2'),
        ('https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1920&q=80', 'o8_3'),
        ('https://images.pexels.com/photos/3184416/pexels-photo-3184416.jpeg?w=1920&auto=compress', 'op8_1'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80', 'b8_1'),
        ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=80', 'b8_2'),
        ('https://images.pexels.com/photos/261857/pexels-photo-261857.jpeg?w=1920&auto=compress', 'bp8_1'),
    ],
    'city': [
        ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'c8_1'),
        ('https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=1920&q=80', 'c8_2'),
        ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80', 'c8_3'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'g8_1'),
        ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'g8_2'),
        ('https://images.pexels.com/photos/585419/pexels-photo-585419.jpeg?w=1920&auto=compress', 'gp8_1'),
    ],
    'nature': [
        ('https://images.unsplash.com/photo-1470071459604-3a5ec3aed4de?w=1920&q=80', 'n8_1'),
        ('https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920&q=80', 'n8_2'),
        ('https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg?w=1920&auto=compress', 'np8_1'),
    ],
    'tech': [
        ('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1920&q=80', 't8_1'),
        ('https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80', 't8_2'),
        ('https://images.pexels.com/photos/270348/pexels-photo-270348.jpeg?w=1920&auto=compress', 'tp8_1'),
    ],
    'motivation': [
        ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'm8_1'),
        ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80', 'm8_2'),
        ('https://images.pexels.com/photos/1287142/pexels-photo-1287142.jpeg?w=1920&auto=compress', 'mp8_1'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=80', 'e8_1'),
        ('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1920&q=80', 'e8_2'),
        ('https://images.pexels.com/photos/5668859/pexels-photo-5668859.jpeg?w=1920&auto=compress', 'ep8_1'),
    ],
    'writing': [
        ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=80', 'w8_1'),
        ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'w8_2'),
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
    print('批次18 - 综合扩展11')
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
