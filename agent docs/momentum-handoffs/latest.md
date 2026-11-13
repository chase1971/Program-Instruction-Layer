# Momentum handoff — AACU combined panel review

**Written:** 2026-11-12  
**Continue in:** fresh task (any tool / model)

---

## Objective and current phase

Chase is reviewing AACU session panels in the combined / starred review HTML stack
(`AI presentations`), clarifying talk premises from transcripts, and tightening panel
summaries when the compressed one-liners were confusing or under-sold cool detail.

Phase: **mid review.** Tagging + starring queue already built earlier. This stretch was
Q&A on specific panels, then two summary expansions Chase liked enough to keep in the
data files.

Open combined review:
[aacu-combined-review](http://127.0.0.1:8765/ai-presentations/aacu-combined-review.html)
(starred:
[aacu-starred-review](http://127.0.0.1:8765/ai-presentations/aacu-starred-review.html)).

---

## Chase's desired feel

- Plain-language premises first. If a summary mashup confuses him, expand the actual
  case (who did what) before the framework jargon.
- When a workflow is cool and concrete (Texas Tech tools), put the **steps** in the
  panel summary/claims, not leave them only in chat.
- STT slips are expected (Malala is real; “football” ≈ soccer for international
  student examples). Correct quietly when obvious.
- Flat handoffs. Links only as `http://127.0.0.1:8765/...`. No “want me to…”.
- No surprise GUIs.

---

## Accepted decisions

- **Who Does Your AI Policy Protect** (`who-policy-protects` in `day2-candidates.js`):
  summary + first claim now spell Student A vs Student B clearly (A used chatbot → low
  detector → no flag; B multilingual / first-gen / phone-between-shifts → high score →
  referral → 5-day appeal requiring version history they lack).
- **Barking Up the Right Tree** (`barking-right-tree`): summary + claims expanded with
  Retriever (minutes/video → Gemini → ~5-para timestamped drafts; Copilot / All Coverage;
  Lubbock 1 of 17 book-ban example) and NewsHound (citation-only library → questions →
  hypothesis stress-test → stories / sources / FOIAs). Verification-first, human publishes.
- **When AI Interprets** clarification (chat only, no file edit this stretch): students
  made their own advocacy visuals (often found images / arrangement, not studio art),
  uploaded to JSTOR Seeklight; AI as second audience vs artist statement; gap drives
  revision. Malala Yousafzai is the real activist; football ≈ soccer in that example.

---

## Rejected directions

- Do not compress Student A/B back into “one flagged… unable to meet five-day appeal”
  (that mashup made Chase think one student had both problems).
- Do not treat Texas Tech as a vague “local news research study”; it is an operating
  university newsroom tool stack (Watchdogs / Retriever / NewsHound).
- Momentum handoff ≠ end-of-session: no commit/push unless Chase asks separately.

---

## Current implementation state

**Touched this stretch (AI presentations):**
- `site/shared/day2-candidates.js` — `who-policy-protects` and `barking-right-tree`
  summary/claims expansions.

**Already in place from earlier in the broader AACU thread (do not rebuild):**
- Combined + starred review HTML, `panel-tags.js`, `panel-fields.js`, starring queue
  (Pending → starred boards, scroll-to-top), Day 1–3 candidates, watched HTML.
- Stage deck work (slide video autoplay, learn-before-lesson art) was earlier; not the
  active thread at handoff time.

**Uncommitted:** expect dirty `AI presentations` (and possibly Programs root docs from
this handoff). No push this turn.

**Verification:** content edits only; no GUI launch.

**Transcript sources (My Drive):**
- `AACU/unwatched/Who Does Your AI Policy Protect.md`
- `AACU/unwatched/Barking Up the Right Tree.md`
- `AACU/unwatched/When AI Interprets.md`

---

## Open questions and constraints

- Chase may keep walking panels and ask for more summary expansions; prefer editing the
  candidate JS that feeds the review pages over inventing new HTML.
- Stage / References / sort-beyond-stars called out as later in prior chat; not started
  here.
- Never deploy Netlify unless he says so in the same message.
- Permission per run for any visible window.

---

## Exact next step

Open
[aacu-combined-review](http://127.0.0.1:8765/ai-presentations/aacu-combined-review.html),
find **Barking Up the Right Tree** and **Who Does Your AI Policy Protect**, confirm the
expanded summaries read the way Chase wants, then continue panel-by-panel clarifications
(or starring) from wherever he left off in Pending.
