# Momentum handoff — TC preview frame + guided practice polish

**Written:** 2026-09-16 (Wednesday, ~4:37 PM)

---

## 1. Objective and current phase

Two threads in one session, both largely **done pending Chase verify**:

**A. Teacher Console landscape phone preview** — frame bezel + color match **done** (Chase verified top/bottom/sides).
**B. Gauss-Jordan guided practice** — cell sizing, row merge animation, flow trim, format feedback **done** (needs Chase verify in portal).

**Phase now:** Chase verification only, or small nudge fixes if preview/animation still off by a pixel.

---

## 2. Chase's desired feel

### TC preview vs real iPhone
- Preview must show **same horizontal space** as phone (notch clearance + right margin)
- **Embedded BrowserView width** must actually change when constants change (Chase measured with ruler)
- Landscape viewport **932×360** (812 chrome + **120px** extra width)
- **Single navy bezel** around app — no double outer ring
- Navy must match portal header: **`#002d5b`** (`--portal-navy`), not `#1e3a5f`
- Frame hairline tuning was pixel-by-pixel: side in, bottom up, inner bezel asymmetric padding

### Guided practice
- **Live digits** in pulsing cell while value builder open; ⌫ live; Next/Enter commits
- Entry cells wide enough for **negative fractions** (e.g. `-1/3`) — no clip
- **Blank cells empty** — no middle dot placeholder
- After correct row entry: **slide entry row left** to replace old row (tutorial Matrix B → A feel)
- **Skip obvious “become 0?” step** after pick-zero in row replacement — go straight to operation type
- Row entry grid must **align vertically** with the row being filled (R2 not top-aligned to R1)
- **Format vs incorrect:** blank/incomplete notation (e.g. `1/3R1→` with nothing after arrow) → amber format message, **not** “Incorrect.” Wrong but complete answers still get Incorrect + hint

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| `STUDENT_PORTAL_PREVIEW_LANDSCAPE_WIDTH_EXTRA_PX = 120` | Chase tuned from 150 → 120 |
| Viewport via `--student-portal-preview-viewport-width/height` on holder | Only way to resize Electron BrowserView |
| **No outer box-shadow ring** — holder padding for ring removed | Chase saw double border; inner padding bezel is the only navy frame |
| Frame outer size = viewport + inset only (no ring) | Matches removed ring |
| Phone-frame asymmetric padding: top +1, left +1, bottom −2 vs inset | Pixel hairline tuning per Chase |
| Browser holder +1px height paired with bottom padding −2 | Bottom gap fix — padding alone made it worse |
| `transform: translate(2px, 0)` on phone-frame | Side nudge after ring removal |
| Frame/ring color `#002d5b` | Match `--portal-navy` |
| Shared `MATRIX_CELL_BUTTON_CLASSES`: `w-10 h-9 px-1` | Negative fraction room; consistent all matrix cells |
| Portal embed `--matrix-cell-width: 2.3125rem`, `--matrix-cell-height: 1.8125rem` | Landscape embed sizing |
| Row merge: check flash → slide → `matrixAfter` → advance | Tutorial step-14 slide pattern |
| Row refs stored in **ref not state** | setState in ref callback caused infinite loop — fixed |
| Replace ops skip `target-value` question | “Obviously zero” after pick-zero |
| `formatMessage` separate from `wrongAttempt` | Format issues ≠ incorrect answer |

---

## 4. Rejected directions — do not redo

- **Outer 11px box-shadow ring + holder padding** — double border; removed entirely
- **Bottom padding −1 without browser +1px** — created 1px empty strip (made bottom worse)
- **Row element refs via useState** — maximum update depth crash
- **Smaller font on entry cells** — flex squeeze was root cause of clip, not font size
- **Bezel-only width changes** for BrowserView — doesn't resize embedded view
- **target-value after pick-zero in replace flow** — Chase: step 7 irrelevant

---

## 5. Current implementation state (uncommitted)

### Macro App — TC preview
- `renderer/src/styles/teacher-console.css` — phone-frame padding, translate, browser +1px height
- `renderer/src/styles/teacher-console-neumorphic.css` — ring removed; drop shadow only; `#002d5b`
- `renderer/src/utils/studentProgress/studentPortalChromeWindow.ts` — frame calc without ring
- `renderer/src/utils/studentProgress/studentPortalChromeWindow.test.ts` — viewport/frame tests
- `renderer/src/components/teacher-console/TeacherConsolePortalPreviewEmbed.tsx` — phone-frame wrapper

### Student portal — embed/layout
- `src/styles/matrix-embed.css` — cell width/height vars, `.matrix-cell-button` selectors
- `src/styles/portal-compact-layout.css` — TC preview notch inset (earlier session)

### Matrix app — guided practice
- `src/app/components/shared/matrixCellButtonClasses.ts` — shared cell sizing
- `src/app/components/builders/MatrixEntryGrid.tsx` — live preview, readOnly, no dot, shared classes
- `src/app/components/guided-practice/GuidedPracticeRowMerge.tsx` — slide animation (new)
- `src/app/components/guided-practice/GuidedPracticeSolver.tsx` — merge wiring, row align marginTop
- `src/app/components/guided-practice/GuidedPracticeMatrixDisplay.tsx` — mergingRowIndex fade, row refs
- `src/app/components/guided-practice/GuidedPracticeOverlay.tsx` — formatMessage display
- `src/app/hooks/use-guided-practice-session.ts` — merge state, format vs wrong, skip target-value path
- `src/app/engine/question-script.ts` — removed target-value from replace questions
- `src/app/components/builders/parse-row-op-expression.ts` — `isIncompleteRowOpExpression`
- `src/app/constants/animation-timing.ts` — `ROW_MERGE_SLIDE_DURATION_S`
- Matrix solvers updated to `MATRIX_CELL_BUTTON_CLASSES`

### Verification
- Matrix app `npm test -- --run` — **39 passed** (last run this session)
- Macro App `studentPortalChromeWindow.test.ts` — **2 passed** (earlier)
- TC frame + guided practice — **Chase verify in Macro App / portal dev**, not agent-launched GUI

---

## 6. Open questions and constraints

- **Do not commit/push** unless Chase asks
- **Do not launch GUI** without asking (dwell/voice accessibility)
- **Calendar 2.0** frozen — do not touch
- **Windows PowerShell** — no `&&`
- Scale operations still have **target-value “become 1?”** — only replace flow skips it; ask before removing scale step too
- Row merge uses **measured getBoundingClientRect** — if embed CSS changes cell height, re-check R2 alignment + slide landing
- Macro App has **other dirty files** (PreviewTester, BrowserTabVisibility, etc.) from parallel work — don't conflate with this handoff's scope

---

## 7. Exact next step (one concrete action)

Chase verifies in portal guided practice (landscape):

1. Op 2 flow: pick zero → **skips** “become 0?” → operation type (step numbers shifted)
2. Row notation: submit `1/3R1→` incomplete → **amber format message**, not Incorrect
3. Row entry for **R2**: entry grid **lines up with row 2**; `-1/3` doesn't clip; blanks have **no dot**
4. Correct row submit → **green check → slide left → matrix updates**

If anything fails, fix the specific item — do not redo Gauss-Jordan builder/keypad work unless Chase asks.

For TC preview: restart Macro App, confirm bezel still single-navy and bottom sealed after rebuild.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/AGENTS.md` — guided practice / matrix work
3. `School Scrips/student-portal/AGENTS.md` — portal embed / notch if touching layout
4. `School Scrips/Macro App/AGENTS.md` — TC preview if frame work resumes
5. Key files:
   - `Matrix app/.../use-guided-practice-session.ts`
   - `Matrix app/.../GuidedPracticeRowMerge.tsx`
   - `Macro App/renderer/src/styles/teacher-console.css`
   - `student-portal/src/styles/matrix-embed.css`
