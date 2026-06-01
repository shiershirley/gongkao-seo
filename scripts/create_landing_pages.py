#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建二维码扫描后的资料领取落地页
"""

import os

LANDING_PAGES = {
    "ziliao/index.html": {
        "title": "公考备考资料领取中心",
        "subtitle": "扫码成功！请选择您需要的备考资料",
        "items": [
            {"name": "2026国考职位表完整版", "desc": "含报录比、进面分数线", "link": "/guokao/"},
            {"name": "申论高分范文100篇", "desc": "历年高分范文精选", "link": "/guokao/"},
            {"name": "行测速算技巧手册", "desc": "资料分析速算公式", "link": "/beikao-zhinan/"},
            {"name": "面试真题解析合集", "desc": "结构化面试真题+解析", "link": "/beikao-zhinan/"},
            {"name": "公考备考时间规划表", "desc": "3个月/6个月备考计划", "link": "/beikao-zhinan/"},
        ]
    },
    "ziliao/guokao/index.html": {
        "title": "国考备考资料领取",
        "subtitle": "扫码成功！国考专属资料包",
        "items": [
            {"name": "2026国考职位表完整版", "desc": "含报录比、进面分数线", "link": "/guokao/"},
            {"name": "国考行测高频考点速记", "desc": "言语/数量/判断/资料/常识", "link": "/guokao/"},
            {"name": "申论大作文万能模板", "desc": "10套高分模板", "link": "/guokao/"},
            {"name": "国考面试真题80道", "desc": "结构化+无领导小组", "link": "/guokao/"},
            {"name": "2026国考报考指南", "desc": "报名流程、照片要求、缴费说明", "link": "/guokao/"},
        ]
    },
    "ziliao/shengkao/index.html": {
        "title": "省考备考资料领取",
        "subtitle": "扫码成功！省考专属资料包",
        "items": [
            {"name": "各省省考时间表汇总", "desc": "2026年各省笔试面试时间", "link": "/shengkao/"},
            {"name": "省考选岗技巧指南", "desc": "如何避开热门岗位", "link": "/shengkao/"},
            {"name": "申论省考真题合集", "desc": "近5年各省申论真题", "link": "/shengkao/"},
            {"name": "行测省考模拟试卷", "desc": "3套全真模拟题", "link": "/shengkao/"},
        ]
    },
    "ziliao/shegong/index.html": {
        "title": "上海社工备考资料领取",
        "subtitle": "扫码成功！社工专属资料包",
        "items": [
            {"name": "上海社工考试大纲", "desc": "笔试内容+面试形式", "link": "/shanghai-shegong/"},
            {"name": "社工政策法规汇编", "desc": "社区工作相关法律法规", "link": "/shanghai-shegong/"},
            {"name": "社工面试模拟题", "desc": "结构化面试50道", "link": "/shanghai-shegong/"},
            {"name": "上海社工待遇解析", "desc": "各区薪资+福利对比", "link": "/shanghai-shegong/"},
        ]
    },
    "ziliao/shiyedanwei/index.html": {
        "title": "事业单位备考资料领取",
        "subtitle": "扫码成功！事业编专属资料包",
        "items": [
            {"name": "事业单位考试大纲", "desc": "职测+综应考试内容", "link": "/shiye-dan-wei/"},
            {"name": "事业单位岗位竞争比", "desc": "热门岗位vs冷门岗位", "link": "/shiye-dan-wei/"},
            {"name": "职测高频考点", "desc": "数量关系/判断推理速解", "link": "/shiye-dan-wei/"},
            {"name": "综应写作模板", "desc": "公文写作+案例分析", "link": "/shiye-dan-wei/"},
        ]
    },
}

def generate_html(page_data):
    """生成落地页HTML"""
    title = page_data["title"]
    subtitle = page_data["subtitle"]
    items = page_data["items"]
    
    items_html = ""
    for item in items:
        items_html += f'''
        <a href="{item['link']}" class="item-card">
            <h3>{item['name']}</h3>
            <p>{item['desc']}</p>
            <span class="btn">立即查看 &rarr;</span>
        </a>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 公考资讯站</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .header p {{ font-size: 18px; opacity: 0.9; }}
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        .item-card {{
            background: white;
            border-radius: 12px;
            padding: 28px;
            text-decoration: none;
            color: #333;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .item-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .item-card h3 {{
            font-size: 20px;
            color: #1890ff;
            margin-bottom: 8px;
        }}
        .item-card p {{
            font-size: 14px;
            color: #666;
            margin-bottom: 16px;
            line-height: 1.6;
        }}
        .btn {{
            display: inline-block;
            background: #1890ff;
            color: white;
            padding: 10px 24px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            font-size: 14px;
            opacity: 0.8;
        }}
        .footer a {{ color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div class="card-grid">
            {items_html}
        </div>
        <div class="footer">
            <p>更多公考资讯，请访问 <a href="/">公考资讯站</a></p>
            <p style="margin-top:10px; font-size:12px;">提示：关注公众号"上海公考资讯站"，回复"资料"获取更多备考资源</p>
        </div>
    </div>
</body>
</html>'''
    return html

def main():
    print("=" * 60)
    print("创建资料领取落地页")
    print("=" * 60)
    
    for filepath, data in LANDING_PAGES.items():
        fullpath = os.path.join("public", filepath)
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        
        html = generate_html(data)
        with open(fullpath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[成功] {filepath}")
    
    print("\n" + "=" * 60)
    print("落地页创建完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
