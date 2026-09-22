# Momentum handoff — Gauss-Jordan guided practice UX (row notation + help triggers)

**Written:** 2026-09-20 (Sunday, ~4:35 PM)

---

## 1. Objective and current phase

**Active thread:** Local UX polish for **Gauss-Jordan Method Practice** in the **student portal**, which embeds the **Matrix app** via Vite alias `@matrix/`. Chase tests with dwell-click + speech-to-text. **Local dev only** unless he explicitly asks to deploy.

**Phase:** **Row-notation wrong-answer flows and help-trigger interaction are implemented; awaiting Chase's live verification.** Earlier in this multi-session arc, Phase 1 (resume, abandonment tracking, pool rules, teacher console visibility) was deployed to Netlify + Supabase — that is **not** the current focus.

**This session's deliverable (just finished):**
- Help trigger: **! icon = click to open help**, **label text = drag handle**
- Row-replacement notation help at **`{ x: 294, y: 133 }`**
- Row transformation notation stays **one unbreakable line** (`.gp-row-transformation-notation`)
- Dev jump button → **step 15 op4 row-notation give-answer** (incorrect screen preview)

---

## 2. Chase's desired feel (use his language)

- **Help triggers must be usable with dwell-click.** The whole surface dragging blocked opening help — he could not click the ! to trigger it. Split interaction: drag the text, click the icon.
- **Row transformation notation must not word-wrap mid-expression.** e.g. `-3/2R2 + R1 → R1` should read as one unit, not split across lines. Applies to **all** notation displays, not just give-answer.
- **Give-answer incorrect screen:** show "Incorrect. Here is the correct row transformation." with the notation on its own line, **Next** bottom-right — he wanted to **see what this incorrect screen looks like** specifically (dev jump lands there).
- **Position tuning:** he gives pixel coords from dev readout under triggers (`showCoordinates={import.meta.env.DEV}`). Row-replacement notation help: **294, 133**.
- **No surprise windows** — never launch GUI without asking. Hand him what to run and what to expect.
- **Modals never dismiss on backdrop click.**

---

## 3. Accepted decisions (do not re-litigate)

| Decision | Why |
|---|---|
| **Wrong-answer row-entry reveal Next skips merge animation** | After wrong answer there is no aligned entry row for slide-in merge; apply `matrixAfter` and advance directly (`use-guided-practice-row-entry-reveal.ts`). |
| **`recordRecoveryStep` must be wired through wrong flows** | Next was firing but crashing — root cause was missing pass-through in `use-guided-practice-wrong-flows.ts`. |
| **Help triggers portal to `document.body`, viewport-fixed** | `GuidedPracticeHelpTrigger.tsx` — draggable label, clickable icon. |
| **Row-replacement notation help visible during recovery** | Removed `!session.rowNotationRecovery` guard in solver; `stackBelowInstructionPopover` when recovery active so inline Next stays clickable. |
| **Separate positions for scaling vs replacement notation help** | `ROW_NOTATION_HELP_POSITION` (280, 152) vs `ROW_REPLACEMENT_NOTATION_HELP_POSITION` (294, 133). |
| **Dev jump seeds recovery via `devSessionSeed`** | `GuidedPracticeView` → `GuidedPracticeSolver` → `useGuidedPracticeSession`; bypasses replaying session events for preview. |
| **Label font bumped one step** | `theme.css` + `student-portal/.../guided-practice-fraction-help.css`. |

---

## 4. Rejected directions (do not rediscover)

| Tried / discussed | Why wrong |
|---|---|
| **Whole help trigger surface opens help on click** | Drag and click conflict — dwell cannot reliably open help. |
| **`break-words` on row transformation notation** | Splits mid-notation; Chase wants nowrap unit. |
| **Dev jump to step 8 op2 row-entry** | Replaced — he wanted step 15 give-answer incorrect screen preview. |
| **Row-entry reveal Next via merge/finishCorrectQuestion** | Broken UX after wrong answer; direct advance path is correct. |
| **Assuming Next "doesn't work" without checking console** | It was calling `recordRecoveryStep is not a function` — handler existed, wiring didn't. |

---

## 5. Current implementation state

### Key files (Matrix app)

| Area | File |
|---|---|
| Help trigger click/drag split | `src/app/components/guided-practice/GuidedPracticeHelpTrigger.tsx` |
| Help positions | `src/app/components/guided-practice/fractionHelpButtonPosition.ts` |
| Give-answer UI + notation nowrap | `src/app/components/guided-practice/GuidedPracticeRowNotationRecovery.tsx` |
| Notation nowrap on slots/errors | `BlankSlot.tsx`, `GuidedPracticeOverlay.tsx`, help panels |
| CSS class | `.gp-row-transformation-notation` in `theme.css` + `student-portal/.../guided-practice-fraction-help.css` |
| Row-entry reveal Next (no merge) | `src/app/hooks/use-guided-practice-row-entry-reveal.ts` |
| recordRecoveryStep wiring | `src/app/hooks/use-guided-practice-wrong-flows.ts` |
| Dev seed option | `use-guided-practice-session.ts` → `GuidedPracticeDevSessionSeed` |
| Solver orchestration | `GuidedPracticeSolver.tsx` |

### Key files (student portal)

| Area | File |
|---|---|
| Dev jump button | `GuidedPracticeHomePanel.tsx` — "Dev: jump to step 15 (op4 row-notation give-answer)" |
| Dev seed + workspace open | `GuidedPracticeView.tsx` |
| Types | `src/types/matrix-app.d.ts` |

### Help trigger positions (current)

| Context | Position |
|---|---|
| op2/op4 row-entry fraction help | `{ x: 333, y: 159 }` |
| Row-scaling notation help | `{ x: 280, y: 152 }` |
| Row-replacement notation help | `{ x: 294, y: 133 }` |
| Row-entry scaling reveal help | `{ x: 276, y: 108 }` |
| Row-entry replacement reveal fraction help | `{ x: 301, y: 108 }` |

### Verification already run

- Matrix app guided-practice tests: **57 passed** (`npm test -- --run guided-practice`)
- Session tracking bump logged for this deliverable
- **No commit, no push, no deploy**

### Git state

Both **Matrix app** and **student-portal** have **large uncommitted dirty trees** from this arc (guided + unguided practice, archive plumbing, UX). Do not assume only the files above changed — `git status` before any scoped work.

---

## 6. Open questions and constraints

1. **Chase has not yet confirmed live verification** of dev jump screen, help trigger click/drag, or notation nowrap after hard refresh.
2. **Row-replacement reveal Next** — fixed via `recordRecoveryStep` wiring; needs Chase confirmation after hard refresh (HMR can cause hooks-order warnings — full refresh recommended).
3. **Position tuning may continue** — Chase drags label in dev, reads `{ x, y }`, reports coords.
4. **Separate paused thread:** Practice archive gap analysis handoff existed earlier today (`2026-09-20_practice-archive-gap-analysis.md`) — Chase completing one intentional-mistake session for capture review. **Not active unless Chase switches back to it.**
5. **Frozen:** Calendar 2.0 — do not touch.
6. **Deploy:** only when Chase asks; current work is local dev testing.

---

## 7. Exact next step

**Chase tests the dev jump screen** (`npm run dev` in student-portal → home → "Dev: jump to step 15…" → hard refresh):

1. Give-answer shows **Incorrect** + full notation on **one line** + **Next** bottom-right
2. **Click !** opens row-replacement notation help; **drag label** moves trigger
3. **Next** advances from give-answer

Fresh agent: read his feedback and apply any position/copy/layout tweaks — **do not reopen merge-on-wrong-reveal or whole-surface drag** unless he asks.

---

## Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/AGENTS.md` (if exists) or Matrix app guided-practice components folder
3. `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeView.tsx` (dev jump + seed wiring)
4. `GuidedPracticeHelpTrigger.tsx` + `fractionHelpButtonPosition.ts`

## Dev workflow

```powershell
# student-portal (embeds Matrix app via Vite alias)
cd "C:\Users\chase\Documents\Programs\School Scrips\student-portal"
npm run dev
```

Hard refresh after hook/code changes. Dev coords appear under help triggers in DEV mode.

## Copy-ready context for Chase

If reporting issues, specify: which step/slot, what he clicked, what appeared vs expected, and `{ x, y }` if repositioning a trigger.
