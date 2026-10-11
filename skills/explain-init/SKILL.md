---
name: explain-init
description: >
  Install command-anatomy's auto-explain rule for other AI coding agents -
  Codex CLI, GitHub Copilot (CLI and VS Code), Cursor - globally or for the
  current repository, so they show a command's anatomy tree before running it.
  Dry run first; never overwrites. Use for /explain-init.
argument-hint: "[global | repo] [--only codex|copilot-cli|copilot-vscode|cursor|agents] [--force]"
---

# /explain-init

Explain each step and command before running it.

## 1. Build the rule block

Read `rules/auto-explain.md` at the plugin root (two folders up from this skill's directory) and wrap it
in markers:

```
<!-- command-anatomy:start -->
...rule text...
<!-- command-anatomy:end -->
```

## 2. Targets

Default scope is **global** (every repository) where the agent supports it; `repo` installs into the
current repository instead.

| Agent | Global file | Repo file |
|---|---|---|
| Codex CLI | `${CODEX_HOME:-~/.codex}/AGENTS.md` | `AGENTS.md` |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` | `.github/copilot-instructions.md` |
| GitHub Copilot in VS Code | user-profile instructions file (see note) | `.github/copilot-instructions.md` |
| Cursor | none as a file (Settings -> Rules -> User Rules: paste the block) | `.cursor/rules/command-anatomy.mdc` with frontmatter `alwaysApply: true` |
| Any AGENTS.md-aware agent | - | `AGENTS.md` |

Only offer agents that look installed (`~/.codex`, `~/.copilot`, `code` on PATH, `~/.cursor`) unless the
user names one. Notes:
- **Copilot in VS Code (global):** VS Code keeps user-level `*.instructions.md` files in the user profile.
  Ask the user to run *Chat: New Instructions File* -> *User Data* in VS Code, name it `command-anatomy`,
  and tell you the path it created (or paste the block themselves). Add frontmatter `applyTo: "**"`.
- **Codex global AGENTS.md:** a reported bug in some Codex versions skips the global file; suggest the user
  verifies in a fresh session and falls back to the repo `AGENTS.md`.
- **A repo `AGENTS.md` imported by `CLAUDE.md` (`@AGENTS.md`):** Claude Code would get the rule twice (plugin
  hook + file). Skip it for Claude, or warn.

## 3. Dry run, then write

1. For each target show: path, and *create* / *append* (file exists without our block) / *update* (block
   present but different) / *skip* (block identical). Ask before writing, unless `--force`.
2. Append the block at the end of existing files; replace only the content between our markers on update;
   change nothing else.
3. Report what was written, how to verify (start a fresh session of that agent and ask it to run
   `ls -la`), and how to remove it (delete the marked block).
