# Report grid layout

> **When:** Teacher Console read-only grids (Matrix report, exit ticket Responses, Logins week grid), or any gradebook-style table that shows symbols/scores — not the full Enter Grades gradebook.
>
> **Chase might say:** report grid · compact grid · matrix report · logins table · exit ticket responses · gradebook-style grid · table doesn't fill the screen · grid scroll

Read this **before** grepping for scroll-frame CSS or inventing column widths.

---

## Why this exists

Report grids share one shell: **arrow pad + scroll viewport + natural-width table**. Logins was built before the scroll-frame half was written down, so the table stopped at content height instead of filling the workspace. Copy the exemplar stack; do not assemble a one-off layout.

---

## 1 — Scroll frame (fill the workspace)

The grid must stretch to the bottom of the Teacher Console body; only the roster scrolls inside the bordered viewport.

### Component stack (copy in order)

1. **Screen** — `section.teacher-console-screen.teacher-console-screen--matrix-report` (or `--logins` with the logins CSS block).
2. **Scroll shell** — `MatrixReportScrollFrame` or `LoginsScrollFrame` (`gradebook-scroll-frame matrix-report-scroll-frame matrix-report-scroll-frame--compact`).
3. **Viewport** — `ViewportScrollFrame` with these classes:
   - `className`: `teacher-console-scroll-frame matrix-report-scroll …`
   - `viewportClassName`: `teacher-console-scroll-viewport … gradebook-scroll-frame__viewport`
4. **Table** — `<table className="gradebook-table gradebook-table--natural-width …">`

### Required CSS flex chain

Screen and workspace body must participate in flex:

- `.teacher-console-workspace__body > .teacher-console-screen--matrix-report` (or `--logins`) → `flex: 1; min-height: 0; align-self: stretch`
- `.matrix-report-scroll-frame` inside the screen → `flex: 1; min-height: 0`
- `.viewport-scroll-frame` / `.matrix-report-scroll` → `flex: 1; min-height: 0`
- `.viewport-scroll-frame__viewport` / `.gradebook-scroll-frame__viewport` → `flex: 1; min-height: 0; max-height: 100%`

CSS owners: [`teacher-console-matrix-report.css`](../../School%20Scrips/Macro%20App/renderer/src/styles/teacher-console-matrix-report.css), [`teacher-console-grades.css`](../../School%20Scrips/Macro%20App/renderer/src/styles/teacher-console-grades.css) (§ logins).

### Scrolling

- **Vertical:** `GradebookArrowPad` in the left rail (`viewportRef` + up/down). See [vertical-scroll-rail.md](./vertical-scroll-rail.md).
- **Horizontal (many columns):** left/right on the arrow pad pages columns (matrix / exit ticket). Logins uses left/right for **week** navigation instead.

### Do not

- Position the tooltip or viewport with SVG viewBox percentages — see §4.
- Omit `gradebook-scroll-frame__viewport` on the scroll viewport — the table will not fill height.
- Use default `.teacher-console-screen` padding on a full-height grid screen without the compact override.

---

## 2 — Column sizing

**Report grids hug content.** Do not stretch columns to fill the viewport.

- Add `gradebook-table--natural-width` on the `<table>` (with `gradebook-table`).
- Default column widths should fit the data (Excel-style ~8–12 character name columns; grade-field width for ✓/✗ cells).
- Table sits top-left in the scroll viewport; horizontal scroll when there are many columns.
- Use `useGradebookNameColumns(..., 'report')` for name-column drag — separate storage and a **48px** resize floor (not the 80px gradebook floor).

### Do not

- Rely on `.gradebook-table { min-width: 100% }` for report grids — that spreads columns edge-to-edge.
- Reuse gradebook name-column localStorage for report grids.

---

## 3 — Full gradebook exception

Enter Grades and Manage Grades **keep** `min-width: 100%` — those workspaces are meant to fill the frame width, not hug content.

---

## 4 — Hover tooltips (charts and grids)

Chase runs Windows display **zoom ~175%**. Tooltips positioned with CSS `%` inside an SVG-scaled container **will not** line up with the bar or cell.

**Rule:** portal to `document.body`, `position: fixed`, place with `anchorEl.getBoundingClientRect()` in `useLayoutEffect`. Viewport coordinates already include zoom — do not multiply by `devicePixelRatio`.

Exemplar: [`GradebookCombinedGradeHoverTooltip.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/gradebook/GradebookCombinedGradeHoverTooltip.tsx)

For SVG bars, use the bar `<rect>` (or hit-area rect) as `anchorEl` — `SVGElement.getBoundingClientRect()` works.

**SVG stacking:** if a visible bar `<rect>` is drawn on top of a full-column invisible hit target, the bar steals pointer events and hover only fires in the empty space above the bar. Fix: bottom-align the hit target to the bar (`pointer-events` on the visible bar → `none`), or put handlers on the visible bar directly.

### Do not

- Put `position: absolute; left: N%` on a tooltip sibling of a `viewBox`-scaled SVG.
- Assume hover tooltips track the cursor — anchor to the bar/cell, clamp to viewport.
- Use a full-column-height invisible hit rect under a visible bar — hover will miss the bar itself.

---

## Exemplars

| What | File |
|---|---|
| Matrix report screen | [`ConsoleMatrixReportScreen.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/teacher-console/screens/ConsoleMatrixReportScreen.tsx) |
| Exit ticket responses | [`ConsoleExitTicketResponseScreen.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/teacher-console/screens/ConsoleExitTicketResponseScreen.tsx) |
| Logins week grid | [`ConsoleLoginsScreen.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/teacher-console/screens/ConsoleLoginsScreen.tsx) + [`LoginsWeekGrid.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/teacher-console/LoginsWeekGrid.tsx) |
| Scroll shell | [`MatrixReportScrollFrame.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/teacher-console/MatrixReportScrollFrame.tsx) |
| Grid tables | [`MatrixReportGrid.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/teacher-console/MatrixReportGrid.tsx), [`ExitTicketResponseGrid.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/teacher-console/ExitTicketResponseGrid.tsx) |
| Natural-width CSS | [`table-grid.css`](../../School%20Scrips/Macro%20App/renderer/src/styles/gradebook/table-grid.css) — `.gradebook-table--natural-width` |
| Portaled hover tooltip | [`GradebookCombinedGradeHoverTooltip.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/gradebook/GradebookCombinedGradeHoverTooltip.tsx) |
| Dashboard logins chart tooltip | [`DashboardLoginsPreview.tsx`](../../School%20Scrips/Macro%20App/renderer/src/components/teacher-console/dashboard/DashboardLoginsPreview.tsx) |
