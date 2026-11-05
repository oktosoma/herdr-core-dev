# Release authorization and evidence

- Release ID and target environment: <identity>
- Founder authorization and named release operator: <reference>
- Authorized actions (main promotion, deployment, migration): <explicit list>
- Candidate / reviewed / integrated / released SHA and artifact identity: <revisions>
- Required checks, tester findings, and founder acceptance: <evidence links>
- Unresolved findings and explicit approved risk exceptions: <none or references>
- Configuration/migration plan and execution owner: <plan>
- Previous healthy artifact/configuration: <identity>
- Backup/restore verification and irreversible-change limits: <evidence>
- Announcement, readiness request, and functional smoke check: <plan/results>
- Failure halt/recovery procedure and owner: <plan/results>
- Actual deployment identity, time, and outcome: <result>

Implementation approval is not authorization to release. Do not proceed with unrun required checks or unresolved critical security/data-loss findings. If recovery restores the old deployment, record the attempted release as failed and the recovery outcome separately.
