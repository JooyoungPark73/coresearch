---
name: research-survey
description: Verified literature survey and related-work synthesis for systems/cloud, ML-systems, and computer-architecture topics. Use when the user asks for related work, papers on a topic, citation categories, a literature map, survey writing, or paper recommendations. Requires real-paper verification, crawler-compatible evidence tables when useful, and explicit metadata/PDF confidence; never fabricates citations, venues, or paper claims.
---

# research-survey — Literature Survey & Related Work

Find, verify, classify, synthesize real papers — real papers, not inferred
papers. Default is an in-chat Markdown survey; LaTeX/BibTeX only on request.

## What & When

Verified related work, literature maps, paper recommendations, citation
categories, survey prose, closest-competitor search for `systems_cloud` (OSDI,
SOSP, NSDI, EuroSys, SoCC), `ml_systems` (MLSys), `computer_architecture`
(ISCA, MICRO, HPCA, IISWC), and ASPLOS `cross_layer` work, crawler roadmaps when full-text verification is needed. Use when:
"related work", "papers on X", "literature map", "survey", "citation
categories", "closest competitors", "what should I cite".
Not for: batch PDF download → in-skill crawler
(`skills/research-survey/crawler.py`); contribution planning → `research-design`;
fixed draft/source fact-check → `research-verify`; gaps worth a paper
(importance × tractability × novelty, with falsification) → `research-gap`.
research-survey maps the field; it does not judge or falsify gaps.
Research-qualitative work is included only as an optional method stream when it
directly informs the scoped systems question, not as a primary field mode.

## Procedure

Verify existence and metadata before citing. Synthesize by mechanism, research
question, field object, contribution type, or evaluation regime — never chronology by default.
Keep metadata-only papers out of detailed method/result/limitation claims.

**Search policy.** OMX `researcher` posture when available: official /
proceedings / source-backed first, version/date awareness, links in the final
answer. Prefer primary sources: (1) paper PDFs, publisher pages,
arXiv/OpenReview/ACM/IEEE/official proceedings; (2) DBLP, Semantic Scholar,
OpenReview, Google Scholar snippets when accessible; (3) project pages/blogs
only as secondary evidence. Do not cite without verified existence and key
metadata.

**Verification status — assign to every paper; this is the skill's axis:**

- `PDF VERIFIED` — full text or PDF retrieved and inspected, and the survey claim is supported by that text.
- `FULL TEXT VERIFIED` — official HTML/full-text page inspected when no PDF is needed or available.
- `METADATA VERIFIED` — title, authors, venue/year, source link verified, but paper text not inspected; only existence, bibliographic, or high-level positioning claims.
- `PARTIALLY VERIFIED` — some metadata unresolved or conflicting; not a closest-competitor claim without caveat.
- `NOT FOUND` — candidate or manual-follow-up item; do not cite as established work.

Uncertain metadata → `PARTIALLY VERIFIED`. Never infer methods, results, venue,
or contribution from a title, citation graph, abstract snippet, or model memory.
Never upgrade beyond `METADATA VERIFIED` without inspected paper text.

**Workflow:**

1. **Scope** — topic, venue community, time window, desired depth. Ask one question only if scope is impossible to infer.
2. **Search broadly** — multiple query formulations and adjacent terms.
3. **Evidence ledger** — candidates in a crawler-compatible roadmap table (or equivalent in-chat table) before synthesis.
4. **Verify each candidate** — title, authors, venue/year, DOI/arXiv/OpenReview/proceedings link when possible; assign verification status.
5. **Crawl or inspect text when needed** — crawler for batch open-access PDFs when a roadmap file exists; otherwise inspect official PDFs/full text directly.
6. **Classify** — group by mechanism, research question, contribution type, or evaluation regime, not chronology. Use the canonical mode/lens vocabulary when useful: `systems_cloud`, `ml_systems`, `computer_architecture`; `general_systems`, `networked_distributed`, `cloud`, `cross_layer`, `workload_characterization`.
7. **Synthesize from evidence** — what each stream enabled, its assumptions, and how the user's project differs or builds on it. For claim-bearing comparisons, extract only from inspected text: workload representativeness and operating envelope; baseline/configuration fairness; warmup/repetitions and tail treatment; scale/failure/cloud variance; ML quality parity; simulator fidelity and PPA methodology. Metadata-only papers stay out of these detailed claims.
8. **Identify risks** — closest competitors, missing citations, novelty overlap, weak positioning.
9. **Output sources** — links used + crawler command/output summary when run.

**Inclusion.** No rigid citation-count threshold unless the user asks. Include
directly competing work even if not highly cited; foundational work; recent or
concurrent work; strong surveys with useful taxonomies; official benchmarks or
datasets when relevant.

**Crawler workflow** — when exactness matters, the user says "don't assume", or
the task asks for a paper list/roadmap:

1. Build or request a roadmap table in the crawler's format:

   ```markdown
   | # | 제목 | 저자 | 저널/학회 | 비고 |
   |---|---|---|---|---|
   | 1 | Paper Title | First Author et al. | Venue/Journal | Year; DOI/arXiv/OpenReview/proceedings link |
   ```

2. Dry run first:

   ```bash
   python3 skills/research-survey/crawler.py "<path-to-roadmap.md>" --dry-run    # dev (repo root)
   python3 "<SKILLS_DIR>/research-survey/crawler.py" "<path-to-roadmap.md>" --dry-run   # installed
   ```

   `<SKILLS_DIR>` is your installed skills root (`~/.codex/skills` or project `.codex/skills`); resolve the crawler relative to the `research-survey` skill folder.

3. For real downloads, follow guardrails exactly: open-access sources by default, no paywall bypassing, `--allow-publisher-pdf` only for legitimately accessible publisher PDFs, fuzzy DOI matches are candidates only, and lists over 30 papers require reviewed dry-run output plus `--yes-large`.
4. Use downloaded PDFs in `pdf/` next to the roadmap, official full-text pages, or verified source PDFs as the basis for method/result/limitation claims.
5. If the user only requested an in-chat survey and did not request file writes/downloads, do not create files solely for process — include a `PDF Crawl Roadmap` table that can be saved and passed to the crawler.

## Output

```markdown
# Literature Map — [Topic]

## Scope
- Topic:
- Venue/community lens:
- Search status: [verified / partial]
- Inclusion rule:
- Evidence standard: [PDF/full-text inspected / metadata-only allowed with caveats]
- PDF crawl status: [not needed / roadmap provided / dry run / downloaded / partial]

## Taxonomy
1. [Stream]: [what this stream studies or enables]
2. [Stream]: [what this stream studies or enables]

## Paper Table
| Paper | Authors | Venue/Year | Link | Category | Why it matters | Verification status | PDF status |
|---|---|---|---|---|---|---|---|

## PDF Crawl Roadmap
Use this when PDFs should be fetched with the crawler; omit if no crawl/download workflow is needed.

| # | 제목 | 저자 | 저널/학회 | 비고 |
|---|---|---|---|---|

## Synthesis by Stream
### [Stream]
[What it enabled, common assumptions, representative papers, and relation to the user's work.]

## Closest Competitors
| Paper | Overlap | Difference | Risk level |
|---|---|---|---|

## Missing Citation Categories
- [Category and why it matters]

## Positioning Recommendation
[How to phrase the contribution without overclaiming.]

## Open Questions
- [Research gap or uncertainty]

## Sources Used
- [Links]

## Verification Notes
- crawler command/output summary if run:
- Metadata-only papers and why:
- Not-found/manual-access papers:
```

## Reject when

Before final output, reject or fix:

- invented title or venue;
- arXiv year confused with publication year;
- guessed author list;
- paper-result claim not supported by its abstract, paper text, or verified metadata;
- method/result/limitation claim from a metadata-only paper;
- evaluation-comparability claim (workload/envelope, configuration fairness,
  repetitions/tails, scale/failures/variance, quality parity, simulator fidelity,
  or PPA) not supported by inspected full text;
- engineering implementation status presented as the paper's research insight;
- fuzzy crawler or DOI match treated as a verified paper;
- crawler "not found" paper cited as established evidence unless independently verified elsewhere;
- `PDF VERIFIED` or `FULL TEXT VERIFIED` marked without actually inspecting local PDFs or official full text;
- any uncertainty left unmarked.

## State & Handoff

State: every paper carries a `verification_status`; never upgrade without the
matching evidence (PDF inspected / full text inspected / metadata confirmed).
Next: research-gap (map → gaps) / research-audit (load-bearing paper) /
research-verify (one-citation fact check) / research-design (contribution
planning). Artifacts: in-chat literature map, optional roadmap `.md` + `pdf/`
when a crawl was run. Carry forward not-found and partially-verified papers as
manual follow-ups.

In a multi-skill run, also write `source_state` per paper to the orchestrator ledger (state-ledger.md), mapping verification_status → state (PDF VERIFIED / FULL TEXT VERIFIED → fully_read; METADATA VERIFIED → screened; PARTIALLY VERIFIED → retrieved; NOT FOUND → missing).

Re-entry: return to `coresearch` to re-route the next stage.
