# Coresearch development

Python 3.10+ and the standard library only. The installable, self-contained
payload is `skills/coresearch/`; this file is not installed into research projects.

`scripts/coresearch.py` installs that payload or creates `research/brief.md`.
It never edits host configuration, global prompts, `AGENTS.md`, or `CLAUDE.md`.

When writing or updating skills, consult [OpenAI's skill-authoring guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

Local validation: `python3 -B -m unittest discover -s tests -v`.
Tests use disposable directories and mocked network boundaries, with no account
or production access. These checks and corrections need no intermediate approval.
