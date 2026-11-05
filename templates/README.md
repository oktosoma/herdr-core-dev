# templates/

Example `hc` templates (line-based frontmatter). Copy the ones you use to `~/.config/herdr-core/templates/` on the agent box, then verify with `hc --skill` and `hc templates`.

- `codex.md` — Codex (reasoning).
- `omp.md` — omp (worker). `ready: quiet` until its OSC status is proven on the version in use.

Templates run via `sh`; by default they wait for the first OSC report (30 s timeout).
