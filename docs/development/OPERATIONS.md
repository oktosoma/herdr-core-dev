# Operations and recovery

## Serialized control

Use one project-scoped lock for dispatch, integration, and register transitions. All entry points, including manual orchestration and cron, must acquire it. On a single Linux host, a nonblocking `flock` on a persistent local path outside worktrees is sufficient. For multiple control hosts, choose a shared transactional lock/lease mechanism in an accepted ADR; local flock does not coordinate hosts.

The lock path is stable for the project, not a per-run temporary file. A busy lock means skip the tick or wait within a bounded timeout. Do not delete the lock file to bypass another owner. Pause new dispatch if worker capacity, reviewer backlog, disk, memory, or quota limits are reached.

Record a stable run/action ID before a side effect. Keep durable, non-secret checkpoints outside transient terminal output. Each action records intent, expected prior state, effect identity (terminal ID or commit SHA), and completion. `BACKLOG.md` remains the outcome register; checkpoints are operational recovery state, not an alternative decision authority. Do not claim this protocol is implemented merely because a cron entry exists.

## Recovery procedure

1. Acquire the control lock. Inspect Git refs, candidate files, active terminals, current deployment identity, and the last durable checkpoint.
2. Reconcile the intended action with actual state. A terminal with the recorded run ID may already exist; an integration SHA may already have advanced the branch.
3. If the effect completed, record the missing outcome once. If it did not, retry using the same action identity and current authorization. If evidence is ambiguous, mark Blocked and preserve work for inspection.
4. After host restart, relaunch only absent sessions and deliver the saved scope plus current evidence. Revalidate authentication and runtime resources. Do not assume snapshot restoration preserves processes or connections.
5. OSC `done`, a PID, or an open port is not enough. Require the role's report/check artifact and a representative functional request for a service.

Before enabling unattended operation, rehearse duplicate ticks, a stopped worker, a stale OSC report, and interruption after merge but before register recording. Record the results. Keep the dispatcher disabled until its accepted trial passes these controls.

## Verification resources

Allocate databases, schemas, ports, directories, and external-service test accounts by project/run ID. Credentials must grant access only to the intended disposable resources. Check the target identity before migrations or destructive setup. Never infer a safe database from a convenient URL or reuse a production binding for tests.

Build an isolated test deployment from the integration SHA for tester journeys. The founder's shared dev environment is a separate target. Cleanup removes only resources tagged/owned by the run, after retaining useful failure evidence. Use timeout and resource limits; a crashed run must have a recoverable cleanup record.

## Credentials, local access, and logs

Worktrees share Git metadata and are not a security sandbox. If roles require enforced local separation, use separate accounts/containers and scoped mounts. Avoid broad sudo in agent runtimes. Give remote write/release access only to authorized roles; configure protected branches, required checks, and ownership reviews in repository settings and verify those settings.

Use the existing platform credential route or approved vault. Inspect binding names/presence, not values. Secret scanning complements `.gitignore`; ignoring a file does not remove prior history. Define terminal/log access, redaction, retention duration, and deletion ownership. After suspected exposure, stop propagation, rotate the affected credential, and record a sanitized incident outcome.

## Release recovery

Before an authorized release, identify the previous healthy artifact/configuration and the owner able to restore them. Verify the database backup/restore strategy before irreversible migrations. Prefer compatible expand/contract migrations; do not invent a down migration for data that cannot be reconstructed.

Prepare and check the replacement before announcing a short shared-service interruption. Promote the approved artifact, make a representative functional request, and record the actual deployed revision. On failed health or data validation, halt further promotion and follow the approved recovery plan. A failed release is recorded as failed even if the old deployment was restored successfully.
