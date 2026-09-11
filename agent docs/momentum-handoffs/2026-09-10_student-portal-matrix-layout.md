# Momentum handoff — 2026-09-10 — Student Portal Matrix tutorial layout + UX

> **Written:** 2026-09-10 · **Repos:** student-portal, Matrix app, App Dashboard, electron-toolbar (all uncommitted)

## Objective and current phase

Ship the **Gauss-Jordan Matrix tutorial** inside **Student Portal** for M1324 students, viewed in the **812×460 horizontal Chrome launcher** (`student-portal-horizontal` / **Portal Wide**). Tutorial flow, home screen, exit-to-home, and **viewport-fit layout** are implemented. Chase confirmed **2026-09-10: "this looks good"** on the layout fix.

Phase: **feature + layout green locally** — ready for tutorial walkthrough QA, optional cleanup, then commit/deploy when Chase asks.

## Chase's desired feel

- **Shaped window matters** — never hand Chase raw browser URLs; use **Portal Wide** (812×460) or **Portal Debug** launchers. Full-browser links are useless for sizing judgment.
- **One white panel** — navy header through bottom rounded curve; **no gray/navy band** below the card.
- **Home screen** — matrix visible, intro text beside it, small **Start Tutorial** + **Auto Solve** (not a giant Tutorial button). No "step 1" label on open; flashing restored on buttons when applicable.
- **Red Exit** near Next (~20px offset) returns to **home**, not assignments Back.
- **No auto-resume** for this tutorial on load (resume is for homework later; teacher-console toggle deferred).
- **Cannot type URLs** — launchers must bake query params (`?s=CHASE1`, `layout-debug=1`) into `apps.json` `openQuery`.
- Layout debug overlays are **optional/dev** — too messy for daily use; Chase identifies frames by color when needed.

## Accepted decisions

| Decision | Why |
|---|---|
| Mount Matrix parts via `MatrixSolver` / Part 2 / Part 3 directly in portal — not Matrix `App.tsx` | Matrix app owns part-selector chrome; portal supplies nav |
| Portal props on `MatrixSolver`: `hideStartControls`, `rightPanel`, `skipIntroOnStart`, `ref.startTutorial` | Home vs in-tutorial without forking Matrix repo heavily |
| `useMatrixTutorialAttempt` — no resume on load; phase starts `'tutorial'` | Chase: resume later for homework, not this walkthrough |
| Eager-import `MatrixTutorialView` in `App.tsx` (no lazy/Suspense) | Removed double loading flash |
| Matrix CSS scoped in `matrix-embed.css` — do **not** import Matrix `theme.css` / second Tailwind | Would repaint portal globals |
| Flex column fill for `.portal-quiz--matrix` chain (`100dvh`, white body bg) | Fixes gray below card in 460px-tall window |
| `matrix-embed--with-nav { padding-top: 2.35rem }` | Nav is absolute; matrix must not sit under Part/Back/Next/Exit |
| Override `.min-h-screen` / `.min-h-[500px]` inside `.matrix-embed` — flex fill, not 500px floor | 500px min-height caused scroll/clipping in 460px viewport |
| **`student-portal-horizontal-debug`** launcher + toolbar tile **Portal Debug** (🔍) | `openQuery`: `?s=CHASE1&layout-debug=1#/matrix-tutorial` — same geometry as Portal Wide |
| `portal-layout-debug.css` + `?layout-debug=1` | Dev-only colored frames; off by default |

## Rejected directions

- **`max-height: 500px` + inner scroll on `.matrix-embed`** — shrank usable area to ~200px; reverted.
- **Handing Chase `localhost` or `127.0.0.1` links** — wrong viewport; use launchers.
- **Expecting relaunch to show debug** without `layout-debug=1` in launcher URL — debug is opt-in.
- **Nested rectangular card inside curved panel** — removed; one white shell.
- **Big custom Tutorial button on home** — Chase wanted original small Start Tutorial + Auto Solve restored.
- **End-of-session commit/push as part of this handoff** — not requested.

## Current implementation state

### student-portal (dirty)

| Area | Files |
|---|---|
| Tutorial view / home / exit | `MatrixTutorialView.tsx`, `MatrixTutorialHomePanel.tsx`, `MatrixTutorialNav.tsx`, `useMatrixTutorialParts.ts`, `useMatrixTutorialAttempt.ts`, `matrixTutorialActivity.ts` |
| Layout fill fix | `src/styles/index.css` (`.portal-quiz--matrix` flex chain), `matrix-embed.css` |
| Layout debug | `useLayoutDebug.ts`, `LayoutDebugLegend.tsx`, `portal-layout-debug.css`, `data-layout-frame` on shell/panel/view |
| App wiring | `App.tsx` (eager import + legend), `PortalShell.tsx`, `PortalContentPanel.tsx` |
| Launcher | `launch-horizontal-debug.bat` |

### Matrix app (dirty)

- `matrix-solver.tsx` — portal props above
- `use-matrix-tutorial.ts` — `startTutorial({ skipIntro?: boolean })`

### App Dashboard (dirty)

- `apps.json` — new entry `student-portal-horizontal-debug` (`viewOf: student-portal`, 812×460, debug openQuery)

### electron-toolbar (dirty)

- `scripts-panel.html` — **Portal Debug** tile (`student-portal-horizontal-debug`)

### Reference (optional)

- `agent docs/scratch/student-portal-matrix-layout-frames.html` — nested diagram (not shaped window)

### Verification

- `npm run build` in student-portal — **passes**
- Chase verified layout on **Portal Wide** — **looks good**

### Launcher URLs (for agents — Chase uses tiles, not URLs)

| Tile | apps.json id | Window | openQuery |
|---|---|---|---|
| Portal Wide | `student-portal-horizontal` | 812×460 | `?s=CHASE1` |
| Portal Debug | `student-portal-horizontal-debug` | 812×460 | `?s=CHASE1&layout-debug=1#/matrix-tutorial` |
| Student Portal (vertical) | `student-portal` | 460×812 | `?s=CHASE1` |

Close other portal Chrome windows before launching — shared `chrome-mobile-profile` / `localStorage` student code.

## Open questions and constraints

- **Tutorial step-by-step QA** on Portal Wide (Parts 1–3, submit, Auto Solve after completion) — not fully walked this session after layout fix.
- **Remove layout debug** (launcher + CSS + legend) when Chase is done diagnosing — keep until he says otherwise.
- **Teacher Console** publish toggle + resume policy — explicitly deferred.
- **Netlify deploy** — only when Chase asks (`npm run deploy:prod`).
- **Commit/push** — dirty across 4 repos; wait for "put on GitHub" or end-of-session.
- **Never display without permission** — QA is Chase's launcher, not agent opening Chrome.

## Exact next step

Walk the **full tutorial on Portal Wide** (812×460): home → Start Tutorial → Parts 1–3 → Exit to home → Auto Solve (after completion). Log any step where popovers clip, matrix overlaps nav, or content scrolls unexpectedly. If all green, ask Chase whether to remove debug launcher/CSS and commit all four repos.

## Read first (fresh agent)

1. This file
2. `School Scrips/student-portal/AGENTS.md`
3. `School Scrips/student-portal/src/features/matrix-tutorial/MatrixTutorialView.tsx`
4. `School Scrips/student-portal/src/styles/index.css` — `.portal-quiz--matrix` block (~line 194)
5. `School Scrips/student-portal/src/styles/matrix-embed.css`
6. `School Scrips/App Dashboard/docs/LAUNCHER.md` — shaped Chrome / `viewOf` / profile sharing
