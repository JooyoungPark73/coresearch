# Bounded delegation

Use the host's native workers or a configured Claude Code process, not a
Coresearch runtime. Sonnet or Opus can handle substantial exploration,
implementation, tests, and independent audits. Luna/Terra/Sol or other capable workers
are also options. Choose by task and available tools, not a fixed model ladder.
Astra retains architecture, ambiguous/high-impact decisions, synthesis, and final
verification. Delegation is optional, including for small research tasks.

A quick survey can use lower reasoning effort. Tracing a cause across systems
or disentangling interacting explanations can warrant higher effort.
When the user or skill specifies a worker model or reasoning effort, pass the
requested settings explicitly in the spawn call. If the host requires
`fork_turns: "none"` for overrides, set it and give the worker a self-contained
task brief.

A useful assignment contains the objective, only the relevant context/paths,
owned scope and interfaces, constraints, expected artifact, and completion
criteria. Specify read-only scope for exploration/audits and disjoint files or
worktrees for concurrent edits. A worker should flag an architecture issue rather
than silently expanding its mandate. Do not pass confidential data to a worker
or service outside the user's authorized environment.

Request a compact handoff: findings; files/components; changes made; unresolved
issues; and validation commands/results. Return artifact paths instead of raw
transcripts or large logs. Evidence gathering should include source locators and
what was actually inspected. An implementation handoff should identify the patch
or revision the tests exercised.

Launch once, then do independent lead work or wait on the host's completion
mechanism. Consume the completed result when it informs a decision. Do not build
status-polling loops, repeated progress requests, or automatic reviewer chains.
On a blocked result, Astra decides whether to rescope, supply missing context,
change workers, or do the task directly. Never claim a worker ran when no runtime
was available.

For an already configured Claude Code installation in a trusted worktree, the
non-interactive interface can consume a bounded brief and emit a final handoff:

```bash
claude -p --model sonnet "$(cat task.md)" > handoff.md
# Use --model opus for a task better suited to that worker.
```

The brief is task-local, not persistent repository instruction. Use the host's
permission controls for the assigned scope; this command is not a sandbox.
Repository hooks/configuration may load in ordinary `-p` mode. For untrusted
checkouts or stronger isolation, use the host's supported sandbox/bare execution
and its required authentication, not permission-bypass flags.
