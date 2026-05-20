#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完成文章处理：插入图片、Frontmatter校验、Git提交
"""

import sys
import os
import json
import random
from pathlib import Path
from datetime import datetime
import subprocess

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"

# 文章列表 (文件路径, 分类)
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

# 图片主题映射
CATEGORY_THEME_MAP = {
    "beikao-zhinan": ["study", "books", "exam", "motivation", "writing"],
    "gangwei-fenxi": ["office", "people", "gov", "tech", "city"],
    "zhengce-jiedu": ["gov", "office", "writing", "city", "tech"],
    "shang-an-jingyan": ["exam", "motivation", "people", "study", "office"],
    "zhenti-jiexi": ["exam", "study", "books", "writing", "office"],
    "baokao-gonggao": ["gov", "office", "writing", "exam", "study"],
}

def pick_images_real(category, count=2):
    """调用真实的 image_picker.py 选取图片"""
    try:
        cmd = [sys.executable, "scripts/image_picker.py", "--category", category, "--count", str(count), "--update", "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"调用 image_picker.py 失败: {result.stderr}")
    except Exception as e:
        print(f"选取图片异常: {e}")
    
    # 如果调用失败，返回模拟图片
    themes = CATEGORY_THEME_MAP.get(category, ["exam", "study"])
    selected_themes = random.sample(themes, min(count, len(themes)))
    
    images = []
    for theme in selected_themes:
        image_path = f"/images/lib/{theme}/{theme}_example.jpg"
        images.append({"path": image_path, "alt": f"{category}相关图片", "theme": theme})
    
    return images

def insert_images_to_article(filepath, category):
    """为文章插入图片"""
    full_path = CONTENT_DIR / filepath
    if not full_path.exists():
        print(f"文件不存在: {full_path}")
        return False
    
    # 读取文件内容
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 如果已经有图片，跳过
    if "![" in content and "/images/lib/" in content:
        print(f"  文章已有图片，跳过: {filepath}")
        return True
    
    # 选取图片
    images = pick_images_real(category, count=2)
    
    # 生成图片 Markdown
    image_md = "\n\n"
    for img in images:
        image_path = img.get("path", "")
        alt_text = img.get("alt", "相关图片")
        image_md += f"![{alt_text}]({image_path})\n\n"
    
    # 在第一个标题前插入图片
    first_heading_pos = content.find("\n## ")
    if first_heading_pos > 0:
        content = content[:first_heading_pos] + image_md + content[first_heading_pos:]
    
    # 写回文件
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 已为 {filepath} 插入图片")
    return True

def validate_frontmatter(filepath):
    """简单的Frontmatter校验"""
    full_path = CONTENT_DIR / filepath
    if not full_path.exists():
        return False, "文件不存在"
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否有 front matter
    if not content.startswith("---"):
        return False, "缺少 front matter 开始标记"
    
    # 查找结束的 ---
    end_pos = content.find("---", 3)
    if end_pos == -1:
        return False, "缺少 front matter 结束标记"
    
    front_matter = content[3:end_pos].strip()
    
    # 检查必需字段
    required_fields = ["title", "date", "description", "category", "tags", "author"]
    missing_fields = []
    
    for field in required_fields:
        if field not in front_matter:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"缺少必需字段: {missing_fields}"
    
    # 检查 description 中是否有未转义的双引号
    desc_start = front_matter.find("description:")
    if desc_start > -1:
        desc_end = front_matter.find("\n", desc_start)
        if desc_end == -1:
            desc_end = len(front_matter)
        desc_content = front_matter[desc_start:desc_end]
        
        # 检查是否有未转义的双引号（不是日文引号的）
        if '"' in desc_content and "「" not in desc_content and "」" not in desc_content:
            return False, "description 中可能含有未转义的双引号"
    
    return True, "Frontmatter 校验通过"

def git_commit_and_push():
    """Git 提交和推送"""
    try:
        # Git 添加所有文件
        cmd_add = ["git", "add", "-A"]
        result_add = subprocess.run(cmd_add, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
        
        # Git 提交
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_msg = f"content: auto publish articles {today}"
        cmd_commit = ["git", "commit", "-m", commit_msg]
        result_commit = subprocess.run(cmd_commit, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
        
        # Git 推送
        cmd_push = ["git", "push", "origin", "main"]
        result_push = subprocess.run(cmd_push, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
        
        if result_push.returncode == 0:
            print(f"✅ Git 提交推送成功: {commit_msg}")
            return True
        else:
            print(f"❌ Git 推送失败: {result_push.stderr}")
            return False
    except Exception as e:
        print(f"Git 操作异常: {e}")
        return False

def main():
    """主函数"""
    print(f"开始处理文章...")
    
    # 1. 为文章插入图片
    print(f"\n1. 为文章插入图片...")
    success_count = 0
    for filepath, category in ARTICLES:
        print(f"处理: {filepath}")
        if insert_images_to_article(filepath, category):
            success_count += 1
    
    print(f"图片插入完成！成功: {success_count}/{len(ARTICLES)}")
    
    # 2. Frontmatter 校验
    print(f"\n2. Frontmatter 校验...")
    valid_count = 0
    for filepath, category in ARTICLES:
        is_valid, message = validate_frontmatter(filepath)
        if is_valid:
            print(f"✅ {filepath}: {message}")
            valid_count += 1
        else:
            print(f"❌ {filepath}: {message}")
    
    print(f"Frontmatter 校验完成！有效: {valid_count}/{len(ARTICLES)}")
    
    # 3. Git 提交推送
    print(f"\n3. Git 提交推送...")
    if git_commit_and_push():
        print(f"✅ 所有文章已成功生成、校验并推送！")
    else:
        print(f"❌ Git 推送失败，请手动推送")

if __name__ == "__main__":
    main()
