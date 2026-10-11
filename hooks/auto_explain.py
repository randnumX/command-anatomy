#!/usr/bin/env python3
"""SessionStart hook: tell Claude to show a command's anatomy before running it.

Plain text printed by a SessionStart hook is added to the session's context.
Settings: ~/.config/command-anatomy/config.json  ->  {"auto": true}
(missing file = on; `/explain auto off` writes {"auto": false}).
Override the location with the COMMAND_ANATOMY_CONFIG environment variable.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path(os.environ.get("COMMAND_ANATOMY_CONFIG", "~/.config/command-anatomy/config.json")).expanduser()


def auto_enabled():
    try:
        return json.loads(CONFIG.read_text()).get("auto", True) is not False
    except (OSError, ValueError):
        return True


def main():
    if not auto_enabled():
        return
    rules = (ROOT / "rules" / "auto-explain.md").read_text()
    sys.stdout.write(rules + "\nTurn off with `/explain auto off`.\n")


if __name__ == "__main__":
    main()
