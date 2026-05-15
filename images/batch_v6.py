# -*- coding: utf-8 -*-
"""批次8 - 考试相关扩展"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

BASE_DIR = Path(__file__).parent

URLS_BY_CAT = {
    'exam': [
        ('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920&q=80', 'exam_grad_1'),
        ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=80', 'exam_venue_1'),
        ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=80', 'exam_team_1'),
        ('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1920&q=80', 'exam_success_1'),
        ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=80', 'exam_celebrate_1'),
        ('https://images.pexels.com/photos/267885/pexels-photo-267885.jpeg?w=1920&auto=compress', 'exam_grad_px_1'),
        ('https://images.pexels.com/photos/3762800/pexels-photo-3762800.jpeg?w=1920&auto=compress', 'exam_grad_px_2'),
        ('https://images.pexels.com/photos/2306297/pexels-photo-2306297.jpeg?w=1920&auto=compress', 'exam_success_px_1'),
        ('https://images.pexels.com/photos/3601081/pexels-photo-3601081.jpeg?w=1920&auto=compress', 'exam_cert_px_1'),
        ('https://images.pexels.com/photos/8613089/pexels-photo-8613089.jpeg?w=1920&auto=compress', 'exam_ceremony_px_1'),
    ],
    'writing': [
        ('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&q=80', 'writing_1'),
        ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'writing_2'),
        ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=80', 'writing_3'),
        ('https://images.pexels.com/photos/4857715/pexels-photo-4857715.jpeg?w=1920&auto=compress', 'writing_px_1'),
        ('https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?w=1920&auto=compress', 'writing_px_2'),
    ],
    'people': [
        ('https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1920&q=80', 'person_1'),
        ('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&q=80', 'person_2'),
        ('https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=1920&q=80', 'person_3'),
        ('https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=1920&q=80', 'person_4'),
        ('https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1920&q=80', 'person_5'),
        ('https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?w=1920&auto=compress', 'person_px_1'),
        ('https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg?w=1920&auto=compress', 'person_px_2'),
        ('https://images.pexels.com/photos/7125133/pexels-photo-7125133.jpeg?w=1920&auto=compress', 'person_px_3'),
    ],
    'gov': [
        ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'gov_1'),
        ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'gov_2'),
        ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80', 'gov_3'),
        ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'gov_4'),
        ('https://images.pexels.com/photos/2067278/pexels-photo-2067278.jpeg?w=1920&auto=compress', 'gov_px_1'),
        ('https://images.pexels.com/photos/3739120/pexels-photo-3739120.jpeg?w=1920&auto=compress', 'gov_px_2'),
    ],
}

def download(url, name, cat_dir):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    cat_path = Path('lib') / cat_dir
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
    print('批次8 - 考试/人物/政府扩展')
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
