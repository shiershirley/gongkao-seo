#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为今天新生成的8篇文章插入图片"""
import sys
sys.path.insert(0, 'scripts')

from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"

# 今天生成的8篇文章（手动生成的）
target_articles = [
    "content/shanghai-shegong/2026-05-19-shegong-wuzhida-luntan.md",
    "content/shanghai-shegong/2026-05-19-shegong-yuzhiyuanzhe-qubie.md",
    "content/shanghai-shegong/2026-05-19-shegong-cunguan-qubie.md",
    "content/shanghai-shegong/2026-05-19-shegong-shang'an-jingyan.md",
    "content/shanghai-shegong/2026-05-19-shegong-cizhi-fenxi.md",
    "content/shanghai-shegong/2026-05-19-jiangsu-shegong-zhaopin.md",
    "content/shanghai-shegong/2026-05-19-zhejiang-shegong-zhaopin.md",
    "content/shanghai-shegong/2026-05-19-guangdong-shegong-zhaopin.md",
]

# 导入 image_picker 功能
import importlib.util
spec = importlib.util.spec_from_file_location("image_picker", PROJECT_ROOT / "scripts" / "image_picker.py")
image_picker_module = importlib.util.load_from_spec = None

# 直接调用 image_picker 的逻辑
import json, random
from datetime import timedelta

IMAGE_LIB = PROJECT_ROOT / "images" / "lib"
USAGE_LOG = PROJECT_ROOT / "scripts" / "image_usage_log.json"

CATEGORY_IMAGE_MAP = {
    "shanghai-shegong": ["gov", "office", "people", "city", "exam"],
    "guokao": ["exam", "study", "gov", "motivation", "office"],
    "shengkao": ["exam", "study", "motivation", "office", "books"],
    "beikao-zhinan": ["study", "books", "exam", "motivation", "writing"],
    "gangwei-fenxi": ["office", "people", "gov", "tech", "city"],
    "baokao-gonggao": ["gov", "office", "writing", "exam", "study"],
    "zhenti-jiexi": ["exam", "study", "books", "writing", "office"],
    "zhengce-jiedu": ["gov", "office", "writing", "city", "tech"],
    "shang-an-jingyan": ["exam", "motivation", "people", "study", "office"],
}

THEME_ALT_MAP = {
    "study": "备考学习",
    "exam": "考试上岸",
    "books": "备考资料",
    "motivation": "励志备考",
    "office": "职场工作",
    "gov": "政府政务",
    "people": "职业人物",
    "city": "城市景观",
    "tech": "科技数字",
    "nature": "自然风景",
    "writing": "笔记文档",
}

def load_usage_log():
    if not USAGE_LOG.exists():
        return {}
    with open(USAGE_LOG, "r", encoding="utf-8") as f:
        return json.load(f)

def save_usage_log(log):
    log["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(USAGE_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def get_available_images(themes, usage, days=10):
    cutoff = datetime.now() - timedelta(days=days)
    available = []
    seen = set()
    for theme in themes:
        theme_dir = IMAGE_LIB / theme
        if not theme_dir.exists():
            continue
        for f in theme_dir.iterdir():
            if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            rel = f"/images/lib/{theme}/{f.name}"
            if rel in seen:
                continue
            seen.add(rel)
            # 检查最近是否使用过
            if rel in usage:
                last_used = datetime.strptime(usage[rel], "%Y-%m-%d")
                if last_used > cutoff:
                    continue
            available.append({"path": rel, "theme": theme})
    return available

def pick_for_article(category, count=2):
    log = load_usage_log()
    usage = log.get("usage", {})
    themes = CATEGORY_IMAGE_MAP.get(category, ["study", "exam", "motivation"])
    available = get_available_images(themes, usage, days=10)
    
    if len(available) < count:
        # 放宽到5天
        available = get_available_images(themes, usage, days=5)
    if len(available) < count:
        available = get_available_images(themes, usage, days=0)
    
    if not available:
        return []
    
    count = min(count, len(available))
    selected = random.sample(available, count)
    
    for item in selected:
        item["alt"] = THEME_ALT_MAP.get(item["theme"], "公考备考")
        # 更新使用记录
        usage[item["path"]] = datetime.now().strftime("%Y-%m-%d")
    
    log["usage"] = usage
    save_usage_log(log)
    return selected

def insert_images_to_article(article_path, images):
    """将图片插入文章：第1张放在正文开头，第2张放在中部"""
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 找到 --- 结束位置（正文开始）
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  跳过（无有效frontmatter）: {article_path.name}")
        return False
    
    fm = '---' + parts[1] + '---'
    body = parts[2].lstrip('\n')
    
    # 第1张图：放在正文开头
    img1 = f'![{images[0]["alt"]}]({images[0]["path"]})\n'
    # 第2张图：放在文章中部（找第一个 ## 标题后插入）
    img2 = f'\n![{images[1]["alt"]}]({images[1]["path"]})\n'
    
    # 在第一个 ## 标题前插入第1张图
    lines = body.split('\n')
    result_lines = []
    inserted1 = False
    inserted2 = False
    h2_count = 0
    
    for i, line in enumerate(lines):
        if line.startswith('##') and not inserted1:
            # 在第一个 ## 前插入第1张图
            result_lines.append('\n' + img1)
            inserted1 = True
            result_lines.append('\n')
        result_lines.append(line)
        if line.startswith('##'):
            h2_count += 1
            # 在第3个 ## 前插入第2张图
            if h2_count == 2 and not inserted2:
                result_lines.append('\n' + img2)
                inserted2 = True
    
    # 如果还没插入，追加到末尾
    if not inserted1:
        result_lines.insert(0, '\n' + img1)
    if not inserted2:
        result_lines.append('\n' + img2)
    
    new_body = '\n'.join(result_lines)
    new_content = fm + '\n' + new_body
    
    with open(article_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return True

# 主逻辑
print(f"开始为8篇文章插入图片...")
for rel_path in target_articles:
    article_path = PROJECT_ROOT / rel_path
    if not article_path.exists():
        print(f"  文件不存在: {rel_path}")
        continue
    
    # 判断分类
    category = "shanghai-shegong"  # 这8篇都是 shanghai-shegong
    images = pick_for_article(category, count=2)
    
    if len(images) < 2:
        print(f"  ⚠️  {article_path.name}: 只获取到 {len(images)} 张图片")
    
    if images:
        ok = insert_images_to_article(article_path, images)
        if ok:
            print(f"  ✅ {article_path.name}")
            for img in images:
                print(f"      - {img['path']} ({img['alt']})")
    else:
        print(f"  ❌ {article_path.name}: 无可用图片")

print("\n图片插入完成！")
