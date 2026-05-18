# -*- coding: utf-8 -*-
"""
公考网站图片库批量下载脚本 V2
来源: Wikimedia Commons (免费无版权)
无需API Key
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

# ========== 配置 ==========
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'images'
INDEX_FILE = BASE_DIR / 'image_index.json'
IMAGES_PER_THEME = 40  # 每主题数量
REQUEST_DELAY = 1.5  # 请求延时

# ========== 图片主题配置 ==========
# 使用Wikimedia Commons搜索关键词
THEMES = [
    # 学习备考类
    ('library reading', '01_study', '图书馆学习'),
    ('student studying', '01_study', '学生学习'),
    ('textbook education', '01_study', '教材'),
    ('writing studying', '01_study', '写作学习'),
    
    # 考试上岸类
    ('graduation ceremony', '02_exam', '毕业典礼'),
    ('diploma certificate', '02_exam', '证书'),
    ('success achievement', '02_exam', '成功'),
    
    # 政务职场类
    ('government building', '03_career', '政府建筑'),
    ('office meeting', '03_career', '办公室会议'),
    ('business professional', '03_career', '商务职业'),
    
    # 城市政策类
    ('Beijing city', '04_city', '北京'),
    ('Shanghai skyline', '04_city', '上海'),
    ('Chinese architecture', '04_city', '中国建筑'),
    
    # 励志奋斗类
    ('mountain sunrise', '05_motivation', '日出'),
    ('road path', '05_motivation', '道路'),
    ('goal success', '05_motivation', '目标'),
    
    # 书籍资料类
    ('books library', '06_books', '书籍'),
    ('open book reading', '06_books', '阅读'),
    ('bookshelf', '06_books', '书架'),
    
    # 自然风景类
    ('blue sky clouds', '07_nature', '蓝天白云'),
    ('lake nature', '07_nature', '湖泊'),
    ('forest trees', '07_nature', '森林'),
    ('sunset sky', '07_nature', '日落'),
]

# ========== Wikimedia Commons API ==========
def search_wikimedia(keyword, limit=40):
    """通过Wikimedia Commons搜索图片"""
    search_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': keyword,
        'srnamespace': 6,  # 文件
        'srlimit': limit,
        'format': 'json'
    }
    
    try:
        headers = {'User-Agent': 'GongkaoImageBot/1.0'}
        response = requests.get(search_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        filenames = [item['title'].replace('File:', '') for item in data.get('query', {}).get('search', [])]
        return filenames
    except Exception as e:
        print(f"   Search error: {e}")
        return []

def get_image_url(filename):
    """获取Wikimedia图片的直接URL"""
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        'action': 'query',
        'titles': f'File:{filename}',
        'prop': 'imageinfo',
        'iiprop': 'url',
        'iiurlwidth': 1920,
        'format': 'json'
    }
    
    try:
        headers = {'User-Agent': 'GongkaoImageBot/1.0'}
        response = requests.get(api_url, params=params, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        pages = data.get('query', {}).get('pages', {})
        for page in pages.values():
            if 'imageinfo' in page:
                return page['imageinfo'][0].get('thumburl') or page['imageinfo'][0].get('url')
    except:
        pass
    return None

def download_image(url, save_path, max_size=(1920, 1920)):
    """下载并保存图片"""
    try:
        headers = {
            'User-Agent': 'GongkaoImageBot/1.0',
            'Referer': 'https://commons.wikimedia.org/'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 验证图片
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        
        # 调整大小
        if width > max_size[0] or height > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 转为RGB保存
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img.save(save_path, 'JPEG', quality=85, optimize=True)
        return True, f'{img.width}x{img.height}'
    except Exception as e:
        return False, str(e)[:50]

# ========== 主程序 ==========
def main():
    print('='*60)
    print('公考网站图片库批量下载 V2')
    print(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'来源: Wikimedia Commons')
    print('='*60)
    
    # 初始化
    IMAGE_DIR.mkdir(exist_ok=True)
    for _, theme_dir, _ in THEMES:
        (IMAGE_DIR / theme_dir).mkdir(exist_ok=True)
    
    # 加载索引
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            image_index = json.load(f)
    else:
        image_index = {'total': 0, 'images': [], 'themes': {}}
    
    downloaded = 0
    skipped = 0
    failed = 0
    start_time = time.time()
    
    # 去重集合
    downloaded_hashes = {img['hash'] for img in image_index['images']}
    
    for theme_keyword, theme_dir, theme_desc in THEMES:
        print(f'\n📂 主题: {theme_desc}')
        print('-'*50)
        
        if theme_desc not in image_index['themes']:
            image_index['themes'][theme_desc] = {'count': 0, 'images': []}
        
        # 搜索图片
        filenames = search_wikimedia(theme_keyword, IMAGES_PER_THEME)
        print(f'   搜索到 {len(filenames)} 个文件')
        
        for i, filename in enumerate(filenames):
            # 检查是否已下载
            file_hash = hashlib.md5(filename.encode()).hexdigest()
            if file_hash in downloaded_hashes:
                skipped += 1
                continue
            
            # 获取URL
            url = get_image_url(filename)
            if not url:
                failed += 1
                continue
            
            # 保存路径
            safe_name = filename.replace(' ', '_')[:50]
            ext = Path(filename).suffix or '.jpg'
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
                ext = '.jpg'
            save_name = f'{safe_name}{ext}' if ext else f'{safe_name}.jpg'
            save_path = IMAGE_DIR / theme_dir / save_name
            
            if save_path.exists():
                skipped += 1
                continue
            
            # 下载
            print(f'   ⬇️ [{i+1}/{len(filenames)}] {filename[:30]}...', end='', flush=True)
            success, info = download_image(url, save_path)
            
            if success:
                downloaded += 1
                downloaded_hashes.add(file_hash)
                image_index['total'] += 1
                image_index['themes'][theme_desc]['count'] += 1
                
                # 获取文件大小
                size_kb = save_path.stat().st_size // 1024
                
                image_index['images'].append({
                    'path': str(save_path.relative_to(BASE_DIR)),
                    'theme': theme_desc,
                    'source': 'Wikimedia Commons',
                    'original': filename,
                    'size': info,
                    'file_size': f'{size_kb}KB',
                    'hash': file_hash
                })
                image_index['themes'][theme_desc]['images'].append(str(save_path.relative_to(BASE_DIR)))
                print(f' ✅ {info} ({size_kb}KB)')
            else:
                failed += 1
                print(f' ❌ {info}')
            
            time.sleep(REQUEST_DELAY)
        
        # 保存索引
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(image_index, f, ensure_ascii=False, indent=2)
        
        elapsed = time.time() - start_time
        print(f'   📊 {downloaded}已下载, {skipped}跳过, {failed}失败')
    
    # 最终统计
    print('\n' + '='*60)
    print('下载完成!')
    print(f'总计: {downloaded} 张成功, {skipped} 张跳过, {failed} 张失败')
    print(f'耗时: {(time.time() - start_time)/60:.1f} 分钟')
    print(f'保存位置: {IMAGE_DIR}')
    print('='*60)
    
    print('\n各主题统计:')
    for theme, info in image_index['themes'].items():
        print(f'  {theme}: {info["count"]} 张')
    
    print(f'\n总计图片库: {image_index["total"]} 张')

if __name__ == '__main__':
    main()
