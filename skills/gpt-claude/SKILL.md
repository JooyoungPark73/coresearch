---
name: gpt-claude
description: Consult local Claude Code via claude -p for a second opinion, code review, or scoped delegated task.
---

# Consult Claude Code

Use the installed `claude` CLI and existing login. Give Claude the goal, relevant
context, constraints, and desired output; it does not inherit this conversation.
Run from the intended working directory.

For an optional connectivity check, run with a 60-second process timeout:

```bash
claude -p --tools '' --no-session-persistence 'Reply with exactly CLAUDE_OK.'
```

Use the execution host's process deadline, or prefix with `timeout 60s` where that
utility is installed. A tool's output-yield interval is not a process timeout.

For substantive requests, replace the prompt or supply it through stdin using a
prompt file or quoted heredoc. Keep credentials out of supplied context.

- `--tools ''` disables built-in tools for consultation on supplied text. For
  repository inspection, use `--tools 'Read,Glob,Grep'`. Enable editing or command
  execution only when the delegated task needs it; coordinate shared-file edits.
  `--tools` does not restrict MCP tools; add `--disallowedTools 'mcp__*'` when
  the consultation should exclude configured MCP tools as well.
- `--no-session-persistence` suits one-shot requests. For follow-ups, omit it,
  capture `session_id` with `--output-format json`, and use
  `claude -p --resume SESSION_ID 'Follow-up prompt'` with the intended tool flags.
- Choose a timeout appropriate to the task and inspect the exit status. If
  sandbox restrictions block access, use the execution host's approval path;
  Claude's permission-bypass flag does not resolve host sandbox restrictions.
  If the CLI or login is unavailable, report the blocker instead of repeatedly
  retrying or changing authentication settings.
- Check Claude's findings against the code or evidence before adopting them.
  The calling agent owns integration and final verification.

Flag reference: [Claude Code CLI documentation](https://code.claude.com/docs/en/cli-reference).
