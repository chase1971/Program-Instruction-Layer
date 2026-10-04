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
  palette in `scene_style.py` and set `caption_color = PAPER_INK` on the scene (`PAPER_MUTED` read washed out on the white
  frame -- captions are the first thing a student reads, so they get the darkest text); exemplar
  `slope_intercept_form.py`. Older clips stay navy (`NAVY` palette) until re-rendered.
- **Set `color=INK` on every `MathTex`/`mathtex`.** Manim's default text colour is white,
  which vanishes on the paper background. Accent pieces (gold, blue) get coloured by index
  afterwards, but a piece nobody colours stays white and invisible. The layout audit does not
  catch this (it checks overlaps, edges and type size, not contrast): the first quadratic
  domain/range clip passed the audit with its equation mostly invisible. Look at a frame.
- Large high-contrast math, muted instructional captions.
- **Captions ride along the top of the frame, never the bottom.** They say what is going
  on, so they should be read first. `scene_style.CAPTION_Y` owns the position; content
  then lives below roughly y = 2.5.
- Gold for the GCF, blue for the remaining factors, ink (white on navy, near-black on white) for operators and structure.
- Keep the equation readable on a phone held upright: see "Portal clips" below.
- Use MathTex for formulas; do not render equations as ordinary text.
- Produce a reviewable MP4 first. Interactive student manipulation belongs in the web app, not in the rendered clip.

## Portal clips -- portrait frame, captions, pacing (Chase, 2026-10-04)

Written after the quadratic domain/range clip: a cheap-model first cut passed the layout audit
and was still unusable. **Exemplar to copy: `quadratic_domain_range.py`** (formulas) and
`angle_between_vectors.py` (figure + formulas). Read the scene before writing a new one.

- **Phone-shaped frame.** The portal plays the video about 375 px wide, so a 14.2-unit
  landscape frame draws type about 2.2x too small. New portal clips call
  `portrait_frame.apply_portrait_frame()` (4:5, 6.4 x 8 units) **before any other project
  import**. Stack steps one per line instead of running equations sideways; use the height.
- **Every `MathTex` gets `color=INK`.** See Visual style: the default is white on white.
- **Variables are never plain letters.** Anywhere a variable appears -- in an equation use
  LaTeX (`mathtex`), in a caption use italics and its colour:
  `<span foreground="#1565C0"><i>a</i></span>` (`var()` in `quadratic_domain_range.py`).
  A bare "a" in a sentence reads as the word. Wrapped captions accept this markup
  (`scene_style.wrap_words` keeps a tag with spaces in one piece).
- **Captions are set 4x and scaled down** (`scene_style.CAPTION_SUPERSAMPLE`): at small sizes
  Pango snaps glyph advances to whole pixels and word gaps come out uneven. Do not build
  captions with raw `Text(...)`; use `self.say()`.
- **Say it before you show it.** Call `self.say(...)` *before* the animation it describes, so
  the student reads the sentence and then sees the thing. Never the reverse.
- **Hold long enough to read, no longer.** About 1 s after a short caption, 1.5 s after a long
  one, on top of the animation (`READ_SHORT` / `READ_LONG` in the exemplar), with `pace`
  around 0.9. A first cut at 26 s was too fast; 88 s was too slow; about 35 s per worked
  example felt right.
- **One line per caption.** Wrap width 5.9 at font 20; reword rather than leave a single
  stranded word ("numbers." / "k.") on the second line.
- **Pulse, do not box.** To draw attention to part of a formula use `Indicate(piece,
  color=..., scale_factor=1.3)` (use ~1.6 for a lone variable). No `SurroundingRectangle`
  around terms. When a value moves, `copy_into(source, target)` so it never teleports.
- **Build every row once, at its final spot, and only fade it in.** Rows that re-stack as
  new ones arrive jump around; fixed row positions (`ROW_Y`) cannot.
- **Check frames, not just the audit.** Render, run `contact_sheet.py`, and read one frame
  per mark. The audit passed a clip whose equation was invisible.
- **Formula-parameter -> interval clips** (domain and range of a vertex-form function, and the
  square-root / rational siblings) follow the beat order in the exemplar's docstring.
- **When playback stops, the frame must not be blank.** Chase watches clips in the student
  portal; each example tab and each full clip should pause on **finished work still on screen**
  — equations, intervals, captions, or a deliberate summary slide. Hold that composition at
  least ~1 s (`READ_SHORT` / `READ_LONG`) before any fade. Do not fade out the board and then
  end the example on empty white. If a lesson truly needs a transition between examples, fade
  in the blank *between* segments only; the portal plays Example 1 up to an **`ex1_hold`** mark
  and starts Example 2 at **`ex2_form`**, so the player never stops mid-fade. Single-example
  clips: the last mark should be a hold with the final summary visible, not a post-fade frame.

## Delivery — a clip is not done until it is in the student portal (Chase, 2026-10-04)

Chase watches every clip in the student portal, nowhere else. A render under `Manim Trial/media`
is not delivered.

- **Put it in the portal and replace the old version.** Copy the final MP4 into
  `School Scrips/student-portal/src/assets/video-examples/` (exemplar:
  `domain-range/quadratic-domain-range.mp4`, wired by
  `features/domain-range-chart/domainRangeQuadraticExample.ts`) and update the
  per-example segment times from the clip's marks JSON: Example 1 ends at `ex1_hold`,
  Example 2 starts at `ex2_form` (not `ex2_start`, which is after the fade between examples).
  The shared player also seeks ~0.08 s before each segment end so a mistimed mark still lands
  on content (`useVideoExamplePlayer.ts`); authors should still mark and hold the full board.
- **Final size only, never a draft.** Render `-r 1080,1350 --fps 30` for the portrait frame
  (1920x1080 for old landscape clips). Soft text in the portal was a 700 px draft stretched
  to phone width. Check frames with a contact sheet, but do not leave a draft anywhere a
  preview can pick it up.
- **Examples autoplay.** Any portal example that plays an animation starts as soon as the
  student opens it: `useVideoExamplePlayer(examples, { autoPlay: true })`
  (`features/video-examples/useVideoExamplePlayer.ts`). The default is still tap-to-start,
  so new example views must pass the option.

## Solving an equation or inequality on screen -- the one house style (Chase, 2026-10-04)

When a clip says "solve this", do it exactly as `slope_intercept_form.py` does (`move_x`,
`divide`). Chase should never have to re-explain it. The helpers are in
**`Manim Trial/solve_steps.py`** -- import them; exemplar use: `sqrt_domain_range.py`.

- **Add / subtract:** the operation goes **under both sides** in gold (`op_under`), the
  cancelling pair is struck in red (`strike_pair`), the next line is built from copies
  (`copy_into`) of what is left. Quick and silent if the caption above already says what is
  being solved.
- **Divide: never a division sign (`\div`).** A **fraction bar under every term** with the divisor
  under each bar in gold (`divide_bars`), then the next line is built from copies.
- **Flip:** dividing an inequality by a negative -- the old sign pulses red, the new sign is
  copied in red, then settles to ink.
- **Bring down only what is being solved.** "The inside must be >= 0" copies the radicand
  alone (`form[3].submobjects[2:]` -- [0] is the radical, [1] the bar over it), never the root sign or its bar; the same goes for any piece of a
  function: copy the part the next line needs, not its wrapper.
- **Bringing a piece down is a slide, not a morph.** Copy it, `animate.scale(...).move_to(...)`, then
  swap in the real row. `copy_into` morphs glyphs and looks like it is reshaping (Chase, 2026-10-04).
- Student-facing line sequence: statement -> operation under both sides -> struck pair ->
  new line -> bars and divisors -> answer line. No narration of every step.

## Prompt template

> Create a Manim mathematical explanation animation using the attached “Math explanation animation recipe.” Teach [CONCEPT] with [EQUATION]. Keep the original equation written on one baseline. Develop the work downward like handwriting. Preserve the final position of each completed expression; build new factors, parentheses, and equality signs around it. Use fraction bars and visible operations where they clarify the algebra. Use deliberate pauses and plain classroom captions. Use the white-background PAPER palette (ink, gold, blue) from the recipe. Render a phone-readable MP4. Do not invent extra algebraic steps; ask only if the intended mathematical sequence is ambiguous.
