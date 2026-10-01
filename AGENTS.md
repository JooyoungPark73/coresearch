# Coresearch development

Python 3.10+ and the standard library only. The installable, self-contained
payload is `skills/coresearch/`; this file is not installed into research projects.

`scripts/coresearch.py` installs that payload or creates `research/brief.md`.
It never edits host configuration, global prompts, `AGENTS.md`, or `CLAUDE.md`.

Local validation: `python3 -B -m unittest discover -s tests -v`.
Tests use disposable directories and mocked network boundaries, with no account
or production access. These checks and corrections need no intermediate approval.
