# herdr-core-dev

An English-language template for developing projects with the Herdr-Core Development Model. Model **v2.2**; template **2.2.0**. Version metadata lives in [template.json](template.json). Read the [guide](docs/guide/index.html) for the explanation and [HERDR.md](HERDR.md) for operational rules.

## Start a project

1. Create a **new repository from this template** in GitHub. If using a normal clone instead, follow [adoption](docs/development/ADOPTION.md) and verify the destination remote before any push.
2. Read [setup](docs/development/SETUP.md). Fill ADR-001 with the approved stack and checks, and decide role assignments, release authority, capacity, and whether to trial a dispatcher. Record accepted decisions in the [ADR index](docs/adr/README.md).
3. Copy `project.example.json` to `project.json`, fill the reviewed operational values, and link accepted ADRs. This profile contains no credentials. Run `python3 scripts/doctor.py --profile project --config project.json`.
4. Have the orchestrator initialize the register and `coord/<milestone>`. Complete the bootstrap ticket for the project's real test harness and CI before normal product dispatch.
5. Run one small ticket through the [SDLC](docs/development/SDLC.md), using the [task templates](templates/README.md). Keep review, integration, verification, and release distinct.

For this template's own maintenance, use Python 3.12 and Node 24 (CI pins are in `.python-version` and `.node-version`). There are no third-party test dependencies:

```sh
python3 scripts/doctor.py --profile template
make check
```

The doctor is a prerequisite check, not proof that application tests or agent dispatch passed. Product projects map checks to their own native tools; this template does not impose an application stack.

## Documents and ownership

| File | Owns |
|---|---|
| [AGENTS.md](AGENTS.md) | Agent entry instructions and scope |
| [HERDR.md](HERDR.md) | Role permissions and runtime operation |
| [SDLC.md](docs/development/SDLC.md) | Ticket states, review, integration, and release |
| [BACKLOG.md](docs/development/BACKLOG.md) | Project outcomes and decisions; orchestrator writes it |
| [ADRs](docs/adr/README.md) | Approved project choices and explicit policy overrides |
| [Setup](docs/development/SETUP.md) | Tool sources, prerequisites, and readiness |
| [Operations](docs/development/OPERATIONS.md) | Locks, recovery, isolated verification, and releases |
| [Adoption](docs/development/ADOPTION.md) | Project creation and template upgrades |
| [Templates](templates/README.md) | Harness launch examples and structured task/evidence contracts |
| [Guide](docs/guide/index.html) | Explanatory reference; update with policy changes |

`make check` validates documentation, example profiles, policy versions, and guide behavior. GitHub Actions runs the same checks. Configure the `template-checks` job as a required check in repository settings; a workflow file does not establish branch protection by itself.

Changes to the operating model must update its canonical document, guide, version metadata, and dated guide history in the same change. [Adoption](docs/development/ADOPTION.md) explains how derived projects consume updates.
