# Modal/Dialog Pattern

> **You might say:** "new modal", "make it look like that modal", "the modal is too wide", "it closes when I click outside", "modal over the browser", "PAUSED stuck", "snapshot/freeze"
> **What it is:** The standard modal/dialog/wizard shell: max-w-md, no backdrop dismiss, design to fit without scrolling.

**Exemplar files — read these before writing new code:**

- `School Scrips/Macro App/renderer/src/components/ModalContainer.tsx` — follows the rules already; prefer it
- `School Scrips/Macro App/renderer/src/components/ModalPortal.tsx` — the real portal component (not `portals/PortalLayer`, which doesn't exist)
- `School Scrips/Macro App/renderer/src/components/ViewportScrollFrame.tsx` — for genuinely unbounded lists
- `School Scrips/Macro App/renderer/src/components/gradebook/CategoryWeightsModal.tsx` — multi-column, fits without a scrollbar

---

## Macro App: modal over the embedded browser (read first)

**If the modal appears while the Browser tab / embedded D2L view is visible, sizing and
`ModalContainer` alone are not enough.** You must also follow the snapshot/freeze pattern or
the user can get stuck with **PAUSED** on the browser and **no way to close anything** except
restarting the app.

**Before writing or changing that modal, read:**

`School Scrips/Macro App/docs/EMBEDDED_BROWSER_AND_MODALS.md`

That doc is the owner for freeze order, `unfreeze()` on every close path, and why nothing may
reattach the live browser while a modal overlay is open.

### Mandatory checklist (Macro App browser-panel modals)

1. **Read** `EMBEDDED_BROWSER_AND_MODALS.md` § Seamless snapshot modals.
2. **Freeze before open** — `await freezeBrowserBeforeOverlay(browserModal, 'label')` then
   `flushSync(() => setModalOpen(true))`. Never `setModalOpen(true)` first and freeze in
   `useEffect`.
3. **Unfreeze on every close path** — Cancel, OK, error, and handoff to live browser work.
   Pair with `useStableBrowserModalFreeze({ preFrozenOnOpen: true })` when you pre-freeze on
   open.
4. **Exemplars:** `useManageWorkspaceTabsModal.ts`, `useRenameCoursesModal.ts`,
   `useMacroAppTabHandlers.ts` (setup/retire/clear).
5. **Live browser during the flow** — close the modal and `unfreeze()` before visible D2L
   navigation (bulk pull, setup export). Show progress in the side panel banner instead of
   keeping the modal open over a frozen browser.
6. **Then** apply the sizing / no-backdrop-dismiss rules in the rest of this file.

Skipping step 1–5 produces modals that look fine in code review but brick the app in use.

---

## Critical: Modal Sizing

### ⚠️ Common mistake: modals spanning full width

**Problem:** AI often creates modals that span the entire screen width, making them unusable.
**Root cause:** `w-full` without a `max-w-*` constraint, or an oversized one like `max-w-3xl`,
`max-w-4xl`, `max-w-6xl`.

**Size guidelines:**
- **Standard modals**: `max-w-md` (448px) — most dialogs, forms, confirmations
- **Wide modals**: `max-w-lg` (512px) — wizards with multiple columns or large forms
- **Extra wide (rare)**: `max-w-xl` (576px) — only for complex wizards with many fields
- **Never use**: `max-w-2xl` and above, or `w-full` without a max-width

**Height:** always `max-h-[85vh]`, with `overflow-y-auto` on the content area as a **safety
net** — not the normal scrolling experience.

### Aim for no scrolling (design to fit)

**A scrollbar is a smell, not a solution.** The default goal is a modal whose content fits in
the viewport with everything visible at once. `max-h-[85vh]` + `overflow-y-auto` stay in place
so controls can never leave the screen, but design so they rarely trigger.

This matters extra for dwell-mouse / head-mouse users: scrolling inside a modal is a slow,
error-prone interaction. Showing everything at once is far more accessible.

When a modal is too tall, fix it in this order:

1. **Cut padding and gaps.** Most "too long" modals are mostly whitespace.
2. **Shrink elements.** Smaller fonts, shorter inputs, single-line rows instead of
   stacked label-above-input.
3. **Drop redundant text.** Remove restating helper copy and hints the user already sees.
4. **Split into columns.** Dense lists (categories, settings, per-item rows) belong in a
   multi-column grid, not one tall single column — a wider modal with 2-3 columns usually
   beats a scrolling `max-w-md`.
5. Only after the above, accept scrolling for genuinely unbounded content — prefer
   `ViewportScrollFrame` for those.

Exemplar (Macro App): `CategoryWeightsModal.tsx` — one column per gradebook, compact
single-line rows, trimmed spacing so all categories show without a scrollbar.

### Footer button order

In a **stacked** (single-column) footer, the **primary action goes above Cancel** — e.g.
Macro App's `d2l-picker-actions` column. With a head-mouse, the button nearest the content is
the one the cursor reaches first; putting Cancel there makes the destructive-ish choice the
easy one. Side-by-side footers keep the conventional order.

### No overlay / backdrop dismiss (hard rule)

**Never** close a modal when the user clicks outside the dialog (overlay/backdrop). Do not use
`onClick={onClose}`, `onClick={onCancel}`, or conditional overlay handlers. The user must use
an explicit control: OK, Cancel, Close, Done, etc.

This is required for dwell-mouse and head-mouse users — accidental cursor movement must not
dismiss wizards or half-finished setup flows. Same rule, stated tersely, in root
`AGENTS.md` § "The most violated rules" — this section is the implementation detail for it,
not a competing source.

```tsx
// ✅ CORRECT — overlay is inert; dialog lives on the inner panel
<div className="courses-modal-overlay" role="presentation">
  <div
    className="courses-modal"
    role="dialog"
    aria-modal="true"
    aria-label="Setup courses"
    onClick={(event) => event.stopPropagation()}
  >
    {/* content */}
    <button type="button" onClick={onClose}>OK</button>
  </div>
</div>

// ❌ WRONG — clicking outside closes the modal
<div className="courses-modal-overlay" onClick={onClose}>

// ❌ WRONG — "smart" dismiss only when idle (still fires on dwell-mouse accidents)
<div className="courses-modal-overlay" onClick={() => { if (canDismiss) onClose(); }}>
```

Prefer **`ModalContainer`** in Macro App — it already follows this rule.

---

## Modal Structure Pattern

```tsx
import React from 'react';
import { X } from 'lucide-react';
import { ModalPortal } from '../ModalPortal';

interface MyModalProps {
  isOpen: boolean;
  onClose: () => void;
  theme: { panel: string; border: string; text: string };
}

export default function MyModal({ isOpen, onClose, theme }: MyModalProps) {
  if (!isOpen) return null;

  return (
    <ModalPortal>
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        {/* CRITICAL: max-w-md, not max-w-3xl or larger */}
        <div
          className="w-full max-w-md max-h-[85vh] rounded-lg border shadow-xl overflow-hidden flex flex-col"
          style={{ background: theme.panel, borderColor: theme.border }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-center justify-between p-4 border-b" style={{ borderColor: theme.border }}>
            <h2 className={`text-xl font-bold ${theme.text}`}>Modal Title</h2>
            <button onClick={onClose} className="p-2 rounded-lg border shadow-lg">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-6">
            {/* Modal content here */}
          </div>

          <div className="flex gap-3 p-4 border-t" style={{ borderColor: theme.border }}>
            <button className="flex-1 py-3 px-4 rounded-lg border shadow-lg text-sm font-semibold" onClick={onClose}>Cancel</button>
            <button className="flex-1 py-3 px-4 rounded-lg border shadow-lg text-sm font-semibold">Save</button>
          </div>
        </div>
      </div>
    </ModalPortal>
  );
}
```

`ModalPortal` wraps the modal in the correct DOM layer for z-index stacking — always use it
rather than rendering the modal inline in the component tree.

---

## Multi-step wizards

Prefer showing all steps in one view (or all sections at once with disabled states until
prerequisites are met) over hiding steps one at a time — it keeps the modal scannable and
avoids extra navigation for a head-mouse user:

```tsx
const [step, setStep] = useState<1 | 2 | 3>(1);

<div className="flex flex-col gap-6">
  <div className="flex flex-col gap-3"><h3>Step 1: Upload</h3></div>
  {step >= 2 && <div className="flex flex-col gap-3 border-t pt-4"><h3>Step 2: Configure</h3></div>}
  {step >= 3 && <div className="flex flex-col gap-3 border-t pt-4"><h3>Step 3: Review</h3></div>}
</div>
```

---

## Accessibility

- **Escape**: close modal. **Tab**: navigate focusable elements. **Enter**: submit/confirm.
- **Focus trap**: keep focus within the modal while open.
- `role="dialog"`, `aria-modal="true"`, and an `aria-label` on the close button.

---

## Anti-patterns

```tsx
// ❌ No max-width — spans the whole screen
<div className="w-full">

// ❌ Modal outside ModalPortal — z-index conflicts
<div className="fixed inset-0 z-50">{/* no portal */}</div>

// ❌ No scrollable content area — long content overflows the shell
<div className="p-6">{/* long content, no overflow-y-auto anywhere */}</div>
```

---

## Related Patterns

- [React Patterns](./react-patterns.md) — Component organization, hooks
- [File Headers](./file-headers.md) — Modal component documentation

## Quick Reference

| Modal Type | Max Width | Use Case |
|------------|-----------|----------|
| Confirmation | `max-w-md` | Yes/No dialogs |
| Form | `max-w-md` | Single-column forms |
| Wizard | `max-w-lg` | Multi-step wizards |
| Complex Wizard | `max-w-xl` | Rare — only if absolutely necessary |

**Remember:** always `max-h-[85vh]` for height, `overflow-y-auto` on the content area.

---

## Macro App variant (CSS modals, not Tailwind)

The Macro App renderer does **not** use the Tailwind template above. It uses shared classes in
`School Scrips/Macro App/renderer/src/styles/modals.css`.

Before adding a modal there, read **`School Scrips/Macro App/guidelines/Guidelines.md` § Modals**
and copy an exemplar (`GradesBackupModal.tsx`, `GradebookHistoryModal.tsx`).

**If the modal opens over the embedded Browser tab**, also read
**`School Scrips/Macro App/docs/EMBEDDED_BROWSER_AND_MODALS.md`** (see § Macro App: modal over
the embedded browser above). That is not optional — missing freeze/unfreeze requires an app
restart to recover.

---

## When scrolling is unavoidable (Electron / portal modals)

**Symptom:** Modal overflows the viewport but no scrollbar appears.

**Cause:** Tailwind height utilities (`h-[540px]`, `max-h-[85vh]`) are unreliable in React
portals — JIT may skip them, or `electron.css` / global styles override them.

**Fix:** use **inline styles** for critical height constraints on the modal shell:

```tsx
<div
  className="rounded-lg border shadow-xl flex flex-col"
  style={{ width: '800px', height: '540px', maxHeight: '85vh' }}
>
  <div className="flex-1 flex flex-col overflow-hidden">
    <div className="flex-1 overflow-y-auto p-4">
      {/* scrollable content */}
    </div>
  </div>
</div>
```

Rules:
- Parent of scroll area: `flex-1 overflow-hidden`
- Scroll child: `flex-1 overflow-y-auto`
- Do **not** rely on Tailwind alone for `height` / `maxHeight` in portaled modals
- Prefer designing modals to fit without scrolling (see "Aim for no scrolling" above)

Two-panel layout (sidebar + scroll): fixed-width sidebar (`flex-shrink-0`), right panel uses
the same `overflow-hidden` / `overflow-y-auto` pair. Test with 50+ items when scroll behavior
matters.

---

**Last updated:** 2026-08-08 — fixed a fabricated `ModalPortal` import path and a fabricated
`useModalState` hook that had zero real usages; cut the sizing guidance's fourfold repetition
down to one canonical statement + the Quick Reference table.
