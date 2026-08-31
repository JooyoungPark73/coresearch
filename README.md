# Coresearch

Coresearch is a standalone research-agent bundle for Codex and Claude Code. It
installs fifteen complete research skills, eight fixed native roles per
provider, a host-neutral durable-run contract, and safe project/global prompt
bridges. It adds no third-party dependency and does not replace unrelated
skills, roles, or prompt content.

See [`DESIGN.md`](DESIGN.md) for architecture, boundaries, control flow, state,
and single-source ownership.

## Repository surfaces

| Path | Purpose | Installed destination |
|---|---|---|
| `skills/*/SKILL.md` | Complete research skills and central router | User or project `skills/` for either provider |
| `skills/manifest.json` | Exact 15-skill inventory | Harness and validation input |
| `agents/manifest.json` | Exact roles, capabilities, models, and efforts | Harness and validation input |
| `agents/codex/*.toml` | Codex-native role definitions | `${CODEX_HOME:-~/.codex}/agents` or `<project>/.codex/agents` |
| `agents/claude/*.md` | Claude Code-native role definitions | `${CLAUDE_HOME:-~/.claude}/agents` or `<project>/.claude/agents` |
| `templates/research/AGENTS.md` | Full research-project contract | Project `AGENTS.md` through explicit initialization |
| `scripts/harness.py` | Canonical install, status, doctor, repair, and prompt logic | Invoked by `harness` and thin wrappers |
| `.codex-plugin/plugin.json` | Skill-only plugin package metadata | Plugin loader; native roles remain harness-installed |

The root `AGENTS.md` is development guidance for this repository, not the
template installed into research projects.

## Fixed role and model matrix

[`agents/manifest.json`](agents/manifest.json) is authoritative. Native files
repeat these exact pins because each host requires them.

| Role | Codex model / effort | Claude model / effort |
|---|---|---|
| `coresearch-planner` | `gpt-5.6-sol` / `xhigh` | `claude-opus-5` / `xhigh` |
| `coresearch-researcher` | `gpt-5.6-terra` / `high` | `claude-sonnet-5` / `high` |
| `coresearch-reader` | `gpt-5.6-luna` / `low` | `claude-haiku-4-5-20251001` / `low` |
| `coresearch-implementer` | `gpt-5.6-luna` / `medium` | `claude-haiku-4-5-20251001` / `medium` |
| `coresearch-experimenter` | `gpt-5.6-luna` / `medium` | `claude-haiku-4-5-20251001` / `medium` |
| `coresearch-debugger` | `gpt-5.6-sol` / `high` | `claude-opus-5` / `high` |
| `coresearch-synthesizer` | `gpt-5.6-sol` / `low` | `claude-opus-5` / `low` |
| `coresearch-verifier` | `gpt-5.6-sol` / `xhigh` | `claude-opus-5` / `xhigh` |

Rolling provider aliases and inherited or unspecified effort are rejected.
Coresearch instructions do not pass a per-invocation model override.
The Luna/Haiku implementer handles mechanically clear, decomposed slices;
complex integrated implementation stays with the frontier parent. The
Sol/Opus-low synthesizer consolidates already-resolved evidence; unresolved
causal or dialectical reconciliation also stays with the frontier parent.

## Recommended development install

From this repository:

```bash
./harness self-install
harness link --surface both
harness doctor --strict --surface both
```

This creates user-scope symlinks:

```text
${CODEX_HOME:-~/.codex}/skills/<skill>   -> <repo>/skills/<skill>
${CODEX_HOME:-~/.codex}/agents/<role>.toml -> <repo>/agents/codex/<role>.toml
${CLAUDE_HOME:-~/.claude}/skills/<skill> -> <repo>/skills/<skill>
${CLAUDE_HOME:-~/.claude}/agents/<role>.md -> <repo>/agents/claude/<role>.md
```

Local edits then appear immediately through the symlinks. Restart Codex and
Claude Code after installation to reload skill and role metadata.

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
`--mode copy|symlink` options apply to skills and roles.

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

Project destinations are `<project>/.codex/{skills,agents}` and
`<project>/.claude/{skills,agents}`. The harness replaces only recognized
Coresearch copies or links. A same-name unrelated entry is preserved and
reported; `--force` is required for an intentional replacement.

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
- manifest parity for every name, model, effort, capability, and skill list;
- read-only versus workspace-write boundaries;
- installed role configuration and link health;
- that `CLAUDE_CODE_SUBAGENT_MODEL` is unset during the audit.

Static success does not prove which model a host actually used. When installed
CLIs, credentials, network, token budget, and host metadata support a live
audit, run:

```bash
harness doctor --strict --surface both --probe-models
```

This explicit command invokes every named fixed role without passing a model or
effort override and reports. It may make eight host calls per selected surface;
each role probe has a 120-second timeout.

- `verified` — observed role, model, and effort metadata match the manifest;
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

The fifteen owned skills cover design, survey, durable loops, gaps,
dialectics, causal reasoning, engineering, qualitative analysis, writing,
review, rebuttal, verification, methodology audit, and adversarial evidence
review. Exact inventory lives in `skills/manifest.json`.

Primary field modes are Systems/Cloud (OSDI, SOSP, NSDI, EuroSys, SoCC), ML
Systems (MLSys), and Computer Architecture/Workload Characterization (ISCA,
MICRO, HPCA, IISWC), with an ASPLOS cross-layer lens.

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
