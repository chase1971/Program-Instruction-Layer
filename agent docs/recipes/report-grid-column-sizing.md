# Report grid column sizing

> **When:** Teacher Console read-only grids (Matrix report, exit ticket Responses, Logins week grid), or any gradebook-style table that shows symbols/scores — not the full Enter Grades gradebook.

## Rule

**Report grids hug content.** Do not stretch columns to fill the viewport.

- Add `gradebook-table--natural-width` on the `<table>` (with `gradebook-table`).
- Default column widths should fit the data (Excel-style ~8–12 character name columns; grade-field width for ✓/✗ cells).
- Table sits top-left in the scroll viewport; horizontal scroll when there are many columns.
- Use `useGradebookNameColumns(..., 'report')` for name-column drag — separate storage and a 48px resize floor (not the 80px gradebook floor).

## Do not

- Rely on `.gradebook-table { min-width: 100% }` for report grids — that spreads columns edge-to-edge.
- Reuse gradebook name-column localStorage for report grids.

## Exemplars

- [`ExitTicketResponseGrid.tsx`](../../School Scrips/Macro App/renderer/src/components/teacher-console/ExitTicketResponseGrid.tsx)
- [`MatrixReportGrid.tsx`](../../School Scrips/Macro App/renderer/src/components/teacher-console/MatrixReportGrid.tsx)
- CSS: [`table-grid.css`](../../School Scrips/Macro App/renderer/src/styles/gradebook/table-grid.css) — `.gradebook-table--natural-width`

## Full gradebook exception

Enter Grades and Manage Grades **keep** `min-width: 100%` — those workspaces are meant to fill the frame.
