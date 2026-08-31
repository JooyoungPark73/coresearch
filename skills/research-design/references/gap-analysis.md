# Gap analysis

Find important, testable, insufficiently resolved opportunities—not merely
uncrowded topics. An empty search can mean weak terminology, low importance,
infeasibility, or known failure.

## Method

1. State the field objective and recurring assumptions.
2. Map closest work, alternate terminology, adjacent fields and layers,
   partial solutions, negative results, and relevant methodological failures.
3. Form each candidate as: the field wants A; current approaches depend on B;
   B fails under C; prior work does not resolve D; a testable contribution is E.
4. Falsify it against closest work, fair baselines, representative workloads,
   realistic resources, and whether it is merely unfinished engineering or a
   new application domain.
5. Rank importance, tractability, and novelty independently as high, medium, or
   low with a reason. Never collapse them into one score.

## Required fields

Each surviving candidate includes the gap statement, evidence, closest work,
why existing work is insufficient, candidate mechanism, falsifiable
hypothesis, expected contribution, evaluation path, and risks.

`absence classification` is exactly one of:

- `no_papers`
- `few_papers`
- `none_on_mechanism`
- `unresolved_limitations`
- `actual_testable_gap`

Default conservatively. Use `actual_testable_gap` only after closest-work
falsification passes. Reject feature requests, application-domain novelty
alone, unevaluable hypotheses, unrealistic dependencies, and solutions
disconnected from the bottleneck.

For durable work, preserve `gap_state.{candidates,falsified,surviving}`, search
blind spots, and rejected reasons. Do not regenerate a falsified gap without
new evidence. Failed methodology checks and unidentifiable hypotheses may seed
new candidates, but they do not prove a gap.
