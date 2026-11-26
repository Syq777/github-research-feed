#!/usr/bin/env python3
"""Create the research files in a local checkout. Never creates a public repository."""
import argparse
import json
from pathlib import Path
import re
import sys

SKILL = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL / "assets" / "repository"


def json_bytes(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()


def initialize(target, topic, title=None, description=None):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", topic):
        raise ValueError("Use a topic ID of up to 80 lowercase letters, digits, dashes or underscores.")
    target = target.resolve()
    if target == SKILL or SKILL in target.parents:
        raise ValueError("Choose a research checkout outside the installed skill.")
    files = {}
    for relative in ["build.py", "render_site.py", "update.py", "README.md", "AGENTS.md",
                     "research/README.md", "workflow.yml", "test_build.py", "research_ai.py", "test_research_ai.py"]:
        if relative == "workflow.yml":
            name = ".github/workflows/research-feed.yml"
        elif relative.startswith("test_"):
            name = "tests/" + relative
        else:
            name = relative
        files[name] = (TEMPLATE / relative).read_bytes()
    files["RESEARCH-FEED-LICENSE"] = (SKILL / "LICENSE").read_bytes()
    preset = TEMPLATE / "topics" / (topic + ".json")
    cfg = json.loads(preset.read_bytes()) if preset.is_file() else {
        "id": topic, "title": title or topic, "description": description or (title or topic) + " 研究订阅",
        "keywords": [], "sources": [], "catalog": f"catalog/{topic}.json"}
    if title:
        cfg["title"] = title
    if description:
        cfg["description"] = description
    files[f"topics/{topic}.json"] = json_bytes(cfg)
    for group in ["catalog", "editorial"]:
        name = f"{group}/{topic}.json"
        source = TEMPLATE / name
        files[name] = source.read_bytes() if source.is_file() else json_bytes([])
    files["site.json"] = json_bytes({"topic": topic})
    # Existing files such as the user's README and agent instructions belong to the user.
    # Choose a documented fallback for these two names, and refuse any other collision.
    for original, alternative in [("README.md", "RESEARCH-FEED.md"), ("AGENTS.md", "RESEARCH-AGENT.md")]:
        if (target / original).is_symlink() or ((target / original).exists() and (target / original).read_bytes() != files[original]):
            files[alternative] = files.pop(original)
    pending = []
    for name, data in files.items():
        path = target / name
        if not path.resolve().is_relative_to(target) or path.is_symlink():
            raise ValueError(f"Path leaves the checkout or is a symlink: {name}")
        if path.exists():
            if not path.is_file() or path.read_bytes() != data:
                raise ValueError(f"Existing {name} differs. Use the checkout's update.py for updates.")
        else:
            pending.append((path, data))
    for path, data in pending:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as f:
            f.write(data)
    return len(pending)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="target research checkout")
    parser.add_argument("--topic", required=True, help="rsi, harness, or a new topic ID")
    parser.add_argument("--title")
    parser.add_argument("--description")
    args = parser.parse_args()
    try:
        count = initialize(args.repo, args.topic, args.title, args.description)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Initialization stopped: {exc}\n")
    print(f"{args.topic}: {count} files created in {args.repo.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
