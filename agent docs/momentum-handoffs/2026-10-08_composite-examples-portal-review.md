# Momentum handoff — Composite Examples (notation captions + portal polish)

**Written:** 2026-10-08 (Thursday)

---

## Objective and current phase

Chase is finishing **Composite Examples** in the student portal (M1314): three Manim clips (`composite_domain.py`, `_2`, `_3`) with intro captions, domain work, **notation teaching before the plug-in animation**, then the existing fly-in / simplify / domain-merge beats.

**Current phase:** Implementation and re-renders are **done for this round**. Chase said he wants to **watch all three tabs in the portal** and may request wording or pacing tweaks after review. No further code changes until that review — unless something is clearly broken.

---

## Chase's desired feel

- **Caption bar only** for directions — never duplicate “Find …” on the board under `f(x)` / `g(x)`.
- **Say before you show:** each caption gets time to read **before** the next caption or the animation it describes.
- **Plain teaching:** name the notation, say what it *means*, then start the plug-in animation **without** repeating the same idea in a third “now substitute …” line.
- **∘ examples (1 & 3):** two beats — (1) what $\circ$ means in $(f\circ g)(x)$; (2) $g$ replaces every $x$ in $f$ → then **Indicate / fly-in** with caption (2) still visible through `READ_CAPTION_EXTRA`.
- **Parentheses example (2):** two beats — (1) $g(f(x))$ is another composite notation; (2) same as $(g\circ f)(x)$, $g$ composed with $f$ → then plug-in animation. **No** third “plug $f$ into $g$” line (redundant with beat 2).
- **Number lines** should draw **quickly** (Chase: “way faster”) — not slow 2.4 s / 3.0 s builds.
- **Rejected:** em dash joining two sentences in one caption (looked like a stray line next to $g$ when wrapped); redundant “substitute $g$ into $f$” / “this time plug …” after the meaning was already stated.

---

## Accepted decisions (shipped)

| Area | Decision |
|---|---|
| Read time | `self.wait(READ_LONG)` after each `say()` in notation block; **`READ_CAPTION_EXTRA` (2.5 s)** after the **last** notation line before `play(Indicate…)`. `Narrated.say()` does **not** wait — only cross-fades (~0.6 s). |
| Ex1 & Ex3 copy | (1) `The $\circ$ in $(f\circ g)(x)$ means $f$ composed with $@b g$.` (2) `This means $@b g$ replaces every $x$ in $f$.` → animation. |
| Ex2 copy | (1) `Another way to write a composite is $g(f(x))$.` (2) `That is the same as $(g\circ f)(x)$: $g$ composed with $@b f$.` → animation. |
| NL pacing | Shared constants in `composite_domain.py`: `NL_BUILD_RUN` 1.1, `NL_WIDE_BUILD_RUN` 1.4, `NL_ARROW_RUN` 0.55, `NL_HIGHLIGHT_RUN` 0.5 — used in `_2` / `_3` imports. |
| Intro | `composite_problem_intro.py` unchanged — still “Find $(f\circ g)(x)$…” / “Find $g(f(x))$…” at clip start. |
| Player | Prior session: tab switch while playing; same tab = restart; Replay always on. |
| Delivery | `-r 1080,1350 --fps 30`; MP4s in `student-portal/src/assets/video-examples/composite/`; holds from `hold` mark in `composite_domain*_marks.json`. |

---

## Current implementation state

**Manim — composite notation entry (~L246–251 ex1, ~L159–164 ex2, ~L302–307 ex3):**

- Two `say` + `wait` pairs (ex2: two says; ex1/3: same).
- Plug-in animation unchanged after that block.

**Portal holds (latest render):**

| Example | `COMPOSITE_EXAMPLES_*_HOLD_SECONDS` |
|---|---|
| 1 | **99.94** |
| 2 | **67.5** |
| 3 | **152** |

**Verification:** `compositeExamples.test.ts` passes. Chase portal review of **all three tabs** pending (his words: “let me look at all of them”).

**Git (likely uncommitted):** `Manim Trial/composite_domain*.py`, `*_marks.json`, `composite_problem_intro.py`; portal `composite-examples*.mp4`, `compositeExamplesGuide.ts`. Programs root may also have dirty agent-docs / session logs.

---

## Rejected directions (do not redo)

- Single notation line with **no** `wait` between consecutive captions (~1 s flash).
- **Em dash** in one caption: `… composed with g — g replaces …`
- **Third** action caption before Indicate (“substitute / plug …”) when beat 2 already says replace/plug meaning.
- On-board duplicate problem statement; worksheet 1.a/b/c layout.

---

## Open questions (resolve during Chase's review)

- Any caption still too fast/slow? Adjust `READ_LONG` vs `READ_CAPTION_EXTRA` only — don’t remove waits.
- Ex2 beat 2 wrap at width 5.9 — reword if ugly break.
- If Chase wants “how to find $(f\circ g)(x)$” **again** after domain section (beyond intro), add as **first** beat of composite block only if he asks — not shipped to avoid repeating intro.

---

## Constraints

- No GUI without permission. Re-render: `Manim Trial/.venv/Scripts/python.exe -m manim -r 1080,1350 --fps 30 --disable_caching …`
- Don’t bloat `composite_domain_3.py` with unrelated refactors.
- `$...$` / `@b` in captions per `math_caption.py`.

---

## Read first

1. This file.
2. `Manim Trial/ANIMATION_STYLE_RECIPE.md` (captions, say-before-show).
3. `Manim Trial/scene_style.py` — `Narrated.say()` has no read wait.
4. `Manim Trial/composite_domain.py` — `READ_*` and `NL_*` constants + composite section exemplar.

---

## Exact next step

Chase watches **Example 1, 2, and 3** in the portal through the **composite-build** section (notation captions → plug-in). Note any wording or timing issues. If all three pass, optional: sync Manim + portal to GitHub when Chase asks. If one clip needs copy change: edit strings in that `.py` only, re-render that scene, copy one MP4, update one hold constant in `compositeExamplesGuide.ts`.
