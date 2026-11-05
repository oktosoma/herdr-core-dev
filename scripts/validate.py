#!/usr/bin/env python3
"""Validate the template's actual documents and examples, without network access."""
import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from project_profile import validate_profile

ROOT = Path(__file__).resolve().parents[1]


class Guide(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets = [], [], []
        self.version = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag in ("script", "link", "img"):
            self.assets.append(attrs.get("src", attrs.get("href", "")))
        if tag == "html":
            self.version = attrs.get("data-model-version")


def validate(root=ROOT):
    root = Path(root)
    errors = []
    metadata = json.loads((root / "template.json").read_text())
    example = json.loads((root / "project.example.json").read_text())
    errors.extend(validate_profile(example, root, example=True))
    if example["template_version"] != metadata["template_version"]:
        errors.append("Profile example and template version disagree")
    model = metadata["model_version"]
    readme = (root / "README.md").read_text()
    if f"Model **v{model}**" not in readme or f"template **{metadata['template_version']}**" not in readme:
        errors.append("README version is stale")
    if f"Model v{model}." not in (root / "HERDR.md").read_text():
        errors.append("Runbook version is stale")
    guide_path = root / "docs/guide/index.html"
    guide = Guide()
    guide.feed(guide_path.read_text())
    if guide.version != model:
        errors.append("Guide version is stale")
    if any(count > 1 for count in Counter(guide.ids).values()):
        errors.append("Guide contains duplicate IDs")
    if any(urlsplit(asset).scheme in ("http", "https") or asset.startswith("//") for asset in guide.assets):
        errors.append("Offline guide contains an external asset")
    links = [(guide_path, link) for link in guide.links]
    listing = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                             cwd=root, capture_output=True, check=True).stdout.decode().split("\0")
    for name in filter(None, listing):
        path = root / name
        if not path.is_file():
            continue
        if path.suffix == ".md":
            links.extend((path, link) for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()))
        if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            errors.append(f"Environment value file is included in source: {name}")
    for source, link in links:
        parsed = urlsplit(link)
        if parsed.scheme or link.startswith("//"):
            continue
        target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source.resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            errors.append(f"Missing or escaping local link in {source.relative_to(root)}: {link}")
        elif target == guide_path.resolve() and parsed.fragment and unquote(parsed.fragment) not in guide.ids:
            errors.append(f"Missing guide fragment: {parsed.fragment}")
    for line in (root / ".env.example").read_text().splitlines():
        if line.strip() and not line.lstrip().startswith("#") and not re.fullmatch(r"[A-Z][A-Z0-9_]*=", line):
            errors.append(".env.example must contain variable names with empty values only")
    for name in ("codex", "omp"):
        content = (root / f"templates/{name}.md").read_text()
        command = content.splitlines()[0]
        if not command.startswith("command: "):
            errors.append(f"{name} launch template lacks command frontmatter")
            continue
        rendered = command.removeprefix("command: ").replace("<model-id>", "approved-model-id")
        if "<" in rendered or ">" in rendered:
            errors.append(f"{name} launch example has an unrecognized command placeholder")
        elif subprocess.run(["sh", "-n", "-c", rendered], capture_output=True).returncode:
            errors.append(f"{name} rendered launch command does not parse")
    return errors


if __name__ == "__main__":
    try:
        problems = validate()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        problems = [f"Validation could not complete: {type(error).__name__}"]
    for problem in problems:
        print(f"FAIL: {problem}")
    if not problems:
        print("PASS: template profiles, versions, links, offline assets, environment example, and rendered launch syntax")
    raise SystemExit(bool(problems))
