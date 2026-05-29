# MEMORY.md - 公考SEO项目长期记忆

## 项目基本信息

- **项目路径**：`d:\AI\task\gongkao-seo`
- **部署地址**：https://gk.edu-sjtu.cn（Vercel自动部署）
- **内容目录**：`content/`（按类别分子目录）
- **脚本目录**：`scripts/`

## 内容分类规范

**允许的9个分类**（frontmatter_validator.py中ALLOWED_CATEGORIES）：
- guokao, shengkao, shanghai-shegong, baokao-gonggao
- zhengce-jiedu, beikao-zhinan, zhenti-jiexi, gangwei-fenxi, shang-an-jingyan

**注意**：事业单位内容统一用`gangwei-fenxi`，不要创建`shiyedanwei`分类（会导致404）

## 各时段内容比例（每批次8篇）

| 社工类 | 国考 | 省考 | 事业单位 | 通用备考 |
|--------|------|------|---------|---------|
| 2篇(25%) | 2篇(25%) | 2篇(25%) | 1篇(12.5%) | 1篇(12.5%) |

## 关键词策略

- 关键词池：`scripts/keywords_pool.md`（P0-P3分级管理）
- **当前状态**：P0-P3全部已覆盖，采用「角度轮换策略」生成差异化文章
- 角度维度：地域变体、年份变体、人群变体、场景变体、科目变体、问题变体

## YAML Frontmatter 规范（关键！）

**1. description内不能用英文双引号**
- ❌ 错误：`description: "考生常把「网上填表」理解为"报名"..."`
- ✅ 正确：用日文直角引号「」代替英文双引号

**2. date字段必须加引号**
- ❌ 错误：`date: 2026-05-19` → YAML解析为Date对象 → 前端显示时间戳
- ✅ 正确：`date: "2026-05-19"`

**3. title字段禁止纯数字（会致Vercel构建失败！）**
- ❌ 错误：`title: 2026` → YAML解析为Number → Next.js预渲染报错：`TypeError: Cannot use 'in' operator to search for 'template' in 2026`
- ✅ 正确：`title: "2026"`
- **批量修复命令**：`cd d:/AI/task/gongkao-seo && python -c "import os,re; [(__import__('re').sub(r'^(title:\s*)([\+\-]?\d+[\s]*)$', r'\1\"\2\"', open(p:=os.path.join(r,f),'r',encoding='utf-8').read(), flags=re.M) != open(p,'r',encoding='utf-8').read() and open(p,'w',encoding='utf-8').write(__import__('re').sub(r'^(title:\s*)([\+\-]?\d+[\s]*)$', r'\1\"\2\"', open(p,'r',encoding='utf-8').read(), flags=re.M))) for r,d,files in os.walk('content') for f in files if f.endswith('.md')]"`

**4. 校验工具**：`python scripts/frontmatter_validator.py`（`--fix`自动修复）

## 图片配图规范

- 每篇文章2张配图，调用`auto_gen_xxxx.py`内置逻辑（基于image_usage_log.json去重）
- 图片路径格式：`/images/lib/[主题]/xxx.jpg`
- 10天内不重复选同一张图

### 图片主题映射
| 分类 | 可用主题 |
|------|---------|
| guokao | exam/study/gov/motivation/office |
| shengkao | exam/study/motivation/office/books |
| shanghai-shegong | gov/office/people/city/exam |
| gangwei-fenxi | office/people/gov/tech/city |
| beikao-zhinan | study/books/exam/motivation/writing |
| baokao-gonggao | gov/office/writing/exam/study |
| zhengce-jiedu | gov/office/writing/city/tech |
| zhenti-jiexi | exam/study/books/writing/office |
| shang-an-jingyan | exam/motivation/people/study/office |

## 自动化发文脚本

每个时段有独立的生成脚本：
- `scripts/auto_gen_0915.py` - 09:15批次
- `scripts/auto_gen_1000_2.py` - 10:00-2批次
- 其他时段类似模式

**运行方式**：`python -X utf8 scripts/auto_gen_xxxx.py`（`-X utf8`解决PowerShell中文编码问题）

## Git操作规范

- commit格式：`content: auto publish articles YYYY-MM-DD HH:MM (N articles)`
- **已知问题**：GitHub网络不稳定，push常失败。commit成功后需多次重试push，或网络恢复后手动推送
- **当前状态（2026-05-28 14:06）**：GitHub推送再次失败，错误为`fatal: could not read Username for 'https://github.com': terminal prompts disabled`。此前13:21批次推送正常，但14:06批次（seo-8-00-2）推送失败。建议改用SSH密钥认证替代HTTPS。

## 自动化任务列表

| 时段 | 任务ID | 说明 |
|------|--------|------|
| 06:00 | seo-8-00 | 早批次发文 |
| 08:00 | seo-8-00-2 | 第二批次 |
| 08:30 | seo-8-30 | 第三批次 |
| 09:00 | seo-9-00 | 第四批次 |
| 09:15 | seo-9-15 | 第五批次 |
| 10:00 | seo-10-00 | 第六批次 |
| 10:00 | seo-10-00-2 | 第七批次 |
| 10:30 | seo-2（收录检查）| 检查10天前文章 |

**发布后必须检查**：首页 + 每篇文章（HTTP200、日期格式、正文完整、配图加载）+ Sitemap

## SEO收录检查

- **脚本**：`scripts/seo_indexing_checker.py`（三引擎：百度/Bing/Google + Sitemap）
- **报告路径**：`reports/indexing_check_YYYYMMDD_HHMMSS.md`
- **注意**：百度反爬较强（❌不代表未收录），Google国内限制（超时返回—），需手动二次确认

## 内容风险管理

- 避免具体数字：招聘人数、薪资待遇、竞争比、分数线等数据风险高
- 已删除3篇极高风险文章（含具体招聘数字/竞争比/薪资数据的文章）
- 高风险文章约150篇，建议添加免责声明模板

## 脚本问题记录

### 2026-05-29 发现：auto_gen_daily.py 标题/内容不匹配

**问题**：脚本中文章定义（title/description/tags）与 `generate_XXX_content` 实际生成的正文内容不一致。
- beikao-zhinan：标题「面试礼仪」→ 实际生成「数字化工具」内容
- guokao-tips：标题「真题数据分析」→ 实际生成「言语理解」内容

**根因**：`generate_body_by_category` 按 `content_angle` 匹配生成器，但部分角度无对应处理逻辑，fallback到默认内容，与标题不匹配。

**修复**：`a0b14d8` 已修改文章定义为匹配实际生成内容的标题/描述/标签，并同步修改脚本防止后续批次复现。

## Sitemap 修复记录（2026-05-29）

**问题**：SEO收录检查发现159篇2026-05-19文章不在Sitemap中
- **根因**：约687篇文章的 frontmatter 中 `title` 为空，`getAllArticles()` 跳过这些文章
- **修复**：修改 `src/app/sitemap.ts`（commit 426c626），直接从文件系统扫描生成 URL，不再依赖 `getAllArticles()`
- **效果**：
  - Sitemap URL：621 → 1388（+767）
  - 线上已验证：`curl https://gk.edu-sjtu.cn/sitemap.xml | grep -c "<loc>"` = 1388
  - 2026-05-19 文章全部包含
- **副作用**：首页/分类列表仍依赖 `getAllArticles()`，空 title 文章不会出现在列表中（但直接访问URL正常）

## 已知问题：大量文章 frontmatter title 为空

**影响范围**：约687篇文章（占总数50%）
**表现**：
- frontmatter 中 `title:` 后无内容，或 title 为纯数字如 `2026`
- 这些文章在首页/分类列表不可见，但直接访问URL可正常打开
**根因**：文章生成脚本未正确写入 title（可能为脚本bug或生成失败后的残留文件）
**临时解决**：Sitemap 已绕过此问题直接包含所有URL
**长期解决**：需修复生成脚本，或批量为无title文章补全标题

## 后续待完成事项

| 优先级 | 任务 |
|-------|------|
| P1 | 修复文章生成脚本，确保 frontmatter title 正确写入 |
| P1 | 批量修复现有687篇空 title 文章的 frontmatter |
| P2 | 为高风险文章添加免责声明模板 |
| P3 | 扩充国考/省考/事业单位关键词池 |
| P3 | 提交sitemap至百度搜索资源平台 |
| P4 | 解决GitHub网络连接稳定性问题（考虑SSH密钥替代HTTPS） |
