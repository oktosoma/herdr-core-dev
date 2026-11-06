# Development lifecycle

This document owns ticket states, review, integration, and release. `HERDR.md` owns permissions. Accepted ADRs define project choices and explicitly approved exceptions.

## Readiness and states

The bootstrap ticket establishes the project's actual test harness and CI. Its own review uses explicit reproducible checks; normal product dispatch waits until the applicable CI gates work. A missing gate is a blocker, not a successful or empty check.

| State | Required evidence / next owner |
|---|---|
| Proposed | Scope, acceptance criteria, dependencies, and unresolved decisions; founder/orchestrator |
| Ready | Approved scope, resolved blocking decisions, verification plan, assigned worker, capacity available |
| Running | Run ID, exact base SHA, branch/directory, terminal ID, and brief; worker |
| Candidate | Committed SHA, changed behavior, verification results, remaining limitations; worker report |
| In Review | Separate clean checkout at candidate SHA; independent reviewer |
| Changes Requested | Findings tied to the reviewed SHA; worker returns a new candidate |
| Accepted | Reviewer verdict and applicable checks tied to an immutable candidate |
| Integrated | Recorded integration base/result SHA and passing required checks; orchestrator |
| Verified | Integration test deployment and required tester/founder acceptance complete |
| Released | Explicit release authorization, deployed artifact/commit identity, health and recovery evidence |
| Blocked / Parked | Reason, owner, preserved work location, and next action; orchestrator records status |

Worker completion is **Candidate**, not acceptance or release. `BACKLOG.md` is the orchestrator-owned outcome register; the existing example row is illustrative, not a state schema. Use `templates/tasks/evidence.md` for complete records. Retain candidate, reviewed, and integrated SHAs as separate fields.

## Dispatch and work

1. The orchestrator records a stable ticket/run ID, approved scope, dependencies, base SHA, directory, branch, assigned role/harness/model, acceptance criteria, required checks, and stop conditions. Use `templates/tasks/worker.md`.
2. A worker uses `task/<ticket-id>` in an isolated checkout. Existing managed cloud checkouts count when isolated; create an additional worktree only for concurrent work sharing a checkout. Never use the directory serving shared dev.
3. Keep related work in the ticket. Report missing decisions or credentials without inventing them. Commit the candidate and report verification outcomes; preserve unexpected local changes.
4. The reviewer checks out that exact SHA in a separate clean directory, inspects the diff and tests, and reproduces relevant checks independently. Only that reviewer issues the verdict. Failed or unrun required checks cannot support ACCEPT.

## Integration: serialize, verify, then advance

All integrations and register transitions use the project lock described in `OPERATIONS.md`.

1. Capture the current `coord/<milestone>` tip as the **expected base**. Check that the candidate is the reviewed SHA and the approval is still valid.
2. Prepare the proposed integration result in a disposable integration checkout. Never experiment with merges in the checkout serving dev. The default policy preserves candidate history through fast-forward or merge commits; squash/rebase requires a recorded project policy and traceable evidence.
3. If the target advanced, merge the expected base into the candidate in isolation. Re-run all applicable required checks on the proposed result. Content changes, conflict resolutions, or a rewritten candidate require renewed independent review. An unchanged reviewed candidate can retain its review only when the proposed merge is clean and the full applicable integration checks pass; record both SHAs.
4. Before promotion, compare the integration branch tip with the expected base under the lock. If it moved, discard stale integration evidence and repeat against the new base. Never force-update the branch to avoid this check.
5. Advance the integration branch to the verified result using the project's approved Git/PR mechanism. Record base, candidate, reviewed, and result SHAs, review verdict, and check evidence. Remote branch rules must require the applicable checks; verify the actual settings at setup.
6. Prepare the replacement build before an announced shared-dev restart. Run readiness and smoke checks; recover to the last accepted deployment if startup fails. Tests use an isolated deployment of the integrated SHA, not the founder's live data.

Do not merge to main during routine integration. A failed check leaves the accepted branch/deployment in place. If a process stops after promotion but before the register update, reconcile Git before retrying; do not repeat the merge blindly.

## Verification policy

Projects map these outcomes to their native tools in ADR-001 and `project.json`:

- Logic tests for changed behavior; integration checks for affected boundaries; contract checks for promised interfaces.
- Applicable lint/static analysis, type checking, build, isolated migrations, health, smoke, and user journeys.
- Reproducible fixtures and isolated resources; no production calls, paid service actions, or destructive operations without the specific authorization.
- Passed / failed / skipped / not applicable / unrun are distinct outcomes. Not applicable requires a reason and reviewer acceptance. An empty test run does not satisfy a required behavioral check.
- Existing tests can adequately cover a change. Add new tests when they protect meaningful behavior or a regression, not to satisfy a count. Native discovery/layout and equivalent warning policies are valid; `--max-warnings=0` is only an ESLint example.
- Define flaky-test ownership and expiry for any approved quarantine; never silently retry until green or disable a required assertion.

High-risk changes (including auth, permissions, payments, destructive data changes, and externally promised contracts) and milestone close-out receive a conditional tester pass. The tester reports findings and severity; critical unresolved security, data-loss, or release-blocking defects halt promotion. The founder accepts any proposed risk exception explicitly. This does not replace independent review or CI.

## Release and close-out

The founder authorizes a named release operator and specific revision/environment. Use `templates/tasks/release.md`: record the approved revision/artifact, checks, tester/founder acceptance, configuration/migration plan, backup/recovery, and health evidence. Main promotion and deployment are separately authorized actions; neither follows automatically from implementation approval.

Mark every ticket integrated, blocked, or parked with evidence. Preserve necessary unmerged work before removing worktrees or branches. Remove only worktrees owned by the completed run; refusal due to local files is a reason to inspect, not to use force. Record adopted decisions, deferred findings, and the next milestone gate. Never delete a branch solely because a worker said it was done.

After a ticket branch is integrated into the integration branch and verified, the orchestrator removes the task branch and its worktree as routine hygiene: remove the worktree first when one exists, then delete the local branch and the remote branch when it was pushed. Verify before deleting that the branch is fully merged into the integration branch and that the worktree holds no uncommitted changes; a branch that is not fully merged is never deleted, and its work is preserved. Never delete an active ticket branch, the integration branch, or main. Deleting a merged branch does not hinder rollback: the merged commits remain in the integration branch history, and the register records the candidate and integration SHAs.
