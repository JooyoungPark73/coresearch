# Terminal result schema

Every durable run ends with
`docs/research/runs/<run-id>/result.json`. New runs use schema version 2:

```json
{
  "schema_version": 2,
  "run_id": "string",
  "mission_path": "string",
  "status": "success|blocked|failed|cancelled",
  "host": "codex|claude",
  "goal_id": "string|null",
  "role_runs": [
    {
      "assignment_id": "implement-unit-1",
      "attempt_id": "implement-unit-1-a1",
      "execution_provider": "codex",
      "execution_method": "native",
      "role": "coresearch-implementer",
      "status": "success|blocked|failed|cancelled",
      "requested_model": "string",
      "requested_effort": "string",
      "observed_model": "string|null",
      "observed_effort": "string|null",
      "routing_status": "verified|static-only|mismatch",
      "artifacts": [],
      "validators": [],
      "stop_reason": "string"
    }
  ],
  "artifacts": [],
  "validators": [],
  "claim_evidence": [],
  "ledger_updates": [],
  "remaining_risks": [],
  "stop_reason": "string"
}
```

Record every attempted assignment in `role_runs`, including independent
verification and blocked, failed, or cancelled lanes. `verified` requires host
metadata matching the requested role, model, and effort. Successful execution
with missing or partial metadata is `static-only`; blocked execution,
substitution, unavailability, or a different role, model, or effort is `mismatch`.
Record the host evidence establishing role identity in the assignment's validator
evidence; the `role` field alone is a request, not proof of observed routing.

The top-level `host` identifies the parent. New entries include `attempt_id`,
`execution_provider` (`codex` or `claude`), and `execution_method` (`native` or
`claude-cli`). Historical version-2 entries without these additive fields mean
native execution on the parent host, with `assignment_id` identifying the
attempt. Do not rewrite them. A Codex-led run may contain a Claude CLI worker;
use that entry's provider to interpret model and effort. Preserve each attempt.

The [Claude adapter](../../coresearch/references/claude-worker.md) returns a
role-run record with additional report, timing, limits, role-source hash, and
log fields. `limits.timeout_seconds` defaults to 3600 per attempt;
`limits.max_budget_usd` is null when uncapped, or the explicit positive dollar
cap. Parent validation supplies its `artifacts` and `validators` before
integration; generated worker validation does not establish validator success.
Never infer observed metadata from the report. Keep the existing run directory
and ledger as the only durable research state.

For Codex, `requested_model` is one of the approved Astra, Sol, or Luna
model IDs, never the policy label `assignment`. Keep selection rationale in the
mission assignment or handoff; record each escalated attempt separately with
its requested values, failure evidence, and stop reason. Compare the observed
model to that attempt's requested model, not a historical role pin.

`requested_effort` is the parent's concrete assignment choice
(`low`, `medium`, `high`, or `xhigh`), never the manifest label `assignment`.
For Claude it remains the configured role effort. Compare observed effort with
this recorded request, not a historical Codex role default. Model and effort
retain their existing version-2 meaning; historical records are unchanged.

Schema version 1 remains valid for historical zero- or one-role runs. Do not
rewrite old results solely to upgrade them. A resumed run using multiple role
assignments emits version 2 while preserving historical artifacts and ledger
records.

Success requires validator evidence for the claimed artifacts and explicit
remaining risks. `status`, assignment status, and `stop_reason` must agree; a
blocked, failed, or cancelled run is a valid terminal record, not missing work.
