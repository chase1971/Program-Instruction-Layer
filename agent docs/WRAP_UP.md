# Wrap up — document this chat only (no git)

> **Rung 5 — on demand.** Always-on trigger: root `AGENTS.md` § Wrap up.
>
> **Fires on:** **"wrap up the session"**, **"wrap up"** (when clearly ending *this* agent’s work).
>
> **Not the same as** end-of-session protocol — wrap up **does not** commit, push, or run
> `check-docs`. Chase saves to GitHub once at the end of the night (or when he says
> **"put on GitHub"** / **end of session protocol**).

---

## What this phrase means

**Wrap up = log what this conversation did.** Use when parallel agents are still working,
tests are running elsewhere, or Chase is not ready for GitHub to see half-finished work.

- **This chat only** — do not invent a full story for other agents’ tasks.
- **No git** — no `git status` sweep for commit purposes, no commit, no push.
- **Do not ask** Chase to run, launch, or verify anything.

Night sync or **"put on GitHub"** moves code + these log entries to the other machine.

---

## Steps

1. **Append one session entry, newest at top** — same routing as
   [END_OF_SESSION.md](./END_OF_SESSION.md) step 3 (app log vs `agent docs/sessions/SESSIONS.md`).

   Use this template. **`Repos touched:` is required** so a later **pull** can find the right
   git roots without Chase naming them.

   ```
   ## YYYY-MM-DD — [Brief title]

   **Repos touched:** [git roots — e.g. `School Scrips/Macro App`, `School Scrips/student-portal`, `Programs/` root]

   **Files changed:** [main paths — optional line deltas]

   **What worked:** [what this chat accomplished]

   **Current state:** Green / Broken / Mid-refactor — [one sentence]

   **File size flag:** [files >500 lines or grew >200, else "None"]

   **Next session:** [concrete next action for a future agent]
   ```

   **`Repos touched:` rules:** list **folder paths that are git repo roots** (see
   [APP_LOCATIONS.md](../APP_LOCATIONS.md)). Portal work → always list **both**
   `student-portal` and `student-session-kit`. Macro gradebook / Teacher Console →
   `School Scrips/Macro App` only. Manim / agent docs → `Programs/` root.

2. **Leave TODO comments** in code if this chat stopped mid-edit.

3. **Report one short line:** which `SESSIONS.md` was updated and the entry title. No git recap.

---

## Optional

- Task still finishing → `node scripts/append-session-scorecard.js --note "…"` if a deliverable
  just completed (same as mid-session bumps).
- **Do not** run `--finalize-file` or full session metrics here — that stays with end-of-night sync
  unless Chase asks.

---

## Other agents and unpushed logs

Wrap-up entries stay **local** until a later commit/push. Another machine’s pull **cannot**
see tonight’s wrap-up on the desktop until GitHub has it. Session-guided pull (see
[rules/multi-repo-git-push.md](./rules/multi-repo-git-push.md) § Session-guided pull) uses
**already-pushed** `SESSIONS.md` entries on `origin`.
