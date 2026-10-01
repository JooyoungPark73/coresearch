# Claude workers from a Codex parent

Use this adapter for an authorized, bounded second opinion. Codex retains
research routing, dependency joins, integration, ledger updates, and final
decisions. The Claude process executes one existing native role and returns.
It cannot schedule another assignment or choose the next research stage.

Default triggers are consequential claim review (`coresearch-verifier`) and
diagnosis after repeated observed failures (`coresearch-debugger`). Explicit
assignments may use `coresearch-planner` for experiment criticism, or
`coresearch-reader` / `coresearch-researcher` for independent interpretation of
supplied local sources. This adapter has no web or shell tools; discovery and
reproduction requiring those tools return to the parent. Routine implementation,
experiment execution, and integration stay on Codex. Preserve the required
Sol scientific verification gate; Claude adds review without replacing it.

## Handoff

Declare Claude access, the local evidence scope, timeout and optional dollar cap, and the
reason for a second opinion in the assignment or mission sandbox. A provider
change sends the supplied context and files read by the worker to that provider;
the parent must apply the mission's confidentiality and external-call limits.
Give the reviewer the question, artifact, evidence, and criteria before the
parent's justification, so it can first form its own assessment. Model agreement
does not validate a claim.

Write an assignment JSON file outside installed skills and roles:

```json
{
  "assignment_id": "claim-review",
  "attempt_id": "claim-review-a1",
  "role": "coresearch-verifier",
  "primary_skill": "research-verify",
  "field_mode": "systems_cloud",
  "target": "Check whether the supplied evidence supports the throughput claim.",
  "inputs": ["docs/research/claim.md", "results/measurements.csv"],
  "read_only_scope": ["docs/research", "results"],
  "validator": "Identify supporting and contradicting evidence with exact locators.",
  "stop_condition": "Return after the bounded review; report missing evidence.",
  "requested_model": "claude-opus-5",
  "requested_effort": "xhigh",
  "reason": "Independent review of a consequential claim",
  "depends_on": [],
  "working_modes": {}
}
```

Copy the exact model and effort from the installed role. The values in this
example are illustrative pins, validated against the canonical role matrix by
maintenance checks. Never silently substitute an unavailable model. Inputs and
read-only scopes must exist under the selected project directory, and each
input must fall within a declared scope. Pass any active working modes.

## Invocation and installation

From the source checkout or installed harness:

```bash
harness claude-worker --project-dir /path/to/project \
  --assignment /path/to/project/.tmp/claim-review.json \
  --output /path/to/project/.tmp/claim-review-a1.json
```

Each attempt defaults to a 3600-second (one-hour) wall timeout and no dollar
cap. Use `--timeout SECONDS` to override the timeout and `--max-budget-usd USD`
only when an explicit dollar cap is wanted. Both explicit values must be finite
and positive. An omitted cap is recorded as `limits.max_budget_usd: null`;
the adapter omits Claude's budget flag. Subscription usage limits still apply.

Without the harness, locate the installed `coresearch` skill and invoke its
packaged runner using the same arguments:

```bash
python3 /path/to/installed/coresearch/scripts/claude_worker.py --help
```

Copy and symlink installs both include the runner. It uses only Python's
standard library and requires Claude Code with `--restricted` support
(documented in v2.1.248+), authentication already configured, and native Claude
roles installed. Claude remains optional for ordinary Codex use. The runner
checks CLI support without a model call; incompatible hosts produce a blocked
record. It never installs roles or changes global settings automatically.

Discovery uses `<project>/.claude/agents/` first, then
`${CLAUDE_CONFIG_DIR:-~/.claude}/agents/`; `--claude-home` overrides the user root.
By default, the child preserves `CLAUDE_CONFIG_DIR` exactly, including its unset
state. Explicit `--claude-home` also sets the child's config directory to that
resolved path and can select a different credential store; it is not just a
role-search override.
Duplicate matching names within a scope are rejected. An unrelated or invalid
project definition blocks execution rather than falling through to a user role.
The selected Coresearch-owned definition must match the requested pins and
support the primary skill. Its content is snapshotted into `--agents` and
selected with `--agent`, so ancestor and plugin role discovery cannot silently
choose another definition. The snapshot retains native instructions, skills,
model and effort, and narrows tools and permission mode for this invocation.
Native files and the source manifest are never modified by a worker call.

## Authentication from a sandboxed parent

Before launching a worker, check `claude auth status` in the same environment
and credential context intended for the worker. This check does not call a
model. Keep raw authentication output private; report only the relevant status.
On macOS, an authenticated terminal can coexist with a sandboxed process that
reports `Not logged in` because it cannot access the credential store.

When sandbox authentication fails, use the parent's supported approval path to
check authentication outside the sandbox (in Codex's exec tool, request
`sandbox_permissions: "require_escalated"` when available). If that check
succeeds, launch the adapter through the same host-approved execution mode.
Reuse that confirmed mode within the session while the credential context and
host authorization remain applicable. Keep the worker restrictions below.
The Python adapter cannot grant itself permissions or escape its parent sandbox.

If escalation is denied or unavailable, report that boundary and preserve the
failure logs. Recommend `/login` only if authentication also fails in a context
that can access the user's credentials. Do not copy credentials or config into
the project or temporary directories, change global permissions, or silently
switch authentication providers. A failed worker remains a recorded attempt;
any authorized retry uses a fresh attempt ID and output path.

## Execution boundary

- Assignment content goes through stdin; subprocess arguments are not shell code.
- Available tools are only `Read`, `Glob`, and `Grep`. Shell, writes, web tools,
  skill invocation, and recursive delegation are unavailable.
- `--restricted` confines file tools to the working directory and excludes user
  and project settings. `dontAsk` denies permission requests without prompting.
- The adapter disables configurable hooks, supplies an empty strict MCP
  configuration, and disables session persistence. Organization-managed policy
  still applies; this is not an OS sandbox or a bypass of host policy.
- The project directory is the enforced file boundary. Narrower
  `read_only_scope` entries are assignment instructions, not filesystem ACLs.
  For stronger separation, prepare a dedicated directory with approved evidence.
- Model/effort environment overrides are rejected. No automatic fallback or
  retry occurs. Retries need a fresh attempt ID and output path within the
  parent's budget.
- The default wall timeout is one hour; the API dollar cap is optional and
  absent by default. Claude enforces an explicitly supplied API budget flag;
  this is not a subscription-token quota. The timeout bounds each attempt,
  including CLI startup, rather than the whole research mission.
  Timeout or cancellation terminates the worker process group and records a
  terminal result. SIGKILL or machine failure cannot guarantee finalization.

Full stdout/stderr and the role snapshot stay in a private attempt directory
under project `.tmp/claude-worker/`; keep `.tmp/` ignored. No runtime files go
inside a skill or role directory. Output is a new file inside the project;
existing files are never overwritten. Raw logs may contain confidential material.

## Return and integration

The adapter writes one role-run record with `assignment_id`, `attempt_id`,
`execution_provider: claude`, `execution_method: claude-cli`, native role source
and hash, requested and observed routing values, limits, terminal status,
duration, and raw-log location. `report` contains bounded findings, evidence
locators, uncertainty, counterevidence, blockers, and worker-reported validation.
Stdout contains only status and the output path. Non-success returns exit 1.

Host `system/init` metadata and terminal model usage can establish observed
routing. Generated prose and structured findings cannot. Missing metadata stays
`static-only`; conflicting or substituted metadata is `mismatch`. `verified`
requires observed role, model, and effort matching the request. Do not infer
verification from a successful process exit or the adapter's role snapshot.
CLI errors, malformed output, permission denials, and worker blockers never
count as success. A malformed handoff can produce a blocked record with null
assignment fields; fix the handoff before admitting that record to a mission.

Codex inspects the findings and supporting evidence, performs the declared
validator, promotes relevant evidence to declared artifacts, and appends the
terminal role-run entry to the existing run result. The adapter leaves
`artifacts` and `validators` empty for the parent to populate with checked
evidence; worker-reported validation is not parent validation. Preserve failures
and partial findings. The top-level run `host` remains `codex`, and only Codex
updates the existing ledger. No new mission, mailbox, or provider state tree is
created by the adapter.

Live role probes remain exclusively under the explicit
`harness doctor --strict --surface claude --probe-models` path. Offline tests
use fake executables and never spend model tokens.

Host contracts: [CLI flags](https://code.claude.com/docs/en/cli-reference),
[native and CLI-defined agents](https://code.claude.com/docs/en/sub-agents),
[credential storage](https://code.claude.com/docs/en/authentication#credential-management).
