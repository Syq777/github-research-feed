# 维护这个研究仓库

先读 site.json、topics/、catalog/、editorial/、editions/、research/ 和 state/，按 github-research-feed Skill 维护。

启用 daily_brief 时，首页与 RSS 发布每日精选，原始抓取和来源目录放在 archive.html。只运行 python3 update.py 不会生成新一期。制作新一期需实际阅读原文，核对首次发布日期，补齐 headline、summary、why_read、kind、score、event_id、reviewed_at，并运行 python3 digest.py --date YYYY-MM-DD --lead '本期导读'。

默认最多 10 篇、论文目标 30% 且不超过实际条数的 40%；缺少的类型让给其他非论文内容，不凑数。从完整 catalog 发现线索，不限于 RSS 端点。同一事件和过去七天已选文章不重复。中文概要说明具体内容，阅读理由说明读者能带走什么；两者不要重复。无新一期保留原日期。

修改前在干净工作树 git pull --ff-only，保留用户未提交改动。发布授权以当前用户会话为准，已有授权继续有效。运行测试、构建，检查 public/status.json、首页和 feed.xml，只提交本次相关文件，跟到 Pages 部署成功并验证实际网址。本地离线检查用 python3 update.py --offline，不能视作网络或部署验证。
