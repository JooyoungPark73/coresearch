# Hierarchical Argument Design and Iterative Writing for Computer Systems Papers

## Purpose

This document defines a writing model for computer systems research papers. It combines two complementary views:

1. **Paper-level argument design:** determine the single idea the paper should transmit, express it as a connected set of refutable claims, and identify the evidence required to support each claim.
2. **Hierarchical manuscript realization:** expand that argument through sections, paragraphs, and sentences, while preserving the ability to reconcile later feedback across every affected level.

The intended use is both human and computational. A senior Ph.D. student or faculty member should be able to inspect the structured state and understand what the paper argues, why the argument matters, how its method, artifact, analysis, or observations support it, and which evidence remains missing. An AI writing system should be able to render academic prose from the same state without inventing new claims or losing logical relationships.

This document is design input for Coresearch. Installed `research-write`
instructions and their progressively loaded references own runtime behavior;
this document does not create another router, ledger, or execution engine.

The central principle is simple:

> A systems paper is a structured argument supported by evidence appropriate to
> its paper type. When the argument depends on an artifact, the paper must state
> what was implemented and how it supports the claims. The manuscript realizes
> that argument without replacing its claim and evidence contract.

This view follows Simon Peyton Jones's argument that writing is part of doing research and that a paper should transmit one clear, reusable idea. It also incorporates Irene Zhang's organization of a systems paper around the **why**, **how**, and **results**, and Levin and Redell's reviewer-oriented tests of originality, reality, lessons, design choices, context, focus, and presentation.

## 1. What a paper is trying to accomplish

A paper does not primarily exist to document how much work the authors performed or to describe every component they built. Its purpose is to cause the reader to understand and believe one useful research idea.

Writing should therefore begin before the research is considered finished. Early structured writing forces the authors to state what they believe, reveals missing logical steps, separates assumptions from results, and exposes experiments that do not support any important claim. The writing state will initially contain hypotheses, plans, and unresolved questions. These must be explicitly marked rather than silently rendered as established facts.

The finished paper should have one recognizable, coherent payload, or what
Peyton Jones calls one “ping.” This does not mean that a paper may contain only
one contribution or one literal claim. It means that the contributions and
findings should combine into a recognizable takeaway. A mechanism paper may
organize that payload around a thesis; a measurement, benchmark, experience,
or cross-layer paper may organize it around linked findings or paired claims.
If two contributions do not need each other to establish a common conclusion,
they may belong in different papers.

For a typical systems paper, the payload can be diagnosed using the following structure:

> For an important application or workload **Y** operating in environment **Z**, existing approaches fail to satisfy requirement **R** because of problem **P**. Our key insight **I** enables system **X** to make design choice **D**. Under assumptions **A**, evidence **E** shows that **X** improves outcome **O** over appropriate alternatives **B**. The broader lesson is **L**.

This is a reasoning aid, not a sentence template. A strong paper may organize or phrase the idea differently. Nevertheless, if the authors cannot fill these roles unambiguously, the global argument is probably not ready for prose.

## 2. The two coupled structures of a paper

As an operating model, the writing state can maintain two coupled structures.
This representation is a practical discipline for an AI writer, not a claim
that every author or paper must serialize every rhetorical decision.

### 2.1 The argument graph

The argument graph records what must be true for the thesis to hold. Its nodes are claims, assumptions, evidence, design decisions, limitations, and lessons. Its edges express relationships such as:

- **depends on:** claim B is credible only if claim A holds;
- **supports:** evidence E increases confidence in claim C;
- **contrasts with:** claim C distinguishes the proposed work from alternative A;
- **qualifies:** condition Q narrows the scope of claim C;
- **motivates:** observation O establishes the need for design requirement R;
- **realizes:** mechanism M implements insight I; and
- **generalizes to:** lesson L follows from a set of results under stated assumptions.

The argument is a graph rather than a pure tree because one experiment may support several claims, one assumption may qualify several results, and one prior system may be relevant to multiple design choices.

### 2.2 The manuscript hierarchy

The manuscript hierarchy records how the argument is communicated:

1. **Message:** the problem, stakes, thesis, and intended takeaway.
2. **Claims:** the refutable propositions the paper asks the reader to accept.
3. **Sections:** the sequence of promises through which the paper establishes those claims.
4. **Paragraphs:** the local rhetorical units that motivate, explain, support, interpret, or qualify a claim.
5. **Sentences:** the concrete wording, transitions, and epistemic calibration.

The hierarchy controls exposition, while the graph controls validity. The paper is therefore **hierarchically rendered but logically graph-structured**.

## 3. Constructing the paper-level argument

### 3.1 Define the target context

Before introducing the system, state the application or workload **Y** and environment **Z** precisely. Explain why Y matters, why Y actually occurs in Z, and which properties of Y and Z affect the design. Avoid motivating a universal problem if the evidence covers only a particular deployment setting.

The context should include:

- the target users, applications, or workloads;
- the execution or deployment environment;
- the operational constraints and objectives;
- the assumptions on which the design relies; and
- the boundary beyond which the thesis may no longer hold.

This context is part of the claim, not background decoration. A design may be novel and effective specifically because Y or Z has changed. The paper should teach the reader why that changed context invalidates an older assumption or creates a new opportunity.

### 3.2 State one central thesis

The thesis is the paper's main refutable proposition. It should assert more than the existence of a system. “We designed and implemented X” reports an activity; it does not tell the reader what was learned or what should now be believed.

A useful thesis identifies:

- the condition under which it applies;
- the proposed idea or system;
- the important comparison or counterfactual;
- the dimension on which it should be judged; and
- the scope of the conclusion.

The thesis should be understandable to a systems researcher who knows the general area but has not followed the project. If it cannot be stated concisely in one paragraph, the authors may not yet understand the paper's contribution—or may be attempting to combine several papers.

### 3.3 Decompose the thesis into a claim chain

The paper's claims should form a chain of proof obligations rather than a list of accomplishments.

| Claim role | Question the claim must answer | Typical support |
| --- | --- | --- |
| Context and significance | Does Y in Z occur, and is the objective important? | Traces, deployments, workload studies, prior evidence |
| Problem | Does P actually prevent the desired outcome? | Characterization, diagnosis, motivating example |
| Prior-work insufficiency | Why do existing approaches not already solve P for Y in Z? | Explicit comparison, analytical mismatch, measurements |
| Insight | What new observation makes a different solution possible? | Reasoning, data, counterexample to an old assumption |
| Design | How does X turn the insight into a working mechanism? | Architecture, invariants, algorithms, implementation |
| End-to-end result | Does X improve the outcome that motivates the paper? | Comparison with relevant baselines under representative conditions |
| Mechanism or causal result | Which choices are consistent with the outcome, and what stronger attribution is justified? | Ablations, breakdowns, alternatives, and sensitivity for mechanism evidence; an identification strategy and credible counterfactual for causality |
| Lesson | What reusable knowledge should the community retain? | Synthesis across claims and evidence |
| Scope and limitation | Under what assumptions does the conclusion stop applying? | Boundary cases, negative results, threats to validity |

Not every row must become a claimed contribution, but every relevant proof obligation must be addressed somewhere in the paper. In particular, novelty does not follow merely from building a large system, and performance does not establish significance unless it measures the outcome named in the thesis.

### 3.4 Make contributions refutable

The contribution list is the paper's contract with the reader. Write it early, before drafting the body. Each item should state a claim that could, in principle, be disproved and should point to the evidence that will substantiate it.

Weak contribution statements describe activity:

- “We present X.”
- “We implement a prototype.”
- “We evaluate the system extensively.”

Stronger contribution statements declare what the work establishes:

- a previously hidden bottleneck accounts for a measured fraction of cost under a defined workload;
- a specific design principle removes that bottleneck while preserving stated semantics;
- an implementation demonstrates feasibility within a stated scope; or
- controlled experiments show an improvement over named alternatives and identify the mechanisms responsible.

The paper body must contain evidence for every contribution claim. Conversely, every major experiment should support a claim that matters to the thesis. “We measured it because the system has this component” is not an adequate reason for an experiment.

### 3.5 Separate the system from the lesson

The system is usually the instrument through which the paper tests an idea. The lasting contribution is often a design principle, trade-off, or newly established fact that readers can reuse after the artifact becomes obsolete.

The structured state should therefore distinguish:

- **artifact:** what was built;
- **mechanism:** how it operates;
- **hypothesis:** what the mechanism is intended to demonstrate;
- **result:** what the implementation and experiments actually establish; and
- **lesson:** what follows beyond the exact prototype, under stated assumptions.

The lesson must not generalize beyond the evidence. A result from one system, workload, or environment does not automatically establish a universal principle.

## 4. A human-readable manuscript map

The manuscript map should be inspectable and serializable when persistence is
needed. In Coresearch it is a view over the canonical claim and evidence
records, not a second copy of their provenance, confidence, experimental
context, or status. A professor should be able to inspect the map without
reverse-engineering hidden dependencies, while the author retains control of
the manuscript itself.

At the paper level, the view can contain:

```yaml
manuscript_map:
  paper_type: system|measurement|architecture|method|benchmark|dataset|experience|theory|design_proposal
  payload: string
  intended_takeaway: string
  context:
    application_or_workload: string|null
    environment: string|null
    objective: string
    assumptions: [string]
    exclusions: [string]
  argument:
    problem_or_question: string
    gap: string|null
    insight_or_central_finding: string
    thesis_or_payload: string
    scoped_lesson: string|null
  claim_bindings:
    - claim_id: string
      role: string
      depends_on: [string]
      section_ids: [string]
  design_decisions:
    - id: string
      requirement: string
      choice: string
      alternatives: [string]
      rationale: string
      tradeoffs: [string]
      claim_ids: [string]
      evidence_ids: [string]
  section_promises:
    - section_id: string
      reader_question: string
      promise: string
      claim_ids: [string]
      evidence_ids: [string]
  terminology: {}
  unresolved_writing_gaps: [string]
  revision_impacts: [string]
```

Keep status dimensions separate. Claim status is epistemic (`unresolved`,
`supported`, `contradicted`, `qualified`, or `rejected`); evidence status is
operational (`planned`, `collected`, `validated`, or `invalid`); artifact status
is material (`proposed`, `implemented`, `tested`, or `deployed`). Manuscript
status, when useful, records drafting progress only. An AI writer must never
convert planned evidence into a measured result, an implemented component into
a validated empirical claim, or a plausible explanation into an established
cause.

The claim/evidence records govern factual and epistemic consistency. The
manuscript remains an author-controlled artifact, and the map exists to plan,
inspect, criticize, and reconcile it rather than to make prose disposable.

## 5. Turning the global argument into a paper

### 5.1 Use the why–how–results spine

A systems paper should make three answers easy to recover.

**Why:** What is the thesis? Which application and environment matter? What problem prevents the desired outcome? Why are existing systems insufficient? What new lesson might follow?

**How:** What is the key insight? Where does the proposed system fit? Which mechanisms realize the insight? Why were these design choices selected over alternatives? What trade-offs and exclusions follow?

**Results:** What was actually implemented? Which experiments test which claims? How does the system compare with prior approaches? Which mechanisms account for the result? Under what conditions does the conclusion hold?

The why–how–results spine is an argumentative organization, not necessarily three literal section headings. It should remain recognizable in the abstract, introduction, body, and conclusion.

### 5.2 Treat the first page as a contract

Readers decide quickly whether a paper has a clear and significant idea. For
many systems papers, the first page should therefore establish the argument
directly; treat the following sequence as a diagnostic, not a venue-independent
template:

1. Begin with a concrete instance of the problem, not a broad statement that the general area is important.
2. Identify Y and Z and explain the relevant constraint.
3. Show why the problem remains unsolved in that context.
4. State the key insight and introduce X at the level needed to understand it.
5. State the strongest result if it is already available.
6. End with refutable contribution claims and forward references to their evidence.

Do not spend the first page on a generic structural roadmap such as “Section 2 presents background.” Forward references should instead connect claims to evidence: a characterization claim points to the section that measures it; a design claim points to the mechanism; an empirical claim points to the evaluation.

The introduction should describe a molehill precisely rather than invoke a mountain vaguely. A small concrete problem that the paper demonstrably solves is more persuasive than an enormous societal problem connected only indirectly to the work.

### 5.3 Compress before expanding

Before writing full sections, test whether the argument survives compression.

- **One sentence:** the central thesis.
- **One paragraph:** problem, insight, system, principal evidence, and lesson.
- **Three-sentence conclusion:** hypothesis or thesis; system or method used to test it; result and lesson.
- **Four-move abstract:** concrete problem; gap or insight; approach; principal result and implication.

These are diagnostics rather than rigid templates. If the compressed versions disagree, the global state is inconsistent. Do not compensate with more polished sentences; reconcile the argument first.

### 5.4 Present intuition before abstraction

Introduce the problem and the key insight with a concrete example before general notation, algorithms, or exhaustive terminology. The example should expose the exact failure and make the proposed mechanism feel necessary. Once the reader has the intuition, the paper can generalize and formalize it.

Choose the most direct explanatory route to the idea. The order of exposition need not reproduce the chronology of discovery. However, a clean narrative must not falsely imply that design choices were made for reasons that the authors discovered only later. Relevant failed alternatives should be reported when they explain a trade-off or establish a useful lesson; unrelated dead ends need not burden the main narrative.

## 6. Hierarchical manuscript realization

Once the paper-level argument is coherent, expand it from coarse semantic decisions into fine-grained prose.

### 6.1 Message

The message contains the problem, stakes, central thesis, and intended takeaway. It is the highest-level contract. The title, abstract, introduction, and conclusion must realize the same message at different levels of compression.

The message should answer:

- What should the reader remember a week later?
- What belief should change after reading the paper?
- What is the strongest conclusion justified by the evidence?

### 6.2 Claims

Claims decompose the message into refutable propositions. Each claim records its scope, dependencies, evidence, status, and destination in the manuscript. Claims should not be created merely to match section headings; sections exist to establish claims.

### 6.3 Sections

Each section should have a **reader question** and a **promise**. The promise states what the reader will understand or believe after reading the section. A section should not exist solely because papers conventionally contain one with that name.

A design section normally establishes why a mechanism satisfies a requirement and why its trade-off is appropriate. An evaluation section normally establishes one or more empirical claims. A background section should contain only concepts required to understand the problem and solution.

### 6.4 Paragraphs

Each paragraph should perform one primary rhetorical function, such as:

- establish context;
- state or refine a claim;
- provide a concrete example;
- explain mechanism or intuition;
- present evidence;
- interpret a result;
- compare an alternative;
- qualify scope; or
- transition between reasoning steps.

When paragraph-level planning is useful, its state should identify the local
message and the claim it serves. Do not require a serialized record for every
paragraph in an ordinary local rewrite. If a paragraph cannot be connected to
a section promise or paper-level claim, it is probably irrelevant or the claim
graph is incomplete.

### 6.5 Sentences

Sentences realize the paragraph's function with appropriate wording and epistemic strength. They should distinguish among observation, measurement, interpretation, hypothesis, and speculation. Fluency must not strengthen a claim beyond its evidence.

Use direct language, define terms before relying on them, minimize unsupported forward references, and prefer active constructions when they make responsibility and action clearer.

## 7. Writing the system design

The design should explain, not merely enumerate, the system.

For artifact-bearing papers, first show where X sits relative to Y and Z. When
an overview figure materially clarifies the design, it should make boundaries,
interfaces, trusted components, data paths, and changed responsibilities
visible. If X changes an API, deployment assumption, or interaction with Y or
Z, state that change explicitly.

For every load-bearing or non-obvious design decision, record:

1. the requirement derived from the problem;
2. the chosen mechanism;
3. the plausible alternatives;
4. why the selected trade-off is appropriate for Y in Z;
5. the cost or limitation introduced; and
6. the claim and evidence that will test the decision.

New terminology should be introduced only when it compresses a recurring concept. If many terms are necessary, provide a compact definition table. Do not require readers to remember undefined names until a later section.

State out-of-scope problems and unsupported features directly. Reviewers should not have to infer whether an omission is deliberate, an engineering limitation, or a failure of the idea.

## 8. Connecting evaluation to claims

An evaluation is not a collection of available measurements. It is an evidence program for the paper's claim graph.

### 8.1 Establish implementation reality

State early what exists:

- which components were implemented;
- which components are simulated, emulated, or omitted;
- how the prototype differs from the proposed full design;
- whether and how the system has been used; and
- why the implemented subset is sufficient to test the thesis.

Implementation effort is not itself evidence of novelty or significance. The paper must explain what the artifact teaches.

### 8.2 Give every experiment a proof obligation

Each evaluation subsection should identify:

- the claim it tests;
- the hypothesis or question;
- the relevant baseline or alternative;
- the metric and why it represents the claimed outcome;
- the controlled and varied conditions;
- the setup and repetition methodology;
- the result and uncertainty; and
- the boundary or threat to validity.

The subsection should state the intended conclusion near its beginning, establish it with data, and restate the supported conclusion at the end. The figure caption should also say what the reader should learn and, when necessary, how to read the figure.

### 8.3 Cover outcome and mechanism when the claims require them

Many mechanism-led systems-paper evaluations need two complementary forms of
evidence. They are common categories, not an exhaustive experiment taxonomy:

1. **End-to-end comparison:** Does X improve the important outcome for Y in Z relative to credible alternatives?
2. **Mechanism evidence:** Which mechanisms or design decisions are consistent
   with the improvement, and what overheads or trade-offs do they introduce?

The first establishes usefulness; the second improves understanding. Ablations,
breakdowns, sensitivity studies, and alternative designs can support mechanism
attribution, but they do not by themselves establish causality. Use causal
language only when the work declares an identification strategy that rules out
credible alternatives.

### 8.4 Maintain a claim–evidence matrix

Before rendering the evaluation, inspect a matrix with one row per empirical claim:

| Claim | Required evidence | Baseline | Metric | Experiment | Evidence status | Claim status | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claim ID | What would make the claim credible? | What is the relevant counterfactual? | What directly represents the outcome? | Where is it tested? | Planned, collected, validated, or invalid | Unresolved, supported, contradicted, qualified, or rejected | Where does it stop holding? |

The matrix should expose four common failures:

- a contribution with no evidence;
- an experiment with no important claim;
- a metric that does not measure the claimed benefit; and
- a conclusion broader than the evaluated scope.

## 9. Related work, novelty, credit, and limitations

Related-work analysis must happen early in the research process even when the full related-work section appears late in the paper.

Before drafting, construct an explicit comparison against the strongest relevant prior systems. Identify what each system already accomplishes, which assumptions differ, and why the proposed work is not an obvious restatement. This comparison may remain an internal table, but the authors must understand it before claiming novelty.

In the manuscript, include enough prior context near the problem to explain why it remains unsolved. Defer the comprehensive comparison until the reader understands the paper's vocabulary and design; otherwise, dense literature discussion becomes a barrier between the reader and the main idea.

Comparisons must be specific. State the exact mechanism, assumption, interface, environment, or trade-off that differs. Avoid vague statements that another system is “orthogonal,” “complementary,” or simply “different.”

Credit is not zero-sum. Describe prior work at its strongest, acknowledge what it established, and then define the remaining gap precisely. This makes the novelty argument more credible. Likewise, state limitations and negative results without waiting for reviewers to discover them. A narrow claim with an explicit boundary is stronger than a universal claim contradicted by an obvious counterexample.

## 10. Revision as bidirectional semantic reconciliation

Text-first AI writing commonly proceeds from prompt to introduction, body, and conclusion. It is effective at continuation and local polishing, but late feedback is often applied as a patch to rendered prose. Earlier framing then remains semantically sticky.

Hierarchical iterative writing instead treats canonical claims and evidence as
authoritative for factual and epistemic consistency while keeping the
manuscript author-controlled. After a reader critiques the manuscript,
revision follows this cycle:

> **render → critique → locate semantic change → reconcile state → re-realize affected text → render**

### 10.1 Locate the semantic change

Determine whether the critique changes:

- surface wording;
- a paragraph's local explanation;
- a section promise or organization;
- a claim's content, scope, or evidence;
- the central thesis or intended takeaway; or
- an assumption or design decision connected to several claims.

A comment attached to one sentence may express a paper-level objection. The physical location of feedback does not determine its semantic level.

### 10.2 Reconcile upward and across

Update the targeted node, then inspect its ancestors and graph neighbors. If a result is weaker than expected, the contribution, abstract, title, and conclusion may need qualification. If the intended takeaway changes, claims and section promises derived from the old framing must be reconsidered.

### 10.3 Re-realize downward

Revise only affected descendants after the higher-level state is coherent. A
high-level change may alter only a few fields in the structured state while
requiring many paragraph- and sentence-level edits. Conversely, a stylistic
correction should not trigger unnecessary global rewriting. Preserve
unaffected prose, terminology, author voice, and deliberate organization.

The edit pattern may be a large local change with smaller revisions elsewhere
when semantic consistency requires them; a genuinely local correction may
require no other edit. The magnitude of textual change is not the same as the
importance of the semantic change.

### 10.4 Validate global invariants

After revision, verify that:

- title, abstract, introduction, contributions, and conclusion express the same payload;
- every claim retains adequate evidence and correct scope;
- section promises match what their sections establish;
- evaluation conclusions match the reported data;
- terminology and system boundaries remain consistent; and
- no planned or hypothetical result has been rendered as fact.

## 11. An end-to-end writing workflow

### Phase 1: Start before the research is finished

Create the manuscript map as soon as a coherent payload can be stated when
whole-paper planning benefits from it. Mark uncertainty explicitly. Use
missing fields and unsupported edges to expose the next research discussion,
artifact task, study, analysis, or experiment; return those research decisions
to their owning stage.

### Phase 2: Establish the global argument

Write the coherent payload, relevant context, problem or question, prior-work
gap, insight or central finding, principal claims, and intended lesson. Select
the applicable paper archetype—implemented mechanism/system, measurement or
workload characterization, architecture or cross-layer mechanism,
method/benchmark/dataset, experience or negative results, theory/analysis, or
design proposal—and do not let the manuscript imply more implementation or
evidence maturity than exists.

### Phase 3: Build the evidence program

For each claim, identify what evidence would make a skeptical reader accept it. Select baselines and metrics from the claim, not from convenience. Record missing evidence before prose generation.

### Phase 4: Compress and test

Write the one-sentence thesis, one-paragraph argument, short conclusion, and abstract moves. Ask whether they transmit the same idea and whether every asserted result is supported.

### Phase 5: Expand hierarchically

Assign claims and evidence to section promises. For whole-paper work, use
paragraph functions when they improve planning or diagnosis, then realize
sentences and transitions. A local rewrite need not serialize either level.
Use concrete examples before abstractions when they clarify the idea and take
the shortest honest route to it.

### Phase 6: Render and inspect

Generate a conventional manuscript, but inspect it against canonical
claim/evidence state and the manuscript map when one is in use. Local fluency
cannot compensate for an unsupported claim, missing comparison, or inconsistent
scope.

### Phase 7: Obtain fresh-reader feedback

Use readers carefully because each person can encounter the paper for the first time only once. Ask them where they became lost, what they believe the main idea is, which claim they doubt, and what evidence they expected. Grammar comments are useful, but comprehension failures reveal defects higher in the hierarchy.

### Phase 8: Reconcile rather than patch

Interpret reviewer feedback as possible evidence that the structured state, its exposition, or both are wrong. Locate the semantic level of the problem, update the argument graph, propagate the change, and re-render affected prose. If a reader misunderstands a claim, revise the paper so that the intended interpretation becomes difficult to miss.

## 12. Quality gates for a systems paper

Before treating a draft as complete, apply the following gates.

### Payload

- Can a knowledgeable reader state the paper's one main idea after reading the abstract and introduction?
- Do all claimed contributions support that idea?
- Is the paper's lesson reusable beyond the name of its system, artifact, or study?

### Originality and context

- Are Y, Z, assumptions, and objectives explicit?
- Is the new idea stated concisely?
- Is the difference from the strongest relevant prior work specific and significant?
- Does the novelty arise from a new mechanism, changed context, new application, new evidence, or a defensible combination?

### Claim–evidence alignment

- Is every contribution refutable?
- Does every major claim have identifiable evidence?
- Does every major experiment support a claim?
- Do metrics, baselines, and workloads match the thesis?
- Do causal claims state an identification strategy rather than relying only on
  correlation, ablation, or breakdown evidence?

### Reality and scope

- When the argument is artifact-bearing, is implementation status clear from
  the beginning and is the implemented subset sufficient to test the thesis?
- Are assumptions, exclusions, limitations, and negative results explicit?
- Are conclusions no broader than the evidence?

### Design explanation

- When a mechanism or artifact is load-bearing, does each major mechanism
  follow from a requirement?
- Are plausible alternatives and trade-offs discussed where a design decision
  affects a claim?
- Does the paper explain why the selected design is appropriate for its stated
  context?
- Are boundaries, interfaces, and responsibilities visible when applicable?

### Reader experience

- When the first-page contract applies, does it present a concrete problem or
  finding, gap, insight, approach or artifact when applicable, and principal
  claims?
- Are examples presented before difficult abstractions?
- Is related work sufficient early but comprehensive only after the idea is understood?
- Does each section have a clear promise, and does each paragraph have a clear
  function when paragraph-level diagnosis is useful?
- Are terms defined before use?

### Revision consistency

- Have semantic revisions propagated to every affected claim and passage?
- Do the title, abstract, introduction, body, and conclusion agree?
- Are epistemic qualifiers preserved during polishing?
- Are unresolved gaps visible rather than hidden by fluent prose?

## 13. Common failure modes

1. **System-description paper:** The manuscript explains what was built but never states what the reader should now believe.
2. **Contribution laundry list:** Several technically valid accomplishments do not combine into one recognizable thesis.
3. **Mountain motivation:** The introduction invokes an enormous problem but the evaluation supports only a narrow, weakly connected result.
4. **Implicit Y and Z:** The proposed design appears arbitrary because the target workload and environment are underspecified.
5. **Activity as claim:** “We designed, implemented, and evaluated” substitutes for refutable contributions.
6. **Feature-driven evaluation:** Experiments correspond to components rather than proof obligations.
7. **Convenient baselines:** Comparisons avoid the strongest counterfactual relevant to the thesis.
8. **Unexplained design:** The paper lists mechanisms without alternatives, rationale, or trade-offs.
9. **Front-loaded literature barrier:** Detailed related work appears before the reader understands the problem or terminology.
10. **Hidden prototype boundary:** The text allows readers to assume that unimplemented parts exist.
11. **Overgeneralized lesson:** A narrow measurement is rendered as a universal conclusion.
12. **Local semantic patching:** Late feedback changes one passage while dependent framing, claims, or results remain untouched.
13. **Fluency-induced overclaim:** Sentence polishing removes qualifiers or turns hypotheses into facts.
14. **Chronological research diary:** The paper follows the authors' path of discovery instead of the reader's shortest path to understanding.

## 14. Operational principles for an AI writing system

An AI system implementing this model should obey the following rules:

1. Treat canonical claims and evidence as authoritative for factual and
   epistemic consistency; treat prose as an author-controlled, revisable
   artifact.
2. Expose the paper's thesis, claims, dependencies, evidence, scope, and unresolved gaps in human-readable form.
3. Require each contribution to identify its proof obligation and evidence destination.
4. Distinguish observed facts, author-provided facts, hypotheses, planned work, interpretations, and generated suggestions.
5. Never invent evidence, implementation status, citations, baselines, numerical results, or causal explanations.
6. Detect when a requested local edit changes a higher-level claim or scope condition.
7. Reconcile affected ancestors and graph neighbors before regenerating descendants.
8. Preserve unaffected content when possible, but never preserve it at the cost of semantic consistency.
9. Report unsupported claims, unused experiments, scope conflicts, and terminology conflicts before polishing prose.
10. Optimize for reader understanding and claim–evidence alignment, not merely stylistic fluency.

## References

- Simon Peyton Jones, [*How to Write a Great Research Paper*](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/) and the accompanying [slides](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/How-to-write-a-great-research-paper.pdf). The talk motivates writing as part of research, one clear idea, refutable contributions tied to evidence, concrete examples, delayed related work, direct exposition, and feedback-driven revision.
- Irene Zhang, [*Hints on How to Write an SOSP Paper*](https://irenezhang.net/blog/2021/06/05/hints.html). The essay organizes systems-paper reasoning around the why, how, and results; emphasizes the X/Y/Z thesis structure, design trade-offs and scope, implementation clarity, and experiments with explicit conclusions.
- Roy Levin and David D. Redell, [*How (and How Not) to Write a Good Systems Paper*](https://www.usenix.org/conferences/author-resources/how-and-how-not-write-good-systems-paper), originally published in *ACM SIGOPS Operating Systems Review*, 1983. The article frames paper preparation through reviewer questions about originality, reality, lessons, choices, assumptions, focus, organization, and clarity.
