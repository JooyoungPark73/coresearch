# Research Contract

The one rule everything hangs on: **every research output traceable from
source evidence → extracted claim → interpreted implication → final conclusion.**
No major claim without supporting evidence. No novelty without closest-work
comparison. No causal language without identification. No absence-from-search.

## Orchestrator input contract (what a run needs)

```yaml
topic: string
research_question: string
field_mode: systems_cloud|ml_systems|computer_architecture
venue_lens: general_systems|networked_distributed|cloud|cross_layer|workload_characterization
intended_contribution: method|system|representation|theory|dataset|benchmark|empirical_finding|design_knowledge|architecture|measurement_characterization
claim_class: capability|correctness|performance|scalability|efficiency|reliability|cost|quality_performance_tradeoff|power_area_performance|generality|measurement|causal
target_venues: [string]
scope: { years: [start,end], domains: [string], workloads: [string], platforms: [string], scales: [string], populations: [string], excluded_topics: [string] }
evidence_requirements: { minimum_primary_sources: int, minimum_independent_groups: int, require_counterevidence: bool }
output_path: string
# optional: known_papers, existing_project_claims, candidate_hypotheses,
# available_datasets, time_budget, compute_budget, implementation_constraints
```

`field_mode` has exactly three primary values: `systems_cloud` covers OSDI,
SOSP, NSDI, EuroSys, and SoCC; `ml_systems` covers MLSys; and
`computer_architecture` covers ISCA, MICRO, HPCA, and IISWC. ASPLOS uses the
`cross_layer` venue lens with the primary field chosen from the paper's
load-bearing claim. The other lenses express general systems,
networked/distributed, cloud, or workload-characterization expectations without
creating another field mode. `claim_class` classifies the primary claim at
intake; each synthesized claim records its own class in the shared evidence
contract.

## Claim ↔ evidence binding

The evidence + claim object structure, confidence dimensions, and rating rules
live in [evidence-grounding.md](evidence-grounding.md) — skills load that ONE
file per invocation. Binding rules that live here: no major claim without ≥1
`supporting_evidence`; contradicting evidence narrows scope, never hidden;
unresolved evidence id = blocker.

## Contribution ↔ evidence matching

`intended_contribution` decides what evidence the claim must carry:

| Contribution | Evidence must establish |
|---|---|
| method | what is new vs closest work; a test that would fail without it |
| system | components, data flow, failure modes, cost |
| representation | what it captures, what it loses, where it helps |
| theory | scope conditions, predictions, disconfirming cases |
| dataset | coverage, bias, annotation procedure, license |
| benchmark | difficulty calibration, leakage check, baselines, evaluation protocol |
| empirical_finding | direction, magnitude, identification strategy, limitations |
| design_knowledge | grounded excerpts, negative cases, transfer conditions |
| architecture | mechanism and interface, workload representativeness, validated methodology, configuration-matched baseline, PPA/complexity assumptions, sensitivity |
| measurement_characterization | collection and sampling method, representativeness, warmup/measurement window, repetitions and uncertainty, provenance, scoped implications |

## Backward compatibility

- New runs populate every field above and use the evidence and claim objects in
  [evidence-grounding.md](evidence-grounding.md).
- On re-entry, an existing ledger without `field_mode` remains valid. Infer the
  mode from its target venue and load-bearing claim, record that mode, and do
  not rewrite unrelated state. For ASPLOS, infer the primary mode from the
  hardware, systems, or ML-systems claim and retain `venue_lens: cross_layer`.
- Existing `intended_contribution` values retain their meanings; `architecture`
  and `measurement_characterization` are appended values, not replacements.
- An existing evidence object without `evidence_kind` defaults to `literature`.
  Do not require the expanded locator and evaluation fields retroactively;
  require them for newly created evidence records.

## Harness rules (spec §19 / §21)

1. Separate retrieval from synthesis. No single agent search + read + novelty + write.
2. Preserve rejected directions — log with reason; don't regenerate unless new evidence.
3. Load only relevant context: current RQ, schema, relevant artifacts, unresolved. Not every doc.
4. No novelty claim without closest-work comparison.
5. No causal claim without an identification strategy.
6. Match evidence to contribution type (table above).
7. Maintain explicit stopping criteria.
8. Report uncertainty as output, not as absence.

## Integrity floor (overrides everything)

Canonical text lives in [evidence-grounding.md](evidence-grounding.md)
§Integrity floor (no-invent list, fact/inference separation, untrusted-content
and confidentiality rules). Update there only; do not maintain a parallel copy.
