---
name: explain
description: >
  Dissect any terminal command into an aligned anatomy tree - every program,
  sub-command, flag, argument, pipe and redirect labelled - plus its general
  pattern, risk level, macOS/Linux gotchas and related flags. Use for
  /explain <command>, /explain last, "what does this command do", "break down
  this command", "explain these flags".
argument-hint: "<command> | last"
---

# /explain - command anatomy

**Never run the command being explained.** Only read documentation about it. The user may be asking
precisely because the command is dangerous (`rm -rf`, `dd`, `chmod -R`, `curl ... | sh`).

## 1. Get the command

- `/explain <command>` - use the text after `/explain` exactly as given.
- `/explain last` - the most recent shell command run in this session.
- No argument - the command most recently shown or discussed in the conversation; if unclear, ask.

## 2. Check before you explain

When a flag's meaning is not certain, or behaviour differs between platforms, read the local docs -
read-only and fast:

- `<tool> --help 2>&1 | grep -n -- '<flag>'` (or `<tool> <subcommand> --help` for git/docker/gh/kubectl);
- `man <tool> | col -b | grep -n -A3 -- '<flag>'`;
- `uname -s` to know whether the user is on macOS (BSD tools) or Linux (GNU tools).

Explain what *their* installed version does. If docs are unavailable, say the explanation is from general
knowledge.

## 3. Split into parts

A **part** is the smallest piece a learner would want explained. Copy its text from the command exactly
(same spacing and quotes) - the renderer matches it character for character.

| Keep together as one part | Example |
|---|---|
| a flag and its value | `--since 10m`, `-o out.txt`, `-c:v libx264` |
| combined short flags | `-la`, `-fsSL` (list each letter in the label) |
| a quoted string or URL | `"frigate/#"`, `https://get.docker.com` |
| a redirect | `2>&1`, `>/dev/null`, `>> log.txt`, `< input` |
| an environment assignment | `PATIENT_SENIOR_CONFIG=$S/c.json` |

Give pipes (`|`), `&&`, `||` and `;` their own part - they are what confuses people most.

**Labels:** start with the part itself, then plain words: `--since 10m: only the last 10 minutes`. Aim for
under 60 characters. Say what it *does*, not what the letters stand for (add that only when it helps
memory: `-h: human-readable sizes (K, M, G)`).

## 4. Split long or nested commands into several trees

Draw one tree per piece, then one line explaining how the pieces connect, when:
- the command is longer than about 80 characters or has three or more pipeline stages - one tree per stage;
- it contains a command inside a command - `ssh host '<cmd>'`, `sh -c '<cmd>'`, `$( <cmd> )`,
  `xargs <cmd>`, `find ... -exec <cmd> {} \;`, `sudo <cmd>`, `docker exec <container> <cmd>` - one tree for
  the outer command (label the inner one as "the command to run remotely/inside"), one for the inner.

## 5. Render with the script - never draw the tree by hand

Language models miscount columns; the script places every `│` and `└` exactly. Run it from this skill's
directory and paste its output verbatim inside a ```text block:

```bash
python3 "<this skill's directory>/scripts/anatomy.py" <<'JSON'
{"command": "docker logs --since 10m frigate 2>&1 | grep -i error",
 "parts": [
  {"text": "docker", "label": "docker: the program"},
  {"text": "logs", "label": "logs: show a container's output"},
  {"text": "--since 10m", "label": "--since 10m: only the last 10 minutes"},
  {"text": "frigate", "label": "the container"},
  {"text": "2>&1", "label": "2>&1: send stderr where stdout goes, so grep sees both"},
  {"text": "|", "label": "|: pipe - feed the output into the next command"},
  {"text": "grep", "label": "grep: keep only matching lines"},
  {"text": "-i", "label": "-i: ignore case"}]}
JSON
```

For several trees, pass a JSON list of such objects. Add `--ascii` if the user's terminal cannot show
box-drawing characters. If the script reports `part ... not found`, the part's text does not match the
command exactly - fix the part, do not edit the output.

## 6. After the tree

```text
Pattern:   docker logs [--since <time>] [--tail <n>] [-f] <container>
Risk:      read-only
Gotcha:    -  (only when there is one)
Related:   --tail 50 (last 50 lines) · -f (keep following new lines)
```

- **Pattern** - the general shape, `<placeholders>` for values and `[brackets]` for optional parts.
- **Risk** - one of: `read-only` · `writes files` · `changes system settings` · `network` · `needs root` ·
  `destructive - <what is lost, and whether it can be undone>`.
- **Gotcha** - platform differences and traps worth knowing, for example: GNU vs BSD flags (`sed -i` vs
  `sed -i ''`, `du --max-depth` vs `du -d`), tools missing on macOS (`timeout`), shell quoting surprises,
  `ping -t` meaning TTL on Linux but timeout on macOS. Omit the line when there is nothing real to say.
- **Related** - at most two flags or companion commands that the user is likely to want next.

Finish with one sentence on what the whole command achieves, in plain words.

## 7. Optional extras

- If the user is learning (they asked to be quizzed, or a patient-senior mode block is in this session),
  end with a variation challenge: "Your turn: how would you change it to ...?" and wait.
- If the patient-senior plugin is active, also follow its flashcard rule for any command new to the user.
