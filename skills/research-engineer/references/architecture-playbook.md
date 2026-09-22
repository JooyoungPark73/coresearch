# Research Engineering Architecture Playbook

Use this for a persistent, multi-component reproducible research artifact: one
with multiple workloads or baselines, a shared measurement path, repeated runs,
or tables/figures that other people must regenerate. Do not force it onto a
one-off scratch script. The target is a transparent claim-to-evidence pipeline,
not production architecture for its own sake.

## Architecture target

Use the existing project layout where it supports experimental substitutions
and provenance. The following is an illustrative layout for larger artifacts;
create only the components the evaluation actually needs:

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
and file formats at adapters when those boundaries improve comparability or
reuse. Tie evaluation units to a research insight, hypothesis, or claim;
supporting utilities need only serve the declared artifact and its validation.

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

## Documentation and state

Keep durable research decisions in `docs/research/decisions/ledger.yaml`,
following [state-ledger.md](../../coresearch/references/state-ledger.md).
Run contracts remain under `docs/research/runs/<run-id>/`. Documentation may
link claims to code, data, figures, and reproduction commands, but must not
copy claim state into another ledger.

Use existing documentation first. Add a runbook or architecture map only when
it helps a reader execute or understand the artifact. Larger projects may
separate current guidance, indexes, and archives; there is no required
documentation tree. Raw diagnostic logs stay in ignored scratch storage.

## AGENTS.md architecture block

When project initialization or documentation updates are in scope and agents
need non-obvious architecture guidance, add a compact block to the existing
project prompt or architecture document. Include only applicable details:

```markdown
## Architecture Notes
- Claim-bearing units: [insight/hypothesis/evidence produced]
- Main evaluations: [benchmark/testbed/simulate/measure/train-serve/hardware]
- Boundaries: workload, baseline, system, and artifact adapters.
- Repro commands: [smoke] / [table or figure from manifest]
- Docs routing: [existing reproduction guide, architecture map, canonical ledger].
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

A flat script or notebook can support a paper figure or reusable artifact when
its inputs, configuration, execution order, provenance, and validation are
explicit and reproducible. Add modules or adapters when actual variation,
shared logic, or independently testable boundaries justify them. Claim-bearing
use requires the evaluation and provenance contract above, not a particular
directory layout.
