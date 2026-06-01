#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成网站二维码图片
- 通用二维码：指向网站资料领取页
- 分类二维码：指向各分类资料页
"""

import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont

def create_qr_with_text(url, title, output_path, size=400):
    """生成带标题的二维码图片"""
    # 创建二维码
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # 生成二维码图像
    qr_img = qr.make_image(fill_color="#1890ff", back_color="white").convert('RGB')
    qr_img = qr_img.resize((size, size))
    
    # 创建带文字的新图像
    padding_top = 60
    padding_bottom = 40
    new_width = size + 40
    new_height = size + padding_top + padding_bottom
    
    new_img = Image.new('RGB', (new_width, new_height), 'white')
    
    # 粘贴二维码
    new_img.paste(qr_img, (20, padding_top))
    
    # 添加标题文字
    draw = ImageDraw.Draw(new_img)
    
    # 尝试加载字体
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
    except:
        try:
            font_title = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 24)
            font_sub = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 16)
        except:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
    
    # 绘制标题
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (new_width - title_width) // 2
    draw.text((title_x, 15), title, fill="#1890ff", font=font_title)
    
    # 绘制副标题
    sub_text = "扫码领取备考资料"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (new_width - sub_width) // 2
    draw.text((sub_x, new_height - 30), sub_text, fill="#666666", font=font_sub)
    
    # 保存
    new_img.save(output_path, quality=95)
    print(f"[成功] 生成二维码: {output_path}")
    return output_path

def main():
    base_url = "https://gk.edu-sjtu.cn"
    output_dir = "public/images/qrcode"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 定义各分类二维码
    qr_configs = [
        ("通用", f"{base_url}/ziliao/", "qrcode-general.png"),
        ("国考", f"{base_url}/ziliao/guokao/", "qrcode-guokao.png"),
        ("省考", f"{base_url}/ziliao/shengkao/", "qrcode-shengkao.png"),
        ("上海社工", f"{base_url}/ziliao/shegong/", "qrcode-shegong.png"),
        ("事业单位", f"{base_url}/ziliao/shiyedanwei/", "qrcode-shiyedanwei.png"),
    ]
    
    print("=" * 60)
    print("生成网站二维码")
    print("=" * 60)
    
    generated = []
    for title, url, filename in qr_configs:
        output_path = os.path.join(output_dir, filename)
        create_qr_with_text(url, title, output_path)
        generated.append({
            "category": title,
            "url": url,
            "file": f"/images/qrcode/{filename}"
        })
    
    print("\n" + "=" * 60)
    print("二维码生成完成")
    print("=" * 60)
    for g in generated:
        print(f"  [{g['category']}] {g['file']}")
        print(f"     指向: {g['url']}")
    
    return generated

if __name__ == "__main__":
    main()
