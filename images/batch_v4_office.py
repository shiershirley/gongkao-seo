# -*- coding: utf-8 -*-
"""
第二批：考试/职场/办公/会议/政府建筑 主题
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

URLS = [
    # === 办公室/职场 ===
    ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=85', 'office', 'open_office'),
    ('https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920&q=85', 'office', 'meeting_table'),
    ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=85', 'office', 'teamwork_desk'),
    ('https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920&q=85', 'office', 'office_meeting'),
    ('https://images.unsplash.com/photo-1556761175-4b46a572b786?w=1920&q=85', 'office', 'business_team'),
    ('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1920&q=85', 'office', 'professional_woman'),
    ('https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1920&q=85', 'office', 'office_woman'),
    ('https://images.unsplash.com/photo-1565728744382-61accd4aa148?w=1920&q=85', 'office', 'conference_room'),
    ('https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=1920&q=85', 'office', 'office_clean'),
    ('https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1920&q=85', 'office', 'business_meeting'),
    ('https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1920&q=85', 'office', 'tech_office'),
    ('https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1920&q=85', 'office', 'suit_business'),
    ('https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=1920&q=85', 'office', 'company_building'),
    ('https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1920&q=85', 'office', 'mobile_work'),
    ('https://images.unsplash.com/photo-1531545514256-b1400bc00f31?w=1920&q=85', 'office', 'presentation'),
    ('https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1920&q=85', 'office', 'remote_work'),
    ('https://images.unsplash.com/photo-1568992687947-868a62a9f521?w=1920&q=85', 'office', 'office_3'),
    ('https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1920&q=85', 'office', 'coworking'),
    ('https://images.unsplash.com/photo-1538688525198-9b88f6f53126?w=1920&q=85', 'office', 'desk_notebook'),
    ('https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1920&q=85', 'office', 'coding_screen'),

    # Pexels 职场
    ('https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?w=1920&auto=compress', 'office', 'team_meeting_px'),
    ('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=1920&auto=compress', 'office', 'teamwork_px'),
    ('https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?w=1920&auto=compress', 'office', 'business_px'),
    ('https://images.pexels.com/photos/3182812/pexels-photo-3182812.jpeg?w=1920&auto=compress', 'office', 'office_px2'),
    ('https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?w=1920&auto=compress', 'office', 'coding_px'),
    ('https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?w=1920&auto=compress', 'office', 'presentation_px'),
    ('https://images.pexels.com/photos/3184360/pexels-photo-3184360.jpeg?w=1920&auto=compress', 'office', 'discussion_px'),
    ('https://images.pexels.com/photos/1181406/pexels-photo-1181406.jpeg?w=1920&auto=compress', 'office', 'office_desk_px'),
    ('https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?w=1920&auto=compress', 'office', 'team_work_px'),
    ('https://images.pexels.com/photos/1181772/pexels-photo-1181772.jpeg?w=1920&auto=compress', 'office', 'office_laptop_px'),

    # === 考试/证书/成就 ===
    ('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1920&q=85', 'exam', 'exam_desk'),
    ('https://images.unsplash.com/photo-1588702547919-26089e690ecc?w=1920&q=85', 'exam', 'exam_paper'),
    ('https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1920&q=85', 'exam', 'certificate'),
    ('https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1920&q=85', 'exam', 'celebration_confetti'),
    ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=85', 'exam', 'conference_hall'),
    ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=85', 'exam', 'achievement_mountain'),
    ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920&q=85', 'exam', 'success_team'),
    ('https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1920&q=85', 'exam', 'study_success'),
    ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=85', 'exam', 'writing_exam'),
    ('https://images.unsplash.com/photo-1453928582365-b6ad33cbcf64?w=1920&q=85', 'exam', 'writing_desk'),
    ('https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1920&q=85', 'exam', 'teacher_class'),
    ('https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1920&q=85', 'exam', 'todo_plan'),

    # Pexels 考试
    ('https://images.pexels.com/photos/267885/pexels-photo-267885.jpeg?w=1920&auto=compress', 'exam', 'graduation_px'),
    ('https://images.pexels.com/photos/3762800/pexels-photo-3762800.jpeg?w=1920&auto=compress', 'exam', 'graduation2_px'),
    ('https://images.pexels.com/photos/3601081/pexels-photo-3601081.jpeg?w=1920&auto=compress', 'exam', 'diploma_px'),
    ('https://images.pexels.com/photos/5905709/pexels-photo-5905709.jpeg?w=1920&auto=compress', 'exam', 'exam_table_px'),
    ('https://images.pexels.com/photos/5905445/pexels-photo-5905445.jpeg?w=1920&auto=compress', 'exam', 'exam_writing_px'),
    ('https://images.pexels.com/photos/4778621/pexels-photo-4778621.jpeg?w=1920&auto=compress', 'exam', 'study_table_px'),

    # === 政府/建筑 ===
    ('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920&q=85', 'gov', 'city_square'),
    ('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=85', 'gov', 'city_skyline'),
    ('https://images.unsplash.com/photo-1486325212027-8081e485255e?w=1920&q=85', 'gov', 'urban_building'),
    ('https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920&q=85', 'gov', 'city_road'),
    ('https://images.unsplash.com/photo-1464817739973-0128fe77aaa1?w=1920&q=85', 'gov', 'congress_building'),
    ('https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=1920&q=85', 'gov', 'flag_building'),
    ('https://images.unsplash.com/photo-1534430480872-3498386e7856?w=1920&q=85', 'gov', 'government_hall'),
    ('https://images.unsplash.com/photo-1581092921461-39b9d08a9b21?w=1920&q=85', 'gov', 'civic_center'),
    ('https://images.pexels.com/photos/3739120/pexels-photo-3739120.jpeg?w=1920&auto=compress', 'gov', 'buildings_px'),
    ('https://images.pexels.com/photos/2067278/pexels-photo-2067278.jpeg?w=1920&auto=compress', 'gov', 'urban_px'),
    ('https://images.pexels.com/photos/1769380/pexels-photo-1769380.jpeg?w=1920&auto=compress', 'gov', 'city_hall_px'),
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
print('第二批：职场/考试/政府建筑主题')
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
