# 关键词池 | 公考SEO内容策略

> 本文件是自动化发文的关键词来源库
> 每天生成100篇文章，从「未覆盖」列表中选取关键词
> 支持关键词多角度复用（同一关键词可通过不同地域/年份/角度生成多篇文章）

---

## 📌 使用说明

### 文件格式
```yaml
- keyword: 关键词名称
  priority: P0/P1/P2/P3  (P0最高)
  type: question|compare|study|info|guide
  covered: true/false
  note: 备注
  angles: [角度1, 角度2, ...]  # 可选，同一关键词的不同写作角度
```

### 优先级定义
| 等级 | 含义 | 策略 |
|------|------|------|
| P0 | 核心词 | 必须覆盖，优先生成 |
| P1 | 高价值 | 重点覆盖 |
| P2 | 中价值 | 常规覆盖 |
| P3 | 长尾补充 | 有空再做 |

### 类型定义
| 类型 | 特点 | SEO适配 |
|------|------|----------|
| question | 问题型 | 天然适配，直接回答 |
| compare | 对比型 | 竞争度低，精准获客 |
| study | 备考型 | 转化意图强 |
| info | 资讯型 | 流量入口 |
| guide | 指南型 | 长期排名价值大 |

### 角度轮换策略
同一关键词可通过以下维度生成差异化文章：
- **地域变体**：上海/北京/广州/深圳/杭州/成都/武汉/南京/天津/重庆
- **年份变体**：2024年/2025年/2026年/最新
- **人群变体**：零基础/大专/非专业/宝妈/应届生/社会人员
- **场景变体**：一次通过/高分技巧/速成/系统备考/冲刺
- **科目变体**：行测/申论/公基/面试/笔试
- **问题变体**：怎么准备/用什么书/要多久/难不难/有前途吗

---

## P0 - 核心关键词（必须覆盖）

### 社区工作者通用
```yaml
- keyword: 社区工作者招聘
  priority: P0
  type: info
  covered: true
  note: 核心流量词
  angles: [2026年最新, 各地汇总, 报名人数统计, 招聘条件变化, 什么时候出公告]

- keyword: 社区工作者考试
  priority: P0
  type: info
  covered: true
  note: 核心流量词
  angles: [2026年考试安排, 各省考试时间, 考试大纲变化, 考试难度分析, 通过率统计]

- keyword: 社区工作者报名
  priority: P0
  type: info
  covered: true
  note: 报名阶段流量大
  angles: [报名入口汇总, 报名时间安排, 报名条件详解, 报名常见问题, 报名流程图解]

- keyword: 社区工作者待遇
  priority: P0
  type: info
  covered: true
  note: 学员刚需问题
  angles: [工资构成, 五险一金, 各地待遇对比, 福利待遇, 薪资增长机制]
```

### 上海社工专项
```yaml
- keyword: 上海社区工作者招聘
  priority: P0
  type: info
  covered: true
  note: 本项目核心词
  angles: [2026年公告, 历年招聘情况, 各区招聘汇总, 报名条件, 招聘人数]

- keyword: 上海社工考试
  priority: P0
  type: info
  covered: true
  angles: [2026年考试大纲, 考试科目, 考试时间, 考试地点, 合格分数线]

- keyword: 上海社区工作者报名
  priority: P0
  type: info
  covered: true
  angles: [报名入口, 报名时间, 报名流程, 报名条件, 常见问题解答]
```

---

## P1 - 高价值关键词（重点覆盖）

### 考试内容类
```yaml
- keyword: 社区工作者考试内容
  priority: P1
  type: info
  covered: true
  angles: [各省市对比, 2026年新变化, 笔试内容, 面试内容, 复习重点]

- keyword: 社区工作者考什么
  priority: P1
  type: question
  covered: true
  angles: [零基础版, 大纲解读, 重点科目, 各地差异, 最新变化]

- keyword: 社区工作者笔试考什么
  priority: P1
  type: question
  covered: true
  angles: [题型分析, 分值分布, 各科目详解, 难点剖析, 备考重点]

- keyword: 社区工作者面试内容
  priority: P1
  type: info
  covered: true
  angles: [常见题型, 考察要点, 评分标准, 答题技巧, 注意事项]

- keyword: 社区工作者笔试科目
  priority: P1
  type: info
  covered: true
  angles: [行测, 公共基础知识, 申论写作, 社区专业知识, 各地差异]

- keyword: 社区工作者考试题型
  priority: P1
  type: info
  covered: true
  angles: [选择题, 判断题, 简答题, 案例分析, 论述题]

- keyword: 社区工作者用什么书
  priority: P1
  type: question
  covered: true
  angles: [教材推荐, 真题推荐, 题库推荐, 网课推荐, 备考资料清单]

- keyword: 社区工作者考试题型
  priority: P1
  type: info
  covered: true
  angles: [选择题, 判断题, 简答题, 案例分析, 论述题]

- keyword: 社区工作者考试范围
  priority: P1
  type: info
  covered: false
  angles: [考试大纲, 知识点分布, 重点章节, 命题规律, 复习范围]
```

### 报名条件类
```yaml
- keyword: 社区工作者报名条件
  priority: P1
  type: info
  covered: true
  angles: [各地条件对比, 2026年新规定, 学历要求, 年龄要求, 户籍要求]

- keyword: 社区工作者报考要求
  priority: P1
  type: info
  covered: true
  angles: [基本条件, 特殊要求, 学历要求, 专业限制, 各地差异]

- keyword: 社区工作者学历要求
  priority: P1
  type: question
  covered: true
  angles: [大专可以考吗, 本科要求吗, 成人学历可以吗, 非全日制学历, 各地学历要求]

- keyword: 社区工作者年龄限制
  priority: P1
  type: question
  covered: true
  angles: [最大年龄, 最小年龄, 年龄放宽政策, 各地差异, 超龄怎么办]

- keyword: 社区工作者专业要求
  priority: P1
  type: question
  covered: true
  angles: [不限专业, 社会工作专业优先, 法学专业, 管理专业, 各地要求]

- keyword: 社区工作者户籍要求
  priority: P1
  type: question
  covered: false
  angles: [本地户籍, 外地人可以考吗, 户籍放宽政策, 各地规定, 居住证行吗]
```

### 备考规划类
```yaml
- keyword: 社区工作者备考攻略
  priority: P1
  type: guide
  covered: true
  angles: [三个月计划, 零基础版, 冲刺版, 高分攻略, 上岸经验]

- keyword: 社区工作者复习计划
  priority: P1
  type: guide
  covered: true
  angles: [一个月计划, 三个月计划, 半年计划, 每日时间安排, 复习进度表]

- keyword: 社工考试多久开始准备
  priority: P1
  type: question
  covered: true
  angles: [零基础版, 在职版, 全职版, 各科目分配时间, 最佳备考时机]

- keyword: 社区工作者用什么书
  priority: P1
  type: question
  covered: true
  angles: [教材推荐, 真题推荐, 题库推荐, 网课推荐, 备考资料清单]

- keyword: 社区工作者网课推荐
  priority: P1
  type: info
  covered: false
  angles: [免费网课, 付费网课, 行测网课, 申论网课, 面试网课]

- keyword: 社区工作者培训班
  priority: P1
  type: info
  covered: false
  angles: [线下班, 线上班, 培训费用, 培训效果, 如何选择]
```

---

## P2 - 中价值关键词（常规覆盖）

### 考试流程类
```yaml
- keyword: 社区工作者考试流程
  priority: P2
  type: guide
  covered: true
  angles: [完整流程图, 各地流程差异, 时间节点, 注意事项, 常见问题]

- keyword: 社工招聘报名流程
  priority: P2
  type: guide
  covered: true
  angles: [网上报名, 现场确认, 资格审查, 报名材料, 各地流程差异]

- keyword: 社区工作者准考证打印
  priority: P2
  type: info
  covered: false
  angles: [打印时间, 打印入口, 注意事项, 准考证信息, 遗失补办]

- keyword: 社区工作者成绩查询
  priority: P2
  type: info
  covered: false
  angles: [查询入口, 查询时间, 成绩有效期, 分数线, 成绩复核]

- keyword: 社区工作者面试流程
  priority: P2
  type: guide
  covered: false
  angles: [签到抽签, 答题环节, 计分方式, 面试时间, 注意事项]

- keyword: 社区工作者体检标准
  priority: P2
  type: info
  covered: false
  angles: [体检项目, 合格标准, 体检时间, 特殊情况, 常见问题]

- keyword: 社区工作者政审要求
  priority: P2
  type: info
  covered: false
  angles: [政审内容, 政审流程, 不合格情况, 家庭成员影响, 各地标准]
```

### 真题资料类
```yaml
- keyword: 社区工作者真题
  priority: P2
  type: info
  covered: true
  note: 注意版权
  angles: [2025年真题, 2024年真题, 各省市真题, 免费下载, 真题解析]

- keyword: 社区工作者笔试题库
  priority: P2
  type: info
  covered: false
  angles: [在线刷题, 题库推荐, 免费题库, 分模块练习, 错题整理]

- keyword: 社工考试真题答案
  priority: P2
  type: question
  covered: false
  angles: [2025年答案, 参考答案, 评分标准, 答案解析, 争议题]

- keyword: 社区工作者模拟题
  priority: P2
  type: info
  covered: false
  angles: [模拟卷推荐, 在线模考, 预测卷, 模拟评分, 模考分析]

- keyword: 社区工作者历年分数线
  priority: P2
  type: info
  covered: true
  angles: [各地分数线, 进面分数线, 笔试分数线, 近三年趋势, 各区分数线]
```

### 面试相关
```yaml
- keyword: 社区工作者面试技巧
  priority: P2
  type: guide
  covered: true
  angles: [开场白技巧, 答题框架, 语言表达, 仪态仪表, 加分技巧]

- keyword: 社区工作者面试题
  priority: P2
  type: info
  covered: true
  angles: [常见面试题, 历年面试题, 情景模拟题, 综合分析题, 人际关系题]

- keyword: 社工面试一般问什么
  priority: P2
  type: question
  covered: false
  angles: [自我介绍, 岗位认知, 情景处理, 计划组织, 应急应变]

- keyword: 社区工作者面试自我介绍
  priority: P2
  type: guide
  covered: false
  angles: [模板范文, 注意事项, 一分钟版, 三分钟版, 亮点打造]

- keyword: 社区工作者面试着装
  priority: P2
  type: guide
  covered: false
  angles: [男生着装, 女生着装, 着装禁忌, 仪容仪表, 加分细节]

- keyword: 社区工作者无领导小组讨论
  priority: P2
  type: guide
  covered: false
  angles: [讨论流程, 发言技巧, 角色定位, 常见题目, 加分策略]
```

### 各省市专项（高流量地域）
```yaml
- keyword: 北京社区工作者招聘
  priority: P2
  type: info
  covered: true
  angles: [2026年公告, 报名条件, 薪资待遇, 考试科目, 上岸经验]

- keyword: 广州社区工作者招聘
  priority: P2
  type: info
  covered: true
  angles: [2026年公告, 各区招聘, 报名条件, 薪资待遇, 考试内容]

- keyword: 深圳社区工作者招聘
  priority: P2
  type: info
  covered: true
  angles: [2026年公告, 薪资水平, 报名条件, 考试内容, 竞争比]

- keyword: 杭州社区工作者招聘
  priority: P2
  type: info
  covered: false
  angles: [2026年公告, 各区招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 成都社区工作者招聘
  priority: P2
  type: info
  covered: false
  angles: [2026年公告, 招聘人数, 报名条件, 薪资待遇, 考试内容]

- keyword: 南京社区工作者招聘
  priority: P2
  type: info
  covered: false
  angles: [2026年公告, 各区招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 武汉社区工作者招聘
  priority: P2
  type: info
  covered: false
  angles: [2026年公告, 各区招聘, 报名条件, 薪资待遇, 考试内容]

- keyword: 天津社区工作者招聘
  priority: P2
  type: info
  covered: false
  angles: [2026年公告, 招聘人数, 报名条件, 薪资待遇, 考试信息]

- keyword: 重庆社区工作者招聘
  priority: P2
  type: info
  covered: false
  angles: [2026年公告, 各区招聘, 报名条件, 薪资待遇, 考试内容]

- keyword: 苏州社区工作者招聘
  priority: P2
  type: info
  covered: false
  angles: [2026年公告, 各区招聘, 报名条件, 薪资待遇, 考试信息]
```

### 薪资待遇类
```yaml
- keyword: 社区工作者工资多少
  priority: P2
  type: question
  covered: true
  angles: [各地对比, 2026年标准, 工资构成, 绩效奖金, 加班工资]

- keyword: 社区工作者五险一金
  priority: P2
  type: info
  covered: true
  angles: [缴纳标准, 公积金比例, 医保待遇, 养老保险, 各地差异]

- keyword: 社区工作者发展前景
  priority: P2
  type: info
  covered: true
  angles: [晋升路径, 职业发展, 转编机会, 长期前景, 行业趋势]

- keyword: 社区工作者稳定性
  priority: P2
  type: question
  covered: false
  angles: [合同制还是编制, 聘用期限, 辞退风险, 稳定性分析, 各地政策]
```

### 工作内容类
```yaml
- keyword: 社区工作者工作内容
  priority: P2
  type: info
  covered: true
  angles: [日常工作, 疫情防控, 矛盾调解, 便民服务, 网格化管理]

- keyword: 社区工作者每天做什么
  priority: P2
  type: question
  covered: true
  angles: [上班时间, 工作安排, 典型一天, 加班情况, 工作强度]

- keyword: 社区工作者岗位职责
  priority: P2
  type: info
  covered: true
  angles: [岗位分类, 职责清单, 考核标准, 问责情况, 各地差异]
```

---

## P3 - 长尾补充词（持续覆盖）

### 对比类
```yaml
- keyword: 社工和网格员区别
  priority: P3
  type: compare
  covered: false
  angles: [职责对比, 薪资对比, 发展前景, 考试难度, 如何选择]

- keyword: 社区工作者和辅警哪个好
  priority: P3
  type: compare
  covered: false
  angles: [薪资对比, 稳定性对比, 工作内容对比, 发展前景, 如何选择]

- keyword: 街道办和社区工作者区别
  priority: P3
  type: compare
  covered: false
  angles: [编制区别, 待遇区别, 晋升区别, 工作内容, 如何区分]

- keyword: 社工和社区志愿者区别
  priority: P3
  type: compare
  covered: false
  angles: [性质区别, 报酬区别, 权限区别, 工作内容, 如何选择]

- keyword: 社区工作者和事业单位区别
  priority: P3
  type: compare
  covered: false
  angles: [编制区别, 薪资区别, 稳定性, 考试难度, 如何选择]

- keyword: 社区工作者和公务员区别
  priority: P3
  type: compare
  covered: false
  angles: [编制区别, 待遇差距, 社会地位, 发展前景, 考试难度]

- keyword: 社区工作者和村官区别
  priority: P3
  type: compare
  covered: false
  angles: [工作地点, 待遇区别, 发展路径, 转编政策, 各自优势]

- keyword: 社会工作者和社区工作者区别
  priority: P3
  type: compare
  covered: false
  angles: [概念区别, 证书区别, 待遇区别, 职业前景, 如何选择]
```

### 零基础类
```yaml
- keyword: 零基础备考社区工作者
  priority: P3
  type: study
  covered: false
  angles: [备考计划, 学习方法, 重点科目, 时间安排, 上岸经验]

- keyword: 非专业可以考社工吗
  priority: P3
  type: question
  covered: false
  angles: [专业限制, 各地要求, 非专业备考方法, 成功率, 经验分享]

- keyword: 社工考试难不难
  priority: P3
  type: question
  covered: false
  angles: [难度分析, 各地难度对比, 通过率, 与公考难度对比, 如何应对]

- keyword: 大专可以考社区工作者吗
  priority: P3
  type: question
  covered: false
  angles: [各地学历要求, 大专岗位, 成人学历, 提升学历, 经验分享]

- keyword: 社区工作者需要证书吗
  priority: P3
  type: question
  covered: false
  angles: [社工证, 初级社工证, 中级社工证, 证书含金量, 如何考取]

- keyword: 应届生可以考社区工作者吗
  priority: P3
  type: question
  covered: false
  angles: [应届生优势, 报名条件, 岗位选择, 备考建议, 经验分享]

- keyword: 宝妈可以考社区工作者吗
  priority: P3
  type: question
  covered: false
  angles: [宝妈优势, 备考时间, 工作与家庭平衡, 岗位选择, 经验分享]
```

### 薪资待遇详细类
```yaml
- keyword: 上海社工薪资待遇
  priority: P3
  type: info
  covered: false
  angles: [工资构成, 各区待遇, 年终奖, 五险一金, 涨薪机制]

- keyword: 社区工作者年终奖
  priority: P3
  type: question
  covered: false
  angles: [各地标准, 发放时间, 考核标准, 绩效奖金, 福利补贴]

- keyword: 社区工作者有编制吗
  priority: P3
  type: question
  covered: false
  angles: [编制情况, 合同制, 转编政策, 各地政策, 未来趋势]

- keyword: 社区工作者能转编制吗
  priority: P3
  type: question
  covered: false
  angles: [转编条件, 转编渠道, 各地政策, 成功案例, 如何准备]

- keyword: 社区工作者有寒暑假吗
  priority: P3
  type: question
  covered: false
  angles: [休假制度, 法定假日, 年假制度, 加班情况, 各地差异]
```

### 工作体验类
```yaml
- keyword: 社区工作者工作强度
  priority: P3
  type: question
  covered: false
  angles: [加班情况, 工作压力, 网格员工作, 疫情期间, 各地差异]

- keyword: 社区工作者好考吗
  priority: P3
  type: question
  covered: false
  angles: [通过率, 竞争比, 各地难度, 与公考对比, 备考建议]

- keyword: 社区工作者上岸经验
  priority: P3
  type: study
  covered: false
  angles: [零基础上岸, 一个月上岸, 高分经验, 面试逆袭, 各地经验]

- keyword: 社区工作者值得考吗
  priority: P3
  type: question
  covered: false
  angles: [优缺点分析, 适合人群, 职业规划, 长期发展, 各地情况]

- keyword: 社区工作者辞职多吗
  priority: P3
  type: question
  covered: false
  angles: [离职率, 辞职原因, 工作压力, 职业发展, 各地情况]

- keyword: 社区工作者可以兼职吗
  priority: P3
  type: question
  covered: false
  angles: [相关规定, 兼职限制, 副业可能, 各地政策, 风险提示]
```

### 地域类长尾词
```yaml
- keyword: 山东社区工作者考试
  priority: P3
  type: info
  covered: false
  angles: [2026年安排, 报名条件, 考试科目, 各市招聘, 备考经验]

- keyword: 河南社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 江苏社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 浙江社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 广东社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 四川社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 湖北社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 湖南社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 福建社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 安徽社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 河北社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 辽宁社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 陕西社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 江西社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 云南社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 贵州社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 黑龙江社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 吉林社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 山西社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]

- keyword: 广西社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 各市招聘, 报名条件, 薪资待遇, 考试信息]
```

### 行测申论专项
```yaml
- keyword: 社区工作者行测怎么复习
  priority: P3
  type: guide
  covered: false
  angles: [零基础版, 高分技巧, 速成方法, 重点模块, 题型分析]

- keyword: 社区工作者申论怎么写
  priority: P3
  type: guide
  covered: false
  angles: [写作模板, 高分范文, 常见话题, 答题技巧, 评分标准]

- keyword: 社区工作者公共基础知识
  priority: P3
  type: info
  covered: false
  angles: [考试范围, 重点知识, 考点梳理, 备考方法, 常考内容]

- keyword: 社区工作者数量关系技巧
  priority: P3
  type: guide
  covered: false
  angles: [速算技巧, 常考题型, 解题方法, 高分策略, 易错点]

- keyword: 社区工作者言语理解技巧
  priority: P3
  type: guide
  covered: false
  angles: [阅读理解, 逻辑填空, 语句排序, 高分策略, 常见陷阱]

- keyword: 社区工作者判断推理技巧
  priority: P3
  type: guide
  covered: false
  angles: [图形推理, 逻辑判断, 定义判断, 类比推理, 解题技巧]

- keyword: 社区工作者资料分析技巧
  priority: P3
  type: guide
  covered: false
  angles: [速算方法, 常考图表, 解题步骤, 高分策略, 时间分配]

- keyword: 社区工作者常识判断
  priority: P3
  type: info
  covered: false
  angles: [时政热点, 法律常识, 历史文化, 地理科技, 备考范围]
```

### 政策时事类
```yaml
- keyword: 社区工作者新政策2026
  priority: P3
  type: info
  covered: false
  angles: [国家政策, 地方政策, 薪资调整, 编制改革, 发展趋势]

- keyword: 社区工作者职业化改革
  priority: P3
  type: info
  covered: false
  angles: [改革方向, 政策解读, 影响分析, 各地进展, 未来趋势]

- keyword: 社区工作者薪酬改革
  priority: P3
  type: info
  covered: false
  angles: [改革内容, 薪资变化, 各地标准, 实施进展, 影响分析]

- keyword: 社区工作者持证上岗
  priority: P3
  type: info
  covered: false
  angles: [政策要求, 证书类型, 考取方法, 各地进展, 过渡期安排]
```

### 国考省考相关（交叉流量）
```yaml
- keyword: 国考和社区工作者哪个好
  priority: P3
  type: compare
  covered: false
  angles: [待遇对比, 难度对比, 发展前景, 稳定性, 如何选择]

- keyword: 省考和社区工作者哪个好
  priority: P3
  type: compare
  covered: false
  angles: [待遇对比, 难度对比, 备考成本, 发展前景, 如何选择]

- keyword: 社区工作者和三支一扶区别
  priority: P3
  type: compare
  covered: false
  angles: [性质区别, 待遇区别, 服务期, 转编政策, 如何选择]

- keyword: 社区工作者和特岗教师区别
  priority: P3
  type: compare
  covered: false
  angles: [工作内容, 待遇对比, 发展前景, 转编政策, 各自优势]
```

### 社工证相关
```yaml
- keyword: 初级社工证报考条件
  priority: P3
  type: info
  covered: false
  angles: [学历要求, 工作年限, 专业要求, 报名时间, 考试科目]

- keyword: 中级社工证报考条件
  priority: P3
  type: info
  covered: false
  angles: [学历要求, 工作年限, 专业要求, 报名时间, 考试科目]

- keyword: 社工证难考吗
  priority: P3
  type: question
  covered: false
  angles: [通过率, 难度分析, 备考时间, 各科难度, 如何应对]

- keyword: 社工证含金量
  priority: P3
  type: question
  covered: false
  angles: [证书价值, 薪资补贴, 职业发展, 各地政策, 值得考吗]

- keyword: 社工证考试时间2026
  priority: P3
  type: info
  covered: false
  angles: [考试安排, 报名时间, 各科目时间, 成绩公布, 注意事项]

- keyword: 社工证怎么复习
  priority: P3
  type: guide
  covered: false
  angles: [复习计划, 学习方法, 重点章节, 真题练习, 高分经验]
```

### 各城市社工考试专项（更多地域）
```yaml
- keyword: 青岛社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 大连社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 宁波社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 厦门社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 长沙社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 郑州社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 西安社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 合肥社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 济南社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 沈阳社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 哈尔滨社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 长春社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 昆明社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 南昌社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]

- keyword: 福州社区工作者招聘
  priority: P3
  type: info
  covered: false
  angles: [2026年公告, 报名条件, 薪资待遇, 考试信息, 竞争比]
```

### 高频问题类
```yaml
- keyword: 社区工作者上班时间
  priority: P3
  type: question
  covered: false
  angles: [朝九晚五, 周末休息, 加班情况, 值班安排, 各地差异]

- keyword: 社区工作者考试报名费
  priority: P3
  type: question
  covered: false
  angles: [各地费用, 免费政策, 缴费方式, 退费政策, 注意事项]

- keyword: 社区工作者政审严格吗
  priority: P3
  type: question
  covered: false
  angles: [政审内容, 审查标准, 不合格案例, 各地差异, 如何自查]

- keyword: 社区工作者要考几次
  priority: P3
  type: question
  covered: false
  angles: [考试频次, 各地安排, 一年几次, 报名次数限制, 备考周期]

- keyword: 社区工作者有效期几年
  priority: P3
  type: question
  covered: false
  angles: [聘用期限, 合同续签, 考核标准, 期满政策, 各地规定]

- keyword: 社区工作者退休待遇
  priority: P3
  type: question
  covered: false
  angles: [退休年龄, 养老保险, 退休金水平, 与编制差异, 各地标准]

- keyword: 社区工作者可以考公务员吗
  priority: P3
  type: question
  covered: false
  angles: [在岗期间, �基层工作经验, 岗位选择, 备考时间, 经验分享]

- keyword: 社区工作者试用期多久
  priority: P3
  type: question
  covered: false
  angles: [试用期长度, 试用期待遇, 考核标准, 转正条件, 各地规定]
```

---

## 动态关键词池（招聘公告触发）

> 以下关键词由 wx-monitor 监测到公众号文章时自动触发
> 不走静态生成队列，实时性优先

```yaml
# 公告发布阶段
- keyword: 招聘公告
  trigger: ["公告", "招聘", "报名"]
  template: 公告解读

- keyword: 报名通知
  trigger: ["报名", "通知"]
  template: 报名攻略

# 报名阶段
- keyword: 报名入口
  trigger: ["报名", "入口", "网址"]
  template: 报名指南

- keyword: 报名时间
  trigger: ["报名", "时间", "截止"]
  template: 报名提醒

# 准考证阶段
- keyword: 准考证打印
  trigger: ["准考证", "打印", "领取"]
  template: 打印指南

# 笔试阶段
- keyword: 笔试时间
  trigger: ["笔试", "时间", "地点"]
  template: 笔试提醒

- keyword: 笔试内容
  trigger: ["笔试", "科目", "范围"]
  template: 备考指导

# 成绩阶段
- keyword: 笔试成绩
  trigger: ["成绩", "查询", "公布"]
  template: 成绩查询

- keyword: 进面分数
  trigger: ["分数", "合格", "分数线"]
  template: 分数线分析

# 面试阶段
- keyword: 面试名单
  trigger: ["面试", "名单", "公示"]
  template: 名单汇总

- keyword: 面试时间
  trigger: ["面试", "时间", "安排"]
  template: 面试准备
```

---

## 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-05-15 | 大规模扩充关键词池：从40个扩展到150+，新增angles字段支持角度轮换，新增地域词、社工证、行测申论专项、高频问题等类别 |
| 2026-04-29 | 初始版本建立 |
