# Momentum handoff: Matrix Part 1 landscape tuning + roster deploy done

**Written 2026-09-13.** Day-valid only. If you are reading this on a later date, say so before acting.

**Slug:** `2026-09-13_matrix-part1-landscape-tuning`

---

## Read first

1. **`School Scrips/student-portal/src/styles/matrix-embed.css`** — all Part 1 portal-only layout tuning lives here.
2. **`School Scrips/student-portal/src/features/matrix-tutorial/MatrixTutorialView.tsx`** — `matrix-tutorial-part1-inset` wrapper (when `!atHome`).
3. **`School Scrips/Macro App/renderer/src/utils/studentProgress/studentPortalChromeWindow.ts`** — landscape preview 812×360.
4. **`School Scrips/Macro App/renderer/src/styles/teacher-console.css`** — landscape notch indicator on preview frame.
5. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — deploy rules; portal CSS needs `npm run deploy:prod` for live Netlify.
6. **`agent docs/momentum-handoffs/2026-09-13_tester-codes-roster-cleanup.md`** — roster/tester codes work from earlier today (deploy steps completed).

**Stale handoff warning:** `2026-09-12_portal-review-2` (Matrix 033 save bug, anon RPC) is separate backlog — do not conflate unless Chase asks.

---

## Objective and current phase

Two threads in one session:

### A. Tester codes roster cleanup — **deploy done, UI not verified by Chase**

Migration 036 pushed, M1314 codes regenerated (SPARE-3/4/5 universal), `sync-portal-rosters` run for M1314 + M1324. Macro App roster UI code is implemented but **uncommitted**; Chase has **not** smoke-tested Teacher Console → Roster.

### B. Matrix tutorial landscape fit — **Part 1 only, tuned in portal CSS, not on live yet**

Chase's phone in landscape loses ~100px to the browser URL bar. Goal: **avoid fullscreen** by tightening layout so Part 1 tutorial fits. Teacher Console landscape preview was shortened to simulate that. Part 1 tutorial steps got notch-aware inset + smaller matrix + bracket fix.

**Phase now:** Chase was iterating on Part 1 pixel tuning via **local dev preview** (live Netlify does not show portal CSS until deploy). Part 1 looks close; **Parts 2/3 not yet given the same treatment**. Fullscreen API was discussed and **deferred** — CSS focus mode + layout tuning preferred.

---

## Chase's desired feel (use his language)

- **No fullscreen if possible** — shrink/tighten layout so matrix + instruction bubble fit in real phone landscape with URL bar visible.
- Teacher Console **landscape preview should match his phone** — shortened by **100px** total (simulates URL bar eating bottom content).
- **Notch on iPhone landscape** — content shifts **right ~20px**; nav **1/2/3 · Back · Next · Exit stays put**.
- **First panel = Part 1 tutorial steps** after starting tutorial (`!atHome`), not the home screen with Start Tutorial.
- Matrix numbers **a little smaller**; brackets must **end at the bottom row** — not hang below shrunken cells.
- Row Swap / Row Scaling / Row Replacement controls and their notation **tucked up** under the matrix.
- If Part 1 works on **his slightly narrower phone**, it works for everyone else's.
- **Live Netlify ≠ local dev** — Chase hit "nothing changed" once because he was on production, not dev.

---

## Accepted decisions

| Decision | Why |
|---|---|
| Portal-only CSS in `matrix-embed.css`, not Matrix app repo changes | Matrix app stays standalone; portal owns embed overrides |
| `matrix-tutorial-part1-inset` wrapper in `MatrixTutorialView` when `!atHome` | Shifts matrix + popovers + animations; nav stays absolute at top-left |
| Inset `translate(20px, -2px)` after iterative tuning (-20 → -10 → -5 → -2) | Clears notch without crowding nav |
| `--matrix-cell-size: 1.6875rem` (~27px, down from 32px) | Modest shrink for landscape fit |
| Divider height = cell height (was hanging brackets) | Row height was set by `h-12` divider, not cells |
| Bracket SVG `max-height: calc(cell * 2 + 0.25rem)` | Brackets track two-row matrix |
| Row-op buttons `top: 107px` (was 112px) | 5px up after cell shrink |
| Landscape preview **812×360** (`STUDENT_PORTAL_PREVIEW_LANDSCAPE_URL_BAR_PX = 100`) | Matches Chase's phone URL bar loss |
| Dark notch pill on left edge of landscape preview frame | Visual aid while tuning in Teacher Console |
| Migration 036 + codes regen + roster sync | Completed earlier this session |
| Fullscreen API deferred | CSS layout tuning first; iPhone Safari limits true fullscreen |

---

## Rejected directions (do not redo)

- **Fullscreen as first move** — deferred; layout tightening preferred.
- **Moving 1/2/3 nav with the matrix** — rejected; only workspace shifts.
- **Applying inset to home screen (`atHome`)** — rejected; tutorial steps only.
- **Transform on wrapper when Chase was on live Netlify** — looked like "nothing changed"; not a layout-frame bug, was deploy gap.
- **Rolling Part 2/3 inset before Chase approves Part 1** — explicitly paused.

---

## Current implementation state

### Matrix Part 1 landscape (student-portal, uncommitted)

| File | What |
|---|---|
| `student-portal/src/styles/matrix-embed.css` | `--matrix-cell-size`, inset transform, cell/divider/bracket/row-op/notation rules |
| `student-portal/src/styles/index.css` | Nav-to-matrix spacing (`matrix-embed--with-nav` padding-top 1.65rem; `.p-8` top 0.15rem) |
| `student-portal/src/features/matrix-tutorial/MatrixTutorialView.tsx` | `matrix-tutorial-part1-inset` div when `!atHome` |

**Part 1 inset values (current):**
- Transform: `translate(20px, -2px)`
- Cell: 1.6875rem, font 0.9375rem
- Row-op cluster: top 107px
- Notation padding-top override: 5px

### Teacher Console preview (Macro App, uncommitted)

| File | What |
|---|---|
| `Macro App/.../studentPortalChromeWindow.ts` | Landscape preview height 460 − 100 = **360px** |
| `Macro App/renderer/src/styles/teacher-console.css` | Left-edge notch indicator on `--landscape` holder |

### Roster cleanup (completed deploy, uncommitted code)

| Step | Status |
|---|---|
| Migration 036 pushed | Done |
| M1314 `student-portal-codes.json` regen | Done — SPARE-3/4/5 match M1324 (`WTNWHG`, `QG6WR7`, `9BCSUL`) |
| `sync-portal-rosters` | Done — both courses OK |
| Teacher Console Roster UI verify | **Not done by Chase** |

### Verification

- Portal CSS: tuned in local dev; **not deployed to Netlify**.
- Macro App preview height/notch: reload Macro App to see.
- Roster UI: handoff test statement was given; Chase has not confirmed.

### Git (uncommitted — do not push unless Chase asks)

- `School Scrips/student-portal` — matrix-embed.css, index.css, MatrixTutorialView.tsx
- `School Scrips/Macro App` — tester roster files + preview chrome + teacher-console.css + earlier session dirty files
- `School Scrips/student-session-kit` — migration 036 (already pushed to Supabase)
- Programs root — agent docs, session logs

---

## Open questions and constraints

1. **Deploy portal to Netlify** before Chase can verify Part 1 tuning on live / on phone via production URL — only when he asks (`npm run deploy:prod`).
2. **Roll Part 1 CSS patterns to Parts 2 and 3** — waiting on Chase approval after Part 1 phone check.
3. **Roster UI smoke test** — still outstanding; needs Macro App launch (ask first per AGENTS.md).
4. **Fullscreen / CSS focus mode** — discussed, not built; revisit only if layout tuning insufficient after deploy.
5. Never commit `.env`, credentials, or machine-local `config/d2l-courses.json`.
6. `portal-review-2` backlog remains separate.

---

## Exact next step

1. If Chase wants phone verification on production: **`npm run deploy:prod`** in `student-portal` (only when he asks).
2. Chase verifies **Part 1 tutorial steps** on his phone in landscape — matrix, brackets, instruction bubble, row-op buttons all visible without fullscreen.
3. If approved → replicate `matrix-tutorial-part1-inset` pattern for **Part 2 and Part 3** (rename/generalize class or duplicate rules).
4. Separately: Chase smoke-tests **Teacher Console → Roster** (test statement in `2026-09-13_tester-codes-roster-cleanup.md`).

If Part 1 still clips after deploy, nudge inset/cell-size in `matrix-embed.css` — do not touch Matrix app repo unless portal CSS cannot reach the element.
