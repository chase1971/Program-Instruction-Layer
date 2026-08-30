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

**Full repo index, sister-app pairs, skip lists:** `AGENTS.md` § End-of-Session + multi-repo table in user rules.

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
4. Skip unless asked: `.env`, credentials, `config/d2l-courses.json`, Calendar `server-port.json`.
5. **Do include:** `Macro App/modules/makeup-exam/exam_history.jsonl` (tracked sync log).
6. Summary table: repo, commit, push result, skipped.

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
