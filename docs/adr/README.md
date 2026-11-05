# Architecture decision records

| Record | Subject | Template status |
|---|---|---|
| [ADR-001](ADR-001.md) | Stack, toolchain, and verification | Draft; fill and accept per project |
| [ADR-002](ADR-002.md) | Optional dispatcher trial | Draft; accept or reject per project |

Use the same structure for additional numbered records. Lifecycle: `DRAFT` → `ACCEPTED` or `REJECTED`; an accepted decision can become `SUPERSEDED` only with a link to its replacement. Accepted records identify the approving founder, date, considered alternatives, choice, consequences, and affected tickets/rules. Do not silently rewrite a historical accepted decision.

`project.json` links the accepted records for stack, roles, and release authority. One record may cover more than one category if that is explicit. The operational profile implements these choices; it does not approve them.

The founder can delegate bounded categories of reversible implementation decisions. Record the allowed category, constraints, escalation trigger, and owner. Product scope, security boundaries, budget increases, destructive operations, and release authority remain explicit decisions unless specifically delegated. Agents do not silently resolve an unassigned open question.
