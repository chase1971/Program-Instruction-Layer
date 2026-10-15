"""Graphing a rational function with a hole: f(x) = (x + 3) / (x^2 - 9).

Chase's order, same as rational_function_graph.py (example 1), with the cancel step doing work:
    factor the bottom (difference of squares) -> cancel x + 3 top and bottom
    -> from here on use the REDUCED function 1 / (x - 3) for everything
    -> x-intercept: the top is just the number 1, no x, so none
    -> y-intercept: plug in 0 -> vertical asymptote: bottom = 0
    -> horizontal asymptote: bottom has the bigger degree, so y = 0
    -> hole: bring back the canceled factor, set it to 0, solve, plug into the REDUCED function
    -> graph: dashed asymptotes, the y-intercept and an open circle at the hole, one curve
       through them, the other in the diagonally opposite corner.

Verified (check() re-derives it with Fraction):
    x^2 - 9 = (x + 3)(x - 3); reduced f = 1/(x - 3); no x-intercept; y-intercept (0, -1/3);
    vertical asymptote x = 3 (NOT x = -3, that is the hole); horizontal asymptote y = 0;
    hole at x = -3, y = 1/(-3 - 3) = -1/6.

Reuses the helpers and layout of example 1 (subclass), see rational_function_graph.py.
"""

from rational_function_graph import (
    ASYMPTOTE_COLOR,
    CURVE_COLOR,
    DEGREE_Y,
    COEFF_Y,
    FUNC_SIZE,
    FUNC_Y,
    GRAPH_X,
    GRAPH_Y,
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
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    RIGHT,
    ReplacementTransform,
    UP,
    VGroup,
    Write,
)

from math_notation import NEG, hanging_fraction  # noqa: E402
from rational_domain_range import READ_LONG, READ_SHORT, tex  # noqa: E402
from scene_style import PAPER_GOLD, PORTAL_PAGE_WHITE  # noqa: E402
from solve_steps import strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402


def f(x):
    """The reduced function. The original is the same everywhere except x = -3."""
    return 1 / (x - 3)


def check():
    """Re-derive every number the clip says."""
    x = Fraction(7)                                        # any x, not a root of x^2 - 9
    assert (x + 3) / (x ** 2 - 9) == f(x)
    assert f(Fraction(0)) == Fraction(-1, 3)
    assert f(Fraction(-3)) == Fraction(-1, 6)
    assert (-3) ** 2 - 9 == 0 and -3 + 3 == 0              # the hole: top and bottom both 0
    assert f(Fraction(10 ** 6)) < Fraction(1, 1000)        # y = 0 from the degrees


check()


class RationalFunctionHole(RationalFunctionGraph):
    def construct(self):
        s = FUNC_SIZE
        original = frac_row(s, ('f(x)', '='), tex('x', '+3', size=s), tex('x^2', '-9', size=s), 1)
        factored = frac_row(s, ('f(x)', '='), tex('x', '+3', size=s),
                            tex('(', 'x', '+3', ')', '(', 'x', '-3', ')', size=s), 1)
        reduced = frac_row(s, ('f(x)', '='), tex('1', size=s), tex('x', '-3', size=s), 1)
        for row in (original, factored, reduced):
            row.move_to([0, FUNC_Y, 0])
        f_top, f_bottom = reduced[1][0], reduced[1][2]
        factor_top, factor_bottom = factored[1][0], VGroup(*factored[1][2][0:4])

        # ---- the answer list ----------------------------------------------------------------
        xint_item = list_row('x', r'\text{-int: }', r'\text{none}', x=LEFT_X, y=LIST_Y[0])
        yint_item = list_row('y', r'\text{-int: }', '(', '0', ',', hanging_fraction('1', '3'), ')',
                             x=LEFT_X, y=LIST_Y[1])
        holes_item = list_row(r'\text{Holes: }', '(', NEG + '3', ',', hanging_fraction('1', '6'),
                              ')', x=LEFT_X, y=LIST_Y[2])
        va_item = list_row(r'\text{V.A.: }', 'x', '=', '3', x=RIGHT_X, y=LIST_Y[0])
        ha_item = list_row(r'\text{H.A.: }', 'y', '=', '0', x=RIGHT_X, y=LIST_Y[1])
        canceled_item = list_row(r'\text{Canceled: }', 'x', '+3', x=RIGHT_X, y=LIST_Y[2])
        canceled = VGroup(canceled_item[1], canceled_item[2])

        # ---- the y-intercept rows -----------------------------------------------------------
        def y_row(frac_tex, lhs='f(0)'):
            return tex(lhs, '=', frac_tex, size=46).move_to([0, YINT_Y, 0])

        plug = y_row(r'\frac{1}{0-3}')
        simple = y_row(r'\frac{1}{' + NEG + '3}')
        negative_up = y_row(hanging_fraction('1', '3'))

        # ---- the horizontal asymptote rows --------------------------------------------------
        degree_top = tex(r'\text{degree of top: }', '0', size=36).move_to([0, DEGREE_Y[0], 0])
        degree_bottom = tex(r'\text{degree of bottom: }', '1', size=36
                            ).move_to([0, DEGREE_Y[1], 0])
        zero = tex('y', '=', '0', size=46).move_to([0, COEFF_Y, 0])

        # ---- the hole rows ------------------------------------------------------------------
        hole_plug = y_row(r'\frac{1}{' + NEG + '3-3}', lhs='f(' + NEG + '3)')
        hole_simple = y_row(r'\frac{1}{' + NEG + '6}', lhs='f(' + NEG + '3)')
        hole_up = y_row(hanging_fraction('1', '6'), lhs='f(' + NEG + '3)')

        # ---- the graph -----------------------------------------------------------------------
        plane = self.build_graph()
        c2p = plane.c2p
        va_line = DashedLine(c2p(3, GRAPH_Y[0]), c2p(3, GRAPH_Y[1]), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        ha_line = DashedLine(c2p(GRAPH_X[0], 0), c2p(GRAPH_X[1], 0), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        va_label = tex('x', '=', '3', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(3, -6.5), RIGHT, buff=0.1)
        ha_label = tex('y', '=', '0', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(-10, 0), UP, buff=0.08)
        yint_dot = Dot(c2p(0, Fraction(-1, 3)), color=CURVE_COLOR, radius=0.07)
        hole_mark = Circle(radius=0.075, color=CURVE_COLOR, stroke_width=4, fill_color=PORTAL_PAGE_WHITE,
                           fill_opacity=1).move_to(c2p(-3, Fraction(-1, 6)))
        # Each branch runs to the edge of the window: f = -8 at x = 23/8, f = 8 at x = 25/8.
        left_curve = plane.plot(f, x_range=[GRAPH_X[0], 23 / 8, 0.02], color=CURVE_COLOR,
                                stroke_width=5)
        right_curve = plane.plot(f, x_range=[25 / 8, GRAPH_X[1], 0.02], color=CURVE_COLOR,
                                 stroke_width=5)

        # ---- 1. factor the bottom -----------------------------------------------------------
        self.say('Here is a rational function. Everything must be factored first.')
        self.play(Write(original), run_time=1.3)
        self.beat('problem', READ_LONG)

        self.say('The bottom is a difference of squares, so it factors.')
        self.play(ReplacementTransform(original, factored), run_time=1.5)
        self.beat('factored', READ_LONG)

        # ---- 2. cancel -----------------------------------------------------------------------
        self.say('Now check whether anything cancels. The x + 3 on top and bottom cancel.')
        strikes = strike_pair(factor_top, factor_bottom)
        self.play(Create(strikes[0]), run_time=0.5)
        self.play(Create(strikes[1]), run_time=0.5)
        self.beat('cancel', READ_LONG)

        self.say('After canceling, we have the reduced function. '
                 'Use it to find everything else.')
        self.play(FadeOut(strikes), copy_into(factor_top, canceled),
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

        self.say('Move the negative to the top number.')
        self.play(ReplacementTransform(simple, negative_up), run_time=1.3)
        self.beat('yint_negative', READ_SHORT)

        self.say('The y-intercept is (0, −1/3).')
        self.play(FadeIn(VGroup(*[yint_item[i] for i in (0, 1, 2, 3, 4, 6)])),
                  copy_into(negative_up[2], yint_item[5]), run_time=1.3)
        self.play(FadeOut(negative_up), run_time=0.5)
        self.beat('yint', READ_LONG)

        # ---- 5. vertical asymptote -----------------------------------------------------------
        self.say('For the vertical asymptote, set the bottom equal to zero and solve.')
        iso = self.solve_for_x(f_bottom, '-', '3', 'va')
        self.say('The vertical asymptote is x = 3.')
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

        # ---- 7. the hole ---------------------------------------------------------------------
        self.say('Now the hole. Bring back the term that canceled, set it equal to zero, '
                 'and solve.')
        iso = self.solve_for_x(canceled, '+', '3', 'hole')

        self.say('Plug that x into the reduced function to find the y.')
        self.play(FadeOut(iso), Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(hole_plug), run_time=1.3)
        self.beat('hole_plug', READ_LONG)

        self.say('Simplify the bottom.')
        self.play(ReplacementTransform(hole_plug, hole_simple), run_time=1.3)
        self.beat('hole_simplify', READ_SHORT)

        self.say('Move the negative to the top number.')
        self.play(ReplacementTransform(hole_simple, hole_up), run_time=1.3)
        self.beat('hole_negative', READ_SHORT)

        self.say('The hole is at (−3, −1/6).')
        self.play(FadeIn(VGroup(*[holes_item[i] for i in (0, 1, 2, 3, 5)])),
                  copy_into(hole_up[2], holes_item[4]), run_time=1.3)
        self.play(FadeOut(hole_up), FadeOut(VGroup(canceled_item[0], canceled)), run_time=0.5)
        self.beat('holes', READ_LONG)

        # ---- 8. the graph --------------------------------------------------------------------
        self.say('Now graph it. Draw the asymptotes as dashed lines.')
        self.play(FadeIn(plane), run_time=1.0)
        self.play(Create(va_line), Create(ha_line), FadeIn(VGroup(va_label, ha_label)),
                  run_time=1.5)
        self.beat('asymptotes', READ_LONG)

        self.say('Plot the y-intercept. Mark the hole with an open circle.')
        self.play(FadeIn(yint_dot, scale=1.6), FadeIn(hole_mark, scale=1.6), run_time=1.0)
        self.beat('points', READ_LONG)

        self.say('There is no x-intercept, but the y-intercept shows where this curve goes. '
                 'It is below the x-axis, so there is only one place the curve can go.')
        self.play(Indicate(yint_dot, color=PAPER_GOLD, scale_factor=2.0), run_time=1.3)
        self.beat('cross', READ_LONG)

        self.say('Sketch through the point and the hole. The curve heads down toward the '
                 'vertical asymptote and levels out along y = 0 on the far left.')
        self.play(Create(left_curve), run_time=2.5)
        self.add(hole_mark)
        self.beat('left_curve', READ_LONG)

        self.say('This side is going down, so the diagonally opposite side goes up.')
        self.play(Indicate(left_curve, color=PAPER_GOLD, scale_factor=1.06), run_time=1.3)
        self.beat('opposite', READ_LONG)

        self.say('Sketch the other curve, coming down from the top and leveling out '
                 'along y = 0.')
        self.play(Create(right_curve), run_time=2.5)
        self.beat('hold', READ_LONG)
        self.write_marks('rational_function_hole_marks.json')
