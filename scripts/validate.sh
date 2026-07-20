#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

pass() {
  echo "PASS: $*"
}

python3 -m json.tool .codex-plugin/plugin.json >/dev/null
pass "plugin manifest JSON parses"

python3 - <<'PY'
from pathlib import Path

for rel in ("skills/research-survey/crawler.py", "scripts/harness.py"):
    text = Path(rel).read_text()
    compile(text, rel, "exec")
PY
pass "python utilities compile without pycache"

bash -n scripts/install.sh
bash -n scripts/validate.sh
bash -n bin/harness
bash -n harness
pass "shell scripts parse"

BRIDGE_HANDOFF_LINE="For native subagents or team lanes, use installed OMX agent roles and pass Coresearch stage, skill, field, evidence, scope, validation, confidentiality context, and active Ponytail/Caveman mode when relevant."

python3 - <<'PY'
from pathlib import Path
import json
import re

broken = []
files_with_cr = []
skip = {'.git', 'tmp', '.omx', '__pycache__'}
for path in Path('.').rglob('*'):
    parts = set(path.parts)
    if parts & skip:
        continue
    if path.is_symlink() and not path.exists():
        broken.append(str(path))
    if path.is_file() and not path.is_symlink() and (path.suffix in {'.md', '.py', '.sh', '.json'} or path.name == 'harness'):
        if b'\r' in path.read_bytes():
            files_with_cr.append(str(path))
assert not broken, broken
assert not files_with_cr, files_with_cr

readme = Path('README.md').read_text()
assert 'positional target is planned' not in readme
assert 'planned ergonomic alias' not in readme
assert 'harness init              # same as' not in readme
assert '/Users/alansynn' not in readme
assert 'Global skills vs. global AGENTS.md' in readme
assert 'harness link' in readme and 'harness global -y' in readme
assert 'defaults to . / full / apply' in readme

agents = Path('templates/research/AGENTS.md').read_text()
required = [
    '<!-- OMX:RUNTIME:START -->',
    '<!-- OMX:RUNTIME:END -->',
    '<!-- OMX:TEAM:WORKER:START -->',
    '<!-- OMX:TEAM:WORKER:END -->',
]
for marker in required:
    assert marker in agents, marker
assert 'PaperSmith' not in agents
assert '/project_brief.md' not in agents
assert 'Do not create separate `.agents/` chats' in agents

field_modes = Path('skills/coresearch/references/field-modes.md').read_text()
router = Path('skills/coresearch/SKILL.md').read_text()
venue_groups = {
    'systems/cloud': ('OSDI', 'SOSP', 'NSDI', 'EuroSys', 'SoCC'),
    'ml-systems': ('MLSys',),
    'architecture/workload': ('ISCA', 'MICRO', 'HPCA', 'IISWC'),
    'cross-layer': ('ASPLOS',),
}
for group, venues in venue_groups.items():
    for venue in venues:
        assert venue in agents, f'template missing {group} venue: {venue}'
        assert venue in field_modes, f'field modes missing {group} venue: {venue}'
for mode in ('Systems / Cloud', 'ML Systems', 'Computer Architecture'):
    assert mode in agents, f'template missing primary mode: {mode}'
    assert mode in field_modes, f'field modes missing primary mode: {mode}'
for legacy_heading in (
    '**Graphics / Visual Computing:**',
    '**AI / ML / Computer Vision:**',
    '**Robotics:**',
    '**HCI / Technical HCI:**',
):
    assert legacy_heading not in agents, f'template still advertises legacy primary mode: {legacy_heading}'
for legacy_list in ('AI / Robotics / Graphics / HCI', 'AI/ML/CV, Robotics, Graphics'):
    assert legacy_list not in router, f'router still advertises legacy primary modes: {legacy_list}'

contract = Path('skills/coresearch/references/research-contract.md').read_text()
ledger = Path('skills/coresearch/references/state-ledger.md').read_text()
schema_contract = (
    'field_mode: systems_cloud|ml_systems|computer_architecture',
    'venue_lens: general_systems|networked_distributed|cloud|cross_layer|workload_characterization',
    'intended_contribution: method|system|representation|theory|dataset|benchmark|empirical_finding|design_knowledge|architecture|measurement_characterization',
)
for line in schema_contract:
    assert line in contract, f'research contract missing schema line: {line}'
    assert line in ledger, f'state ledger missing synchronized schema line: {line}'

evidence = Path('skills/coresearch/references/evidence-grounding.md').read_text()
for field in (
    'evidence_kind: literature|experiment|artifact|trace|dataset',
    'claim_class: capability|correctness|performance|scalability|efficiency|reliability|cost|quality_performance_tradeoff|power_area_performance|generality|measurement|causal',
    'support_locator:',
    'artifact_path:',
    'run_ids:',
    'config_or_manifest:',
    'evaluation_context:',
):
    assert field in evidence, f'evidence schema missing: {field}'
assert 'passage and location may be null only' in evidence, 'non-literature provenance rule missing'
assert 'experiment_state:' not in ledger, 'domain refit must not add a new experiment state machine'

scenario_contracts = {
    'skills/research-design/SKILL.md': (
        'OSDI', 'reusable research insight', 'Claim class',
    ),
    'skills/coresearch/references/field-modes.md': (
        'For SoCC work', 'multitenancy', 'cloud variability',
        'quality/performance/cost frontier',
    ),
    'skills/research-audit/SKILL.md': (
        'simulator', 'power-area-performance', 'warm-up', 'baseline',
    ),
    'skills/research-review/SKILL.md': (
        'IISWC measurement/workload characterization',
        'primary research contribution',
    ),
}
for rel, phrases in scenario_contracts.items():
    body = ' '.join(Path(rel).read_text().split())
    for phrase in phrases:
        assert phrase in body, f'{rel} missing acceptance-scenario contract: {phrase}'

for named_style in ('Alan', 'Ha', 'Oh'):
    assert named_style in agents, f'template dropped requested named style: {named_style}'
    assert named_style in field_modes, f'field modes dropped requested named style: {named_style}'

# Experiment work must stay experiment-first: implement, minimal smoke, real
# run, evidence-driven fix, then one release-gate regression pass.
experiment_policy = [
    'implement one experiment unit',
    'run one executable minimal smoke',
    'run the actual claim-bearing evaluation',
    'fix only from observed result/error',
    'run full regression once immediately before finalizing a claim',
]
for rel in (
    'templates/research/AGENTS.md',
    'skills/coresearch/SKILL.md',
    'skills/research-engineer/SKILL.md',
    'skills/research-loop/SKILL.md',
    'skills/coresearch/references/omx-pony-caveman.md',
):
    text = ' '.join(Path(rel).read_text().lower().split())
    for rule in experiment_policy:
        assert rule in text, f'{rel} missing experiment policy: {rule}'

agent_budget_policy = (
    'agents are allowed when',
    'owned scope',
    'expected output',
    'stop condition',
    'never add agents merely to re-check the same change',
)
for rel in (
    'templates/research/AGENTS.md',
    'skills/coresearch/SKILL.md',
    'skills/research-engineer/SKILL.md',
    'skills/research-loop/SKILL.md',
    'skills/coresearch/references/omx-pony-caveman.md',
):
    text = ' '.join(Path(rel).read_text().lower().split())
    for rule in agent_budget_policy:
        assert rule in text, f'{rel} missing agent budget policy: {rule}'

cadence_policy = (
    'one smallest targeted check',
    'auto-retry once',
    'at most two fix cycles',
    'no new artifact or error signal',
)
for rel in (
    'templates/research/AGENTS.md',
    'skills/coresearch/SKILL.md',
    'skills/research-engineer/SKILL.md',
    'skills/research-loop/SKILL.md',
):
    text = ' '.join(Path(rel).read_text().lower().split())
    for rule in cadence_policy:
        assert rule in text, f'{rel} missing cadence policy: {rule}'

research_first_rule = 'a passing build or test establishes artifact correctness, not scientific validity.'
for rel in (
    'templates/research/AGENTS.md',
    'skills/coresearch/SKILL.md',
    'skills/research-engineer/SKILL.md',
    'skills/research-loop/SKILL.md',
):
    text = ' '.join(Path(rel).read_text().lower().split())
    assert research_first_rule in text, f'{rel} missing research-first validity guard'

template_text = ' '.join(agents.lower().split())
assert 'test-verify loops' not in template_text
assert 'if a stage stalls or repeats with no new evidence' in template_text
assert 'twice that duration' in template_text
assert 'one execution lane per phase' in ' '.join(Path('skills/coresearch/references/routing.md').read_text().lower().split())

safe_execution = ' '.join(Path('skills/coresearch/references/execution-safe.md').read_text().lower().split())
for rule in (
    '## advisor gate',
    '## run discipline',
    '## artifact tiers',
    'omx ask claude',
    'project `.tmp/build-safe/`',
    'bounded summary',
    'do not `cat` a long log',
    'redact secrets',
    'never the full log',
):
    assert rule in safe_execution, f'execution-safe.md missing: {rule}'
assert '.tmp/' in Path('.gitignore').read_text()
for rel in (
    'AGENTS.md',
    'templates/research/AGENTS.md',
    'skills/coresearch/SKILL.md',
    'skills/research-engineer/SKILL.md',
    'skills/research-loop/SKILL.md',
):
    assert 'execution-safe.md' in Path(rel).read_text(), f'{rel} missing execution-safe reference'

root_agents = Path('AGENTS.md').read_text()
assert 'Coresearch Bundle Development Guidelines' in root_agents
assert 'OMX Research Agent System' not in root_agents

manifest = json.loads(Path('.codex-plugin/plugin.json').read_text())
assert manifest['skills'] == './skills/'
for forbidden in ('agents', 'prompts', 'hooks'):
    assert forbidden not in manifest, forbidden

skill_manifest = json.loads(Path('skills/manifest.json').read_text())
expected = {item['name'] for item in skill_manifest['owned']}
assert 'coresearch' in expected
assert all(Path('skills', name, 'SKILL.md').exists() for name in expected)
assert all((Path('skills', name) / '_coresearch').exists() for name in expected), 'owned skill missing _coresearch ownership marker'
assert 'aliases' not in skill_manifest
assert 'companions' not in skill_manifest, 'file-format companions purged; user invokes external format tools directly'
assert 'preferences' not in skill_manifest, 'caveman/ponytail inlined into owned omx-pony-caveman.md'
assert set(skill_manifest.get('external_routes', [])) == {
    'autopilot', 'autoresearch', 'best-practice-research', 'deep-interview',
    'ralph', 'ralplan', 'swarm', 'team', 'ultragoal', 'ultraqa',
}, 'external_routes must be exactly the 10 optional OMX acceleration lanes (single-source policy)'

skills = []
for f in sorted(Path('skills').glob('*/SKILL.md')):
    text = f.read_text()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    assert m, f'Missing frontmatter: {f}'
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    assert fm.get('name') == f.parent.name, (f, fm)
    assert fm.get('description') and len(fm['description']) > 40, f
    skills.append(fm['name'])

assert set(skills) == expected, sorted(set(skills) ^ expected)
print(f'PASS: skill frontmatter and catalog set ({len(skills)} skills)')
PY

python3 - <<'PY'
import json, re
from pathlib import Path

owned = {item['name'] for item in json.loads(Path('skills/manifest.json').read_text())['owned']}

# 1. The AGENTS.md template ships as a project prompt via `harness init --full`.
#    Every skill it lists as a canonical bullet must still be owned (catches
#    stale `pptx` / `research-pdfs` drift after a trim).
agents = Path('templates/research/AGENTS.md').read_text()
listed = set(re.findall(r'(?m)^- `([a-z][a-z0-9-]*)` — ', agents))
stale = sorted(name for name in listed if name not in owned)
assert not stale, f'AGENTS.md template lists non-owned skills: {stale}'

# 2. Every non-router role skill carries the canonical 5-section template,
#    as an ordered subsequence of its actual ## headings, so each role skill is
#    a valid loadable re-entry unit (heading order, not just presence). Headings
#    may carry a parenthetical or em-dash subtitle (e.g. "## Reject when (gates
#    3,7,8)" or "## Output — three views"), matched at a word boundary.
required = ['## What & When', '## Procedure', '## Output', '## Reject when', '## State & Handoff']
def is_section(h, need):
    return h.startswith(need) and (len(h) == len(need) or not (h[len(need)].isalnum() or h[len(need)] == '_'))
for f in sorted(Path('skills').glob('research-*/SKILL.md')):
    text = f.read_text()
    headings = re.findall(r'^## .+', text, re.M)
    i = 0
    for need in required:
        while i < len(headings) and not is_section(headings[i], need):
            i += 1
        assert i < len(headings), f'{f} missing or out-of-order heading: {need}'
        i += 1
print('PASS: AGENTS.md template skills are owned; role skills use the ordered 5-section template')
PY

python3 - <<'PY'
from pathlib import Path
refs = Path('skills/coresearch/references')
for name in ('evidence-grounding', 'execution-safe', 'research-contract', 'state-ledger', 'reasoning-skills'):
    assert (refs / f'{name}.md').exists(), f'missing shared ref: {name}.md'
PY
pass "shared evidence references exist"

python3 skills/research-survey/crawler.py --help >/tmp/research-skills-pdf-help.txt
grep -q -- '--dry-run' /tmp/research-skills-pdf-help.txt
grep -q -- '--yes-large' /tmp/research-skills-pdf-help.txt
grep -q -- '--allow-publisher-pdf' /tmp/research-skills-pdf-help.txt
pass "research-survey crawler safety flags exposed"

sample_dir="$(mktemp -d)"
cat > "$sample_dir/papers.md" <<'MD'
| # | 제목 | 저자 | 저널/학회 | 비고 |
|---|---|---|---|---|
| 1 | Attention Is All You Need | Vaswani et al. | NeurIPS | 2017 |
MD
python3 skills/research-survey/crawler.py "$sample_dir/papers.md" --dry-run --limit 1 >/tmp/research-skills-pdf-dryrun.txt
if [[ -d "$sample_dir/pdf" ]] && find "$sample_dir/pdf" -type f | grep -q .; then
  fail "crawler dry run created PDF files"
fi
pass "crawler dry run does not download files"

user_home="$(mktemp -d)"
echo "GLOBAL HEADER" > "$user_home/AGENTS.md"
./scripts/install.sh --scope user --codex-home "$user_home" --global-bridge >/tmp/research-skills-install-user-1.txt
[[ -f "$user_home/skills/research-loop/SKILL.md" ]] || fail "user install missing research-loop"
[[ -f "$user_home/skills/research-survey/crawler.py" ]] || fail "user install missing crawler"
grep -q 'GLOBAL HEADER' "$user_home/AGENTS.md" || fail "existing global AGENTS content was not preserved"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$user_home/AGENTS.md" || fail "user bridge missing"
grep -qF "$BRIDGE_HANDOFF_LINE" "$user_home/AGENTS.md" || fail "user bridge missing subagent handoff line"
count="$(grep -c 'RESEARCH_AGENT_SKILLS:START' "$user_home/AGENTS.md")"
[[ "$count" == "1" ]] || fail "user bridge count after first install: $count"
./scripts/install.sh --scope user --codex-home "$user_home" --global-bridge >/tmp/research-skills-install-user-2.txt
count="$(grep -c 'RESEARCH_AGENT_SKILLS:START' "$user_home/AGENTS.md")"
[[ "$count" == "1" ]] || fail "user bridge duplicated after second install: $count"
ls "$user_home"/AGENTS.md.bak.* >/dev/null 2>&1 || fail "bridge backup missing on second install"
pass "user install copy mode and bridge idempotency"

user_link_home="$(mktemp -d)"
mkdir -p "$user_link_home/skills"
ln -s "$ROOT_DIR/skills/paper-design" "$user_link_home/skills/paper-design"
mkdir -p "$user_link_home/skills/paper-review"
cat > "$user_link_home/skills/paper-review/SKILL.md" <<'MD'
---
name: paper-review
description: Venue-calibrated simulated review and score forecast for research papers.
---
# Paper Review
MD
ln -s "$user_link_home/not-coresearch" "$user_link_home/skills/claim-check"
./scripts/install.sh --scope user --codex-home "$user_link_home" --mode symlink --force >/tmp/research-skills-install-user-symlink.txt 2>/tmp/research-skills-install-user-symlink.err
[[ -L "$user_link_home/skills/research-design" ]] || fail "user symlink install missing research-design symlink"
[[ ! -e "$user_link_home/skills/paper-design" && ! -L "$user_link_home/skills/paper-design" ]] || fail "user symlink install unexpectedly kept paper-design alias"
[[ ! -e "$user_link_home/skills/paper-review" && ! -L "$user_link_home/skills/paper-review" ]] || fail "user symlink install unexpectedly kept copied paper-review alias"
[[ -L "$user_link_home/skills/claim-check" ]] || fail "user symlink install pruned non-Coresearch broken legacy-name symlink"
grep -q 'points outside Coresearch' /tmp/research-skills-install-user-symlink.err || fail "user symlink install did not warn for non-Coresearch broken legacy-name symlink"
[[ -L "$user_link_home/skills/research-loop" ]] || fail "user symlink install missing research-loop symlink"
resolved="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve())' "$user_link_home/skills/research-loop")"
[[ "$resolved" == "$ROOT_DIR/skills/research-loop" ]] || fail "user symlink target mismatch: $resolved"
pass "user install symlink mode for repo-auto-update"

harness_copy_home="$(mktemp -d)"
./harness install --scope user --codex-home "$harness_copy_home" >/tmp/research-skills-harness-install-user-copy.txt
[[ -f "$harness_copy_home/skills/research-loop/SKILL.md" ]] || fail "harness install user copy missing research-loop"
[[ ! -L "$harness_copy_home/skills/research-loop" ]] || fail "harness install user copy unexpectedly symlinked research-loop"
pass "harness install user copy mode"

harness_home="$(mktemp -d)"
./harness link --codex-home "$harness_home" >/tmp/research-skills-harness-link.txt
[[ -L "$harness_home/skills/research-loop" ]] || fail "harness link did not symlink research-loop"
./harness status --codex-home "$harness_home" --target . >/tmp/research-skills-harness-status.txt
grep -q 'research-loop: symlink:OK' /tmp/research-skills-harness-status.txt || fail "harness status did not report symlink OK"
pass "harness link/status"

both_codex_home="$(mktemp -d)"
both_claude_home="$(mktemp -d)"
./harness link --surface both --codex-home "$both_codex_home" --claude-home "$both_claude_home" >/tmp/research-skills-harness-link-both.txt
[[ -L "$both_codex_home/skills/coresearch" ]] || fail "harness link both missing codex coresearch"
[[ -L "$both_claude_home/skills/coresearch" ]] || fail "harness link both missing claude coresearch"
[[ -L "$both_claude_home/skills/research-design" ]] || fail "harness link both missing claude research-design"
[[ ! -e "$both_claude_home/skills/paper-design" && ! -L "$both_claude_home/skills/paper-design" ]] || fail "harness link both unexpectedly kept claude paper-design alias"
mkdir -p "$both_codex_home/plugins/cache/vendor/skills/research-loop"
cat > "$both_codex_home/plugins/cache/vendor/skills/research-loop/SKILL.md" <<'MD'
---
name: research-loop
description: External Codex plugin skill with same name as a Coresearch-owned skill.
---
# External research-loop
MD
mkdir -p "$both_claude_home/plugins/marketplaces/vendor/skills/research-loop"
cat > "$both_claude_home/plugins/marketplaces/vendor/skills/research-loop/SKILL.md" <<'MD'
---
name: research-loop
description: External Claude plugin skill with same name as a Coresearch-owned skill.
---
# External research-loop
MD
mkdir -p "$both_codex_home/plugins/cache/vendor/skills/ponytail"
cat > "$both_codex_home/plugins/cache/vendor/skills/ponytail/SKILL.md" <<'MD'
---
name: ponytail
description: External preference skill for over-engineering review.
---
# Ponytail
MD
ln -s "$both_codex_home/.orchestra/skills/old-research" "$both_codex_home/skills/old-research"
./harness inventory --codex-home "$both_codex_home" --claude-home "$both_claude_home" --include-plugins >/tmp/research-skills-harness-inventory-overlap.txt
grep -q $'codex-user\towned\tresearch-loop' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify codex user research-loop as owned"
grep -q $'claude-user\towned\tresearch-loop' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify claude user research-loop as owned"
grep -q $'codex-cache\tplugin-overlap\tresearch-loop' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify codex cache research-loop as plugin-overlap"
grep -q $'claude-marketplace\tplugin-overlap\tresearch-loop' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify marketplace research-loop as plugin-overlap"
grep -q $'codex-cache\tpreference\tponytail' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not classify ponytail as preference"
grep -q $'codex-user\tlegacy-orchestra\told-research' /tmp/research-skills-harness-inventory-overlap.txt || fail "inventory did not surface legacy orchestra symlink"
pass "harness link --surface both"

cmd_bin="$(mktemp -d)"
./harness self-install --bin-dir "$cmd_bin" >/tmp/research-skills-harness-self-install.txt
[[ -L "$cmd_bin/harness" ]] || fail "harness self-install did not create symlink"
"$cmd_bin/harness" status --codex-home "$harness_home" --target . >/tmp/research-skills-installed-command-status.txt
grep -q 'research-loop: symlink:OK' /tmp/research-skills-installed-command-status.txt || fail "installed harness command failed status"
./harness self-uninstall --bin-dir "$cmd_bin" >/tmp/research-skills-harness-self-uninstall.txt
[[ ! -e "$cmd_bin/harness" && ! -L "$cmd_bin/harness" ]] || fail "harness self-uninstall did not remove symlink"
pass "harness self-install/self-uninstall"

global_home="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$global_home/AGENTS.md"
./harness global --codex-home "$global_home" >/tmp/research-skills-harness-global-dry.txt
grep -q 'Dry run only' /tmp/research-skills-harness-global-dry.txt || fail "harness global dry-run missing"
! grep -q 'RESEARCH_AGENT_SKILLS:START' "$global_home/AGENTS.md" || fail "harness global dry-run wrote file"
./harness global --codex-home "$global_home" -y >/tmp/research-skills-harness-global-apply.txt
grep -q 'RESEARCH_AGENT_SKILLS:START' "$global_home/AGENTS.md" || fail "harness global apply missing bridge"
grep -qF "$BRIDGE_HANDOFF_LINE" "$global_home/AGENTS.md" || fail "harness global bridge missing subagent handoff line"
./harness global --codex-home "$global_home" --remove -y >/tmp/research-skills-harness-global-remove.txt
! grep -q 'RESEARCH_AGENT_SKILLS:START' "$global_home/AGENTS.md" || fail "harness global remove left bridge"
pass "harness global bridge dry/apply/remove"

doctor_home="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$doctor_home/AGENTS.md"
./harness link --codex-home "$doctor_home" >/tmp/research-skills-harness-doctor-link.txt
CLAUDE_HOME="$doctor_home" ./harness doctor --codex-home "$doctor_home" --target . --strict >/tmp/research-skills-harness-doctor.txt
grep -q 'Doctor result: PASS' /tmp/research-skills-harness-doctor.txt || fail "harness doctor did not pass"
pass "harness doctor strict"

broken_home="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$broken_home/AGENTS.md"
./harness link --codex-home "$broken_home" >/tmp/research-skills-harness-broken-link-setup.txt
rm -f "$broken_home/skills/research-loop"
ln -s "$broken_home/does-not-exist" "$broken_home/skills/research-loop"
if CLAUDE_HOME="$broken_home" ./harness doctor --codex-home "$broken_home" --target . --strict >/tmp/research-skills-harness-broken-link-doctor.txt 2>&1; then
  fail "harness doctor passed with a broken skill symlink"
fi
grep -q 'bad skill install: research-loop: symlink:BROKEN' /tmp/research-skills-harness-broken-link-doctor.txt || fail "harness doctor did not report broken research-loop symlink"
pass "harness doctor rejects broken skill symlinks"

repair_home="$(mktemp -d)"
repair_bin="$(mktemp -d)"
printf '# oh-my-codex - Intelligent Multi-Agent Orchestration\n<!-- OMX:RUNTIME:START -->\n<!-- OMX:RUNTIME:END -->\n' > "$repair_home/AGENTS.md"
CLAUDE_HOME="$repair_home" ./harness repair --codex-home "$repair_home" --bin-dir "$repair_bin" --target . --no-validate >/tmp/research-skills-harness-repair.txt
[[ -L "$repair_home/skills/research-loop" ]] || fail "harness repair did not relink research-loop"
[[ -L "$repair_bin/harness" ]] || fail "harness repair did not install harness command"
grep -q 'Doctor result: PASS' /tmp/research-skills-harness-repair.txt || fail "harness repair did not run strict doctor"
pass "harness repair relink/self-install/doctor"

update_home="$(mktemp -d)"
./harness update --codex-home "$update_home" --no-validate >/tmp/research-skills-harness-update.txt
[[ -L "$update_home/skills/research-loop" ]] || fail "harness update did not relink skills"
grep -q 'Update complete' /tmp/research-skills-harness-update.txt || fail "harness update did not complete"
pass "harness update relink"

update_both_codex_home="$(mktemp -d)"
update_both_claude_home="$(mktemp -d)"
./harness update --surface both --codex-home "$update_both_codex_home" --claude-home "$update_both_claude_home" --no-validate >/tmp/research-skills-harness-update-both.txt
[[ -L "$update_both_codex_home/skills/research-loop" ]] || fail "harness update --surface both missing codex link"
[[ -L "$update_both_claude_home/skills/research-loop" ]] || fail "harness update --surface both missing claude link"
pass "harness update --surface both relink"

harness_project="$(mktemp -d)"
./harness init "$harness_project" --bridge >/tmp/research-skills-harness-init-dry.txt
grep -q 'Dry run only' /tmp/research-skills-harness-init-dry.txt || fail "harness init dry-run did not report dry run"
[[ ! -f "$harness_project/AGENTS.md" ]] || fail "harness init dry-run wrote AGENTS.md"
./harness init "$harness_project" --bridge -y >/tmp/research-skills-harness-init-apply.txt
grep -q 'RESEARCH_AGENT_SKILLS:START' "$harness_project/AGENTS.md" || fail "harness init bridge apply missing bridge"
grep -qF "$BRIDGE_HANDOFF_LINE" "$harness_project/AGENTS.md" || fail "harness init bridge missing subagent handoff line"
./harness init --target "$harness_project" --mode bridge --apply >/tmp/research-skills-harness-init-apply-2.txt
count="$(grep -c 'RESEARCH_AGENT_SKILLS:START' "$harness_project/AGENTS.md")"
[[ "$count" == "1" ]] || fail "harness bridge duplicated: $count"
target_override_a="$(mktemp -d)"
target_override_b="$(mktemp -d)"
./harness init "$target_override_a" --target "$target_override_b" --bridge -y >/tmp/research-skills-harness-target-override.txt
[[ ! -f "$target_override_a/AGENTS.md" ]] || fail "--target did not override positional target"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$target_override_b/AGENTS.md" || fail "--target override did not write chosen target"
grep -qF "$BRIDGE_HANDOFF_LINE" "$target_override_b/AGENTS.md" || fail "--target override bridge missing subagent handoff line"
pass "harness init shorthand/target-override bridge dry/apply/idempotent"

# omx-conditional bridge: default bridges when omx present; CORESEARCH_OMX_CHECK=0 seam skips when absent; --bridge forces.
omx_present_default="$(mktemp -d)"
omx_stub_dir="$(mktemp -d)"
printf '#!/usr/bin/env sh\nexit 0\n' > "$omx_stub_dir/omx"
chmod +x "$omx_stub_dir/omx"
PATH="$omx_stub_dir:$PATH" ./harness init "$omx_present_default" -y </dev/null >/tmp/research-skills-harness-init-omx-present.txt
grep -q 'omx detected' /tmp/research-skills-harness-init-omx-present.txt || fail "harness init default did not report omx detection"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$omx_present_default/AGENTS.md" || fail "harness init default did not bridge when omx present"

omx_absent_default="$(mktemp -d)"
CORESEARCH_OMX_CHECK=0 ./harness init "$omx_absent_default" -y </dev/null >/tmp/research-skills-harness-init-omx-absent.txt
grep -q 'omx not detected' /tmp/research-skills-harness-init-omx-absent.txt || fail "harness init absent-default did not notify omx absent"
grep -q 'Skipping OMX-aware bridge' /tmp/research-skills-harness-init-omx-absent.txt || fail "harness init absent-default did not skip bridge"
[[ ! -f "$omx_absent_default/AGENTS.md" ]] || fail "harness init absent-default wrote AGENTS.md (should skip)"

omx_absent_force="$(mktemp -d)"
CORESEARCH_OMX_CHECK=0 ./harness init "$omx_absent_force" --bridge -y </dev/null >/tmp/research-skills-harness-init-omx-force.txt
grep -q 'INFO omx not detected' /tmp/research-skills-harness-init-omx-force.txt || fail "harness init absent-force did not emit INFO"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$omx_absent_force/AGENTS.md" || fail "harness init absent-force did not bridge (--bridge must force)"
pass "harness init omx-conditional bridge: present/default bridges, absent/default skips, absent/--bridge forces"

noninteractive_init="$(mktemp -d)"
printf 'ORIGINAL\n' > "$noninteractive_init/AGENTS.md"
(cd "$noninteractive_init" && PATH="$omx_stub_dir:$PATH" "$ROOT_DIR/harness" init </dev/null) >/tmp/research-skills-harness-init-nontty.txt
grep -q 'Dry run only' /tmp/research-skills-harness-init-nontty.txt || fail "harness init non-TTY did not stay dry-run"
! grep -q 'Interactive project setup' /tmp/research-skills-harness-init-nontty.txt || fail "harness init non-TTY opened wizard"
grep -q '^ORIGINAL$' "$noninteractive_init/AGENTS.md" || fail "harness init non-TTY modified existing AGENTS.md"

wizard_full="$(mktemp -d)"
(cd "$wizard_full" && printf '\n2\n2\n' | "$ROOT_DIR/harness" init --interactive) >/tmp/research-skills-harness-init-wizard.txt
grep -q 'Interactive project setup' /tmp/research-skills-harness-init-wizard.txt || fail "harness init interactive wizard did not start"
grep -q 'Selected mode: full' /tmp/research-skills-harness-init-wizard.txt || fail "harness init interactive wizard did not select full mode"
grep -q 'Selected action: apply' /tmp/research-skills-harness-init-wizard.txt || fail "harness init interactive wizard did not select apply action"
cmp -s templates/research/AGENTS.md "$wizard_full/AGENTS.md" || fail "harness init interactive wizard did not write full template"
pass "harness init non-TTY safe; explicit wizard defaults to . / full / apply"

rollback_project="$(mktemp -d)"
printf 'ORIGINAL\n' > "$rollback_project/AGENTS.md"
./harness init "$rollback_project" --bridge -y >/tmp/research-skills-harness-rollback-setup.txt
./harness rollback --scope project "$rollback_project" >/tmp/research-skills-harness-rollback-dry.txt
grep -q 'Dry run only' /tmp/research-skills-harness-rollback-dry.txt || fail "harness rollback dry-run missing"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$rollback_project/AGENTS.md" || fail "rollback dry-run modified file"
./harness rollback --scope project "$rollback_project" -y >/tmp/research-skills-harness-rollback-apply.txt
grep -q '^ORIGINAL$' "$rollback_project/AGENTS.md" || fail "rollback did not restore original"
! grep -q 'RESEARCH_AGENT_SKILLS:START' "$rollback_project/AGENTS.md" || fail "rollback left bridge"
pass "harness rollback positional dry/apply"

harness_full="$(mktemp -d)"
./harness init "$harness_full" --full -y >/tmp/research-skills-harness-full.txt
cmp -s templates/research/AGENTS.md "$harness_full/AGENTS.md" || fail "harness full init did not copy research template"
./harness diff "$harness_full" --full >/tmp/research-skills-harness-diff-full.txt
grep -q 'No AGENTS.md changes needed' /tmp/research-skills-harness-diff-full.txt || fail "harness diff positional full did not work"
legacy_full="$(mktemp -d)"
./harness init "$legacy_full" --mode full --apply >/tmp/research-skills-harness-legacy-full.txt
cmp -s templates/research/AGENTS.md "$legacy_full/AGENTS.md" || fail "legacy --mode full --apply did not copy research template"
pass "harness init full shorthand and legacy template copy"

project_dir="$(mktemp -d)"
./scripts/install.sh --scope project --project-dir "$project_dir" --project-bridge --mode symlink >/tmp/research-skills-install-project.txt
[[ -L "$project_dir/.codex/skills/research-design" ]] || fail "project symlink install missing research-design symlink"
[[ ! -e "$project_dir/.codex/skills/paper-design" && ! -L "$project_dir/.codex/skills/paper-design" ]] || fail "project symlink install unexpectedly kept paper-design alias"
[[ -L "$project_dir/.codex/skills/research-loop" ]] || fail "project symlink install missing research-loop symlink"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$project_dir/AGENTS.md" || fail "project bridge missing"
grep -qF "$BRIDGE_HANDOFF_LINE" "$project_dir/AGENTS.md" || fail "project bridge missing subagent handoff line"
pass "project install symlink mode and bridge"

harness_project_install="$(mktemp -d)"
./harness install --scope project --project-dir "$harness_project_install" --project-bridge >/tmp/research-skills-harness-install-project.txt
[[ -f "$harness_project_install/.codex/skills/research-loop/SKILL.md" ]] || fail "harness install project missing research-loop"
grep -q 'RESEARCH_AGENT_SKILLS:START' "$harness_project_install/AGENTS.md" || fail "harness install project bridge missing"
grep -qF "$BRIDGE_HANDOFF_LINE" "$harness_project_install/AGENTS.md" || fail "harness install project bridge missing subagent handoff line"
pass "harness install project copy mode and bridge"

project_full="$(mktemp -d)"
./scripts/install.sh --scope project --project-dir "$project_full" --full-project-agents >/tmp/research-skills-install-full-project.txt
cmp -s templates/research/AGENTS.md "$project_full/AGENTS.md" || fail "full project AGENTS install differs"
pass "full project AGENTS install when absent"

if command -v omx >/dev/null 2>&1; then
  omx --version >/tmp/research-skills-omx-version.txt 2>&1 || fail "omx exists but version failed"
  pass "omx available: $(head -n 1 /tmp/research-skills-omx-version.txt)"
else
  echo "WARN: omx not found on PATH; skipped runtime availability check"
fi

python3 - <<'PY'
# #5: every depends_on: target in a research-*/SKILL.md frontmatter must resolve
# to an existing file when joined to the skill dir.
import re
from pathlib import Path

dead = []
checked = 0
for f in sorted(Path('skills').glob('research-*/SKILL.md')):
    text = f.read_text()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    assert m, f'Missing frontmatter: {f}'
    lines = m.group(1).splitlines()
    for idx, line in enumerate(lines):
        if not line.startswith('depends_on:'):
            continue
        rest = line.split(':', 1)[1].strip()
        targets = []
        if rest:
            targets.append(rest)
        for nxt in lines[idx + 1:]:
            if not nxt.startswith((' ', '\t')):
                break
            lm = re.match(r'\s+-\s+(.+?)\s*$', nxt)
            if lm:
                targets.append(lm.group(1).strip())
        for rel in targets:
            checked += 1
            resolved = (f.parent / rel).resolve()
            if not resolved.exists():
                dead.append((str(f), rel, str(resolved)))
assert not dead, f'unresolved depends_on targets: {dead}'
print(f'PASS: depends_on targets resolve ({checked} checked)')
PY

python3 - <<'PY'
# #6: lock the cross-skill ledger contract. The canonical *_state keys are read
# straight from state-ledger.md (single source of truth): every research-*/SKILL.md
# may reference only those keys, and each documented producer still names its key.
# Catches producer-key drift across re-entry hops (the headline contract risk).
import re
from pathlib import Path

ledger_doc = Path('skills/coresearch/references/state-ledger.md').read_text()
m = re.search(r'```yaml\n(.*?)```', ledger_doc, re.S)
assert m, 'state-ledger.md schema block not found'
schema = m.group(1)
doc_top = {ln.split(':', 1)[0] for ln in schema.splitlines() if re.match(r'^[a-z_]+:', ln)}
canonical = {k for k in doc_top if k.endswith('_state')}
assert canonical == {'source_state', 'claim_state', 'gap_state',
                     'hypothesis_state', 'quality_state'}, sorted(canonical)

# skills that write a ledger key must still name it in State & Handoff.
producers = {
    'research-survey': 'source_state',
    'research-audit': 'source_state',
    'research-gap': 'gap_state',
    'research-loop': 'hypothesis_state',
    'research-causal': 'hypothesis_state',
    'research-dialectic': 'claim_state',
    'research-verify': 'claim_state',
    'research-qualitative': 'quality_state',
    'research-adversary': 'quality_state',
    'research-review': 'quality_state',
}
for skill, key in producers.items():
    text = (Path('skills') / skill / 'SKILL.md').read_text()
    assert key in text, f'{skill} State & Handoff dropped canonical ledger key {key}'

# no skill may reference a *_state token outside the canonical set (typos, drift).
token_re = re.compile(r'\b([a-z][a-z0-9_]*_state)\b')
bad = []
for f in sorted(Path('skills').glob('research-*/SKILL.md')):
    for tok in token_re.finditer(f.read_text()):
        if tok.group(1) not in canonical:
            bad.append((str(f), tok.group(1)))
assert not bad, f'non-canonical ledger *_state tokens in skills: {bad}'
print(f'PASS: ledger state keys locked to state-ledger.md ({len(canonical)} keys); '
      f'{len(producers)} producer keys present; no non-canonical *_state tokens')
PY

gate_tmp="$(mktemp -d)"
{
  printf '| # | 제목 | 저자 | 저널/학회 | 비고 |\n|---|---|---|---|---|\n'
  for i in $(seq 1 35); do
    printf '| %d | Alpha%d Study | Smith%d | Venue | 2020 |\n' "$i" "$i" "$i"
  done
} > "$gate_tmp/papers.md"
# #9: --dry-run bypasses the >30 gate by design (the gate requires not dry_run),
# so to exercise the gate branch with NO network we run WITHOUT --dry-run: the
# refusal prints and crawl() returns before any process_one()/HTTP call.
python3 skills/research-survey/crawler.py "$gate_tmp/papers.md" >/tmp/research-skills-crawler-gate.txt 2>&1 || true
grep -q 'refusing to process more than 30 papers' /tmp/research-skills-crawler-gate.txt || fail "crawler did not refuse >30 papers without --yes-large"
if find "$gate_tmp" -type f | grep -qv 'papers\.md$'; then
  fail "crawler >30 gate wrote files before refusal"
fi
python3 skills/research-survey/crawler.py "$gate_tmp/papers.md" --dry-run >/tmp/research-skills-crawler-gate-dry.txt 2>&1
grep -q 'DRY RUN' /tmp/research-skills-crawler-gate-dry.txt || fail "crawler --dry-run did not short-circuit past the gate"
rm -rf "$gate_tmp"
pass "crawler >30-paper gate refuses without --yes-large and writes no files; --dry-run bypasses gate (no network)"

python3 - <<'PY'
# #10: resolve relative markdown links and bare references/*.md mentions under
# skills/ against each file's dir; assert every target exists.
import re
from pathlib import Path

link_re = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
# Lookbehind skips the trailing segment of a longer ../coresearch/references/...
# path, so only standalone references/ mentions are resolved.
ref_re = re.compile(r'(?<![\w./])references/[A-Za-z0-9_./-]+\.md')

dead = []
checked = 0
for md in sorted(Path('skills').rglob('*.md')):
    text = md.read_text()
    targets = []
    for m in link_re.finditer(text):
        raw = m.group(2).strip()
        if raw.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        path_part = raw.split('#', 1)[0]
        if path_part:
            targets.append(path_part)
    for m in ref_re.finditer(text):
        targets.append(m.group(0))
    for t in targets:
        checked += 1
        resolved = (md.parent / t).resolve()
        if not resolved.exists():
            dead.append((str(md), t, str(resolved)))
assert not dead, f'dead relative links under skills/: {dead}'
print(f'PASS: no dead relative links under skills/ ({checked} targets)')
PY

pass "all validations completed"
