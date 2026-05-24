#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, json, sys

categories = [
    'shanghai-shegong',
    'shanghai-shegong',
    'guokao',
    'guokao',
    'shengkao',
    'shengkao',
    'gangwei-fenxi',
    'beikao-zhinan',
]

all_images = []
for cat in categories:
    r = subprocess.run(
        ['python', '-X', 'utf8', 'scripts/image_picker.py', '--category', cat, '--count', '2', '--update', '--json'],
        capture_output=True, text=True, encoding='utf-8', cwd=r'd:\AI\task\gongkao-seo'
    )
    imgs = json.loads(r.stdout.strip())
    all_images.append(imgs)
    paths = [i['path'] for i in imgs]
    print(cat + ': ' + str(paths))

print('--- JSON OUTPUT ---')
print(json.dumps(all_images, ensure_ascii=False))
