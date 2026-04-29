#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontmatter_validator.py
公考SEO文章 frontmatter 校验脚本

使用方法:
  python scripts/frontmatter_validator.py                    # 检查所有 content/*.md
  python scripts/frontmatter_validator.py content/guokao/   # 检查指定目录
  python scripts/frontmatter_validator.py --fix             # 自动修复可识别的问题

校验规则:
  1. frontmatter 必须以 --- 包围
  2. title/description/date/category/tags/author 六个字段必须存在
  3. description 值内嵌英文双引号 " 必须替换为 「」 (YAML 单行字符串规范)
  4. 中文引号 "" 为全角字符，正常使用（不在 YAML 字符串内时）
  5. date 字段格式必须为 YYYY-MM-DD
  6. date 值不得超过今天（严格禁止未来日期）
  7. category 必须在允许的分类列表中
  8. tags 必须为列表格式
"""

import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

# ========== 配置 ==========
ALLOWED_CATEGORIES = {
    "guokao", "shengkao", "shanghai-shegong", "baokao-gonggao",
    "zhengce-jiedu", "beikao-zhinan", "zhenti-jiexi",
    "gangwei-fenxi", "shang-an-jingyan"
}

REQUIRED_FIELDS = ["title", "description", "date", "category", "tags", "author"]

TODAY = date.today()

# ========== 核心校验逻辑 ==========

def extract_frontmatter(content: str) -> tuple[Optional[str], Optional[str]]:
    """提取 frontmatter 和正文"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, None
    return match.group(1), content[match.end():]

def parse_frontmatter_yaml(fm_text: str) -> dict:
    """简单 YAML 解析（支持标准 frontmatter 格式）"""
    result = {}
    current_key = None
    current_indent = 0

    lines = fm_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        # 空行
        if not line.strip():
            i += 1
            continue

        # 列表项（如 tags: ["标签1", "标签2"] 或 tags:\n  - 标签1）
        if current_key and line.startswith(' ') and not line.startswith('  '):
            # 遇到同级新 key
            current_key = None

        # 缩进检测：二级缩进 = 列表项
        if line.startswith('    - ') or line.startswith('      - '):
            val = line.strip().lstrip('- ').strip()
            if current_key and isinstance(result.get(current_key), list):
                result[current_key].append(val)
            i += 1
            continue

        # 一级缩进列表项（  - 标签）
        if line.startswith('  - ') or line.startswith('    - '):
            val = line.strip().lstrip('- ').strip()
            if current_key and isinstance(result.get(current_key), list):
                result[current_key].append(val)
            elif current_key == 'tags':
                result.setdefault('tags', []).append(val)
            i += 1
            continue

        # 键值对（key: value 或 key: ["val1", "val2"]）
        kv_match = re.match(r'^(\w+):\s*(.*)$', line)
        if kv_match:
            key = kv_match.group(1)
            raw_val = kv_match.group(2).strip()

            # 空值
            if not raw_val:
                result[key] = []
                current_key = key
                i += 1
                continue

            # 列表格式 tags: ["a", "b"]
            if raw_val.startswith('[') and raw_val.endswith(']'):
                inner = raw_val[1:-1]
                items = [x.strip().strip('"\'').strip('「」') for x in inner.split(',')]
                result[key] = [x for x in items if x]
                current_key = key
                i += 1
                continue

            # 单行字符串
            result[key] = raw_val.strip('"\'')
            current_key = key
            i += 1
            continue

        # 其他缩进行（可能是多行字符串，但这里先跳过）
        i += 1

    return result

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
    match = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', date_str)
    if not match:
        issues.append(f"date 格式错误，应为 YYYY-MM-DD，实际: {date_str}")
        return issues

    try:
        d = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError as e:
        issues.append(f"date 日期非法: {e}")
        return issues

    if d > TODAY:
        issues.append(f"date 为未来日期 {date_str}，超过今天 {TODAY.isoformat()}，禁止使用！")
    return issues

def validate_frontmatter(content: str, filepath: str) -> list[str]:
    """对单篇文章做全面校验，返回问题列表"""
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
            issues.append(f"缺少必填字段: {field}")

    # 2. description 内嵌引号检测
    if 'description' in fm:
        issues.extend(check_escaped_quotes(fm['description']))

    # 3. date 合法性
    if 'date' in fm:
        issues.extend(check_date_validity(fm['date']))

    # 4. category 合法性
    if 'category' in fm and fm['category'] not in ALLOWED_CATEGORIES:
        issues.append(f"category 不在允许列表中: {fm['category']}，允许: {sorted(ALLOWED_CATEGORIES)}")

    # 5. tags 必须为列表
    if 'tags' in fm and isinstance(fm['tags'], str):
        issues.append("tags 应为列表格式（如 tags: [\"标签1\", \"标签2\"]），当前为字符串")

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

    fm = parse_frontmatter_yaml(fm_text)

    # 修复 description 内嵌引号
    if 'description' in fm:
        desc = fm['description']
        if '"' in desc:
            fm['description'] = desc.replace('"', '「').replace('"', '」')
            fixed_count += 1

    # 重新构建 frontmatter
    new_fm_lines = ['---']
    for key in ['title', 'description', 'date', 'category', 'tags', 'author']:
        if key not in fm:
            continue
        val = fm[key]
        if isinstance(val, list):
            tags_str = ', '.join(f'「{t}」' for t in val)
            new_fm_lines.append(f'{key}: [{tags_str}]')
        else:
            new_fm_lines.append(f'{key}: "{val}"')
    new_fm_lines.append('---')

    return '\n'.join(new_fm_lines) + '\n' + body, fixed_count

# ========== 主程序 ==========

def main():
    fix_mode = '--fix' in sys.argv
    target_args = [a for a in sys.argv[1:] if not a.startswith('--')]

    # 默认扫描 content 目录
    if not target_args:
        target_args = [str(Path(__file__).parent.parent / 'content')]

    all_files = []
    for target in target_args:
        p = Path(target)
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
            print(f"  ❌ 读取失败: {filepath.relative_to(Path.cwd())}: {e}")
            total_errors += 1
            continue

        issues = validate_frontmatter(content, str(filepath))

        if fix_mode:
            fixed_content, fixed_count = fix_frontmatter(content)
            if fixed_count > 0:
                filepath.write_text(fixed_content, encoding='utf-8')
                total_fixed += fixed_count
                issues = validate_frontmatter(fixed_content, str(filepath))  # 重新校验
                if issues:
                    print(f"  ⚠️  修复后仍有问题: {filepath.name}")
                    for issue in issues:
                        print(f"       - {issue}")
                else:
                    print(f"  ✅ 已修复: {filepath.name}")
            elif issues:
                print(f"  ❌ 问题: {filepath.name}")
                for issue in issues:
                    print(f"       - {issue}")
                total_errors += len(issues)
        else:
            if issues:
                print(f"  ❌ {filepath.relative_to(Path.cwd())}")
                for issue in issues:
                    print(f"       - {issue}")
                total_errors += len(issues)

    # 汇总
    print()
    if fix_mode:
        print(f"📦 自动修复完成: {total_fixed} 处问题已修复，{total_errors} 处需人工处理")
    else:
        if total_errors == 0:
            print("✅ 所有文件 frontmatter 校验通过！")
        else:
            print(f"❌ 共发现 {total_errors} 处问题，请修复后再提交！")
            print(f"   提示：运行 python scripts/frontmatter_validator.py --fix 可自动修复部分问题")

    return 1 if total_errors > 0 else 0

if __name__ == '__main__':
    sys.exit(main())
