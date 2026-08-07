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

## Start of session — pull first

Trigger: first substantive request, or "what's the state", "where did we leave off", "I'm on my laptop/PC", "let's start", "pull". **Before any code changes.**

1. Scan git repos under Programs (`School Scrips/*`, Programs root). `git status --short` + `git fetch` each. **Skip frozen apps** (`agent docs/rules/frozen-apps.md` — Calendar 2.0).
2. Clean + behind → `git pull --ff-only`. Report updates.
3. Dirty + remote ahead → **STOP** — surface local vs incoming (two-machine collision).
4. Merge conflict → **STOP** — never auto-resolve. Per-machine styling in committed source → ask Chase (likely belongs in AppData profile, not source).
5. Summary: pulled / current / needs attention.

## Commit / push / "put on GitHub" / end-of-session

Also: Cursor Automation, nightly backup. **No npm test / pytest / builds** unless Chase asks — sync only.

1. Same multi-repo scan; skip frozen apps.
2. Commit + push **every dirty repo** with meaningful changes — not only the active app. One repo per commit.
3. Sister pair when either changed: Macro App ↔ assignment-assistant-engine.
4. Skip unless asked: `.env`, credentials, `config/d2l-courses.json` backups, Calendar `server-port.json`.
5. **Do include:** `Macro App/modules/makeup-exam/exam_history.jsonl` (tracked sync log).
6. Summary table: repo, commit, push result, skipped.

Run commit/push scan **before** `SESSIONS.md` on end-of-session.

## `.gitignore` does not untrack files

If a runtime file keeps appearing in `git status` even though the path is in `.gitignore`,
Git is already tracking it. `.gitignore` only blocks new untracked files; it does not remove
tracked files from the index.

Fix:

1. Confirm the file should not be versioned.
2. Keep the `.gitignore` pattern.
3. Run `git rm --cached <path>` for the tracked runtime file, then commit that removal.
4. Leave the local file on disk unless Chase asked to delete it.
