# First-paint gate — paint the screen once

> **When Chase says:** "pop-in", "things load in after", "paint all at once",
> "staged load", "layout shift on open".

## The failure mode

Several async pieces (identity, roster, classwork, exit tickets, logins, …) each
resolve on their own schedule. If each section renders `null` or a placeholder
while waiting, the screen **grows in stages** — banner first, then text, then
tiles. Chase reads that as pop-in.

## The rule

**Hold the whole screen until every piece that belongs on the first frame is
ready, then paint once.**

- Waiting state: empty shell or a single neutral background — **not** a subset of
  the final layout.
- Warm cache: read cached data **during render** so a return visit pays no extra
  frame (see student-portal classwork snapshot).
- Do **not** cache error results — transient failures must retry on the next open.

## Exemplars

| App | Gate hook | What it waits for |
|---|---|---|
| **student-portal** | `src/hooks/usePortalFirstPaint.ts` | identity + app access + classwork |
| **Macro App Teacher Console dashboard** | `renderer/src/hooks/teacher-console/useTeacherConsoleDashboardFirstPaint.ts` | portal maps + exit tickets + announcements + logins chart |
| **Macro App exit ticket quiz editor** | `ConsoleExitTicketQuizScreen.tsx` + `useExitTicketQuizEdit.ts` session cache | ticket metadata + questions before edit form paints |

## How to implement

1. List every async input on the first screen.
2. Fetch them in parallel from the shell (or a dedicated data hook), not from
   nested cards that paint independently.
3. Export one `firstPaintReady` boolean — true only when all required inputs
   have settled (success **or** failure; never hang forever).
4. Parent screen returns an empty shell until `firstPaintReady`, then renders
   the full layout in one pass.

## Anti-patterns

- `isLoading ? null : <Tiles />` inside each card on the same screen.
- `aria-busy` on one card while siblings are already visible.
- Caching error state so a retry never runs after a gateway timeout.
