# Multi-repo Git — `Pull` means full machine sync

> **Rung 5 — on demand.** The always-on summary is root `AGENTS.md` § Git; this
> file is the detail behind it. Read it when that section is not enough.
> **What it covers:** When Chase says **`pull`**, sync **every** git repo under Programs in
> **both directions** — bring down what the other machine pushed, push up what this machine
> has — not just the app open in Cursor. Summary lives in AGENTS.md § Git.
>
> *Was `.cursor/rules/40-multi-repo-git-push.mdc` until 2026-08-02. Moved because `.cursor/rules/*.mdc`
> only load when a matching file is open in a Cursor editor tab — which is not how Chase works.
> AGENTS.md links this file by path instead, so every tool can reach it.*

---

Chase uses **sibling repos** under `C:\Users\chase\Documents\Programs\` (not a monorepo). **Pull before you start, push before you stop** — agent drives this; Chase cannot rely on remembering.

**Why GitHub exists for Chase:** crash backup and moving work between home and work. He does not curate what is in the repo — he needs **everything that makes the tree work** (and anything he asked to keep) on GitHub. The agent decides commit vs skip; he should never have to.

**Full repo index, sister-app pairs, skip lists:** `AGENTS.md` § End-of-Session + multi-repo table in user rules.

## Silent skip list — exclude, never report

These paths are **never committed**. Exclude them from `git add` and from **every report** Chase sees — pull recap, push recap, end-of-session, "put on GitHub", status summaries. Do **not** write "left uncommitted: `d2l-courses.json`" or similar. From his perspective, skip-list files do not exist for sync purposes; mentioning them makes him wonder what went wrong when nothing did.

| Path | Why |
|---|---|
| `.env`, credentials, secrets | Security |
| `Macro App/config/d2l-courses.json` (both path spellings) | Machine-local course list |
| Calendar `server-port.json` | Machine-local port |

**When unsure whether a file is machine-local-only:** ask **one** focused question — then add it to this table if it belongs here. Do not ask about paths already on the skip list.

**When unsure whether to commit (not on skip list):** **commit and push.** There is no downside for Chase — worst case an extra file is on GitHub. Do not ask him to decide. Do not list "judgment call" leftovers in the wrap-up report.

**Only mention a path when** something actually **blocked** sync: merge conflict, hook failure, secret accidentally staged, or a file too large for GitHub. Fix or surface the blocker — not a skip-list item, not "preserved locals", not "still uncommitted".

## Sync recap — what Chase hears after `pull` or `push`

Chase does not track which files are machine-local. Any line about something **not** pulled,
pushed, or committed — even with a good reason — reads like a failure and sends him hunting
for a problem that does not exist.

**On success (no blockers):** say only that sync succeeded. Use plain wording like:

> Everything was pulled and there were no issues.

> Everything was pushed and there were no issues.

> Everything was pulled and pushed and there were no issues.

Optional: one short line on **what landed** (e.g. "Macro App and Programs root — 13 commits
each") if he asked for a pull and something meaningful changed. **No** "except", **no**
"preserved", **no** "left uncommitted", **no** "machine-local", **no** file paths from the
skip list, **no** untracked/scratch callouts unless sync failed because of them.

**On failure:** say what blocked sync and what you did or need — one blocker, plain language.
Do not pad the failure report with skip-list or local-file footnotes.

**Never in a success recap:**

- "Your local changes are still in place"
- "`d2l-courses.json` was not committed"
- "Machine-local files were stashed and restored"
- "These files remain uncommitted"
- A `git status` dump of dirty paths that are normal/local

## Wrap-up report shape (end-of-session / put on GitHub)

Same rule as § Sync recap. Success: *everything committed and pushed* or *everything was pushed
and there were no issues* — not *everything except X, Y, Z*. Skip-list and local-only paths are
omitted entirely. Only report **broken** or **blocked**.

## Why `Pull` must not ask — and must not stop at one repo

Chase works on **two machines** (desktop PC and laptop). GitHub is how files move between them.
When he says **`pull`** — or "pull everything", "pull from GitHub", "pull Macro App",
"same as my PC/laptop", "get everything relevant" — he means **full machine sync**:

- **Down:** every repo under Programs that is behind `origin/main` gets pulled (or merged if diverged).
- **Up:** every repo with work to share gets committed and pushed.
- **Local-only:** paths on the silent skip list stay on this machine and never go to GitHub.
- **No questions:** do not ask which repos, whether to stash, or whether to push. One word is enough.

**The 2026-09-27 laptop incident:** Chase said pull everything relevant. The agent pulled Macro App
(13 commits) but **not** the Programs root repo (also 13 commits — Manim animations, `agent docs/`
scratch pages). He had to ask twice before the animation links worked. **Root cause:** scoped sync to
the Cursor workspace folder instead of scanning all sibling repos.

**Minimum scan set** (every `Pull`, no exceptions):

| Repo | Why it is never optional |
|---|---|
| `Programs/` (root) | Manim Trial, `agent docs/`, session tracking, momentum handoffs |
| `School Scripts/Macro-App` and `School Scrips/Macro App` | Main app (either spelling on disk) |
| `assignment-assistant-engine` | Sister to Macro when vendored separately |
| `student-portal`, Matrix app(s), `electron-toolbar` | Portal / matrix / toolbar work |
| Every other `School Scripts/*` and `School Scrips/*` git repo | Chase expects parity, not curation |

Skip only **frozen** apps (`agent docs/rules/frozen-apps.md` — Calendar 2.0).

## Machine-local paths (preserve; never treat as “dirty repo, skip pull”)

These may differ per machine and must **not** block a pull or get committed on sync:

| Path | Why it stays local |
|---|---|
| `Macro-App/config/d2l-courses.json` (and `School Scrips/Macro App/...`) | Course list / labels differ or drift between machines |
| `student-portal/vite.config.ts`, `student-portal/src/styles/index.css` | `Matrix app` vs `Matrix-app` folder name per machine |
| `student-portal/scripts/lib/roster-codes.mjs` | Tester spare labels per machine |
| `agent docs/session-*.jsonl`, `agent docs/session-*-log.html` | Per-machine session bumps; merge on pull (see below) |
| Calendar `server-port.json` | Port per machine |
| `.env`, credentials, secrets | Never sync |

AppData prefs (Drive roots, machine-profile) live **outside** the repo — leave them alone.

**Procedure when dirty ∩ machine-local only + behind:**  
`git stash push -m "machine-local before pull" -- <those paths>` → `git pull --ff-only` → `git stash pop`. Report what was pulled; mention preserved locals in one line. **Never** leave the repo un-pulled because only those files were dirty.

## Diverged branches — merge and finish (do not ask)

When `git pull --ff-only` fails because the branch is **ahead and behind** (common on the
Programs root after laptop + PC both commit session tracking):

1. Stash machine-local paths if the working tree is dirty.
2. `git merge origin/<branch>` (default merge — **not** rebase unless Chase names it).
3. Fix conflicts, commit the merge, `git stash pop` if needed.
4. **Never** report "needs merge" or "diverged — what do you want?" and stop. Chase's answer is
   always: merge, fix, commit, move on.

**Session-tracking conflicts** (`session-tracking.jsonl`, `session-scorecards.jsonl`, generated
HTML): union both sides' jsonl lines (dedupe), then regenerate:
`node -e "require('./scripts/session-scorecard-ops').regenerate()"`. Do not hand-merge the HTML.

**Other merge conflicts:** resolve in favor of keeping both machines' work when obvious; prefer
remote for generated/scratch you did not touch this session. Commit when clean.

**Only STOP (surface to Chase):** secret/credential accidentally staged, pre-commit hook failure,
file too large for GitHub — not because a merge exists.

## Explicit `Pull` — full sync (pull + push)

Trigger: **`pull`**, "pull everything", "pull from GitHub", "pull Macro App", "pull all",
"same as my PC/laptop", "get everything on this machine", "everything relevant from GitHub".
**Before any other work.** This **is** permission to commit and push mid-session.

For **each** repo in the minimum scan set (and any other git repo under Programs):

1. `git fetch origin`
2. If dirty **only** on machine-local paths → stash those paths (see § Machine-local paths).
3. If behind → `git pull --ff-only`, or merge when diverged (§ Diverged branches).
4. If dirty with shareable work → stage, commit (one message per repo), **push** to `main`.
5. If ahead after pull → **push** even when the working tree is clean.
6. Restore machine-local stashes. Union-merge session-tracking jsonl when both sides bumped.
7. **Do not stop** after the first repo. Named app ("pull Macro App") still means **all** repos.

Summary for Chase (§ Sync recap): on success, *everything was pulled/pushed and there were no
issues* — optional one line on repos that had meaningful commits. **No** local-file footnotes.
Blockers only when sync failed. **No clarifying questions. No "Macro App only" unless every other
repo is current.**

## Start of session without `pull` — pull half only

Trigger: first substantive request, "what's the state", "where did we leave off", "I'm on my
laptop/PC", "let's start" — **without** the word pull. Same full-repo **scan** and **pull**
steps as above (steps 1–3, 6–7), but **do not commit or push** unless he also said pull,
"put on GitHub", or end-of-session.

## Commit / push / "put on GitHub" / end-of-session

Also: Cursor Automation, nightly backup. **No npm test / pytest / builds** unless Chase asks — sync only.

1. Same multi-repo scan; skip frozen apps.
2. Commit + push **every dirty repo** with meaningful changes — not only the active app. One repo per commit.
3. Sister pair when either changed: Macro App ↔ assignment-assistant-engine.
4. **Silent skip** (exclude from add and from Chase's report): `.env`, credentials, `config/d2l-courses.json`, Calendar `server-port.json`. See § Silent skip list above.
5. **Do include:** `Macro App/modules/makeup-exam/exam_history.jsonl` (tracked sync log). **Default:** commit any other dirty tracked or untracked file unless it is on the silent skip list.
6. Summary for Chase (§ Sync recap): success wording only — **no "skipped" column**, no local
paths, no uncommitted inventory. Only report blockers (conflict, hook fail, oversize file).

Run commit/push scan **before** `SESSIONS.md` on end-of-session.

**End-of-session and start-of-session both pull when behind** — do not “skip Macro App” because only `d2l-courses.json` was dirty. That was the laptop incident of 2026-08-24.

## `.gitignore` does not untrack files

If a runtime file keeps appearing in `git status` even though the path is in `.gitignore`,
Git is already tracking it. `.gitignore` only blocks new untracked files; it does not remove
tracked files from the index.

Fix:

1. Confirm the file should not be versioned.
2. Keep the `.gitignore` pattern.
3. Run `git rm --cached <path>` for the tracked runtime file, then commit that removal.
4. Leave the local file on disk unless Chase asked to delete it.

## Anti-patterns

- **`Pull` = Macro App only** (or only the Cursor workspace folder) while Programs root or
  sister repos are behind — the 2026-09-27 Manim incident.
- Asking “stash d2l-courses and pull?” after he said pull.
- Pulling without pushing when this machine has unpushed commits — he expects both machines
  to match GitHub after `pull`.
- Skipping an entire repo at EOS because a machine-local file was dirty.
- Waiting for him to name every sibling repo when he said “pull” / “same as my PC.”
- Overwriting `d2l-courses.json` with the other machine’s copy during pull restore.
- Leaving a repo **diverged** or **mid-merge** because Chase "might want rebase" — he doesn't; merge and finish.
- Reporting "Programs root needs attention" without merging when he said pull / pull everything.
- Explaining the sync plan instead of executing it — he uses GitHub to avoid re-explaining every session.
- Success recap that mentions uncommitted, machine-local, stashed, or "preserved" files — makes
  him think sync failed when it did not.
- Dumping `git status` dirty paths after a successful pull/push unless something blocked sync.
