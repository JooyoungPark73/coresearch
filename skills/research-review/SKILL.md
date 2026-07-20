---
name: research-review
description: Venue-calibrated simulated review and score forecast for systems/cloud, ML-systems, and computer-architecture papers. Use when the user asks to review, critique, score, triage, forecast acceptance, identify acceptance risks, simulate reviewers, or assess submission readiness for OSDI, SOSP, NSDI, EuroSys, SoCC, MLSys, ISCA, MICRO, HPCA, IISWC, ASPLOS, or related venues.
---

# research-review — Venue Review & Score Forecast

Act as a strict but fair author-side reviewer; provide explicit scores. Not for
confidential official peer review unless venue policy permits. In OMX this is a
verification surface: may block completion when score-moving evidence gaps remain.

## What & When

Venue-calibrated simulated review, acceptance-risk triage, score forecast,
reviewer-modeling, submission readiness — for `systems_cloud`, `ml_systems`,
`computer_architecture` (including IISWC `measurement_characterization` as a
primary contribution), and ASPLOS `cross_layer` papers. Use when: "review", "critique", "score", "triage", "forecast acceptance",
"identify acceptance risks", "simulate reviewers", "assess submission readiness";
finding score-moving evidence gaps and rewrite priorities.

Not for: replacement prose → research-write;
citation/source faithfulness → research-verify.

Inputs: manuscript text, figures, captions, supplement, code, results, author
notes. If key inputs are missing, score lower-confidence and state what could not
be checked.

## Procedure

Use official scales if the current venue form is verified; otherwise label scales
`INTERNAL` — memorized mappings go stale each cycle. One internal anchor; map to
an official scale only after verifying the target venue's current form:

- **INTERNAL 1–6:** 6 strong accept, 5 accept, 4 borderline accept, 3
  borderline reject, 2 reject, 1 strong reject; rate quality/clarity/significance/
  originality 1–4 when useful.

State score/recommendation, confidence, variance, blockers, and movement
conditions. Judge claim-evidence alignment, not just writing quality. Flag
confidentiality/policy limits before using official reviews.

Review dimensions — always assess:

- clarity of contribution; venue fit;
- novelty/originality relative to supplied or verified related work; claim-evidence alignment;
- technical soundness and research insight; baselines/comparisons and configuration fairness or rationale for absence;
- reproducibility and implementation detail; writing and figure effectiveness;
- ethics/data/participant/societal issues when relevant; limitations and failure cases.

Evaluation contract — always audit the applicable rows:

- representative workloads and explicit operating envelope;
- fair baseline versions, tuning, resources, hardware/software configurations, and cost accounting;
- warmup, repetitions, statistical/variance treatment, distributions and tail metrics;
- scale, overload, failure/recovery behavior, and cloud temporal/instance variance for systems/cloud claims;
- task/model/data quality or convergence parity before ML-systems throughput, latency, energy, or cost claims;
- simulator fidelity/calibration, sampling methodology, sensitivity, hardware validation where feasible, and defensible PPA models for architecture claims;
- a genuine cross-layer mechanism and end-to-end co-evaluation for ASPLOS claims;
- for IISWC measurement/workload characterization, the representativeness,
  measurement validity, findings, and implications as the primary research
  contribution; do not require a new mechanism when none is claimed;
- research-qualitative rigor only when that optional method bears a claim; never require it by default.

Borderline discipline — for any borderline score, explicitly state: what real
contribution supports acceptance; what evidence/novelty/clarity gap supports
rejection; what would move the paper up; what would move the paper down.

## Output

Mandatory fields:

- **Recommendation:** Overall score/recommendation; Confidence (1–5 or official);
  Reviewer stance (strong accept / accept / borderline / reject); Likely variance (low / medium / high); Submission-ready now (yes / no / borderline).
- **Summary:** 2–4 sentences describing what the paper claims and contributes.
- **Claimed Contributions:** numbered list.
- **Strengths:** each tied to specific evidence.
- **Weaknesses:** each tied to claim/evidence.
- **Score Rationale:** why this score, not one level higher or lower.
- **Score Movement Conditions:** "Would increase if" (concrete evidence, rewrite, or analysis); "Would decrease if" (concrete risk or missing support).
- **Top Acceptance Risks:** ranked, ~5.
- **Required Revisions Ranked by Score Impact:** table — Impact | Revision | Evidence affected | Feasibility.
- **Questions for Authors:** answers that could move the score.
- **Venue-Specific Score Sheet:** the relevant venue dimensions.
- **Meta-review Forecast:** likely decision-level synthesis, disagreement pattern, correctable vs fundamental negatives, and likely decision path; keep committee roles venue-neutral unless the current form is verified.

## Reject when

- score/recommendation missing confidence, variance, blockers, or movement conditions;
- borderline score missing any of the four required statements (accept support / reject support / up-mover / down-mover);
- official scale cited without current-form verification, or without flagging confidentiality/policy limits.
- review accepts engineering completion, a single favorable configuration, or a mean-only result as sufficient support for the central research claim;
- applicable workload, operating-envelope, fairness, warmup/repetition, tail, scale/failure/variance, quality-parity, or simulator/PPA risk is omitted from the assessment.

## State & Handoff

State: review produced; score-moving evidence gaps block OMX completion until
closed. Next: research-write (revision prose) / research-verify (citation faithfulness) / research-audit (methodology attack). Carry forward variance and unanswered author-questions as warnings. In
a multi-skill run, also seed `quality_state` (unsupported_claims /
missing_counterevidence / unresolved_methodology_issues) from the score-moving
gaps (state-ledger.md); standalone, the review above is enough.

Re-entry: return to `coresearch` to re-route the next stage.
