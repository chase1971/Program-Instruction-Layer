# AGENTS.md — Programs Root

> This file is auto-loaded by Codex for every session inside
> `C:\Users\chase\Documents\Programs\` and its subdirectories. It is the
> entry point for all coding guidance.

---

## Read This First

Before writing or modifying ANY code, read:

**`C:\Users\chase\Documents\Programs\cursor-patterns\CODING_STANDARDS.md`**

That file is the canonical source of truth for:
- File size limits (max 800 lines — the most violated rule)
- App.tsx as orchestrator (never an implementer)
- Module/file organization (where things go)
- React patterns (custom hooks, service layer, state extraction)
- Modal sizing (`max-w-md`, never `max-w-3xl`)
- Electron shell: per-monitor **Display** scaling (required for every Electron app)
- **Windows hidden launchers** (`.bat` + Node spawn — no visible cmd windows)
- Naming conventions
- Input validation, API response shape
- Final build checklist (9/10 quality)
- Anti-patterns

---

## Cursor rules (this workspace)

Cursor loads **`.cursor/rules/*.mdc`** automatically:

| Rule | Scope |
|------|--------|
| `00-programs-entrypoint.mdc` | always on — index of `cursor-patterns/` + hard rules |
| `05-never-display-without-permission.mdc` | always on — no GUI launches without Chase's permission |
| `10-file-size-before-edit.mdc` | globs — when editing `.ts` / `.tsx` / `.py` / `.css` |
| `20-modal-pattern.mdc` | globs — when editing modal files |
| `25-dwell-accessibility.mdc` | globs — any `.tsx` / `.jsx` / overlay file (head-mouse + dwell) |
| `30-powershell-shell-commands.mdc` | always on — no `&&` / `||` in PowerShell |
| `40-multi-repo-git-push.mdc` | always on — pull at session start, commit/push at end |
| `45-frozen-apps.mdc` | always on — skip Calendar 2.0 unless Chase explicitly asks |
| `html-infographic-delivery.mdc` | glob — `docs/**/*.html`; read when Chase asks for linked HTML |
| `50-electron-toolbar-launcher-panel.mdc` | globs — `electron-toolbar/**` only |

Per-app rules live in `[app]/.cursor/rules/` (e.g. Macro App modal + browser rules).
Full index: `cursor-patterns/README.md` § How AI Sessions Find This.

---

## Ask Before You Assume

Chase prefers you to ask ONE focused clarifying question before starting work
when ANY of these are true:
- The request has multiple plausible interpretations
- A significant choice affects the outcome (which library, pattern, location)
- The scope isn't obvious (just this file? the whole feature?)
- An app-specific decision is needed and the answer isn't in AGENTS.md / Guidelines.md
- The work will take more than a few file edits and there's any uncertainty

**Don't ask** if the request is clear, it's an obvious follow-up in an active
task chain, or the decision is trivial and easily reversible.

**Format:** ONE focused question. Not a barrage of 5. Then wait.

Default posture when uncertain: **ask**. A 5-second clarification beats
redoing work or unwinding unwanted changes.

## The 8 Most Violated Rules (Quick Reminder)

If you only remember these 8 things, you'll already be ahead:

1. **CHECK FILE SIZE BEFORE EDITING.** Read the file, report the line count,
 estimate addition impact, and STOP if you'd cross 700/800 lines. If the
 file is already over the cap, you MUST refactor it first before making
 the requested change — this is not optional. If the refactor is larger
 than the session allows, stop and surface it to the user rather than
 silently adding to an over-cap file.

2. **App.tsx is an orchestrator, never an implementer.** Target under 100 lines.
   Extract feature components, don't inline them.

3. **Modals use `max-w-md` (448px).** Never `max-w-3xl`, `max-w-4xl`, or
   `max-w-6xl`. Always `max-h-[85vh]` with `overflow-y-auto` on content.

4. **All API calls go through a service layer.** Never inline `fetch()` in
   components.

5. **State over 5 useState calls or component over 300 lines → extract to a
   custom hook.**

6. **Preserve existing behavior.** Don't refactor things you weren't asked to
   touch.

7. **Grep before adding any new mechanism.** Before creating a new hook,
   utility, service, IPC channel, log helper, state store, partition,
   registry, or any system another part of the code might already do: search
   the codebase (and sister apps) for what it would replace. If something
   exists, extend it. **If you would create a second implementation of an
   existing concept, STOP and surface it for a decision** — do not proceed
   on your own judgment. Parallel mechanisms are the #1 way this tree
   accumulates duplicate solutions and inconsistent patterns — they look
   like "I solved the task" but read later as "nothing fits together
   anymore." Naming what you chose not to reuse after the fact is not a
   substitute for asking before you build it.

8. **Document the lesson when you finish a focused refactor or hotfix.**
   When a session retires multiple band-aids, fixes a class of bugs, or
   restructures a subsystem, write a `docs/<subsystem>_INTEGRATION.md`
   next to the affected code. Exemplar:
   `School Scrips/Macro App/docs/BROWSER_TAB_INTEGRATION.md`. Must
   include: (1) one-page mental model, (2) symptom → root-cause → fix
   table, (3) anti-patterns ("what burned us") with the bug each one
   previously caused, (4) key-files index, (5) a reusable method for the
   next instance of the same problem class. This is what stops the next
   AI from removing "looks redundant" code and re-deriving the same bug.
   The reasons code exists must live in the repo, not in your head.

---

## Dwell & head-mouse (applies to every UI file)

Chase drives every app with a **gyro head-mounted mouse + dwell click**. Two rules
subsume most of the rest:

1. **Every hover affordance must also have a click path.** He cannot rely on
   precise hover.
2. **Assume every hovered element gets clicked.** The toolbar fires a real
   OS-level click on whatever the cursor rests on.

Also: move thresholds must be generous (tight ones never latch), never cancel an
armed interaction on `pointerleave` (wobble fires it constantly), never dismiss a
modal on backdrop click, and **grep before adding another hover/dwell
mechanism** — several already exist.

**No timing values appear here on purpose.** Every threshold and duration lives in
the source-of-truth file below, so the numbers cannot drift between copies. Open
it before writing hover/dwell/drag code; never copy a number from anywhere else.

- Source of truth: **`cursor-patterns/dwell-and-head-mouse.md`**
- Rule: `.cursor/rules/25-dwell-accessibility.mdc`
- Exemplar rule to copy the shape of: `School Scrips/Math App Studio/.cursor/rules/studio-dwell-mechanics.mdc`
- Exemplar constants file (named values + *reasons*): `electron-toolbar/modules/dwell/backend/dwell_constants.py`

---

## Windows Hidden Launchers (School Scrips)

When adding or fixing **`.bat` launchers**, **Toolbar hotkeys**, or **Electron spawn** code on Windows:

1. Read **`cursor-patterns/CODING_STANDARDS.md`** → section **Windows: Hidden Launchers**.
2. Per-app `.bat` files **delegate** to `App Dashboard/scripts/launch-app-invoke.bat` — never inline `npm run` in the app folder.
3. Electron hosts spawning **`electron-vite`**: piped stdio + `windowsHide: false` + **not** `detached` (exemplar: `App Dashboard/electron/processManager.ts`).
4. **Never** use visible detached `cmd.exe` — closing that window kills the app.

Detail: `School Scrips/App Dashboard/docs/LAUNCHER.md`.

---

## Project-Specific Guidelines

Individual apps may have their own additional guidance:
- `[app]/AGENTS.md` (if it exists, read it after this file)
- `[app]/guidelines/Guidelines.md`
- `[app]/.cursorrules`

These **supplement** the master standards, not replace them. App-specific
rules win for app-specific concerns (color schemes, math libraries, etc.),
but the file-size, App.tsx, and modal rules always apply.

---

## Session scorecard — bump as you go (cheap, every chat)

After each **completed deliverable** (“here’s the fix”, “done”, “linked”, a refactor **phase**
finished — not after every grep/shell call), append to the running tally:

1. Read **`docs/SESSION_SCORECARD.md`** § bump (procedure only — **never** read
   `session-scorecards-log.html`).
2. Run `node scripts/append-session-scorecard.js --bump-file <delta.json>` with **this chunk’s**
   greps, files read/edited, docs/rules opened.

Counts live on disk in `docs/.session-scorecard-running.json` — **safe if the chat summarizes
mid-session.** Chase can say **“log the task”** if you finished a chunk but didn’t bump.

**Refactors:** bump after each **logical chunk** (e.g. one module extracted, one hook split) —
not every tool use. Many bumps OK; each is ~50–150 tokens.

At **wrap/end-of-session**, **finalize** (below) — do not re-guess totals from memory if bumps exist.

---

## End-of-Session Protocol

When the user says "end of session protocol", "wrap the session", "end the
session", "we're done for now", or similar, do these in order:

1. **Check git status** (if a git repo). Briefly list what's untracked or modified.
2. **Session scorecard (report only)** — read `docs/SESSION_SCORECARD.md` (not the HTML log).
   **Finalize** the running tally: `node scripts/append-session-scorecard.js --finalize-file <meta.json>`
   (uses counts logged after each task via `--bump-file`). If no bumps happened, finalize still works from best-effort recall.
   **Never read** `docs/session-scorecards-log.html`. Give Chase
   `http://127.0.0.1:8765/session-scorecards-log.html`. No fixes after scorecard unless Chase asks.
   Pairing: step 6 below is the **robot** pass; this step is the **AI** pass.
3. **Append an entry** to the app's `docs/sessions/SESSIONS.md`. Use this format,
   with the newest entry at the top:

```
## YYYY-MM-DD — [Brief title]

**Files changed:** [files with line-count deltas if relevant]

**What worked:** [what got accomplished]

**Current state:** Green / Broken / Mid-refactor — [one sentence]

**File size flag:** [any files now >500 lines or that grew >200 lines, else "None"]

**Next session:** [the concrete next action]
```

4. **Leave TODO comments in the code** if work stopped mid-edit. A comment in
   the actual file beats a description in SESSIONS.md — the next agent will
   see it when they open the file.
5. **Commit and push to GitHub** — follow the multi-repo scan in
   `.cursor/rules/40-multi-repo-git-push.mdc` (all dirty repos under Programs,
   not just the active app). Invoking end-of-session counts as explicit
   permission to commit. Follow the git safety protocol in user rules: parallel
   `git status` / `git diff` / `git log`, draft a message from the session work,
   stage relevant files only (never `.env`, credentials, or local backups unless
   the user asked), commit, then `git push` if a remote exists. Skip commit if
   there are no changes; ask once if the repo would need a large first commit of
   previously untracked files. **Do not run npm test, pytest, builds, or other
   smoke/verification steps** unless Chase explicitly asks.
6. **Instruction-layer health check (robot / rung 2)** — from Programs root run
   `node scripts/check-docs.js` (advisory; use `--strict` only if Chase asks).
   Report the summary line (dead links, duplicates, unindexed rules, orphans).
   If this session added, moved, or retired docs/rules, fix dead links and index
   any new `.mdc` in the relevant `CLAUDE.md` when straightforward.
7. **Report back** to the user: one short line summarizing what was logged,
   commit hash/message (or "nothing to commit"), push result, check-docs summary,
   scorecard spike (if any), and anything broken/unfinished.

When the user starts a new session and says "what's the state" or "read the
session log" or "where did we leave off", read the latest entry in
`docs/sessions/SESSIONS.md` and summarize it back in 2-3 lines.

---

## Starting a New App

If the user asks to "initialize a new app", "bootstrap a new [variant] app",
"set up a new project", or similar, follow the recipe in:
`C:\Users\chase\Documents\Programs\cursor-patterns\INIT_NEW_APP.md`

That recipe asks 3 clarifying questions first (name, variant, location), then
scaffolds the folder structure, AGENTS.md, Guidelines.md, configs, and session
log. Three variants supported: `educational-math`, `functional-tool`,
`electron-overlay`.

## Apps in This Tree

**Full index (paths, aliases, legacy folders, sister apps):**
**`APP_LOCATIONS.md`** — read this before searching folders for an app name.

- `School Scrips/` — React/Vite/Tailwind educational math apps (Calendar 2.0,
  factoring-app, logic-app, Matrix app, Probability App, transformations-app,
  makeup-exam-standalone, D2L-Assignment-Platform, etc.)
- `electron-toolbar/` — Python + Electron overlay toolbar with dwell-mouse
  accessibility. Has its own architecture docs at
  `electron-toolbar/ARCHITECTURE_PATTERNS.md` and
  `electron-toolbar/OVERLAY_MODULE_PATTERN.md`.
- `Agent Browser/` — Personal Electron shell with embedded Chromium for agent
  web automation. CDP port **9227** when running. Launch: toolbar Launcher Panel
  (🤖) or **Shift+F20**. Docs: `Agent Browser/CLAUDE.md`.
- `Video Player/` — Electron + embedded VLC; toolbar Launcher Panel + Shift+F19.
- `cursor-patterns/` — Reusable pattern library (this is where
  CODING_STANDARDS.md lives). Electron apps: **`cursor-patterns/electron-per-monitor-display-scaling.md`**
  (exemplar: Calendar 2.0).

---

## Frozen apps

Chase may **detach** from an app — no routine scans, edits, or git sync until he explicitly unfreezes it.

| App | Folder | Since |
|-----|--------|-------|
| Calendar 2.0 | `School Scrips/Calendar 2.0` | 2026-07-29 |

See `.cursor/rules/45-frozen-apps.mdc` and each app's `FROZEN.md`.

---

## HTML pages Chase can click from chat

**Trigger:** Chase asks to **link**, **open**, or **deliver** something as HTML — infographic,
report, map, table, comparison, or "something I can click from here."

**Contract:** `.cursor/rules/html-infographic-delivery.mdc` (glob + on request — **not** always-on)

1. Save self-contained HTML under **`docs/`**
2. Run **`node scripts/serve-programs-docs.js`** (port **8765**) if not already up
3. Give Chase **only** **`http://127.0.0.1:8765/<filename>.html`** in chat — markdown link

Or say **"link it like exam2-review-map"** — agent copies exemplar delivery without a permanent rule slot.

**Never** `C:\...` paths, `file:///`, folder paths as the only link, or `.bat` openers.
Exemplars: `docs/context-engineering-infographic.html`, `docs/exam2-review-map.html`.

---

## Capturing a lesson — trigger phrases

When Chase says any of these, run the **`capture`** skill
(`.claude/skills/capture/SKILL.md`) — do not just answer conversationally:

| He says | What it means |
|---------|---------------|
| "remember: …" / "capture that" | Put this on the ladder now |
| "make sure you always / never …" | Same — a durable rule, not a task instruction |
| "that was the third time" / "I've told you this before" / "again" | The current rung is **proven too low** — graduate it up at least one level |

He should never have to write these files or decide where they go. He says one
sentence; the skill greps for existing coverage, picks the rung, writes it in the
five-ingredient shape, deletes the copy it replaces, and updates the index.
**Ask at most one question, and only if the rung is genuinely ambiguous.**

---

## Searching this tree (token discipline)

Build outputs, caches, and vendored deps (`dist*/`, `build/`, `node_modules/`,
`__pycache__/`, `.pytest_cache/`, `site-packages/`) hold **duplicate copies of real
source** — ~178 such directories live under Programs. Reading them costs tokens and
risks editing the wrong copy.

- **`Grep` respects ignore files and skips them — prefer it for finding code.**
- **`Glob` and Bash `find`/`ls` do NOT** (verified: they ignore `.gitignore` *and*
  `.ignore`). Over half their raw results can be junk. Scope `Glob` with `path:` to a
  single app folder; never use Bash `find`/`ls` to locate files.
- If a search returns installer or cache copies, the owning repo's `.gitignore` has a
  **gap** — fix the `.gitignore`, don't work around it in the search.

### `/.ignore` controls tree-wide search visibility — do not delete it

Root `.gitignore` is a **strict allowlist** (`/*`) scoped to the meta-backup repo. On
its own that makes *every* app tree invisible to `Grep` started at Programs root — a
tree-wide search silently returns **zero hits for code that definitely exists**, which
is exactly how rule 7 above gets violated and duplicate mechanisms get built.

**`/.ignore` fixes this** (ripgrep reads it, and it outranks `.gitignore`): it
re-includes the active app trees and holds `Deprecated apps/` and the frozen
`School Scrips/Calendar 2.0/` out of search. Per-repo `.gitignore` files still filter
build/cache junk inside each app.

If a tree-wide `Grep` returns nothing for something you're sure exists, **read
`/.ignore` first** — assume the filter is wrong before you assume the code is missing.

## Keeping the instruction layer healthy

```
node scripts/check-docs.js
```

Reports the four ways this system decays: **dead links**, **orphans** (docs
nothing references — functionally deleted), **duplicates** (two sources of truth),
and **unindexed `.mdc` rules** (invisible to Claude Code, which does not auto-load
them). Advisory by default; `--strict` exits non-zero on any finding.

Run it when a doc is added, moved, or retired — and at end of session.

---

## Capture ladder (when a bug is fixed or a correction repeats)

Push the lesson as far up this ladder as it will go. **Graduating to a higher level requires deleting the lower-level copy** — prose that lint or a contract already enforces is noise.

1. **Make it structurally impossible** (code shape, single owner, API that cannot be misused)
2. **Lint rule or test** (exemplar: `School Scrips/Macro App/renderer/.eslintrc.cjs`, pre-commit `check-file-size.js`)
3. **Glob-scoped `.mdc` contract** (exemplar: `School Scrips/Math App Studio/.cursor/rules/`)
4. **Always-on rule** (budget ~200 lines total across all always-on rules)
5. **On-demand doc** (`docs/*_INTEGRATION.md`, `cursor-patterns/` — read when relevant, not every turn)

`CODING_STANDARDS.md` is a reference index, not something loaded every turn. Prefer lint + glob contracts for rules that must fire reliably.

### One content home, many pointers (rungs 3–5)

**Cursor and Claude Code do not load the same files.** Cursor auto-loads
`.cursor/rules/*.mdc`; **Claude Code never does** — it always loads `AGENTS.md`
and the nearest `CLAUDE.md`. A rule written into only one of those formats fires
for only one tool, and the same lesson written into *both* drifts apart.

So content lives in **exactly one file**, and everything else points at it:

| File | Role | May contain |
|------|------|-------------|
| `cursor-patterns/<topic>.md` (or `docs/*_INTEGRATION.md`) | **The content.** Single source of truth | Everything — values, tables, reasons |
| `.cursor/rules/*.mdc` | Cursor's glob trigger | Behavior statements + the pointer. **No numbers** |
| `AGENTS.md` / `CLAUDE.md` | Claude Code's entry point | The pointer, and at most a 2-line summary. **No numbers** |

**Never put a threshold, duration, or size in two files.** A number that appears
twice is a number that will disagree with itself. Put it in the content file and
point at it — the pointer is what makes both tools land on the same text.

Exemplar of this shape: `cursor-patterns/dwell-and-head-mouse.md` (content) ←
`.cursor/rules/25-dwell-accessibility.mdc` (glob trigger) + § *Dwell & head-mouse*
above (entry point).

---

## Archived Docs

Old session notes, completed refactoring reports, and stale duplicates have
been moved to `C:\Users\chase\Documents\Programs\Archived markdowns\`. Don't
look there for current guidance — it's history only.
