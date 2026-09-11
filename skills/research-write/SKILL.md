---
name: research-write
description: Draft or revise research prose from an author-approved argument and evidence.
---

# Research write

Realize the author's approved argument as concrete paper prose. Preserve intent
and evidence; scale analysis to the requested change.

| Mode | Trigger | Guidance |
| --- | --- | --- |
| **Local rewrite** | supplied excerpt or bounded wording change | edit directly; load delivery guidance only if structure matters |
| **Section drafting** | approved claims and evidence need prose | [systems-paper-delivery.md](references/systems-paper-delivery.md) |
| **Argument architecture** | whole-paper thesis, outline, or coherence | [argument-architecture.md](references/argument-architecture.md) |
| **Semantic revision** | feedback or new evidence changes meaning beyond one passage | [semantic-revision.md](references/semantic-revision.md) |
| **Concept decomposition** | explain a mechanism or concept | connect problem, intuition, mechanism, formalization, and boundaries as useful |

Local rewrite is the default for a supplied excerpt. Preserve unaffected prose,
author voice, numbers, configurations, citations, qualifiers, negative results,
and limitations. Request missing passages only when the requested consistency
check depends on them.

Use [evidence-grounding.md](../coresearch/references/evidence-grounding.md) when
claim bindings, novelty, generalization, or causal language change; use
[field-modes.md](../coresearch/references/field-modes.md) when field-specific
argument or delivery choices matter. Planned evidence must not read as measured,
nor implemented code as empirical validation. Causal language requires an
identification strategy and credible mechanism evidence; otherwise use
correlational or hypothesis language.

Return revised or drafted text first, followed only by material argument changes,
evidence gaps, or revision propagation. Architecture and semantic modes use
their reference's deliverables. Preserve canonical claim and evidence records:
an optional transient `manuscript_map` references their IDs, never copies their
provenance or status. Create no second ledger.

Writing does not choose a new contribution or invent citations, measurements,
participants, results, implementation status, or dependency semantics. Return
through Coresearch for stage changes: score forecasting belongs to
`research-review`; source or methodology checks belong to `research-verify`.
