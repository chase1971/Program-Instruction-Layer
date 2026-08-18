# INDEX — where everything lives

> **This file holds pointers only. Never rules.**
> Rules that fire every session live in root [AGENTS.md](../AGENTS.md). This file is for
> things you **look up** when the topic comes up.

**How to use it:** match what Chase said — or what you're about to do — to a row, then read
**that one file**. Do this **before grepping the tree**. If nothing matches, grep — then add
the row before the session ends.

**This index names owners; owners name their contents.** It points at
[recipes/INDEX.md](./recipes/INDEX.md), never at an individual recipe. So adding a recipe
never touches this file.

---

## Start here — the four branches

| You might say | Read this |
|---|---|
| any app by name · "where does X live" · which folder is that in | [APP_LOCATIONS.md](../APP_LOCATIONS.md) |
| anything inside one app — its subsystems, its docs, "Pearson", "the gradebook", "the launcher panel" | that app's `AGENTS.md` — find the folder via [APP_LOCATIONS.md](../APP_LOCATIONS.md) |
| building an interaction — drag, dwell, hover, overlay, modal, canvas, animation, toggle, scroll | [recipes/INDEX.md](./recipes/INDEX.md) |
| how code should look — standards, naming, refactor, React, file headers, "initialize a new app" | [recipes/INDEX.md](./recipes/INDEX.md) |
| school HTML — exam maps, review maps, teaching documents | [School Scrips/School documents/](../School%20Scrips/School%20documents/) |

## The detail behind an always-on rule

> The rule itself is already loaded from `AGENTS.md`. Read these only when the summary there
> isn't enough.

| You might say | Read this |
|---|---|
| "don't put that on my screen" · launch the app · GUI or UI test · change the display config | [rules/never-display-without-permission.md](./rules/never-display-without-permission.md) |
| PowerShell error · `&&` didn't work · curl failed · shell syntax | [rules/powershell-shell-commands.md](./rules/powershell-shell-commands.md) |
| "put it on GitHub" · pull at start · push at end · which repos get committed | [rules/multi-repo-git-push.md](./rules/multi-repo-git-push.md) |
| `.gitignore` didn't work · ignored file still shows in git · runtime file keeps changing | [rules/multi-repo-git-push.md](./rules/multi-repo-git-push.md) |
| frozen apps · Calendar 2.0 · "don't touch that one" | [rules/frozen-apps.md](./rules/frozen-apps.md) |
| "make me an HTML page I can click" · deliver a link · the docs server on 8765 | [rules/html-delivery.md](./rules/html-delivery.md) |

## Session flow

| You might say | Read this |
|---|---|
| "end of session protocol" · wrap the session · we're done for now | [END_OF_SESSION.md](./END_OF_SESSION.md) — the seven steps and the log template |
| "where did we leave off" · what's the state · what did we do last time | [sessions/SESSIONS.md](./sessions/SESSIONS.md) — or that app's `docs/sessions/SESSIONS.md` |
| "log the task" · bump session tracking · task navigation path | [SESSION_TRACKING.md](./SESSION_TRACKING.md) |
| finalize session metrics · grep/file counts · hook enforcement | [SESSION_METRICS.md](./SESSION_METRICS.md) |
| Macro App browser residency plan · browser memory plan | [scratch/MACRO_APP_BROWSER_RESIDENCY_PHASE_PLAN.md](./scratch/MACRO_APP_BROWSER_RESIDENCY_PHASE_PLAN.md) · [review](./scratch/MACRO_APP_BROWSER_RESIDENCY_PHASE_PLAN_REVIEW.md) |
| "remember: …" · "capture that" · "that's the third time" · "always/never do X" | [.claude/skills/capture/SKILL.md](../.claude/skills/capture/SKILL.md) |
| where should this rule go · which rung · is this always-on or on-demand | [AGENTS.md](../AGENTS.md) § Capture ladder |

## The instruction layer itself

| You might say | Read this |
|---|---|
| "run the audit" · clean up the docs · is the instruction layer healthy | [INSTRUCTION_LAYER_AUDIT.md](./INSTRUCTION_LAYER_AUDIT.md) |
| "run the conformance pass on \<app\>" · bring one app up to standard | [APP_CONFORMANCE_PASS.md](./APP_CONFORMANCE_PASS.md) |
| how does this whole setup work · which tool reads which file · why did `.mdc` go away | [HOW_TO_INTERACT_WITH_AI.md](../HOW_TO_INTERACT_WITH_AI.md) |
| explain my setup to another developer | [AGENT_SETUP_FOR_PEER_REVIEW.md](./AGENT_SETUP_FOR_PEER_REVIEW.md) |
| "show me the diagram" · the pages on 8765 · how is the index laid out | [index.html](./index.html) → `instructional-layer-htmls/` (maintained) · `scratch/` (one-off, goes stale) |
| what is this index · how do I add a row | this file — § Keeping this honest, below |

## Scripts

| You might say | Read this |
|---|---|
| check the docs are healthy · dead links · orphans · is anything unrouted | [scripts/check-docs.js](../scripts/check-docs.js) |
| serve a page Chase can click · start the docs server · port 8765 | [scripts/serve-programs-docs.js](../scripts/serve-programs-docs.js) |
| bump task tracking or finalize session metrics | [scripts/append-session-scorecard.js](../scripts/append-session-scorecard.js) |
| archive old plans · sweep `docs/plans/` | [scripts/archive-stale-plans.js](../scripts/archive-stale-plans.js) |
| turn a markdown file into a PDF | [scripts/md-to-pdf.js](../scripts/md-to-pdf.js) |

---

## Keeping this honest

**Adding a row.** A lookup failed, or you had to grep to find something. Add a row using
**the words Chase actually said**, not the doc's title. `accessibility-patterns.md` would
title itself "accessibility patterns"; what he says is *"the button is too small to click."*
The second one is the row that works.

**Never add a row for:**
- an individual recipe or standard — those belong to [recipes/INDEX.md](./recipes/INDEX.md).
  Adding them here creates a second copy that will drift.
- a rule that fires every session — that belongs in [AGENTS.md](../AGENTS.md). Routing it
  makes it optional.

**Row budget: 120, warning at 100.** This file gets read in full on every lookup, so its length
is a cost paid every time. Past ~120 rows it costs more than the grep it exists to replace.
When it warns, the fix is to branch a section into its own index — not to trim rows.

**What the robot checks** (`node scripts/check-docs.js`):
- every doc is reachable from this file within two hops
- this file still names every branch — if it stops, the check hard-fails
- no doc has grown past the line cap

It will suggest keyword rows for anything unrouted. It never writes them — the words have to
be Chase's.
