# -*- coding: utf-8 -*-
"""
公考网站图片库批量下载脚本 V3
使用预定义高质量图片URL（Unsplash/Pexels直链）
无需API Key，直接下载
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import time
import json
import hashlib
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========== 配置 ==========
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'images'
INDEX_FILE = BASE_DIR / 'image_index.json'
MAX_WORKERS = 5  # 并行下载数
REQUEST_DELAY = 1  # 请求延时

# ========== 预定义图片URL列表（公考主题）==========
IMAGE_URLS = {
    '01_study': {
        'name': '学习备考',
        'urls': [
            ('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920&q=80', 'library_1'),
            ('https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920&q=80', 'study_desk_1'),
            ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'books_1'),
            ('https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1920&q=80', 'library_books_1'),
            ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'notebook_1'),
            ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=80', 'books_2'),
            ('https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=1920&q=80', 'books_shelf_1'),
            ('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920&q=80', 'library_2'),
            ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=80', 'books_3'),
            ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80', 'books_4'),
            ('https://images.unsplash.com/photo-1491841651911-c44c30c34548?w=1920&q=80', 'study_1'),
            ('https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=1920&q=80', 'books_5'),
            ('https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=1920&q=80', 'student_1'),
            ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=80', 'books_6'),
            ('https://images.unsplash.com/photo-1589998059171-988d887df646?w=1920&q=80', 'reading_1'),
            ('https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=1920&q=80', 'study_3'),
            ('https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920&q=80', 'education_1'),
            ('https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1920&q=80', 'library_3'),
            ('https://images.unsplash.com/photo-1476659360475-4369e475abc2?w=1920&q=80', 'study_4'),
            ('https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&cs=tinysrgb&w=1920', 'books_px_1'),
            ('https://images.pexels.com/photos/207662/pexels-photo-207662.jpeg?auto=compress&cs=tinysrgb&w=1920', 'library_px_1'),
            ('https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?auto=compress&cs=tinysrgb&w=1920', 'book_px_1'),
            ('https://images.pexels.com/photos/2747449/pexels-photo-2747449.jpeg?auto=compress&cs=tinysrgb&w=1920', 'laptop_px_1'),
            ('https://images.pexels.com/photos/1203801/pexels-photo-1203801.jpeg?auto=compress&cs=tinysrgb&w=1920', 'library_px_2'),
            ('https://images.pexels.com/photos/1370298/pexels-photo-1370298.jpeg?auto=compress&cs=tinysrgb&w=1920', 'study_px_1'),
            ('https://images.pexels.com/photos/261857/pexels-photo-261857.jpeg?auto=compress&cs=tinysrgb&w=1920', 'books_px_3'),
            ('https://images.pexels.com/photos/2676096/pexels-photo-2676096.jpeg?auto=compress&cs=tinysrgb&w=1920', 'reading_px_1'),
        ]
    },
    '02_exam': {
        'name': '考试上岸',
        'urls': [
            ('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920&q=80', 'graduation_1'),
            ('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1920&q=80', 'success_1'),
            ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=80', 'team_success_1'),
            ('https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1920&q=80', 'certificate_1'),
            ('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&q=80', 'trophy_1'),
            ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=80', 'celebration_1'),
            ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=80', 'auditorium_1'),
            ('https://images.pexels.com/photos/267885/pexels-photo-267885.jpeg?auto=compress&cs=tinysrgb&w=1920', 'graduation_px_1'),
            ('https://images.pexels.com/photos/3762800/pexels-photo-3762800.jpeg?auto=compress&cs=tinysrgb&w=1920', 'graduation_px_2'),
            ('https://images.pexels.com/photos/2306297/pexels-photo-2306297.jpeg?auto=compress&cs=tinysrgb&w=1920', 'success_px_1'),
            ('https://images.pexels.com/photos/3601081/pexels-photo-3601081.jpeg?auto=compress&cs=tinysrgb&w=1920', 'diploma_px_1'),
        ]
    },
    '03_career': {
        'name': '政务职场',
        'urls': [
            ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80', 'office_1'),
            ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'city_1'),
            ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'cityscape_1'),
            ('https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920&q=80', 'meeting_1'),
            ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=80', 'teamwork_1'),
            ('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1920&q=80', 'professional_1'),
            ('https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1920&q=80', 'woman_professional_1'),
            ('https://images.unsplash.com/photo-1556761175-4b46a572b786?w=1920&q=80', 'business_1'),
            ('https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920&q=80', 'office_2'),
            ('https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=1920', 'office_px_1'),
            ('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=1920', 'teamwork_px_1'),
            ('https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=1920', 'business_px_1'),
            ('https://images.pexels.com/photos/3182812/pexels-photo-3182812.jpeg?auto=compress&cs=tinysrgb&w=1920', 'office_px_2'),
        ]
    },
    '04_city': {
        'name': '城市政策',
        'urls': [
            ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=80', 'beijing_1'),
            ('https://images.unsplash.com/photo-1508804052814-cd3ba865a116?w=1920&q=80', 'shanghai_1'),
            ('https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?w=1920&q=80', 'city_2'),
            ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80', 'skyline_1'),
            ('https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80', 'paris_1'),
            ('https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=1920&q=80', 'beijing_2'),
            ('https://images.pexels.com/photos/2067278/pexels-photo-2067278.jpeg?auto=compress&cs=tinysrgb&w=1920', 'city_px_1'),
            ('https://images.pexels.com/photos/3739120/pexels-photo-3739120.jpeg?auto=compress&cs=tinysrgb&w=1920', 'buildings_px_1'),
        ]
    },
    '05_motivation': {
        'name': '励志奋斗',
        'urls': [
            ('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80', 'mountain_1'),
            ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'sunrise_1'),
            ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80', 'mountain_2'),
            ('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&q=80', 'nature_1'),
            ('https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=1920&q=80', 'forest_1'),
            ('https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920&q=80', 'landscape_1'),
            ('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&q=80', 'forest_2'),
            ('https://images.unsplash.com/photo-1518173946687-a4c036bc7d86?w=1920&q=80', 'path_1'),
            ('https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920&q=80', 'road_1'),
            ('https://images.pexels.com/photos/1365421/pexels-photo-1365421.jpeg?auto=compress&cs=tinysrgb&w=1920', 'mountain_px_1'),
            ('https://images.pexels.com/photos/1366919/pexels-photo-1366919.jpeg?auto=compress&cs=tinysrgb&w=1920', 'sunrise_px_1'),
            ('https://images.pexels.com/photos/1287142/pexels-photo-1287142.jpeg?auto=compress&cs=tinysrgb&w=1920', 'nature_px_1'),
        ]
    },
    '06_books': {
        'name': '书籍资料',
        'urls': [
            ('https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=1920&q=80', 'bookshelf_1'),
            ('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920&q=80', 'library_books_1'),
            ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80', 'books_stack_1'),
            ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=80', 'books_3'),
            ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=80', 'books_4'),
            ('https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=1920&q=80', 'books_5'),
            ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=80', 'books_6'),
            ('https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?auto=compress&cs=tinysrgb&w=1920', 'book_px_1'),
            ('https://images.pexels.com/photos/261857/pexels-photo-261857.jpeg?auto=compress&cs=tinysrgb&w=1920', 'books_px_1'),
            ('https://images.pexels.com/photos/207662/pexels-photo-207662.jpeg?auto=compress&cs=tinysrgb&w=1920', 'library_px_1'),
        ]
    },
    '07_nature': {
        'name': '自然风景',
        'urls': [
            ('https://images.unsplash.com/photo-1470071459604-3a5ec3aed4de?w=1920&q=80', 'lake_1'),
            ('https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920&q=80', 'nature_2'),
            ('https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920&q=80', 'nature_3'),
            ('https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=1920&q=80', 'waterfall_1'),
            ('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80', 'beach_1'),
            ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=80', 'sunset_1'),
            ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80', 'mountain_3'),
            ('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&q=80', 'landscape_2'),
            ('https://images.pexels.com/photos/1223648/pexels-photo-1223648.jpeg?auto=compress&cs=tinysrgb&w=1920', 'nature_px_1'),
            ('https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg?auto=compress&cs=tinysrgb&w=1920', 'sky_px_1'),
            ('https://images.pexels.com/photos/1032650/pexels-photo-1032650.jpeg?auto=compress&cs=tinysrgb&w=1920', 'sunset_px_1'),
        ]
    },
}

def download_single_image(args):
    """下载单张图片"""
    url, theme_key, idx = args
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        
        if width <= height:
            return False, idx, 'Not horizontal'
        
        filename = f'{theme_key}_{idx:03d}.jpg'
        save_path = IMAGE_DIR / theme_key / filename
        
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(save_path, 'JPEG', quality=85, optimize=True)
        
        size_kb = len(response.content) // 1024
        return True, idx, f'{width}x{height}', str(save_path.relative_to(BASE_DIR)), size_kb
        
    except Exception as e:
        return False, idx, str(e)[:30], None, 0

def main():
    print('='*60)
    print('公考网站图片库批量下载 V3')
    print(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'来源: Unsplash + Pexels 直链')
    print('='*60)
    
    IMAGE_DIR.mkdir(exist_ok=True)
    for theme_key in IMAGE_URLS:
        (IMAGE_DIR / theme_key).mkdir(exist_ok=True)
    
    tasks = []
    for theme_key, theme_data in IMAGE_URLS.items():
        for idx, (url, desc) in enumerate(theme_data['urls'], 1):
            tasks.append((url, theme_key, idx))
    
    print(f'\n总任务数: {len(tasks)}')
    print('开始下载...\n')
    
    results = {'success': 0, 'failed': 0}
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_single_image, task): task for task in tasks}
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result[0]:
                results['success'] += 1
                print(f'[{i}/{len(tasks)}] SUCCESS {result[1]}: {result[2]} ({result[4]}KB)')
            else:
                results['failed'] += 1
                print(f'[{i}/{len(tasks)}] FAILED {result[1]}: {result[2]}')
            
            if i % 10 == 0:
                print(f'   Progress: {i}/{len(tasks)} | Success: {results["success"]}')
            
            time.sleep(REQUEST_DELAY)
    
    elapsed = time.time() - start_time
    
    print('\n' + '='*60)
    print('Download Complete!')
    print(f'Total: {results["success"]} success, {results["failed"]} failed')
    print(f'Time: {elapsed:.1f} seconds')
    print('='*60)
    
    # Generate index
    index = {'total': 0, 'themes': {}}
    for theme_key, theme_data in IMAGE_URLS.items():
        theme_path = IMAGE_DIR / theme_key
        images = list(theme_path.glob('*.jpg'))
        if images:
            index['themes'][theme_data['name']] = {
                'count': len(images),
                'key': theme_key,
                'images': [str(p.relative_to(BASE_DIR)) for p in images]
            }
            index['total'] += len(images)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print('\nStats by theme:')
    for name, info in index['themes'].items():
        print(f'  {name}: {info["count"]} images')
    
    print(f'\nTotal: {index["total"]} images')
    print(f'Saved to: {IMAGE_DIR}')

if __name__ == '__main__':
    main()
