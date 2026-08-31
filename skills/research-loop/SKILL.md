---
name: research-loop
description: Define, steer, or audit a durable host-neutral research mission with hypotheses, artifacts, validators, sandbox limits, retries, routing provenance, and terminal conditions.
---

# Research loop

Create an artifact-gated mission whose completion is determined by validators,
not an agent's completion claim. Codex goals and Claude Code sessions continue
the same host-neutral mission; they do not select research stages or replace
the canonical ledger.

## Modes

- **Start:** turn an approved direction into a durable mission.
- **Steer:** update authorized mission state after new evidence or failure.
- **Audit:** test an existing mission for missing validators, unsafe scope,
  invalid routing, or unverifiable stop conditions.

## Method

1. Define objective, non-goals, research question, intended contribution,
   hypotheses or design questions, and falsifiers.
2. Bind each hypothesis to claim-bearing evidence, an inspectable artifact, and
   a validator. A smoke test is not a scientific validator.
3. Declare ordered units, dependencies, retry/fix budget, success, blocked,
   failed, cancelled, and human-decision stop conditions.
4. Bound files, data, models, external calls, credentials, confidentiality,
   destructive actions, compute, time, token, and cost. For long commands load
   [execution-safe.md](../coresearch/references/execution-safe.md).
5. When delegation is useful, load
   [agent-routing.md](../coresearch/references/agent-routing.md). Give every
   assignment a fixed role, unique ID, dependencies, disjoint ownership,
   expected artifact, validator, and stop condition. Record every attempt,
   including blocked, failed, or cancelled work.
6. Use one host per run and the adapter in
   [execution-adapters.md](../coresearch/references/execution-adapters.md).
   Record observed model routing only when exposed by the host; otherwise use
   `static-only`.
7. Keep cross-stage state in
   `docs/research/decisions/ledger.yaml`. Read
   [state-ledger.md](../coresearch/references/state-ledger.md). If the canonical
   ledger does not exist for durable or multi-stage work, initialize it once
   using that reference after the run identity is fixed. Never replace an
   existing ledger; update only mission-authorized keys and preserve history.

Use [mission-schema.md](references/mission-schema.md) when creating or auditing
`mission.md` and `sandbox.md`. Use [result-schema.md](references/result-schema.md)
for terminal results and compatibility. Load the shared evidence or field
reference only when a mission must define those scientific controls.

## Output and completion

For durable work, create or update only the declared run artifacts under
`docs/research/runs/<run-id>/` and the authorized canonical ledger keys. For an
ordinary audit, return findings in chat unless file changes were requested.

Completion requires a terminal `result.json`, inspectable validator evidence,
one terminal role-run record per attempted assignment, explicit remaining
risks, and independent verification after writable artifacts are integrated.
Host continuation must not create a second ledger, silently change the mission,
or route itself into another research stage.
