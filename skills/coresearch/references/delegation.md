# Bounded delegation with low communication overhead

Astra is the research and engineering lead, not a relay for every worker step.
Keep tightly coupled reasoning, consequential architecture, synthesis, and final
interpretation with the lead. The lead also does substantive work directly.
Delegate an independently useful artifact when specialization, parallelism, or
context isolation is worth briefing, startup, communication, and integration.
A small task or a task on the critical path may be faster to finish directly.

Use the host's native workers or configured processes, not a Coresearch runtime.
GPT-6.1 Sol is a worker candidate for substantial bounded engineering and analysis;
Claude Code workers, Luna, or other capable models can also fit. Select by the
actual task, tools, evidence of reliability, and total cost, not a fixed ladder.
Do not restrict a capable worker to mechanical edits.

## Give ownership, not a stream of micro-instructions

A useful assignment contains the objective, relevant context and artifact paths,
owned scope and interfaces, constraints, expected deliverable, and acceptance
criteria. Include a real resource budget and escalation conditions when they
matter. Define what the worker may decide without another approval. Workers
should implement, test, and repair within that scope rather than returning after
each tool call or first implementation. Keep normal tool-result feedback local
to the worker; low communication does not mean unobserved execution.

Use read-only scope for exploration/audits and disjoint files or worktrees for
concurrent edits. Do not have the lead redo delegated work while a worker edits
the same files. A material architecture or scientific-contract change belongs
back with the lead. Do not send confidential inputs outside the authorized
worker environment. Avoid recursive delegation unless its scope, budget, and
benefit are clear and the host supports it.

## Communicate at decision boundaries, not on a timer

Launch once, then perform independent lead work or use the host's native wait
or completion mechanism. Do not interrupt a healthy worker for percentage-done
updates, repeated status requests, or automatic reviewer sign-offs. A normal
assignment needs its brief and a completion handoff, not a fixed series of
check-ins. Join only when a decision needs the result; do not wait for unrelated
workers at an artificial global barrier.

Intermediate messages are warranted for a genuine blocker, an authority or
budget boundary, a violated shared assumption/interface, evidence that changes
the research direction, or an explicitly agreed high-value checkpoint before
expensive or irreversible work. Report the changed fact, its consequence, and
the decision or input needed. Bundle related questions. Continue safe independent
work where possible; do not silently exceed the assignment to avoid messaging.

Keep health checks, process supervision, telemetry, and hard limits in the host.
They need not become model-facing conversations. If a completion event is lost,
use the host's recovery procedure or inspect the specific task handle; do not
infer success from silence or start an unbounded polling loop. A blocked, failed,
canceled, or timed-out task is not a completed artifact. Never claim a worker or
an asynchronous facility ran when none was available.

## Handoffs preserve evidence, not transcripts

Return findings, changed files/artifacts and revision, actual validation commands
and outcomes, source locators, and unresolved issues. Separate observed results
from interpretation. Keep raw logs, data, and diagnostic detail accessible at
stable paths; send only the portion needed for the lead's decision. A summary
must not hide counterevidence or replace a critical source. Do not request hidden
reasoning traces or reconstruct a worker's whole conversation as project state.

The lead inspects load-bearing evidence and verifies consequential integrations.
Reopen work for an identified gap, not a ritual second opinion. Additional review
should offer a different check rather than replay the worker's entire task.
Compare delegation against direct execution on actual deliverables; fewer
messages alone do not establish better science or engineering.

## Existing host interfaces

A configured Claude Code installation in a trusted worktree can consume a bounded
brief and emit a final handoff:

```bash
claude -p --model sonnet "$(cat task.md)" > handoff.md
# Use another configured worker when its capability better fits the assignment.
```

The brief is task-local, not persistent repository instruction. This command is
not a sandbox; ordinary host hooks and configuration can load. Use the host's
supported isolation, authentication, and permission controls for untrusted code,
not permission-bypass flags. Verify model selection and heterogeneous-worker
support in the actual host. A native multi-agent feature may share one model
across its agent tree; it does not automatically implement Astra-to-Sol routing.
Coresearch neither selects models nor provisions that routing.
