# CLAUDE.md — Programs Root

> This file is auto-loaded by Claude Code for every session inside
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

- `00-programs-entrypoint.mdc` — always on; index of `cursor-patterns/` + hard rules
- `10-file-size-before-edit.mdc` — when editing `.ts` / `.tsx` / `.py` / `.css`
- `20-modal-pattern.mdc` — when editing modal files

Per-app rules live in `[app]/.cursor/rules/` (e.g. Macro App modal + browser rules).
Full index: `cursor-patterns/README.md` § How AI Sessions Find This.

---

## Ask Before You Assume

Chase prefers you to ask ONE focused clarifying question before starting work
when ANY of these are true:
- The request has multiple plausible interpretations
- A significant choice affects the outcome (which library, pattern, location)
- The scope isn't obvious (just this file? the whole feature?)
- An app-specific decision is needed and the answer isn't in CLAUDE.md / Guidelines.md
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
   exists, extend it. If you add a new one anyway, your response MUST name
   what you chose not to reuse and why. Parallel mechanisms are the #1 way
   this tree accumulates duplicate solutions and inconsistent patterns —
   they look like "I solved the task" but read later as "nothing fits
   together anymore."

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
- `[app]/CLAUDE.md` (if it exists, read it after this file)
- `[app]/guidelines/Guidelines.md`
- `[app]/.cursorrules`

These **supplement** the master standards, not replace them. App-specific
rules win for app-specific concerns (color schemes, math libraries, etc.),
but the file-size, App.tsx, and modal rules always apply.

---

## End-of-Session Protocol

When the user says "end of session protocol", "wrap the session", "end the
session", "we're done for now", or similar, do these in order:

1. **Verify state.** If renderer code was changed in this session, run
 `npm test` in `renderer/` and report results before logging. If Python
 automation code was changed, run `pytest modules/d2l/tests` (and any
 other relevant test dirs) and report results. If a build/dev server is
 involved, ask: "Want me to run the build to confirm it still works before
 logging?" (Run only if user says yes.)
2. **Check git status** (if a git repo). Briefly list what's untracked or modified.
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
5. **Commit and push to GitHub** in the active app's git repo. Invoking
   end-of-session counts as explicit permission to commit. Follow the git safety
   protocol in user rules: parallel `git status` / `git diff` / `git log`,
   draft a message from the session work, stage relevant files only (never
   `.env`, credentials, or local backups unless the user asked), commit, then
   `git push` if a remote exists. Skip commit if there are no changes; ask once
   if the repo would need a large first commit of previously untracked files.
6. **Report back** to the user: one short line summarizing what was logged,
   commit hash/message (or "nothing to commit"), push result, and anything
   broken/unfinished.

When the user starts a new session and says "what's the state" or "read the
session log" or "where did we leave off", read the latest entry in
`docs/sessions/SESSIONS.md` and summarize it back in 2-3 lines.

---

## Starting a New App

If the user asks to "initialize a new app", "bootstrap a new [variant] app",
"set up a new project", or similar, follow the recipe in:
`C:\Users\chase\Documents\Programs\cursor-patterns\INIT_NEW_APP.md`

That recipe asks 3 clarifying questions first (name, variant, location), then
scaffolds the folder structure, CLAUDE.md, Guidelines.md, configs, and session
log. Three variants supported: `educational-math`, `functional-tool`,
`electron-overlay`.

## Apps in This Tree

- `School Scrips/` — React/Vite/Tailwind educational math apps (Calendar 2.0,
  factoring-app, logic-app, Matrix app, Probability App, transformations-app,
  makeup-exam-standalone, D2L-Assignment-Platform, etc.)
- `electron-toolbar/` — Python + Electron overlay toolbar with dwell-mouse
  accessibility. Has its own architecture docs at
  `electron-toolbar/ARCHITECTURE_PATTERNS.md` and
  `electron-toolbar/OVERLAY_MODULE_PATTERN.md`.
- `cursor-patterns/` — Reusable pattern library (this is where
  CODING_STANDARDS.md lives). Electron apps: **`cursor-patterns/electron-per-monitor-display-scaling.md`**
  (exemplar: Calendar 2.0).

---

## Archived Docs

Old session notes, completed refactoring reports, and stale duplicates have
been moved to `C:\Users\chase\Documents\Programs\Archived markdowns\`. Don't
look there for current guidance — it's history only.
