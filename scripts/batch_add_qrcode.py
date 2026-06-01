#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为现有文章添加二维码区块
在已有CTA后面追加二维码引导
"""

import os
import re
from pathlib import Path

# 分类到二维码的映射
CATEGORY_QR_MAP = {
    "guokao": ("/images/qrcode/qrcode-guokao.png", "扫码领取国考资料包"),
    "shengkao": ("/images/qrcode/qrcode-shengkao.png", "扫码领取省考资料包"),
    "shanghai-shegong": ("/images/qrcode/qrcode-shegong.png", "扫码领取社工备考资料"),
    "gangwei-fenxi": ("/images/qrcode/qrcode-shiyedanwei.png", "扫码领取事业编资料包"),
    "shiye-dan-wei": ("/images/qrcode/qrcode-shiyedanwei.png", "扫码领取事业编资料包"),
    "shiyedanwei": ("/images/qrcode/qrcode-shiyedanwei.png", "扫码领取事业编资料包"),
    "beikao-zhinan": ("/images/qrcode/qrcode-general.png", "扫码领取备考资料"),
    "zhengce-jiedu": ("/images/qrcode/qrcode-general.png", "扫码领取政策解读资料"),
    "baokao-gonggao": ("/images/qrcode/qrcode-general.png", "扫码获取最新公告提醒"),
    "zhenti-jiexi": ("/images/qrcode/qrcode-general.png", "扫码领取真题资料"),
    "shang-an-jingyan": ("/images/qrcode/qrcode-general.png", "扫码加入上岸交流群"),
}

def extract_category(content):
    """从文章frontmatter中提取category"""
    match = re.search(r'^category:\s*"([^"]+)"', content, re.MULTILINE)
    if match:
        return match.group(1)
    return "default"

def generate_qr_html(category):
    """根据分类生成二维码HTML"""
    qr_code, qr_title = CATEGORY_QR_MAP.get(category, ("/images/qrcode/qrcode-general.png", "扫码领取备考资料"))
    
    return f"""

<div class="qr-section" style="background: #fff; border: 2px dashed #1890ff; padding: 24px; margin: 30px 0; border-radius: 8px; text-align: center;">
  <h3 style="margin-top: 0; color: #1890ff; font-size: 18px;">{qr_title}</h3>
  <p style="color: #666; font-size: 14px; margin: 10px 0;">手机扫码，免费领取备考资料包</p>
  <img src="{qr_code}" alt="{qr_title}" style="width: 180px; height: 180px; margin: 15px auto; display: block; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  <p style="color: #999; font-size: 12px; margin-top: 10px;">关注后回复"资料"，自动发送下载链接</p>
</div>
"""

def process_article(md_path):
    """处理单个文章文件"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有二维码区块
        if 'qr-section' in content:
            return False, "已包含二维码"
        
        # 提取分类
        category = extract_category(content)
        
        # 生成二维码HTML
        qr_html = generate_qr_html(category)
        
        # 在文章末尾追加二维码
        # 找到最后一个 </div> 或 <script> 标签之后追加
        # 简单策略：在文件末尾追加
        new_content = content.rstrip() + qr_html + "\n"
        
        # 写回文件
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"已添加二维码 [分类: {category}]"
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    base_dir = Path("content")
    if not base_dir.exists():
        print(f"[失败] 目录不存在: {base_dir}")
        return
    
    print("=" * 70)
    print("批量添加二维码到现有文章")
    print("=" * 70)
    
    processed = 0
    modified = 0
    skipped = 0
    failed = 0
    
    for category_dir in base_dir.iterdir():
        if not category_dir.is_dir():
            continue
        
        for md_file in category_dir.glob("*.md"):
            processed += 1
            is_modified, msg = process_article(md_file)
            
            if is_modified:
                modified += 1
                if modified <= 10 or modified % 100 == 0:
                    print(f"[{modified}] {md_file.name} - {msg}")
            elif "已包含二维码" in msg:
                skipped += 1
            else:
                failed += 1
                print(f"[X] {md_file.name} - {msg}")
    
    print("\n" + "=" * 70)
    print("处理完成")
    print(f"  扫描: {processed} 篇")
    print(f"  修改: {modified} 篇")
    print(f"  跳过: {skipped} 篇（已包含二维码）")
    print(f"  失败: {failed} 篇")
    print("=" * 70)

if __name__ == "__main__":
    main()
