# Momentum handoff — Transformations portal (Identifying Correct overlay)

**Written:** 2026-10-01 (America/Chicago)

---

## Objective and current phase

Chase is polishing **Transformations Homework** in the **student portal** for phone use (landscape, scroll, save errors, result copy, graphing table picker). The active thread at handoff is **Identifying Transformations — keep “✓ Correct!” in the same visual slot on problem 1** when the first badge row and “Click a badge for extra information.” appear. Implementation is done locally; **not deployed yet**.

---

## Chase's desired feel

- **Correct must not jump** when badge hint text appears on the first problem — it looked lower than on every other slide.
- **Do not solve by moving Correct to the side** or under the equation — it should stay **centered under the question** like other slides.
- **Badges and hint can stay in normal flow below the question**; Correct should **float above** (higher z-index) so hint/badge growth **does not push layout**.
- Phone: graphing stage 3 tables were too low / no scroll to Next — fixed in a prior deploy; identifying Correct overlay still needs deploy + phone check.
- End screen: plain **“You got X out of Y correct. You missed N.”** — no “first try” or percent (shipped in last deploy).
- Homework home: **no instructor margin teleports** (shipped).

---

## Accepted decisions

| Decision | Why |
|---|---|
| `CorrectBanner` **`layout="overlay"`** — `absolute`, `top: 100%` of question wrapper, `z-20`, `pointer-events-none`, centered | Removes Correct from document flow; badges/hint below question unchanged |
| Value + specific correct phases with badges: question in `relative` wrapper + overlay Correct + `CompletedBadges` sibling below | Matches original stack order visually without vertical shift |
| Phases without badges (general, letter-id, etc.) keep stacked `CorrectBanner` (default `layout="stack"`) | No overlay needed |
| Reserved hint line min-height in `CompletedBadges` | Kept; overlay is the real fix for Correct position |
| Portal graphing: `graphing-portal-embed__scroll`, table grid `translateY(0)` | Shipped 2026-10-01 deploy |
| Landscape gate at `TransformationsHomeworkEntry`, fullscreen in header, save/start-over fixes | Shipped 2026-10-01 deploy |

---

## Rejected directions (do not redo)

1. **Correct under the general-form equation** (between equation and prompt) — wrong slot for “select all…” general step; reverted.
2. **Correct above or below badges in flow only** — first badge + hint still shifts Correct on problem 1.
3. **Side-by-side row** (`IdentifyingCorrectBadgesRow`) — Correct on opposite side, not same place; **file deleted**.
4. **Only reserved min-height for hint line** — insufficient when badge row first appears.

---

## Current implementation state

### Deployed (production Netlify ~2026-10-01)

- **student-portal** @ `1044148` area: landscape gate, fullscreen, activity header/save UX, result copy, teleports removed, graphing scroll CSS.
- **transformations-app** @ `fb24992`: graphing table position + portal scroll wrapper.

### Uncommitted (transformations-app only)

```
 M panels/SpecificQuestionPanel.tsx
 M panels/ValueQuestionPanel.tsx
 M panels/panelHelpers.tsx   — CorrectBanner stack | overlay
 M shared/CompletedBadges.tsx — optional className, hint min-height
 D shared/IdentifyingCorrectBadgesRow.tsx (deleted)
```

**Key code:** `CorrectBanner` overlay in `transformations-app/src/app/components/IdentifyingTransformations/panels/panelHelpers.tsx`. Used from `ValueQuestionPanel.tsx` (`value-correct`) and `SpecificQuestionPanel.tsx` (sign/magnitude/specific correct with badges).

**student-portal:** clean working tree (overlay lives in embedded transformations-app source via Vite alias).

---

## Open questions / constraints

- **Phone verify** after deploy: problem 1, first value-correct — Correct aligned with later slides; badges clickable under overlay (`pointer-events-none` on Correct).
- If overlay overlaps hint unreadably, adjust offset or subtle shadow — **ask Chase before** moving Correct again.
- **No commit/push/deploy** unless Chase asks (handoff boundary).
- Long session: prefer fresh task for unrelated work.

---

## Read first (next agent)

1. This file.
2. `School Scrips/student-portal/AGENTS.md` — orientation, deploy (`npm run deploy:prod` only when asked).
3. `transformations-app/.../ValueQuestionPanel.tsx`, `panelHelpers.tsx` (`CorrectBanner`).
4. Optional: `IdentifyingTransformationsView.tsx` left column overflow if overlay clips (currently should be fine).

---

## Exact next step

1. **Commit + push** `transformations-app` overlay changes; **deploy** student-portal (`npm run deploy:prod` in `School Scrips/student-portal`) so Chase can test on phone.
2. Handoff test (Chase): Identifying problem 1 → first correct answer → Confirm **✓ Correct!** same vertical position as problem 2+; badge hint can appear without moving Correct; badges still tappable.
3. If still wrong, inspect overlay anchor (`top: 100%` + `mt-1`) vs portal compact CSS — do **not** revert to side-by-side or flow stacking without Chase's OK.
