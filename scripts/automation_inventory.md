# gongkao-seo 自动化流程梳理报告

> 生成时间：2026-06-02 | 共 20 个自动化流程

---

## 一、活跃流程（ACTIVE）：11 个

### A. 每日自动发文（10 个）

| 编号 | ID | 名称 | 执行时间 | 每批数量 | 工作目录 | 提示词版本 |
|------|-----|------|---------|---------|---------|-----------|
| 1 | `seo-8-00` | 公考SEO每日自动发文（08:03） | 08:03 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V1 |
| 2 | `seo-8-30` | 公考SEO每日自动发文（8:30） | 08:30 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V1 |
| 3 | `seo-9-15` | 公考SEO每日自动发文（09:15） | 09:15 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V1 |
| 4 | `seo-9-00` | 公考SEO每日自动发文（09:19） | 09:19 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V1 |
| 5 | `seo-10-00-2` | 公考SEO每日自动发文（10:00） | 10:00 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V1 |
| 6 | `seo-10-00` | 公考SEO每日自动发文（10:23） | 10:23 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V1 |
| 7 | `seo-11-00` | 公考SEO每日自动发文（11:14） | 11:14 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V1 |
| 8 | `seo-12-00` | 公考SEO每日自动发文（12:11） | 12:11 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V1 |
| 9 | `seo-13-00` | 公考SEO每日自动发文（13:21） | 13:21 | 8篇 | `d:\AI\task\gongkao-seo` | 完整版V2 |
| 10 | `seo-8-00-2` | 公考SEO每日自动发文（8:00） | **14:06** ⚠️ | 7-8篇 | `d:\AI\task\gongkao-seo` | 简化版 |

> **每天发文总量**：约 **79 篇**（10批次 × 8篇，其中1批7-8篇）

### B. 收录检查（1 个）

| 编号 | ID | 名称 | 执行时间 | 工作目录 |
|------|-----|------|---------|---------|
| 11 | `seo-10-2` | 公考SEO-每日10点收录检查 | 10:00 | `d:\AI\task\gongkao-seo` |

---

## 二、已暂停流程（PAUSED）：9 个

| 编号 | ID | 名称 | 执行时间 | 工作目录 | 暂停原因 |
|------|-----|------|---------|---------|---------|
| 1 | `seo` | 公考SEO每日自动发文 | 06:00 | `c:\Users\HYY\WorkBuddy\gongkao-seo` | 旧路径，旧提示词 |
| 2 | `automation` | 公考SEO每日自动发文 | 06:00 | `d:\AI\task\gongkao-seo` | 旧版本，无内容比例 |
| 3 | `seo-10` | 公考SEO-10天前文章收录检查 | 10:00 | `d:\AI\task\gongkao-seo` | 与 `seo-10-2` 重复 |
| 4 | `seo-2` | SEO每日收录检查 | 07:30 | `d:\AI\task\gongkao-seo` | 旧版收录检查 |
| 5 | `seo-20-00` | SEO收录检查（每日20:00） | 20:00 | `d:\AI\task\gongkao-seo` | 旧版收录检查 |
| 6 | `automation-2` | 上海社区工作者每日简报 | 07:00 | `d:\AI\task\dailynews-SHshegong` | 最完整的简报流程 |
| 7 | `automation-4` | 上海社区工作者每日简报 | 07:00 | `d:\AI\task\dailynews-SHshegong` | 简化版简报 |
| 8 | `automation-6` | 上海社区工作者每日简报 | 07:00 | `c:\Users\HYY\WorkBuddy\automation-claw-20260429115436` | 旧路径 |
| 9 | `automation-3` | 公众号数据监测 | 09:00 | （未明确） | 状态未知 |

---

## 三、提示词版本对比

### 版本 A：完整版 V1（`seo-8-00` ~ `seo-12-00`、`seo-10-00-2`、`seo-8-30`、`seo-9-15`）

**共 9 个流程使用此版本**（仅执行时间不同）

```
公考SEO网站（gk.edu-sjtu.cn）每日文章生成任务。每日{HH}:{MM}执行，生成8篇文章。

工作目录：d:\AI\task\gongkao-seo

## 执行步骤

### 1. 读取关键词池
读取 scripts/keywords_pool.md，按优先级选取未覆盖的关键词
优先级：P0 > P1 > P2 > P3
类型：question > compare > study > info > guide

### 2. 内容比例要求（每批次8篇）
- 社工类（上海社工资讯）：2篇（25%）
- 国考：2篇（25%）
- 省考：2篇（25%）
- 事业单位：1篇（12.5%）
- 通用备考：1篇（12.5%）

注意：
- 社工类仅聚焦上海社工资讯，不生成其他省份社工招聘数据
- 事业单位为新增内容，需扩充相关关键词

### 3. 生成文章（每篇带图片配图）
执行命令：
cd d:/AI/task/gongkao-seo
python -X utf8 scripts/auto_gen_daily.py --hour {H} --minute {M}

此脚本会：
- 根据关键词生成1500-2500字SEO文章
- frontmatter必须字段：title/description(150字,「」引号)/date/category/tags/author(公考助手)
- 图片配图：自动为每篇文章选取2张图片（调用image_picker逻辑）
  - 图片路径格式：/images/lib/[主题]/xxx.jpg
  - 10天内不重复选同一张图

### 4. Frontmatter校验
运行 python -X utf8 scripts/frontmatter_validator.py --content-check
如有问题使用 --fix 参数修复

### 5. Git提交推送
git add -A && git commit -m "content: auto publish articles $(date +%Y-%m-%d) {HH}:{MM}"
&& git push origin main

### 6. 发布后检查与修复（必须执行）
等待Vercel部署完成后（约2-3分钟），执行以下检查：
1. 首页检查：访问 https://gk.edu-sjtu.cn
2. 新文章检查：逐一打开本次发布的每篇文章页面
3. Sitemap检查：访问 /sitemap.xml

异常处理：
- YAML解析错误 → 修复frontmatter → 重新push
- 日期显示为时间戳 → 检查date字段引号 → 重新push
- 图片无法加载 → 检查图片路径 → 重新push

### 图片分类映射
guokao → exam/study/gov/motivation/office
shengkao → exam/study/motivation/office/books
shanghai-shegong → gov/office/people/city/exam
baokao-gonggao → gov/office/writing/exam/study
zhengce-jiedu → gov/office/writing/city/tech
beikao-zhinan → study/books/exam/motivation/writing
zhenti-jiexi → exam/study/books/writing/office
gangwei-fenxi → office/people/gov/tech/city
shang-an-jingyan → exam/motivation/people/study/office
```

### 版本 B：完整版 V2（`seo-13-00`）

**与 V1 基本一致，仅第2步增加一条约束：**

```
注意：
- 社工类仅聚焦上海社工资讯，不生成其他省份社工招聘数据
- 事业单位内容统一使用 gangwei-fenxi 分类，不要使用 shiyedanwei
```

### 版本 C：简化版（`seo-8-00-2`）

**缺少以下关键内容：**
- 无"内容比例要求"（社工/国考/省考分配）
- 步骤编号从"2"开始写生成文章，无"1. 读取关键词池"标题
- 无 `python -X utf8` 前缀（仅 `python`）
- Frontmatter 校验命令缺少 `--content-check`
- Git commit 消息格式为硬编码 `"YYYY-MM-DD HH:MM"` 而非 `$(date)`
- 图片配图逻辑不同：明确要求调用 `scripts/image_picker.py` 而非脚本内部自动处理

```
公考SEO网站（gk.edu-sjtu.cn）每日文章生成任务。每日8:00执行，生成7-8篇文章。

工作目录：d:\AI\task\gongkao-seo

## 执行步骤

### 1. 读取关键词池
读取 scripts/keywords_pool.md，按优先级选取未覆盖的关键词
优先级：P0 > P1 > P2 > P3
类型：question > compare > study > info > guide

### 2. 生成文章（每篇带图片配图）
- 根据关键词生成1500-2500字SEO文章
- frontmatter必须字段：title/description(150字,「」引号)/date/category/tags/author(公考助手)
- 图片配图：使用 scripts/image_picker.py 为每篇文章选取2张图片
  - 命令：python scripts/image_picker.py --category [分类] --count 2 --update --json
  - 将图片Markdown语法 ![](图片路径) 插入文章合适位置
  - 图片路径格式：/images/lib/[主题]/xxx.jpg
  - 10天内不重复选同一张图

### 3. Frontmatter校验
运行 python scripts/frontmatter_validator.py，如有问题使用 --fix 参数修复

### 4. Git提交推送
git add -A && git commit -m "content: auto publish articles YYYY-MM-DD HH:MM"
&& git push origin main

### 图片分类映射
（与V1相同）

### 6. 发布后检查与修复（必须执行）
（与V1相同）
```

### 版本 D：收录检查版（`seo-10-2`）

```
对公考SEO网站 gk.edu-sjtu.cn 执行文章收录检查任务：

## 任务说明
1. 进入工作目录 d:\AI\task\gongkao-seo
2. 运行 Python 脚本检查10天前发布的文章收录情况：
   python scripts/seo_indexing_checker.py
3. 脚本会自动：
   - 查找 content 目录下10天前发布的文章
   - 检查每篇文章在 Sitemap、Bing 的收录状态
   - 生成 Markdown 格式收录报告，保存到 reports/ 目录
4. 报告文件名格式：indexing_check_{目标日期}_{检查日期}_{时间戳}.md

## 注意事项
- 如果目标日期没有文章，脚本会自动查找最近的可用日期
- 报告包含每篇文章的标题、URL、分类、收录状态等信息
- 百度收录需要登录百度搜索资源平台手动检查
```

### 版本 E：上海社区工作者简报（`automation-2`，最完整）

```
## 任务：生成上海社区工作者每日简报并推送通知

每天早上7:00自动执行以下步骤，完成简报生成后发送飞书消息通知用户。

### 第一步：多渠道信息搜集（7天回溯）

使用以下关键词组同步搜索，合并去重：

web_search（通用搜索引擎，多轮并发）：
- "上海 社区工作者 招聘 公告 2026"
- "上海 社区工作者 报名 笔试 面试 通知"
- "上海 社区工作者 准考证 成绩查询"
- "上海 社工考试 报名时间 2026"
- "浦东新区 社区工作者 招聘"
- "静安区 社区工作者 招聘 报名"
- "奉贤区 社区工作者 笔试 准考证"
- "崇明区 社区工作者 招聘 报名"
- "上海 社区工作者 政策 待遇 2026"

关键：扩大搜索范围到16区官方渠道
- 对尚未搜索的区逐一搜索"XX区 社区工作者 招聘/报名/公告 2026"
- 优先引用政府官网和官方公众号信息

16区官方公众号参考：
浦东发布、上海黄浦、上海静安、上海徐汇、上海长宁、上海普陀、
上海虹口、上海杨浦、今日闵行、上海宝山、上海嘉定、i金山、
上海松江、绿色青浦、上海奉贤、上海崇明

### 第二步：信息筛选与去重（含历史对比）
1. 地域过滤：仅保留明确涉及上海的条目
2. 内容过滤：排除纯广告、纯课程推广
3. 时效过滤：保留过去7天内内容
4. 去重：相同标题或相似度 > 80% 只保留1篇
5. 历史去重：读取 social_worker_history.md，对比过去3天标题
6. 优先级排序：紧急 > 官方首发 > 近期重要 > 一般
7. 来源优先：政府官网 > 官方公众号 > 权威媒体 > 聚合平台 > 培训机构

最终筛选出10条最有价值的信息。

### 第三步：生成飞书文档
使用 lark-cli 创建飞书文档
文档格式：顶部监测信息 + 主体飞书表格（4列：标题|时间|核心摘要|原文链接）+ 底部时间节点汇总

### 第四步：生成微信友好分享文本
从10条资讯中提炼核心信息，生成可直接分享到微信群的文本
格式：标题 + TOP 6 重要资讯 + 完整简报链接

### 第五步：生成Top6海报图片
使用 image_gen 工具生成 1024x1536 竖版海报
风格：深蓝色渐变背景，专业资讯海报

### 第六步：推送飞书群
使用 lark-cli 发送消息到「职考项目部」群
同时保存微信分享文本到 wechat_share_{日期}.txt

### 第七步：更新历史记录
将当天10条标题追加到 social_worker_history.md
保留最近7天，删除7天前的记录

### 错误处理
- 某步骤失败，跳过继续后续步骤
- 筛选结果为空，跳过文档创建和推送
- image_gen 失败不影响其他步骤
```

### 版本 F：上海社区工作者简报（`automation-4`，简化版）

```
## 上海社区工作者每日简报自动化任务

### 任务目标
每天自动搜集上海社区工作者相关资讯，生成简报文档并推送到飞书群。

### 工作流程
第1步：多渠道搜索搜集
- 使用 multi-search-engine 或查找资料 skill
- 搜索关键词：上海社区工作者招聘/考试/公告/报名/社工招聘
- 搜集最近24小时内的新闻和公告

第2步：内容筛选与去重
- 过滤重复内容
- 筛选高质量内容（政府公告优先）
- 每类保留3-5条

第3步：生成飞书文档
- 使用 lark-doc skill 创建飞书文档
- 每个条目包含：标题、发布时间、核心摘要（150-200字）、原文链接
- 按类别分组，全部罗列不删减

第4步：推送到飞书群「职考项目部」
- 消息格式：📢 今日简报已更新 + 文档链接
```

### 版本 G：上海社区工作者简报（`automation-6`，另一简化版）

```
## 任务：生成上海社区工作者每日简报并推送到飞书群

### 第一步：多渠道信息搜集
web_search 搜索（3组关键词）+ search-wx 搜索（3组关键词）
每组取前10条，共30-60条原始结果

### 第二步：信息筛选与去重
地域过滤 → 内容过滤 → 时效过滤 → 去重 → 排序
最终保留5-10条

### 第三步：生成飞书文档
使用 lark-cli 创建飞书文档
提取返回值中的 data.doc_id 和 data.url

### 第四步：生成飞书群消息文本
提炼3-5条要点，保存为 message.txt

### 第五步：发送到飞书群「职考项目部」
lark-cli im +messages-send --as user --chat-id oc_f43a7c6ba8dbdc711f863c41216a0eaa

### 执行记录
追加到工作区 .workbuddy/memory/YYYY-MM-DD.md
```

### 版本 H：旧版发文（`seo`，PAUSED）

```
你是公考SEO网站的自动内容发布助手。

## 工作目录
c:\Users\HYY\WorkBuddy\gongkao-seo

## 任务流程

### 1. 搜索最新公考信息
使用 web_search 搜索：
- "上海社区工作者 招聘 2026"
- "公务员考试 公告 2026"
- "省考 报名 时间 2026"
- "国考 职位表 2026"

### 2. 生成 15-20篇 SEO 文章
- 9个分类目录
- 1500-2500字
- frontmatter 必须包含 title/description/date/category/tags/author
- 文章优先覆盖：上海社区工作者、国考公告、省考公告

### ⚠️ 日期严格校验规则
- 所有文章的 date 字段必须使用当天日期
- 绝对禁止未来日期和过去日期

### ⚠️ 写作风格规范
- 语气像公考培训老师写公众号推文
- 禁止纯数字编号作为章节标题
- 尽量少用表格，表格前后必须有引导语和总结
- 禁止AI痕迹（"总而言之"、套话结尾、过度粗体等）

### 3. Frontmatter 校验
运行 scripts/frontmatter_validator.py
- exit code = 0 → 继续Git推送
- exit code ≠ 0 → 立即修复 → 重新校验

### 4. 推送到 GitHub
git add -A && git commit && git push origin main

### 5. 记录日志
在工作记忆中记录今天发布的文章标题和数量
```

---

## 四、关键问题汇总

| 问题类型 | 详情 | 影响 |
|---------|------|------|
| 名称与时间不匹配 | `seo-8-00-2` 名称写"8:00"，实际执行14:06 | 误导 |
| 工作目录不一致 | `seo` 使用旧路径 `c:\Users\HYY\WorkBuddy\gongkao-seo` | 启用会失败 |
| 提示词版本混乱 | 10个活跃发文流程中，9个用完整版，1个用简化版 | 内容质量不一致 |
| 发文频率过高 | 每天10批次×8篇=约80篇 | 关键词耗尽、内容重复、Git冲突 |
| 收录检查重复 | `seo-10-2`(ACTIVE) 与 `seo-10`(PAUSED) 功能相同 | 冗余 |
| 简报流程重复 | 3个简报自动化，功能高度重叠 | 冗余 |
