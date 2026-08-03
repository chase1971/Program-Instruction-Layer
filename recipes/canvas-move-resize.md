# Canvas element move & resize

> **You might say:** "move/resize a canvas element", "drag handles", "carry mode"
> **What it is:** Canvas element move, resize, and carry — exact visual chrome + hook wiring (no improvised handles)
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/studio-canvas-move-resize.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `School Scrips/Math App Studio/renderer/src/app/components/DesignCanvas*.tsx`
- `School Scrips/Math App Studio/renderer/src/app/components/AnimationStudio.tsx`
- `School Scrips/Math App Studio/renderer/src/app/components/ButtonArrayOverlay.tsx`
- `School Scrips/Math App Studio/renderer/src/app/components/VocabTooltipZoneOverlay.tsx`
- `School Scrips/Math App Studio/renderer/src/app/hooks/useCanvasElementCarry.ts`
- `School Scrips/Math App Studio/renderer/src/utils/designCanvasGeometry.ts`

---

All layout editing uses **`rectPct`** (percent of canvas). One `useDwellRectEdit` instance is created in **`DesignCanvas.tsx`** and passed down as **`DwellEditHandlers`** (`dwellEditHandlers.ts`).

## Visual spec — do NOT improvise (critical)

**Chase expects every surface to look identical.** Do not design your own handles, dots, circles, or corner widgets. **Import the shared parts** or copy their classes **verbatim**.

| Wrong (never do) | Correct (always do) |
|------------------|---------------------|
| Circular resize dots (`rounded-full`, SVG circles) | **Square** navy corner handles (`h-5 w-5`, slight `rounded`) |
| Edge/center resize grips | **Four corners only** (`nw`, `ne`, `sw`, `se`) |
| Custom colors/sizes per feature | Exact tokens below — same in Design canvas, Animation Studio, button grids |
| Inline one-off handle markup | **`ResizeHandles`** + **`MoveHandle`** from `DesignCanvasElementParts.tsx` |

### Resize corner handles (canonical)

**Component:** `ResizeHandles` in `DesignCanvasElementParts.tsx` — **use this component**; do not reimplement.

| Property | Value |
|----------|-------|
| Shape | **Square** 20×20px (`h-5 w-5`) — NOT a circle |
| Corner radius | `rounded` (small) — **never** `rounded-full` |
| Fill | `#2B4C7E` (navy) — `bg-[#2B4C7E]` |
| Border | 2px white — `border-2 border-white` |
| Shadow | `shadow-sm` |
| Cursor | `cursor-grab` |
| z-index | `z-20` |
| Count / placement | 4 corners; offset **10px outside** the element box (`RESIZE_HANDLE_OFFSET_PX = 10`) |
| Exact class string | `absolute z-20 h-5 w-5 cursor-grab rounded border-2 border-white bg-[#2B4C7E] shadow-sm` |

`ButtonArrayOverlay.tsx` duplicates this same class string on purpose — if you cannot use `ResizeHandles`, **paste that exact string**; do not substitute circles.

### Move handle (tool tray)

**Component:** `MoveHandle` in `DesignCanvasElementParts.tsx`.

| Property | Value |
|----------|-------|
| Type | `<button>` labeled **"Move"** (visible text, not icon-only) |
| Size | `min-h-5`, `px-2` |
| Border | Dashed light blue — `border border-dashed border-[#93c5fd]` |
| Background | `#f8fbff` |
| Text | `#1e3a8a`, `text-[10px] font-bold`, `rounded-md` |

### Tool tray row (Copy / Link / Lock / ›)

**Component:** `HandleTray` — Move handle on the left; **›** expand button; extra tools expand on **hover** (1s close delay). Do not use click-to-toggle menus.

**Action buttons:** `ActionHandle` — `min-h-5 min-w-5`, `rounded-md`, `text-[10px] font-bold`; inactive `border-[#cbd5e1] bg-white text-[#334155]`; active lock `border-[#16a34a] bg-[#16a34a] text-white`.

**Tray position:** `absolute z-10 flex items-center gap-1` on handle side (`HANDLE_ROW_POS` in `DesignCanvasElement.tsx`: top / bottom / left / right of element).

### Selection & bounds chrome

| State | Visual |
|-------|--------|
| Selected (layout locked) | `outline outline-[3px] outline-[#2B4C7E]` |
| Size-pick / save-pick / place-pick | Orange / green / blue outline + soft shadow (see `DesignCanvasElement.tsx` `outline` variable) |
| Text/equation bounds (edit) | Inset ring `ring-2 ring-inset ring-[#93c5fd]` on white `rounded-md` background |
| Dim label (unlock + selected) | Mono `% × %` chip: `-bottom-5`, `text-[10px] font-mono text-[#6B7280]` |
| Locked badge | `LockBadge` — 🔒, `-top-7 right-0` |
| Dwell arming / latched | CSS `.dwell-arming` (blue glow) / `.dwell-active` (green fill) on the **handle element** — see `studio-dwell-mechanics.mdc` |

### Button grid overlay ring

When emphasized: `ring-2 ring-[#2B4C7E] ring-offset-1`. Idle: `ring-1 ring-[#93c5fd]/50`. Container: `rounded-lg box-border`.

---

## Two movement modes (do not merge)

| Mode | When | Mechanism |
|------|------|-----------|
| **Handle move/resize** | Layout unlocked + element selected/hovered | `MoveHandle` / `ResizeHandles` → `useDwellRectEdit` |
| **Click-to-carry** | `arrangeMode` (🔓 toolbar) | `useCanvasElementCarry` — pick up on pointer down, drop on canvas click, snap guides |

Both call `onRectChange` / `onRectCommit` — do not write rect updates elsewhere.

## Standard handle wiring

**Exemplar:** `DesignCanvasElement.tsx` → `bindMove`, `bindMoveGrab`, `bindResize`, `bindResizeGrab`

```tsx
// MoveHandle
onPointerEnter → startMove(event, rect, onRectChange, onRectRelease)
onPointerDown  → grabMove(event, rect, onRectChange, onRectRelease)

// ResizeHandles — pass bindResize / bindResizeGrab from exemplar
```

## Resize math

Use **`resizeRectByCorner()`** in `designCanvasGeometry.ts`. Locked elements: `{ anchorCenter: true }`.

## When handles show

```tsx
showResizeHandles = layoutUnlocked && (selected || layoutHovered) && !beingCarried && !suppressLayoutControls
```

## Adding move/resize to a new element type

1. **Import `ResizeHandles` and `MoveHandle`** — do not draw new handle UI.
2. Mount in `DesignCanvasElements.tsx` with `dwellEdit` handlers (copy a sibling element).
3. `rectPctStyle(rect)` from `@canvas-kit`; `onRectChange(..., false)` while dragging; `onRectCommit()` on release.
4. Preview/Live: follow **`edit-underlay-layer-contract.mdc`**.

## Key files

| Role | File |
|------|------|
| **Visual source of truth** | `DesignCanvasElementParts.tsx` |
| Hook instance | `DesignCanvas.tsx` |
| Generic element chrome | `DesignCanvasElement.tsx` |
| Button grids | `ButtonArrayOverlay.tsx` |
| Animation Studio canvas | `AnimationStudio.tsx` (same parts + hooks) |

## Anti-patterns

- **Circular resize handles** or any non-square corner grip.
- Custom handle colors/sizes “that look fine”.
- Skipping `ResizeHandles` / `MoveHandle` because “this overlay is different”.
- Inline pointermove listeners instead of `useDwellRectEdit`.
- Skipping `onRectCommit` on release.
