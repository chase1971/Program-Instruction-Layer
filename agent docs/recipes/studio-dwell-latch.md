# Studio dwell mechanics (head-mouse / dwell-click)

> **You might say:** "dwell in the Studio", "the React dwell hook", "it clicks before I'm ready"
> **What it is:** Dwell-before-attach timing — reuse hooks; never invent parallel drag logic
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/studio-dwell-mechanics.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `School Scrips/Math App Studio/renderer/src/app/hooks/useDwell*.ts`
- `School Scrips/Math App Studio/renderer/src/app/hooks/dwellEditHandlers.ts`
- `School Scrips/Math App Studio/renderer/src/utils/dwellStationary.ts`
- `School Scrips/Math App Studio/renderer/src/styles/electron.css`

---

Chase uses a **gyro head-mouse + dwell click**. Drag handles must work two ways:

1. **Dwell latch** — hover a handle → attaches; move cursor → pause → drops.
2. **Mouse grab** — press-and-hold on handle → drag immediately; release after moving → drops.

## Single implementation — extend, do not duplicate

| Use case | Hook | Exemplar consumer |
|----------|------|-------------------|
| Move/resize canvas elements (`rectPct`) | `useDwellRectEdit` | `DesignCanvas.tsx` |
| Move floating toolbar panel (px) | `useDwellAttachDrag` | `FloatingToolbar.tsx` |

## Timing — never stated here

All shared timing (latch, release, move threshold, poll interval, hit padding)
lives in **`renderer/src/utils/dwellStationary.ts`**. That file is the owner —
read the constants there, never a number copied into a doc.

Studio's latch timing is deliberately layered on top of the toolbar's OS-level dwell click,
not a copy of it — don't invent a shared value between them. Toolbar timing lives in
`electron-toolbar/modules/dwell/backend/dwell_constants.py` and its own settings.

**Grep before adding** any new drag/attach hook. If you need element move/resize, wire through existing hooks.

## Non-negotiable behaviors

- **`onHandlePointerLeave` is a no-op** on dwell handles. Wobbly head-mouse fires leave constantly; a **poll loop** owns hit-testing via `isPointerOverRect`.
- **`needsExitHandleRef`** — after release, the same handle cannot re-arm until the cursor **physically leaves** it (prevents instant re-latch).
- **Dwell release** only starts after the cursor has **moved** off the latch point (`hasMoved`). Holding still after latch keeps the grab active.
- **Mouse release** — `pointerup` after movement releases; click-without-drag switches to dwell-hold mode.
- Visual feedback: `setDwellHandleState(el, 'arming'|'active'|'none')` → CSS `.dwell-arming` / `.dwell-active` in `electron.css`.

## Adding a new dwell-draggable surface

1. Reuse `useDwellRectEdit` or `useDwellAttachDrag` — do not copy the poll/release state machine.
2. Wire handles: `onPointerEnter` → `startMove` / `startResize` (arms dwell); `onPointerDown` → `grabMove` / `grabResize` (immediate mouse grab).
3. Pass `onRelease` to persist/commit (`onRectCommit` on canvas).
4. Use real pointer coordinates from events — no synthetic mouse simulation.

## Anti-patterns

- Tight stationary thresholds (never latches for head-mouse) — use the constant, not a guess.
- Using `onPointerLeave` to cancel arming (breaks dwell).
- A second drag implementation for “just this one overlay”.
- Hover-only actions with no click path (Chase cannot rely on precise hover).
