# Margin teleport buttons — use the side whitespace

> **You might say:** "teleport button", "teleport", "jump to preview", "instructor preview
> shortcut", "put it in the empty space", "don't stack it under the menu"
> **What it is:** Small labeled controls that live in the **horizontal margin** beside a
> centered home card — left and right of the white space — so the main menu never gains
> extra rows or height.

Chase's student portal menus (Transformations Homework, Guided Practice home, Logic home)
center a **narrow card** inside a wide shell. On landscape phone (**812×460**) there is
plenty of unused width. **Teleports belong there**, not in a new section below the title or
as full-width rows under Start/Resume.

**Exemplar files — read before adding teleports:**

- `School Scrips/student-portal/src/app/components/PortalMarginTeleportsLayout.tsx`
- `School Scrips/student-portal/src/styles/portal-margin-teleports.css`
- `School Scrips/student-portal/src/features/transformations/TransformationsHomeworkHomePanel.tsx`
  (Identifying instructor previews: pass result, fail result, post survey)

Also read **`viewport-budget-layout.md`** — teleports are the approved fix for "add a
shortcut" when the vertical stack is already full.

---

## Rules

| Rule | Why |
|---|---|
| **Three-column shell: margin \| card \| margin** | Card keeps `max-width: 26rem`; side columns absorb teleports |
| **Small dot + short label** | Label sits beside the dot — label toward the outer edge, dot toward the card |
| **Never add a `<section>` below the card for teleports** | That steals vertical budget and pushes working UI down |
| **Do not shrink Start/Resume or crush the card into two columns** | Main buttons stay as-is; only margins change |
| **Instructor-only unless Chase says otherwise** | `isInstructorDevice()` in portal; students should not see preview jumps |
| **Wire to existing preview hooks** | Extend `previewIdentifyingResult` / similar — do not duplicate mock data |

## Shape

- **Left margin:** items aligned toward the card (`flex-end`); order `[label][dot]`.
- **Right margin:** items aligned toward the card (`flex-start`); order `[dot][label]`.
- **Stack** multiple teleports vertically within one margin column with tight `gap` (~0.35rem).
- **Variants** (optional color on dot only): `pass` (blue), `fail` (gray), `survey` (amber).

## Anti-patterns

- Full-width teleport buttons under each activity row.
- Dots in the title row that wrap and increase card height.
- Landscape `@media` rules that turn the home card into a 2-column grid.
- Shrinking the whole menu to fit teleports that should have gone in the margin.

## Adding teleports elsewhere

1. Import `PortalMarginTeleportsLayout` and pass `left` / `right` `MarginTeleportItem[]`.
2. Wrap the existing `guided-practice-home__card` (or equivalent) — **do not** move Start/Resume.
3. Add CSS only if a new app needs a different card width; prefer reusing the shell grid.
4. Add a keyword row to that app's `AGENTS.md` if teleports are app-specific.
