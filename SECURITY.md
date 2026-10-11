# Security

## What runs on your machine

command-anatomy is mostly Markdown instructions. The only code is small, dependency-free Python:

- `hooks/auto_explain.py` - runs at session start; reads `~/.config/command-anatomy/config.json` and prints the rule. No network, no writes.
- `skills/explain/scripts/anatomy.py` - renders a tree from JSON on stdin. No network, no writes.
- `scripts/install_rules.py` - writes only between its markers in the instruction files you choose; when piped from `curl` it downloads `rules/auto-explain.md` from this repository.
- `/explain` never runs the command it explains; it may read `--help` and `man` pages.

There is no telemetry and no background process.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting (Security tab -> "Report a vulnerability") rather than a
public issue.
