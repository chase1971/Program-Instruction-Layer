# Momentum handoff — 2026-09-09 — M1324 Matrix portal pilot

> **Written:** 2026-09-09 · **Repos:** student-portal (uncommitted), Drive/Supabase (operational)

## Objective and current phase

Pilot the **Matrix Gauss-Jordan tutorial** for **MATH-1324 (Finite)** only. Students get a dead-simple portal: sign in → one button → tutorial. College Algebra (1314) must see nothing yet. Teacher Console publish toggles and grade viewing are **explicitly out of scope** for this phase.

Phase: **implementation done headlessly**; Chase was verifying locally with CHASE1 when dev server connection failed — fixed same session.

## Chase's desired feel

- **No thinking required** — one obvious button, no tabs, no classwork/exit tickets for now.
- **1324 only** for real students; 1314 blocked until Chase gives them something later.
- **CHASE1** must work on **either** section (personal test bypass).
- Matrix tutorial behavior unchanged — scoring, Part 3 answer recording, submit flow stay as built.
- Don't connect to Teacher Console yet; he'll want publish on/off later.

## Accepted decisions

| Decision | Why |
|---|---|
| One portal, section-gated via `portalAccess.ts` | Exit tickets already use `section_id`; same pattern, portal-side for Matrix |
| `MATRIX_ENABLED_SECTION_IDS` hardcoded with Supabase UUID | Fast pilot; Teacher Console replaces later |
| `PORTAL_BYPASS_CODES = ['CHASE1']` | Chase tests without moving his code off 1314 |
| Simplify `App.tsx` — home + matrix route only | Old tab views stay in repo but not routed |
| Codes via `npm run codes` + `npm run sync-portal-rosters` | Existing pipeline; no manual SQL paste |
| Section UUID from **sync script output**, not SQL hash | Sync uses DB-generated id (`956144f1-…`); hash in generate-student-codes SQL differs |
| Vite `host: '127.0.0.1'` | Stale IPv6-only listener broke Firefox on `127.0.0.1:5340` |
| No Netlify deploy until Chase asks | AGENTS shipping policy |

## Rejected directions

- **Two separate portals / two Netlify sites** — one site, section gate.
- **Course encoded in every activity UUID** — `section_id` is enough.
- **Teacher Console Apps screen now** — placeholder exists; not wired.
- **1314 Matrix access** — blocked except CHASE1 bypass.
- **End-of-session commit/push as part of handoff** — momentum handoff ≠ end of session.

## Current implementation state

### student-portal (git dirty, not pushed)

| File | Change |
|---|---|
| `src/config/portalAccess.ts` | **New** — allowlist + CHASE1 bypass |
| `src/app/components/MatrixHomeView.tsx` | **New** — single Gauss-Jordan tile |
| `src/app/components/PortalNoAccess.tsx` | **New** — valid code, wrong section |
| `src/app/App.tsx` | Simplified routing |
| `src/hooks/usePortalRoute.ts` | Default `home`; legacy tabs → home |
| `vite.config.ts` | `host: '127.0.0.1'` |
| `docs/sessions/SESSIONS.md` | Session entry with test URLs |

`npm run type-check` and `npm run build` **green**.

### Operational (Drive / Supabase)

- **1324 codes:** `My Drive/Rosters etc/MATH-1324 4202 1/student-portal-codes.json` + `student-portal-links.csv` (28 students + 5 spares)
- **Supabase section:** `956144f1-49be-42d6-be6b-dc46cb6845ad` for `MATH-1324 4202 1`
- **1314** also re-synced (33 students) — those codes hit PortalNoAccess

### Local dev

- `npm run dev` in student-portal → **http://127.0.0.1:5340/**
- Dev server was started in agent session; may need restart if machine rebooted.

### Test URLs

| URL | Expected |
|---|---|
| `http://127.0.0.1:5340/?s=CHASE1` | Home + Matrix button |
| `http://127.0.0.1:5340/?s=4AX6UT` | 1324 student — same |
| `http://127.0.0.1:5340/?s=AYNBWC` | 1314 student — "Nothing here yet" |

Production **mathappsclass.netlify.app** still has **old multi-tab UI** until deploy.

## Open questions and constraints

- Chase has **not** live-verified Matrix submit after the UI simplification (headless build only).
- **Deploy:** `npm run deploy:prod` in student-portal only when Chase asks.
- **Macro App Teacher Console** — grades/roster for Matrix attempts exist in Supabase but Macro UI not priority.
- **Remove CHASE1 bypass** when 1314 gets its own app.
- Never open browser/GUI without permission; handoff tests are for Chase to run.

## Exact next step

1. Confirm Chase can load **http://127.0.0.1:5340/?s=CHASE1** (start `npm run dev` if needed).
2. Click through Matrix tutorial once; confirm score/submit still works.
3. If good, ask Chase whether to **deploy to Netlify** for 1324 student links from `student-portal-links.csv`.

**Read first in fresh task:** `School Scrips/student-portal/AGENTS.md` · `School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` · this file.
