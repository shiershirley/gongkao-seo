#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为文章选取配图并插入 - 2026-05-20
"""
import sys, json, subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

ARTICLES = [
    ("beikao-zhinan/2026-shegong-baoming-liucheng-xiangjie.md", "beikao-zhinan"),
    ("gangwei-fenxi/2026-shegong-xinzi-goucheng-yanjing.md", "gangwei-fenxi"),
    ("zhengce-jiedu/2026-shegong-hukou-zhengce-jiedu.md", "zhengce-jiedu"),
    ("shang-an-jingyan/2026-shegong-mianshi-yingdu-yingbian.md", "shang-an-jingyan"),
    ("zhenti-jiexi/2026-shegong-gongji-shiti-fenxi.md", "zhenti-jiexi"),
    ("baokao-gonggao/2026-shegong-baoming-jiaofei-wenti.md", "baokao-gonggao"),
    ("beikao-zhinan/2026-shegong-zhengshen-cailiao.md", "beikao-zhinan"),
    ("gangwei-fenxi/2026-shegong-zhuanbian-bianzhi.md", "gangwei-fenxi"),
]

def pick_images(category):
    cmd = [sys.executable, "scripts/image_picker.py", "--category", category, "--count", "2", "--update", "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    if r.returncode == 0:
        return json.loads(r.stdout)
    return []

def insert_images(filepath, images):
    fp = CONTENT / filepath
    if not fp.exists():
        return False
    
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Skip if already has images
    if "![" in content and "/images/lib/" in content:
        return True
    
    md = "\n\n"
    for img in images:
        md += f"![{img.get('alt', '')}]({img.get('path', '')})\n\n"
    
    pos = content.find("\n## ")
    if pos > 0:
        content = content[:pos] + md + content[pos:]
    
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    return True

for fp, cat in ARTICLES:
    imgs = pick_images(cat)
    if imgs:
        ok = insert_images(fp, imgs)
        status = "OK" if ok else "SKIP"
    else:
        status = "FAIL"
    print(f"[{status}] {fp} ({cat})")
