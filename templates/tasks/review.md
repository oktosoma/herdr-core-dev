# Independent review contract

- Ticket / run ID and worker identity: <id/producer>
- Reviewer identity, harness, model: <assignment distinct from producer>
- Candidate SHA and base SHA: <immutable revisions>
- Separate clean checkout: <path>
- Approved scope, decisions, acceptance criteria: <links>
- Required checks and isolated resources: <plan>

Inspect the actual diff and relevant code, instructions, and tests. Independently execute required checks at the named SHA; do not trust a worker's transcript as evidence of execution. Report behavior, regressions, scope deviations, and remaining uncertainty. Do not patch the product or approve your own output.

Verdict: <ACCEPT / CHANGES REQUESTED / REJECT>
Reviewed SHA: <sha>
Checks: <command, directory, outcome/counts, artifacts>
Findings: <severity, file/line, reproduction, required correction>
Not applicable / unrun: <reason and effect on verdict>

A changed candidate invalidates the verdict for that candidate. Unrun required checks block ACCEPT. Open decisions go to the founder through the orchestrator.
