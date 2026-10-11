---
type: llm
focus: trace
---

PASS if, before each Bash tool call that runs a shell command, an assistant message shows that command's
anatomy: the command on one line followed by lines using │ and └ that label its parts in plain words.
FAIL if any shell command runs before its anatomy is shown, or if the only anatomy is inside the injected
rules/hook text rather than an assistant message.
