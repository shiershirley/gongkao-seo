#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 auto_gen_daily.py 中的内容生成函数"""
import sys
import os

# 设置文件路径
sys.path.insert(0, 'D:/AI/task/gongkao-seo/scripts')

# 模拟 __file__ 变量以避免错误
import builtins
builtins.__file__ = 'D:/AI/task/gongkao-seo/scripts/auto_gen_daily.py'

# 读取并准备代码（移除 argparse 部分）
with open('D:/AI/task/gongkao-seo/scripts/auto_gen_daily.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 移除 argparse 相关代码和 main 入口，只保留函数定义
# 找到 if __name__ == "__main__": 的位置并截断
main_pos = code.find('if __name__ == "__main__":')
if main_pos > 0:
    code = code[:main_pos]

# 执行代码以定义所有函数
exec(code)

# 测试各个分类的内容生成
test_cases = [
    ('shanghai-shegong', '公告', '上海社区工作者招聘', '测试标题', []),
    ('guokao', '零基础', '国考备考', '测试标题', []),
    ('shengkao', '差异', '省考联考', '测试标题', []),
    ('gangwei-fenxi', '岗位', '事业单位招聘', '测试标题', []),
    ('beikao-zhinan', '学习', '公考备考工具', '测试标题', []),
]

print('Content Generation Test:')
print('=' * 50)

for category, angle, keyword, title, tags in test_cases:
    try:
        # 直接调用 generate_body_by_category
        content = generate_body_by_category(category, angle, keyword, title, tags)
        word_count = len(content)
        status = 'PASS' if word_count > 1000 else 'FAIL'
        
        # 显示前100个字符作为预览
        preview = content[:100].replace('\n', ' ')
        print(f'{category}/{angle}:')
        print(f'  Characters: {word_count} - {status}')
        print(f'  Preview: {preview}...')
        print()
        
    except Exception as e:
        print(f'{category}/{angle}: ERROR - {e}')
        import traceback
        traceback.print_exc()

print('=' * 50)
print('Test completed!')
