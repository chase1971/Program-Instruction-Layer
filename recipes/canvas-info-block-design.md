# Info block design (instruction boxes)

> **You might say:** "the blue instruction box", "info block", "step badge"
> **What it is:** Info block visual design — blue card, step badge, typography (canvas-kit + Studio)
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/canvas-info-block-design.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `School Scrips/canvas-kit/src/CanvasInfoBlockLayer.tsx`
- `School Scrips/canvas-kit/src/InfoBlockVocabText.tsx`
- `School Scrips/Math App Studio/renderer/src/app/components/DesignCanvasElement.tsx`
- `School Scrips/**/screens.json`

---

Tutorial and practice **instruction panels** are **info blocks**. One visual system in **Preview, Live, and Studio Edit** — do not redesign per screen.

## Single source of truth

| Layer | File |
|-------|------|
| **Live / Preview render** | `canvas-kit/src/CanvasInfoBlockLayer.tsx` |
| **Studio edit chrome** | `DesignCanvasElement.tsx` (`elementType === 'info-block'`) — **same classes** |
| **Typography helper** | `infoBlockParagraphStyle()` in `CanvasInfoBlockLayer.tsx` (exported from `@canvas-kit`) |

**Grep before adding** a second info-box component. Extend `CanvasInfoBlockLayer` or the edit-layer branch in `DesignCanvasElement`.

## Card container (exact look)

| Property | Value |
|----------|-------|
| Outer layout | `relative flex h-full w-full flex-col` |
| Border | 2px light blue — `border-2 border-[#93c5fd]` |
| Background | Pale blue — `bg-[#eff6ff]` |
| Corners | `rounded-xl` |
| Padding | `p-2` |
| Overflow | `overflow-visible` on wrappers (vocab tooltips escape the box) |

**Exact shell class string:**

`relative flex h-full w-full flex-col rounded-xl border-2 border-[#93c5fd] bg-[#eff6ff] p-2`

## Step badge (numbered circle)

| Property | Value |
|----------|-------|
| Shape | **Circle** — `h-7 w-7 rounded-full` (only the badge is circular, not resize handles) |
| Fill | `#2563eb` — `bg-[#2563eb]` |
| Border | 3px white — `border-[3px] border-white` |
| Text | White, `text-xs font-bold`, shows `blockNumber` (default 1) |
| Position | `absolute -top-3`, offset **-12px** from left or right edge per `badgeSide` |
| Side | `badgeSide: 'left' \| 'right'` — default **right** if omitted |

## Body text defaults

From `infoBlockParagraphStyle()` / typical GCF spec:

| Field | Default |
|-------|---------|
| `fontSizePx` | **15** |
| `color` | **`#1e3a8a`** (navy blue) |
| `align` | **`center`** (also `left` / `right`) |
| Weight / style | `fontBold`, `fontItalic`, `fontUnderline` when set |

Edit mode: `EditableText` with `className="… leading-relaxed outline-none"` + `infoBlockParagraphStyle(block)`.

## Spec fields (screens.json)

```json
{
  "id": "info-gcf-step-1",
  "text": "…",
  "rectPct": { "xPct": 52, "yPct": 12, "wPct": 44, "hPct": 28 },
  "blockNumber": 1,
  "badgeSide": "left",
  "tutorialStep": 1,
  "seriesId": "series-…",
  "fontSizePx": 15,
  "align": "center",
  "color": "#1e3a8a"
}
```

- **`tutorialStep`** — only this block shows on that step (with matching nav buttons).
- **`seriesId`** — groups blocks for Studio series tools / shared style.
- Default placement helper: `defaultInfoBlockRect()` in Studio `canvasDefaults.ts` (~55% x, 35% w, 18% h) — adjust in Studio, not hardcoded in app code.

## Vocab tooltips inside blocks

- Terms: `InfoBlockVocabText` in canvas-kit — do not rebuild tooltip UI.
- Below-block panel: `vocabPanelRectPct` + `VocabDefinitionPanel` — see Studio tooltip zone rule / `vocabPanelLayout.ts`.

## Anti-patterns

- White/gray cards, dark mode boxes, or shadow-only panels without the blue border.
- Square step badges or missing badge on numbered steps.
- Different border radius (`rounded-lg` vs `rounded-xl`) on live vs edit.
- Inline-styled info paragraphs outside `infoBlockParagraphStyle`.
- A second “InfographicBox” / “InstructionPanel” component.
