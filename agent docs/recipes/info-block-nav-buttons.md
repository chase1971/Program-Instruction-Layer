# Info block Back / Next buttons

> **You might say:** "Back/Next buttons on the info block", "tutorial nav buttons"
> **What it is:** Back / Next tutorial nav buttons — MenuButton look, spec wiring, disabled state
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/info-block-nav-buttons.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `School Scrips/canvas-kit/src/MenuButton.tsx`
- `School Scrips/canvas-kit/src/CanvasButtonLayer.tsx`
- `School Scrips/canvas-kit/src/menuButtonStyles.ts`
- `School Scrips/Math App Studio/renderer/src/utils/infoBlockNavButtons.ts`
- `School Scrips/Math App Studio/renderer/src/app/hooks/useCanvasInfoBlocks.ts`
- `School Scrips/**/screens.json`
- `School Scrips/**/gcfTutorialFilter.ts`

---

Tutorial **Back** and **Next** are standard **menu buttons** nested to an info block — not text links, not outline buttons, not icon-only arrows.

## Visual — use MenuButton (mandatory)

| Layer | Component |
|-------|-----------|
| Live / Preview | `CanvasButtonLayer` → **`MenuButton`** with `fillRect` |
| Studio edit | `MenuButton` `fillRect` inside info block (`DesignCanvasElement.tsx`) |

**Styles come from `canvas-kit/src/menuButtonStyles.ts`** — do not duplicate gradients elsewhere.

| State | Look |
|-------|------|
| **Normal** | Blue gradient `#3b82f6 → #2563eb → #1d4ed8`, white text, 3D shadow (`0 4px 0 #1e40af` + soft drop shadow), `rounded-lg` |
| **Pressed** | Darker gradient, `translateY(2px)`, inset shadow (`ACTIVE_PRESSED`) |
| **Disabled** | Flat light blue gradient `#dbeafe → #bfdbfe`, text `#93c5fd`, `cursor: not-allowed` — via `CanvasButtonLayer` `DISABLED_STYLE` |

**MenuButton classes (fillRect):** `h-full min-h-0 w-full min-w-0 overflow-hidden rounded-lg text-sm font-medium text-white transition-all`

**Wrong:** plain `<button className="border…">`, Tailwind `bg-blue-500` only, circular icon buttons, underline “Back” text.

## Labels and actions (fixed strings)

| Button | `label` | `action` |
|--------|---------|----------|
| Back | **`"Back"`** | `{ "type": "custom", "instruction": "btn-info-back" }` |
| Next | **`"Next"`** | `{ "type": "custom", "instruction": "btn-info-next" }` |

Handler wiring (live app): intercept `btn-info-back` / `btn-info-next` in tutorial screen wrapper — e.g. `GcfTutorialScreen.tsx` → `prevStep()` / `nextStep()`.

## Spec shape (screens.json)

Each nav button is a **screen-level** `buttons[]` entry with **`infoBlockId`** pointing at its info block:

```json
{
  "id": "btn-info-back-1",
  "label": "Back",
  "action": { "type": "custom", "instruction": "btn-info-back" },
  "rectPct": { "xPct": 54, "yPct": 30.9, "wPct": 8, "hPct": 7 },
  "infoBlockId": "info-gcf-step-1",
  "tutorialStep": 1,
  "linkGroupId": "link-gcf-step-1",
  "fontSizePx": 14
}
```

| Field | Rule |
|-------|------|
| `fontSizePx` | **14** on tutorial nav (GCF exemplar) |
| `wPct` / `hPct` | **8 × 7** when synced (Back and Next **same size**) |
| `tutorialStep` | Must match parent info block’s step |
| `linkGroupId` | Shared by Back+Next pair; `buttonLinkGroups[id].syncSize: true`, `alignRow: true` |
| `variant` | Omit (default menu) — **not** `exit` |

**Exit** is a separate red button (`variant: "exit"`) — top-left, not inside the info block row.

## Placement (bottom row of info block)

**Helpers (Studio):** `infoBlockNavButtonRects()` / `useCanvasInfoBlocks.addInfoBlockElement()` in `infoBlockNavButtons.ts`.

| Position | Rule |
|----------|------|
| Row Y | Near **bottom inside** block — `yPct ≈ block.yPct + block.hPct - hPct - 2` |
| Back | **Left** — `xPct ≈ block.xPct + 4` |
| Next | **Right** — `xPct ≈ block.xPct + block.wPct - wPct - 4` |
| Width | ~38% of block width, clamped (`repairInfoBlockNavButtons` syncs pair) |

Coordinates are **screen-space** `rectPct`; canvas-kit converts to local via `rectPctToLocal` when rendering inside the block.

## Disabled behavior (runtime, not spec)

Tutorial filter sets `disabled: true` on:

- **Back** when `step <= 0` (first step)
- **Next** when `navLocked` (animation sequence still running)

Exemplar: `gcfTutorialFilter.ts` → `filterGcfTutorialScreen`. Disabled buttons use **`CanvasButtonLayer`** disabled branch — same size, grayed gradient (not hidden).

## Creating a new step’s nav pair

1. Add info block with `tutorialStep: N`.
2. Add **Back** + **Next** buttons with matching `infoBlockId`, `tutorialStep: N`, instructions above.
3. Run / call **`repairInfoBlockNavButtons(screen)`** to sync sizes and link group.
4. For series: **`applyInfoBlockButtonLayoutToSeries()`** copies layout from one block to siblings.

## Anti-patterns

- Custom button styling instead of `MenuButton` / `CanvasButtonLayer`.
- Different Back vs Next sizes on the same step.
- `navigate` action instead of `btn-info-back` / `btn-info-next` for tutorial steps.
- Hiding Next while locked instead of showing disabled MenuButton.
- Placing nav buttons as top-level buttons without `infoBlockId`.
