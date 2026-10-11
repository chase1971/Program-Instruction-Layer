# Momentum handoff — Macro App gradebook History restore (M1324 Exam 2)

**Written:** 2026-10-10 (Saturday afternoon, US Central)

---

## Objective and current phase

Chase is recovering **Exam 2 grades in the Macro App gradebook** for **MATH-1324 4202 1** (`COURSE_1692723`). Grades were typed and pushed Oct 9, then the **working grid in the app showed blanks** while **baseline still had 27 Exam 2 scores** and the app showed **27 pending to push** (false “push blanks” risk). He chose **History → Restore app to after this batch** (Oct 9 ~11:12–11:14, 30 Exam 2 edits) instead of only “Restore missing grades from baseline.”

**Phase now:** Diagnostics and fixes for **History restore hanging** on Google Drive I/O are **implemented but not yet verified by Chase** after the latest preview fix. Restore has **not successfully completed** on disk (no `before-restore` snapshot, `pausedAutoPushAfterRestore` still false, `working.csv` still 0 Exam 2 filled on disk vs 27 in baseline and Oct 9 snapshot `7d31be6e-…`).

---

## Chase's desired feel

- **Trust the tool:** restore should behave like the preview (list of cells, then grid matches Oct 9 batch end state — last value per student, not every typo line in history).
- **Visibility when stuck:** no infinite “Restoring…” / “Loading preview…” with no cancel; logs he can rely on without hunting the UI behind modals.
- **D2L safety:** History restore must **not** push to D2L; auto-push should pause after restore until he confirms.
- **Accessibility:** no keyboard-only flows; Cancel must work; don’t assume he can read detail log behind a modal.

---

## Accepted decisions

| Decision | Why |
|---|---|
| Use **snapshot-based** History restore (`restoreEditBatch` / `previewRestoreEditBatch`), not replaying history lines | Snapshots hold whole-grid state at batch end; duplicate history lines are audit only. |
| **Restore target for Oct 9 batch “after”** = manifest entry `7d31be6e-2e35-48ee-b552-b5f2152a6a5f` (`batchStartedAt` 2026-10-09T16:12:46.940Z) | 27 Exam 2 cells in snapshot CSV. |
| **Step trace** in Gradebook detail log prefix **`[History restore]`** + disk **`current-session/restore-trace.jsonl`** | UI log doesn’t go to `macro-app.log`; disk trace survives hangs. |
| **Skip re-read of `working.csv`** for restore when live grid + `sessionMeta` are in memory (after flush) | Trace showed 6–20s+ hangs on Drive re-read immediately after flush. |
| **Preview uses in-memory grid** from active tab (`restoreInMemoryWorking` wired SidePanel → History modal → course view) | Preview was stuck on “Loading preview…” forever; Restore button disabled. |
| Whitelist **`restore-trace.jsonl`** in Electron `ALLOWED_SESSION_FILES` | Trace writes were silently rejected until fixed. |
| Pending-push diff by **header + student name** (earlier session) | Fixed false “27 pending” / pull blocked; still relevant after restore. |

---

## Rejected directions

- **Assuming `macro-app.log` has History lines** — it doesn’t; only module log store / optional console mirror.
- **Relying on disk read for preview/restore right after flush** — reproduces Drive lock / slow read hangs.
- **Closing app as the only escape** — Cancel during preview should clear loading; restore confirm still disables Cancel while `restoreBusy` (known UX gap if execute hangs).

---

## Current implementation state

**Repo:** `School Scrips/Macro App` (uncommitted). Programs root `agent docs` handoff only.

**Key files touched this arc:**

| Area | Path |
|---|---|
| Restore trace + disk log | `renderer/src/services/gradebookRestoreTraceLog.ts` |
| Restore/preview service | `renderer/src/services/gradebookRestoreService.ts` |
| Edit session restore entry | `renderer/src/hooks/gradebook/useGradebookEditSession.ts` |
| History UI preview | `renderer/src/components/gradebook/GradebookHistoryCourseView.tsx`, `GradebookHistoryModal.tsx`, `GradebookSidePanel.tsx` |
| Shell log on fail | `renderer/src/components/shell/AppSidePanel.tsx` |
| Session file allowlist | `electron-app/grades-backup-paths.js` (`restore-trace.jsonl`) |
| Pending push / baseline restore (parallel track) | `renderer/src/hooks/gradebook/useGradebookPendingPushDiagnostics.ts`, `buildGradebookImportCsv.ts`, etc. |

**Tests:** `npx vitest run src/__tests__/gradebook-restore-contract.test.ts` — **14 passed** after changes.

**On-disk course state (M1324, `C:\Users\chase\My Drive\Rosters etc\MATH-1324 4202 1\gradebook files`):**

- `current-session/baseline.csv` — **27** Exam 2 scores (col 35), last write Oct 9 11:14 AM.
- `current-session/working.csv` — **0** Exam 2 filled on disk; touched on each restore attempt (~2:12–2:21 PM Oct 10).
- `restore-points.jsonl` — last entries still Oct 9 push; **no `before-restore`** entries.
- `current-session/restore-trace.jsonl` — exists; last run **mv2s62f0** got through flush, slow disk load, started **read restore-point manifest** then stopped logging (likely hung on Drive read of snapshot or manifest).
- `session.json` — `pausedAutoPushAfterRestore: false`, `pendingImportGradeCount: 27`, `hasPendingImport: true`.

**React note:** `macro-app.log` had **`Should have a queue`** errors in `useGradebookPendingPushDiagnostics` (~2:05 PM Oct 10) — may have contributed to UI weirdness; not fixed in this arc.

---

## Open questions and constraints

1. **Next hang point:** After in-memory preview/restore, **`resolveTargetSnapshot` → `parseSnapshotGradebook`** may still block on **reading `restore-points/*.csv` from Google Drive** (trace stalled after “read restore-point manifest”).
2. **Batch 7 “after” UI** showed **“Snapshot: Current app grid”** while loading — label is default when `snapshotCreatedAt` null; misleading during load (cosmetic).
3. **Chase must restart Macro App** after Electron allowlist + preview wiring (Vite alone insufficient for main-process change).
4. **Fallback if History restore keeps failing:** **Restore missing grades in app** (baseline → working) — baseline already has 27 Exam 2; does **not** need History snapshot path.
5. **No commit/push** unless Chase asks end-of-session / put on GitHub.
6. **Don't launch GUI for Chase** without permission; reading trace files on Drive is fine.

---

## Read first (fresh agent)

1. This file.
2. `School Scrips/Macro App/renderer/src/services/gradebookRestoreService.ts` — `previewRestoreEditBatch`, `restoreEditBatch`, `resolveTargetSnapshot`.
3. `School Scrips/Macro App/renderer/src/services/gradebookRestoreTraceLog.ts`.
4. On failure: read `…/MATH-1324 4202 1/gradebook files/current-session/restore-trace.jsonl` (last `step` without `stepDone`).

---

## Exact next step

**After Chase restarts Macro App:** Open M1324 tab → History → batch 7 (Oct 9 Exam 2) → **Restore app to after this batch**. Confirm preview lists **~30 cells** and **Restore** enables. If restore completes, verify grid shows Exam 2 scores, `session.json` has `pausedAutoPushAfterRestore: true`, and **do not push to D2L** until Chase confirms. If it hangs again, read `restore-trace.jsonl` and fix the **next** blocking Drive read (likely snapshot CSV load — consider caching manifest snapshots in memory for active session or timeout + error surfaced in modal).

---

## Copy-ready verification checklist (for Chase or agent)

- [ ] Preview loads cell list (not eternal “Loading preview…”)
- [ ] Restore completes or trace shows clear failing step
- [ ] Exam 2 visible in grid OR use baseline restore button
- [ ] Pending push count sane vs baseline

**Repos touched (when syncing later):** `School Scrips/Macro App`, Programs `agent docs/momentum-handoffs/`.
