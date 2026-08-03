# AGENTS.md — Programs Root

> Auto-loaded every session inside `C:\Users\chase\Documents\Programs\`.
> **This is the only always-on file in this tree.** Anything that must fire in *every*
> session belongs here, once. See § Where rules live.
>
> **`.cursor/rules/*.mdc` were retired 2026-08-02.** They only loaded when a matching
> file happened to be open in a Cursor editor tab — which is not how Chase works, so
> they almost never fired. Their content now lives in `Programs/recipes/` (how to build
> something), `agent docs/rules/` (detail behind a section here), or the owning app's
> `AGENTS.md`. **Do not create new `.mdc` files.**

---

## Never put anything on Chase's screen without asking

Chase drives the cursor with a **head-mounted gyro mouse + dwell click**. A window that
appears unannounced steals focus; a display change can leave him unable to click the
button that would undo it. Treat "something appeared on screen" as **destructive**.

**Permission is per run, not per session.** "Yes, launch it" once is not standing consent.

**Ask first:** launching any GUI app (`python main_app.py`, `launch.bat`, Electron/Tkinter),
any window/dialog/overlay, **UI smoke tests** ("just checking the dialog renders" counts),
opening a browser, changing display config (`SetDisplayConfig`, `DisplaySwitch.exe`,
resolution/topology), anything topmost or full-screen.

**Fine without asking:** headless and read-only — `py_compile`, import checks, unit tests
that create no window, read-only display queries, linters, `git`, file reads, starting a
server *without* opening a browser at it.

**Instead of running it:** verify headlessly, then hand the test to Chase — what to run,
what he should see, what to report back. If a visible test is the only path, **ask first**
and say what appears, on which screen, and how it goes away.

Detail + the incident that caused this rule: `agent docs/rules/never-display-without-permission.md`

---

## Ask before you assume

**ONE** focused question — not five — then wait, when: the request has multiple plausible
readings, a significant choice affects the outcome, the scope isn't obvious, or the work is
more than a few edits and there's uncertainty. **Don't ask** when the request is clear, it's
an obvious follow-up, or the decision is trivial and reversible. Default when uncertain: **ask**.

Chase's prompts come through **speech-to-text** — expect misheard technical terms. Ask only
when acting on the literal transcription would produce something noticeably wrong.

---

## Windows PowerShell 5.x

**`&&` and `||` are invalid** and will error. Use separate tool calls with a working
directory, or `;` in one invocation. No `curl` — use `Invoke-WebRequest -UseBasicParsing`.

---

## The most violated rules

1. **Check file size before editing.** Report the line count first. Hard cap **800**;
   extract before **700**. Already over cap → refactor first, or stop and surface it.
   Never silently add to an over-cap file.
2. **App.tsx is an orchestrator, never an implementer** (target under 100 lines).
3. **Modals: `max-w-md`** (448px), `max-h-[85vh]` + `overflow-y-auto`, **never dismiss on
   backdrop click**.
4. **All API calls go through a service layer** — no inline `fetch()` in components.
5. **Over 5 `useState` or over 300 lines → extract a custom hook.**
6. **Preserve existing behavior.** Don't refactor what you weren't asked to touch.
7. **Grep before adding any new mechanism** — hook, service, IPC channel, log helper, store,
   registry. If it exists, extend it. **If you would build a second implementation of an
   existing concept, STOP and ask.** Parallel mechanisms are the #1 way this tree decays.
8. **Document the lesson** after a focused refactor or hotfix: `docs/<subsystem>_INTEGRATION.md`
   with (1) mental model, (2) symptom → root cause → fix table, (3) anti-patterns and the bug
   each one caused, (4) key-files index, (5) reusable method. Exemplar:
   `School Scrips/Macro App/docs/BROWSER_TAB_INTEGRATION.md`.

Full standards (naming, validation, Electron display scaling, build checklist, anti-patterns):
**`cursor-patterns/CODING_STANDARDS.md`** — read before writing code; it is a reference,
not something to load every turn.

---

## Dwell & head-mouse (every UI file)

1. **Every hover affordance needs a click path.** He cannot rely on precise hover.
2. **Assume every hovered element gets clicked** — the toolbar fires a real OS-level click
   on whatever the cursor rests on.

Move thresholds must be generous; never cancel an armed interaction on `pointerleave`
(wobble fires it constantly); **grep before adding another hover/dwell mechanism** — several
exist.

**No timing values here on purpose** — every threshold lives in
**`cursor-patterns/dwell-and-head-mouse.md`**. Never copy a number from anywhere else.
Exemplar constants: `electron-toolbar/modules/dwell/backend/dwell_constants.py`.
How to *build* one: `recipes/` (dwell-click, dwell-drag, hover-to-lock-drag, …).

---

## Windows hidden launchers (School Scrips)

Per-app `.bat` files **delegate** to `App Dashboard/scripts/launch-app-invoke.bat` — never
inline `npm run`. Electron hosts spawning `electron-vite`: piped stdio, `windowsHide: false`,
**not** `detached` (exemplar: `App Dashboard/electron/processManager.ts`). **Never** a visible
detached `cmd.exe` — closing that window kills the app.
Detail: `School Scrips/App Dashboard/docs/LAUNCHER.md`, `CODING_STANDARDS.md` § Windows.

---

## Git — pull at start, commit and push at end

Sibling repos under Programs, **not** a monorepo. Chase cannot rely on remembering; the agent
drives this. Skip frozen apps.

**Start** (first substantive request, "what's the state", "where did we leave off", "pull"):
scan repos, `git status --short` + `git fetch`. Clean + behind → `git pull --ff-only`.
Dirty + remote ahead, or a merge conflict → **STOP and surface it** (two-machine collision);
never auto-resolve.

**End / "put on GitHub":** commit and push **every dirty repo**, one commit per repo — not
only the active app. Sister pair: Macro App ↔ `assignment-assistant-engine`. Skip unless
asked: `.env`, credentials, `config/d2l-courses.json` backups, Calendar `server-port.json`.
**Do include** `Macro App/modules/makeup-exam/exam_history.jsonl`. No tests or builds unless
Chase asks — sync only.

Detail: `agent docs/rules/multi-repo-git-push.md`.

---

## Session scorecard — bump as you go

After each **completed deliverable** ("here's the fix", "done", a refactor phase) — not after
every tool call — run
`node scripts/append-session-scorecard.js --bump-file <delta.json>` with that chunk's greps and
files. Procedure: **`agent docs/SESSION_SCORECARD.md`**. **Never read**
`session-scorecards-log.html`; give Chase `http://127.0.0.1:8765/session-scorecards-log.html`.

Counts live on disk, so they survive a mid-session summarize. Chase can say **"log the task"**
if a chunk finished without a bump.

---

## End-of-Session Protocol

On "end of session protocol", "wrap the session", "we're done for now":

1. **Git status** — briefly list untracked/modified.
2. **Scorecard finalize** — `--finalize-file <meta.json>` (uses the bumped counts; don't
   re-guess). Report only; no fixes after this unless Chase asks.
3. **Append a session entry, newest at top.** Which log depends on what the work touched:

| Work was… | Log |
|---|---|
| Inside one app | `<app>/docs/sessions/SESSIONS.md` |
| **Instruction layer, recipes, scripts, or cross-app** | **`agent docs/sessions/SESSIONS.md`** |

If it touched both, log it where the *substance* was and name the other in the entry.

```
## YYYY-MM-DD — [Brief title]

**Files changed:** [files with line-count deltas if relevant]

**What worked:** [what got accomplished]

**Current state:** Green / Broken / Mid-refactor — [one sentence]

**File size flag:** [files now >500 lines or that grew >200, else "None"]

**Next session:** [the concrete next action]
```

4. **Leave TODO comments** in code where work stopped mid-edit.
5. **Commit and push** per § Git above — invoking end-of-session *is* permission to commit.
6. **`node scripts/check-docs.js`** — report the summary line; fix dead links and index any
   new recipe or doc this session added.
7. **Report back** in one short line: what was logged, commit/push result, check-docs summary,
   anything broken.

On "what's the state" / "where did we leave off": read the latest `SESSIONS.md` entry and
summarize in 2–3 lines.

---

## Capturing a lesson — trigger phrases

"remember: …", "capture that", "make sure you always/never …" → run the **`capture`** skill
(`.claude/skills/capture/SKILL.md`); don't just answer conversationally. "that was the third
time" / "I've told you this before" / "again" → the current rung is **proven too low**;
graduate it up at least one level and delete the copy it replaces.

Chase should never have to decide where a rule goes. Ask at most one question, and only if the
rung is genuinely ambiguous.

---

## Where rules live

Every tool lands on the same text: `AGENTS.md` holds the content, `CLAUDE.md` is a
three-line `@AGENTS.md` import of it. Cursor and Codex read `AGENTS.md` directly.

| Layer | Read when | Holds |
|---|---|---|
| **`AGENTS.md`** (this file) | **Every session, all tools** | Rules that must always fire — short |
| `<app>/AGENTS.md` | Working in that app | **Keyword table** — what Chase says → the one doc to read |
| **`recipes/`** | **Building an interaction** — drag, dwell, hover, overlay, modal, canvas, animation | How we've built it before, + exemplar file paths |
| `cursor-patterns/*.md` | Writing code | Standards — the shape all code must have |
| `agent docs/rules/*.md` | A section above isn't enough | Detail behind one always-on rule |
| `<app>/docs/*.md` | That subsystem | Why this app's code is the way it is |

**Content lives in exactly one file; everything else points at it.** A threshold that
appears twice is a threshold that will disagree with itself.

**Capture ladder** (push as high as it goes; graduating means deleting the lower copy):

| Rung | Form | Fires |
|---|---|---|
| **1** | Structurally impossible — one owner, an API that can't be misused | Always |
| **2** | Lint rule or test | Every commit |
| **3** | **A recipe in `recipes/` + its index row**, or a **keyword row in the app's `AGENTS.md`** | When Chase describes the task in his own words |
| **4** | Always-on rule (this file) | Every session — **costs tokens every session; keep it short** |
| **5** | On-demand doc nothing routes to | Only if something points at it |

Rung 3 used to be a glob-scoped `.mdc`. That trigger depended on a file being open in a
Cursor editor tab, which is not how Chase works — so it never fired. A keyword row fires
on **what he says**, which is always present. Full procedure: `.claude/skills/capture/SKILL.md`.

**Detail docs behind the sections above** — `agent docs/rules/`:

| Doc | Detail behind |
|---|---|
| `never-display-without-permission.md` | § Never put anything on Chase's screen |
| `powershell-shell-commands.md` | § Windows PowerShell 5.x |
| `multi-repo-git-push.md` | § Git |
| `frozen-apps.md` | § Apps in this tree |
| `html-delivery.md` | § HTML pages Chase can click from chat |

App-specific guidance (`<app>/AGENTS.md`) **supplements** these — app rules win for app
concerns; file-size, App.tsx, and modal rules always apply.

---

## Apps in this tree

**`APP_LOCATIONS.md`** — paths, aliases, sister apps. Read it before searching for an app name.

- `School Scrips/` — React/Vite/Tailwind math apps + **Macro App** (main Electron hub)
- `electron-toolbar/` — Python + Electron dwell-mouse overlay toolbar
- `Agent Browser/` — Electron + Chromium for agent automation (CDP **9227**)
- `Video Player/`, `recipes/` (how to build things), `cursor-patterns/` (standards),
  `agent docs/` (this layer's docs)

**Every real app has an `AGENTS.md`** with a keyword table — read that app's file when
Chase names it or when working inside it. `APP_LOCATIONS.md` maps a name to a folder.

**Frozen:** Calendar 2.0 (`School Scrips/Calendar 2.0`, since 2026-07-29) — no scans, edits, or
git sync; it is also held out of search by `/.ignore`. Unfreeze only when Chase names it.
See `FROZEN.md` in that folder and `agent docs/rules/frozen-apps.md`.

**New app:** follow `cursor-patterns/INIT_NEW_APP.md` (asks 3 questions first).

---

## HTML pages Chase can click from chat

When he asks to **link**, **open**, or **deliver** something as HTML: save a self-contained
file under `docs/`, run `node scripts/serve-programs-docs.js` (port **8765**), and give him
**only** `http://127.0.0.1:8765/<filename>.html` as a markdown link. **Never** a `C:\` path,
`file:///`, or a `.bat` opener.

**The server serves `Programs/docs/` and `Programs/agent docs/` only** — a page anywhere
else is not reachable at that URL. Exemplar: `agent docs/exam2-review-map.html`.
Contract: `agent docs/rules/html-delivery.md`.

---

## Searching this tree

`dist*/`, `build/`, `node_modules/`, `__pycache__/`, `site-packages/` hold **duplicate copies
of real source** (~178 such dirs) — reading them wastes tokens and risks editing the wrong copy.

- **`Grep` respects ignore files — prefer it.**
- **`Glob` and shell `find`/`ls` do not.** Scope `Glob` with a single app folder; never use
  shell `find`/`ls` to locate files.
- Junk in results means the owning repo's `.gitignore` has a gap — fix that, not the search.

**`/.ignore` controls tree-wide search visibility — do not delete it.** Root `.gitignore` is a
strict allowlist for the meta-backup repo, which alone would make every app tree invisible to a
Grep started at Programs root — silently **zero hits for code that exists**. `/.ignore` outranks
it and re-includes the active trees. If a tree-wide Grep finds nothing you're sure exists, read
`/.ignore` before assuming the code is missing.

**Instruction-layer health:** `node scripts/check-docs.js` reports dead links, orphans,
duplicates, and unindexed rule files. Run it when a doc is added, moved, or retired.

History only, not current guidance: `Archived markdowns/`.
