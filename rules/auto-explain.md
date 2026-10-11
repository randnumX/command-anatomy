# command-anatomy: auto-explain is ON

Before you run any terminal command (shell, bash or terminal tool), show its anatomy in your message so the user can understand it and write it themselves later. Then run it.

This applies to **every** command you run - including retries, fixes and alternatives after an error: a changed command is a new command. Errors are when explanations matter most, so before each retry write one line on why the last attempt failed, then a short tree covering only the parts that changed (`Anatomy: same as above` if nothing did).

1. **Split the command into parts**, copying each part's text exactly as it appears:
   - the program, sub-commands and positional arguments;
   - a flag together with its value (`--since 10m`, `-o out.txt`); combined short flags as one part (`-la`);
   - quoted strings and URLs as one part; redirects (`2>&1`, `> file`, `< input`) as one part;
   - pipes `|` and the operators `&&`, `||`, `;` as parts of their own.

   Label each part `<part>: <what it does in plain words>`, under 60 characters.
2. **Draw the tree in your message, right before the tool call** - text written before a tool call is shown to the user first, so the explanation always arrives before the command runs. Build it mechanically, one line per part, last part first:
   - start each line as a copy of the command where every character is replaced by a space;
   - put `│` at the column where each *earlier* part begins, and `└ <label>` at the column where the current part begins;
   - the first line under the command is for the last part; the final line is `└ <first part's label>`.

   ```text
   docker logs --since 10m frigate
   │      │    │           └ frigate: the container
   │      │    └ --since 10m: only the last 10 minutes
   │      └ logs: show a container's output
   └ docker: the program
   ```

   Put the tree in a `text` code block. Commands longer than about 80 characters, or with a command inside a command (`ssh host '...'`, `sh -c`, `$( )`, `xargs`, `find -exec`, `sudo`, `docker exec`), get one tree per piece - short trees stay aligned. For a perfectly aligned tree of a long command, the user can run `/explain` on it.
3. **Under the tree, one line:** `Risk: read-only` / `writes files` / `changes system settings` / `network` / `needs root` / `destructive - <what is lost, and whether it can be undone>`.
4. **Then run the command.**

**Exempt:** a command identical to one already explained in this conversation (write `Anatomy: same as above`); commands you only mention without running.

