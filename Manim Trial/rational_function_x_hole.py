"""Graphing a rational function whose hole sits on the y-axis: f(x) = 3x / (x^2 + x).

Chase's order, same as rational_function_graph.py (example 1), with example 2's cancel and hole:
    factor the bottom (pull out x) -> cancel x top and bottom
    -> from here on use the REDUCED function 3 / (x + 1)
    -> x-intercept: the top is just the number 3, no x, so none
    -> y-intercept: plug 0 into the reduced function gives 3, but that 0 comes from the canceled
       x (x = 0), so (0, 3) is actually the HOLE, answered right there; since the hole is on the
       y-axis there is no y-intercept: none
    -> vertical asymptote: bottom = 0 (x = -1)
    -> horizontal asymptote: bottom has the bigger degree, so y = 0
    -> hole: already answered in the y-intercept step
    -> graph: dashed asymptotes, an open circle at the hole, the curve through it, the other
       curve in the diagonally opposite corner.

Verified (check() re-derives it with Fraction):
    x^2 + x = x(x + 1); reduced f = 3/(x + 1); no x-intercept; no y-intercept (x = 0 is not in the
    domain of the original); vertical asymptote x = -1; horizontal asymptote y = 0;
    hole at x = 0, y = 3/(0 + 1) = 3.

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
    LEFT,
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

GRAPH_X, GRAPH_Y = (-6, 6), (-5, 5)
X_UNIT, Y_UNIT = 0.45, 0.36


def f(x):
    """The reduced function. The original is the same everywhere except x = 0."""
    return 3 / (x + 1)


def check():
    """Re-derive every number the clip says."""
    for x in (Fraction(5), Fraction(-7, 2), Fraction(10)):
        assert x ** 2 + x == x * (x + 1)
        assert 3 * x / (x ** 2 + x) == f(x)
    assert 3 * 0 == 0 and 0 ** 2 + 0 == 0                    # the hole: top and bottom both 0
    assert f(Fraction(0)) == 3
    assert f(Fraction(-2, 5)) == 5 and f(Fraction(-8, 5)) == -5
    assert abs(f(Fraction(10 ** 6))) < Fraction(1, 1000)    # y = 0 from the degrees


check()


class RationalFunctionXHole(RationalFunctionGraph):
    graph_x, graph_y = GRAPH_X, GRAPH_Y
    x_unit, y_unit = X_UNIT, Y_UNIT
    graph_step = 1
    graph_center_y = -1.95

    def construct(self):
        s = FUNC_SIZE
        original = frac_row(s, ('f(x)', '='), tex('3x', size=s), tex('x^2', '+x', size=s), 1)
        factored = frac_row(s, ('f(x)', '='), tex('3', 'x', size=s),
                            tex('x', '(', 'x', '+1', ')', size=s), 1)
        reduced = frac_row(s, ('f(x)', '='), tex('3', size=s), tex('x', '+1', size=s), 1)
        for row in (original, factored, reduced):
            row.move_to([0, FUNC_Y, 0])
        f_top, f_bottom = reduced[1][0], reduced[1][2]
        top_x, bottom_x = factored[1][0][1], factored[1][2][0]

        # ---- the answer list ----------------------------------------------------------------
        xint_item = list_row('x', r'\text{-int: }', r'\text{none}', x=LEFT_X, y=LIST_Y[0])
        yint_item = list_row('y', r'\text{-int: }', r'\text{none}', x=LEFT_X, y=LIST_Y[1])
        va_item = list_row(r'\text{V.A.: }', 'x', '=', '-1', x=RIGHT_X, y=LIST_Y[0])
        ha_item = list_row(r'\text{H.A.: }', 'y', '=', '0', x=RIGHT_X, y=LIST_Y[1])
        holes_item = list_row(r'\text{Hole: }', '(', '0', ',', '3', ')', x=RIGHT_X, y=0.3)
        canceled_item = list_row(r'\text{Canceled: }', 'x', x=RIGHT_X, y=0.3)
        canceled = canceled_item[1]

        # ---- the y-intercept and hole rows --------------------------------------------------
        plug = tex('f(0)', '=', r'\frac{3}{0+1}', size=46).move_to([0, YINT_Y, 0])
        simple = tex('f(0)', '=', '3', size=46).move_to([0, YINT_Y, 0])
        hole_cond = tex('x', '=', '0', size=46).move_to([0, -0.45, 0])

        # ---- the horizontal asymptote rows --------------------------------------------------
        degree_top = tex(r'\text{degree of top: }', '0', size=36).move_to([0, DEGREE_Y[0], 0])
        degree_bottom = tex(r'\text{degree of bottom: }', '1', size=36
                            ).move_to([0, DEGREE_Y[1], 0])
        zero = tex('y', '=', '0', size=46).move_to([0, COEFF_Y, 0])

        # ---- the graph -----------------------------------------------------------------------
        plane = self.build_graph()
        c2p = plane.c2p
        va_line = DashedLine(c2p(-1, GRAPH_Y[0]), c2p(-1, GRAPH_Y[1]), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        ha_line = DashedLine(c2p(GRAPH_X[0], 0), c2p(GRAPH_X[1], 0), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        # The right curve is above the axis and the left curve below it, so the labels sit on
        # the empty sides: x = -1 to the left near the top, y = 0 above the line on the left.
        va_label = tex('x', '=', '-1', size=26).set_color(ASYMPTOTE_COLOR
                                                          ).next_to(c2p(-1, 4.3), LEFT, buff=0.1)
        ha_label = tex('y', '=', '0', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(-5.3, 0), UP, buff=0.08)
        hole_mark = Circle(radius=0.07, color=CURVE_COLOR, stroke_width=3,
                           fill_color=PORTAL_PAGE_WHITE, fill_opacity=1).move_to(c2p(0, 3))
        # Each branch runs to the edge of the window: f = 5 at x = -2/5, f = -5 at x = -8/5.
        right_curve = plane.plot(f, x_range=[-0.4, GRAPH_X[1], 0.02], color=CURVE_COLOR,
                                 stroke_width=5)
        left_curve = plane.plot(f, x_range=[GRAPH_X[0], -1.6, 0.02], color=CURVE_COLOR,
                                stroke_width=5)

        # ---- 1. factor the bottom -----------------------------------------------------------
        self.say('Here is a rational function. Everything must be factored first.')
        self.play(Write(original), run_time=1.3)
        self.beat('problem', READ_LONG)

        self.say('Factor an x out of the bottom.')
        self.play(ReplacementTransform(original, factored), run_time=1.5)
        self.beat('factored', READ_LONG)

        # ---- 2. cancel -----------------------------------------------------------------------
        self.say('Now check whether anything cancels. The x on top and bottom cancel.')
        strikes = strike_pair(top_x, bottom_x)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.6)
        self.beat('cancel', READ_LONG)

        self.say('After canceling, we have the reduced function. '
                 'Use it to find everything else.')
        self.play(FadeOut(strikes), copy_into(top_x, canceled),
                  FadeIn(canceled_item[0]), run_time=1.0)
        self.play(ReplacementTransform(factored, reduced), run_time=1.5)
        self.beat('reduced', READ_LONG)

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

        self.say('Simplify the bottom.')
        self.play(ReplacementTransform(plug, simple), run_time=1.3)
        self.beat('yint_simplify', READ_SHORT)

        self.say('But the zero we plugged in comes from the term that canceled.')
        self.play(Indicate(canceled, color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  copy_into(canceled, hole_cond[0]), FadeIn(VGroup(hole_cond[1], hole_cond[2])),
                  run_time=1.3)
        self.beat('yint_canceled', READ_LONG)

        self.say('So this is actually the hole. The hole is at (0, 3).')
        self.play(ReplacementTransform(canceled_item[0], holes_item[0]), FadeOut(canceled),
                  FadeIn(VGroup(holes_item[1], holes_item[3], holes_item[5])), run_time=1.0)
        self.play(copy_into(hole_cond[2], holes_item[2]), copy_into(simple[2], holes_item[4]),
                  run_time=1.3)
        self.beat('holes', READ_LONG)

        self.say('Since the hole is on the y-axis, there is no y-intercept.')
        self.play(FadeIn(yint_item), FadeOut(VGroup(hole_cond, simple)), run_time=1.3)
        self.beat('yint', READ_LONG)

        # ---- 5. vertical asymptote -----------------------------------------------------------
        self.say('For the vertical asymptote, set the bottom equal to zero and solve.')
        iso = self.solve_for_x(f_bottom, '+', '1', 'va')
        self.say('The vertical asymptote is x = −1.')
        self.play(FadeIn(VGroup(va_item[0], va_item[1], va_item[2])),
                  copy_into(iso[2], va_item[3]), run_time=1.3)
        self.play(FadeOut(iso), run_time=0.5)
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

        self.say('Sketch through the hole, up toward x = −1 and out along y = 0.')
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
        self.write_marks('rational_function_x_hole_marks.json')
