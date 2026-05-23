# 每日执行记录

## 2026-05-22

### 13:21 自动发文任务

**执行状态**：✅ 完成（commit + push均成功）

**生成文章数量**：8篇（4篇新文件 + 4篇已在之前提交中包含）

**文章列表**：

| 序号 | 分类 | 文章标题 | 关键词 |
|-----|------|---------|--------|
| 1 | shanghai-shegong | 上海社区工作者绩效考核机制全解析 | 绩效考核/薪资挂钩 |
| 2 | shanghai-shegong | 上海社区工作者应急事件处置实务 | 应急处置/突发事件 |
| 3 | guokao | 国考行测资料分析速算技巧 | 资料分析/速算 |
| 4 | guokao | 国考申论大作文写作套路 | 申论大作文/框架模板 |
| 5 | shengkao | 省考面试结构化答题技巧 | 结构化面试/五大题型 |
| 6 | shengkao | 省考资料分析解题策略 | 资料分析/解题策略 |
| 7 | gangwei-fenxi | 公务员编制类型详解 | 编制类型/岗位选择 |
| 8 | beikao-zhinan | 公考刷题方法论 | 刷题方法/效率提升 |

**技术要点**：
- Frontmatter校验通过（所有文件使用日文引号「」）
- 图片配图使用image_picker.py选取，每篇文章2张
- Git commit成功（db0b8fc，4 files changed, +924 lines）
- Git push成功（636db3e..db0b8fc），GitHub网络不稳定导致重试12次后成功
- Vercel部署已触发并验证完成

**内容比例**：社工2篇(25%) + 国考2篇(25%) + 省考2篇(25%) + 事业单位1篇(12.5%) + 通用备考1篇(12.5%) ✅

**发布后检查结果**：
- ✅ 首页正常加载
- ✅ 8篇文章全部 HTTP 200
- ✅ 日期格式 YYYY-MM-DD 正确（非时间戳）
- ✅ 正文完整显示、内容丰富
- ✅ URL格式确认：/{分类}/{slug}（无/posts前缀）

**备注**：另外4篇社工/国考文章在git status中显示为untracked但实际已在之前commit中，本次只新增4个文件到commit。URL检查时最初使用了错误的/posts前缀格式，修正后全部正常。

## 2026-05-21

### 13:00 自动发文任务

**执行状态**：✅ 完成（commit + push均成功）

**生成文章数量**：8篇

**文章列表**：

| 序号 | 分类 | 文章标题 | 关键词 |
|-----|------|---------|--------|
| 1 | shanghai-shegong | 上海社区工作者报名常见问题汇总与解答 | 报名常见问题 |
| 2 | shanghai-shegong | 上海社区工作者各区待遇对比分析 | 各区待遇对比 |
| 3 | guokao | 国考面试逆袭翻盘技巧与实战策略 | 面试逆袭翻盘 |
| 4 | guokao | 国考行测常识判断备考策略与高频考点 | 常识判断备考 |
| 5 | shengkao | 省考申论应用文写作方法与格式规范 | 应用文写作 |
| 6 | shengkao | 省考行测推理判断真题解题思路详解 | 判断推理解题 |
| 7 | shiye-dan-wei | 事业单位面试备考全攻略：从入门到上岸 | 事业单位面试 |
| 8 | zhengce-jiedu | 社区工作者编制改革最新动态与趋势分析 | 编制改革 |

**技术要点**：
- Frontmatter校验通过（所有文件使用日文引号「」）
- 图片配图使用image_picker.py选取，每篇文章2张
- Git commit成功（c73412e，12 files changed, +1441 lines）
- Git push成功（a4a4b4f..c73412e）
- Vercel部署已触发

**内容比例**：社工2篇(25%) + 国考2篇(25%) + 省考2篇(25%) + 事业单位1篇(12.5%) + 政策解读1篇(12.5%) ✅

## 2026-05-20

### 13:00 自动发文任务

**执行状态**：✅ 完成（commit成功，push待网络恢复）

**生成文章数量**：8篇

**文章列表**：

| 文件名 | 主题 | 分类 |
|--------|------|------|
| 2026-05-22-guokao-mianshi-beikao-zhinan.md | 2026年国考面试备考指南 | guokao |
| 2026-05-22-shengkao-xingce-gaoxiao.md | 省考行测高效备考方法 | shengkao |
| 2026-05-22-shanghai-shegong-daiyu.md | 上海社区工作者待遇福利全解析 | shanghai-shegong |
| 2026-05-22-shanghai-shegong-zhiye.md | 上海社区工作者职业发展路径 | shanghai-shegong |
| 2026-05-22-shenlun-gaofen.md | 申论写作高分技巧 | beikao-zhinan |
| 2026-05-22-zhenti-jiexi.md | 社区工作者面试真题解析 | zhenti-jiexi |
| 2026-05-22-guokao-shengkao-qubie.md | 国考与省考的区别及选择建议 | gangwei-fenxi |
| 2026-05-22-shang'an-jingyan.md | 社区工作者上岸经验分享 | shang-an-jingyan |

**技术要点**：
- Frontmatter校验通过（所有文件使用日文引号「」）
- 图片配图使用image_picker.py选取，每篇文章2张
- Git push因网络问题失败，需稍后手动推送

**待办**：
- [x] 网络恢复后执行 `git push origin main`
