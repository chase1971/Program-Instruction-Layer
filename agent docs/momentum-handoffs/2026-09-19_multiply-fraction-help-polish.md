# Momentum handoff — Multiply fraction help polish (Q5 tutorial)

**Written:** 2026-09-19 (Saturday, ~12:28 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **guided practice** in the student portal — **Q5 multiply
fraction help** tutorial (segmented video, EX1/EX2/EX3, intro screen, layout). Secondary
touch this session: **Q9 pick-cell prompt** text, home-panel **skip-to-help** shortcuts.

**Phase:** Multiply tutorial is **working end-to-end locally** — intro, per-example steps,
centered layout, skip buttons open tutorial directly, EX1/EX2 flows verified by Chase.
**EX3 segment start time is still being tuned** against the **old 6-example MP4** (estimated
timestamps); Chase last said EX3 needs to go forward a little more — currently **44.8s** but
may still show tail of previous clip.

**Exact next step:** Live-check EX3 on device after refresh; nudge `fractionHelpTutorialConfigs.ts`
EX3 hold/play start (try **45.0–46.0s**) OR re-render Manim + copy new MP4 for exact marks.

---

## 2. Chase's desired feel

- **Intro screen:** "Examples **1** and **2**… Example **3**…" (numerals, not words). Pick
  EX1/EX2/EX3 to enter that example — no auto-play through all three.
- **No Back button** on intro or first step of an example (nothing to go back to).
- **Always "Next"** (never "Start"). **Replay** lives **inside the instruction box** with Back.
- **EX buttons + video centered** on the full workspace (instruction left and Resume right
  float as overlays — do not push center column right).
- **Video slightly zoomed** (`scale(1.2)`, column `min(54%, 28rem)`).
- **One clip per Manim set** (not three 1/3 examples):
  - EX1: ⅓ × 15
  - EX2: ⅖ × 14 (cancel 14 & 7 first, then multiply new numbers)
  - EX3: ⅖ × ⅜ (fraction × fraction)
- **EX2 pedagogy:** rewrite → "Simplify the 14 and 7 first." → **pause on 2/1 × 2/1** →
  "Multiply the top two **new** numbers…" → play through **= 4**, then stop **before** next
  problem appears.
- **Home panel:** "Skip to multiply help" / "Skip to add/subtract help" → **straight into
  tutorial** (no Yes/No prompt).
- **Q9 prompt:** "Click or tap where the one needs to go." (not "Column two:…")

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| `useSegmentedHelpAnimation` uses **per-example** steps + optional **intro phase** | Independent EX1/2/3; no linear auto-advance through all examples |
| **Hold frames** (`segment.start === segment.end`) before each motion; Next on hold plays next segment | Problem visible before caption animation; fixes off-by-one |
| EX2 has **6 steps** (rewrite, simplify+cancel, multiply) vs EX1 **3 steps** | Cancel-first pedagogy for 2/7 × 14 |
| EX2/EX3 times point into **later half of existing 50s MP4** (6-example render) | Until new 3-example MP4 copied to assets |
| Manim `construct()` trimmed to **3 examples** + `example_*_cancelled` mark after pull_cancel | Future re-render syncs marks json |
| `initialFractionHelpTopic` on `useGuidedPracticeSession` + `GuidedPracticeView` skip handlers | Skip buttons bypass prompt modal |
| Stage layout: video column `position:absolute; left:50%; transform:translate(-50%,-50%)` | True center; side panels don't offset math |
| `question-script.ts` + `matrixSlotCatalog.ts` Q9 prompt updated | Chase wording for column-two pick-cell |

---

## 4. Rejected directions — do not redo

- **Full-width EX picker row** spanning instruction+video+resume columns — pushed examples right; reverted to center overlay on video column.
- **`transform: scale(1.25)` without fixed layout** — caused visible jump when controls appeared; zoom kept but with stable overlay layout.
- **Replay under video** — hidden; moved into instruction box.
- **"Start" button label** — Chase wants Next everywhere.
- **Sequential auto-advance** from EX1 → EX2 → EX3 after finishing an example — replaced by explicit Next-to-example-N copy + jump.
- **Using second/third 1/3 clips** (1/3×4, 1/3×22) for EX2/EX3 — Chase wanted one clip per set.

---

## 5. Current implementation state

### Matrix app — **dirty, not committed**

| File | Role |
|---|---|
| `fractionHelpTutorialConfigs.ts` | MULTIPLY intro, EX1/2/3 steps & segment times |
| `useSegmentedHelpAnimation.ts` | Intro/tutorial phases, hold/play, showBack, example-complete → next EX |
| `GuidedPracticeFractionHelpPanel.tsx` | Layout, Replay in instruction box |
| `GuidedPracticeSolver.tsx` | `initialFractionHelpTopic` prop |
| `use-guided-practice-session.ts` | Auto-open help on load when skip |
| `question-script.ts` | Q9 prompt text |
| `fractionHelpTutorialConfigs.test.ts` | 12 tests pass |

### Student portal — **dirty, not committed**

| File | Role |
|---|---|
| `GuidedPracticeView.tsx` | Skip → `openPractice(index, topic)` |
| `guided-practice-fraction-help.css` | Centered overlay, zoom |
| `matrix-app.d.ts` | `initialFractionHelpTopic` typing |

### Macro App — **dirty** (Q9 prompt only in catalog)

`renderer/src/utils/matrixReport/matrixSlotCatalog.ts` — same Q9 prompt as engine.

### Manim Trial — **dirty**

`fraction_times_whole.py` — 3 examples (1/3×15, 2/7×14, 2/7×3/8), `_cancelled` mark.

**Asset NOT updated:** `Matrix app/src/assets/guided-practice/fraction-times-whole.mp4` is still
the **old ~50s / 6-example** render. `fraction_times_whole_marks.json` on disk still reflects
old marks (only example_one/two/three as 1/3 family).

### Current EX segment times (estimated for old MP4)

| Example | Key timestamps |
|---|---|
| EX1 | hold 1.17, rewrite 1.17–3.21, products 3.21–7.33 |
| EX2 | hold 23.67, rewrite … 25.71, cancel 25.71–**27.95**, multiply 27.95–**31.6** |
| EX3 | hold/play **44.8**–49.5 |

### Verification

- `npm test -- --run fractionHelpTutorialConfigs` — pass (Matrix app)
- `npm test -- --run guided-practice-engine` — pass
- Chase live-verified: intro flow, centering, skip buttons, EX1, EX2 simplify pause (after
  several timing nudges). **EX3 start still open.**

---

## 6. Open questions and constraints

- **EX3 start:** May need +0.2–1.0s more (45.0–46.0) on current MP4 — Chase said "still not
  showing" then "push forward a little" → landed at 44.8; confirm on device.
- **Permanent fix:** Re-render Manim (`fraction_times_whole.py`), copy MP4 to Matrix assets,
  paste new marks into `fractionHelpTutorialConfigs.ts` for all three examples.
- **Add/subtract help (Q9):** Not reworked this session beyond existing stepped config; separate pass if needed.
- **No commit/push/deploy** unless Chase asks — all dirty.
- **Never launch GUI / portal deploy** without asking (AGENTS.md).
- Read `School Scrips/Matrix app/AGENTS.md` for viewport budget + step numbering (UI step 9 = `step === 8`).

---

## 7. Exact next step

1. Refresh portal, click **Skip to multiply help** → **EX3**.
2. If still wrong frame, bump EX3 `holdFrame` + segment `start` in
   `fractionHelpTutorialConfigs.ts` (small increments, 0.3–0.5s).
3. When Chase is ready: re-render Manim on work machine, replace MP4, sync all segment times
   from new `fraction_times_whole_marks.json`.

---

## Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/AGENTS.md`
3. `School Scrips/Matrix app/src/app/components/guided-practice/fractionHelpTutorialConfigs.ts`
4. `School Scrips/student-portal/src/styles/guided-practice-fraction-help.css`
5. `Manim Trial/fraction_times_whole.py` + `fraction_times_whole_marks.json`

Prior related handoff: `2026-09-18_guided-practice-polish-deploy.md` (Q9 add/subtract, trigger position — partially superseded for multiply flow).
