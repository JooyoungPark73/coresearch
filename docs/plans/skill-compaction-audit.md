# Coresearch Skill Compaction Audit

## Conclusion

The skill layer is functionally rich but over-specified. The main problem is
context and routing cost, not disk size:

- all fifteen descriptions compete during discovery;
- selected entrypoints are commonly 700–1,300 words;
- broad requests load `coresearch` before another large skill;
- several references repeat routing or field rules; and
- six narrow analytical skills are better expressed as conditional modes.

Recommended target: **eight core skills plus optional qualitative analysis**.

1. `coresearch`
2. `research-design`
3. `research-survey`
4. `research-loop`
5. `research-engineer`
6. `research-write`
7. `research-review`
8. `research-verify`
9. `research-qualitative` as optional or explicit-only

All current research capabilities can be retained. The eight provider roles
and their exact model/effort pins remain unchanged; role routing is orthogonal
to skill consolidation.

No compaction is implemented by this audit.

## Measurements

Word counts are a host-neutral context proxy, not exact token counts.

| Surface | Current size | Why it matters |
| --- | ---: | --- |
| Fifteen descriptions | 681 words / 5,465 characters | Catalog cost and overlapping activation |
| Fifteen `SKILL.md` files | 12,476 words | Selected-skill context |
| Eighteen Markdown references | 10,771 words | Conditional context when loaded |
| `coresearch/SKILL.md` | 1,339 words | Paid before a routed target skill |
| `research-survey/SKILL.md` | 1,322 words | Heavy for short literature requests |
| `research-loop/SKILL.md` | 1,195 words | Mixes mission, schema, delegation, execution, and state |
| `research-write/SKILL.md` | 1,130 words | Local edits inherit whole-paper rules |
| `research-design/SKILL.md` | 1,069 words | Forces a large design contract |
| Installed project template | 1,695 words | Adjacent always-on routing cost when installed in full |

Repeated structure:

- fourteen skills have fixed `Output`, `Reject`, and `State & Handoff`
  sections and the same re-entry sentence;
- operating-envelope rules occur in eleven entrypoints;
- quality-parity rules occur in thirteen;
- simulator-fidelity and PPA rules occur in twelve; and
- warmup/repetition rules occur in thirteen.

Four route references—`routing.md`, `stage-map.md`,
`reasoning-skills.md`, and `skill-catalog.md`—contain 1,554 words in addition
to the route map already in `coresearch/SKILL.md`.

Six analytical skills use custom `depends_on` and `produces` frontmatter:
`research-gap`, `research-dialectic`, `research-causal`,
`research-qualitative`, `research-audit`, and `research-adversary`. Native skill
loaders are not guaranteed to interpret those fields as reference loading or
write authorization. Direct invocation can therefore miss the intended shared
contract while still seeing a fixed output path.

### Plausible current load paths

References are progressive, so these are possible paths rather than claims
that every host always loads every linked file.

| Request path | Approximate words before user material |
| --- | ---: |
| Direct local `research-write` | 1,130 |
| Routed local writing | 2,742 |
| Analytical route with reasoning + evidence | 3,300–3,700 |
| Analytical route with contract, ledger, and field mode | 4,500–5,200 |
| Whole-paper writing with relevant references | 5,000–6,000 |
| Durable loop with state, adapters, roles, and safe execution | 5,500–6,100 |

`crawler.py`, validation code, old plans, and ignored logs do not normally
consume task context unless explicitly inspected. They are not the priority for
this skill-focused compaction.

## What is too verbose or rigid

### Repeated field methodology

Design, survey, gap, dialectic, causal, loop, engineering, review, rebuttal,
verify, audit, adversary, and writing restate similar systems/cloud,
ML-systems, and architecture checklists. This both consumes context and creates
near-duplicate rules the model must reconcile.

Keep one authoritative `field-modes.md`; each skill should load only the
applicable subsection when a claim actually depends on it.

### Mandatory report shapes

Most skills require a full report even for a narrow question: an eleven-part
design contract, three causal views, full review score sheets, multi-table
surveys, or complete rebuttal plans. This encourages field completion instead
of judgment.

Use two levels:

- ordinary request: requested artifact first, followed only by material gaps;
- durable/audit request: load the complete schema from a reference.

### Duplicate routing authorities

Skill ownership is repeated in the router, four router references, and the
project template. Keep one compact route table in `coresearch/SKILL.md` and
derive inventory checks from `skills/manifest.json`. Keep role routing and host
continuation in separate conditional references.

### Narrow analytical routes

Gap scouting, dialectical synthesis, causal modeling, methodology audit, and
adversarial checking are valuable lenses, but they frequently co-occur inside
one user request. Making each a stage causes route churn and pipeline-shaped
answers.

Move them under broader owners:

- gap and causal hypothesis design → `research-design`;
- conflict synthesis → `research-survey`;
- methodology, adversarial, and causal-claim audit → `research-verify`.

### Overlapping descriptions

Descriptions list venue families, detailed procedures, outputs, and many
exclusions. Keep only the primary outcome, likely trigger, and one useful
boundary. Venue lists and schemas belong in conditional instructions.

### Excessive absolutes

Exact numbers of hypotheses or contribution bullets, fixed step counts,
mandatory matrices, and mandatory score forecasts constrain open-ended work.
Absolute language should be reserved for evidence integrity, non-fabrication,
causal identification, confidentiality, state ownership, permissions, and
durable terminal validators.

### Repeated execution policy

`coresearch`, `research-loop`, and `research-engineer` repeat experiment-unit,
smoke-test, claim-bearing evaluation, retry, regression, delegation, and stop
rules. Five-word phrase containment is about 14% between loop and engineer.

Keep ownership distinct:

- `coresearch`: select stage and bounded role;
- `research-loop`: mission, validator, sandbox, retry, and terminal contract;
- `research-engineer`: implement and run reproducible work;
- `execution-safe.md`: long-command logging and cancellation.

### Eager artifact paths

Remove `produces` from discovery frontmatter. Ordinary invocations should be
in-chat. Durable paths belong in an explicit mission or output reference.

## Per-skill disposition

| Skill | Words | Recommendation |
| --- | ---: | --- |
| `coresearch` | 1,339 | Keep; reduce to classification, one route table, reference triggers, re-entry |
| `research-design` | 1,069 | Keep; adaptive modes; absorb gap and causal hypothesis design |
| `research-survey` | 1,322 | Keep; move crawler manual to a reference; absorb conflict synthesis |
| `research-loop` | 1,195 | Keep; move mission/result schemas to references; remove engineering cadence |
| `research-engineer` | 884 | Keep; implementation/execution only; load field rules conditionally |
| `research-write` | 1,130 | Keep; shorten entrypoint while preserving its progressive modes |
| `research-review` | 795 | Keep; absorb rebuttal as a response mode/reference |
| `research-verify` | 692 | Keep; add fact, methodology, adversarial, and causal-audit modes |
| `research-gap` | 715 | Merge into `research-design` |
| `research-dialectic` | 473 | Merge into `research-survey` |
| `research-causal` | 472 | Shared conditional reference for design and verification |
| `research-audit` | 666 | Merge into `research-verify` |
| `research-adversary` | 569 | Merge into `research-verify` |
| `research-rebuttal` | 745 | Merge into `research-review` |
| `research-qualitative` | 410 | Keep optional/explicit-only, or package separately if rarely used |

## Target capability map

| Capability | Target owner |
| --- | --- |
| Contribution, venue, claims, evidence plan | `research-design` |
| Gap discovery/falsification | design → `gap-analysis.md` |
| Causal hypothesis/identification planning | design → shared `causal-reasoning.md` |
| Literature retrieval, mapping, closest work | `research-survey` |
| Conflicting-literature synthesis | survey → `conflict-synthesis.md` |
| Durable missions and validators | `research-loop` |
| Code and experiment execution | `research-engineer` |
| Drafting and semantic revision | `research-write` |
| Venue assessment and scoring | review assess mode |
| Rebuttal/discussion response | review respond mode → `rebuttal.md` |
| Citation and factual checks | verify fact mode |
| Methodology audit | verify methodology mode → `methodology-audit.md` |
| Bias/counterevidence attack | verify adversarial mode → `adversarial-audit.md` |
| Causal-claim audit | verify + shared `causal-reasoning.md` |
| Qualitative coding/themes | optional `research-qualitative` |

Do not compact further by merging:

- design with writing;
- survey with verification;
- loop with engineering;
- review with verification; or
- Coresearch routing with Codex/Claude continuation.

Those are genuine responsibility and state boundaries. Six or fewer broad
skills would recreate monolithic prompts with internal mode ambiguity.

## Suggested budgets

Treat these as review warnings, not hard correctness limits.

| Surface | Target |
| --- | ---: |
| Description | 20–35 words; normally under 220 characters |
| `coresearch/SKILL.md` | 450–650 words |
| Other core entrypoint | 450–700 words |
| Optional narrow entrypoint | 300–500 words |
| Ordinary output | requested artifact + concise material risks |
| Detailed schema | conditional reference only |

The eight-plus-one target should reduce first-class entrypoints from 12,476 to
roughly 5,000–5,500 words and descriptions from 681 to about 250–320 words: a
55–60% reduction without deleting reasoning capability.

## Compaction rules

1. Keep only instructions that change routing, scientific validity, safety, or
   state ownership.
2. Use one mode table per broad skill instead of one skill per reasoning lens.
3. Return the requested artifact first.
4. Make matrices and schemas conditional.
5. Load field rules and evidence schemas once, only when relevant.
6. Use explicit Markdown links; do not rely on custom `depends_on` behavior.
7. Default to in-chat state; write only when requested or mission-declared.
8. Keep fixed-role pins out of skills; the agent manifest owns them.
9. Keep Ponytail and Caveman explicit progressive references.
10. Preserve uncertainty and evidence boundaries when compressing output.

## Options

| Option | Benefit | Remaining cost | Recommendation |
| --- | --- | --- | --- |
| A. Keep fifteen, shorten all | Lowest migration risk; likely 35–45% reduction | Narrow routing ambiguity remains | Useful first phase |
| B. Eight core + optional qualitative | Likely 55–60% reduction; integrated reasoning | Requires manifest/install/design migration | **Recommended target** |
| C. Six or fewer broad skills | Small catalog | Large internal prompts and mode ambiguity | Do not use |

Option B requires deliberately changing the current fifteen-skill invariant,
`skills/manifest.json`, installation pruning, validation, `DESIGN.md`, README,
and the project template. Do not preserve retired names as shim skills; shims
would preserve catalog and context bloat.

## Migration order

1. Capture behavioral baselines for ambiguous routing, direct invocation,
   small-output behavior, evidence integrity, and durable missions.
2. Compact descriptions and entrypoints without merging skills.
3. Centralize field rules, output schemas, and route ownership.
4. Merge gap/causal into design, dialectic into survey, audit/adversary into
   verify, and rebuttal into review.
5. Choose whether qualitative analysis stays explicit-only or becomes an
   optional package.
6. Remove retired skills from the manifest and recognized installations; add
   no aliases.
7. Forward-test output usefulness and evidence correctness, not just keywords.
8. Update architecture, documentation, template, and validation in the same
   reviewed change.

## Contracts that must remain

Compaction must preserve:

- source → evidence → claim → conclusion traceability;
- causal identification and planned-versus-measured distinctions;
- non-fabrication, confidentiality, and prompt-injection boundaries;
- the canonical ledger and durable terminal-result semantics;
- reproducible claim-bearing experiment provenance;
- exact fixed-role model/effort ownership;
- local versus whole-paper versus semantic-revision writing behavior;
- long-command safety and cancellation; and
- Ponytail and Caveman as explicit, orthogonal modes.

These should be owned once and loaded conditionally, not repeated.

## Recommendation

Adopt Option B, but implement Option A first as a non-semantic compaction pass.
This establishes behavioral tests and removes obvious duplication before route
boundaries change. It makes any later quality regression attributable either to
shorter instructions or to skill consolidation, rather than both at once.
