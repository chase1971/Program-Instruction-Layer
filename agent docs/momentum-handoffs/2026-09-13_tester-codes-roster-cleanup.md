# Momentum handoff: tester codes roster cleanup + Teacher Console polish

**Written 2026-09-13.** Day-valid only. If you are reading this on a later date, say so before acting.

**Slug:** `2026-09-13_tester-codes-roster-cleanup`

---

## Read first

1. **`School Scrips/Macro App/AGENTS.md`** — Teacher Console keyword rows.
2. **`School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`** — migration push rules,
   roster sync, multi-section tester model (migration 033 + new 036).
3. **`agent docs/recipes/report-grid-layout.md`** — if touching Logins table or dashboard chart layout.
4. **`School Scrips/Macro App/electron-app/shared-multi-section-testers.js`** — canonical universal
   tester IDs/codes (source of truth for SPARE-3/4/5).

**Stale handoff warning:** `2026-09-12_portal-review-2` findings (Matrix 033 bug, anon RPC exposure)
are still open but **not part of this session's work**. Do not conflate unless Chase asks.

---

## Objective and current phase

Chase wanted the **Tester codes** table in Teacher Console → Roster cleaned up: horizontal actions,
clear separation between **app access** (Activate/Deactivate) and **course membership** (Assign/Remove),
universal spare codes across all courses, rename labels, and visual gray-out when a tester is not in
the current course.

**Code is implemented in Macro App + migration 036 drafted. Not yet applied to Supabase, not yet
regenerated in roster JSONs, not verified in the live UI by Chase.**

Same session also shipped (code only, uncommitted): Logins dashboard refresh/chart fixes, report-grid
layout recipe, student-portal pamphlet scratch assets, exit-ticket preview browse-without-answer fix.

---

## Chase's desired feel (use his language)

- **App access** = turning Math App Survey (or current activity) on/off → keep **Activate / Deactivate**.
- **Course membership** = which section their universal link opens → **not** Activate/Deactivate.
  - **Remove from course** (not "Deactivate for this course")
  - **Assign to course** (not "Reactivate")
- Testers (Chase, Chris, Kristy, spares) share **one code forever**; only **one course active at a
  time** so he can move them between sections without reissuing links.
- **SPARE-3/4/5** must use the **same codes in every course** — not per-course random minting.
- He wants to **rename** spare/tester labels to remember who he gave a code to (saved globally, not
  per course).
- Rows **gray out** when the tester is **not in the current course**; still show Assign button.
- Actions should **spread horizontally** — he disliked the stacked pair of red Deactivate buttons.

---

## Accepted decisions

| Decision | Why |
|---|---|
| Universal tester roster built from `SHARED_MULTI_SECTION_TESTERS`, not per-course `courseMap.spares` | Same table every course; only membership differs |
| SPARE-3/4/5 canonical codes from MATH-1324 JSON: `WTNWHG`, `QG6WR7`, `9BCSUL` | M1324 was existing source of truth in shared-multi-section-testers comment |
| `grant_student_membership` RPC deactivates other course memberships when assigning | Enforces one active course at a time |
| Tester labels in `tester-code-labels.json` via `tester-code-labels-io.js` | Rename anywhere; persists in userData |
| Course column badges: **In course** / **Not in course** | Easier than inferring from gray row alone |
| Delete `RosterSpareRevokeButton.tsx`; course actions live inside `RosterStudentActions` horizontal row | Fixes stacked-button UX |
| Logins: manual Refresh only (no auto-refresh); refresh must not blank dashboard | `hasResolvedOnce` gate in `useLoginsScreenData` |
| Report grid recipe replaces column-sizing-only doc | Full scroll-frame + tooltip stacking guidance |

---

## Rejected directions (do not redo)

- **Two red Deactivate buttons** stacked (app + course) — rejected; course action is secondary/outline or primary Assign, not danger red.
- **"Deactivate for this course"** label — rejected; use **Remove from course**.
- **Per-course random codes for SPARE-3/4/5** — rejected; extend shared list like Chris/Kristy.
- **Revoke code** for multi-section testers in this table — removed from UI; course removal is the right tool (revoke code was for legacy per-course spares).
- **Auto-refresh Logins dashboard every 60s** — removed per Chase.
- **HTML pamphlet as deliverable** — Chase wanted image; PNG + viewer HTML on docs server was compromise.

---

## Current implementation state

### Tester codes (primary — needs deploy + verify)

| Area | Files |
|---|---|
| Shared codes | `Macro App/electron-app/shared-multi-section-testers.js`, `renderer/.../sharedMultiSectionTesters.ts` (+ `buildUniversalTesterRows`) |
| Migration **not pushed** | `student-session-kit/supabase/migrations/036_multi_section_spares_grant_membership.sql` — `grant_student_membership`, backfill SPARE-3/4/5 |
| IPC | `student-progress-io.js` — `grantSectionMembership`, `listSectionMemberships`; `tester-code-labels-io.js` (new) |
| Preload/types/service | `preload.js`, `macroAppStudentProgress.d.ts`, `studentProgressService.ts` |
| UI | `ConsoleRosterScreen.tsx`, `RosterStudentActions.tsx`, `RosterTesterCourseActions.tsx`, `TesterRenameModal.tsx`, `useTesterSectionMemberships.ts` |
| CSS | `teacher-console-grades.css` — `--tester` row actions wrap, course badges, rename modal |
| Deleted | `RosterSpareRevokeButton.tsx` |
| Roster codes script | `student-portal/scripts/lib/roster-codes.mjs` — `sharedTesterForSpareIndex` now maps indices 0–4 to all non-instructor shared testers |

**Canonical SPARE IDs/codes (M1324):**

- SPARE-3: `57ccdad0-6017-4f9b-8e7d-10334b97dc42` / `WTNWHG`
- SPARE-4: `a6e0fa4a-c760-4afb-af09-24866bc00c3d` / `QG6WR7`
- SPARE-5: `e7ba6610-240b-4bab-b508-737841fc1019` / `9BCSUL`

**M1314 `student-portal-codes.json` still has old per-course spare IDs/codes** (`NBALW3`, etc.) —
needs `npm run codes` regen after shared list update.

### Other session changes (uncommitted)

- **Logins:** `DashboardLoginsPreview.tsx`, `useLoginsScreenData.ts`, `LoginsWeekGrid.tsx`, shell wiring
- **Exit ticket preview:** `ExitTicketLivePreview.tsx` — Next works without answering (browse mode)
- **Docs:** `agent docs/recipes/report-grid-layout.md`, INDEX update; pamphlet in `agent docs/scratch/`
- **Macro App** also has unrelated dirty files (packaging, slim build, ci-shims) — do not revert blindly

### Verification

- `tester-spare-labels.test.js` passes.
- **Not run:** Macro App UI smoke (needs Chase permission — GUI).
- **Not applied:** migration 036 to Supabase.
- **Not run:** roster codes regen or `sync-portal-rosters`.

### Git state (uncommitted, do not push unless asked)

- `School Scrips/Macro App` — many modified + new tester files
- `School Scrips/student-session-kit` — new 036 migration
- Programs root — agent docs, scratch pamphlet, session logs

---

## Open questions and constraints

1. **Migration 036 must be pushed** before Assign/Remove course buttons work (RPC missing until then).
2. **Regenerate codes** for M1314 (and any other course folders) so JSON spares match universal IDs.
3. **Sync rosters** after codes regen so Supabase memberships/codes align.
4. Chase has **not seen** the new roster UI — hand him a flat test statement after deploy, do not launch GUI without asking.
5. **Chris code in screenshot** showed `KQ8ZC8` once; canonical in code is `KQRZC6` — if live DB differs, reconcile against Supabase, not the screenshot.
6. **Portal review-2** (Matrix 033 save bug, anon RPC revoke) remains a separate backlog — see `2026-09-12_portal-review-2.md`.
7. Never commit `.env`, credentials, or `config/d2l-courses.json` machine-local dirty.

---

## Exact next step

1. Push **`036_multi_section_spares_grant_membership.sql`** to Supabase (per STUDENT_PROGRESS_PIPELINE).
2. Regenerate **`student-portal-codes.json`** for **MATH-1314 4201 1** (and verify M1324 spares unchanged) via `npm run codes` in student-portal.
3. Run **`sync-portal-rosters`** for affected courses.
4. Hand Chase the roster test: open Teacher Console → Roster on M1324 vs M1314 — same tester table, Course column shows In/Not in course, horizontal actions, Rename saves label globally.

If migration or sync fails, stop and surface the error — do not patch around missing RPC.
