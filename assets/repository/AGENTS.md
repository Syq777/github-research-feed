# 维护这个研究仓库

先读 site.json、topics/、catalog/、editorial/、editions/、research/ 和 state/，按 github-research-feed Skill 维护。

若存在 sources/主题.json，先运行 poll_sources.py 轮询所有登记动态源，记录失败和限制，不能找到十篇就停。查看各领域 Top 20 和完整池，比较候选并读入围原文；在 research/reviews 保存逐源筛查方法、入选/落选理由与 poll 指纹。机器链接初筛不等于精读。daily_brief.require_source_review 开启时，缺失覆盖记录会阻止生成新一期。每期有自然名字和 3–5 个具体关键词，digest.py 用 --name 和 --keywords 传入，名字体现实际条数。

启用 daily_brief 时，首页与 RSS 发布每日精选，原始抓取和来源目录放在 archive.html。只运行 python3 update.py 不会生成新一期。制作新一期需实际阅读原文，核对首次发布日期，补齐 headline、summary、why_read、kind、score、event_id、reviewed_at，并运行 python3 digest.py --date YYYY-MM-DD --lead '本期导读'。

默认最多 10 篇。按周而非每日固定配额看均衡：balance.py 查看近七天的领域、形式、来源及近四周覆盖，weeks/ 中记录有证据的当周重点，文章标注 domain。同等质量时补近期缺少的视角；允许不同周重点不同，不机械轮换或凑数。论文三成是滚动参考，每日不超过实际条数四成。从完整 catalog 发现线索，周重点不缩小轮询范围。同一事件和过去七天已选文章不重复。概要与阅读理由互补，无新一期保留原日期。

修改前在干净工作树 git pull --ff-only，保留用户未提交改动。发布授权以当前用户会话为准，已有授权继续有效。运行测试、构建，检查 public/status.json、首页和 feed.xml，只提交本次相关文件，跟到 Pages 部署成功并验证实际网址。本地离线检查用 python3 update.py --offline，不能视作网络或部署验证。
