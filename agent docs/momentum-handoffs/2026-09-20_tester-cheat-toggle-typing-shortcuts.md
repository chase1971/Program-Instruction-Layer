# Momentum handoff — Tester cheat toggle + typing-only guided practice shortcuts

**Written:** 2026-09-20 (Sunday, ~5:45 PM)

---

## 1. Objective and current phase

**Active thread:** Give **universal testers** (not enrolled students) **typing shortcuts** in Gauss-Jordan guided practice — row-op notation prefill and matrix **Use answer** — controlled by a **Teacher Console toggle** per tester, backed by Supabase. **No step-skip or “submit whole answer” cheats.**

**Phase:** **Implementation complete; headless tests green; awaiting Chase live verification.** Migrations **048 + 049 pushed** to Supabase. **Not committed, not deployed to Netlify.**

**Earlier same-day thread (superseded for fresh task):** Row-notation UX polish (help trigger click/drag, notation nowrap) — archived at `2026-09-20_guided-practice-row-notation-ux.md`. Cheat work builds on that Matrix embed but is the current focus.

---

## 2. Chase's desired feel (use his language)

- **Cheats = typing shortcuts only** — row transformation notation prefill, **Use answer** on matrix slots. **Not** dev jumps, Back/Next skips, home skips, or whole-answer submission.
- **Remove all “Submit correct answer” buttons** — including instructor-only ones that existed in practice mode. No admin nav bar for step jumping.
- **Testers default ON** for cheat; **enrolled students never** get cheat (no toggle for them, always off at sign-in).
- **Teacher Console:** right-aligned **Cheat enabled** checkbox on each **Preview workspace tester card** (universal testers only). Toggle takes effect on tester's **next portal reload/sign-in**.
- **Instructors** still get typing shortcuts via `is_instructor` — same as before, but still **not** full portal bypass through cheat flag.
- **No surprise windows** — never launch GUI without asking. Hand him what to run and what to expect.
- **Modals never dismiss on backdrop click.**

---

## 3. Accepted decisions (do not re-litigate)

| Decision | Why |
|---|---|
| **`hasAdminCheats()`** = instructor OR stored `cheatEnabled` from sign-in | Typing shortcuts only; does **not** grant full instructor portal access. `portalAccess.ts`. |
| **Cheat returned from RPC only when `multi_section_tester AND cheat_enabled`** | Enrolled students always get `cheat_enabled: false` on sign-in even if column were wrong. Migration 049. |
| **`students.cheat_enabled` column + `list_student_cheat_enabled` / `set_student_cheat_enabled` RPCs** | Service-role only; set RPC guarded to universal testers. Migration 048. |
| **Testers upserted with `cheat_enabled: true`** in `sync-portal-rosters.mjs` | New shared testers default on. |
| **Matrix `adminCheatsEnabled` prop** gates `rowOpQuickFillExpression` and **Use answer** (`showAdminCheats`) | Single gate from portal → session hook → overlay. |
| **Deleted** `GuidedPracticeAdminNav`, `guided-practice-admin-cheat.ts` (+ tests), all `submitCorrectAnswer` wiring | Chase explicitly rejected button/step-skip cheats. |
| **Unguided practice:** no cheat button wiring at all | Cheats are guided-practice typing shortcuts only. |

---

## 4. Rejected directions (do not rediscover)

| Tried / discussed | Why wrong |
|---|---|
| **“Submit correct answer” / step-skip admin nav** | Chase wants typing shortcuts only, not whole-answer or step jumps. |
| **Dev jumps / Back-Next as cheat path** | Same — not acceptable cheat surfaces. |
| **Cheat toggle for enrolled students** | Students always off; RPC cannot enable for non-testers. |
| **`hasAdminCheats` granting instructor portal bypass** | Cheat flag is shortcuts only; instructor bypass stays on `is_instructor`. |
| **Leaving unguided “Answer correctly” button** | Removed entirely from `UnguidedPracticeProblemNav`. |

---

## 5. Current implementation state

### student-session-kit (migrations pushed via `npm run db:push`)

| File | Role |
|---|---|
| `048_student_cheat_enabled.sql` | Column + list/set RPCs; extends `claim_student` / `log_portal_sign_in` |
| `049_tester_cheat_default_on.sql` | All testers `cheat_enabled = true`; sign-in returns cheat only for testers |
| `scripts/sync-portal-rosters.mjs` | New testers upsert with `cheat_enabled: true` |

**Note:** Repo also has **unpushed** migrations 043–047 (practice archive / unguided / abandon) from the broader practice arc — separate from cheat work but same dirty tree.

### student-portal

| File | Role |
|---|---|
| `src/config/portalAccess.ts` | `hasAdminCheats()` |
| `src/config/portalAccess.test.ts` | 3 unit tests |
| `src/services/studentIdentity.ts` | Store/read `cheatEnabled` in localStorage |
| `src/hooks/useStudentIdentity.ts`, `portalLoginEvents.ts` | Pass cheat flag from sign-in |
| `src/features/guided-practice/GuidedPracticeView.tsx` | `adminCheatsEnabled={hasAdminCheats()}` to Matrix embed |
| `src/features/guided-practice/UnguidedPracticeView.tsx` | Cheat button wiring removed |
| `UnguidedPracticeProblemNav.tsx` | `onAnswerCorrectly` / button removed |
| **Deleted:** `GuidedPracticeAdminNav.tsx` | Admin step nav removed |

### Matrix app

| File | Role |
|---|---|
| `GuidedPracticeSolver.tsx` | Passes `adminCheatsEnabled` into session hook |
| `guided-practice-session-types.ts` | `adminCheatsEnabled` on session options |
| `use-guided-practice-session-builder.ts` | Gates `rowOpQuickFillExpression` |
| `use-guided-practice-session.ts` | Threads prop |
| `GuidedPracticeOverlay.tsx` | `showAdminCheats` gates **Use answer** |
| **Deleted:** `guided-practice-admin-cheat.ts`, `.test.ts` | Whole-answer cheat removed |

### Macro App (Teacher Console)

| File | Role |
|---|---|
| `electron-app/student-progress-io.js` | IPC: `listStudentCheatEnabled`, `setStudentCheatEnabled` |
| `electron-app/preload.js`, `macroAppStudentProgress.d.ts` | Preload + types |
| `studentProgressCheatService.ts` | Service layer |
| `useTesterCheatFlags.ts` | Hook |
| `useMacroAppStudentProgressShell.ts` | Wires hook |
| `PreviewTesterCard.tsx` | **Cheat enabled** checkbox (default display `!== false`) |
| `PreviewTesterPanel.tsx`, workspace screens | Pass cheat props |
| `teacher-console-workspaces.css` | Checkbox layout |

**Optional not done:** cheat column on `ConsoleRosterScreen.tsx` testers table (plan noted as optional).

**Note:** Macro App dirty tree includes **practice archive** work (`PracticeArchivePanel`, `useSectionActivityArchive`, etc.) — same session arc, separate deliverable.

### Verification already run

- **student-portal:** full suite **47 passed** (16 files); `portalAccess` **3 passed**
- **Matrix app:** guided-practice **60 passed** (13 files); admin-cheat test removed with deleted module
- **Migrations 048 + 049:** pushed to Supabase
- **No commit, no push, no Netlify deploy**

### Git state (uncommitted)

All four repos above have dirty trees. Cheat-specific paths listed above; run `git status` in each repo before scoped work — **do not assume** only cheat files changed.

---

## 6. Open questions and constraints

1. **Chase has not live-verified:** Teacher Console checkbox → tester reload → guided practice shows Use answer + notation prefill; regular student → no shortcuts.
2. **Toggle is sign-in scoped** — tester must reload portal after Console change.
3. **Deploy:** student-portal (+ Matrix if bundled separately) only when Chase asks; hard-refresh production after.
4. **Frozen:** Calendar 2.0 — do not touch.
5. **Paused thread:** Practice archive gap analysis (`2026-09-20_practice-archive-gap-analysis.md`) — not active unless Chase switches back.
6. **Row-notation UX** from earlier today remains in place; don't reopen help-trigger drag/click split or notation nowrap unless Chase reports issues.

---

## 7. Exact next step

**Chase manual verify (local dev):**

1. **Macro App** → Teacher Console → Preview workspace → toggle **Cheat enabled** on a tester card.
2. **student-portal** (`npm run dev`) → sign in as that tester (fresh reload) → open guided practice.
3. Confirm: **Use answer** visible on matrix steps; row-op notation prefill works; **no** Submit correct answer button or admin nav bar.
4. Sign in as regular enrolled student → confirm **no** shortcuts.

If good → Chase says deploy / put on GitHub. If not → report which role, which step, what appeared vs expected.

---

## Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` (sign-in RPCs, service_role pattern)
3. `student-portal/src/config/portalAccess.ts` + `GuidedPracticeView.tsx`
4. `Macro App/renderer/src/components/teacher-console/PreviewTesterCard.tsx`
5. `Matrix app/src/app/components/guided-practice/GuidedPracticeOverlay.tsx` + `use-guided-practice-session-builder.ts`

## Dev workflow

```powershell
# student-portal (embeds Matrix app via Vite alias @matrix/)
cd "C:\Users\chase\Documents\Programs\School Scrips\student-portal"
npm run dev

# Macro App — Teacher Console (Electron; ask before launching if not already open)
# cd "C:\Users\chase\Documents\Programs\School Scrips\Macro App"
# npm run dev   # only if Chase approves visible launch
```

Hard refresh portal after sign-in or code changes.

## Copy-ready context for Chase

When reporting: tester label vs student, cheat checkbox state, whether portal was reloaded after toggle, which guided-practice step, and whether Use answer / notation prefill appeared.
