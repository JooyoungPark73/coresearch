#!/usr/bin/env python3
"""Install one skill or create an optional research brief. Python 3.10+, stdlib."""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "coresearch"


def payload(root: Path) -> dict[str, Path]:
    """Enumerate portable skill files, excluding interpreter caches."""
    result = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if "__pycache__" in relative.parts or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError(f"skill payload contains a symlink: {path}")
        if path.is_file():
            result[relative.as_posix()] = path
    if "SKILL.md" not in result:
        raise ValueError(f"missing SKILL.md: {root}")
    return result


def identical(left: dict[str, Path], right: dict[str, Path]) -> bool:
    return left.keys() == right.keys() and all(
        hashlib.sha256(left[key].read_bytes()).digest()
        == hashlib.sha256(right[key].read_bytes()).digest()
        for key in left
    )


def install(directory: Path, *, link: bool = False, dry_run: bool = False) -> str:
    source = SKILL.resolve()
    destination = directory.expanduser().resolve() / "coresearch"
    if destination == source or source in destination.parents:
        raise ValueError("installation destination is inside the source skill")
    files = payload(source)
    if destination.is_symlink():
        if link and destination.resolve() == source:
            return f"Already linked: {destination}"
        raise FileExistsError(f"preserving existing link: {destination}")
    if destination.exists():
        if not link and destination.is_dir() and identical(files, payload(destination)):
            return f"Already installed: {destination}"
        raise FileExistsError(f"preserving existing destination: {destination}")
    if dry_run:
        return f"Would {'link' if link else 'copy'} {source} -> {destination}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if link:
        destination.symlink_to(source, target_is_directory=True)
    else:
        # Exclusive creation prevents concurrent installers from sharing a target.
        destination.mkdir()
        try:
            # Publish discovery metadata last, after references and scripts exist.
            for relative in sorted(files, key=lambda name: name == "SKILL.md"):
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(files[relative], target)
        except BaseException:
            shutil.rmtree(destination)
            raise
    return f"{'Linked' if link else 'Installed'}: {destination}"


def initialize(project: Path, *, question: str | None = None, dry_run: bool = False) -> str:
    research = project.expanduser().resolve() / "research"
    if research.is_symlink():
        raise ValueError(f"preserving linked research directory: {research}")
    destination = research / "brief.md"
    if destination.exists() or destination.is_symlink():
        return f"Preserved existing brief: {destination}"
    text = (SKILL / "templates" / "brief.md").read_text(encoding="utf-8")
    text = text.replace("{{question}}", question or "State the research question.")
    if dry_run:
        return f"Would create: {destination}\n\n{text}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as stream:
        stream.write(text)
    return f"Created: {destination}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    install_parser = commands.add_parser("install", help="install the skill without changing prompts")
    install_parser.add_argument("--to", type=Path, required=True, help="host's skills directory")
    install_parser.add_argument("--link", action="store_true", help="link to this checkout instead of copying")
    install_parser.add_argument("--dry-run", action="store_true")
    init_parser = commands.add_parser("init", help="create research/brief.md; optional for any workflow")
    init_parser.add_argument("project", type=Path, nargs="?", default=Path.cwd())
    init_parser.add_argument("--question")
    init_parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "install":
            result = install(args.to, link=args.link, dry_run=args.dry_run)
        else:
            result = initialize(args.project, question=args.question, dry_run=args.dry_run)
        print(result)
        return 0
    except (OSError, ValueError) as error:
        print(f"coresearch: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
