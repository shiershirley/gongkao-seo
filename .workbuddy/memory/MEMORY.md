# MEMORY.md - 公考SEO项目长期记忆

## 项目基本信息

- **项目路径**：`d:\AI\task\gongkao-seo`（已从C:\Users\HYY\WorkBuddy\gongkao-seo迁移）
- **旧路径**：C:\Users\HYY\WorkBuddy\gongkao-seo（已废弃，仅保留git远程）
- **部署地址**：https://gk.edu-sjtu.cn（Vercel）
- **内容目录**：`content/`（按类别分子目录：shanghai-shegong/guokao/shengkao等）
- **脚本目录**：`scripts/`

## 关键词策略

### 关键词池 `scripts/keywords_pool.md`
- 分类管理：P0(核心)、P1(高价值)、P2(中价值)、P3(长尾)
- 类型分类：question(问题型)、compare(对比型)、study(备考型)、info(资讯型)、guide(指南型)
- 动态关键词池：招聘公告各阶段触发词（公告发布→报名→笔试→成绩→面试）

### 关键词校验 `frontmatter_validator.py`
- 新增关键词覆盖率检查（建议性，不阻断）
- 检测title/description/tags是否包含P0/P1关键词
- 提示格式：`[建议] 以下P0/P1词未出现在标题/描述/标签中: ...`

## 技术要点

### YAML Frontmatter 规范（Build失败预防）
**问题**：description字段内嵌英文双引号`"`会导致YAML解析错误，Vercel build失败。

**正确写法**：
- 使用日文直角引号「」代替英文双引号
- 示例：`description: "考生常把报名流程理解为「网上填表」，实际需经过..."`

**预防工具**：`scripts/frontmatter_validator.py`
- 每次文章生成后、git commit前必须运行
- 支持自动修复模式 `--fix`
- 校验项：必填字段、内嵌引号、日期格式、分类白名单、标签格式、关键词覆盖率

### 本地Build验证
```bash
cd C:\Users\HYY\WorkBuddy\gongkao-seo
npm run build
```
成功标志：146个页面生成完成，无错误

## Git操作规范

- 每次修改后检查 `git status`
- commit信息格式：`content: auto publish articles YYYY-MM-DD`
- 本地常有未推送的commit，需注意手动push

## 已知问题记录

### 2026-04-28/29 Vercel Build失败
- **原因**：4篇文章description字段含未转义双引号
- **影响文件**：
  - content/baokao-gonggao/2026-04-28-shegong-baoming-quanliucheng.md
  - content/gangwei-fenxi/2026-04-29-guokao-zhiweibiao-xuanzhuanqubie.md
  - content/gangwei-fenxi/2026-04-29-guokao-tiaoji-bulou-jihui.md
  - content/zhenti-jiexi/2026-04-29-xingce-shuliao-suyong.md
- **修复**：替换内嵌双引号为「」
- **预防**：frontmatter_validator.py

## 自动化配置

- **自动化ID**：automation
- **自动化名称**：公考SEO每日自动发文
- **执行时间**：每天06:00
- **工作目录**：`d:\AI\task\gongkao-seo`（2026-05-07迁移自旧路径）
- **关键步骤**：文章生成 → frontmatter校验 → git commit/push → Vercel部署

## 关键词生成器

### `scripts/keyword_driven_generator.py`
- 扫描已发布文章，统计已覆盖关键词
- 从关键词池选取未覆盖的高价值词
- 生成文章生成指令（带SEO要求）

**使用方式**：
```bash
python scripts/keyword_driven_generator.py --next      # 获取下一个建议词
python scripts/keyword_driven_generator.py --list     # 列出未覆盖关键词
python scripts/keyword_driven_generator.py --prompt    # 生成完整文章指令
```

## SEO收录优化（2026-05-14新增）

### 收录检查脚本 `scripts/seo_indexing_checker.py`
- 检查文章在百度/Bing/Google的收录状态
- 支持指定日期检查
- 生成收录报告

**使用方式**：
```bash
python scripts/seo_indexing_checker.py                    # 检查所有文章
python scripts/seo_indexing_checker.py --date 2026-05-14  # 检查指定日期
```

### 收录优化要点
1. **Sitemap正常**：sitemap.xml已配置，Vercel自动更新
2. **robots.txt正常**：允许爬虫抓取
3. **文章收录延迟**：新文章通常1-7天被收录（百度较慢）
4. **主动提交**：建议手动提交sitemap至百度/Google Search Console

### 收录检查报告
- **报告路径**：`SEO收录检查报告_YYYY-MM-DD.md`
- **检查周期**：每周一对7天前发布的内容进行检查
- **报告内容**：总发布数量、收录数量、未收录原因、优化建议

### 自动化流程更新（2026-05-14）

#### 新增自动化任务

| 任务名称 | 执行时间 | 执行内容 |
|---------|---------|---------|
| SEO收录检查 | 每天07:00 | 检查前一天文章收录状态 |
| 收录周报生成 | 每周一09:00 | 汇总上周收录数据，生成MD报告 |
| 百度主动推送 | 每天06:05 | 文章发布后自动推送URL到百度 |

#### 更新后完整自动化流程

**每日06:00 - 文章生成与发布**
1. 读取关键词池，生成SEO文章（1500-2500字）
2. frontmatter校验（YAML格式、关键词覆盖率）
3. git push触发Vercel部署
4. 自动推送URL到百度（新增）

**每日07:00 - 收录检查（新增）**
1. 检查前一天发布的文章在百度/Bing/Google的收录状态
2. 记录未收录文章，分析原因

**每周一09:00 - 收录周报（新增）**
1. 汇总上周7天的新增文章和收录数据
2. 生成MD格式收录报告
3. 根据未收录原因调整内容生成策略

### 待完成
- [ ] 登录百度搜索资源平台，提交sitemap
- [ ] 登录Google Search Console，提交sitemap
- [ ] 申请百度主动推送API Token
- [ ] 创建SEO收录检查自动化任务（07:00）
- [ ] 创建收录周报生成自动化任务（周一09:00）

## 每日发文执行记录摘要

| 日期 | 生成篇数 | 主要关键词 | 状态 | 收录状态 |
|------|---------|-----------|------|---------|
| 2026-05-14 | 4篇 | 上海社工考试、上海社区工作者报名、社区工作者考试内容、社区工作者面试技巧 | ✅ 已推送 | ⏳ 待检查 |
| 2026-05-13 | 4篇 | 社区工作者考试、报名、备考攻略、面试内容 | ✅ 已推送 | ⏳ 待检查 |
| 2026-05-12 | 4篇 | 社区工作者招聘、上海招聘、待遇、报名条件 | ✅ 已推送 | ⏳ 待检查 |
| 2026-05-08 | 6篇 | 考什么、报考要求、学历要求、年龄限制等 | ✅ 已推送 | ⏳ 待检查 |
