#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键词驱动的文章生成器
从关键词池中选择未覆盖的高价值词，生成文章或输出生成指令
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime

# ============ 配置 ============
PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
KEYWORD_POOL_FILE = PROJECT_ROOT / "scripts" / "keywords_pool.md"

# 关键词分类
CATEGORY_KEYWORDS = {
    "shanghai-shegong": ["上海", "社工", "社区工作者"],
    "guokao": ["国考", "公务员", "行测", "申论"],
    "shengkao": ["省考", "事业单位"],
    "beikao-zhinan": ["备考", "考试", "复习", "技巧"],
    "gangwei-fenxi": ["岗位", "职位", "选岗"],
    "baokao-gonggao": ["招聘", "公告", "报名", "笔试", "成绩"],
    "zhenti-jiexi": ["真题", "解析", "答案"],
}


def get_existing_keywords():
    """扫描已发布的文章，提取所有已覆盖的关键词"""
    covered = set()
    if not CONTENT_DIR.exists():
        return covered
    
    for md_file in CONTENT_DIR.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 frontmatter（不用yaml）
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    fm_text = parts[1]
                    
                    # 提取 title
                    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)
                    if title_match:
                        covered.add(title_match.group(1).strip())
                    
                    # 提取 tags
                    tags_match = re.search(r'^tags:\s*\[(.*?)\]', fm_text, re.MULTILINE | re.DOTALL)
                    if tags_match:
                        tags = re.findall(r'["\'](.*?)["\']', tags_match.group(1))
                        covered.update(tags)
                    
                    # 提取 description
                    desc_match = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)
                    if desc_match:
                        # 简单分词
                        words = re.findall(r'[\u4e00-\u9fa5]{2,}', desc_match.group(1))
                        covered.update(words)
        except Exception as e:
            continue
    
    return covered


def load_keyword_pool():
    """加载关键词池 - 支持 YAML 格式"""
    keywords = {
        "P0": [],  # 核心词
        "P1": [],  # 高价值
        "P2": [],  # 中价值
        "P3": [],  # 长尾
        "dynamic": [],  # 动态词
    }
    
    if not KEYWORD_POOL_FILE.exists():
        print(f"⚠️ 关键词池文件不存在: {KEYWORD_POOL_FILE}")
        return keywords
    
    current_section = None
    current_type = None
    in_yaml_block = False
    yaml_buffer = []
    
    with open(KEYWORD_POOL_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析逻辑
    for line in content.split('\n'):
        line_stripped = line.strip()
        
        # 优先级分类
        if line_stripped.startswith('## P0'):
            current_section = 'P0'
        elif line_stripped.startswith('## P1'):
            current_section = 'P1'
        elif line_stripped.startswith('## P2'):
            current_section = 'P2'
        elif line_stripped.startswith('## P3'):
            current_section = 'P3'
        elif line_stripped.startswith('## 动态关键词池'):
            current_section = 'dynamic'
        
        # 类型分类
        elif line_stripped.startswith('### ') and not line_stripped.startswith('### 文件格式'):
            current_type = line_stripped.replace('### ', '').strip()
        
        # 关键词行：支持 YAML 格式 "- keyword: xxx"
        elif '- keyword:' in line_stripped and current_section:
            kw_match = re.search(r'- keyword:\s*(.+?)(?:\s*$|\s*#)', line_stripped)
            if kw_match:
                keyword = kw_match.group(1).strip()
                keywords[current_section].append({
                    "keyword": keyword,
                    "type": current_type or "general"
                })
    
    return keywords


def suggest_category_for_keyword(keyword):
    """根据关键词推断适合的分类"""
    keyword_lower = keyword.lower()
    
    for category, category_words in CATEGORY_KEYWORDS.items():
        for cw in category_words:
            if cw in keyword:
                return category
    
    # 默认分类
    return "beikao-zhinan"


def generate_article_prompt(keyword_info, output_path=None):
    """生成文章生成指令"""
    keyword = keyword_info["keyword"]
    priority = keyword_info.get("priority", "P1")
    kw_type = keyword_info.get("type", "general")
    category = keyword_info.get("category", "beikao-zhinan")
    
    prompt = f"""
## 文章生成指令

**目标关键词**：{keyword}
**优先级**：{priority}
**关键词类型**：{kw_type}
**推荐分类**：{category}

### SEO要求
1. **标题**：必须包含关键词「{keyword}」，控制在25字以内
2. **description**：100-160字，必须包含关键词，简明扼要
3. **tags**：3-5个标签，必须包含「{keyword}」

### 内容要求
- 回答用户搜索意图
- 结构清晰，有小标题
- 适当内链到其他相关文章

### 分类目录
- 上海社工：shanghai-shegong
- 国考：guokao  
- 省考/事业单位：shengkao
- 备考指南：beikao-zhinan
- 岗位分析：gangwei-fenxi
- 报考公告：baokao-gonggao
- 真题解析：zhenti-jiexi

### 输出文件路径
`content/{category}/{datetime.now().strftime('%Y-%m-%d')}-{keyword[:20].replace(' ', '-')}.md`
"""
    return prompt.strip()


def select_next_keyword(keywords_pool, covered_keywords):
    """选择下一个要生成的关键词"""
    # 按优先级遍历
    for priority in ["P0", "P1", "P2", "P3", "dynamic"]:
        for kw_info in keywords_pool.get(priority, []):
            keyword = kw_info["keyword"]
            
            # 检查是否已覆盖
            is_covered = any(
                keyword.lower() in str(c).lower() 
                for c in covered_keywords
            )
            
            if not is_covered:
                kw_info["priority"] = priority
                kw_info["category"] = suggest_category_for_keyword(keyword)
                return kw_info
    
    return None


def list_uncovered_keywords(keywords_pool, covered_keywords, limit=20):
    """列出未覆盖的关键词"""
    uncovered = []
    
    for priority in ["P0", "P1", "P2", "P3"]:
        for kw_info in keywords_pool.get(priority, []):
            keyword = kw_info["keyword"]
            is_covered = any(
                keyword.lower() in str(c).lower() 
                for c in covered_keywords
            )
            
            if not is_covered:
                kw_info["priority"] = priority
                kw_info["category"] = suggest_category_for_keyword(keyword)
                uncovered.append(kw_info)
    
    return uncovered[:limit]


def main():
    parser = argparse.ArgumentParser(description='关键词驱动的文章生成器')
    parser.add_argument('--list', action='store_true', help='列出未覆盖的关键词')
    parser.add_argument('--next', action='store_true', help='输出下一个要生成的关键词')
    parser.add_argument('--prompt', action='store_true', help='生成文章生成指令')
    parser.add_argument('--limit', type=int, default=20, help='列出关键词数量限制')
    
    args = parser.parse_args()
    
    print("🔍 正在扫描已覆盖的关键词...")
    covered = get_existing_keywords()
    print(f"   已覆盖：{len(covered)} 个词/短语")
    
    print("\n📦 加载关键词池...")
    pool = load_keyword_pool()
    
    total = sum(len(v) for v in pool.values())
    print(f"   关键词池总数：{total} 个")
    print(f"   - P0核心词：{len(pool['P0'])} 个")
    print(f"   - P1高价值：{len(pool['P1'])} 个")
    print(f"   - P2中价值：{len(pool['P2'])} 个")
    print(f"   - P3长尾词：{len(pool['P3'])} 个")
    print(f"   - 动态词：{len(pool['dynamic'])} 个")
    
    if args.list:
        print("\n" + "="*60)
        print("📋 未覆盖的关键词列表（按优先级排序）")
        print("="*60)
        
        uncovered = list_uncovered_keywords(pool, covered, args.limit)
        
        if not uncovered:
            print("✅ 所有关键词都已覆盖！")
        else:
            current_priority = None
            for i, kw_info in enumerate(uncovered, 1):
                priority = kw_info["priority"]
                if priority != current_priority:
                    print(f"\n【{priority}】")
                    current_priority = priority
                
                kw_type = kw_info.get("type", "general")
                category = kw_info.get("category", "")
                print(f"  {i}. {kw_info['keyword']} | {kw_type} | {category}")
    
    elif args.next or args.prompt:
        print("\n🎯 选择下一个关键词...")
        next_kw = select_next_keyword(pool, covered)
        
        if next_kw:
            print(f"\n✅ 建议生成：{next_kw['keyword']}")
            print(f"   优先级：{next_kw.get('priority', 'P1')}")
            print(f"   类型：{next_kw.get('type', 'general')}")
            print(f"   推荐分类：{next_kw.get('category', 'beikao-zhinan')}")
            
            if args.prompt:
                prompt = generate_article_prompt(next_kw)
                print("\n" + "="*60)
                print("📝 文章生成指令")
                print("="*60)
                print(prompt)
        else:
            print("\n✅ 所有关键词都已覆盖！无需生成新文章。")
    
    else:
        # 默认：显示摘要
        uncovered = list_uncovered_keywords(pool, covered, 5)
        print(f"\n📊 摘要")
        print(f"   未覆盖关键词：{len(uncovered)} 个")
        
        if uncovered:
            print("\n🔥 高优先级未覆盖词：")
            for kw in uncovered[:5]:
                print(f"   - {kw['keyword']} [{kw['priority']}]")


if __name__ == "__main__":
    main()
