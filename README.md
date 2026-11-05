# herdr-core-dev

Template repo for starting a new project with the **Herdr-Core Development Model** (general guide: `docs/guide/index.html`, also published as the "Herdr-Core Development Model" guide, v1.2).

## How to use

1. Clone this repo as the start of a new project (or use it as a template).
2. Rename the project + fill in the placeholders in `docs/adr/ADR-001.md` (stack, tooling, pinning).
3. Fill `docs/development/BACKLOG.md` with the first milestone + tickets + the list of open decisions.
4. Prepare the agent box (see `HERDR.md` § setup).
5. The founder decides the role→harness→model mapping, capacity, and the dispatcher trial.
6. Dispatch the first ticket. The register is written only by the orchestrator.

## Repo contents

- `HERDR.md` — runbook: roles, the core, dispatcher, monitor, model policy.
- `AGENTS.md` — instructions for agents working in this repo.
- `docs/guide/index.html` — the full general guide (a single self-contained HTML file). Keep it in sync: a model change updates the guide in the same commit, with a dated entry in its Versions section.
- `docs/development/BACKLOG.md` — the register (source of truth for status + decisions).
- `docs/development/SDLC.md` — ticket lifecycle, review, integration.
- `docs/adr/` — numbered ADRs (ADR-001 stack, ADR-002 dispatcher).
- `apps/` — new products live here (the stack is decided per project).
- `templates/` — example `hc` templates (copy to `~/.config/herdr-core/templates`).

## Hard rules (summary)

- The register is written only by the orchestrator. Agents never write the register.
- One ticket → one branch → one worktree. Review from a separate checkout; independent reproduction is mandatory.
- Open decisions are founder decisions. The orchestrator never makes them.
- Secrets live only in mode-600 env files / the vault — never in the repo.
- Full guide: `docs/guide/index.html` (v1.2, 2026-11-05).
