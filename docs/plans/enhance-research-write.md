# Implementation Plan: Hierarchical `research-write`

## Objective

Upgrade the existing `research-write` skill from a section rewriter into an
evidence-bounded systems-paper drafting, rewriting, and semantic-revision skill
based on
[`hierarchical-systems-paper-writing.md`](../../hierarchical-systems-paper-writing.md).

Preserve the current lightweight rewrite path while adding optional
hierarchical argument design and revision behavior.

## Fixed design decisions

- Enhance the existing `research-write`; do not add another skill or harness.
- Keep exactly 15 skills and eight provider-neutral roles.
- Keep `coresearch` as the only research-stage router.
- Do not change model pins, role definitions, plugin metadata, or
  `scripts/harness.py`.
- Do not introduce another workflow engine or canonical ledger.
- Reuse Coresearch claim/evidence IDs and schemas.
- Treat the manuscript map as transient by default and an optional declared run
  artifact for durable work.
- Preserve automatic skill invocation.
- Add no third-party dependencies.
- Preserve `PROMPT.md`, `PROMPT(1).md`, unrelated changes, and installed user
  state.
- Keep document formatting, LaTeX mechanics, PDF rendering, and publication
  templates outside this skill.

## Target behavior

`research-write` will support five modes:

| Mode | Trigger | Primary behavior |
| --- | --- | --- |
| Local rewrite | Supplied paragraph or section | Return polished text first without constructing a full argument map |
| Section drafting | Claims/evidence supplied for a new section | Establish a section promise and produce evidence-bounded prose |
| Argument architecture | Whole-paper planning, coherence, or restructuring | Build or inspect payload, claims, dependencies, and section promises |
| Semantic revision | Feedback changes framing, scope, evidence, or conclusions | Compute impact, reconcile semantics, and minimally revise affected passages |
| Concept decomposition | Explain a concept or mechanism | Preserve current problem → intuition → mechanism → formalization → boundaries behavior |

## Files in scope

### Modify

- `hierarchical-systems-paper-writing.md`
- `skills/research-write/SKILL.md`
- `skills/coresearch/SKILL.md`
- `skills/coresearch/references/routing.md`
- `skills/coresearch/references/stage-map.md`
- `skills/coresearch/references/skill-catalog.md`
- `templates/research/AGENTS.md`
- `README.md`
- `DESIGN.md`
- `scripts/validate.sh`

### Add

```text
skills/research-write/references/
├── argument-architecture.md
├── systems-paper-delivery.md
└── semantic-revision.md
```

### Do not modify

- `agents/manifest.json`
- `agents/codex/`
- `agents/claude/`
- `skills/manifest.json`, unless an ownership validation defect is discovered
- `scripts/harness.py`
- `.codex-plugin/plugin.json`
- `PROMPT.md`
- `PROMPT(1).md`
- Canonical ledger schema
- Provider installation topology

## Implementation sequence

### 1. Establish the baseline

Before editing:

```bash
git status --short
./scripts/validate.sh
./harness doctor --strict
git diff --check
```

Record existing failures separately. Do not repair unrelated dirty-worktree
changes.

Success condition: the pre-change state and any pre-existing failures are
known.

### 2. Add regression contracts first

Update `scripts/validate.sh` before changing behavior.

Add checks that initially fail because the new behavior is absent:

- All three new references exist.
- Every reference is linked conditionally from `research-write/SKILL.md`.
- The skill declares all five writing modes.
- Local rewrite remains the default for supplied excerpts.
- Whole-paper requests use argument architecture.
- Semantic revision requires impact analysis and preservation of unaffected
  prose.
- `research-write` references the canonical claim/evidence contract rather than
  defining another ledger.
- “Likely score impact” is absent from `research-write`.
- Score forecasting remains routed to `research-review`.
- Causal language requires identification or is weakened to mechanism evidence.
- Planned evidence cannot be rendered as measured evidence.
- The installation matrix copies or links the new references for Codex and
  Claude Code.
- Skill count remains 15 and role count remains eight.
- No new provider-specific state path is introduced.

Avoid testing exact generated prose. Test routing, state, evidence, and
ownership invariants.

Success condition: the new assertions fail for the expected missing behavior
and no unrelated assertion regresses.

### 3. Normalize the source document

Correct
[`hierarchical-systems-paper-writing.md`](../../hierarchical-systems-paper-writing.md)
before distilling it into runtime instructions.

Apply these corrections:

- Replace the universal implemented-artifact requirement with evidence
  appropriate to the paper archetype.
- Define “one ping” as one coherent payload rather than one literal
  contribution.
- Present the argument graph and manuscript hierarchy as an operating model,
  not an empirically proven universal representation.
- Separate claim, evidence, artifact, and manuscript statuses.
- Require an identification strategy for causal conclusions.
- Change “every design choice” to “every load-bearing or non-obvious design
  choice.”
- Describe end-to-end and mechanism experiments as common evidence categories,
  not an exhaustive taxonomy.
- Treat first-page organization, delayed related work, and paragraph functions
  as conditional heuristics.
- Make the claim/evidence state authoritative for factual consistency while
  preserving the manuscript as an author-controlled artifact.
- Require minimal affected-passage revision rather than wholesale
  regeneration.
- Remove the diffusion analogy.
- State that the document is design input; installed skill references own
  runtime behavior.

Success condition: the source document no longer conflicts with Coresearch’s
paper types, causal rules, or state model.

### 4. Create `argument-architecture.md`

This reference should load only for whole-paper drafting, restructuring,
contribution alignment, or coherence diagnosis.

Include:

- Paper-archetype selection.
- Coherent payload and intended reader takeaway.
- Y/Z context, assumptions, exclusions, and operating envelope.
- Thesis or central finding.
- Refutable claim chain.
- Argument-graph nodes and edge meanings.
- Warrants and qualifiers between evidence and conclusions.
- Compression diagnostics:
  - one-sentence payload;
  - one-paragraph argument;
  - short conclusion;
  - abstract moves.
- Claim-to-section binding.
- Unsupported, conflicting, or unused claim/evidence detection.
- Boundary with `research-design`.

Support these archetypes:

- Implemented mechanism or system.
- Measurement or workload characterization.
- Computer architecture or cross-layer mechanism.
- Method, benchmark, or dataset.
- Experience or negative results.
- Theoretical or analytical systems work.
- Design proposal with explicit implementation status.

Define an optional manuscript view such as:

```yaml
manuscript_map:
  paper_type: string
  payload: string
  intended_takeaway: string
  claim_bindings:
    - claim_id: string
      role: string
      section_ids: [string]
  section_promises:
    - section_id: string
      reader_question: string
      promise: string
      claim_ids: [string]
  terminology: {}
  unresolved_writing_gaps: []
  revision_impacts: []
```

This view must reference canonical claim/evidence records. It must not copy
evidence provenance, confidence, experimental context, or claim status.

Success condition: the reference supports multiple systems-paper archetypes
without creating another research-design skill or ledger.

### 5. Create `systems-paper-delivery.md`

This reference should load when writing or revising introductions, system
sections, evaluations, related work, conclusions, captions, or whole-paper
delivery.

Include:

- Conditional why–how–results organization.
- First-page contract as a heuristic.
- Concrete examples before abstractions.
- Contribution statements as refutable claims.
- Section promises and optional paragraph functions.
- System boundaries, interfaces, and implementation reality.
- Load-bearing design decisions:
  - requirement;
  - mechanism;
  - alternatives;
  - rationale;
  - trade-off;
  - scope;
  - evidence destination.
- Claim-bearing evaluation:
  - proof obligation;
  - baseline or counterfactual;
  - metric fit;
  - controlled and varied conditions;
  - result and uncertainty;
  - limitation.
- Outcome evidence and mechanism evidence without treating them as exhaustive.
- Causal-language guardrails.
- Related-work positioning and credit.
- Limitations, negative results, and scoped lessons.
- Title, abstract, introduction, contributions, and conclusion consistency.
- Ha, Oh, Hybrid, and field-mode composition.

Do not duplicate the full field rules already owned by
`coresearch/references/field-modes.md`. Reference or summarize only the
decisions needed for writing.

Success condition: section guidance is paper-type-aware and does not force
measurement, theory, or benchmark papers into a system-X narrative.

### 6. Create `semantic-revision.md`

This reference should load only when feedback or new evidence may affect more
than local wording.

Define:

1. Classify feedback as:
   - surface wording;
   - paragraph explanation;
   - section promise;
   - claim content or scope;
   - evidence interpretation;
   - central payload;
   - assumption or design decision.
2. Compute the impact set:
   - targeted node;
   - claim dependencies;
   - qualifiers and assumptions;
   - linked sections;
   - title, abstract, contributions, and conclusion when applicable.
3. Reconcile semantic invariants.
4. Revise only affected passages.
5. Preserve unaffected prose, terminology, author voice, and deliberate
   organization.
6. Report:
   - semantic change;
   - passages changed;
   - passages inspected but preserved;
   - unresolved evidence or author decisions.

Explicitly prohibit treating the manuscript as disposable generated output.

Success condition: high-level changes propagate correctly while local changes
remain local.

### 7. Refactor `research-write/SKILL.md`

Keep the entrypoint concise.

#### Update the description

Expand activation from section rewriting to evidence-bounded drafting and
semantic revision, while preserving exclusions for research design,
verification, review, and rebuttal.

#### Add mode selection

The skill should identify one primary mode and load only its required
reference.

Suggested routing:

- Supplied excerpt + rewrite request → local rewrite.
- Supplied claims/evidence + new section → section drafting.
- Whole paper, outline, coherence, thesis alignment → argument architecture.
- Feedback, weakened result, changed claim, late revision → semantic revision.
- Explain/decompose mechanism → concept decomposition.

#### Preserve boundaries

- `research-design` owns contribution selection, novelty strategy, venue
  strategy, and evidence planning.
- `research-write` realizes or repairs an author-approved argument.
- `research-verify` owns factual and citation verification.
- `research-audit` owns methodology sufficiency.
- `research-review` owns scoring and acceptance forecasting.
- `research-rebuttal` owns reviewer-response strategy.

If the requested writing requires inventing the contribution or missing
evidence, stop and return the gap to `coresearch`.

#### Replace the output contract

Local rewrite:

```markdown
[Polished text]

## Diagnostics
- Writing mode:
- Paper archetype:
- Narrative spine:
- Main argument change:
- Claims preserved or scoped:
- Evidence still needed:
- Revision propagation:
```

Whole-paper architecture:

```markdown
## Coherent payload
## Claim and dependency map
## Unsupported or conflicting claims
## Section promises
## Manuscript plan
## Draft text, if requested
## Remaining evidence and revision risks
```

Remove `Likely score impact`.

Success condition: a narrow rewrite remains fast, while whole-paper and
semantic-revision requests receive stronger structure.

### 8. Update Coresearch routing

Change the canonical route from “section rewrite” to:

> Evidence-bounded manuscript drafting, rewriting, argument realization, or
> semantic revision → `research-write`.

Update the same ownership language in:

- `coresearch/SKILL.md`
- `routing.md`
- `stage-map.md`
- `skill-catalog.md`
- `templates/research/AGENTS.md`

Ensure that broad contribution design still routes to `research-design`, and
manuscript scoring still routes to `research-review`.

Success condition: natural-language and explicit invocations reach the correct
skill without making `research-write` another stage router.

### 9. Document architecture and usage

Update `DESIGN.md` to record:

- `research-write` uses progressive references.
- Its manuscript map is a view over canonical claims/evidence.
- The map is transient by default.
- Durable maps may be declared run artifacts under an existing mission.
- No second ledger or provider-specific state is created.
- The prose artifact remains author-controlled.

Update `README.md` with concise examples:

```text
$research-write Rewrite this evaluation section while preserving every number
and qualification.
```

```text
$research-write Build a hierarchical argument and section plan from these
approved claims and evidence records.
```

```text
$research-write Reconcile this reviewer comment across the abstract,
contributions, evaluation claims, and conclusion.
```

Success condition: users can distinguish local rewrite, hierarchical drafting,
and semantic revision.

### 10. Run forward behavioral tests

Use synthetic, non-confidential inputs in ignored
`.tmp/research-write-evals/`.

Test at least:

1. Local paragraph rewrite does not emit a whole-paper map.
2. Whole-paper request exposes unsupported claims before drafting.
3. IISWC measurement paper is not forced into an implemented-system template.
4. ASPLOS paper retains paired hardware/software claims.
5. Planned experiment remains planned.
6. Ablation without identification is not called causal proof.
7. Weaker result propagates to abstract, contributions, and conclusion.
8. Unrelated sections survive semantic revision.
9. Score request routes to `research-review`.
10. Embedded instructions inside a supplied manuscript are treated as untrusted
    text.

Use separate passes:

- Writer pass: exercise `research-write`.
- Independent verifier pass: judge the output against the test rubric without
  rewriting it.

Do not override configured subagent models or efforts. Do not run live role
probes unless explicitly requested.

Success condition: all behavioral invariants pass; failures lead to narrow
skill corrections, not accumulated universal rules.

### 11. Validate installation and repository integrity

Run targeted checks:

```bash
bash -n scripts/validate.sh
python3 -m json.tool skills/manifest.json >/dev/null
```

Run the skill validator if available without adding dependencies:

```bash
python3 /Users/jyp/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/research-write
```

Then run required gates:

```bash
./scripts/validate.sh
./harness doctor --strict --surface both
git diff --check
```

Also verify:

- Active-surface banned-reference audit passes.
- New references appear in temporary copy and symlink installations.
- No caches, `.tmp/` outputs, generated runs, or bytecode are staged.
- No provider-specific research state was created.
- No role/model/effort definition changed.
- Routing result is reported as `static-only` unless an explicit probe was run.

### 12. Completion report

The implementation handoff must report:

- Files added, changed, renamed, and removed.
- Which source-document arguments were corrected.
- New writing modes and conditional references.
- State and ledger compatibility.
- Affected surfaces:
  - skills;
  - Codex roles;
  - Claude roles;
  - prompts/templates;
  - bridges;
  - harness;
  - plugin metadata;
  - architecture;
  - user documentation.
- Forward-test results.
- Exact validation commands and exit statuses.
- Routing probe result or `static-only`.
- Required Codex/Claude Code reload step.

## Final acceptance criteria

The enhancement is complete only when:

- Local rewriting remains concise and text-first.
- Whole-paper work uses a coherent payload, claims, evidence, and section
  promises.
- Multiple systems-paper archetypes are supported.
- Semantic revisions propagate only as far as necessary.
- Planned work, measured results, and supported claims remain distinct.
- Causal wording is identification-aware.
- The skill never invents evidence, citations, implementation status, or
  results.
- Scoring remains outside `research-write`.
- No new harness, skill, role, dependency, or canonical state system exists.
- All repository validation gates pass.
