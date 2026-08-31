# Semantic Revision

Read this reference when feedback, a changed result, or a new limitation may
affect more than local wording. The manuscript is author-controlled; do not
treat it as disposable generated output.

## Classify the change

Locate the semantic level before editing:

1. surface wording or grammar;
2. paragraph explanation or example;
3. section reader question, promise, or organization;
4. claim content, scope, qualifier, or evidence binding;
5. evidence interpretation or implementation/study reality;
6. coherent payload or intended takeaway;
7. assumption or design decision shared by several claims.

The physical location of a comment does not determine its semantic level. A
sentence comment may expose a paper-level objection; a terminology correction
may be genuinely local.

## Compute the impact set

Start with the targeted node and inspect only its relevant graph neighborhood:

- ancestors and dependent claims;
- assumptions, qualifiers, warrants, and credible counterevidence;
- bound section promises and paragraphs;
- terminology and system/interface boundaries;
- title, abstract, introduction, contributions, and conclusion when the
  coherent payload or claim strength changes.

Record passages as `change`, `inspect`, or `unaffected`. The impact set may be
one sentence; do not require nonzero edits elsewhere when consistency already
holds.

## Reconcile before rewriting

1. Restate the semantic change using the evidence-supported strength.
2. Update the transient manuscript map or identify the canonical claim/evidence
   owner that must change. `research-write` must not silently mutate a research
   claim owned by another stage.
3. Resolve contradictions among the affected payload, claims, scopes, section
   promises, and terminology.
4. Revise only affected passages after the semantic representation is
   coherent.
5. Preserve unaffected prose, author voice, citations, numbers, qualifiers,
   and deliberate organization.
6. Run global invariants only at the level justified by the impact set.

If a result weakens, inspect every passage that states or compresses that
result. If an example changes without altering the claim, revise the example
and local explanation only. If a reviewer misunderstood a claim, determine
whether the state, exposition, or both are defective before rewriting.

If the user supplies a semantic delta or affected-location list without the
original text, request the missing passages before producing full replacement
prose. You may provide bounded replacement clauses that restate only the exact
approved claim, number, qualifier, and scope supplied by the user; do not
invent surrounding sentences, citations, transitions, or section content.

## Global invariants

After a substantive revision, verify as applicable:

- title, abstract, introduction, contributions, and conclusion express the
  same supported payload;
- every affected claim retains evidence and correct scope;
- section promises match what the revised sections establish;
- evaluation conclusions match reported results and uncertainty;
- implementation/study boundaries and terminology remain consistent;
- no planned or hypothetical result is rendered as fact;
- causal or generalization language still satisfies its evidence contract.

## Output

Return the revised affected passages followed by:

```markdown
## Revision impact
- Semantic change: [supported restatement]
- Passages changed: [locations and purpose]
- Passages inspected but preserved: [locations and why unchanged]
- Claims or evidence requiring author action: [items / none]
```

Do not use score movement as a writing diagnostic. A score forecast belongs to
`research-review`; reviewer-response planning uses its response mode.
