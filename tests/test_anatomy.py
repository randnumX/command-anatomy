"""Run with: python3 -m unittest discover -s tests"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "explain" / "scripts" / "anatomy.py"
sys.path.insert(0, str(SCRIPT.parent))
from anatomy import render  # noqa: E402

DOCKER = "docker logs --since 10m frigate 2>&1 | grep -i error"
DOCKER_PARTS = [
    {"text": "docker", "label": "the program"},
    {"text": "logs", "label": "sub-command: show a container's output"},
    {"text": "--since 10m", "label": "only the last 10 minutes"},
    {"text": "frigate", "label": "which container"},
    {"text": "2>&1", "label": "include error output too"},
    {"text": "grep", "label": "keep only matching lines"},
    {"text": "-i", "label": "ignore case"},
]
DOCKER_TREE = """\
docker logs --since 10m frigate 2>&1 | grep -i error
│      │    │           │       │      │    └ ignore case
│      │    │           │       │      └ keep only matching lines
│      │    │           │       └ include error output too
│      │    │           └ which container
│      │    └ only the last 10 minutes
│      └ sub-command: show a container's output
└ the program"""


def run_script(payload, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=json.dumps(payload),
                          capture_output=True, text=True)


class RenderTest(unittest.TestCase):
    def test_reference_diagram(self):
        self.assertEqual(render(DOCKER, DOCKER_PARTS), DOCKER_TREE)

    def test_repeated_tokens_match_in_order(self):
        tree = render("grep -i a | grep -i b", [
            {"text": "grep", "label": "first grep"}, {"text": "-i", "label": "first -i"},
            {"text": "|", "label": "pipe"}, {"text": "grep", "label": "second grep"},
            {"text": "-i", "label": "second -i"}])
        self.assertEqual(tree.splitlines()[1], "│    │    │ │    └ second -i")

    def test_missing_part_fails_cleanly(self):
        result = run_script({"command": "ls -la", "parts": [{"text": "-x", "label": "nope"}]})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stderr)

    def test_list_input_renders_each_tree(self):
        one = {"command": "ls -la", "parts": [{"text": "ls", "label": "list"}, {"text": "-la", "label": "long, all"}]}
        result = run_script([one, one])
        self.assertEqual(result.stdout.count("└ list"), 2)

    def test_ascii_mode(self):
        result = run_script({"command": "ls -la", "parts": [{"text": "ls", "label": "list"},
                                                            {"text": "-la", "label": "long, all"}]}, "--ascii")
        self.assertEqual(result.stdout.splitlines()[1], "|  ` long, all")


if __name__ == "__main__":
    unittest.main()
