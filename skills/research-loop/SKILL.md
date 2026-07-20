---
name: research-loop
description: Autonomous research mission and validator-gated loop design for systems/cloud, ML-systems, computer-architecture, or cross-layer research projects. Use when the user wants to start, steer, or audit an autonomous research loop, define hypotheses and evaluations, or create artifact validators, sandbox limits, and stop conditions. Optionally hands off execution to `$autoresearch` when an OMX install is present; does not create ad-hoc `.agents/` state.
---

# Research Loop

Design an artifact-gated research loop: progress is complete only when evidence
artifacts satisfy explicit validators — not when an agent says it is done. Run
cumulatively in chat (default); if OMX is installed, optionally hand off
execution to `$autoresearch`.

## What & When

Start, steer, or audit autonomous research missions; convert hypotheses into
artifacts, validators, sandbox limits, stop conditions, OMX handoff contracts;
default to chat-only execution; if OMX is installed, `$autoresearch`, `$ralplan`, and `$team` are optional OMX executors.
Use when: starting a multi-hypothesis project; turning an idea into experiments
and stop conditions; creating an OMX mission after `$deep-interview
--autoresearch`; auditing an existing loop for weak validators, unsafe
assumptions, or unverifiable claims. Not for: ordinary paper planning →
`research-design`; single experiment implementation → `research-engineer`;
creating legacy `.agents/` state, mailboxes, or ad-hoc multi-agent frameworks.

## Procedure

- **Define mission** — objective, domain, intended contribution, non-goals.
- **State hypotheses** — 2–5 hypotheses or design questions, each tied to evidence.
- **Fix the evaluation contract** — name representative workloads, the claimed
  operating envelope, metrics, explicit configurations, and fair baselines
  before implementation. Every implementation unit must instantiate a research
  insight, test a hypothesis, or produce claim evidence; otherwise keep it out
  of the research loop.
- **Specify artifacts** — code, logs, tables, figures, datasets, study notes,
  benchmark outputs, result manifests, provenance, manuscript sections.
- **Define validators** — for each artifact, a pass/fail check, threshold,
  reviewer-usefulness test, or human-inspection criterion. Prefer one minimal
  validator per artifact; do not add redundant validators that prove the same
  thing. A passing build or test establishes artifact correctness, not scientific validity.
- **Set sandbox boundaries** — allowed files, datasets, external calls, compute
  limits, credentials, privacy/confidentiality, destructive-operation policy.
- **Choose command handling** — read `coresearch/references/execution-safe.md`
  before any long build, test, training, evaluation, or benchmark command.
- **Plan the loop** — inner experiment loop, outer synthesis loop, reflection
  cadence, stop conditions.
- **Bound the execution** — agents are allowed when they reduce wall-clock time
  or cover disjoint work. Use the fewest needed; every agent gets an owned
  scope, expected output, and stop condition. Never add agents merely to
  re-check the same change.
- **Run the experiment** — implement one experiment unit; run one executable
  minimal smoke; run the actual claim-bearing evaluation — benchmark, testbed,
  simulation, measurement campaign, training/serving run, or hardware study;
  fix only from observed result/error; run full regression once immediately
  before finalizing a claim. Run one smallest targeted check after a behavior-
  changing edit; full regression is a release gate, not a development loop.
  Auto-retry once, allow at most two fix cycles per experiment unit, and stop if
  two attempts produce no new artifact or error signal.
- **Apply field methodology** — for systems/cloud, include warm-up, repetitions,
  distributions and tails, scale, failure behavior, and cloud temporal/placement
  variance. For ML systems, compare performance/cost at quality parity. For
  computer architecture, establish simulator fidelity or hardware grounding and
  state power-area-performance (PPA) assumptions and methods.
- **Score research risk** — novelty, evidence, reproducibility, ethics, venue-fit
  at mission start and when evidence or constraints change; do not re-score on
  every iteration.
- **Choose handoff** — choose one execution lane at a phase boundary: stay in
  chat, create requested files, or hand off to `$deep-interview --autoresearch`
  / `$autoresearch` when OMX runtime is active. Add another lane only for a
  distinct artifact or a material wall-clock gain; execute `$autoresearch` only
  after validator mode exists.

## Output

Research Mission Contract:
- **Mission** — Objective / Domain & venue mode / Intended contribution / Non-goals.
- **Hypotheses / Research Questions** — table: ID / hypothesis or question /
  evidence needed / artifact / validator / risk.
- **Loop Design** — Inner Loop (experiment/build/analyze iteration) + Outer Loop
  (synthesis, decision, pivot, reflection).
- **Evaluation Contract** — workloads / operating envelope / fair baselines /
  configurations / metrics / warm-up and repetitions / tails, scale, and
  failures / cloud variance, quality parity, or simulator-fidelity and PPA
  controls as applicable.
- **Sandbox and Permissions** — allowed files & directories / allowed data,
  models, APIs / compute or time limits / credentials & private-data boundary /
  destructive operations.
- **Stop Conditions** — Success / Blocked / Failure / Human decision required.
- **OMX Handoff** — recommended lane (chat / `$deep-interview --autoresearch` /
  `$autoresearch` / `$ralplan` / `$team`) / files to create only if authorized /
  validation evidence required before completion.
- **Immediate Next Actions** — ordered list, highest-impact first.

## Reject when

- completion claimed by "agent says done" with no validator passed;
- a goal lacks a metric, evidence artifact, or review criterion — "improve
  results" is not a validator;
- a build, unit test, or smoke check is offered as scientific support without
  the claim-bearing evaluation;
- a claim needs human/official evidence and has none.

## State & Handoff

Canonical Coresearch state is the orchestrator `ledger.yaml`
(state-ledger.md); skills never write state inside their own directory.
Otherwise state lives in chat, or in `.omx/` only when an OMX workflow is
active or requested. Do not create `.agents/` chats or mailboxes. Write an OMX
`.omx/specs/autoresearch-{slug}/mission.md`, `sandbox.md`, and `result.json`
only when an OMX autoresearch workflow is invoked or the user asks — those are
the OMX runtime's mirror of this mission contract, not the canonical
Coresearch state. Keep validators executable or inspectable. In a multi-skill
run, seed `hypothesis_state.candidates` (each with a falsifier) to the ledger
so research-causal can extend them; standalone, the mission contract above is
enough. Next: `$autoresearch` (OMX runtime, only when installed) /
`research-design` (scope narrows to a paper) / `research-engineer` (single
experiment).

Re-entry: return to `coresearch` to re-route the next stage.
