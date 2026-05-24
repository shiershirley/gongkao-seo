# 🏛️ 公考SEO自动内容发布系统

> 一个全自动化的SEO内容生产与发布系统，涵盖**关键词策略 → AI内容生成 → 图片配图 → 质量校验 → Git部署 → 收录监控**完整闭环。

**部署地址**：https://gk.edu-sjtu.cn  
**日均产出**：约 100 篇文章（7-8 批次 × 7-8 篇/批）  
**技术栈**：Next.js + TypeScript + TailwindCSS + Vercel + Python 自动化脚本

---

## 📌 目录

- [项目概述](#项目概述)
- [架构总览](#架构总览)
- [文件结构](#文件结构)
- [环境搭建](#环境搭建)
- [内容体系](#内容体系)
- [自动化流水线](#自动化流水线)
- [核心脚本详解](#核心脚本详解)
- [图片配图系统](#图片配图系统)
- [SEO优化措施](#seo优化措施)
- [Git操作规范](#git操作规范)
- [关键词策略](#关键词策略)
- [收录监控](#收录监控)
- [常见问题与踩坑](#常见问题与踩坑)
- [待办事项](#待办事项)

---

## 项目概述

这是一个面向公考行业的SEO内容网站，自动化生产并发布国考、省考、上海社区工作者、事业单位等公考相关文章。整个流程由AI驱动，每日定时执行，无人值守。

### 核心数据

| 指标 | 数据 |
|------|------|
| 内容分类 | 9个 |
| 累计文章数 | 900+ 篇 |
| 每篇文章字数 | 1,500-2,500 字 |
| 日均产出 | ~100 篇 |
| 单日最高纪录 | 209 篇（2026-05-19） |
| 图片库 | 1,150+ 张（12个主题） |
| Bing 收录率 | ~100%（部署成功即可达） |
| Google 收录率 | ~33%（受国内网络限制） |

---

## 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                      自动化流水线                            │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│  关键词池    │  AI生成文章  │  质量校验    │  Git → Vercel    │
│  .md 文件   │  每批8篇     │  YAML检查   │  自动部署         │
│  P0-P3分级  │  内容比例分配│  自动修复    │  百度自动推送     │
│  角度轮换   │  图片配图    │             │                  │
└─────────────┴─────────────┴─────────────┴──────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      监控闭环                               │
├─────────────────────────────────────────────────────────────┤
│  收录检查（次日07:00）  →  四维度（Sitemap/百度/Bing/Google）│
│  周报生成（每周一09:00） →  收录率趋势 + 优化建议            │
└─────────────────────────────────────────────────────────────┘
```

### 技术架构

```
前端：Next.js 16 (App Router) + React 19 + TypeScript + TailwindCSS 4
部署：Vercel (连接 GitHub 仓库自动部署)
脚本：Python 3（Windows 环境，30+ 脚本文件）
内容：Markdown (.md) + YAML Frontmatter
图片：Pexels API 下载 → 本地 /images/lib/ 静态托管
监控：百度统计 + 百度自动推送 + 四维度收录检查脚本
```

---

## 文件结构

```
gongkao-seo/
├── README.md                          # 本文件
├── package.json                       # Node.js 依赖
├── next.config.ts                     # Next.js 配置（图片缓存策略）
│
├── content/                           # ★ 文章内容（Markdown 文件）
│   ├── guokao/                        #     国考
│   ├── shengkao/                      #     省考
│   ├── shanghai-shegong/              #     上海社区工作者
│   ├── baokao-gonggao/               #     报考公告
│   ├── zhengce-jiedu/                #     政策解读
│   ├── beikao-zhinan/                #     备考指南
│   ├── zhenti-jiexi/                 #     真题解析
│   ├── gangwei-fenxi/                #     岗位分析（含事业单位）
│   └── shang-an-jingyan/             #     上岸经验
│
├── src/                               # Next.js 源代码
│   ├── app/
│   │   ├── layout.tsx                 # 根布局（SEO元数据/百度统计/JSON-LD）
│   │   ├── page.tsx                   # 首页
│   │   ├── sitemap.ts                 # 动态生成 sitemap.xml
│   │   ├── robots.ts                  # robots.txt
│   │   ├── [category]/page.tsx        # 分类列表页（SSG）
│   │   └── [category]/[slug]/page.tsx # 文章详情页（SSG + JSON-LD）
│   ├── components/
│   │   ├── layout/Header.tsx          # 顶部导航
│   │   ├── layout/Footer.tsx          # 底部
│   │   └── ui/                        # ArticleCard / Breadcrumbs
│   └── lib/
│       ├── content.ts                 # 核心数据层（遍历MD/解析frontmatter）
│       └── types.ts                   # TypeScript 类型定义
│
├── scripts/                           # ★ Python 自动化脚本（详见下方）
│   ├── frontmatter_validator.py       #  YAML校验 + 自动修复（核心）
│   ├── keyword_driven_generator.py    #  关键词驱动文章生成器
│   ├── seo_indexing_checker.py       #  四维度收录检查
│   ├── image_picker.py               #  图片智能选取
│   ├── insert_images.py              #  文章图片插入
│   ├── keywords_pool.md              #  关键词池（P0-P3）
│   ├── auto_gen_xxxx.py              #  各时段生成脚本
│   └── ...                           #  更多辅助脚本
│
├── images/                            # ★ 图片库
│   ├── lib/                           # 12个主题目录（study/exam/career/gov/...）
│   │   └── index.json                  # 图片索引
│   ├── gk_images/                     # 公考主题专用图片
│   └── README.md                      # Pexels API 下载说明
│
├── reports/                           # SEO收录检查报告
│   └── indexing_check_*.md            # 按日期组织的收录报告
│
└── docs/
    └── SEO收录优化策略.md              # SEO策略文档
```

---

## 环境搭建

### 前置条件

| 工具 | 版本要求 | 说明 |
|------|---------|------|
| Node.js | ≥18.x | 前端构建 |
| Python | ≥3.8 | 自动化脚本 |
| Git | 任意版本 | 版本控制与Vercel部署 |
| GitHub 账号 | - | 连接Vercel自动部署 |
| Vercel 账号 | - | 网站托管 |
| Pexels API Key | 免费申请 | 图片下载 |

### 安装步骤

```bash
# 1. 克隆项目
git clone <你的仓库地址>
cd gongkao-seo

# 2. 安装 Node.js 依赖
npm install

# 3. 安装 Python 依赖
pip install requests Pillow

# 4. 配置 Pexels API Key（用于下载图片）
# 访问 https://www.pexels.com/api/ 注册获取 Key
# 更新 images/download_images.py 中的 API_KEY

# 5. 下载图片库（首次需要）
cd images
python download_images.py

# 6. 启动开发服务器
npm run dev
# 访问 http://localhost:3000
```

### Vercel 部署

1. 将项目推送到 GitHub
2. 在 Vercel 中新建 Project，连接该仓库
3. Vercel 自动识别 Next.js，无需额外配置
4. 绑定自定义域名（本项目使用 `gk.edu-sjtu.cn`）
5. 每次 `git push` 到 main 分支自动触发部署

---

## 内容体系

### 9个合法分类

| 分类 slug | 中文名 | 描述 | SEO关键词 |
|-----------|--------|------|-----------|
| `guokao` | 国考 | 国家公务员考试招录公告、职位表、政策解读 | 国考、国家公务员考试、国考公告 |
| `shengkao` | 省考 | 各省市公务员考试信息汇总 | 省考、省考公告、省考时间 |
| `shanghai-shegong` | 上海社区工作者 | 上海社工招聘公告、考试、待遇 | 上海社区工作者、上海社工 |
| `baokao-gonggao` | 报考公告 | 各类公职考试报名公告、时间节点 | 招考公告、报名入口、考试时间 |
| `zhengce-jiedu` | 政策解读 | 考试政策变化、新规解读 | 政策解读、考试政策、报考条件 |
| `beikao-zhinan` | 备考指南 | 行测、申论、面试备考方法 | 备考指南、行测、申论、面试 |
| `zhenti-jiexi` | 真题解析 | 历年真题解析与答题技巧 | 真题、真题解析、历年真题 |
| `gangwei-fenxi` | 岗位分析 | 热门岗位、薪资待遇、职业发展 | 岗位分析、岗位待遇、热门岗位 |
| `shang-an-jingyan` | 上岸经验 | 学员备考经验与心得分享 | 上岸经验、备考心得、经验分享 |

> ⚠️ **重要**：`shiye-dan-wei`（含连字符/无连字符变体）不是合法分类。事业单位内容统一归入 `gangwei-fenxi`，否则会导致页面404。

### YAML Frontmatter 规范

每篇文章开头必须包含完整的 YAML frontmatter：

```yaml
---
title: "2026年省考备考全攻略：从零基础到笔试上线的系统学习方法"
description: "2026年省考竞争持续激烈，本文从备考规划、行测专项、申论技巧三大维度，提供系统备考方法。"
date: "2026-04-26"
category: "beikao-zhinan"
tags: ["省考备考", "2026省考", "行测备考", "申论技巧", "公务员备考方法"]
author: "公考资讯站"
---
```

#### 字段要求

| 字段 | 要求 | 示例 |
|------|------|------|
| `title` | 必填，25字以内，必须包含核心关键词 | `"2026年国考职位表全面解析"` |
| `description` | 必填，100-160字，必须包含关键词 | 见上 |
| `date` | 必填，YYYY-MM-DD 格式，**必须加引号** | `"2026-05-20"` |
| `category` | 必填，必须是9个合法分类之一 | `"beikao-zhinan"` |
| `tags` | 必填，列表格式，3-5个标签 | `["标签1", "标签2"]` |
| `author` | 必填 | `"公考资讯站"` 或 `"公考SEO"` |

#### ⚠️ 关键规范（踩坑经验）

1. **description 内嵌引号必须用日文直角引号「」代替英文双引号 "**
   - ❌ 错误：`description: "考生常把"网上填表"理解为报名..."`
   - ✅ 正确：`description: "考生常把「网上填表」理解为报名..."`

2. **date 字段必须加引号**
   - ❌ 错误：`date: 2026-05-19` → YAML 解析为 Date 对象 → 前端显示 Unix 时间戳
   - ✅ 正确：`date: "2026-05-19"`

3. **date 不能是未来日期**（严格禁止）

4. **tags 必须是列表格式**
   - ❌ 错误：`tags: 标签1` 或 `tags: "标签1"`
   - ✅ 正确：`tags: ["标签1", "标签2"]`

5. **文件名格式**：`YYYY-MM-DD-简短slug.md`（日期前缀用于脚本识别）

### 内容比例配置（每批次8篇）

| 类别 | 数量 | 占比 | 分配 |
|------|------|------|------|
| 上海社工 | 2篇 | 25% | shanghai-shegong |
| 国考 | 2篇 | 25% | guokao |
| 省考 | 2篇 | 25% | shengkao |
| 事业单位 | 1篇 | 12.5% | gangwei-fenxi |
| 通用备考 | 1篇 | 12.5% | beikao-zhinan |

---

## 自动化流水线

### 流程总览

```
关键词池读取 → AI生成文章(8篇/批) → 图片配图 → frontmatter校验
                                                       ↓
                                                  git add + commit
                                                       ↓
                                                  git push → Vercel自动部署
                                                       ↓
                                              百度自动推送（push.js）
                                                       ↓
                                         收录检查（次日07:00，四维度）
                                                       ↓
                                         周报生成（每周一09:00）
```

### 自动化任务调度

系统通过 WorkBuddy 自动化引擎按时段调度：

| 时段 | 任务ID | 批次 | 产量 |
|------|--------|------|------|
| 06:00 | seo-8-00 | 第1批 | 8篇 |
| 08:00 | seo-8-00-2 | 第2批 | 8篇 |
| 08:30 | seo-8-30 | 第3批 | 8篇 |
| 09:00 | seo-9-00 | 第4批 | 8篇 |
| 09:15 | seo-9-15 | 第5批 | 8篇 |
| 10:00 | seo-10-00 | 第6批 | 8篇 |
| 10:00 | seo-10-00-2 | 第7批 | 8篇 |
| 10:30 | seo-2 | 收录检查 | — |

> **日均总产量**：7批 × 8篇 = 56篇（基础），实际可达100+。

### 完成后必检项

发布后必须执行以下检查确保质量：

- [ ] 首页 HTTP 200 正常访问
- [ ] 每篇文章正常打开（日期格式正确、正文完整、无乱码）
- [ ] 配图正常加载
- [ ] sitemap.xml 包含所有新文章URL
- [ ] Vercel 部署状态无报错

---

## 核心脚本详解

### 1. `frontmatter_validator.py` — 质量守卫

```bash
python -X utf8 scripts/frontmatter_validator.py              # 校验全部文章
python -X utf8 scripts/frontmatter_validator.py content/guokao/  # 指定目录
python -X utf8 scripts/frontmatter_validator.py --fix          # 自动修复
```

**校验维度**：
- ✅ 6个必填字段：title / description / date / category / tags / author
- ✅ description 未转义英文双引号检测
- ✅ date 格式（YYYY-MM-DD）+ 未来日期检测
- ✅ category 合法性（9个分类白名单）
- ✅ tags 列表格式检测
- ✅ 关键词覆盖率建议提示（不强制）

**`--fix` 自动修复**：将 description 内的英文双引号替换为日文直角引号「」。

### 2. `keyword_driven_generator.py` — 关键词策略引擎

```bash
python -X utf8 scripts/keyword_driven_generator.py --list      # 列出未覆盖关键词
python -X utf8 scripts/keyword_driven_generator.py --next      # 推荐下一个关键词
python -X utf8 scripts/keyword_driven_generator.py --prompt    # 生成文章指令
```

**功能**：
- 扫描 content/ 下所有文章的 title / tags / description 提取已覆盖关键词
- 按 P0 → P3 优先级遍历关键词池，找出未覆盖项
- 自动推断关键词的推荐分类（社工→shanghai-shegong，国考→guokao 等）
- 生成包含 SEO 要求的文章生成指令

### 3. `seo_indexing_checker.py` — 收录监控

```bash
python -X utf8 scripts/seo_indexing_checker.py                       # 检查10天前文章
python -X utf8 scripts/seo_indexing_checker.py --date 2026-05-14    # 指定日期
python -X utf8 scripts/seo_indexing_checker.py --days-ago 7          # N天前
```

**检查维度**：

| 维度 | 方法 | 可靠性 | 注意 |
|------|------|--------|------|
| Sitemap | 请求 sitemap.xml 精确匹配URL | ⭐⭐⭐⭐⭐ | 最快最准 |
| Bing | site: 查询 | ⭐⭐⭐⭐ | 主要参考 |
| 百度 | site: 查询 | ⭐⭐ | 反爬极强，大概率被拦截 |
| Google | site: 查询 | ⭐⭐ | 国内网络受限 |

**三种判定**：✅ 已收录 / ❌ 确认未收录 / ⚠️ 无法判断（反爬/网络限制）

报告自动保存到 `reports/indexing_check_YYYYMMDD_HHMMSS.md`。

### 4. `image_picker.py` — 智能配图

```bash
python scripts/image_picker.py --category shang-an-jingyan --count 2
python scripts/image_picker.py --category beikao-zhinan --count 1 --update --json
```

**核心机制**：
- 9类文章各有5个匹配图片主题（优先级排序）
- 10天内不重复选择同一张图（通过 `image_usage_log.json` 追踪）
- 可用图片不足时自动放宽限制：10天 → 5天 → 不限
- `--update` 标记图片为已使用，防止重复

### 5. `insert_images.py` — 图片插入

自动调用 `image_picker.py`，将选取的图片以 `![alt](path)` 格式插入到文章的 `## ` 标题前。

### 6. `complete_article_processing.py` — 一键完成

整合三个步骤：① 图片插入 → ② Frontmatter 校验 → ③ Git 提交推送。

---

## 图片配图系统

### 图片库结构

图片通过 [Pexels API](https://www.pexels.com/api/) 下载，12个主题分类：

```
images/lib/
├── study/      # 学习备考（读书、图书馆、笔记）
├── exam/       # 考试上岸（考场、自信、毕业）
├── career/     # 职场发展
├── city/       # 城市景观
├── motivation/ # 励志奋斗
├── books/      # 书籍资料
├── gov/        # 政府政务
├── office/     # 办公场景
├── people/     # 人物形象
├── tech/       # 科技数字
├── nature/     # 自然风景
└── writing/    # 笔记文档
```

### 文章分类 → 图片主题映射

| 文章分类 | 优先图片主题（前→后） |
|----------|----------------------|
| guokao | exam → study → gov → motivation → office |
| shengkao | exam → study → motivation → office → books |
| shanghai-shegong | gov → office → people → city → exam |
| baokao-gonggao | gov → office → writing → exam → study |
| zhengce-jiedu | gov → office → writing → city → tech |
| beikao-zhinan | study → books → exam → motivation → writing |
| zhenti-jiexi | exam → study → books → writing → office |
| gangwei-fenxi | office → people → gov → tech → city |
| shang-an-jingyan | exam → motivation → people → study → office |

### 图片配置

```typescript
// next.config.ts 中配置 1 年强缓存
headers: async () => [{
  source: "/images/:path*",
  headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }],
}]
```

---

## SEO优化措施

### 结构化数据（JSON-LD）

| 位置 | Schema 类型 | 作用 |
|------|------------|------|
| 全局 `<head>` | `Organization` | 品牌信号 |
| 全局 `<head>` | `WebSite` + `SearchAction` | 触发 Google 即时答案框 |
| 文章详情页 | `Article` | 文章结构化展示 |
| 面包屑导航 | `BreadcrumbList` | 面包屑路径标记 |

### 页面级 SEO

| 措施 | 说明 |
|------|------|
| Canonical URL | 每页设置唯一规范URL |
| Open Graph / Twitter Card | 社交分享优化 |
| 动态 sitemap.xml | 包含首页 + 分类页 + 所有文章（SSG自动生成） |
| robots.txt | 允许全部爬虫，禁止 `/api/` 和 `/admin/` |
| 百度统计 | 集成百度统计代码（hm.js） |
| 百度自动推送 | 集成 push.js 自动提交URL |
| 百度站点验证 | meta codeva-Uerc481wpT |
| Google 站点验证 | meta fs28DCK1- |

### Sitemap 配置

- 首页：`priority: 1.0`，`daily`
- 分类页：`priority: 0.8`，`daily`
- 文章页：`priority: 0.6`，`weekly`

---

## Git操作规范

### Commit 格式

```
content: auto publish articles YYYY-MM-DD HH:MM (N articles)
```

示例：
```
content: auto publish articles 2026-05-22 08:00 (8 articles)
```

### 发布流程

```bash
# 1. 生成文章（由自动化脚本完成）

# 2. 运行校验
python -X utf8 scripts/frontmatter_validator.py

# 3. 如有问题，自动修复
python -X utf8 scripts/frontmatter_validator.py --fix

# 4. Git 提交
git add -A
git commit -m "content: auto publish articles 2026-05-22 08:00 (8 articles)"

# 5. 推送（Windows PowerShell 使用 -X utf8 避免编码问题）
python -X utf8 -c "import subprocess; subprocess.run(['git', 'push', 'origin', 'main'])"

# 6. 验证部署
# 等待 Vercel 部署完成 → 确认首页 + 文章页正常访问
```

### 已知问题

- **GitHub 网络不稳定**：push 常失败，需多次重试。建议 commit 成功后隔一段时间再 push，或网络稳定后手动推送。
- **Windows 编码问题**：运行 Python 脚本务必加 `-X utf8`，否则中文路径或输出会乱码。

---

## 关键词策略

### 四级优先级

| 等级 | 含义 | 策略 | 当前状态 |
|------|------|------|----------|
| P0 | 核心词（搜索量大、竞争强） | 必须覆盖，优先生成 | ✅ 全部已覆盖 |
| P1 | 高价值（搜索量中等、转化高） | 重点覆盖 | ✅ 全部已覆盖 |
| P2 | 中价值（长尾词、细分需求） | 常规覆盖 | ✅ 全部已覆盖 |
| P3 | 长尾（问题型、对比型） | 灵活创作 | ✅ 全部已覆盖 |

### 角度轮换策略

P0-P3 已全部覆盖后，通过**多维度角度轮换**对同一关键词生成差异化文章：

| 维度 | 变体示例 |
|------|---------|
| 地域 | 上海/北京/广州/深圳/杭州/成都/武汉... |
| 年份 | 2024年/2025年/2026年/最新 |
| 人群 | 零基础/大专/非专业/宝妈/应届生/社会人员 |
| 场景 | 一次通过/高分技巧/速成/系统备考/冲刺 |
| 科目 | 行测/申论/公基/面试/笔试 |
| 问题 | 怎么准备/用什么书/要多久/难不难/有前途吗 |

### 关键词池管理

关键词池文件：`scripts/keywords_pool.md`（1200+ 行）

```yaml
- keyword: 社区工作者招聘
  priority: P0
  type: info
  covered: true
  note: 核心流量词
  angles: [2026年最新, 各地汇总, 报名人数统计, 招聘条件变化]
```

---

## 收录监控

### 收录率参考

| 搜索引擎 | 收录率 | 说明 |
|---------|--------|------|
| Sitemap | ~100% | 部署成功即收录 |
| Bing | ~80-100% | 收录较快，是主要参考 |
| Google | ~33% | 国内网络受限，实际可能更高 |
| 百度 | ~11% | 反爬拦截严重，数据不准 |

### 优化目标

完成以下操作后，目标收录率提升至 60%+：

1. **提交 sitemap**：登录 [百度搜索资源平台](https://ziyuan.baidu.com) 和 [Google Search Console](https://search.google.com/search-console) 提交 sitemap
2. **主动推送 API**：申请百度主动推送 Token，每次发布后主动提交新URL
3. **外链建设**：知乎/微信公众号等平台分发内容摘要并附原文链接

---

## 常见问题与踩坑

### 🔴 YAML 引号问题

**现象**：Vercel 部署失败，`gray-matter` 解析错误  
**原因**：description 中包含英文双引号 "  
**解决**：将内嵌双引号替换为日文直角引号「」  
**预防**：每次发布前运行 `python -X utf8 scripts/frontmatter_validator.py --fix`

### 🔴 date 字段显示异常

**现象**：前端文章日期显示为一个长数字（时间戳）  
**原因**：date 字段未加引号，YAML 解析为 Date 对象  
**解决**：`date: "2026-05-19"` 必须加引号

### 🔴 分类错误导致 404

**现象**：事业单位相关文章页面 404  
**原因**：使用了 `shiye-dan-wei` / `shiyedanwei` 等非法分类  
**解决**：事业单位内容统一使用 `gangwei-fenxi` 分类

### 🟡 GitHub push 失败

**现象**：`git push` 超时或连接拒绝  
**原因**：国内网络到 GitHub 不稳定  
**解决**：commit 成功后多次重试 push；或配置 SSH 密钥替代 HTTPS；或使用代理

### 🟡 Windows 编码乱码

**现象**：PowerShell 中 Python 脚本输出中文乱码  
**原因**：Windows 默认使用 GBK 编码  
**解决**：始终使用 `python -X utf8 scripts/xxx.py` 运行脚本

### 🟡 百度反爬拦截

**现象**：收录检查脚本显示百度 `⚠️` 无法判断  
**原因**：百度对自动化查询有极强的反爬验证  
**解决**：手动在浏览器搜索 `site:gk.edu-sjtu.cn` 二次确认；建议尽快开通百度搜索资源平台

### 🟡 图片重复使用

**现象**：同一张图片在多篇文章中频繁出现  
**原因**：未正确更新 `image_usage_log.json`  
**解决**：使用 `image_picker.py --update` 确保每次选取后标记使用记录

---

## 待办事项

| 优先级 | 任务 | 状态 |
|--------|------|------|
| 🔴 高 | 登录百度搜索资源平台，提交 sitemap | ⏳ |
| 🔴 高 | 登录 Google Search Console，提交 sitemap | ⏳ |
| 🔴 高 | 申请百度主动推送 API Token | ⏳ |
| 🟡 中 | 为高风险文章（含招聘人数/薪资数据）添加免责声明 | 📋 |
| 🟡 中 | 修复自动化任务中图片配图缺失问题 | 📋 |
| 🟡 中 | 扩充国考/省考/事业单位关键词池 | 📋 |
| 🟢 低 | GitHub 网络稳定性优化（SSH密钥替代HTTPS） | 📋 |
| 🟢 低 | Vercel 部署失败自动通知机制 | 📋 |

---

## 技术参考

- [Next.js 文档](https://nextjs.org/docs)
- [Vercel 部署文档](https://vercel.com/docs)
- [Pexels API](https://www.pexels.com/api/)
- [百度搜索资源平台](https://ziyuan.baidu.com)
- [Google Search Console](https://search.google.com/search-console)
- [Schema.org Article](https://schema.org/Article)

---

> **注意**：本站仅用于学习交流，不构成报考建议。具体考试信息以官方公告为准。

> **版权**：蜀ICP备2024012345号-1
