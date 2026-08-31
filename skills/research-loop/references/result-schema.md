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
metadata matching both requested model and effort. Missing or partial metadata
is `static-only`; substitution, unavailability, or mismatch is `mismatch`.

Schema version 1 remains valid for historical zero- or one-role runs. Do not
rewrite old results solely to upgrade them. A resumed run using multiple role
assignments emits version 2 while preserving historical artifacts and ledger
records.

Success requires validator evidence for the claimed artifacts and explicit
remaining risks. `status`, assignment status, and `stop_reason` must agree; a
blocked, failed, or cancelled run is a valid terminal record, not missing work.
