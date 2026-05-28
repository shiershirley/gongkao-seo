import re
from pathlib import Path

ROOT = Path("d:/AI/task/gongkao-seo")
today = "2026-05-28"

files = [
    ROOT / "content/shanghai-shegong" / f"{today}-shanghai-shegong-xinzi-daoyu.md",
    ROOT / "content/shanghai-shegong" / f"{today}-shanghai-shegong-zhengce-fazhan.md",
    ROOT / "content/guokao" / f"{today}-guokao-gangwei-xuanze.md",
    ROOT / "content/guokao" / f"{today}-guokao-bishi-jiqiao.md",
    ROOT / "content/shengkao" / f"{today}-shengkao-yidi-gangwei.md",
    ROOT / "content/shengkao" / f"{today}-shengkao-tijian-zhuyi.md",
    ROOT / "content/gangwei-fenxi" / f"{today}-gangwei-fenxi-zonghe-guanli.md",
    ROOT / "content/beikao-zhinan" / f"{today}-beikao-zhinan-zaizhi-shijian.md",
]

for f in files:
    if not f.exists():
        print(f"文件不存在: {f}")
        continue
    
    content = f.read_text(encoding="utf-8")
    
    # 匹配 frontmatter
    match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
    if not match:
        print(f"无法解析 frontmatter: {f}")
        continue
    
    fm = match.group(1)
    
    # 检查是否已有缺失字段
    if "source_url:" in fm and "source_date:" in fm and "content_type:" in fm:
        print(f"已有缺失字段，跳过: {f.name}")
        continue
    
    # 找到 author 行
    lines = fm.strip().split('\n')
    author_idx = None
    for i, line in enumerate(lines):
        if line.startswith('author:'):
            author_idx = i
            break
    
    if author_idx is None:
        print(f"未找到 author 行: {f}")
        continue
    
    # 在 author 行之后插入新字段
    new_lines = lines[:author_idx+1] + [
        'source_url: ""',
        'source_date: ""',
        'content_type: "原创"'
    ] + lines[author_idx+1:]
    
    new_fm = '\n'.join(new_lines)
    if not new_fm.endswith('\n'):
        new_fm += '\n'
    new_content = new_fm + content[match.end():]
    
    f.write_text(new_content, encoding="utf-8")
    print(f"已更新: {f.name}")

print("完成！")
