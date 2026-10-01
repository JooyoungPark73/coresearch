# Coresearch

An Astra-led research harness: one skill, on-demand research resources, and two
small utilities. Astra frames the problem, chooses the strategy, synthesizes
worker results, and verifies the deliverable. Native agents handle bounded work
when that helps. Coresearch does not run a second agent framework.

## Start

Use Python 3.10+; no packages or API keys are needed to install the skill.
Run from this checkout and choose the host's skills directory:

```bash
# Codex, user-level linked install
python3 scripts/coresearch.py install --to "$HOME/.agents/skills" --link

# Claude Code, user-level linked install
python3 scripts/coresearch.py install --to "$HOME/.claude/skills" --link
```

For one project, use `/path/to/project/.agents/skills` (Codex) or
`/path/to/project/.claude/skills` (Claude Code) instead. Omit `--link` for a
self-contained copy. The destination argument is the **skills directory**, not
its `coresearch` child. Paths follow the current
[Codex](https://developers.openai.com/codex/skills) and
[Claude Code](https://code.claude.com/docs/en/skills) discovery interfaces.

Reload the host's skill discovery as needed and request, for example:

> Use Coresearch to assess this research idea, implement the most informative
> feasible experiment, and review what the results actually support.

Select Astra as the sole lead in a host that supports it. Installation does not
select models, provision workers, or grant tool permissions.
The native Codex plugin manifest is also retained; choose plugin distribution or
manual installation, not duplicate installations of the same skill.

Neither installation nor research work requires changing global or project
`AGENTS.md` / `CLAUDE.md`. No OMX installation is needed.

## What the skill adds

Only its name and short description need discovery. The loaded
[skill](skills/coresearch/SKILL.md) establishes lead ownership and exposes six
independent resources, not a pipeline:

| Resource | Research capability |
|---|---|
| [Literature](skills/coresearch/references/literature.md) | Source-grounded synthesis, closest work, citation provenance, optional PDF collection |
| [Experiments](skills/coresearch/references/experiments.md) | Contribution design, falsifiers, baselines, executable evaluation, reproducible artifacts |
| [Engineering](skills/coresearch/references/engineering.md) | SOLID/DDD, research-code maturity, architectural decisions, executable contracts, reliable execution |
| [Analysis](skills/coresearch/references/analysis.md) | Gaps, contradictory findings, causal explanations, measurement analysis, evidence-chain audits |
| [Manuscripts](skills/coresearch/references/manuscripts.md) | Writing, figures/slides, venue critique, rebuttal, verification, release |
| [Delegation](skills/coresearch/references/delegation.md) | Coarse assignments, event-driven handoffs, and native workers, including Sol and Claude Code |

Astra owns consequential decisions and final interpretation. Workers own a clear
scope, relevant inputs, an expected artifact, and completion criteria. The host
supplies execution, permissions, and completion events. No model registry,
polling service, mandatory reviewer chain, or transcript ingestion is added.

## Lead ownership without constant check-ins

Keep Astra on problem framing, consequential decisions, difficult coupled work,
and final synthesis. Delegate self-contained work to a capable configured worker,
including GPT-6.1 Sol when appropriate. Workers own local execution and validation;
they do not need the lead's approval after each step. Completion, blockers, and
material decision changes justify communication. Routine progress polling does not.
The host owns telemetry, task supervision, permissions, and completion delivery.

Evaluate whether delegation helps the task.
Compare direct Astra, direct Sol, and selective delegation on the same research
and engineering tasks. See the [decision rationale](docs/architecture.md) and
[host evaluation protocol](docs/validation.md). Model selection and heterogeneous
workers remain host capabilities, not features installed by this skill.

An optional [personal instruction example](examples/astra-AGENTS.md) captures
cross-project research and engineering expectations in English. It is outside the
installable payload, is never imported automatically, and does not replace this
repository's maintenance `AGENTS.md`. Adapt only what your host and projects need;
skill use does not require installing this example or loading it into workers.

## Optional project continuity

Small tasks run directly. Longer projects can reuse their existing notes or
create a brief:

```bash
python3 scripts/coresearch.py init /path/to/project --question "What would distinguish these explanations?"
```

This creates only `research/brief.md`, never overwrites an existing brief, and
never injects instructions into the project. Keep decisions and evidence paths
there when useful; it is ordinary Markdown, not a required state schema.
Both `install` and `init` apply explicitly requested writes without a wizard.
Add `--dry-run` to preview without writing.

## Optional source collection

The agent uses its search tools to resolve paper identities and direct open-access
HTTPS URLs. The downloader does not guess bibliographic matches or verify claims.
Prepare a JSON array with `id`, `title`, `url`, and `access: "open"`; see the
[placeholder example](examples/sources.json) and the
[input/output contract](skills/coresearch/references/literature.md).

```bash
python3 skills/coresearch/scripts/fetch_sources.py sources.json --output research/pdfs --dry-run
python3 skills/coresearch/scripts/fetch_sources.py sources.json --output research/pdfs
```

The real run requires a new output directory. It writes downloaded PDFs and a
`report.json` with source metadata, outcomes, requested/final URLs, timestamps,
byte counts, and SHA-256 hashes. Downloads are not marked as read or verified.
Exit codes: `0` success, `1` partial retrieval failure, `2` invalid configuration
or output, `130` interruption. Completed sources survive a later failure.

Only public HTTPS endpoints are allowed, with IP-pinned TLS, redirect checks,
byte limits, and socket timeouts. There is no proxy support, credential forwarding,
paywall bypass, publisher scraping, fuzzy title resolver, or automatic retry.
This checks transport and a PDF signature, not scientific identity or validity.

## Updating and removal

A linked installation follows the checkout. Review and update it through normal
Git operations. An identical copy or identical link is a no-op; a conflicting,
modified, or broken destination is preserved with an error. To replace a copy,
move the existing `coresearch` directory aside for review, then install again.
Removal is ordinary removal of that installed directory or symlink. No global
prompt or host configuration needs restoring.

Version 2 intentionally removes the old `harness` command, prompt bridges,
full-project prompt, role skills, and OMX routing. Existing installations are not
silently cleaned on other machines. See [migration and decisions](docs/architecture.md)
before upgrading an old installation.

## Development and validation

```bash
python3 -B -m unittest discover -s tests -v
```

Tests exercise installation, copied-skill portability, optional initialization,
source transport/security boundaries, partial results, and repository structure.
They need no external network, account, or model. CI runs the same command.
[Validation and host scenarios](docs/validation.md) distinguish tested software
contracts from live model behavior that requires a configured host.

The design follows OpenAI's
[Astra skill and prompt guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra):
remove inferred workflow machinery, disclose resources when needed, and define
real decision boundaries and completion rather than reasoning recipes.
