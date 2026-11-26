# GitHub Research Feed

一份可移植的 Agent Skill，用来在 GitHub 仓库中进行主题调研、积累可核验的资料，并发布读者可订阅的静态网页和 RSS。维护者提供主题和目标仓库，AI 按 SKILL.md 的同一流程执行。RSI 与 Agent Harness 为两个开箱示例，其他主题可从空白配置开始。

## 安装

开源分发时，把本目录作为 GitHub 仓库的根目录（保留 scripts/、references/、assets/）。在 Codex 的项目目录 .agents/skills/ 或 Claude Code 的项目目录 .claude/skills/ 下放置名为 github-research-feed 的完整文件夹。也可以使用客户端支持的个人技能目录。程序使用 Python 3.10+，支持 Linux 和 macOS，GitHub Actions 使用 Ubuntu。公共源的定时获取只需 Python 标准库。

## 使用

- 「用 github-research-feed 在当前空仓库建立 RSI 调研订阅。保留我给你的来源大类和小类，跑一次，告诉我哪些源实际抓到了内容。」
- 「调研这周长任务 Agent Harness 的进展，回到原文核实，将有出处的结论写进我的研究仓库，并更新订阅。」
- 「用同一 Skill 为一个新主题建立独立仓库，沿用采集、归档和 GitHub Pages 的流程。」

`python3 scripts/init_repo.py --repo /path/to/my-research --topic harness` 可单独初始化。进入该仓库，运行 `python3 update.py` 获取实际条目，或用 `--offline` 从已有档案构建。完整工作流程见 [SKILL.md](SKILL.md)，配置见 [运行说明](references/github.md)。

本项目的自有代码与流程采用 MIT 许可证。所引论文、外部文章、订阅源材料和商标由相应权利人持有。目录保留原文链接。
