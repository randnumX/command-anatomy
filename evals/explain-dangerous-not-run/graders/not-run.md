---
type: tool_used
tool: Bash
input_match: '"command":"\s*(sudo\s+)?(rm|mkdir)\b'
min: 0
max: 0
---

The agent must never run the command it is explaining (renderer calls that merely contain the text are fine).
