# -*- coding: utf-8 -*-
"""
公考网站图片库 - 公考主题专用版
关键词精准匹配：学习、考试、职场、政务、书籍等
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time
import json
from datetime import datetime

# ========== 配置 ==========
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'gk_images'
INDEX_FILE = BASE_DIR / 'gk_image_index.json'

# ========== 公考主题精准图片URL ==========
# 全部来自 Unsplash/Pexels 真实摄影师作品
IMAGE_URLS = {
    'study': {
        'name': '学习场景',
        'urls': [
            # 学习桌面
            ('https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920&q=85', 'study_desk'),
            ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=85', 'study_desk_2'),
            ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=85', 'study_desk_3'),
            ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=85', 'study_desk_4'),
            ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=85', 'study_desk_5'),
            # 图书馆学习
            ('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920&q=85', 'library_study'),
            ('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920&q=85', 'library_study_2'),
            ('https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1920&q=85', 'library_study_3'),
            # 阅读
            ('https://images.unsplash.com/photo-1589998059171-988d887df646?w=1920&q=85', 'reading'),
            ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=85', 'reading_2'),
            # 笔记
            ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=85', 'notebook'),
            ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=85', 'notebook_2'),
            # 电脑学习
            ('https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1920&q=85', 'laptop_study'),
            ('https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1920&q=85', 'laptop_study_2'),
            ('https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=1920&q=85', 'laptop_study_3'),
            # 书本特写
            ('https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=1920&q=85', 'books_close'),
            ('https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=1920&q=85', 'books_close_2'),
            # 学生
            ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=85', 'student_reading'),
            ('https://images.unsplash.com/photo-1476659360475-4369e475abc2?w=1920&q=85', 'student_study'),
        ]
    },
    'exam': {
        'name': '考试相关',
        'urls': [
            # 考场/试卷
            ('https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1920&q=85', 'exam_paper'),
            ('https://images.unsplash.com/photo-1550399105-c4db5fb85c18?w=1920&q=85', 'exam_paper_2'),
            ('https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=1920&q=85', 'exam_paper_3'),
            # 铅笔/文具
            ('https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=1920&q=85', 'pencil'),
            ('https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=1920&q=85', 'pencil_2'),
            # 计时器
            ('https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=85', 'timer'),
            # 考试场景
            ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=85', 'exam_scene'),
            ('https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=1920&q=85', 'exam_scene_2'),
        ]
    },
    'achievement': {
        'name': '成就上岸',
        'urls': [
            # 毕业典礼
            ('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920&q=85', 'graduation'),
            ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=85', 'graduation_2'),
            # 证书/文凭
            ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=85', 'certificate'),
            ('https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1920&q=85', 'certificate_2'),
            ('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1920&q=85', 'certificate_3'),
            # 奖杯/成功
            ('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&q=85', 'trophy'),
            ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=85', 'success'),
            # 庆祝
            ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=85', 'celebration'),
        ]
    },
    'office': {
        'name': '政务职场',
        'urls': [
            # 办公室
            ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=85', 'office'),
            ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=85', 'office_2'),
            ('https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920&q=85', 'office_3'),
            # 政府建筑
            ('https://images.unsplash.com/photo-1543286386-713bdd548da4?w=1920&q=85', 'government'),
            ('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&q=85', 'government_2'),
            # 会议
            ('https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920&q=85', 'meeting'),
            ('https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=1920&q=85', 'meeting_2'),
            # 团队协作
            ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=85', 'teamwork'),
            ('https://images.unsplash.com/photo-1556761175-4b46a572b786?w=1920&q=85', 'teamwork_2'),
            # 专业人士
            ('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1920&q=85', 'professional'),
            ('https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1920&q=85', 'professional_2'),
            # 商务
            ('https://images.unsplash.com/photo-1553484771-371a605b060b?w=1920&q=85', 'business'),
        ]
    },
    'books': {
        'name': '书籍资料',
        'urls': [
            # 书架
            ('https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=1920&q=85', 'bookshelf'),
            ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=85', 'bookshelf_2'),
            # 书本堆叠
            ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=85', 'books_stack'),
            ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=85', 'books_stack_2'),
            # 打开的书
            ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=85', 'open_book'),
            ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=85', 'open_book_2'),
            # 教材
            ('https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=1920&q=85', 'textbook'),
            ('https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=1920&q=85', 'textbook_2'),
            # 书房
            ('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920&q=85', 'study_room'),
            ('https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1920&q=85', 'study_room_2'),
        ]
    },
    'motivation': {
        'name': '励志奋斗',
        'urls': [
            # 日出/开始
            ('https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1920&q=85', 'sunrise'),
            ('https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920&q=85', 'sunrise_2'),
            # 山峰/攀登
            ('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=85', 'mountain'),
            ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=85', 'mountain_2'),
            # 道路/前进
            ('https://images.unsplash.com/photo-1518173946687-a4c036bc7d86?w=1920&q=85', 'path'),
            ('https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920&q=85', 'road'),
            # 目标/方向
            ('https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?w=1920&q=85', 'target'),
            # 坚持
            ('https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=1920&q=85', 'perseverance'),
        ]
    },
}

def download_image(url, theme_key, idx):
    """下载单张图片"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        
        if width <= height:
            return False, idx, 'Not horizontal', None, 0
        
        filename = f'{theme_key}_{idx:03d}.jpg'
        save_path = IMAGE_DIR / theme_key / filename
        
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(save_path, 'JPEG', quality=85, optimize=True)
        
        size_kb = len(response.content) // 1024
        return True, idx, f'{width}x{height}', str(save_path.relative_to(BASE_DIR)), size_kb
        
    except Exception as e:
        return False, idx, str(e)[:50], None, 0

def main():
    print('='*60)
    print('公考主题图片库下载 - 精准主题版')
    print(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*60)
    
    # 创建目录
    IMAGE_DIR.mkdir(exist_ok=True)
    for theme_key in IMAGE_URLS:
        (IMAGE_DIR / theme_key).mkdir(exist_ok=True)
    
    # 统计
    tasks = []
    for theme_key, theme_data in IMAGE_URLS.items():
        for idx, (url, desc) in enumerate(theme_data['urls'], 1):
            tasks.append((url, theme_key, idx))
    
    print(f'\n总任务数: {len(tasks)}')
    print('\n开始下载...\n')
    
    results = {'success': 0, 'failed': 0}
    theme_stats = {k: {'success': 0, 'failed': 0} for k in IMAGE_URLS}
    
    for i, (url, theme_key, idx) in enumerate(tasks, 1):
        success, num, info, path, size = download_image(url, theme_key, idx)
        
        if success:
            results['success'] += 1
            theme_stats[theme_key]['success'] += 1
            print(f'[{i}/{len(tasks)}] ✓ {IMAGE_URLS[theme_key]["name"]} #{num}: {info} ({size}KB)')
        else:
            results['failed'] += 1
            theme_stats[theme_key]['failed'] += 1
            print(f'[{i}/{len(tasks)}] ✗ {theme_key} #{num}: {info}')
        
        time.sleep(0.5)  # 避免请求过快
    
    # 生成索引
    index = {'total': 0, 'themes': {}}
    for theme_key, theme_data in IMAGE_URLS.items():
        theme_path = IMAGE_DIR / theme_key
        images = sorted(theme_path.glob('*.jpg'))
        if images:
            index['themes'][theme_data['name']] = {
                'key': theme_key,
                'count': len(images),
                'images': [str(p.relative_to(BASE_DIR)) for p in images]
            }
            index['total'] += len(images)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print('\n' + '='*60)
    print('下载完成!')
    print(f'总计: {results["success"]} 成功, {results["failed"]} 失败')
    print('='*60)
    print('\n各主题统计:')
    for theme_key, stats in theme_stats.items():
        name = IMAGE_URLS[theme_key]['name']
        print(f'  {name}: {stats["success"]} 张')
    print(f'\n总计: {index["total"]} 张')
    print(f'保存位置: {IMAGE_DIR}')
    print('='*60)

if __name__ == '__main__':
    main()
