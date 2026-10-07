# Portal pause and resume — save on every student action

> **You might say:** "save progress", "pause resume", "pick up where they left off",
> "save on every click", "connective pick should resume", "like Transformations Homework"
> **What it is:** Non-negotiable for **every student-portal assignment** — persist after
> each meaningful interaction, restore the exact workspace on Resume, Start fresh abandons
> the in-progress attempt when there is real progress.

**Exemplar files — read these before wiring a new portal app:**

| Layer | Exemplar |
|---|---|
| Portal shell | `School Scrips/student-portal/src/hooks/useResumableAttempt.ts` |
| Portal attempt hook | `School Scrips/student-portal/src/features/transformations/useTransformationsIdentifyingAttempt.ts` |
| Embed — save on state change | `School Scrips/transformations-app/src/app/hooks/useIdentifyingTransformations.ts` (`emitPortalProgress` + `useEffect` deps) |
| Embed — sub-step snapshot | `School Scrips/transformations-app/src/app/hooks/useGraphingEmbedProgress.ts` |
| Logic Homework (truth table) | `School Scrips/logic-app/src/app/hooks/useLogicProblemPortalSync.ts` + `portal/logicActiveProblem.ts` |

Student-portal policy (orchestrator only): `School Scrips/student-portal/AGENTS.md` § Pause and resume.

---

## Rules (absolute)

1. **One save path** — `useResumableAttempt` + `saveProgress(index, blob)` in the feature
   attempt hook. No second persistence mechanism.
2. **Save on every meaningful interaction** — not only on "Next problem" or submit. Examples:
   connective picked, cell toggled, stage advanced, intro dismissed. If the student would
   notice they lost work when reopening, that action must have triggered a save.
3. **Blob must restore the workspace** — problem index alone is not enough. Serialize enough
   embed state to repaint the same screen (columns, picker open, in-progress answers).
4. **Resume enables when any real progress exists** — feature `canResume` / `*HasMeaningfulProgress`
   must include mid-problem work, not only completed items.
5. **Start fresh** — abandon in-progress attempt when meaningful progress exists (see
   Transformations / Logic `abandonIfNeeded` patterns).
6. **Submit** — pass `resumeProgress` into `submitCompletedAttempt` so a failed submit does
   not wipe the blob.

## Embed implementation pattern

1. Define a versioned progress type (`*ProgressV1`) in the embed package under `portal/`.
2. Expose `portalHost.onProgress(snapshot)` from the portal attempt hook → `saveProgress`.
3. In the embed, call `onProgress` from a **`useEffect` whose dependencies are every piece of
   state that must survive resume** (mirror Identifying / Graphing / Logic hooks).
4. On restore, apply the blob **once** (`hasAppliedRestoreRef`), then allow saves again — avoid
   infinite loops when the parent mirrors `restoredProgress` (see Identifying restore tests).
5. Keep `portalHost` identity stable in the parent (`useMemo`); use refs for callbacks if needed.
   **Never** put a fresh `{ ...portalHost }` inline on every render — the embed save
   `useEffect` will treat it as changed every time and loop (`Maximum update depth exceeded`).
6. Do **not** reset `hasAppliedRestoreRef` on every render when `restoredProgress` is null;
   apply restore once per blob (exemplar: Identifying restore tests).

## Adding a new portal app

1. Copy the **generic-quiz** or **Transformations Homework** feature folder shape.
2. Wire `useResumableAttempt` in `use*Attempt.ts`.
3. Add Start / Resume home UI (Transformations / Logic home panels are exemplars).
4. Implement embed snapshot + restore before shipping.

## Related

- Pipeline overview: `School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`
- No layout shift on reopen: [first-paint-gate.md](./first-paint-gate.md)
