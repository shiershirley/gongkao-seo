# -*- coding: utf-8 -*-
import yaml
import re

files = [
    'content/zhenti-jiexi/2026-05-20-shegong-panduan-tuili-jiqiao.md',
    'content/beikao-zhinan/2026-05-20-shegong-yanyu-lijie-gaofeng-jiqiao.md',
    'content/gangwei-fenxi/2026-05-20-shanghai-shegong-gedai-daiyu-hengxiang-duibi.md',
    'content/zhengce-jiedu/2026-05-20-shegong-zhiyyehua-gaige-zuixin-jinzhan.md',
    'content/shanghai-shegong/2026-05-20-beijing-shegong-zhaopin-2026.md',
    'content/shang-an-jingyan/2026-05-20-baoma-beikao-shegong-qinli-fenxiang.md',
    'content/beikao-zhinan/2026-05-20-shegong-gonggong-jichu-zhishi-gaofen-beikao.md',
]

ok = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            data = yaml.safe_load(match.group(1))
            required = ['title','description','date','category','tags','author']
            missing = [k for k in required if k not in data]
            desc_issues = []
            if '"' in data.get('description', ''):
                desc_issues.append('has英文双引号')
            if missing:
                print(f'X {f}: missing {missing}')
            elif desc_issues:
                print(f'W {f}: {desc_issues[0]}')
            else:
                print(f'OK {f}')
                ok += 1
        except Exception as e:
            print(f'X {f}: YAML error {e}')
    else:
        print(f'X {f}: no frontmatter')

print(f'Total: {ok}/{len(files)} passed')
