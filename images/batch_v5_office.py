# -*- coding: utf-8 -*-
"""批次6 - 政务职场扩展（2nd batch）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'lib' / 'office'
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

URLS = [
    # 办公室场景
    ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80', 'office_1'),
    ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=80', 'office_2'),
    ('https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920&q=80', 'office_3'),
    ('https://images.unsplash.com/photo-1497366412874-3415097a27e7?w=1920&q=80', 'office_4'),
    # 会议场景
    ('https://images.unsplash.com/photo-1556761175-4b46a572b786?w=1920&q=80', 'meeting_1'),
    ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=80', 'meeting_2'),
    ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=80', 'meeting_3'),
    # 团队协作
    ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=80', 'team_1'),
    ('https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1920&q=80', 'team_2'),
    # 商务人士
    ('https://images.unsplash.com/photo-1560250097-0b93528c311a?w=1920&q=80', 'business_1'),
    ('https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1920&q=80', 'business_2'),
    ('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1920&q=80', 'business_3'),
    # 工作场景
    ('https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1920&q=80', 'work_1'),
    ('https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1920&q=80', 'work_2'),
    # 政府建筑
    ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'gov_building_1'),
    ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'gov_building_2'),
    # Pexels补充
    ('https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?w=1920&auto=compress', 'office_px_1'),
    ('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=1920&auto=compress', 'office_px_2'),
    ('https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?w=1920&auto=compress', 'office_px_3'),
    ('https://images.pexels.com/photos/3182812/pexels-photo-3182812.jpeg?w=1920&auto=compress', 'office_px_4'),
]

def download(url, name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        w, h = img.size
        if w <= h:
            return False, f'{name}: Not horizontal'

        path = IMAGE_DIR / f'{name}.jpg'
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(path, 'JPEG', quality=85, optimize=True)
        return True, f'{name}: {w}x{h}'
    except Exception as e:
        return False, f'{name}: {str(e)[:40]}'

def main():
    print('='*50)
    print('批次6 - 政务职场扩展（第2批）')
    print('='*50)

    success, failed = 0, []
    for i, (url, name) in enumerate(URLS, 1):
        ok, msg = download(url, name)
        if ok:
            success += 1
            print(f'[{i}/{len(URLS)}] ✓ {msg}')
        else:
            failed.append(msg)
            print(f'[{i}/{len(URLS)}] ✗ {msg}')
        time.sleep(0.5)

    print(f'\n完成: {success}成功, {len(failed)}失败')

if __name__ == '__main__':
    main()
