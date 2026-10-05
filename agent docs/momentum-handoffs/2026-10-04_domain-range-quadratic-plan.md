# Momentum handoff — Domain & Range portal chart + quadratic animation plan

Written: 2026-10-04 11:26 -05:00 (America/Chicago)
Workspace: C:\Users\chase\Documents\Programs
Phase: portal reference chart shipped locally (layout/LaTeX iterated); **approved plan not executed** for linear footnote, scroll, Manim clip, and full-screen example player.

## Read first

1. Root `AGENTS.md` — never open GUI without per-run permission; handoff is not end-of-session (no commit/push unless asked).
2. **`c:\Users\chase\.cursor\plans\quadratic_range_animation_a341b6ea.plan.md`** — authoritative next-work checklist (six todos, all pending).
3. `School Scrips/student-portal/src/features/domain-range-chart/README.md` and feature folder.
4. `School Scrips/student-portal/AGENTS.md` § Orientation, header back labels.
5. For Manim work: `Manim Trial/ANIMATION_STYLE_RECIPE.md`, `Manim Trial/docs/LAYOUT_GUARDRAILS.md`, `Manim Trial/docs/ANIMATION_REUSE.md` (add formula→interval row after clip exists).
6. Video player exemplar: `School Scrips/student-portal/src/features/video-examples/` (`linearInequalitiesGuide.ts`, `VideoExamplesPlayerStage.tsx`, `useVideoExamplePlayer.ts`).

## Objective and desired feel

Chase is building **student-portal reference material** for domain and range (linear, quadratic vertex form, square root, rational graphing form), eventually with **Manim clips** under quadratic / square root / rational — **not** under linear.

The chart must feel like the **Transformations course** apps: **one portrait screen**, **white** body (not gray cards), **KaTeX** (not plain HTML math), **centered** function + rules under each family name. Range cases for quadratic and square root: **Domain:** and **Range:** labels aligned; **first** `a` case on the **same line** as **Range:**; second case stacked below; use thin **`\\to`** arrows, not `\\Rightarrow`.

Linear should **not** teach the old `m=0` / `{b}` split on the chart — Chase wants simple **Domain/Range (−∞, ∞)** plus a **parenthetical footnote** that vertical and horizontal lines are excluded (wording still to implement per plan). Page should **scroll** if needed (no longer force `overflow: hidden` on the whole chart).

For quadratic teaching video: a **formula → rule** animation — highlight `(x-h)^2` as “quadratic,” show domain all reals, then range beats: **`a` grows**, **copy** of `a` beside **`a>0` / `a<0`**, **`k` pops**, interval builds. **Two numeric examples** (`a=2` and `a=-2`, same `h,k`). Reuse `copy_into` / `Indicate` patterns; **width** is the main layout constraint (`scene_layout.CENTER`, `fit_into`).

Portal playback: Chase chose **full-screen example route** (not inline in the chart). **“Show example”** under Quadratic only → dedicated player → **Back to chart** (not Exit to home). Two tabs Example 1 / Example 2 on **one MP4** with segment times from marks JSON (like linear inequalities guide).

## Accepted decisions

| Decision | Detail |
|---|---|
| Deliverable location | **Student portal app**, not scratch HTML on 8765 (early infographic was wrong shape; optional scratch page remains for Manim preview only). |
| Section / access | Tile on **M1314 Transformations** axis; same gate as Transformations homework (`transformationsHomeworkVisible`, identifying/graphing access). Activity id `reference/domain-range-chart` — **no Supabase row**, ungraded. |
| Layout | Vertical stack; linear **compact** band; other three **standard** with flex **media slot** reserved below rules (for future embeds). |
| LaTeX structure | Single `rulesLatex` per family using `aligned`; centered via CSS flex on `.domain-range-chart-copy`. |
| Example player UX | Full-screen route; reuse video-examples player patterns; white shell, `object-fit: contain`, width cap ~30rem column. |
| Manim examples | `f(x)=2(x-1)^2+3` and `f(x)=-2(x-1)^2+3`; PAPER palette, `mathtex()`, marks + scratch HTML via `build_page.py`. |

## Rejected directions

- **2×2 grid** on one portrait frame — too small text, wasted whitespace; replaced with vertical stack.
- **Gray/blue card backgrounds** — user wanted white matching quiz shell.
- **Separate Domain/Range LaTeX blocks left-aligned** — user wanted centered under the function.
- **Empty line under “Range:” before first case** — first case must sit **beside** “Range:”.
- **8765 infographic as the product** — portal app is the real deliverable.
- **Inline video in chart section** — user selected **full-screen** player in plan Q&A.

## Current implementation state

### Student portal (`School Scrips/student-portal`)

Feature folder `src/features/domain-range-chart/`:

- `domainRangeChartContent.ts` — four families, `rulesLatex` with aligned domain/range; linear still has **old** `(m≠0)` / `{b}` text (**plan says replace**).
- `DomainRangeChartView.tsx` — navy quiz shell, vertical stack, empty `domain-range-chart-media-slot` on standard layouts.
- `domain-range-chart.css` — white background, centered KaTeX, stack layout; **overflow still hidden** on body/stack (**plan says enable scroll**).
- Wired: `portalHomeApps.ts` (tile after Transformations homework), `usePortalRoute.ts` (`domain-range-chart`), `App.tsx`, `MatrixHomeView.tsx`, `portalFirstPaintAccess.ts`.
- Tests: `src/test/domainRangeChart.test.tsx` — passed when last run.

**Not built yet:** `Show example` link, `DOMAIN_RANGE_QUADRATIC_EXAMPLE_ROUTE`, `DomainRangeQuadraticExampleView`, MP4 asset under `src/assets/video-examples/domain-range/`.

**Git (student-portal repo):** At handoff time only `domainRangeChartContent.ts` and `domain-range-chart.css` showed as modified vs `origin/main`; rest of feature may already be on remote — **verify with `git status` / diff** before assuming.

### Programs root

- Optional scratch HTML `agent docs/scratch/domain-range-family-chart.html` + `page-manifest.json` row may exist from early iteration — **not** the portal product.
- Plan file: `.cursor/plans/quadratic_range_animation_a341b6ea.plan.md`.

### Manim Trial

- **No** `quadratic_domain_range.py` yet.
- Unrelated dirty files in Programs root (`angle_between_vectors.py`, `scene_style.py`, `portrait_frame.py`) — **do not touch** unless Chase asks; preserve user work.

## Verification already done

- `npm test -- --run src/test/domainRangeChart.test.tsx` in student-portal — passed (2 tests).
- Session scorecard bumps logged for chart work and handoff reminder.
- **No** Manim render, **no** portal `npm run build` after final LaTeX centering, **no** browser/GUI review, **no** deploy.

## Constraints

- **Never** launch GUI, browser, or `npm run dev` portal preview without Chase’s per-run permission.
- **No commit/push/deploy** unless explicitly requested (handoff ≠ end-of-session).
- **No Supabase migration** for reference chart or example video.
- Modals / dwell: big click targets for “Show example”; no hover-only affordances.
- File size cap 800 lines on edits; Manim scene target &lt;500 lines.

## Open questions

- Exact parenthetical wording for linear vertical/horizontal exclusion (plan: plain language in LaTeX footnote).
- Whether `portalNavigationLabels.ts` needs a new **Back to chart** constant or reuse an existing in-app back label.
- MP4 binary size in git — follow existing `video-examples` asset pattern (committed MP4 like linear inequalities).

## Exact next step

Execute the plan in **`quadratic_range_animation_a341b6ea.plan.md`** starting with **todo `chart-linear-scroll`**: update linear `rulesLatex` (simple domain/range + footnote) and set chart body/stack to **`overflow: auto`**. Then implement **`quadratic_domain_range.py`**, render, add `build_page.py` scratch preview, then portal example route + player + “Show example” link. Do not deploy Netlify unless Chase asks.

This handoff is a continuation boundary only — no GitHub or end-of-session actions were performed.
