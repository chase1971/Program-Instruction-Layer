"""Graphing a rational function that factors, cancels and leaves a hole: f(x) = (6x - 12) / (2x^2 - 4x).

Chase's order, same as rational_function_graph.py (example 1), with example 2's cancel and hole:
    factor the top and the bottom (a GCF each) -> cancel x - 2 top and bottom
    -> reduce the numbers too: 6 / (2x) = 3 / x, and use that REDUCED function from here on
    -> x-intercept: the top is just the number 3, no x, so none
    -> y-intercept: plug in 0, the bottom is 0, undefined, so none
    -> vertical asymptote: bottom = 0 (x = 0)
    -> horizontal asymptote: bottom has the bigger degree, so y = 0
    -> hole: bring back the canceled x - 2, set it to 0, solve, plug into the REDUCED function
    -> graph: dashed asymptotes, an open circle at the hole, the curve through it, the other
       curve in the diagonally opposite corner.

Verified (check() re-derives it with Fraction):
    6x - 12 = 6(x - 2); 2x^2 - 4x = 2x(x - 2); reduced f = 3/x; no x-intercept; no y-intercept;
    vertical asymptote x = 0; horizontal asymptote y = 0; hole at x = 2, y = 3/2.

Reuses the helpers and layout of example 1 (subclass), see rational_function_graph.py.
"""

from rational_function_graph import (
    ASYMPTOTE_COLOR,
    CURVE_COLOR,
    DEGREE_Y,
    COEFF_Y,
    FUNC_SIZE,
    FUNC_Y,
    LEFT_X,
    LIST_Y,
    RIGHT_X,
    WORK_Y,
    YINT_Y,
    RationalFunctionGraph,
    frac_row,
    list_row,
)

from fractions import Fraction  # noqa: E402

from manim import (  # noqa: E402
    Circle,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Indicate,
    RIGHT,
    ReplacementTransform,
    UP,
    VGroup,
    Write,
)

from rational_domain_range import READ_LONG, READ_SHORT, tex  # noqa: E402
from scene_style import PAPER_GOLD, PORTAL_PAGE_WHITE  # noqa: E402
from solve_steps import strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

# Equal scales: the curve 3/x and the hole (2, 3/2) read naturally. A sketch, not to scale in y.
GRAPH_X, GRAPH_Y = (-6, 6), (-4, 4)
X_UNIT, Y_UNIT = 0.45, 0.42


def f(x):
    """The reduced function. The original is the same everywhere except x = 2."""
    return 3 / x


def check():
    """Re-derive every number the clip says."""
    for x in (Fraction(5), Fraction(-7, 2), Fraction(10)):
        assert 6 * x - 12 == 6 * (x - 2)
        assert 2 * x ** 2 - 4 * x == 2 * x * (x - 2)
        assert (6 * x - 12) / (2 * x ** 2 - 4 * x) == f(x)
    assert 6 * 2 - 12 == 0 and 2 * 2 ** 2 - 4 * 2 == 0     # the hole: top and bottom both 0
    assert f(Fraction(2)) == Fraction(3, 2)
    assert Fraction(6, 2) == 3
    assert abs(f(Fraction(10 ** 6))) < Fraction(1, 1000)    # y = 0 from the degrees


check()


class RationalFunctionGcfHole(RationalFunctionGraph):
    graph_x, graph_y = GRAPH_X, GRAPH_Y
    x_unit, y_unit = X_UNIT, Y_UNIT
    graph_step = 1
    graph_center_y = -2.08

    def construct(self):
        s = FUNC_SIZE
        original = frac_row(s, ('f(x)', '='), tex('6x', '-12', size=s), tex('2x^2', '-4x', size=s), 1)
        factored = frac_row(s, ('f(x)', '='),
                            tex('6', '(', 'x', '-2', ')', size=s),
                            tex('2x', '(', 'x', '-2', ')', size=s), 1)
        half = frac_row(s, ('f(x)', '='), tex('6', size=s), tex('2x', size=s), 1)
        reduced = frac_row(s, ('f(x)', '='), tex('3', size=s), tex('x', size=s), 1)
        for row in (original, factored, half, reduced):
            row.move_to([0, FUNC_Y, 0])
        f_top, f_bottom = reduced[1][0], reduced[1][2]
        top_factor = VGroup(*factored[1][0][1:5])         # (x - 2) on top
        bottom_factor = VGroup(*factored[1][2][1:5])      # (x - 2) on the bottom

        # ---- the answer list ----------------------------------------------------------------
        xint_item = list_row('x', r'\text{-int: }', r'\text{none}', x=LEFT_X, y=LIST_Y[0])
        yint_item = list_row('y', r'\text{-int: }', r'\text{none}', x=LEFT_X, y=LIST_Y[1])
        va_item = list_row(r'\text{V.A.: }', 'x', '=', '0', x=RIGHT_X, y=LIST_Y[0])
        ha_item = list_row(r'\text{H.A.: }', 'y', '=', '0', x=RIGHT_X, y=LIST_Y[1])
        holes_item = list_row(r'\text{Hole: }', '(', '2', ',', r'\frac{3}{2}', ')',
                              x=RIGHT_X, y=0.1)
        canceled_item = list_row(r'\text{Canceled: }', 'x', '-2', x=RIGHT_X, y=0.1)
        canceled = VGroup(canceled_item[1], canceled_item[2])

        # ---- the y-intercept rows -----------------------------------------------------------
        plug = tex('f(0)', '=', r'\frac{3}{0}', size=46).move_to([0, YINT_Y, 0])
        undefined = tex('f(0)', '=', r'\text{undefined}', size=46).move_to([0, YINT_Y, 0])
        va_cond = tex('x', '=', '0', size=46).move_to([0, WORK_Y, 0])

        # ---- the horizontal asymptote rows --------------------------------------------------
        degree_top = tex(r'\text{degree of top: }', '0', size=36).move_to([0, DEGREE_Y[0], 0])
        degree_bottom = tex(r'\text{degree of bottom: }', '1', size=36
                            ).move_to([0, DEGREE_Y[1], 0])
        zero = tex('y', '=', '0', size=46).move_to([0, COEFF_Y, 0])

        # ---- the hole row -------------------------------------------------------------------
        hole_plug = tex('f(2)', '=', r'\frac{3}{2}', size=46).move_to([0, YINT_Y, 0])

        # ---- the graph -----------------------------------------------------------------------
        plane = self.build_graph()
        c2p = plane.c2p
        va_line = DashedLine(c2p(0, GRAPH_Y[0]), c2p(0, GRAPH_Y[1]), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        ha_line = DashedLine(c2p(GRAPH_X[0], 0), c2p(GRAPH_X[1], 0), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        # The left curve is below the axis and the right curve above it, so the labels sit on
        # the empty sides: x = 0 to the right near the bottom, y = 0 above the line on the left.
        va_label = tex('x', '=', '0', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(0, -3.3), RIGHT, buff=0.1)
        ha_label = tex('y', '=', '0', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(-5.3, 0), UP, buff=0.08)
        hole_mark = Circle(radius=0.07, color=CURVE_COLOR, stroke_width=3,
                           fill_color=PORTAL_PAGE_WHITE, fill_opacity=1).move_to(c2p(2, 1.5))
        # Each branch runs to the edge of the window: f = 4 at x = 3/4, f = -4 at x = -3/4.
        right_curve = plane.plot(f, x_range=[0.75, GRAPH_X[1], 0.02], color=CURVE_COLOR,
                                 stroke_width=5)
        left_curve = plane.plot(f, x_range=[GRAPH_X[0], -0.75, 0.02], color=CURVE_COLOR,
                                stroke_width=5)

        # ---- 1. factor the top and the bottom -----------------------------------------------
        self.say('Here is a rational function. Everything must be factored first.')
        self.play(Write(original), run_time=1.3)
        self.beat('problem', READ_LONG)

        self.say('Factor the common factor out of the top and out of the bottom.')
        self.play(ReplacementTransform(original, factored), run_time=1.5)
        self.beat('factored', READ_LONG)

        # ---- 2. cancel -----------------------------------------------------------------------
        self.say('Now check whether anything cancels. The x − 2 on top and bottom cancel.')
        strikes = strike_pair(top_factor, bottom_factor)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.6)
        self.beat('cancel', READ_LONG)

        self.say('After canceling, we have the reduced function. '
                 'Use it to find everything else.')
        self.play(FadeOut(strikes),
                  copy_into(VGroup(factored[1][0][2], factored[1][0][3]), canceled),
                  FadeIn(canceled_item[0]), run_time=1.0)
        self.play(ReplacementTransform(factored, half), run_time=1.5)
        self.beat('reduced', READ_LONG)

        self.say('Reduce the numbers too. 6 divided by 2 is 3.')
        self.play(ReplacementTransform(half, reduced), run_time=1.3)
        self.beat('reduced_numbers', READ_LONG)

        # ---- 3. x-intercept ------------------------------------------------------------------
        self.say('For the x-intercept, set the top equal to zero. The top is just a number, '
                 'with no x in it, so there is none.')
        self.play(Indicate(f_top, color=ASYMPTOTE_COLOR, scale_factor=1.6), run_time=1.2)
        self.play(FadeIn(xint_item), run_time=1.0)
        self.beat('xint', READ_LONG)

        # ---- 4. y-intercept ------------------------------------------------------------------
        self.say('For the y-intercept, plug in zero for x.')
        self.play(Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(plug), run_time=1.3)
        self.beat('yint_plug', READ_LONG)

        self.say('The bottom is zero, and we cannot divide by zero. '
                 'So there is no y-intercept.')
        self.play(ReplacementTransform(plug, undefined), run_time=1.3)
        self.play(FadeIn(yint_item), run_time=1.0)
        self.beat('yint', READ_LONG)
        self.play(FadeOut(undefined), run_time=0.5)

        # ---- 5. vertical asymptote -----------------------------------------------------------
        self.say('For the vertical asymptote, set the bottom equal to zero and solve.')
        self.play(Indicate(f_bottom, color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  copy_into(f_bottom, va_cond[0]), FadeIn(VGroup(va_cond[1], va_cond[2])),
                  run_time=1.3)
        self.beat('va_set', READ_SHORT)

        self.say('The vertical asymptote is x = 0.')
        self.play(FadeIn(VGroup(va_item[0], va_item[1], va_item[2])),
                  copy_into(va_cond[2], va_item[3]), run_time=1.3)
        self.play(FadeOut(va_cond), run_time=0.5)
        self.beat('va', READ_LONG)

        # ---- 6. horizontal asymptote ---------------------------------------------------------
        self.say('For the horizontal asymptote, compare the degrees of the top and the bottom.')
        self.play(Indicate(f_top, color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(degree_top), FadeIn(degree_bottom), run_time=1.5)
        self.beat('ha_degrees', READ_LONG)

        self.say('The bottom has the bigger degree, so the horizontal asymptote is y = 0.')
        self.play(FadeIn(zero), run_time=1.2)
        self.play(FadeIn(VGroup(ha_item[0], ha_item[1], ha_item[2])),
                  copy_into(zero[2], ha_item[3]), run_time=1.3)
        self.play(FadeOut(VGroup(zero, degree_top, degree_bottom)), run_time=0.5)
        self.beat('ha', READ_LONG)

        # ---- 7. the hole ---------------------------------------------------------------------
        self.say('Now the hole. Bring back the term that canceled, set it equal to zero, '
                 'and solve.')
        # once the term is brought down, "Canceled" becomes "Hole" with empty parentheses
        to_hole = [ReplacementTransform(canceled_item[0], holes_item[0]), FadeOut(canceled),
                   FadeIn(VGroup(holes_item[1], holes_item[3], holes_item[5]))]
        iso = self.solve_for_x(canceled, '-', '2', 'hole', on_copy=to_hole)
        self.play(copy_into(iso[2], holes_item[2]), run_time=1.0)

        self.say('Plug it into the reduced function to get the y.')
        self.play(FadeOut(iso), Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(hole_plug), run_time=1.3)
        self.beat('hole_plug', READ_LONG)

        self.say('The hole is at (2, 3/2).')
        self.play(copy_into(hole_plug[2], holes_item[4]), run_time=1.3)
        self.play(FadeOut(hole_plug), run_time=0.5)
        self.beat('holes', READ_LONG)

        # ---- 8. the graph --------------------------------------------------------------------
        self.say('Now graph it. Draw the asymptotes as dashed lines.')
        self.play(FadeIn(plane), run_time=1.0)
        self.play(Create(va_line), Create(ha_line), FadeIn(VGroup(va_label, ha_label)),
                  run_time=1.5)
        self.beat('asymptotes', READ_LONG)

        self.say('Put an open circle at the hole.')
        self.play(FadeIn(hole_mark, scale=1.6), run_time=1.0)
        self.beat('points', READ_LONG)

        self.say('No intercepts, but the hole is a point on the curve, '
                 'so start on the side that has it.')
        self.play(Indicate(hole_mark, color=PAPER_GOLD, scale_factor=2.0), run_time=1.3)
        self.beat('cross', READ_LONG)

        self.say('Sketch through the hole, up toward x = 0 and out along y = 0.')
        self.play(Create(right_curve), run_time=2.5)
        self.add(hole_mark)
        self.beat('right_curve', READ_LONG)

        self.say('This side is going up, so the diagonally opposite side goes down.')
        self.play(Indicate(right_curve, color=PAPER_GOLD, scale_factor=1.06), run_time=1.3)
        self.beat('opposite', READ_LONG)

        self.say('Sketch the other curve, coming down from the asymptote and leveling out '
                 'along y = 0.')
        self.play(Create(left_curve), run_time=2.5)
        self.beat('hold', READ_LONG)
        self.write_marks('rational_function_gcf_hole_marks.json')
