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
The lead can delegate independent questions in parallel and match worker
reasoning effort to investigation depth, following [OpenAI's GPT-6.2 prompting guide](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra).

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

The research capability mapping is intentional, not a silent feature drop:
`research-survey` and citation checking become Literature; `research-design`,
`research-loop`, and `research-engineer` become Experiments; `research-gap`,
`research-dialectic`, `research-causal`, `research-qualitative`, `research-audit`,
and `research-adversary` become Analysis. `research-write`, `research-review`,
`research-rebuttal`, and manuscript verification become Manuscripts. Source
verification remains shared with Literature. AI/ML/CV, Robotics, Graphics, HCI,
and hybrid evidence standards remain in the experiments resource. Office-format
mechanics stay with appropriate external tools.

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
Real authorization boundaries still apply to confidential data, participant
studies, external publication, compute, and destructive operations.

The two Python utilities own only deterministic mechanics. Installation refuses
conflicts instead of acquiring overwrite/backup/rollback responsibilities.
The downloader assumes an authorized, curated URL manifest, pins TLS to validated
public DNS answers, and retains partial results in a fresh directory. DNS and
socket timeouts are not a wall-clock job scheduler. Host limits remain necessary
for hard deadlines. It does not parse or execute downloaded documents.

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
