# Momentum handoff — Composite notation captions (wording + read time)

**Written:** 2026-10-08 (Thursday)

---

## Objective and current phase

Chase is polishing **Composite Examples** (Manim `composite_domain.py`, `_2`, `_3`). Intro + player are done. The **composite-build section** needs caption beats that **teach notation before the fly-in animation**, with **enough on-screen time to read each sentence** — same pacing rhythm as the rest of the clip (caption → hold → next caption or animation).

**Phase now:** Wording and timing were updated in this session; **verify in the portal** at the composite section on all three tabs. Tweak copy only if a line wraps awkwardly or still feels rushed.

---

## Chase's desired feel (his words, refined)

- Directions stay in the **caption bar only** — not a second problem line on the board (overlaps `f(x)` / `g(x)`).
- **Say it before you show it** — each caption gets a **full read pause** before the next caption or the plug-in animation.
- Tone: plain teaching — what does **∘** or **parentheses** mean, then what do you **do**.
- **Example 1 & 3 (∘):**
  1. Name **$(f\circ g)(x)$** and explain **∘** as **$f$ composed with $g$**, and that **$g$ replaces every $x$ in $f$** (not just “composed with” in one short phrase).
  2. Then explicitly: **plug $g$ in for every $x$ in $f$** before the existing Indicate / parentheses / fly-in beats.
- **Example 2 (parentheses):**
  1. **Another way to write a composite** is **$g(f(x))$** (not a different operation).
  2. Relate it to **$(g\circ f)(x)$** — same idea, **$g$ composed with $f$** (order matters; this problem is **not** $f\circ g$).
  3. **This time** plug **$f$ into $g$** (matches animation: **f** flies into **g**).
- Intro at clip start already says **Find $(f\circ g)(x)$…** or **Find $g(f(x))$…** — the composite section is **how to build** it, not repeating the whole problem statement unless a line needs “now find …” for clarity.

---

## Accepted decisions

| Area | Decision |
|---|---|
| Timing | After **every** pre-composite `self.say(...)`, call **`self.wait(READ_LONG)`** (1.5 s at pace 0.9) before the next `say` or `play`. Matches `composite_problem_intro.py` (`say` → `wait`). |
| Why | `Narrated.say()` only cross-fades captions (~0.6 s); **`beat()` waits come after animations**, so back-to-back `say()` lines flash ~1 s total. |
| Ex1 & Ex3 copy | Beat 1: `The $\circ$ in $(f\circ g)(x)$ means $f$ composed with $@b g$ — $@b g$ replaces every $x$ in $f$.` Beat 2: `Plug g in for every x in f.` (via `G_WORD` / `F_WORD` / `X_WORD`). |
| Ex2 copy | Beat 1: `Another way to write a composite is $g(f(x))$.` Beat 2: `That is the same as $(g\circ f)(x)$: $g$ composed with $@b f$.` Beat 3: `This time plug f in for every x in g.` |
| Animation | Unchanged after the new caption block (Indicate, wrap, fly-in, simplify). |
| Delivery | 1080×1350 @ 30 fps; MP4s in `student-portal/.../composite/`; holds from `hold` mark in `composite_domain*_marks.json`. |

---

## Rejected directions

- **Single terse line** only (“$(f\circ g)(x)$ means $f$ composed with $g$”) with **no wait** — reads for ~1 s; Chase flagged this in portal review.
- **Board duplicate** of “Find …” under `f(x)` / `g(x)`.
- **Replacing** the intro caption at clip start — keep `composite_problem_intro.py` as-is.

---

## Current implementation state

**Manim (updated this session):**

| File | Composite caption block (~lines) |
|---|---|
| `Manim Trial/composite_domain.py` | ~241–248: two says + two `READ_LONG` waits, then existing animation |
| `Manim Trial/composite_domain_2.py` | ~156–165: three says + three waits |
| `Manim Trial/composite_domain_3.py` | ~298–305: same as ex1 |

**Portal holds (after re-render):**

| Example | `hold` seconds |
|---|---|
| 1 | **106.78** |
| 2 | **72.56** |
| 3 | **161** |

**Tests:** `compositeExamples.test.ts` — 3/3 pass.

**Verify:** Open Composite Examples in portal; at composite build, each caption should stay ~1.5 s before the next; then plug-in animation as before.

---

## Open questions

- Beat 1 on ex1/ex3 may **wrap to two lines** at width 5.9 — OK per recipe if no orphan word; reword if Chase dislikes the break.
- Optional third beat on ex1 (“Here’s how to find $(f\circ g)(x)$”) only if Chase wants explicit “how to find” **again** after domain work — not added yet to avoid repeating intro.

---

## Constraints

- No GUI without permission. Re-render via `.venv` manim headless.
- Do not refactor `composite_domain_3.py` beyond caption block.
- `$...$` / `@b` accent per `math_caption.py`.

---

## Read first

1. This file.
2. `Manim Trial/ANIMATION_STYLE_RECIPE.md` (say-before-show, one line per caption).
3. `Manim Trial/scene_style.py` — `Narrated.say()` has **no built-in read wait**.
4. `Manim Trial/composite_problem_intro.py` — exemplar `say` + `wait`.

---

## Exact next step

Watch **Example 1** in the portal at the composite section: confirm both caption beats feel long enough and the wording matches Chase’s intent. If yes, spot-check ex2 (three beats + ∘ link) and ex3 (∘ like ex1). If a line wraps badly or copy should say “how to find” explicitly, adjust strings and re-render that clip only, then refresh hold seconds from the marks JSON.
