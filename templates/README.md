# Launch and task templates

`codex.md` and `omp.md` are **unrendered examples** of hc's line-based launch format. Task contracts live under `tasks/`. A launch command is not a complete brief.

1. Select the approved harness/model from the project profile; verify official support and the installed `hc --skill` documentation.
2. Replace the example command and brief placeholders. For omp, replace `<model-id>` before any shell execution: literal angle brackets are shell redirection syntax, not hc variables.
3. Render the selected task contract with ticket/run IDs, role, explicit report recipient, and acceptance criteria. Keep credentials out of the brief.
4. Validate the command and required fields, then install the rendered template under the approved hc template directory. Do not overwrite existing user templates blindly.
5. Inspect `hc templates` and run the harmless readiness/report-delivery exercise in `docs/development/SETUP.md`.

Commands run through `sh`; shell/PATH and readiness behavior are version-dependent. `ready: quiet` in the omp example is a timing fallback until the project's version is verified. Never use it as proof of completion.

A dispatcher terminal must run on a harness that can execute `hc` itself. Verified: omp can dispatch; Codex cannot (its command daemon cannot reach the core socket). Any harness qualifies if it can run shell commands in its own terminal and reach the `hc` binary and core socket — verify with `hc ls` before assigning the role. Use absolute paths for `hc` and the agent binary when they are not on the agent shell's `PATH`. See the runbook's Harness compatibility note for the full analysis.

Spawn workers fresh per task or fix round, with a self-contained brief (goal slice, acceptance criteria, relevant file paths, register entry). After any usage-limit stall, always respawn fresh — never resume the stalled session. Do not let one worker run two or more fix rounds in the same session. The reviewer is a fresh agent with no write access, given only the diff plus the criteria. The register is the blackboard. See the runbook's Worker invocation & context note for the full rule set.

| Contract | Purpose |
|---|---|
| [Worker](tasks/worker.md) | Scope, acceptance, base, resources, and stop conditions |
| [Review](tasks/review.md) | Independent reproduction and verdict tied to SHA |
| [Tester](tasks/tester.md) | Integration journeys in disposable resources |
| [Evidence](tasks/evidence.md) | Candidate, blocked handoff, and durable outcomes |
| [Release](tasks/release.md) | Explicit release authority and recovery evidence |

These files define required information. Filled outcomes can be committed in a project evidence directory; raw prompt/session transcripts and secrets must not be committed. The orchestrator links outcomes from the register.
