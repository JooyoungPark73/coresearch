# Research design and experiments

A useful design connects a consequential question, a specific contribution,
credible alternatives, and evidence that could change the conclusion. Name what
would falsify the proposed explanation or make the contribution unimportant.
Astra owns that judgment; workers can gather baselines, implement bounded units,
and run evaluations against an agreed interface.

Evidence should fit the contribution, not a universal paper recipe:

| Research object | Evidence often needed |
|---|---|
| AI/ML/CV method or representation | Matched baselines, leakage controls, ablations, variation across seeds/data, compute costs |
| Robotics system | Real operating conditions, failure modes, hardware/control limits, simulation-to-reality assumptions |
| Graphics/visual computing | Visual comparisons plus relevant numerical/perceptual measures and performance tradeoffs |
| HCI/design knowledge | Participant/context rationale, task or qualitative evidence, ethical handling, limits on transfer |

Hybrids need evidence for both the technical mechanism and the human/workflow
claim. A benchmark gain alone does not establish usefulness, causation, or
reliability outside the evaluated conditions.

## Executable work

Define the experiment's question, inputs, comparison, observable result, resource
budget, and completion criterion. Keep commands, code revision, environment,
configuration/seeds, data version or split, and raw result paths sufficient to
reproduce any reported number. Planned results are not observed results.

Validate the smallest meaningful path before expensive runs. Testing and repair
follow the diagnosed risk, not a fixed retry count. Preserve negative results and
failed-run diagnostics. A worker reports measurements and validation, while
Astra decides whether they answer the question or expose missing evidence.

For an autonomous search loop, make the metric/validator executable and keep
held-out evaluation separate from optimization. Set a real compute/time/iteration
budget and a scientific stop condition. Changing the validator changes the
comparison and belongs to the lead. Use the host's existing job lifecycle for
long runs rather than adding polling or a Coresearch scheduler.

Participant studies, restricted data, external publication, and expensive actions
remain subject to the actual authorization and applicable project constraints.
No research result should be inferred from a successful build or test suite alone.
