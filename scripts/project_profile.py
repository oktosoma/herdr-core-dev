"""Validate reviewed, non-secret project configuration without executing commands."""
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

FIELDS = {"schema_version", "project_name", "template_version", "integration_branch",
          "max_workers", "reviewer_count", "roles", "tools", "decisions", "checks"}
CHECKS = {"unit", "integration", "contract", "static", "build", "smoke"}
VERSION = re.compile(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9._-]+)?")


def filled(value):
    return isinstance(value, str) and bool(value.strip()) and not re.search(r"<[^>]+>", value)


def validate_profile(data, root, *, example=False):
    errors = []
    root = Path(root).resolve()
    if not isinstance(data, dict):
        return ["Profile must be a JSON object"]
    if set(data) != FIELDS:
        errors.append("Profile fields do not match the documented schema")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        errors.append("schema_version must be 1")
    for key in ("project_name", "template_version", "integration_branch"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip() or (not example and not filled(value)):
            errors.append(f"{key} must be filled")
    name = data.get("project_name", "")
    if filled(name) and not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        errors.append("project_name must use lowercase letters, digits, and hyphens")
    version = data.get("template_version", "")
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        errors.append("template_version must be an exact semantic version")
    branch = data.get("integration_branch", "")
    if filled(branch) and (not re.fullmatch(r"coord/[A-Za-z0-9][A-Za-z0-9._/-]*", branch)
                           or any(x in branch for x in ("..", "//", "/."))
                           or branch.endswith(("/", "."))
                           or any(part.endswith(".lock") for part in branch.split("/"))):
        errors.append("integration_branch must be a valid coord/<milestone> ref")
    if type(data.get("max_workers")) is not int or data["max_workers"] < 1:
        errors.append("max_workers must be a positive integer")
    if type(data.get("reviewer_count")) is not int or data["reviewer_count"] != 1:
        errors.append("reviewer_count must be 1 under the current model")
    roles = data.get("roles")
    if not isinstance(roles, dict) or set(roles) != {"orchestrator", "worker", "reviewer"}:
        errors.append("roles must assign orchestrator, worker, and reviewer")
    elif any(not isinstance(v, str) or not v.strip() or (not example and not filled(v)) for v in roles.values()):
        errors.append("Every role must name its approved harness/model")
    tools = data.get("tools")
    if not isinstance(tools, dict) or not tools:
        errors.append("tools must declare at least one required tool")
    else:
        for name, spec in tools.items():
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", name):
                errors.append("Tool names must be executable names without paths or arguments")
            if not isinstance(spec, dict) or set(spec) != {"version", "source"}:
                errors.append(f"Tool {name}: declare only version and source")
                continue
            version, source = spec["version"], spec["source"]
            if not isinstance(version, str) or not version.strip() or (not example and not filled(version)):
                errors.append(f"Tool {name}: exact version is required")
            elif filled(version) and not VERSION.fullmatch(version):
                errors.append(f"Tool {name}: version must be exact, not a range")
            if not isinstance(source, str) or not source.strip() or (not example and not filled(source)):
                errors.append(f"Tool {name}: official HTTPS source is required")
            elif filled(source):
                try:
                    parsed = urlsplit(source)
                    valid = (parsed.scheme == "https" and parsed.hostname and not parsed.username
                             and not parsed.password and not parsed.query and not parsed.fragment)
                except ValueError:
                    valid = False
                if not valid:
                    errors.append(f"Tool {name}: source must be HTTPS without credentials/query/fragment")
    decisions = data.get("decisions")
    if not isinstance(decisions, dict) or set(decisions) != {"stack", "roles", "release"}:
        errors.append("decisions must link stack, roles, and release records")
    elif not example:
        for kind, relative in decisions.items():
            if not filled(relative):
                errors.append(f"Decision {kind}: accepted record is required")
                continue
            path = (root / relative).resolve()
            if Path(relative).is_absolute() or not path.is_relative_to(root) or not path.is_file():
                errors.append(f"Decision {kind}: file must exist inside the repository")
                continue
            content = path.read_text(encoding="utf-8")
            if not re.search(r"^Status:[ \t]*ACCEPTED[ \t]*$", content, re.MULTILINE):
                errors.append(f"Decision {kind}: record must be ACCEPTED")
            for label in ("Approver", "Date"):
                match = re.search(rf"^{label}:[ \t]*(\S[^\n]*)$", content, re.MULTILINE)
                if not match or not filled(match.group(1)):
                    errors.append(f"Decision {kind}: {label} must be recorded")
                elif label == "Date":
                    try:
                        value = match.group(1).strip()
                        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                            raise ValueError
                        date.fromisoformat(value)
                    except ValueError:
                        errors.append(f"Decision {kind}: Date must be a valid YYYY-MM-DD date")
    checks = data.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be a list")
    else:
        names = []
        for check in checks:
            if not isinstance(check, dict) or set(check) != {"name", "status", "command", "reason"}:
                errors.append("Each check must declare name, status, command, and reason")
                continue
            names.append(check["name"])
            if check["status"] == "required":
                if not isinstance(check["command"], str) or not check["command"].strip() or (not example and not filled(check["command"])):
                    errors.append(f"Check {check['name']}: required command must be filled")
            elif check["status"] == "not_applicable":
                if not filled(check["reason"]) or check["command"] != "":
                    errors.append(f"Check {check['name']}: not applicable needs a reason and empty command")
            else:
                errors.append(f"Check {check['name']}: unsupported status")
        if any(not isinstance(n, str) for n in names) or len(names) != len(CHECKS) or set(n for n in names if isinstance(n, str)) != CHECKS:
            errors.append("Declare unit, integration, contract, static, build, and smoke exactly once")
    return errors
