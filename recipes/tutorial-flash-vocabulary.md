# Tutorial flash vocabulary

> **You might say:** "make the word flash", "blue pulse", "vocabulary highlight"
> **What it is:** Tutorial flash vs pop — infinite blue pulse; step-driven wiring (no custom animations)
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/tutorial-flash-vocabulary.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `School Scrips/**/gcf-tutorial/**`
- `School Scrips/**/styles/index.css`
- `School Scrips/**/styles/theme.css`
- `School Scrips/**/docs/TUTORIAL_FLASH.md`

---

When Chase says **“flash”** an element during a tutorial step, this is the **only** approved look and wiring. Do not invent yellow highlights, opacity toggles, or one-off CSS.

## Flash = infinite blue pulse

| Property | Value |
|----------|-------|
| Meaning | Target **pulses blue forever** while that tutorial step is active |
| CSS class | `.animate-tutorial-pulse` |
| Keyframes | `tutorial-pulse-blue` — 1.5s, `ease-in-out`, **infinite** |
| Effect | Blue box-shadow ring + slight scale to 1.05 at midpoint |
| Defined in | App `src/styles/index.css` or `theme.css` (same class in Fractions, Matrix, Logic, Transformations) |

**Do NOT** use green/red pulse variants unless Chase explicitly asks — default is **blue only** (`.animate-tutorial-pulse`).

## Pop / slide (different words — not “flash”)

| Word | Class | When |
|------|-------|------|
| **Pop** | `.animate-gcf-pop-in` (or app-specific pop) | One-shot appear (divisors, labels, arrows) |
| **Slide** | `.animate-gcf-slide-in`, `.animate-gcf-paren-slide` | One-shot motion into place |
| **Drop** | `.animate-gcf-quotient-drop` | Quotient terms dropping under columns |

These run **once** when a flag turns true — not tied to “flash while step active.”

## Wiring rule (React state, not DOM hacks)

1. **`flashPartsForStep(stepIndex)`** (or equivalent) returns a `Set` of part ids for that step.
2. Hook exposes **`isFlashing(part) => boolean`** — e.g. `useGcfTutorialFlashes`.
3. Apply pulse in **render** from step state:
   - **KaTeX / HTML:** `\\htmlClass{animate-tutorial-pulse}{content}` via `flashWrap()` in `gcfEquationLatex.ts`
   - **React DOM:** `className={isFlashing('part-id') ? 'animate-tutorial-pulse' : ''}`

**Never** `querySelector` + `classList` for tutorial flashes unless matching an existing legacy app pattern elsewhere.

## Exemplar (GCF tutorial — copy this shape)

| File | Role |
|------|------|
| `gcfEquationPhases.ts` | `GcfFlashPart` union + `flashPartsForStep()` |
| `useGcfTutorialFlashes.ts` | `isFlashing`, `showGcfLabelText` |
| `gcfEquationLatex.ts` | `flashWrap()` → `animate-tutorial-pulse` |
| `GcfEquationDisplay.tsx` | Consumes `isFlashing` |
| `docs/TUTORIAL_FLASH.md` | Human glossary |

## Adding flashes to a new tutorial

1. Add part ids to a typed union (like `GcfFlashPart`).
2. Map steps → parts in one function (`flashPartsForStep`).
3. Reuse existing `.animate-tutorial-pulse` CSS — **copy keyframes** from Solving Quadratics or Matrix `theme.css` if the app lacks them.
4. Timed sequences (division, etc.) live in a separate animation hook; **Next** may disable until sequence ends (`navLocked`) — see info-block nav rule.

## Anti-patterns

- Custom `@keyframes` for “flash” that aren’t `tutorial-pulse-blue`.
- Always-on pulse with no step filter.
- Replacing pulse with border highlight or background color swap.
- Calling any one-shot pop animation a “flash.”
