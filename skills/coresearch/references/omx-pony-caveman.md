# OMX, Ponytail, Caveman

## Ponytail

Use minimal code, not toy output. For research code, shortest durable architecture wins:

- reuse repo patterns first;
- keep workloads, baselines, platforms, models, data, and simulator/testbed IO at adapters;
- keep config explicit;
- add one runnable check for non-trivial logic;
- avoid speculative abstractions.

Use a persistent multi-component architecture only for a research artifact or
release that genuinely needs it. Such artifacts keep experiment configurations
explicit, isolate workload and baseline adapters, emit result manifests with
run IDs and git/config provenance, and provide one command to reproduce each
claim-bearing table or figure. Production hardening, feature count, and clean
architecture are not paper contributions by themselves; each implementation
unit must instantiate an insight, test a hypothesis, or produce claim-bearing
evidence.

For executable research work, use this fixed minimum loop: implement one
experiment unit; run one executable minimal smoke; run the actual claim-bearing evaluation
(benchmark, testbed, simulation, measurement, training/serving, or hardware
run); fix only from observed result/error; run full regression once immediately
before finalizing a claim. Full regression is a release gate, not a development
loop.

For long commands, use Coresearch's canonical `execution-safe` policy;
do not paste raw build/test logs into the main context.

Agents are allowed when they reduce wall-clock time or cover disjoint work. Use
the fewest needed; every agent gets an owned scope, expected output, and stop
condition. Never add agents merely to re-check the same change.

## Caveman

Keep prose terse, but expand when safety/order/confidentiality would become ambiguous.

## Autoresearch

Before `$autoresearch`, require:

- mission;
- sandbox;
- validator mode: `mission-validator-script` or `prompt-architect-artifact`;
- completion artifact path;
- output artifact path if prompt-reviewed.

## Native subagents

Use native subagents only for bounded parallel work that improves quality, speed, or safety. The handoff contract below applies after deciding that an agent is worth its wall-clock cost; ordinary experiment work may still use agents when the scope is disjoint. Coresearch skills do not automatically transfer into a fresh subagent context, so every handoff must include:

- `agent_type`: pick the narrow OMX role (`explore`, `researcher`, `executor`, `test-engineer`, `verifier`, `code-reviewer`, `writer`, `critic`, etc.); do not use `worker` outside active `$team`/`$swarm`.
- Research context: field mode, primary skill, claim/evidence target, confidentiality limits, and expected output.
- Skill context: pass the relevant `coresearch`/`research-*` skill item or quote the minimal instructions needed; use `fork_context` only when prior thread context is actually required.
- Style/plugin context: explicitly restate active Ponytail/Caveman mode and level (for example, `Ponytail full active; prefer minimal durable code` or `Caveman lite active; keep report terse`). Do not assume fresh subagents inherit active skill/plugin modes.
- Scope: disjoint files or read-only question, validation expected, and what not to invent.

Default native `agent_type` mappings (not `$skill` routes):

| Need | `agent_type` | Required context |
|---|---|---|
| Repo/file/symbol lookup | `explore` | paths, symbols, exact question |
| Official docs, current venue policy, literature metadata | `researcher` | source priority, date/version needs, citation format |
| Research code edit | `executor` | claim supported, files owned, smallest check |
| Test/reproducibility plan | `test-engineer` | command surface, expected artifact, failure criteria |
| Claim/source/completion audit | `verifier` | claims, sources, PASS/FAIL/PARTIAL schema |
| Deck/figure/manuscript quality review | `code-reviewer`, `critic`, or `writer` | field mode, audience/venue, no-fabrication rule |

## Team / Ultragoal

Use Team only for explicitly requested or materially useful parallel lanes with disjoint write scopes and explicit stop conditions. Use Ultragoal as durable ledger/checkpoint owner. Ralph only when persistent single-owner verification is explicitly selected; cancel any lane that stalls or repeats without new evidence.

## Re-entry to coresearch

OMX lanes (the full set is in [routing.md](routing.md) §OMX lanes; e.g.
`$autoresearch`, `$ralplan`, `$team`, `$ultragoal`, `$deep-interview`) and native
subagents are executors, not routers. On terminal — or when a research stage
follows their output — re-enter `coresearch` to re-classify and route the next
stage. Example: `$autoresearch` terminal → `coresearch` → `research-write`
(write-up) or `research-verify` (result claims). Do not chain a research skill
from inside the lane. Lane results land in the canonical `ledger.yaml`
(state-ledger.md); downstream skills read them there, not from a guessed OMX path.
