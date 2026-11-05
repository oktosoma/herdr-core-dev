# Project adoption and template updates

## Create the destination safely

Prefer GitHub's **Use this template** flow to create a repository owned by the intended account/organization. Choose visibility explicitly; the source template being private does not establish the destination setting. Clone the new repository and verify its fetch/push destination before the first push. Do not print a remote URL if it contains credentials.

For a normal clone, preserve the template's history if desired, create the intended empty destination, and deliberately configure the new origin. Record the source template as an upstream only if that fits the project's permissions. Verify both fetch and push destinations. Do not remove history, overwrite local changes, or push back to the template as part of initialization.

## Initialization checklist

- Rename the project and record the adopted `template_version` in `project.json`.
- Accept ADR-001 and decisions covering role mapping, resource capacity, risk/decision delegation, and release authority. Reject or accept the optional dispatcher trial explicitly.
- Fill the operational profile without credentials; run the project doctor. Accepted decision paths must point to files inside this repository.
- Have the orchestrator initialize the register and create `coord/<milestone>` from a recorded base. Assign a bootstrap ticket for applicable checks and CI before normal product work.
- Install project-specific dependencies with a lockfile or equivalent, provision disposable verification resources, and record actual readiness evidence.
- Configure and verify remote branch rules and required check names. Add project-specific ownership review for sensitive paths. A local CODEOWNERS file alone does not enforce protection.
- Run one small ticket through independent review, integration, recovery rehearsal, and milestone verification. Authorize release separately.

Unfilled placeholders are valid in this source template. They are blockers in a project profile presented as ready. Template mode and project mode intentionally make different checks.

## Upgrade an existing project

1. Read the source template's dated guide history and compare the adopted version with the proposed version. Model 2.0 clarifies role exceptions, separates Candidate/Accepted/Integrated/Released, adds a serialized integration/recovery contract, and moves hardcoded tool/hosting assumptions into project choices.
2. Open a scoped upgrade ticket. Review changes against accepted project ADRs; preserve overrides, application files, secret bindings, and local work.
3. Apply the relevant changes through normal review and CI. Never copy the entire template over an initialized project or replace its register with the example.
4. Run template checks that still apply and the project's affected checks. Record any deferred migration, then update the adopted version only when the upgrade is complete.
5. Keep this source template's model version in `template.json` synchronized with its README, guide, runbook, and profile example. A derived project records adoption in its own profile; it need not mirror every future template release immediately.

Contribute generally useful improvements back through a separate reviewed change. Remove project names, ticket history, internal service addresses, and secrets before submission. Repository owners decide distribution/reuse rights; do not assume that a private template or an external skill grants a public license.
