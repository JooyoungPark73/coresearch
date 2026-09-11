#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_TEMPLATE = ROOT / "templates" / "research" / "AGENTS.md"
SKILL_MANIFEST = ROOT / "skills" / "manifest.json"
AGENT_MANIFEST = ROOT / "agents" / "manifest.json"
ROLE_MARKER = "coresearch-managed: role-description-version="
CODEX_AGENTS_START = "# >>> coresearch-managed: agents:start >>>"
CODEX_AGENTS_END = "# <<< coresearch-managed: agents:end <<<"


def skill_manifest() -> dict:
    return json.loads(SKILL_MANIFEST.read_text())


def owned_skill_names() -> list[str]:
    return [item["name"] for item in skill_manifest()["owned"]]


def agent_manifest() -> dict:
    return json.loads(AGENT_MANIFEST.read_text())


def roles() -> list[dict]:
    return agent_manifest()["roles"]


def role_names() -> list[str]:
    return [item["name"] for item in roles()]


SKILLS = owned_skill_names()
ROLES = role_names()

START = "<!-- RESEARCH_AGENT_SKILLS:START -->"
END = "<!-- RESEARCH_AGENT_SKILLS:END -->"


def codex_home(value: str | None = None) -> Path:
    return Path(value or os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser().resolve()


def codex_skills_root(value: str | None = None) -> Path:
    return Path(value or Path.home() / ".agents" / "skills").expanduser().resolve()


def claude_home(value: str | None = None) -> Path:
    return Path(value or os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude").expanduser().resolve()


def default_bin_dir() -> Path:
    return Path(os.environ.get("RESEARCH_HARNESS_BIN_DIR") or Path.home() / ".local" / "bin").expanduser().resolve()


def bridge_block() -> str:
    role_skills = ", ".join(f"`{name}`" for name in owned_skill_names() if name != "coresearch")
    native_roles = ", ".join(f"`{name}`" for name in role_names())
    return f"""{START}
Coresearch skills are installed. For broad academic research tasks, load `coresearch` first; for narrow tasks, load the smallest matching skill: {role_skills}.
Bounded native roles are installed: {native_roles}. Give each assignment one fixed role, a unique ID, dependencies, the primary skill and field mode, claim/evidence target, owned and read-only scope, confidentiality limits, expected artifact, validation, stop condition, and active working modes. Independent assignments may run concurrently; the parent owns joins, integration, and verification. Role results return to the parent, which re-enters `coresearch` before selecting another stage.
Keep durable research state in `docs/research/decisions/ledger.yaml`; use `docs/research/runs/<run-id>/` for mission, sandbox, and result artifacts, with one schema-version-2 `role_runs` entry per attempted assignment. Do not create provider-specific state forests. Verify current venue rules and citations from official or primary sources when exactness matters.
{END}
"""


def remove_codex_agents_block(text: str) -> str:
    has_start = CODEX_AGENTS_START in text
    has_end = CODEX_AGENTS_END in text
    if has_start != has_end:
        raise ValueError("incomplete Coresearch Codex registration markers")
    if not has_start:
        return text
    before, rest = text.split(CODEX_AGENTS_START, 1)
    _old, after = rest.split(CODEX_AGENTS_END, 1)
    joined = before.rstrip() + ("\n\n" if before.strip() and after.strip() else "") + after.lstrip()
    return joined.rstrip() + "\n" if joined.strip() else ""


def upsert_bridge_text(text: str) -> str:
    block = bridge_block().strip()
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _old, after = rest.split(END, 1)
        return (before.rstrip() + "\n\n" + block + "\n" + after.lstrip()).rstrip() + "\n"
    if text.strip():
        return text.rstrip() + "\n\n" + block + "\n"
    return block + "\n"


def remove_bridge_text(text: str) -> str:
    if START not in text or END not in text:
        return text
    before, rest = text.split(START, 1)
    _old, after = rest.split(END, 1)
    return (before.rstrip() + "\n\n" + after.lstrip()).rstrip() + "\n"


def project_agents_candidate(target: Path, mode: str, replace: bool) -> str:
    path = target / "AGENTS.md"
    current = path.read_text() if path.exists() else ""
    if mode == "bridge":
        return upsert_bridge_text(current)
    if mode == "full":
        return RESEARCH_TEMPLATE.read_text()
    raise ValueError(mode)


def unified_diff(old: str, new: str, fromfile: str, tofile: str) -> str:
    return "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile=fromfile, tofile=tofile))


BACKUP_KEEP = 8


def _backup_index(path: Path) -> int:
    m = re.search(r"\.bak\.(\d+)$", path.name)
    return int(m.group(1)) if m else -1


def atomic_write(path: Path, text: str) -> None:
    """Write via a temp file + os.replace so an interrupt never truncates the target."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp.write_text(text)
    os.replace(tmp, path)


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    idx = 1
    while path.with_name(f"{path.name}.bak.{idx}").exists():
        idx += 1
    candidate = path.with_name(f"{path.name}.bak.{idx}")
    shutil.copy2(path, candidate)
    # Prune oldest beyond the retention cap so re-runs do not accumulate backups.
    backups = sorted(
        (p for p in path.parent.glob(f"{path.name}.bak.*") if p.exists()),
        key=_backup_index,
    )
    for stale in backups[:-BACKUP_KEEP]:
        stale.unlink(missing_ok=True)
    return candidate


def latest_backup(path: Path) -> Path | None:
    """Newest backup by sequence index, not mtime — copy2 preserves source mtime,
    so mtime ordering can return the current content and make rollback a no-op."""
    candidates = sorted(
        (p for p in path.parent.glob(f"{path.name}.bak.*") if p.exists()),
        key=_backup_index,
    )
    return candidates[-1] if candidates else None


def path_has_dir(directory: Path) -> bool:
    paths = os.environ.get("PATH", "").split(os.pathsep)
    return str(directory) in paths


def is_repo_launcher(path: Path) -> bool:
    if not path.exists() and not path.is_symlink():
        return False
    try:
        return path.resolve(strict=False) in {(ROOT / "harness").resolve(), (ROOT / "bin" / "harness").resolve(), (ROOT / "scripts" / "harness.py").resolve()}
    except OSError:
        return False


def run(cmd: list[str], *, cwd: Path | None = None) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.call(cmd, cwd=str(cwd) if cwd else None)


def arg_target(args: argparse.Namespace) -> str:
    return getattr(args, "target", None) or getattr(args, "target_arg", None) or "."


def add_mode_flags(parser: argparse.ArgumentParser) -> None:
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--mode", choices=["bridge", "full"], dest="mode", default=None, help="legacy explicit mode selector")
    mode.add_argument("--bridge", action="store_const", const="bridge", dest="mode", help="use the small project bridge block")
    mode.add_argument("--full", action="store_const", const="full", dest="mode", help="use the full research AGENTS.md template")
    parser.set_defaults(mode="bridge")


def add_apply_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-y", "--yes", "--apply", dest="apply", action="store_true", help="write changes; explicit commands default to dry-run diff")


def prompt_text(label: str, default: str) -> str:
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{label}{suffix}: ").strip()
    except EOFError:
        value = ""
    return value or default


def prompt_bool(label: str, default: bool) -> bool:
    marker = "Y/n" if default else "y/N"
    try:
        value = input(f"{label} [{marker}]: ").strip().lower()
    except EOFError:
        value = ""
    if not value:
        return default
    return value in {"y", "yes", "1", "true", "t"}


def prompt_choice(label: str, choices: list[tuple[str, str]], default: str) -> str:
    print(label + ":")
    for idx, (value, description) in enumerate(choices, start=1):
        default_marker = " (default)" if value == default else ""
        print(f"  {idx}) {value}{default_marker} - {description}")
    valid_values = {value for value, _description in choices}
    while True:
        try:
            raw = input(f"Choose [default: {default}]: ").strip().lower()
        except EOFError:
            raw = ""
        if not raw:
            return default
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(choices):
                return choices[idx - 1][0]
        matches = [value for value in valid_values if value.startswith(raw)]
        if len(matches) == 1:
            return matches[0]
        print("Invalid choice. Enter a number or choice name.")


def should_interactive_init(args: argparse.Namespace) -> bool:
    if getattr(args, "interactive", False):
        return True
    raw_argv = getattr(args, "_raw_argv", [])
    return raw_argv == ["init"] and sys.stdin.isatty()


def explicit_init_mode(args: argparse.Namespace) -> str | None:
    raw_argv = getattr(args, "_raw_argv", [])
    for idx, token in enumerate(raw_argv):
        if idx == 0:
            continue
        if token == "--bridge":
            return "bridge"
        if token == "--full":
            return "full"
        if token == "--mode" and idx + 1 < len(raw_argv):
            return raw_argv[idx + 1]
        if token.startswith("--mode="):
            return token.split("=", 1)[1]
    return None


def apply_interactive_init(args: argparse.Namespace) -> None:
    print("# Interactive project setup")
    target = prompt_text("Target directory", arg_target(args))
    mode = prompt_choice(
        "Install mode",
        [
            ("bridge", "preserve AGENTS.md and add a small research bridge block"),
            ("full", "copy templates/research/AGENTS.md as the project AGENTS.md"),
        ],
        explicit_init_mode(args) or "full",
    )
    action = prompt_choice(
        "Action",
        [
            ("dry-run", "preview diff only"),
            ("apply", "write AGENTS.md, creating a backup first when needed"),
        ],
        "apply",
    )
    replace = getattr(args, "replace", False)
    target_path = Path(target).expanduser()
    if mode == "full" and (target_path / "AGENTS.md").exists():
        replace = prompt_bool("Existing AGENTS.md found. Allow full replacement?", replace)

    args.target = target
    args.target_arg = None
    args.mode = mode
    args.apply = action == "apply"
    args.replace = replace
    print()
    print(f"Selected target: {Path(target).expanduser().resolve()}")
    print(f"Selected mode: {args.mode}")
    print(f"Selected action: {'apply' if args.apply else 'dry-run'}")
    if args.mode == "full":
        print(f"Replace existing AGENTS.md: {'yes' if args.replace else 'no'}")
    print()


def assert_no_broken_repo_symlinks() -> list[Path]:
    broken: list[Path] = []
    skip = {".git", ".tmp", "tmp", "__pycache__"}
    for path in ROOT.rglob("*"):
        if any(part in skip for part in path.relative_to(ROOT).parts):
            continue
        if path.is_symlink() and not path.exists():
            broken.append(path)
    return broken


def _install_roots(codex_skills: Path, codex_roles: Path, claude_skills: Path, claude_roles: Path) -> list[Path]:
    """Candidate installed skill and role surfaces scanned for broken links.

    Tolerant of absent directories; callers filter by existence. Shared by
    broken_install_symlinks (the scan) and cmd_doctor (the report label) so
    the scanned set and the reported set cannot drift apart.
    """
    return [codex_skills, codex_roles, claude_skills, claude_roles]


def broken_install_symlinks(roots: list[Path]) -> list[Path]:
    broken: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for entry in root.iterdir():
            if entry.is_symlink() and not entry.exists():
                broken.append(entry)
    return broken


REMOVED_SKILLS = {
    "paper-design", "paper-survey", "paper-figures", "paper-rewrite",
    "paper-review", "paper-proofread", "rebuttal-plan", "claim-check",
    "pdf-crawl", "research-guidelines", "pptx", "research-pdfs",
    "research-gap", "research-dialectic", "research-causal",
    "research-audit", "research-adversary", "research-rebuttal",
}


def _remove_entry(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _link_target(path: Path) -> Path:
    target = Path(os.readlink(path))
    if not target.is_absolute():
        target = path.parent / target
    return target.resolve(strict=False)


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve())
        return True
    except (OSError, ValueError):
        return False


def _is_managed_entry(path: Path, kind: str) -> bool:
    if path.is_symlink():
        target = _link_target(path)
        source_root = ROOT / ("skills" if kind == "skill" else "agents")
        return _inside(target, source_root)
    if kind == "skill":
        return path.is_dir() and (path / "_coresearch").exists()
    return path.is_file() and ROLE_MARKER in path.read_text(errors="replace")


def _install_entry(src: Path, dst: Path, *, mode: str, kind: str, force: bool) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        if _is_managed_entry(dst, kind) or force:
            _remove_entry(dst)
        else:
            print(f"Refusing to replace unrelated {kind}: {dst}", file=sys.stderr)
            print("Use --force only for an intentional replacement.", file=sys.stderr)
            return False
    if mode == "symlink":
        dst.symlink_to(src.resolve(), target_is_directory=src.is_dir())
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    print(f"Installed {kind}: {dst}")
    return True


def _recognized_removed_skill(path: Path) -> bool:
    if _is_managed_entry(path, "skill"):
        return True
    if not path.is_dir() or not (path / "SKILL.md").is_file():
        return False
    text = (path / "SKILL.md").read_text(errors="replace")
    return bool(re.search(rf"(?m)^name:\s*['\"]?{re.escape(path.name)}['\"]?\s*$", text)) and (
        "compatibility shim" in text.lower()
        or any(token in text for token in (
            "Complete research planning workflow for paper ideas",
            "Verified literature survey and related-work synthesis for research topics",
            "Research figure planning and caption architecture",
            "Rewrite research paper sections with venue-aware argument",
            "Venue-calibrated simulated review and score forecast for research papers",
            "Final line-level proofreading workflow for academic manuscripts",
            "Factual verification and hallucination detection for research text",
            "Batch-download open-access PDFs",
            "Compact behavioral guidelines for research assistance",
            "Coresearch-owned PowerPoint workflow",
        ))
    )


def _prune_removed_skills(root: Path) -> None:
    for name in sorted(REMOVED_SKILLS):
        dst = root / name
        if not dst.exists() and not dst.is_symlink():
            continue
        if _recognized_removed_skill(dst):
            _remove_entry(dst)
            print(f"Pruned removed Coresearch skill: {dst}")
        else:
            print(f"WARN unrelated legacy-name skill preserved: {dst}", file=sys.stderr)


def _prune_removed_roles(root: Path, provider: str) -> None:
    suffix = ".toml" if provider == "codex" else ".md"
    expected = {f"{name}{suffix}" for name in ROLES}
    if not root.is_dir():
        return
    for dst in sorted(root.glob(f"coresearch-*{suffix}")):
        if dst.name in expected:
            continue
        if _is_managed_entry(dst, "role"):
            _remove_entry(dst)
            print(f"Pruned removed Coresearch role: {dst}")
        else:
            print(f"WARN unrelated Coresearch-named role preserved: {dst}", file=sys.stderr)


def _provider_roots(args: argparse.Namespace, provider: str) -> tuple[Path, Path, Path]:
    if args.scope == "project":
        if not args.project_dir:
            project = Path.cwd()
        else:
            project = Path(args.project_dir).expanduser().resolve()
        project.mkdir(parents=True, exist_ok=True)
        if provider == "codex":
            return project / ".agents" / "skills", project / ".codex" / "agents", project / ".codex"
        home = project / ".claude"
        return home / "skills", home / "agents", home
    if provider == "codex":
        home = codex_home(getattr(args, "codex_home", None))
        return codex_skills_root(getattr(args, "codex_skills_root", None)), home / "agents", home
    home = claude_home(getattr(args, "claude_home", None))
    return home / "skills", home / "agents", home


def _legacy_codex_skill_entries(root: Path) -> list[Path]:
    entries: list[Path] = []
    for name in sorted(set(SKILLS) | REMOVED_SKILLS):
        path = root / name
        if not path.exists() and not path.is_symlink():
            continue
        if _is_managed_entry(path, "skill") or _recognized_removed_skill(path):
            entries.append(path)
    return entries


def _migrate_legacy_codex_install(config_home: Path) -> None:
    for path in _legacy_codex_skill_entries(config_home / "skills"):
        _remove_entry(path)
        print(f"Removed legacy Coresearch Codex skill: {path}")

    config_path = config_home / "config.toml"
    if not config_path.is_file():
        return
    old = config_path.read_text()
    try:
        new = remove_codex_agents_block(old)
    except ValueError as exc:
        print(f"WARN legacy Codex registration block was not changed in {config_path}: {exc}", file=sys.stderr)
        return
    if new == old:
        return
    backup = backup_file(config_path)
    atomic_write(config_path, new)
    print(f"Removed legacy Codex role registrations: {config_path}")
    if backup:
        print(f"Backup: {backup}")


def _write_bridge(path: Path) -> None:
    old = path.read_text() if path.exists() else ""
    new = upsert_bridge_text(old)
    if old == new:
        print(f"Bridge already current: {path}")
        return
    backup = backup_file(path)
    atomic_write(path, new)
    print(f"Updated bridge: {path}")
    if backup:
        print(f"Backup: {backup}")


def cmd_install(args: argparse.Namespace) -> int:
    providers = ["codex", "claude"] if args.surface == "both" else [args.surface]
    failures = 0
    installed: list[Path] = []
    for provider in providers:
        skills_root, roles_root, config_home = _provider_roots(args, provider)
        provider_failures = 0
        _prune_removed_skills(skills_root)
        _prune_removed_roles(roles_root, provider)
        for name in SKILLS:
            if not _install_entry(
                ROOT / "skills" / name,
                skills_root / name,
                mode=args.mode,
                kind="skill",
                force=args.force,
            ):
                failures += 1
                provider_failures += 1
        suffix = ".toml" if provider == "codex" else ".md"
        role_mode = "copy" if provider == "codex" else args.mode
        for name in ROLES:
            if not _install_entry(
                ROOT / "agents" / provider / f"{name}{suffix}",
                roles_root / f"{name}{suffix}",
                mode=role_mode,
                kind="role",
                force=args.force,
            ):
                failures += 1
                provider_failures += 1
        if provider == "codex" and provider_failures == 0:
            _migrate_legacy_codex_install(config_home)
        installed.extend((skills_root, roles_root))

    project = Path(args.project_dir).expanduser().resolve() if args.project_dir else Path.cwd().resolve()
    if args.scope == "project" and not _is_git_worktree(project):
        print(
            f"WARN project target is not a Git worktree; nested repositories will not inherit this install: {project}",
            file=sys.stderr,
        )
    if args.global_bridge:
        _write_bridge(codex_home(args.codex_home) / "AGENTS.md")
    if args.project_bridge:
        _write_bridge(project / "AGENTS.md")
    if getattr(args, "full_project_agents", False):
        if args.scope != "project":
            print("--full-project-agents requires --scope project", file=sys.stderr)
            return 2
        path = project / "AGENTS.md"
        if path.exists():
            print(f"Project AGENTS.md already exists; not replacing: {path}", file=sys.stderr)
        else:
            atomic_write(path, RESEARCH_TEMPLATE.read_text())
            print(f"Installed full research project AGENTS.md: {path}")

    print()
    print("Install target(s): " + ", ".join(str(path) for path in installed))
    print(f"Mode: {args.mode}")
    if "codex" in providers:
        print("Codex role mode: copy (regular files required by current Codex)")
    print(f"Scope: {args.scope}")
    print(f"Surface: {args.surface}")
    print("Restart Codex or Claude Code to reload skill and role metadata.")
    return 3 if failures else 0


def cmd_link(args: argparse.Namespace) -> int:
    args.scope = "user"
    args.mode = "symlink"
    args.force = False
    if not hasattr(args, "surface") or not args.surface:
        args.surface = "codex"
    return cmd_install(args)


def cmd_self_install(args: argparse.Namespace) -> int:
    bin_dir = Path(args.bin_dir).expanduser().resolve() if args.bin_dir else default_bin_dir()
    dst = bin_dir / args.name
    src = (ROOT / "scripts" / "harness.py").resolve()
    bin_dir.mkdir(parents=True, exist_ok=True)

    if dst.exists() or dst.is_symlink():
        if is_repo_launcher(dst):
            print(f"Already installed: {dst} -> {dst.resolve(strict=False)}")
        elif args.force:
            backup = backup_file(dst) if dst.exists() and not dst.is_symlink() else None
            if dst.is_dir() and not dst.is_symlink():
                print(f"Refusing to replace directory: {dst}", file=sys.stderr)
                return 3
            dst.unlink()
            dst.symlink_to(src)
            print(f"Installed: {dst} -> {src}")
            if backup:
                print(f"Backup: {backup}")
        else:
            print(f"Refusing to replace existing command: {dst}", file=sys.stderr)
            print("Use --force only if you intentionally want to replace it.", file=sys.stderr)
            return 3
    else:
        dst.symlink_to(src)
        print(f"Installed: {dst} -> {src}")

    if not path_has_dir(bin_dir):
        print(f"WARN: {bin_dir} is not on PATH. Add it to your shell profile to run `{args.name}` globally.")
    else:
        print(f"OK: {bin_dir} is on PATH")
    return 0


def cmd_self_uninstall(args: argparse.Namespace) -> int:
    bin_dir = Path(args.bin_dir).expanduser().resolve() if args.bin_dir else default_bin_dir()
    dst = bin_dir / args.name
    if not dst.exists() and not dst.is_symlink():
        print(f"Not installed: {dst}")
        return 0
    if not is_repo_launcher(dst) and not args.force:
        print(f"Refusing to remove non-research-harness command: {dst}", file=sys.stderr)
        print("Use --force if you intentionally want to remove it.", file=sys.stderr)
        return 3
    if dst.is_dir() and not dst.is_symlink():
        print(f"Refusing to remove directory: {dst}", file=sys.stderr)
        return 3
    dst.unlink()
    print(f"Removed: {dst}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    if should_interactive_init(args):
        apply_interactive_init(args)

    target = Path(arg_target(args)).expanduser().resolve()
    if not target.exists():
        if args.apply:
            target.mkdir(parents=True)
        else:
            print(f"Target does not exist: {target}")
            print("Re-run with --apply to create it.")
            return 2
    path = target / "AGENTS.md"
    old = path.read_text() if path.exists() else ""
    new = project_agents_candidate(target, args.mode, args.replace)
    diff = unified_diff(old, new, str(path) + " (current)", str(path) + f" ({args.mode})")

    print(f"Target: {target}")
    print(f"Mode: {args.mode}")
    print(f"AGENTS.md: {'exists' if path.exists() else 'absent'}")
    if args.mode == "full" and path.exists() and not args.replace and diff:
        print("Refusing to replace existing AGENTS.md without --replace.")
        if diff:
            print("\n--- Diff preview ---")
            print(diff, end="")
        return 3 if args.apply else 0

    if diff:
        print("\n--- Diff preview ---")
        print(diff, end="")
    else:
        print("No AGENTS.md changes needed.")

    if not args.apply:
        print("\nDry run only. Re-run with --apply to write changes.")
        return 0

    if not diff:
        return 0
    backup = backup_file(path)
    atomic_write(path, new)
    print(f"\nWrote: {path}")
    if backup:
        print(f"Backup: {backup}")
    return 0


def cmd_global(args: argparse.Namespace) -> int:
    home = codex_home(args.codex_home)
    path = home / "AGENTS.md"
    old = path.read_text() if path.exists() else ""
    new = remove_bridge_text(old) if args.remove else upsert_bridge_text(old)
    label = "remove-bridge" if args.remove else "bridge"
    diff = unified_diff(old, new, str(path) + " (current)", str(path) + f" ({label})")
    print(f"Global AGENTS: {path}")
    print(f"Mode: {label}")
    if diff:
        print("\n--- Diff preview ---")
        print(diff, end="")
    else:
        print("No global AGENTS.md changes needed.")
    if not args.apply:
        print("\nDry run only. Re-run with --apply to write changes.")
        return 0
    home.mkdir(parents=True, exist_ok=True)
    if not diff:
        return 0
    backup = backup_file(path)
    atomic_write(path, new)
    print(f"\nWrote: {path}")
    if backup:
        print(f"Backup: {backup}")
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    if args.scope == "global":
        path = codex_home(args.codex_home) / "AGENTS.md"
    else:
        path = Path(arg_target(args)).expanduser().resolve() / "AGENTS.md"
    backup = Path(args.backup).expanduser().resolve() if args.backup else latest_backup(path)
    if backup is None or not backup.exists():
        print(f"No backup found for {path}", file=sys.stderr)
        return 2
    old = path.read_text() if path.exists() else ""
    new = backup.read_text()
    diff = unified_diff(old, new, str(path) + " (current)", str(backup) + " (restore)")
    print(f"Rollback target: {path}")
    print(f"Backup: {backup}")
    if diff:
        print("\n--- Diff preview ---")
        print(diff, end="")
    else:
        print("No changes needed; current file already equals backup.")
    if not args.apply:
        print("\nDry run only. Re-run with --apply to restore backup.")
        return 0
    if not diff:
        return 0
    pre_restore = backup_file(path)
    atomic_write(path, new)
    print(f"\nRestored: {path}")
    if pre_restore:
        print(f"Pre-restore backup: {pre_restore}")
    return 0


def skill_status(skills_dir: Path) -> list[str]:
    rows: list[str] = []
    for name in SKILLS:
        dst = skills_dir / name
        src = ROOT / "skills" / name
        expected_skill = src / "SKILL.md"
        if dst.is_symlink():
            try:
                target = dst.resolve(strict=False)
            except OSError:
                target = Path(os.readlink(dst))
            if not dst.exists():
                rows.append(f"{name}: symlink:BROKEN -> {target}")
            elif target != src:
                rows.append(f"{name}: symlink:OTHER -> {target}")
            elif not expected_skill.exists():
                rows.append(f"{name}: symlink:BROKEN missing source SKILL.md -> {target}")
            else:
                rows.append(f"{name}: symlink:OK -> {target}")
        elif dst.exists():
            if (dst / "SKILL.md").exists():
                rows.append(f"{name}: copy/dir -> {dst}")
            else:
                rows.append(f"{name}: dir:BROKEN missing SKILL.md -> {dst}")
        else:
            rows.append(f"{name}: missing")
    # Surface orphaned entries: skills present in the install target but no
    # longer owned (e.g. pptx, research-pdfs after a trim). Lets `doctor`/`status`
    # see stragglers that `prune_removed_skills` should clear. Only flag names that
    # look Coresearch-origin so a user's own unrelated skills are left alone.
    owned = set(SKILLS)
    legacy_names = {
        "coresearch", "pptx", "claim-check", "pdf-crawl", "rebuttal-plan",
        "research-guidelines", "research-pdfs",
        "paper-design", "paper-survey", "paper-figures", "paper-rewrite",
        "paper-review", "paper-proofread",
        "research-gap", "research-dialectic", "research-causal",
        "research-audit", "research-adversary", "research-rebuttal",
    }

    def looks_coreskills(name: str) -> bool:
        return name in legacy_names or name.startswith("research") or name.startswith("paper-")

    if skills_dir.is_dir():
        for entry in sorted(skills_dir.iterdir()):
            name = entry.name
            if name in owned or not looks_coreskills(name):
                continue
            if entry.is_symlink():
                try:
                    target = entry.resolve(strict=False)
                except OSError:
                    target = Path(os.readlink(entry))
                kind = "orphaned-coreskills-symlink" if str(target).startswith(str(ROOT)) else "legacy-symlink"
                rows.append(f"{name}: {kind} -> {target}")
            elif entry.is_dir() and (entry / "SKILL.md").exists():
                rows.append(f"{name}: legacy-dir (old Coresearch copy?) -> {entry}")
    return rows


def _frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return {}
    raw = text[4:].split("\n---\n", 1)[0]
    data: dict[str, object] = {}
    current: str | None = None
    for line in raw.splitlines():
        if line.startswith("  - ") and current:
            value = data.setdefault(current, [])
            if isinstance(value, list):
                value.append(line[4:])
        elif ": " in line:
            current, value = line.split(": ", 1)
            data[current] = value.strip().strip("\"'")
        elif line.endswith(":"):
            current = line[:-1]
            data[current] = []
    return data


def parse_role_definition(path: Path, provider: str) -> dict[str, object]:
    if not path.is_file():
        return {}
    text = path.read_text(errors="replace")
    if provider == "claude":
        return _frontmatter(text)
    result: dict[str, object] = {}
    for key in ("name", "description", "model", "model_reasoning_effort", "sandbox_mode"):
        match = re.search(rf'(?m)^{key}\s*=\s*"([^"\n]+)"\s*$', text)
        if match:
            result[key] = match.group(1)
        elif re.search(rf"(?m)^\s*{key}\s*=", text):
            # An unparsed value is still an override, not an omitted setting.
            result[key] = "<unparsed>"
    return result


def role_status(roles_root: Path, provider: str) -> list[str]:
    rows: list[str] = []
    suffix = ".toml" if provider == "codex" else ".md"
    by_name = {item["name"]: item for item in roles()}
    for name in ROLES:
        dst = roles_root / f"{name}{suffix}"
        src = ROOT / "agents" / provider / f"{name}{suffix}"
        pin = by_name[name]["providers"][provider]
        kind = "missing"
        if dst.is_symlink():
            target = _link_target(dst)
            if not dst.exists():
                kind = f"symlink:BROKEN -> {target}"
            elif provider == "codex":
                kind = f"symlink:UNSUPPORTED -> {target}"
            elif target != src.resolve():
                kind = f"symlink:OTHER -> {target}"
            else:
                kind = f"symlink:OK -> {target}"
        elif dst.exists():
            kind = f"copy/file -> {dst}" if dst.is_file() else f"path:BROKEN -> {dst}"
        config = parse_role_definition(dst, provider)
        effort_key = "model_reasoning_effort" if provider == "codex" else "effort"
        observed = (config.get("model"), config.get(effort_key))
        expected = (pin["model"], None if pin["effort"] == "assignment" else pin["effort"])
        if dst.exists() and observed != expected:
            kind += f" CONFIG-MISMATCH requested={pin['model']}/{pin['effort']} observed={observed[0]}/{observed[1]}"
        elif dst.exists():
            kind += f" model={expected[0]} effort={pin['effort']}"
        rows.append(f"{name}: {kind}")

    if roles_root.is_dir():
        expected_files = {f"{name}{suffix}" for name in ROLES}
        for entry in sorted(roles_root.glob(f"coresearch-*{suffix}")):
            if entry.name not in expected_files and _is_managed_entry(entry, "role"):
                rows.append(f"{entry.stem}: orphaned-coresearch-role -> {entry}")
    return rows


def global_agents_status(home: Path) -> list[str]:
    path = home / "AGENTS.md"
    rows = [f"global AGENTS: {path}"]
    if not path.exists():
        rows.append("  missing")
        return rows
    text = path.read_text(errors="replace")
    rows.append(f"  research-bridge: {'yes' if START in text and END in text else 'no'}")
    return rows


def cmd_status(args: argparse.Namespace) -> int:
    home = codex_home(args.codex_home)
    codex_skills = codex_skills_root(getattr(args, "codex_skills_root", None))
    claude = claude_home(getattr(args, "claude_home", None))
    target = Path(arg_target(args)).expanduser().resolve()
    print(f"Repo: {ROOT}")
    print(f"CODEX_HOME: {home}")
    print(f"Codex skill root: {codex_skills}")
    print(f"CLAUDE_CONFIG_DIR: {claude}")
    print(f"Project target: {target}")
    print()
    for row in global_agents_status(home):
        print(row)
    print()
    project_agents = target / "AGENTS.md"
    if project_agents.exists():
        text = project_agents.read_text(errors="replace")
        print(f"project AGENTS: {project_agents}")
        print(f"  research-bridge: {'yes' if START in text and END in text else 'no'}")
        exact_template = text.rstrip("\n") == RESEARCH_TEMPLATE.read_text().rstrip("\n")
        print(f"  full-research-template: {'yes' if exact_template else 'no'}")
    else:
        print(f"project AGENTS: missing ({project_agents})")
    print()
    print("Installed research skills (codex):")
    for row in skill_status(codex_skills):
        print("  " + row)
    print("Installed native roles (codex):")
    for row in role_status(home / "agents", "codex"):
        print("  " + row)
    print("Installed research skills (claude):")
    for row in skill_status(claude / "skills"):
        print("  " + row)
    print("Installed native roles (claude):")
    for row in role_status(claude / "agents", "claude"):
        print("  " + row)
    return 0


def read_skill_name_and_description(skill_dir: Path) -> tuple[str, str]:
    skill_file = skill_dir / "SKILL.md"
    name = skill_dir.name
    description = ""
    if not skill_file.exists():
        return name, description
    text = skill_file.read_text(errors="replace")
    if text.startswith("---\n"):
        try:
            frontmatter = text.split("---\n", 2)[1]
        except IndexError:
            frontmatter = ""
        for line in frontmatter.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("\"'")
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip().strip("\"'")
    return name, description


def inventory_roots(args: argparse.Namespace) -> list[tuple[str, Path]]:
    codex = codex_home(args.codex_home)
    skills = codex_skills_root(getattr(args, "codex_skills_root", None))
    claude = claude_home(args.claude_home)
    roots: list[tuple[str, Path]] = [
        ("codex-user", skills),
        ("codex-system", codex / "skills" / ".system"),
        ("claude-user", claude / "skills"),
    ]
    if args.include_plugins:
        roots.extend(
            [
                ("codex-cache", codex / "plugins" / "cache"),
                ("claude-marketplace", claude / "plugins" / "marketplaces"),
                ("claude-cache", claude / "plugins" / "cache"),
            ]
        )
    return roots


def iter_skill_dirs(root: Path, *, recursive: bool) -> list[Path]:
    if not root.exists():
        return []
    pattern = "**/SKILL.md" if recursive else "*/SKILL.md"
    dirs = {path.parent for path in root.glob(pattern)}
    if not recursive:
        dirs.update(path for path in root.iterdir() if path.is_dir() or path.is_symlink())
    return sorted(dirs)


def classify_skill(name: str, surface: str, manifest: dict, skill_dir: Path) -> str:
    owned = {item["name"] for item in manifest["owned"]}
    plugin_surface = surface in {"codex-cache", "claude-marketplace", "claude-cache"}
    if surface == "codex-system":
        return "system"
    if not (skill_dir / "SKILL.md").exists():
        target = str(skill_dir.resolve(strict=False)) if skill_dir.is_symlink() else ""
        if ".orchestra" in target:
            return "legacy-orchestra"
        return "non-skill"
    # Ownership oracle: the per-skill _coresearch marker is authoritative (hard
    # provenance, survives copy + symlink install); the manifest owned[] set is a
    # migration bridge; a Coresearch-family name with neither is surfaced as
    # owned-unmarked (diagnostic, not silent). classify_skill answers "is this
    # owned?" off the filesystem, so manifest is metadata, not the sole oracle.
    if (skill_dir / "_coresearch").exists():
        return "plugin-overlap" if plugin_surface else "owned"
    if name in owned:
        return "plugin-overlap" if plugin_surface else "owned"
    if name.startswith(("coresearch", "research-")):
        return "plugin-overlap" if plugin_surface else "owned-unmarked"
    return "unknown"


def cmd_inventory(args: argparse.Namespace) -> int:
    manifest = skill_manifest()
    print("# Coresearch skill inventory")
    print(f"Repo: {ROOT}")
    print(f"CODEX_HOME: {codex_home(args.codex_home)}")
    print(f"Codex skill root: {codex_skills_root(getattr(args, 'codex_skills_root', None))}")
    print(f"CLAUDE_CONFIG_DIR: {claude_home(args.claude_home)}")
    print()
    print("surface\tclass\tname\tkind\tpath\ttarget\tdescription")
    for surface, root in inventory_roots(args):
        recursive = "plugin" in surface or "marketplace" in surface or "cache" in surface
        for skill_dir in iter_skill_dirs(root, recursive=recursive):
            if ".system" in skill_dir.parts and surface != "codex-system":
                continue
            name, description = read_skill_name_and_description(skill_dir)
            kind = "symlink" if skill_dir.is_symlink() else "dir"
            target = str(skill_dir.resolve(strict=False)) if skill_dir.is_symlink() else ""
            klass = classify_skill(name, surface, manifest, skill_dir)
            print(
                "\t".join(
                    [
                        surface,
                        klass,
                        name,
                        kind,
                        str(skill_dir),
                        target,
                        description.replace("\t", " ")[:160],
                    ]
                )
            )
    print()
    print("# Coresearch native role inventory")
    print("surface\tclass\tname\tkind\tpath\trequested-model\trequested-effort")
    role_map = {item["name"]: item for item in roles()}
    for provider, home in (("codex", codex_home(args.codex_home)), ("claude", claude_home(args.claude_home))):
        suffix = ".toml" if provider == "codex" else ".md"
        root = home / "agents"
        for name in ROLES:
            path = root / f"{name}{suffix}"
            if not path.exists() and not path.is_symlink():
                continue
            kind = "symlink" if path.is_symlink() else "file"
            klass = "owned" if _is_managed_entry(path, "role") else "unrelated"
            pin = role_map[name]["providers"][provider]
            print("\t".join((f"{provider}-user", klass, name, kind, str(path), pin["model"], pin["effort"])))
    return 0


def validate_source_roles() -> list[str]:
    failures: list[str] = []
    manifest = agent_manifest()
    if manifest.get("schema_version") != 2:
        failures.append("agents/manifest.json schema_version must be 2")
    policy = manifest.get("codex_effort_policy", {})
    allowed = policy.get("allowed", [])
    if allowed != ["low", "medium", "high", "xhigh"] or policy.get("probe_effort") not in allowed:
        failures.append("agents/manifest.json invalid Codex assignment effort policy")
    if manifest.get("role_description_version") != 2:
        failures.append("agents/manifest.json role_description_version must be 2")
    manifest_roles = manifest.get("roles", [])
    if len(manifest_roles) != 8 or {item.get("name") for item in manifest_roles} != set(ROLES):
        failures.append("agents/manifest.json must contain exactly the eight Coresearch roles")
        return failures

    forbidden = {"gpt-5.6", "opus", "sonnet", "haiku", "inherit"}
    for role in manifest_roles:
        name = role["name"]
        capability = role.get("capability")
        if capability not in {"read-only", "workspace-write"}:
            failures.append(f"{name}: invalid capability {capability!r}")
        for skill in role.get("skills", []):
            if not (ROOT / "skills" / skill / "SKILL.md").is_file():
                failures.append(f"{name}: missing referenced skill {skill}")
        for provider in ("codex", "claude"):
            suffix = ".toml" if provider == "codex" else ".md"
            path = ROOT / "agents" / provider / f"{name}{suffix}"
            if not path.is_file():
                failures.append(f"{name}: missing {provider} definition {path}")
                continue
            config = parse_role_definition(path, provider)
            pin = role["providers"][provider]
            effort_key = "model_reasoning_effort" if provider == "codex" else "effort"
            if config.get("name") != name:
                failures.append(f"{path}: name mismatch {config.get('name')!r}")
            if config.get("model") != pin["model"]:
                failures.append(f"{path}: model mismatch requested={pin['model']} observed={config.get('model')}")
            expected_effort = None if provider == "codex" else pin.get("effort")
            if provider == "codex" and pin.get("effort") != "assignment":
                failures.append(f"{name}: Codex effort must be assignment-selected")
            if provider == "claude" and pin.get("effort") not in {"low", "medium", "high", "xhigh"}:
                failures.append(f"{name}: invalid fixed Claude effort")
            if config.get(effort_key) != expected_effort:
                failures.append(f"{path}: effort mismatch requested={pin['effort']} observed={config.get(effort_key)}")
            if config.get("model") in forbidden:
                failures.append(f"{path}: rolling or inherited model alias is forbidden")
            text = path.read_text(errors="replace")
            if ROLE_MARKER not in text:
                failures.append(f"{path}: Coresearch ownership marker missing")
            if provider == "codex":
                expected_sandbox = "workspace-write" if capability == "workspace-write" else "read-only"
                if config.get("sandbox_mode") != expected_sandbox:
                    failures.append(f"{path}: sandbox_mode must be {expected_sandbox}")
                if not all(skill in text for skill in role.get("skills", [])):
                    failures.append(f"{path}: relevant skill list drifted from manifest")
            else:
                tools = set(config.get("tools", []))
                skills = config.get("skills", [])
                if skills != role.get("skills", []):
                    failures.append(f"{path}: skill list drifted from manifest")
                if capability == "read-only":
                    if tools & {"Edit", "Write"} or config.get("permissionMode") != "plan":
                        failures.append(f"{path}: read-only role exposes write capability")
                elif not {"Edit", "Write"}.issubset(tools) or config.get("permissionMode") != "acceptEdits":
                    failures.append(f"{path}: writable role lacks explicit edit capability")
    return failures


def _json_values(value: object, keys: set[str]) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in keys and isinstance(child, str):
                found.append(child)
            found.extend(_json_values(child, keys))
    elif isinstance(value, list):
        for child in value:
            found.extend(_json_values(child, keys))
    return found


def _one_unique(values: list[str]) -> str | None:
    unique = list(dict.fromkeys(values))
    return unique[0] if len(unique) == 1 else None


def _probe_observed(output: str) -> tuple[str | None, str | None, str | None]:
    documents: list[object] = []
    for line in output.splitlines():
        try:
            documents.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    models: list[str] = []
    efforts: list[str] = []
    observed_roles: list[str] = []
    for document in documents:
        models.extend(_json_values(document, {"model", "model_id", "model_name"}))
        efforts.extend(_json_values(document, {"effort", "reasoning_effort", "model_reasoning_effort"}))
        observed_roles.extend(
            value
            for value in _json_values(document, {"agent_type", "agent_name", "role_name", "role"})
            if value in ROLES
        )
    return _one_unique(observed_roles), _one_unique(models), _one_unique(efforts)


def _probe_error_detail(output: str) -> str | None:
    """Return one bounded, diagnostic host message without echoing probe prompts."""
    candidates: list[str] = []
    for line in output.splitlines():
        try:
            document = json.loads(line)
        except json.JSONDecodeError:
            continue
        candidates.extend(_json_values(document, {"error", "message", "output", "result", "text"}))
    indicators = ("unavailable", "not available", "error", "failed", "denied", "invalid", "not found")
    for candidate in candidates:
        normalized = " ".join(candidate.split())
        if "CORESEARCH_ROLE_PROBE" in normalized or not any(word in normalized.lower() for word in indicators):
            continue
        return normalized[:240]
    for line in output.splitlines():
        normalized = " ".join(line.split())
        if any(word in normalized.lower() for word in indicators):
            return normalized[:240]
    return None


def _is_git_worktree(path: Path) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc.returncode == 0


def probe_role_routing(
    providers: list[str],
    homes: dict[str, Path],
    target: Path,
    role_filter: str | None = None,
) -> tuple[list[str], list[str]]:
    reports: list[str] = []
    failures: list[str] = []
    selected_roles = [role for role in roles() if role_filter is None or role["name"] == role_filter]
    for provider in providers:
        executable = shutil.which(provider)
        if not executable:
            for role in selected_roles:
                pin = role["providers"][provider]
                effort = agent_manifest()["codex_effort_policy"]["probe_effort"] if provider == "codex" else pin["effort"]
                reports.append(
                    f"routing provider={provider} role={role['name']} requested={pin['model']}/{effort} "
                    "observed_role=null observed=null/null status=static-only"
                )
            failures.append(f"{provider} named-role probes are static-only: CLI not found")
            continue
        for role in selected_roles:
            name = role["name"]
            pin = role["providers"][provider]
            model = pin["model"]
            # The probe is a bounded assignment: select its effort explicitly,
            # then compare observed metadata against that request, not a role pin.
            effort = agent_manifest()["codex_effort_policy"]["probe_effort"] if provider == "codex" else pin["effort"]
            marker = f"CORESEARCH_ROLE_PROBE {name}"
            if provider == "codex":
                command = [executable, "exec", "--ephemeral", "--json"]
                if not _is_git_worktree(target):
                    command.append("--skip-git-repo-check")
                command.append(
                    f"Spawn exactly the custom agent named {name} with reasoning_effort={effort} "
                    "and fork_turns=none. Do not override its model. The child must reply exactly "
                    f"{marker}. Return that child reply unchanged and do not perform the probe yourself."
                )
            else:
                command = [
                    executable, "--agent", name, "--print", "--output-format", "json",
                    f"Reply exactly {marker}.",
                ]
            env = os.environ.copy()
            if provider == "codex":
                env["CODEX_HOME"] = str(homes[provider])
            else:
                env["CLAUDE_CONFIG_DIR"] = str(homes[provider])
            try:
                proc = subprocess.run(
                    command,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=env,
                    cwd=target,
                    timeout=120,
                )
            except subprocess.TimeoutExpired:
                reports.append(
                    f"routing provider={provider} role={name} requested={model}/{effort} "
                    "observed_role=null observed=null/null status=mismatch"
                )
                failures.append(f"{provider} named-role probe timed out for {name} after 120 seconds")
                continue
            observed_role, observed_model, observed_effort = _probe_observed(proc.stdout)
            if proc.returncode != 0:
                status = "mismatch"
                detail = _probe_error_detail(proc.stdout)
                suffix = f": {detail}" if detail else ""
                failures.append(
                    f"{provider} named-role probe failed for {name} (exit {proc.returncode}){suffix}"
                )
            elif marker not in proc.stdout:
                status = "mismatch"
                detail = _probe_error_detail(proc.stdout)
                suffix = f": {detail}" if detail else ""
                failures.append(
                    f"{provider} named-role probe for {name} returned no completion marker{suffix}"
                )
            elif observed_role is not None and observed_role != name:
                status = "mismatch"
                failures.append(f"{provider} role mismatch requested={name} observed={observed_role}")
            elif observed_model is not None and observed_model != model:
                status = "mismatch"
                failures.append(f"{provider} model mismatch for {name} requested={model} observed={observed_model}")
            elif observed_effort is not None and observed_effort != effort:
                status = "mismatch"
                failures.append(f"{provider} effort mismatch for {name} requested={effort} observed={observed_effort}")
            elif observed_role is None or observed_model is None or observed_effort is None:
                status = "static-only"
                failures.append(
                    f"{provider} did not expose complete role/model/effort metadata for {name}"
                )
            else:
                status = "verified"
            reports.append(
                f"routing provider={provider} role={name} requested={model}/{effort} "
                f"observed_role={observed_role or 'null'} "
                f"observed={observed_model or 'null'}/{observed_effort or 'null'} status={status}"
            )
    return reports, failures


def cmd_doctor(args: argparse.Namespace) -> int:
    user_codex = codex_home(args.codex_home)
    user_codex_skills = codex_skills_root(getattr(args, "codex_skills_root", None))
    user_claude = claude_home(getattr(args, "claude_home", None))
    target_value = getattr(args, "project_dir", None) or arg_target(args)
    target = Path(target_value).expanduser().resolve()
    scope = getattr(args, "scope", "user")
    if scope == "project":
        codex_skills = target / ".agents" / "skills"
        codex_roles = target / ".codex" / "agents"
        codex_config_home = target / ".codex"
        claude_skills = target / ".claude" / "skills"
        claude_roles = target / ".claude" / "agents"
    else:
        codex_skills = user_codex_skills
        codex_roles = user_codex / "agents"
        codex_config_home = user_codex
        claude_skills = user_claude / "skills"
        claude_roles = user_claude / "agents"
    providers = ["codex", "claude"] if args.surface == "both" else [args.surface]
    skill_roots = {"codex": codex_skills, "claude": claude_skills}
    role_roots = {"codex": codex_roles, "claude": claude_roles}
    runtime_homes = {
        "codex": user_codex,
        "claude": user_claude,
    }
    failures = validate_source_roles()
    warnings: list[str] = []
    if getattr(args, "probe_role", None) and not args.probe_models:
        failures.append("--probe-role requires --probe-models")

    print("# Coresearch Harness Doctor")
    print(f"Repo: {ROOT}")
    print(f"CODEX_HOME: {user_codex}")
    print(f"Codex skill root: {codex_skills}")
    print(f"Codex role root: {codex_roles}")
    print(f"CLAUDE_CONFIG_DIR: {user_claude}")
    print(f"Claude skill root: {claude_skills}")
    print(f"Claude role root: {claude_roles}")
    print(f"Project target: {target}")
    print(f"Install scope: {scope}")
    print(f"Surface audit: {args.surface}")
    print()

    if failures:
        print(f"Static role contract: FAIL ({len(failures)} issue(s))")
    else:
        print("PASS static role manifest and all 16 native definitions")

    if os.environ.get("CLAUDE_CODE_SUBAGENT_MODEL"):
        failures.append("CLAUDE_CODE_SUBAGENT_MODEL overrides Coresearch Claude role pins")
    else:
        print("PASS Claude subagent model override is unset")

    for provider in providers:
        for row in skill_status(skill_roots[provider]):
            if "symlink:OK" in row or "copy/dir" in row:
                print(f"PASS [{provider}] skill {row}")
            else:
                failures.append(f"bad {provider} skill install: {row}")
        for row in role_status(role_roots[provider], provider):
            if ("symlink:OK" in row or "copy/file" in row) and "CONFIG-MISMATCH" not in row:
                print(f"PASS [{provider}] role {row}")
            else:
                failures.append(f"bad {provider} role install: {row}")
        if provider == "codex" and _legacy_codex_skill_entries(codex_config_home / "skills"):
            failures.append(f"legacy Coresearch Codex skills remain in unsupported root: {codex_config_home / 'skills'}")
        if provider == "codex" and (codex_config_home / "config.toml").is_file():
            config_text = (codex_config_home / "config.toml").read_text(errors="replace")
            if CODEX_AGENTS_START in config_text or CODEX_AGENTS_END in config_text:
                failures.append(f"legacy Coresearch Codex role registration block remains: {codex_config_home / 'config.toml'}")

    broken_repo_links = assert_no_broken_repo_symlinks()
    if broken_repo_links:
        failures.extend(f"broken repo symlink: {link}" for link in broken_repo_links)
    else:
        print("PASS no broken symlinks in repo")

    install_roots = _install_roots(codex_skills, codex_roles, claude_skills, claude_roles)
    scanned_install_roots = [root for root in install_roots if root.is_dir()]
    broken_install_links = broken_install_symlinks(install_roots)
    if broken_install_links:
        failures.extend(f"broken install symlink: {link}" for link in broken_install_links)
    else:
        scanned = ", ".join(str(root) for root in scanned_install_roots) or "none present"
        print(f"PASS no broken symlinks in install surfaces ({scanned})")

    global_path = user_codex / "AGENTS.md"
    if global_path.exists():
        text = global_path.read_text(errors="replace")
        print(f"INFO global research bridge: {'installed' if START in text and END in text else 'not installed'}")
    else:
        warnings.append("global AGENTS.md missing")

    project_agents = target / "AGENTS.md"
    if project_agents.exists():
        text = project_agents.read_text(errors="replace")
        exact = text.rstrip("\n") == RESEARCH_TEMPLATE.read_text().rstrip("\n")
        if START in text and END in text:
            print("PASS project AGENTS has research bridge")
        elif exact:
            print("PASS project AGENTS is the full research template")
        else:
            print("INFO project AGENTS exists without a Coresearch bridge or full template")
    else:
        print("INFO project AGENTS missing")

    command_path = shutil.which(args.command_name)
    if command_path:
        resolved = Path(command_path).resolve(strict=False)
        repo_launchers = {
            (ROOT / "harness").resolve(), (ROOT / "bin" / "harness").resolve(),
            (ROOT / "scripts" / "harness.py").resolve(),
        }
        if resolved in repo_launchers:
            print(f"PASS command `{args.command_name}` resolves to this repo: {command_path}")
        else:
            warnings.append(f"command `{args.command_name}` resolves elsewhere: {command_path}")
    else:
        warnings.append(f"command `{args.command_name}` not found on PATH")

    if args.probe_models:
        reports, probe_failures = probe_role_routing(
            providers,
            runtime_homes,
            target,
            getattr(args, "probe_role", None),
        )
        for report in reports:
            print(report)
        failures.extend(probe_failures)

    if args.validate:
        code = subprocess.call([str(ROOT / "scripts" / "validate.sh")])
        if code != 0:
            failures.append(f"validate.sh failed with exit code {code}")

    print()
    for warning in warnings:
        print("WARN " + warning)
    for failure in failures:
        print("FAIL " + failure)
    if failures:
        print(f"Doctor result: FAIL ({len(failures)} failure(s), {len(warnings)} warning(s))")
        return 1 if args.strict or args.probe_models else 0
    print(f"Doctor result: PASS ({len(warnings)} warning(s))")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    if args.pull:
        code = run(["git", "pull", "--ff-only"], cwd=ROOT)
        if code != 0:
            return code
    if not args.no_link:
        link_args = argparse.Namespace(
            codex_home=args.codex_home,
            codex_skills_root=getattr(args, "codex_skills_root", None),
            claude_home=args.claude_home,
            surface=args.surface,
            global_bridge=args.global_bridge,
            project_bridge=False,
            project_dir=None,
            scope=getattr(args, "scope", "user"),
            mode=getattr(args, "mode", "symlink"),
            force=False,
        )
        code = cmd_install(link_args)
        if code != 0:
            return code
    if not args.no_validate:
        code = subprocess.call([str(ROOT / "scripts" / "validate.sh")])
        if code != 0:
            return code
    print("Update complete.")
    return 0


def cmd_repair(args: argparse.Namespace) -> int:
    project_dir = arg_target(args) if getattr(args, "scope", "user") == "project" else None
    link_args = argparse.Namespace(
        codex_home=args.codex_home,
        codex_skills_root=getattr(args, "codex_skills_root", None),
        claude_home=getattr(args, "claude_home", None),
        surface=getattr(args, "surface", "codex"),
        global_bridge=args.global_bridge,
        project_bridge=False,
        project_dir=project_dir,
        scope=getattr(args, "scope", "user"),
        mode=getattr(args, "mode", "symlink"),
        force=False,
    )
    code = cmd_install(link_args)
    if code != 0:
        return code
    if not args.no_self_install:
        code = cmd_self_install(argparse.Namespace(bin_dir=args.bin_dir, name=args.name, force=True))
        if code != 0:
            return code
    if not args.no_validate:
        code = subprocess.call([str(ROOT / "scripts" / "validate.sh")])
        if code != 0:
            return code
    doctor_args = argparse.Namespace(
        codex_home=args.codex_home,
        codex_skills_root=getattr(args, "codex_skills_root", None),
        claude_home=getattr(args, "claude_home", None),
        surface=getattr(args, "surface", "codex"),
        scope=getattr(args, "scope", "user"),
        project_dir=project_dir,
        target=arg_target(args),
        target_arg=None,
        command_name=args.name,
        strict=True,
        validate=False,
        probe_models=False,
        probe_role=None,
    )
    return cmd_doctor(doctor_args)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="harness", description="Coresearch install/init/status harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    install = sub.add_parser("install", help="Install Coresearch skills and native roles")
    install.add_argument("--scope", choices=["user", "project"], default="user")
    install.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    install.add_argument("--mode", choices=["copy", "symlink"], default="copy")
    install.add_argument("--codex-home")
    install.add_argument("--codex-skills-root", help="Codex user skill directory (default: ~/.agents/skills)")
    install.add_argument("--claude-home")
    install.add_argument("--project-dir")
    install.add_argument("--global-bridge", action="store_true")
    install.add_argument("--project-bridge", action="store_true")
    install.add_argument("--full-project-agents", action="store_true", help="install the full project template when AGENTS.md is absent")
    install.add_argument("--force", action="store_true")
    install.set_defaults(func=cmd_install)

    link = sub.add_parser(
        "link",
        help="Link supported user-scope entries and copy Codex roles as required by the host",
    )
    link.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    link.add_argument("--codex-home")
    link.add_argument("--codex-skills-root", help="Codex user skill directory (default: ~/.agents/skills)")
    link.add_argument("--claude-home")
    link.add_argument("--global-bridge", action="store_true")
    link.add_argument("--project-bridge", action="store_true")
    link.add_argument("--project-dir")
    link.set_defaults(func=cmd_link)

    self_install = sub.add_parser("self-install", help="Install the `harness` command into a bin directory")
    self_install.add_argument("--bin-dir")
    self_install.add_argument("--name", default="harness")
    self_install.add_argument("--force", action="store_true")
    self_install.set_defaults(func=cmd_self_install)

    self_uninstall = sub.add_parser("self-uninstall", help="Remove an installed harness command symlink")
    self_uninstall.add_argument("--bin-dir")
    self_uninstall.add_argument("--name", default="harness")
    self_uninstall.add_argument("--force", action="store_true")
    self_uninstall.set_defaults(func=cmd_self_uninstall)

    init = sub.add_parser("init", help="Initialize project AGENTS.md; bare TTY init opens the wizard")
    init.add_argument("target_arg", nargs="?", help="target directory (default: .)")
    init.add_argument("--target", help="target directory (overrides positional target)")
    init.add_argument("-i", "--interactive", action="store_true", help="ask target/mode/action with a small built-in menu")
    add_mode_flags(init)
    add_apply_flag(init)
    init.add_argument("--replace", action="store_true", help="allow full mode to replace existing AGENTS.md")
    init.set_defaults(func=cmd_init)

    diff = sub.add_parser("diff", help="Alias for init/global dry-run diff")
    diff.add_argument("target_arg", nargs="?", help="target directory (default: .)")
    diff.add_argument("--target", help="target directory (overrides positional target)")
    add_mode_flags(diff)
    diff.add_argument("--replace", action="store_true")
    diff.add_argument("--global", dest="global_", action="store_true", help="show global AGENTS bridge diff instead of project diff")
    diff.add_argument("--codex-home")
    diff.set_defaults(func=lambda a: cmd_global(argparse.Namespace(codex_home=a.codex_home, remove=False, apply=False)) if a.global_ else cmd_init(a), apply=False)

    global_cmd = sub.add_parser("global", help="Preview/apply/remove the global research bridge")
    global_cmd.add_argument("--codex-home")
    global_cmd.add_argument("--remove", action="store_true")
    add_apply_flag(global_cmd)
    global_cmd.set_defaults(func=cmd_global)

    rollback = sub.add_parser("rollback", help="Preview/apply rollback from latest AGENTS.md backup")
    rollback.add_argument("--scope", choices=["project", "global"], default="project")
    rollback.add_argument("target_arg", nargs="?", help="target directory for project rollback (default: .)")
    rollback.add_argument("--target", help="target directory (overrides positional target)")
    rollback.add_argument("--codex-home")
    rollback.add_argument("--backup")
    add_apply_flag(rollback)
    rollback.set_defaults(func=cmd_rollback)

    status = sub.add_parser("status", help="Show global/project/skill/role install status")
    status.add_argument("--codex-home")
    status.add_argument("--codex-skills-root", help="Codex user skill directory (default: ~/.agents/skills)")
    status.add_argument("--claude-home")
    status.add_argument("target_arg", nargs="?", help="target directory (default: .)")
    status.add_argument("--target", help="target directory (overrides positional target)")
    status.set_defaults(func=cmd_status)

    inventory = sub.add_parser("inventory", help="Audit Codex/Claude skills and native roles")
    inventory.add_argument("--codex-home")
    inventory.add_argument("--codex-skills-root", help="Codex user skill directory (default: ~/.agents/skills)")
    inventory.add_argument("--claude-home")
    inventory.add_argument("--include-plugins", action="store_true", help="also scan Claude plugin marketplaces/cache")
    inventory.set_defaults(func=cmd_inventory)

    doctor = sub.add_parser("doctor", help="Run install and exact role-routing checks")
    doctor.add_argument("--codex-home")
    doctor.add_argument("--codex-skills-root", help="Codex user skill directory (default: ~/.agents/skills)")
    doctor.add_argument("--claude-home")
    doctor.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    doctor.add_argument("--scope", choices=["user", "project"], default="user")
    doctor.add_argument("--project-dir")
    doctor.add_argument("target_arg", nargs="?", help="target directory (default: .)")
    doctor.add_argument("--target", help="target directory (overrides positional target)")
    doctor.add_argument("--command-name", default="harness")
    doctor.add_argument("--strict", action="store_true", help="return nonzero on failures")
    doctor.add_argument("--validate", action="store_true", help="also run scripts/validate.sh")
    doctor.add_argument("--probe-models", action="store_true", help="spend network/tokens to invoke each named role and compare host-reported role/model/effort metadata with the manifest")
    doctor.add_argument("--probe-role", choices=ROLES, help="limit an explicit live probe to one named role")
    doctor.set_defaults(func=cmd_doctor)

    repair = sub.add_parser("repair", help="Relink skills, reinstall harness command, validate, and run strict doctor")
    repair.add_argument("target_arg", nargs="?", help="target directory for doctor (default: .)")
    repair.add_argument("--target", help="target directory (overrides positional target)")
    repair.add_argument("--codex-home")
    repair.add_argument("--codex-skills-root", help="Codex user skill directory (default: ~/.agents/skills)")
    repair.add_argument("--claude-home")
    repair.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    repair.add_argument("--scope", choices=["user", "project"], default="user")
    repair.add_argument("--mode", choices=["copy", "symlink"], default="symlink")
    repair.add_argument("--bin-dir")
    repair.add_argument("--name", default="harness")
    repair.add_argument("--global-bridge", action="store_true")
    repair.add_argument("--no-self-install", action="store_true")
    repair.add_argument("--no-validate", action="store_true")
    repair.set_defaults(func=cmd_repair)

    update = sub.add_parser("update", help="Optionally pull, relink user skills, and validate")
    update.add_argument("--pull", action="store_true", help="run git pull --ff-only before relinking")
    update.add_argument("--codex-home")
    update.add_argument("--codex-skills-root", help="Codex user skill directory (default: ~/.agents/skills)")
    update.add_argument("--claude-home")
    update.add_argument("--surface", choices=["codex", "claude", "both"], default="codex")
    update.add_argument("--scope", choices=["user", "project"], default="user")
    update.add_argument("--mode", choices=["copy", "symlink"], default="symlink")
    update.add_argument("--global-bridge", action="store_true")
    update.add_argument("--no-link", action="store_true")
    update.add_argument("--no-validate", action="store_true")
    update.set_defaults(func=cmd_update)
    return p


def main(argv: list[str] | None = None) -> int:
    raw_argv = sys.argv[1:] if argv is None else list(argv)
    parser = build_parser()
    args = parser.parse_args(raw_argv)
    args._raw_argv = raw_argv
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
