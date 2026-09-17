# Momentum handoff — Q5/Q9 fraction help + row-entry polish

**Written:** 2026-09-16 (Wednesday, ~8:54 PM)

---

## 1. Objective and current phase

**Active thread:** Guided practice **row-entry polish** in Matrix app (embedded in student-portal) — Submit row gating, row-notation commit validation, and **Q5 + Q9 draggable fraction-help buttons** with pause overlays (animation stubs).

**Phase:** **Done in code**, headless tests pass — **Chase has not verified in portal dev**. Help button default positions are placeholders; Chase tunes via drag + on-screen `pos: x, y` readout.

**Parallel thread (same day, separate):** Manim `fraction_times_whole.py` for multiply-fractions teaching clip — intended to feed **Q5 help video** when approved. See archive `2026-09-16_manim-fraction-times-whole.md`. Chase has that file open; do not conflate Manim edits with Matrix app unless wiring the MP4.

**Older paused work (still uncommitted, mixed dirty trees):** TC landscape preview bezel (Macro App), guided practice engine/home polish (Start/Resume/Restart), row merge animation, builder keypad — from earlier today. Do not assume next task is more of that unless Chase says resume.

---

## 2. Chase's desired feel

### Row entry (Q5 badge 5, Q9 badge 9)
- **Submit row grayed** until all three cells have committed values — no clickable-looking button on empty/partial rows
- Invalid keypad input (e.g. `/` alone, nonsense) → amber *"Enter a valid number or fraction."* on Next/Enter — not "Incorrect."
- **Help buttons** under the entry row area, visually separated from the value builder/calculator to the right
- **Q5:** "Do you need help with multiplying fractions?"
- **Q9:** "Do you need help with adding or subtracting fractions?"
- Click help → **pause problem** (draft preserved), show overlay with explanation + animation area; **Resume problem** returns to same row with keypad restored
- Help button is **draggable** — **⋮⋮ grip** moves it; label click opens help. On-screen **`pos: x, y`** so Chase can report final coords without DevTools
- No backdrop dismiss on help overlay — Resume only (dwell safety)

### Row transformation (Q4, Q8)
- Invalid notation rejected on **builder Enter/commit**, not only on Submit — same amber messages as submit (incomplete vs invalid form)

### Fraction animations (when ready)
- Q5 multiply help expects a Manim-style clip (Chase building `fraction_times_whole.py`) — cancel-first pedagogy, not chained products
- Q9 add/subtract help — animation TBD; stub shows *"Animation coming soon"*

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| `canSubmitMatrixRow` = every `matrixDraft` cell non-null | Gray Submit until all three committed |
| Shared `validateRowOpDraft()` in `parse-row-op-expression.ts` | Same messages for row-notation commit + submit |
| Reusable `GuidedPracticeFractionHelpPanel` + topic config | One overlay; multiply vs add-subtract content |
| `FractionHelpTopic = 'multiply' \| 'add-subtract'` keyed by slot | `op1-row-entry` → Q5, `op2-row-entry` → Q9 |
| Draggable help via tutorial drag pattern (grip mousedown) | Chase tunes placement; separate from help click |
| `localStorage` keys `gp-fraction-help-pos-{slot}` + defaults file | Persists across refresh until hardcoded |
| Default positions in `fractionHelpButtonPosition.ts` | `{ x: 280, y: 120 }` Q5, `{ x: 280, y: 168 }` Q9 — placeholders |
| `FRACTION_*_HELP_VIDEO_SRC = null` until MP4 wired | Stub UI ready |
| `closeFractionHelp` reopens value builder on row-entry | Seamless resume after help |
| Help button absolutely positioned in solver workspace | Does not shift entry grid or builder |

---

## 4. Rejected directions — do not redo

- **Submit row always enabled** with format message only on click — Chase wanted grayed until complete
- **Row-notation commit saves garbage to slot** without validation — fixed; do not revert
- **Help button in MatrixEntryGrid column** — floats absolute so drag doesn't shift layout
- **Backdrop click to close help** — modal/dwell rule
- **Single help position for Q5 and Q9** — separate slots; Q9 aligns to R2

(Carry forward from earlier paused thread — still valid if that work resumes: outer TC box-shadow ring, row refs via useState, Start full-width hiding Resume, etc. — see `2026-09-16_guided-practice-paused-new-project.md`.)

---

## 5. Current implementation state (uncommitted)

### Matrix app — this session (new/edited)
| File | Role |
|---|---|
| `use-guided-practice-session.ts` | `canSubmitMatrixRow`, `fractionHelpTopic`, open/close help, row-notation commit validation |
| `GuidedPracticeOverlay.tsx` | Submit row `disabled={!canSubmitMatrixRow}` |
| `GuidedPracticeSolver.tsx` | Mount draggable help buttons + help panel |
| **New** `GuidedPracticeFractionHelpButton.tsx` | Drag grip, label, `pos: x, y` readout, localStorage save |
| **New** `GuidedPracticeFractionHelpPanel.tsx` | Pause overlay, video stub, Resume |
| **New** `fractionHelpTopics.ts` | Labels, copy, `videoSrc` constants (null) |
| **New** `fractionHelpButtonPosition.ts` | Default coords + load/save |
| `parse-row-op-expression.ts` | `validateRowOpDraft()` |
| `parse-row-op-expression.test.ts` | +1 test for validation helper |

### Matrix app — earlier paused GP polish (same dirty tree)
Row merge, builder polish, question-script skip target-value, matrix cell classes, etc. — see Matrix `git status`; not verified by Chase as a bundle.

### Student portal — dirty (embed/notch/home, not this session's Matrix-only files)
`GuidedPracticeHomePanel.tsx`, `GuidedPracticeView.tsx`, `useGuidedPracticeAttempt.ts`, CSS embed/notch — consumes Matrix bundle at dev time.

### Manim Trial — parallel (for Q5 video when ready)
`fraction_times_whole.py` (~227 lines), rendered MP4, scratch HTML — see `2026-09-16_manim-fraction-times-whole.md`.

### Verification (this session)
- Matrix app `npm test -- --run` — **40 passed**
- Matrix app `npm run build` — pass
- Student portal `npm run build` — pass
- **Chase portal dev verify — NOT DONE**

---

## 6. Open questions and constraints

- **Do not commit/push** unless Chase asks
- **Do not launch GUI** (portal dev, Manim preview, browser) without asking
- **Calendar 2.0** frozen
- **Windows PowerShell** — no `&&`
- Help button **default coords are guesses** — Chase should drag on Q5 and Q9, read `pos: x, y`, report for hardcoding in `fractionHelpButtonPosition.ts`
- When Manim clip approved: set `FRACTION_MULTIPLY_HELP_VIDEO_SRC` in `fractionHelpTopics.ts` to public asset path; Q9 animation still TBD
- Macro App dirty tree may include unrelated PreviewTester work — don't conflate with GP

---

## 7. Exact next step (fresh task)

**Chase verifies in portal dev** (when he chooses to open it):
1. Q5: Submit row gray until 3 cells; multiply help opens/closes with draft intact; drag help button, note `pos: x, y`
2. Q9: add/subtract help same; separate position
3. Q4/Q8: invalid row notation rejected on builder Enter

Fix only what fails. If positions are good, Chase reports coords → agent updates `fractionHelpButtonPosition.ts` defaults.

**Optional follow-up:** Wire approved Manim MP4 into Q5 help panel.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/AGENTS.md`
3. `School Scrips/student-portal/AGENTS.md` (if verifying portal embed)
4. New files under `Matrix app/src/app/components/guided-practice/` — help button, panel, topics, positions
5. If wiring video: `Manim Trial/fraction_times_whole.py` + archive `2026-09-16_manim-fraction-times-whole.md`
6. If resuming older GP polish: archive `2026-09-16_guided-practice-paused-new-project.md`
