# Momentum handoff — Logic Gates extra credit (Part 2)

**Written:** 2026-10-18 (day-valid only)
**Repos touched:** `School Scrips/logic-app` (primary this thread), `School Scrips/student-portal` (embed alias only; may still have older uncommitted portal files from prior sessions)
**Git:** uncommitted work in logic-app (and likely student-portal from earlier). Nothing committed or pushed from this continuation thread. No Netlify deploy.

---

## Read first

1. This file through **Exact next step**.
2. `School Scrips/logic-app/src/app/hooks/useCanvasPointer.ts` (wiring + gate drag behavior).
3. `School Scrips/logic-app/src/app/hooks/useGateTableCheck.ts` (XOR table flow).
4. `School Scrips/logic-app/src/app/components/gates/GateSandbox.tsx` (orchestrator).
5. `School Scrips/student-portal/src/features/logic-homework/LogicHomeworkView.tsx` (portal shell).
6. `School Scrips/student-portal/src/config/portalAccess.ts` (`hasLogicGatesExtraCreditAccess`, `hasAdminCheats`).

Portal shipping: `School Scrips/student-portal/AGENTS.md` § Shipping (deploy only when Chase asks in that message).

---

## 1. Objective and current phase

**Logic Gates Extra Credit (Part 2)** in the student portal: XOR **truth table** (homework-shaped), then **circuit build** with AND/OR/NOT. Cheat-gated preview (`hasLogicGatesExtraCreditAccess` / TC cheat).

**Phase now:** Table UX and circuit interaction were heavily iterated this thread (auto-advance picker, sizing, Example 2, wiring model). **Chase has not confirmed wiring feels right on his device** after the latest `useCanvasPointer` rewrite (drag-only gate move + click/drag wires). **Browser verify in portal** is the gate before ship. Netlify may be stale vs local.

---

## 2. Chase's desired feel

### Truth table (Part 2)
- Match **Logic 7.1 Homework**: formula row, `TruthTable`, **Check / Undo**, wrong = “Incorrect. Try again.” only, **never reveal answers**.
- **First column only:** flashing **`?`** + blue side hint; student must click **`?`** once to open **ConnectivePicker**.
- **After that:** on correct Check (non-final column), **ConnectivePicker opens automatically** for the next column; when **one connective remains**, **auto-fill header** and show **“Complete the final column.”**
- **Intro modal** like Logic homework (540px, no truth table in popup); **no backdrop dismiss** on gates intro.
- **Go to circuit** visible, disabled until table verified; **`hasAdminCheats()`** bypasses (banner + in-table button).
- A/B **input columns 1/0** on table; student columns T/F.

### Circuit
- **A and B fixed** (stacked vertically, same x, gap between). **OUTPUT draggable**; gates move **only by drag**, not click-then-click placement.
- **Wiring:** press an **output** (A, B, gate out) → **dashed wire follows pointer**; **release on input** (gate in or OUTPUT in) **or** second **click** on port/gate body/OUTPUT box connects. **Drag** from output to input also works. Same output again or empty canvas **cancels** armed wire.
- **No** “fill truth table first” under Submit in circuit; match line only after OUTPUT wired + table answers ready.
- Gates and OUTPUT ~**30% larger** (`gateTypes.ts` scale constants).
- **Example 2** must **not** be De Morgan **¬(A ∨ B)** (homework later). Current example: **(¬A) ∨ B** (NOT on A, OR with B).

---

## 3. Accepted decisions

| Topic | Decision |
|---|---|
| XOR formula | `(A ∨ B) ∧ ¬(A ∧ B)` |
| Table hook | `useGateTableCheck.ts` — auto-open picker after first `?`; auto-fill last sub-expression |
| Portal modes | `gatesMode` `'table' \| 'circuit'`; table overlays circuit |
| Example 2 | `(¬A) ∨ B` in `gateExamples.ts` (truth 11,10,01,00 → 1,0,1,1) |
| Terminals | `AB_TERMINALS_LOCKED` — A/B fixed; **OUTPUT movable** |
| Wiring owner | `useCanvasPointer.ts` — `pendingRef` + rubber band in `WireLayer`; no click-to-carry gates |
| Bypass | `canBypassTableGate` / `hasAdminCheats()` for table gate |
| Sidebar | `GateMatchStatus` silent until OUTPUT wired |

---

## 4. Rejected directions

- **Click-to-move gates** (pick up on click, drop on next click) — removed; caused gates jumping onto OUTPUT when wiring.
- **Drag-only wiring without rubber band** — Chase wants **cursor-following wire** plus click-to-complete.
- **De Morgan Example 2** **¬(A ∨ B)** — wrong for timing vs homework.
- **“Fill in your truth table first”** under circuit Submit — removed.
- **A/B horizontal stagger** — replaced with vertical stack.
- **Netlify deploy** without explicit ask in message.

---

## 5. Implementation state (logic-app, uncommitted)

| Area | Key files |
|---|---|
| Wiring / drag | `useCanvasPointer.ts`, `WireLayer.tsx` (pending rubber band), `Port.tsx` (armed ring) |
| Terminals | `gateTypes.ts` (`AB_TERMINALS_LOCKED`, sizes, default OUT position), `IOTerminal.tsx` |
| Table | `useGateTableCheck.ts`, `GateTableMode.tsx`, `GateExtraCreditIntroModal.tsx` |
| Circuit UI | `GateSandbox.tsx`, `GateMatchStatus.tsx`, `GateSubmitPanel.tsx`, `GateShape.tsx` |
| Examples | `gateExamples.ts`, `gateEval.test.ts` (Example 2 assertion) |

**Tests run this thread:** `gateTableShared` + `gateEval` — passed after changes.

**Not re-verified:** full logic-app test suite; **no portal browser pass** after final pointer rewrite.

---

## 6. Open questions / constraints

- **Wiring on phone/dwell:** Chase reported A→gate and gate→OUTPUT still broken before final rewrite; **needs his pass** on latest `useCanvasPointer` build.
- **Deploy:** local portal embeds logic-app via Vite `@logic/` alias — refresh dev server; prod Netlify only on explicit request.
- **Student release:** still cheat/admin only until `hasLogicGatesExtraCreditAccess` changes.
- **Grading/persistence:** extra credit may not be wired to Supabase; confirm if needed.
- **Modal width:** gates intro 540px (homework exemplar) vs generic max-w-md rule — intentional for Chase.

---

## 7. Exact next step

**Chase browser check (or agent after explicit GUI permission):** Portal + cheat → Logic Gates extra credit → dismiss intro → truth table through auto-picker / final column → **Go to circuit** → verify **A → gate → gate → OUTPUT** via **drag wire** and via **click output then click target**. Confirm gates **only move when dragged**, not on double-click empty space. If anything fails, fix in **logic-app** first (`useCanvasPointer.ts` / port hit radii / capture order).

If pass and Chase asks to ship: **student-portal** `npm run deploy:prod` only when explicitly requested, then smoke live URL.

---

## Copy-ready repos for end-of-session (when Chase asks)

- `School Scrips/logic-app`
- `School Scrips/student-portal` (if portal-only files changed or deploy)
