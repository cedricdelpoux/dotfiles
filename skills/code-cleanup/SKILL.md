---
name: code-cleanup
description: Keep it simple. Write self-explanatory code with short explicit names and almost no comments, and trim the comments and homogenise the names (functions, booleans, events, callbacks, props, slots) a branch or a working tree adds. Use every time you develop a feature, fix a bug or refactor, before writing code and again on the final diff, and when asked to clean up, lighten, simplify or homogenise code ("kis", "nettoie", "allège les commentaires", "enlève les commentaires inutiles", "homogénéise les emits / les noms", "trop d'incohérences").
---

# KIS: keep it simple

A name says what, a comment says why, and almost nothing needs a why. Reach for a better name first;
a comment survives only when it explains an invariant, a trap or a workaround that no name can carry.
One line, and expect it to be challenged.

This skill is framework-agnostic. The project's own rules win over its defaults: before deciding
anything, load the project's conventions skills when they exist (`code-comments`, `*-conventions`,
a `code-cleanup-<project>` companion such as `code-cleanup-shipfix`) and read its CLAUDE.md.

## Names

- **Short and plain**: the shortest name a newcomer understands without reading the code around it.
  Two or three words, four at most for a constant, never a sentence (`findPopupSpot`, not
  `findLeastCoveredTopLeftPxNearClick`). Everyday English a non-native speaker knows, no rare synonym
  or jargon (`check`, not `probe`; `step`, not `stride`).
- **What it holds or does**: a variable is named for its content, with its unit or shape when it matters
  (`timeoutMs`, `linesById`, not `data`, `result`, `t`); a function starts with a verb. A magic value
  becomes a named constant, a complex condition a named boolean, and a block that needs a comment to say
  what it does becomes a named function.
- **Name the subject**, so the name still makes sense out of its file (`MAX_ROUND_TRIP_METERS`, not
  `MAX_LEG_METERS`), and name what the thing is, not a vague category (`selectedRoute`, not
  `selectedRouteDetails`).
- **Prefixes, by priority**: the first that gives a short name wins; the next ones only when none does.
  - Booleans: 1. `is` / `are` (plural); 2. `has` (something is present); 3. `can` / `should` (ability, policy).
  - Lookups: 1. `get` (always returns) / `find` (may return `undefined`); 2. `resolve` (computed from several sources). Never a bare `…Of` (`groupOfPath` → `getGroupPath`).
  - Conversions: 1. `to` (same data, another shape); 2. `build` / `create` (a new object); 3. `with…` for a modified copy `to` cannot describe.
  - Side effects: an imperative verb (`remove`, `apply`, `commit`, `open`); `set…` writes a state; `on…` handles an event.
  - Never a subject-verb phrase (`queryHoldsGroups` → `hasQueryGroups`). Mirror an existing sibling's shape.
- **State is named for what it represents, not for how it is stored**: a variable holding the id of
  the selected row is `activeItem`, not `activeId`; what is dragged is `draggedItem`. The storage word
  (`id`, `path`, `index`) belongs to the utilities that manipulate it.
- **Reuse the module's existing vocabulary** before inventing one: if the module calls a chip a `tag`,
  a new component is `…Tag`, not `…Chip`. Grep the base branch for the word before naming, use the same
  word for the same thing everywhere, and once the user picks a word, rename every related name to it.
- **Rename only what is wrong or missing** (a name that lies, a boolean without a prefix, a stale
  reference, a name that fails the rules above); a name that merely reads differently stays. Group the proposals by vocabulary and submit
  them as one mapping, not one by one.
- **Events and callbacks**: an imperative verb in the present tense, the object only when the verb
  alone is ambiguous (`activate`, `expand`, `remove`, `removeGroup`, `toggleOperator`, `addFilter`,
  `dragStart`). Never the past tense (`groupMoved`). One spelling from the declaration to the listener:
  the one the repo already uses most (grep before choosing), with the framework's own convention for
  handler props (`onRemove` for a React callback prop, `@remove` for a Vue listener).
- **Props**: camelCase, named for what they are, not for how one parent uses them; booleans as above.
  Defaults live in code (the framework's defaults mechanism), not in a comment.
- **Slots, render props, children**: the main one is named for what it renders (`filter`), a secondary
  one for where it goes (`after`). The name stays the same through every forwarding level.
- **Constants and CSS variables** carry their meaning (`$resizable-handle-thickness`), never a comment
  beside a vague name.
- When no short plain name fits, the code probably does too many things: split it rather than lengthen
  the name.

## Comments

Default to none, and always in English. Never on: a CSS rule (the selector is the explanation), a prop,
an event, a slot or a type field (the name is), a test (its title is), a function whose name and
signature say it, a diff or a ticket's intent, another repo's implementation, UI mechanics or layout (a
hover delay, a color, an event that does not fire during a drag), a list of what a function returns
when the code lists it, a "see X" pointer the names already lead to.

A comment is allowed only for a why a reader would get wrong without it: a constraint from a library,
browser or API, a deliberate choice that looks like a mistake, a complex algorithm in one or two lines.

Decide each comment in scope, in this order, and stop at the first that applies:

| The comment… | Do |
|---|---|
| restates the code, the signature, the selector or the name | delete |
| says what a name could say | rename, extract a named function or boolean, then delete |
| narrates history ("was", "used to", "now", "without this", a bug story) | keep only the durable why, in the present tense, or delete |
| explains non-obvious logic | keep, cut to the one or two lines that carry the why |

What a surviving comment may say (present tense, no ticket tags, no change narration) follows the
project's `code-comments` skill when one exists.

## Workflow

When writing code, apply the names and comments rules as you go. Before handing over, or when asked
to clean up:

1. **Scope**: by default what the change adds. `git diff <base>...HEAD -U0` (`main` or `master`) plus
   `git diff -U0` for uncommitted work, new files in full. Moved code counts: moving a block is the
   moment to trim it.
2. **Review every comment** added or modified with the table, and **every name** added or renamed with
   the names rules. On an explicit cleanup request, list the decisions as a table (line → decision →
   why) before editing, so the user can object to one of them. Otherwise fix what fails before handing
   over rather than asking the user to review it.
3. **Apply** without changing behaviour. A rename covers every occurrence: declarations, listeners,
   templates, tests, comments (`grep` the old name afterwards).
4. **Verify**: the project's formatter, linter and type-checker on the touched files, then the tests of
   the touched module, with the commands its CLAUDE.md or check skill gives.

## Pitfalls

- A kept comment must stay true for the code as it is now: after a rename or a reorder, re-read the
  comments around it.
- Comments contain prose: a naive search for ` as ` matches the English word.
- Some linters reject a `//` comment directly above a function or export: drop it, or write it as
  `/** */` if it survives the table.
