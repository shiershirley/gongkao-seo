# 关键词池 | 公考SEO内容策略

> 本文件是自动化发文的关键词来源库
> 静态内容生成时，从「未覆盖」列表中选取关键词
> 动态内容（招聘公告类）单独处理，不走此池

---

## 📌 使用说明

### 文件格式
```yaml
- keyword: 关键词名称
  priority: P0/P1/P2/P3  (P0最高)
  type: question|compare|study|info|guide
  covered: true/false
  note: 备注
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

---

## P0 - 核心关键词（必须覆盖）

### 社区工作者相关
```yaml
- keyword: 社区工作者招聘
  priority: P0
  type: info
  covered: false
  note: 核心流量词，泛指

- keyword: 社区工作者考试
  priority: P0
  type: info
  covered: false
  note: 核心流量词

- keyword: 社区工作者报名
  priority: P0
  type: info
  covered: false
  note: 报名阶段流量大

- keyword: 社区工作者待遇
  priority: P0
  type: info
  covered: false
  note: 学员刚需问题
```

### 上海社工专项
```yaml
- keyword: 上海社区工作者招聘
  priority: P0
  type: info
  covered: false
  note: 本项目核心词

- keyword: 上海社工考试
  priority: P0
  type: info
  covered: false
  note: 上海专属词

- keyword: 上海社区工作者报名
  priority: P0
  type: info
  covered: false
  note: 上海报名节点
```

---

## P1 - 高价值关键词（重点覆盖）

### 考试内容类
```yaml
- keyword: 社区工作者考试内容
  priority: P1
  type: info
  covered: false
  note: 备考基础问题

- keyword: 社区工作者考什么
  priority: P1
  type: question
  covered: false
  note: 问题型，高搜索量

- keyword: 社区工作者笔试考什么
  priority: P1
  type: question
  covered: false
  note: 细化版本

- keyword: 社区工作者面试内容
  priority: P1
  type: info
  covered: false
  note: 面试备考
```

### 报名条件类
```yaml
- keyword: 社区工作者报名条件
  priority: P1
  type: info
  covered: false
  note: 高频问题

- keyword: 社区工作者报考要求
  priority: P1
  type: info
  covered: false
  note: 同义词

- keyword: 社区工作者学历要求
  priority: P1
  type: question
  covered: false
  note: 常见问题

- keyword: 社区工作者年龄限制
  priority: P1
  type: question
  covered: false
  note: 常见问题
```

### 备考规划类
```yaml
- keyword: 社区工作者备考攻略
  priority: P1
  type: guide
  covered: false
  note: 备考综合指南

- keyword: 社区工作者复习计划
  priority: P1
  type: guide
  covered: false
  note: 学习规划

- keyword: 社工考试多久开始准备
  priority: P1
  type: question
  covered: false
  note: 备考时间问题
```

---

## P2 - 中价值关键词（常规覆盖）

### 考试流程类
```yaml
- keyword: 社区工作者考试流程
  priority: P2
  type: guide
  covered: false

- keyword: 社工招聘报名流程
  priority: P2
  type: guide
  covered: false

- keyword: 社区工作者准考证打印
  priority: P2
  type: info
  covered: false
  note: 考前节点

- keyword: 社区工作者成绩查询
  priority: P2
  type: info
  covered: false
  note: 考后节点
```

### 真题资料类
```yaml
- keyword: 社区工作者真题
  priority: P2
  type: info
  covered: false
  note: 流量入口，注意版权

- keyword: 社区工作者笔试题库
  priority: P2
  type: info
  covered: false

- keyword: 社工考试真题答案
  priority: P2
  type: question
  covered: false
```

### 面试相关
```yaml
- keyword: 社区工作者面试技巧
  priority: P2
  type: guide
  covered: false

- keyword: 社区工作者面试题
  priority: P2
  type: info
  covered: false

- keyword: 社工面试一般问什么
  priority: P2
  type: question
  covered: false
```

---

## P3 - 长尾补充词（有空覆盖）

### 对比类
```yaml
- keyword: 社工和网格员区别
  priority: P3
  type: compare
  covered: false
  note: 对比词，竞争度低

- keyword: 社区工作者和辅警哪个好
  priority: P3
  type: compare
  covered: false

- keyword: 街道办和社区工作者区别
  priority: P3
  type: compare
  covered: false

- keyword: 社工和社区志愿者区别
  priority: P3
  type: compare
  covered: false
```

### 零基础类
```yaml
- keyword: 零基础备考社区工作者
  priority: P3
  type: study
  covered: false

- keyword: 非专业可以考社工吗
  priority: P3
  type: question
  covered: false

- keyword: 社工考试难不难
  priority: P3
  type: question
  covered: false
```

### 薪资待遇类
```yaml
- keyword: 社区工作者工资多少
  priority: P3
  type: question
  covered: false

- keyword: 上海社工薪资待遇
  priority: P3
  type: info
  covered: false

- keyword: 社区工作者年终奖
  priority: P3
  type: question
  covered: false
```

### 工作内容类
```yaml
- keyword: 社区工作者工作内容
  priority: P3
  type: info
  covered: false

- keyword: 社区工作者每天做什么
  priority: P3
  type: question
  covered: false

- keyword: 社工岗位工作强度
  priority: P3
  type: question
  covered: false
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
| 2026-04-29 | 初始版本建立 |
