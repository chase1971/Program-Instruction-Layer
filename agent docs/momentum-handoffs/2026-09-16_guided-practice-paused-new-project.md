# Momentum handoff — guided practice paused; new matrix app work next

**Written:** 2026-09-16 (Wednesday, ~8:10 PM)

---

## 1. Objective and current phase

**Paused thread:** Gauss-Jordan **guided practice** + TC landscape phone preview — substantial uncommitted work, **not fully verified by Chase**, but at a clean stopping point.

**Chase is pivoting** to a **big new project** within the Matrix app / student-portal stack. Do not assume the next task is more guided-practice polish unless Chase says so.

### Where the paused work stands

| Area | Status |
|---|---|
| TC preview bezel (Macro App) | **Done** — Chase verified top/bottom/sides earlier |
| Guided practice engine/UI polish | **Done in code** — headless tests pass; **Chase verify in portal dev still outstanding** |
| Guided practice **home screen** (Start / Resume / Restart) | **Done this session** — equal-width Start + Resume row; build passes |
| Git | **Nothing committed** from this work unless Chase asks |

---

## 2. Chase's desired feel

### TC preview vs real iPhone
- Preview must show **same horizontal space** as phone (notch clearance + right margin)
- **Embedded BrowserView width** must actually change when constants change (Chase measured with ruler)
- Landscape viewport **932×360** (812 chrome + **120px** extra width)
- **Single navy bezel** around app — no double outer ring
- Navy must match portal header: **`#002d5b`** (`--portal-navy`), not `#1e3a5f`
- Frame hairline tuning was pixel-by-pixel: side in, bottom up, inner bezel asymmetric padding

### Guided practice workspace
- **Live digits** in pulsing cell while value builder open; ⌫ live; Next/Enter commits
- Entry cells wide enough for **negative fractions** (e.g. `-1/3`) — no clip
- **Blank cells empty** — no middle dot placeholder
- After correct row entry: **slide entry row left** to replace old row (tutorial Matrix B → A feel)
- **Skip obvious “become 0?” step** after pick-zero in row replacement — go straight to operation type
- Row entry grid must **align vertically** with the row being filled (R2 not top-aligned to R1)
- **Format vs incorrect:** incomplete notation (e.g. `1/3R1→`) → amber format message, **not** “Incorrect.”

### Guided practice home screen (added ~4:54–8:10 PM)
- Title **Gauss-Jordan Method Practice** on **one line** — wider card (`max-width: 26rem`)
- Section label **Guided Practice** (not “Practice Modes”)
- **Start** and **Resume** always visible **side by side, equal width** (`flex: 1 1 0` each)
- **Resume disabled** (greyed) until saved in-progress progress exists
- **Restart** muted text link below when resumable — clears progress and opens from question 1
- **Start** when resumable: clears saved progress and opens fresh (same as restart entering practice)
- Chase drives with dwell — big click targets, no typing-heavy flows

### Database / grading (discussion only — not built)
- Chase wants to record **how many times** a student does a problem (many attempt rows over time)
- **Not a volume concern** at classroom scale — Supabase free tier is 500 MB / millions of rows fine
- Current wiring: in-progress events in jsonb blob; completed run → `attempts` + `attempt_items`
- Pipeline doc: `student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` § costs + “do not size for volume”

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| `STUDENT_PORTAL_PREVIEW_LANDSCAPE_WIDTH_EXTRA_PX = 120` | Chase tuned from 150 → 120 |
| Viewport via CSS vars on holder | Only way to resize Electron BrowserView |
| **No outer box-shadow ring** on TC preview | Double border; single navy bezel only |
| Frame/ring color `#002d5b` | Match `--portal-navy` |
| Shared `MATRIX_CELL_BUTTON_CLASSES`: `w-10 h-9 px-1` | Room for `-1/3`; consistent cells |
| Row merge: check flash → slide → `matrixAfter` → advance | Tutorial step-14 pattern |
| Row refs in **ref not state** | useState in ref callback → infinite loop |
| Replace ops skip `target-value` question | “Obviously zero” after pick-zero |
| `formatMessage` separate from `wrongAttempt` | Format ≠ incorrect answer |
| Home: **Start + Resume always paired, equal size** | Chase: room for Resume next to Start |
| `canResume` from saved index + event count; clears after successful `finish()` | Resume hides after completed submit |
| `useGuidedPracticeAttempt.restart()` | Clears events blob + index 0 via existing save path |

---

## 4. Rejected directions — do not redo

- **Outer 11px box-shadow ring + holder padding** — double border
- **Bottom padding −1 without browser +1px** — 1px empty strip at bottom
- **Row element refs via useState** — maximum update depth crash
- **Smaller font on entry cells** — flex squeeze was clip cause, not font
- **Bezel-only width changes** for BrowserView — doesn't resize embedded view
- **target-value after pick-zero in replace flow** — Chase: irrelevant step
- **`width: 100%` on flex mode buttons** — prevented Start from shrinking; broke paired layout
- **Start full-width until `canResume`** — Chase couldn't see smaller Start; Resume must always occupy its half

---

## 5. Current implementation state (uncommitted)

### Student portal — guided practice home + embed
- `src/features/guided-practice/GuidedPracticeHomePanel.tsx` — Start / Resume / Restart UI
- `src/features/guided-practice/GuidedPracticeView.tsx` — `practiceSessionKey`, start/resume/restart wiring
- `src/features/guided-practice/useGuidedPracticeAttempt.ts` — `canResume`, `restart()`, post-finish reset
- `src/styles/guided-practice.css` — wider card, equal-width button row
- `src/styles/matrix-embed.css`, `portal-compact-layout.css`, `previewNotch.ts` — embed/notch (earlier)

### Matrix app — guided practice engine
- `use-guided-practice-session.ts`, `GuidedPracticeRowMerge.tsx`, `GuidedPracticeSolver.tsx`, etc.
- `question-script.ts` — replace flow omits target-value
- `parse-row-op-expression.ts` — `isIncompleteRowOpExpression`
- `matrixCellButtonClasses.ts`, builder/keypad polish files

### Macro App — TC preview (separate dirty set)
- `teacher-console.css`, `teacher-console-neumorphic.css`, `studentPortalChromeWindow.ts`, tests
- **Also dirty but out of scope:** PreviewTester*, BrowserTabVisibility*, `config/d2l-courses.json`, etc.

### Verification
- Matrix app `npm test -- --run` — **39 passed**
- Student portal `npm run build` — **passes**
- Macro App `studentPortalChromeWindow.test.ts` — **2 passed** (earlier)
- **Chase verify in portal dev / Macro App** — not agent-launched

### Outstanding verify checklist (if GP work resumes)
1. Op 2: pick zero → skips “become 0?” → operation type
2. Incomplete `1/3R1→` → amber format, not Incorrect
3. R2 entry aligns; `-1/3` doesn't clip; blank cells empty
4. Correct row → green check → slide left → matrix updates
5. Home: Start + Resume equal width; Resume disabled until mid-problem save; Restart clears

---

## 6. Open questions and constraints

- **Do not commit/push** unless Chase asks
- **Do not launch GUI** without asking (dwell/voice accessibility)
- **Calendar 2.0** frozen
- **Windows PowerShell** — no `&&`
- Scale ops still have **target-value “become 1?”** — only replace flow skips it
- **Next work is Chase's new project** — scope TBD; read what Chase describes in the fresh task
- Macro App dirty tree mixes TC preview with unrelated PreviewTester work — don't conflate

---

## 7. Exact next step (fresh task)

**Chase describes the new big project** — read this handoff for paused-state context, then **`School Scrips/Matrix app/AGENTS.md`** and **`School Scrips/student-portal/AGENTS.md`** for whichever side the new work touches.

If resuming guided practice instead: Chase verifies the five-item checklist above in portal dev (landscape); fix only what fails.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. Chase's description of the **new project** (primary)
3. `School Scrips/Matrix app/AGENTS.md` — matrix / guided practice / tutorial
4. `School Scrips/student-portal/AGENTS.md` — portal embed, attempts, shipping
5. If TC preview resumes: `School Scrips/Macro App/AGENTS.md`
