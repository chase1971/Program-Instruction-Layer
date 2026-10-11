# Momentum handoff — Logic Homework intro modal copy

**Written:** 2026-10-11  
**Repos in scope:** `School Scrips/logic-app` (intro lives in embedded component), portal consumes via `@logic/app`

---

## Objective and current phase

Chase is polishing **Logic Homework** student-facing copy. The intro **popup** appears after **Start** on the home menu (not on tile click). Source of truth today: `School Scrips/logic-app/src/app/components/LogicProblems.tsx` (~lines 268–327), title **Logic 7.1 Homework**.

**This handoff’s next task is copy-only:** produce the **full revised modal text** for Chase to read. **Do not edit code** in the fresh task unless Chase explicitly asks to implement after approving the wording.

---

## Chase’s desired feel (his words / STT)

- Paragraph about points should stay **short**: still **10 points**; **90%+ on first try** = full credit; **below 90%** = score matches percentage — **stop there** (no long examples like 60% = 6/10, no “one mistake is still full credit” repetition).
- Next sentence: **“You can repeat this as many times as needed.”** — **period, done.** Remove everything about entering name, submitting when happy, submit once, no penalty for multiple submits — **portal auto-submit / no student name step anymore**; that copy is obsolete.
- Keep **MyLab replacement** line, **Directions** block (click **?**, T/F, **Check**), **error screenshot → email** line, and **Got it** unless Chase says otherwise.

---

## Accepted decisions (this session, already implemented — separate from copy task)

- Logic Homework **standalone** TC catalog + portal `logic` section gate (Macro + student-portal).
- TC preview landscape on `#/logic-homework`; teleport React keys fixed.
- Doc: `agent docs/recipes/portal-app-standalone-not-bundled.md`.
- **Not deployed** to Netlify this session unless Chase did separately.

---

## Rejected / do not redo

- Bundling Logic into “matrix apps” only in Teacher Console.
- Treating instructor **teleport** buttons as the student path.
- Expanding intro modal with submit/name instructions again.

---

## Current implementation state (intro modal — unchanged pending copy approval)

| Block | Current text (summary) |
|--------|-------------------------|
| Title | Logic 7.1 Homework |
| ¶1 | Complete problems **instead of** MyLab Math |
| ¶2 | 10 pts, 90% first try, examples, “one mistake…” |
| ¶3 | Repeat + enter name + submit once + multi-submit |
| ¶4 | Screenshot errors → email |
| Directions | Truth table, **?**, T/F, **Check** |
| Button | Got it |

Home menu (before Start): title **Logic Homework**, subtitle **Truth tables · 6 problems** — not part of this copy change unless Chase says so.

---

## Draft proposed modal (for next agent to present — align with Chase, then implement only if asked)

**Title:** Logic 7.1 Homework

1. Complete the following problems **instead of** the problems on MyLab Math.

2. This homework is worth **10 points**. Score **90% or higher** on your first try to earn full credit (10/10). Anything below 90% matches your percentage.

3. You can repeat this as many times as needed.

4. If you run into any errors or something looks wrong, take a screenshot and email it to me.

**Directions**

Build a truth table step by step. Click the **?** column to pick which connective to work out next, fill in T / F, then hit **Check**. Work through each part until the full statement is done.

**Button:** Got it

---

## Open questions

- Keep title **Logic 7.1 Homework** vs portal title **Logic Homework**?
- Keep ¶4 (screenshot/email) as-is?
- After copy approval: single edit in `LogicProblems.tsx` (+ optional portal deploy); logic-app rebuild if Macro bundles it.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`).
2. `School Scrips/logic-app/src/app/components/LogicProblems.tsx` (intro modal JSX only — read, don’t change until approved).
3. `Programs/agent docs/recipes/portal-app-standalone-not-bundled.md` if touching portal wiring (unlikely for copy-only).

---

## Exact next step

In a **fresh Codex task**, read `latest.md`, refine the **Draft proposed modal** above if needed, and **post the full final modal text to Chase in chat** (all paragraphs + Directions + button label). **Do not implement code** in that task unless Chase says to apply it after he approves the wording.
