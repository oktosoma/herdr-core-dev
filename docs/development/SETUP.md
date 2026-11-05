# Setup and readiness

## Maintain this template

Use Python 3.12 and Node 24. CI uses the exact versions in `.python-version` and `.node-version`; local compatible versions are reported by the doctor. Git and make are also required for the documented workflow. Tests use standard libraries only; there is no package install step.

```sh
python3 scripts/doctor.py --profile template
make check
```

A template checkout intentionally has no application, service, production credentials, or selected product stack. The template CI checks its own contracts. It does not validate hc, a model subscription, or a future project's application.

For guide changes, also verify in a real browser with page networking disabled: clipboard success, permission rejection and unavailable-API fallback; search followed by contents/fragment navigation; keyboard operation; and page widths of 320, 390, 768, and 1280 px. The Node tests cover script behavior through a DOM adapter; they do not measure rendered layout. Record the browser version and actual outcomes. This additional check is separate from the dependency-free CI suite.

## Initialize a project

Follow `ADOPTION.md` before any push. Complete ADR-001 and the project decisions for role mapping and release authority. Copy `project.example.json` to `project.json`, replace every required placeholder, and link accepted ADR files. The profile is reviewed configuration, not a credential store. Do not include secret values in tool sources, check commands, or decision documents.

```sh
python3 scripts/doctor.py --profile project --config project.json
```

The project doctor validates the profile and decision references, checks required tools on PATH, and compares their `--version` output with the declared exact version. It does not install tools, start agents, log in, execute configured check commands, alter Git identity, or touch databases. Version checks run without a shell and have a timeout. Run the doctor only on reviewed project configuration and PATH.

The doctor succeeding establishes prerequisites only. Execute the project's mapped checks separately, confirm tests actually ran, and retain outcome evidence. Complete the startup exercise below before declaring the agent loop ready.

## Tool provenance and installation

Record each selected tool's exact version and authoritative HTTPS distribution/documentation source. Use the vendor's supported installation and verification procedure, including package signatures/checksums and TLS verification. Do not use guessed package names or disable integrity checks.

- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/en/download
- Git: https://git-scm.com/downloads
- Codex: https://developers.openai.com/codex/cli and https://github.com/openai/codex
- hc and omp: the template does not currently supply verified distribution URLs or pins. The project owner must provide the official source and supported version in its accepted toolchain decision. Keep project readiness blocked until those entries and installation are verified.
- Anti-slop: if required by the project, record the authoritative source, exact version, harness installation location, and verification evidence. A named but unavailable skill is not implicitly installed.

Installation procedures must be repeatable and preserve existing user configuration. Prefer repository-supported settings and approved runtime bindings. If an installer changes global configuration, document the effect before adopting it. Never embed authentication in an install command or profile.

## Actual launch and authentication checks

1. Confirm the approved role/harness/model is available using existing authentication through its supported route. Platform Git authentication may be supplied by a proxy; missing token variables alone do not prove missing access.
2. Validate `hc --skill`, `hc schema`, and template behavior against the installed version. Render the chosen launch template; no placeholder may remain in its executable command or task brief.
3. Check executable discovery in the same shell context used by hc. Verify foreground behavior, readiness, OSC reporting when supported, and explicit delivery to the orchestrator's recorded terminal ID. A quiet terminal is not enough.
4. Run a harmless task that creates no external side effect and produces a concrete report. Verify its exit/status and report receipt. Record versions and date; do not generalize one test to all later versions.
5. Run the project's real checks and a representative readiness request in disposable resources. Record actual counts/outcomes, cleanup, and the independent reviewer verdict.
6. Verify branch protections, required status checks, scoped permissions, release authority, resource capacity, and the control lock. Rehearse recovery before enabling the monitor or optional dispatcher.

## Runtime profiles

A private Linux agent box can use supported hc shell configuration and approved SSH/VPN/tunnels. A managed cloud task should use its existing checkout, network proxy, credential bindings, and isolation. Do not install another VPN or assume direct credentials are available when the platform supplies them through a proxy. Live processes do not survive publication/restoration unless the platform explicitly guarantees that behavior.

Keep provider-specific runtime limits, costs, cooldowns, and public URLs in the derived project's deployment documentation with a source and verification date. They are not universal model requirements. Required startup instructions must name working directories and functional readiness checks; a PID or listening port alone does not prove readiness.
