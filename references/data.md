# 资料格式

同一个研究仓库使用一个稳定主题 ID。以下示例的占位地址仅用于解释字段，实际收录时必须替换并核对。

| 文件 | 单条数据及处理 |
| --- | --- |
| site.json | `{"topic":"harness"}`，本仓库主题 |
| topics/harness.json | `id`、`title`、`description`、`keywords`、`sources`、`catalog`；每个订阅源含 `id,name,url,feed,filter`。url 是入口，feed 是经验证的 RSS/Atom 地址 |
| catalog/harness.json | 数组，每条含 `group,topic,name,url,note`。group 为大类、topic 为小类；概括性渠道可使用空 url |
| editorial/harness.json | 数组，每条含 `title,url,date,source,source_id,summary`。date 取自原始来源，支持 YYYY-MM-DD 或有时区的 ISO 日期时间；source_id 为稳定小写短名，可来自无 feed 的出版者 |
| research/ | Markdown 调研笔记、查询范围、日期、引文与待核问题 |
| state/harness.json | 更新器合并维护的有限字段历史记录；人工修订优先写 editorial |
| public/ | 网页、聚合 RSS、上游 OPML 和逐源抓取状态 |

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
