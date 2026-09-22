---
name: research-loop
description: Define, steer, or audit durable research missions with artifacts, validators, and stop conditions.
---

# Research loop

Define or maintain a durable mission whose completion is determined by
inspectable validators. Codex goals and Claude Code sessions continue the same
host-neutral mission; Coresearch owns stage selection.

- **Start:** turn an approved direction into a mission using
  [mission-schema.md](references/mission-schema.md) for `mission.md` and
  `sandbox.md`.
- **Steer:** apply new evidence or observed failures to authorized mission
  fields; preserve history and existing limits. Read the mission schema when
  changing its contract.
- **Audit:** assess validators, scope, routing, budgets, and stop conditions
  against the mission schema; return findings in chat unless edits are requested.

Complete a mission-drafting request with the requested plan or files, and an
audit with findings. Neither authorizes running experiments or creating execution
state. Apply the execution requirements below only when run execution is
authorized; preserve any authorization already established in the session.

Bind hypotheses to falsifiers, claim-bearing evidence, artifacts, and validators.
A smoke test cannot validate an empirical claim. Declare dependencies, retry
budgets, and success, blocked, failed, cancelled, and human-decision conditions.
During execution, continue authorized units through validation and repair until
a terminal condition is met; a first implementation alone is not completion.

For durable execution, use
[execution-adapters.md](../coresearch/references/execution-adapters.md) with one
host per run. The parent primarily orchestrates: delegate substantial reading,
bounded implementation, experiments, and diagnosis, including sequential work
when context isolation helps. Retain research decisions, evidence reconciliation,
integration, and final conclusions. Use
[agent-routing.md](../coresearch/references/agent-routing.md) for handoffs,
compact evidence-backed returns, and direct-work exceptions. Assigned workers
execute their own unit and return; they do not delegate. Use
[execution-safe.md](../coresearch/references/execution-safe.md) for long commands.
Load shared evidence or field contracts only for scientific controls the mission
needs to define.

Keep authorized run artifacts under `docs/research/runs/<run-id>/`. During
authorized run initialization or execution, use
[state-ledger.md](../coresearch/references/state-ledger.md) for authorized keys in
`docs/research/decisions/ledger.yaml`. If the canonical ledger does not exist,
initialize it once after fixing run identity. Never replace an existing ledger
or create a second ledger.

At run termination, use [result-schema.md](references/result-schema.md) for
`result.json`, validator outcomes, a terminal role-run record for every attempted
assignment, and remaining risks. Successful claim-bearing completion requires
validator evidence and independent verification after writable artifacts are
integrated; blocked, failed, or cancelled runs record their terminal reason.
Use the result schema's routing criteria; absent observations never establish
`verified`. Host continuation cannot silently change mission scope or select
another research stage.
