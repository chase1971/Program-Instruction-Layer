# Momentum handoff — Guided practice Q5/Q9 fraction help

**Written:** 2026-09-16 (Wednesday, ~9:50 PM)

---

## 1. Objective and current phase

**Active thread:** Guided practice **fraction help** on Q5 (multiply) and Q9 (add/subtract) in Matrix app embedded in student-portal. Chase drives on **Portal Wide 812×460** landscape phone.

**Phase:** **Done in code**, headless builds pass — **Chase is actively verifying in portal dev**. Latest change: Yes/No prompt **+30% size** and **dimmed workspace backdrop** behind the card (not blur). Chase wanted dim to cut clutter from overlapping UI.

**Do not continue** unless Chase reports failures or asks for next phase (video overlays, Q9 full workspace video, hardcode help positions, Manim polish).

---

## 2. Chase's desired feel

### Viewport / layout (captured this session)
- **Do not squish unrelated UI** when fixing overflow — re-layout first (e.g. skip buttons **side by side**, not stacked)
- **Do not shrink Start/Resume** when adding dev skip buttons — only fix the new control placement
- Recipe: `agent docs/recipes/viewport-budget-layout.md`

### Home screen
- **Skip to question 5** / **Skip to question 9** on home — one horizontal row, original Start/Resume sizing unchanged

### Q5 help trigger
- **Clip-art alert badge** (glossy yellow circle + cartoon `!`) — not plain text in a box
- Draggable via **⋮⋮ grip**; **`pos: x, y`** readout for hardcoding defaults later

### Yes/No prompt (before video)
- **Compact** blue card — not huge padded portal buttons
- **Dimmed background** over workspace so matrix/builder/overlays don't compete visually (Chase chose dim over blur)
- Card ~**30% larger than first compact pass** (current CSS baseline)
- No backdrop dismiss — dwell safety

### Q5 video help
- **Yes** → entire white workspace clears; **full-area video** with Resume
- **No** → close prompt, stay on problem
- Manim MP4 bundled: `Matrix app/src/assets/guided-practice/fraction-times-whole.mp4`

### Q9
- Same help button pattern; add/subtract prompt copy; video still stub / modal — **not** full workspace yet

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| `GUIDED_PRACTICE_Q5_INDEX` / `Q9_INDEX` from catalog | Skip buttons stay aligned with question order |
| `FractionHelpAlertIcon.tsx` inline SVG | Clip-art badge; yellow multiply / blue default |
| Yes/No prompt on **solver root** (`relative` + `absolute inset-0`) | Fixes gray bar when overlay was tied to matrix-row height only |
| Prompt styles in **student-portal** `guided-practice.css` | Portal `matrix-embed.css` 1rem button rule excluded via `.gp-fraction-help-prompt__btn` |
| Dim backdrop `rgba(15, 23, 42, 0.42)` on `.gp-fraction-help-prompt` | Chase: cluttered UI needs visual separation |
| Prompt card sizes ×**1.3** from compact base | Chase request this session |
| Pause snapshot on help open; restore on close | Resume lands on exact Q5 state |
| Hooks before conditional returns in `GuidedPracticeSolver` | Fixed "fewer hooks" crash |

---

## 4. Rejected directions — do not redo

- **Shrinking entire home screen** to fit skip buttons — wrong; only skip placement was the issue
- **Stacked full-width skip buttons** + extra section header — pushed past viewport
- **Tiny 20px Q5/Q9 chips** on home — over-correction
- **Gray `bg-black/40` overlay tied to inner relative div** — showed as horizontal bar, not full workspace
- **Huge shadcn `Button` in prompt** — portal embed blew up to 1rem padded buttons
- **Backdrop click dismiss** on any help modal — dwell rule

---

## 5. Current implementation state (uncommitted)

### Matrix app
| File | Role |
|---|---|
| `GuidedPracticeFractionHelpButton.tsx` | Drag grip + clip-art icon |
| `FractionHelpAlertIcon.tsx` | SVG alert badge |
| `GuidedPracticeFractionHelpPromptModal.tsx` | Yes/No gate (no shadcn Button) |
| `GuidedPracticeFractionHelpPanel.tsx` | Q5 full-workspace video |
| `GuidedPracticeSolver.tsx` | Orchestrates help; prompt on solver root |
| `use-guided-practice-session.ts` | Prompt/confirm/dismiss/close + pause snapshot |
| `fractionHelpTopics.ts` | Q5 MP4 import wired |
| `fractionHelpButtonPosition.ts` | Drag positions + defaults |
| `guided-practice-catalog.ts` | `GUIDED_PRACTICE_Q5_INDEX`, `Q9_INDEX` |
| `src/assets/guided-practice/fraction-times-whole.mp4` | Manim render |

### Student portal
| File | Role |
|---|---|
| `GuidedPracticeHomePanel.tsx` | Start/Resume + side-by-side skip row |
| `GuidedPracticeView.tsx` | Skip handlers, first-paint gate, fraction help nav hide |
| `src/styles/guided-practice.css` | Help trigger, prompt (+30%), video screen, home |
| `src/styles/matrix-embed.css` | Excludes help trigger + prompt buttons from 1rem rule |

### Docs captured
| File | Role |
|---|---|
| `agent docs/recipes/viewport-budget-layout.md` | Measure viewport; re-layout not squish |
| Matrix + student-portal `AGENTS.md` | Keyword rows |
| `agent docs/recipes/INDEX.md` | Index row |

### Verification
- Matrix `npm test -- --run` — 40 passed
- Matrix + student-portal `npm run build` — pass
- **Chase portal dev — in progress** (alert icon, prompt dim/size latest)

---

## 6. Open questions and constraints

- **Do not commit/push** unless Chase asks
- **Do not launch GUI** without asking
- **Calendar 2.0** frozen
- Help button **defaults still placeholders** — Chase drags, reads `pos: x, y`, reports for `fractionHelpButtonPosition.ts`
- **Deferred:** tutorial text over video, example switching, helpful/not helpful, Q9 full-workspace video, Manim further polish
- Macro App / TC preview dirty trees — unrelated; don't touch unless Chase names it

---

## 7. Exact next step (fresh task)

**Chase verifies** after reload:
1. Q5 → alert badge → prompt with **dimmed workspace** and **+30% card** → Yes → video → Resume back to Q5
2. Home skip Q5/Q9 still side-by-side, Start/Resume unchanged size
3. Report: help button position coords, prompt size/dim feel, anything still cluttered

Fix **only what fails**. If positions good → hardcode in `fractionHelpButtonPosition.ts`.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/AGENTS.md`
3. `School Scrips/student-portal/AGENTS.md`
4. `agent docs/recipes/viewport-budget-layout.md` (if layout/sizing)
5. `Matrix app/src/app/components/guided-practice/` — help button, prompt, panel, topics
6. `student-portal/src/styles/guided-practice.css` — prompt dim + sizing owner
