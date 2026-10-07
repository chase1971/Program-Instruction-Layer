# Portal instruction text box

> **You might say:** "instruction box", "tutorial tip text", "how do we do the blue text box",
> "put the hint in a dialog like Matrix practice"
> **What it is:** Blue bordered rounded box for one-shot instructions — not a full-width banner,
> not a numbered tutorial step badge unless Chase asks for numbers.

**Exemplar files — read these before writing new code:**

- `School Scrips/student-portal/src/app/components/PortalInstructionBox.tsx`
- `School Scrips/student-portal/src/styles/portal-features.css` (`.portal-instruction-box*`)
- `School Scrips/student-portal/src/features/guided-practice/UnguidedPracticeSessionIntro.tsx` (intro + Okay)
- `School Scrips/student-portal/src/features/logic-homework/LogicFirstProblemHint.tsx` (via `portalHost.firstProblemHint` in ConnectivePicker slot, stacked copy, no button)
- Standalone Matrix app (same visual, Tailwind): `School Scrips/Matrix app/src/app/components/guided-practice/GuidedPracticeOverlay.tsx` — `bg-blue-50 border-2 border-blue-200 rounded-xl`; optional numbered badge is **tutorial-only**, not required for portal hints

---

## When to use

| Use this | Not this |
|---|---|
| Short instruction before or during an activity | Full-width colored strip under the header |
| `role="dialog"` + meaningful `aria-label` | Plain `<p role="status">` with custom one-off CSS |
| Dismiss via explicit action **or** the action the text describes (e.g. tap the flashing target) | Numbered step badge unless it is a multi-step tutorial |

## Portal implementation

1. Import `PortalInstructionBox` from `@/app/components/PortalInstructionBox`.
2. Wrap in `portal-instruction-box-slot` when the box sits in the page flow (not a centered full-screen intro). Logic Homework passes the box through **`LogicPortalHostProps.firstProblemHint`** so it renders in the **same row slot as `ConnectivePicker`**; tapping **?** dismisses the hint and opens the picker (see `ProblemScreen.tsx`).
3. Pass copy as `children`. Optional `actions` for an Okay / Next button (`portal-instruction-box__okay-btn`).
4. Do **not** add new colors, borders, or shadow — extend the shared classes only if every consumer needs the change.

```tsx
<div className="portal-instruction-box-slot portal-instruction-box-slot--compact">
  <PortalInstructionBox ariaLabel="How to start">
    Click the <strong>?</strong> at the top of the table to start.
  </PortalInstructionBox>
</div>
```

## Matrix embed (guided / unguided practice)

Inside the portal, Matrix keeps using `GuidedPracticeOverlay` from the Matrix app package (Tailwind classes). Visual match is intentional; portal-native features should use `PortalInstructionBox` + CSS so embed and shell stay consistent without duplicating Tailwind in every feature folder.

## Related

- Flashing a target during a step: [tutorial-flash-vocabulary.md](./tutorial-flash-vocabulary.md) — separate from the instruction box chrome.
- Modals and confirmations: [modal-shell.md](./modal-shell.md).
