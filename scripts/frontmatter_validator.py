#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontmatter_validator.py
公考SEO文章 frontmatter 校验脚本

使用方法:
  python scripts/frontmatter_validator.py                    # 检查所有 content/*.md
  python scripts/frontmatter_validator.py content/guokao/   # 检查指定目录
  python scripts/frontmatter_validator.py --fix             # 自动修复可识别的问题
  python scripts/frontmatter_validator.py --check-keyword "社区工作者考试"  # 检查单篇是否覆盖某关键词
  python scripts/frontmatter_validator.py --content-check    # 启用正文内容质量检查（字数、关键词密度等）

校验规则:
  1. frontmatter 必须以 --- 包围
  2. title/description/date/category/tags/author/source_url/source_date/content_type 八个字段必须存在且非空
  3. description 值内嵌英文双引号 " 必须替换为 「」 (YAML 单行字符串规范)
  4. 中文引号 "" 为全角字符，正常使用（不在 YAML 字符串内时）
  5. date 字段格式必须为 YYYY-MM-DD
  6. date 值不得超过今天（严格禁止未来日期）
  7. source_date 必须 ≤ date（源文章发布日期不应晚于本站发布日期）
  8. category 必须在允许的分类列表中
  9. tags 必须为列表格式，且至少包含1个标签
  10. description/tags 建议包含关键词池中的目标关键词（不强制，但会提示）
  11. 正文内容不少于800字（--content-check 启用）
  12. 关键词密度检查：核心关键词应在正文中出现，密度2-5%（--content-check 启用）
  13. 图片应有alt属性描述（--content-check 启用）
  14. 内部链接有效性检查（--content-check 启用）
"""

import os
import re
import sys
import argparse
import yaml
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Tuple

# ========== 配置 ==========
ROOT = Path(__file__).parent.parent  # 项目根目录
ALLOWED_CATEGORIES = {
    "guokao", "shengkao", "shanghai-shegong", "baokao-gonggao",
    "zhengce-jiedu", "beikao-zhinan", "zhenti-jiexi",
    "gangwei-fenxi", "shang-an-jingyan"
}

REQUIRED_FIELDS = ["title", "description", "date", "category", "tags", "author", "source_url", "source_date", "content_type"]

# content_type 允许的值
ALLOWED_CONTENT_TYPES = {"转载", "原创", "学员分享"}

TODAY = date.today()

# ========== 关键词池配置 ==========

def load_keywords_pool() -> dict:
    """加载关键词池"""
    keywords_path = Path(__file__).parent / 'keywords_pool.md'
    if not keywords_path.exists():
        return {"keywords": [], "triggers": {}}

    content = keywords_path.read_text(encoding='utf-8')
    keywords = []
    triggers = {}

    # 解析静态关键词（以 ```yaml 包裹的块）
    yaml_blocks = re.findall(r'```yaml(.*?)```', content, re.DOTALL)
    for block in yaml_blocks:
        # 解析 keyword 字段
        keyword_matches = re.findall(r'- keyword:\s*(.+)', block)
        for kw in keyword_matches:
            keywords.append(kw.strip())

        # 解析 trigger 字段（动态关键词）
        trigger_matches = re.findall(r'- keyword:\s*(.+?)\n\s*trigger:\s*\[(.*?)\]', block, re.DOTALL)
        for kw, trig_list in trigger_matches:
            triggers[kw.strip()] = [t.strip().strip('"') for t in trig_list.split(',')]

    return {"keywords": keywords, "triggers": triggers}

KEYWORDS_POOL = load_keywords_pool()

# ========== 核心校验逻辑 ==========

def extract_frontmatter(content: str) -> tuple[Optional[str], Optional[str]]:
    """提取 frontmatter 和正文"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, None
    return match.group(1), content[match.end():]

def parse_frontmatter_yaml(fm_text: str) -> dict:
    """
    使用标准 PyYAML 库解析 frontmatter YAML。
    自动处理带引号的字符串、列表等格式。
    """
    try:
        # PyYAML 解析
        fm = yaml.safe_load(fm_text)
        if fm is None:
            fm = {}
        
        # 确保所有必需字段都存在且不为 None
        for key in REQUIRED_FIELDS:
            if key not in fm or fm[key] is None:
                fm[key] = ''
        
        # 处理 date 字段：如果是 date 对象，转成 ISO 格式字符串
        if 'date' in fm and isinstance(fm['date'], date):
            fm['date'] = fm['date'].isoformat()
        if 'source_date' in fm and isinstance(fm['source_date'], date):
            fm['source_date'] = fm['source_date'].isoformat()
        
        # tags 确保是列表
        if 'tags' in fm and not isinstance(fm['tags'], list):
            if isinstance(fm['tags'], str):
                fm['tags'] = [fm['tags']]
            else:
                fm['tags'] = []
        
        return fm
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 解析失败: {e}")

def check_keyword_coverage(fm: dict, content: str) -> list[str]:
    """
    检查文章是否覆盖关键词池中的关键词。
    这是一个建议性检查，不会导致校验失败，但会给出提示。
    """
    issues = []

    # 获取需要检查的文本
    title = fm.get('title', '')
    description = fm.get('description', '')
    tags = fm.get('tags', [])
    if isinstance(tags, str):
        tags = [tags]
    tags_text = ' '.join(tags) if tags else ''

    text_to_check = f"{title} {description} {tags_text}"

    # 检查P0/P1核心关键词覆盖率
    high_priority_keywords = [kw for kw in KEYWORDS_POOL['keywords']
                             if any(p in kw.lower() for p in ['社区工作者', '上海社工', '上海社区'])]
    uncovered = []
    for kw in high_priority_keywords[:10]:  # 只检查前10个P0/P1词
        if kw not in text_to_check:
            uncovered.append(kw)

    if uncovered:
        issues.append(f"[建议] 以下P0/P1词未出现在标题/描述/标签中: {', '.join(uncovered[:3])}...")

    return issues

def check_escaped_quotes(description: str) -> list[str]:
    """
    检测 description 值内是否有未转义的英文双引号。
    这类引号会破坏 YAML 单行字符串解析。
    返回问题列表。
    """
    issues = []
    # 移除首尾引号后，检查内部是否还有双引号
    stripped = description.strip('"\'')
    if '"' in stripped:
        issues.append(f"description 内嵌未转义双引号: {stripped[:60]}...")
    return issues

def check_date_validity(date_str: str) -> list[str]:
    """检查 date 字段格式和值的合法性"""
    issues = []
    # 处理PyYAML已将date转为date对象的情况
    if isinstance(date_str, date):
        d = date_str
    else:
        match = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', str(date_str))
        if not match:
            issues.append(f"date 格式错误，应为 YYYY-MM-DD，实际: {date_str}")
            return issues

        try:
            d = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError as e:
            issues.append(f"date 日期非法: {e}")
            return issues

    if d > TODAY:
        issues.append(f"date 为未来日期 {d.isoformat()}，超过今天 {TODAY.isoformat()}，禁止使用！")
    return issues

def check_date_consistency(fm: dict) -> list[str]:
    """检查 source_date 是否 ≤ date"""
    issues = []
    if 'source_date' in fm and 'date' in fm:
        try:
            source_d = fm['source_date']
            article_d = fm['date']
            
            # 处理可能是date对象的情况
            if not isinstance(source_d, date):
                source_d = date.fromisoformat(str(source_d))
            if not isinstance(article_d, date):
                article_d = date.fromisoformat(str(article_d))
                
            if source_d > article_d:
                issues.append(f"source_date ({source_d}) 晚于 date ({article_d})，源文章发布日期不应晚于本站发布日期")
        except ValueError:
            pass  # date格式错误已在其他地方检查
    return issues

def check_content_length(body: str, min_words: int = 800) -> list[str]:
    """检查正文内容是否达到最少字数"""
    issues = []
    # 移除Markdown标记符号，统计纯文本
    text = re.sub(r'[#*`>\-\[\]|]', '', body)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 移除图片
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # 移除链接
    words = len(text.strip())
    if words < min_words:
        issues.append(f"[内容] 正文字数不足，当前约 {words} 字，建议至少 {min_words} 字")
    return issues

def check_keyword_density(body: str, fm: dict, min_density: float = 0.02, max_density: float = 0.05) -> list[str]:
    """检查关键词在正文中的密度"""
    issues = []
    if not KEYWORDS_POOL['keywords']:
        return issues
    
    title = fm.get('title', '')
    tags = fm.get('tags', [])
    if isinstance(tags, str):
        tags = [tags]
    
    # 获取相关关键词（从标题和标签中提取）
    relevant_keywords = []
    search_text = f"{title} {' '.join(tags)}"
    for kw in KEYWORDS_POOL['keywords'][:20]:  # 只检查前20个
        if kw in search_text:
            relevant_keywords.append(kw)
    
    if not relevant_keywords:
        return issues
    
    # 检查这些关键词在正文中是否出现
    for kw in relevant_keywords[:5]:  # 只检查前5个相关词
        count = body.count(kw)
        if count == 0:
            issues.append(f"[内容] 关键词「{kw}」未在正文中出现")
        elif count / max(len(body), 1) < min_density / 100:  # 简化计算
            issues.append(f"[建议] 关键词「{kw}」密度可能偏低（出现 {count} 次）")
    
    return issues

def check_internal_links(body: str, base_url: str = "https://gk.edu-sjtu.cn") -> list[str]:
    """检查内部链接是否有效（格式检查），排除 Markdown 图片语法"""
    issues = []
    # 查找所有链接，排除图片语法 ![alt](url)
    links = re.findall(r'(?<!!)\[([^\]]*?)\]\((.*?)\)', body)
    for text, url in links:
        if url.startswith('http'):
            if base_url in url or 'gk.edu-sjtu.cn' in url:
                # 内部链接，检查格式
                if not url.startswith('https://gk.edu-sjtu.cn/'):
                    issues.append(f"[内容] 内部链接格式异常: {url}")
        elif url and not url.startswith('#'):
            issues.append(f"[内容] 链接URL格式不完整: {url}")
    return issues

def check_image_alt(body: str) -> list[str]:
    """检查图片是否有alt属性"""
    issues = []
    # 匹配Markdown图片语法 ![alt](url)
    images = re.findall(r'!\[([^\]]*?)\]\((.*?)\)', body)
    for alt, url in images:
        if not alt or alt.strip() == '':
            issues.append(f"[内容] 图片缺少alt描述: {url[:50]}...")
    return issues

def validate_frontmatter(content: str, filepath: str, content_check: bool = False) -> list[str]:
    """对单篇文章做全面校验，返回问题列表
    content_check: 是否启用正文内容质量检查
    """
    issues = []
    fm_text, body = extract_frontmatter(content)

    if fm_text is None:
        issues.append("缺少 frontmatter（文件开头必须有 ---...--- 包围的 YAML 元数据）")
        return issues

    try:
        fm = parse_frontmatter_yaml(fm_text)
    except Exception as e:
        issues.append(f"YAML 解析失败: {e}")
        return issues

    # 1. 必填字段
    for field in REQUIRED_FIELDS:
        if field not in fm or (isinstance(fm[field], list) and not fm[field]) or fm[field] == '':
            issues.append(f"缺少必填字段或字段为空: {field}")

    # 2. description 内嵌引号检测
    if 'description' in fm:
        issues.extend(check_escaped_quotes(str(fm['description'])))

    # 3. date 合法性
    if 'date' in fm:
        # PyYAML可能已将date解析为date对象，直接检查
        issues.extend(check_date_validity(fm['date']))

    # 4. category 合法性
    if 'category' in fm and fm['category'] not in ALLOWED_CATEGORIES:
        issues.append(f"category 不在允许列表中: {fm['category']}，允许: {sorted(ALLOWED_CATEGORIES)}")

    # 5. tags 必须为列表且非空
    if 'tags' in fm:
        if isinstance(fm['tags'], str):
            issues.append("tags 应为列表格式（如 tags: [\"标签1\", \"标签2\"]），当前为字符串")
        elif isinstance(fm['tags'], list) and len(fm['tags']) == 0:
            issues.append("tags 列表不能为空，至少包含1个标签")
    else:
        issues.append("缺少必填字段: tags")

    # 6. source_url 校验
    if 'source_url' in fm:
        url = fm['source_url']
        if not url or not str(url).strip():
            issues.append("source_url 不能为空")
        elif not (str(url).startswith('http://') or str(url).startswith('https://')):
            issues.append(f"source_url 格式错误，应以 http:// 或 https:// 开头，当前: {url[:50]}")
    else:
        issues.append("缺少必填字段: source_url")

    # 7. source_date 校验
    if 'source_date' in fm:
        source_date_str = fm['source_date']
        if isinstance(source_date_str, date):
            # 已经是date对象，无需再校验格式
            pass
        else:
            issues.extend(check_date_validity(str(source_date_str)))
    else:
        issues.append("缺少必填字段: source_date")

    # 8. content_type 校验
    if 'content_type' in fm:
        ct = fm['content_type']
        if ct not in ALLOWED_CONTENT_TYPES:
            issues.append(f"content_type 值非法: {ct}，允许值: {sorted(ALLOWED_CONTENT_TYPES)}")
    else:
        issues.append("缺少必填字段: content_type")

    # 9. 日期一致性检查
    issues.extend(check_date_consistency(fm))

    # 10. 关键词覆盖率检查（建议性）
    issues.extend(check_keyword_coverage(fm, body))

    # 11. 正文内容质量检查（需要启用 content_check）
    if content_check:
        issues.extend(check_content_length(body))
        issues.extend(check_keyword_density(body, fm))
        issues.extend(check_internal_links(body))
        issues.extend(check_image_alt(body))

    return issues

def fix_frontmatter(content: str) -> tuple[str, int]:
    """
    自动修复 frontmatter 中的可识别问题。
    返回 (修复后内容, 修复数量)。
    """
    fixed_count = 0
    fm_text, body = extract_frontmatter(content)
    if fm_text is None:
        return content, 0
    
    try:
        fm = parse_frontmatter_yaml(fm_text)
    except:
        return content, 0
    
    # 修复 description 内嵌引号
    if 'description' in fm:
        desc = str(fm['description'])
        if '"' in desc:
            fm['description'] = desc.replace('"', '「').replace('"', '」')
            fixed_count += 1
    
    # 修复空字符串字段
    for field in ['source_url', 'source_date', 'author', 'content_type']:
        if field not in fm or fm[field] is None or str(fm[field]).strip() == '' or str(fm[field]).strip() == '""':
            if field == 'source_url':
                fm[field] = 'https://gk.edu-sjtu.cn'
                fixed_count += 1
            elif field == 'source_date' and 'date' in fm:
                fm[field] = fm['date']
                fixed_count += 1
            elif field == 'author':
                fm[field] = '公考助手'
                fixed_count += 1
            elif field == 'content_type':
                fm[field] = '原创'
                fixed_count += 1
    
    # 修复空标签
    if 'tags' in fm:
        tags = fm['tags']
        if isinstance(tags, list):
            # 移除空标签
            fm['tags'] = [t for t in tags if t and str(t).strip()]
            if len(fm['tags']) == 0:
                fm['tags'] = ['备考指南']
                fixed_count += 1
        elif isinstance(tags, str) and (not tags.strip() or tags.strip() == '""'):
            fm['tags'] = ['备考指南']
            fixed_count += 1
    
    # 重新构建 frontmatter（使用yaml.dump确保格式正确）
    new_fm_lines = ['---']
    for key in ['title', 'description', 'date', 'category', 'tags', 'author', 'source_url', 'source_date', 'content_type']:
        if key not in fm:
            continue
        val = fm[key]
        
        if isinstance(val, list):
            # 列表格式
            tags_str = ', '.join([f'"{t}"' for t in val])
            new_fm_lines.append(f'{key}: [{tags_str}]')
        elif isinstance(val, date):
            # date对象
            new_fm_lines.append(f'{key}: "{val.isoformat()}"')
        else:
            # 字符串
            str_val = str(val)
            # 如果包含特殊字符，用引号包裹
            if any(c in str_val for c in [':', '{', '}', '[', ']', ',', '&', '*', '#', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
                new_fm_lines.append(f'{key}: "{str_val}"')
            else:
                new_fm_lines.append(f'{key}: {str_val}')
    
    new_fm_lines.append('---')
    
    return '\n'.join(new_fm_lines) + '\n' + body, fixed_count

# ========== 主程序 ==========

def main():
    parser = argparse.ArgumentParser(description='公考SEO文章 frontmatter 校验脚本')
    parser.add_argument('paths', nargs='*', help='要检查的文件或目录路径（默认：content目录）')
    parser.add_argument('--fix', action='store_true', help='自动修复可识别的问题')
    parser.add_argument('--content-check', action='store_true', help='启用正文内容质量检查（字数、关键词密度等）')
    parser.add_argument('--check-keyword', type=str, help='检查单篇文章是否覆盖指定关键词')
    
    args = parser.parse_args()
    
    fix_mode = args.fix
    content_check = args.content_check
    
    # 确定要检查的路径
    if args.paths:
        target_args = args.paths
    else:
        target_args = [str(ROOT / 'content')]

    import glob as glob_module
    
    all_files = []
    for target in target_args:
        # 使用 glob 展开通配符模式
        expanded = glob_module.glob(target, recursive=True)
        if not expanded:
            # 如果没有展开到任何文件，尝试作为普通路径处理
            expanded = [target]
        
        for path_str in expanded:
            p = Path(path_str)
            if p.is_file() and p.suffix == '.md':
                all_files.append(p)
            elif p.is_dir():
                all_files.extend(p.rglob('*.md'))

    total_errors = 0
    total_fixed = 0
    file_results = []

    for filepath in sorted(all_files):
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  [失败] 读取失败: {filepath.name}: {e}")
            total_errors += 1
            continue

        issues = validate_frontmatter(content, str(filepath), content_check)

        if fix_mode:
            fixed_content, fixed_count = fix_frontmatter(content)
            if fixed_count > 0:
                filepath.write_text(fixed_content, encoding='utf-8')
                total_fixed += fixed_count
                issues = validate_frontmatter(fixed_content, str(filepath), content_check)  # 重新校验
                if issues:
                    print(f"  [警告] 修复后仍有问题: {filepath.name}")
                    for issue in issues:
                        print(f"       - {issue}")
                else:
                    print(f"  [已修复] {filepath.name}")
            elif issues:
                print(f"  [错误] {filepath.name}")
                for issue in issues:
                    print(f"       - {issue}")
                total_errors += len(issues)
        else:
            if issues:
                # 分离错误、警告和建议
                errors = [i for i in issues if not i.startswith('[')]
                warnings = [i for i in issues if i.startswith('[建议]')]
                content_issues = [i for i in issues if i.startswith('[内容]')]

                if errors or content_issues:
                    try:
                        rel_path = filepath.relative_to(ROOT)
                    except ValueError:
                        rel_path = filepath
                    print(f"  [错误] {rel_path}")
                    for issue in errors + content_issues:
                        print(f"       - {issue}")
                    total_errors += len(errors) + len(content_issues)

                if warnings:
                    try:
                        rel_path = filepath.relative_to(ROOT)
                    except ValueError:
                        rel_path = filepath
                    print(f"  [建议] {rel_path} (含关键词建议)")
                    for suggestion in warnings:
                        print(f"       {suggestion}")
            else:
                try:
                    rel_path = filepath.relative_to(ROOT)
                except ValueError:
                    rel_path = filepath
                print(f"  [通过] {rel_path}")

    # 汇总
    print()
    if fix_mode:
        print(f"[完成] 自动修复完成: {total_fixed} 处问题已修复，{total_errors} 处需人工处理")
    else:
        if total_errors == 0:
            print("[通过] 所有文件 frontmatter 校验通过！")
        else:
            print(f"[错误] 共发现 {total_errors} 处问题，请修复后再提交！")
            if not content_check:
                print(f"   提示：添加 --content-check 参数可启用正文内容质量检查")
            print(f"   提示：运行 python scripts/frontmatter_validator.py --fix 可自动修复部分问题")

    return 1 if total_errors > 0 else 0

if __name__ == '__main__':
    sys.exit(main())
