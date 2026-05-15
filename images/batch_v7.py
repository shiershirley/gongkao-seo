# -*- coding: utf-8 -*-
"""批次9 - 励志/城市/风景扩展"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

BASE_DIR = Path(__file__).parent

URLS_BY_CAT = {
    'motivation': [
        ('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80', 'motiv_1'),
        ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'motiv_2'),
        ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80', 'motiv_3'),
        ('https://images.unsplash.com/photo-1518173946687-a4c036bc7d86?w=1920&q=80', 'motiv_4'),
        ('https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920&q=80', 'motiv_5'),
        ('https://images.pexels.com/photos/1365421/pexels-photo-1365421.jpeg?w=1920&auto=compress', 'motiv_px_1'),
        ('https://images.pexels.com/photos/1366919/pexels-photo-1366919.jpeg?w=1920&auto=compress', 'motiv_px_2'),
        ('https://images.pexels.com/photos/1287142/pexels-photo-1287142.jpeg?w=1920&auto=compress', 'motiv_px_3'),
    ],
    'city': [
        ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'city_shanghai_1'),
        ('https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=1920&q=80', 'city_beijing_1'),
        ('https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80', 'city_paris_1'),
        ('https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=1920&q=80', 'city_night_1'),
        ('https://images.pexels.com/photos/2067278/pexels-photo-2067278.jpeg?w=1920&auto=compress', 'city_px_1'),
    ],
    'nature': [
        ('https://images.unsplash.com/photo-1470071459604-3a5ec3aed4de?w=1920&q=80', 'nature_1'),
        ('https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920&q=80', 'nature_2'),
        ('https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920&q=80', 'nature_3'),
        ('https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=1920&q=80', 'nature_4'),
        ('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80', 'nature_beach_1'),
        ('https://images.pexels.com/photos/1223648/pexels-photo-1223648.jpeg?w=1920&auto=compress', 'nature_px_1'),
        ('https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg?w=1920&auto=compress', 'nature_px_2'),
    ],
    'tech': [
        ('https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80', 'tech_1'),
        ('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1920&q=80', 'tech_2'),
        ('https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80', 'tech_3'),
        ('https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1920&q=80', 'tech_4'),
        ('https://images.pexels.com/photos/1181316/pexels-photo-1181316.jpeg?w=1920&auto=compress', 'tech_px_1'),
        ('https://images.pexels.com/photos/270348/pexels-photo-270348.jpeg?w=1920&auto=compress', 'tech_px_2'),
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
    print('批次9 - 励志/城市/风景/科技扩展')
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
