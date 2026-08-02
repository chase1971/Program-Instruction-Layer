# AGENTS.md — Programs Root

> Auto-loaded every session inside `C:\Users\chase\Documents\Programs\`.
> **This is the only always-on file in this tree.** No `.cursor/rules/*.mdc` is
> `alwaysApply: true` — they are glob- or description-triggered detail. Anything that
> must fire in *every* session belongs here, once. See § Where rules live.

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

Detail + the incident that caused this rule: `.cursor/rules/05-never-display-without-permission.mdc`

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
Glob rule: `.cursor/rules/25-dwell-accessibility.mdc`. Exemplar constants:
`electron-toolbar/modules/dwell/backend/dwell_constants.py`.

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

Detail: `.cursor/rules/40-multi-repo-git-push.mdc`.

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
3. **Append to** the app's `docs/sessions/SESSIONS.md`, newest at top:

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
6. **`node scripts/check-docs.js`** — report the summary line; fix dead links and index any new
   `.mdc` this session added.
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

| Layer | Loads when | May contain |
|---|---|---|
| **`AGENTS.md`** (this file) | **Every session, all tools** | Rules that must always fire — short |
| `<app>/CLAUDE.md` | Working in that app | Index of that app's rules + docs |
| `.cursor/rules/*.mdc` | **Cursor only**, when a matching file is open (or by description) | Behavior + pointer. **No numbers** |
| `cursor-patterns/*.md`, `docs/*_INTEGRATION.md` | Read on demand | The content — values, tables, reasons |

**Content lives in exactly one file; everything else points at it.** A threshold that appears
twice is a threshold that will disagree with itself. Claude Code never auto-loads `.mdc`, so a
lesson written only there fires for one tool.

**Capture ladder** (push as high as it goes; graduating means deleting the lower copy):
structurally impossible → lint/test → glob `.mdc` → this file → on-demand doc. Full procedure:
`.claude/skills/capture/SKILL.md`.

**Root rules in `.cursor/rules/`** — all glob- or description-triggered, none always-on:

| Rule | Fires when |
|---|---|
| `00-programs-entrypoint.mdc` | superseded by this file; kept as a reading order |
| `05-never-display-without-permission.mdc` | detail behind § Never put anything on Chase's screen |
| `10-file-size-before-edit.mdc` | editing `.ts` / `.tsx` / `.py` / `.css` |
| `20-modal-pattern.mdc` | editing modal files |
| `25-dwell-accessibility.mdc` | `.tsx` / `.jsx` / overlay files |
| `30-powershell-shell-commands.mdc` | `.ps1` / `.bat` / `.cmd` |
| `40-multi-repo-git-push.mdc` | detail behind § Git |
| `45-frozen-apps.mdc` | anything under `School Scrips/Calendar 2.0/` |
| `50-electron-toolbar-launcher-panel.mdc` | `electron-toolbar/**` |
| `html-infographic-delivery.mdc` | `docs/**/*.html` |

Per-app rules: `[app]/.cursor/rules/`, indexed in that app's `CLAUDE.md`.

App-specific guidance (`[app]/CLAUDE.md`, `guidelines/Guidelines.md`) **supplements** these —
app rules win for app concerns; file-size, App.tsx, and modal rules always apply.

---

## Apps in this tree

**`APP_LOCATIONS.md`** — paths, aliases, sister apps. Read it before searching for an app name.

- `School Scrips/` — React/Vite/Tailwind math apps + **Macro App** (main Electron hub)
- `electron-toolbar/` — Python + Electron dwell-mouse overlay toolbar
- `Agent Browser/` — Electron + Chromium for agent automation (CDP **9227**)
- `Video Player/`, `cursor-patterns/` (pattern library), `agent docs/` (this layer's docs)

**Frozen:** Calendar 2.0 (`School Scrips/Calendar 2.0`, since 2026-07-29) — no scans, edits, or
git sync; it is also held out of search by `/.ignore`. Unfreeze only when Chase names it.
See `FROZEN.md` in that folder and `.cursor/rules/45-frozen-apps.mdc`.

**New app:** follow `cursor-patterns/INIT_NEW_APP.md` (asks 3 questions first).

---

## HTML pages Chase can click from chat

When he asks to **link**, **open**, or **deliver** something as HTML: save a self-contained
file under `docs/`, run `node scripts/serve-programs-docs.js` (port **8765**), and give him
**only** `http://127.0.0.1:8765/<filename>.html` as a markdown link. **Never** a `C:\` path,
`file:///`, or a `.bat` opener. Exemplar: `docs/exam2-review-map.html`. Contract:
`.cursor/rules/html-infographic-delivery.mdc`.

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
duplicates, and unindexed `.mdc`. Run it when a doc is added, moved, or retired.

History only, not current guidance: `Archived markdowns/`.
