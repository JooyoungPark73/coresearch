# Coresearch Routing

## Skill selection

Pick one primary skill.

- `research-design`: contribution, claim ledger, evidence plan, venue strategy;
  it decides what the paper may claim.
- `research-survey`: verified papers, related-work map, novelty risk.
- `research-write`: evidence-bounded local rewriting, section drafting,
  author-approved argument realization, semantic revision, and concept
  decomposition. It decides how approved claims and evidence are expressed,
  never invents research, and does not forecast scores.
- `research-review`: simulated venue review, score, blockers.
- `research-verify`: citation, number, source-faithfulness audit.
- `research-rebuttal`: reviewer response strategy.
- `research-engineer`: research code, experiments, datasets, benchmarks, artifact release.
- `research-loop`: hypotheses, validators, sandbox, and host-neutral durable mission design.
- `research-survey` owns open-access PDF batch download via its in-skill crawler.
- Analytical skills (`research-gap`, `research-dialectic`, `research-causal`, `research-qualitative`, `research-audit`, `research-adversary`) → see [reasoning-skills.md](reasoning-skills.md).

## Field modes

- Field/tone uncertainty → read `field-modes.md`, then route to `research-design` or `research-write`.
- Research importance / contribution object uncertainty → read `research-rules.md`, then route to `research-design`.

File-format output (`.docx`/`.pdf`/`.pptx`/`.xlsx`/web) is owned by the user via external tools; Coresearch owns research content and claim integrity, not format mechanics.

## Native role and host routing

Select at most one fixed role per bounded assignment when delegation materially
improves quality, speed, or safety. The parent may run multiple independent
assignments concurrently and owns their dependency joins and integration. Use
[agent-routing.md](agent-routing.md) for the eight-role catalog, capability
boundaries, escalation, and required handoff fields.

Use [execution-adapters.md](execution-adapters.md) when a durable run needs
Codex goal continuation or Claude Code session continuation. Choose one host
adapter for a run. Host execution owns continuation; `coresearch` remains the
only stage router and every terminal role or run returns here before the next
skill is selected.
