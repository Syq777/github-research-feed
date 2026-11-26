# 在 GitHub 运行

## 第一次启用

发布前运行 `gh auth status`、`git status --short`、`git remote -v`，并检查 `git var GIT_AUTHOR_IDENT`。缺少提交身份时，优先沿用用户已有配置；确需补齐时只设置当前仓库的 `user.name` 和其 GitHub noreply 邮箱，不改全局身份。

1. 打开用户指定的 GitHub 研究仓库，在其 checkout 用本 Skill 初始化主题，将研究配置、代码及 workflow 提交至默认分支。若没有可写远端，先完成本地验证。
2. 在仓库 Settings → Pages → Build and deployment 选择 GitHub Actions，启用 Actions。workflow 需要把 state/ 与 public/ 写回默认分支；仓库的工作流权限和分支规则都要允许这项写入。如采用严格保护分支，先和维护者选定其允许的写入方式。
3. 在 Actions → Update research feed → Run workflow 运行默认分支，或使用 gh workflow run。完成后查看 github-pages 环境 URL，并实际打开站点及相对路径 feed.xml。GitHub 项目站的 URL 带仓库子路径，自定义域名使用 Pages 返回的 base_url。
4. 每天 UTC 00:17（北京时间 08:17）安排更新。默认分支上的相关配置或精选改动也触发构建。GitHub 可能延迟定时任务；检查最近成功的 workflow run。Fork 后需在自己的仓库启用 Actions 和 Pages。
5. 网页和 RSS 均直接发布 public/ 里的文件。历史归档以及对应发布版本可由仓库提交追溯。仓库内的 research/ 保留详细笔记，订阅读者收到 editorial/ 和订阅源里的条目。

具备权限且用户已要求发布时，可用 `gh api repos/OWNER/REPO/pages` 检查 Pages；仅在响应确认为 404、尚未启用时，用 `gh api --method POST repos/OWNER/REPO/pages -f build_type=workflow` 启用。已有 Pages 配置先核对，不覆盖现有域名或其他站点。首次推送工作流前启用 Pages，可避免 configure-pages 在未配置站点时失败。以返回的 `html_url` 作为本地构建的 `--site-url`；不用 localhost 版本代替线上产物。

发布后检查对应 commit 的 Actions 结果；远端工作流会自动提交 `state/`、`public/`、`research/`，再次修改前先在干净工作树执行 `git pull --ff-only`，避免本地提交落后而 push 被拒。用 HTTP GET 验证首页、feed.xml、feeds.opml、status.json，并解析 RSS 自引用 URL 和条目数。

## 各种更新

- 即时 AI 调研：在 Codex 或 Claude 中提出研究问题，由本技能指导检索、核实和提交结果；用户授权发布后，可用同一 GitHub 工作流更新站点。
- 普通无人值守刷新：每日直接拉取提供 RSS/Atom 的公开源，做主题筛选、合并与构建。无需模型账号。
- 可选 GitHub 托管调研：在 Actions 的 Secrets 中设置 OPENAI_API_KEY，并在 Variables 中设置 RESEARCH_MODEL 为该账号可用且支持 web search 的模型 ID。每日和手动构建随后可调用 API，在 research/ 里存带出处的待复核报告。此步骤使用该仓库持有人的 API 额度。核实后将精选写到 editorial/ 即可进入正式订阅。

## 故障定位

- 查看 public/status.json 的逐源结果。匹配为零表示本次没有符合当前关键词的条目。解析失败时打开 URL 检查返回类型和上游变化。
- 全部已配置订阅失败时终止部署，保留上一次成功的站点与归档。离线检查用 python3 update.py --offline。
- Pages 配置错误先看 configure-pages 步骤；写回被拒看 workflow permissions 和分支保护；上传或部署错误看 github-pages 环境。
- 操作线上时只报告 GitHub 返回且已核验的部署 URL。不要从账号和仓库名拼一个“已经上线”的链接给用户。
- API 可访问不代表 Git HTTPS、网页或压缩包域名都可访问。HTTPS 超时时分别检查连通性；若用户已经配置了 GitHub SSH，可验证身份后将该仓库 remote 改用 SSH，不改全局 Git URL 规则。安装根目录技能时使用完整 clone，避免稀疏检出漏文件。
- 模板的离线测试不依赖外部 DNS。macOS `/var` 与 `/private/var` 可能是同一路径，比较测试输出路径前需 resolve。生成仓库的测试与技能根目录的初始化测试都需通过。

GitHub 官方说明：[Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) · [定时事件](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
