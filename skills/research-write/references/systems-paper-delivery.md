# Systems Paper Delivery

Read this reference when section-level conventions or whole-paper delivery
materially affect the requested prose. Compose it with the current field mode
and venue lens; do not duplicate or override their evidence requirements.

## Use the shortest honest spine

Why–how–results is a common systems-paper diagnostic, not three mandatory
headings:

- **Why:** context, objective, problem/gap, closest-work insufficiency, and
  intended lesson.
- **How:** insight or finding, mechanism/method, system position when relevant,
  design choices, trade-offs, and exclusions.
- **Results:** implementation or study reality, claim-bearing evidence,
  uncertainty, interpretation, and scope.

Mechanism-led papers usually use Ha: operating need → bottleneck → insight →
mechanism → evaluation → limits. Measurement/workload papers use Oh: context →
method → findings → implications → transfer boundary. ASPLOS uses Hybrid only
when the hardware and software claims share a cross-layer dependency and both
receive evidence.

## First page and compression

For many papers, the first page should quickly establish a concrete problem or
finding, relevant application/workload and environment, unresolved gap, key
insight, approach, strongest supported evidence, and refutable contributions.
Treat this as a heuristic. A theory, benchmark, dataset, experience, or
measurement paper may use a different sequence while preserving the same
reader contract.

Prefer claim-linked forward references over a table-of-contents paragraph.
Use a concrete example before difficult abstraction when it exposes the exact
failure or mechanism. Do not rewrite the chronology of discovery as a false
causal history; report failed alternatives when they establish a load-bearing
trade-off or lesson.

## Section contracts

- **Title, abstract, introduction, contributions, conclusion:** realize the
  same coherent payload at different compression levels. Do not strengthen a
  claim as it becomes shorter.
- **Abstract:** make the problem/finding, gap, approach, principal evidence,
  and scoped implication recoverable without undefined internal terminology.
- **Introduction:** establish the reader’s problem and the paper’s proof
  obligations; do not inflate a narrow evaluated result into a mountain-sized
  motivation.
- **Background:** include only concepts needed to understand the problem,
  method, or mechanism.
- **Method/system:** explain boundaries, inputs/outputs, state, control/data
  path, invariants, interfaces, constraints, failure modes, and
  evaluation-relevant implementation reality when applicable.
- **Evaluation/findings:** lead with the claim or question, present evidence,
  interpret it at the supported strength, and state the boundary. Do not follow
  experiment chronology unless sequence is itself the finding.
- **Related work:** describe prior work at its strongest; compare exact
  assumptions, mechanisms, interfaces, environments, or trade-offs. Provide
  enough early positioning to motivate the gap, and place comprehensive
  comparison where the reader has the needed vocabulary.
- **Discussion/limitations:** say what each limitation affects, what it does
  not, and what evidence would test the boundary. Preserve negative results.
- **Captions:** state the supported takeaway and enough reading guidance to
  interpret the figure; do not claim more than the plotted evidence.

## Explain load-bearing design choices

For each load-bearing design decision, connect:

1. requirement derived from the problem;
2. selected mechanism;
3. credible alternatives;
4. rationale for the selected trade-off in the target context;
5. cost, limitation, or excluded case;
6. claim and evidence destination.

Do not enumerate every implementation choice. Explain choices whose rationale,
trade-off, or validity affects a paper claim.

## Make evaluation claim-bearing

For each empirical claim, make recoverable:

- proof obligation or hypothesis;
- baseline/counterfactual and configuration parity;
- metric and why it represents the claimed outcome;
- controlled and varied conditions;
- workload/dataset/platform and operating envelope;
- setup, warmup, repetitions, uncertainty, tails/variance when applicable;
- result status and supported conclusion;
- limitation or threat to validity.

End-to-end outcome evidence and mechanism evidence are common complementary
categories, not exhaustive requirements. Correctness proofs, security
analysis, failure recovery, scalability, cost, usability, longitudinal
deployment, formal analysis, benchmark validity, and qualitative evidence may
be load-bearing depending on the claim.

Ablations, breakdowns, sensitivity studies, and alternative designs can supply
mechanism evidence. They do not automatically prove that a component causes an
outcome. Use causal language only when an identification strategy addresses
credible competing explanations; otherwise say “is consistent with,”
“accounts for under this decomposition,” or “provides mechanism evidence.”

## Realize paragraphs and sentences

A paragraph should normally perform one primary rhetorical job, but record that
function only when it improves planning or diagnosis. Sentences must preserve
the difference among observation, author-provided result, interpretation,
hypothesis, planned evidence, and speculation. Define terms before relying on
them, use direct language, and prefer active constructions when they clarify
responsibility or action.

## Delivery gates

Before returning prose, check:

- every major rendered claim has supplied evidence or is visibly marked
  unresolved;
- implementation/study reality is explicit when it affects credibility;
- metrics, baselines, workloads, and scope match the claim;
- ML quality parity or architecture fidelity/PPA qualifications are preserved;
- causal and generalization language does not exceed identification or scope;
- terminology and system boundaries are consistent;
- planned evidence has not become a result;
- no unrelated author prose was rewritten merely for stylistic uniformity.
