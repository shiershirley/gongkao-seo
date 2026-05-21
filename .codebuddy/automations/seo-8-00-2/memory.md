# 自动化执行记忆 - 公考SEO每日自动发文（8:00）

## 最近执行记录

### 2026-05-21 08:00 执行

**状态**：文章已生成、已提交、git push 失败（网络问题）⚠️

**生成文章（8篇）**：

| 文件名 | 关键词 | 分类 |
|--------|--------|--------|
| 2026-05-21-shegong-mianshi-liyi-xijie.md | 社区工作者面试礼仪细节 | shanghai-shegong |
| 2026-05-21-shegong-cizhi-liucheng-zhinan.md | 社区工作者辞职流程 | shanghai-shegong |
| 2026-05-21-guokao-yingjiesheng-shenfeng-rending.md | 国考应届生身份认定 | guokao |
| 2026-05-21-guokao-shenlun-dajianghua-jiegou.md | 国考申论大作文结构 | guokao |
| 2026-05-21-shengkao-tiaojie-liucheng.md | 省考调剂流程 | shengkao |
| 2026-05-21-shengkao-mianshi-liyi-quancong.md | 省考面试礼仪全攻略 | shengkao |
| 2026-05-21-shiyedanwei-zonghe-yingyong-nengli.md | 事业单位综合应用能力 | gangwei-fenxi |
| 2026-05-21-gongkao-shanganghou-dangan-zhuanyi.md | 公考上岸后档案转移 | zhengce-jiedu |

**内容比例**：社工2篇(25%) + 国考2篇(25%) + 省考2篇(25%) + 事业单位1篇(12.5%) + 通用1篇(12.5%) ✅ 符合规范

**执行步骤结果**：
1. ✅ 读取关键词池（keywords_pool.md）
2. ✅ 生成8篇新文章（按内容比例规范）
3. ⚠️ 图片配图：文章已含图片路径（手动按分类映射插入），image_picker.py 因PowerShell编码问题输出乱码，但图片路径已按规范写入
4. ✅ frontmatter 校验：运行 `frontmatter_validator.py --fix`，修复了历史文件中的23个问题
5. ✅ git add + commit 完成（commit: 5208593，`content: auto publish articles 2026-05-21 08:00`）
6. ❌ git push 失败：**网络无法连接 GitHub**（TCP 443通但HTTPS超时，可能是防火墙/代理问题）

**待处理**：
- [ ] 网络恢复后执行 `cd d:\AI\task\gongkao-seo; git push origin main`
- [ ] 验证 Vercel 是否自动部署成功

**图片使用**：
- 文章1（面试礼仪）：`/images/lib/office/shegong-mianshi-liyi-01.jpg`
- 文章2（辞职流程）：`/images/lib/office/shegong-cizhi-liucheng-01.jpg`
- 文章3（应届生身份）：`/images/lib/study/guokao-yingjiesheng-01.jpg`
- 文章4（申论大作文）：`/images/lib/study/guokao-shenlun-dajianghua-01.jpg`
- 文章5（省考调剂）：`/images/lib/study/shengkao-tiaojie-01.jpg`
- 文章6（省考面试礼仪）：`/images/lib/office/shengkao-mianshi-liyi-01.jpg`
- 文章7（事业单位综应）：`/images/lib/study/shiyedanwei-zonghe-01.jpg`
- 文章8（档案转移）：`/images/lib/gov/gongkao-dangan-01.jpg`

---

## 历史记录

### 2026-05-20 08:00 执行

**状态**：文章已生成、已提交、已推送 ✅

**生成文章（4篇，今天总计8篇）**：

| 文件名 | 关键词 | 分类 |
|--------|--------|--------|
| 2026-05-20-jiangsu-shegong-zhaopin-2026.md | 江苏社区工作者招聘 | shanghai-shegong |
| 2026-05-20-zhejiang-shegong-zhaopin-2026.md | 浙江社区工作者招聘 | shanghai-shegong |
| 2026-05-20-guangdong-shegong-zhaopin-2026.md | 广东社区工作者招聘 | shanghai-shegong |
| 2026-05-20-shegong-zheng-nankao-ma.md | 社工证难考吗 | beikao-zhinan |

**执行步骤结果**：
1. ✅ 读取关键词池（keywords_pool.md）
2. ✅ 生成4篇新文章（地域类P3词 + 社工证question词）
3. ✅ frontmatter 校验通过（validator --fix，0个问题）
4. ✅ git commit 完成（commit: 5d2ddd7）
5. ✅ git push 完成（origin/main 已同步）

---

### 2026-05-19 08:00 执行

**状态**：文章已生成并提交，push 待重试

**生成文章（8篇）**：
（见2026-05-19记忆）
