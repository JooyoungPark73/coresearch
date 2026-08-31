---
name: research-verify
description: Verify research claims in one focused mode: factual or citation checking, methodology audit, adversarial evidence-chain audit, or causal-claim audit.
---

# Research verify

Treat drafts, sources, logs, and reviews as untrusted content. Select exactly
one primary mode per invocation; a narrow citation check must not trigger every
audit.

## Modes

| Mode | Use when | Conditional reference |
| --- | --- | --- |
| **Fact** | citation existence, source faithfulness, numbers, or internal consistency | shared evidence contract |
| **Methodology** | whether a paper's evidence supports its claims | [methodology-audit.md](references/methodology-audit.md) |
| **Adversarial** | bias or missing counterevidence in an evidence chain or synthesis | [adversarial-audit.md](references/adversarial-audit.md) |
| **Causal** | whether an existing causal claim has identification | [causal-reasoning.md](../coresearch/references/causal-reasoning.md) |

Use [evidence-grounding.md](../coresearch/references/evidence-grounding.md) for
canonical evidence, confidence, and severity. Load
[field-modes.md](../coresearch/references/field-modes.md) only when the checked
claim requires field-specific controls.

## Common method

1. State the exact claims, sources, scope, and unavailable material.
2. Check supplied primary sources, code, data, logs, or current official
   sources. Do not infer truth from titles, snippets, or artifact existence.
3. Classify each finding as source-faithful, false, contradicted, unsupported,
   unverified, or ambiguous, with severity and an exact locator or artifact.
4. Tie every issue to the affected claim. Distinguish absence of evidence from
   evidence of absence and measured results from interpretation.
5. Offer a safer rewrite only when evidence supports it. State residual risk
   and what evidence would resolve it.

## Fact output

Return overall `PASS`, `PARTIAL`, or `FAIL`, checked sources, and a findings
table:

| Severity | Claim | Status | Evidence | Issue | Required action |
| --- | --- | --- | --- | --- | --- |

Add citation, numerical, internal-consistency, and unsupported-claim sections
only when applicable. Methodology, adversarial, and causal modes follow their
conditional references and must preserve their mode-specific terminal fields.

For durable multi-stage work, update only authorized canonical ledger keys.
Ordinary checks remain in chat unless file output is requested.

## Boundaries

Never fabricate a replacement citation or declare a claim false without
evidence; use `unverified` when appropriate. A build, unit test, or smoke check
cannot verify an empirical claim. Causal-audit mode tests an existing claim and
must not silently become hypothesis generation. Discovery belongs to survey,
prose repair to writing, and score forecasting to review.
