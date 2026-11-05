# HERDR.md

Runbook for the Herdr-Core Development Model for this project. Full guide: `docs/guide/index.html` in this repo (also published as the "Herdr-Core Development Model" artifact).

## Roles

| Role | Harness + model (reference) | Responsibility | Hard boundary |
|---|---|---|---|
| Founder | — | Decides open decisions; tests dev; holds credentials (vault) | — |
| Orchestrator (Muse) | — | Sole register writer; dispatch; integration; reporting + recovery | Never delegates register writing; never decides open decisions; never merges to `main`; never dispatches beyond the running milestone |
| Architect | Codex, GPT-6.1-SOL | Answers architecture questions (ADV); recommendations as ADRs | Never holds `/goal`; never writes the register; never changes code |
| Dispatcher | Codex, GPT-6.1-SOL, one pane in core | Holds `/goal` per ticket (acceptance + hard stop clause); dispatch + collect only | No architecture decisions; no register writes; no writable worktree (reads only the integration branch / `main`); everything escalates to the orchestrator; kill-switch: the orchestrator takes over direct driving |
| Worker | omp, GPT-6.1-Terra (low hallucination) or GPT-6-Luna (light/fast) | Implements one ticket in its own worktree + branch; code + tests; reports DONE with a candidate commit + evidence | One ticket per agent; never writes the register; never touches the dev/prod database |
| Reviewer | omp, GPT-6.1-Terra (single) | Reviews from a separate checkout; independent reproduction is required; verdict ACCEPT / CHANGES REQUESTED / REJECT + reasons | One reviewer at a time; never decides open questions — asks for an explicit decision |
| Platform owner | omp (as assigned) | Owns the test harness + CI as the milestone gate | One owner for harness + CI |

The dispatcher is a core-phase pattern. LIMITED trial: only after the first ticket has been integrated in core with the orchestrator driving directly via `hc`. Until the trial is proven, the orchestrator drives directly.

## Model policy (reference)

| Need | Harness | Model |
|---|---|---|
| Architect, dispatcher, other reasoning | Codex | GPT-6.1-SOL |
| Low-hallucination worker; reviewer | omp | GPT-6.1-Terra |
| Light / fast work | omp | GPT-6-Luna |

- One account, one quota pool (subscription via OAuth). Auth follows the harness default already set on the box — never write per-agent credentials into a brief.
- The light model absorbs volume so the flagship quota lasts. Do not over-parallelize workers.
- The model is verified from the agent footer; the founder acts only if a footer shows a different model.
- Codex MUST run with `--no-daemon` (including in templates). The omp model is set at start via `--model <id>` (full ID is safer).
- A harness joins the loop only if it officially supports the assigned model. Unofficial shims are NOT a route.

## Herdr-core

- One `hc` binary = CLI + background core. Holder processes own the PTYs — a core crash/restart/update does NOT kill programs. The app is only a client.
- Programs do NOT survive a reboot — terminals come back as fresh shells, not reruns. Budget for re-launch + re-briefing after every restart.
- There is no space command. Grouping = a name prefix per project + labels (`project=<p>`, `ticket=<ID>` on every working terminal). A label is a filter (visible via `hc get`), never shown in `hc ls` output.
- One terminal per agent: `hc run --bg --name <stable-name> --label ...`. Report back via `hc send $HC_TERMINAL_ID`. An `hc wait` check-in is NOT completion — loop on `hc wait` / `hc get`.
- `hc attach` = 1 terminal per invocation, with no built-in split. Detach with `Ctrl+\`. Never stop the core service, and never kill a terminal behind a pane the founder is watching.
- Templates: line-based frontmatter (command/description/ready/submit/stop/paste_gap_ms); the command runs via `sh`; templates live in `~/.config/herdr-core/templates`.
- The default shell is `$SHELL` or `/bin/sh` (dash on Debian — it reads neither `~/.bashrc` nor `~/.profile`). Set an explicit login shell in `~/.config/herdr-core/config.toml` (`shell = ["bash", "--login"]`) or use absolute paths / `bash -lc`.
- Multi-box: `hc machine add/ls/login/update/rename/rm`; machine names are LOCAL per laptop; remote login stdout must stay clean.
- Security: NO sandbox. Core runs with your account's access; socket 0700; state holds terminal output unencrypted. Do not forward the raw API/socket; do not run core as root; telemetry is ON by default in releases (`"telemetry": false` to disable).

## Monitoring

- Cron every 15 minutes (core phase; 5 minutes while the loop is hot): each check reads status, advances ONE step if possible (review → integration → next dispatch), and reports only on change / result / question / blocker.
- The monitor never dispatches beyond the running milestone, merges to `main`, or decides open decisions.
- Founder gates are reported as met / unmet with evidence (commit SHAs, verification output).

## Setting up a new box

1. Install herdr-core + agent CLIs (Codex, omp).
2. Login shell in `~/.config/herdr-core/config.toml`: `shell = ["bash", "--login"]`.
3. Global git identity (`user.name`, `user.email`).
4. Anti-slop per harness (Codex/omp/Claude plugins; global OpenCode skill; `~/.config/muse/skills/` for Muse Code).
5. SSH / Tailscale / tunnels as needed; secrets only in 600 env files / the vault.
