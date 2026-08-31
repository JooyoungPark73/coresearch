# Historical migration to standalone Coresearch

This document records the removal of the former OMX integration. It is
migration history, not an active compatibility or execution path.

Coresearch previously delegated research lifecycle control to optional OMX
modes, stored convenience mirrors under `.omx/`, selected OMX role names, and
conditioned prompt bridges on the `omx` executable. The standalone design
replaced those concepts with:

- `coresearch` as the only research-stage router;
- eight fixed native Coresearch roles for Codex and Claude Code;
- a shared mission, sandbox, and result contract under
  `docs/research/runs/<run-id>/`;
- Codex `/goal` or Claude Code native session continuation;
- `docs/research/decisions/ledger.yaml` as the only canonical research state;
- executable-independent, marker-bounded prompt bridges;
- harness installation and strict diagnostics for skills and native roles.

No migration command uninstalls or modifies a user's separate OMX installation.
Existing Coresearch prompt backups remain recoverable through
`harness rollback`. Re-run `harness link --surface both` and
`harness doctor --strict --surface both` to install and statically validate the
standalone bundle.

The former combined `omx-pony-caveman.md` reference mixed useful working
preferences with runtime-specific orchestration. Its runtime, role, state, and
continuation material remains removed. Only the orthogonal behavior was
re-expressed as provider-neutral
[`ponytail.md`](../../skills/coresearch/references/ponytail.md) and
[`caveman.md`](../../skills/coresearch/references/caveman.md): explicit
task/mission-scoped modifiers for minimal durable engineering and communication
compression, respectively.
