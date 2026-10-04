# Momentum handoff — Vector Projections portal + M2412 Teacher Console responses

**Written:** 2026-10-03 (America/Chicago)

---

## Objective and current phase

Chase is shipping **Vectors & Projections** as a **student-portal video-examples activity** with **engagement tracking** (who watched which clips) and a **one-time helpfulness survey**, while **Macro App Teacher Console** shows a **full-class roster grid** (Last/First) plus survey answers and clip-watch data for M2412.

**Phase now:** Portal behavior and credit rules are **implemented locally** (watch credit, autoplay, survey option, navy UI, nav labels, Next-while-playing). **Not deployed** to Netlify in this session chunk. Macro vector responses UI is **local/uncommitted** and mixed with **other unrelated Macro dirty files** — next agent must not assume the whole Macro tree is vector-only.

---

## Chase's desired feel

- **Responses tab must always show the whole roster** — not an empty panel when only a few students engaged. Vector projections: grid is the main “response” surface; survey + clip watches are the data.
- **Survey should not spam** from students clicking **Next** through clips without watching — but students who **actually watch** should still get credit if they **Next early** once they “get it.”
- **Discuss policy before coding** — Chase pushed back when watch rules were implemented without aligning on **20s + ~90%** first; that spec is now coded; don’t revert to “must reach end only” or “Next always denies credit.”
- **Portal nav:** **Exit** → portal home; **Back to clips** from player; no bottom “Back to clips.” Documented in portal + pipeline docs (pipeline note may already be pushed).
- **Visual:** Navy shell (`--portal-navy`) on **all** `portal-quiz--video-examples` (gallery + player); white video/thumbnail windows.
- **Clip titles:** Title case in guide + Macro clip labels.
- **Autoplay:** Picking a clip from **gallery or in-player thumbnail strip** should **start playback**; **Next** already autoplays the following clip. **Previous** still opens paused (not requested).
- **Accessibility:** No typing-heavy flows; modals no backdrop dismiss; no ephemeral “Copied!” toasts.

---

## Accepted decisions

| Decision | Detail |
|---|---|
| Survey after **5 distinct credited clips** | Before opening clip index **5** (6th clip), one-time survey if not completed and that clip not already credited. Constants in `vectorProjectionsSurveyLogic.ts`. |
| Watch **credit** toward survey | **≥ 20s** real playback **and** (**segment ended** **or** **≥ 90%** of clip duration). Credit on **Next** when thresholds met. Logic: `vectorProjectionsWatchCredit.ts`; playback sampled in `useVideoExamplePlayer.ts` (`getPlaybackWatchSeconds`, `getClipDurationSeconds`). |
| Survey answers | Yes / Somewhat / No / **Only looked quickly** (`looked_quickly`). Portal + Macro label map updated. |
| **Next while playing** | Enabled for vector projections (`nextEnabledWhilePlaying` on `VideoExamplesPlayerStage`). |
| **Autoplay** | `openClip(index, { autoPlay: true })` from gallery + strip; Next unchanged. `handleVideoReady` → `playFromStart`. Survey gate preserves `autoPlayPendingRef` through completion. |
| Teacher Console | Dedicated vector projections responses panel + hooks/report utils; exit tickets always roster grid; activity panel routes video kind appropriately. |

---

## Rejected directions (do not redo)

1. **Credit only when `segmentFinished`** with **no credit if Next before end** — wrong for “watched 90% then Next.”
2. **Implementing watch/survey policy without Chase confirming** — caused rework; ask when rules are ambiguous.
3. **Empty Responses view** when roster exists but few submissions — policy is full grid always for this activity class.

---

## Current implementation state

### student-portal (`School Scrips/student-portal`) — **dirty, not deployed**

```
 M VectorProjectionsGuideEntry.tsx      — credit, autoplay, nav, survey flow
 M VectorProjectionsHelpfulSurvey.tsx   — looked_quickly option
 M VideoExamplesPlayerStage.tsx        — nextEnabledWhilePlaying, onVideoReady
 M useVideoExamplePlayer.ts             — playback watch seconds, duration, sampling fixes
 M vectorProjectionsGuide.ts            — title case labels
 M vectorProjectionsSurveyLogic.ts      — 20s min, 0.9 ratio constants
 M vectorProjectionsSurveyService.ts    — looked_quickly type
 M video-examples.css                   — navy theme .portal-quiz--video-examples
?? vectorProjectionsWatchCredit.ts
?? src/test/vectorProjectionsWatchCredit.test.ts   — vitest passes (4 tests)
```

**Deployed earlier (production):** partial vector portal work (clips 3–7, header Exit/Back, survey Continue fix) — **does not include** this session’s credit/autoplay/navy/looked_quickly/watch credit unless redeployed.

**Deploy when Chase asks:** `npm run deploy:prod` in `student-portal` (no browser unless permitted).

### student-session-kit — **uncommitted migration**

```
?? supabase/migrations/070_vector_projections_survey_looked_quickly.sql
```

Summary said **`db:push` applied** on one machine; migration file still **untracked** in repo — **commit/push kit** with portal deploy or when Chase says pull/put on GitHub.

### Macro App — **large dirty tree**

Vector-relevant (new/modified):

- `ActivityResponsesPanel.tsx`
- `VectorProjectionsResponsesPanel.tsx`, `VectorProjectionsResponseGrid.tsx` (new)
- `useVectorProjectionsResponseReport.ts`, `useVectorProjectionClipWatches.ts` (new)
- `vectorProjectionsResponseReport.ts` + test
- `vectorProjectionsHelpfulSurveyReport.ts`, `vectorProjectionsWatchReport.ts` (labels)

**Also modified/untracked:** tutorial onboarding, makeup exam, display scale, gradebook chrome, etc. — **do not commit as one blob** without Chase; prefer **vector-only commit** or confirm scope.

**Verify locally:** restart Macro if IPC stale when testing Teacher Console.

---

## Verification already done

- `vitest run src/test/vectorProjectionsWatchCredit.test.ts` — pass.

---

## Open questions / constraints

- **Deploy portal** — bundles navy, autoplay, credit rules, looked_quickly UI, Next-while-playing, titles.
- **Session-kit 070** — ensure RPC allows `looked_quickly`; file committed and pushed with kit repo.
- **Macro commit scope** — vector responses only vs whole working tree.
- **Previous clip autoplay** — not requested; ask if desired.
- **Constants** — 20s and 90% are Chase-aligned; change only if he says so.
- **No commit/push/deploy** at handoff boundary unless separately requested.
- Read `School Scrips/student-portal/AGENTS.md` and `student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` for Exit/nav conventions.

---

## Read first (next agent)

1. This file.
2. `School Scrips/student-portal/AGENTS.md` (portal patterns).
3. `vectorProjectionsWatchCredit.ts` + `VectorProjectionsGuideEntry.tsx` (credit + autoplay wiring).
4. Macro: `VectorProjectionsResponsesPanel.tsx`, `vectorProjectionsResponseReport.ts`.
5. Root `AGENTS.md` — never display without permission; full **pull** = all repos.

---

## Exact next step

**Deploy student portal to Netlify** (`npm run deploy:prod` in `School Scrips/student-portal`) **after** Chase confirms deploy is OK — then smoke-test one clip (gallery autoplay, watch ~25s, Next with credit, survey option). **In parallel or after:** commit **student-session-kit** migration `070_…looked_quickly.sql` and **student-portal** vector changes; commit **Macro** vector Teacher Console files separately from unrelated dirty Macro work unless Chase wants everything synced.
