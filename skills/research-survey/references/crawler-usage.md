# Crawler usage

Use `crawler.py` only for a verified full-text collection workflow; ordinary
searches do not need it. Inspect `--help`, run a dry run, and review the plan
before downloads or API use.

Prefer publisher, proceedings, DOI, arXiv, OpenReview, author, or other
open-access primary sources. Respect access controls, licenses, rate limits,
privacy, and repository policy. Never bypass authentication or upload private
papers, reviews, or credentials to an external service.

Start with a narrow query and explicit inclusion criteria. A roadmap may target
up to 30 papers, but volume is not a completeness claim. Deduplicate by stable
identifier and title/author evidence. Keep metadata discovery separate from PDF
verification, and preserve failed retrievals rather than inventing missing
fields.

For every retained paper, record discovery source, canonical identifier,
verification status, local or official source location, and extraction status.
Inspect a sample before scaling. Stop when the stated coverage criterion is met,
new results cease changing the literature map, or access/quality limits make
further retrieval misleading.
