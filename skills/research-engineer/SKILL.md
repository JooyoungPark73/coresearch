---
name: research-engineer
description: Implement research code and run reproducible experiments under an explicit evaluation contract.
---

# Research engineer

Implement research artifacts and execute experiments tied to a research insight,
hypothesis, claim, figure, or release. Use the existing evaluation contract;
resolve only missing details that affect validity or authorized scope.

**Implementation** delivers working code, configuration, data pipelines, or
other requested artifacts. **Experiment** executes the declared evaluation
and produces results with provenance. A utility need not invent a scientific
hypothesis, but an experiment must have a defined research job.

For claim-bearing runs, make workloads or data, operating envelope, baselines,
resolved configurations, metrics, and validators explicit. Preserve units,
versions, seeds, hardware or compute context, and failed or censored runs.
Build and test success establish artifact correctness, not scientific validity;
empirical claims require the actual benchmark, testbed, simulation, measurement,
or other declared evaluation.

Read only what the work requires:

- [architecture-playbook.md](references/architecture-playbook.md) for persistent
  multi-component artifacts; ordinary exploratory work can stay flat.
- [field-modes.md](../coresearch/references/field-modes.md) when scientific
  controls depend on the field.
- [execution-safe.md](../coresearch/references/execution-safe.md) for long or
  noisy commands and provenance handling.

Continue authorized implementation through relevant validation and fixes for
observed failures. Repeat checks when changes or failures justify them; stop
at a satisfied contract, an exhausted retry budget, or a blocker requiring
new evidence or authority. Existing authorization covers actions within its
scope; obtain authorization for destructive actions, external writes, public
release, data deletion, or history changes only when it is missing.

Report the implemented result, changed files or interfaces, validation commands
and outcomes, result artifacts and provenance, and limits on what the evidence
establishes. Follow existing mission paths for durable artifacts; ordinary
diagnostics stay in chat. Contribution design and independent claim
verification return through Coresearch to their owning stage.
