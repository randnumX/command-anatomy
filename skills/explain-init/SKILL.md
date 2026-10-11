---
name: explain-init
description: >
  Install command-anatomy's auto-explain rule for other AI coding agents -
  Codex CLI, GitHub Copilot (CLI, VS Code), Cursor, Windsurf, Cline - globally
  or for the current repository, so they show a command's anatomy tree before
  running it. Dry run first; never touches text outside its markers. Use for /explain-init.
argument-hint: "[global | repo] [--agents codex,copilot-cli,agents-md,copilot,cursor,windsurf,cline] [--remove]"
---

# /explain-init

All file changes are made by the installer script (exact and tested) - do not edit the files yourself.
Script: `scripts/install_rules.py` at the plugin root (two folders up from this skill's directory).

1. **Dry run** - explain the command, then run it and show the output:
   ```bash
   python3 "<plugin root>/scripts/install_rules.py" --global --dry-run
   ```
   Use `--repo .` instead of `--global` when the user asked for this repository only. Pass `--agents` or
   `--remove` through from the user's arguments. `--global` covers Codex (`~/.codex/AGENTS.md`) and Copilot
   CLI (`~/.copilot/copilot-instructions.md`) when they are installed; `--repo` covers `AGENTS.md`,
   `.github/copilot-instructions.md` (Copilot in VS Code and CLI) and `.cursor/rules/` by default.
2. **Ask** the user to confirm the listed changes.
3. **Write** - the same command with `--yes` instead of `--dry-run`.
4. **Tell the user** how to verify (a fresh session of that agent, ask it to run `ls -la`) and how to undo
   (`--remove --yes`).

Copilot in VS Code also supports a user-level instructions file: in VS Code run *Chat: New Instructions File*
-> *User Data*, then paste the rule from `rules/auto-explain.md` (with `applyTo: "**"` in its frontmatter).
