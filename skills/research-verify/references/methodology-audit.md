# Methodology audit

Attack the evidence logic, not the author. Tie every issue to the affected
claim and always end with what the evidence does support.

## Applicable checks

- claim definition and measured operating envelope;
- experimental unit, sampling, censoring, and train/tune/test separation;
- workload, trace, dataset, scale, topology, and platform representativeness;
- baseline version, tuning, resource, configuration, and measurement fairness;
- metric validity, units, aggregation, measurement protocol, repetitions,
  uncertainty, tails, and failures;
- statistical independence, effect sizes, intervals, repeated measures, and
  multiple comparisons;
- ablations and alternative explanations;
- generalization beyond tested workloads, platforms, models, or conditions;
- optional human evidence only when it bears the claim;
- reproducibility: code, data, commands, configs, seeds, versions, manifests,
  and failed or censored runs;
- applicable field-specific controls from the shared field reference.

Never generalize beyond the measured operating envelope. Abstract-only support
for a central claim leaves statistics and reproducibility `uncertain`; do not
guess.

## Output

Return claim-to-evidence alignment, applicable dimension findings, and a table:

| Severity | Issue | Evidence | Effect on claim | Required fix |
| --- | --- | --- | --- | --- |

Then state valid contributions, the **revised defensible claim**, its
confidence and scope, residual uncertainty, and the smallest additional
evaluation that could resolve a load-bearing issue.

When durable state is active, set the audited source's `source_state` to
`audited`, update affected claim state, and add unresolved issues without
overwriting unrelated ledger keys. For abstract-only material, attach an
`abstract-only; partial audit` note so the state does not imply full-text
coverage. An audit without a revised defensible claim is incomplete.
