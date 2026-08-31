---
name: research-survey
description: Find, verify, classify, and synthesize real literature as a map or conflict analysis; never infer paper metadata, methods, or results from titles and snippets.
---

# Research survey

Produce a source-faithful literature map. Default to map mode; use conflict
synthesis only when the evidence contains a material disagreement.

## Modes

| Mode | Use when | Output |
| --- | --- | --- |
| **Literature map** | related work, paper discovery, closest competitors, or citation categories | verified source table and thematic synthesis |
| **Conflict synthesis** | credible findings disagree after contexts are normalized | load [conflict-synthesis.md](references/conflict-synthesis.md) |

Use [crawler-usage.md](references/crawler-usage.md) only when the local crawler
is useful. Use [evidence-grounding.md](../coresearch/references/evidence-grounding.md)
for claim-bearing extraction and [field-modes.md](../coresearch/references/field-modes.md)
when comparability depends on field-specific controls.

## Method

1. Define the question, inclusion and exclusion criteria, time range,
   terminology variants, adjacent fields, and stopping rule.
2. Search broadly, then verify each paper through a primary source. Prefer
   publisher, proceedings, DOI, arXiv, OpenReview, author PDF, or official
   artifact pages. Search snippets are discovery leads, not evidence.
3. Record per-paper verification status: `PDF VERIFIED`, `FULL TEXT VERIFIED`,
   `METADATA VERIFIED`, `PARTIALLY VERIFIED`, or `NOT FOUND`. Metadata-only
   records cannot support detailed method, result, limitation, or
   comparability claims.
4. Extract normalized claims and contexts: workload or dataset, platform,
   scale, baseline, metric, method, result, limitations, and exact support
   locator. Never infer bibliographic or result details from a title or snippet.
5. Group by research stream, mechanism, or comparison dimension—not one
   paragraph per paper. Separate direct competitors, enabling work, adjacent
   work, and unresolved evidence.
6. Search explicitly for closest work, negative results, and contradictory
   evidence. State coverage limits and confidence; absence from retrieval is
   not proof of absence.

## Output

Return the requested survey first, then the minimum evidence table needed to
audit it:

| Paper | Verification | Category | Claim supported | Context | Locator | Limits |
| --- | --- | --- | --- | --- | --- | --- |

Follow with synthesis by stream, closest-work comparison, contradictions or
open questions, coverage gaps, and confidence. Provide BibTeX or durable files
only when requested. If no genuine disagreement exists, do not manufacture a
conflict narrative; report the aligned or incomparable evidence instead.

## Boundaries

Survey discovers and synthesizes sources; it does not decide whether an
opportunity is important, design experiments, audit a paper's methodology, or
write unsupported novelty prose. Route those stages back through Coresearch.
