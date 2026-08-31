# Ponytail Working Mode

Ponytail is an optional, provider-neutral working mode for **minimal durable
research engineering**. It keeps research code and experiment infrastructure
as small as possible while preserving everything needed to reproduce and
audit a result.

It is not a research stage, skill route, native role, model tier, permission
grant, or substitute for an evaluation contract. It must not change model or
role selection.

## Activation and scope

Activate Ponytail only when the user explicitly requests it or a durable
mission declares it under `working_modes.ponytail`. Allowed levels are `off`,
`lite`, and `full`.

- `off`: ordinary Coresearch engineering rules apply.
- `lite`: minimize the current implementation or experiment unit.
- `full`: also minimize the persistent claim-bearing experiment architecture.

The setting is scoped to the current task or mission. Do not infer it from an
earlier conversation, store it as undeclared global state, or silently apply
it to another project.

## Lite contract

- Reuse repository patterns, utilities, file formats, and test fixtures before
  creating another abstraction.
- Prefer the smallest reviewable diff and the fewest moving parts that satisfy
  the declared experiment unit.
- Keep exploratory work flat and disposable until an artifact must persist.
- Make changed behavior explicit in configuration rather than hidden in code.
- Add no speculative layer, generalized framework, or dependency for a future
  consumer that does not yet exist.
- Give non-trivial logic one smallest runnable check.

## Full contract

Full mode includes Lite and adds these requirements:

- Persist only artifacts needed to execute, reproduce, inspect, or validate a
  claim-bearing evaluation.
- Keep workload, baseline, system or model, dataset, simulator or testbed,
  hardware, and file-format differences behind narrow adapters.
- Use explicit, versioned experiment configuration.
- Capture an immutable result manifest with run ID, source revision,
  configuration identity, input provenance, and output locations.
- Provide one documented command for every claim-bearing table or figure.
- Introduce a shared component only after a real second consumer or interface
  boundary demonstrates the need.

The shortest implementation is not automatically the best one. Choose the
smallest design that remains durable under the declared provenance,
reproduction, and validator requirements.

## Scientific and safety boundary

Ponytail reduces engineering surface, not scientific obligation. A smoke test
can establish executability, but the declared claim-bearing evaluation is
still required. The mode cannot remove baselines, controls, repetitions,
quality-parity checks, provenance, validators, confidentiality controls, or
safety constraints needed by the primary research skill.

Production hardening, framework breadth, and architectural polish are not
research contributions by themselves. Conversely, deleting required evidence
or reproducibility machinery is not simplification.

Follow [execution-safe.md](execution-safe.md) for long or noisy commands and
the [research engineering workflow](../../research-engineer/SKILL.md) for the
complete implementation and evaluation contract.

## Handoff and composition

Pass the active level explicitly in every bounded role assignment and durable
mission:

```yaml
working_modes:
  ponytail: lite  # or full
```

A receiving role treats this as an engineering constraint inside its existing
scope. It does not gain tools, write access, routing authority, or a different
model. If the mode conflicts with the evaluation or safety contract, preserve
the contract and report the conflict to the parent.

Ponytail composes independently with Caveman: one minimizes durable
engineering surface; the other compresses communication.
