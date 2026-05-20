import re
import os

# 读取关键词池
with open('scripts/keywords_pool.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 找出所有带angles字段的已覆盖关键词
pattern = r'- keyword: (.+?)\n  priority: (P\d)\n  type: (\w+)\n  covered: true\n  .*?angles: \[(.+?)\]'
matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

print('有angles字段的关键词（可用于角度轮换）:')
count = 0
for kw, pri, typ, angles in matches[:30]:  # 只显示前30个
    angle_list = [a.strip().strip('"').strip("'") for a in angles.split(',')]
    print(f'  [{pri}][{typ}] {kw}')
    print(f'    可选角度: {angle_list[:3]}...')
    count += 1
    
if count == 0:
    print('  未找到带angles字段的已覆盖关键词')
else:
    print(f'\n共找到 {count} 个可轮换关键词')
    
# 写一个新关键词建议
print('\n=== 建议的新关键词（基于角度轮换）===')
print('可以从以下已有的关键词中选取未使用的角度生成新文章：')
for kw, pri, typ, angles in matches[:10]:
    angle_list = [a.strip().strip('"').strip("'") for a in angles.split(',')]
    print(f'  {kw}: {angle_list[0] if angle_list else "无角度"}')
