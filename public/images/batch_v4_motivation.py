# -*- coding: utf-8 -*-
"""
第三批：励志/人物/团队/未来/科技/人文 主题
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
    # === 励志/目标/坚持 ===
    ('https://images.unsplash.com/photo-1552508744-1696d4464960?w=1920&q=85', 'motivation', 'running_success'),
    ('https://images.unsplash.com/photo-1519834785169-98be25ec3f84?w=1920&q=85', 'motivation', 'finish_line'),
    ('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&q=85', 'motivation', 'confident_man'),
    ('https://images.unsplash.com/photo-1517021897933-0e0319cfbc28?w=1920&q=85', 'motivation', 'reading_sunrise'),
    ('https://images.unsplash.com/photo-1499728603263-13726abce5fd?w=1920&q=85', 'motivation', 'sunrise_person'),
    ('https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?w=1920&q=85', 'motivation', 'workspace_clean'),
    ('https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=1920&q=85', 'motivation', 'typing_laptop'),
    ('https://images.unsplash.com/photo-1455849318743-b2233052fcff?w=1920&q=85', 'motivation', 'road_ahead'),
    ('https://images.unsplash.com/photo-1493612276216-ee3925520721?w=1920&q=85', 'motivation', 'data_growth'),
    ('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920&q=85', 'motivation', 'business_planning'),
    ('https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1920&q=85', 'motivation', 'laptop_notebook'),
    ('https://images.unsplash.com/photo-1508780709619-79562169bc64?w=1920&q=85', 'motivation', 'goal_target'),
    ('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920&q=85', 'motivation', 'team_smile'),
    ('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1920&q=85', 'motivation', 'matrix_code'),
    ('https://images.unsplash.com/photo-1533227268428-f9ed0900fb3b?w=1920&q=85', 'motivation', 'goal_post'),

    # Pexels 励志
    ('https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?w=1920&auto=compress', 'motivation', 'success_team_px'),
    ('https://images.pexels.com/photos/3861958/pexels-photo-3861958.jpeg?w=1920&auto=compress', 'motivation', 'success_px'),
    ('https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?w=1920&auto=compress', 'motivation', 'running_px'),
    ('https://images.pexels.com/photos/3836849/pexels-photo-3836849.jpeg?w=1920&auto=compress', 'motivation', 'achievement_px'),

    # === 人物/职业形象 ===
    ('https://images.unsplash.com/photo-1560250097-0b93528c311a?w=1920&q=85', 'people', 'businessman_suit'),
    ('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1920&q=85', 'people', 'professional_woman2'),
    ('https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=1920&q=85', 'people', 'man_portrait'),
    ('https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=1920&q=85', 'people', 'woman_portrait'),
    ('https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=1920&q=85', 'people', 'man_smile'),
    ('https://images.unsplash.com/photo-1573497019236-17f8177b81e8?w=1920&q=85', 'people', 'office_people'),
    ('https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1920&q=85', 'people', 'handshake'),
    ('https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1920&q=85', 'people', 'meeting_people'),
    ('https://images.unsplash.com/photo-1499952127939-9bbf5af6c51c?w=1920&q=85', 'people', 'woman_laptop'),
    ('https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=1920&q=85', 'people', 'woman_thinking'),

    # Pexels 人物
    ('https://images.pexels.com/photos/3184405/pexels-photo-3184405.jpeg?w=1920&auto=compress', 'people', 'people_meeting_px'),
    ('https://images.pexels.com/photos/3184317/pexels-photo-3184317.jpeg?w=1920&auto=compress', 'people', 'office_people_px'),
    ('https://images.pexels.com/photos/3184325/pexels-photo-3184325.jpeg?w=1920&auto=compress', 'people', 'team_px'),

    # === 科技/数字/信息 ===
    ('https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=85', 'tech', 'circuit_board'),
    ('https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=1920&q=85', 'tech', 'laptop_dark'),
    ('https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1920&q=85', 'tech', 'programming'),
    ('https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1920&q=85', 'tech', 'cowork_tech'),
    ('https://images.unsplash.com/photo-1526628953301-3cd0a11a5752?w=1920&q=85', 'tech', 'data_screen'),
    ('https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1920&q=85', 'tech', 'data_analytics'),
    ('https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?w=1920&q=85', 'tech', 'tech_screen'),
    ('https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?w=1920&auto=compress', 'tech', 'tech_px'),
    ('https://images.pexels.com/photos/3861964/pexels-photo-3861964.jpeg?w=1920&auto=compress', 'tech', 'data_px'),

    # === 写作/笔记/文档 ===
    ('https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1920&q=85', 'writing', 'pen_paper'),
    ('https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1920&q=85', 'writing', 'writing_notes2'),
    ('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=85', 'writing', 'exam_writing2'),
    ('https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1920&q=85', 'writing', 'planner'),
    ('https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1920&q=85', 'writing', 'document_signing'),
    ('https://images.unsplash.com/photo-1508780709619-79562169bc64?w=1920&q=85', 'writing', 'notebook_write'),
    ('https://images.unsplash.com/photo-1517842645767-c639042777db?w=1920&q=85', 'writing', 'notepad_pen'),
    ('https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=1920&q=85', 'writing', 'stickynotes'),
    ('https://images.pexels.com/photos/3059654/pexels-photo-3059654.jpeg?w=1920&auto=compress', 'writing', 'writing_px2'),
    ('https://images.pexels.com/photos/4144923/pexels-photo-4144923.jpeg?w=1920&auto=compress', 'writing', 'notes_px2'),
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
print('第三批：励志/人物/科技/写作主题')
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
