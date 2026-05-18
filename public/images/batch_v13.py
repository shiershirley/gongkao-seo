# -*- coding: utf-8 -*-
"""批次15 - 综合扩展8"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=1920&q=80', 's5_1'),
        ('https://images.unsplash.com/photo-1511370235399-1802cae1c622?w=1920&q=80', 's5_2'),
        ('https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1920&q=80', 's5_3'),
        ('https://images.unsplash.com/photo-1530259277001-e5b8b8b8f7b5?w=1920&q=80', 's5_4'),
        ('https://images.pexels.com/photos/1203801/pexels-photo-1203801.jpeg?w=1920&auto=compress', 'sp5_1'),
        ('https://images.pexels.com/photos/1370298/pexels-photo-1370298.jpeg?w=1920&auto=compress', 'sp5_2'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=1920&q=80', 'o5_1'),
        ('https://images.unsplash.com/photo-1531973576160-7125cd663d86?w=1920&q=80', 'o5_2'),
        ('https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=1920&q=80', 'o5_3'),
        ('https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1920&q=80', 'o5_4'),
        ('https://images.unsplash.com/photo-1496503986002-6c5be36b7d15?w=1920&q=80', 'o5_5'),
        ('https://images.pexels.com/photos/3184416/pexels-photo-3184416.jpeg?w=1920&auto=compress', 'op5_1'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'b5_1'),
        ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=80', 'b5_2'),
        ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=80', 'b5_3'),
        ('https://images.pexels.com/photos/159868/pexels-photo-159868.jpeg?w=1920&auto=compress', 'bp5_1'),
        ('https://images.pexels.com/photos/1162519/pexels-photo-1162519.jpeg?w=1920&auto=compress', 'bp5_2'),
    ],
    'city': [
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'c5_1'),
        ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80', 'c5_2'),
        ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'c5_3'),
        ('https://images.pexels.com/photos/2067278/pexels-photo-2067278.jpeg?w=1920&auto=compress', 'cp5_1'),
    ],
    'nature': [
        ('https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920&q=80', 'n5_1'),
        ('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80', 'n5_2'),
        ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'n5_3'),
        ('https://images.pexels.com/photos/1032650/pexels-photo-1032650.jpeg?w=1920&auto=compress', 'np5_1'),
    ],
    'tech': [
        ('https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80', 't5_1'),
        ('https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1920&q=80', 't5_2'),
        ('https://images.pexels.com/photos/1181316/pexels-photo-1181316.jpeg?w=1920&auto=compress', 'tp5_1'),
    ],
    'motivation': [
        ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'm5_1'),
        ('https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920&q=80', 'm5_2'),
        ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80', 'm5_3'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=80', 'e5_1'),
        ('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1920&q=80', 'e5_2'),
        ('https://images.pexels.com/photos/5668859/pexels-photo-5668859.jpeg?w=1920&auto=compress', 'ep5_1'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'g5_1'),
        ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'g5_2'),
        ('https://images.pexels.com/photos/3739120/pexels-photo-3739120.jpeg?w=1920&auto=compress', 'gp5_1'),
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
    print('批次15 - 综合扩展8')
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
