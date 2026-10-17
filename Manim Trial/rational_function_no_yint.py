"""Graphing a rational function with NO y-intercept: f(x) = (2x + 1) / x.

Chase's order, same as rational_function_graph.py (example 1):
    factored, nothing cancels -> x-intercept: top = 0 (subtract 1, divide by 2)
    -> y-intercept: plug in 0, the bottom is 0, undefined, so none
    -> vertical asymptote: bottom = 0 (x = 0, already solved)
    -> horizontal asymptote: equal degrees, divide the leading coefficients (2 / 1)
    -> holes: none -> graph: the x-intercept is the one point the curve must cross.

Verified (check() re-derives it with Fraction):
    f(x) = 2 + 1/x. x-intercept (-1/2, 0); no y-intercept (x = 0 is not in the domain);
    vertical asymptote x = 0; horizontal asymptote y = 2. Left of x = 0 the curve passes the
    x-intercept and falls to -inf (f(-1/2) = 0, f(-1/5) = -3), settling to y = 2 from below on the
    far left; right of it the curve comes down from +inf (f(1/5) = 7) to y = 2.

Reuses the helpers, layout and solving beats of example 1 (subclass).
"""

from rational_function_graph import (
    ASYMPTOTE_COLOR,
    COEFF_Y,
    CURVE_COLOR,
    DEGREE_Y,
    FUNC_SIZE,
    FUNC_Y,
    LEFT_X,
    LIST_Y,
    RESULT_Y,
    RIGHT_X,
    WORK_Y,
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
    RIGHT,
    ReplacementTransform,
    UP,
    VGroup,
    Write,
)

from math_notation import NEG, hanging_fraction  # noqa: E402
from rational_domain_range import READ_LONG, READ_SHORT, operation, tex  # noqa: E402
from scene_style import PAPER_GOLD  # noqa: E402
from solve_steps import divide_bars, strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

GRAPH_X, GRAPH_Y = (-4, 4), (-3, 7)
X_UNIT, Y_UNIT = 0.72, 0.36


def f(x):
    return 2 + 1 / x


def check():
    """Re-derive every number the clip says."""
    assert (2 * Fraction(5) + 1) / 5 == f(Fraction(5))      # 2 + 1/x is (2x + 1) / x
    assert f(Fraction(-1, 2)) == 0
    assert f(Fraction(-1, 5)) == -3 and f(Fraction(1, 5)) == 7
    assert f(Fraction(-10 ** 6)) < 2 < f(Fraction(10 ** 6))   # y = 2, approached from each side
    assert 2 / 1 == 2                                          # leading coefficients 2 and 1


check()


class RationalFunctionNoYInt(RationalFunctionGraph):
    graph_x, graph_y = GRAPH_X, GRAPH_Y
    x_unit, y_unit = X_UNIT, Y_UNIT
    graph_step = 1

    def construct(self):
        s = FUNC_SIZE
        function = frac_row(s, ('f(x)', '='), tex('2x', '+1', size=s), tex('x', size=s), 1)
        function.move_to([0, FUNC_Y, 0])
        f_top, f_bottom = function[1][0], function[1][2]

        # ---- the answer list ----------------------------------------------------------------
        xint_item = list_row('x', r'\text{-int: }', '(', hanging_fraction('1', '2'), ',', '0',
                             ')', x=LEFT_X, y=LIST_Y[0])
        yint_item = list_row('y', r'\text{-int: }', r'\text{none}', x=LEFT_X, y=0.6)
        va_item = list_row(r'\text{V.A.: }', 'x', '=', '0', x=RIGHT_X, y=LIST_Y[0])
        ha_item = list_row(r'\text{H.A.: }', 'y', '=', '2', x=RIGHT_X, y=LIST_Y[1])
        holes_item = list_row(r'\text{Hole: }', r'\text{none}', x=RIGHT_X, y=0.3)

        # ---- the x-intercept rows -----------------------------------------------------------
        cond = tex('2x', '+1', '=', '0', size=46).move_to([0, WORK_Y, 0])
        s1 = tex('2x', '=', NEG + '1', size=46).move_to([0, RESULT_Y, 0])
        done = tex('x', '=', hanging_fraction('1', '2'), size=46).move_to([0, RESULT_Y, 0])

        # ---- the y-intercept rows -----------------------------------------------------------
        def y_row(frac_tex):
            return tex('f(0)', '=', frac_tex, size=46).move_to([0, YINT_Y, 0])

        plug = y_row(r'\frac{2(0)+1}{0}')
        simple = y_row(r'\frac{1}{0}')
        undefined = tex('f(0)', '=', r'\text{undefined}', size=46).move_to([0, YINT_Y, 0])

        # ---- the vertical / horizontal asymptote rows ---------------------------------------
        va_cond = tex('x', '=', '0', size=46).move_to([0, WORK_Y, 0])
        degree_top = tex(r'\text{degree of top: }', '1', size=36).move_to([0, DEGREE_Y[0], 0])
        degree_bottom = tex(r'\text{degree of bottom: }', '1', size=36
                            ).move_to([0, DEGREE_Y[1], 0])
        coefficients = tex('y', '=', r'\frac{2}{1}', size=46).move_to([0, COEFF_Y, 0])
        coefficients_done = tex('y', '=', '2', size=46).move_to([0, COEFF_Y, 0])

        # ---- the graph -----------------------------------------------------------------------
        plane = self.build_graph()
        c2p = plane.c2p
        va_line = DashedLine(c2p(0, GRAPH_Y[0]), c2p(0, GRAPH_Y[1]), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        ha_line = DashedLine(c2p(GRAPH_X[0], 2), c2p(GRAPH_X[1], 2), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        va_label = tex('x', '=', '0', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(0, -2.4), RIGHT, buff=0.1)
        ha_label = tex('y', '=', '2', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(-3.6, 2), UP, buff=0.08)
        xint_dot = Dot(c2p(Fraction(-1, 2), 0), color=CURVE_COLOR, radius=0.07)
        # Each branch runs to the edge of the window: f = -3 at x = -1/5, f = 7 at x = 1/5.
        left_curve = plane.plot(f, x_range=[GRAPH_X[0], -0.2, 0.01], color=CURVE_COLOR,
                                stroke_width=5)
        right_curve = plane.plot(f, x_range=[0.2, GRAPH_X[1], 0.01], color=CURVE_COLOR,
                                 stroke_width=5)

        # ---- 1. factored, nothing cancels ---------------------------------------------------
        self.say('Here is a rational function. Everything must be factored first.')
        self.play(Write(function), run_time=1.3)
        self.play(Indicate(f_top, color=ASYMPTOTE_COLOR, scale_factor=1.25),
                  Indicate(f_bottom, color=ASYMPTOTE_COLOR, scale_factor=1.6), run_time=1.2)
        self.beat('problem', READ_LONG)

        self.say('Next, check whether anything cancels. Nothing does here.')
        self.beat('cancel', READ_LONG)

        # ---- 2. x-intercept ------------------------------------------------------------------
        self.say('For the x-intercept, set the top equal to zero and solve.')
        self.play(Indicate(f_top, color=ASYMPTOTE_COLOR, scale_factor=1.3),
                  copy_into(f_top, VGroup(cond[0], cond[1])),
                  FadeIn(VGroup(cond[2], cond[3])), run_time=1.3)
        self.beat('xint_set', READ_SHORT)

        op_left = operation('-', '1').next_to(cond[1], DOWN, buff=0.3)
        op_right = operation('-', '1').next_to(cond[3], DOWN, buff=0.3)
        strikes = strike_pair(cond[1], op_left)
        self.play(FadeIn(op_left, shift=DOWN * 0.15), FadeIn(op_right, shift=DOWN * 0.15),
                  run_time=0.6)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.5)
        self.play(FadeOut(VGroup(cond[1], cond[2], cond[3], op_left, strikes)),
                  copy_into(cond[0], s1[0]), FadeIn(s1[1]), copy_into(op_right, s1[2]),
                  run_time=0.9)
        self.play(FadeOut(VGroup(cond[0], op_right)),
                  s1.animate.move_to([0, WORK_Y, 0]), run_time=0.5)
        self.beat('xint_s1', READ_SHORT)

        self.say('Divide both sides by 2.')
        bars, divisors = divide_bars([s1[0], s1[2]], '2')
        self.play(*[Create(b) for b in bars],
                  *[FadeIn(d, shift=DOWN * 0.15) for d in divisors], run_time=0.9)
        self.beat('xint_bars', READ_SHORT)
        self.play(copy_into(VGroup(s1[0], divisors[0]), done[0]), FadeIn(done[1]),
                  copy_into(VGroup(s1[2], divisors[1]), done[2]), run_time=1.1)
        self.beat('xint_solved', READ_SHORT)

        self.say('The x-intercept is (−1/2, 0).')
        self.play(FadeIn(VGroup(*[xint_item[i] for i in (0, 1, 2, 4, 5, 6)])),
                  copy_into(done[2], xint_item[3]), run_time=1.3)
        self.play(FadeOut(VGroup(s1, bars, divisors, done)), run_time=0.5)
        self.beat('xint', READ_LONG)

        # ---- 3. y-intercept ------------------------------------------------------------------
        self.say('For the y-intercept, plug in zero for x.')
        self.play(Indicate(f_top[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(plug), run_time=1.3)
        self.beat('yint_plug', READ_LONG)

        self.say('Simplify the top.')
        self.play(ReplacementTransform(plug, simple), run_time=1.3)
        self.beat('yint_simplify', READ_SHORT)

        self.say('The bottom is zero, and we cannot divide by zero. '
                 'So there is no y-intercept.')
        self.play(ReplacementTransform(simple, undefined), run_time=1.3)
        self.play(FadeIn(yint_item), run_time=1.0)
        self.beat('yint', READ_LONG)
        self.play(FadeOut(undefined), run_time=0.5)

        # ---- 4. vertical asymptote -----------------------------------------------------------
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

        # ---- 5. horizontal asymptote ---------------------------------------------------------
        self.say('For the horizontal asymptote, compare the degrees of the top and the bottom.')
        self.play(Indicate(f_top[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(degree_top), FadeIn(degree_bottom), run_time=1.5)
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

        self.say('Plot the x-intercept.')
        self.play(FadeIn(xint_dot, scale=1.6), run_time=1.0)
        self.beat('points', READ_SHORT)

        self.say('There is no y-intercept, but the x-intercept is a point the curve must '
                 'cross. Start on the side that has it.')
        self.play(Indicate(xint_dot, color=PAPER_GOLD, scale_factor=2.0), run_time=1.3)
        self.beat('cross', READ_LONG)

        self.say('Sketch through the x-intercept, heading down toward x = 0 '
                 'and leveling out along y = 2.')
        self.play(Create(left_curve), run_time=2.5)
        self.beat('left_curve', READ_LONG)

        self.say('This side is going down, so the diagonally opposite side goes up.')
        self.play(Indicate(left_curve, color=PAPER_GOLD, scale_factor=1.06), run_time=1.3)
        self.beat('opposite', READ_LONG)

        self.say('Sketch the other curve, coming down from the top and leveling out '
                 'along y = 2.')
        self.play(Create(right_curve), run_time=2.5)
        self.beat('hold', READ_LONG)
        self.write_marks('rational_function_no_yint_marks.json')
