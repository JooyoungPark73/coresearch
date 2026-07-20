# Research Engineering Architecture Playbook

Use this for a persistent, multi-component reproducible research artifact: one
with multiple workloads or baselines, a shared measurement path, repeated runs,
or tables/figures that other people must regenerate. Do not force it onto a
one-off scratch script. The target is a transparent claim-to-evidence pipeline,
not production architecture for its own sake.

## Architecture target

Prefer the smallest layout that makes experimental substitutions and provenance
explicit:

```text
src/<project>/
  core/                 # claim-level logic, metrics, invariants
  orchestration/        # run lifecycle and evaluation coordination
  adapters/
    workloads/          # datasets, traces, load generators, benchmark suites
    baselines/          # competing systems/methods behind comparable contracts
    systems/            # cloud, runtime, model-serving, simulator, hardware IO
    artifacts/          # manifests, metrics, traces, tables, figures
  interfaces/           # CLI and thin notebook/script entrypoints
configs/
  workloads/            # versioned workload and operating-envelope configs
  baselines/            # disclosed baseline and tuning configs
  experiments/          # composed claim-bearing evaluations
experiments/            # runnable entrypoints; no hidden notebook state
results/<run-id>/        # manifest + raw/derived evidence, never source inputs
tests/                   # core tests plus one executable smoke path
docs/                    # claim, command, data, and artifact routing
```

Separate workload and baseline adapters from orchestration so every method sees
the same inputs, budget, measurement window, and metric implementation. Keep
cloud/provider APIs, model runtimes, simulators, devices, counters, datasets,
and file formats at adapters. Every implementation unit must instantiate a
research insight, test a hypothesis, or produce claim evidence.

## Claim-bearing evaluation contract

Make each evaluation config declare:

- claim or hypothesis ID and intended table/figure;
- workloads, versions, selection logic, and claimed operating envelope;
- system and baseline configs, tuning procedure, resource/compute budget, and
  parity constraints;
- metrics and units, warm-up/steady-state rule, repetitions/seeds, aggregation,
  confidence intervals, distributions and tail percentiles;
- scale points, overload behavior, injected/natural failures, and recovery
  criteria;
- cloud provider/region/zone, instance type, placement or tenancy, run times,
  and temporal/placement-variance plan when applicable;
- model/data/preprocessing/precision/batching and the task-quality parity gate
  for ML-systems comparisons;
- simulator/version/configuration, fidelity validation, hardware/counter setup,
  and power-area-performance (PPA) tools, technology assumptions, and
  normalization for computer-architecture studies.

The minimal smoke proves that the pipeline executes. Then run the actual claim-bearing evaluation: benchmark, testbed, simulation, measurement campaign,
training/serving run, or hardware study. A passing build or test establishes
artifact correctness, not scientific validity.

## Result manifests and provenance

Write an immutable manifest beside every result. Record at least `run_id`, claim
ID, command, timestamp, repository commit and dirty-diff locator, resolved config
paths or hashes, workload and baseline versions, seeds, environment/dependency
lock, hardware or cloud placement, metric definitions, exit status, and paths or
checksums for raw and derived artifacts. Add the domain controls above when they
apply. Preserve failed and censored runs with their status; do not silently drop
them from summaries.

Generate tables and figures from manifests/raw results, not hand-copied numbers.
One documented command must regenerate each claim-bearing table or figure from
declared inputs. If licensed data, hardware, or cloud access prevents a complete
rerun, make the command reproduce from archived raw evidence and state exactly
which acquisition step remains external.

## Hot / index / cold docs

Use docs as an LLM-friendly routing layer:

- `docs/hot/` — current decisions, active experiment commands, claim ledger, latest results, known blockers.
- `docs/index/` — maps from claims → code → data → figures → paper sections; stable enough for agents to route context.
- `docs/cold/` — archived runs, old notes, superseded designs, long logs, prior failed attempts.

Minimum useful files:

```text
docs/hot/claim-ledger.md
docs/hot/runbook.md
docs/index/architecture.md
docs/index/data-contracts.md
docs/index/experiment-map.md
docs/cold/README.md
```

Do not dump everything into `docs/hot`; hot means the next agent probably needs it.

## AGENTS.md architecture block

When a research repo is being initialized or upgraded, add a compact architecture block to project `AGENTS.md` or a linked `docs/index/architecture.md`:

```markdown
## Architecture Notes
- Claim-bearing units: [insight/hypothesis/evidence produced]
- Main evaluations: [benchmark/testbed/simulate/measure/train-serve/hardware]
- Boundaries: workload, baseline, system, and artifact adapters.
- Repro commands: [smoke] / [table or figure from manifest]
- Docs routing: hot = current, index = maps, cold = archive.
- Claim link: every result-producing command states which paper claim/figure it supports.
```

## Reproducible research defaults

- One command can reproduce each table/figure or explain why not.
- Workload, baseline, and experiment configs are explicit, resolved, and versioned;
  seeds are passed, not hidden.
- Outputs include result manifests and provenance sufficient to reconstruct the
  evaluation context.
- Tests cover domain logic and one smoke path through each result-producing pipeline.
- Logging preserves per-run samples, distributions, tails, failures, and exclusions
  rather than only final averages.
- Failure cases are first-class outputs, not deleted evidence.
- Dependencies are justified; use stdlib/repo helpers first.

## When to stay simpler

Use a flat script/notebook only when all are true:

- exploratory throwaway;
- no paper claim depends on the output yet;
- no user/reviewer/reproducer will run it;
- no second workload, baseline, system adapter, or result consumer exists;
- no hidden state or external side effect matters.

Once a script supports a figure, table, benchmark, release artifact, or rebuttal experiment, promote it to a reproducible pipeline.
