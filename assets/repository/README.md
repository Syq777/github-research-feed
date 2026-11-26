# 主题研究仓库

主题名称和说明位于 topics/，启用的主题 ID 在 site.json。每日精选模式用中文概要和一句阅读理由帮助读者选文章；默认每天最多 10 篇，论文目标三成、最多四成，其他名额按当日内容调整。完整来源与原始采集保留在次级归档。未启用 daily_brief 的主题沿用普通聚合模式。

| 路径 | 内容 |
| --- | --- |
| topics/ | 主题范围、关键词和已验证的上游订阅地址 |
| catalog/ | 按大类、小类整理的完整来源目录，包括需要人工查阅的来源 |
| research/ | 有出处的调研记录、覆盖情况和待查问题 |
| editorial/ | 经核对的公开条目，每条有标题、原文地址、原始发布日期、来源、来源 ID 与短摘要 |
| editions/ | 每日精选快照，保留当日中文标题、概要、阅读理由及原文信息 |
| state/ | 历次获取和精选条目的累计索引，以规范化原文地址去重 |
| public/ | 精选 index.html、issues/ 往期、archive.html 候选及目录、feed.xml、feeds.opml、status.json |
| .github/workflows/research-feed.yml | 每日、手动和默认分支相关改动触发的构建发布流程 |

## 本地检查

使用 Python 3.10+ 和 Linux 或 macOS。每日模式先按 github-research-feed Skill 读原文、补齐 editorial 的中文 headline、summary、why_read、kind、score、event_id 和 reviewed_at，执行 `python3 digest.py --date YYYY-MM-DD --lead '本期导读'`。运行 `python3 -B -m unittest discover -s tests`，再运行 `python3 update.py` 构建。后者只刷新候选和渲染既有期刊，不会生成新一期。离线预览用 `python3 update.py --offline`。在仓库根目录运行 `python3 -m http.server 8000 --directory public`，打开 http://localhost:8000/ 。本地预览地址只供本机使用。线上构建从 Pages 配置读取实际网址及项目路径。

## GitHub 上自动更新

将本仓库的文件提交到 GitHub 默认分支，在 Settings → Pages → Build and deployment → Source 选择 GitHub Actions，并启用仓库的 Actions。工作流需要把 state/ 和 public/ 写回默认分支，仓库的工作流权限及分支规则须允许该写入。首次在 Actions → Update research feed → Run workflow 运行；之后每天 UTC 00:17（北京时间 08:17）触发，实际执行时间由 GitHub 调度。首次部署或故障恢复后，在 Actions 的部署环境或 Settings → Pages 查看真实网址，打开首页并校验其 RSS 链接。公开访问以仓库的 Pages 配置为准。

日常提问可以用「更新今天的精选，每篇有中文概要和阅读理由」。每日中文编辑需要模型：可以在用户同意后使用本机 Codex 自动化，无需另配 API，电脑需在线。GitHub 的定时抓取无需模型，但不会完成编辑；没有新一期时保留最近一期真实日期。人工检索从完整 catalog 扩展，不限于已接通的 RSS 域名。部分源失败时保留历史；全部已配置订阅同时失败则停止部署；没有 RSS 的主题可使用已核实的 editorial。

每日模式的 feed.xml 只含精选，最近至多 200 篇，带中文概要与阅读理由。feeds.opml 是未筛选的上游源集合，不能用它代替精选 RSS。历史候选在 state/，每日快照在 editions/。原文及第三方作品权利归相应权利人。

## 可选的 GitHub 托管 AI 调研

仓库持有人可以设置 Actions secret `OPENAI_API_KEY` 和仓库变量 `RESEARCH_MODEL` 启用带网页检索的候选发现。模型 ID 需要支持 Responses API 的 web search，调用计入该 API 账户。在 research/主题/ 下查看候选报告；每日模式仍需核实原文、补齐 editorial 并运行 digest.py。现有自动检索只使用配置中的来源域名和关键词，尚不是全自动中文编辑发布流程。
