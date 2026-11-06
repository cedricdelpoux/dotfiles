---
name: archive-sessions
description: Archive the Claude Code sessions of the VS Code sidebar whose work is merged and has nothing pending. Use when asked to "archive les sessions", tidy the session list, or after cleaning up branches.
---

# Archive finished sessions

`python3 -I ~/.claude/skills/archive-sessions/sessions.py list [repo]` prints each session the
extension still shows: its branches (the last one is where it ended), title and last reply.

Classify each session, then show the table (session, branch, MR state, verdict) and wait for an ok:

- **Archive**: its last feature branch has a merged MR (`glab mr list --source-branch <b> --all`, or
  `gh pr list --head <b> --state all` on GitHub), or it ran on the default branch and its last reply
  shows the task done (answered question, finished tooling change, reviewed MR now merged).
- **Keep**: its branch has an open MR or unpushed commits, its last reply asks a question or lists a
  next step, or it is the current session.
- **Ask**: anything else (closed MR, deleted branch with no MR, unclear last reply).

On the ok, `sessions.py archive <id>…`. VS Code rewrites its state on exit, so while it runs the
script forks a waiter that writes the archived list once VS Code quits: tell the user to quit VS Code
(⌘Q, not just the window) and reopen it. The script backs up `state.vscdb` first and logs to
`~/.claude/archive-sessions.log`. Unarchiving stays possible from the extension's session list.
