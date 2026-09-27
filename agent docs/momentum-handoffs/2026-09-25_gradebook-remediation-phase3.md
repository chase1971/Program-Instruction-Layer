# Momentum handoff — Gradebook remediation: Phases 0–2 done, Phase 3 (snapshot restore points) next

**Written:** 2026-09-25
**App:** `School Scrips/Macro App` — Gradebook tab

> Another session's handoff from today (Macro App embedded-browser restructure, Phase 4 next) was
> the previous `latest.md`. It is preserved at
> `agent docs/momentum-handoffs/2026-09-25_macro-app-restructure-phase4.md` — not this task.

## Read first

1. `School Scrips/Macro App/docs/plans/GRADEBOOK_REMEDIATION_PLAN.md` — **the plan; authoritative.**
   Phase 3 + Phase 4 sections are the spec for the next work. "Done" notes under Phases 0–2 record
   what landed.
2. `renderer/src/__tests__/gradebook-restore-contract.test.ts` + `__tests__/helpers/gradebookRestoreHarness.ts`
   — the restore contract the rebuild must satisfy.
3. `School Scrips/Macro App/AGENTS.md` (keyword row "gradebook remediation / restore point").

## 1. Objective and current phase

Chase is cleaning up the Macro App Gradebook tab: remove risks to real grades, then rebuild
History restore points so he can safely go back to an earlier grid. He coded restore long ago,
never tried it, and is worried about using it — he wants it reviewed and made trustworthy, then
he'll test on his **sandbox class**.

| Phase | Status |
|---|---|
| 0 Containment | Done except **0.1** (land other session's in-flight work — not ours to commit) |
| 1 Save safety | Done |
| 2 Restore characterization tests | Done |
| **3 Snapshot-based restore points** | **Next** |
| 4 Restore UX (preview, Undo restore, persistent status) + sandbox test | After 3 |
| 5 Backup "newest" across New Year | Later |
| 6 Hook/component/CSS splits | Last, separate commits |

Plans in `docs/plans/` auto-archive after 7 untouched days (start Phase 3 by ~2026-10-02).

## 2. Chase's desired feel

- Worried about restore: wants **certainty before anything changes** — preview of exactly which
  cells change, a way back (Undo restore), and **nothing reaches D2L until he pushes**.
- Accessibility: head-mounted gyro mouse + dwell click. Big targets, no typing, **no backdrop-dismiss
  modals**, no toasts / "Saved!" ephemera, no hover-only info (visible text for reasons).
- **Never launch the app or any window** — verify headlessly; end with a flat statement of what he'll
  see next time he opens it (never "want me to…").
- Liked comparing two independent plans; chose the merge. Prefers practical over over-engineered.

## 3. Accepted decisions

- **Restore = immutable CSV snapshots**, not change-log replay. Change log stays for in-session
  undo/diagnostics only.
- **Restore by student + assignment name onto the current grid** (org-defined ID when present, else
  "Last, First"; duplicate names → that student skipped and listed). Cells only in one side are left
  alone and **listed in the preview**. Reason: exact-structure-only restore would make every older
  point view-only after routine D2L pulls add assignments (that was the other plan's weakness).
- Trim over-engineering from the independent plan: no content fingerprints / tamper tests /
  per-course write queue. Keep snapshots, preview, before-restore recovery snapshot, rollback,
  restore event in history, auto-push pause.
- Storage: `<course>/restore-points/` + `restore-points.jsonl` manifest; written via
  `writeUtf8FileWithUnlock` (now the single crash-safe write owner). Retain all snapshots for now.
- Snapshot triggers: after a debounced edit batch is saved (**reuse the working-flush timer**, no new
  scheduler), after pull merge, after push, before restore. Each edit-batch snapshot records the one
  before it so "before this batch" is a real file.
- After restore: `pausedAutoPushAfterRestore` for that course; cleared by manual push, Undo restore,
  or a confirmed pull.
- Legacy history: visible, labelled "View only — from before restore points". No migration/deletion.
- Remove replay-restore code (`restoreGradebookToChangeSeq`, `resolveGradeHistoryClusterSeq`, unused
  `replayGradebookCurrent`) only after 3.1–3.6 pass.

## 4. Rejected directions (don't rediscover)

- Patching log-replay (name-keyed replay) as the restore authority — superseded by snapshots.
- Exact column/roster compatibility as the only restore rule — too restrictive (see above).
- Temp-folder test harness — used an in-memory fake of the gradebook file IPC instead (same envelope).
- Committing the other session's uncommitted work to "land" Phase 0.1 — it was still changing.
- `node:test` files in `electron-app/` for new tests — CI doesn't run them. Use Vitest
  `renderer/src/__tests__/electron-*.test.ts` + `requireElectronApp`.

## 5. Current implementation state (all uncommitted)

Verification at handoff: renderer full suite **1502 passed**; `tsc -p tsconfig.app.json` clean;
electron lint clean. (Full `tsc -p .` has pre-existing errors in unrelated test files.)

**Phase 0** — `GradebookSidePanel.tsx` no longer forwards `onRestoreFromHistory` (restore unreachable);
History shows "Restore is being rebuilt — history is view-only for now." (`GradebookHistoryModal/CourseView/ClusterBlock.tsx`);
auto-push checkbox restored on the Push button (`GradebookSessionStatusLights.tsx`, lost in July
commit `dd22d0c`; stays clickable when nothing pending); label "Open D2L Gradebook".

**Phase 1** — `electron-app/gradebook-close-flush.js` + `preload gradebook.onFlushBeforeClose` +
`hooks/gradebook/useGradebookFlushOnAppClose.ts` (main waits ≤ 3 s before destroy);
`gradebook-file-unlock.js`: temp+rename writes, `appendUtf8FileWithUnlock`, closes Excel/Word only
if exact path AND saved, never Notepad, clear "open in another program" error;
`useGradebookEditSession.flushAndResetSession` (clearGradebook race); `readGradeHistory` throws on
real read errors. Extracted `useGradebookChangeLogWriter.ts` (edit session 739 → 684 lines).

**Phase 2** — `__tests__/helpers/fakeGradebookFiles.ts`, `__tests__/helpers/gradebookRestoreHarness.ts`
(`FakeCourse`: start/edit/nextBatch/push/pull/startNewSession/grid/restoreBatch), and
`__tests__/gradebook-restore-contract.test.ts`: 6 passing guards + 7 `it.fails` known bugs, each
verified to fail on exactly its bug. **`FakeCourse.restoreBatch` is the only seam to swap in Phase 3.**
Phase 1 tests: `__tests__/electron-gradebook-file-unlock.test.ts`, `electron-gradebook-close-flush.test.ts`.

**Shared/dirty files with the other (restructure) session:** `electron-app/preload.js` (their 8 lines +
our `onFlushBeforeClose`), `AppSidePanel.tsx`, `useMacroAppShell.ts`, `useGradesBulkEdit.ts`,
`useMacroAppShellGradebookPipeline.ts`, slot/isolation files. Don't edit theirs; commit care needed.

## 6. Open questions and constraints

- File sizes: `useGradebook.ts` 748 (over 700 extract line — extract before adding), edit session 684,
  `GradebookSidePanel.tsx` 523, `styles/gradebook/panel-shell.css` >1000 (don't add CSS there — new file).
- No commits/pushes mid-session unless Chase asks ("put on GitHub" / end-of-session).
- Chip pending for Chase: "Run orphaned electron-app tests in CI" (task_f0d7ce40).
- Undecided detail (proposal, not approved): exact wording/placement of the persistent
  "Restored in app — not pushed to D2L" status — plan puts it in the Session section.

## 7. Exact next step

Start Phase 3.1–3.2: add `sessionId` to session meta (new only on a genuinely new session) and a
restore-point snapshot store (`restore-points/` + manifest) behind the existing gradebook IPC/path
owners, written with `writeUtf8FileWithUnlock`; create edit-batch snapshots from the working-flush
path. Then implement 3.3–3.4 (name-keyed restore + transaction), point `FakeCourse.restoreBatch` at
the new service, and flip each `it.fails` to `it` as it passes.
