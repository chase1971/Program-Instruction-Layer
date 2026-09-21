# Momentum handoff — Practice archive: Chase's live session → gap analysis

**Written:** 2026-09-20 (Sunday, ~3:28 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **guided practice archive** — permanently store what students do (`session_log`, `problem_id`, help usage, wrong answers, recovery steps) so teachers can review later.

**Phase:** **Capture plumbing is built; teacher review UX is explicitly NOT the product yet.** Contract tests + DB verify script prove events *can* land in Supabase. Macro App has a placeholder **Practice archive** panel (health strip, heatmap, raw timeline) — Chase confirmed it is **not useful enough** for teaching decisions.

**Chase's plan (approved this session):**
1. **Chase** will complete **one full guided practice problem himself**, making **intentional mistakes** along the way (wrong cell, wrong op type, wrong row notation, help feedback, recovery steps, etc.).
2. **Next agent** waits until that attempt exists, then builds a **gap-analysis tool/report** for that single session: what happened vs what was stored vs what a teacher would need — **before** designing stats, replay, or polished Teacher Console UI.

**Why this order:** View/analyze UX can be done after the fact. **Capture shape cannot** — once students move on, that data is gone forever.

---

## 2. Chase's desired feel (use his language)

### What the current timeline fails at
- `help-feedback · Yes` tells him nothing — **"help feedback for what?"** He needs: multiply topic, example EX1, the question being answered.
- `answer · op1-pick-cell · R1C2 · wrong` — he can infer row/column, but **not the matrix they were looking at**, not the prompt in plain English.
- `recovery-step · highlight-row` — **meaningless without context** (which step? what did the system do?).
- Row transformation wrong — he needs **what they typed**, ideally **what error they saw**; maybe eventually a mockup of the screen, but at minimum the typed expression + matrix state.

### What he wants eventually (NOT this task)
- Optional drill-down: almost a screenshot / screen mockup at each wrong moment.
- Statistical buckets: "how many got row transformation wrong because reciprocal vs wrong op type" — **robust taxonomy**, built **after** capture is right.
- He does **not** want to spend a lot of time on Teacher Console polish **now**.

### What he wants **this** task to produce
- After his one live session: a **gap analysis** — "here's what you did, here's what's in `session_log`, here's what's missing or unreadable."
- That analysis drives the **next** capture changes (e.g. `matrixBefore`, `errorMessage`, richer `meta`) — not guesswork from fixtures.

---

## 3. Accepted decisions (do not re-litigate)

| Decision | Detail |
|---|---|
| Archive first, pretty UI later | Supabase `attempts.session_log` + `problem_id` is the source of truth |
| Migration 045 + bank RPCs | `student-session-kit/supabase/migrations/045_practice_bank_and_problem_id.sql` — pushed |
| Portal writes events on finish | `useGuidedPracticeAttempt.ts` → `buildGuidedPracticeSessionLog` |
| Contract tests gate portal | `student-portal/src/test/*Archive*.contract.test.ts` — **42 tests pass** |
| DB round-trip script | `student-session-kit`: `npm run verify-practice-archive` |
| Teacher Console panel = placeholder | `PracticeArchivePanel.tsx` — useful for dev inspection only |
| UUID label fix | Show `Instructor · CODE` via `instructorStudents` lookup — restart Macro App + Refresh responses |
| Static shape sample | [practice-archive-sample.html](http://127.0.0.1:8765/scratch/practice-archive-sample.html) — not live data |
| Chase does the first real session | Intentional mistakes, full guided problem — **not** an AI bot for this step |
| Next agent: gap analysis only | No full replay UI, no error taxonomy dashboard, no Netlify deploy unless Chase asks |

---

## 4. Rejected directions — do not redo

- **Building rich Teacher Console review UI before Chase's live session** — he explicitly deferred analyze/view work.
- **Assuming the sample HTML timeline is teacher-ready** — it shows JSON *shape*, not usable review.
- **AI random walk as the first test** — Chase will walk through himself so ground truth is known.
- **Screenshot capture as v1** — discussed as expensive; matrix snapshot + typed values are the pragmatic middle ground *after* gap analysis.
- **Treating `session_log: null` rows as bugs** — old attempts pre-archive; ignore them.

---

## 5. Current implementation state

### What gets captured today (guided)

Events in `session_log.events[]` (see `Matrix app/src/app/hooks/guided-practice-event-emit.ts`):

| Kind | Stored fields | Example gap |
|---|---|---|
| `answer` | `slot`, `prompt`, `choice`, `correct`, `attemptIndex`, `elapsedMs` | **No** `matrixBefore`, **no** validator error text |
| `help-open` | `meta.helpTopic` | Timeline **drops** `meta` |
| `help-example` | `choice` (e.g. EX1) | Not linked to topic in display |
| `help-feedback` | `choice`, `meta.helpTopic` | Timeline shows only `Yes` |
| `recovery-step` | `slot`, `choice` (e.g. `highlight-row`) | No human label |
| `portal-nav` | `choice`, `meta.problemId` | OK |

Fixture with full event shape: `student-portal/src/test/fixtures/guidedPracticeArchiveFixtures.ts`

Summarizers (Macro App, not wired to rich UI yet):
- `guidedPracticeSessionLog.ts` — `wrongAttemptsBySlot`, `helpUsageSummary`
- `practiceSessionTimeline.ts` — **stripped display** (root cause of "help feedback yes" confusion)

### Key files

| Area | Path |
|---|---|
| Portal hook | `student-portal/src/features/guided-practice/useGuidedPracticeAttempt.ts` |
| Event normalize | `student-portal/src/features/guided-practice/guidedPracticeSessionEvents.ts` |
| Matrix app emit | `Matrix app/src/app/hooks/guided-practice-event-emit.ts` |
| Slot labels | `Macro App/renderer/src/utils/matrixReport/matrixSlotCatalog.ts` |
| TC placeholder | `Macro App/renderer/src/components/teacher-console/PracticeArchivePanel.tsx` |
| Verify script | `student-session-kit/scripts/verify-practice-archive.mjs` |

### Verification already done
- `student-portal`: `npm test` — 42 pass; `npm run build` — pass
- `npm run verify-practice-archive` — writes/reads unguided row with full JSON
- **Portal NOT deployed** to Netlify unless Chase asks (`npm run deploy:prod`)

### Git
- **Uncommitted** across student-portal, student-session-kit, Macro App. Do **not** commit until Chase says "put on GitHub" or end-of-session protocol.

---

## 6. Open questions and constraints

### Before Chase's session — capture must be live
**Critical:** Production Netlify may **not** have archive code yet. For his session to land in Supabase with full `session_log`:
- **Option A:** Chase runs portal locally (`npm run dev` in student-portal) against Supabase, **or**
- **Option B:** Agent deploys with `npm run deploy:prod` **only if Chase asks first**

If he tests on stale Netlify, `session_log` may be null — gap analysis will be worthless.

### Finding his attempt afterward
- Macro App Teacher Console → Guided Practice activity → **Practice archive** tab → pick attempt **without** `· no archive` suffix
- Or query Supabase `attempts` for his instructor student id (verify script uses same account)
- Or re-run/adapt `verify-practice-archive.mjs` to **fetch** by attempt id instead of write

### Next agent must NOT
- Launch GUI / open browser without Chase's permission
- Build full session replay or screenshot pipeline in the first gap-analysis pass
- Deploy to Netlify without explicit ask

### Frozen
- Calendar 2.0 — do not touch

---

## 7. Exact next step (for fresh agent)

**Wait for Chase's completed guided session, then build gap analysis on that one attempt.**

1. Read this file first.
2. Confirm with Chase: session is done; note **problem id**, **attempt id** or approximate time, and whether he used **local dev** or **Netlify**.
3. Pull raw `session_log` JSON for that attempt (Supabase / Macro App IO / script).
4. Build a **gap-analysis deliverable** — HTML on port 8765 is fine (`agent docs/scratch/`) — that walks event-by-event:
   - **What Chase did** (from his description or a checklist he confirms)
   - **What's in the log** (raw + decoded with `prompt`, `meta`, slot labels from `matrixSlotCatalog`)
   - **What's missing** for teacher usefulness (matrix state, error text, help context, recovery labels, etc.)
5. Propose **minimal capture additions** ranked by impact — do **not** implement them until Chase approves the list.
6. **Do not** build polished Teacher Console review UI in this task.

**Tier A display fix** (show existing `prompt` + `meta` in timeline) is optional quick win *after* gap analysis confirms those fields are populated in the live session — not a substitute for gap analysis.

---

## 8. Chase's pre-task checklist (flat statement)

1. Use a build that has archive capture (local dev or deployed Netlify after deploy).
2. Sign in as instructor/test account.
3. Complete **one full guided problem** — all ~17 steps if possible.
4. Make **intentional mistakes**: wrong cell, wrong op type, wrong row notation, open help + feedback, trigger recovery.
5. Finish the problem so `session_log` submits.
6. Tell the next agent: done + which environment + rough time or attempt picker label.

---

## Copy-ready navigation path

`latest.md` → pull attempt `session_log` → `guidedPracticeArchiveFixtures.ts` (shape reference) → `guidedPracticeSessionLog.ts` + `matrixSlotCatalog.ts` (decode) → write gap-analysis HTML in `agent docs/scratch/`
