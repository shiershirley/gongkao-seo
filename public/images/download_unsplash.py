# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

# Unsplash 免费高质量图片（无需API Key）
test_urls = [
    ('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920&q=80', 'study_library', 'test_001.jpg'),
    ('https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920&q=80', 'study_desk', 'test_002.jpg'),
    ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80', 'books', 'test_003.jpg'),
    ('https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1920&q=80', 'library_books', 'test_004.jpg'),
    ('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920&q=80', 'graduation', 'test_005.jpg'),
    ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80', 'office', 'test_006.jpg'),
    ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=80', 'city', 'test_007.jpg'),
    ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=80', 'notebook', 'test_008.jpg'),
]

output_dir = Path('test_images')
output_dir.mkdir(exist_ok=True)

print('='*50)
print('Downloading images from Unsplash...')
print('='*50)

for url, keyword, filename in test_urls:
    try:
        print(f'\nDownloading [{keyword}]: {filename}...')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        width, height = img.size
        print(f'   Size: {width}x{height}')

        filepath = output_dir / filename
        with open(filepath, 'wb') as f:
            f.write(response.content)

        size_kb = len(response.content) // 1024
        print(f'   SUCCESS: {filepath} ({size_kb} KB)')

    except Exception as e:
        print(f'   FAILED: {e}')

print('\n' + '='*50)
print('Done!')
print('='*50)
