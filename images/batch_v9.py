# -*- coding: utf-8 -*-
"""批次11-14 - 综合扩展4"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

URLS_BY_CAT = {
    'study': [
        ('https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=1920&q=80', 's_1'),
        ('https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=1920&q=80', 's_2'),
        ('https://images.unsplash.com/photo-1511370235399-1802cae1c622?w=1920&q=80', 's_3'),
        ('https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1920&q=80', 's_4'),
        ('https://images.unsplash.com/photo-1530259277001-e5b8b8b8f7b5?w=1920&q=80', 's_5'),
        ('https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=1920&q=80', 's_6'),
        ('https://images.unsplash.com/photo-1529408632839-a54952c491e5?w=1920&q=80', 's_7'),
        ('https://images.pexels.com/photos/301920/pexels-photo-301920.jpeg?w=1920&auto=compress', 'sp_1'),
        ('https://images.pexels.com/photos/3660204/pexels-photo-3660204.jpeg?w=1920&auto=compress', 'sp_2'),
        ('https://images.pexels.com/photos/4050315/pexels-photo-4050315.jpeg?w=1920&auto=compress', 'sp_3'),
        ('https://images.pexels.com/photos/5082579/pexels-photo-5082579.jpeg?w=1920&auto=compress', 'sp_4'),
        ('https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?w=1920&auto=compress', 'sp_5'),
    ],
    'office': [
        ('https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1920&q=80', 'o_1'),
        ('https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=1920&q=80', 'o_2'),
        ('https://images.unsplash.com/photo-1531973576160-7125cd663d86?w=1920&q=80', 'o_3'),
        ('https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=1920&q=80', 'o_4'),
        ('https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1920&q=80', 'o_5'),
        ('https://images.unsplash.com/photo-1496503986002-6c5be36b7d15?w=1920&q=80', 'o_6'),
        ('https://images.pexels.com/photos/3184416/pexels-photo-3184416.jpeg?w=1920&auto=compress', 'op_1'),
        ('https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?w=1920&auto=compress', 'op_2'),
        ('https://images.pexels.com/photos/3182811/pexels-photo-3182811.jpeg?w=1920&auto=compress', 'op_3'),
        ('https://images.pexels.com/photos/3182730/pexels-photo-3182730.jpeg?w=1920&auto=compress', 'op_4'),
    ],
    'books': [
        ('https://images.unsplash.com/photo-1491841651911-c44c30c34548?w=1920&q=80', 'b_1'),
        ('https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=1920&q=80', 'b_2'),
        ('https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=1920&q=80', 'b_3'),
        ('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1920&q=80', 'b_4'),
        ('https://images.pexels.com/photos/159711/pexels-photo-159711.jpeg?w=1920&auto=compress', 'bp_1'),
        ('https://images.pexels.com/photos/46505/pexels-photo-46505.jpeg?w=1920&auto=compress', 'bp_2'),
        ('https://images.pexels.com/photos/159868/pexels-photo-159868.jpeg?w=1920&auto=compress', 'bp_3'),
        ('https://images.pexels.com/photos/1162519/pexels-photo-1162519.jpeg?w=1920&auto=compress', 'bp_4'),
    ],
    'exam': [
        ('https://images.unsplash.com/photo-1529408686214-b48b8532f72c?w=1920&q=80', 'e_1'),
        ('https://images.unsplash.com/photo-143108HTTP?w=1920&q=80', 'e_2'),
        ('https://images.pexels.com/photos/5668859/pexels-photo-5668859.jpeg?w=1920&auto=compress', 'ep_1'),
        ('https://images.pexels.com/photos/8612937/pexels-photo-8612937.jpeg?w=1920&auto=compress', 'ep_2'),
        ('https://images.pexels.com/photos/6552539/pexels-photo-6552539.jpeg?w=1920&auto=compress', 'ep_3'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'g_1'),
        ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'g_2'),
        ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'g_3'),
        ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80', 'g_4'),
        ('https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=1920&q=80', 'g_5'),
        ('https://images.pexels.com/photos/3739120/pexels-photo-3739120.jpeg?w=1920&auto=compress', 'gp_1'),
        ('https://images.pexels.com/photos/585419/pexels-photo-585419.jpeg?w=1920&auto=compress', 'gp_2'),
        ('https://images.pexels.com/photos/1480714378408-67cf0d13bc1b?w=1920&auto=compress', 'gp_3'),
    ],
    'motivation': [
        ('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&q=80', 'm_1'),
        ('https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=1920&q=80', 'm_2'),
        ('https://images.unsplash.com/photo-1518173946687-a4c036bc7d86?w=1920&q=80', 'm_3'),
        ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80', 'm_4'),
        ('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80', 'm_5'),
        ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'm_6'),
        ('https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920&q=80', 'm_7'),
        ('https://images.pexels.com/photos-1223648?w=1920&auto=compress', 'mp_1'),
        ('https://images.pexels.com/photos/1365421/pexels-photo-1365421.jpeg?w=1920&auto=compress', 'mp_2'),
        ('https://images.pexels.com/photos/1287142/pexels-photo-1287142.jpeg?w=1920&auto=compress', 'mp_3'),
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
    print('批次11 - 综合扩展4')
    print('='*50)
    total_ok, total_fail = 0, 0
    for cat, urls in URLS_BY_CAT.items():
        print(f'\n[{cat}]')
        ok, fail = 0, 0
        for url, name in urls:
            ok_f, msg = download(url, name, cat)
            if ok_f:
                ok += 1
                print(f'  ✓ {msg}')
            else:
                fail += 1
                print(f'  ✗ {msg}')
            time.sleep(0.3)
        print(f'  -> {ok}/{len(urls)}')
        total_ok += ok
        total_fail += fail
    print(f'\n总计: {total_ok}成功, {total_fail}失败')

if __name__ == '__main__':
    main()
