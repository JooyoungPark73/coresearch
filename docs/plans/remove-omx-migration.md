# Coresearch OMX-Removal Migration Plan

Status: implementation-ready plan; no migration changes have been applied.

Primary execution surface: Codex CLI `/goal`.

## 1. Objective

Remove oh-my-codex (OMX) from Coresearch's runtime, routing, installation,
documentation, and validation paths while preserving the research behavior that
Coresearch owns:

- the central `coresearch` stage and skill router;
- all 15 Coresearch-owned `coresearch` and `research-*` skills;
- the source -> evidence -> claim -> conclusion research contract;
- the validator-gated research loop;
- reproducible research implementation and experiment execution;
- the canonical research decision ledger;
- bounded native subagent delegation on Codex and Claude Code;
- exact provider/model/effort routing through a fixed set of Coresearch roles;
- a canonical `DESIGN.md` explaining Coresearch's structure, boundaries,
  control flow, state, installation topology, and extension rules;
- marker-bounded project/global prompt updates, dry-run diffs, backups, and
  rollback;
- copy and symlink installation for user and project scopes.

The final bundle must run without `omx` installed, must never invoke `omx`, and
must not refer to OMX as an active or optional execution lane.

## 2. Locked Decisions

These are migration requirements, not open design questions.

1. Coresearch becomes a standalone Codex + Claude Code research bundle.
2. OMX modes, roles, state, hooks, markers, detection, setup instructions, and
   acceleration routes are removed from active surfaces.
3. Historical migration documentation may name OMX. Runtime files, active
   guidance, manifests, installers, templates, and tests may not depend on it.
4. `coresearch` remains the only research-stage router. Role agents execute a
   bounded assignment and return to `coresearch`; they do not independently
   choose the next research stage.
5. Codex `/goal` supplies durable execution for long implementation and
   experiment missions. It does not replace the Coresearch research loop or
   ledger.
6. Claude Code executes the same host-neutral mission contract through its
   native session and subagent surfaces. Coresearch will not emulate `/goal`
   with a second workflow engine.
7. Coresearch owns exactly eight provider-neutral role names. Each role pins an
   exact Codex model ID and exact Claude model ID plus an explicit effort.
8. Rolling Claude aliases (`opus`, `sonnet`, `haiku`, `inherit`) and the Codex
   `gpt-5.6` alias are forbidden in Coresearch role definitions.
9. A requested model mismatch is never silently reported as successful
   routing. Static validation and optional live routing probes must expose
   `verified`, `static-only`, or `mismatch` status.
10. The canonical research state remains
    `docs/research/decisions/ledger.yaml`. No `.omx/` or `.agents/` state forest
    replaces it.
11. Existing safe harness behavior is preserved when it is provider-neutral:
    installation, linking, initialization, status, inventory, doctor, repair,
    update, diff, backups, rollback, and optional marker-bounded bridges.
12. No new third-party dependency is added for this migration.
13. The untracked user files `PROMPT.md` and `PROMPT(1).md` are read-only
    migration examples. Do not edit, delete, add, or stage them.
14. A root `DESIGN.md` becomes the canonical developer-facing structural
    overview. It explains relationships and ownership but links to executable
    manifests/contracts instead of becoming a second source of truth.

## 3. Current-State Evidence

The migration must preserve the research method and remove only its external
orchestration coupling.

- `skills/manifest.json:4-79` declares the 15 owned skills. Its
  `external_routes` at `skills/manifest.json:81-92` are entirely external
  OMX-style lanes and must be removed.
- `skills/coresearch/SKILL.md:57-106` contains the central router but currently
  names OMX lanes, `.omx` mirrors, and an OMX-specific handoff reference.
- `skills/coresearch/references/research-contract.md:3-6` defines the core
  source/evidence/claim/conclusion invariant. This remains unchanged in
  meaning.
- `skills/coresearch/references/research-contract.md:74-83` already defines
  harness-level research safeguards independent of OMX.
- `skills/coresearch/references/state-ledger.md:44-65` defines idempotent,
  key-scoped ledger updates. `state-ledger.md:84-91` makes
  `docs/research/decisions/ledger.yaml` canonical but still describes `.omx`
  mirrors; only the mirror language is removed.
- `skills/research-loop/SKILL.md:25-70` already contains the essential mission,
  hypotheses, evaluation, artifact, validator, sandbox, retry, and stop
  contracts. Its OMX handoff and state paragraphs at `:66-70` and `:88-115`
  are replaced with host-neutral run and goal contracts.
- `skills/research-engineer/SKILL.md` remains the implementation/experiment
  workflow. Do not replace it with a generic coding workflow.
- `skills/coresearch/references/omx-pony-caveman.md:50-84` contains useful
  bounded-handoff and re-entry ideas mixed with OMX role and mode names. Extract
  the useful contract into a neutral reference, then delete this file.
- `scripts/harness.py:35-44` has provider-neutral Codex/Claude home resolution.
  Its OMX detection and prompt-signature branches at `:235-269`, `:606-619`,
  `:784-849` are removed.
- `scripts/install.sh:107-149` already has safe copy/symlink skill installation.
  Its active OMX bridge and setup text at `:218-223`, `:277-283`, and
  `:314-316` is removed or neutralized.
- `templates/research/AGENTS.md:48-83` contains the intended research routing
  contract, but `:54-67` depends on OMX lanes and OMX roles. Its marker blocks
  at `:184-187` are deleted.
- `scripts/validate.sh:518-537` locks the current OMX-conditional bridge, while
  `:596-600` probes the OMX executable. These tests must be replaced rather
  than simply deleted.
- `.codex-plugin/plugin.json:26` packages only `./skills/`. Keep plugin
  packaging skill-only unless the official plugin schema is separately
  verified to support native agents; the harness is the canonical role-agent
  installer for this migration.

Baseline evidence captured before planning:

- branch: `feat/system`;
- dirty state: only untracked `PROMPT.md` and `PROMPT(1).md`;
- `./scripts/validate.sh`: PASS, exit 0, approximately 5 seconds;
- baseline log: ignored `.tmp/pre-omx-removal-validation.log`.

## 4. Target Architecture

```text
research request
    |
    v
coresearch skill router
    |-- selects one primary research-* skill
    |-- selects one fixed Coresearch role when delegation helps
    v
native host adapter
    |-- Codex: .codex/agents/*.toml and optional /goal
    `-- Claude: .claude/agents/*.md and native session/subagents
    v
bounded task or research mission
    |-- artifacts
    |-- validators
    |-- exact model-routing provenance
    `-- result.json
    v
docs/research/decisions/ledger.yaml
    v
independent coresearch-verifier at a claim boundary
    v
coresearch re-entry for the next stage
```

Repository layout after migration:

```text
DESIGN.md                         # canonical architecture/structure overview
agents/
  manifest.json                  # canonical fixed role/model matrix
  codex/*.toml                   # Codex-native role definitions
  claude/*.md                    # Claude Code-native role definitions
skills/
  manifest.json                  # owned skills only
  coresearch/
    SKILL.md                     # central research router
    references/
      agent-routing.md           # bounded role selection and escalation
      execution-adapters.md      # Codex /goal and Claude handoff rules
      research-contract.md
      state-ledger.md
      ...
templates/research/AGENTS.md      # standalone project research contract
scripts/harness.py               # canonical installer/doctor implementation
scripts/install.sh               # compatibility wrapper or thin entry point
scripts/link-local.sh            # symlink-development wrapper
scripts/validate.sh              # zero-OMX regression suite
```

Do not create a new public workflow skill solely to imitate OMX. Extend
`research-loop` with the host-neutral run contract and place host-specific
details in `coresearch/references/execution-adapters.md`.

## 5. Fixed Coresearch Role Matrix

Create exactly these role names on both providers.

| Role | Main responsibility | Codex model / effort | Claude model / effort | Default capability |
|---|---|---|---|---|
| `coresearch-planner` | Research architecture, hypothesis/evaluation planning, durable goal decomposition | `gpt-5.6-sol` / `xhigh` | `claude-opus-5` / `xhigh` | Read-only; may inspect and browse |
| `coresearch-researcher` | Broad retrieval, current official documentation, literature discovery, multi-source comparison | `gpt-5.6-terra` / `high` | `claude-sonnet-5` / `high` | Read/search/web; no repository edits |
| `coresearch-reader` | Narrow paper/doc reading, metadata extraction, abstraction, evidence extraction | `gpt-5.6-luna` / `low` | `claude-haiku-4-5-20251001` / `low` | Read/search only |
| `coresearch-implementer` | Clear bounded code/config/test changes | `gpt-5.6-luna` / `medium` | `claude-haiku-4-5-20251001` / `medium` | Workspace write; targeted tests |
| `coresearch-experimenter` | Mechanical experiment setup/execution, provenance, result capture | `gpt-5.6-luna` / `medium` | `claude-haiku-4-5-20251001` / `medium` | Workspace write and bounded commands |
| `coresearch-debugger` | Difficult root-cause analysis after observed failures | `gpt-5.6-sol` / `high` | `claude-opus-5` / `high` | Read/diagnose; fixes return to implementer |
| `coresearch-synthesizer` | Integrate collected evidence into scoped claims and conclusions | `gpt-5.6-sol` / `low` | `claude-opus-5` / `low` | Read-only; no new evidence fabrication |
| `coresearch-verifier` | Independent claim, methodology, implementation, and completion gate | `gpt-5.6-sol` / `xhigh` | `claude-opus-5` / `xhigh` | Read-only, may run non-mutating checks |

Routing and escalation rules:

1. Use `coresearch-reader` for bounded reading/extraction when sources are
   already known.
2. Use `coresearch-researcher` when discovery, current external evidence, or
   cross-source comparison is required.
3. Use `coresearch-implementer` only after scope, owned files, expected output,
   and validation are explicit.
4. Use `coresearch-experimenter` for execution and capture, not for changing
   the research question or evaluation contract.
5. Repeated implementation or experiment failure routes once to
   `coresearch-debugger`; the debugger diagnoses and returns a minimal fix plan.
6. Use `coresearch-planner` for materially branching research design and for
   constructing long-running goal missions.
7. Use `coresearch-synthesizer` only after evidence exists.
8. Use `coresearch-verifier` once at a claim/completion boundary and after any
   later evidence-changing edit. It must not approve its own implementation.
9. Every role receives: primary skill, field mode, claim/evidence target,
   owned/read-only scope, confidentiality limits, expected artifact,
   validation, and stop condition.
10. Every role returns its artifact/result to the parent. The parent re-enters
    `coresearch`; role agents do not chain other research stages themselves.

## 6. Exact Model Routing Contract

### 6.1 Static pins

`agents/manifest.json` is the canonical machine-readable role matrix. It must
contain:

- a schema version;
- exactly eight roles;
- the Codex model and effort for each role;
- the Claude model and effort for each role;
- read/write capability and intended skill set;
- a role-description version.

Native agent definitions must repeat the resolved model/effort because both
hosts require those fields in their own formats. Validation compares every
native definition against the canonical manifest and fails on drift.

For Claude 4.6-generation and later, a dateless full model ID is a fixed
snapshot rather than a rolling alias. Therefore `claude-opus-5` and
`claude-sonnet-5` satisfy the full-version pin requirement; Haiku remains the
dated `claude-haiku-4-5-20251001`. See Anthropic's
[model ID and versioning contract](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions).

The Codex IDs and supported effort levels follow OpenAI's current
[GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model).

### 6.2 Override and substitution defense

Static configuration alone is not proof that a host used the requested model.
Claude Code resolves an environment override and a per-invocation model before
the agent definition, and may substitute an inherited model when an exact ID is
blocked by an organization allowlist. This behavior is documented in
[Claude Code subagents](https://code.claude.com/docs/en/sub-agents).

Implement these controls:

- Coresearch instructions must not pass a per-invocation model override.
- `harness doctor --strict` fails when
  `CLAUDE_CODE_SUBAGENT_MODEL` is set during a Coresearch routing audit.
- Static doctor verifies exact model and effort fields in all 16 native role
  definitions.
- Add `harness doctor --strict --probe-models` as an explicit network/token-using
  runtime audit. It launches the smallest supported probe per distinct model,
  reads host-reported model usage/metadata, and compares the observed model to
  the manifest.
- A host that cannot expose the observed model returns `static-only`; it must
  not return `verified`.
- A blocked, substituted, unavailable, or different model returns nonzero with
  `mismatch` and requested/observed IDs.
- Normal research result artifacts record the requested model. When the host
  exposes the observed model, record that too.

Do not claim that native model selection is infallible. The acceptance claim is
that Coresearch pins exact IDs, detects known override paths, and refuses to
label routing verified without runtime evidence.

## 7. Host-Neutral Research Run Contract

For durable work, `research-loop` creates or updates these artifacts under the
user project's declared research output path:

```text
docs/research/runs/<run-id>/mission.md
docs/research/runs/<run-id>/sandbox.md
docs/research/runs/<run-id>/result.json
```

`mission.md` contains:

- objective and non-goals;
- research question and intended contribution;
- hypotheses/design questions;
- evaluation contract;
- artifacts and validators;
- ordered experiment units;
- retry/fix budget;
- success, blocked, failure, cancellation, and human-decision stop conditions;
- ledger path and keys this run may update;
- the role assignments allowed for the run.

`sandbox.md` contains:

- allowed files and directories;
- allowed data, models, APIs, and external calls;
- compute/time/token/cost budgets when known;
- credentials, privacy, and confidentiality boundaries;
- destructive and external-write prohibitions;
- long-command log location and cancellation policy.

`result.json` has this minimum schema:

```json
{
  "schema_version": 1,
  "run_id": "string",
  "mission_path": "string",
  "status": "success|blocked|failed|cancelled",
  "host": "codex|claude",
  "goal_id": "string|null",
  "role": "coresearch-*",
  "requested_model": "string",
  "requested_effort": "string",
  "observed_model": "string|null",
  "observed_effort": "string|null",
  "routing_status": "verified|static-only|mismatch",
  "artifacts": [],
  "validators": [],
  "claim_evidence": [],
  "ledger_updates": [],
  "remaining_risks": [],
  "stop_reason": "string"
}
```

The ledger gains an optional backward-compatible `execution_state` section:

```yaml
execution_state:
  active_run: {id, mission_path, host, status}
  completed_runs: [{id, result_path, status}]
```

Old ledgers without this section remain valid. Skills update only the run keys
they own and retain the existing idempotent update rules.

### Codex adapter

Use `/goal` only when the task is multi-turn, experiment-bearing, or requires
durable validators. The goal objective references the mission file rather than
embedding the full mission in the slash command. Canonical handoff shape:

```text
/goal Execute docs/research/runs/<run-id>/mission.md within sandbox.md. Keep
docs/research/decisions/ledger.yaml current. Stop only after result.json has a
terminal status and every required validator has evidence, or when a declared
blocked/failure/human-decision condition is reached.
```

The goal owns continuation; Coresearch owns research routing and evidence
quality. `/goal` must not be used for a narrow answer, one bounded read, or a
single small edit.

### Claude Code adapter

Claude Code receives the same mission and sandbox paths and uses the installed
fixed role definitions. Do not create a fake `/goal`, `.omx` state, or a second
ledger. The main Claude session owns continuation and writes the same
`result.json` terminal record.

## 8. Implementation Sequence

Follow this order. Each phase must leave the repository parseable and must run
its targeted validation before the next phase.

### Phase 0: Freeze behavior and add failing migration checks

Files:

- `scripts/validate.sh`
- `.gitignore` only if required by later cleanup

Actions:

1. Re-run the existing validation and preserve the baseline PASS summary.
2. Add tests for the new contract before editing implementation:
   - exactly 15 owned skills remain;
   - `skills/manifest.json` has no `external_routes`;
   - exactly eight canonical roles exist;
   - both provider definitions exist for every role;
   - every model/effort matches `agents/manifest.json`;
   - aliases and `inherit` are rejected;
   - active runtime/template/install files contain no OMX lanes, markers,
     commands, or `.omx` paths;
   - neutral bridges apply whether or not an `omx` executable exists;
   - the research-loop run contract and result fields exist;
   - installers handle skills and agents on both surfaces.
3. Scope the banned-reference scan to active files. Exclude this migration plan,
   an explicit historical migration note, `.git/`, `.tmp/`, and the untracked
   `PROMPT*.md` examples.
4. Confirm the new tests fail for the expected pre-migration reasons, not from
   syntax or fixture errors.

Acceptance:

- baseline suite still passes before the new assertions;
- new migration assertions fail with precise messages naming the old OMX
  surfaces;
- untracked prompt examples remain unchanged.

### Phase 1: Add the role manifest and neutral routing contracts

Files to add:

- `agents/manifest.json`
- `skills/coresearch/references/agent-routing.md`
- `skills/coresearch/references/execution-adapters.md`

Files to remove after references are migrated:

- `skills/coresearch/references/omx-pony-caveman.md`

Files to update:

- `skills/coresearch/references/skill-catalog.md`
- `skills/coresearch/references/routing.md`
- `skills/coresearch/references/reasoning-skills.md` if it refers to the old
  handoff surface

Actions:

1. Encode the eight-role matrix exactly as specified in section 5.
2. Extract bounded handoff, owned scope, expected output, stop condition, and
   `coresearch` re-entry rules into `agent-routing.md`.
3. Put `/goal` and Claude session behavior in `execution-adapters.md`.
4. Replace the optional OMX acceleration catalog with the fixed native role
   catalog.
5. Remove Ponytail/Caveman behavior rather than renaming it.

Acceptance:

- the manifest parses with Python standard library JSON;
- role names and pins match section 5 exactly;
- the neutral references contain no active OMX concepts;
- all relative links from `coresearch/SKILL.md` resolve after the old file is
  removed.

### Phase 2: Add native Codex and Claude role definitions

Files to add:

- `agents/codex/coresearch-planner.toml`
- `agents/codex/coresearch-researcher.toml`
- `agents/codex/coresearch-reader.toml`
- `agents/codex/coresearch-implementer.toml`
- `agents/codex/coresearch-experimenter.toml`
- `agents/codex/coresearch-debugger.toml`
- `agents/codex/coresearch-synthesizer.toml`
- `agents/codex/coresearch-verifier.toml`
- matching eight files under `agents/claude/` with `.md` suffixes

Actions:

1. Codex TOML files must define the native name, description, exact `model`,
   exact `model_reasoning_effort`, least-privilege sandbox, relevant skills, and
   bounded developer instructions.
2. Claude Markdown files must define YAML frontmatter with name, description,
   exact `model`, explicit `effort`, least-privilege tools/permission mode,
   relevant skills, and a bounded role prompt.
3. Read-only roles omit editing tools. Implementer and experimenter retain only
   the tools needed for local workspace edits and bounded commands.
4. Role prompts state that evidence/result artifacts return to the parent and
   that stage selection returns to `coresearch`.
5. Keep prompts short; shared research rules remain in Coresearch skills and
   references rather than being copied eight times.

Acceptance:

- all Codex files parse via `tomllib`;
- all Claude frontmatter passes the repository parser and, when available,
  `claude plugin validate` against the agent directory;
- no agent uses a model alias or inherited model;
- manifest/native-definition comparison is exact;
- read-only roles have no write capability;
- the two writable roles have explicit owned-scope and validation rules.

### Phase 3: Make Coresearch and research skills standalone

Files to update:

- `skills/coresearch/SKILL.md`
- `skills/coresearch/references/routing.md`
- `skills/coresearch/references/skill-catalog.md`
- `skills/coresearch/references/state-ledger.md`
- `skills/coresearch/references/execution-safe.md`
- `skills/research-loop/SKILL.md`
- `skills/research-design/SKILL.md`
- `skills/research-survey/SKILL.md`
- `skills/research-verify/SKILL.md`
- `skills/research-review/SKILL.md`
- any other owned skill found by the banned-reference test
- `skills/manifest.json`

Actions:

1. Keep `coresearch` as a lightweight stage/skill router. Replace OMX lane
   selection with native fixed-role selection and goal/session selection.
2. Preserve the rule that one primary research skill owns an invocation and
   that every completed skill/role re-enters `coresearch`.
3. Remove `external_routes` from `skills/manifest.json`; bump its schema version
   only if the manifest schema materially changes.
4. Replace `research-loop`'s OMX handoff with the run contract in section 7.
5. Preserve its validator, retry, fix-cycle, sandbox, claim-bearing evaluation,
   and stop rules.
6. Extend `state-ledger.md` with optional `execution_state`; remove all `.omx`
   mirror language.
7. Replace `omx ask claude` advisor language in `execution-safe.md` with one
   bounded native Coresearch role. Raw logs remain under ignored `.tmp/`.
8. Remove OMX-specific wording from review/verify/survey/design without
   changing their research standards.
9. Do not add generic coding, planning, or QA workflows that duplicate the
   native hosts. Preserve research-specific behavior only.

Acceptance:

- all 15 skill names and their research purposes remain available;
- core routing chooses a skill, an optional fixed role, and a host execution
  adapter without mentioning OMX;
- no skill writes runtime state into its own directory;
- old ledgers remain valid;
- `research-loop` can emit a complete mission/sandbox/result contract for both
  hosts;
- no active skill/reference contains an OMX command, lane, marker, or `.omx`
  path.

### Phase 4: Extend and simplify the harness

Files to update:

- `scripts/harness.py`
- `scripts/install.sh`
- `scripts/link-local.sh`
- `harness`, `bin/harness` only if wrapper arguments change

Actions:

1. Make `scripts/harness.py` the canonical install/status/doctor logic for both
   skills and agents. Reduce `scripts/install.sh` and `scripts/link-local.sh` to
   thin compatibility entry points where practical.
2. Install role definitions to:
   - user Codex: `${CODEX_HOME:-~/.codex}/agents`;
   - project Codex: `<project>/.codex/agents`;
   - user Claude: `${CLAUDE_HOME:-~/.claude}/agents`;
   - project Claude: `<project>/.claude/agents`.
3. Preserve `--surface codex|claude|both`, `--scope user|project`, and
   `--mode copy|symlink` for both skills and roles.
4. In symlink mode, link native role definitions so local edits propagate.
5. Never overwrite an unrelated user agent with the same filename. Replace
   only recognized Coresearch copies/symlinks or entries explicitly authorized
   by `--force`.
6. Extend `status`, `inventory`, `doctor`, and `repair` to report both skills
   and roles, including requested model and effort.
7. Remove OMX signature constants, executable detection, install prompts,
   `CORESEARCH_OMX_CHECK`, conditional bridge behavior, and runtime version
   checks.
8. Keep project/global Coresearch bridges provider-neutral and optional. A
   requested bridge applies without inspecting whether OMX exists.
9. Keep marker-bounded diff, backup, idempotent upsert/remove, and rollback
   behavior. Never replace a complete existing project `AGENTS.md` without the
   existing explicit replacement semantics.
10. Add static routing checks to normal strict doctor. Add the explicit
    token/network-using `--probe-models` path described in section 6.2.
11. Keep repair deterministic: relink/copy Coresearch skills and agents, run
    validation, then strict doctor.

Acceptance:

- user and project copy installs contain all 15 skills and 8 correct native
  roles per selected surface;
- user and project symlink installs resolve to this repository;
- `--surface both` installs correct provider-specific role files;
- broken Coresearch links are repaired while unrelated user entries remain;
- neutral bridge dry-run/apply/idempotency/remove/rollback tests pass with an
  empty `PATH` and with a fake `omx` binary; results are identical;
- `doctor --strict` never invokes or checks OMX;
- `doctor --strict --probe-models` returns verified, static-only failure, or
  mismatch failure according to section 6.2.

### Phase 5: Create canonical Coresearch design/structure documentation

File to add:

- `DESIGN.md`

Files that must link to it:

- `README.md`
- `AGENTS.md`

Purpose:

`DESIGN.md` is the developer-facing map of how Coresearch is assembled and why
its boundaries exist. It is not an installable prompt, skill, role definition,
model manifest, runtime ledger, or user tutorial. Those remain authoritative in
their own files.

Required sections:

1. **Purpose and non-goals** — what Coresearch owns; what it delegates to Codex
   or Claude Code; why it does not implement another generic workflow engine.
2. **Design invariants** — one research router, one primary skill per
   invocation, explicit evidence/claim binding, canonical ledger, bounded
   delegation, exact role pins, independent verification, and no provider-
   specific state forest.
3. **Repository structure and ownership** — a directory/component table for
   `skills/`, `agents/`, `templates/`, `scripts/`, plugin metadata, and research
   run artifacts. State who may read/write each surface.
4. **Research control flow** — intake -> `coresearch` -> primary skill ->
   optional fixed role -> host adapter -> artifacts/ledger -> verifier ->
   `coresearch` re-entry.
5. **Skill architecture** — router versus complete role skills, progressive
   loading of references, re-entry semantics, and how the 15-skill manifest is
   extended without overlapping ownership.
6. **Role architecture** — the eight provider-neutral roles, least-privilege
   categories, escalation edges, and why exact provider pins live in
   `agents/manifest.json` rather than prose.
7. **Host adapters** — Codex native agents and `/goal`; Claude Code native
   agents/session continuation; which behaviors are shared and which remain
   host-specific.
8. **State and artifact model** — canonical ledger, mission/sandbox/result
   artifacts, raw `.tmp` logs, evidence artifacts, update ownership, and
   backward compatibility.
9. **Installation topology** — user/project x Codex/Claude x copy/symlink,
   optional prompt bridges, template installation, ownership/non-overwrite
   rules, doctor, repair, and rollback.
10. **Trust and safety boundaries** — confidentiality, untrusted source text,
    credentials, external writes, destructive actions, model substitution, and
    observed-model verification.
11. **Extension guide** — checklists for adding a research skill, role, provider
    adapter, ledger field, or harness command while preserving single-source
    ownership and tests.
12. **Validation and lifecycle** — static contracts, integration matrix,
    optional live probes, model-pin upgrades, schema/version changes, and the
    requirement to update `DESIGN.md` when architectural boundaries change.
13. **Architectural decisions** — concise rationale and consequences for the
    standalone design, fixed roles, host-neutral run contract, and canonical
    ledger; link to `docs/migrations/from-omx.md` for historical detail.

Required diagrams:

- one compact component diagram showing router, skills, role definitions,
  host adapters, run artifacts, ledger, and verifier;
- one execution sequence for a durable experiment from request through
  `/goal` or Claude continuation to verified result and router re-entry;
- one installation topology showing source files and user/project destinations
  for both providers.

Use Mermaid or plain Markdown diagrams that render on GitHub. Keep diagrams
structural; do not duplicate all skill descriptions or role prompts in them.

Single-source-of-truth table required in `DESIGN.md`:

| Concern | Authoritative file |
|---|---|
| Owned skill inventory | `skills/manifest.json` |
| Fixed roles and model/effort pins | `agents/manifest.json` |
| Stage/skill routing behavior | `skills/coresearch/SKILL.md` and `skills/coresearch/references/routing.md` |
| Claim/evidence rules | `skills/coresearch/references/research-contract.md` and `evidence-grounding.md` |
| Durable research state | `skills/coresearch/references/state-ledger.md` |
| Host execution semantics | `skills/coresearch/references/execution-adapters.md` |
| Native provider definitions | `agents/codex/` and `agents/claude/` |
| Installation behavior | `scripts/harness.py` |
| Installed project behavior | `templates/research/AGENTS.md` |
| User-facing setup and examples | `README.md` |

Documentation rules:

1. Describe boundaries and rationale; link to detailed behavioral contracts.
2. Do not manually duplicate JSON schemas, complete agent prompts, the full
   role/model matrix, or all skill procedures.
3. If a short table repeats machine-readable facts for readability, validation
   must prove it matches the authoritative manifest.
4. Use relative repository links and verify that every target exists.
5. Distinguish architecture invariants from current implementation details.
6. Label historical migration rationale as history, never active routing.
7. Add a working agreement to root `AGENTS.md`: architectural boundary,
   manifest ownership, run-artifact, or installation-topology changes require a
   corresponding `DESIGN.md` update.

Acceptance:

- `DESIGN.md` contains all 13 required sections and three structural diagrams;
- it clearly distinguishes design documentation from prompts, skills,
  manifests, and runtime state;
- its single-source-of-truth table points to existing files;
- README and root AGENTS link to it;
- every local path/link in it resolves;
- it contains no active OMX instruction or optional compatibility path;
- validation detects missing required sections, broken local links, and any
  repeated role/model table that drifts from `agents/manifest.json`.

### Phase 6: Rewrite templates, metadata, and user documentation

Files to update:

- `AGENTS.md`
- `templates/research/AGENTS.md`
- `README.md`
- `.codex-plugin/plugin.json`
- `.gitignore`

File to add:

- `docs/migrations/from-omx.md`

Actions:

1. Rewrite the root development contract as a standalone Codex/Claude bundle
   contract. Preserve the distinction between root development guidance and
   the installable template. Link to `DESIGN.md` and require it to stay current
   when architectural boundaries change.
2. Rewrite the research template around Coresearch skills, the eight native
   roles, host-neutral run artifacts, `/goal`, the ledger, and verification.
3. Delete OMX runtime/team marker blocks.
4. Rewrite README installation and workflow examples around skills + native
   role installation. Include exact paths, model pins, strict doctor, runtime
   probe behavior, `/goal` handoff, and Claude execution. Link to `DESIGN.md`
   for structural details rather than duplicating them.
5. Remove OMX keywords and descriptions from plugin metadata. Keep its skills
   path and do not invent an unverified native-agent plugin field.
6. Remove `.omx/` from `.gitignore` if no retained tool generates it. Keep
   `.tmp/` ignored for execution logs.
7. Add a concise historical migration document that explains removed
   commands/concepts and their replacements. This is the only tracked document
   besides this plan that may intentionally discuss OMX in detail.
8. Do not touch or stage the untracked `PROMPT*.md` files. Put a standalone
   `/goal` example in README/migration docs instead.

Acceptance:

- a new user can install and operate Coresearch without knowing OMX existed;
- template and README role/model tables match `agents/manifest.json`;
- active metadata contains no OMX keyword or optional-route claim;
- root and template AGENTS files contain no OMX marker;
- historical references are clearly labeled migration history, not active
  instructions.

### Phase 7: Replace validation and prove zero-OMX operation

Files:

- `scripts/validate.sh`
- fixtures embedded or created by the validation script

Required validation groups:

1. Static structure:
   - plugin and both manifests parse;
   - shell scripts parse;
   - Python compiles without committed cache;
   - 15 skills and 8 roles are exact;
   - all relative skill links resolve;
   - `DESIGN.md` has its required structure, diagrams, source-of-truth table,
     and resolvable local links.
2. Role contract:
   - all 16 native definitions parse;
   - exact model and effort parity with manifest;
   - no alias/inherit values;
   - least-privilege read/write classification;
   - role skill references resolve.
3. Zero-OMX active surface:
   - no active installer/template/skill/manifest/runtime test invokes `omx`;
   - no `.omx` state path or OMX runtime marker remains;
   - historical plan/migration docs are explicit scan exclusions.
4. Install matrix:
   - user/project x copy/symlink x codex/claude/both;
   - idempotency;
   - external-file non-overwrite;
   - removed/stale Coresearch entry pruning;
   - broken-link detection and repair.
5. Prompt initialization:
   - bridge dry-run/apply/idempotency/remove;
   - full-template install and replace protection;
   - backups and rollback;
   - identical behavior regardless of an `omx` executable on `PATH`.
6. Research contracts:
   - research contract and ledger keys remain present;
   - legacy ledger compatibility;
   - run artifact paths and minimum `result.json` schema;
   - `/goal` adapter and Claude adapter both reference the same mission.
7. Documentation consistency:
   - README and root AGENTS link to `DESIGN.md`;
   - design structure does not duplicate executable contracts without a drift
     assertion;
   - any repeated role/model facts match `agents/manifest.json`;
   - active design text passes the zero-OMX scan.
8. Doctor:
   - correct installed skills and roles pass strict doctor;
   - wrong model, wrong effort, alias, missing role, broken link, or environment
     override fails with a targeted message;
   - runtime probes are explicit and never run during ordinary validation.

Final local commands:

```bash
./scripts/validate.sh
./harness status
./harness doctor --strict
```

Run live routing probes only when credentials/network/token spend are available
and authorized:

```bash
./harness doctor --strict --probe-models
```

Capture full validation output under ignored `.tmp/` and report only exit code,
duration, PASS/FAIL summary, and log path.

Acceptance:

- `./scripts/validate.sh` exits 0 with an exact final PASS line;
- static strict doctor exits 0 in clean temporary Codex and Claude homes;
- no test requires OMX to be installed;
- runtime route verification is never silently skipped when explicitly
  requested.

### Phase 8: Independent verification and cleanup

Actions:

1. Run the complete validation once on the final diff.
2. Inspect `git diff --check` and the final file list.
3. Run the active-surface banned-reference search manually and classify every
   remaining match as historical plan/migration text or a defect.
4. Verify no `.omx/`, `.agents/`, cache, temporary, or generated run artifact is
   staged.
5. Verify `PROMPT.md` and `PROMPT(1).md` remain byte-for-byte unchanged and
   untracked.
6. Invoke an independent `coresearch-verifier` definition, or the closest
   available native verifier before the new definitions are installed, to
   review:
   - research behavior preservation;
   - exact role/model routing;
   - design documentation accuracy and single-source ownership;
   - installer safety;
   - test adequacy;
   - remaining active OMX coupling.
7. Apply only evidence-backed findings, rerun affected targeted tests, then run
   the complete validation once more if the diff changed.

Stop only when all acceptance criteria in section 9 are satisfied or a declared
blocker is recorded with evidence.

## 9. Final Acceptance Criteria

The migration is complete only when all of the following are true.

### Research behavior

- [ ] All 15 owned skills from the original manifest remain installed and
      discoverable.
- [ ] `coresearch` remains the sole stage router and re-entry point.
- [ ] The research contract still prohibits unsupported novelty, causal, and
      major claims.
- [ ] `research-loop` retains explicit hypotheses, evaluation contract,
      artifacts, validators, sandbox, retry budget, and stop conditions.
- [ ] `research-engineer` remains the implementation/experiment workflow.
- [ ] The canonical ledger stays at
      `docs/research/decisions/ledger.yaml`; old ledgers remain valid.

### Roles and models

- [ ] Exactly eight fixed Coresearch roles exist on each provider.
- [ ] Every role uses the exact model and effort in section 5.
- [ ] No role uses a rolling alias, `inherit`, or an unspecified effort.
- [ ] Native definitions match `agents/manifest.json` exactly.
- [ ] Read-only and writable tool boundaries match the role matrix.
- [ ] Strict doctor detects Claude environment override risk.
- [ ] Explicit runtime probes report requested and observed models and do not
      label unobservable routing as verified.

### Execution

- [ ] Codex `/goal` references a host-neutral mission rather than embedding or
      recreating the research workflow.
- [ ] Claude Code consumes the same mission/sandbox/result contract.
- [ ] Every durable run has a terminal `result.json` with routing provenance,
      artifacts, validators, and stop reason.
- [ ] A claim-bearing completion receives independent verification.

### Design documentation

- [ ] Root `DESIGN.md` is the canonical structural overview and is linked from
      README and root AGENTS.
- [ ] It documents purpose, invariants, repository ownership, control flow,
      skills, roles, host adapters, state, installation, safety, extension, and
      lifecycle.
- [ ] It contains component, durable-run sequence, and installation-topology
      diagrams.
- [ ] It links to authoritative manifests/contracts rather than becoming a
      competing source of truth.
- [ ] All local links resolve and any repeated machine-readable facts are
      covered by drift validation.

### Installation and safety

- [ ] User/project and copy/symlink installation work for Codex, Claude, and
      both.
- [ ] Skills and native roles are both installed, reported, repaired, and
      validated.
- [ ] Unrelated user skills, agents, and AGENTS files are not overwritten.
- [ ] Bridge/full-template changes retain dry-run, backup, idempotency, and
      rollback behavior.
- [ ] Ordinary install/init/doctor/validate behavior is identical with or
      without an `omx` executable on `PATH`.

### Zero-OMX active surface

- [ ] No active skill, role, manifest, template, installer, harness path, or
      runtime validation calls or depends on OMX.
- [ ] No `.omx` runtime state or OMX marker is produced.
- [ ] OMX is mentioned only in explicitly historical migration documentation.
- [ ] `.codex-plugin/plugin.json` has no OMX keyword or compatibility promise.

### Verification and repository hygiene

- [ ] `./scripts/validate.sh` reports PASS and exits 0.
- [ ] `./harness doctor --strict` exits 0 in the validated install fixture.
- [ ] `git diff --check` passes.
- [ ] No new third-party dependency is added.
- [ ] No cache, `.tmp`, run output, `.omx`, or `.agents` state artifact is
      staged.
- [ ] Untracked `PROMPT.md` and `PROMPT(1).md` are unchanged.
- [ ] Final report lists changed files, affected install surfaces, exact
      validation results, routing-probe status, and any remaining manual reload
      step.

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Research behavior is accidentally deleted with OMX wording | Lock the 15-skill set and research/ledger contracts before edits; change one surface at a time |
| Provider definitions drift | Canonical `agents/manifest.json` plus exact validation against all native files |
| Claude silently substitutes a blocked model | Detect environment override, forbid per-call overrides, add explicit observed-model probes, never call static-only routing verified |
| Luna is assigned an underspecified or complex task | Require bounded scope; escalate planning to planner and repeated failures to debugger |
| `/goal` becomes a second research router | Mission references Coresearch contracts; goal owns continuation only; every terminal result re-enters `coresearch` |
| Parallel agents conflict on files or invalidate experiments | Owned scopes, minimal concurrency, no parallel mutation of the same experiment, verifier at claim boundary |
| Installer overwrites user-owned agents | Recognized Coresearch ownership checks, dry-run where applicable, `--force` only for explicit replacement |
| Shell and Python installers diverge | Make Python harness canonical and keep shell entry points thin |
| Active OMX references survive in obscure docs/tests | Banned-reference regression with explicit historical exclusions plus final manual classification |
| `DESIGN.md` drifts into a stale second specification | Keep executable facts in manifests/contracts, validate links and repeated tables, and require design updates for boundary changes |
| Existing users still have a separate OMX installation | Do not uninstall or mutate third-party OMX state; make Coresearch operation independent of it |
| Current pinned models are unavailable to an account | Strict doctor reports unavailable/mismatch; update pins only through an explicit reviewed manifest change |

## 11. Rollback Strategy

1. Implement in reviewable phases matching section 8; do not combine role,
   skill, harness, and documentation changes into one opaque rewrite.
2. Preserve existing AGENTS bridge/full-template backups and rollback commands.
3. Never delete or modify a user's separate OMX installation or global prompt
   outside Coresearch's marker-bounded block.
4. If native role installation fails, roll back the role/harness phase while
   retaining the unchanged research skills.
5. If goal/run integration fails, revert only the new adapter/run-contract
   phase; the canonical ledger and original research contracts must remain
   readable.
6. Do not use destructive Git reset/checkout operations. Revert through small
   patches or commits.

## 12. Codex CLI Handoff

From the repository root, start Codex CLI and submit this goal:

```text
/goal Implement docs/plans/remove-omx-migration.md exactly. Preserve the dirty
worktree and do not edit, add, delete, or stage PROMPT.md or PROMPT(1).md. Work
phase-by-phase, adding regression checks before changing behavior. Keep all 15
Coresearch research skills and the canonical ledger contract. Replace OMX with
the eight fixed native roles and exact model/effort pins in the plan. Use the
host-neutral mission/result contract and Codex /goal adapter; do not recreate
an OMX-like workflow engine. Create the canonical root DESIGN.md required by
phase 5 and keep executable facts in their manifests/contracts. Run targeted
checks after each phase and the full scripts/validate.sh plus harness doctor
--strict at the end. Stop only when all
section 9 acceptance criteria pass, or record a concrete blocker with evidence.
```

The implementation agent may use native subagents for independent bounded
inspection, implementation, and verification slices. It must not invoke OMX,
an OMX skill, or an OMX team/runtime mode while performing this migration.

## 13. Completion Report Contract

The Codex CLI implementation must finish with:

- files added, changed, renamed, and removed;
- which surfaces changed: skills, Codex roles, Claude roles, project template,
  global/project bridge, harness, plugin metadata, `DESIGN.md`, and user
  documentation;
- exact requested model/effort matrix installed;
- validation commands with exact PASS/FAIL exit status;
- live routing-probe result or a clear statement that routing remains
  `static-only` and therefore is not runtime-verified;
- confirmation that no active OMX dependency/reference remains;
- confirmation that the two untracked prompt examples were untouched;
- remaining risks or manual step, including restarting Codex/Claude Code to
  reload skill and agent metadata.
