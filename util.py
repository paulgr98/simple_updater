import json
import subprocess


def load_config(path):
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def run_winget(arg, package_id):
    return subprocess.run(
        ["winget", arg, "--id", package_id],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
