# GitHub Research Feed

一份可移植的 Agent Skill：从广泛来源选出每天值得读的研究进展，用中文说清楚文章讲什么、为什么值得读，发布到 GitHub Pages 与 RSS。默认每日最多 10 篇，论文目标三成、最多四成，其他名额在工程、研究、评测、观点和访谈间调整。维护者提供主题和目标仓库，AI 按 SKILL.md 调研、编辑和发布。完整来源目录保留在次级归档。

[RSI 示例网站](https://syq777.github.io/rsi-research-feed/) · [RSS](https://syq777.github.io/rsi-research-feed/feed.xml) · [示例研究仓库](https://github.com/Syq777/rsi-research-feed)

[六领域 Top 20 与完整来源访问表](https://syq777.github.io/rsi-research-feed/sources.html)：先轮询完整动态来源池，再比较候选、读原文、挑出十条。不能找到十篇就停止。每期有自然的名字和 3–5 个关键词；重要性、公开入口读取和全文权限分别记录。RSI 初版有 270 个去重目录条目，185 个动态公开入口，六领域 Top 20 合并为 112 个重点入口。

## 安装

开源分发时，把本目录作为 GitHub 仓库的根目录（保留 scripts/、references/、assets/）。在 Codex 的项目目录 .agents/skills/ 或 Claude Code 的项目目录 .claude/skills/ 下放置名为 github-research-feed 的完整文件夹。也可以使用客户端支持的个人技能目录。程序使用 Python 3.10+，支持 Linux 和 macOS，GitHub Actions 使用 Ubuntu。公共源的定时获取只需 Python 标准库。

Codex 个人安装（目标目录应尚不存在）：

```bash
git clone https://github.com/Syq777/github-research-feed.git "${CODEX_HOME:-$HOME/.codex}/skills/github-research-feed"
python3 -B "${CODEX_HOME:-$HOME/.codex}/skills/github-research-feed/scripts/init_repo.py" --check
```

已配置 GitHub SSH 的机器可将 clone 地址替换为 `git@github.com:Syq777/github-research-feed.git`。不要对仓库根目录使用 `git sparse-checkout set .`：这会漏掉脚本和模板。若安装器已创建带 `.git` 的不完整目录，在该目录执行 `git sparse-checkout disable`，再做完整性检查。普通压缩包安装应复制整个文件夹。安装完成后，Codex 可在下一轮对话使用该技能。

更新通过完整 clone 安装的技能：在技能目录运行 `git status --short`，确认没有本地改动后 `git pull --ff-only`，再执行 `scripts/init_repo.py --check`。研究仓库里的手工数据不会随技能更新而自动覆盖。

## 使用

- 「用 github-research-feed 在当前空仓库建立 RSI 调研订阅。保留我给你的来源大类和小类，跑一次，告诉我哪些源实际抓到了内容。」
- 「调研这周长任务 Agent Harness 的进展，回到原文核实，将有出处的结论写进我的研究仓库，并更新订阅。」
- 「更新今天的 RSI 精选，每篇给中文概要和一句阅读理由，不够十篇可以少选，论文不要超过四成。」
- 「用同一 Skill 为一个新主题建立独立仓库，沿用采集、归档和 GitHub Pages 的流程。」

`python3 scripts/init_repo.py --repo /path/to/my-research --topic harness` 可单独初始化。进入该仓库，运行 `python3 update.py` 获取实际条目，或用 `--offline` 从已有档案构建。完整工作流程见 [SKILL.md](SKILL.md)，配置见 [运行说明](references/github.md)。

RSI 和新主题默认启用每日精选，Harness 预置保留普通归档模式。`update.py` 只采集和渲染；AI 查原文并补齐 editorial 后，运行 `digest.py --date YYYY-MM-DD --lead '本期导读'` 才生成新一期。RSI 附带带日期的示例，不能把示例日期改成安装日来伪装更新。

中文精选需要模型参与。可复用本机 Codex 定时编辑和发布，不另配 API，电脑需在线；GitHub Actions 则每天更新原始候选。未生成新一期时首页保留最近一期及真实日期。可选云端 API 脚本仅发现候选，不等价于完整自动编辑。

RSI 预置目录沿用提供材料的 11 大类、36 小类，包含 271 条入口和线索；其中 7 个端点配置为自动 RSS/Atom 抓取。其余目录条目需要按研究问题另行查阅，目录数量不代表已自动订阅或逐条核实的来源数量。可选 AI 调研目前只搜索 `topics/` 中已配置源的域名，结果留在 `research/` 待复核，不会自动进入正式 RSS。

修改模板后运行 `python3 -B -m unittest discover -s tests`；CI 会在 Linux 和 macOS 上检查安装、初始化、离线输出及生成仓库的测试。首次实操问题与修复见 [验证记录](references/validation.md)。

本项目的自有代码与流程采用 MIT 许可证。所引论文、外部文章、订阅源材料和商标由相应权利人持有。目录保留原文链接。
