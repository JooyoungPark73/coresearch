# Literature and sources

The useful product is a defensible synthesis: scope, competing approaches,
closest relevant work, evidence for the distinctions, and remaining uncertainty.
Organize by the research question or mechanism rather than a list of abstracts.
A novelty claim needs an active search for counterexamples, not just missing hits.

For sources that matter to a conclusion, retain the identifier and version,
bibliographic metadata, a page/section/table locator, and the claim supported.
Distinguish metadata-only records from inspected full text; downloading does not
upgrade either. Disagreement between versions or sources belongs in the synthesis.
Independent evidence means independent data or groups, not merely more citations.
Use primary sources for precise claims and current official rules for venue advice.

Existing notes, a small table, or a bibliography are sufficient. No compulsory
source-state schema or minimum paper count is imposed. For a large collection,
delegate discovery and metadata checks, then inspect the load-bearing evidence
and adjudicate contradictions at the lead level.

## Optional batch PDF retrieval

Search and metadata matching belong to the agent's available search tools.
The bundled `../scripts/fetch_sources.py` only downloads explicit HTTPS PDF URLs.
Resolve its path relative to this skill, including when installed elsewhere.

Input is a JSON array; each entry needs a unique lowercase slug `id`, a `title`,
a direct `url`, and `access: "open"`. Extra bibliographic fields are preserved.
`open` records the curator's access decision; it is not an automated rights check.

```json
[
  {"id": "paper-1", "title": "Verified paper title", "url": "https://example.org/paper.pdf", "access": "open"}
]
```

The URL above is a placeholder, not a real paper. For a prepared manifest:

```bash
python3 <skill-dir>/scripts/fetch_sources.py sources.json --output research/pdfs --dry-run
python3 <skill-dir>/scripts/fetch_sources.py sources.json --output research/pdfs
```

Dry-run validates without network or writes; it is optional, not an approval gate.
Real retrieval requires a **new output directory** and writes `report.json` with
requested/final URLs, timestamps, byte counts, SHA-256 hashes, and per-source
outcomes. Partial failure returns exit code 1 while retaining successes. Retry
only failed entries into a new directory. Inputs/configuration errors return 2.

Defaults: 25 MiB per PDF, 30-second socket timeout, at most five redirects.
`--max-bytes` and `--timeout` override the first two. Public IPs are pinned for
TLS connections; redirects are checked again. No proxies, cookies, publisher
scraping, paywall bypass, or automatic retries. DNS resolution is OS-managed;
this is not a hard process deadline. Use the host's process limits when needed.
PDF signature and transport checks are not full document validation. Inspect
retrieved documents against their bibliographic identities before using them.
