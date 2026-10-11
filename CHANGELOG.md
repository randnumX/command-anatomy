# Changelog

All notable changes to command-anatomy. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [0.2.0] - 2026-10-11
### Added
- Automatic anatomy before every command (SessionStart hook in Claude Code; on by default, `/explain auto off`).
- `scripts/install_rules.py` and `/explain-init`: the same rule for Codex, Copilot, Cursor, Windsurf and Cline, globally or per repo, without Claude Code.
- Unit tests for the installer, CI, contributing and security docs.
### Changed
- Automatic trees are drawn in the message before the tool call (a renderer round-trip was batched with the command by agents, so the tree never reached the user).

## [0.1.0] - 2026-10-11
### Added
- `/explain <command>`: aligned anatomy tree from a dependency-free renderer, pattern, risk, gotchas, related flags; never runs the command.
