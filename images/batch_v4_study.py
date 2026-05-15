# -*- coding: utf-8 -*-
"""
第一批：学习/备考/图书馆/书籍 主题
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os, time, requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path('d:/AI/task/gongkao-seo/images/lib')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Unsplash 和 Pexels 直链，全部为学习/书籍/图书馆主题
URLS = [
    # === 学习/图书馆 ===
    ('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920&q=85', 'study', 'library_reading_room'),
    ('https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920&q=85', 'study', 'study_desk_lamp'),
    ('https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1920&q=85', 'study', 'library_bookshelf'),
    ('https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=1920&q=85', 'study', 'notebook_pen'),
    ('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920&q=85', 'study', 'library_aisle'),
    ('https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1920&q=85', 'study', 'library_window'),
    ('https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920&q=85', 'study', 'classroom_students'),
    ('https://images.unsplash.com/photo-1510531704581-5b2870972060?w=1920&q=85', 'study', 'study_laptop'),
    ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=85', 'study', 'student_writing'),
    ('https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1920&q=85', 'study', 'pen_paper_writing'),
    ('https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1920&q=85', 'study', 'writing_notes'),
    ('https://images.unsplash.com/photo-1543269664-56d93c1b41a6?w=1920&q=85', 'study', 'study_together'),
    ('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920&q=85', 'study', 'group_study'),
    ('https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1920&q=85', 'study', 'lecture_hall'),
    ('https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=1920&q=85', 'study', 'blackboard_classroom'),
    ('https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1920&q=85', 'study', 'teacher_student'),
    ('https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1920&q=85', 'study', 'open_notebook'),
    ('https://images.unsplash.com/photo-1526628953301-3cd0a11a5752?w=1920&q=85', 'study', 'data_analysis_screen'),
    ('https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=1920&q=85', 'study', 'coffee_study'),
    ('https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=1920&q=85', 'study', 'vintage_library'),
    ('https://images.unsplash.com/photo-1568667256531-05b07a6f7fb0?w=1920&q=85', 'study', 'reading_girl'),
    ('https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1920&q=85', 'study', 'student_laptop'),
    ('https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=1920&q=85', 'study', 'study_concentration'),
    ('https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1920&q=85', 'study', 'contract_signing'),
    ('https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1920&q=85', 'study', 'digital_notes'),

    # === 书籍 ===
    ('https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=1920&q=85', 'books', 'colorful_books'),
    ('https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=85', 'books', 'books_table'),
    ('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920&q=85', 'books', 'books_shelf_warm'),
    ('https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1920&q=85', 'books', 'books_reading'),
    ('https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=1920&q=85', 'books', 'open_book_light'),
    ('https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1920&q=85', 'books', 'book_stack_glasses'),
    ('https://images.unsplash.com/photo-1589998059171-988d887df646?w=1920&q=85', 'books', 'book_open_pages'),
    ('https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=85', 'books', 'books_blurred'),
    ('https://images.unsplash.com/photo-1476659360475-4369e475abc2?w=1920&q=85', 'books', 'books_row'),
    ('https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=1920&q=85', 'books', 'book_coffee'),
    ('https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=1920&q=85', 'books', 'books_stacked'),
    ('https://images.unsplash.com/photo-1437913135140-944c1ee62782?w=1920&q=85', 'books', 'old_books'),
    ('https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=1920&q=85', 'books', 'book_open_vintage'),
    ('https://images.unsplash.com/photo-1550399105-c4db5fb85c18?w=1920&q=85', 'books', 'book_reading_close'),
    ('https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=1920&q=85', 'books', 'books_office'),
    ('https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=1920&q=85', 'books', 'books_shelves_library'),
    ('https://images.unsplash.com/photo-1456735190827-d1262f71b8a3?w=1920&q=85', 'books', 'book_hand'),
    ('https://images.unsplash.com/photo-1491841651911-c44c30c34548?w=1920&q=85', 'books', 'book_pages_open'),
    ('https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=1920&q=85', 'books', 'books_stacked_2'),
    ('https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=1920&q=85', 'books', 'book_hands_read'),

    # Pexels 书籍
    ('https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?w=1920&auto=compress', 'books', 'bookstore_px'),
    ('https://images.pexels.com/photos/207662/pexels-photo-207662.jpeg?w=1920&auto=compress', 'books', 'library_row_px'),
    ('https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?w=1920&auto=compress', 'books', 'book_single_px'),
    ('https://images.pexels.com/photos/261857/pexels-photo-261857.jpeg?w=1920&auto=compress', 'books', 'books_many_px'),
    ('https://images.pexels.com/photos/1370298/pexels-photo-1370298.jpeg?w=1920&auto=compress', 'books', 'study_table_px'),
    ('https://images.pexels.com/photos/2676096/pexels-photo-2676096.jpeg?w=1920&auto=compress', 'books', 'reading_px'),
    ('https://images.pexels.com/photos/1516983/pexels-photo-1516983.jpeg?w=1920&auto=compress', 'books', 'stack_books_px'),
    ('https://images.pexels.com/photos/904616/pexels-photo-904616.jpeg?w=1920&auto=compress', 'books', 'open_book_px'),
    ('https://images.pexels.com/photos/1029141/pexels-photo-1029141.jpeg?w=1920&auto=compress', 'books', 'books_white_px'),
    ('https://images.pexels.com/photos/2041540/pexels-photo-2041540.jpeg?w=1920&auto=compress', 'books', 'books_table_px'),
    ('https://images.pexels.com/photos/694740/pexels-photo-694740.jpeg?w=1920&auto=compress', 'books', 'open_book2_px'),
    ('https://images.pexels.com/photos/256541/pexels-photo-256541.jpeg?w=1920&auto=compress', 'books', 'library_big_px'),

    # Pexels 学习
    ('https://images.pexels.com/photos/1205651/pexels-photo-1205651.jpeg?w=1920&auto=compress', 'study', 'student_study_px'),
    ('https://images.pexels.com/photos/3807571/pexels-photo-3807571.jpeg?w=1920&auto=compress', 'study', 'laptop_study_px'),
    ('https://images.pexels.com/photos/4050315/pexels-photo-4050315.jpeg?w=1920&auto=compress', 'study', 'student_online_px'),
    ('https://images.pexels.com/photos/1438072/pexels-photo-1438072.jpeg?w=1920&auto=compress', 'study', 'library_px2'),
    ('https://images.pexels.com/photos/3059654/pexels-photo-3059654.jpeg?w=1920&auto=compress', 'study', 'writing_px'),
    ('https://images.pexels.com/photos/2781814/pexels-photo-2781814.jpeg?w=1920&auto=compress', 'study', 'notes_px'),
    ('https://images.pexels.com/photos/1184580/pexels-photo-1184580.jpeg?w=1920&auto=compress', 'study', 'group_study_px'),
    ('https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?w=1920&auto=compress', 'study', 'coding_study_px'),
]

def download_img(args):
    url, category, name = args
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        w, h = img.size
        if w <= h:
            return False, name, 'Not horizontal'
        save_dir = BASE_DIR / category
        save_dir.mkdir(parents=True, exist_ok=True)
        out = save_dir / f'{name}.jpg'
        if out.exists():
            return True, name, f'{w}x{h}', str(out), 0
        if img.mode in ('RGBA','P'):
            img = img.convert('RGB')
        img.save(out, 'JPEG', quality=85, optimize=True)
        return True, name, f'{w}x{h}', str(out), len(r.content)//1024
    except Exception as e:
        return False, name, str(e)[:50]

print('='*60)
print('第一批：学习/书籍主题')
print(f'共 {len(URLS)} 个URL')
print('='*60)

ok = fail = 0
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(download_img, u): u for u in URLS}
    for i, f in enumerate(as_completed(futs), 1):
        r = f.result()
        if r[0]:
            ok += 1
            print(f'[{i}/{len(URLS)}] ✓ {r[1]}: {r[2]} ({r[4]}KB)')
        else:
            fail += 1
            print(f'[{i}/{len(URLS)}] ✗ {r[1]}: {r[2]}')
        time.sleep(0.5)

print(f'\n完成: {ok} 成功 / {fail} 失败')
print(f'图片目录: {BASE_DIR}')
