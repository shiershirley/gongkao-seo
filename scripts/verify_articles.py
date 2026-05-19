#!/usr/bin/env python3
import os, glob

pattern = 'content/*/2026-05-19-*-13-00.md'
files = glob.glob(pattern)
print(f'13:00批次文章数: {len(files)}')
for f in sorted(files):
    fname = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    wc = len(content.replace(' ', '').replace('\n', ''))
    has_tags_yaml = 'tags:' in content and '  - ' in content
    has_images = '![](' in content and '/images/lib/' in content
    tags_status = 'YAML' if has_tags_yaml else 'ERROR'
    img_status = '有' if has_images else '无'
    print(f'  {fname}')
    print(f'    字数: {wc} | tags: {tags_status} | 配图: {img_status}')
