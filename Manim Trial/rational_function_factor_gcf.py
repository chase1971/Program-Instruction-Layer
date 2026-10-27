"""Graphing a rational function whose top needs a common factor: f(x) = (2x - 4) / (x + 1).

Chase's order, same as rational_function_graph.py (example 1), with a factoring step first:
    factor the top (pull out the 2) -> check whether anything cancels (nothing does)
    -> x-intercept: top = 0 (the 2 can never be 0, so x - 2 = 0)
    -> y-intercept: plug in 0 -> vertical asymptote: bottom = 0
    -> horizontal asymptote: equal degrees, divide the leading coefficients (2 / 1)
    -> holes: none
    -> graph: dashed asymptotes, both intercepts, sketch the side that has them first, the other
       side goes the opposite way.

Verified (check() re-derives it with Fraction):
    2x - 4 = 2(x - 2); x-intercept (2, 0); y-intercept (0, -4); vertical asymptote x = -1;
    equal degrees so horizontal asymptote y = 2/1 = 2; nothing cancels so no holes.
    Right of x = -1 the curve falls to -inf at the asymptote, passes (0, -4) and (2, 0) and levels
    out below y = 2; left of it the curve comes down from +inf (f(-3) = 5) toward y = 2.

Reuses the helpers and layout of example 1 (subclass), see rational_function_graph.py.
"""

from rational_function_graph import (
    ASYMPTOTE_COLOR,
    COEFF_Y,
    CURVE_COLOR,
    DEGREE_Y,
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
    Create,
    DashedLine,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LEFT,
    ReplacementTransform,
    UR,
    VGroup,
    Write,
)

from rational_domain_range import READ_LONG, READ_SHORT, tex  # noqa: E402
from scene_style import PAPER_GOLD  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402


def f(x):
    return (2 * x - 4) / (x + 1)


def check():
    """Re-derive every number the clip says."""
    for x in (Fraction(3), Fraction(-7, 2), Fraction(10)):
        assert 2 * x - 4 == 2 * (x - 2)
    assert f(Fraction(2)) == 0
    assert f(Fraction(0)) == -4
    assert f(Fraction(-3)) == 5
    assert Fraction(2, 1) == 2                       # leading coefficients 2 and 1: y = 2
    assert f(Fraction(-2)) == 8 and f(Fraction(-2, 5)) == -8
    assert abs(f(Fraction(10 ** 6)) - 2) < Fraction(1, 1000)


check()


class RationalFunctionFactorGcf(RationalFunctionGraph):
    def construct(self):
        s = FUNC_SIZE
        original = frac_row(s, ('f(x)', '='), tex('2x', '-4', size=s), tex('x', '+1', size=s), 1)
        function = frac_row(s, ('f(x)', '='),
                            tex('2', '(', 'x', '-2', ')', size=s), tex('x', '+1', size=s), 1)
        for row in (original, function):
            row.move_to([0, FUNC_Y, 0])
        f_top, f_bottom = function[1][0], function[1][2]
        top_factor = VGroup(f_top[2], f_top[3])          # the x - 2 inside the parentheses

        # ---- the answer list ----------------------------------------------------------------
        xint_item = list_row('x', r'\text{-int: }', '(', '2', ',', '0', ')',
                             x=LEFT_X, y=LIST_Y[0])
        yint_item = list_row('y', r'\text{-int: }', '(', '0', ',', '-4', ')',
                             x=LEFT_X, y=LIST_Y[1])
        holes_item = list_row(r'\text{Holes: }', r'\text{none}', x=LEFT_X, y=LIST_Y[2])
        va_item = list_row(r'\text{V.A.: }', 'x', '=', '-1', x=RIGHT_X, y=LIST_Y[0])
        ha_item = list_row(r'\text{H.A.: }', 'y', '=', '2', x=RIGHT_X, y=LIST_Y[1])

        # ---- the y-intercept rows -----------------------------------------------------------
        def y_row(frac_tex):
            return tex('f(0)', '=', frac_tex, size=46).move_to([0, YINT_Y, 0])

        plug = y_row(r'\frac{2(0-2)}{0+1}')
        simple_top = y_row(r'\frac{2(-2)}{1}')
        answer = tex('f(0)', '=', '-4', size=46).move_to([0, YINT_Y, 0])

        # ---- the horizontal asymptote rows --------------------------------------------------
        degree_top = tex(r'\text{degree of top: }', '1', size=36).move_to([0, DEGREE_Y[0], 0])
        degree_bottom = tex(r'\text{degree of bottom: }', '1', size=36
                            ).move_to([0, DEGREE_Y[1], 0])
        coefficients = tex('y', '=', r'\frac{2}{1}', size=46).move_to([0, COEFF_Y, 0])
        coefficients_done = tex('y', '=', '2', size=46).move_to([0, COEFF_Y, 0])

        # ---- the graph -----------------------------------------------------------------------
        plane = self.build_graph()
        c2p = plane.c2p

        def dot(x, y):
            return Dot(c2p(x, y), color=CURVE_COLOR, radius=0.07)

        va_line = DashedLine(c2p(-1, GRAPH_Y[0]), c2p(-1, GRAPH_Y[1]), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        ha_line = DashedLine(c2p(GRAPH_X[0], 2), c2p(GRAPH_X[1], 2), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        # The right curve is at y = -6.5 near x = -0.5, so the label sits on the empty left side.
        va_label = tex('x', '=', '-1', size=26).set_color(ASYMPTOTE_COLOR
                                                          ).next_to(c2p(-1, -6.5), LEFT, buff=0.1)
        # The left curve rides above y = 2, so the label goes under the line.
        ha_label = tex('y', '=', '2', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(-10, 2), DOWN, buff=0.08)
        points = VGroup(dot(2, 0), dot(0, -4))
        # Each branch runs to the edge of the window: f = 8 at x = -2, f = -8 at x = -2/5.
        left_curve = plane.plot(f, x_range=[GRAPH_X[0], -2, 0.02], color=CURVE_COLOR,
                                stroke_width=5)
        right_curve = plane.plot(f, x_range=[-0.4, GRAPH_X[1], 0.02], color=CURVE_COLOR,
                                 stroke_width=5)

        # ---- 1. factor the top, nothing cancels ---------------------------------------------
        self.say('Here is a rational function. Everything must be factored first.')
        self.play(Write(original), run_time=1.3)
        self.beat('problem', READ_LONG)

        self.say('Factor the common factor of 2 out of the top.')
        self.play(ReplacementTransform(original, function), run_time=1.5)
        self.beat('factored', READ_LONG)

        self.say('Next, check whether anything cancels. Nothing does here.')
        self.play(Indicate(f_top, color=ASYMPTOTE_COLOR, scale_factor=1.25),
                  Indicate(f_bottom, color=ASYMPTOTE_COLOR, scale_factor=1.25), run_time=1.2)
        self.beat('cancel', READ_LONG)

        # ---- 2. x-intercept ------------------------------------------------------------------
        self.say('For the x-intercept, set the top equal to zero. The 2 can never be zero, '
                 'so solve x − 2 = 0.')
        iso = self.solve_for_x(top_factor, '-', '2', 'xint')
        self.say('The x-intercept is (2, 0).')
        self.play(FadeIn(VGroup(*[xint_item[i] for i in (0, 1, 2, 4, 5, 6)])),
                  copy_into(iso[2], xint_item[3]), run_time=1.3)
        self.play(FadeOut(iso), run_time=0.5)
        self.beat('xint', READ_LONG)

        # ---- 3. y-intercept ------------------------------------------------------------------
        self.say('For the y-intercept, plug in zero for x.')
        self.play(Indicate(f_top[2], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(plug), run_time=1.3)
        self.beat('yint_plug', READ_LONG)

        self.say('Simplify inside the parentheses and the bottom.')
        self.play(ReplacementTransform(plug, simple_top), run_time=1.3)
        self.beat('yint_simplify', READ_SHORT)

        self.say('Multiply the top, then divide by 1.')
        self.play(ReplacementTransform(simple_top, answer), run_time=1.3)
        self.beat('yint_multiply', READ_SHORT)

        self.say('The y-intercept is (0, −4).')
        self.play(FadeIn(VGroup(*[yint_item[i] for i in (0, 1, 2, 3, 4, 6)])),
                  copy_into(answer[2], yint_item[5]), run_time=1.3)
        self.play(FadeOut(answer), run_time=0.5)
        self.beat('yint', READ_LONG)

        # ---- 4. vertical asymptote -----------------------------------------------------------
        self.say('For the vertical asymptote, set the bottom equal to zero and solve.')
        iso = self.solve_for_x(f_bottom, '+', '1', 'va')
        self.say('The vertical asymptote is x = −1.')
        self.play(FadeIn(VGroup(va_item[0], va_item[1], va_item[2])),
                  copy_into(iso[2], va_item[3]), run_time=1.3)
        self.play(FadeOut(iso), run_time=0.5)
        self.beat('va', READ_LONG)

        # ---- 5. horizontal asymptote ---------------------------------------------------------
        self.say('For the horizontal asymptote, compare the degrees. '
                 'The degree is the power on x.')
        # Show the invisible power of 1 on each x once, pulse it, then take it away.
        powers = VGroup(*[tex('1', size=20).set_color(ASYMPTOTE_COLOR
                                                      ).move_to(x_term.get_corner(UR) + [0.1, lift, 0])
                          for x_term, lift in ((f_top[2], 0.08), (f_bottom[0], 0.0))])
        self.play(FadeIn(powers, scale=1.4), run_time=0.8)
        self.play(Indicate(VGroup(f_top[2], powers[0]), color=ASYMPTOTE_COLOR, scale_factor=1.5),
                  Indicate(VGroup(f_bottom[0], powers[1]), color=ASYMPTOTE_COLOR,
                           scale_factor=1.5), run_time=1.5)
        self.play(FadeOut(powers), run_time=0.5)
        self.beat('ha_power', READ_SHORT)

        self.say('The degree of the top is 1 and the degree of the bottom is 1.')
        self.play(FadeIn(degree_top), FadeIn(degree_bottom), run_time=1.2)
        self.beat('ha_degrees', READ_LONG)

        self.say('The degrees are equal, so divide the leading coefficients.')
        self.play(FadeIn(coefficients), run_time=1.2)
        self.beat('ha_coefficients', READ_LONG)

        self.say('The leading coefficients are 2 and 1, so the horizontal asymptote is y = 2.')
        self.play(ReplacementTransform(coefficients, coefficients_done), run_time=1.2)
        self.play(FadeIn(VGroup(ha_item[0], ha_item[1], ha_item[2])),
                  copy_into(coefficients_done[2], ha_item[3]), run_time=1.3)
        self.play(FadeOut(VGroup(coefficients_done, degree_top, degree_bottom)), run_time=0.5)
        self.beat('ha', READ_LONG)

        # ---- 6. holes ------------------------------------------------------------------------
        self.say('Holes come from factors that cancel. Nothing canceled, so there are no holes.')
        self.play(FadeIn(holes_item), run_time=1.0)
        self.beat('holes', READ_LONG)

        # ---- 7. the graph --------------------------------------------------------------------
        self.say('Now graph it. Draw the asymptotes as dashed lines.')
        self.play(FadeIn(plane), run_time=1.0)
        self.play(Create(va_line), Create(ha_line), FadeIn(VGroup(va_label, ha_label)),
                  run_time=1.5)
        self.beat('asymptotes', READ_LONG)

        self.say('Plot the intercepts.')
        self.play(FadeIn(points, scale=1.6), run_time=1.0)
        self.beat('points', READ_SHORT)

        self.say('To sketch the curve, look for points it has to cross. '
                 'Start on the side that has them.')
        self.play(Indicate(points[0], color=PAPER_GOLD, scale_factor=2.0),
                  Indicate(points[1], color=PAPER_GOLD, scale_factor=2.0), run_time=1.3)
        self.beat('cross', READ_LONG)

        self.say('Sketch through both points. The curve heads down toward the vertical '
                 'asymptote and levels out along y = 2 on the far right.')
        self.play(Create(right_curve), run_time=2.5)
        self.beat('right_curve', READ_LONG)

        self.say('This side is going down, so on the opposite side of the asymptote '
                 'the curve goes up.')
        self.play(Indicate(right_curve, color=PAPER_GOLD, scale_factor=1.06), run_time=1.3)
        self.beat('opposite', READ_LONG)

        self.say('So the other curve is up here. Sketch it, coming down from the top '
                 'and leveling out along y = 2.')
        self.play(Create(left_curve), run_time=2.5)
        self.beat('hold', READ_LONG)
        self.write_marks('rational_function_factor_gcf_marks.json')
