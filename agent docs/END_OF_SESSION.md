# End-of-session protocol

> **Rung 5 — on demand.** The always-on trigger is root `AGENTS.md` § End-of-session; this file
> holds the steps.
>
> **Fires on:** "end of session protocol" · "wrap the session" · "we're done for now".
>
> **Invoking it *is* permission to commit and push.** No separate ask needed.
>
> **Invoking it also means:** Chase is **done** — no more coding, no more running
> anything tonight. Assume he already tested what mattered (or accepts headless CI).
> **Do not ask him to run, launch, restart, open, or verify anything** — not apps, not
> servers, not browsers, not smoke tests, not "quick checks."

---

## What this phrase means

**"End of session protocol" = I'm done.** Wrap-up is **agent-only**: git, scorecard,
session log, commit/push, check-docs, one-line report — then stop.

- **Never** ask Chase to run anything as part of wrap-up.
- **Never** end with handoff steps directed at him ("restart and confirm…", "want to
  launch…?", "smoke-test these three things…").
- Headless checks during the session are enough for **Current state** unless he said
  something is still broken.
- If he confirmed it works in chat, log **Green** — not "Green headlessly — live test
  needed."
- **Next session** in the log is for a *future* agent/session, not a to-do list for Chase
  tonight.

Mid-session is different: still ask before launching GUIs per root `AGENTS.md` § Never put
anything on Chase's screen without asking.

---

## The seven steps

1. **Git status** — briefly list untracked/modified across the tree, not just the active app.

2. **Session metrics finalize** — `node scripts/append-session-scorecard.js --finalize-file <meta.json>`.
   Task **tracking** bumps should already be on disk from `--bump-file` during the session
   ([SESSION_TRACKING.md](./SESSION_TRACKING.md)). Finalize writes the metrics card only —
   see [SESSION_METRICS.md](./SESSION_METRICS.md). **Don't re-guess counts** from memory.

3. **Append a session entry, newest at top.** Which log depends on what the work touched:

   | Work was… | Log |
   |---|---|
   | Inside one app | `<app>/docs/sessions/SESSIONS.md` |
   | **The instruction layer itself** — `agent docs/`, root `AGENTS.md`/`CLAUDE.md`, `agent docs/recipes/INDEX.md`, `agent docs/recipes/INDEX.md`, the capture skill, `check-docs.js` and friends | **`agent docs/sessions/SESSIONS.md`** |
   | Cross-app work with no instructional-layer content (touched several apps' code, not their docs) | The most-touched app's `SESSIONS.md`; name the others in the entry |

   **This log is for the documentation system, not a catch-all cross-app diary.** If it touched
   both instruction-layer docs and app code, log it where the *instructional* substance was and
   name the app work in the entry. School documents / exam-map / Pearson-harvest work belongs in
   `School Scrips/School documents/docs/sessions/SESSIONS.md`, even when the output HTML happened
   to be served from `agent docs/` — the folder a page is *served* from is not the same as the
   work being *about* the instructional layer.

   ```
   ## YYYY-MM-DD — [Brief title]

   **Files changed:** [files with line-count deltas if relevant]

   **What worked:** [what got accomplished]

   **Current state:** Green / Broken / Mid-refactor — [one sentence]

   **File size flag:** [files now >500 lines or that grew >200, else "None"]

   **Next session:** [the concrete next action]
   ```

4. **Leave TODO comments** in code wherever work stopped mid-edit.

5. **Commit and push** per root `AGENTS.md` § Git — **every dirty repo, one commit per repo**,
   not only the active app. Sibling repos are separate git repos; committing the root does not
   commit them.

6. **`node scripts/check-docs.js`** — report the summary line. Fix dead links, and add an index
   row for any recipe or doc this session created.

7. **Report back in one short line:** what was logged, commit/push result, check-docs summary,
   anything left broken. **Do not ask Chase to run anything.**

---

## Never correct a past entry

`SESSIONS.md` is history. If an old entry is wrong, the next entry says so — the old one stays as
written. This is why the rename sweeps in this tree skip `SESSIONS.md` files.

## On "what's the state" / "where did we leave off"

Not this protocol. Read the latest `SESSIONS.md` entry and summarize in 2–3 lines.
