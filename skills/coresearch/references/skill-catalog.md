# Coresearch Skill Catalog

## Owned by Coresearch harness

`coresearch`, `research-design`, `research-survey`, `research-loop`, `research-gap`, `research-dialectic`, `research-causal`, `research-engineer`, `research-qualitative`, `research-write`, `research-review`, `research-rebuttal`, `research-verify`, `research-audit`, `research-adversary`.

## Shared evidence infrastructure (one file per skill)

The analytical/audit skills run over ONE shared evidence model so outputs are
traceable source → claim → conclusion. Each skill loads a single per-skill ref:

- `evidence-grounding.md` — evidence object + claim object (one definition),
  `claim_type` enum, 3-dim confidence + rating rules, source priority + evidence
  levels, the 10 quality gates + gate↔skill map. **The per-skill load.**
- `research-contract.md` — orchestrator input contract + contribution↔evidence
  table + harness rules + integrity floor. Loaded once at run start, not per skill.
- `state-ledger.md` — orchestrator state schema + read/update protocol. Loaded
  only by the router.
- `reasoning-skills.md` — disambiguation table + cross-skill pipelines. Router-only.

Per-invocation load: analytical/audit skills = skill + `evidence-grounding.md`; a multi-skill run also loads `state-ledger.md`; discovery/manuscript skills = skill only.

## No shim aliases

Coresearch uses canonical `coresearch` and `research-*` names only. Old `paper-*`, `claim-check`, `pdf-crawl`, `rebuttal-plan`, and `research-guidelines` shims are intentionally not managed by this harness. File-format output (`.pptx`/`.docx`/`.xlsx`/web) is produced by the user with external tools; no format-mechanics skill is owned.

## Native role catalog

Skill names and native role names are different namespaces. `coresearch` may
delegate bounded assignments to eight installed provider-neutral roles, with
one fixed role per assignment. The parent may run independent assignments
concurrently and owns their joins and integration:

- `coresearch-planner`
- `coresearch-researcher`
- `coresearch-reader`
- `coresearch-implementer`
- `coresearch-experimenter`
- `coresearch-debugger`
- `coresearch-synthesizer`
- `coresearch-verifier`

The canonical responsibilities, capabilities, intended skills, exact provider
models, and efforts live in [`agents/manifest.json`](../../../agents/manifest.json).
Use [agent-routing.md](agent-routing.md) for selection, bounded handoff, and
re-entry rules. Use [execution-adapters.md](execution-adapters.md) for Codex
goal and Claude session continuation.

File-format output (`.docx`/`.pdf`/`.pptx`/`.xlsx`/web) is owned by the user via external tools; Coresearch owns research content and claim integrity, not format mechanics. Do not bulk-copy proprietary external-skill text into this repo.
