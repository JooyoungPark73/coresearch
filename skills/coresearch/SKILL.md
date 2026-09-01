---
name: coresearch
description: Route broad or multi-stage research work to one primary Coresearch skill, optional native role, and only the references needed for the current stage.
---

# Coresearch router

`coresearch` is the sole research-stage router and re-entry point. Classify the
earliest blocked stage, load one primary skill, complete that stage, then return
here if the work changes stage. Do not preload the bundle or build a fixed
pipeline.

## Route

| Need | One primary skill | Mode |
| --- | --- | --- |
| Paper contribution, evidence plan, gap, or causal hypothesis | [`research-design`](../research-design/SKILL.md) | paper design / gap analysis / causal hypothesis |
| Papers, closest work, literature map, or real disagreement | [`research-survey`](../research-survey/SKILL.md) | literature map / conflict synthesis |
| Durable hypotheses, validators, retries, and stop conditions | [`research-loop`](../research-loop/SKILL.md) | start / steer / audit mission |
| Research code, experiment execution, debugging, or artifacts | [`research-engineer`](../research-engineer/SKILL.md) | implementation / experiment |
| Evidence-bounded manuscript drafting, rewriting, argument realization, or semantic revision | [`research-write`](../research-write/SKILL.md) | writing mode matching scope |
| Venue assessment, score forecast, or response to reviews | [`research-review`](../research-review/SKILL.md) | assessment / response |
| Fact, citation, methodology, bias, or causal-claim check | [`research-verify`](../research-verify/SKILL.md) | fact / methodology / adversarial / causal |
| Interview, observation, or open-response coding explicitly requested | [`research-qualitative`](../research-qualitative/SKILL.md) | qualitative synthesis |

Resolve common ambiguities as follows:

- planning claim-bearing evidence is design; running it is engineering;
- defining a durable mission is loop; ordinary planning is design;
- discovering sources is survey; checking a supplied claim is verification;
- venue scoring and review responses are review; truth and method checks are verification;
- writing expresses an approved argument; it does not invent the contribution or evidence.
- causal formulation without supplied evidence is design; testing a supplied causal claim against
  methods or evidence is verification. Ask once only if indeterminate.

If a request spans stages, start at the earliest blocked stage. Route again only
after that output exists. Ordinary requests return the requested artifact in
chat; durable files are created only when requested or declared by a mission.

## Shared contracts

Load references conditionally:

- [evidence-grounding.md](references/evidence-grounding.md) for claims,
  citations, novelty, causal language, or confidential evidence.
- [field-modes.md](references/field-modes.md) when field or venue methodology
  changes the evidence contract.
- [causal-reasoning.md](references/causal-reasoning.md) for causal planning or
  causal audit.
- [state-ledger.md](references/state-ledger.md) only for durable or multi-stage
  work using `docs/research/decisions/ledger.yaml`.
- [stall-diagnosis.md](references/stall-diagnosis.md) when work repeats, gathers
  without synthesis, or stops producing useful artifacts.
- [execution-safe.md](references/execution-safe.md) before long or noisy
  commands.
- [agent-routing.md](references/agent-routing.md) when a bounded native-role
  assignment materially improves speed, quality, or independence.
- [execution-adapters.md](references/execution-adapters.md) for durable Codex
  goals or Claude Code session continuation.

## Native roles and re-entry

Roles execute bounded assignments, not stage selection. Give each disjoint
ownership, artifact, validator, and stop condition. Installed roles are
self-contained: do not look for a runtime manifest. `verified` requires matching
metadata; `static-only` requires successful execution with incomplete metadata;
blocked, substituted, unavailable, or different is `mismatch`.

Every terminal role or mission result returns to the parent. Integrate stable
artifacts before independent verification, update only authorized ledger keys,
then re-enter Coresearch if another stage is needed.

## Optional working modes

Ponytail and Caveman are explicit-only task or mission modifiers (`off`, `lite`,
`full`), never routes, roles, models, or permissions. Load
[ponytail.md](references/ponytail.md) for minimal durable engineering and
[caveman.md](references/caveman.md) for communication compression. Pass active
levels through handoffs; neither may weaken evidence, validation, or safety.

## Guardrails

- Separate fact, inference, recommendation, and unknown.
- Do not invent citations, results, participants, metrics, or code behavior.
- Do not create provider-specific research state or runtime state in skills.
- Do not treat build or test success as scientific evidence.
- Keep `research-qualitative` optional and explicit; it is not a field mode.
