---
name: research-loop
description: Host-neutral research mission and validator-gated loop design for systems/cloud, ML-systems, computer-architecture, or cross-layer research projects. Use when the user wants to start, steer, or audit a durable research loop, define hypotheses and evaluations, or create mission, sandbox, result, validator, retry, and stop contracts for Codex or Claude Code.
---

# Research Loop

Design an artifact-gated research loop: progress is complete only when evidence
artifacts satisfy explicit validators, not when an agent says it is done. Use
one host-neutral mission contract for Codex and Claude Code. Host continuation
does not replace Coresearch routing or the canonical ledger.

## What & When

Start, steer, or audit durable research missions; convert hypotheses into
artifacts, validators, sandbox limits, retry budgets, terminal conditions, and
host handoff contracts. Use when starting a multi-hypothesis project, turning
an idea into ordered experiment units, or auditing an existing loop for weak
validators, unsafe assumptions, or unverifiable claims. Not for ordinary paper
planning (`research-design`), one bounded experiment implementation
(`research-engineer`), or a new generic workflow or state system.

## Procedure

- **Define mission** — objective, domain, intended contribution, research
  question, and non-goals.
- **State hypotheses** — 2–5 hypotheses or design questions, each tied to a
  falsifier, evidence, artifact, and validator.
- **Fix the evaluation contract** — name representative workloads, the claimed
  operating envelope, metrics, resolved configurations, and fair baselines
  before implementation. Every implementation unit must instantiate a
  research insight, test a hypothesis, or produce claim evidence.
- **Specify artifacts** — code, logs, tables, figures, datasets, study notes,
  benchmark outputs, result manifests, provenance, and manuscript sections.
- **Define validators** — for each artifact, a pass/fail check, threshold,
  reviewer-usefulness test, or human-inspection criterion. Prefer one minimal
  validator per artifact. A passing build or test establishes artifact
  correctness, not scientific validity.
- **Set sandbox boundaries** — allowed files and directories; allowed data,
  models, APIs, and external calls; compute/time/token/cost budgets when known;
  credentials, privacy, confidentiality, destructive-action, and external-write
  limits; long-command log location and cancellation policy.
- **Choose command handling** — read
  `coresearch/references/execution-safe.md` before a long build, test, training,
  evaluation, benchmark, or command with large output.
- **Plan ordered units** — inner experiment loop, outer synthesis loop,
  reflection cadence, dependencies, retry/fix budget, and stop conditions. For
  delegated work, give each assignment a unique ID, fixed role, dependencies,
  owned scope, artifact, validator, and terminal condition.
- **Bound delegation** — agents are allowed when they reduce wall-clock time or
  cover disjoint work. Use the fewest needed; every agent gets an owned scope,
  expected output, and stop condition. Never add agents merely to re-check the
  same change. Allowed roles must come from `agents/manifest.json` and receive
  the complete handoff in `coresearch/references/agent-routing.md`. Run ready
  read-only assignments concurrently when useful; serialize overlapping writes,
  join all declared dependencies before synthesis, and verify only after the
  integrated artifact is stable.
- **Run the experiment** — implement one experiment unit; run one executable
  minimal smoke; run the actual claim-bearing evaluation; fix only from
  observed result/error; run full regression once immediately before
  finalizing a claim. Run one smallest targeted check after a behavior-changing
  edit. Auto-retry once, allow at most two fix cycles per experiment unit, and
  stop if two attempts produce no new artifact or error signal.
- **Apply field methodology** — for systems/cloud, include warm-up,
  repetitions, distributions and tails, scale, failure behavior, and cloud
  temporal/placement variance. For ML systems, compare performance/cost at
  quality parity. For computer architecture, establish simulator fidelity or
  hardware grounding and state performance/power/area assumptions and methods.
- **Score research risk** — novelty, evidence, reproducibility, ethics, and
  venue fit at mission start and when evidence or constraints change.
- **Select continuation** — keep narrow work in the current session. Use the
  Codex goal adapter only for multi-turn, experiment-bearing work or durable
  validators. Claude Code uses native session continuation over the same
  mission. Use one host for a run and never pass a per-invocation model
  override.

## Output

For a durable run, create or update exactly these artifacts under the declared
research output path:

```text
docs/research/runs/<run-id>/mission.md
docs/research/runs/<run-id>/sandbox.md
docs/research/runs/<run-id>/result.json
```

`mission.md` contains:

- objective and non-goals;
- research question and intended contribution;
- hypotheses or design questions;
- evaluation contract;
- artifacts and validators;
- ordered experiment units;
- optional `max_concurrency` and a role-assignment graph where every assignment
  has `assignment_id`, `role`, `depends_on`, owned/read-only scope, expected
  artifacts, validator, stop/escalation conditions, and active working modes;
- retry/fix budget;
- success, blocked, failure, cancellation, and human-decision stop conditions;
- `docs/research/decisions/ledger.yaml` and the keys this run may update;
- allowed role assignments.

`sandbox.md` contains:

- allowed files and directories;
- allowed data, models, APIs, and external calls;
- compute, time, token, and cost budgets when known;
- credential, privacy, and confidentiality boundaries;
- destructive and external-write prohibitions;
- ignored long-command log location and cancellation policy.

New runs use result schema version 2:

```json
{
  "schema_version": 2,
  "run_id": "string",
  "mission_path": "string",
  "status": "success|blocked|failed|cancelled",
  "host": "codex|claude",
  "goal_id": "string|null",
  "role_runs": [
    {
      "assignment_id": "implement-unit-1",
      "role": "coresearch-implementer",
      "status": "success|blocked|failed|cancelled",
      "requested_model": "string",
      "requested_effort": "string",
      "observed_model": "string|null",
      "observed_effort": "string|null",
      "routing_status": "verified|static-only|mismatch",
      "artifacts": [],
      "validators": [],
      "stop_reason": "string"
    }
  ],
  "artifacts": [],
  "validators": [],
  "claim_evidence": [],
  "ledger_updates": [],
  "remaining_risks": [],
  "stop_reason": "string"
}
```

Record every attempted assignment in `role_runs`, including the independent
verifier and any blocked, failed, or cancelled lane. For each role, record the
exact requested model and effort. Record observed routing only when the host
exposes both values. An unobservable or partially observable route is
`static-only`, never `verified`; a blocked, substituted, unavailable, or
different route is `mismatch`.

Schema version 1 remains valid for existing zero- or one-role runs. Do not
rewrite historical results merely to upgrade them. Any new run or resumed run
that uses multiple role assignments writes schema version 2.

Use `coresearch/references/execution-adapters.md` for the canonical Codex goal
handoff and Claude Code continuation semantics.

## Reject when

- completion is claimed without a terminal `result.json` and validator
  evidence;
- a goal lacks a metric, evidence artifact, or review criterion;
- a build, unit test, or smoke check is offered as scientific support without
  the claim-bearing evaluation;
- a claim needs human or official evidence and has none;
- the mission omits a retry budget, sandbox boundary, terminal condition,
  ledger ownership, requested routing provenance, or independent verifier;
- delegated work lacks assignment IDs, dependencies, disjoint ownership, a
  join before consumption, or one terminal `role_runs` record per assignment;
- host continuation selects research stages or creates a second ledger.

## State & Handoff

Canonical Coresearch state is
`docs/research/decisions/ledger.yaml` as defined by
`coresearch/references/state-ledger.md`. Skills never write runtime state inside
their own directory. Old ledgers without `execution_state` remain valid. A
durable run may update only its authorized `execution_state` keys and domain
keys, using idempotent merges.

Keep validators executable or inspectable. Seed
`hypothesis_state.candidates` with a falsifier so `research-causal` can extend
them. Every terminal result returns to the parent. Claim-bearing success then
receives independent `coresearch-verifier` review before `coresearch` re-entry.
The parent records each role attempt in `role_runs`, joins dependencies,
integrates writable artifacts, and only then starts that verifier.

Next: `research-design` when scope narrows to a paper;
`coresearch-implementer` for a mechanically clear bounded implementation unit;
`coresearch-experimenter` for mechanical run execution;
`coresearch-debugger` after repeated observed failure.
Complex integrated implementation and unresolved causal or dialectical
reasoning stay with the frontier parent until decomposed.

Re-entry: return to `coresearch` to re-route the next stage.
