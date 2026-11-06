---
name: claude-handoff
description: Generate a concise, self-contained prompt to spin up a fresh agent session
disable-model-invocation: true
argument-hint: <task description>
---

Write a handoff prompt. The new session will start with no context, so it must be self-contained — but keep it as short as the task allows.

If I give no task, assume I want to continue the current work from a clean state.

Your context is filling up, you should not work on this yourself.

Include only what the next agent needs:
- **Goal** — what to accomplish.
- **Context** — key decisions, constraints, and gotchas found this session.
- **Where** — repo/worktree, branch, and the files that matter (with paths).
- **State** — what's done vs. what's left.

Skip the conversational back-and-forth and anything trivially rediscoverable.

Output it as a single fenced code block so I can copy it directly.


Task: Handoff $ARGUMENTS
