# 🏛️ 公考SEO网站 - 从零复刻指南

> **目标**：无论你是什么技术背景，跟着这份指南一步步操作，就能搭建出一个完全一样的公考SEO内容网站。

**复刻结果预览**：Next.js 16 SSG 网站，Markdown 内容驱动，Vercel 自动部署，日均产出 50-100 篇 AI 文章，全自动化流水线。

⏱️ **预计耗时**：首次搭建约 2-4 小时（不含 AI 文章生成时间）

---

## 目录

1. [成品预览：你将得到什么](#1-成品预览你将得到什么)
2. [准备工作：安装工具](#2-准备工作安装工具)
3. [创建 Next.js 项目骨架](#3-创建-nextjs-项目骨架)
4. [安装所有依赖包](#4-安装所有依赖包)
5. [配置文件——项目的"地基"](#5-配置文件项目的"地基")
6. [创建 TypeScript 类型定义](#6-创建-typescript-类型定义)
7. [创建核心数据层 content.ts](#7-创建核心数据层-contentts)
8. [创建全局样式 globals.css](#8-创建全局样式-globalscss)
9. [创建全局布局 layout.tsx](#9-创建全局布局-layouttsx)
10. [创建首页 page.tsx](#10-创建首页-pagetsx)
11. [创建分类列表页 [category]/page.tsx](#11-创建分类列表页-categorypagetsx)
12. [创建文章详情页 [category]/[slug]/page.tsx](#12-创建文章详情页-categoryslugpagetsx)
13. [创建 404 页面](#13-创建-404-页面)
14. [创建 sitemap 和 robots](#14-创建-sitemap-和-robots)
15. [创建公共组件](#15-创建公共组件)
16. [创建内容目录与文章规范](#16-创建内容目录与文章规范)
17. [创建图片库](#17-创建图片库)
18. [创建 Python 自动化脚本](#18-创建-python-自动化脚本)
19. [Git 仓库初始化和推送](#19-git-仓库初始化和推送)
20. [Vercel 部署与绑定域名](#20-vercel-部署与绑定域名)
21. [SEO 高级优化（收录、站长平台）](#21-seo-高级优化收录站长平台)
22. [设置自动化定时任务](#22-设置自动化定时任务)
23. [日常运维与监控](#23-日常运维与监控)
24. [踩坑经验总汇](#24-踩坑经验总汇)

---

## 1. 成品预览：你将得到什么

### 技术架构

```
前端框架：  Next.js 16 (App Router)
语言：      TypeScript + React 19
样式：      TailwindCSS 4
内容存储：  Markdown (.md) + YAML Frontmatter
数据解析：  gray-matter
部署：      Vercel（连接 GitHub 自动部署）
域名：      gk.edu-sjtu.cn（你需要自己买域名）
脚本语言：  Python 3（自动化文章生成）
图片来源：  Pexels API → 本地 /images/lib/
监控：      百度统计 + 百度自动推送 + 收录检查脚本
```

### 网站结构

```
首页 (/)
  ├── 国考 (/guokao)                     → 117+ 篇
  ├── 省考 (/shengkao)                   → 120+ 篇
  ├── 上海社区工作者 (/shanghai-shegong)  → 252+ 篇
  ├── 报考公告 (/baokao-gonggao)          → 70+ 篇
  ├── 政策解读 (/zhengce-jiedu)           → 107+ 篇
  ├── 备考指南 (/beikao-zhinan)           → 126+ 篇
  ├── 真题解析 (/zhenti-jiexi)            → 59+ 篇
  ├── 岗位分析 (/gangwei-fenxi)           → 83+ 篇
  └── 上岸经验 (/shang-an-jingyan)        → 42+ 篇
```

### 自动化流水线

```
关键词池 → AI生成文章(8篇/批) → 图片配图 → Frontmatter校验
                                              ↓
                                       git add/commit/push
                                              ↓
                                      Vercel 自动部署
                                              ↓
                                    百度自动推送(push.js)
                                              ↓
                                    次日收录检查(四维度)
```

### 内容比例（每批次 8 篇）

| 类别 | 篇数 | 占比 |
|------|------|------|
| 上海社工 | 2 | 25% |
| 国考 | 2 | 25% |
| 省考 | 2 | 25% |
| 事业单位 | 1 | 12.5% |
| 通用备考 | 1 | 12.5% |

---

## 2. 准备工作：安装工具

### 必须安装的软件

| 软件 | 最低版本 | 下载地址 | 用途 |
|------|---------|----------|------|
| Node.js | 18.x+ | https://nodejs.org | 前端构建 |
| Python | 3.8+ | https://python.org | 自动化脚本 |
| Git | 任意版 | https://git-scm.com | 版本控制 |
| VS Code | 任意版 | https://code.visualstudio.com | 代码编辑 |

### 必须注册的账号

| 账号 | 地址 | 用途 |
|------|------|------|
| GitHub | https://github.com | 代码仓库 |
| Vercel | https://vercel.com | 网站托管（用 GitHub 账号登录） |
| Pexels | https://www.pexels.com/api | 获取免费图片 API Key |
| 百度统计 | https://tongji.baidu.com | 网站流量统计 |
| 百度搜索资源平台 | https://ziyuan.baidu.com | 提交 sitemap |
| Google Search Console | https://search.google.com/search-console | 提交 sitemap |

### 验证安装

打开终端（PowerShell），依次运行：

```powershell
node --version    # 应输出 v18.x.x 或更高
npm --version     # 应输出 9.x.x 或更高
python --version  # 应输出 3.8.x 或更高
git --version     # 应输出 git version 2.x.x
```

---

## 3. 创建 Next.js 项目骨架

在你想存放项目的目录下打开终端，运行：

```powershell
# 创建 Next.js 项目（选择 TypeScript + TailwindCSS + App Router + src/）
npx create-next-app@latest gongkao-seo
```

交互式选项（按如下选择）：

```
✔ Would you like to use TypeScript? → Yes
✔ Would you like to use ESLint? → Yes
✔ Would you like to use Tailwind CSS? → Yes
✔ Would you like to use `src/` directory? → Yes
✔ Would you like to use App Router? → Yes
✔ Would you like to customize the default import alias (@/*)? → No
```

```powershell
# 进入项目目录
cd gongkao-seo

# 用 VS Code 打开
code .
```

---

## 4. 安装所有依赖包

在项目根目录运行：

```powershell
npm install gray-matter reading-time @mdx-js/loader @mdx-js/react @next/mdx
npm install -D @tailwindcss/postcss @types/node @types/react @types/react-dom typescript tailwindcss
```

### 依赖说明

| 包名 | 作用 |
|------|------|
| `gray-matter` | 解析 Markdown 文件的 YAML frontmatter |
| `reading-time` | 计算文章阅读时长 |
| `@mdx-js/loader` | MDX 文件加载器 |
| `@mdx-js/react` | MDX React 组件支持 |
| `@next/mdx` | Next.js 官方 MDX 插件 |
| `tailwindcss` | CSS 框架 |
| `@tailwindcss/postcss` | TailwindCSS PostCSS 插件 |

**注意**：这是 **TailwindCSS v4** 版本，不再需要 `tailwind.config.ts` 文件，所有配置在 CSS 文件中完成。

---

## 5. 配置文件——项目的"地基"

### 5.1 `package.json` — 项目元数据

项目根目录已有的 `package.json` 需要确认 `scripts` 部分：

```json
{
  "name": "gongkao-seo",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint"
  },
  "dependencies": {
    "@mdx-js/loader": "^3.1.1",
    "@mdx-js/react": "^3.1.1",
    "@next/mdx": "^16.2.4",
    "gray-matter": "^4.0.3",
    "next": "16.2.4",
    "react": "19.2.4",
    "react-dom": "19.2.4",
    "reading-time": "^1.5.0"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "eslint": "^9",
    "eslint-config-next": "16.2.4",
    "tailwindcss": "^4",
    "typescript": "^5"
  }
}
```

### 5.2 `next.config.ts` — Next.js 配置

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  pageExtensions: ["ts", "tsx", "md", "mdx"],
  images: {
    formats: ["image/avif", "image/webp"],
  },
  // 图片缓存策略：1年不变，提升加载速度
  async headers() {
    return [
      {
        source: "/images/:path*",
        headers: [
          { key: "Cache-Control", value: "public, max-age=31536000, immutable" },
        ],
      },
    ];
  },
};

export default nextConfig;
```

> **关键**：`pageExtensions` 包含了 `.md` 和 `.mdx`，这不是用来做动态页面的，而是为了让 Next.js 能够处理 Markdown 文件作为页面（如果放在 `app/` 下）。我们实际上在 `src/lib/content.ts` 中手动读取 `.md` 文件。

### 5.3 `tsconfig.json` — TypeScript 配置

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### 5.4 `postcss.config.mjs` — PostCSS 配置

```javascript
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
```

---

## 6. 创建 TypeScript 类型定义

创建文件 `src/lib/types.ts`（如果 `src/lib/` 目录不存在，先创建该目录）：

```typescript
export interface ArticleMeta {
  title: string;
  description: string;
  date: string;
  category: string;
  tags: string[];
  slug: string;
  author?: string;
  coverImage?: string;
}

export interface ArticleData extends ArticleMeta {
  content: string;
  readingTime: string;
}

export interface CategoryInfo {
  name: string;
  slug: string;
  description: string;
  keywords: string[];
}
```

---

## 7. 创建核心数据层 `content.ts`

这是整个网站的心脏——所有文章数据的读取、解析、排序都在这里完成。

创建文件 `src/lib/content.ts`：

```typescript
import fs from "fs";
import path from "path";
import matter from "gray-matter";
import readingTime from "reading-time";
import type { ArticleMeta, ArticleData, CategoryInfo } from "./types";

const contentDir = path.join(process.cwd(), "content");

// 统一日期格式化：无论 date 是字符串还是 Date 对象，都输出 YYYY-MM-DD
function formatDate(date: unknown): string {
  if (!date) return "";
  if (typeof date === "string") {
    const match = date.match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (match) return `${match[1]}-${match[2]}-${match[3]}`;
    return date;
  }
  if (date instanceof Date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    return `${y}-${m}-${d}`;
  }
  return String(date);
}

// 频道分类配置（请根据你的网站主题修改）
export const categories: CategoryInfo[] = [
  {
    name: "国考",
    slug: "guokao",
    description: "国家公务员考试招录公告、职位表、政策解读与备考指南",
    keywords: ["国考", "国家公务员考试", "国考公告", "国考职位表", "国考时间"],
  },
  {
    name: "省考",
    slug: "shengkao",
    description: "各省市公务员考试信息汇总，含多省联考和独立省考",
    keywords: ["省考", "省考公告", "省考时间", "多省联考", "省考职位表"],
  },
  {
    name: "上海社区工作者",
    slug: "shanghai-shegong",
    description: "上海社区工作者招聘公告、考试信息、政策待遇与备考资料",
    keywords: ["上海社区工作者", "上海社工", "上海社区工作者招聘", "上海社工考试"],
  },
  {
    name: "报考公告",
    slug: "baokao-gonggao",
    description: "各类公职考试报名公告、时间节点、岗位信息汇总",
    keywords: ["招考公告", "报名入口", "考试时间", "职位表", "报名条件"],
  },
  {
    name: "政策解读",
    slug: "zhengce-jiedu",
    description: "公务员考试政策变化、新规解读与趋势分析",
    keywords: ["政策解读", "考试政策", "报考条件", "新规变化"],
  },
  {
    name: "备考指南",
    slug: "beikao-zhinan",
    description: "行测、申论、面试备考方法、学习计划与复习攻略",
    keywords: ["备考指南", "行测", "申论", "面试", "复习计划"],
  },
  {
    name: "真题解析",
    slug: "zhenti-jiexi",
    description: "历年国考省考真题解析与答题技巧",
    keywords: ["真题", "真题解析", "历年真题", "真题答案"],
  },
  {
    name: "岗位分析",
    slug: "gangwei-fenxi",
    description: "热门岗位分析、薪资待遇对比、职业发展路径",
    keywords: ["岗位分析", "岗位待遇", "热门岗位", "报考指导"],
  },
  {
    name: "上岸经验",
    slug: "shang-an-jingyan",
    description: "公考上岸学员分享备考经验与心得",
    keywords: ["上岸经验", "备考心得", "经验分享", "高分经验"],
  },
];

// 获取所有文章的元数据
export function getAllArticles(): ArticleMeta[] {
  if (!fs.existsSync(contentDir)) return [];

  const articles: ArticleMeta[] = [];

  function walkDir(dir: string, category: string) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const fullPath = path.join(dir, file);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        walkDir(fullPath, category || file);
      } else if (file.endsWith(".mdx") || file.endsWith(".md")) {
        const fileContent = fs.readFileSync(fullPath, "utf-8");
        const { data } = matter(fileContent);
        if (data.title) {
          articles.push({
            title: data.title || "",
            description: data.description || "",
            date: formatDate(data.date),
            category: data.category || category || "",
            tags: data.tags || [],
            slug: file.replace(/\.(mdx|md)$/, ""),
            author: data.author || "公考资讯站",
            coverImage: data.coverImage || "",
          });
        }
      }
    }
  }

  walkDir(contentDir, "");

  // 按日期倒序排列
  articles.sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  return articles;
}

// 获取单篇文章完整数据
export function getArticleBySlug(
  slug: string,
  category?: string
): ArticleData | null {
  const searchDirs: string[] = [];
  if (category) {
    searchDirs.push(path.join(contentDir, category));
  }
  searchDirs.push(contentDir);

  for (const dir of searchDirs) {
    if (!fs.existsSync(dir)) continue;
    const files = fs.readdirSync(dir);
    for (const file of files) {
      if (file === `${slug}.mdx` || file === `${slug}.md`) {
        const fullPath = path.join(dir, file);
        const fileContent = fs.readFileSync(fullPath, "utf-8");
        const { data, content } = matter(fileContent);
        const time = readingTime(content);

        return {
          title: data.title || "",
          description: data.description || "",
          date: formatDate(data.date),
          category: data.category || category || "",
          tags: data.tags || [],
          slug,
          author: data.author || "公考资讯站",
          coverImage: data.coverImage || "",
          content,
          readingTime: time.text,
        };
      }
    }
  }

  return null;
}

// 按分类获取文章
export function getArticlesByCategory(category: string): ArticleMeta[] {
  return getAllArticles().filter(
    (a) => a.category.toLowerCase() === category.toLowerCase()
  );
}

// 获取相关文章
export function getRelatedArticles(
  currentSlug: string,
  currentCategory: string,
  limit = 5
): ArticleMeta[] {
  return getAllArticles()
    .filter((a) => a.slug !== currentSlug && a.category === currentCategory)
    .slice(0, limit);
}

// 获取所有分类下的文章数量
export function getCategoryCount(): Record<string, number> {
  const articles = getAllArticles();
  const counts: Record<string, number> = {};
  for (const a of articles) {
    counts[a.category] = (counts[a.category] || 0) + 1;
  }
  return counts;
}
```

### `formatDate` 为什么重要？

YAML 中 `date: 2026-05-19`（没引号）会被解析为 JavaScript 的 Date 对象，而 `date: "2026-05-19"`（有引号）才是字符串。`formatDate` 函数统一处理两种情况，防止前端显示 `1716076800000`（Unix 时间戳）。

---

## 8. 创建全局样式 `globals.css`

清空并重写 `src/app/globals.css`：

```css
@import "tailwindcss";

/* 自定义变量 */
:root {
  --primary: #1e40af;
  --primary-light: #3b82f6;
  --primary-dark: #1e3a8a;
  --accent: #dc2626;
  --text-primary: #111827;
  --text-secondary: #4b5563;
  --bg-light: #f9fafb;
  --border-color: #e5e7eb;
}

body {
  color: var(--text-primary);
  background: var(--bg-light);
}

/* Prose 样式（文章内容） */
.prose h1,
.prose h2,
.prose h3,
.prose h4 {
  color: var(--text-primary);
  font-weight: 700;
  margin-top: 2em;
  margin-bottom: 0.5em;
}

.prose h2 {
  font-size: 1.5rem;
  padding-bottom: 0.3rem;
  border-bottom: 2px solid var(--primary-light);
}

.prose h3 {
  font-size: 1.25rem;
}

.prose p {
  line-height: 1.8;
  margin-bottom: 1em;
}

.prose a {
  color: var(--primary);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.prose a:hover {
  color: var(--primary-dark);
}

.prose ul,
.prose ol {
  padding-left: 1.5rem;
  margin-bottom: 1em;
}

.prose li {
  margin-bottom: 0.3em;
  line-height: 1.8;
}

.prose blockquote {
  border-left: 4px solid var(--primary-light);
  padding-left: 1rem;
  margin: 1.5em 0;
  background: #eff6ff;
  padding: 1rem 1.5rem;
  border-radius: 0 8px 8px 0;
}

.prose table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
}

.prose th,
.prose td {
  border: 1px solid var(--border-color);
  padding: 0.5rem 0.75rem;
  text-align: left;
}

.prose th {
  background: #f3f4f6;
  font-weight: 600;
}

.prose code {
  background: #f3f4f6;
  padding: 0.15em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
}

.prose img {
  border-radius: 8px;
  margin: 1.5em 0;
}
```

---

## 9. 创建全局布局 `layout.tsx`

清空并重写 `src/app/layout.tsx`：

> ⚠️ **重要**：以下代码中的 `YOUR_DOMAIN`、`YOUR_BAIDU_VERIFY_CODE`、`YOUR_GOOGLE_VERIFY_CODE`、`YOUR_BAIDU_HM_ID` 都需要替换为你自己的值。

```typescript
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Script from "next/script";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"], display: "swap" });

// ⚠️ 把 YOUR_DOMAIN 替换为你的实际域名
const SITE_URL = "https://YOUR_DOMAIN.com";
const SITE_NAME = "你的网站名称";
const SITE_DESC = "你的网站描述（120-160字，包含核心关键词）";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${SITE_NAME} - 网站副标题`,
    template: `%s | ${SITE_NAME}`,
  },
  description: SITE_DESC,
  keywords: ["关键词1", "关键词2", "关键词3", "关键词4", "关键词5"],
  openGraph: {
    type: "website",
    locale: "zh_CN",
    siteName: SITE_NAME,
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <head>
        {/* ⚠️ 替换为你的百度验证码 */}
        <meta name="baidu-site-verification" content="YOUR_BAIDU_VERIFY_CODE" />
        {/* ⚠️ 替换为你的 Google 验证码 */}
        <meta name="google-site-verification" content="YOUR_GOOGLE_VERIFY_CODE" />

        {/* Organization JSON-LD：品牌信号 */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Organization",
              name: SITE_NAME,
              url: SITE_URL,
              logo: `${SITE_URL}/og-cover.svg`,
              description: SITE_DESC,
              sameAs: [],
              contactPoint: {
                "@type": "ContactPage",
                availableLanguage: "Chinese",
              },
            }),
          }}
        />

        {/* WebSite JSON-LD：配合搜索框，触发 Google 即时答案框 */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebSite",
              name: SITE_NAME,
              url: SITE_URL,
              description: SITE_DESC,
              potentialAction: {
                "@type": "SearchAction",
                target: {
                  "@type": "EntryPoint",
                  urlTemplate: `${SITE_URL}/search?q={search_term_string}`,
                },
                "query-input": "required name=search_term_string",
              },
              inLanguage: "zh-CN",
            }),
          }}
        />
      </head>
      <body className={`${inter.className} antialiased`}>
        <Header />
        <main className="min-h-screen bg-gray-50">{children}</main>
        <Footer />

        {/* 百度统计 — 去 https://tongji.baidu.com 申请后填入你的 hm.js ID */}
        <Script
          id="baidu-tongji"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              var _hmt = _hmt || [];
              (function() {
                var hm = document.createElement("script");
                hm.src = "https://hm.baidu.com/hm.js?YOUR_BAIDU_HM_ID";
                var s = document.getElementsByTagName("script")[0];
                s.parentNode.insertBefore(hm, s);
              })();
            `,
          }}
        />

        {/* 百度自动推送 — 不需要修改，所有网站通用 */}
        <Script
          id="baidu-push"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              (function(){
                var bp = document.createElement('script');
                var curProtocol = window.location.protocol.split(':')[0];
                if (curProtocol === 'https') {
                  bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
                } else {
                  bp.src = 'http://push.zhanzhang.baidu.com/push.js';
                }
                var s = document.getElementsByTagName("script")[0];
                s.parentNode.insertBefore(bp, s);
              })();
            `,
          }}
        />
      </body>
    </html>
  );
}
```

> **关于百度统计和验证码的获取**，详见 [第 21 节](#21-seo-高级优化收录站长平台)。

---

## 10. 创建首页 `page.tsx`

清空并重写 `src/app/page.tsx`：

```typescript
import Link from "next/link";
import type { Metadata } from "next";
import { getAllArticles, categories, getCategoryCount } from "@/lib/content";

const SITE_URL = "https://YOUR_DOMAIN.com";
const SITE_NAME = "你的网站名称";

export const metadata: Metadata = {
  alternates: {
    canonical: SITE_URL,
  },
  openGraph: {
    title: `${SITE_NAME} - 网站副标题`,
    description: "你的网站描述",
    url: SITE_URL,
    siteName: SITE_NAME,
    locale: "zh_CN",
    type: "website",
    images: [{ url: "/og-cover.svg", width: 1200, height: 630, alt: SITE_NAME }],
  },
  twitter: {
    card: "summary_large_image",
    title: `${SITE_NAME} - 网站副标题`,
    description: "你的网站描述",
    images: ["/og-cover.svg"],
  },
};

// 热搜关键词 → 指向真实分类/内容页（根据你的网站主题修改）
const hotKeywords = [
  { label: "关键词1", href: "/category-slug" },
  { label: "关键词2", href: "/category-slug" },
  { label: "关键词3", href: "/category-slug" },
  { label: "关键词4", href: "/category-slug" },
  { label: "关键词5", href: "/category-slug" },
  { label: "关键词6", href: "/category-slug" },
  { label: "关键词7", href: "/category-slug" },
  { label: "关键词8", href: "/category-slug" },
  { label: "关键词9", href: "/category-slug" },
  { label: "关键词10", href: "/category-slug" },
  { label: "关键词11", href: "/category-slug" },
  { label: "关键词12", href: "/category-slug" },
];

export default function HomePage() {
  const allArticles = getAllArticles();
  const categoryCounts = getCategoryCount();
  const latestArticles = allArticles.slice(0, 8);

  return (
    <>
      {/* Hero 区域 */}
      <section className="bg-gradient-to-br from-blue-800 via-blue-700 to-indigo-800 text-white">
        <div className="max-w-6xl mx-auto px-4 py-16 md:py-24">
          <h1 className="text-3xl md:text-5xl font-bold mb-4">
            🏛️ {SITE_NAME}
          </h1>
          <p className="text-lg md:text-xl text-blue-100 mb-8 max-w-2xl">
            你的网站介绍，建议包含核心关键词。
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/category-slug-1"
              className="bg-white text-blue-800 px-6 py-3 rounded-lg font-medium hover:bg-blue-50 transition"
            >
              📢 按钮1
            </Link>
            <Link
              href="/category-slug-2"
              className="border border-white/30 text-white px-6 py-3 rounded-lg font-medium hover:bg-white/10 transition"
            >
              📚 按钮2
            </Link>
          </div>
        </div>
      </section>

      {/* 频道分类 */}
      <section className="max-w-6xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">📂 内容频道</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map((cat) => (
            <Link
              key={cat.slug}
              href={`/${cat.slug}`}
              className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md hover:border-blue-200 transition-all group"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-700">
                  {cat.name}
                </h3>
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                  {categoryCounts[cat.slug] || 0} 篇
                </span>
              </div>
              <p className="text-sm text-gray-500">{cat.description}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* 最新文章 */}
      <section className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">📰 最新内容</h2>
          <Link href="/category-slug" className="text-sm text-blue-600 hover:text-blue-800">
            查看全部 →
          </Link>
        </div>
        {latestArticles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {latestArticles.map((article, idx) => (
              <Link
                key={article.slug}
                href={`/${article.category}/${article.slug}`}
                className={`bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all ${
                  idx === 0 ? "md:col-span-2 md:flex md:gap-6" : ""
                }`}
              >
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-medium">
                      {categories.find((c) => c.slug === article.category)?.name || article.category}
                    </span>
                    <span className="text-xs text-gray-400">{article.date}</span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">
                    {article.title}
                  </h3>
                  <p className="text-sm text-gray-500 line-clamp-2">
                    {article.description}
                  </p>
                  {article.tags.length > 0 && (
                    <div className="flex gap-1 mt-3 flex-wrap">
                      {article.tags.slice(0, 3).map((tag) => (
                        <span key={tag} className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded">
                          #{tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-xl p-12 text-center border border-gray-100">
            <p className="text-4xl mb-4">📝</p>
            <p className="text-gray-500">网站正在建设中，敬请期待...</p>
          </div>
        )}
      </section>

      {/* SEO 内容区 - 关键词聚合 */}
      <section className="bg-white border-t border-gray-100">
        <div className="max-w-6xl mx-auto px-4 py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">🔍 热门搜索</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {hotKeywords.map((kw) => (
              <Link
                key={kw.label}
                href={kw.href}
                className="text-sm text-gray-600 bg-gray-50 hover:bg-blue-50 hover:text-blue-700 px-3 py-2 rounded-lg transition"
              >
                🔎 {kw.label}
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
```

---

## 11. 创建分类列表页 `[category]/page.tsx`

创建 `src/app/[category]/page.tsx`：

```typescript
import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { categories, getArticlesByCategory } from "@/lib/content";
import { Breadcrumbs } from "@/components/ui/Breadcrumbs";
import { ArticleCard } from "@/components/ui/ArticleCard";

const SITE_URL = "https://YOUR_DOMAIN.com";

interface PageProps {
  params: Promise<{ category: string }>;
}

// 生成所有分类的静态路径
export async function generateStaticParams() {
  return categories.map((cat) => ({ category: cat.slug }));
}

// 动态生成 metadata
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { category } = await params;
  const cat = categories.find((c) => c.slug === category);
  if (!cat) return {};

  const canonicalUrl = `${SITE_URL}/${category}`;

  return {
    title: `${cat.name} - ${cat.description}`,
    description: cat.description,
    keywords: cat.keywords,
    alternates: { canonical: canonicalUrl },
    openGraph: {
      title: `${cat.name} | ${SITE_URL.replace("https://", "")}`,
      description: cat.description,
      url: canonicalUrl,
      siteName: SITE_URL.replace("https://", ""),
      locale: "zh_CN",
      type: "website",
      images: [{ url: "/og-cover.svg", width: 1200, height: 630, alt: cat.name }],
    },
    twitter: {
      card: "summary_large_image",
      title: `${cat.name} | ${SITE_URL.replace("https://", "")}`,
      description: cat.description,
      images: ["/og-cover.svg"],
    },
  };
}

export default async function CategoryPage({ params }: PageProps) {
  const { category } = await params;
  const cat = categories.find((c) => c.slug === category);

  if (!cat) notFound();

  const articles = getArticlesByCategory(category);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <Breadcrumbs items={[{ label: cat.name }]} />

      {/* 分类头部 */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{cat.name}</h1>
        <p className="text-gray-500">{cat.description}</p>
        <div className="flex gap-2 mt-4 flex-wrap">
          {cat.keywords.map((kw) => (
            <span key={kw} className="text-xs bg-blue-50 text-blue-600 px-3 py-1 rounded-full">
              {kw}
            </span>
          ))}
        </div>
      </div>

      {/* 文章列表 */}
      {articles.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {articles.map((article) => (
            <ArticleCard key={article.slug} article={article} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-xl p-12 text-center border border-gray-100">
          <p className="text-4xl mb-4">📝</p>
          <p className="text-gray-500">该分类暂无文章</p>
          <Link href="/" className="inline-block mt-4 text-blue-600 hover:text-blue-800 text-sm">
            ← 返回首页
          </Link>
        </div>
      )}
    </div>
  );
}
```

---

## 12. 创建文章详情页 `[category]/[slug]/page.tsx`

创建 `src/app/[category]/[slug]/page.tsx`。这是最复杂的页面，包含 **SSG 静态生成**、**动态 SEO 元数据**、**JSON-LD 结构化数据**、**自定义 Markdown 渲染**。

```typescript
import { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { categories, getArticleBySlug, getRelatedArticles, getAllArticles } from "@/lib/content";
import { Breadcrumbs } from "@/components/ui/Breadcrumbs";

const SITE_URL = "https://YOUR_DOMAIN.com";
const SITE_NAME = "你的网站名称";

interface PageProps {
  params: Promise<{ category: string; slug: string }>;
}

// 预生成所有文章路径 → SSG
export async function generateStaticParams() {
  const articles = getAllArticles();
  return articles.map((article) => ({
    category: article.category,
    slug: article.slug,
  }));
}

// 动态生成 metadata
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { category, slug } = await params;
  const article = getArticleBySlug(slug, category);
  if (!article) return {};

  const canonicalUrl = `${SITE_URL}/${category}/${slug}`;

  return {
    title: article.title,
    description: article.description,
    keywords: article.tags,
    alternates: { canonical: canonicalUrl },
    openGraph: {
      title: article.title,
      description: article.description,
      type: "article",
      url: canonicalUrl,
      publishedTime: article.date,
      authors: [article.author || SITE_NAME],
      siteName: SITE_NAME,
      images: [{ url: "/og-cover.svg", width: 1200, height: 630, alt: article.title }],
    },
    twitter: {
      card: "summary_large_image",
      title: article.title,
      description: article.description,
      images: ["/og-cover.svg"],
    },
  };
}

export default async function ArticlePage({ params }: PageProps) {
  const { category, slug } = await params;
  const article = getArticleBySlug(slug, category);

  if (!article) notFound();

  const cat = categories.find((c) => c.slug === article.category);
  const relatedArticles = getRelatedArticles(slug, article.category, 4);
  const canonicalUrl = `${SITE_URL}/${category}/${slug}`;

  // Article JSON-LD 结构化数据
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: article.title,
    description: article.description,
    datePublished: article.date,
    dateModified: article.date,
    author: { "@type": "Person", name: article.author || SITE_NAME },
    publisher: { "@type": "Organization", name: SITE_NAME, url: SITE_URL },
    mainEntityOfPage: { "@type": "WebPage", "@id": canonicalUrl },
    keywords: article.tags.join(", "),
    articleSection: cat?.name || article.category,
    inLanguage: "zh-CN",
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Article JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <Breadcrumbs
        items={[
          { label: cat?.name || article.category, href: `/${article.category}` },
          { label: article.title },
        ]}
      />

      {/* 文章头部 */}
      <article>
        <header className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
              {cat?.name || article.category}
            </span>
            <time className="text-sm text-gray-400">{article.date}</time>
            <span className="text-sm text-gray-400">{article.readingTime}</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4 leading-tight">
            {article.title}
          </h1>
          <p className="text-lg text-gray-500">{article.description}</p>
          {article.tags.length > 0 && (
            <div className="flex gap-2 mt-4 flex-wrap">
              {article.tags.map((tag) => (
                <span key={tag} className="text-sm bg-gray-100 text-gray-500 px-3 py-1 rounded-full">
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </header>

        {/* 文章内容（Markdown → HTML） */}
        <div
          className="prose max-w-none"
          dangerouslySetInnerHTML={{
            __html: renderMarkdownToHtml(article.content),
          }}
        />

        {/* 底部信息 */}
        <footer className="mt-12 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-400">
              作者：{article.author} | 发布：{article.date}
            </p>
            <Link href={`/${article.category}`} className="text-sm text-blue-600 hover:text-blue-800">
              ← 返回{cat?.name || article.category}
            </Link>
          </div>
        </footer>
      </article>

      {/* 相关文章 */}
      {relatedArticles.length > 0 && (
        <aside className="mt-12">
          <h2 className="text-xl font-bold text-gray-900 mb-4">📖 相关推荐</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {relatedArticles.map((rel) => (
              <Link
                key={rel.slug}
                href={`/${rel.category}/${rel.slug}`}
                className="bg-white p-4 rounded-lg border border-gray-100 hover:shadow-sm transition"
              >
                <h3 className="font-medium text-gray-900 text-sm line-clamp-2 mb-1">
                  {rel.title}
                </h3>
                <p className="text-xs text-gray-400">{rel.date}</p>
              </Link>
            ))}
          </div>
        </aside>
      )}
    </div>
  );
}

// ─── 自定义 Markdown → HTML 渲染器 ───
// 支持：h1-h3、图片、链接、粗体斜体、无序/有序列表、引用、表格
function renderMarkdownToHtml(markdown: string): string {
  const lines = markdown.split('\n');
  const result: string[] = [];
  let inUl = false;
  let inOl = false;
  let inTable = false;
  let tableHeaderParsed = false;

  const closeOpenBlocks = () => {
    if (inUl) { result.push('</ul>'); inUl = false; }
    if (inOl) { result.push('</ol>'); inOl = false; }
    if (inTable) { result.push('</tbody></table>'); inTable = false; tableHeaderParsed = false; }
  };

  for (const line of lines) {
    const trimmed = line.trim();

    // 标题
    if (/^### /.test(trimmed)) {
      closeOpenBlocks();
      result.push(`<h3>${processInline(trimmed.slice(4))}</h3>`);
    } else if (/^## /.test(trimmed)) {
      closeOpenBlocks();
      result.push(`<h2>${processInline(trimmed.slice(3))}</h2>`);
    } else if (/^# /.test(trimmed)) {
      closeOpenBlocks();
      result.push(`<h1>${processInline(trimmed.slice(2))}</h1>`);
    }
    // 引用
    else if (/^> /.test(trimmed)) {
      closeOpenBlocks();
      result.push(`<blockquote>${processInline(trimmed.slice(2))}</blockquote>`);
    }
    // 表格
    else if (/^\|/.test(trimmed)) {
      if (!inTable) {
        result.push('<table><thead>');
        inTable = true;
        tableHeaderParsed = false;
      }
      if (/^\|[\s\-|:]+\|$/.test(trimmed)) {
        result.push('</thead><tbody>');
        tableHeaderParsed = true;
      } else {
        const cells = trimmed.replace(/^\||\|$/g, '').split('|').map(c => c.trim());
        const tag = tableHeaderParsed ? 'td' : 'th';
        result.push(`<tr>${cells.map(c => `<${tag}>${processInline(c)}</${tag}>`).join('')}</tr>`);
      }
    }
    // 无序列表
    else if (/^[-*] /.test(trimmed)) {
      if (inOl) { result.push('</ol>'); inOl = false; }
      if (inTable) { result.push('</tbody></table>'); inTable = false; tableHeaderParsed = false; }
      if (!inUl) { result.push('<ul>'); inUl = true; }
      result.push(`<li>${processInline(trimmed.slice(2))}</li>`);
    }
    // 有序列表
    else if (/^\d+\. /.test(trimmed)) {
      if (inUl) { result.push('</ul>'); inUl = false; }
      if (inTable) { result.push('</tbody></table>'); inTable = false; tableHeaderParsed = false; }
      if (!inOl) { result.push('<ol>'); inOl = true; }
      result.push(`<li>${processInline(trimmed.replace(/^\d+\. /, ''))}</li>`);
    }
    // 空行
    else if (trimmed === '') {
      closeOpenBlocks();
    }
    // 普通段落
    else {
      closeOpenBlocks();
      result.push(`<p>${processInline(trimmed)}</p>`);
    }
  }

  closeOpenBlocks();
  return result.join('\n');
}

function processInline(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" />')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
}
```

> **关于 Markdown 渲染器**：我们没有用第三方 Markdown 解析器，而是手写了这个轻量渲染器。它只支持网站内容中用到的语法，避免了引入大型库的体积开销。如果你的内容有更复杂的语法，可以考虑引入 `react-markdown` 或 `marked`。

---

## 13. 创建 404 页面

修改或创建 `src/app/not-found.tsx`：

```typescript
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-24 text-center">
      <p className="text-6xl mb-4">🔍</p>
      <h1 className="text-3xl font-bold text-gray-900 mb-4">页面未找到</h1>
      <p className="text-gray-500 mb-8">您访问的页面不存在或已被移除。</p>
      <Link href="/" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
        返回首页
      </Link>
    </div>
  );
}
```

---

## 14. 创建 sitemap 和 robots

### 14.1 `sitemap.ts` — 动态生成 sitemap.xml

修改 `src/app/sitemap.ts`：

```typescript
import { MetadataRoute } from "next";
import { getAllArticles, categories } from "@/lib/content";

const SITE_URL = "https://YOUR_DOMAIN.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  // 静态页面
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: SITE_URL,
      lastModified: now,
      changeFrequency: "daily",
      priority: 1.0,
    },
    ...categories.map((cat) => ({
      url: `${SITE_URL}/${cat.slug}`,
      lastModified: now,
      changeFrequency: "daily" as const,
      priority: 0.8,
    })),
  ];

  // 动态文章页
  const articles = getAllArticles();
  const articlePages: MetadataRoute.Sitemap = articles.map((article) => ({
    url: `${SITE_URL}/${article.category}/${article.slug}`,
    lastModified: new Date(article.date),
    changeFrequency: "weekly" as const,
    priority: 0.6,
  }));

  return [...staticPages, ...articlePages];
}
```

### 14.2 `robots.ts` — robots.txt

修改 `src/app/robots.ts`：

```typescript
import { MetadataRoute } from "next";

const SITE_URL = "https://YOUR_DOMAIN.com";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/api/", "/admin/"],
    },
    sitemap: `${SITE_URL}/sitemap.xml`,
  };
}
```

---

## 15. 创建公共组件

### 15.1 目录结构

在 `src/components/` 下创建如下目录和文件：

```
src/components/
├── layout/
│   ├── Header.tsx
│   └── Footer.tsx
└── ui/
    ├── ArticleCard.tsx
    └── Breadcrumbs.tsx
```

### 15.2 `Header.tsx`

```typescript
import Link from "next/link";

// 根据你的分类修改导航项
const navItems = [
  { name: "分类1", href: "/slug1" },
  { name: "分类2", href: "/slug2" },
  { name: "分类3", href: "/slug3" },
  { name: "分类4", href: "/slug4" },
  { name: "分类5", href: "/slug5" },
  { name: "分类6", href: "/slug6" },
  { name: "分类7", href: "/slug7" },
];

export function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 shrink-0">
            <span className="text-2xl">🏛️</span>
            <span className="text-xl font-bold text-blue-800 hidden sm:inline">
              网站名称
            </span>
          </Link>

          {/* 导航 */}
          <nav className="flex items-center gap-1 overflow-x-auto">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors whitespace-nowrap"
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
```

### 15.3 `Footer.tsx`

```typescript
import Link from "next/link";

const footerLinks = {
  "栏目1": [
    { name: "链接1", href: "/slug1" },
    { name: "链接2", href: "/slug2" },
    { name: "链接3", href: "/slug3" },
  ],
  "栏目2": [
    { name: "链接4", href: "/slug4" },
    { name: "链接5", href: "/slug5" },
    { name: "链接6", href: "/slug6" },
    { name: "链接7", href: "/slug7" },
  ],
  "栏目3": [
    { name: "链接8", href: "/slug8" },
    { name: "链接9", href: "/slug9" },
  ],
};

export function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-16">
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {/* 品牌信息 */}
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <span className="text-2xl">🏛️</span>
              <span className="text-lg font-bold text-white">网站名称</span>
            </Link>
            <p className="text-sm text-gray-400 leading-relaxed">
              你的网站简介。
            </p>
          </div>

          {/* 链接区 */}
          {Object.entries(footerLinks).map(([title, links]) => (
            <div key={title}>
              <h3 className="text-white font-semibold mb-4">{title}</h3>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link.href}>
                    <Link href={link.href} className="text-sm text-gray-400 hover:text-white transition-colors">
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* 版权 */}
        <div className="border-t border-gray-800 mt-10 pt-6 text-center text-sm text-gray-500">
          <p>© {new Date().getFullYear()} 网站名称. 仅供学习交流，不构成报考建议。</p>
          {/* 如果你有 ICP 备案号 */}
          <p className="mt-2">ICP备XXXXXXXX号-1</p>
        </div>
      </div>
    </footer>
  );
}
```

### 15.4 `ArticleCard.tsx`

```typescript
import Link from "next/link";
import type { ArticleMeta } from "@/lib/types";
import { categories } from "@/lib/content";

export function ArticleCard({ article }: { article: ArticleMeta }) {
  const cat = categories.find((c) => c.slug === article.category);

  return (
    <Link
      href={`/${article.category}/${article.slug}`}
      className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md hover:border-blue-200 transition-all group block"
    >
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">
          {cat?.name || article.category}
        </span>
        <time className="text-xs text-gray-400">{article.date}</time>
      </div>
      <h3 className="font-semibold text-gray-900 mb-1 group-hover:text-blue-700 transition-colors line-clamp-2">
        {article.title}
      </h3>
      <p className="text-sm text-gray-500 line-clamp-2">{article.description}</p>
      {article.tags.length > 0 && (
        <div className="flex gap-1 mt-3 flex-wrap">
          {article.tags.slice(0, 3).map((tag) => (
            <span key={tag} className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded">
              #{tag}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}
```

### 15.5 `Breadcrumbs.tsx`

```typescript
import Link from "next/link";

interface BreadcrumbItem {
  label: string;
  href?: string;
}

export function Breadcrumbs({ items }: { items: BreadcrumbItem[] }) {
  return (
    <nav aria-label="面包屑" className="text-sm text-gray-500 mb-6">
      <ol className="flex items-center gap-1 flex-wrap" itemScope itemType="https://schema.org/BreadcrumbList">
        <li itemProp="itemListElement" itemScope itemType="https://schema.org/ListItem">
          <Link href="/" itemProp="item" className="hover:text-blue-600">
            <span itemProp="name">首页</span>
          </Link>
          <meta itemProp="position" content="1" />
        </li>
        {items.map((item, idx) => (
          <li
            key={idx}
            itemProp="itemListElement"
            itemScope
            itemType="https://schema.org/ListItem"
            className="flex items-center gap-1"
          >
            <span className="text-gray-300">/</span>
            {item.href ? (
              <Link href={item.href} itemProp="item" className="hover:text-blue-600">
                <span itemProp="name">{item.label}</span>
              </Link>
            ) : (
              <span itemProp="name" className="text-gray-700">{item.label}</span>
            )}
            <meta itemProp="position" content={String(idx + 2)} />
          </li>
        ))}
      </ol>
    </nav>
  );
}
```

---

## 16. 创建内容目录与文章规范

### 16.1 创建目录结构

在项目根目录创建 `content/` 文件夹，然后为每个分类创建子目录：

```powershell
mkdir content\guokao
mkdir content\shengkao
mkdir content\shanghai-shegong
mkdir content\baokao-gonggao
mkdir content\zhengce-jiedu
mkdir content\beikao-zhinan
mkdir content\zhenti-jiexi
mkdir content\gangwei-fenxi
mkdir content\shang-an-jingyan
```

### 16.2 文章格式规范

每篇 Markdown 文章必须以 YAML frontmatter 开头，格式如下：

```markdown
---
title: "文章标题（25字以内，必须包含核心关键词）"
description: "文章描述（100-160字，必须包含关键词，内嵌引号用「」代替"）"
date: "2026-05-24"
category: "guokao"
tags: ["标签1", "标签2", "标签3", "标签4"]
author: "作者名称"
---

# 文章标题

![](images/lib/study/example.jpg)

正文内容，Markdown 格式...

## 二级标题

正文内容...

### 三级标题

正文内容...

> 引用内容

| 表头1 | 表头2 |
|-------|-------|
| 数据1 | 数据2 |

- 无序列表项
- 无序列表项

1. 有序列表项
2. 有序列表项
```

#### ⚠️ 关键规范（非常重要！）

| 规范 | 错误示例 | 正确示例 |
|------|---------|---------|
| **date 必须加引号** | `date: 2026-05-24` | `date: "2026-05-24"` |
| **description 内嵌引号** | `description: "他问"这是什么""` | `description: "他问「这是什么」"` |
| **tags 必须是列表** | `tags: 标签1` | `tags: ["标签1", "标签2"]` |
| **date 不能是未来日期** | `date: "2027-01-01"` | 必须是今天或过去的日期 |
| **category 必须在9个白名单内** | `category: "shiyedanwei"` | `category: "gangwei-fenxi"` |

### 16.3 创建示例文章

创建 `content/guokao/2026-05-24-test-article.md` 用于测试：

```markdown
---
title: "2026年国考备考指南：从零开始系统备考"
description: "2026年国考即将来临，本文为考生提供从零基础到笔试上岸的完整备考指南，涵盖行测、申论学习方法与时间规划。"
date: "2026-05-24"
category: "guokao"
tags: ["国考备考", "行测", "申论", "公务员考试"]
author: "公考助手"
---

# 2026年国考备考指南：从零开始系统备考

国家公务员考试（国考）是我国规模最大的公务员选拔考试。2026年国考预计将在2025年10月发布公告，11月底举行笔试。如何科学备考是每个考生最关心的问题。

## 行测备考策略

行测（行政职业能力测验）是国考笔试的第一科，包含五大模块。

### 1. 言语理解与表达

这部分考察对文字材料的理解和表达能力。

- 每天练习20道言语理解题
- 重点积累常见成语和近义词辨析
- 掌握片段阅读的快速定位技巧

### 2. 数量关系

数量关系是拉开分差的关键模块。

1. 先掌握基础题型（工程问题、行程问题）
2. 再攻克进阶题型（排列组合、概率）
3. 最后练习限时套题

> 备考小贴士：行测考试时间紧张，不会的题目果断跳过，保证会的题全对。

## 申论写作技巧

申论是国考笔试的重头戏。

| 题型 | 分值 | 建议用时 |
|------|------|----------|
| 概括归纳 | 15分 | 20分钟 |
| 综合分析 | 20分 | 30分钟 |
| 提出对策 | 25分 | 35分钟 |
| 大作文 | 40分 | 65分钟 |

坚持每天阅读人民日报评论文章，积累规范表达。
```

---

## 17. 创建图片库

### 17.1 图片库架构

```
images/
└── lib/
    ├── study/       # 学习备考
    ├── exam/        # 考试上岸
    ├── career/      # 职场发展
    ├── city/        # 城市景观
    ├── motivation/  # 励志奋斗
    ├── books/       # 书籍资料
    ├── gov/         # 政府政务
    ├── office/      # 办公场景
    ├── people/      # 人物形象
    ├── tech/        # 科技数字
    ├── nature/      # 自然风景
    ├── writing/     # 笔记文档
    └── index.json   # 图片索引
```

### 17.2 获取图片的方式

#### 方式一：Pexels API 批量下载（推荐）

1. 注册 Pexels API：https://www.pexels.com/api/
2. 获取你的 API Key
3. 使用脚本下载（见第 18 节中的图片下载脚本）

#### 方式二：手动收集

从 Unsplash、Pixabay 等免费图库下载。注意：
- 图片宽度统一 1920px
- 格式为 JPEG 或 WebP
- 确保免费商用许可

### 17.3 创建图片索引

创建 `images/lib/index.json`：

```json
{
  "total": 0,
  "updated": "2026-05-24",
  "categories": {
    "study": {"name": "学习备考", "count": 0},
    "office": {"name": "政务职场", "count": 0},
    "books": {"name": "书籍资料", "count": 0},
    "exam": {"name": "考试上岸", "count": 0},
    "motivation": {"name": "励志奋斗", "count": 0},
    "gov": {"name": "政府城市", "count": 0},
    "tech": {"name": "科技数字", "count": 0},
    "city": {"name": "城市景观", "count": 0},
    "people": {"name": "职业人物", "count": 0},
    "nature": {"name": "自然风景", "count": 0},
    "writing": {"name": "写作文档", "count": 0}
  },
  "quality": {
    "width": 1920,
    "format": "JPEG",
    "source": "Unsplash + Pexels",
    "license": "免费商用"
  }
}
```

### 17.4 图片 URL 规范

文章中引用图片使用相对于项目根目录的路径：

```markdown
![](images/lib/study/example.jpg)
```

> Next.js 的 `public/` 目录在 SSG 时会自动映射，`images/` 应该放在 `public/` 目录下而不是项目根目录。你需要把 `images/` 文件夹放在 `public/images/` 下，或者配置 Next.js 映射它。

---

## 18. 创建 Python 自动化脚本

在项目根目录创建 `scripts/` 文件夹，存放所有 Python 自动化脚本。

### 18.1 `frontmatter_validator.py` — 核心质量校验

这是最重要的脚本，每次发布前必须运行。完整代码（378 行）较长，你可以在项目仓库中直接使用。

**关键功能**：
- 校验 6 个必填字段
- 检测 description 中的未转义引号
- 验证 date 格式和未来日期
- 验证 category 白名单
- `--fix` 自动修复模式

**使用方式**：
```powershell
# 检查全部文章
python -X utf8 scripts/frontmatter_validator.py

# 检查指定目录
python -X utf8 scripts/frontmatter_validator.py content/guokao/

# 自动修复
python -X utf8 scripts/frontmatter_validator.py --fix
```

### 18.2 `image_picker.py` — 智能配图

```python
#!/usr/bin/env python3
"""
图片选取器 - 按文章分类选取匹配主题的图片
10天内不重复选同一张图
每篇文章选取1-2张图
"""
import json
import random
import argparse
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).parent.parent
USAGE_LOG = ROOT / "scripts" / "image_usage_log.json"
IMAGE_LIB = ROOT / "public" / "images" / "lib"

# 文章分类 → 图片主题映射
CATEGORY_IMAGE_MAP = {
    "guokao":           ["exam", "study", "gov", "motivation", "office"],
    "shengkao":         ["exam", "study", "motivation", "office", "books"],
    "shanghai-shegong": ["gov", "office", "people", "city", "exam"],
    "baokao-gonggao":   ["gov", "office", "writing", "exam", "study"],
    "zhengce-jiedu":    ["gov", "office", "writing", "city", "tech"],
    "beikao-zhinan":    ["study", "books", "exam", "motivation", "writing"],
    "zhenti-jiexi":     ["exam", "study", "books", "writing", "office"],
    "gangwei-fenxi":    ["office", "people", "gov", "tech", "city"],
    "shang-an-jingyan": ["exam", "motivation", "people", "study", "office"],
}

_IMAGE_CACHE: dict[str, list[str]] = {}

def get_images_by_theme(theme: str) -> list[str]:
    if theme in _IMAGE_CACHE:
        return _IMAGE_CACHE[theme]
    theme_dir = IMAGE_LIB / theme
    if not theme_dir.exists():
        return []
    images = []
    for f in theme_dir.iterdir():
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            images.append(f"/images/lib/{theme}/{f.name}")
    _IMAGE_CACHE[theme] = images
    return images

def load_usage_log() -> dict:
    if not USAGE_LOG.exists():
        return {"usage": {}}
    with open(USAGE_LOG, "r", encoding="utf-8") as f:
        return json.load(f)

def save_usage_log(log: dict):
    log["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(USAGE_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def pick_images(category: str, count: int = 2, days: int = 10) -> list[str]:
    log = load_usage_log()
    usage = log.get("usage", {})
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    themes = CATEGORY_IMAGE_MAP.get(category, ["study", "exam"])

    available = []
    for theme in themes:
        for img in get_images_by_theme(theme):
            last_used = usage.get(img, "")
            if last_used < cutoff:
                available.append(img)

    # 不够则放宽限制：10天→5天→不限
    if len(available) < count:
        for d in [5, 0]:
            if len(available) >= count:
                break
            available = []
            new_cutoff = (datetime.now() - timedelta(days=d)).strftime("%Y-%m-%d")
            for theme in themes:
                for img in get_images_by_theme(theme):
                    last_used = usage.get(img, "")
                    if last_used < new_cutoff:
                        available.append(img)

    selected = random.sample(available, min(count, len(available)))
    return selected

def mark_used(images: list[str]):
    log = load_usage_log()
    usage = log.get("usage", {})
    today = datetime.now().strftime("%Y-%m-%d")
    for img in images:
        usage[img] = today
    log["usage"] = usage
    save_usage_log(log)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="图片选取器")
    parser.add_argument("--category", required=True, help="文章分类 slug")
    parser.add_argument("--count", type=int, default=2, help="选取数量")
    parser.add_argument("--update", action="store_true", help="标记为已使用")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    images = pick_images(args.category, args.count)
    if args.json:
        print(json.dumps(images, ensure_ascii=False))
    else:
        for img in images:
            print(img)

    if args.update:
        mark_used(images)
```

### 18.3 `seo_indexing_checker.py` — 收录监控

```python
#!/usr/bin/env python3
"""
SEO 收录检查器 - 四维度收录状态检查
维度：Sitemap / Bing / 百度 / Google
"""
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

SITE_URL = "https://YOUR_DOMAIN.com"
REPORTS_DIR = Path(__file__).parent.parent / "reports"

def check_sitemap(articles):
    """检查 sitemap 中是否包含文章 URL"""
    try:
        resp = requests.get(f"{SITE_URL}/sitemap.xml", timeout=10)
        if resp.status_code == 200:
            return {a: a["url"] in resp.text for a in articles}
    except:
        pass
    return {}

def check_bing(articles):
    """通过 Bing site: 查询"""
    results = {}
    for a in articles:
        query = f"site:{SITE_URL} {a['title'][:30]}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            resp = requests.get(
                "https://www.bing.com/search",
                params={"q": query},
                headers=headers,
                timeout=10
            )
            results[a["slug"]] = a["url"] in resp.text or SITE_URL in resp.text
        except:
            results[a["slug"]] = None
    return results

# ... 更多检查逻辑（完整脚本约550行）

if __name__ == "__main__":
    # 从 content/ 读取指定日期的文章列表
    # 然后逐维度检查收录状态
    pass
```

> 完整的收录检查脚本约 558 行，包含反爬检测、自动回退、Markdown 报告生成等功能。建议直接从项目仓库获取完整版本。

---

## 19. Git 仓库初始化和推送

### 19.1 创建 `.gitignore`

```gitignore
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts

# python
__pycache__/
*.pyc
.DS_Store

# reports
reports/*.md
!reports/.gitkeep
```

### 19.2 初始化并推送

```powershell
# 初始化 Git 仓库
git init
git add -A
git commit -m "feat: initial commit - gongkao SEO website scaffolding"

# 在 GitHub 上创建新仓库（不要勾选 Initialize with README）
# 然后：
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

## 20. Vercel 部署与绑定域名

### 20.1 连接 Vercel

1. 打开 https://vercel.com
2. 用 GitHub 账号登录
3. 点击 **Add New → Project**
4. 选择你刚刚推送的 GitHub 仓库
5. Vercel 会自动识别 Next.js 项目，无需额外配置
6. 点击 **Deploy**

### 20.2 绑定自定义域名

1. 在域名提供商（如阿里云/腾讯云）购买域名
2. 在 Vercel 项目设置 → **Domains** → 添加你的域名
3. 根据 Vercel 提示，在域名 DNS 中添加相应的记录：
   - 通常是添加一条 CNAME 记录指向 `cname.vercel-dns.com`
   - 或添加 A 记录指向 `76.76.21.21`
4. 等待 DNS 生效（通常几分钟到几小时）

### 20.3 每次发布流程

```powershell
# 1. 添加新文章或修改内容
# ...编辑 content/ 下的 .md 文件...

# 2. 运行质量检查
python -X utf8 scripts/frontmatter_validator.py

# 3. 如有问题，自动修复
python -X utf8 scripts/frontmatter_validator.py --fix

# 4. Git 提交
git add -A
git commit -m "content: auto publish articles 2026-05-24 21:00 (1 articles)"

# 5. 推送
git push origin main

# Vercel 会自动检测到 push 并重新部署
```

### 20.4 Git commit 格式规范

所有文章发布 commit 统一格式：
```
content: auto publish articles YYYY-MM-DD HH:MM (N articles)
```

---

## 21. SEO 高级优化（收录、站长平台）

### 21.1 百度搜索资源平台

1. 访问 https://ziyuan.baidu.com
2. 注册/登录账号
3. 添加站点 → 选择验证方式（推荐 HTML 标签验证）
4. 复制验证码，填入 `layout.tsx` 的 `<meta name="baidu-site-verification">` 中
5. 提交 `sitemap.xml`
6. 申请主动推送 API Token（用于自动化脚本）

### 21.2 Google Search Console

1. 访问 https://search.google.com/search-console
2. 添加资源 → URL 前缀方式 → 输入 `https://YOUR_DOMAIN.com`
3. 选择验证方式（推荐 HTML 标签验证）
4. 复制验证码，填入 `layout.tsx`
5. 提交 `sitemap.xml`

### 21.3 百度统计

1. 访问 https://tongji.baidu.com
2. 注册/登录
3. 添加站点 → 获取统计代码
4. 找到 `hm.js?XXXXX` 中的 ID
5. 填入 `layout.tsx` 中百度统计的 `Script` 标签

### 21.4 SEO 已实施清单

| 措施 | 说明 | 状态 |
|------|------|------|
| title / description / keywords | 每个页面动态生成 | ✅ |
| Canonical URL | 每页唯一规范 URL | ✅ |
| Open Graph / Twitter Cards | 社交分享优化 | ✅ |
| JSON-LD (Organization/WebSite/Article/BreadcrumbList) | 结构化数据 | ✅ |
| 动态 sitemap.xml | SSG 自动生成 | ✅ |
| robots.txt | 爬虫访问规则 | ✅ |
| 百度自动推送 (push.js) | 页面加载时自动提交 URL | ✅ |
| 百度统计 (hm.js) | 流量数据 | ✅ |
| 图片强缓存 | Cache-Control: 1年 | ✅ |
| 关键词聚合区块 | 首页底部 SEO 内容 | ✅ |

---

## 22. 设置自动化定时任务

在项目工作目录配置 WorkBuddy 自动化任务（或使用系统的 cron/scheduled tasks）：

### 22.1 每日发布任务（示例）

```
任务名: seo-8-00
时间:   每天 06:00
内容:   生成 8 篇文章（2社工/2国考/2省考/1事业/1通用）
        → 图片配图 → frontmatter 校验 → git commit & push

任务名: seo-9-15
时间:   每天 09:15
内容:   同上

任务名: seo-10-00
时间:   每天 10:00
内容:   同上

任务名: seo-2
时间:   每天 10:30
内容:   检查昨日文章收录状态
```

### 22.2 Windows 任务计划程序（备选方案）

```powershell
# 创建一个每日 06:00 运行的定时任务
schtasks /create /tn "GongKaoSEO_0600" /tr "python -X utf8 D:\AI\task\gongkao-seo\scripts\auto_gen.py" /sc daily /st 06:00
```

---

## 23. 日常运维与监控

### 23.1 每日发布后必检清单

发布新文章后，确认以下项目：

- [ ] 首页 https://YOUR_DOMAIN.com 正常访问（HTTP 200）
- [ ] 新发布的文章可以正常打开
- [ ] 日期格式正确（不是时间戳数字）
- [ ] 正文完整、无乱码
- [ ] 配图正常加载
- [ ] sitemap.xml 包含新文章 URL
- [ ] Vercel 部署无报错

### 23.2 收录率监控

```powershell
# 检查指定日期的文章收录状态
python -X utf8 scripts/seo_indexing_checker.py --date 2026-05-24

# 检查 7 天前的文章
python -X utf8 scripts/seo_indexing_checker.py --days-ago 7
```

### 23.3 关键词覆盖统计

```powershell
# 列出所有未覆盖的关键词
python -X utf8 scripts/keyword_driven_generator.py --list

# 推荐下一个要覆盖的关键词
python -X utf8 scripts/keyword_driven_generator.py --next
```

---

## 24. 踩坑经验总汇

### 🔴 P0 级（会导致整个网站崩溃）

#### 1. YAML 引号问题
- **现象**：Vercel 部署失败，`gray-matter` 解析错误
- **原因**：description 中包含英文双引号 `"`
- **解决**：将内嵌英文双引号替换为日文直角引号 `「」`
- **预防**：每次发布前运行 `python -X utf8 scripts/frontmatter_validator.py --fix`

#### 2. date 字段显示异常
- **现象**：前端文章日期显示为 `1716076800000` 或 `Invalid Date`
- **原因**：date 字段未加引号，YAML 解析为 Date 对象
- **解决**：`date: "2026-05-24"` 必须加引号

#### 3. 分类错误导致 404
- **现象**：文章页面 404
- **原因**：使用了不在 9 个白名单内的分类名（如 `shiye-dan-wei`）
- **解决**：统一使用 `gangwei-fenxi`（岗位分析）存放事业单位内容

#### 4. Category 目录不存在
- **现象**：文章文件放在 `content/category-name/` 但该目录下有很多 .md 文件，`content.ts` 的 `walkDir` 会把目录名当作 category 而不是文件里的 category 字段
- **解决**：确保每篇文章 frontmatter 中都包含正确的 `category` 字段

### 🟡 P1 级（影响使用但不致命）

#### 5. GitHub push 失败
- **现象**：`git push` 超时或连接拒绝
- **原因**：国内网络到 GitHub 不稳定
- **解决**：commit 成功后多次重试；或配置 SSH 密钥替代 HTTPS

#### 6. Windows 编码乱码
- **现象**：PowerShell 中 Python 脚本输出中文乱码
- **原因**：Windows 默认使用 GBK 编码
- **解决**：始终使用 `python -X utf8 scripts/xxx.py`

#### 7. 图片重复使用
- **现象**：同一张图片在短期内多次出现
- **原因**：未正确更新 `image_usage_log.json` 或未使用 `--update` 标记
- **解决**：使用 `image_picker.py --update` 确保每次选取后标记

#### 8. `generateStaticParams` 返回空数组
- **现象**：本地 `npm run dev` 正常但 `npm run build` 文章页 404
- **原因**：`contentDir` 路径在构建时和开发时不同
- **解决**：使用 `path.join(process.cwd(), "content")` 代替相对路径

### 🟢 P2 级（改进项）

#### 9. 百度反爬
- **现象**：收录检查脚本显示百度 ⚠️ 无法判断
- **原因**：百度对自动化查询有极强的反爬验证
- **解决**：手动在浏览器搜索 `site:YOUR_DOMAIN.com` 二次确认

#### 10. 图片加载慢
- **现象**：文章页图片加载时间长
- **原因**：图片未做压缩优化
- **解决**：统一 1920px 宽 JPEG 格式 + Next.js 自动 WebP/AVIF + 1 年缓存

---

## 附录 A：快速启动开发环境

```powershell
# 克隆项目
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd gongkao-seo

# 安装依赖
npm install

# 启动开发服务器
npm run dev
# 访问 http://localhost:3000
```

## 附录 B：文件结构总览

```
gongkao-seo/
├── README.md                    # 本文件
├── package.json
├── next.config.ts
├── tsconfig.json
├── postcss.config.mjs
│
├── content/                     # ★ 所有文章内容
│   ├── guokao/
│   ├── shengkao/
│   ├── shanghai-shegong/
│   ├── baokao-gonggao/
│   ├── zhengce-jiedu/
│   ├── beikao-zhinan/
│   ├── zhenti-jiexi/
│   ├── gangwei-fenxi/
│   └── shang-an-jingyan/
│
├── src/
│   ├── app/
│   │   ├── layout.tsx           # 全局布局 + SEO + JSON-LD
│   │   ├── page.tsx             # 首页
│   │   ├── globals.css          # 全局样式
│   │   ├── sitemap.ts           # 动态 sitemap
│   │   ├── robots.ts            # robots.txt
│   │   ├── not-found.tsx        # 404 页面
│   │   ├── [category]/
│   │   │   ├── page.tsx         # 分类列表页
│   │   │   └── [slug]/
│   │   │       └── page.tsx     # 文章详情页
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   └── Footer.tsx
│   │   └── ui/
│   │       ├── ArticleCard.tsx
│   │       └── Breadcrumbs.tsx
│   └── lib/
│       ├── content.ts           # 核心数据层
│       └── types.ts             # 类型定义
│
├── public/
│   └── images/
│       └── lib/                 # 图片库（11个主题）
│           └── index.json
│
├── scripts/                     # ★ Python 自动化脚本
│   ├── frontmatter_validator.py  #  前端校验
│   ├── keyword_driven_generator.py  #  关键词引擎
│   ├── seo_indexing_checker.py  #  收录监控
│   ├── image_picker.py          #  图片选取
│   └── keywords_pool.md         #  关键词池
│
└── reports/                     # 收录检查报告
```

## 附录 C：技术参考链接

- [Next.js 文档](https://nextjs.org/docs)
- [Vercel 部署文档](https://vercel.com/docs)
- [Pexels API](https://www.pexels.com/api/)
- [百度搜索资源平台](https://ziyuan.baidu.com)
- [Google Search Console](https://search.google.com/search-console)
- [Schema.org Article](https://schema.org/Article)
- [gray-matter](https://github.com/jonschlinkert/gray-matter)

---

> **许可证**：本项目代码仅供学习交流使用。
>
> **免责声明**：网站内容仅供参考，具体考试信息以官方公告为准。
