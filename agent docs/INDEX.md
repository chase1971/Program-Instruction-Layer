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
| seating chart save · wipe on reopen · sticky room · attendance save · persistence | [School Scrips/Seating-Chart/docs/PERSISTENCE_INTEGRATION.md](../School%20Scrips/Seating-Chart/docs/PERSISTENCE_INTEGRATION.md) |
| student portal · student codes · exit tickets · custom quiz · "can students cheat" · Student Progress tab · how an app becomes a grade | [School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md](../School%20Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md) |
| **deploy the portal** · push to netlify · **update supabase** · push migration · ship student site · netlify credits · deploy budget | pipeline doc § Shipping changes to production · `student-portal/docs/netlify-deploy-counter.json` |
| building an interaction — drag, dwell, hover, overlay, modal, canvas, animation, toggle, scroll | [recipes/INDEX.md](./recipes/INDEX.md) |
| manim · "animate solving an equation" · math explainer video · the animation guide we wrote | [Manim Trial/ANIMATION_STYLE_RECIPE.md](../Manim%20Trial/ANIMATION_STYLE_RECIPE.md) — scenes and render command in that folder's [README](../Manim%20Trial/README.md) |
| how code should look — standards, naming, refactor, React, file headers, "initialize a new app" | [recipes/INDEX.md](./recipes/INDEX.md) |
| school HTML — exam maps, review maps, teaching documents · factoring pdf · factoring handout · "pull School documents" | [School Scrips/School documents/](../School%20Scrips/School%20documents/) |
| "do this from my phone" · send a task from my phone · my PC isn't showing up · desktop missing from the machine list | [PHONE_AGENT_ACCESS.md](./PHONE_AGENT_ACCESS.md) |

## The detail behind an always-on rule

> The rule itself is already loaded from `AGENTS.md`. Read these only when the summary there
> isn't enough.

| You might say | Read this |
|---|---|
| "don't put that on my screen" · launch the app · GUI or UI test · change the display config | [rules/never-display-without-permission.md](./rules/never-display-without-permission.md) |
| PowerShell error · `&&` didn't work · curl failed · shell syntax | [rules/powershell-shell-commands.md](./rules/powershell-shell-commands.md) |
| "put it on GitHub" · pull · "pull Macro App" · "same as my PC" · push at end · which repos get committed · laptop vs PC files · don't tell me what's uncommitted · commit everything · GitHub backup | [rules/multi-repo-git-push.md](./rules/multi-repo-git-push.md) |
| `.gitignore` didn't work · ignored file still shows in git · runtime file keeps changing | [rules/multi-repo-git-push.md](./rules/multi-repo-git-push.md) |
| frozen apps · Calendar 2.0 · "don't touch that one" | [rules/frozen-apps.md](./rules/frozen-apps.md) |
| "make me an HTML page I can click" · deliver a link · the docs server on 8765 | [rules/html-delivery.md](./rules/html-delivery.md) |
| **"read my comments on \<page\>"** · he annotated an HTML report · comment boxes on a page | [rules/html-delivery.md](./rules/html-delivery.md) § Reader comments — read `<page>.comments.json` beside the page |

## Session flow

| You might say | Read this |
|---|---|
| "end of session protocol" · wrap the session · we're done for now | [END_OF_SESSION.md](./END_OF_SESSION.md) — the seven steps and the log template |
| "perform a momentum handoff" · switch to a fresh task · give the next agent our momentum | [MOMENTUM_HANDOFF.md](./MOMENTUM_HANDOFF.md) — write [momentum-handoffs/latest.md](./momentum-handoffs/latest.md), then copy-ready prompt |
| **"read the latest momentum handoff"** · continue from the handoff · pick up the momentum handoff · what did the last agent leave off (fresh task) | **[momentum-handoffs/latest.md](./momentum-handoffs/latest.md)** first, then [MOMENTUM_HANDOFF.md](./MOMENTUM_HANDOFF.md) § Read — check the Written date; stale → ask Chase |
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
| "show me the diagram" · the pages on 8765 · how is the index laid out | [pages.html](./pages.html) → `instructional-layer-htmls/` (maintained) · `scratch/` (one-off, goes stale) |
| what is this index · how do I add a row | this file — § Keeping this honest, below |

## Scripts

| You might say | Read this |
|---|---|
| check the docs are healthy · dead links · orphans · is anything unrouted · is anything out of date · does that folder still exist | [scripts/check-docs.js](../scripts/check-docs.js) |
| serve a page Chase can click · start the docs server · port 8765 | [scripts/serve-programs-docs.js](../scripts/serve-programs-docs.js) |
| bump task tracking or finalize session metrics | [scripts/append-session-scorecard.js](../scripts/append-session-scorecard.js) |
| archive old plans · sweep `docs/plans/` | [scripts/archive-stale-plans.js](../scripts/archive-stale-plans.js) |
| prune old momentum handoffs · dated handoff cleanup | [scripts/prune-momentum-handoffs.js](../scripts/prune-momentum-handoffs.js) — auto after each perform; keeps 3 days |
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
- every absolute path in [APP_LOCATIONS.md](../APP_LOCATIONS.md) still exists on disk
- dead links, duplicate docs, orphans, unindexed `.mdc`, restated constants, stale plans

It will suggest keyword rows for anything unrouted. It never writes them — the words have to
be Chase's.
