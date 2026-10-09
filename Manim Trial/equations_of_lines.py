"""Equations of Lines (M1314, 2.5): write a line's equation from its slope and a point.

Chase's order, every clip in this module runs the same beats:
    point-slope form, plug in everything -> clear the fraction by multiplying both sides by the
    denominator -> distribute -> switch to the form the problem asks for.
    Slope-intercept form is whatever y = mx + b comes out to; standard form has no fractions
    and a positive x term (add the x term and the constant across instead of dividing).

Each scene is one Problem. Verified (Fraction arithmetic in Problem.__post_init__ re-checks it):
    SlopePointSlopeIntercept: m = 5/7, (3, 4)
        y - 4 = 5/7 (x - 3)  ->  7(y - 4) = 5(x - 3)  ->  7y - 28 = 5x - 15
        ->  7y = 5x + 13  ->  y = 5/7 x + 13/7        check (3, 4): 15/7 + 13/7 = 4
    TwoPointsStandard: (11, 2) and (2, 8), standard form -- the slope formula first
        m = (8 - 2)/(2 - 11) = 6/-9 = -2/3, then the same beats with (2, 8):
        y - 8 = -2/3 (x - 2)  ->  3(y - 8) = -2(x - 2)  ->  3y - 24 = -2x + 4
        ->  2x + 3y = 28 (add 2x and 24 to both sides)   check (11, 2): 22 + 6 = 28

    ParallelSlopeIntercept: parallel to 8x + 6y = 15 through (3, -4) -- the given line first
        6y = -8x + 15  ->  y = -8/6 x + 15/6 = -4/3 x + 5/2, so m = -4/3 (parallel: same slope)
        then the same beats with (3, -4):
        y + 4 = -4/3 (x - 3)  ->  3(y + 4) = -4(x - 3)  ->  3y + 12 = -4x + 12
        ->  3y = -4x (subtract 12 from both sides)  ->  y = -4/3 x    check (3, -4): -4

PORTRAIT: drawn for the phone player in the 4:5 frame (portrait_frame.py), 6.4 x 8 units.
Every row is built once at its final spot and only fades in, except the cleared row, which
slides to the top once so the rest of the work can stack under it (the slope-intercept clips do
the same). Every MathTex is given INK explicitly: its default is white, invisible on paper.
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from dataclasses import dataclass  # noqa: E402
from fractions import Fraction  # noqa: E402
from math import gcd  # noqa: E402

from manim import (  # noqa: E402
    DOWN,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    ReplacementTransform,
    Scene,
    SurroundingRectangle,
    VGroup,
    Write,
    smooth,
)

from math_notation import NEG, hanging_fraction, mathtex, unsigned  # noqa: E402
from scene_style import (  # noqa: E402
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    Narrated,
    apply_portal_paper_background,
)
from solve_steps import divide_bars, op_under, strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

apply_portal_paper_background()

INK = PAPER_INK
M_COLOR = PAPER_BLUE   # the slope
PT_COLOR = PAPER_GOLD  # the point's numbers
FORM_SIZE = 44
MATH_SIZE = 52
MAX_WIDTH = 5.8
# Row centres, top to bottom; the caption owns y > 2.95.
GIVEN_Y, GENERAL_Y, PLUG_Y, CLEAR_Y = 2.3, 1.3, 0.1, -1.9
TOP_Y = 1.9      # the cleared row's final spot
LINE_Y = (2.1, 0.75, -0.95, -2.35)   # the given line, rewritten row by row
DIST_Y = 0.85
ROW2_Y = -0.7
ANSWER_Y = -2.75
STANDARD_ANSWER_Y = -1.5  # nothing sits below the ops row, so the answer rides closer

READ_SHORT = 1.0
READ_LONG = 1.5


@dataclass
class Problem:
    """Everything that differs between clips: a slope m = num/den and a point (x1, y1).

    `first` is a second point on the line: when given, the clip finds the slope from the two
    points first (so num/den must match them). `line` = (A, B, C) is a given line Ax + By = C the
    new line is `relation` ('parallel') to: the clip finds that line's slope first. `ending` is
    the form asked for. x1 is a positive whole number (y1 is negative only for slope-intercept),
    the slope is in lowest terms and the result divides cleanly -- the beats show those numbers,
    they do not simplify anything beyond the slope itself.
    """
    num: int
    den: int
    x1: int
    y1: int
    marks_file: str
    first: tuple = None
    line: tuple = None
    relation: str = None
    ending: str = 'slope-intercept'

    def __post_init__(self):
        if min(self.den, self.x1) < 1 or self.y1 == 0 or self.num == 0:
            raise ValueError('Only a positive x, a nonzero y and a nonzero slope are built so far.')
        if self.y1 < 0 and self.ending != 'slope-intercept':
            raise ValueError('A negative y is built for slope-intercept only.')
        if gcd(abs(self.num), self.den) != 1:
            raise ValueError('The slope must be in lowest terms.')
        slope = Fraction(self.num, self.den)
        self.c = self.den * self.y1 - self.num * self.x1  # den*y = num*x + c
        if self.first:
            fx, fy = self.first
            self.dy, self.dx = self.y1 - fy, self.x1 - fx
            if not self.dy > 0 > self.dx:
                raise ValueError('The slope-formula beats are built for a falling line only.')
            if Fraction(self.dy, self.dx) != slope:
                raise ValueError('The slope does not match the two points.')
            if slope * fx + Fraction(self.c, self.den) != fy:
                raise ValueError('The result does not pass through the first point.')
        if self.line:
            a, b, c = self.line
            if self.relation != 'parallel' or a < 1 or b < 1:
                raise ValueError('Only a parallel line Ax + By = C with A, B > 0 is built.')
            if Fraction(-a, b) != slope:
                raise ValueError("The slope is not the given line's slope.")
        if self.ending == 'standard':
            # den*y - den*y1 = num*x - num*x1  ->  (-num)x + den*y = c, x term positive
            self.a, self.b = -self.num, self.den
            if self.a < 1 or gcd(gcd(self.a, self.b), self.c) != 1:
                raise ValueError('Standard form here needs a negative slope and no common factor.')
        else:
            if self.c and gcd(abs(self.c), self.den) != 1:
                raise ValueError('b = c/den must be a fraction that does not reduce.')
            if slope * self.x1 + Fraction(self.c, self.den) != self.y1:
                raise ValueError('The result does not pass through the point.')


SLOPE_POINT = Problem(num=5, den=7, x1=3, y1=4, marks_file='equations_of_lines_marks.json')
TWO_POINTS = Problem(num=-2, den=3, x1=2, y1=8, first=(11, 2), ending='standard',
                     marks_file='equations_of_lines_two_points_marks.json')
PARALLEL = Problem(num=-4, den=3, x1=3, y1=-4, line=(8, 6, 15), relation='parallel',
                   marks_file='equations_of_lines_parallel_marks.json')


def tex(*parts, size=MATH_SIZE, color=INK):
    return mathtex(*parts, font_size=size, color=color)


def var(letter, color):
    """A variable inside a caption: italic and coloured, so it is not read as the word 'y'."""
    return f'<span foreground="{color}"><i>{letter}</i></span>'


def fraction(top, bottom, size=MATH_SIZE, color=INK):
    """top over bottom as separate pieces (top, bar, bottom), so the bottom can be struck.

    A negative top hangs left of the bar (Chase's negative on the top number): the bar spans
    the digits only.
    """
    t, b = tex(top, size=size, color=color), tex(bottom, size=size, color=color)
    body = unsigned(t[0]) if top.startswith('-') else t
    width = max(body.width, b.width) + 0.14
    bar = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=color, stroke_width=4)
    group = VGroup(t, bar, b).arrange(DOWN, buff=0.1)
    t.shift(RIGHT * (bar.get_center()[0] - body.get_center()[0]))
    return group


def slope_tex(p):
    """The slope as one MathTex part, negative hanging left of the bar."""
    if p.num < 0:
        return hanging_fraction(str(abs(p.num)), str(p.den))
    return rf'\frac{{{p.num}}}{{{p.den}}}'


def signed(n):
    """A whole number as a MathTex part: a negative gets Chase's short dash."""
    return f'{NEG}{abs(n)}' if n < 0 else str(n)


class EquationsOfLines(Narrated, Scene):
    caption_color = PAPER_INK  # PAPER_MUTED read washed out on the white frame
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9
    problem = SLOPE_POINT

    def beat(self, mark, seconds, allow=()):
        """Hold the caption long enough to read, then record the pause point."""
        self.wait(seconds)
        self.mark(mark, allow=allow)

    def find_slope(self, p):
        """Two points -> the slope formula -> m. Returns (second point row, m row, the rest)."""
        fx, fy = p.first
        pts = []
        for n, (x, y), row_y in ((1, p.first, 2.5), (2, (p.x1, p.y1), 1.85)):
            pt = tex('(', f'x_{n}', r',\ ', f'y_{n}', ')', '=', '(', str(x), r',\ ', str(y), ')',
                     size=FORM_SIZE).move_to([0, row_y, 0])
            pt[7].set_color(PT_COLOR)
            pt[9].set_color(PT_COLOR)
            pts.append(pt)
        formula = tex('m', '=', r'\frac{y_2-y_1}{x_2-x_1}',
                      size=FORM_SIZE).move_to([0, 0.75, 0])
        plug = tex('m', '=', rf'\frac{{{p.y1}-{fy}}}{{{p.x1}-{fx}}}',
                   size=FORM_SIZE).move_to([0, -0.5, 0])
        step = tex('m', '=', rf'\frac{{{p.dy}}}{{{NEG}{abs(p.dx)}}}',
                   size=FORM_SIZE).move_to([0, -1.65, 0])
        result = tex('m', '=', slope_tex(p), size=FORM_SIZE).move_to([0, -2.8, 0])
        result[2].set_color(M_COLOR)
        g = gcd(p.dy, abs(p.dx))

        self.say('There are two points, so find the slope first.')
        self.play(FadeIn(pts[0]), FadeIn(pts[1]), run_time=1.0)
        self.beat('points', READ_SHORT)

        self.say('Use the slope formula.')
        self.play(Write(formula), run_time=1.3)
        self.beat('slope-formula', READ_SHORT)

        self.say('The y values go on top and the x values go on the bottom.')
        self.play(Indicate(pts[0][9], color=PT_COLOR, scale_factor=1.5),
                  Indicate(pts[1][9], color=PT_COLOR, scale_factor=1.5), run_time=1.1)
        self.play(copy_into(formula, plug), run_time=1.3)
        self.beat('slope-plug', READ_LONG)

        self.say('Subtract on the top and on the bottom.')
        self.play(copy_into(plug, step), run_time=1.2)
        self.beat('slope-subtract', READ_LONG)

        self.say(f'Divide the top and the bottom by {g}.')
        self.play(copy_into(step, result), run_time=1.2)
        self.beat('slope', READ_LONG)
        return pts[1], result, VGroup(pts[0], formula, plug, step)

    def find_line_slope(self, p, given):
        """A line is given: put it in slope-intercept form, read its slope, carry it to `given`.

        Returns the point pieces of `given` still to fade in.
        """
        a, b, c = p.line
        slope = Fraction(-a, b)
        # -a/b and c/b, then both reduced.
        raw = hanging_fraction(str(a), str(b))
        const = Fraction(c, b)

        r1 = tex(f'{a}x', '+', f'{b}y', '=', str(c)).move_to([0, LINE_Y[0], 0])
        slope_intercept = tex('y', '=', 'm', 'x', '+', 'b', size=FORM_SIZE).move_to([0, LINE_Y[1], 0])
        slope_intercept[2].set_color(M_COLOR)
        r2 = tex(f'{b}y', '=', f'{-a}x', '+', str(c)).move_to([0, LINE_Y[1], 0])
        take = op_under('-', f'{a}x', r1[0])
        take_right = op_under('-', f'{a}x', r1[4])
        level = min(take.get_center()[1], take_right.get_center()[1]) - 0.1  # clear the 6y descender
        for op in (take, take_right):
            op.move_to([op.get_center()[0], level, 0])
        cancel_a = strike_pair(r1[0], take)
        bars, divisors = divide_bars([r2[0], r2[2], r2[4]], str(b))
        r3 = tex('y', '=', raw, 'x', '+', rf'\frac{{{c}}}{{{b}}}').move_to([0, LINE_Y[2], 0])
        r4 = tex('y', '=', hanging_fraction(str(abs(slope.numerator)), str(slope.denominator)),
                 'x', '+', rf'\frac{{{const.numerator}}}{{{const.denominator}}}'
                 ).move_to([0, LINE_Y[3], 0])
        r4[2].set_color(M_COLOR)
        g = gcd(a, b)

        self.say("To write a parallel line, we need the given line's slope.")
        self.play(FadeIn(r1), run_time=1.2)
        self.beat('need-slope', READ_LONG)

        self.say('Parallel lines have the same slope.')
        self.beat('same-slope', READ_SHORT)

        self.say('In order to find the slope, we need to rewrite it in slope-intercept form.')
        self.play(Write(slope_intercept), run_time=1.2)
        self.beat('slope-intercept-form', READ_LONG)

        self.say(f'Subtract {a}x from both sides.')
        self.play(FadeOut(slope_intercept), run_time=0.6)
        self.play(FadeIn(take, shift=DOWN * .15), FadeIn(take_right, shift=DOWN * .15),
                  run_time=1.0)
        self.beat('subtract-x', READ_SHORT)

        self.play(Create(cancel_a[0]), run_time=.6)
        self.play(Create(cancel_a[1]), run_time=.6)
        self.play(copy_into(r1[2], r2[0]), copy_into(r1[3], r2[1]),
                  copy_into(take_right, r2[2]), copy_into(r1[4], r2[4]),
                  FadeIn(r2[3]), run_time=1.5)
        self.beat('line-isolated', READ_LONG)

        self.say(f'Divide every term by {b}.')
        for bar, divisor in zip(bars, divisors):
            self.play(Create(bar), FadeIn(divisor, shift=DOWN * .15), run_time=.8)
        self.beat('line-divide', READ_LONG)

        self.say(f'Now {var("y", PAPER_BLUE)} is alone.')
        self.play(copy_into(VGroup(r2[0], divisors[0]), r3[0]), copy_into(r2[1], r3[1]),
                  copy_into(VGroup(r2[2], divisors[1]), VGroup(r3[2], r3[3])),
                  copy_into(r2[3], r3[4]),
                  copy_into(VGroup(r2[4], divisors[2]), r3[5]), run_time=1.6)
        self.beat('line-alone', READ_LONG)

        self.say(f'Reduce each fraction by dividing by {g}.')
        self.play(copy_into(r3, r4), run_time=1.4)
        self.beat('line-reduced', READ_LONG)

        self.say(f'The number in front of {var("x", PAPER_BLUE)} is the slope.')
        self.play(Indicate(r4[2], color=M_COLOR, scale_factor=1.3), run_time=1.1)
        self.beat('line-slope', READ_SHORT)

        self.say(f'Parallel lines have the same slope, so this is {var("m", PAPER_BLUE)}.')
        self.play(FadeIn(VGroup(given[0], given[1])), copy_into(r4[2], given[2]),
                  FadeOut(VGroup(r1, r2, r3, r4, take, take_right, cancel_a, bars, divisors)),
                  run_time=1.5)
        self.beat('slope-given', READ_LONG)

    def construct(self):
        p = self.problem
        # ---- every row, built once at its final spot ------------------------------------
        y_sign = '+' if p.y1 < 0 else '-'   # y - (-4) is y + 4
        y_abs = abs(p.y1)
        given = tex('m', '=', slope_tex(p), r'\qquad(', str(p.x1), r',\ ',
                    signed(p.y1), ')', size=FORM_SIZE).move_to([0, GIVEN_Y, 0])
        given[2].set_color(M_COLOR)
        given[4].set_color(PT_COLOR)
        given[6].set_color(PT_COLOR)

        general = tex('y', '-', 'y_1', '=', 'm', '(', 'x', '-', 'x_1', ')',
                      size=FORM_SIZE).move_to([0, GENERAL_Y, 0])
        general[2].set_color(PT_COLOR)
        general[4].set_color(M_COLOR)
        general[8].set_color(PT_COLOR)

        left = tex('y', y_sign, str(y_abs), '=')
        left[2].set_color(PT_COLOR)
        slope = fraction(str(p.num), str(p.den), color=M_COLOR)
        right = tex('(', 'x', '-', str(p.x1), ')')
        right[3].set_color(PT_COLOR)
        plug = VGroup(left, slope, right).arrange(RIGHT, buff=0.14)
        slope.shift(UP * (left[3].get_center()[1] - slope[1].get_center()[1]))
        plug.move_to([0, PLUG_Y, 0])
        right_side = VGroup(slope, right)

        # The same row with a 7 inserted in front of each side: the left side's stays, the
        # right side's cancels the fraction's denominator.
        times_left = tex(str(p.den), '(', 'y', y_sign, str(y_abs), ')', '=')
        times_right = tex(str(p.den), r'\cdot')
        times_slope = fraction(str(p.num), str(p.den), color=M_COLOR)
        times_x = tex('(', 'x', '-', str(p.x1), ')')
        times = VGroup(times_left, times_right, times_slope, times_x).arrange(RIGHT, buff=0.24)
        times_slope.shift(UP * (times_left[6].get_center()[1] - times_slope[1].get_center()[1]))
        if times.width > MAX_WIDTH:
            times.scale(MAX_WIDTH / times.width)
        times.move_to([0, PLUG_Y, 0])
        for gold in (times_left[0], times_left[4], times_right[0], times_x[3]):
            gold.set_color(PT_COLOR)
        strikes = strike_pair(times_slope[2], times_right[0])  # the 7, not the dot

        clear = tex(str(p.den), '(', 'y', y_sign, str(y_abs), ')', '=', str(p.num), '(', 'x', '-',
                    str(p.x1), ')').move_to([0, CLEAR_Y, 0])
        clear[0].set_color(PT_COLOR)   # the multiplier arrives gold, like the op it came from
        clear[4].set_color(PT_COLOR)
        clear[7].set_color(M_COLOR)
        clear[11].set_color(PT_COLOR)

        dist_sign = '+' if p.num * p.x1 < 0 else '-'  # distributing a negative flips the sign
        dist = tex(f'{p.den}y', y_sign, str(p.den * y_abs), '=', f'{p.num}x', dist_sign,
                   str(abs(p.num * p.x1))).move_to([0, DIST_Y, 0])

        op_sign = '-' if p.y1 < 0 else '+'   # undoes the constant on the left
        shift_word = 'Subtract {n} from' if p.y1 < 0 else 'Add {n} to'
        add_left = op_under(op_sign, str(p.den * y_abs), dist[2])
        add_right = op_under(op_sign, str(p.den * y_abs), dist[6])
        if p.ending == 'standard':
            add_x_left = op_under('+', f'{p.a}x', dist[0])
            add_x_right = op_under('+', f'{p.a}x', dist[4])
            ops = (add_left, add_right, add_x_left, add_x_right)
        else:
            ops = (add_left, add_right)
        level = min(op.get_center()[1] for op in ops)
        for op in ops:
            op.move_to([op.get_center()[0], level, 0])
        cancel = strike_pair(dist[1:3], add_left)
        cancel_right = strike_pair(dist[5:7], add_right)   # used only when the constants cancel
        if p.ending == 'standard':
            cancel_x = strike_pair(dist[4], add_x_right)
            answer = tex(f'{p.a}x', '+', f'{p.b}y', '=', str(p.c),
                         size=MATH_SIZE + 8).move_to([0, STANDARD_ANSWER_Y, 0])
        else:
            sign = '+' if p.c > 0 else '-'
            slope_x = (hanging_fraction(str(abs(p.num)), str(p.den)) if p.num < 0
                       else rf'\frac{{{p.num}}}{{{p.den}}}') + 'x'
            if p.c:
                isolated = tex(f'{p.den}y', '=', f'{p.num}x', sign,
                               str(abs(p.c))).move_to([0, ROW2_Y, 0])
                bars, divisors = divide_bars([isolated[0], isolated[2], isolated[4]], str(p.den))
                answer = tex('y', '=', slope_x, sign, rf'\frac{{{abs(p.c)}}}{{{p.den}}}',
                             size=MATH_SIZE + 8).move_to([0, ANSWER_Y, 0])
            else:   # the constants cancel: nothing is left but the x term
                isolated = tex(f'{p.den}y', '=', f'{p.num}x').move_to([0, ROW2_Y, 0])
                bars, divisors = divide_bars([isolated[0], isolated[2]], str(p.den))
                answer = tex('y', '=', slope_x,
                             size=MATH_SIZE + 8).move_to([0, ANSWER_Y, 0])
        box = SurroundingRectangle(answer, color=INK, buff=0.2, stroke_width=4)  # all black

        y_word = var('y', PAPER_BLUE)

        # ---- 1. point-slope form, plug in -------------------------------------------------
        if p.first:
            pt2, result, rest = self.find_slope(p)
            self.say(f'Use either point. We will use ({p.x1}, {p.y1}).')
            self.play(Indicate(pt2, color=PT_COLOR, scale_factor=1.15), run_time=1.1)
            self.play(copy_into(result[0], given[0]), copy_into(result[1], given[1]),
                      copy_into(result[2], given[2]), copy_into(pt2[7], given[4]),
                      copy_into(pt2[9], given[6]),
                      FadeIn(VGroup(given[3], given[5], given[7])),
                      FadeOut(VGroup(rest, result, pt2)), run_time=1.5)
            self.beat('given', READ_SHORT)

            self.say('Now use point-slope form.')
            self.play(Write(general), run_time=1.3)
            self.beat('form', READ_SHORT)
        elif p.line:
            self.find_line_slope(p, given)
            self.say(
                f'So now we can find the equation of the line that passes through the point '
                f'({p.x1}, {p.y1}).',
            )
            self.play(FadeIn(VGroup(given[3], given[4], given[5], given[6], given[7])),
                      run_time=1.0)
            self.beat('given', READ_SHORT)

            self.say('Use point-slope form, like problem 1.')
            self.play(Write(general), run_time=1.3)
            self.beat('form', READ_SHORT)
        else:
            self.say('Start with point-slope form.')
            self.play(Write(general), run_time=1.3)
            self.beat('form', READ_SHORT)

            self.say('We are given the slope and a point.')
            self.play(FadeIn(given), run_time=1.0)
            self.beat('given', READ_SHORT)

        self.say('Plug the slope and the point into the formula.')
        self.play(Indicate(general[4], color=M_COLOR, scale_factor=1.4),
                  Indicate(given[2], color=M_COLOR, scale_factor=1.3), run_time=1.1)
        self.play(copy_into(given[2], slope),
                  *[FadeIn(piece) for piece in (left[0], left[1], left[3], right[0], right[1],
                                                right[2], right[4])], run_time=1.2)
        if p.y1 < 0:
            self.say('Subtracting a negative is the same as adding.')
        self.play(Indicate(general[2], color=PT_COLOR, scale_factor=1.5),
                  Indicate(general[8], color=PT_COLOR, scale_factor=1.5),
                  Indicate(given[4], color=PT_COLOR, scale_factor=1.4),
                  Indicate(given[6], color=PT_COLOR, scale_factor=1.4), run_time=1.1)
        self.play(copy_into(given[6], left[2]), copy_into(given[4], right[3]), run_time=1.2)
        self.beat('plug', READ_LONG)

        # ---- 2. clear the fraction --------------------------------------------------------
        self.say(f'Clear the fraction: multiply both sides by {p.den}.')
        self.play(*[ReplacementTransform(old, new) for old, new in (
            (left[0], times_left[2]), (left[1], times_left[3]), (left[2], times_left[4]),
            (left[3], times_left[6]), (slope, times_slope),
            *[(right[i], times_x[i]) for i in range(5)])],
            FadeIn(VGroup(times_left[0], times_left[1], times_left[5], times_right)),
            run_time=1.5)
        self.beat('multiply', READ_LONG)

        self.say(f'The {p.den}s cancel on the right side.')
        self.play(Create(strikes[0]), run_time=.6)
        self.play(Create(strikes[1]), run_time=.6)
        self.beat('cancel', READ_SHORT)

        self.play(*[copy_into(times_left[i], clear[i]) for i in range(7)],
                  copy_into(times_slope[0], clear[7]),
                  *[copy_into(times_x[i], clear[8 + i]) for i in range(5)], run_time=1.5)
        self.beat('cleared', READ_LONG)

        # Clear the board but the cleared row, and slide it up so the rest stacks beneath it.
        self.play(FadeOut(VGroup(given, general, times_left, times_right, times_slope, times_x,
                                 strikes)),
                  clear.animate.move_to([0, TOP_Y, 0]), run_time=1.2, rate_func=smooth)

        # ---- 3. distribute ----------------------------------------------------------------
        num_word = str(p.num) if p.num > 0 else f'negative {abs(p.num)}'
        self.say(f'Distribute the {p.den} and the {num_word}.')
        self.play(Indicate(clear[0], color=PT_COLOR, scale_factor=1.4),
                  Indicate(clear[7], color=M_COLOR, scale_factor=1.4), run_time=1.1)
        self.play(copy_into(VGroup(clear[0], clear[2]), dist[0]),
                  copy_into(clear[3], dist[1]),
                  copy_into(VGroup(clear[0], clear[4]), dist[2]),
                  copy_into(clear[6], dist[3]),
                  copy_into(VGroup(clear[7], clear[9]), dist[4]),
                  copy_into(clear[10], dist[5]),
                  copy_into(VGroup(clear[7], clear[11]), dist[6]), run_time=1.6)
        self.beat('distribute', READ_LONG)

        # ---- 4. the form the problem asks for -----------------------------------------------
        if p.ending == 'standard':
            self.say('Standard form: the x term comes first and is positive, with no fractions.')
            self.wait(READ_LONG)
            self.say(f'Add {p.a}x to both sides.')
            self.play(FadeIn(add_x_left, shift=DOWN * .15), FadeIn(add_x_right, shift=DOWN * .15),
                      run_time=1.0)
            self.beat('add-x', READ_SHORT)

            self.play(Create(cancel_x[0]), run_time=.6)
            self.play(Create(cancel_x[1]), run_time=.6)
            self.beat('cancel-x', READ_SHORT)

            self.say(f'Add {p.den * p.y1} to both sides.')
            self.play(FadeIn(add_left, shift=DOWN * .15), FadeIn(add_right, shift=DOWN * .15),
                      run_time=1.0)
            self.beat('add', READ_SHORT)

            self.play(Create(cancel[0]), run_time=.6)
            self.play(Create(cancel[1]), run_time=.6)
            self.say('Write the x term first.')
            self.play(copy_into(add_x_left[1], answer[0]), copy_into(add_x_left[0], answer[1]),
                      copy_into(dist[0], answer[2]), copy_into(dist[3], answer[3]),
                      copy_into(VGroup(dist[5], dist[6], add_right), answer[4]), run_time=1.6)
            self.play(Create(box), run_time=.8)
            self.beat('answer', READ_LONG)

            self.say('This is standard form.')
        else:
            self.say(f'Slope-intercept form means {y_word} by itself.')
            self.wait(READ_SHORT)
            self.say(shift_word.format(n=p.den * y_abs) + ' both sides.')
            self.play(FadeIn(add_left, shift=DOWN * .15), FadeIn(add_right, shift=DOWN * .15),
                      run_time=1.0)
            self.beat('add', READ_SHORT)

            self.play(Create(cancel[0]), run_time=.6)
            self.play(Create(cancel[1]), run_time=.6)
            if p.c:
                self.play(copy_into(dist[0], isolated[0]), copy_into(dist[3], isolated[1]),
                          copy_into(dist[4], isolated[2]),
                          copy_into(VGroup(dist[5], dist[6], add_right),
                                    VGroup(isolated[3], isolated[4])), run_time=1.5)
            else:
                self.say(f'The {p.den * y_abs}s on the right side cancel too.')
                self.play(Create(cancel_right[0]), run_time=.6)
                self.play(Create(cancel_right[1]), run_time=.6)
                self.play(copy_into(dist[0], isolated[0]), copy_into(dist[3], isolated[1]),
                          copy_into(dist[4], isolated[2]), run_time=1.5)
            self.beat('isolated', READ_LONG)

            self.say(f'Divide every term by {p.den}.')
            for bar, divisor in zip(bars, divisors):
                self.play(Create(bar), FadeIn(divisor, shift=DOWN * .15), run_time=.8)
            self.beat('divide', READ_LONG)

            self.say(f'Now {y_word} is alone.')
            self.play(copy_into(VGroup(isolated[0], divisors[0]), answer[0]),
                      copy_into(isolated[1], answer[1]),
                      copy_into(VGroup(isolated[2], divisors[1]), answer[2]),
                      *([copy_into(isolated[3], answer[3]),
                         copy_into(VGroup(isolated[4], divisors[2]), answer[4])] if p.c else []),
                      run_time=1.6)
            self.play(Create(box), run_time=.8)
            self.beat('answer', READ_LONG)


            self.say('This is slope-intercept form.')
        self.beat('hold', READ_LONG)
        self.write_marks(self.problem.marks_file)


class SlopePointSlopeIntercept(EquationsOfLines):
    """Problem 1: m = 5/7 through (3, 4), written in slope-intercept form."""
    problem = SLOPE_POINT


class TwoPointsStandard(EquationsOfLines):
    """Problem 2: through (11, 2) and (2, 8), written in standard form."""
    problem = TWO_POINTS


class ParallelSlopeIntercept(EquationsOfLines):
    """Problem 3: parallel to 8x + 6y = 15 through (3, -4), written in slope-intercept form."""
    problem = PARALLEL
