# Architecture and migration

## Starting point and decision

The inspected baseline is `d62ad4e0609b5ec912a2f7c0d3b0d378326e3f0f`.
It bundled 15 skills, an explicit stage/re-entry router, cross-skill YAML state,
OMX-specific runtime references, full/bridge project prompts, and a large
installer/repair/rollback surface. Those mechanisms mostly managed agent behavior
and prompt placement rather than producing research evidence.

The redesign starts with Astra's judgment and the host's existing tools. Coresearch
is a portable research skill, not an agent server. There is deliberately no
`run` command: invoking a model, granting permissions, starting workers, and
tracking jobs are host responsibilities. This avoids embedding provider APIs,
credentials, model identifiers, and another orchestration lifecycle.

[OpenAI's design guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
informs the separation of short routing metadata, task-local resources, and
repository-specific instructions. It is not copied into a persistent prompt.

## What survived, and what did not

| Earlier assumption | Replacement and reason |
|---|---|
| Every task needs a stage, field, primary role, and router re-entry | One skill exposes resources. Astra chooses the relevant work directly. |
| Analytical lenses need separate agents/skills and serialized outputs | One analysis reference; use only the lens that resolves a real uncertainty. |
| Persistent orchestration needs an active-skill/blocked/gap/claim YAML ledger | Existing artifacts plus an optional short Markdown brief; no schema engine or mirrors. |
| Research requires an OMX prompt bridge or full project instructions | No installed project/global instructions. Native skill discovery is sufficient. |
| Install lifecycle requires self-install, aliases, repair, update, rollback, inventory, wizards | Two explicit commands: install one payload; optionally create one brief. Git and ordinary files handle the rest. |
| Autonomous research requires framework lane selection and fixed retry counts | Scientific validators and budgets in task context; host job lifecycle; lead decides when to change direction. |
| Source collection should infer paper identity through multiple fuzzy APIs | The agent resolves identity. A small downloader fetches exact open URLs and records transport provenance. |
| Every role needs repeated evidence and safety instructions | One short evidence floor, then only task-specific standards in relevant resources. |

Literature owns source synthesis and citation provenance. Experiments covers
contributions, evaluation design and experimental controls; Engineering covers
implementation, measurement pipelines and reproducible artifacts. Analysis handles
gaps, contradictory findings, causal explanations and evidence audits.
Manuscripts covers writing, review, rebuttal and release. Delegation describes
bounded assignments using the host. Format mechanics remain with appropriate tools.

A retrieved PDF is intentionally weaker evidence than an inspected paper, and an
inspected paper is weaker than support for a particular claim. Transport reports
never collapse those distinctions. Fuzzy lookup and the old roadmap table parser
are removed, not retained as compatibility adapters.

## Boundaries

The root `AGENTS.md` is only for maintaining this repository. Installation copies
or links `skills/coresearch` including its relative references, template, and
source utility; it never copies this root file. Skill names are discovered from
the actual payload, not a second role manifest. `.codex-plugin/plugin.json`
contains distribution metadata only.

Astra decides research strategy and validates the final synthesis. A worker gets
a bounded objective, scope, needed context, artifact, and completion criteria.
Native workers and configured Claude Code processes are alternatives, not
additional mandatory infrastructure. A task without available workers proceeds
directly. Completion notifications or a blocking native call replace polling.

The optional brief is project state, not persistent behavioral instruction. No
reference is mandatory for every task; no initialization, output directory,
agent, or approval ceremony is required merely to answer a small question.
Real authorization boundaries still apply to confidential data, external
publication, compute, and destructive operations.

The two Python utilities own only deterministic mechanics. Installation refuses
conflicts instead of acquiring overwrite/backup/rollback responsibilities.
The downloader assumes an authorized, curated URL manifest, pins TLS to validated
public DNS answers, and retains partial results in a fresh directory. DNS and
socket timeouts are not a wall-clock job scheduler. Host limits remain necessary
for hard deadlines. It does not parse or execute downloaded documents.

## Research engineering and event-driven coordination

**Decision, 2026-10-01:** Retain Astra as the sole lead, expose Engineering on
demand, and use coarse, event-driven delegation instead of periodic model-facing
check-ins. This extends the existing ownership boundary without adding a runtime.
Worker choice follows the task; delegation is optional.

The Engineering resource makes SOLID, strategic/tactical DDD, maturity, architectural
decisions, and scientific contracts available when implementation choices warrant
them. It does not prescribe a software framework for a small experiment. A changed
metric, workload mix, latency boundary, or preprocessing rule can invalidate evidence
without breaking an API; preserve the old definition and affected results.
The optional personal example remains outside `skills/coresearch`. The installer,
root maintenance instructions, discovery metadata, and Python utilities are unchanged.

### Separate three responsibilities

Astra owns research judgment and substantial direct work as well as synthesis.
Workers own bounded execution, local observation, tests, and correction. The host
owns scheduling, permissions, hard budgets, process supervision, and completion
transport. A health event does not require a model conversation unless it changes
a decision. Reducing lead-worker traffic must not remove tool feedback, meaningful
verification, budget enforcement, or the ability to interrupt unsafe work.

Use a compact initial contract and an evidence-bearing final handoff. Escalate
blockers, violated assumptions, material new evidence, and authority boundaries.
A checkpoint before an expensive experiment can be valuable if its result changes
the decision to proceed. A timer-driven request to restate progress is different.
Avoid transcript replay, forced narration of hidden reasoning, microtask relays,
and global barriers between independent assignments. Preserve raw artifacts for
selective inspection. Silence is not a success signal.

### Alternatives and reconsideration

Direct Astra remains preferable for strongly coupled or difficult work where
briefing and integration would dominate. Astra plus capable workers is the
default candidate for separable, substantial work, not an obligation to create a
hierarchy. Nested coordinators and continual lead approval add coordination and
must justify themselves against those simpler baselines.

Reconsider worker choices and delegation policy when representative runs show a
different quality/cost tradeoff, missed early failure, integration rework, or
changed host capabilities.
Measure time and spend to a valid deliverable, not just worker tokens or message
count. The [host protocol](validation.md) keeps Astra as lead and separates
delegation from check-in policy; no live comparative improvement is claimed by
this change.

### Evidence and limits of the architectural analogy

The following sources were inspected on 2026-09-29. They motivate the design;
they do not constitute a Coresearch performance evaluation.

- [OpenAI's skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
  recommends minimal routing, on-demand resources, and meaningful decision boundaries
  rather than inherited procedures for less capable models.
- [GPT-6.1 Sol documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
  describes a lower-cost option for complex work and recommends task-level comparison
  with Astra. That is vendor guidance, not evidence of a universal worker/lead ranking.
- [Async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling)
  supports continuing independent work and waiting when a pending result is needed.
  Job execution and result delivery remain application responsibilities.
- [Responses Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent)
  documents a same-model agent tree and availability constraints. It is not by itself
  a heterogeneous Astra/Sol runtime. Host support must be checked before assigning
  models; Coresearch does not implement an API transport or model router.
- [Raschka's article](https://magazine.sebastianraschka.com/p/gpt-6-astra-looped-transformers-and)
  discusses recurrent depth and hidden reasoning, not a controlled comparison of
  worker check-in schedules. Do not infer that a status message destroys latent
  state or that looped transformers prove a particular orchestration topology.
  [Recurrent-depth research](https://arxiv.org/abs/2502.05171)
  concerns computation inside a model, a different level from inter-agent messaging.

## Migration from version 1

This is a breaking replacement, not a compatibility release. The repository
contains no old role skills, `_coresearch` markers, `skills/manifest.json`, OMX
reference layer, `harness`/`bin` wrappers, shell installer, prompt template, or
old validation script.

On an existing machine, inspect the previous install before removal. Remove only
Coresearch-owned `research-*` skill directories or links and the old `coresearch`
copy/link from the previous installation; preserve unrelated skills and local
edits. Old defaults included `~/.codex/skills`, `~/.claude/skills`, and project
`.codex/skills` / `.claude/skills`. Install version 2 in the current host directory
shown in the README. A conflicting old destination is deliberately not erased.

Remove the old `~/.local/bin/harness` link only after confirming it belongs to
this checkout. Existing prompt blocks bounded by
`<!-- RESEARCH_AGENT_SKILLS:START -->` and `<!-- RESEARCH_AGENT_SKILLS:END -->`
are obsolete. Review and remove just that block, retaining all surrounding
instructions. A former full-project prompt needs a human-readable review to
retain genuine project constraints; do not replace it wholesale with the new
bundle's root `AGENTS.md`. The new installer never edits these files for you.

Keep old research artifacts, PDFs, notes, and ledgers as evidence. They need no
conversion to continue using them, and can be summarized into the optional brief
only when useful. New source batches use explicit URL JSON manifests. This is
one-time migration guidance, not a legacy runtime kept inside version 2.
