#!/usr/bin/env python3
"""Render a terminal command as an anatomy tree with exact column alignment.

Input (stdin): JSON describing one command, or a list of them (one tree each):

    {"command": "docker logs --since 10m frigate",
     "parts": [{"text": "docker", "label": "the program"},
               {"text": "logs", "label": "show a container's output"},
               {"text": "--since 10m", "label": "only the last 10 minutes"},
               {"text": "frigate", "label": "which container"}]}

Each part's "text" must appear in "command" exactly as written, in order. The
script finds each part after the end of the previous one, so repeated tokens
are matched to the right occurrence.

Output:

    docker logs --since 10m frigate
    │      │    │           └ which container
    │      │    └ only the last 10 minutes
    │      └ show a container's output
    └ the program

Options: --ascii uses | and ` instead of box-drawing characters.
"""
import json
import sys

PIPE, ELBOW = "│", "└"


def locate(command, parts):
    """Return the start column of every part, matching them left to right."""
    columns, cursor = [], 0
    for part in parts:
        text = part["text"]
        col = command.find(text, cursor)
        if col < 0:
            raise ValueError(f"part {text!r} not found in command after column {cursor}")
        columns.append(col)
        cursor = col + len(text)
    return columns


def render(command, parts, pipe=PIPE, elbow=ELBOW):
    columns = locate(command, parts)
    lines = [command]
    for i in range(len(parts) - 1, -1, -1):
        row = [" "] * columns[i]
        for col in columns[:i]:
            row[col] = pipe
        lines.append("".join(row) + f"{elbow} {parts[i]['label']}")
    return "\n".join(line.rstrip() for line in lines)


def main():
    ascii_mode = "--ascii" in sys.argv
    pipe, elbow = ("|", "`") if ascii_mode else (PIPE, ELBOW)
    data = json.load(sys.stdin)
    trees = data if isinstance(data, list) else [data]
    try:
        out = [render(t["command"], t["parts"], pipe, elbow) for t in trees]
    except (KeyError, ValueError) as err:
        sys.exit(f"anatomy.py: {err}")
    print("\n\n".join(out))


if __name__ == "__main__":
    main()
