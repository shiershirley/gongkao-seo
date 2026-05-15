# -*- coding: utf-8 -*-
"""
生成图片索引 image_index.json
"""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

BASE = Path('d:/AI/task/gongkao-seo/images')
LIB = BASE / 'lib'

THEME_NAMES = {
    'study':      '学习备考',
    'books':      '书籍资料',
    'exam':       '考试上岸',
    'office':     '政务职场',
    'gov':        '政府城市',
    'motivation': '励志奋斗',
    'people':     '职业人物',
    'tech':       '科技数字',
    'writing':    '写作文档',
}

index = {'total': 0, 'themes': {}, 'all_images': []}

for folder in sorted(LIB.iterdir()):
    if not folder.is_dir():
        continue
    key = folder.name
    name = THEME_NAMES.get(key, key)
    imgs = sorted(folder.glob('*.jpg'))
    paths = [f'images/lib/{key}/{p.name}' for p in imgs]
    index['themes'][key] = {
        'name': name,
        'count': len(imgs),
        'images': paths
    }
    index['all_images'].extend(paths)
    index['total'] += len(imgs)

out = BASE / 'image_index.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f'生成完成: {out}')
print(f'总计: {index["total"]} 张')
for k, v in index['themes'].items():
    print(f'  {v["name"]}({k}): {v["count"]} 张')
