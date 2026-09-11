---
name: research-survey
description: Find and synthesize verified literature, closest work, and conflicting findings.
---

# Research survey

Produce a source-faithful literature synthesis at the requested scope.

| Mode | Use when | Guidance |
| --- | --- | --- |
| **Literature map** | discovering papers, closest work, or related-work categories | group verified sources by mechanism, stream, or comparison dimension |
| **Conflict synthesis** | credible findings disagree after contexts are normalized | [conflict-synthesis.md](references/conflict-synthesis.md) |

Verify papers through primary sources. Titles and search snippets are discovery
leads, never evidence of methods or results. Record each paper as `PDF VERIFIED`,
`FULL TEXT VERIFIED`, `METADATA VERIFIED`, `PARTIALLY VERIFIED`, or `NOT FOUND`.
Metadata-only records cannot support detailed method, result, limitation, or
comparability claims.

Bind extracted claims to exact support locators and relevant context: workload
or dataset, platform, scale, baseline, metric, method, results, and limitations.
Use [evidence-grounding.md](../coresearch/references/evidence-grounding.md) for
claim-bearing extraction and [field-modes.md](../coresearch/references/field-modes.md)
when field controls affect comparability. Read
[crawler-usage.md](references/crawler-usage.md) only when using the local crawler.

Scale search coverage and stopping criteria to the question. Closest-work or
novelty searches must consider alternate terminology, adjacent work, negative
results, and counterevidence. Absence from retrieval is not proof of absence.
Do not manufacture disagreement from aligned or incomparable findings.

Return the requested synthesis with enough source, verification, context, and
locator information to audit it. Distinguish direct competitors, enabling work,
adjacent work, and unresolved evidence; state coverage gaps and confidence.
Provide BibTeX or durable files only when requested or mission-declared.

Contribution decisions, experiment design, independent methodology audits, and
manuscript writing return through Coresearch to their owning stage.
