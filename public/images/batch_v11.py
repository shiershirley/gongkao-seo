# -*- coding: utf-8 -*-
"""批次13 - 综合扩展6"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=1920&q=80', 's3_1'),
        ('https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1920&q=80', 's3_2'),
        ('https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1920&q=80', 's3_3'),
        ('https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1920&q=80', 's3_4'),
        ('https://images.pexels.com/photos/3762800/pexels-photo-3762800.jpeg?w=1920&auto=compress', 'sp3_1'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1497366412874-3415097a27e7?w=1920&q=80', 'o3_1'),
        ('https://images.unsplash.com/photo-1556761175-4b46a572b786?w=1920&q=80', 'o3_2'),
        ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=80', 'o3_3'),
        ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=80', 'o3_4'),
        ('https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?w=1920&auto=compress', 'op3_1'),
        ('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=1920&auto=compress', 'op3_2'),
        ('https://images.pexels.com/photos/3182812/pexels-photo-3182812.jpeg?w=1920&auto=compress', 'op3_3'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=1920&q=80', 'b3_1'),
        ('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920&q=80', 'b3_2'),
        ('https://images.unsplash.com/photo-1517581177682-a085bb7ffb38?w=1920&q=80', 'b3_3'),
        ('https://images.pexels.com/photos/1370298/pexels-photo-1370298.jpeg?w=1920&auto=compress', 'bp3_1'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'g3_1'),
        ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'g3_2'),
        ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80', 'g3_3'),
        ('https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=1920&q=80', 'g3_4'),
    ],
    'nature': [
        ('https://images.unsplash.com/photo-1470071459604-3a5ec3aed4de?w=1920&q=80', 'n3_1'),
        ('https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920&q=80', 'n3_2'),
        ('https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920&q=80', 'n3_3'),
        ('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80', 'n3_4'),
        ('https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg?w=1920&auto=compress', 'np3_1'),
        ('https://images.pexels.com/photos/1223648/pexels-photo-1223648.jpeg?w=1920&auto=compress', 'np3_2'),
    ],
    'motivation': [
        ('https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920&q=80', 'm3_1'),
        ('https://images.unsplash.com/photo-1518173946687-a4c036bc7d86?w=1920&q=80', 'm3_2'),
        ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80', 'm3_3'),
        ('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80', 'm3_4'),
        ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'm3_5'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1529408686214-b48b8532f72c?w=1920&q=80', 'e3_1'),
        ('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1920&q=80', 'e3_2'),
        ('https://images.pexels.com/photos/5668859/pexels-photo-5668859.jpeg?w=1920&auto=compress', 'ep3_1'),
        ('https://images.pexels.com/photos/6552539/pexels-photo-6552539.jpeg?w=1920&auto=compress', 'ep3_2'),
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
    print('批次13 - 综合扩展6')
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
