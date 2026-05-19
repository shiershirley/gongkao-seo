import os, re
from datetime import datetime

content_dir = 'd:/AI/task/gongkao-seo/content'
today = '2026-05-19'
published_titles = set()
published_files = []

for root, dirs, files in os.walk(content_dir):
    for f in files:
        if f.endswith('.md') and today in f:
            fpath = os.path.join(root, f)
            published_files.append(fpath)
            try:
                with open(fpath, 'r', encoding='utf-8') as fp:
                    content = fp.read(500)
                    m = re.search(r'title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
                    if m:
                        published_titles.add(m.group(1).strip())
            except:
                pass

print(f'今日已发布文件数: {len(published_files)}')
print(f'今日已发布标题数: {len(published_titles)}')
print()
print('今日已发布文件:')
for f in sorted(published_files):
    print(f'  {os.path.basename(f)}')
print()
print('今日已发布标题:')
for t in sorted(published_titles):
    print(f'  - {t}')
