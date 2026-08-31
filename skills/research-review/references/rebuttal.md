# Review response

Use response mode only when reviews or discussion feedback exist. This is
response planning, not experiment execution.

## Method

1. Parse each review's score or stance, confidence, positive anchors,
   score-moving concerns, legitimate weaknesses, and possible misunderstandings.
   If no score is supplied, label inferred stance low or moderate confidence.
2. Classify concerns: factual error, missed explanation, evidence gap, novelty,
   fairness, methodology, writing, venue fit, or fundamental flaw.
3. Estimate response leverage as high, medium, low, or very low. Prioritize
   consensus factual corrections and score movement; do not fight every
   sentence.
4. Pair every response with existing evidence. A build or bug fix does not
   resolve a research-evidence concern.
5. Prefer the smallest addition that directly bears the disputed claim. Do not
   promise an experiment, analysis, figure, or edit until the user confirms
   feasibility and current venue rules permit it.
6. Acknowledge legitimate weaknesses, scope claims, and avoid defensive or
   adversarial tone.

## Detailed output when needed

When multiple distinct reviews are supplied, review-by-review diagnosis is
required. Add the remaining sections only when they help answer the request:

- global strategy in priority order;
- review-by-review diagnosis with positive anchors and leverage;
- cross-review themes and evidence needs;
- evidence-linked response bullets;
- allowed additions with feasibility and expected score movement;
- risks and what not to say;
- before/after forecast with confidence;
- concise rebuttal skeleton.

Separate confirmed corrections, feasible but unproduced additions, and
impossible or low-value requests. Unsupported or post-hoc claims are rejected,
not polished into the response.
