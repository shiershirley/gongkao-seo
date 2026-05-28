#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内链网络构建脚本
功能：为新文章自动匹配2-3篇站内相关旧文，提升SEO整站权重
"""

import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "content"

def parse_frontmatter(filepath):
    """解析文章的frontmatter"""
    try:
        content = filepath.read_text(encoding='utf-8')
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
        
        fm_text = match.group(1)
        # 简单解析YAML（避免完整yaml库依赖）
        fm = {}
        for line in fm_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                key, _, value = line.partition(':')
                key = key.strip()
                value = value.strip()
                
                # 处理标签数组
                if key == 'tags' and value.startswith('['):
                    try:
                        fm[key] = json.loads(value)
                    except:
                        fm[key] = []
                else:
                    # 去除引号
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    fm[key] = value
        
        return fm
    except Exception as e:
        print(f"解析失败 {filepath.name}: {e}")
        return None

def build_article_index(content_dir=None):
    """构建文章索引：标题、标签、分类、路径"""
    if content_dir is None:
        content_dir = CONTENT_DIR
    
    index = []
    
    for md_file in content_dir.rglob("*.md"):
        fm = parse_frontmatter(md_file)
        if not fm:
            continue
        
        # 生成相对路径（用于内链）
        rel_path = md_file.relative_to(ROOT)
        # 移除content/前缀，因为网站URL不包含这个目录
        url_path = str(rel_path).replace('\\', '/')
        if url_path.startswith('content/'):
            url_path = url_path[len('content/'):]
        # 移除.md后缀，网站URL不包含文件扩展名
        if url_path.endswith('.md'):
            url_path = url_path[:-3]
        # 转换为网站URL
        url = f"https://gk.edu-sjtu.cn/{url_path}/"
        
        article_info = {
            'path': str(md_file),
            'rel_path': str(rel_path),
            'url': url,
            'title': fm.get('title', md_file.stem),
            'category': fm.get('category', ''),
            'tags': fm.get('tags', []),
            'date': fm.get('date', ''),
            'content_type': fm.get('content_type', '原创')
        }
        
        index.append(article_info)
    
    print(f"已索引 {len(index)} 篇文章")
    return index

def calculate_relevance(new_article, old_article, exclude_same=True):
    """计算两篇文章的相关性分数（0-100）"""
    score = 0
    
    # 1. 分类相同 +30分
    if new_article.get('category') == old_article.get('category'):
        score += 30
    
    # 2. 标签重叠 +10分/个（最多+40分）
    new_tags = set(new_article.get('tags', []))
    old_tags = set(old_article.get('tags', []))
    overlap_tags = new_tags & old_tags
    score += min(len(overlap_tags) * 10, 40)
    
    # 3. 标题关键词重叠 +5分/个（最多+20分）
    new_title_words = set(re.findall(r'[\w\u4e00-\u9fff]+', new_article.get('title', '')))
    old_title_words = set(re.findall(r'[\w\u4e00-\u9fff]+', old_article.get('title', '')))
    # 过滤停用词
    stop_words = {'的', '是', '在', '了', '年', '月', '日', '和', '与', '及', '等', '如何', '怎么', '什么'}
    new_title_words -= stop_words
    old_title_words -= stop_words
    overlap_words = new_title_words & old_title_words
    score += min(len(overlap_words) * 5, 20)
    
    # 4. 时间接近度（越新越相关）+10分以内
    try:
        new_date = datetime.strptime(new_article.get('date', '2000-01-01'), '%Y-%m-%d')
        old_date = datetime.strptime(old_article.get('date', '2000-01-01'), '%Y-%m-%d')
        days_diff = abs((new_date - old_date).days)
        if days_diff <= 30:
            score += 10
        elif days_diff <= 90:
            score += 5
    except:
        pass
    
    return score

def find_related_articles(new_article, index, max_links=3, exclude_path=None):
    """为新文章找到最相关的旧文"""
    candidates = []
    
    for old_article in index:
        # 排除自己
        if exclude_path and old_article['path'] == exclude_path:
            continue
        
        # 排除同一天发布的文章（可能是批量生成的）
        if old_article.get('date') == new_article.get('date'):
            continue
        
        score = calculate_relevance(new_article, old_article)
        if score > 0:
            candidates.append((score, old_article))
    
    # 按相关性排序
    candidates.sort(key=lambda x: x[0], reverse=True)
    
    # 返回前N篇
    return [article for _, article in candidates[:max_links]]

def generate_related_links_section(new_article, related_articles):
    """生成"相关阅读"章节的Markdown"""
    if not related_articles:
        return ""
    
    section = "\n## 相关阅读\n\n"
    for article in related_articles:
        title = article['title']
        url = article['url']
        section += f"- [{title}]({url})\n"
    
    return section

def insert_internal_links(content, new_article, index, max_links=3):
    """在文章内容中插入内链"""
    # 找到相关文章
    related = find_related_articles(
        new_article, 
        index, 
        max_links=max_links,
        exclude_path=new_article.get('path')
    )
    
    if not related:
        return content
    
    # 在总结章节前插入"相关阅读"
    related_section = generate_related_links_section(new_article, related)
    
    # 查找"## 四、总结与建议"或类似章节
    patterns = [
        r'(## 四、总结与建议)',
        r'(## 三、总结与建议)',
        r'(## 总结)',
        r'(---\n\*本文仅供参考)',
    ]
    
    inserted = False
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            pos = match.start()
            content = content[:pos] + related_section + "\n" + content[pos:]
            inserted = True
            break
    
    # 如果没找到合适位置，追加到末尾
    if not inserted:
        content += "\n" + related_section
    
    return content

def main():
    """主函数：演示内链生成"""
    print("=" * 60)
    print("内链网络构建工具")
    print("=" * 60)
    print()
    
    # 构建索引
    print("正在构建文章索引...")
    index = build_article_index()
    
    if len(index) < 2:
        print("文章数量不足，无法生成内链")
        return
    
    # 测试：为新文章找相关文章
    print("\n测试内链匹配：")
    print("-" * 60)
    
    # 模拟一篇新文章
    test_article = {
        'title': '2026年国考面试技巧全攻略',
        'category': 'guokao',
        'tags': ['国考', '面试', '面试技巧'],
        'date': '2026-05-27'
    }
    
    related = find_related_articles(test_article, index, max_links=3)
    
    print(f"新文章：{test_article['title']}")
    print(f"分类：{test_article['category']}")
    print(f"标签：{test_article['tags']}")
    print("\n推荐的相关文章：")
    for i, article in enumerate(related, 1):
        print(f"{i}. {article['title']}")
        print(f"   分类：{article['category']}，标签：{article['tags']}")
        print(f"   链接：{article['url']}")
        print()
    
    # 生成相关阅读章节
    links_section = generate_related_links_section(test_article, related)
    print("生成的相关阅读章节：")
    print(links_section)

if __name__ == "__main__":
    main()
