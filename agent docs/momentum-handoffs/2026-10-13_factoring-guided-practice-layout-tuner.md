# Momentum handoff — Factoring Guided Practice portal layout (tuner + GCF UI)

**Written:** 2026-10-13

## Read first

- This file, then root `Programs/AGENTS.md` (never display without permission, no ephemeral toasts, modal/backdrop rules N/A here).
- Portal host: `School Scrips/student-portal/src/features/factoring-guided-practice/FactoringGuidedPracticeEntry.tsx`
- Portal CSS: `School Scrips/student-portal/src/styles/factoring-guided-embed.css`
- Enable flag: `School Scrips/student-portal/src/features/factoring-guided-practice/factoringGuidedPracticeActivity.ts` (`FACTORING_GUIDED_PRACTICE_ENABLED = true` on desktop this session).
- Practice UI (Vite alias `@factoring-guided/` from portal): `School Scrips/Factoring Guided Practice/src/app/components/` — especially `FactoringPracticeView.tsx`, `FactoringGcfInfoBlock.tsx`, `FactoringStepControls.tsx`, `FactoringEquationPanel.tsx`.
- Baked layout constants (still default **off**): `School Scrips/Factoring Guided Practice/src/app/config/factoringPortalEmbedLayout.ts`
- Layout tuner hook (portal): `School Scrips/student-portal/src/hooks/useFactoringLayoutTuner.ts`
- Drag/resize logic: `School Scrips/Factoring Guided Practice/src/app/hooks/useFloatingRectTuner.ts`
- Visual exemplars Chase named: **Transformations** identifying view problem label (`Problem N / 10`, gray bold); **Solving Quadratics / GCF tutorial** two-column workspace + blue info card (Math App Studio info-block colors).

## Objective and current phase

Chase is bringing **Factoring Guided Practice** into the **student portal** with the same feel as other guided activities (Matrix header, landscape gate, GCF-tutorial-style body). He is **tuning where the prompt/Yes-No box sits and how big it is** before asking the agent to lock values into code. **Phase: layout tuner works for instructor; Chase has not yet pasted JSON to bake in final position/size.**

## Chase's desired feel

- **Problem number near the top** like Transformations — `Problem N / total`, not buried in the equation column.
- **Equation large, no visible box** around the main `= 0` line (partial-factoring strips can keep their lighter boxes).
- **Prompt lives in the blue GCF info card** on the right (~GCF tutorial), not a huge bottom instruction bar.
- **Yes/No and prompt card smaller** than the first portal pass (he said Yes/No and text box were too big).
- **Do not make him type coordinates.** He wants to **drag and resize**, then **one action that tells the agent what to codify** (JSON / copy button), not manual coordinate entry.
- He tests in **portal dev** or **Macro Teacher Console preview** (M1314 area); standalone Factoring launcher lacks portal chrome.

## Accepted decisions

| Decision | Why |
|---|---|
| Portal shell: `portal-quiz--guided-practice` + navy header + `UnguidedPracticeProblemNav` | Match Matrix guided practice, not Logic layout. |
| Two-column flex **or** floating info block when tuner/baked layout active | Flex is default; absolute `%` rect when tuning or after bake. |
| Layout tuner on **`hasAdminCheats()`** sessions by default (instructor/cheat) | URL-only `?factoring-layout=1` was invisible; Chase saw CSS tweaks but no drag. |
| Green **Move box** toggle in problem nav row (`unguided-practice-problem-nav__dev-btn`) | Dwell-friendly; turns tuner on/off; persists in `sessionStorage` key `factoring-layout-tuner`. URL overrides: `?factoring-layout=0\|1`. |
| Tuner UI: blue **Move** bar + corner resize grip + bottom green panel with JSON + **Copy layout for agent** | Communicates `useFloatingInfoBlock` + `infoBlockRectPct` for `factoringPortalEmbedLayout.ts`. |
| Pointer capture on handles (not window-only listeners) | Dwell/head-mouse dragging was unreliable without it. |
| `FACTORING_PORTAL_EMBED_LAYOUT.useFloatingInfoBlock: false` until Chase locks | Students keep flex column until bake. |

## Rejected / do not redo

- **URL-only layout mode** without a visible control — Chase never got drag handles; looked “unchanged” except CSS.
- **Huge info block** filling half the screen (`flex-1` + vertical center on full-height card) — fixed earlier; card should hug content in flex mode.
- **Bottom `PortalInstructionBox`** for the GCF prompt — prompt is inside the embed info block now.
- **Oversized Yes/No** (full-width flex-1 menu buttons) — shrunk in `factoring-guided-embed.css`; may need another pass after lock.

## Current implementation state

### Shipped in working tree (uncommitted)

**student-portal**

- `FactoringGuidedPracticeEntry.tsx` — landscape gate, embed, `totalProblems` + problem nav, layout tuner toggle, class `portal-quiz--factoring-layout-tuner` when on.
- `factoring-guided-embed.css` — equation bare/larger KaTeX, smaller Yes/No, floating info + tuner chrome styles.
- `UnguidedPracticeProblemNav.tsx` — optional `totalProblems`, optional `endControls` slot.
- `useFactoringLayoutTuner.ts` — new.
- `factoringGuidedPracticeActivity.ts` — enabled on desktop (verify before prod deploy).
- `factoring-guided-practice.d.ts` — props for tuner callbacks.

**Factoring Guided Practice**

- `FactoringPracticeView.tsx` — embedded GCF workspace, floating info when tuner or baked layout, wires `FactoringLayoutTunerBar`.
- `FactoringGcfInfoBlock.tsx`, `FactoringLayoutTunerBar.tsx` — new.
- `FactoringEquationPanel.tsx` — portal bare equation shell.
- `FactoringStepControls.tsx` — `embeddedInfoInParent` for float wrapper.
- `factoringPortalEmbedLayout.ts`, `useFloatingRectTuner.ts` — layout spec + drag math.

### Verification

- `npm run build` in **Factoring Guided Practice** — passes.
- Chase confirmed **partial** UI delta (equation frame gone, smaller Yes/No) but **could not drag** until second fix (admin default + Move box toggle + pointer capture). **Not re-confirmed after that fix in this thread.**

### Git

- **Not committed or pushed** (momentum handoff — no sync).
- student-portal also has **unrelated dirty** logic-homework files — do not bundle into a factoring-only commit without Chase scope.

## Open questions / constraints

- **Chase has not pasted layout JSON yet** — next agent should bake `infoBlockRectPct` into `factoringPortalEmbedLayout.ts` and set `useFloatingInfoBlock: true`, then tune default Yes/No/message sizes to match locked rect.
- **Problem indicator styling** — shows `Problem N / 5` in nav; Transformations also has centered “Guided Practice” in-app — portal uses header title instead; OK unless Chase asks for more parity.
- **Students** never see Move box toggle unless they have admin cheats (intentional).
- **Netlify prod deploy** — only if Chase explicitly asks; flag enable is local dirty.
- Portal `tsc --noEmit` has **pre-existing** errors in logic/transformations — unrelated.

## Exact next step

1. Ask Chase to reload Factoring GP on an **instructor** session, confirm **Move box: on**, blue **Move** bar, dashed outline, green JSON panel.
2. When placement/size is right: he clicks **Copy layout for agent** (or pastes JSON from the panel) → write into `factoringPortalEmbedLayout.ts`, set `useFloatingInfoBlock: true`, remove reliance on tuner for production layout, adjust CSS defaults (info block max-height, button sizes) to match.
3. Optional polish only if he asks: equation vertical position, partial-factoring strip styling in portal, problem nav vs Transformations pixel match.
