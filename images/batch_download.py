# -*- coding: utf-8 -*-
"""
公考网站图片库批量下载脚本
来源: Unsplash (免费高清图片)
无需API Key
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import time
import json
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from datetime import datetime

# ========== 配置 ==========
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / 'images'
INDEX_FILE = BASE_DIR / 'image_index.json'

# 每个主题下载数量
IMAGES_PER_THEME = 80

# 请求延时（秒）- 防止被限流
REQUEST_DELAY = 2

# ========== 图片主题配置 ==========
# 格式: (Unsplash搜索关键词, 保存子目录, 描述)
THEMES = [
    # 学习备考类
    ('library reading books', '01_study', '图书馆学习'),
    ('student studying desk', '01_study', '学生学习'),
    ('textbooks notebooks', '01_study', '教材笔记'),
    ('online learning computer', '01_study', '在线学习'),
    ('writing notes pen', '01_study', '记笔记'),
    ('reading books cozy', '01_study', '阅读书籍'),
    
    # 考试上岸类
    ('graduation ceremony cap', '02_exam', '毕业典礼'),
    ('exam test paper', '02_exam', '考试试卷'),
    ('success achievement', '02_exam', '成功成就'),
    ('certificate diploma', '02_exam', '证书文凭'),
    ('confetti celebration', '02_exam', '庆祝场景'),
    ('trophy award winner', '02_exam', '奖杯获奖'),
    
    # 政务职场类
    ('government office building', '03_career', '政府大楼'),
    ('business meeting conference', '03_career', '商务会议'),
    ('professional woman office', '03_career', '职业女性'),
    ('teamwork collaboration', '03_career', '团队协作'),
    ('job interview professional', '03_career', '求职面试'),
    ('chinese government building', '03_career', '中国政府建筑'),
    
    # 城市政策类
    ('beijing city skyline', '04_city', '北京城市'),
    ('shanghai skyline night', '04_city', '上海夜景'),
    ('chinese architecture traditional', '04_city', '中国建筑'),
    ('city development urban', '04_city', '城市发展'),
    ('government policy document', '04_city', '政策文件'),
    ('beijing olympic bird nest', '04_city', '北京地标'),
    
    # 励志奋斗类
    ('sunrise mountain climbing', '05_motivation', '日出登山'),
    ('perseverance determination', '05_motivation', '坚持不懈'),
    ('goal target achievement', '05_motivation', '目标达成'),
    ('hard work dedication', '05_motivation', '勤奋努力'),
    ('morning sunlight forest', '05_motivation', '晨光森林'),
    ('path road ahead', '05_motivation', '前路'),
    
    # 书籍资料类
    ('bookshelf library', '06_books', '书架'),
    ('open book reading', '06_books', '翻开的书'),
    ('stack of books', '06_books', '书堆'),
    ('knowledge education', '06_books', '知识教育'),
    ('dictionary encyclopedia', '06_books', '字典百科'),
    ('book cafe reading', '06_books', '书咖'),
    
    # 自然风景类（舒缓配图）
    ('calm lake nature', '07_nature', '宁静湖泊'),
    ('blue sky clouds peaceful', '07_nature', '蓝天白云'),
    ('green forest trees', '07_nature', '绿色森林'),
    ('sunset sky orange', '07_nature', '日落天空'),
    ('ocean waves beach', '07_nature', '海浪沙滩'),
    ('mountain landscape scenic', '07_nature', '山川风景'),
]

# ========== Unsplash 图片搜索URL ==========
# 使用 Unsplash 的随机图片 API
def get_unsplash_urls(keyword, count=10):
    """获取指定关键词的Unsplash图片URL"""
    urls = []
    search_url = f"https://unsplash.com/napi/search/photos?query={keyword}&per_page={count}&xp=search-synergy%3Acontrol"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://unsplash.com/'
        }
        response = requests.get(search_url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        for photo in data.get('results', []):
            # 获取高质量横向图片
            img_url = photo['urls']['regular'].replace('w=1080', 'w=1920')
            urls.append({
                'url': img_url,
                'author': photo.get('user', {}).get('name', 'Unknown'),
                'description': photo.get('description') or photo.get('alt_description', keyword)
            })
    except Exception as e:
        print(f"   Warning: {e}")
    
    return urls

# ========== 下载单张图片 ==========
def download_image(img_info, save_path):
    """下载并保存单张图片"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(img_info['url'], headers=headers, timeout=30)
        response.raise_for_status()
        
        # 验证图片
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        
        # 只保留横向图片 (宽 > 高)
        if width <= height:
            return False, 'Not horizontal'
        
        # 保存
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return True, f'{width}x{height}'
    except Exception as e:
        return False, str(e)

# ========== 主程序 ==========
def main():
    print('='*60)
    print('公考网站图片库批量下载')
    print(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'保存目录: {IMAGE_DIR}')
    print(f'每主题数量: {IMAGES_PER_THEME}')
    print('='*60)
    
    # 初始化
    IMAGE_DIR.mkdir(exist_ok=True)
    
    # 加载已有索引
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            image_index = json.load(f)
    else:
        image_index = {'total': 0, 'images': [], 'themes': {}}
    
    downloaded = 0
    failed = 0
    start_time = time.time()
    
    for theme_keyword, theme_dir, theme_desc in THEMES:
        print(f'\n📂 主题: {theme_desc} ({theme_keyword})')
        print('-'*50)
        
        theme_path = IMAGE_DIR / theme_dir
        theme_path.mkdir(exist_ok=True)
        
        if theme_desc not in image_index['themes']:
            image_index['themes'][theme_desc] = {'count': 0, 'images': []}
        
        # 获取图片URL列表
        urls = get_unsplash_urls(theme_keyword, IMAGES_PER_THEME)
        print(f'   获取到 {len(urls)} 个图片源')
        
        for i, img_info in enumerate(urls):
            # 生成文件名
            safe_keyword = theme_keyword.replace(' ', '_')[:20]
            filename = f'{safe_keyword}_{i+1:03d}.jpg'
            save_path = theme_path / filename
            
            # 跳过已下载
            if save_path.exists():
                print(f'   ⏭️  跳过(已存在): {filename}')
                continue
            
            # 下载
            print(f'   ⬇️  [{i+1}/{len(urls)}] {filename}...', end='', flush=True)
            success, info = download_image(img_info, save_path)
            
            if success:
                downloaded += 1
                image_index['total'] += 1
                image_index['themes'][theme_desc]['count'] += 1
                image_index['images'].append({
                    'path': str(save_path.relative_to(BASE_DIR)),
                    'theme': theme_desc,
                    'author': img_info['author'],
                    'size': info
                })
                image_index['themes'][theme_desc]['images'].append(str(save_path.relative_to(BASE_DIR)))
                print(f' ✅ {info}')
            else:
                failed += 1
                print(f' ❌ {info}')
            
            time.sleep(REQUEST_DELAY)
        
        # 每完成一个主题保存一次索引
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(image_index, f, ensure_ascii=False, indent=2)
        
        elapsed = time.time() - start_time
        rate = downloaded / elapsed if elapsed > 0 else 0
        remaining = (len(THEMES) * IMAGES_PER_THEME - downloaded - failed) / rate if rate > 0 else 0
        print(f'   📊 小计: {downloaded} 已下载, {failed} 失败, 预计剩余 {remaining/60:.1f} 分钟')
    
    # 最终统计
    print('\n' + '='*60)
    print('下载完成!')
    print(f'总计: {downloaded} 张成功, {failed} 张失败')
    print(f'耗时: {(time.time() - start_time)/60:.1f} 分钟')
    print(f'保存位置: {IMAGE_DIR}')
    print(f'索引文件: {INDEX_FILE}')
    print('='*60)
    
    # 显示各主题数量
    print('\n各主题统计:')
    for theme, info in image_index['themes'].items():
        print(f'  {theme}: {info["count"]} 张')

if __name__ == '__main__':
    main()
