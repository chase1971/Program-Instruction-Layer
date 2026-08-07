# Edit mode — underlay + edit layer contract

> **You might say:** "the element vanishes when I click it in edit mode", "edit chrome"
> **What it is:** Edit-mode two-layer contract — underlay + edit chrome must stay in sync
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/edit-underlay-layer-contract.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `School Scrips/Math App Studio/renderer/src/app/components/DesignCanvas*.tsx`
- `School Scrips/Math App Studio/renderer/src/app/components/EditCanvasUnderlay.tsx`
- `School Scrips/Math App Studio/renderer/src/app/components/StudioCanvasArea.tsx`
- `School Scrips/Math App Studio/renderer/src/app/components/ButtonArrayOverlay.tsx`
- `School Scrips/Math App Studio/renderer/src/utils/editLiveLayer.ts`
- `School Scrips/canvas-kit/src/**`

---

Edit mode stacks **two layers** on the design canvas:



1. **Underlay** — `EditCanvasUnderlay` + `@canvas-kit` `CanvasRenderer` (frozen live look)

2. **Edit chrome** — `DesignCanvasElement` / `DesignCanvasWidget` / `ButtonArrayOverlay` (select, drag, resize, dock)



Both use the same lens screen: `composeScreenForEventTab()` in `StudioCanvasArea`.



**Single source of truth:** `renderer/src/utils/editLiveLayer.ts`



## The rule (covers all static elements + future buttons/modals/grids)



| Element kind | Underlay when selected | Edit layer when `liveAppearance` |

|--------------|------------------------|----------------------------------|

| **Button, modal, button-grid, widget** | **Always renders** (never omit) | Transparent hit target + selection chrome only — **never** repaint MenuButton/modal card |

| **Title, info-block, text-block** | Omits **only when that element is selected** (inline edit) | Paints EditableText while selected; transparent hit target otherwise |



This prevents the “vanish on click” class of bugs: static visuals never depend on the edit layer repainting them.



## Adding a new element type



1. **`canvas-kit`** — add a layer in `CanvasRenderer.tsx` if it appears in Preview/Live.

2. **`DesignCanvasElement.tsx` or dedicated component** — wire through `shouldUseLiveHitTargetOnly` / `shouldPaintVisualOnEditLayer` from `editLiveLayer.ts`.

   - If it is **static** (like a button): add nothing to `INLINE_EDIT_ELEMENT_TYPES` — underlay handles visuals automatically.

   - If it needs **inline text edit**: add the type to `INLINE_EDIT_ELEMENT_TYPES` and implement the editable branch.

3. **`DesignCanvasElements.tsx`** — mount the element with `liveAppearance={liveAppearance}`.

4. **Smoke-test** — click element → stays visible; click away → no double ghost.



## Key files



| Role | File |

|------|------|

| Rules (one place) | `renderer/src/utils/editLiveLayer.ts` |

| Underlay omit | `renderer/src/app/components/EditCanvasUnderlay.tsx` |

| Edit chrome | `renderer/src/app/components/DesignCanvasElement.tsx` |

| Wiring | `renderer/src/app/components/DesignCanvasElements.tsx` |

| Live render | `canvas-kit/src/CanvasRenderer.tsx` |



## Anti-patterns



- Omitting buttons/modals/grids from the underlay when selected (causes vanish unless edit repaints).

- Edit layer drawing visible MenuButton/modal shells when `liveAppearance` is on (double-stack ghosting).

- Per-element omit/paint logic outside `editLiveLayer.ts`.

- Fixing vanish bugs in `screens.json` — renderer/canvas-kit only.


