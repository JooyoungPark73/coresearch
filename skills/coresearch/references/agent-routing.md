# Native Role Routing

`coresearch` is the only research-stage router. A native role performs one
bounded assignment and returns its artifact or result to the parent; the
parent then re-enters `coresearch` before selecting another research stage.

The authoritative role names, provider models, efforts, capabilities, and
intended skills live in [`agents/manifest.json`](../../../agents/manifest.json).
Do not substitute another role name or pass a per-invocation model override.

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

Use the fewest roles that materially improve quality, speed, or safety. Do not
delegate a narrow task the parent can complete directly, do not assign two
roles to mutate the same files, and do not add a role merely to re-check an
unchanged result.

Use at most one fixed role per bounded assignment. Multiple independent assignments
may run concurrently when their inputs and owned scopes do not overlap.

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
