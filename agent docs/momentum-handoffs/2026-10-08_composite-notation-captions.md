# Momentum handoff — Composite Examples notation captions

**Written:** 2026-10-08 (Thursday)

---

## Objective and current phase

Chase is polishing the **Composite Examples** portal clips (Manim `composite_domain.py`, `_2`, `_3`). Intro screens and player behavior are done. **Next phase:** richer **caption directions** right before each clip builds the composite — teach what the notation *means* before the existing “plug in / fly in” animation runs. No change to the math animation beats after that; only replace/expand the `self.say(...)` lines at the start of the composite section.

---

## Chase's desired feel

- Directions live in the **caption bar** (top), same as the rest of the clip — not a second line of math on the board (that overlapped `f(x)` / `g(x)`).
- **Say it before you show it** — two short caption beats if needed; reword so each line wraps cleanly (recipe: one line per caption, width 5.9).
- Tone: plain teaching — “what does this symbol mean?” then “what do you actually do?”
- Example 2 is **different notation** (parentheses), not a different operation — frame it as **another way to write the same composite**, then note **which function goes inside which** for *this* problem.

---

## Accepted decisions (already shipped)

| Area | Decision |
|---|---|
| Problem intro | `composite_problem_intro.py`: caption `Find $(f\circ g)(x)$…` or `Find $g(f(x))$…`; write `f(x)` and `g(x)` on board; title fades N/A; **f/g stay** for “Start with the domain of each function.” |
| Notation per clip | Ex1 & Ex3: **∘** in intro caption. Ex2: **g(f(x))** in intro caption. |
| Portal delivery | MP4s in `student-portal/src/assets/video-examples/composite/`; holds in `compositeExamplesGuide.ts`. |
| Player | `useVideoExamplePlayer`: tab switch while playing; **same tab = restart**; **Replay always enabled** (`VideoExamplesPlayerStage.tsx`). |

---

## Rejected directions (do not redo)

- Worksheet layout (1.) a/b/c/d blanks on screen.
- Duplicating directions in **caption + board title** (looked like the problem was stated twice).
- Large on-board “Find … domain” line low on the frame (collided with `f(x)`).

---

## Current implementation state

**Manim — composite beat entry (what to rewrite):**

| Clip | File | Current caption (approx.) | Order in problem |
|---|---|---|---|
| 1 | `Manim Trial/composite_domain.py` ~L240 | `Now the composite: put $g$ in for every $x$ in $f$.` | **f∘g** — plug **g** into **f** |
| 2 | `Manim Trial/composite_domain_2.py` ~L156 | `Now the composite: put $f$ in for every $x$ in $g$.` | **g(f(x))** — plug **f** into **g** |
| 3 | `Manim Trial/composite_domain_3.py` ~L298 | Same pattern as ex1 (g into f) | **f∘g** again |

Uses `F_WORD`, `G_WORD`, `X_WORD` and `G_COLOR` on board; see `ANIMATION_STYLE_RECIPE.md` and existing `self.say()` patterns in those files.

**Portal (likely uncommitted):** player + guide hold times + composite MP4s from last render (~102.78 / 66.22 / 157 s holds).

**Verification:** Composite portal tests pass; Manim not re-run after player-only edits.

---

## Proposed caption structure (Chase's intent — implement in fresh task)

### Example 1 (`CompositeDomain`, ∘ notation, g into f)

Before the existing composite animation (`Indicate` / `copy_into` / etc.):

1. **Notation:** $(f \circ g)(x)$ — the **∘** symbol means **f composed with g** (name the composite; tie to intro caption).
2. **Action:** That means **plug $g$ in for every $x$ in $f$** (can drop or shorten the old single line “Now the composite…”).

Optional: one board beat is **not** required if captions carry it; keep animation as-is after captions.

### Example 2 (`CompositeDomainTwo`, parentheses, f into g)

1. **Another notation:** $g(f(x))$ is **another way to write a composite** (parentheses instead of ∘).
2. **Link symbols:** Show/read that this is the same idea as **$(g \circ f)(x)$** — g composed with f (order matters; **not** f∘g).
3. **Action for this problem:** **Plug $f$ in for every $x$ in $g$** (matches current animation: f flies into g).

Chase mentioned “show how that equals g composite f” — interpret as **relating g(f(x)) to (g∘f)(x)** on screen or in caption math, without reversing the problem’s order.

### Example 3 (`CompositeDomainThree`, ∘ like ex1)

Same **two-beat structure as example 1** (∘ means f composed with g; plug g into f). Functions differ; intro caption already uses ∘.

---

## Constraints

- **No GUI** without Chase permission; re-render Manim headless, copy MP4s, update `COMPOSITE_EXAMPLES_*_HOLD_SECONDS` from new `composite_domain*_marks.json`.
- Caption lines: use `self.say()` with `$...$` / `@b` accent per `math_caption.py`; variables italic/colored in captions.
- Do not refactor unrelated composite logic or file-size creep in `composite_domain_3.py` (already large).

---

## Open questions (resolve while implementing if unclear)

- Ex2: Chase wants **g(f(x)) ↔ (g∘f)(x)** spelled out — confirm whether a **brief on-board** `(g∘f)(x)` next to `g(f(x))` is wanted or **caption-only** is enough (default: caption-only unless layout audit complains).
- Whether to keep the word **“Now the composite:”** or replace entirely with the new wording.

---

## Read first

1. This file.
2. `Manim Trial/ANIMATION_STYLE_RECIPE.md` (captions, say-before-show).
3. `Manim Trial/composite_domain.py` composite section (~L240+) as exemplar; mirror pattern in `_2` and `_3`.
4. `Manim Trial/composite_problem_intro.py` (intro already correct).

---

## Exact next step

In **`composite_domain.py`**, replace the single `self.say` at the start of the composite section with **two** `self.say` calls (notation meaning, then plug-in rule), then run the existing composite animation unchanged. Repeat for `_2` (three beats: parentheses notation, link to ∘, plug f into g) and `_3` (same as ex1). Re-render all three, copy to portal assets, update hold seconds, run `compositeExamples.test.ts`.
