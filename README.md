# Coresearch

Coresearch is a standalone research-agent bundle for Codex and Claude Code. It
installs nine focused research skills, eight fixed native roles per
provider, a host-neutral durable-run contract, and safe project/global prompt
bridges. It adds no third-party dependency and does not replace unrelated
skills, roles, or prompt content.

See [`DESIGN.md`](DESIGN.md) for architecture, boundaries, control flow, state,
and single-source ownership.

## Repository surfaces

| Path | Purpose | Installed destination |
|---|---|---|
| `skills/*/SKILL.md` | Complete research skills and central router | Codex `.agents/skills`; Claude `.claude/skills` |
| `skills/manifest.json` | Exact nine-skill inventory | Harness and validation input |
| `agents/manifest.json` | Exact roles, capabilities, models, and effort policies | Harness and validation input |
| `agents/codex/*.toml` | Codex-native role definitions | `${CODEX_HOME:-~/.codex}/agents` or `<project>/.codex/agents` |
| `agents/claude/*.md` | Claude Code-native role definitions | `${CLAUDE_CONFIG_DIR:-~/.claude}/agents` or `<project>/.claude/agents` |
| `templates/research/AGENTS.md` | Full research-project contract | Project `AGENTS.md` through explicit initialization |
| `scripts/harness.py` | Canonical install, status, doctor, repair, and prompt logic | Invoked by `harness` and thin wrappers |
| `.codex-plugin/plugin.json` | Skill-only plugin package metadata | Plugin loader; native roles remain harness-installed |

The root `AGENTS.md` is development guidance for this repository, not the
template installed into research projects.

## Fixed role and model matrix

[`agents/manifest.json`](agents/manifest.json) is the source authority. Native
files repeat model pins and implement each provider's effort policy. The harness
does not install the manifest under `.codex/agents`
or `.claude/agents`, and its absence there is not a registration failure.

| Role | Codex model / effort | Claude model / effort |
|---|---|---|
| `coresearch-planner` | `gpt-6-astra` / `assignment` | `claude-opus-5` / `xhigh` |
| `coresearch-researcher` | `gpt-6-astra` / `assignment` | `claude-sonnet-5` / `high` |
| `coresearch-reader` | `gpt-6-astra` / `assignment` | `claude-haiku-4-5-20251001` / `low` |
| `coresearch-implementer` | `gpt-6-astra` / `assignment` | `claude-haiku-4-5-20251001` / `medium` |
| `coresearch-experimenter` | `gpt-6-astra` / `assignment` | `claude-haiku-4-5-20251001` / `medium` |
| `coresearch-debugger` | `gpt-6-astra` / `assignment` | `claude-opus-5` / `high` |
| `coresearch-synthesizer` | `gpt-6-astra` / `assignment` | `claude-opus-5` / `low` |
| `coresearch-verifier` | `gpt-6-astra` / `assignment` | `claude-opus-5` / `xhigh` |

All eight Codex roles use Astra. `assignment` means the parent explicitly
chooses effort for each task: `low` for extraction or resolved synthesis,
`medium` for bounded execution, `high` for difficult reasoning, and `xhigh` for
deeply branching planning or verification. These are complexity guidelines,
not fixed role defaults. See [assignment effort](skills/coresearch/references/agent-routing.md).
After updating this checkout, run `./harness link --surface codex` to refresh
installed role copies, then start a new Codex session to load them.

Rolling provider aliases are rejected. Codex role files omit effort overrides;
the parent must pass the chosen effort explicitly at spawn time. Claude retains
fixed efforts. Stale Codex role copies with fixed effort fail strict doctor.
Coresearch instructions do not pass a per-invocation model override.
The implementer handles mechanically clear, decomposed slices;
complex integrated implementation stays with the frontier parent. The
synthesizer consolidates already-resolved evidence; unresolved
conflicting evidence or mechanism choices stay with the frontier parent.

## Recommended development install

From this repository:

```bash
./harness self-install
harness link --surface both
harness doctor --strict --surface both
```

This creates user-scope skill symlinks and provider-native roles. Current Codex
requires role TOMLs to be regular files, so Codex roles are copied even in link
mode:

```text
~/.agents/skills/<skill>                   -> <repo>/skills/<skill>
${CODEX_HOME:-~/.codex}/agents/<role>.toml    copied regular file
${CLAUDE_CONFIG_DIR:-~/.claude}/skills/<skill> -> <repo>/skills/<skill>
${CLAUDE_CONFIG_DIR:-~/.claude}/agents/<role>.md -> <repo>/agents/claude/<role>.md
```

Local skill edits and Claude role edits then appear immediately through their
symlinks. Re-run `harness link --surface codex` after changing a Codex role so
its required regular-file copy is refreshed. Restart Codex and Claude Code
after installation to reload skill and role metadata.

For a copy install:

```bash
harness install --scope user --surface both --mode copy
```

The compatibility wrapper is equivalent:

```bash
./scripts/install.sh --scope user --surface both --mode copy
```

## Installation matrix

The same `--surface codex|claude|both`, `--scope user|project`, and
`--mode copy|symlink` options are accepted across providers. Codex roles retain
the regular-file copy exception described above.

```bash
# User Codex copy
harness install --scope user --surface codex --mode copy

# User Claude Code symlink
harness install --scope user --surface claude --mode symlink

# Project both-provider copy
harness install --scope project --surface both --mode copy \
  --project-dir /path/to/research-repo

# Project both-provider symlink
harness install --scope project --surface both --mode symlink \
  --project-dir /path/to/research-repo
```

Project destinations are `<project>/.agents/skills`,
`<project>/.codex/agents`, and `<project>/.claude/{skills,agents}`. Install at
the actual repository root. An umbrella directory that merely contains several
Git repositories is not inherited by those repositories; either use user scope
once or run the project install separately in each repository. The harness
warns when a project target is not a Git worktree.

The harness replaces only recognized Coresearch copies or links. A same-name
unrelated entry is preserved and reported; `--force` is required for an
intentional replacement. Codex role TOMLs are always regular copied files;
skill directories may use copy or symlink mode. Existing managed Coresearch
skills under the legacy
`.codex/skills` location and the retired managed role-registration block are
removed during a successful Codex install, while unrelated configuration is
preserved and backed up before a block removal.

Codex user skills are independent of `CODEX_HOME`; use
`--codex-skills-root` only for an explicit alternate or isolated test root.
Claude user configuration follows `CLAUDE_CONFIG_DIR` (default `~/.claude`);
`--claude-home` is the harness's explicit override.

The paths follow the official [Codex Skills discovery
rules](https://developers.openai.com/codex/skills) and [custom-agent discovery
rules](https://developers.openai.com/codex/multi-agent). Codex role copies also
avoid the host's explicit [rejection of symlinked custom-role
files](https://github.com/openai/codex/pull/39299).

## Project and global prompts

Prompt changes are separate from installing skills and roles.

### Marker-bounded project bridge

```bash
harness init /path/to/research-repo --bridge       # dry-run diff
harness init /path/to/research-repo --bridge -y    # apply
```

The bridge preserves existing content and updates only:

```text
<!-- RESEARCH_AGENT_SKILLS:START -->
...
<!-- RESEARCH_AGENT_SKILLS:END -->
```

The result is independent of unrelated executables on `PATH`.

### Full project template

```bash
harness init /path/to/research-repo --full         # dry-run
harness init /path/to/research-repo --full -y      # apply when absent
harness init /path/to/research-repo --full --replace -y
```

Full mode copies `templates/research/AGENTS.md`. It refuses to replace an
existing file unless `--replace` is explicit. Bare `harness init` opens the
interactive wizard only on a TTY; explicit commands remain deterministic and
dry-run unless `-y` is supplied.

### Optional global bridge

```bash
harness global                  # dry-run diff
harness global -y               # apply
harness global --remove -y      # remove only the Coresearch block
```

Global and project writes create bounded backups. Preview and apply rollback:

```bash
harness rollback --scope project /path/to/research-repo
harness rollback --scope project /path/to/research-repo -y
harness rollback --scope global
harness rollback --scope global -y
```

## Harness commands

```bash
harness status                         # skills, roles, prompts, requested pins
harness inventory --include-plugins    # Coresearch ownership and overlap audit
harness doctor --strict                # static source + installed Codex audit
harness doctor --strict --surface both # static + both installed providers
harness repair --surface both          # relink, validate, strict doctor
harness update --surface both          # relink and validate
harness self-install                   # link command into ~/.local/bin
harness self-uninstall                 # remove only this repo's command link
```

`repair` restores recognized broken Coresearch entries while preserving
unrelated entries. It honors `--scope`, `--mode`, and `--surface`; pass the
project path positionally for project repair. `update` honors the same install
options and uses the current directory for project scope. `status` and
`inventory` report skills and roles separately, including requested model and
effort.

## Static and live routing verification

Ordinary strict doctor is local and static. It verifies:

- exactly eight source roles and sixteen native definitions;
- manifest parity for every name, model, effort policy, capability, and skill list;
- read-only versus workspace-write boundaries;
- installed role configuration and link health;
- documented Codex and Claude discovery roots;
- regular-file enforcement for Codex role TOMLs;
- that `CLAUDE_CODE_SUBAGENT_MODEL` is unset during the audit.

Static success does not prove which model a host actually used. When installed
CLIs, credentials, network, token budget, and host metadata support a live
audit, run:

```bash
harness doctor --strict --surface both --probe-models
harness doctor --strict --surface codex --probe-models \
  --probe-role coresearch-reader
```

This explicit command invokes each named role without a model override. Codex
probes explicitly request `low` effort for their simple diagnostic assignment;
Claude probes retain configured effort. `--probe-role` limits a diagnostic run to one role.
Codex probes are ephemeral, use the doctor target as their project root, and do
not depend on the shell's starting directory. A full probe may make eight host
calls per selected surface; each role probe has a 120-second timeout. Bounded
host errors such as an unavailable agent type are included in failures.

- `verified` — observed role, model, and effort metadata match the requested assignment, with the model pinned by the manifest;
- `static-only` — the host or CLI does not expose all three observed values;
- `mismatch` — the role is missing or a role/model/effort is blocked,
  substituted, unavailable, or different.

An explicit probe that is unobservable or mismatched returns nonzero. Runtime
probes never run during ordinary validation.

## Research routing

Use `coresearch` for broad requests. It selects one primary skill, zero or more
bounded fixed-role assignments, and one host adapter. Each assignment has one
role; independent assignments may run concurrently under parent-owned
dependency joins and integration. Every terminal role or run returns to the
parent and re-enters `coresearch` before the next research stage.

The nine owned skills are `coresearch`, design, survey, durable loop,
engineering, writing, review, verification, and explicit-only qualitative
synthesis. Narrow analyses are modes: design owns gap and causal-hypothesis
planning; survey owns conflict synthesis; review owns responses; verification
owns factual, methodology, adversarial, and causal audits. Detailed mode
contracts load only when selected. Exact inventory lives in
`skills/manifest.json`.

Skill descriptions stay short for discovery. Entrypoints provide scope decisions
and essential research constraints; full paper plans, venue assessments, and
specialized audits load their references only when needed. Narrow requests stay
narrow, and authorized multi-stage work continues through applicable validation
without pausing for approval at each stage handoff.

Primary field modes are Systems/Cloud (OSDI, SOSP, NSDI, EuroSys, SoCC), ML
Systems (MLSys), and Computer Architecture/Workload Characterization (ISCA,
MICRO, HPCA, IISWC), with an ASPLOS cross-layer lens.

### Hierarchical manuscript writing

`research-write` keeps supplied-excerpt rewrites local and text-first, while
whole-paper or semantic-change requests can progressively inspect the coherent
payload, claim dependencies, section promises, and affected passages. Its
optional manuscript map references canonical claim/evidence IDs; it is
transient by default and may become a declared artifact of an existing durable
run. It does not create a second ledger or provider-specific writing state,
and score forecasting remains owned by `research-review`.

```text
$research-write Rewrite this evaluation section while preserving every number
and qualification.
```

```text
$research-write Build a hierarchical argument and section plan from these
approved claims and evidence records.
```

```text
$research-write Reconcile this reviewer comment across the abstract,
contributions, evaluation claims, and conclusion.
```

## Durable run contract

`research-loop` creates or updates:

```text
docs/research/runs/<run-id>/mission.md
docs/research/runs/<run-id>/sandbox.md
docs/research/runs/<run-id>/result.json
```

The canonical research ledger remains:

```text
docs/research/decisions/ledger.yaml
```

This path is relative to the research project, not the installed bundle. The
first durable or multi-stage run initializes it locally when absent; ordinary
in-chat work does not. Existing ledgers are read and merged, never replaced.

For Codex, use a goal only when the run is multi-turn, experiment-bearing, or
validator-bearing:

```text
/goal Execute docs/research/runs/<run-id>/mission.md within sandbox.md. Keep
docs/research/decisions/ledger.yaml current. Stop only after result.json has a
terminal status and every required validator has evidence, or when a declared
blocked/failure/human-decision condition is reached.
```

For Claude Code, give the main session the same mission and sandbox paths. It
uses the installed fixed roles and writes the same terminal `result.json`. No
second ledger or emulated goal surface is created.

New results use schema version 2. Top-level fields describe the whole run, and
`role_runs` records every attempted assignment with requested routing, observed
routing when available, artifacts, validators, and stop reason. Historical
schema-version-1 zero- or one-role results remain valid. Claim-bearing
completion requires an independent `coresearch-verifier` entry after writable
artifacts are integrated.

## Plugin packaging

`.codex-plugin/plugin.json` packages `./skills/` only. Native roles are
installed by the harness because the plugin manifest does not declare an
unverified agent field.

## Validation

Run the complete local suite:

```bash
./scripts/validate.sh
```

It validates structure, all role pins and capabilities, zero active runtime
coupling, copy/symlink installation across user/project and both providers,
prompt backup/rollback safety, durable research contracts, documentation drift,
and strict doctor failures for wrong or missing routing data.

Final repository gates:

```bash
./scripts/validate.sh
./harness doctor --strict
git diff --check
```

Full validation logs belong under ignored `.tmp/` scratch and should be
reported by exit code, duration, PASS/FAIL summary, and log path rather than
pasted in full.
