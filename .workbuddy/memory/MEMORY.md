# MEMORY.md - 公考SEO项目长期记忆

## 项目基本信息

- **项目路径**：`C:\Users\HYY\WorkBuddy\gongkao-seo`
- **部署地址**：https://gk.edu-sjtu.cn（Vercel）
- **内容目录**：`content/`（按类别分子目录：shanghai-shegong/guokao/shengkao等）
- **脚本目录**：`scripts/`

## 技术要点

### YAML Frontmatter 规范（Build失败预防）
**问题**：description字段内嵌英文双引号`"`会导致YAML解析错误，Vercel build失败。

**正确写法**：
- 使用日文直角引号「」代替英文双引号
- 示例：`description: "考生常把报名流程理解为「网上填表」，实际需经过..."`

**预防工具**：`scripts/frontmatter_validator.py`
- 每次文章生成后、git commit前必须运行
- 支持自动修复模式 `--fix`
- 校验项：必填字段、内嵌引号、日期格式、分类白名单、标签格式

### 本地Build验证
```bash
cd C:\Users\HYY\WorkBuddy\gongkao-seo
npm run build
```
成功标志：163个页面生成完成，无错误

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
