# ============================================================
# 公考图片库下载脚本 - gk.edu-sjtu.cn 专用
# 使用 Pexels API 获取真实、非AI生成的高质量图片
# ============================================================

## ⚠️ 使用前必读

### 1. 获取 Pexels API Key（免费）
1. 访问 https://www.pexels.com/api/
2. 注册账号并登录
3. 点击 "Your API Key" 复制 API Key
4. 将 API Key 填入下方配置区

### 2. API 限制说明
- 免费额度：每日 200 张图片下载
- 获取 1000+ 图片：约 5-6 天可完成
- 可申请更多额度（免费）

### 3. 图片主题分类
```
├── study/         # 学习备考（读书、图书馆、做笔记）
├── exam/          # 考试上岸（考场、自信、毕业）
├── career/        # 职场政府（办公场景、公职人员）
├── city/          # 城市政策（城市建筑、文件）
└── motivation/    # 励志奋斗（日出、攀登、坚持）
```

## API Key 配置
PEXELS_API_KEY=your_api_key_here

## 使用方法
pip install requests Pillow
python download_images.py
