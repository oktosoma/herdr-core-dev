# Herdr-Core runbook

Model v2.1. This file owns role permissions and runtime operation. `AGENTS.md` is the entry point, `docs/development/SDLC.md` owns workflow transitions, and accepted ADRs record project decisions. The guide is explanatory; it does not silently override these sources.

## Roles and authority

A role is an assignment, not a model name or a continuously running process. One person or harness may fill different roles at different times, but the producer and approving reviewer for a change must be different agents. Record assignments in the brief and register.

| Role | Allowed actions | Boundaries |
|---|---|---|
| Founder | Approves product, architecture, scope, budget, risk acceptance, and release authority | Records decisions through the orchestrator; delegates categories explicitly |
| Orchestrator | Dispatches within the approved milestone; writes the register; serializes integration; coordinates recovery | Does not approve its own implementation, change open decisions, or merge to main/release without explicit authorization |
| Architect | Researches and proposes ADRs on `docs/<area>` | Does not implement product changes, write the register, or hold dispatcher goals |
| Dispatcher (optional) | Starts and collects assigned work under the orchestrator's lock/protocol | No register writes, writable checkout, architecture decisions, or independent milestone advancement. Requires a harness that can run `hc` (see Harness compatibility) |
| Worker | Implements one brief, tests it, and reports a candidate SHA | Own isolated directory; no register writes, shared dev changes, dev/prod DB access, or self-approval |
| Reviewer | Reads and verifies the exact candidate independently; issues ACCEPT / CHANGES REQUESTED / REJECT | Separate clean checkout; no product patches or unapproved decision changes |
| Tester (conditional) | Exercises the integrated candidate in an isolated test deployment; reports reproducible findings | No product patches; no destructive journeys against shared dev; no independent release authority |
| Platform owner | Maintains the harness and CI through reviewed tickets | One accountable owner; its implementation still receives independent review |
| Release operator | Promotes the approved revision when explicitly authorized by the founder | Uses the approved release/migration plan and stops on failed gates |

The release operator is an authorization assigned for a release, not an additional standing agent. A reviewer remains independent even when the worker and reviewer use the same approved model. The orchestrator alone records outcomes in `BACKLOG.md`; other agents submit reports.

## Project runtime profile

`project.json` maps approved decisions to operational values; see `project.example.json`. It records tool versions and official sources, role mappings, worker capacity, required checks, and accepted decision paths. Credentials are supplied separately through the platform or a vault.

- Choose tools/models by required capability and official support. Record tested versions and dates; a successful version check does not establish OSC, model access, or authentication.
- Reference mapping: Codex for reasoning; omp for implementation/review; another supported harness may orchestrate. These are examples, not mandatory model defaults. The dispatcher role is assigned by hc-access capability, not by harness brand (see Harness compatibility).
- Start with one worker and one reviewer. Increase capacity only within the approved profile and measured CPU, memory, disk, and quota limits. Pause new dispatch when the reviewer queue or resource budget is full.
- Do not silently substitute a model, shim an unsupported route, or initiate a new account login when existing injected authentication may be available.
- The dispatcher stays disabled until one ticket completes under direct orchestration. ADR-002 defines a bounded trial and its acceptance/rollback conditions.

## hc operation

Validate these behaviors against the installed version's `hc --skill` and `hc schema` before automation. No hc compatibility claim is established by this template's own unit tests.

- Use one terminal per active agent, a stable project/run name, and `project` / `ticket` labels. Record the terminal ID in the dispatch evidence.
- Report to an explicitly recorded orchestrator terminal ID; do not assume that the current terminal's `HC_TERMINAL_ID` identifies its parent or recipient. Confirm delivery with a harmless startup message.
- `hc wait` is a check-in. Require the candidate/report artifact and exit/check outcome before advancing a ticket. OSC status is observability, not review acceptance or authorization.
- Templates use line-based frontmatter and commands run through `sh`. Render placeholders first. Check shell/PATH in the actual launch context; use the supported login-shell setting or an absolute executable when needed.
- Foreground execution and OSC readiness vary by harness/version. Verify both. `ready: quiet` is a timing fallback, not evidence of agent readiness.
- Holder processes can survive a core restart; processes do not survive host shutdown. Reconcile existing terminals before relaunching after an interruption. Follow the recovery procedure rather than blindly replaying dispatch.
- Do not stop a shared core or kill a terminal the founder is using. Announce the impact of an authorized shared-service restart.

### Harness compatibility

A harness can fill a role only if it can do what the role requires in its own terminal. Most roles need only a shell and the project's tools. The dispatcher (and an orchestrator running inside herdr-core) additionally needs to run `hc` itself — to spawn, read, and wait on other terminals. That requirement is a property of the harness's command-execution path, not of its model.

- **Verified: omp can dispatch.** omp runs commands directly in its terminal shell, so `hc` works there. Verified live 2026-11-08 (herdr-core 0.1.15, omp 18.16.0, GPT-6.1-Terra): an omp dispatcher read its brief, ran `hc ls` / `hc send` / `hc wait`, dispatched a worker, and collected its status. Note: `hc` was not on `PATH` in the agent's shell, so the dispatcher used the absolute path (`/data/home/.local/bin/hc`). Use absolute paths for `hc` and for the agent binary when spawning.
- **Verified: Codex cannot dispatch.** The Codex CLI runs commands through its app-server daemon, which cannot reach the core socket (`/run/user/1000/herdr-core/default.sock`); `hc` fails with `cannot start core: Read-only file system (os error 30)`. Codex remains suitable for reasoning, architect, worker, and reviewer roles, which do not need `hc`. It cannot be the dispatcher (or an in-core orchestrator) until its command path can reach the core.
- **The model is harness-agnostic.** The dispatcher is not tied to Codex, omp, or any other named harness. Any harness qualifies if it can (a) execute shell commands in its own terminal, (b) reach the `hc` binary, and (c) reach the core socket through its command path. A harness that runs commands through a separate daemon or sandbox that cannot see the core socket cannot dispatch, even if it can do everything else.
- **Verify before assigning.** Before giving a harness the dispatcher role, spawn it and have it run `hc ls` (absolute path if `hc` is not on `PATH`) and report the live terminals. A correct terminal list proves it can dispatch; a read-only-filesystem or cannot-reach-core error proves it cannot. Record the harness, version, and test date in the project profile.

## Security and operations

hc is not an access sandbox. Its local API and terminal state have the account's trust boundary, and terminal logs may contain sensitive output. Worktrees share Git metadata and do not prevent cross-directory writes. Use scoped credentials, protected remote branches, separate test resources, and stronger process isolation where required.

Do not expose the raw core socket/API or run it as root. Configure telemetry using the installed tool's documented syntax and the approved project policy. Define log retention and redaction. Never store real values in `project.json`, examples, briefs, or the register.

The monitor is an entry point to the same serialized orchestrator, not a second writer. Its cadence is a profile decision; 15 minutes idle / 5 minutes active is an example. See [operations](docs/development/OPERATIONS.md) for locks, run IDs, checkpoints, and restart handling.

Follow [setup](docs/development/SETUP.md) for a fresh machine and [SDLC](docs/development/SDLC.md) before integrating or releasing.
