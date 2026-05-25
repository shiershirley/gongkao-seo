#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese Slug Fixer for Next.js Static Generation

Problem: Chinese characters in filenames cause 500 errors on Vercel 
         during static generation (SSG), even though local build works.

Solution: This script renames files with Chinese characters in the filename 
         to English-based slugs, while preserving the Chinese title in frontmatter.

Usage: python -X utf8 scripts/fix_chinese_slugs_v3.py
"""

import os
import re
import shutil
from datetime import datetime

# Mapping table for common Chinese phrases in filenames
SLUG_MAPPING = {
    '社区工作者准考证打印指南': 'shegong-zkz-dayin-zhinan',
    '社区工作者常识判断高分策略': 'shegong-changshi-gaofen-celue',
    '社区工作者数量关系技巧': 'shegong-shuliang-guanxi-jiqiao',
    '社区工作者与事业单位区别': 'shegong-vs-shiyedanwei',
    '社区工作者与省考国考区别': 'shegong-vs-shengkao-guokao',
    '社区工作者持证上岗政策': 'shegong-chizheng-shanggang',
    '社区工作者面试真题解析': 'shegong-mianshi-zhenti-jiexi',
    '宝妈考社区工作者成功经验': 'bama-shegong-chenggong',
    '社区工作者宝妈备考经验': 'shegong-bama-beikao',
    '零基础跨专业考生3个月公考上岸复习计划': 'lingji-chuak-zhuanye-3geyue',
    '国考笔试成绩查询时间及入口': 'guokao-bizhang-chaxun',
    '国考面试礼仪全攻略': 'guokao-mianshi-liyi',
    '年国考报名人数统计': 'guokao-baoming-renshu',
    '国考应届生身份认定及报考优势分析': 'guokao-yingjie-shenfen',
    '国考调剂补录政策详解及申请技巧': 'guokao-tiaoji-bulu',
    '事业单位联考职业能力倾向测验考情分析': 'shiye-liankao-zhiye-nce',
    '中级社工证报考条件': 'zhongji-shegongzheng-tiaojian',
    '初级社工证报考条件': 'chuji-shegongzheng-tiaojian',
    '云南社区工作者招聘': 'yunnan-shegong-zhaopin',
    '南昌社区工作者招聘': 'nanchang-shegong-zhaopin',
    '厦门社区工作者招聘': 'xiamen-shegong-zhaopin',
    '合肥社区工作者招聘': 'hefei-shegong-zhaopin',
    '吉林社区工作者招聘': 'jilin-shegong-zhaopin',
    '哈尔滨社区工作者招聘': 'haerbin-shegong-zhaopin',
    '四川社区工作者招聘': 'sichuan-shegong-zhaopin',
    '大连社区工作者招聘': 'dalian-shegong-zhaopin',
    '宁波社区工作者招聘': 'ningbo-shegong-zhaopin',
    '安徽社区工作者招聘': 'anhui-shegong-zhaopin',
    '山西社区工作者招聘': 'shanxi-shegong-zhaopin',
    '广东社区工作者招聘': 'guangdong-shegong-zhaopin',
    '广西社区工作者招聘': 'guangxi-shegong-zhaopin',
    '昆明社区工作者招聘': 'kunming-shegong-zhaopin',
    '江苏社区工作者招聘': 'jiangsu-shegong-zhaopin',
    '江西社区工作者招聘': 'jiangxi-shegong-zhaopin',
    '沈阳社区工作者招聘': 'shenyang-shegong-zhaopin',
    '河北社区工作者招聘': 'hebei-shegong-zhaopin',
    '济南社区工作者招聘': 'jinan-shegong-zhaopin',
    '浙江社区工作者招聘': 'zhejiang-shegong-zhaopin',
    '湖北社区工作者招聘': 'hubei-shegong-zhaopin',
    '湖南社区工作者招聘': 'hunan-shegong-zhaopin',
    '国考和社区工作者哪个好': 'guokao-vs-shegong-better',
    '省考和社区工作者哪个好': 'shengkao-vs-shegong-better',
    '社区工作者公共基础知识': 'shegong-gonggong-jichu',
    '社区工作者判断推理技巧': 'shegong-panduan-tuili',
    '社区工作者可以考公务员吗': 'shegong-keyi-kao-gwy',
    '社区工作者和三支一扶区别': 'shegong-vs-sanzhiyifu',
    '社区工作者和特岗教师区别': 'shegong-vs-tegang',
    '社区工作者常识判断': 'shegong-changshi-panduan',
    '社区工作者持证上岗': 'shegong-chizheng-shanggang',
    '社区工作者政审严格吗': 'shegong-zhengshen-yange',
    '社区工作者数量关系技巧': 'shegong-shuliang-guanxi',
    '社区工作者新政策2026': 'shegong-xin-zhengce-2026',
    '社区工作者有效期几年': 'shegong-youxiaoqi-jinian',
    '社区工作者申论怎么写': 'shegong-shenlun-xie',
    '社区工作者考试报名费': 'shegong-kaoshi-baoming-fei',
    '社区工作者职业化改革': 'shegong-zhiyehua-gaige',
    '社区工作者薪酬改革': 'shegong-xinchou-gaige',
    '社区工作者行测怎么复习': 'shegong-xingce-fuxi',
    '社区工作者要考几次': 'shegong-yao-kao-jici',
    '社区工作者言语理解技巧': 'shegong-yanyu-lijei',
    '社区工作者试用期多久': 'shegong-shiyongqi-duoji',
    '社区工作者资料分析技巧': 'shegong-ziliao-fenxi',
    '社工证含金量': 'shegongzheng-hanjinliang',
    '社工证怎么复习': 'shegongzheng-zenme-fuxi',
    '社工证考试时间2026': 'shegongzheng-kaoshi-shijian-2026',
    '社工证难考吗': 'shegongzheng-nan-kao',
    '福州社区工作者招聘': 'fuzhou-shegong-zhaopin',
    '福建社区工作者招聘': 'fujian-shegong-zhaopin',
    '西安社区工作者招聘': 'xian-shegong-zhaopin',
    '贵州社区工作者招聘': 'guizhou-shegong-zhaopin',
    '辽宁社区工作者招聘': 'liaoning-shegong-zhaopin',
    '郑州社区工作者招聘': 'zhengzhou-shegong-zhaopin',
    '长春社区工作者招聘': 'changchun-shegong-zhaopin',
    '长沙社区工作者招聘': 'changsha-shegong-zhaopin',
    '陕西社区工作者招聘': 'shaanxi-shegong-zhaopin',
    '青岛社区工作者招聘': 'qingdao-shegong-zhaopin',
    '黑龙江社区工作者招聘': 'heilongjiang-shegong-zhaopin',
    '上海社区工作者各区招聘计划解读': 'shanghai-shegong-geqv-jihua',
    '上海社工考试行测模块备考策略及真题分析': 'shanghai-shegong-xingce-beikao',
    '上海社区工作者各区待遇对比分析': 'shanghai-shegong-geqv-daiyu',
    '省考申论大作文万能框架及高分技巧': 'shengkao-shenlun-dazuo-wanneng',
    '省考联考省份及考试时间汇总': 'shengkao-liankao-shengfen-shijian',
    '社区工作者省考与国考区别': 'shegong-vs-shengkao-guokao',
}

def contains_chinese(text):
    """Check if string contains Chinese characters"""
    return any('\u4e00' <= c <= '\u9fff' for c in text)

def convert_filename(old_filename):
    """
    Convert filename with Chinese characters to English slug.
    Returns (new_filename, matched_key) or (None, None) if no conversion needed.
    """
    # Remove extension
    name_without_ext = re.sub(r'\.(md|mdx)$', '', old_filename)
    ext = old_filename[len(name_without_ext):]
    
    if not contains_chinese(name_without_ext):
        return None, None
    
    # Try to find matching key in mapping (try longest match first)
    matched_key = None
    for key in sorted(SLUG_MAPPING.keys(), key=len, reverse=True):
        if key in name_without_ext:
            matched_key = key
            new_name = name_without_ext.replace(key, SLUG_MAPPING[key])
            return new_name + ext, matched_key
    
    # If no mapping found, return None (skip this file)
    return None, None

def rename_file_safely(old_path, new_path):
    """Safely rename file, checking for conflicts"""
    if os.path.exists(new_path):
        print(f"  ⚠️  Target file already exists: {os.path.basename(new_path)}")
        return False
    try:
        shutil.move(old_path, new_path)
        return True
    except Exception as e:
        print(f"  ❌ Error renaming: {e}")
        return False

def main():
    content_dir = "content"
    renamed = []
    skipped = []
    
    print("=" * 70)
    print("Chinese Slug Fixer for Next.js SSG on Vercel")
    print("=" * 70)
    print()
    
    # Walk through all content files
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            if not (filename.endswith('.md') or filename.endswith('.mdx')):
                continue
            
            filepath = os.path.join(root, filename)
            new_filename, matched_key = convert_filename(filename)
            
            if new_filename is None:
                if contains_chinese(filename):
                    skipped.append((filepath, "No mapping found"))
                continue
            
            new_filepath = os.path.join(root, new_filename)
            print(f"Processing: {filename}")
            print(f"  -> {new_filename}")
            
            if rename_file_safely(filepath, new_filepath):
                renamed.append((filepath, new_filepath, matched_key))
                print(f"  ✅ Renamed successfully")
            print()
    
    # Summary
    print("=" * 70)
    print(f"Total files renamed: {len(renamed)}")
    print(f"Total files skipped: {len(skipped)}")
    
    if skipped:
        print("\nSkipped files (no mapping):")
        for filepath, reason in skipped:
            print(f"  - {os.path.basename(filepath)}: {reason}")
    print("=" * 70)
    
    # Save log
    if renamed:
        log_file = f"slug_fix_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Chinese Slug Fix Log\n")
            f.write("=" * 70 + "\n\n")
            for old, new, key in renamed:
                f.write(f"OLD: {old}\n")
                f.write(f"NEW: {new}\n")
                f.write(f"MAPPING KEY: {key}\n")
                f.write("-" * 70 + "\n")
        print(f"\nLog saved to: {log_file}")

if __name__ == "__main__":
    main()
