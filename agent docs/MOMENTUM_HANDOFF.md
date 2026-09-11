# Momentum handoff protocol

> **Rung 5 — on demand.** The always-on trigger is root `AGENTS.md` § Momentum handoff;
> this file owns the procedure.
>
> **Fires on:** "perform a momentum handoff" · "switch to a fresh task" ·
> "give the next agent our momentum".
>
> **Resume fires on:** "read the latest momentum handoff" · "continue from the handoff" ·
> "pick up the momentum handoff" · "what did the last agent leave off" (when clearly
> meaning a fresh-task continuation, not `SESSIONS.md` history).

---

## What this phrase means

**"Momentum handoff" = continue this work in a fresh Codex task without losing the judgment
built through the conversation.** It is not the end-of-session protocol.

- Finish the current coherent deliverable; do not abandon an edit halfway through.
- Do not commit, push, finalize session metrics, append an end-of-session entry, archive the
  task, or run broad closeout checks unless Chase separately asks.
- Do not create or switch tasks automatically. Give Chase one copy-ready prompt for the fresh
  task, then stop.
- A normal session-tracking bump is still required for any deliverable completed before the
  handoff.

---

## Where handoffs live (single predictable place)

| File | Role |
|---|---|
| **`agent docs/momentum-handoffs/latest.md`** | **Always read this first** when Chase says "read the latest momentum handoff." Overwritten on every perform. |
| `agent docs/momentum-handoffs/YYYY-MM-DD_short-slug.md` | Same content, dated archive for the last few days. |
| This file (`MOMENTUM_HANDOFF.md`) | Procedure only — not the handoff content. |

**Freshness:** `latest.md` is only trustworthy for **today's continuation work**. If it is
missing or clearly stale (wrong date, unrelated topic), say so — do not guess from old dated
files without telling Chase.

**Retention:** After writing, run `node scripts/prune-momentum-handoffs.js --yes` — deletes
dated archives older than **3 days**. Never deletes `latest.md`.

---

## Perform a momentum handoff — agent steps

1. Build the handoff from evidence (see sections below) — do not re-investigate for show.
2. **Write disk:**
   - Overwrite `agent docs/momentum-handoffs/latest.md` with the full handoff.
   - Write the same content to `agent docs/momentum-handoffs/YYYY-MM-DD_short-slug.md`.
3. Run `node scripts/prune-momentum-handoffs.js --yes` from Programs root.
4. Bump session tracking if a deliverable just finished.
5. Reply to Chase: one sentence (no GitHub / no end-of-session), then a **copy-ready fresh-task
   prompt** that starts with: *Read `agent docs/momentum-handoffs/latest.md` first, then …*

---

## Read the latest momentum handoff — agent steps

1. Read **`agent docs/momentum-handoffs/latest.md`** immediately — before grepping or opening
   app code.
2. Check the **Written** date in that file. If it is not from today (or the topic does not
   match what Chase said), stop and tell him — one focused question if needed.
3. Read the "Read first" and "Exact next step" sections, then the app docs they name.
4. Do **not** treat `docs/sessions/SESSIONS.md` as a substitute — that is end-of-session
   history; this file is continuation judgment.

---

## Build the handoff from evidence

Inspect only what is needed to make the handoff accurate: the current conversation, relevant
plans or app documentation, changed-file status, and verification already performed. Do not
start a new investigation or repeat tests merely to make the summary look complete.

Preserve the working relationship, not the transcript. The handoff must contain:

1. **Objective and current phase** — what Chase is trying to achieve and where the work stands.
2. **Chase's desired feel** — the qualities, priorities, comparisons, and examples that shaped
   the direction, using his language where it carries meaning.
3. **Accepted decisions** — what was chosen and why.
4. **Rejected directions** — what was tried or discussed, why it was wrong, and what must not
   be rediscovered.
5. **Current implementation state** — relevant files, completed changes, uncommitted state,
   and verification results.
6. **Open questions and constraints** — unresolved choices, blockers, permissions, and rules
   that materially affect the next move.
7. **Exact next step** — one concrete action for the fresh task to begin with.

Separate facts from interpretation. If Chase has not approved a direction, label it as a
proposal rather than turning it into a decision.

---

## Final response shape (perform only)

Start with one sentence saying the current deliverable is safely stopped and no GitHub or
end-of-session actions were performed. Note that **`agent docs/momentum-handoffs/latest.md`**
was updated. Then provide one fenced text block that Chase can paste as the first message of a
fresh Codex task. The prompt must instruct the new agent to read `latest.md` first, then the
applicable repository docs.

End after the block. Do not add a second checklist for Chase.

---

## Anti-patterns

- A generic status report that preserves files but loses Chase's taste, corrections, or reasons.
- Copying the whole conversation and carrying its token-heavy dead ends into the new task.
- Treating tentative discussion as an approved specification.
- Running the end-of-session protocol, committing, or pushing without an explicit request.
- Telling the new agent only to "continue where we left off" without supplying the state.
- Handoff only in chat with **no** `latest.md` write — the next agent will not see it.
- Reading week-old `latest.md` without checking the date.
