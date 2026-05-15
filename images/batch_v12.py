# -*- coding: utf-8 -*-
"""批次14-16 - 综合扩展7"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1920&q=80', 's4_1'),
        ('https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1920&q=80', 's4_2'),
        ('https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920&q=80', 's4_3'),
        ('https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1920&q=80', 's4_4'),
        ('https://images.unsplash.com/photo-1476659360475-4369e475abc2?w=1920&q=80', 's4_5'),
        ('https://images.pexels.com/photos/301920/pexels-photo-301920.jpeg?w=1920&auto=compress', 'sp4_1'),
        ('https://images.pexels.com/photos/3660204/pexels-photo-3660204.jpeg?w=1920&auto=compress', 'sp4_2'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1920&q=80', 'o4_1'),
        ('https://images.unsplash.com/photo-1531545514256-b1400bc00f31?w=1920&q=80', 'o4_2'),
        ('https://images.unsplash.com/photo-1553028826-f4804a6dba3b?w=1920&q=80', 'o4_3'),
        ('https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1920&q=80', 'o4_4'),
        ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80', 'o4_5'),
        ('https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?w=1920&auto=compress', 'op4_1'),
        ('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=1920&auto=compress', 'op4_2'),
    ],
    'city': [
        ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'c4_1'),
        ('https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=1920&q=80', 'c4_2'),
        ('https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80', 'c4_3'),
        ('https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=1920&q=80', 'c4_4'),
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'c4_5'),
        ('https://images.pexels.com/photos/2067278/pexels-photo-2067278.jpeg?w=1920&auto=compress', 'cp4_1'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1491841651911-c44c30c34548?w=1920&q=80', 'b4_1'),
        ('https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=1920&q=80', 'b4_2'),
        ('https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=1920&q=80', 'b4_3'),
        ('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1920&q=80', 'b4_4'),
        ('https://images.pexels.com/photos/159711/pexels-photo-159711.jpeg?w=1920&auto=compress', 'bp4_1'),
        ('https://images.pexels.com/photos/46505/pexels-photo-46505.jpeg?w=1920&auto=compress', 'bp4_2'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'g4_1'),
        ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80', 'g4_2'),
        ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'g4_3'),
        ('https://images.pexels.com/photos/585419/pexels-photo-585419.jpeg?w=1920&auto=compress', 'gp4_1'),
    ],
    'nature': [
        ('https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=1920&q=80', 'n4_1'),
        ('https://images.unsplash.com/photo-1470071459604-3a5ec3aed4de?w=1920&q=80', 'n4_2'),
        ('https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920&q=80', 'n4_3'),
        ('https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg?w=1920&auto=compress', 'np4_1'),
    ],
    'tech': [
        ('https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80', 't4_1'),
        ('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1920&q=80', 't4_2'),
        ('https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80', 't4_3'),
        ('https://images.pexels.com/photos/1181316/pexels-photo-1181316.jpeg?w=1920&auto=compress', 'tp4_1'),
        ('https://images.pexels.com/photos/270348/pexels-photo-270348.jpeg?w=1920&auto=compress', 'tp4_2'),
    ],
    'motivation': [
        ('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&q=80', 'm4_1'),
        ('https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=1920&q=80', 'm4_2'),
        ('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80', 'm4_3'),
        ('https://images.pexels.com/photos/1365421/pexels-photo-1365421.jpeg?w=1920&auto=compress', 'mp4_1'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920&q=80', 'e4_1'),
        ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=80', 'e4_2'),
        ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=80', 'e4_3'),
        ('https://images.pexels.com/photos/3762800/pexels-photo-3762800.jpeg?w=1920&auto=compress', 'ep4_1'),
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
    print('批次14 - 综合扩展7')
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
