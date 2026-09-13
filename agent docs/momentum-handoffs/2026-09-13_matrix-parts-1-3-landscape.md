# Momentum handoff: Matrix tutorial Parts 1–3 landscape + Part 3 copy tweak

**Written 2026-09-13.** Day-valid only. If you are reading this on a later date, say so before acting.

**Slug:** `2026-09-13_matrix-parts-1-3-landscape`

---

## Read first

1. **`School Scrips/student-portal/src/styles/matrix-embed.css`** — portal-only landscape tuning for Parts 1–3 (cell size, inset, brackets, row-op top, popover lift, side animations).
2. **`School Scrips/student-portal/src/features/matrix-tutorial/MatrixTutorialView.tsx`** — `matrix-tutorial-part1-inset` (when `!atHome`), `part2-inset`, `part3-inset` wrappers.
3. **`School Scrips/Matrix app/src/app/components/matrix-tutorial-overlay-part-3.tsx`** — step 4 prompt text; step 3 plain text input (fraction template reverted).
4. **`School Scrips/Macro App/renderer/src/utils/studentProgress/studentPortalChromeWindow.ts`** — landscape preview 812×360.
5. **`agent docs/momentum-handoffs/2026-09-13_tester-codes-roster-cleanup.md`** — roster/tester codes deploy from earlier today.

**Stale handoff warning:** `2026-09-12_portal-review-2` (Matrix 033 save bug, anon RPC) is separate backlog — do not conflate unless Chase asks.

---

## Objective and current phase

### A. Tester codes roster cleanup — **deploy done, UI not verified by Chase**

Migration 036 pushed, M1314 codes regenerated, `sync-portal-rosters` run. Chase has **not** smoke-tested Teacher Console → Roster.

### B. Matrix tutorial landscape fit — **Parts 1–3 tuned; phone verify ongoing**

Chase's phone in landscape loses ~100px to the browser URL bar. Goal: **avoid fullscreen** by tightening layout so tutorial steps fit with URL bar visible. Teacher Console landscape preview shortened to simulate that.

**Phase now:** Part 1 approved through iterative tuning. Chase asked to **roll the same patterns to Parts 2 & 3** — done in portal CSS + Matrix app side-animation classes. Chase was actively pixel-checking Part 3 on phone preview when this handoff was requested. **Not deployed to Netlify yet.**

---

## Chase's desired feel (use his language)

- **No fullscreen if possible** — shrink/tighten so matrix + instruction bubble fit in real phone landscape with URL bar visible.
- Teacher Console **landscape preview should match his phone** — shortened by **100px** (simulates URL bar).
- **Notch on iPhone landscape** — content shifts **right ~20px**; nav **1/2/3 · Back · Next · Exit stays put**.
- Matrix numbers **a little smaller**; brackets must **end at the bottom row** — not hang below shrunken cells.
- Row-op buttons and notation **tucked up** under the matrix.
- Side animations (addition, multiply-then-add) should **not collide** with the instruction bubble — shrink/offset via portal CSS.
- **Live Netlify ≠ local dev** — production won't show portal CSS until deploy.
- Step prompts should name the operation explicitly — e.g. step 4: **"What's the proper notation for row scaling?"** not generic "row transformation that does this."
- **Fraction template input (MyLab-style a/b button) is too annoying on phone** — do not reintroduce without explicit ask.

---

## Accepted decisions

| Decision | Why |
|---|---|
| Portal-only CSS in `matrix-embed.css` | Matrix app stays standalone; portal owns embed overrides |
| Shared inset classes `part1-inset` / `part2-inset` / `part3-inset` | Same cell size, transform, bracket, row-op, popover rules |
| Inset `translate(20px, 1px)` | Clears notch; final Part 1 tuning (+3px down from -2px trial) |
| `--matrix-cell-size: 1.6875rem` | Modest shrink for landscape fit |
| Bracket height tracks two-row matrix | Fixed hanging brackets via divider/cell height + `matrix-result-matrix` class |
| Side animations: `matrix-portal-side-animation` class + portal CSS offsets | Part 2 step 5: `left +190px`; Part 3 step 5: `+170px`; Part 3 step 9: `+190px`; all `top: -28px`, `scale(0.88)` |
| Part 2 step 1: only `-2` pulses; pivot `1` gets static `green-done` | Less visual noise |
| Landscape preview **812×360** | Matches Chase's URL bar loss |
| Step 4 Part 3 copy: **"What's the proper notation for row scaling?"** | Chase correction mid-session |
| Fullscreen API deferred | CSS layout tuning first |

---

## Rejected directions (do not redo)

- **MyLab-style fraction template button on Part 3 step 3** — Chase tried it, said too annoying on phone; **fully reverted** (deleted component + util; plain text field restored, popover width back to 340px, original height).
- **Fullscreen as first move** — deferred.
- **Moving 1/2/3 nav with the matrix** — rejected; only workspace shifts.
- **Applying inset to home screen (`atHome`)** — rejected.

---

## Current implementation state

### Portal landscape (student-portal — **committed** in `269b887`)

| File | What |
|---|---|
| `src/styles/matrix-embed.css` | Parts 1–3 shared inset, cell/bracket/row-op/popover/side-animation rules |
| `src/features/matrix-tutorial/MatrixTutorialView.tsx` | `part1-inset` / `part2-inset` / `part3-inset` wrappers |

**Key CSS values:**
- Transform: `translate(20px, 1px)`
- Cell: `1.6875rem`, font `0.9375rem`
- Row-op top: computed via `--matrix-row-op-top`
- Popover lift: `--matrix-popover-lift` (aligned to row-op cluster)

### Matrix app (Part 2/3 app-side — **committed** in `b9e41cd`; Part 3 overlay — **uncommitted**)

| File | Status |
|---|---|
| `matrix-solver-part-2.tsx`, `use-matrix-tutorial-part-2.ts` | Side animation class, green-done pivot — committed |
| `matrix-solver-part-3.tsx`, `matrix-solver.tsx` | Side animation, result matrix class — committed |
| `matrix-tutorial-overlay-part-3.tsx` | **Uncommitted:** fraction template reverted + step 4 copy fix |
| `tutorial-fraction-answer-controls.tsx`, `fraction-answer.ts` | **Deleted locally, uncommitted** (were briefly committed in b9e41cd) |

**Part 3 step 4 prompt (uncommitted):** `What's the proper notation for row scaling?`

### Roster cleanup

Migration 036 + codes regen + sync — done. Teacher Console Roster UI verify — **not done by Chase**.

### Verification

- `npm run build` in student-portal — passes (after fraction revert).
- Portal CSS: local dev only; **not on Netlify**.
- Chase was visually checking Part 3 on phone preview when handoff requested — no final sign-off recorded.

### Git (do not push unless Chase asks)

- **`Matrix app`** — dirty: Part 3 fraction revert + step 4 copy (reverts files that exist in HEAD commit).
- **`Macro App`** — only `config/d2l-courses.json` (machine-local, silent skip).
- **`student-portal`** — clean at HEAD.

---

## Open questions and constraints

1. **Deploy portal to Netlify** — only when Chase asks (`npm run deploy:prod` in student-portal).
2. **Matrix app uncommitted revert** — HEAD still has fraction template files; working tree removes them. Next agent should commit Matrix app when Chase says "put on GitHub" (or include in that pass).
3. **Roster UI smoke test** — outstanding; needs Macro App launch (ask first per AGENTS.md).
4. **Part 3 phone verify** — Chase may have more pixel nudges after reload.
5. Never commit `.env`, credentials, or `config/d2l-courses.json`.
6. `portal-review-2` backlog remains separate.

---

## Exact next step

1. **Matrix app:** ensure working tree is correct (fraction template gone, step 4 says "row scaling") — reload local dev, Part 3 step 3 = plain input, step 4 = new copy.
2. Chase continues **Part 3 landscape phone check** — report any clip/collision on specific steps.
3. If approved → **`npm run deploy:prod`** in student-portal when Chase asks.
4. Separately: Chase smoke-tests **Teacher Console → Roster** (see `2026-09-13_tester-codes-roster-cleanup.md`).

If a step still clips, nudge in `matrix-embed.css` — do not touch Matrix app unless portal CSS cannot reach the element.
