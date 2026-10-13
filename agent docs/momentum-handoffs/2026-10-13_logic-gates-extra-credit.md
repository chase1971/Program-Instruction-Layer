# Momentum handoff — Logic Gates Extra Credit (+ Teacher Console bits)

**Written:** 2026-10-13 ~15:00 CDT · Topic: logic gate sandbox in Logic Homework (student portal)

## Read first

1. This file.
2. `School Scrips/logic-app/README.md` § Student portal embed (the portal does NOT use logic-app's MainMenu).
3. `agent docs/recipes/portal-app-banner.md` (banner rule written this session).
4. Code: `School Scrips/logic-app/src/app/components/gates/` + `src/app/hooks/useCircuitState.ts`, `useCanvasPointer.ts`, `useElementSize.ts`.

## 1. Objective and current phase

Chase wants students to **build XOR (A ⊕ B, "exclusive OR / exclusive disjunction") from AND / OR / NOT gates**
and fill a truth table, tying class truth tables to binary. Phase: **iterating on the skeleton look/feel** with
Chase reviewing in Teacher Console **admin preview** → Logic Homework → **Logic Gates Extra Credit** button.
No scoring, no saving, no portal progress yet. He said "we're going to probably do more than that" for the table.

## 2. Chase's desired feel

- Values are **1 / 0**, never T/F. Truth table should **look like the Logic App's** (`logic/TruthTable.tsx`), A/B instead of P/Q.
- Gates **always face right, never rotate**. Everything **draggable** like gates (A, B, OUTPUT too) — **no drag handles/grip dots**.
- Must be **obvious you can pull a wire** out of a dot. Crossing wires must never connect.
- Canvas should be **basically the whole app**, up to the edges — no inner frame.
- Size: v2 (1.6×) was "way too big", v1 was "too small"; current is **0.85× (85×54 gates), A/B 40×34, OUTPUT 72×34** — he said gates and A/B "could be smaller" right before this; current values are his latest ask, not yet reviewed.
- Gate buttons small, labelled "AND gate / OR gate / NOT gate"; must not be bigger than the gates.
- **Portal banner on every app** (navy: ← Back to home + fullscreen | centered title | Exit). No goal sentence in the banner.

## 3. Accepted decisions

- Lives in `logic-app`, embedded in portal via `@logic/` alias; button on portal `LogicHomeworkHomePanel.tsx`
  **gated by `hasAdminCheats()`** (admin preview only while skeleton) — tell Chase before ungating.
- Portal wraps `GateSandbox` with the standard banner in `LogicHomeworkView.tsx` (`showGates` branch) and passes `hideHeader`.
- Wiring: drag output→input **or** click output then click input (dwell/touch friendly). Input port takes one wire
  (new replaces old); outputs fan out; loops refused; unconnected input = 0. Delete = select gate/wire then "Delete selected"; "Clear all".
- Truth table column sits **under the gate buttons** (left), canvas to the right. Rows 11, 10, 01, 00 (Logic App order).
  Output column = whatever is wired into **OUTPUT**; "?" until wired. **Tapping a row** previews it on the wires (green=1, gray=0) — my addition, not yet commented on by Chase.
- **OUTPUT box kept** (Chase: "I need to have an output"), but it shows no value; value lives in the table. A/B have no 0/1 toggles anymore.
- **Do not change the Logic Homework truth-table activity** (already assigned) — explicit Chase instruction.

## 4. Rejected directions

- Logic-app `MainMenu` button only (portal never shows it) — the first attempt; why the README note exists.
- Fixed A/B, toggles inside A/B, OUTPUT lamp with live 0/1, grip dots, big 1.6× gates, goal sentence in header, inner bordered canvas frame.

## 5. Current implementation state (all uncommitted)

- logic-app: `src/app/components/gates/{gateTypes,gateEval,GateShape,Port,WireLayer,IOTerminal,GatePalette,GateTruthTable,GateSandbox}.ts(x)`,
  hooks above, `src/test/gateEval.test.ts` (6 pass), `App.tsx` + `MainMenu.tsx` (standalone button), README note. `npm run build` OK.
  Gate files type-check clean (logic-app has no tsc; checked with `../student-portal/node_modules/.bin/tsc`). Pre-existing: 7 failing tests in `scoringLogic.test.ts` (not ours).
- student-portal: `LogicHomeworkView.tsx`, `LogicHomeworkHomePanel.tsx`, `logicHomeworkActivity.ts` (`LOGIC_GATES_TITLE`), `types/logic-app.d.ts`, `AGENTS.md` rows. Other dirty portal files (factoring*) belong to a parallel session — leave them.
- Docs: new `agent docs/recipes/portal-app-banner.md`; rows in `recipes/INDEX.md`, portal `AGENTS.md`, `student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md`.
- Macro App: `useTeacherConsoleNavigation.ts` — Students & Responses now defaults to **Responses** (tests pass).
- Side sessions (finished, uncommitted, not independently verified):
  - [Log every student app-access change](local_4afba949-4c55-4b1d-89e1-cceb0800c6b0): migration `087_student_app_access_log.sql` + Macro App `source` plumbing. (Logic access had been mysteriously turned off; history was unrecoverable — nothing automatic writes `false`.)
  - [Logic survey results](local_4a793fbe-678a-4557-9934-55b66db71efa): Feedback tab on Teacher Console Logic Statistics (`LogicStatisticsFeedbackTab.tsx`, `logicPostSurveyReport.ts`).
- Logic post-survey itself already existed (portal `logicPostSurvey/`, migration 085); 1 response so far.

## 6. Open questions and constraints

- Chase hasn't reviewed the truth-table version (v4) yet. Possible next asks: smaller still, student-filled truth table/checking, multiple challenges besides XOR.
- Never launch GUIs/browsers without asking; verify headlessly, hand off as a flat statement. No Netlify deploy unless asked. No commit/push unless "pull" / "put on GitHub" / end-of-session.
- Keep files < 300 lines-ish (hard cap 800); `GateSandbox.tsx` is the orchestrator (~150 lines).

## 7. Exact next step

Wait for Chase's feedback on v4 (truth table column + smaller pieces) in admin preview, then adjust sizes/layout
in `gateTypes.ts` (single size owner: `GATE_SCALE`, `IN_W/IN_H`, `OUT_W/OUT_H`) and `GateTruthTable.tsx`.
