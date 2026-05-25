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

**3. 校验工具**：`python scripts/frontmatter_validator.py`（`--fix`自动修复）

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
- **当前状态（2026-05-25）**：约10个commits未推送，GitHub端口443完全无法连接（timeout 21s）; 图片选取改用Python subprocess + JSON文件方式（避免PowerShell编码问题）

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

## 后续待完成事项

| 优先级 | 任务 |
|-------|------|
| P2 | 为高风险文章添加免责声明模板 |
| P3 | 扩充国考/省考/事业单位关键词池 |
| P3 | 提交sitemap至百度搜索资源平台 |
| P4 | 解决GitHub网络连接稳定性问题（考虑SSH密钥替代HTTPS） |
