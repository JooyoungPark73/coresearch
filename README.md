# Coresearch for OMX

Coresearch is an installable research-agent bundle for Codex + oh-my-codex (OMX). It keeps the OMX global prompt intact, installs complete research skills, and can initialize individual research projects with a small bridge block or a full research `AGENTS.md` template.

## What lives where

| Path | Purpose | Installed where? |
|---|---|---|
| `AGENTS.md` | Development prompt for maintaining this Coresearch bundle | No |
| `templates/research/AGENTS.md` | Full research-project prompt template | Copied by `harness init --full` |
| `skills/*/SKILL.md` | Complete research skills | Symlinked/copied into `${CODEX_HOME:-~/.codex}/skills`, `${CLAUDE_HOME:-~/.claude}/skills`, or project `.codex/.claude` skill dirs |
| `skills/manifest.json` | Coresearch-owned skills and optional external OMX acceleration routes | Used by harness/validation |
| `harness`, `bin/harness`, `scripts/harness.py` | CLI for install/init/status/diff/rollback/repair/update | `harness self-install` symlinks command into `~/.local/bin` |

The root `AGENTS.md` is intentionally **not** the template installed into other projects. It is only for editing this bundle.

## Recommended install

Run this from the Coresearch repo:

```bash
cd /path/to/coresearch
./harness self-install
harness link --surface both
harness doctor --strict
```

This installs the Coresearch command plus user-level skill surfaces:

- `~/.local/bin/harness` as a symlink to this repo's CLI;
- `${CODEX_HOME:-~/.codex}/skills/*` as symlinks to this repo's research skills;
- `${CLAUDE_HOME:-~/.claude}/skills/*` as symlinks when you use `harness link --surface both`.

It does **not** modify `${CODEX_HOME:-~/.codex}/AGENTS.md` unless you explicitly run `harness global -y`.
Use `coresearch` as the broad research router; use the role skills directly for narrow tasks.

Coresearch uses canonical names only: `coresearch` and `research-*` role skills. File-format output (`.pptx`/`.docx`/`.xlsx`/web) is produced by the user with external tools; Coresearch owns research content, not format mechanics. No shim aliases are installed or managed.

Primary research modes: Systems/Cloud (OSDI, SOSP, NSDI, EuroSys, SoCC), ML Systems (MLSys), Computer Architecture/Workload Characterization (ISCA, MICRO, HPCA, IISWC), and an ASPLOS cross-layer lens.

### 1. Install the `harness` command

```bash
./harness self-install
```

Default install path:

```text
${RESEARCH_HARNESS_BIN_DIR:-~/.local/bin}/harness
```

If `~/.local/bin` is on `PATH`, you can then run:

```bash
harness status
harness doctor
harness repair
harness update
```

Remove the installed command:

```bash
harness self-uninstall
```

### 2. Link global user skills so repo edits auto-update Codex/Claude skills

```bash
harness link --surface both
```

Equivalent:

```bash
./scripts/install.sh --scope user --surface both --mode symlink --force
```

This creates symlinks such as:

```text
~/.codex/skills/coresearch       -> ./skills/coresearch
~/.claude/skills/coresearch      -> ./skills/coresearch
~/.codex/skills/research-design  -> ./skills/research-design
~/.claude/skills/research-design -> ./skills/research-design
```

After this, edits in this repo's `skills/` directory are reflected in local Codex and Claude skill files. Restart Codex/OMX/Claude to refresh skill discovery metadata in an already-running session.

If you want a copy install instead of an auto-updating symlink install, use:

```bash
harness install --scope user --surface both
```

### 3. Keep global OMX prompt unchanged by default

Your global prompt should remain the OMX default:

```text
~/.codex/AGENTS.md
```

Check:

```bash
harness status
harness doctor --strict
```

If links or command shims drift, repair the local install without modifying the global prompt:

```bash
harness repair
```

If you want natural global routing into these research skills, add only the small bridge block:

```bash
harness global       # dry-run diff
harness global -y    # apply
```

Remove it later:

```bash
harness global --remove -y
```

This does **not** replace the OMX global prompt; it only updates a marker-bounded block:

```text
<!-- RESEARCH_AGENT_SKILLS:START -->
...
<!-- RESEARCH_AGENT_SKILLS:END -->
```

### Global skills vs. global AGENTS.md

These are separate:

| Surface | Command | Default behavior |
|---|---|---|
| Global user skills | `harness link --surface both` | Symlinks Coresearch skills into `~/.codex/skills` and `~/.claude/skills` |
| Global OMX prompt | `harness global -y` | Optional bridge only; never replaced by default |
| Project prompt | `harness init` | Adds bridge or full research prompt to one repo |

Recommended default:

```text
~/.codex/AGENTS.md       = OMX default
~/.codex/skills/*        = Coresearch skills symlinked by harness link --surface both
~/.claude/skills/*       = Coresearch skills symlinked by harness link --surface both
project/AGENTS.md        = bridge or full research prompt from harness init
```

## Project initialization

### Interactive wizard

For normal use, just run:

```bash
harness init
```

This opens a small built-in menu, similar to a dropdown. Bare `harness init`
runs the wizard **only in an interactive shell** (a real TTY on stdin); inside
the wizard, the default choices are the fast project-start path:

```text
target = .
mode   = full
action = apply
```

The wizard needs a TTY, so it does not run under piped stdin, `make`, or CI. In
those non-interactive contexts bare `harness init` falls back to a dry-run
`bridge` install for `.`. For scripts and CI, pass the intent explicitly instead
of piping answers:

```bash
harness init . --full -y      # apply the full research template
harness init . -y             # apply a bridge block
```

The wizard still prints a diff before writing, creates a backup when replacing an existing file, and refuses to replace an existing `AGENTS.md` in `full` mode unless replacement is explicitly allowed.

1. choose the target directory;
2. choose `bridge` or `full`;
3. choose dry-run preview or apply;
4. choose whether to replace an existing `AGENTS.md` when using `full`.

Force the same wizard even when passing a target:

```bash
harness init . --interactive
harness init . -i
```

No extra Python packages are required. In scripts or CI, use the explicit flags below; explicit target/mode forms remain dry-run unless `-y`/`--apply` is passed.

### Conservative project bridge

Use this for most research repos. It preserves any existing project `AGENTS.md` and adds a small research bridge block.

The bridge is **omx-conditional**: `harness init` applies the OMX-aware bridge when `omx` is detected on PATH; if `omx` is absent it skips the bridge (Coresearch runs standalone), notifies you, and — in an interactive terminal — offers to install `omx` (`oh-my-codex`, via npm/bun/your package manager). Pass `--bridge` to force the bridge regardless of omx.

```bash
cd /path/to/research-repo
harness init . --bridge      # dry-run diff
harness init . --bridge -y   # apply
```

Equivalent explicit form:

```bash
harness init /path/to/research-repo --bridge
harness init /path/to/research-repo --bridge -y
```

### Full research prompt template

Use this for a research-only repo where you want the full project prompt.

```bash
harness init /path/to/research-repo --full
harness init /path/to/research-repo --full -y
```

This copies:

```text
templates/research/AGENTS.md -> /path/to/research-repo/AGENTS.md
```

If the target already has `AGENTS.md`, full mode refuses to replace it unless you explicitly pass `--replace`:

```bash
harness init /path/to/research-repo --full --replace -y
```

Long-form compatibility remains available:

```bash
harness init /path/to/research-repo --mode full --apply
```

### Diff before writing

Explicit flag-based prompt writes are dry-run by default; the bare interactive wizard defaults to apply but still prints the diff before writing.

```bash
harness diff /path/to/research-repo --bridge
harness diff /path/to/research-repo --full
harness diff --global
```

### Rollback

Prompt writes create backups. Preview rollback:

```bash
harness rollback --scope project /path/to/research-repo
```

Apply rollback:

```bash
harness rollback --scope project /path/to/research-repo -y
```

Global rollback:

```bash
harness rollback --scope global
harness rollback --scope global -y
```

## How AGENTS.md execution works under OMX

When you run Codex/OMX in a project, instruction surfaces compose roughly like this:

1. **Global OMX prompt**: `${CODEX_HOME:-~/.codex}/AGENTS.md`
   - Should remain OMX default.
2. **Project prompt**: nearest `AGENTS.md` in the current directory tree.
   - Installed by `harness init --bridge` or `--full`.
3. **Skills**: `${CODEX_HOME:-~/.codex}/skills/*/SKILL.md` or project `.codex/skills/*/SKILL.md`.
   - Installed/linked by `harness link` or `harness install`.
4. **OMX runtime overlay**: runtime/team state appended by OMX marker contracts.

So the intended setup is:

- global `AGENTS.md`: OMX default;
- user skills: symlinked Coresearch skills;
- target research repo `AGENTS.md`: bridge or full research template;
- `.omx/`: only for explicit OMX runtime workflows.

## Harness command reference

```bash
harness status                         # show global/project/skill state
harness inventory --include-plugins    # audit Codex/Claude skill overlap, preferences, legacy symlinks
harness doctor --strict                # verify install health
harness repair                         # relink skills, reinstall command, validate, strict doctor
harness repair --surface both          # repair Codex + Claude skill links
harness link                           # symlink user-scope skills to this repo
harness link --surface both            # symlink to ~/.codex/skills and ~/.claude/skills
harness install --scope user           # copy user-scope skills
harness install --scope user --surface claude
harness install --scope project --project-dir . --project-bridge
harness self-install                   # install harness command into ~/.local/bin
harness self-uninstall                 # remove installed harness command
harness global                         # dry-run global bridge diff
harness global -y                      # apply global bridge
harness global --remove -y             # remove global bridge
harness init                           # interactive wizard (TTY only); defaults to . / full / apply
harness init .                         # dry-run bridge install for explicit target
harness init . --interactive           # force wizard for a target; defaults to full/apply
harness init . -y                      # apply bridge to current dir
harness init . --full -y               # apply full research template
harness diff . --full
harness diff --global
harness rollback --scope project . -y
harness update                         # relink skills and validate
harness update --pull                  # git pull --ff-only, relink, validate
```

## Validation

Run the full local validation harness:

```bash
./scripts/validate.sh
```

It checks:

- plugin JSON parsing;
- Python and shell script syntax without leaving `__pycache__`;
- broken symlinks in this repo;
- stray carriage-return characters in markdown, Python, shell, JSON, and wrapper files;
- skill frontmatter and expected skill catalog;
- OMX marker contracts in `templates/research/AGENTS.md`;
- systems/cloud, ML-systems, architecture/workload, and ASPLOS cross-layer venue contracts;
- synchronized research-contract/ledger modes and contribution enums;
- research-first guards that keep artifact correctness distinct from scientific evidence;
- root `AGENTS.md` remains bundle-development guidance, not the installable research template;
- research-survey crawler safety flags and dry-run behavior;
- user copy install and bridge idempotency;
- user symlink install for repo-auto-update;
- no legacy shim aliases are installed;
- `harness install` user/project wrapper behavior;
- `harness link/status`;
- `harness self-install/self-uninstall`;
- `harness global` dry/apply/remove;
- `harness doctor --strict`;
- `harness doctor` failure on broken skill symlinks;
- `harness repair` relink/self-install/strict-doctor path;
- `harness update` relink;
- `harness init` interactive, positional/flag target, bridge/full/rollback behavior;
- project install behavior;
- OMX availability.

## Policy

- Do not overwrite the global OMX prompt by default.
- Do not create `.agents/` chats, mailboxes, or paper-state forests.
- Use `.omx/` only for explicit OMX workflows, hooks, recovery, or checkpointing.
- Prefer bridge mode for existing projects and full mode for research-only projects.
