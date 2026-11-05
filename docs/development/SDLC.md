# SDLC

## Ticket lifecycle

1. **Dispatch (orchestrator):** a brief with the goal, acceptance criteria, base commit, worktree, harness + model, and a hard stop clause.
2. **Work (worker):** one ticket → one branch `task/<ticket-id>` → one worktree. Reports DONE with a candidate commit SHA + evidence.
3. **Review (single reviewer):** checks out the candidate from a SEPARATE checkout; independent reproduction is required; verdict ACCEPT / CHANGES REQUESTED / REJECT + reasons.
4. **Integration (orchestrator):** merges into `coord/<milestone>` (merge-first if the branch moved, re-verify, then merge). Updates the register. Dev keeps serving from the integration branch; the only pause is a brief rebuild/restart at integration, announced first.
5. **Next:** dispatch the following ticket; the monitor advances one step per check.

## Rules

- The register is written by the orchestrator only. Open decisions belong to the founder only. Do not merge to `main`. Do not dispatch beyond the running milestone.
- Agents do not touch the dev database — verify with disposable DBs; migrations joining integration are announced first.
- Capacity: no limit on active agents; single-reviewer discipline.
- CI: pinned install → lint/typecheck/unit/build → isolated DB + migrations + integration → contract validation → built apps + health + smoke. Harness + CI are owned by one platform owner.
