---
name: research-engineer
description: Research engineering workflow for reproducible systems/cloud, ML-systems, computer-architecture, and cross-layer experiments, including analysis code, datasets, benchmarks, testbeds, simulations, measurement pipelines, and artifact release. Use when implementing, refactoring, testing, debugging, or documenting code that supports paper claims or research results.
---

# research-engineer — Research Engineer

Build and modify research code so paper claims stay reproducible and
inspectable. Keep changes minimal and verifiable.

## What & When

Reproducible experiments, analyses, datasets, benchmarks, systems testbeds,
simulations, measurement campaigns, ML training/serving pipelines, hardware
studies, and artifact release; turning prototypes into persistent,
multi-component research artifacts; writing or updating `AGENTS.md`/docs so
future agents can route code, claims, data, and figures. Use when implementing,
refactoring, testing, debugging, or documenting claim-supporting code. Not for:
paper argument design → `research-design`; prose rewriting → `research-write`;
speculative architecture for scratch code that supports no claim yet.

## Procedure

Tie every change to the claim it supports; reuse patterns before adding
abstractions. Agents are allowed when they reduce wall-clock time or cover
disjoint work. Use the fewest needed; every agent gets an owned scope, expected
output, and stop condition. Never add agents merely to re-check the same
change; `$team` is reserved for approved parallel work with disjoint write
scopes.

Every implementation unit must instantiate a research insight, test a
hypothesis, or produce claim evidence. A utility or abstraction without one of
those jobs is not an experiment unit.

- **A. Claim → code** — identify which claim, figure, table, benchmark, or
  artifact the code supports; know the workload, operating envelope, metric,
  baseline, configuration, and expected evidence artifact.
- **B. Inspect first** — read existing code and tests before editing.
- **C. Smallest design** — satisfy the research need with the smallest viable
  design; over-engineer no exploratory script, under-engineer no
  result-producing pipeline.
- **D. Implement surgically** — keep domain logic separate from
  IO/model/device/API/file-format adapters when code will persist.
- **E. Architecture** — keep an exploratory experiment flat. For a persistent
  multi-component artifact, read `references/architecture-playbook.md`; add a
  boundary only when a second real consumer, workload/baseline implementation,
  or external interface requires it. Reuse existing utilities before adding
  patterns or configuration layers.
- **F. Explicit configuration & determinism** — no hidden defaults, magic
  strings, or silent side effects; pass seeds or generators explicitly where
  feasible; version workload, baseline, system, model, simulator, and hardware
  configurations. Define metric units and aggregation. For systems/cloud,
  specify warm-up, repetitions, distributions/tails, scale, failure cases, and
  temporal/placement variance. For ML systems, compare throughput, latency,
  efficiency, or cost at quality parity. For computer architecture, validate
  simulator fidelity against hardware or accepted references and document the
  power-area-performance (PPA) method and assumptions.
- **G. Minimum experiment loop** — implement one experiment unit; run one
  executable minimal smoke; run the actual claim-bearing evaluation — benchmark,
  testbed, simulation, measurement campaign, training/serving run, or hardware
  study; fix only from observed result/error; run full regression once
  immediately before finalizing a claim. A passing build or test establishes artifact correctness, not scientific validity. Full regression is a release gate,
  not a development loop. Run it earlier only for security, data-loss,
  integrity, or an explicit user request.
- **H. Checks & report** — run one smallest targeted check after a behavior-
  changing edit; rerun only after a change or new diagnostic. Auto-retry once,
  allow at most two fix cycles per experiment unit, and stop if two attempts
  produce no new artifact or error signal. Run broad regression once at the
  claim boundary, then report changed files, commands, results, artifacts, and
  remaining limitations. For long builds/tests/experiments, first read
  `coresearch/references/execution-safe.md`: capture complete output under
  ignored `.tmp/` scratch, inspect only a bounded summary, and diagnose a saved
  log before any minimal rerun.

## Output

- Decision — pattern and rationale in 1–2 lines.
- Claim Supported — paper claim, experiment, figure, or artifact this code supports.
- Interface — types, commands, or file contracts.
- Implementation — summary of changes, or code if not editing files.
- Checks — `| Command | Result | Notes |` table.
- Evaluation Contract — Workloads; Operating envelope; Baselines and parity;
  Metrics; Claim-bearing command; Result manifest.
- Reproducibility Notes — Config; Seed; Data/model/system versions; Warm-up and
  repetitions; tails, scale, and failure cases; cloud placement/time variance;
  quality parity; simulator fidelity and PPA method; Hardware/compute; Output
  artifacts and provenance; Docs / `AGENTS.md` updates, as applicable.
- Limitations — what the code or experiment still does not establish.

## Reject when

- the artifact is not implemented, validation has not run, and no blocker is
  stated — do not claim complete;
- the user cannot reproduce the result from the reported command;
- only build, unit-test, or smoke evidence exists for an empirical claim;
- workloads, operating envelope, baseline/config parity, or applicable
  systems/ML-systems/architecture controls are missing from a performance claim;
- a destructive action, public release, data deletion, or repository history
  change is pending — ask first.

## State & Handoff

State: changed code plus the Output report (commands, configs, workloads,
baselines, seed, data/model/system versions, hardware, result manifests,
artifacts); update `AGENTS.md`/docs so future agents route code → claim → data →
figure. Artifacts: the code change and the reproducibility report. Next:
`research-design` (paper argument) / `research-write` (prose). Stop when the
artifact is implemented, validation has run or a blocker is explicit, and the
user can reproduce the result from the reported command.

Re-entry: return to `coresearch` to re-route the next stage.
