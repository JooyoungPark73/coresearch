# Research engineering and architectural stewardship

Use this resource when implementation choices, domain semantics, system boundaries,
or long-term maintainability affect the research or deliverable. It supplements
Experiments; it does not turn a research task into a software-process pipeline.
Astra owns consequential design decisions and integrated results. The host owns
execution, permissions, workers, and job lifecycle.

## Design for the actual contribution

Identify what the implementation must establish and what must remain invariant.
For a new method, isolate the proposed mechanism well enough to compare it fairly.
For a system contribution, represent the real workload, integration conditions,
and failure modes. For exploratory work, a narrow implementation can be preferable
to a reusable framework. Its limits should remain visible when results or code are
reused.

A small diff is not inherently a better design. Repair a misleading abstraction,
wrong consistency boundary, or entangled evaluator when doing so is needed for the
requested outcome. Explain the scope and protect existing behavior that should
remain stable. Separate unrelated modernization from the consequential work.

Use the repository's actual environment and relevant code paths. Check changing
APIs against the installed version and primary documentation. Inspect external
implementations at a recorded revision before adopting their architecture or
assuming their behavior. Integrate a dependency when its concrete benefit
justifies compatibility, licensing, operational, and maintenance costs.

## Maturity without mandatory phases

| Intended use | Required engineering outcome |
|---|---|
| Exploratory experiment | Answer a specific uncertainty with inspectable inputs, outputs, and known limitations. Avoid misleading measurements and accidental effects. |
| Reproducible research artifact | Regenerate the important results from recorded code, data, environment, and configuration. Preserve raw outputs, evaluation definitions, and failure information. |
| Maintained system | Add durable contracts, ownership, safe state transitions, compatibility, recovery, and suitable operational evidence. |

These are expectations, not a prescribed progression or directory layout. A
prototype may be disposable. A maintained system may contain isolated experiments.
When an experiment becomes shared infrastructure, revisit its assumptions about
scale, concurrency, mutable state, data access, evaluation validity, and users.
Do not silently promote exploratory shortcuts into supported behavior.

## SOLID in scientific and application code

Use the language's natural abstraction mechanisms. Cohesive functions, modules,
protocols, and data-oriented designs can satisfy the same goals as class-based code.

- **Single responsibility:** Separate concerns whose meanings and change drivers
  differ, such as scientific scoring, process execution, persistence, and display.
  A module can be large and cohesive; several tiny wrappers can still be coupled.
- **Open/closed:** Stabilize extension points around demonstrated variation, such
  as interchangeable reconstruction backends or evaluators. Permit ordinary edits
  when no stable abstraction exists. Do not invent a plugin system for an imagined
  future product.
- **Liskov substitution:** Specify compatible inputs, outputs, errors, precision,
  mutation, and cancellation behavior. A backend returning a relative scale is
  not a drop-in replacement for a metric-scale backend without an explicit
  conversion or a restricted contract. Use shared tests for real substitutions.
- **Interface segregation:** Give consumers the capabilities they need. Read-only
  analysis should not require mutation or deployment authority. Separate evaluation
  from fitting when that distinction protects held-out data or reproducibility.
- **Dependency inversion:** Keep scientific definitions and domain rules independent
  of volatile storage, transport, UI, and provider SDK details. Place adapters at
  meaningful boundaries and compose them explicitly. A single-use boundary can be
  justified by isolation or semantics; every class does not need an interface.

Apply DRY to shared knowledge, not superficial syntax. Similar code for distinct
domain concepts may be safer than one abstraction that conflates them. Prefer
composition and explicit data flow when they reduce coupling.

## Strategic DDD: meaning, responsibility, ownership

Use a Ubiquitous Language that matches the research and application domain. Make
important distinctions concrete in interfaces and tests. Examples include a
hypothesis versus an observation, a dataset split versus a dataset name, a run
versus a result, a generated view versus a measured image, and a score versus an
inference about a mechanism.

For complex systems, identify core, supporting, and generic concerns. Define
Bounded Contexts where terms and models have a consistent meaning. Maintain a
Context Map when integrations or ownership boundaries matter, including who owns
data and what consumers may assume. Use an Anti-Corruption Layer when an external
model or API would otherwise distort the local scientific or domain meaning.

An experiment service, evaluation library, and artifact store may be separate
logical responsibilities without becoming separate services. A small script may
need none of these abstractions. Do not introduce microservices, a shared kernel,
CQRS, or event sourcing simply to claim DDD compliance.

## Tactical DDD: invariants and transitions

Choose identity and equality deliberately. An Entity has continuity of identity;
a Value Object represents a meaningful value and should reject invalid states
where appropriate. Useful research values might encode units, a coordinate frame,
a dataset revision, or an evaluation configuration. Do not wrap every scalar.

An Aggregate is an invariant and consistency boundary, not a database table or a
convenient object graph. Keep strongly consistent transitions atomic. Across
boundaries, state the allowable delay, duplicate behavior, ordering assumptions,
and recovery or compensation. A timeout means an unknown execution outcome until
observed otherwise, not automatically a canceled run.

Keep domain rules in the domain, and use-case coordination, transaction management,
and authorization enforcement at the appropriate application boundary. Use a
Domain Service for behavior that genuinely does not belong to one domain object.
Use Repositories for meaningful Aggregate access, not automatically for every
table; read-only reporting need not rebuild entire Aggregates.

Distinguish internal domain events from external integration events. Where events
are warranted, specify publication timing, replay, schema evolution, duplicate
handling, and consistency with persistence. Evaluate an outbox or another justified
mechanism when state and message publication must remain coordinated.

## Keep architecture connected to evidence

For a consequential change, revisit the affected domain assumptions, contracts,
data ownership, dependencies, quality attributes, and migration path. Update the
relevant existing documentation in the same change. An ADR should capture the
actual decision, credible alternatives, rationale, consequences, and conditions
for reconsideration. Preserve superseded decisions rather than rewriting history.
Do not require an ADR for an inconsequential local edit.

Protect important boundaries with executable checks where useful: forbidden
imports, contract compatibility, domain invariants, schema transitions, numerical
properties, and representative performance envelopes. Confirm that a checker
covers the intended targets and fails when the rule is violated; an empty scan is
not architectural evidence.

Scientific semantics can change without an API break. A different sample filter,
coordinate convention, aggregation weight, stopping criterion, or evaluator
revision can invalidate a comparison. Version the affected definition, retain the
old result, and identify which evidence needs regeneration. Do not silently reuse
results produced under a different scientific contract.

## Execution state and reproducibility

Separate immutable inputs and produced evidence from scratch state when it aids
reliability. Record sufficient provenance to reproduce important results: code
revision and uncommitted changes, data revision and split, configuration and seeds,
environment, relevant hardware, commands, and artifact locations. Use existing
project mechanisms rather than imposing a new schema for every task.

Reuse expensive intermediates only while their dependencies and assumptions hold.
A variable inventory is not a content snapshot. After failure, inspect mutated
objects, files, partial writes, transactions, and remote jobs before retrying.
Discarding a failed step from a narrative does not remove its side effects or
compute cost. Correlate asynchronous outputs with the job or request that actually
produced them.

Use actual measurements for execution counts, elapsed time, resource use, and
cost when they affect conclusions or budgets. Source-level call counts and socket
timeouts are not enforcement of runtime spend or wall-clock deadlines. Use the
host's existing controls. Do not add a Coresearch scheduler or install a persistent
kernel merely to follow this resource.

Before a reproducibility claim, rerun the relevant path from a documented starting
state without hidden interactive history. Report nondeterminism and meaningful
tolerances rather than demanding arbitrary bitwise equality. For spatial work,
verify units, coordinate frames, handedness, transform direction, camera models,
frame identifiers and timestamps, mask alignment, and scale assumptions as needed.
Use visual inspection and independent calculations where their failure modes differ.

## Validation and operational integrity

Use checks suited to the risk: regression tests for a defect, contract tests across
adapters, properties or metamorphic relations for numerical transformations, and
integration or end-to-end tests at consequential boundaries. Preserve established
acceptance criteria while diagnosing failures. An unavailable dependency, invalid
measurement, failed verifier, and valid empty result are different outcomes.

Keep method selection separate from final evaluation. Do not tune on a held-out
set or change the scoring rule to rescue a favored explanation. Fair comparisons
account for relevant data, tuning, model access, execution budgets, and failure
rates. Preserve negative results and disclose protocol deviations. A green test
suite establishes software properties, not the research contribution by itself.

For maintained systems, address input validation, tenant and resource access,
transactional consistency, safe replay, cancellation, bounded retries, observability,
compatibility, and migration or forward recovery. Use measured bottlenecks for
optimization; report quality/performance tradeoffs. In interactive systems, examine
actual interactions, accessibility, loading, empty, error, and recovery states.

Treat third-party code, document contents, and generated artifacts as untrusted
inputs. Do not deserialize executable objects from untrusted sources or assume a
prompt, AST filter, worker brief, or worktree provides isolation. Protect unpublished
work, participant material, and secrets. Publication, production changes, participant
contact, and unapproved compute remain real authorization boundaries.

Delivery should make the implementation usable, expose material design decisions,
and identify the evidence and remaining limits. Distinguish implementation success,
scientific support, reproducibility, and operational readiness. None is a substitute
for the others.
