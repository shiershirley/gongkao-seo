#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cross_validate_batch.py
批次内文章交叉验证脚本

使用方法:
  python scripts/cross_validate_batch.py                     # 检查今日文章
  python scripts/cross_validate_batch.py content/shanghai-shegong/  # 检查指定目录
  python scripts/cross_validate_batch.py --date 2026-05-28  # 检查指定日期的文章
  python scripts/cross_validate_batch.py --threshold 0.3       # 设置相似度阈值

校验内容:
  1. 批次内标题相似度检测（防止重复）
  2. 批次内内容相似度检测（防止抄袭自己）
  3. 关键词重叠检测（避免过度集中）
  4. 日期一致性验证（source_date ≤ date）
  5. 生成交叉验证报告
"""

import os
import re
import sys
import json
import argparse
from datetime import date, datetime
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Optional

# ========== 配置 ==========
ROOT = Path(__file__).parent.parent  # 项目根目录

# 相似度阈值
DEFAULT_TITLE_SIMILARITY_THRESHOLD = 0.6  # 标题相似度超过此值报警
DEFAULT_CONTENT_SIMILARITY_THRESHOLD = 0.3  # 内容相似度超过此值报警

# 关键词重叠阈值
DEFAULT_KEYWORD_OVERLAP_THRESHOLD = 3  # 两篇文章共同关键词超过此值报警


def find_today_articles(base_dir: str = None) -> List[Path]:
    """查找今日生成的文章"""
    if base_dir is None:
        base_dir = ROOT / 'content'
    else:
        base_dir = Path(base_dir)
    
    today = date.today().isoformat()
    articles = []
    
    for md_file in base_dir.rglob('*.md'):
        # 文件名包含今日日期
        if today in md_file.name:
            articles.append(md_file)
    
    return sorted(articles)


def find_articles_by_date(target_date: str, base_dir: str = None) -> List[Path]:
    """查找指定日期的文章"""
    if base_dir is None:
        base_dir = ROOT / 'content'
    else:
        base_dir = Path(base_dir)
    
    articles = []
    for md_file in base_dir.rglob('*.md'):
        if target_date in md_file.name:
            articles.append(md_file)
    
    return sorted(articles)


def extract_frontmatter(content: str) -> Tuple[Optional[str], Optional[str]]:
    """提取 frontmatter 和正文"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, None
    return match.group(1), content[match.end():]


def parse_frontmatter_simple(fm_text: str) -> dict:
    """简化版 YAML 解析，支持中英文 key"""
    result = {}
    lines = fm_text.split('\n')
    
    for line in lines:
        if not line.strip():
            continue
        
        # 支持中文、英文、数字、下划线作为 key
        kv_match = re.match(r'^([\w\u4e00-\u9fff]+):\s*(.*)$', line)
        if kv_match:
            key = kv_match.group(1)
            raw_val = kv_match.group(2).strip()
            
            # 列表格式
            if raw_val.startswith('[') and raw_val.endswith(']'):
                inner = raw_val[1:-1]
                items = [x.strip().strip('"\'「」') for x in inner.split(',')]
                result[key] = [x for x in items if x]
            else:
                # 去掉值两端的引号
                if (raw_val.startswith('"') and raw_val.endswith('"')) or \
                   (raw_val.startswith("'") and raw_val.endswith("'")):
                    raw_val = raw_val[1:-1]
                result[key] = raw_val
    
    return result
    
    return result


def extract_keywords_from_article(fm: dict, body: str) -> List[str]:
    """从文章中提取关键词（标题、描述、标签、正文）"""
    keywords = []
    
    # 从标题和描述中提取
    title = fm.get('title', '')
    description = fm.get('description', '')
    
    # 从标签中提取
    tags = fm.get('tags', [])
    if isinstance(tags, str):
        tags = [tags]
    
    # 简单的关键词提取：中文词组（2-6个字）
    text = f"{title} {description} {' '.join(tags)}"
    chinese_words = re.findall(r'[\u4e00-\u9fff]{2,6}', text)
    keywords.extend(chinese_words)
    
    return list(set(keywords))


def calculate_similarity(text1: str, text2: str) -> float:
    """计算两段文本的相似度"""
    return SequenceMatcher(None, text1, text2).ratio()


def cross_validate_articles(articles: List[Path], 
                           title_threshold: float = DEFAULT_TITLE_SIMILARITY_THRESHOLD,
                           content_threshold: float = DEFAULT_CONTENT_SIMILARITY_THRESHOLD,
                           keyword_threshold: int = DEFAULT_KEYWORD_OVERLAP_THRESHOLD) -> Dict:
    """
    对文章列表进行交叉验证
    返回验证结果字典
    """
    results = {
        "total_articles": len(articles),
        "check_time": datetime.now().isoformat(),
        "title_similarity_issues": [],
        "content_similarity_issues": [],
        "keyword_overlap_issues": [],
        "date_consistency_issues": [],
        "article_details": []
    }
    
    # 加载所有文章信息
    article_data = []
    for article_path in articles:
        try:
            content = article_path.read_text(encoding='utf-8')
            fm_text, body = extract_frontmatter(content)
            if fm_text is None:
                results["date_consistency_issues"].append({
                    "file": article_path.name,
                    "issue": "无法解析 frontmatter"
                })
                continue
            
            fm = parse_frontmatter_simple(fm_text)
            keywords = extract_keywords_from_article(fm, body)
            
            article_data.append({
                "path": article_path,
                "name": article_path.name,
                "fm": fm,
                "body": body,
                "keywords": keywords
            })
        except Exception as e:
            results["date_consistency_issues"].append({
                "file": article_path.name,
                "issue": f"读取失败: {e}"
            })
    
    # 交叉对比
    for i, art1 in enumerate(article_data):
        for j, art2 in enumerate(article_data[i+1:], i+1):
            
            # 1. 标题相似度
            title1 = art1["fm"].get("title", "")
            title2 = art2["fm"].get("title", "")
            title_sim = calculate_similarity(title1, title2)
            
            if title_sim > title_threshold:
                results["title_similarity_issues"].append({
                    "file1": art1["name"],
                    "file2": art2["name"],
                    "similarity": round(title_sim, 3),
                    "title1": title1[:50],
                    "title2": title2[:50]
                })
            
            # 2. 内容相似度
            content_sim = calculate_similarity(art1["body"][:2000], art2["body"][:2000])  # 只比较前2000字符
            if content_sim > content_threshold:
                results["content_similarity_issues"].append({
                    "file1": art1["name"],
                    "file2": art2["name"],
                    "similarity": round(content_sim, 3)
                })
            
            # 3. 关键词重叠
            overlap = set(art1["keywords"]) & set(art2["keywords"])
            if len(overlap) > keyword_threshold:
                results["keyword_overlap_issues"].append({
                    "file1": art1["name"],
                    "file2": art2["name"],
                    "overlap_count": len(overlap),
                    "overlap_keywords": list(overlap)[:5]  # 只显示前5个
                })
            
            # 4. 日期一致性
            date1 = art1["fm"].get("date", "")
            date2 = art2["fm"].get("date", "")
            if date1 and date2 and date1 != date2:
                # 如果同一批次日期不一致，可能是错误
                results["date_consistency_issues"].append({
                    "file1": art1["name"],
                    "file2": art2["name"],
                    "date1": date1,
                    "date2": date2,
                    "issue": "批次内文章日期不一致"
                })
    
    # 文章详细信息
    for art in article_data:
        results["article_details"].append({
            "file": art["name"],
            "title": art["fm"].get("title", ""),
            "category": art["fm"].get("category", ""),
            "date": art["fm"].get("date", ""),
            "keywords_count": len(art["keywords"]),
            "content_length": len(art["body"])
        })
    
    return results


def generate_report(results: Dict, output_format: str = "text") -> str:
    """生成验证报告"""
    if output_format == "json":
        return json.dumps(results, ensure_ascii=False, indent=2)
    
    # 文本格式报告
    lines = []
    lines.append("=" * 60)
    lines.append("交叉验证报告")
    lines.append("=" * 60)
    lines.append(f"检查时间: {results['check_time']}")
    lines.append(f"文章总数: {results['total_articles']}")
    lines.append("")
    
    # 标题相似度问题
    if results["title_similarity_issues"]:
        lines.append(f"## 标题相似度问题 ({len(results['title_similarity_issues'])} 处)")
        lines.append("-" * 60)
        for issue in results["title_similarity_issues"]:
            lines.append(f"  [警告] {issue['file1']} vs {issue['file2']}")
            lines.append(f"        相似度: {issue['similarity']} (阈值: {DEFAULT_TITLE_SIMILARITY_THRESHOLD})")
            lines.append(f"        标题1: {issue['title1']}")
            lines.append(f"        标题2: {issue['title2']}")
            lines.append("")
    
    # 内容相似度问题
    if results["content_similarity_issues"]:
        lines.append(f"## 内容相似度问题 ({len(results['content_similarity_issues'])} 处)")
        lines.append("-" * 60)
        for issue in results["content_similarity_issues"]:
            lines.append(f"  [警告] {issue['file1']} vs {issue['file2']}")
            lines.append(f"        相似度: {issue['similarity']} (阈值: {DEFAULT_CONTENT_SIMILARITY_THRESHOLD})")
            lines.append("")
    
    # 关键词重叠问题
    if results["keyword_overlap_issues"]:
        lines.append(f"## 关键词重叠问题 ({len(results['keyword_overlap_issues'])} 处)")
        lines.append("-" * 60)
        for issue in results["keyword_overlap_issues"]:
            lines.append(f"  [警告] {issue['file1']} vs {issue['file2']}")
            lines.append(f"        重叠关键词数: {issue['overlap_count']} (阈值: {DEFAULT_KEYWORD_OVERLAP_THRESHOLD})")
            lines.append(f"        重叠词: {', '.join(issue['overlap_keywords'])}")
            lines.append("")
    
    # 日期一致性问题
    if results["date_consistency_issues"]:
        lines.append(f"## 日期一致性问题 ({len(results['date_consistency_issues'])} 处)")
        lines.append("-" * 60)
        for issue in results["date_consistency_issues"]:
            lines.append(f"  [错误] {issue['file']}")
            lines.append(f"        {issue['issue']}")
            if "date1" in issue:
                lines.append(f"        日期1: {issue['date1']}, 日期2: {issue['date2']}")
            lines.append("")
    
    # 总结
    total_issues = (len(results["title_similarity_issues"]) + 
                   len(results["content_similarity_issues"]) + 
                   len(results["keyword_overlap_issues"]) + 
                   len(results["date_consistency_issues"]))
    
    lines.append("=" * 60)
    if total_issues == 0:
        lines.append("[通过] 交叉验证通过，未发现异常！")
    else:
        lines.append(f"[警告] 共发现 {total_issues} 处问题，请检查！")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='公考SEO文章交叉验证脚本')
    parser.add_argument('paths', nargs='*', help='要检查的文件或目录路径（默认：今日文章）')
    parser.add_argument('--date', type=str, help='检查指定日期的文章（格式：YYYY-MM-DD）')
    parser.add_argument('--title-threshold', type=float, default=DEFAULT_TITLE_SIMILARITY_THRESHOLD,
                        help=f'标题相似度阈值（默认：{DEFAULT_TITLE_SIMILARITY_THRESHOLD}）')
    parser.add_argument('--content-threshold', type=float, default=DEFAULT_CONTENT_SIMILARITY_THRESHOLD,
                        help=f'内容相似度阈值（默认：{DEFAULT_CONTENT_SIMILARITY_THRESHOLD}）')
    parser.add_argument('--keyword-threshold', type=int, default=DEFAULT_KEYWORD_OVERLAP_THRESHOLD,
                        help=f'关键词重叠阈值（默认：{DEFAULT_KEYWORD_OVERLAP_THRESHOLD}）')
    parser.add_argument('--output', type=str, help='报告输出文件路径')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='输出格式（text 或 json，默认：text）')
    
    args = parser.parse_args()
    
    # 确定要检查的文章
    articles = []
    
    if args.paths:
        # 检查指定路径
        for path_str in args.paths:
            p = Path(path_str)
            if p.is_file() and p.suffix == '.md':
                articles.append(p)
            elif p.is_dir():
                articles.extend(p.rglob('*.md'))
    elif args.date:
        # 检查指定日期
        articles = find_articles_by_date(args.date)
        if not articles:
            print(f"[错误] 未找到日期为 {args.date} 的文章")
            return 1
    else:
        # 检查今日文章
        articles = find_today_articles()
        if not articles:
            print(f"[信息] 未找到今日 ({date.today()}) 的文章，请指定路径或日期")
            return 0
    
    print(f"[信息] 找到 {len(articles)} 篇文章，开始交叉验证...")
    print(f"        标题相似度阈值: {args.title_threshold}")
    print(f"        内容相似度阈值: {args.content_threshold}")
    print(f"        关键词重叠阈值: {args.keyword_threshold}")
    print()
    
    # 执行交叉验证
    results = cross_validate_articles(
        articles,
        title_threshold=args.title_threshold,
        content_threshold=args.content_threshold,
        keyword_threshold=args.keyword_threshold
    )
    
    # 生成报告
    report = generate_report(results, output_format=args.format)
    
    # 输出报告
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding='utf-8')
        print(f"[完成] 报告已保存到: {output_path}")
        print()
    
    print(report)
    
    # 返回状态码
    total_issues = (len(results["title_similarity_issues"]) + 
                   len(results["content_similarity_issues"]) + 
                   len(results["keyword_overlap_issues"]) + 
                   len(results["date_consistency_issues"]))
    
    return 1 if total_issues > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
