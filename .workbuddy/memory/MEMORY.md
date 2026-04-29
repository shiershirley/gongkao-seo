# MEMORY.md - 公考SEO项目长期记忆

## 项目基本信息

- **项目路径**：`C:\Users\HYY\WorkBuddy\gongkao-seo`
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

- **自动化名称**：公考SEO每日自动发文
- **执行时间**：每天06:00
- **工作目录**：c:/Users/HYY/WorkBuddy/gongkao-seo
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
