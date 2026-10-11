# command-anatomy

**See inside any terminal command.**

Whenever your AI agent is about to run a terminal command, it first shows you its **anatomy** - every
program, sub-command, flag, argument, pipe and redirect labelled - and how risky it is. Ask for any command
on demand with `/explain` for the full version: aligned tree, general pattern, risk and the macOS/Linux
gotchas that bite.

```text
/explain docker logs --since 10m frigate 2>&1 | grep -i error
```

```text
docker logs --since 10m frigate 2>&1 | grep -i error
│      │    │           │       │    │ │    └ -i: ignore case
│      │    │           │       │    │ └ grep: keep only matching lines
│      │    │           │       │    └ |: pipe - feed the output into the next command
│      │    │           │       └ 2>&1: send stderr where stdout goes
│      │    │           └ the container
│      │    └ --since 10m: only the last 10 minutes
│      └ logs: show a container's output
└ docker: the program

Pattern:   docker logs [--since <time>] [--tail <n>] [-f] <container>
Risk:      read-only
Related:   --tail 50 (last 50 lines) · -f (keep following new lines)
```

## Automatic, in every agent

Installed, it works in the background: before running a command, the agent draws its anatomy tree in the
conversation and adds a `Risk:` line - including for retries after an error.

| Agent | How it is switched on | Scope |
|---|---|---|
| **Claude Code** | the plugin's start-of-session hook (on by default; `/explain auto off` to stop) | every session |
| **Codex CLI** | `/explain-init` writes the rule into `~/.codex/AGENTS.md` ([docs](https://developers.openai.com/codex/guides/agents-md)) | global |
| **GitHub Copilot CLI** | `/explain-init` writes `~/.copilot/copilot-instructions.md` ([docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)) | global |
| **Copilot in VS Code** | `.github/copilot-instructions.md`, or a user-profile instructions file ([docs](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)) | repo or global |
| **Cursor** | `.cursor/rules/command-anatomy.mdc` | repo |

`/explain-init` always does a dry run first and wraps the rule in `<!-- command-anatomy:start/end -->`
markers, so it never overwrites your own instructions and is easy to remove.

**Honest note:** this is an instruction to the agent, not an enforcement mechanism. In testing, trees
appeared before every first attempt and 10 of 11 hand-drawn trees were perfectly aligned (one was off by a
column); retries after errors were the weak spot, which the rule now targets explicitly. For a guaranteed,
script-aligned tree of any command, use `/explain`.

## A dangerous one

`/explain find . -name "*.log" -mtime +7 -exec rm {} \;` - real output:

```text
find . -name "*.log" -mtime +7 -exec rm {} \;
│    │ │             │         │     │     └ \;: end of the -exec command
│    │ │             │         │     └ the command to run (see below)
│    │ │             │         └ -exec: run a command on each match
│    │ │             └ -mtime +7: modified more than 7 days ago
│    │ └ -name "*.log": filename ends in .log
│    └ .: start in the current directory
└ find: search a directory tree

rm {}
│  └ {}: replaced by each file find matched
└ rm: delete files (no trash, no undo)

Pattern:   find <dir> -name "<glob>" -mtime +<days> -exec <cmd> {} \;
Risk:      destructive - permanently deletes every matching .log file under . (recursive); cannot be undone
Gotcha:    -mtime +7 means "older than 7 full 24h periods" (8+ days - fractions round down). Quote "*.log"
           so the shell doesn't expand the glob first.
Related:   swap `rm {}` for `ls -l {}` to preview matches first · `-exec ... {} +` batches files per rm call
```

The command is **never run** - only explained. That is the point when you are asking about `rm -rf`.

## Install (Claude Code)

```bash
claude plugin marketplace add randnumX/command-anatomy
claude plugin install command-anatomy@command-anatomy
```

Then, in any session:

| You type | You get |
|---|---|
| `/explain <command>` | The anatomy of that command |
| `/explain last` | The anatomy of the last command Claude ran |
| `/explain auto on\|off\|status` | Switch the automatic before-every-command anatomy |
| `/explain-init` | Install the automatic rule for Codex, Copilot and Cursor |
| "what does this command do?" | The skill triggers on its own |

(As a plugin skill it may also appear as `/command-anatomy:explain`.)

## Not using Claude Code?

The installer works on its own - no Claude Code needed. Read it first, then run it:

```bash
curl -fsSL https://raw.githubusercontent.com/randnumX/command-anatomy/main/scripts/install_rules.py -o install_rules.py
less install_rules.py                                  # read what it does
python3 install_rules.py --global --dry-run            # Codex + Copilot CLI, every repository
python3 install_rules.py --global --yes
python3 install_rules.py --repo . --yes                # AGENTS.md, Copilot, Cursor for one repository
python3 install_rules.py --repo . --remove --yes       # undo
```

It only writes between `<!-- command-anatomy:start -->` and `<!-- command-anatomy:end -->` markers, so
your own instructions are never touched.

## Why `/explain` trees are always aligned

Language models are bad at counting columns, so hand-drawn trees can drift. With `/explain`, Claude only decides the
**parts** and writes the **labels**; a tiny Python script (`skills/explain/scripts/anatomy.py`, no
dependencies) places every `│` and `└` at the exact column. Parts are matched left to right, so repeated
tokens (`grep -i a | grep -i b`) land in the right place.

```bash
python3 -m unittest discover -s tests     # renderer and installer tests
```

## What else it does

- **Reads your local docs first** (`--help`, `man`) when a flag is uncertain, so the explanation matches
  *your* installed version - GNU or BSD.
- **Splits long and nested commands**: one tree per pipeline stage, and separate trees for commands inside
  commands (`ssh host '...'`, `sh -c`, `$( )`, `xargs`, `find -exec`, `sudo`, `docker exec`).
- **Rates risk**: read-only · writes files · changes system settings · network · needs root · destructive.
- **Flags real gotchas**: `sed -i` vs `sed -i ''`, `timeout` missing on macOS, `ping -t` meaning different
  things, quoting traps.

## Pairs with patient-senior

[patient-senior](https://github.com/randnumX/patient-senior) is an always-on mentor mode that explains
everything your AI does, captures side quests and writes flashcards to Obsidian. With both installed,
command breakdowns use these aligned trees and every new command becomes a flashcard.

## Requirements

Claude Code and `python3`.

## License

[MIT](LICENSE)
