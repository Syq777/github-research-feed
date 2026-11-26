# 来源轮询与选稿

首页只有十条，后台检索不能在十条时停止。Top 20 指每个内容领域的重点来源，不是每个领域每日发二十篇，也不是最多访问二十个来源。

## 来源池

`sources/<主题>.json` 保存 sources 与 domains。每个 domain 的 top20 是有顺序的 source_id 和推荐理由；同源跨领域只请求一次。来源 mode 为 html、feed、manual 或 reference。动态公开入口每天尝试；manual 无具体地址时记录未配置，不能假装已访问；单篇经典论文、书籍与资料工具列为 reference，保留在全表，不能当每日新内容生产者。首次和定期全目录检查可用 `--audit-all`。

重要性与可访问性分别判断：5 核心、4 高、3 中、2 补充、1 背景或工具。数字是主题监测优先级，不是客观学术排名。Top 20 的次序依据主题相关性、一手信息、持续产出及信息增量；不要因容易抓到就提高论文聚合器的重要性。

## 完整一轮

1. 查看当日本地日期、已有期刊与远端部署。若同日已完整发布且没有新的修订请求，只检查健康，不重复编一期。
   每日先运行 balance.py 查看近七天领域/形式/来源和近四周覆盖。每周维护 weeks/YYYY-Www-主题.json：week 为 ISO 周（如 2026-W48），focus_domains 为零至两个领域 ID，reason 写近期缺口和当周证据。六个 ID 为 methods、engineering、science、safety、industry、perspectives。不要固定每天同一比例，也不要为补配额降低质量；重点只影响比较排序，不缩小轮询范围。require_week_plan 开启后新周不能沿用旧周计划。
2. 运行 `python3 poll_sources.py --date YYYY-MM-DD`。它尝试全部动态来源，写 `research/polls/日期-主题.json`；无“够十篇就退出”的逻辑。公开页面、RSS、PDF、登录/订阅提示、403/限流、动态渲染和错误分别记录。HTTP 200 不等于读到全文，关键词未命中不等于源没有新内容。
3. 查看六个领域的来源结果与全部候选链接，过滤导航、过期、重复与弱相关材料。重点源只取到空壳、首页导航或受限时，通过正常浏览/检索寻找公开入口；不绕过付费与登录。必要时修正 poll_url，并重新轮询。保留失败证据。
4. 保存 `research/reviews/日期-主题.json`。`poll_sha256` 必须是 `poll_sources.fingerprint(poll)`；`source_reviews` 覆盖所有动态和 manual 源，每项有 source_id、decision（candidates/no_relevant/unavailable）、method、note。机器筛查要写 listing_keyword_screen，不能冒充人工精读。
5. `candidates` 记录已比较的文章，每项有 url、title、decision（shortlist/exclude）、evidence_level（listing/full_text/abstract/transcript）、reason、reviewed_at。通常至少 30 条，实际不足写 shortfall_reason；不要拿无关链接凑数。列表级判断可用于排除，入围必须读到原文、论文摘要或访谈文字稿。给取舍理由，不要只复述标题。
6. 完成 editorial 的中文概要与阅读理由，再运行带 name、keywords、lead 的 digest.py。启用 daily_brief.require_source_review 时，未完成全池检查、引用旧轮询、重复候选或只看列表就入围，都会阻止生成一期。
7. 构建网站、跑相关测试、按已有授权提交发布，核验线上首页、RSS、sources.html 与 sources.csv。生成表显示全部条目的重要性和实际访问结果；公开页面可读与全文免费不能混写。

`sources/access-notes.json` 可补充人工核实的权限说明，每项附 access 和 evidence URL。403 或超时不能推断为需要付费。已有付费账号也不意味着获得绕过访问限制的授权。

原始轮询、机器初筛、候选比较、精读和最终入选是不同数量，分别报告。日报不必在首页展示所有来源，但维护者应能追查这十条从何而来、什么没查到。
