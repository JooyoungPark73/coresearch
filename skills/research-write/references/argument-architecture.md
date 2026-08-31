# Argument Architecture

Read this reference for whole-paper drafting, restructuring, contribution
alignment, or coherence diagnosis. Do not load it for an ordinary bounded
rewrite.

## Boundary

`research-design` decides the contribution, novelty position, venue strategy,
and evidence program. `research-write` receives that author-approved research
direction and makes its argument inspectable and communicable. If the payload
cannot be formed without inventing a contribution or unsupported result,
report the gap and return to `coresearch`.

The manuscript map is a view over canonical claim and evidence records. It
must not copy evidence provenance, confidence, experimental context, or claim
status, and it must not become another ledger.

## Select a paper archetype

Choose the archetype that matches the load-bearing contribution. Hybrids are
allowed when their claims depend on one another; do not force disconnected
contributions into one payload.

| Paper archetype | Coherent payload | Typical proof obligations |
| --- | --- | --- |
| Implemented mechanism/system | A scoped mechanism changes an important operating outcome | context/problem, mechanism, implementation reality, end-to-end evidence, mechanism evidence, limits |
| Measurement/workload characterization | Rigorous observation reveals a reusable finding or changed assumption | representativeness, collection methodology, uncertainty, finding, implication, transfer boundary |
| Architecture/cross-layer | A hardware, software, or paired mechanism changes a capability/trade-off under constraints | workload trend, mechanism, validated method, feasibility/PPA or system effect, sensitivity, interface |
| Method/benchmark/dataset | A reusable method or artifact lets the field define, measure, or compare something better | need, construction, validity, coverage, discriminative value, reuse conditions |
| Experience/negative results | Deployment or failure evidence changes what the field should expect or do | setting, implementation/reality, observed outcomes, competing explanations, lesson, limits |
| Theory/analysis | A model, theorem, or analysis changes understanding under explicit assumptions | assumptions, derivation/proof, relationship to reality, sensitivity, implication |
| Design proposal | A new design is worth considering before full implementation | novelty/need, assumptions, internal consistency, feasibility evidence, unresolved implementation risk |

## Form the coherent payload

“One ping” means one recognizable takeaway, not one literal contribution.
Represent it with the smallest applicable set of roles:

- target application/workload and environment, when applicable;
- important objective, question, or changed context;
- problem, gap, or prior assumption that fails;
- insight, central finding, method, or mechanism;
- system/artifact only when the paper depends on one;
- strongest supported outcome or result;
- assumptions and exclusions;
- scoped reusable lesson.

Mechanism-led work may use the reasoning aid `Y in Z needs R; P prevents it; I
enables D/X; evidence E supports O over B under A; lesson L follows`. Treat it
as a diagnostic, not a sentence template. Measurement, benchmark, experience,
and theory papers should use roles appropriate to their archetype rather than
inventing X.

## Build the claim graph

Use refutable claims, not accomplishments. Each claim records its canonical
`claim_id`, scope, dependencies, manuscript destinations, supporting
`evidence_id` references, counterevidence references, and unresolved warrant.
Claim-edge direction and meaning must come from author-approved records or an
explicit user statement. Keep an unspecified dependency unresolved and ask the
author which claim depends on which and why; do not infer a mechanism,
interface, ordering, or causal relationship merely because two claims are
described as paired or dependent.

Useful edge meanings:

- `depends_on`: the downstream claim is credible only if the upstream claim
  holds;
- `supports`: evidence increases confidence but does not automatically prove;
- `contrasts_with`: a specific mechanism, assumption, interface, or trade-off
  differs;
- `qualifies`: a condition narrows scope or epistemic strength;
- `motivates`: an observation establishes the need for a requirement;
- `realizes`: a mechanism or method instantiates an insight;
- `warrants`: reasoning connects evidence to the asserted conclusion;
- `generalizes_to`: a scoped lesson follows only under named transfer
  conditions.

Reject a graph that has a contribution without evidence, evidence without an
important claim, a metric that does not measure the claimed outcome, a causal
edge without an identification strategy, or a conclusion broader than its
evaluated scope.

## Keep status dimensions separate

- Claim status: `unresolved`, `supported`, `contradicted`, `qualified`, or
  `rejected`.
- Evidence status: `planned`, `collected`, `validated`, or `invalid`.
- Artifact status: `proposed`, `implemented`, `tested`, or `deployed`.
- Manuscript status: drafting progress only.

Read these values from their owning research artifacts. Do not infer
`supported` from `implemented`, or `measured` from `planned`.

## Bind claims to exposition

For each section, state:

- reader question;
- promise—what the reader should understand or believe afterward;
- claim IDs established or qualified;
- evidence IDs presented;
- dependencies that must already be understood.

Use paragraph functions only where local structure is unclear: context, claim,
example, mechanism, evidence, interpretation, comparison, qualification, or
transition. Do not serialize every paragraph by default.

## Optional manuscript map

Keep this view transient unless the user requests persistence or a durable
mission declares it as an artifact:

```yaml
manuscript_map:
  paper_type: string
  payload: string
  intended_takeaway: string
  claim_bindings:
    - claim_id: string
      role: string
      depends_on: [string]
      section_ids: [string]
  section_promises:
    - section_id: string
      reader_question: string
      promise: string
      claim_ids: [string]
      evidence_ids: [string]
  terminology: {}
  unresolved_writing_gaps: []
  revision_impacts: []
```

The map references canonical claim and evidence IDs. It must not copy their
full records and must not write a second global state tree. A durable map may
live under `docs/research/runs/<run-id>/` as a declared artifact; the existing
mission, result, and canonical ledger remain authoritative for continuation.

## Compression diagnostics

Before expanding a whole paper, compare:

1. one-sentence payload;
2. one-paragraph problem/finding, approach, evidence, and lesson;
3. short conclusion—question/thesis, method/artifact when applicable, result,
   scoped lesson;
4. abstract moves appropriate to the archetype.

If they disagree, reconcile the claim graph before polishing prose. Missing
evidence remains visible; fluent language is not a repair.

## Output floor

Return the coherent payload, claim/dependency map, unsupported or conflicting
claims, section promises, manuscript plan, any requested draft, and remaining
evidence/revision risks. Separate author-provided facts, inference,
recommendation, and unknown.
