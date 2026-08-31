---
name: coresearch
description: Central Coresearch router for academic research, papers, literature, rebuttals, claim verification, research engineering, and validator-gated research-loop work. Use when a request is broad, starts or manages a research project, asks which research skill to use, needs stage, fixed-role, or host-adapter routing, or explicitly activates the Ponytail or Caveman working mode.
---

# Coresearch

Use this as the first-stop router for research work. Keep it small: classify stage, load one matching role skill, run it, then return here to re-route the next stage — do not chain skill-to-skill.

## Good for

- Broad research requests where the right role skill is unclear.
- Starting or re-scoping systems/cloud, ML systems, computer architecture/workload, or ASPLOS-style cross-layer research projects.
- Choosing between paper design, writing, review, survey, engineering, rebuttal, verification, and autonomous-loop work.

## Must do

- Pick one primary research stage and one primary skill.
- Select `systems_cloud`, `ml_systems`, or `computer_architecture` when design, writing, review, or engineering quality depends on field norms; add a venue lens when useful.
- Keep `coresearch` as a central triage unit: route, load only needed references, hand off, then re-enter on the next stage.
- Preserve evidence discipline: separate fact, inference, recommendation, and unknown.
- Agents are allowed when they reduce wall-clock time or cover disjoint work. Use the fewest needed; every agent gets an owned scope, expected output, and stop condition. Never add agents merely to re-check the same change.
- Use one fixed role per bounded assignment. The parent may run independent assignments concurrently, but owns dependency joins, integration, cancellation, and post-integration verification.

## Not for

- Low-level `.docx`, `.pdf`, `.pptx`, `.xlsx`, or web-app mechanics — the user invokes an external format tool directly; Coresearch owns research content, not format mechanics.
- Replacing the native host's general planning, coding, or session-continuation features.
- Bulk-loading every skill or creating `.agents/` state forests.

## Quick workflow

1. Identify research stage: intake, idea, survey, design, prototype, evidence, manuscript, review, rebuttal, release.
2. Pick the smallest role skill from the catalog.
3. Pick field mode: `systems_cloud` for OSDI/SOSP/NSDI/EuroSys/SoCC, `ml_systems` for MLSys, or `computer_architecture` for ISCA/MICRO/HPCA/IISWC; use the `cross_layer` venue lens for ASPLOS.
4. Load only the needed reference below.
5. Record any explicitly requested Ponytail or Caveman working mode and pass it through bounded handoffs.
6. Select a fixed native role only for a bounded assignment that materially improves quality, speed, or safety.
7. Keep facts, inference, and recommendations separate.

For executable research work, use the minimum experiment loop: implement one
experiment unit; run one executable minimal smoke; run the actual claim-bearing evaluation
(benchmark, testbed, simulation, measurement, training/serving, or
hardware run); fix only from observed result/error; run full regression once
immediately before finalizing a claim. Full regression is a release gate, not a
development loop. A passing build or test establishes artifact correctness, not scientific validity.

Execution budget: run one smallest targeted check after a behavior-changing
edit; run broad regression/review/verifier once at the claim boundary; rerun a
check only after a change or new diagnostic. Auto-retry once, allow at most two
fix cycles per experiment unit, and stop if two attempts produce no new
artifact or error signal. Give every long-running command or agent an expected
duration and stop condition; stop/cancel it after twice that duration or two
checks without new output.

## References

- Read [stage-map.md](references/stage-map.md) when starting/reframing a project.
- Read [routing.md](references/routing.md) when choosing a skill, fixed role, or host adapter.
- Read [field-modes.md](references/field-modes.md) when venue tone, narrative, evidence, or architecture depends on systems/cloud, ML-systems, architecture/workload, or cross-layer norms.
- Read [research-rules.md](references/research-rules.md) when screening importance, contribution type, field object, or claim-evidence fit.
- Read [reasoning-skills.md](references/reasoning-skills.md) when routing among the analytical skills (research-gap, research-dialectic, research-causal, research-qualitative, research-audit, research-adversary) or sequencing a multi-skill pipeline.
- Read [research-contract.md](references/research-contract.md) at run start to capture the orchestrator input contract (topic, intended contribution, independent-group floor, output path).
- Read [state-ledger.md](references/state-ledger.md) when orchestrating a multi-skill run or maintaining canonical cross-skill state.
- Read [evidence-grounding.md](references/evidence-grounding.md) for claims, citations, evidence, the integrity floor, or confidential material.
- Read [execution-safe.md](references/execution-safe.md) before long builds, tests, training, evaluation, benchmarks, or commands with potentially large output.
- Read [agent-routing.md](references/agent-routing.md) when native role selection, bounded handoff, escalation, or re-entry affects execution.
- Read [execution-adapters.md](references/execution-adapters.md) when Codex goal or Claude Code session continuation is required.
- Read [ponytail.md](references/ponytail.md) when the user or mission explicitly requests minimal durable research engineering.
- Read [caveman.md](references/caveman.md) when the user or mission explicitly requests communication compression.
- Read [skill-catalog.md](references/skill-catalog.md) when auditing skill and fixed-role ownership.

## Optional working modes

Ponytail and Caveman are provider-neutral modifiers, not research stages,
skills, roles, model tiers, or permissions. Activate them only through an
explicit user request or a mission `working_modes` declaration. Each accepts
`off`, `lite`, or `full` and lasts only for the current task or mission.

- Ponytail minimizes durable engineering surface while preserving the primary
  skill's implementation, provenance, validation, and claim-bearing evidence
  contract.
- Caveman compresses communication while preserving required reasoning,
  evidence, uncertainty, safety, and output fields.

Keep the primary research route unchanged. Pass active levels into every
bounded role handoff and durable mission; they never change role or model
selection. If a mode conflicts with a scientific, safety, or artifact
contract, the contract wins and the conflict returns to the parent.

## Default routes

- Paper idea/contribution/evidence plan, or venue choice/strategy (which venue fits this work) → `research-design`.
- Related work/literature map → `research-survey`.
- Source/citation/fact check → `research-verify`.
- Evidence-bounded manuscript drafting, rewriting, argument realization, or semantic revision → `research-write`.
- Venue review/score forecast → `research-review`.
- Rebuttal/discussion response → `research-rebuttal`.
- Code/experiments/artifact release → `research-engineer`.
- Hypotheses/validators/durable loop design → `research-loop` (one host-neutral mission contract for Codex and Claude Code).
- Experiment scope split (when two apply): which evidence supports each claim (plan) → `research-design`; hypotheses/validators/stop-conditions → `research-loop`; implement the experiment code → `research-engineer`.
- Literature gap / next paper / "is this novel" / where are contradictions → `research-gap`.
- Why papers disagree + a reconciling mechanism → `research-dialectic`.
- Is this paper's methodology sound (claim vs evidence) → `research-audit`.
- Bias in the evidence-gathering chain of a conclusion → `research-adversary`.
- Competing causal explanations / identification → `research-causal`.
- Explain a concept / decompose a mechanism → `research-write` (concept-decomposition mode).
- Qualitative coding → themes (interviews, open responses) → `research-qualitative`.
- Workflow stall diagnosis (stalled, repeating, weak synthesis) → read [reasoning-skills.md](references/reasoning-skills.md) §Stall diagnosis; routes back into the skills above.
- Explicit Ponytail or Caveman request → keep the current primary research route and load only the requested working-mode reference.
- If two routes match: fact-check/number/citation → `research-verify` over `research-audit`; 'review' = venue score → `research-review`, methodology soundness → `research-audit`; experiment PLAN → `research-design`, hypotheses/validators → `research-loop`, implement code → `research-engineer`.

## Re-entry

`coresearch` is a re-entry hub, not one-shot triage. After a role skill emits its
output and any ledger keys (state-ledger.md), return here to re-classify the
stage and route the next skill — do not chain skill-to-skill on `Next:` hints
alone. Role-skill `Next:` lines are conveniences; the `## Default routes` map
above is canonical and complete. Native roles and durable host runs are
executors, not stage routers. On terminal status, return their artifact or
result to the parent, update only authorized ledger keys, and re-enter
`coresearch` to route the follow-up stage; do not chain from inside a role or
host continuation.

Active working modes remain scoped to the current task or mission and must be
passed explicitly to a new role or host continuation. Re-entry does not turn
them into global defaults.

## Guardrails

- Do not create `.agents/` state forests.
- Do not bulk-load every research skill.
- Do not invent citations, venues, results, participants, metrics, or code behavior.
- Do not recreate a generic workflow engine inside Coresearch.
- Do not let a working mode override research routing, role/model selection, evidence, validation, safety, or required artifact fields.
- Treat `research-qualitative` as an optional method, never as a primary field mode.
- Require each implementation unit to instantiate an insight, test a hypothesis, or produce claim-bearing evidence; code, features, build success, and production hardening are not contributions by themselves.
