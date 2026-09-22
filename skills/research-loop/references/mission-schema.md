# Mission and sandbox schema

A durable run owns exactly:

```text
docs/research/runs/<run-id>/mission.md
docs/research/runs/<run-id>/sandbox.md
docs/research/runs/<run-id>/result.json
```

## `mission.md`

Record:

- objective, non-goals, research question, intended contribution, and current
  evidence;
- hypotheses or design questions, each with a falsifier;
- evaluation contract: workloads or data, operating envelope, baselines,
  configurations, metrics, and applicable scientific controls;
- artifacts and validators, with one inspectable pass/fail condition per
  artifact;
- ordered units, dependencies, and optional `max_concurrency`;
- role assignments with `assignment_id`, fixed role, `depends_on`, owned or
  read-only scope, expected artifact, validator, working modes, and stop or
  escalation condition;
- exact `requested_model` and `requested_effort` for each assignment; for Codex,
  the parent's selection rationale and explicit spawn values, with no native
  file overrides; Claude retains its configured model and effort;
- retry/fix budget;
- success, blocked, failure, cancellation, and human-decision stop conditions;
- canonical ledger path and authorized keys.

Plan substantial reading, bounded implementation, experiments, and diagnosis as
fixed-role assignments under the shared
[orchestration policy](../../coresearch/references/agent-routing.md). Dependencies
may require sequential workers; context isolation remains useful. Keep research
decisions and evidence reconciliation with the parent. Use the existing
assignment artifact and validator fields to specify compact returns with evidence
locations, uncertainty, and blockers; retain raw traces outside the main context.
Trivial tasks and tightly coupled reasoning may stay in the parent.
If an observed failure warrants model escalation, record the reason and a new
attempt ID within the existing retry budget. Preserve earlier attempts and
their evidence; do not turn escalation into an automatic model ladder.

Every implementation unit must instantiate an insight, test a hypothesis, or
produce claim-bearing evidence. A build or smoke validator cannot validate an
empirical claim.

## `sandbox.md`

Record allowed files and directories; data, models, APIs, and external calls;
compute, time, token, and cost budgets when known; credentials, privacy, and
confidentiality boundaries; destructive-action and external-write
prohibitions; and the ignored long-command log path and cancellation policy.

Unknown budgets stay explicit rather than being fabricated. Mission changes
that alter claims, permissions, or external impact require parent or human
approval under the host's normal authority model.
