# Reusing Manim animation patterns

First inventory: 2026-10-03. Use this when building a clip, building several clips,
or when Chase says "look at our new animation lists again."

**Read the selection table, then only the matching entries and code.** This is a
small map of teaching actions, not a catalog of every scene or Manim command.
It records existing implementations; it does not make scene-specific code generic
or certify that a new combination will render correctly.

## Select the teaching actions

| The lesson needs to… | Read | Best starting point |
|---|---|---|
| Apply the same operation on both sides; rearrange terms | [Equation operations](#equation-operations) | `SlopeInterceptForm.move_x`, `swap` |
| Divide terms; bring quotients down; factor a GCF | [Division and factoring](#division-and-factoring) | `SlopeInterceptForm.divide`; `GCFDivision.construct` |
| Rewrite whole numbers as fractions; multiply or add fractions | [Fraction operations](#fraction-operations) | `FractionTimesWhole.show_problem`; `FractionAddFractions` |
| Cross out terms or factors and show what remains | [Cancellation](#cancellation) | `pull_cancel_pair`; `make_cancel_work` |
| Build formulas, substitute, align working, move pieces into a result | [Formula assembly](#formula-assembly) | `copy_into`; `make_length_panel`; `line_up` |
| Plot an answer; show rise/run, a line, or an inequality region | [Graphing](#graphing) | `SlopeInterceptForm.graph` |
| Keep a diagram, labels, and measurements synchronized as something changes | [Linked motion and measurements](#linked-motion-and-measurements) | `SquareAreaRate.construct`; `point`, `rebuild` |
| Collect repeated outcomes; rearrange a chart; build a sampling distribution | [Collections and distributions](#collections-and-distributions) | `tip_into_histogram`; `drop`, `rain` |

These are eight broad families. Moving, writing, fading, boxing, coloring, and
pausing are supporting actions within them, not additional catalog entries.

## Build a clip or a batch

1. **Describe the visible lesson.** Record the problem, intended result, and short
   sequence of teaching beats. Say what visibly changes at each beat: "draw a bar
   under each term, add the divisor, bring each quotient down" is actionable;
   "explain division clearly" leaves the animation undecided.
2. **Match existing code.** Prefer a supported new input to an existing scene over
   rebuilding it. Otherwise select the few entries above that cover the lesson.
   Read the named functions and their dependencies, not every file listed here.
3. **Record only the gaps.** Note the motion, layout, or input case that existing
   code does not support. Do not force a new lesson into an unsuitable template.
   Preserve the user's teaching sequence when adapting an example.
4. **Build and inspect one representative first.** For five similar requests,
   establish one working implementation, then supply the other problems. For
   unrelated requests, group only the genuinely shared work. A batch request does
   not require five independently invented animation implementations.
5. **Verify every variant.** Check its mathematics, readable holds, and important
   transitions. Different signs, expression lengths, and diagram ranges can break
   a layout that worked on the first problem. Fix the common cause when shared;
   do not accumulate per-problem offsets to hide a broken layout model.
   **Portal stop frame:** when the clip ends (or an example segment ends), the last
   visible frame must still show the lesson — not a fade to blank. See
   [ANIMATION_STYLE_RECIPE.md](../ANIMATION_STYLE_RECIPE.md) § Portal clips (“When playback stops”).
6. **Deliver through the existing pipeline.** Follow [README](../README.md) for
   rendering and pages, and [layout guardrails](LAYOUT_GUARDRAILS.md) for audits
   and contact sheets. Check that inspection artifacts belong to the current
   render and intended scene, particularly when a module contains several scenes.

A compact working note is enough; keep it with the task, not in a new global registry:

| Clip / problem | Visible beats | Reuse: file + symbol | New work | Verification / unresolved issue |
|---|---|---|---|---|
| Example: another slope-intercept problem | move term; divide; graph | `slope_intercept_form.py`: `Problem`, `SlopeInterceptForm` | input record if supported | math, sign flip if applicable, fraction spacing, graph |

For a batch, use one row per clip. Add precise defect notes only when needed, such
as "at `simplified`, denominator touches next row; during division, sign disappears."
Do not create an exhaustive inventory of every object, fade, or pause.

## Reuse levels and common dependencies

- **Helper:** an existing callable to reuse after reading its signature and dependencies.
- **Input-driven scene:** accepts problem values, but only within its existing teaching structure.
- **Example:** demonstrates a technique; its numbers, indices, coordinates, or scene state are specific.

The current [style recipe](../ANIMATION_STYLE_RECIPE.md) owns appearance, notation,
and teaching conventions. Historical examples do not override it. In particular,
older scenes have different colors/caption placement and some use raw `MathTex`.
Use [math_notation.py](../math_notation.py) for current notation, and
[scene_style.py](../scene_style.py) for `Narrated`, captions, pacing, and marks.
Do not copy constants or make a second implementation of these shared concerns.

Many scene modules change Manim configuration when imported. A function living in
a scene is not automatically an independent library. Inspect its imports, globals,
and expected object structure before reusing it. Extend an existing owner where
possible; this catalog does not authorize a parallel helper library or a refactor.

## Equation operations

**Use for:** adding/subtracting on both sides, canceling an additive inverse,
bringing surviving terms to a new line, and rearranging unlike terms.

**Start:** [slope_intercept_form.py](../slope_intercept_form.py), `Problem`,
`SlopeInterceptForm.move_x`, `swap`, and helper `under`.
**Reuse level:** input-driven scene; its individual methods depend on scene state.
Supply the problem's terms, operation, captions, intermediate rows, and answer.
It is not a symbolic solver: verify that the supplied rows are equivalent.

`move_x` constructs a complete destination line before revealing pieces; `swap`
uses curved paths for the exchanged terms. The indices assume the current term
structure. Check signs travel with the intended terms and the equation retains its
relation. Do not use "move across the equals sign" to skip a requested visible operation.

For the simpler instructional sequence, [two_step_equation.py](../two_step_equation.py),
`TwoStepEquation.construct`, is an **example**, hard-coded to `3x + 7 = 22`.

## Division and factoring

**Use for:** visible division beneath terms, lowering quotients into a completed
line, or assembling a common factor around the remaining expression.

**Start:** [slope_intercept_form.py](../slope_intercept_form.py),
`SlopeInterceptForm.divide` and `negative_on_top` — **example methods within an
input-driven scene**. `divide` expects the five-part `self.row` built earlier.
It draws bars from term geometry using `unsigned`, supplies divisors, constructs
the full answer before revealing it, and handles the inequality flip as a beat.
Check every intended term is divided, operators stay on their baseline, and
new negatives/fractions follow the notation recipe.

**Factoring variation:** [gcf_division.py](../gcf_division.py),
`GCFDivision.construct` — **example**. Find the comment "Reserve the completed
equation's geometry": quotient positions come from the final factored expression;
the factor and parentheses are then built around those positions.
[solve_factors.py](../solve_factors.py), `solve_factors`, shows branching into two
zero-product equations, but is hard-coded to those factors and their piece indices.
Neither is a general factoring engine. Reuse the movement idea with current styling.

## Fraction operations

**Multiplication:** [fraction_times_whole.py](../fraction_times_whole.py),
`aligned_problem`, `FractionTimesWhole.show_problem`, `finish_product`.
**Reuse level:** input-driven scene methods, with fixed two-fraction geometry.
Inputs include four numerator/denominator values, supplied result, optional reduced
values, whole-number mode, and optional intermediate result. The sequence lifts a
whole number above a new bar and denominator, optionally cancels, then multiplies.
It does not derive or validate the supplied reductions/results.

**Addition:** [fraction_add_fractions.py](../fraction_add_fractions.py),
`FractionParts`, `show_whole_plus_fraction`, `show_fraction_plus_fraction`.
**Reuse level:** input-driven scene methods. Supply terms, result, and (for two
fractions) a valid common denominator. `add_multiplier` leaves the original fraction
in place; `morph_product` replaces the products; `combine_over_one_denominator`
moves existing numerators together; `morph_sum` evaluates the addition.
`simplify_result` reduces the supplied result using its GCF.

Check bar widths with longer inputs, multiplier clearance, signs, and numerator /
denominator roles during motion. These support the shown addition/multiplication
sequences; fraction division is **not** an existing supported scene here.

## Cancellation

**Use for:** additive cancellation or reducing multiplicative factors while making
the surviving expression visible. These share visual techniques, not algebraic rules.

**Numeric fractions:** [fraction_times_whole.py](../fraction_times_whole.py),
`slash_on`, `FractionTimesWhole.pull_cancel_pair` — **helper + scene method**.
Supply term keys and reduced values. It strikes terms, shows replacements above or
below, then pulls them into the old slots and updates the object's references.
Check the replacements are correct and later actions target the replacement objects.

**Symbolic factors:** [force_decomposition.py](../force_decomposition.py),
`make_cancel_work` and `ForceDecomposition.cancel`, and [vector_projection_shadow.py](../vector_projection_shadow.py),
`length_panel`, `strike` — **examples / scene-local helper**. Build factors as
separate pieces so precisely those factors can be struck. Inspect the consuming
scene method as well as the builder. Do not try to target a hidden substring in one
opaque typeset fraction, or cancel across addition as if its terms were factors.
Additive cancellation is already demonstrated by `SlopeInterceptForm.move_x`.

## Formula assembly

**Use for:** staged derivations, substitution, copies traveling from a diagram or
earlier row, aligned equals signs, and a final boxed answer. This is the main general
reuse to take from the vector lessons; no projection-specific catalog is needed.

**Start:** [vector_projection_shadow.py](../vector_projection_shadow.py),
`fraction`, `row`, `line_up`, `copy_into`, `make_length_panel`, and `length_panel`.
**Reuse level:** scene-local helpers and examples. `fraction(top, bottom)` returns
separate numerator/bar/denominator pieces. `line_up` assumes the anchor's equals
sign is piece 1 and continuations begin with equals. `copy_into(source, target)`
preserves the source and leaves the actual target object on screen; see the
[guardrails' object-identity gotcha](LAYOUT_GUARDRAILS.md#gotchas).

For an explicit anchor index, see [vector_decomposition.py](../vector_decomposition.py),
`line_up(anchor, index, *rows)`. For formula → substitution → numerical answer,
see [work_wagon.py](../work_wagon.py), `make_angled_work` and `WorkWagon.solve`.
For **formula parameter -> rule / interval** (general form written above the example,
parameters pulse together, a value drops down into an inequality, then replaces `k` in the
interval), see [quadratic_domain_range.py](../quadratic_domain_range.py),
`QuadraticDomainRange.teach_example`, and [rational_domain_range.py](../rational_domain_range.py),
`RationalDomainRange.teach_example` (template condition -> real denominator -> solve for x ->
number line with open circle -> split interval; also `fraction()` / `function_row()` for
a fraction whose pieces need separate colours). Portrait frame, fixed rows, `copy_into` / `Indicate` /
`ReplacementTransform`; reuse for square-root domain/range clips. Caption,
colour, pacing and delivery rules: ANIMATION_STYLE_RECIPE.md "Portal clips".
These builders use scene-specific symbols, sizes, and regions. Check alignment
after fitting the entire panel, preserve meaningful term colors, and verify that
fades/strikes affect the objects actually visible after each transform.

## Graphing

**Use for:** connecting a linear answer to its intercept, rise/run, line, and shading.

**Start:** [slope_intercept_form.py](../slope_intercept_form.py),
`SlopeInterceptForm.graph`, `line_through_box`, `half_plane`.
**Reuse level:** input-driven scene method plus geometry helpers. Inputs come from
`Problem`: `rise_run`, `intercept`, graph `window`, and answer relation. Read `graph`
for its assumptions before using the helpers independently.
Check the supplied slope/intercept agree with the equation, the line crosses the
chosen window, and boundary style and shaded side match the inequality. Vertical
lines and arbitrary nonlinear functions are not supported by this scene template.
The current `graph` method returns immediately for `=`; an equation-only graph
requires adaptation rather than simply changing the problem's relation.

## Linked motion and measurements

**Use for:** changing one quantity while geometry, labels, angle marks, and numeric
readouts stay attached and agree. Covers growth, moving points, tracing, and meters.

**Start simple:** [related_rates_square.py](../related_rates_square.py),
`SquareAreaRate.construct` — **example** using one `ValueTracker`, `always_redraw`,
and numeric updaters. The ladder, drain, cone, lighthouse, and rocket modules are
variations of this family; open only the one whose dependency matches the lesson.
[ellipse_definition.py](../ellipse_definition.py), `EllipseDefinition.construct`,
adds linked distances, a fixed-sum meter, and `TracedPath`.

**For several objects changing together:** [angle_between_vectors.py](../angle_between_vectors.py),
`point`, `make_vector`, `make_tip_label`, `rebuild`, and `normalize` — **examples /
scene-local helpers** using one shared origin and scale. This is useful beyond vectors.
Check endpoints, extremes, and intermediate frames; a correct final position does
not prove that labels stayed attached during motion. Compute dependent geometry
from the same state, check readout rounding/units, and inspect updater cleanup.
Do not transplant a scene's physical speed or geometry constants into another lesson.

## Collections and distributions

**Use for:** showing a few outcomes slowly, collecting many, moving them into a
chart, or building a distribution while preserving the meaning of each item.

**Start:** [dice_stats.py](../dice_stats.py), `DiceStats.tip_into_histogram`, for
mapping existing rows to columns; [dice_sampling.py](../dice_sampling.py),
`DiceSampling.first_sample`, `drop`, `rain`, for example → individual point → batch.
**Reuse level:** examples; binning, axis mappings, counts, and samples are specific.
[dice_sums.py](../dice_sums.py), `chart_row`, shows assembling outcomes;
[dice.py](../dice.py), `die` and `pair`, are helpers only when dice are actually needed.

Check item counts, bin membership, stack positions, and axis meaning after moving
objects. Preserve reproducibility of sampling. Read [PART4_PLAN](../PART4_PLAN.md)
before changing the product-distribution example's sampling choices. A decorative
curve is not evidence that arbitrary new data has the claimed distribution.

## Review and premium-model handoff

Use the existing [audit / contact-sheet loop](LAYOUT_GUARDRAILS.md#the-loop).
The checker covers held frames for participating scenes; older plain `Scene`
examples do not automatically gain `Narrated.mark` coverage. Contact sheets also
need the correct marks and rendered scene. Missing checks are not a clean result.

For each clip assess: **correct math; preserved teaching steps; readable placement;
correct motion; no missing or leftover objects.** Inspect the relevant held frames
and sample intermediate frames from changed transitions. Do not shrink everything,
delete explanatory elements, or replace intended motion with static text merely
to clear an overlap finding. Follow root screen-permission rules for any playback.

Composer can draft using these references and fix audit findings. If premium cleanup
is needed, hand over the brief, exact scene/class and helper paths, current contact
sheet/audit paths, transition timestamps or frames, and unresolved defects. Use a
fresh concise handoff instead of carrying all failed attempts forward. Have the
reviewer repair and verify the scene directly. Model switching remains a choice for
the user or configured workflow; this document does not launch other agents.

The [earlier trial](CHEAP_MODEL_TRIAL.md) shows why inspection must include teaching
motion and construction. This catalog has not yet been benchmarked as a cheaper-model
workflow. Compare premium usage per accepted clip and repair rounds on comparable
work; render duration and raw token count alone do not establish savings.

## Refresh without growing a huge catalog

When Chase asks to revisit the animation list, inspect new or substantially changed
scenes and compare their teaching actions with the eight families above.

- Prefer improving an existing entry's example or adding a supported variation.
- Add a family only for a broadly reusable teaching action that is not already covered;
  a new topic, equation, shape, or Manim method is not enough.
- For a candidate, record purpose, exact file/symbol, reuse level, necessary inputs /
  dependencies, and one important verification check. Remove obsolete references.
- Favor a stronger example over a longer list of alternatives. Keep topic-specific
  scenes discoverable in README rather than expanding this selection table.
- Update the review date and state what was actually checked. Code inspection alone
  does not certify visual quality or arbitrary new inputs. Keep rules/constants in
  their existing owning files and link them here.

**First-pass coverage:** source inspection across algebra/GCF, fraction addition and
multiplication, slope-intercept/inequalities, dice/statistics, ellipse, all six related
rates examples, and the vector/force/ramp/work/reflection scenes. Saved contact sheets
for slope-intercept, angle-between-vectors, and projection were also inspected during
the preceding assessment. No new renders or changes to animation code were made for
this inventory. Specialized lamps, wagons, ray intersections, and projection stories
remain scene references; their broadly useful formula/motion techniques are routed above.
