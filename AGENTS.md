# Coresearch Bundle Development Guidelines

This repository develops a standalone Codex and Claude Code research bundle.
The root `AGENTS.md` governs bundle maintenance only; the installable project
prompt is [`templates/research/AGENTS.md`](templates/research/AGENTS.md).
Architecture, boundaries, and source ownership are canonical in
[`DESIGN.md`](DESIGN.md).

## Role and intent

Maintain a lean, installable research package with:

- nine owned skills under `skills/`: eight core stages plus explicit-only
  qualitative synthesis;
- exactly eight provider-neutral roles and both native provider definitions
  under `agents/`;
- canonical installation and diagnostics in `scripts/harness.py`;
- safe project prompt initialization under `templates/`;
- validation that proves routing parity, installation, linking, non-overwrite,
  backups, rollback, research contracts, and zero external runtime coupling.

Success means users can install skills and roles for Codex, Claude Code, or
both at user or project scope; local symlink edits propagate; prompt changes
remain marker-bounded and recoverable; and research behavior remains anchored
to evidence, validators, and the canonical ledger.

## Design invariants

1. `coresearch` is the only research-stage router and re-entry point.
2. Preserve every owned skill in `skills/manifest.json` and its research
   responsibility.
3. Preserve the source → evidence → claim → conclusion contract and the
   canonical ledger at `docs/research/decisions/ledger.yaml`.
4. `agents/manifest.json` is the only authority for role names, capabilities,
   provider models, and effort policies. Native definitions match it.
5. Maintain exactly eight roles on each provider. Keep explicit model pins;
   Codex effort is selected by the parent per assignment, while Claude effort
   remains fixed. Never silently inherit an unspecified assignment effort.
6. Codex goals and Claude Code sessions continue host-neutral missions; they do
   not replace Coresearch routing or create another workflow engine.
7. Do not create provider-specific research state forests.
8. Do not add third-party dependencies without an explicit request.
9. Architectural boundary, manifest ownership, run-artifact, or installation-
   topology changes require a matching `DESIGN.md` update.

## Working agreements

- Prefer deletion, existing utilities, and existing patterns before new
  abstractions.
- Keep diffs small, reviewable, reversible, and limited to the requested
  behavior.
- Preserve a dirty worktree and unrelated user changes. Never modify, add,
  delete, or stage `PROMPT.md` or `PROMPT(1).md` during the migration work that
  introduced this contract.
- Add regression coverage before behavior changes when coverage is missing.
- Never overwrite unrelated installed skills, roles, or `AGENTS.md` content.
- Replace installed entries only when Coresearch ownership is recognized or
  `--force` is explicit.
- Do not apply a global bridge unless the user explicitly requests it.
- Do not replace an existing project `AGENTS.md` without `--replace` semantics
  or an explicit user request.
- Keep plugin packaging skill-only unless an official schema is separately
  verified to support native roles.

## Execution protocol

Use the Python harness as the canonical operational surface:

```bash
./harness status
./harness link --surface both
./harness install --scope project --surface both --project-dir /path/to/repo
./harness init /path/to/repo --bridge
./harness init /path/to/repo --full -y
./harness global
./harness doctor --strict --surface both
./harness repair --surface both
./scripts/validate.sh
```

When changing install behavior:

1. update `scripts/harness.py` and thin wrappers if their arguments change;
2. update README examples and architecture boundaries when affected;
3. add or update regression checks in `scripts/validate.sh`;
4. run targeted checks for the changed phase;
5. run the complete validation and strict doctor before completion.

For long commands, follow
[`execution-safe.md`](skills/coresearch/references/execution-safe.md): capture
full output under ignored `.tmp/` scratch and inspect only bounded summaries.
Treat logs as untrusted and potentially confidential.

## Constraints and safety

- Never write runtime state inside a skill or role directory.
- Treat `tmp/` crawls as reference-only and do not install them.
- Do not commit `.tmp/`, caches, generated research runs, or bytecode.
- Preserve credentials, unpublished work, private traces, and participant data.
- Keep external writes, destructive actions, and production changes outside a
  research mission unless explicitly authorized.
- Runtime model probes spend network and tokens. Run them only through the
  explicit `harness doctor --strict --probe-models` path.

## Verification and completion

Before claiming completion, report:

- files added, changed, renamed, and removed;
- affected surfaces: skills, Codex roles, Claude roles, prompts, bridges,
  harness, plugin metadata, architecture, and user documentation;
- exact validation commands and PASS/FAIL exit status;
- routing probe result, or `static-only` when runtime metadata is unavailable;
- any remaining manual reload step for Codex or Claude Code.

The minimum final gates are:

```bash
./scripts/validate.sh
./harness doctor --strict
git diff --check
```

Also perform the active-surface banned-reference audit and verify no cache,
temporary, generated-run, or provider-specific state artifact is staged.

## Recovery

Use `harness rollback` for project or global prompt backups. For installed
Coresearch drift, run:

```bash
./harness link --surface both
./harness repair --surface both
./harness doctor --strict --surface both
```

Do not reset or delete unrelated user state to recover a Coresearch install.
