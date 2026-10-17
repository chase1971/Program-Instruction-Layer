"""Graphing a rational function with a SLANT asymptote: f(x) = (2x - 3)(x + 1) / (x - 1).

Chase's order, same as rational_function_graph.py (example 1):
    factored, nothing cancels -> x-intercepts: each factor of the top = 0
    -> y-intercept: plug in 0 -> vertical asymptote: bottom = 0
    -> horizontal asymptote: the top has the bigger degree, so none -- but one degree bigger
       means a slant: multiply the top out and divide by the bottom (synthetic division with 1);
       the quotient 2x + 1 is the slant, the remainder is ignored
    -> holes: none -> graph: start on the side with the most points, the other side goes the
       opposite way, both curves ride the slant.

Verified (check() re-derives it with Fraction):
    (2x - 3)(x + 1) = 2x^2 - x - 3 and f(x) = 2x + 1 - 2/(x - 1). x-intercepts (3/2, 0) and (-1, 0);
    y-intercept (0, 3); vertical asymptote x = 1; slant y = 2x + 1; nothing cancels.
    Left of x = 1 the curve passes (-1, 0) and (0, 3) and rises to +inf (above the slant);
    right of it the curve comes up from -inf through (3/2, 0) and follows the slant from below.

Reuses the helpers, layout and solving beats of example 1 (subclass).
"""

from rational_function_graph import (
    ASYMPTOTE_COLOR,
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
from math import sqrt  # noqa: E402

from manim import (  # noqa: E402
    Create,
    DashedLine,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LEFT,
    Arrow,
    Line,
    Rectangle,
    RIGHT,
    ReplacementTransform,
    UP,
    VGroup,
    Write,
)

from math_notation import NEG, hanging_fraction  # noqa: E402
from rational_domain_range import READ_LONG, READ_SHORT, operation, tex  # noqa: E402
from scene_style import PAPER_GOLD, PAPER_INK  # noqa: E402
from solve_steps import divide_bars, strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

GRAPH_X, GRAPH_Y = (-4, 4), (-8, 10)
X_UNIT, Y_UNIT = 0.72, 0.185
GRAPH_CENTER_Y = -2.08

# Synthetic division grid: the 1 outside, then the coefficients 2, -1, -3 in three columns.
ROOT_X, COL_X = -2.4, (-1.3, -0.3, 0.7)
CORNER_X, RULE_END_X = -1.9, 1.25
COEFF_Y, PRODUCT_Y, RESULT_ROW_Y = -1.65, -2.2, -2.8
SLANT_Y = -3.5


def f(x):
    return (2 * x * x - x - 3) / (x - 1)


def check():
    """Re-derive every number the clip says."""
    for x in (Fraction(5), Fraction(-7), Fraction(1, 3)):          # (2x - 3)(x + 1) = 2x^2 - x - 3
        assert (2 * x - 3) * (x + 1) == 2 * x * x - x - 3
        assert f(x) == 2 * x + 1 - Fraction(2) / (x - 1)           # quotient 2x + 1, remainder -2
    assert f(Fraction(3, 2)) == 0 and f(Fraction(-1)) == 0
    assert f(Fraction(0)) == 3
    assert 1 - 1 == 0                                              # bottom is zero at x = 1
    assert 2 * 1 + (-1) == 1 and 1 * 1 + (-3) == -2                # the synthetic division
    assert f(Fraction(10 ** 6)) < 2 * 10 ** 6 + 1 and f(Fraction(-10 ** 6)) > -2 * 10 ** 6 + 1


check()

# Where each branch leaves the window: f = 10 on the left (x = (11 - sqrt 65) / 4),
# f = -8 on the right (x = (-7 + sqrt 137) / 4).
LEFT_END = (11 - sqrt(65)) / 4
RIGHT_START = (-7 + sqrt(137)) / 4


class RationalFunctionSlant(RationalFunctionGraph):
    graph_x, graph_y = GRAPH_X, GRAPH_Y
    x_unit, y_unit = X_UNIT, Y_UNIT
    graph_step = 1
    graph_center_y = GRAPH_CENTER_Y

    def construct(self):
        s = FUNC_SIZE
        function = frac_row(s, ('f(x)', '='),
                            tex('(', '2x', '-3', ')', '(', 'x', '+1', ')', size=s),
                            tex('x', '-1', size=s), 1)
        unfactored = frac_row(s, ('f(x)', '='), tex('2x^2', '-x', '-3', size=s),
                              tex('x', '-1', size=s), 1)
        unfactored.move_to([0, FUNC_Y, 0])
        function.move_to([0, FUNC_Y, 0])
        f_top, f_bottom = function[1][0], function[1][2]
        factor_a, factor_b = VGroup(*f_top[0:4]), VGroup(*f_top[4:8])

        # ---- the answer list ----------------------------------------------------------------
        xint_a = list_row('x', r'\text{-int: }', '(', r'\frac{3}{2}', ',', '0', ')',
                          x=LEFT_X, y=LIST_Y[0])
        xint_b = list_row('x', r'\text{-int: }', '(', NEG + '1', ',', '0', ')',
                          x=LEFT_X, y=LIST_Y[1])
        yint_item = list_row('y', r'\text{-int: }', '(', '0', ',', '3', ')',
                             x=LEFT_X, y=LIST_Y[2])
        holes_item = list_row(r'\text{Hole: }', r'\text{none}', x=LEFT_X, y=-0.3)
        va_item = list_row(r'\text{V.A.: }', 'x', '=', '1', x=RIGHT_X, y=LIST_Y[0])
        ha_item = list_row(r'\text{H.A.: }', r'\text{none}', x=RIGHT_X, y=LIST_Y[1])
        slant_item = list_row(r'\text{Slant: }', 'y', '=', '2x', '+1', x=RIGHT_X, y=LIST_Y[2])

        # ---- the 2x - 3 = 0 rows -------------------------------------------------------------
        cond = tex('2x', '-3', '=', '0', size=46).move_to([0, WORK_Y, 0])
        s1 = tex('2x', '=', '3', size=46).move_to([0, RESULT_Y, 0])
        done = tex('x', '=', r'\frac{3}{2}', size=46).move_to([0, RESULT_Y, 0])

        # ---- the y-intercept rows ------------------------------------------------------------
        def y_row(rhs):
            return tex('f(0)', '=', rhs, size=42).move_to([0, YINT_Y, 0])

        plug = y_row(r'\frac{(2(0)-3)(0+1)}{0-1}')
        simple = y_row(r'\frac{(' + NEG + r'3)(1)}{' + NEG + '1}')
        answer = y_row('3')

        # ---- the horizontal asymptote rows ---------------------------------------------------
        degree_top = tex(r'\text{degree of top: }', '2', size=36).move_to([0, DEGREE_Y[0], 0])
        degree_bottom = tex(r'\text{degree of bottom: }', '1', size=36
                            ).move_to([0, DEGREE_Y[1], 0])

        # ---- the slant: multiply the top out, then synthetic division --------------------------
        multiplied = tex('2x^2', '-x', '-3', size=46).move_to([0, WORK_Y, 0])

        def cell(text, col, y):
            return tex(text, size=46).move_to([COL_X[col], y, 0])

        root = tex('1', size=46).move_to([ROOT_X, COEFF_Y, 0])
        coeffs = VGroup(cell('2', 0, COEFF_Y), cell(NEG + '1', 1, COEFF_Y),
                        cell(NEG + '3', 2, COEFF_Y))
        down = cell('2', 0, RESULT_ROW_Y)
        product_1 = cell('2', 1, PRODUCT_Y)
        sum_1 = cell('1', 1, RESULT_ROW_Y)
        product_2 = cell('1', 2, PRODUCT_Y)
        sum_2 = cell(NEG + '2', 2, RESULT_ROW_Y)
        for product in (product_1, product_2):
            product.set_color(PAPER_GOLD)
        rule_y = PRODUCT_Y - 0.25
        corner = Line([CORNER_X, COEFF_Y + 0.35, 0], [CORNER_X, rule_y, 0], color=PAPER_INK,
                      stroke_width=4)
        rule = Line([CORNER_X, rule_y, 0], [RULE_END_X, rule_y, 0], color=PAPER_INK,
                    stroke_width=4)
        plus = tex('+', size=40).move_to([ROOT_X, PRODUCT_Y, 0])
        arrow = Arrow([COL_X[0], COEFF_Y - 0.35, 0], [COL_X[0], rule_y - 0.02, 0], buff=0,
                      color=PAPER_INK, stroke_width=5, max_tip_length_to_length_ratio=0.3)
        remainder_box = Rectangle(width=0.8, height=0.6, color=PAPER_INK, stroke_width=4
                                  ).move_to(sum_2)
        remainder_label = tex(r'\text{remainder}', size=28).next_to(remainder_box, RIGHT, buff=0.04)
        slant_row = tex('y', '=', '2x', '+1', size=46).move_to([0, SLANT_Y, 0])
        division = VGroup(root, coeffs, down, product_1, sum_1, product_2, sum_2, corner, rule,
                          plus, arrow, remainder_box, remainder_label)

        # ---- the graph -----------------------------------------------------------------------
        plane = self.build_graph()
        c2p = plane.c2p
        va_line = DashedLine(c2p(1, GRAPH_Y[0]), c2p(1, GRAPH_Y[1]), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        slant_line = DashedLine(c2p(-4, -7), c2p(4, 9), color=ASYMPTOTE_COLOR,
                                stroke_width=4, dash_length=0.12)
        va_label = tex('x', '=', '1', size=24).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(1, -4), LEFT,
                                                                   buff=0.06)
        slant_label = tex('y', '=', '2x', '+1', size=26).set_color(ASYMPTOTE_COLOR
                                                                    ).move_to(c2p(2.2, 8.8))
        xint_dots = VGroup(*[Dot(c2p(x, 0), color=CURVE_COLOR, radius=0.07)
                             for x in (Fraction(-1), Fraction(3, 2))])
        yint_dot = Dot(c2p(0, 3), color=CURVE_COLOR, radius=0.07)
        left_curve = plane.plot(f, x_range=[GRAPH_X[0], LEFT_END, 0.01], color=CURVE_COLOR,
                                stroke_width=5)
        right_curve = plane.plot(f, x_range=[RIGHT_START, GRAPH_X[1], 0.01], color=CURVE_COLOR,
                                 stroke_width=5)

        # ---- 1. factored, nothing cancels ---------------------------------------------------
        self.say('Here is a rational function. Everything must be factored first.')
        self.play(Write(unfactored), run_time=1.3)
        self.beat('problem_start', READ_LONG)

        self.say('Factor the top: 2x² − x − 3 = (2x − 3)(x + 1).')
        self.play(ReplacementTransform(unfactored, function), run_time=1.5)
        self.play(Indicate(f_top, color=ASYMPTOTE_COLOR, scale_factor=1.15),
                  Indicate(f_bottom, color=ASYMPTOTE_COLOR, scale_factor=1.4), run_time=1.2)
        self.beat('problem', READ_LONG)

        self.say('Next, check whether anything cancels. Nothing does here.')
        self.beat('cancel', READ_LONG)

        # ---- 2. x-intercepts: each factor of the top -----------------------------------------
        self.say('For the x-intercepts, set each factor of the top equal to zero and solve. '
                 'Start with 2x − 3.')
        self.play(Indicate(factor_a, color=ASYMPTOTE_COLOR, scale_factor=1.3),
                  copy_into(VGroup(f_top[1], f_top[2]), VGroup(cond[0], cond[1])),
                  FadeIn(VGroup(cond[2], cond[3])), run_time=1.3)
        self.beat('xint_a_set', READ_SHORT)

        op_left = operation('+', '3').next_to(cond[1], DOWN, buff=0.3)
        op_right = operation('+', '3').next_to(cond[3], DOWN, buff=0.3)
        strikes = strike_pair(cond[1], op_left)
        self.play(FadeIn(op_left, shift=DOWN * 0.15), FadeIn(op_right, shift=DOWN * 0.15),
                  run_time=0.6)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.5)
        self.play(FadeOut(VGroup(cond[1], cond[2], cond[3], op_left, strikes)),
                  copy_into(cond[0], s1[0]), FadeIn(s1[1]), copy_into(op_right, s1[2]),
                  run_time=0.9)
        self.play(FadeOut(VGroup(cond[0], op_right)),
                  s1.animate.move_to([0, WORK_Y, 0]), run_time=0.5)
        self.beat('xint_a_s1', READ_SHORT)

        self.say('Divide both sides by 2.')
        bars, divisors = divide_bars([s1[0], s1[2]], '2')
        self.play(*[Create(b) for b in bars],
                  *[FadeIn(d, shift=DOWN * 0.15) for d in divisors], run_time=0.9)
        self.beat('xint_a_bars', READ_SHORT)
        self.play(copy_into(VGroup(s1[0], divisors[0]), done[0]), FadeIn(done[1]),
                  copy_into(VGroup(s1[2], divisors[1]), done[2]), run_time=1.1)
        self.beat('xint_a_solved', READ_SHORT)

        self.say('The first x-intercept is (3/2, 0).')
        self.play(FadeIn(VGroup(*[xint_a[i] for i in (0, 1, 2, 4, 5, 6)])),
                  copy_into(done[2], xint_a[3]), run_time=1.3)
        self.play(FadeOut(VGroup(s1, bars, divisors, done)), run_time=0.5)
        self.beat('xint_a', READ_LONG)

        self.say('Now the other factor, x + 1.')
        iso = self.solve_for_x(VGroup(f_top[5], f_top[6]), '+', '1', 'xint_b',
                               on_copy=(Indicate(factor_b, color=ASYMPTOTE_COLOR,
                                                 scale_factor=1.3),))
        self.say('The second x-intercept is (−1, 0).')
        self.play(FadeIn(VGroup(*[xint_b[i] for i in (0, 1, 2, 4, 5, 6)])),
                  copy_into(iso[2], xint_b[3]), run_time=1.3)
        self.play(FadeOut(iso), run_time=0.5)
        self.beat('xint_b', READ_LONG)

        # ---- 3. y-intercept ------------------------------------------------------------------
        self.say('For the y-intercept, plug in zero for x.')
        self.play(Indicate(f_top[1], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  Indicate(f_top[5], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(plug), run_time=1.3)
        self.beat('yint_plug', READ_LONG)

        self.say('Simplify the top and the bottom.')
        self.play(ReplacementTransform(plug, simple), run_time=1.3)
        self.beat('yint_simplify', READ_SHORT)

        self.say('A negative divided by a negative is positive, so f(0) = 3.')
        self.play(ReplacementTransform(simple, answer), run_time=1.3)
        self.beat('yint_answer', READ_SHORT)

        self.say('The y-intercept is (0, 3).')
        self.play(FadeIn(VGroup(*[yint_item[i] for i in (0, 1, 2, 3, 4, 6)])),
                  copy_into(answer[2], yint_item[5]), run_time=1.3)
        self.play(FadeOut(answer), run_time=0.5)
        self.beat('yint', READ_LONG)

        # ---- 4. vertical asymptote -----------------------------------------------------------
        self.say('For the vertical asymptote, set the bottom equal to zero and solve.')
        iso = self.solve_for_x(f_bottom, '-', '1', 'va')
        self.say('The vertical asymptote is x = 1.')
        self.play(FadeIn(VGroup(va_item[0], va_item[1], va_item[2])),
                  copy_into(iso[2], va_item[3]), run_time=1.3)
        self.play(FadeOut(iso), run_time=0.5)
        self.beat('va', READ_LONG)

        # ---- 5. horizontal asymptote, then the slant ------------------------------------------
        self.say('For the horizontal asymptote, compare the degrees of the top and the bottom.')
        self.play(Indicate(f_top, color=ASYMPTOTE_COLOR, scale_factor=1.15),
                  Indicate(f_bottom, color=ASYMPTOTE_COLOR, scale_factor=1.4),
                  FadeIn(degree_top), FadeIn(degree_bottom), run_time=1.5)
        self.beat('ha_degrees', READ_LONG)

        self.say('The top has the bigger degree, so there is no horizontal asymptote.')
        self.play(FadeIn(ha_item), run_time=1.0)
        self.beat('ha', READ_LONG)

        self.say('But the top is exactly one degree bigger, so there is a slant asymptote. '
                 'Bring back the top from before it was factored.')
        self.play(FadeOut(VGroup(degree_top, degree_bottom)), FadeIn(multiplied), run_time=1.3)
        self.beat('slant_multiply', READ_LONG)

        self.say('Use synthetic division by x − 1. Put 1 in a half box, with 2, −1, −3 '
                 'beside it.')
        self.play(FadeIn(corner), FadeIn(root), FadeIn(coeffs), run_time=1.5)
        self.beat('slant_setup', READ_LONG)

        self.say('Draw a line underneath, put a plus, and bring the first number down '
                 'with an arrow.')
        self.play(Create(rule), FadeIn(plus), run_time=0.9)
        self.play(Create(arrow), run_time=0.7)
        self.play(copy_into(coeffs[0], down), run_time=1.0)
        self.beat('slant_down', READ_SHORT)

        self.say('Multiply 2 by 1 and write it under −1. Then add: −1 + 2 = 1.')
        self.play(copy_into(down, product_1), run_time=1.0)
        self.play(FadeIn(sum_1), run_time=0.9)
        self.beat('slant_step_1', READ_LONG)

        self.say('Multiply 1 by 1 and write it under −3. Then add: −3 + 1 = −2.')
        self.play(copy_into(sum_1, product_2), run_time=1.0)
        self.play(FadeIn(sum_2), run_time=0.9)
        self.beat('slant_step_2', READ_LONG)

        self.say('The last number is the remainder, so box it. It does not matter for the slant. '
                 'The rest, 2 and 1, make the quotient 2x + 1.')
        self.play(Create(remainder_box), FadeIn(remainder_label), run_time=1.0)
        self.play(Indicate(down, color=PAPER_GOLD, scale_factor=1.5),
                  Indicate(sum_1, color=PAPER_GOLD, scale_factor=1.5), run_time=1.3)
        self.play(FadeIn(slant_row), run_time=1.0)
        self.beat('slant_quotient', READ_LONG)

        self.say('The slant asymptote is y = 2x + 1.')
        self.play(FadeIn(VGroup(slant_item[0], slant_item[1], slant_item[2])),
                  copy_into(VGroup(slant_row[2], slant_row[3]),
                            VGroup(slant_item[3], slant_item[4])), run_time=1.3)
        self.play(FadeOut(VGroup(division, multiplied, slant_row)), run_time=0.5)
        self.beat('slant', READ_LONG)

        # ---- 6. holes ------------------------------------------------------------------------
        self.say('Holes come from factors that cancel. Nothing canceled, so there are no holes.')
        self.play(FadeIn(holes_item), run_time=1.0)
        self.beat('holes', READ_LONG)

        # ---- 7. the graph --------------------------------------------------------------------
        self.say('Now graph it. Draw the vertical asymptote and the slant asymptote '
                 'as dashed lines.')
        self.play(FadeIn(plane), run_time=1.0)
        self.play(Create(va_line), Create(slant_line), FadeIn(VGroup(va_label, slant_label)),
                  run_time=1.5)
        self.beat('asymptotes', READ_LONG)

        self.say('Plot the intercepts.')
        self.play(FadeIn(VGroup(xint_dots, yint_dot), scale=1.6), run_time=1.0)
        self.beat('points', READ_SHORT)

        self.say('To sketch the curve, look for points it has to cross. '
                 'The left side of x = 1 has two of them, so start there.')
        self.play(Indicate(xint_dots[0], color=PAPER_GOLD, scale_factor=2.0),
                  Indicate(yint_dot, color=PAPER_GOLD, scale_factor=2.0), run_time=1.3)
        self.beat('cross', READ_LONG)

        self.say('Sketch through both points. The curve heads up toward the vertical '
                 'asymptote and follows the slant on the far left.')
        self.play(Create(left_curve), run_time=2.5)
        self.beat('left_curve', READ_LONG)

        self.say('This side is going up, so on the opposite side of the asymptote '
                 'the curve goes down.')
        self.play(Indicate(left_curve, color=PAPER_GOLD, scale_factor=1.06), run_time=1.3)
        self.beat('opposite', READ_LONG)

        self.say('Sketch the other curve, coming up from the bottom through the '
                 'x-intercept (3/2, 0) and following the slant.')
        self.play(Create(right_curve), run_time=2.5)
        self.beat('hold', READ_LONG)
        self.write_marks('rational_function_slant_marks.json')
