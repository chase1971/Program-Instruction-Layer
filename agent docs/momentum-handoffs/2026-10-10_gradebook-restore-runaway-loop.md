# Momentum handoff — Macro App gradebook: Restore freeze = app-wide runaway loop

**Written:** 2026-10-10 (Saturday ~3:10 PM US Central)

---

## Objective and current phase

Chase wants **History → "Restore app to after this batch"** in the Macro App gradebook to actually work, so he can **test the restore mechanism himself**. **Do NOT fix his data by editing files** — he explicitly said: "I don't want you to just change the grades. I want you to fix the code so that the restore works."

Test case: **MATH-1324 4202 1** (`COURSE_1692723`), History batch 7 (Oct 9 ~11:12–11:14 AM, Exam 2 entry), "after". Data is safe: snapshot `restore-points/7d31be6e-….csv`, `current-session/baseline.csv` and D2L all have the 27 Exam 2 scores; `working.csv` equals the Oct 8 snapshot `d32b9523` exactly (only Exam 2 + derived calc columns differ → preview says "102 cells would change", which is correct).

**Phase now:** diagnosing a **runaway loop that freezes the whole app** (main + main renderer). A **CPU profiler run was in progress** when this was written (see Exact next step).

---

## Chase's desired feel

- **Systemic, not piecemeal.** "Usually when it takes multiple times with agents to try to fix something and nothing gets fixed, it's some kind of systemic problem." He asked for a **governing body / arbiter** (like the browser `slotLoadArbiter`) so things can't overlap or do what they shouldn't "because no one has the authority to dictate what happens."
- **Restore must be trustworthy** and testable by him; never push to D2L.
- He drives with a **head-mounted gyro mouse + dwell click** — a frozen app means he can't click the error messages. Never launch the GUI yourself; hand him statements (not questions) on what to run.
- Be honest about what is proven vs guessed (last agent over-claimed once and had to retract).

---

## Accepted decisions (implemented this session, uncommitted)

| Decision | Where |
|---|---|
| **Gradebook file arbiter** — single owner of gradebook:read/write/append Session/Course/Backup file IPC: async fs, per-course FIFO queue, 20 s deadline per op (`{ok:false,timedOut}`), refuses to overwrite `working.csv`/`baseline.csv` changed on disk since last read/write (`changedOnDisk`), `replaceExternalChanges` for new sessions | `electron-app/gradebook-file-arbiter.js` (+ `.test.js`, 7 pass), `gradebook-files-ipc.js`, `gradebook-text-read.js` (async `readGradebookTextFile`), `gradebook-file-unlock.js` (async writes) |
| **Saves only write real edits** — `unsavedEditGenRef` in edit session; `flushPendingSave` no-ops when nothing unsaved (it used to rewrite the in-memory grid on every course switch/close/restore = silent stale overwrite mechanism) | `renderer/src/hooks/gradebook/useGradebookEditSession.ts` |
| Session cache refreshed after every save/restore; dropped on `changedOnDisk` | `services/gradebookCourseSessionCache.ts` (`refreshGradebookCourseSessionCacheForSlug`, `invalidate…ForSlug`), `gradebookSessionService.ts` |
| AA working-roster sync: `spawnSync` → async `execFile` with 60 s timeout | `electron-app/aa-working-gradebook-sync.js` |
| Runtime main-thread stall watch (≥1 s, names in-flight gradebook ops) | `electron-app/main-thread-stall-watch.js`, wired in `main.js` (now 699 lines — at cap edge) |
| ADR + AGENTS rows | `School Scrips/Macro App/docs/decisions/ADR-005-gradebook-file-arbiter.md`, Macro App `AGENTS.md` |
| **TEMP** main inspector `--inspect=127.0.0.1:9339` in dev launch — **remove once freeze fixed** | `scripts/dev-electron.cjs` |

Verification: renderer `tsc` clean for touched files (one pre-existing unrelated error in `exitTicketsService.ts`); vitest gradebook suites 566 pass; electron lint clean.

Earlier agent (also uncommitted, same repo): restore trace (`gradebookRestoreTraceLog.ts`, `current-session/restore-trace.jsonl`), in-memory preview, name-based pending-push diff, `useGradebookPendingPushDiagnostics.ts` (new hook), pull-skip logging, side-panel buttons.

A follow-up proposal card exists: "Single owner for the in-memory gradebook grid" (renderer side) — not started.

---

## Rejected directions / proven-wrong hypotheses

- **"Google Drive file I/O hangs restore"** — mostly wrong. With the arbiter, preview reads take ~70–100 ms. Slow reads earlier were *symptoms* of a blocked main thread.
- **Directly restoring working.csv on disk** — Chase rejected; he wants the code path fixed.
- **Claim that grades were lost at the 1:59 PM app close** — retracted (pendingImportUpdatedAt resets for other reasons). Exact loss moment unproven; mechanism (flush wrote stale in-memory grid) is fixed.
- Session cache / mirror / AA sync as data-loss cause — mirror ruled out (no gradebook-mirror.json); cache plausible, unproven.
- Main-process log store / console forwarding loop — reviewed, bounded (500-line ring, `[renderer] ` prefix cut); not the cause as far as read.
- `process._debugProcess` on Electron — doesn't work; hence the `--inspect` flag.

---

## Current diagnosis (facts)

- On Restore click (19:58:09 UTC run), main stalls grew ~×1.8 each: 1.1, 2.0, 3.7, 6.7, 12.1, 21.7, 38.0 s. Main process ~2 GB RAM, main renderer **5.7 GB**, both ~100 % CPU. DevTools HTTP (9224) unresponsive.
- **Not restore-specific:** every launch since **19:17 UTC (2:17 PM local)** shows main stalls ~10–60 s after `[BrowserSlot] pearson post-login recreate` / `bootstrap slot=pearson` (45 s loadURL timeouts fire 7–25 s late). Launches up to 19:15 were healthy (`post-login-recreate … load aborted (ignored)` ~1.3 s after).
- Only source change between those launches: `renderer/src/components/shell/AppSidePanel.tsx` (14:16:39 local) — prior agent added `onLogPendingPush` / `onRestoreMissingFromBaseline` / `canRestore…` props + restore try/catch. `useGradebookPendingPushDiagnostics.ts` (14:04) existed before the healthy 19:14/19:15 launches. Causation unproven.
- Earlier today: `Maximum update depth exceeded` (17:03 UTC, moduleLogStore during bulk pull) and `Should have a queue` hooks-order crash (19:05 UTC, HMR after adding the diagnostics hook).

**Interpretation (unproven):** exponential pattern suggests a renderer loop where each round schedules ~2× work (effect re-trigger, listener leak, or IPC ping-pong). Suspects: `useGradebookPendingPushDiagnostics` effects (two effects that each read baseline+working via IPC and set state; effect 2 depends on `syncLog`, `selectedCourse`), new AppSidePanel inline props, Pearson post-login recreate.

---

## Open questions and constraints

- Don't launch the app GUI; Chase launches. Don't commit/push unless he says pull / put on GitHub / end-of-session.
- File-size caps: `main.js` 699 (don't add), `useGradebookEditSession.ts` 632, `gradebook-files-ipc.js` 636.
- Root cause of the original Exam 2 loss remains unproven beyond the (fixed) silent-flush mechanism.
- Bulk-pull "pending pushes" vs tab "no pushes": two sources of truth (session.json count vs file diff) — unify later.

---

## Read first (fresh agent)

1. This file.
2. Profiler results: `C:\Users\chase\AppData\Local\Temp\claude\C--Users-chase-Documents-Programs\3579a8c3-f32f-43e6-9615-c488d9a661b0\scratchpad\prof\summary.txt` (+ `main.cpuprofile`, `renderer.cpuprofile`, `progress.log`). Profiler started 20:09:20 UTC for 180 s.
3. `School Scrips/Macro App/docs/decisions/ADR-005-gradebook-file-arbiter.md`.
4. `renderer/src/hooks/gradebook/useGradebookPendingPushDiagnostics.ts`, `renderer/src/components/shell/AppSidePanel.tsx` (git diff).
5. Log: `%APPDATA%\macro-app\logs\macro-app.log` (`[main] main thread stalled` lines).

---

## Exact next step

Read `summary.txt` above. If it exists, the hottest stacks name the loop — fix that at its owner (no parallel mechanism), add a regression test, then hand Chase a flat statement to relaunch and test restore. If `summary.txt` is missing (Chase didn't click Restore in the window, or stop timed out), re-run the profiler — copy at `agent docs/scratch/profile-macro-app.mjs`: `node "agent docs/scratch/profile-macro-app.mjs" <outDir> 180` in the background, then tell Chase to open the Macro App and click Restore within 2 minutes. After the fix, remove the TEMP `--inspect` from `scripts/dev-electron.cjs`.

---

## Update after handoff (profiler finished 20:16 UTC)

The first profiler run produced **no profiles**: `Profiler.stop` timed out for both main and renderer (each waited 120 s). Either both processes were jammed solid by 20:12 or the app was closed during the run. **Don't re-run that version as is.** Change `agent docs/scratch/profile-macro-app.mjs` to take **rolling 10 s chunks** (stop, save `chunk-N.cpuprofile`, start again) so the chunks from the first seconds of the freeze survive. Also log `Runtime.getHeapUsage` for the renderer every 5 s, to catch the memory climb.
