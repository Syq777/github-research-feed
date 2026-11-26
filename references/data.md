# 资料格式

同一个研究仓库使用一个稳定主题 ID。以下示例的占位地址仅用于解释字段，实际收录时必须替换并核对。

| 文件 | 单条数据及处理 |
| --- | --- |
| site.json | `{"topic":"harness"}`，本仓库主题 |
| topics/harness.json | `id`、`title`、`description`、`keywords`、`sources`、`catalog`；每个订阅源含 `id,name,url,feed,filter`。url 是入口，feed 是经验证的 RSS/Atom 地址 |
| catalog/harness.json | 数组，每条含 `group,topic,name,url,note`。group 为大类、topic 为小类；概括性渠道可使用空 url |
| editorial/harness.json | 数组，每条含 `title,url,date,source,source_id,summary`。date 取自原始来源，支持 YYYY-MM-DD 或有时区的 ISO 日期时间；source_id 为稳定小写短名，可来自无 feed 的出版者 |
| editions/主题/YYYY-MM-DD.json | 每日精选快照：`topic,date,timezone,lead,items`。保留每篇当日的概要与推荐理由，不随未来 editorial 修改而改变 |
| research/ | Markdown 调研笔记、查询范围、日期、引文与待核问题 |
| sources/主题.json | 六个内容领域的 Top 20 与完整来源池；重要性与访问状态独立 |
| sources/access-notes.json | 经核对的登录/付费说明及 evidence 链接 |
| research/polls/ | 当日全池轮询、访问证据、列表链接、注册表指纹 |
| research/reviews/ | 逐源筛查方式、候选入选/落选理由、证据层级；链接初筛不等于原文精读 |
| weeks/YYYY-Www-主题.json | 当周零至两个重点领域 focus_domains、证据理由 reason、ISO 周 week；不会固定每日类别名额 |
| state/harness.json | 更新器合并维护的有限字段历史记录；人工修订优先写 editorial |
| public/ | 精选首页、issues/ 往期、archive.html 候选与目录、精选 RSS、上游 OPML 和逐源抓取状态。未启用每日模式时沿用普通聚合首页 |

## 一条真实的精选记录

```json
{
  "title": "Effective harnesses for long-running agents",
  "url": "https://www.anthropic.com/research/effective-harnesses-for-long-running-agents",
  "date": "2025-11-26",
  "source": "Anthropic Engineering",
  "source_id": "anthropic-engineering",
  "summary": "以跨上下文窗口开发应用为例，说明初始化智能体、功能清单、进度记录和端到端测试如何帮助后续智能体接手工作。"
}
```

## 调研笔记结构

- 问题与范围。写检索日期、考察时间窗和纳入标准。
- 主要发现。每项附原文标题、原始发表日期、直接链接和自己的摘要。若涉及可比较的实验，记下任务、条件与限制。
- 证据和解释。注明作者报告、独立验证或整理者推断。
- 待复查。列出尚未核实的信息，给下次调研留下具体入口。

预置 RSI 保留原分类目录里的材料条目和渠道。目录的计数包含论文、人物、机构与一般方法，不等于可自动订阅的独立站点数。

## 每日精选字段与配置

每日模式在基础 editorial 字段上补充以下字段。只有齐全且当日核对的条目才进入当日候选；没有 `headline` 的旧记录继续留在候选归档。

| 字段 | 含义 |
| --- | --- |
| headline | 中文阅读标题，1–100 字符；title 仍保存原文标题 |
| summary | 一两句具体概要，1–260 字符，不能直接留下长篇英文摘要 |
| why_read | 一句话阅读理由，1–180 字符，说明能带走什么，与概要互补 |
| kind | paper、engineering、research、assessment、perspective、podcast 中的一项 |
| domain | 内容领域：methods、engineering、science、safety、industry、perspectives；按文章内容判断，与 kind 独立 |
| score | 编辑对相关性和阅读价值的 1–5 分判断 |
| event_id | 稳定的事件 ID，同一成果的论文、博客和报道共用一个 ID |
| reviewed_at | 实际打开原文核对的本地日期 YYYY-MM-DD |

在 topics/主题.json 中设置：

```json
"daily_brief": {
  "size": 10,
  "paper_target": 0.3,
  "paper_max": 0.4,
  "recent_days": 14,
  "max_age_days": 30,
  "repeat_days": 7,
  "max_per_source": 3,
  "min_score": 3,
  "timezone": "Asia/Shanghai"
}
```

`digest.py --date YYYY-MM-DD --lead '本期导读'` 读取 editorial 和过去七天的 editions，按内容类型分配名额，缺少的类别让给其他内容，检查实际条数中的论文上限，然后保存快照。没有合格混合内容时返回失败并保留旧一期。`update.py` 只渲染既有 editions，不会生成中文或新日期。

启用 `daily_brief.require_source_review` 时，还需先完成全池 poll 和 review，再提供 `--name '包含条数的本期名字' --keywords 词一 词二 词三`。快照增加 name、keywords、coverage，记录来源检查数、比较候选数和精读数。完整约定见 [来源轮询与选稿](source-review.md)。

`daily_brief.require_week_plan` 要求当周计划。balance.py 汇总近七天与近四周阅读；选稿用有上限的软调整兼顾领域、形式、来源和当周重点，不给每天固定槽位。快照保存 weekly_focus 和 reading_history，便于回看当时的选择依据。历史条目缺少 domain 时暂按 kind 归类；新编辑应明确填写。

每日模式的 feed.xml 从精选快照产生，最近至多 200 篇，按原文 URL 去重。RSS pubDate 是该文入选的期刊日期，概要中另列原始发布日期；首页逐条展示原文日期。feeds.opml 仍是原始上游订阅，读者导入它会看到未筛选内容，不能用它代替精选 RSS。
