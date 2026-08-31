# Host Execution Adapters

Coresearch owns research routing, evidence quality, and the canonical ledger.
Codex and Claude Code own their native session continuation and subagent
execution. Neither host adapter is a second research router.

## Shared durable-run contract

Durable runs use one mission across both hosts:

```text
docs/research/runs/<run-id>/mission.md
docs/research/runs/<run-id>/sandbox.md
docs/research/runs/<run-id>/result.json
```

`mission.md` records the objective and non-goals, research question and
contribution, hypotheses or design questions, evaluation contract, artifacts,
validators, ordered experiment units, retry budget, all terminal conditions,
the canonical ledger path and owned keys, allowed roles, and any delegated
assignment graph. Each assignment declares `assignment_id`, `role`,
`depends_on`, owned/read-only scope, expected artifacts, validator,
stop/escalation conditions, and active working modes. The mission may set a
small `max_concurrency`. It may also
declare a `working_modes` map whose only keys are `ponytail` and `caveman` and
whose values are `off`, `lite`, or `full`.

`sandbox.md` records allowed files, data, models, APIs and external calls;
known compute, time, token and cost budgets; credential, privacy and
confidentiality boundaries; destructive and external-write prohibitions; the
ignored long-command log location; and cancellation policy.

New `result.json` files use schema version 2 and record `schema_version`,
`run_id`, `mission_path`, terminal `status`, `host`, nullable `goal_id`,
`role_runs`, `artifacts`, `validators`, `claim_evidence`, `ledger_updates`,
`remaining_risks`, and `stop_reason`. Every `role_runs` entry records its
`assignment_id`, `role`, terminal `status`, `requested_model`,
`requested_effort`, nullable `observed_model`, nullable `observed_effort`,
`routing_status`, `artifacts`, `validators`, and `stop_reason`.
Allowed terminal statuses are `success`, `blocked`, `failed`, and `cancelled`.
Allowed routing statuses are `verified`, `static-only`, and `mismatch`.

Schema version 1 remains valid for historical zero- or one-role results. New or
resumed multi-role runs use version 2; do not rewrite historical results solely
for migration.

Static configuration proves only `static-only`. Use `verified` only when the
host reports the observed role, model, and effort and all three match the
assignment and manifest. Missing role/model/effort metadata remains
`static-only`. A blocked, substituted, unavailable, or different role, model,
or effort is `mismatch` and must not be reported as successful routing.

## Working modes

The same [Ponytail](ponytail.md) and [Caveman](caveman.md) semantics apply on
both hosts. The mission is authoritative for their run-scoped levels, and each
bounded role handoff repeats the active settings. The modes constrain
engineering or communication only; they do not alter stage routing, native
role selection, exact model/effort pins, permissions, validators, or terminal
conditions.

## Codex

Use native Codex role definitions from `.codex/agents/*.toml`. Use `/goal`
only for multi-turn, experiment-bearing work or work with durable validators.
The goal references the mission instead of embedding or replacing it:

```text
/goal Execute docs/research/runs/<run-id>/mission.md within sandbox.md. Use the
named fixed role for each ready assignment and never override its configured
model or effort. Join dependencies and integrate writable artifacts before
verification. Keep docs/research/decisions/ledger.yaml current. Stop only after
result.json has a terminal status, every assignment has a role_runs record, and
every required validator has evidence, or when a declared
blocked/failure/human-decision condition is reached.
```

The goal owns continuation. It does not select research stages. Do not use a
goal for one bounded read, a narrow answer, or a single small edit.

## Claude Code

Use native Claude Code role definitions from `.claude/agents/*.md`. The main
Claude session receives the same `mission.md` and `sandbox.md`, owns
continuation, invokes the named fixed role for each ready assignment without a
per-invocation model override, and writes the same terminal `result.json`. It
joins dependencies and integrates writable artifacts before verification. Do
not emulate the
Codex goal surface, create a parallel state forest, or introduce a second
ledger.

## Result return

Every attempted assignment appends one terminal `role_runs` entry with its
exact requested model and effort. Record observed routing only when the host
exposes it. The parent waits for declared dependencies, preserves partial and
failed lanes, integrates writable artifacts, and then starts an independent
`coresearch-verifier` assignment for claim-bearing completion. On terminal
status, return the result to the parent, apply only authorized idempotent ledger
updates, and re-enter `coresearch` for the next stage.
