# Native Role Routing

`coresearch` is the only research-stage router. A native role performs one
bounded assignment and returns its artifact or result to the parent; the
parent then re-enters `coresearch` before selecting another research stage.

The source bundle's `agents/manifest.json` is the maintenance authority for role
names, provider models, effort policies, capabilities, and intended skills. Installed
runtimes do not receive or require a manifest under `.codex/agents` or
`.claude/agents`; every native role definition is complete. Do not look for a
runtime manifest, infer registration failure from its absence, substitute
another role name, or relax its capabilities when selecting a model.

## Assignment model

For Codex, choose a model and reasoning effort for every assignment and pass
both explicitly with the named role. Native Codex files omit `model` and
`model_reasoning_effort`: a file-level value would override the spawn request.
Use a bounded or no-history fork that accepts the selection. If the host cannot
apply it, report the limitation; never claim a different model was requested
or verified. Claude keeps its configured model and effort without overrides.

The following installed policy mirrors `agents/manifest.json`:

| Model | Assignment criteria |
| --- | --- |
| `gpt-6-sol` | Default orchestration, implementation, investigation, and synthesis; medium for clear contracts, high for complex dependencies or substantial replanning |
| `gpt-6-luna` | Prefer for known-source extraction, metadata, mechanical transformations, and prescribed execution with directly checkable outputs |
| `gpt-6-astra` | Difficult research design, conflicting evidence, causal judgments, and scientific claim verification where errors are consequential or hard to detect |

Start the main research session with Sol at medium effort when model choice is
available. This is a launch recommendation, not an automatic session switch;
respect the user's selected parent model and effort. The manifest's default
model and orchestrator effort describe this starting point. Workers still
require explicit model and effort on every assignment.

Prefer Luna when inputs, transformation, and validation are unambiguous. Use
Sol when an assignment requires interpretation, implementation judgment, or
substantive synthesis. Select by ambiguity, error consequence, and ease of
validation, not task length or role name. Start Sol assignments at medium;
use high for complex dependencies, diagnosis, or substantial replanning.
Luna can use low/medium for mechanical work and high for bounded reasoning;
checkable outputs remain required. These are workload hypotheses, not measured
guarantees.

Astra remains the uncertainty fallback. Request an Astra planner or verifier
for difficult research design, conflicting evidence, evaluation-contract
changes requiring scientific judgment, or consequential causal conclusions.
Keep scientific claim verification on Astra. The Sol parent must inspect the
supporting evidence before integrating the result; worker confidence is not
validation. If the parent itself needs a stronger model, report the need for
an explicit session selection rather than claiming to switch it automatically.

Effort is a separate choice; increasing a smaller model's effort does not
establish equivalence to Astra. Respect explicit user selections and budgets;
an unavailable or unapproved model requires reporting or a new authorized
selection, not silent substitution.

After a meaningful validation failure or demonstrated capability gap, the parent
may select a more capable model for a new bounded attempt within the existing
retry budget. Diagnose missing data, broken tools, or contract ambiguity first;
these do not justify cycling models. Preserve failed artifacts and record the
reason for escalation. Avoid automatic retry ladders. For unavailable models,
use the declared fallback only when permitted and accessible, recording the
changed request; a failed attempt remains a failed routing attempt.

## Assignment effort

Codex roles do not set `model` or `model_reasoning_effort`.
The parent chooses and explicitly passes `reasoning_effort` for each assignment:

| Effort | Assignment complexity |
| --- | --- |
| `low` | Known-source extraction, straightforward checks, or consolidation of resolved evidence |
| `medium` | Bounded implementation or experiment setup with clear inputs and validators |
| `high` | Multi-source reasoning, difficult diagnosis, or substantial uncertainty |
| `xhigh` | Deeply branching planning or verification with difficult claim dependencies |

These are decision criteria, not role defaults. A narrow verifier check can use
less effort than a difficult reading assignment. Record `requested_effort` and
a brief complexity rationale in the handoff before spawning. Do not pass the
manifest's `assignment` policy label as an effort value.

Prefer `fork_turns="none"` or a bounded history fork with the relevant task
context and artifact pointers to isolate detailed work. For Codex effort
selection, use a compatible fork; full-history forks may reject effort
overrides. If the host cannot accept the
selected effort, report that limitation instead of silently inheriting effort
or claiming verified routing. The child does not choose its own effort.

Claude roles retain their configured model and effort. Effort selection never
changes role capabilities, stage ownership, validators, or independence.

## Role selection

- `coresearch-reader`: bounded reading or extraction from already-known
  sources.
- `coresearch-researcher`: discovery, current external evidence, official
  documentation, or comparison across sources.
- `coresearch-implementer`: a mechanically clear local change after files,
  expected output, and validation are explicit. Integrated or materially
  branching implementation stays with the frontier parent until decomposed.
- `coresearch-experimenter`: mechanical experiment setup, execution,
  provenance, and result capture under an existing evaluation contract.
- `coresearch-debugger`: one difficult root-cause diagnosis after repeated
  implementation or experiment failure. It returns a minimal fix plan; an
  implementer owns any edit.
- `coresearch-planner`: materially branching research design or a durable
  mission decomposition.
- `coresearch-synthesizer`: consolidation after evidence and the mechanism
  decision are resolved. Unresolved causal or dialectical reconciliation stays
  with the frontier parent.
- `coresearch-verifier`: independent verification at a claim or completion
  boundary, and again after an evidence-changing edit. It never approves its
  own implementation.

Use the fewest roles that materially improve context isolation, quality, speed,
or safety. Keep trivial tasks in the parent; bounded scope alone is not a reason
to retain substantial work there. Do not assign two roles to mutate the same
files or add a role merely to re-check an unchanged result.

Use at most one fixed role per bounded assignment. Multiple independent assignments
may run concurrently when their inputs and owned scopes do not overlap.

## Orchestration-first durable runs

For authorized durable research runs, the parent primarily orchestrates.
Delegate substantial source reading, discovery, decomposed implementation,
experiment execution, and bounded diagnosis to their fixed roles. Sequential
delegation is useful when it keeps detailed investigation and execution traces
out of the parent's context, even without a parallel speedup.

The parent owns the research question, hypotheses, evaluation contract,
decomposition, dependency decisions, evidence reconciliation, integration, and
final conclusions. It must inspect the source passages, code, or measurements
needed to assess consequential findings; a worker summary is not independent
evidence. Resolve conflicting definitions and mechanism choices before asking
a synthesizer to consolidate them.

Keep trivial edits and tightly coupled reasoning in the parent when handoff
would lose essential context or add more work than it saves. Decompose substantial
implementation once its boundaries are clear. If workers are unavailable or
prohibited, continue bounded parent work when authority and budget permit;
report the limitation and do not fabricate role runs or waive required
independent verification. Respect user limits on delegation and concurrency.

This policy applies to the parent session. An assigned role performs its own
bounded work and returns to the parent; it never recursively delegates.

## Required handoff

Every role assignment states:

1. unique `assignment_id`, primary Coresearch skill, and field mode;
2. claim or evidence target;
3. `depends_on` assignment IDs and the input artifacts they must provide;
4. owned files and directories, plus read-only boundaries;
5. allowed data, external calls, credentials, privacy, and confidentiality;
6. expected artifact or result shape;
7. validation command or evidence requirement;
8. explicit stop and escalation conditions;
9. `working_modes` with explicit Ponytail or Caveman levels when active.
10. exact `requested_model` and `requested_effort`; for Codex, a selection rationale
    covering complexity, error consequence, and validation, plus the escalation
    reason when this is a retry.

Supply only relevant mission context, definitions, constraints, prior decisions,
and input artifact pointers, with precise source locations where available.
Enough context to interpret the evidence is essential; unrelated conversation
history and raw logs are not. Define the return contract in the handoff:

- result or finding and affected artifact paths;
- evidence locations and relevant commands/configuration for consequential claims;
- validation outcomes, uncertainty, counterevidence, and concrete blockers;
- stop reason and any decision the parent must resolve.

Keep raw logs in ignored scratch following
[execution-safe.md](execution-safe.md); preserve claim-bearing evidence in
declared artifacts. Return concise summaries with pointers, not full transcripts
or log dumps. The parent selectively opens supporting material to challenge or
integrate results. Use existing mission, ledger, and result fields; do not create
a separate context store or another state schema.

Keep model/effort rationale in the mission assignment or handoff; terminal
`role_runs` retains the actual requested values. Each attempt, including a
model escalation, gets its own assignment ID and terminal provenance. Compare
observed routing to that attempt's request, not a fixed historical model pin.

The role must not broaden the research question, choose the next research
stage, silently change the evaluation contract, or write outside its owned
scope. A role that reaches a boundary crossing reports it to the parent.

Working modes are task constraints, not capabilities. Pass
`working_modes.ponytail` or `working_modes.caveman` as `lite` or `full`; do not
assume a fresh role inherits them implicitly. They must not change model or
role selection, tools, permissions, research stage, evidence requirements, or
validation. See [ponytail.md](ponytail.md) and [caveman.md](caveman.md).

## Parallel assignments and joins

The parent owns fan-out, dependency joins, integration, and cancellation. It
may start assignments together only when every `depends_on` entry is complete
and their mutable scopes are disjoint.

- Prefer parallel reader, researcher, and other read-only assignments for
  independent sources, evidence lanes, or audits.
- Never let two assignments write the same file or output directory. Serialize
  overlapping write scopes; keep complex integrated edits in the parent until
  they can be decomposed safely.
- Wait for every dependency at a join before starting a consumer. A synthesizer
  runs only after its declared evidence inputs arrive.
- Integrate writable results before verification. A verifier runs against the
  stable integrated artifact, never concurrently with evidence-changing work.
- Record one terminal `role_runs` entry per assignment, including failures and
  cancellations. Do not discard a partial result when another lane succeeds.

This is a bounded assignment graph inside the existing mission, not another
stage router or workflow engine. Specialized roles never spawn descendants.

## Capability boundary

Planner, researcher, reader, debugger, synthesizer, and verifier are
read-only. Non-mutating checks are allowed when their assignment permits them.
Only implementer and experimenter may edit the workspace, and their handoff
must name the exact owned scope and smallest relevant validation.

## Escalation and re-entry

- A reader escalates discovery needs to the parent for researcher routing.
- A researcher reports an implementation need instead of editing.
- An implementer or experimenter reports repeated failure; the parent may
  route one diagnostic assignment to the debugger.
- A debugger returns diagnosis and a minimal fix plan to the parent.
- A synthesizer returns unsupported claims to evidence collection.
- A verifier returns a verdict and concrete gaps; evidence-changing fixes
  require a fresh independent verification.

All terminal role results return to the parent. The parent records authorized
ledger updates, re-enters `coresearch`, and chooses the next primary skill.
