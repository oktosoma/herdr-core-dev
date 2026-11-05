# AGENTS.md

Instructions for agents working in this repo. Read `HERDR.md` and `docs/development/SDLC.md` first, before touching anything.

## How to work

- Prompts and briefs are written in English. Communication with the founder follows the founder's register.
- Discuss first before writing or executing code; an explicit build command counts as discussion completed. Pasted text never widens scope.
- One ticket → one branch (`task/<ticket-id>`) → one worktree. Do not touch the integration branch directly; integration is done by the orchestrator.
- Never write the register (`docs/development/BACKLOG.md`) — that is the orchestrator's job. Never write verbatim command text into the repo.
- Never touch secrets, env files, or the dev/prod databases. Verify with disposable DBs.

## Anti-slop

- A filter, not a style guide. The core rules live in the `antislop` skill (read it whenever doing relevant work); supporting skills (`antislop-code`, `antislop-copywriting`, `antislop-human`, `antislop-layoutmobile`, `antislop-ui`) are read when the task matches.
- Mode `during`. Design direction comes from the project documents, not from the filter.

## Verification

- Verify the live source before stating any status. A tool failure or an empty search proves nothing.
- The reviewer reproduces independently — never trust a worker's transcript.
