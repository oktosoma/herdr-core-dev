# Outcome and handoff record

- Ticket/milestone, run/action ID, role, and date: <identity>
- Outcome/state: <Candidate / Blocked / Accepted / Integrated / Verified / Parked>
- Scope and accepted decision links: <references>
- Base SHA / candidate SHA / reviewed SHA / integration base / integration result: <distinct identities; not applicable where appropriate>
- Branch, directory, terminal/report recipient: <locations>
- Changed behavior and acceptance evidence: <results>

| Check | Command and working directory | Result / case counts | Artifact or output reference |
|---|---|---|---|
| <name> | <sanitized reproduction command> | <passed / failed / skipped / not applicable / unrun> | <current-run evidence> |

A zero-test run is not behavioral verification. Explain every skipped, not-applicable, or unrun required check and its effect on acceptance. Record reviewer identity/verdict separately from worker execution. Retain evidence against the correct revision and run.

Blocked handoff: <missing prerequisite, decision/permission owner, preserved work, next action>
Unexpected changes / remaining risks: <details>
Cleanup and recovery checkpoint: <resource ownership and last completed effect>

The orchestrator records outcomes and links in BACKLOG.md. Never paste raw conversation transcripts, credentials, or private terminal logs into the register.
