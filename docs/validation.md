# Validation

Run from the checkout:

```bash
python3 -B -m unittest discover -s tests -v
```

## Automated contracts

The suite uses real temporary files and subprocess CLI calls, with HTTP/DNS/TLS
boundaries mocked. It covers copies and links, idempotency, refusal of conflicts
and recursive installs, preservation of host prompts and existing briefs,
cleanup after copy failure, publish-last skill metadata, and a copied utility
running outside the checkout.

Source tests cover manifest validation, byte/hash provenance, relative redirects,
redirect revalidation and limits, mixed public/private DNS answers, IP-pinned TLS
with the original hostname, private/reserved/multicast targets, invalid schemes
and credentials, timeouts, bad PDF signatures, truncated and oversized responses,
partial-batch reports, interruption, and refusal to reuse output directories.
Dry-run performs no network requests or writes.

Bundle tests check local Markdown links, one discoverable skill, routing-only
frontmatter, portable dependencies, and an installed end-to-end fixture workflow.
This is software integration testing, **not** an evaluation of a model's research
quality. The PDF transport fixture is synthetic and is never represented as a
real publication or verified scientific evidence.

## Host scenarios

These are acceptance scenarios for a configured model host, not a mandatory
workflow and not claims that live agents were exercised by the unit tests.

| Scenario | Expected behavior and evidence |
|---|---|
| One citation correction | Inspect the relevant source and edit the claim directly. No project initialization, worker, whole-repo preload, or stage re-entry. |
| Broad research idea to experiment | Astra chooses a discriminating experiment. A bounded worker may implement/test it. Actual commands and results support the final interpretation, including negative evidence. |
| Independent literature collection | Workers get disjoint search scopes and return source locators, verification limits, and compact findings. Astra resolves overlap and contradictory results without ingesting full transcripts. |
| Manuscript/rebuttal | Reuse the existing draft. Separate proposed changes from implemented ones and unrun experiments from results. Finish revisions and verification within authorization. |
| Resuming a project | Read the relevant brief/artifacts, not every skill. Preserve rejected directions and uncertainty; update notes only as needed. |
| No worker or search tool available | Do supported work directly; state any evidence gap rather than invent a worker result, citation, or successful experiment. |
| A consequential permission boundary | Continue safe independent work, but do not publish, expose restricted data, or consume unapproved resources. Ask only for the unresolved decision. |
| Research prototype becomes shared infrastructure | Revisit domain meaning, ownership, contracts, reproducibility, and recovery. Load Engineering only where it helps; do not impose a framework on a disposable experiment. |
| An evaluator changes without an API break | Identify changed scientific assumptions, retain prior results, and rerun affected comparisons. A software test pass must not conceal invalidated research evidence. |
| Substantial worker assignment without blockers | Worker completes local execution, inspection, tests, and repair without periodic lead check-ins; the lead consumes an evidence-bearing completion artifact. |
| Expensive run depends on an uncertain pilot | Inspect the pilot at the agreed decision boundary before committing resources. Low communication is not permission to skip scientific validation. |
| Worker invalidates a shared assumption | Send the changed fact, evidence, and decision needed promptly; continue unrelated safe work. Do not wait for a timer or silently change the shared contract. |
| Missing completion or unavailable mixed-model routing | Use actual host recovery or supported direct work. Do not infer success from silence, duplicate a live job, or claim an Astra/Sol topology the host cannot supply. |

Evaluate both the quality of the deliverable and overhead: unnecessary loaded
references, worker launches, repeated status checks, and user approvals. No
numerical performance improvement is claimed without comparative host runs.

## Comparative host evaluation, not a prescribed workflow

Use representative tasks with real acceptance criteria: a coupled research/design
problem, an independently implementable component, and an evidence-conflict or
methodology audit. Include a cheap task where delegation should be unnecessary.
Keep inputs, tools, permissions, output requirements, and evaluator fixed.
Record exact model/version, reasoning setting, prompt revision, cache treatment,
and resource limits. Equal setting names do not imply equal compute across models.

Compare the following candidates where the host actually supports them:

| Configuration | Question tested |
|---|---|
| Direct Astra | Does keeping judgment and execution together avoid decomposition loss? |
| Direct GPT-6.1 Sol | Does the lower-cost model satisfy the same quality bar without lead overhead? |
| Astra lead plus Sol workers, event-driven | Do coarse independent assignments add useful parallelism or specialization after briefing and integration? |
| Same lead/workers and assignments, with scheduled check-ins | Does additional communication prevent enough rework to offset its interruption and coordination cost? |

The last pair isolates communication policy more closely than comparing different
models and messaging schedules together. It is an experimental control, not the
recommended production default. Counterbalance execution order and repeat tasks
where practical; keep outputs separate to avoid cross-condition leakage. Review
artifacts without configuration labels when feasible.

Report validity/completion, missed counterevidence, regressions, integration rework,
wall-clock time to a valid deliverable, and total measured spend. Include lead and
worker input/output/reasoning usage when available, cached input, tool/GPU costs,
failures and retries, coordination messages, lead interventions, and waiting time.
Separate actual billing from estimates and distinguish supervision telemetry from
model-facing traffic. A lower message count, a faster wrong answer, or an incomplete
cheap run is not a win. Compare quality under a budget and cost to reach a quality
threshold; choose deployment settings from the resulting tradeoff, not a model name.

These are evaluation instructions only. Offline bundle tests do not run models or
establish that Astra is the optimal lead, that Sol is an optimal worker, or that
check-ins reduce quality. Record actual host experiments separately.

## Final-review boundary

The redesign can be reviewed structurally: one payload, no runtime dependencies,
no orchestration or prompt injection, explicit lead/worker responsibility, and
research standards available on demand. The tests establish those software
contracts. Live Astra/Claude delegation, external publisher availability, and
host skill-discovery behavior additionally require the user's configured runtime
and authorized network. Record those runs separately rather than treating an
offline test pass as proof of them.
