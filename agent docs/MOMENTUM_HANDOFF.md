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

**"Momentum handoff" = continue this work in a fresh task, in any tool (Cursor, Claude Code,
Codex) or on a different model, without losing the judgment built through the conversation.**
It is not the end-of-session protocol.

- Finish the current coherent deliverable; do not abandon an edit halfway through.
- Do not commit, push, finalize session metrics, run the end-of-session protocol, archive the
  task, or run broad closeout checks unless Chase separately asks.
- Do not create or switch tasks automatically. Nothing needs to be copied: tell Chase to say
  *"read the latest momentum handoff"* in the fresh task, then stop.
- A normal session-tracking bump is still required for any deliverable completed before the
  handoff.

**Handoff versus wrap-up (no overlap).** The wrap-up entry in `SESSIONS.md` is the permanent
record and carries `Repos touched:` (pull depends on it). The handoff is the continuation state
(feel, decisions, rejected directions, next step) and is overwritten. A handoff writes **both**
so Chase says it once: the full handoff to `latest.md`, plus the short `SESSIONS.md` entry
defined in [WRAP_UP.md](./WRAP_UP.md), whose `Next session:` line just points at `latest.md`.
Do not repeat the handoff's content in the entry.

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
4. Append the short wrap-up entry per [WRAP_UP.md](./WRAP_UP.md) step 1, with `Repos touched:`
   filled in and `Next session: see agent docs/momentum-handoffs/latest.md (<date>)`.
5. Bump session tracking if a deliverable just finished.
6. Reply to Chase with the short shape under "Final response shape". No pasted prompt.

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

Two sentences at most: the current deliverable is safely stopped and no GitHub or end-of-session
actions were performed; **`agent docs/momentum-handoffs/latest.md`** and the `SESSIONS.md` entry
were written. Then: *In the fresh task, say "read the latest momentum handoff."*

No fenced prompt to copy, no checklist. The root `AGENTS.md` trigger loads in every tool, so the
phrase is enough.

---

## Anti-patterns

- A generic status report that preserves files but loses Chase's taste, corrections, or reasons.
- Copying the whole conversation and carrying its token-heavy dead ends into the new task.
- Treating tentative discussion as an approved specification.
- Running the end-of-session protocol, committing, or pushing without an explicit request.
- Telling the new agent only to "continue where we left off" without supplying the state.
- Handoff only in chat with **no** `latest.md` write — the next agent will not see it.
- Reading week-old `latest.md` without checking the date.
- Pasting the handoff's content into `SESSIONS.md` as well. Keep one copy; the entry points.
- Two handoffs on different topics the same day: `latest.md` is a single slot and the second
  overwrites the first. If another topic's handoff is still live, say so and name the file by
  topic instead of overwriting.
