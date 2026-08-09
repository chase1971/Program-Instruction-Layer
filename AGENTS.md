# AGENTS.md — Programs Root

> Auto-loaded every session inside `C:\Users\chase\Documents\Programs\`.
> **This is the only always-on file in this tree.** Anything that must fire in *every*
> session belongs here, once.
>
> **Never create `.cursor/rules/*.mdc` files** — retired 2026-08-02. Why: `HOW_TO_INTERACT_WITH_AI.md`.

---

## First move — find the doc

**Where anything lives: `agent docs/INDEX.md`.** Match what Chase said, or what you're about
to do, to a row; read that one file. Do this **before grepping the tree**. If nothing matches,
grep — then add the row before the session ends.

That file holds **pointers only**. Rules that must fire every session are *here*, not there.

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

## Don't hand Chase a keyboard-driven interface

Never hand Chase an interactive terminal prompt, arrow-key menu, or type-to-filter box as the
next step. Use non-interactive flags, write a small script, or ask before proposing a flow
that requires typing.

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

1. **Check file size before editing.** Hard cap **800**; extract before **700**. Already over
   cap → refactor first, or stop and surface it. Never silently add to an over-cap file.
2. **The entry file orchestrates; it never implements.** `App.tsx`, `main.py`, `index.js` —
   wire things together and delegate. Under ~100 lines.
3. **Preserve existing behavior.** Don't refactor what you weren't asked to touch.
4. **Grep before adding any new mechanism** — hook, service, IPC channel, log helper, store,
   registry. If it exists, extend it. **If you would build a second implementation of an
   existing concept, STOP and ask.** Parallel mechanisms are the #1 way this tree decays.
5. **Modals never dismiss on backdrop click.** Dwell fires clicks constantly, so a modal that
   closes when he clicks outside it is unusable.

**React apps also:** API calls go through a service layer — never an inline `fetch()` in a
component; over 5 `useState` or 300 lines → extract a hook.

Full standards, and where each of these is spelled out: **`agent docs/recipes/INDEX.md`** —
a reference, not something to load every turn.

**These five always apply, even where an app's own `AGENTS.md` says otherwise.** App-specific
guidance supplements this file for app concerns; it never overrides file size, the orchestrator
rule, or the modal rule.

---

## Windows launchers — never a visible console

**Applies to every launcher, everywhere** — App Dashboard, the electron-toolbar **Launcher Panel**,
and any standalone `.bat`. Launchers are how Chase opens everything, so this one is not optional.

**Never spawn a visible detached `cmd.exe`.** Closing that window kills the app, and it steals
focus when it appears. Per-app `.bat` files **delegate** to
`App Dashboard/scripts/launch-app-invoke.bat` — never inline `npm run`. Electron hosts spawning
`electron-vite`: piped stdio, `windowsHide: false`, **not** `detached`.

Exemplar: `App Dashboard/electron/processManager.ts`.
Detail: `School Scrips/App Dashboard/docs/LAUNCHER.md` ·
Toolbar tiles: `electron-toolbar/docs/LAUNCHER_PANEL.md`.

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

**Mid-session:** do not commit or push unless Chase explicitly asks; wait for "put on GitHub"
or end-of-session.

Detail: `agent docs/rules/multi-repo-git-push.md`.

---

## Session scorecard — bump as you go

After each **completed deliverable** ("here's the fix", "done", a refactor phase) — not after
every tool call — run
`node scripts/append-session-scorecard.js --bump-file <delta.json>` with that chunk's greps and
files. Procedure: **`agent docs/SESSION_SCORECARD.md`**. **Never read**
`session-scorecards-log.html`; give Chase `http://127.0.0.1:8765/session-scorecards-log.html`.

**Every bump must include `navigationPath`** — ordered steps showing where you looked first,
what helped (✓), what was a dead end (✗), and nested `steps` for Task sub-agents. Chase uses
this tree on the HTML card to see whether INDEX.md / app `AGENTS.md` are creating short routes.

Counts live on disk, so they survive a mid-session summarize. Chase can say **"log the task"**
if a chunk finished without a bump.

---

## End-of-Session Protocol

On **"end of session protocol"**, "wrap the session", "we're done for now" → follow
**`agent docs/END_OF_SESSION.md`**. Invoking it *is* permission to commit and push, and
means **Chase is done** — wrap up silently; **never ask him to run, launch, or verify anything**.

On "what's the state" / "where did we leave off" → read the latest `SESSIONS.md` entry and
summarize in 2–3 lines. That is not this protocol.

---

## Capturing a lesson — trigger phrases

"remember: …", "capture that", or "make sure you always/never …" → run the **`capture`**
skill (`.claude/skills/capture/SKILL.md`); don't just answer conversationally.

Capture means: grep for existing coverage, place it on the capture ladder, write or update
the owning doc, and make it reachable from the right index (`agent docs/recipes/INDEX.md`,
`<app>/AGENTS.md`, or root `AGENTS.md`). Ask one question only if placement is genuinely
ambiguous.

---

## Capture ladder

**Content lives in exactly one file; everything else points at it.** A threshold, duration,
or rule that appears twice will eventually disagree with itself.

| Rung | Form | Fires |
|---|---|---|
| **1** | Structurally impossible — one owner, an API that can't be misused | Always |
| **2** | Lint rule or test | Every commit |
| **3** | Recipe + `agent docs/recipes/INDEX.md`, or keyword row in `<app>/AGENTS.md` | When Chase describes the task |
| **4** | Always-on rule in this file | Every session — keep short |
| **5** | On-demand doc | Only when something points at it |

Graduating means deleting the lower copy. Full capture procedure:
`.claude/skills/capture/SKILL.md`.

---

## Frozen — do not touch

**Calendar 2.0** (`School Scrips/Calendar 2.0`) — frozen since 2026-07-29. No scans, edits, or
git sync; also held out of search by `/.ignore`. Unfreeze only when Chase names it.
Detail: `agent docs/rules/frozen-apps.md`.

---

## HTML pages Chase can click from chat

When he asks to **link**, **open**, or **deliver** something as HTML, give him **only** a
markdown link to `http://127.0.0.1:8765/<name>.html`. **Never** a `C:\` path, a `file:///`
URL, or a `.bat` opener — he cannot use those.

Where the file goes, which folders are served, and how: `agent docs/rules/html-delivery.md`.

---

## Searching this tree

**`Glob` and shell `find`/`ls` do not respect ignore files.** They return thousands of
`node_modules` hits and can time out. Scope `Glob` to one app folder; use `Grep` for content —
it respects them automatically and needs no special handling.

**`/.ignore` is what makes tree-wide search work — do not delete it.** Root `.gitignore` is a
strict allowlist, so without `/.ignore` a Grep from Programs root returns **zero hits for code
that exists**. Nothing found ≠ nothing there: read `/.ignore` before concluding code is missing.

History only, not current guidance: `Archived markdowns/`.
