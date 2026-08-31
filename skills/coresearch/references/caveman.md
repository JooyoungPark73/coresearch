# Caveman Working Mode

Caveman is an optional, provider-neutral working mode for **communication
compression**. It makes updates and deliverables terse without weakening the
reasoning, evidence, or required output contract behind them.

It is not a research stage, skill route, native role, model tier, permission
grant, or substitute for analysis. It must not change model or role selection.

## Activation and scope

Activate Caveman only when the user explicitly requests it or a durable
mission declares it under `working_modes.caveman`. Allowed levels are `off`,
`lite`, and `full`.

- `off`: use the normal output contract of the primary skill.
- `lite`: shorten progress updates and explanatory prose.
- `full`: emit only the required artifact or answer plus decisive evidence,
  blockers or risks, and the next or terminal condition.

The setting is scoped to the current task or mission. Do not infer it from an
earlier conversation or persist it as undeclared global state.

## Compression contract

In Lite mode:

- Lead with the result, artifact, or current blocker.
- Keep headings, rationale, and process narration to the minimum needed for a
  reader to act.
- State a plan once; later updates report only changed evidence or state.
- Prefer a compact mapping or table only when it is shorter and clearer than
  prose.

In Full mode, retain only:

1. the requested result or artifact;
2. evidence needed to trust or reproduce it;
3. unresolved risk, blocker, or uncertainty; and
4. the next action or stop condition when one exists.

Existing machine-readable schemas, venue limits, rebuttal structures, review
forms, and skill-specific required fields still win. Caveman compresses their
wording, not their contents.

## Non-compressible information

Caveman must not compress away:

- safety, ordering, permission, confidentiality, privacy, or destructive-action
  boundaries;
- citations, source provenance, claim-evidence links, validator commands, or
  validation results needed to audit a conclusion;
- uncertainty, scope conditions, negative results, conflicting evidence,
  limitations, or distinctions among fact, inference, recommendation, and
  unknown;
- configuration and reproduction details required by the primary skill; or
- information the user explicitly requested.

Expand automatically whenever brevity would make any of those items ambiguous.
Compression applies to communication, never to the internal rigor of analysis
or to scientific evidence requirements.

## Handoff and composition

Pass the active level explicitly in every bounded role assignment and durable
mission:

```yaml
working_modes:
  caveman: lite  # or full
```

A receiving role applies the mode only to its reporting style. It does not gain
tools, write access, routing authority, or a different model. If a required
artifact cannot be terse without becoming incomplete, the artifact contract
takes precedence.

Caveman composes independently with Ponytail: one compresses communication;
the other minimizes durable research engineering.
