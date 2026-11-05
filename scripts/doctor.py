#!/usr/bin/env python3
"""Read-only prerequisite checks; never installs tools or runs configured checks."""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from project_profile import validate_profile

ROOT = Path(__file__).resolve().parents[1]


def version_output(name):
    executable = shutil.which(name)
    if not executable:
        return None
    try:
        result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("template", "project"), default="template")
    parser.add_argument("--config", type=Path, default=ROOT / "project.json")
    args = parser.parse_args()
    errors = []
    if sys.version_info < (3, 12):
        errors.append("Python 3.12 or newer is required for template maintenance")
    for tool in (("git", "make", "node") if args.profile == "template" else ("git",)):
        result = version_output(tool)
        if result is None:
            errors.append(f"{tool} is missing or its version check failed")
        elif tool == "node" and not re.match(r"v(?:2[4-9]|[3-9]\d)\.", result):
            errors.append("Node 24 or newer is required for template tests")
    if args.profile == "project":
        try:
            data = json.loads(args.config.read_text(encoding="utf-8"))
            errors.extend(validate_profile(data, ROOT))
        except (OSError, UnicodeError, ValueError):
            errors.append("Cannot read a valid project profile; initialize a reviewed project.json first")
        if not errors:
            for name, spec in data["tools"].items():
                result = version_output(name)
                expected = spec["version"]
                if result is None or not re.search(r"(?<![\w.+-])v?" + re.escape(expected) + r"(?![\w.+-])", result):
                    errors.append(f"{name}: installed version does not match the declared pin, or version check failed")
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"PASS: {args.profile} prerequisites. Application checks, authentication, and dispatch still require separate evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
