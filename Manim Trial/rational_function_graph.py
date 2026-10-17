"""Graphing a rational function from its parts: f(x) = (x + 2) / (x - 3).

Chase's order, every time:
    everything factored, check whether anything cancels
    -> x-intercept: top = 0
    -> y-intercept: plug in 0
    -> vertical asymptote: bottom = 0
    -> horizontal asymptote: compare the degrees (equal -> divide the leading coefficients)
    -> holes: only where something cancelled
    -> graph: dashed asymptotes, the points, pick a side of the vertical asymptote and decide
       which way it goes (the other side goes the opposite way), then the curves ride the
       horizontal asymptote.
Not built yet (they come with their own examples): a slant asymptote, a hole, a squared factor.

Verified (check() re-derives it with Fraction):
    x-intercept (-2, 0); y-intercept (0, -2/3); vertical asymptote x = 3; equal degrees so
    horizontal asymptote y = 1/1 = 1; nothing cancels so no holes.
    Left of x = 3 the curve passes the intercepts and falls to -inf (f(2) = -4); right of it the
    curve comes down from +inf (f(14/3) = 4) toward y = 1.

PORTRAIT 4:5 frame (portrait_frame.py). The function stays on top, the answers collect in a
two-column list under it, and the work area below is cleared for the graph once every answer is
in. Exemplars: rational_domain_range.py (fraction rows, solving), parabola_walkthrough.py (list +
graph). Every MathTex is built through mathtex() with INK.
"""

from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from fractions import Fraction  # noqa: E402

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    NumberPlane,
    ReplacementTransform,
    Scene,
    VGroup,
    Write,
)

from math_notation import NEG, hanging_fraction  # noqa: E402
from rational_domain_range import READ_LONG, READ_SHORT, fraction, operation, tex  # noqa: E402
from scene_style import (  # noqa: E402
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    PAPER_MUTED,
    PAPER_RED,
    Narrated,
    apply_portal_paper_background,
)
from solve_steps import strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

apply_portal_paper_background()

INK = PAPER_INK
CURVE_COLOR = PAPER_RED
ASYMPTOTE_COLOR = PAPER_BLUE
FUNC_SIZE = 44
WORK_SIZE = 46
LIST_SIZE = 28

# Row centres. The caption owns y > 2.95; the graph takes the work area (y < -0.15).
FUNC_Y = 2.3
LIST_Y = (1.2, 0.7, 0.2)
LEFT_X, RIGHT_X = -2.9, 0.15
WORK_Y = -0.8          # the equation being solved
RESULT_Y = -2.2        # where the answer is built, before it slides up to WORK_Y
YINT_Y = -1.3          # the y-intercept rows are taller (fractions)
DEGREE_Y = (-0.8, -1.5)
COEFF_Y = -2.6

GRAPH_X, GRAPH_Y = (-12, 12), (-8, 8)   # zoomed out so the curves visibly settle on y = 1
GRAPH_SCALE = 0.23
GRAPH_CENTER_Y = -1.88

TOP = ('x', '+2')       # x + 2
BOTTOM = ('x', '-3')    # x - 3


def f(x):
    return (x + 2) / (x - 3)


def check():
    """Re-derive every number the clip says."""
    assert f(Fraction(-2)) == 0
    assert f(Fraction(0)) == Fraction(-2, 3)
    assert f(Fraction(2)) == -4 and f(Fraction(14, 3)) == 4
    assert 1 == 1 and 1 == 1          # leading coefficients 1 and 1, equal degrees: y = 1
    assert f(Fraction(10 ** 6)) - 1 < Fraction(1, 1000)


check()


def frac_row(size, lhs, top, bottom, eq):
    """lhs, then top over bottom with the bar on the equals sign's axis."""
    left = tex(*lhs, size=size)
    frac = fraction(top, top, bottom)
    row = VGroup(left, frac).arrange(RIGHT, buff=0.18)
    frac.shift(UP * (left[eq].get_center()[1] - frac[1].get_center()[1]))
    return row


def list_row(*parts, x, y):
    """One answer-list row, left-aligned at x."""
    row = tex(*parts, size=LIST_SIZE)
    return row.move_to([x + row.width / 2, y, 0])


class RationalFunctionGraph(Narrated, Scene):
    caption_color = PAPER_INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9

    def beat(self, mark, seconds):
        self.wait(seconds)
        self.mark(mark)

    # The window the graph shows; subclasses zoom by overriding these (units are frame units
    # per graph unit, per axis, so a sketch can stretch y to separate points from an asymptote).
    graph_x, graph_y = GRAPH_X, GRAPH_Y
    x_unit = y_unit = GRAPH_SCALE
    graph_step = 2
    graph_center_y = GRAPH_CENTER_Y

    def build_graph(self):
        plane = NumberPlane(
            x_range=[*self.graph_x, self.graph_step], y_range=[*self.graph_y, self.graph_step],
            x_length=self.x_unit * (self.graph_x[1] - self.graph_x[0]),
            y_length=self.y_unit * (self.graph_y[1] - self.graph_y[0]),
            axis_config={'color': PAPER_MUTED, 'stroke_width': 2},
            background_line_style={'stroke_color': '#CBD5E1', 'stroke_width': 1,
                                   'stroke_opacity': 1},
            faded_line_ratio=0,
        )
        return plane.move_to([0, self.graph_center_y, 0])

    def solve_for_x(self, source, bottom_sign, value, ex, on_copy=()):
        """x +/- value = 0 -> x = answer, the house style (rational_domain_range.teach_example).

        `source` is the function's numerator or denominator; `on_copy` animations play with the copy. Returns the cleaned-up
        `x = answer` row, left sitting at WORK_Y.
        """
        undo = '-' if bottom_sign == '+' else '+'
        answer = '-' + value if bottom_sign == '+' else value
        cond = tex('x', bottom_sign + value, '=', '0', size=WORK_SIZE).move_to([0, WORK_Y, 0])
        moved, zero = cond[1], cond[3]
        self.play(Indicate(source, color=ASYMPTOTE_COLOR, scale_factor=1.3),
                  copy_into(source, VGroup(cond[0], cond[1])),
                  FadeIn(VGroup(cond[2], cond[3])), *on_copy, run_time=1.3)
        self.beat(f'{ex}_set', READ_SHORT)

        op_left = operation(undo, value).next_to(moved, DOWN, buff=0.3)
        op_right = operation(undo, value).next_to(zero, DOWN, buff=0.3)
        strikes = strike_pair(moved, op_left)
        iso = tex('x', '=', answer, size=WORK_SIZE).move_to([0, RESULT_Y, 0])
        self.play(FadeIn(op_left, shift=DOWN * 0.15), FadeIn(op_right, shift=DOWN * 0.15),
                  run_time=0.6)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.5)
        self.play(FadeOut(VGroup(cond, op_left, op_right, strikes)),
                  copy_into(cond[0], iso[0]), FadeIn(iso[1]), copy_into(op_right, iso[2]),
                  run_time=0.9)
        self.play(iso.animate.move_to([0, WORK_Y, 0]), run_time=0.35)
        self.beat(f'{ex}_solved', 0.5)
        return iso

    def construct(self):
        s = FUNC_SIZE
        top = tex(*TOP, size=s)
        function = frac_row(s, ('f(x)', '='), top, tex(*BOTTOM, size=s), 1)
        function.move_to([0, FUNC_Y, 0])
        f_top, f_bottom = function[1][0], function[1][2]

        # ---- the answer list ----------------------------------------------------------------
        xint_item = list_row('x', r'\text{-int: }', '(', '-2', ',', '0', ')',
                             x=LEFT_X, y=LIST_Y[0])
        yint_item = list_row('y', r'\text{-int: }', '(', '0', ',', hanging_fraction('2', '3'), ')',
                             x=LEFT_X, y=LIST_Y[1])
        holes_item = list_row(r'\text{Holes: }', r'\text{none}', x=LEFT_X, y=LIST_Y[2])
        va_item = list_row(r'\text{V.A.: }', 'x', '=', '3', x=RIGHT_X, y=LIST_Y[0])
        ha_item = list_row(r'\text{H.A.: }', 'y', '=', '1', x=RIGHT_X, y=LIST_Y[1])

        # ---- the y-intercept rows (one tex each, so the morphs are glyph to glyph) ----------
        def y_row(frac_tex, size=WORK_SIZE):
            return tex('f(0)', '=', frac_tex, size=size).move_to([0, YINT_Y, 0])

        plug = y_row(r'\frac{0+2}{0-3}')
        simple = y_row(r'\frac{2}{' + NEG + '3}')
        negative_up = y_row(hanging_fraction('2', '3'))

        # ---- the horizontal asymptote rows --------------------------------------------------
        degree_top = tex(r'\text{degree of top: }', '1', size=36).move_to([0, DEGREE_Y[0], 0])
        degree_bottom = tex(r'\text{degree of bottom: }', '1', size=36
                            ).move_to([0, DEGREE_Y[1], 0])
        coefficients = tex('y', '=', r'\frac{1}{1}', size=WORK_SIZE).move_to([0, COEFF_Y, 0])
        coefficients_done = tex('y', '=', '1', size=WORK_SIZE).move_to([0, COEFF_Y, 0])

        # ---- the graph -----------------------------------------------------------------------
        plane = self.build_graph()
        c2p = plane.c2p

        def dot(x, y):
            return Dot(c2p(x, y), color=CURVE_COLOR, radius=0.07)

        va_line = DashedLine(c2p(3, GRAPH_Y[0]), c2p(3, GRAPH_Y[1]), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        ha_line = DashedLine(c2p(GRAPH_X[0], 1), c2p(GRAPH_X[1], 1), color=ASYMPTOTE_COLOR,
                             stroke_width=4, dash_length=0.12)
        va_label = tex('x', '=', '3', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(3, -6.5), RIGHT, buff=0.1)
        ha_label = tex('y', '=', '1', size=26).set_color(ASYMPTOTE_COLOR
                                                         ).next_to(c2p(-10, 1), UP, buff=0.08)
        points = VGroup(dot(-2, 0), dot(0, Fraction(-2, 3)))
        # Each branch runs to the edge of the window: f = -8 at x = 22/9, f = 8 at x = 26/7.
        left_curve = plane.plot(f, x_range=[GRAPH_X[0], 22 / 9, 0.02], color=CURVE_COLOR,
                                stroke_width=5)
        right_curve = plane.plot(f, x_range=[26 / 7, GRAPH_X[1], 0.02], color=CURVE_COLOR,
                                 stroke_width=5)

        # ---- 1. factored, nothing cancels ---------------------------------------------------
        self.say('Here is a rational function. Everything must be factored first.')
        self.play(Write(function), run_time=1.3)
        self.play(Indicate(f_top, color=ASYMPTOTE_COLOR, scale_factor=1.25),
                  Indicate(f_bottom, color=ASYMPTOTE_COLOR, scale_factor=1.25), run_time=1.2)
        self.beat('problem', READ_LONG)

        self.say('Next, check whether anything cancels. Nothing does here.')
        self.beat('cancel', READ_LONG)

        # ---- 2. x-intercept ------------------------------------------------------------------
        self.say('For the x-intercept, set the top equal to zero and solve.')
        iso = self.solve_for_x(f_top, '+', '2', 'xint')
        self.say('The x-intercept is (−2, 0).')
        self.play(FadeIn(VGroup(*[xint_item[i] for i in (0, 1, 2, 4, 5, 6)])),
                  copy_into(iso[2], xint_item[3]), run_time=1.3)
        self.play(FadeOut(iso), run_time=0.5)
        self.beat('xint', READ_LONG)

        # ---- 3. y-intercept ------------------------------------------------------------------
        self.say('For the y-intercept, plug in zero for x.')
        self.play(Indicate(f_top[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  Indicate(f_bottom[0], color=ASYMPTOTE_COLOR, scale_factor=1.6),
                  FadeIn(plug), run_time=1.3)
        self.beat('yint_plug', READ_LONG)

        self.say('Simplify the top and the bottom.')
        self.play(ReplacementTransform(plug, simple), run_time=1.3)
        self.beat('yint_simplify', READ_SHORT)

        self.say('Move the negative to the top number.')
        self.play(ReplacementTransform(simple, negative_up), run_time=1.3)
        self.beat('yint_negative', READ_SHORT)

        self.say('The y-intercept is (0, −2/3).')
        self.play(FadeIn(VGroup(*[yint_item[i] for i in (0, 1, 2, 3, 4, 6)])),
                  copy_into(negative_up[2], yint_item[5]), run_time=1.3)
        self.play(FadeOut(negative_up), run_time=0.5)
        self.beat('yint', READ_LONG)

        # ---- 4. vertical asymptote -----------------------------------------------------------
        self.say('For the vertical asymptote, set the bottom equal to zero and solve.')
        iso = self.solve_for_x(f_bottom, '-', '3', 'va')
        self.say('The vertical asymptote is x = 3.')
        self.play(FadeIn(VGroup(va_item[0], va_item[1], va_item[2])),
                  copy_into(iso[2], va_item[3]), run_time=1.3)
        self.play(FadeOut(iso), run_time=0.5)
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

        self.say('Both leading coefficients are 1, so the horizontal asymptote is y = 1.')
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
                 'asymptote and levels out along y = 1 on the far left.')
        self.play(Create(left_curve), run_time=2.5)
        self.beat('left_curve', READ_LONG)

        self.say('This side is going down, so on the opposite side of the asymptote '
                 'the curve goes up.')
        self.play(Indicate(left_curve, color=PAPER_GOLD, scale_factor=1.06), run_time=1.3)
        self.beat('opposite', READ_LONG)

        self.say('So the other curve is up here. Sketch it, coming down from the top '
                 'and leveling out along y = 1.')
        self.play(Create(right_curve), run_time=2.5)
        self.beat('hold', READ_LONG)
        self.write_marks('rational_function_graph_marks.json')
