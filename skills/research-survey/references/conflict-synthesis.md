# Conflict synthesis

Use only when credible literature appears to disagree. First normalize claims,
objectives, terminology, workloads or data, methods, baselines, metrics, and
evaluation contexts. If no genuine disagreement remains, say so rather than
manufacturing one.

## Method

1. State the research question and normalized claim form.
2. Classify the `disagreement type` as `factual`, `causal`, `measurement`,
   `scope`, `objective`, `terminology`, or `implementation`.
3. Identify the dominant position from repeated evidence and methodological
   adoption; citation count alone is insufficient.
4. Identify credible counterevidence, including negative results, stronger
   baselines, new boundary conditions, confounds, or measurement artifacts.
5. Propose a mechanistic bridge only when supported. State boundary conditions
   and a distinguishing evaluation.

Output the dominant position, counterevidence, disagreement type, normalized
contexts, mechanistic synthesis, unresolved evidence, distinguishing test, and
confidence for the dominant position and synthesis separately.

Different objectives or terminology mismatches do not receive a forced
synthesis. Incomparable contexts must be labeled before interpreting results as
conflict. Unsupported bridges remain speculation; without a feasible
distinguishing evaluation, leave the synthesis unresolved and record the issue
in `quality_state.unresolved_methodology_issues` when durable state is active.
