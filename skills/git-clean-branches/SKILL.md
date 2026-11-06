---
name: git-clean-branches
user-invocable: false
description: Review every local git branch and worktree, then delete the finished ones behind an archive tag. Use when asked for "un état des lieux des branches", to clean up, prune or tidy local branches or worktrees.
---

# Clean up local branches

## 1. Survey

`git fetch --prune`, then for each local branch except the default one: last commit date, upstream
state (`[gone]`, ahead/behind), commits not on the default branch (`git cherry` catches squashed or
rebased merges), first commit subjects, its MR (`glab mr list --source-branch <b> --all`, or
`gh pr list --head <b> --state all`) and the worktree holding it, dirty or not. A ref listed as
`heads/<x>` is ambiguous with a tag `<x>`: address it as `refs/heads/<x>`.

Report in four groups, with a recommendation:

- ✅ **Already in the default branch**: merged MR, 0 unmerged patches, or the same patch on it.
- 🟢 **In progress**: open MR.
- 🟡 **Unmerged work**: closed MR or none, real commits.
- 🔴 **Leftovers**: WIP, POC, backups, branches included in another one.

Delete nothing at this step.

## 2. Clean up, once the user has said what to keep

1. Tag each branch to delete: `git tag archive/<branch> refs/heads/<branch>`, local only, never pushed.
2. Remove the worktrees of those branches and the review worktrees of merged MRs with
   `git worktree remove` without `--force` (it refuses a dirty one: report it), then delete the
   empty parent folders. Keep the review worktree of an open MR.
3. `git branch -D` the branches, in one command.
4. Never touch remote branches or existing tags. Report what remains and how to restore a branch:
   `git branch <b> archive/<b>`.

Then offer `/claude-archive-sessions` for the sessions of those branches.
