# Math explanation animation recipe

Use this recipe when generating a new Manim animation for Chase's math apps.

Before implementing, select existing teaching patterns from the
[animation reuse catalog](docs/ANIMATION_REUSE.md); it also covers batches and future inventory updates.

This file covers what the frames should **look like** and how the teaching should **move**.
Keeping elements from colliding is a separate, automated job: see
[docs/LAYOUT_GUARDRAILS.md](docs/LAYOUT_GUARDRAILS.md) for the audit that runs at every
pause mark, the named layout regions, and the contact sheet.

## Teaching movement

- Treat the original equation as written work. Put it on one baseline and keep it visible while the next line develops.
- Work downward, like handwriting on paper. Do not make the solution float upward into place.
- Preserve the normal baseline of `+`, `=`, and parentheses. Do not make operators look like separate fractions unless division is the actual point.
- When a new line is complete, make it the final position before building around it. Do not move it again just to add a factor, parentheses, or `= 0`.
- Use deliberate, smooth motion with short pauses after each mathematical idea.

## GCF and division pattern

1. Show the full equation, already written, including `= 0` when relevant.
2. Draw fraction bars directly beneath the terms being divided.
3. Put the same GCF below each bar.
4. Move each quotient downward into its final position.
5. Say that the terms are divided by the same common factor.
6. Merge duplicate GCF labels into one factor and put it in front of the expression that remains.
7. Form parentheses around the quotient expression without moving the quotient.
8. Add `= 0` last when the equation is factored.
9. If solving by the zero-product property, lift the factored equation into the original equation's position, separate the factors diagonally, and create one equation per factor.
10. Solve each equation with the same visible operation style: show the operation beneath both sides, then reveal the simplified result.

## Chase's notation — negatives and dividing by a negative

> **You might say:** "the way I write negatives", "dividing by a negative", "the negative is
> too big", "the fraction bar is too long", "put the negative on top"

**Why:** a full-size minus reads as subtraction and stretches every fraction it sits in;
Chase teaches one consistent way so every student's work looks the same.

**The single implementation:** `Manim Trial/math_notation.py` — build math with `mathtex()`
instead of `MathTex()`; `hanging_fraction()` for a negative fraction; `unsigned()` for what a
drawn division bar spans. Checked by `test_math_notation.py`.
**Exemplar:** `slope_intercept_form.py` (the divide step and the answer).

Non-negotiables:

- **A negative is a short dash; a subtraction is a full minus.** Otherwise "negative" and
  "minus" look identical. `mathtex()` decides by position — a `-` opening the expression or
  following `=`, `<`, `>`, `+`, `-` is a negative. Write a subtraction as its own `'-'` part.
- **A negative never widens a fraction bar.** Dividing −3y by −3: the bar covers `3y` and the
  `3` below it; both negatives hang off the left. Same for typeset fractions (`\llap`).
- **A negative fraction puts the negative on the top number** (−2 over 3, never −2/3 or
  2 over −3). On screen say only "Move the negative to the top number." — no reason. It is
  why graphing always goes up/down by the top number and right by the bottom one.
- **Dividing an inequality by a negative flips the sign** — show it as its own beat: the sign
  pulses red and comes down flipped.

Anti-patterns: raw `MathTex` with a leading `-`; a division bar measured from `term.get_left()`;
a fraction built as `-\frac{2}{3}` or `\frac{-2}{3}`; a smaller *scaled* minus instead of the dash.

## Language

Prefer plain classroom language:

- “Divide each term by the same common factor.”
- “Put the GCF you factored out in front of what is left.”
- “When we factor a GCF, we put it in front like this.”

Avoid “multiply back” unless the lesson specifically teaches checking by multiplication.

## Visual style

- **White background for new clips** (Chase, 2026-09-28): the navy clips were hard to read
  on the classroom projector, and clips are headed for the student portal. Use the `PAPER_*`
  palette in `scene_style.py` and set `caption_color = PAPER_MUTED` on the scene; exemplar
  `slope_intercept_form.py`. Older clips stay navy (`NAVY` palette) until re-rendered.
- Large high-contrast math, muted instructional captions.
- **Captions ride along the top of the frame, never the bottom.** They say what is going
  on, so they should be read first. `scene_style.CAPTION_Y` owns the position; content
  then lives below roughly y = 2.5.
- Gold for the GCF, blue for the remaining factors, ink (white on navy, near-black on white) for operators and structure.
- Keep the equation readable on a phone held horizontally.
- Use MathTex for formulas; do not render equations as ordinary text.
- Produce a reviewable MP4 first. Interactive student manipulation belongs in the web app, not in the rendered clip.

## Prompt template

> Create a Manim mathematical explanation animation using the attached “Math explanation animation recipe.” Teach [CONCEPT] with [EQUATION]. Keep the original equation written on one baseline. Develop the work downward like handwriting. Preserve the final position of each completed expression; build new factors, parentheses, and equality signs around it. Use fraction bars and visible operations where they clarify the algebra. Use deliberate pauses and plain classroom captions. Use the white-background PAPER palette (ink, gold, blue) from the recipe. Render a phone-readable MP4. Do not invent extra algebraic steps; ask only if the intended mathematical sequence is ambiguous.
