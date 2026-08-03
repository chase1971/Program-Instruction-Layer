# Modal/Dialog Pattern

> **Purpose:** Standard pattern for creating modal dialogs and overlays in React applications
>
> **When to Use:** Any time you need a modal, dialog, confirmation popup, or wizard overlay

---

## Critical: Modal Sizing

### ⚠️ COMMON MISTAKE: Modals Spanning Full Width

**Problem:** AI often creates modals that span the entire screen width, making them unusable.

**Root Cause:** Using `w-full` without `max-w-*` constraint, or using overly large `max-w-*` values like `max-w-3xl`, `max-w-4xl`, or `max-w-6xl`.

### ✅ Correct Modal Sizing

**Standard Modal Width:**
```tsx
// ✅ CORRECT - Standard modal size
<div className="w-full max-w-md max-h-[85vh] rounded-lg border shadow-xl">
  {/* Modal content */}
</div>
```

**Size Guidelines:**
- **Standard modals**: `max-w-md` (448px) - Use for most dialogs, forms, confirmations
- **Wide modals**: `max-w-lg` (512px) - Use for wizards with multiple columns or large forms
- **Extra wide (rare)**: `max-w-xl` (576px) - Only for complex wizards with many fields
- **NEVER use**: `max-w-2xl`, `max-w-3xl`, `max-w-4xl`, `max-w-6xl`, or `w-full` without max-width

**Height:**
- Always use `max-h-[85vh]` to prevent modals from exceeding viewport height
- Use `overflow-y-auto` on content area as a **safety net** — not as the normal scrolling experience

### Aim for NO scrolling (design to fit)

**A scrollbar is a smell, not a solution.** The default goal is a modal whose content fits
in the viewport with everything visible at once. `max-h-[85vh]` + `overflow-y-auto` stay in
place so controls can never leave the screen, but you should design so they rarely trigger.

This matters extra for dwell-mouse / head-mouse users: scrolling inside a modal is a slow,
error-prone interaction. Showing everything at once is far more accessible.

When a modal is too tall, fix it in this order:

1. **Cut padding and gaps.** Tighten section margins, list `gap`, and row padding. Most
   "too long" modals are mostly whitespace.
2. **Shrink elements.** Smaller font sizes, shorter inputs, single-line rows instead of
   stacked label-above-input.
3. **Drop redundant text.** Remove restating helper copy, captions that duplicate the
   control, and hints the user already sees in the field.
4. **Split into columns.** Dense lists (categories, settings, per-item rows) belong in a
   multi-column grid, not one tall single column. A wider modal (`max-w-lg`/fixed width with
   a documented reason) with 2–3 columns usually beats a scrolling `max-w-md`.
5. Only after the above, accept scrolling for genuinely unbounded content (long logs, large
   variable-length lists) — and prefer `ViewportScrollFrame` for those.

Exemplar (Macro App): `CategoryWeightsModal.tsx` — one column per gradebook, compact
single-line rows, trimmed spacing so all categories show without a scrollbar.

### Footer button order

In a **stacked** (single-column) footer, the **primary action goes above Cancel**
— e.g. Macro App's `d2l-picker-actions` column. With a head-mouse, the button
nearest the content is the one the cursor reaches first; putting Cancel there
makes the destructive-ish choice the easy one.

Side-by-side footers keep the conventional order.

### No overlay / backdrop dismiss (hard rule)

**Never** close a modal when the user clicks outside the dialog (overlay/backdrop). Do not use `onClick={onClose}`, `onClick={onCancel}`, or conditional overlay handlers. The user must use an explicit control: OK, Cancel, Close, Done, etc.

This is required for dwell-mouse and head-mouse users — accidental cursor movement must not dismiss wizards or half-finished setup flows.

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

### ❌ Common Mistakes

```tsx
// ❌ WRONG - Spans full width
<div className="w-full max-w-4xl">
  {/* This is way too wide! */}
</div>

// ❌ WRONG - No max-width constraint
<div className="w-full">
  {/* This will span entire screen! */}
</div>

// ❌ WRONG - Too large
<div className="w-full max-w-3xl">
  {/* Still too wide for most modals */}
</div>
```

### ✅ Correct Examples

```tsx
// ✅ Standard modal (most common)
<div className="w-full max-w-md max-h-[85vh] rounded-lg border shadow-xl">
  {/* Content */}
</div>

// ✅ Wide modal (for complex forms)
<div className="w-full max-w-lg max-h-[85vh] rounded-lg border shadow-xl">
  {/* Content */}
</div>

// ✅ Wizard with fixed width (if needed)
<div className="w-[800px] max-h-[85vh] rounded-lg border shadow-xl">
  {/* Content - only use fixed width if absolutely necessary */}
</div>
```

---

## Modal Structure Pattern

### Basic Modal Template

```tsx
import React from 'react';
import { X } from 'lucide-react';
import { ModalPortal } from '../portals/PortalLayer';

interface MyModalProps {
  isOpen: boolean;
  onClose: () => void;
  isDark: boolean;
  theme: {
    panel: string;
    border: string;
    text: string;
    textMuted: string;
  };
  metalButtonClass: (textColor?: string) => string;
  metalButtonStyle: () => Record<string, any>;
  soundEnabled: boolean;
}

export default function MyModal({
  isOpen,
  onClose,
  isDark,
  theme,
  metalButtonClass,
  metalButtonStyle,
  soundEnabled
}: MyModalProps) {
  if (!isOpen) return null;

  const handleClose = () => {
    if (soundEnabled) soundEffects.playButtonClick();
    onClose();
  };

  return (
    <ModalPortal>
      <div
        className="fixed inset-0 z-50 flex items-center justify-center"
      >
        {/* Modal Container - CRITICAL: Use max-w-md, NOT max-w-3xl or larger */}
        <div
          className="w-full max-w-md max-h-[85vh] rounded-lg border shadow-xl overflow-hidden flex flex-col"
          style={{
            background: theme.panel,
            borderColor: theme.border
          }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b" style={{ borderColor: theme.border }}>
            <h2 className={`text-xl font-bold ${theme.text}`}>
              Modal Title
            </h2>
            <button
              onClick={handleClose}
              className={`p-2 rounded-lg transition-all border shadow-lg ${metalButtonClass()}`}
              style={metalButtonStyle()}
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          
          {/* Content - Scrollable */}
          <div className="flex-1 overflow-y-auto p-6">
            {/* Modal content here */}
          </div>
          
          {/* Footer (optional) */}
          <div className="flex gap-3 p-4 border-t" style={{ borderColor: theme.border }}>
            <button
              onClick={handleClose}
              className={`flex-1 py-3 px-4 rounded-lg transition-all border shadow-lg text-sm font-semibold ${metalButtonClass()}`}
              style={metalButtonStyle()}
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className={`flex-1 py-3 px-4 rounded-lg transition-all border shadow-lg text-sm font-semibold ${metalButtonClass()}`}
              style={metalButtonStyle()}
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </ModalPortal>
  );
}
```

---

## Modal Portal Pattern

### Always Use ModalPortal

```tsx
import { ModalPortal } from '../portals/PortalLayer';

// ✅ CORRECT - Use portal for proper z-index management
<ModalPortal>
  <div className="fixed inset-0 z-50">
    {/* Modal content */}
  </div>
</ModalPortal>
```

**Why:** Ensures modals render in the correct DOM layer with proper z-index stacking.

---

## Multi-Step Wizard Pattern

### Wizard with Steps

```tsx
const [step, setStep] = useState<1 | 2 | 3>(1);

// Show all steps in one view (preferred)
<div className="flex flex-col gap-6">
  {/* Step 1: Always visible */}
  <div className="flex flex-col gap-3">
    <h3>Step 1: Upload</h3>
    {/* Content */}
  </div>
  
  {/* Step 2: Visible when step 1 complete */}
  {step >= 2 && (
    <div className="flex flex-col gap-3 border-t pt-4">
      <h3>Step 2: Configure</h3>
      {/* Content */}
    </div>
  )}
  
  {/* Step 3: Visible when step 2 complete */}
  {step >= 3 && (
    <div className="flex flex-col gap-3 border-t pt-4">
      <h3>Step 3: Review</h3>
      {/* Content */}
    </div>
  )}
</div>
```

**Alternative:** Show all sections at once with disabled states until prerequisites are met (better UX).

---

## Modal State Management

### Using useModalState Hook

```tsx
// In useModalState.ts
const [myModalOpen, setMyModalOpen] = useState(false);
const [myModalData, setMyModalData] = useState<string | null>(null);

return {
  myModalOpen,
  setMyModalOpen,
  myModalData,
  setMyModalData,
  // ... other modals
};
```

### Opening Modal with Data

```tsx
// In component
const handleOpenModal = (data: string) => {
  modalState.setMyModalData(data);
  modalState.setMyModalOpen(true);
};

// In modal
<MyModal
  isOpen={modalState.myModalOpen}
  onClose={() => {
    modalState.setMyModalOpen(false);
    modalState.setMyModalData(null);
  }}
  data={modalState.myModalData}
/>
```

---

## Common Modal Types

### Confirmation Dialog

```tsx
// Small, centered, max-w-md
<div className="w-full max-w-md max-h-[85vh] rounded-lg border">
  <div className="p-6">
    <h3>Confirm Action</h3>
    <p>Are you sure you want to proceed?</p>
  </div>
  <div className="flex gap-3 p-4 border-t">
    <button onClick={onCancel}>Cancel</button>
    <button onClick={onConfirm}>Confirm</button>
  </div>
</div>
```

### Form Modal

```tsx
// Standard size, max-w-md
<div className="w-full max-w-md max-h-[85vh] rounded-lg border">
  {/* Form content */}
</div>
```

### Wizard Modal

```tsx
// Can be max-w-lg for wider content, but still constrained
<div className="w-full max-w-lg max-h-[85vh] rounded-lg border">
  {/* Multi-step wizard content */}
</div>
```

---

## Accessibility

### Keyboard Support

- **Escape key**: Close modal
- **Tab**: Navigate through focusable elements
- **Enter**: Submit/confirm action
- **Focus trap**: Keep focus within modal when open

### Screen Reader Support

- Use `aria-label` for close button
- Use `role="dialog"` and `aria-modal="true"` on modal container
- Announce modal title when opened

---

## Anti-Patterns

### ❌ Don't Use Full-Width Modals

```tsx
// ❌ WRONG
<div className="w-full">  // No max-width = spans entire screen
<div className="w-full max-w-4xl">  // Too wide
<div className="w-full max-w-6xl">  // Way too wide
```

### ❌ Don't Skip Portal

```tsx
// ❌ WRONG - Modal in component tree
<div className="fixed inset-0 z-50">
  {/* Z-index conflicts possible */}
</div>

// ✅ CORRECT - Use portal
<ModalPortal>
  <div className="fixed inset-0 z-50">
    {/* Proper z-index management */}
  </div>
</ModalPortal>
```

### ❌ Don't Forget Overflow Handling

```tsx
// ❌ WRONG - Content can overflow
<div className="p-6">
  {/* Long content */}
</div>

// ✅ CORRECT - Scrollable content area
<div className="flex-1 overflow-y-auto p-6">
  {/* Long content scrolls */}
</div>
```

---

## Related Patterns

- [React Patterns](../cursor-patterns/react-patterns.md) - Component organization, hooks
- [Accessibility Patterns](../cursor-patterns/accessibility-patterns.md) - Keyboard nav, screen readers
- [File Headers](../cursor-patterns/file-headers.md) - Modal component documentation

---

## Quick Reference

| Modal Type | Max Width | Use Case |
|------------|-----------|----------|
| Confirmation | `max-w-md` | Yes/No dialogs |
| Form | `max-w-md` | Single-column forms |
| Wizard | `max-w-lg` | Multi-step wizards |
| Complex Wizard | `max-w-xl` | Rare - only if absolutely necessary |

**Remember:** Always use `max-h-[85vh]` for height constraint and `overflow-y-auto` on content area.

---

## Macro App variant (CSS modals, not Tailwind)

The Macro App renderer does **not** use the Tailwind template above. It uses shared classes in
`School Scrips/Macro App/renderer/src/styles/modals.css`.

Before adding a modal there, read **`School Scrips/Macro App/guidelines/Guidelines.md` § Modals**
and copy an exemplar (`GradesBackupModal.tsx`, `GradebookHistoryModal.tsx`).

---

**Last Updated:** 2026-07-29

---

## When scrolling is unavoidable (Electron / portal modals)

**Symptom:** Modal overflows the viewport but no scrollbar appears.

**Cause:** Tailwind height utilities (`h-[540px]`, `max-h-[85vh]`) are unreliable in React portals — JIT may skip them, or `electron.css` / global styles override them.

**Fix:** Use **inline styles** for critical height constraints on the modal shell:

```tsx
<div
  className="rounded-lg border shadow-xl flex flex-col"
  style={{
    width: '800px',
    height: '540px',
    maxHeight: '85vh',
  }}
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
- Prefer designing modals to fit without scrolling (see "Aim for NO scrolling" above)

Two-panel layout (sidebar + scroll): fixed-width sidebar (`flex-shrink-0`), right panel uses the same `overflow-hidden` / `overflow-y-auto` pair.

Test with 50+ items when scroll behavior matters.
