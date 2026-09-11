# Multi-repo Git — pull at start, commit and push at end

> **Rung 5 — on demand.** The always-on summary is root `AGENTS.md` § Git; this
> file is the detail behind it. Read it when that section is not enough.
> **What it covers:** Sync every git repo under Programs — pull at the start of a session, commit and push at the end. Not just the active app. Summary lives in AGENTS.md § Git.
>
> *Was `.cursor/rules/40-multi-repo-git-push.mdc` until 2026-08-02. Moved because `.cursor/rules/*.mdc`
> only load when a matching file is open in a Cursor editor tab — which is not how Chase works.
> AGENTS.md links this file by path instead, so every tool can reach it.*

---

Chase uses **sibling repos** under `C:\Users\chase\Documents\Programs\` (not a monorepo). **Pull before you start, push before you stop** — agent drives this; Chase cannot rely on remembering.

**Why GitHub exists for Chase:** crash backup and moving work between home and work. He does not curate what is in the repo — he needs **everything that makes the tree work** (and anything he asked to keep) on GitHub. The agent decides commit vs skip; he should never have to.

**Full repo index, sister-app pairs, skip lists:** `AGENTS.md` § End-of-Session + multi-repo table in user rules.

## Silent skip list — exclude, never report

These paths are **never committed**. Exclude them from `git add` and from **every report** Chase sees — end-of-session, "put on GitHub", status summaries. Do **not** write "left uncommitted: `d2l-courses.json`" or similar. From his perspective, skip-list files do not exist for sync purposes; mentioning them creates work he did not ask for.

| Path | Why |
|---|---|
| `.env`, credentials, secrets | Security |
| `Macro App/config/d2l-courses.json` (both path spellings) | Machine-local course list |
| Calendar `server-port.json` | Machine-local port |

**When unsure whether to commit:** **commit and push.** There is no downside for Chase — worst case an extra file is on GitHub. Do not ask him to decide. Do not list "judgment call" leftovers in the wrap-up report.

**Only mention an uncommitted path when** something actually blocked sync: merge conflict, hook failure, secret accidentally staged, or a file too large for GitHub. Fix or surface the blocker — not a skip-list item.

## Wrap-up report shape

One line (or short table): repos **committed and pushed**, check-docs summary, anything **broken**. Success wording: *everything committed and pushed* — not *everything except X, Y, Z*. Skip-list paths are omitted entirely.

## Why pull must not ask

Chase works on **two machines** (desktop PC and laptop). When he says **"pull"**, **"pull Macro App"**, **"same as my PC"**, or **"I'm on the laptop"**, he means: **bring this machine’s code up to GitHub’s tip**, keep laptop/PC-only files, and **do not ask him to spell out the plan**. Asking “stash d2l-courses.json?” after he already said pull is the failure mode — it blocked a 7-commit Macro App sync while PC had already shipped.

## Machine-local paths (preserve; never treat as “dirty repo, skip pull”)

These may differ per machine and must **not** block a pull or get committed on sync:

| Path | Why it stays local |
|---|---|
| `Macro-App/config/d2l-courses.json` (and `School Scrips/Macro App/...`) | Course list / labels differ or drift between machines |
| Calendar `server-port.json` | Port per machine |
| `.env`, credentials, secrets | Never sync |

AppData prefs (Drive roots, machine-profile) live **outside** the repo — leave them alone.

**Procedure when dirty ∩ machine-local only + behind:**  
`git stash push -m "machine-local before pull" -- <those paths>` → `git pull --ff-only` → `git stash pop`. Report what was pulled; mention preserved locals in one line. **Never** leave the repo un-pulled because only those files were dirty.

**Real collision (STOP):** dirty includes tracked **source** (code, docs, configs that are not in the table above) **and** remote is ahead — surface local vs incoming. Or merge conflict after pull — never auto-resolve. Per-machine styling wrongly living in committed source → ask once (belongs in AppData profile).

## Start of session / explicit pull — pull first

Trigger: first substantive request, or "what's the state", "where did we leave off", "I'm on my laptop/PC", "let's start", "pull", "pull Macro App", "pull all", "same as my PC". **Before any code changes.**

1. Scan git repos under Programs (`School Scripts/*`, `School Scrips/*`, Programs root, `electron-toolbar`). `git status --short` + `git fetch` each. **Skip frozen apps** (`agent docs/rules/frozen-apps.md` — Calendar 2.0).
2. Clean + behind → `git pull --ff-only`.
3. Dirty **only** machine-local paths + behind → stash those paths, pull, restore (see above). **Do not ask.**
4. Named app (“pull Macro App”) → do that repo **and** still scan sisters if they are behind (especially Macro ↔ assignment-assistant-engine). Do not stop after one repo if others are obviously behind unless he named a single app and the others are current.
5. Dirty source + remote ahead, or merge conflict → **STOP** — surface it.
6. Summary: pulled / current / preserved locals / needs attention. **No clarifying questions about what “pull” means.**

## Commit / push / "put on GitHub" / end-of-session

Also: Cursor Automation, nightly backup. **No npm test / pytest / builds** unless Chase asks — sync only.

1. Same multi-repo scan; skip frozen apps.
2. Commit + push **every dirty repo** with meaningful changes — not only the active app. One repo per commit.
3. Sister pair when either changed: Macro App ↔ assignment-assistant-engine.
4. **Silent skip** (exclude from add and from Chase's report): `.env`, credentials, `config/d2l-courses.json`, Calendar `server-port.json`. See § Silent skip list above.
5. **Do include:** `Macro App/modules/makeup-exam/exam_history.jsonl` (tracked sync log). **Default:** commit any other dirty tracked or untracked file unless it is on the silent skip list.
6. Summary for Chase: repo, commit, push result — **no "skipped" column** for silent-skip paths. Only report blockers (conflict, hook fail, oversize file).

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

- Asking “stash d2l-courses and pull?” after he said pull.
- Skipping an entire repo at EOS because a machine-local file was dirty.
- Waiting for him to name every sibling repo when he said “pull” / “same as my PC.”
- Overwriting `d2l-courses.json` with the other machine’s copy during pull restore.
