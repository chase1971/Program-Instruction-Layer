# Momentum handoff — Macro App launch FIXED; resume gradebook remediation (sandbox test → Phase 5)

**Written:** 2026-09-26 (late evening)
**App:** `School Scrips/Macro App`

> Previous `latest.md` (launch regression, "startup worse") is preserved at
> `agent docs/momentum-handoffs/2026-09-26_macro-app-launch-regression.md` — its launch analysis is
> **superseded** by this file (root cause turned out to be data, not launch code).

## Read first

1. **`School Scrips/Macro App/docs/plans/GRADEBOOK_REMEDIATION_PLAN.md`** — status line: Phases 0 (except 0.1), 1–4 done; next = sandbox test, then Phase 5 ("Backup newest across New Year").
2. This file § 5 for what is uncommitted and why.

## 1. Objective and current phase

- **Launch regression: solved and verified** (Chase ran `launch.bat`; log showed one `window revealed (browser slot ready)`, 3.9 s from first paint, 8.8 s total, zero main-thread stalls, no `[renderer]` errors).
- **Next phase:** gradebook remediation — sandbox restore test, then Phase 5. Launch work is done; don't reopen it unless Chase reports a new symptom.

## 2. Chase's desired feel

- "The previous way worked better… I can't let it go that the app has gotten worse" — he wants **root causes fixed**, not symptoms hidden. He **rejected** lengthening the splash grace to mask load time.
- Wants evidence from logs, not blind tweaks. Pattern that worked: add targeted instrumentation → he runs `launch.bat` → agent reads `%APPDATA%\macro-app\logs\macro-app.log`.
- Protective of real course data; asked explicitly whether the real MATH-1314 4201 class was touched (it was not).

## 3. Accepted decisions

- Launch-fix layer from the prior session **reverted** (launch-monitor.js/test, displayZoom.ts back to HEAD; browser boots `visible: true`; no `browserView.hide()` before reveal). **Kept** in `main.js`: `revealOnce` guard, `[renderer]` console-message → macro-app.log forward, gradebook flush-on-close.
- **Guard:** `electron-app/gradebook-text-read.js` (+ `gradebook-text-read.test.js`, 5 pass) — `readBackupFile` / `readSessionFile` / `readCourseFile` refuse ZIP/PDF/old-Office signatures and files > 25 MB with a clear reason.
- **Name shortener:** `renderer/src/utils/shared/compactCourseLabel.ts` keeps `Sandbox` (like `NCBO`); "MATH-1314 Sandbox TTH 10-11:20" → "MATH-1314 Sandbox". Test added (6 pass).
- **Sandbox course (COURSE_1726642):** label in `config/d2l-courses.json` restored to "MATH-1314 Sandbox TTH 10-11:20"; both folder indexes (`Rosters etc\.course-folder-index.json` and `Rosters etc\gradebook files\.course-folder-index.json`) → `MATH-1314 Sandbox TTH 10-11-20`. That folder doesn't exist yet; app creates it and downloads the fake-student roster on first sandbox gradebook open.
- **`Rosters etc\MATH-1314` folder deleted** on Chase's "delete it" (Recycle Bin + Drive trash, 30 days). It held only the bad ZIP + quarantined 223 MB copies.

## 4. Rejected / resolved directions (do not rediscover)

| Direction | Why |
|---|---|
| Launch code (reveal timing, pre-maximize, hidden boot, display-scale grace) as the cause | Real cause: sandbox gradebook built from a 123 MB D2L submissions ZIP saved as `MATH-1314 roster file.csv` → 223 MB `working.csv`/`baseline.csv` read synchronously ~5× at startup prehydrate (~1.2 s each) → browser missed the 6 s splash grace → reveal-then-snap |
| Lengthen splash grace to hide load | Chase rejected — masks, doesn't fix |
| Fix the roster downloader | **Already fixed** in commit `d1b0112` (2026-08-27): `electron-app/grades-download-routing.js` disarms the pending roster target for non-grades-CSV downloads; test replays the exact Aug 27 ZIP case. No code change needed |
| Hooks error chase | Did not reproduce in last 3 launches with `[renderer]` forward on; treat as gone unless Chase reports it |

## 5. Current implementation state

- **Macro App repo: large uncommitted diff (~91 paths)** — gradebook remediation Phases 0–4 + restructure work + this session's launch/guard/shortener changes, all mixed. **Nothing committed/pushed.** Chase has not asked to commit.
- This session's own files: `electron-app/main.js` (net: revealOnce, renderer forward, close-flush), `electron-app/gradebook-text-read.js` + test (new), `electron-app/gradebook-files-ipc.js` (routes 3 reads through guard), `renderer/src/hooks/browser/useEmbeddedBrowser.ts` (boot line back to visible:true; rest of that file's diff is older restructure work — keep), `renderer/src/utils/shared/compactCourseLabel.ts` + test, `config/d2l-courses.json` (machine-local — silent-skip on commit per root AGENTS.md).
- Temporary boot IPC/fs instrumentation was **removed**; `boot-timing.js` = HEAD.
- Verified headless: `tsc -p tsconfig.app.json --noEmit` clean; gradebook-restore-contract + file-unlock vitest 20 pass; launch-monitor 5 pass; grades-download-routing 7 pass.
- Real MATH-1314 4201 (`Rosters etc\MATH-1314 4201 1`, COURSE_1692839) verified intact: working.csv == baseline (Sep 24 10:50 pull), normal sizes.

## 6. Open questions and constraints

- **Sandbox restore test** (plan's next step) needs the sandbox gradebook opened fresh in its new folder — that's a GUI action for Chase; hand it as a statement (what to click, what to expect), never launch yourself.
- `Macro App/AGENTS.md` keyword/on-demand rows still say remediation "Phases 0–2 done" — stale; plan file says 0–4. Fix the row when touching docs.
- No commit/push unless Chase asks. File caps: `useGradebook.ts` ~750 lines (near 800 cap).
- Unknown: what relabeled the sandbox to "MATH-1314" at 8:38 PM (likely course setup's shortener — now fixed); if it flips again, investigate.

## 7. Exact next step

Read `GRADEBOOK_REMEDIATION_PLAN.md` § sandbox test and § Phase 5, then write Chase a flat statement of the sandbox restore test (open the MATH-1314 Sandbox gradebook, confirm roster = fake student, make an edit, use History → restore, what he should see, what to report). Start Phase 5 code only after he reports back or says to proceed.
