# Momentum handoff — Practice mode UI (match guided solution step)

**Written:** 2026-09-20 (Sunday, ~12:35 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **Method Practice** in student portal — one tile, two modes on home (**Guided Practice** + **Practice**), shared 20-problem bank, resume + “another problem?” modal.

**Phase:** **Backend / flow complete; Practice UI polish NOT done.** Problem bank, guided draw-from-bank, unguided attempt tracking, home rework, assignment fixes, and DB migration are in place. **Practice (unguided) works functionally** but **looks wrong** — it uses a centered stack layout instead of matching the guided mode’s **final solution step**.

**Chase’s next ask (explicit — do NOT skip):** Make Practice look **exactly the same** as guided mode at the solution step. **Do not redesign** — copy the existing layout and interaction.

---

## 2. Chase's desired feel (use his language)

- Practice should **look like what the final solution step looks like** in guided mode: **matrix + ordered pair in the corner** (same horizontal row, not centered below the matrix).
- **Flashing / pulsing** empty solution cells until the student picks x or y — same as guided (`solutionPairPulse`).
- **Number builder (“calculator”)** opens **the same way** when tapping a cell — horizontal `BuilderPanel`, same positions/sizing as guided solution step.
- **Instruction copy** (Chase said this via STT — “Josh Jordan” means **Gauss-Jordan**):
  - Top instruction: **“Use Gauss-Jordan elimination to solve. Type in your answers.”**
  - Secondary: **“Tap or click on the ordered pair to enter your answer.”** (Chase also said “under the ordered pair” — match guided wording/placement if they differ; guided engine prompt is in `buildSolutionQuestion`.)
- **No step Back/Next nav** inside the practice workspace (no `GuidedPracticeStepNav`). Portal header **Back** to home is fine.
- **Keep** the two-try solution flow (1st wrong → amber retry; 2nd wrong → reveal answer → `AnotherProblemModal`). Only **layout / presentation** changes.

---

## 3. Accepted decisions (do not re-litigate)

| Decision | Detail |
|---|---|
| One portal tile | `#/matrix/guided-practice` — **not** a second classwork tile |
| Two Supabase activity IDs | Guided: `matrix/guided-practice` · Practice: `matrix/unguided-practice` (migration **043** pushed) |
| Shared problem pool | `problemBank.ts` localStorage `gp-problem-bank:${studentId}` |
| Practice attempt defer | `useResumableAttempt({ deferInitialSave: true })` on unguided — don’t block home on Practice DB init |
| Assignment gate | **Only** block guided at entry; Practice gate inside `UnguidedPracticeView` |
| Home panel | Two sections, Start/Resume each; **no** Restart, **no** skip buttons |
| Exemplar for layout | Guided solution step in `GuidedPracticeSolver.tsx` when `solutionActive` |

---

## 4. Rejected directions — do not redo

- **Centered column layout** in `UnguidedPracticeSolver.tsx` (matrix stacked above prompt/builder) — Chase rejected implicitly (“should look exactly the same”).
- **Blocking entire activity** when `matrix/unguided-practice` fails to load — fixed; don’t restore global gate on `practiceAttempt.blockingMessage`.
- **Old home panel** with `skipButtons.map` — removed; don’t reintroduce skip rows on home.
- **Separate app or renamed assignment** — same tile, same `GUIDED_PRACTICE_ACTIVITY_ID` for access check in `App.tsx`.

---

## 5. Current implementation state

### What works (verify after UI change)

- 20-problem bank + tests (`gauss-jordan-problems.ts`, `problemBank.test.ts`)
- Guided draws `initialMatrix` from bank; dynamic op count per problem
- Home: Guided + Practice sections (`GuidedPracticeHomePanel.tsx` — **147 lines**, new props)
- Unguided: matrix + solution entry + two-try + resume blob (`useUnguidedPracticeAttempt.ts`)
- `AnotherProblemModal` after complete; submit clears resume
- Migration `043_matrix_unguided_practice.sql` — **pushed** to Supabase

### What looks wrong (next task)

| File | Issue |
|---|---|
| `Matrix app/.../UnguidedPracticeSolver.tsx` | Custom vertical layout, inline `<p>` prompt, standalone Submit button — **not** guided solution shell |
| `student-portal/.../UnguidedPracticeView.tsx` | Uses `matrix-embed--unguided-practice` but doesn’t mirror guided workspace chrome (no overlay prompt, no solver class structure) |

### Exemplar files to match (read before editing)

1. **`GuidedPracticeSolver.tsx`** ~314–408 — `solutionActive` branch:
   - `guided-practice-solver` wrapper, `flex items-start gap-3`
   - `GuidedPracticeMatrixDisplay` + `SolutionEntryGrid` **side by side**
   - `BuilderPanel` inline horizontal when field active (`showInlineValueBuilder`)
   - `GuidedPracticeOverlay` for prompt + Submit (absolute layer)
2. **`GuidedPracticeOverlay.tsx`** — `solution-entry` Submit button
3. **`SolutionEntryGrid.tsx`** — pulsing empty cells
4. **`guided-practice.css` / `matrix-embed.css`** — portal sizing for solver inset

### Tests (last known)

- Matrix app: **101** vitest tests pass (includes `unguided-practice-solver.test.tsx`)
- Portal: `problemBank.test.ts`, `guidedPracticeSlots.test.ts` pass
- Portal `npm run build` succeeds
- **No device verify** of new Practice UI — layout still wrong

### Git

- **Uncommitted** across Matrix app, student-portal, student-session-kit (043 migration). Do **not** commit until Chase says “put on GitHub” or end-of-session protocol.

---

## 6. Open questions and constraints

- **Extract shared component?** If duplicating guided layout bloats `UnguidedPracticeSolver`, consider a small shared `GuidedPracticeSolutionLayout` — check file size cap (800) first; prefer matching exemplar over abstraction unless needed.
- **Overlay vs inline prompt:** Guided uses `GuidedPracticeOverlay` + engine `prompt` on question. Practice can pass a static question object or reuse overlay with hardcoded copy — **match visual placement**, not necessarily wire full session hook.
- **Header:** Keep portal Back; omit `GuidedPracticeStepNav` for Practice.
- **Frozen:** Calendar 2.0 — do not touch.
- **Never launch GUI** without Chase’s permission — handoff device checklist as statements.

---

## 7. Exact next step (for fresh agent)

**Rework Practice UI to pixel-match guided final solution step.**

1. Read exemplar: `GuidedPracticeSolver.tsx` (`solutionActive` branch) + `GuidedPracticeOverlay.tsx` (`solution-entry`).
2. Refactor `UnguidedPracticeSolver.tsx` to reuse the **same DOM structure and classes**:
   - Matrix left, `SolutionEntryGrid` right, pulse empty cells
   - Horizontal `BuilderPanel` on cell tap (same `valueSubmitLabel` / commit flow)
   - Prompt text: *“Use Gauss-Jordan elimination to solve. Type in your answers.”* + ordered-pair line
   - Submit positioned like guided (overlay or same flex region — **not** centered below)
3. Update `UnguidedPracticeView.tsx` shell to mirror guided embed (`matrix-embed--with-nav` **without** mounting `GuidedPracticeStepNav`).
4. Preserve two-try logic + `onDraftChange` / `onComplete` props — **behavior unchanged, layout only**.
5. Run Matrix tests + portal build headlessly; give Chase phone verify checklist (below).

**Do NOT** change problem bank, attempt IDs, home panel, or modal flow in this pass unless a layout fix requires a one-line prop wire.

---

## 8. Phone verify checklist (statement for Chase)

1. Home → **Practice** → Start — layout matches guided mode at the **solution** step (matrix + corner ordered pair, not stacked center).
2. Empty x/y cells **pulse** until tapped.
3. Tap cell → **same number builder** as guided; Enter commits value.
4. Wrong once → amber retry; wrong twice → answer shown → **Another problem?** modal.
5. Guided mode still works; home still shows both sections.

---

## Copy-ready navigation path

`latest.md` → `GuidedPracticeSolver.tsx` (solutionActive) → `GuidedPracticeOverlay.tsx` → `UnguidedPracticeSolver.tsx` → `UnguidedPracticeView.tsx` → `guided-practice.css` / `matrix-embed.css`
