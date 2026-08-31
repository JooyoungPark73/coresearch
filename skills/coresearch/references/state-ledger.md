# Orchestrator State Ledger

Durable state so a multi-skill run does not repeat searches, forget rejected
ideas, loop, or silently overwrite. Each skill reads before starting, updates on
finish. Runtime = the user project (NOT inside skills/, NOT a `.agents/` forest).

## Schema (spec §15)

```yaml
project:
  title: string
  research_question: string
  field_mode: systems_cloud|ml_systems|computer_architecture
  venue_lens: general_systems|networked_distributed|cloud|cross_layer|workload_characterization
  intended_contribution: method|system|representation|theory|dataset|benchmark|empirical_finding|design_knowledge|architecture|measurement_characterization
  target_venues: [string]
current_stage: string
completed_skills: [string]
active_skill: string
blocked_by: [{ skill, reason }]
source_state:        # per source_id
  - { id, state: retrieved|screened|fully_read|audited|missing, notes }
claim_state:         # per claim_id
  - id: string
    claim_class: capability|correctness|performance|scalability|efficiency|reliability|cost|quality_performance_tradeoff|power_area_performance|generality|measurement|causal
    state: supported|contradicted|unresolved|rejected
    confidence: high|medium|low
gap_state:
  candidates: [string]
  falsified: [{ gap, reason }]
  surviving: [string]
hypothesis_state:
  candidates: [string]
  distinguishable: [string]
  unidentifiable: [string]
quality_state:
  unsupported_claims: [string]
  missing_counterevidence: [string]
  unresolved_methodology_issues: [string]
next_actions: [string]
stop_conditions: [string]
execution_state:      # optional; old ledgers without it remain valid
  active_run: { id, mission_path, host, status }
  completed_runs: [{ id, result_path, status }]
```

## Bootstrap when absent

Ordinary in-chat work does not create a ledger. When durable or multi-stage
work requires one, the parent owns bootstrap after `output_path`, the research
question, run ID, and mission path are fixed. If the ledger does not exist:

1. create its parent directories under the user's project;
2. initialize it once from the minimal shape below;
3. replace angle-bracket placeholders with known mission values, omit unknown
   optional project fields, and never invent research decisions;
4. preserve the new file for all hosts and roles.

```yaml
project:
  title: <mission title>
  research_question: <research question>
  target_venues: []
current_stage: mission
completed_skills: []
active_skill: research-loop
blocked_by: []
source_state: []
claim_state: []
gap_state:
  candidates: []
  falsified: []
  surviving: []
hypothesis_state:
  candidates: []
  distinguishable: []
  unidentifiable: []
quality_state:
  unsupported_claims: []
  missing_counterevidence: []
  unresolved_methodology_issues: []
next_actions: []
stop_conditions: []
execution_state:
  active_run:
    id: <run-id>
    mission_path: docs/research/runs/<run-id>/mission.md
    host: <codex|claude>
    status: active
  completed_runs: []
```

Never overwrite an existing ledger, even when it is partial or uses an older
schema. Read it and apply the compatibility and idempotent update rules below.
If another process creates it during bootstrap, keep that file and merge only
the keys this run is authorized to update.

## Read/update protocol

- Read the ledger first. If `claim_state` already has a rejected direction for
  the same claim with the same evidence, do not regenerate — surface it.
- On re-entry to a legacy ledger with no `project.field_mode`, infer it from the
  target venue and load-bearing claim, then record only that field: OSDI, SOSP,
  NSDI, EuroSys, and SoCC map to `systems_cloud`; MLSys maps to `ml_systems`;
  ISCA, MICRO, HPCA, and IISWC map to `computer_architecture`. For ASPLOS, use
  the primary hardware, systems, or ML-systems claim and retain
  `venue_lens: cross_layer`. A missing venue lens in an older ledger does not
  invalidate it; record the lens at the next framing update.
- Preserve old records in place. Existing contribution values retain their
  meanings, missing evidence kinds default to `literature`, and expanded claim
  and evidence fields are required only for records created after this contract.
  A ledger without `execution_state` remains valid; add that optional section
  only when a durable run needs it.
- Update only the keys your skill touched. Never blanket-overwrite.
- On finish: set `active_skill` null; add the skill to `completed_skills` only if
  absent; replace (do not duplicate) any `next_actions` entry your skill already
  wrote, else append; merge `stop_conditions` without duplicating. Re-entry and
  pipeline loops may call finish more than once — keep these writes idempotent.
- A skill that cannot proceed writes itself to `blocked_by` with a reason
  (replacing any prior entry for the same skill) rather than emitting a
  fabricated partial result.

## Mapping from skill vocabularies

`research-survey` emits `verification_status`, not `source_state.state`. Map
before writing the ledger:

- `PDF VERIFIED` / `FULL TEXT VERIFIED` → `fully_read`
- `METADATA VERIFIED` → `screened`
- `PARTIALLY VERIFIED` → `retrieved` (flag the uncertainty in notes)
- `NOT FOUND` → `missing`

Producer/consumer pairs that share a ledger key: survey seeds `source_state`;
verification methodology mode writes `source_state.state = audited` after a
load-bearing read. Design gap mode owns `gap_state`; loop may seed
`hypothesis_state.candidates`, and design causal mode extends it. Survey
conflict mode, review, qualitative synthesis, and verification methodology,
adversarial, or causal modes may touch their reasoned `quality_state` subkeys.
Record the broad skill plus its mode for new work. Historical
`completed_skills` values remain valid and are not rewritten.

## Where it lives

Canonical: `docs/research/decisions/ledger.yaml` under the user's `output_path`
project (spec §4, §15). skills never write state inside their own directory.
Durable run artifacts live under `docs/research/runs/<run-id>/`, but they do
not replace the ledger. Every host and skill reads and writes the same
`ledger.yaml`, updating only its authorized keys with the idempotent protocol
above. Do not create a provider-specific state forest.
