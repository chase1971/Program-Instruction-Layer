# Viewport budget layout — measure before you place

> **You might say:** "too big", "I have to scroll", "small scale", "understand the size of
> the app", "padded buttons", "where did that element go", "it doesn't fit on screen",
> "phone viewport", "812×460", "everything has to be smaller"
> **What it is:** Before adding or resizing UI on a fixed viewport, sum element heights
> top-to-bottom against the available pixels. If the stack exceeds the budget, shrink or
> re-layout — do not push content below the fold.

Chase uses a **small landscape phone window** (Portal Wide **812×460** — see
`School Scrips/App Dashboard/docs/LAUNCHER.md` § Chrome window geometries). Many screens
**must not scroll**; the usable height is viewport minus fixed chrome, and that is the entire
budget.

**Exemplar files — read these before writing new code:**

- `School Scrips/student-portal/src/features/guided-practice/GuidedPracticeHomePanel.tsx`
- `School Scrips/student-portal/src/styles/guided-practice.css` (home menu sizing)
- `School Scrips/student-portal/src/utils/matrixTutorialLandscape.ts` (default 812×460)
- `School Scrips/student-portal/src/styles/portal-compact-layout.css` (short-height rescale)

---

## Why it exists

Default web/UI patterns assume a tall desktop page. On a ~460px-tall window, a title +
section label + two padded primary buttons + another section + two full-width skip buttons
**already exceeds the viewport**. Chase cannot scroll reliably with dwell; content below the
fold might as well not exist.

## The procedure (do this before shipping layout)

1. **Name the budget.** Start from the target window height (812×460 for student portal
   landscape). Subtract fixed chrome: quiz header, safe-area/notch inset, shell padding.
   What remains is the content budget — often **~320–380px**, not "the whole phone."
2. **Stack a height estimate.** List every block top-to-bottom: title, gaps, each button row,
   borders, section labels. Use realistic min-heights from CSS (`padding + font-size +
   line-height`), not "feels fine on my monitor."
3. **Check the bottom edge.** If `sum > budget`, you are wrong — **re-layout first** (put
   new controls on the same row as siblings; drop redundant section headers). Shrink padding
   or font only when re-layout is not enough. **Do not squish the whole screen** to fit one
   bad placement — that wastes the viewport Chase already had working.
4. **Use the space you have.** Match the scale of controls already on the screen. A fix for
   overflow is usually horizontal placement, not shrinking everything to 20px chips.
5. **Verify placement.** After edits, ask: "Where is the bottom of the last control relative
   to the viewport bottom?" Use `?layout-debug=1` on student portal (`portal-layout-debug.css`
   outlines `data-layout-frame` regions) or Teacher Console preview at 812×460.

## Non-negotiables

| Rule | Prevents |
|---|---|
| **No surprise scroll on primary menus** | Controls placed off-screen; Chase cannot reach them |
| **Measure; do not guess** | Repeated "make it smaller" passes after every addition |
| **Text-sized controls, not pillow buttons** | Small label + huge `padding` on *new* controls — the default AI failure mode |
| **One row beats a stacked column** | Two full-width buttons stacked = two row heights; put them side-by-side |
| **Do not shrink unrelated UI** | Chase said only the new control was wrong — leave Start/Resume/etc. alone |

## Anti-patterns

- Stacking two new buttons in a column when they fit on one row.
- A new `<h2>` section + border for two skip links that belong in the existing block.
- Shrinking the whole home screen because the *new* rows overflowed — squishing working UI.
- Adding UI without estimating cumulative height — "I'll let Chase scroll if needed."
- Replacing readable labels with 20px chips when the problem was layout, not label length.
- Assuming `min-height` on touch targets from canvas-kit applies here; portal compact menus
  use **much smaller** controls unless Chase confirms on device (`canvas-kit-target-size.md`
  is for canvas overlays, not dense phone menus).

## Relationship to other rules

- **student-portal** compact scale: `src/styles/portal-compact-layout.css` — rescales
  `--quiz-*` variables; do not duplicate markup for landscape.
- **Matrix app / guided practice** phone-first: `School Scrips/Matrix app/AGENTS.md` keyword
  row points here.
- **First paint:** `first-paint-gate.md` — no layout shift; viewport budget — no overflow.
