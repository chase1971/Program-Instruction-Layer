"""Parabolas (pre-calc conics): worksheet problem 2, -(1/4)y^2 = x - 2, a parabola that opens left.

Same process as ParabolaOpensUp, turned sideways: y is squared so it opens left or right, and the
directrix is a vertical line (x =) while the axis of symmetry is horizontal (y =).

Verified (LeftProblem.__post_init__ re-checks it with Fraction):
    -(1/4)y^2 = x - 2  ->  multiply both sides by -4  ->  y^2 = -4(x - 2)
    vertex (2, 0), 4p = -4 so p = -1, opens left, focus (1, 0), focal width 4
    -> (1, 2) and (1, -2), directrix x = 3, axis of symmetry y = 0

Layout and colours are shared with parabola_walkthrough.py: phase 1 is algebra on the full board,
phase 2 keeps the answers in a two-column list above the graph.
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from dataclasses import dataclass  # noqa: E402
from fractions import Fraction  # noqa: E402

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    NumberPlane,
    ParametricFunction,
    ReplacementTransform,
    VGroup,
    Write,
)

from equations_of_lines import READ_LONG, READ_SHORT, fraction, signed, tex, var  # noqa: E402
from math_notation import NEG  # noqa: E402
from parabola_walkthrough import (  # noqa: E402
    CURVE_COLOR,
    DIRECTION_Y,
    FORM_SIZE,
    FORM_Y,
    FOUR_P_Y,
    GRAPH_CENTER_Y,
    GRAPH_WIDTH,
    LEFT_X,
    LIST_Y,
    MATH_SIZE,
    P_COLOR,
    P_Y,
    PROBLEM_Y,
    PT_COLOR,
    RIGHT_X,
    VERTEX_UP_Y,
    VERTEX_Y,
    ParabolaOpensUp,
)
from scene_style import PAPER_BLUE, PAPER_GOLD, PAPER_MUTED  # noqa: E402
from solve_steps import divide_bars, strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

GRAPH_X, GRAPH_Y = (-4, 10), (-4, 4)   # the curve opens left, so the grid starts left of it


@dataclass
class LeftProblem:
    """(y - k)^2 = c(x - h): a horizontal parabola that opens left (c < 0), k = 0, h > 0.

    The worksheet gives it as -(1/4)y^2 = x - 2, so `lead` is the -1/4 and c = 1 / lead.
    c must be divisible by 4 so p is a whole number the graph can count.
    """
    h: int
    lead: Fraction
    marks_file: str

    def __post_init__(self):
        self.k = 0
        self.c = int(1 / self.lead)
        if self.c >= 0 or self.c % 4:
            raise ValueError('c = 4p must be negative and divisible by 4.')
        self.p = self.c // 4
        self.focus = (self.h + self.p, 0)
        self.width = abs(self.c)
        self.half = self.width // 2
        self.ends = ((self.focus[0], self.half), (self.focus[0], -self.half))
        self.directrix = self.h - self.p
        for x, y in self.ends:   # both ends sit on the curve
            if self.c * (x - self.h) != y ** 2:
                raise ValueError('The focal-width ends are not on the parabola.')
        if self.focus[0] - self.h != -(self.directrix - self.h):
            raise ValueError('Focus and directrix must be |p| from the vertex.')


OPENS_LEFT = LeftProblem(h=2, lead=Fraction(-1, 4), marks_file='parabola_opens_left_marks.json')


class ParabolaOpensLeft(ParabolaOpensUp):
    problem = OPENS_LEFT

    def build_graph(self):
        scale = GRAPH_WIDTH / (GRAPH_X[1] - GRAPH_X[0])
        plane = NumberPlane(
            x_range=[*GRAPH_X, 1], y_range=[*GRAPH_Y, 1],
            x_length=GRAPH_WIDTH, y_length=scale * (GRAPH_Y[1] - GRAPH_Y[0]),
            axis_config={'color': PAPER_MUTED, 'stroke_width': 2},
            background_line_style={'stroke_color': '#CBD5E1', 'stroke_width': 1,
                                   'stroke_opacity': 1},
            faded_line_ratio=0,
        )
        plane.move_to([0, GRAPH_CENTER_Y, 0])
        return plane

    def construct(self):
        p = self.problem
        h, k = p.h, p.k
        fx, fy = p.focus
        half_arrow = abs(p.p)

        # ---- phase 1 rows --------------------------------------------------------------------
        # The multiplier goes in front of both sides in gold; the fraction's 4 and the multiplier's 4
        # cancel (the equations_of_lines "clear the fraction" beat). The negatives are not mentioned.
        mult = abs(p.c)
        given_frac = fraction(f'-1', str(mult))
        given_rest = tex('y^2', '=', 'x', '-', str(h), size=MATH_SIZE)
        given = VGroup(given_frac, given_rest).arrange(RIGHT, buff=0.1)
        given_frac.shift(UP * (given_rest[1].get_center()[1] - given_frac[1].get_center()[1]))
        given.move_to([0, PROBLEM_Y, 0])
        t_open = tex(NEG, str(mult), '(', size=MATH_SIZE)
        t_frac = fraction('-1', str(mult))
        t_mid = tex('y^2', ')', '=', size=MATH_SIZE)
        t_right = tex(NEG, str(mult), '(', 'x', '-', str(h), ')', size=MATH_SIZE)
        times = VGroup(t_open, t_frac, t_mid, t_right).arrange(RIGHT, buff=0.12)
        t_frac.shift(UP * (t_mid[2].get_center()[1] - t_frac[1].get_center()[1]))
        if times.width > 6.1:
            times.scale(6.1 / times.width)
        times.move_to([0, PROBLEM_Y, 0])
        for gold in (t_open[0], t_open[1], t_right[0], t_right[1]):
            gold.set_color(PT_COLOR)
        four_strikes = strike_pair(t_frac[2], t_open[1])   # the 4s, bottom and multiplier
        problem = tex('y^2', '=', signed(p.c), '(', 'x', '-', str(h), ')',
                      size=MATH_SIZE).move_to([0, PROBLEM_Y, 0])
        problem[2].set_color(PT_COLOR)   # the multiplier arrives gold, like the op it came from
        form = tex('(', 'y', '-', 'k', ')^2', '=', '4p', '(', 'x', '-', 'h', ')',
                   size=FORM_SIZE).move_to([0, FORM_Y, 0])
        form[3].set_color(PT_COLOR)
        form[10].set_color(PT_COLOR)
        vertex = tex('(', 'h', ',', 'k', ')', '=', '(', str(h), ',', str(k), ')',
                     size=FORM_SIZE).move_to([0, VERTEX_Y, 0])
        for i in (1, 3, 7, 9):
            vertex[i].set_color(PT_COLOR)
        raw = tex('(', 'y', '-', str(k), ')^2', '=', '4p', '(', 'x', '-', str(h), ')',
                  size=FORM_SIZE).move_to([0, FORM_Y, 0])
        plug = tex('y^2', '=', '4p', '(', 'x', '-', str(h), ')',
                   size=FORM_SIZE).move_to([0, FORM_Y, 0])
        for i in (3, 10):
            raw[i].set_color(PT_COLOR)
        plug[6].set_color(PT_COLOR)
        four_p = tex('4p', '=', signed(p.c), size=MATH_SIZE).move_to([0, FOUR_P_Y, 0])
        bars, divisors = divide_bars([four_p[0], four_p[2]], '4')
        p_row = tex('p', '=', signed(p.p), size=MATH_SIZE).move_to([0, P_Y, 0])
        p_row[2].set_color(P_COLOR)
        direction = tex(r'\text{opens }', r'\text{left}', size=48).move_to([0, DIRECTION_Y, 0])
        direction[1].set_color(P_COLOR)

        # ---- phase 2: the answer list, and the graph -----------------------------------------
        vertex_item = self.list_row('Vertex', '(', str(h), ',', str(k), ')', x=LEFT_X, y=LIST_Y[0])
        p_item = self.list_row('p', signed(p.p), x=LEFT_X, y=LIST_Y[1])
        direction_item = self.list_row('Direction', r'\text{left}', x=LEFT_X, y=LIST_Y[2])
        focus_item = self.list_row('Focus', '(', str(fx), ',', str(fy), ')', x=LEFT_X, y=LIST_Y[3])
        width_item = self.list_row('Focal width', str(p.width), x=RIGHT_X, y=LIST_Y[0])
        directrix_item = self.list_row('Directrix', 'x', '=', str(p.directrix),
                                       x=RIGHT_X, y=LIST_Y[1])
        aos_item = self.list_row('A.O.S.', 'y', '=', str(k), x=RIGHT_X, y=LIST_Y[2])

        plane = self.build_graph()

        def c2p(x, y):
            return plane.c2p(x, y)

        def dot(x, y, color):
            return Dot(c2p(x, y), color=color, radius=.09)

        def run(a, b):
            return Arrow(c2p(*a), c2p(*b), buff=0, color=PAPER_GOLD, stroke_width=5,
                         tip_length=.14, max_tip_length_to_length_ratio=.4)

        vertex_dot = dot(h, k, CURVE_COLOR)
        focus_dot = dot(fx, fy, P_COLOR)
        end_dots = VGroup(*[dot(x, y, CURVE_COLOR) for x, y in p.ends])
        left_arrow = run((h, k), p.focus)
        left_label = tex(str(half_arrow), size=28, color=PAPER_GOLD).next_to(left_arrow, UP,
                                                                              buff=.08)
        side_arrows = VGroup(run(p.focus, p.ends[0]), run(p.focus, p.ends[1]))
        side_labels = VGroup(*[
            tex(str(p.half), size=28, color=PAPER_GOLD).next_to(a, LEFT, buff=.08)
            for a in side_arrows])
        right_arrow = run((h, k), (p.directrix, k))
        right_label = tex(str(half_arrow), size=28, color=PAPER_GOLD).next_to(right_arrow, UP,
                                                                               buff=.08)
        curve = ParametricFunction(lambda t: c2p(h + t * t / p.c, t),
                                   t_range=[GRAPH_Y[0], GRAPH_Y[1]], color=CURVE_COLOR,
                                   stroke_width=5)
        directrix_line = DashedLine(c2p(p.directrix, GRAPH_Y[0]), c2p(p.directrix, GRAPH_Y[1]),
                                    color=PAPER_BLUE, stroke_width=4, dash_length=.12)
        directrix_label = tex('x', '=', str(p.directrix), size=28, color=PAPER_BLUE
                              ).next_to(c2p(p.directrix, 3.4), RIGHT, buff=.08)
        aos_line = DashedLine(c2p(GRAPH_X[0], k), c2p(GRAPH_X[1], k), color=PAPER_BLUE,
                              stroke_width=4, dash_length=.12)
        aos_label = tex('y', '=', str(k), size=28, color=PAPER_BLUE
                        ).next_to(c2p(8.6, k), UP, buff=.08)

        # ---- 1. which way does it open, and get the squared term alone -------------------------
        self.say(f'Here is a parabola. The {var("y", PAPER_BLUE)} is squared, so it opens left '
                 f'or right.')
        self.play(FadeIn(given), run_time=1.2)
        self.play(Indicate(given[0], color=PAPER_BLUE, scale_factor=1.25), run_time=1.1)
        self.beat('problem', READ_LONG)

        self.say(f'Multiply both sides by {p.c} to cancel out the denominator.')
        self.play(
            ReplacementTransform(given_frac, t_frac),
            ReplacementTransform(given_rest[0], t_mid[0]),
            ReplacementTransform(given_rest[1], t_mid[2]),
            *[ReplacementTransform(given_rest[2 + i], t_right[3 + i]) for i in range(3)],
            FadeIn(VGroup(t_open, t_mid[1], t_right[0], t_right[1], t_right[2], t_right[6])),
            run_time=1.6)
        self.beat('times', READ_LONG)

        self.play(*[Create(line) for line in four_strikes], run_time=.8)
        self.beat('cancel', READ_LONG)

        self.play(copy_into(t_mid[0], problem[0]), copy_into(t_mid[2], problem[1]),
                  copy_into(VGroup(t_right[0], t_right[1]), problem[2]),
                  *[copy_into(t_right[2 + i], problem[3 + i]) for i in range(5)], run_time=1.5)
        self.play(FadeOut(VGroup(times, four_strikes)), run_time=.6)
        self.beat('alone', READ_SHORT)

        # ---- 2. the vertex, and why the signs flip ---------------------------------------------
        self.say('The vertex is (h, k).')
        self.play(Write(form), run_time=1.3)
        self.play(Indicate(form[3], color=PT_COLOR, scale_factor=1.5),
                  Indicate(form[10], color=PT_COLOR, scale_factor=1.5), run_time=1.1)
        self.beat('form', READ_SHORT)

        self.say('Be careful. This one is flipped, with the y in front. The x part is still h, '
                 'so the vertex is (2, 0), not (0, 2).')
        self.play(Indicate(form[1], color=PAPER_BLUE, scale_factor=1.5),
                  Indicate(form[8], color=PAPER_BLUE, scale_factor=1.5), run_time=1.2)
        self.beat('flipped', READ_LONG)

        self.say('The h and k values come out as the opposite of the numbers you see. '
                 'There is no number with the y, so k is 0.')
        self.play(Indicate(problem[5], color=PT_COLOR, scale_factor=1.6),
                  Indicate(problem[6], color=PT_COLOR, scale_factor=1.6),
                  Indicate(problem[0], color=PT_COLOR, scale_factor=1.3), run_time=1.3)
        self.beat('opposites', READ_LONG)

        self.say(f'So (h, k) equals ({h}, {k}).')
        self.play(FadeIn(vertex), run_time=1.2)
        self.beat('vertex', READ_LONG)

        self.say('Plug these values in, and you get the original expression.')
        self.play(Indicate(vertex[7], color=PT_COLOR, scale_factor=1.4),
                  Indicate(vertex[9], color=PT_COLOR, scale_factor=1.4), run_time=1.1)
        # The values fly up into the form that is already on screen: h and k are replaced in place.
        self.play(*[ReplacementTransform(form[i], raw[i]) for i in range(12) if i not in (3, 10)],
                  FadeOut(VGroup(form[3], form[10])),
                  copy_into(vertex[7], raw[10]), copy_into(vertex[9], raw[3]), run_time=1.8)
        self.beat('plug', READ_LONG)

        self.say('Subtracting zero changes nothing, so the y is just squared.')
        self.play(ReplacementTransform(raw, plug), run_time=1.4)
        self.beat('plug-zero', READ_LONG)

        self.play(FadeOut(plug), vertex.animate.move_to([0, VERTEX_UP_Y, 0]), run_time=1.0)

        # ---- 3. p ----------------------------------------------------------------------------
        self.say(f'Now find p. The number in front is 4p, so divide {p.c} by 4.')
        self.play(Indicate(problem[2], color=P_COLOR, scale_factor=1.5), run_time=1.0)
        self.play(FadeIn(VGroup(four_p[0], four_p[1])), copy_into(problem[2], four_p[2]),
                  run_time=1.2)
        for bar, divisor in zip(bars, divisors):
            self.play(Create(bar), FadeIn(divisor, shift=DOWN * .15), run_time=.8)
        self.beat('divide', READ_LONG)

        self.say(f'So {var("p", PAPER_BLUE)} is {p.p}.')
        self.play(copy_into(VGroup(four_p[0], divisors[0]), p_row[0]), FadeIn(p_row[1]),
                  copy_into(VGroup(four_p[2], divisors[1]), p_row[2]), run_time=1.5)
        self.beat('p', READ_LONG)

        self.say(f'{var("p", PAPER_BLUE)} is negative, so it opens left. '
                 f'A positive {var("p", PAPER_BLUE)} would open right.')
        self.play(Indicate(p_row[2], color=P_COLOR, scale_factor=1.5), run_time=1.0)
        self.play(FadeIn(direction), run_time=1.0)
        self.beat('direction', READ_LONG)

        # ---- 4. the graph and the answer list --------------------------------------------------
        self.say('Now graph it. We will keep our answers in a list.')
        self.play(
            copy_into(vertex, vertex_item), copy_into(p_row, p_item),
            copy_into(direction, direction_item),
            FadeOut(VGroup(four_p, bars, divisors, vertex, p_row, direction, problem)),
            FadeIn(plane), run_time=1.8)
        self.beat('list', READ_LONG)

        self.say(f'Plot the vertex, ({h}, {k}).')
        self.play(FadeIn(vertex_dot, scale=1.6), run_time=1.0)
        self.beat('vertex-dot', READ_SHORT)

        # ---- 5. focus -------------------------------------------------------------------------
        self.say(f'{var("p", PAPER_BLUE)} tells us where the focus is. It is {half_arrow} to the '
                 f'left of the vertex.')
        self.play(Create(left_arrow), FadeIn(left_label), run_time=1.3)
        self.play(FadeIn(focus_dot, scale=1.6), run_time=.8)
        self.play(Write(focus_item), run_time=1.0)
        self.beat('focus', READ_LONG)

        # ---- 6. focal width -------------------------------------------------------------------
        self.say(f'The focal width, or latus rectum, is the absolute value of 4p. '
                 f'|4p| = {p.width}.')
        self.play(Write(width_item), run_time=1.2)
        self.beat('width', READ_LONG)

        self.say(f'Half of {p.width} is {p.half}. Go up {p.half} and down {p.half} from the '
                 f'focus, and put two more dots.')
        self.play(FadeOut(VGroup(left_arrow, left_label)), run_time=.5)
        self.play(*[Create(a) for a in side_arrows], FadeIn(side_labels), run_time=1.3)
        self.play(FadeIn(end_dots, scale=1.6), run_time=.8)
        self.beat('end-dots', READ_LONG)

        # ---- 7. the curve ---------------------------------------------------------------------
        self.say('Now draw the parabola through the three points.')
        self.play(FadeOut(VGroup(side_arrows, side_labels)), run_time=.5)
        self.play(Create(curve), run_time=2.0)
        self.beat('curve', READ_LONG)

        # ---- 8. directrix ---------------------------------------------------------------------
        self.say(f'The directrix is the same distance {var("p", PAPER_BLUE)} from the vertex, '
                 f'in the opposite direction. Right {half_arrow}.')
        self.play(Create(right_arrow), FadeIn(right_label), run_time=1.3)
        self.beat('directrix-right', READ_SHORT)

        self.say('Draw a dashed line there, parallel to the y-axis.')
        self.play(FadeOut(VGroup(right_arrow, right_label)), run_time=.4)
        self.play(Create(directrix_line), FadeIn(directrix_label), run_time=1.3)
        self.play(Write(directrix_item), run_time=1.0)
        self.beat('directrix', READ_LONG)

        # ---- 9. axis of symmetry --------------------------------------------------------------
        self.say('The axis of symmetry splits the parabola down the middle.')
        self.play(Create(aos_line), FadeIn(aos_label), run_time=1.3)
        self.play(Write(aos_item), run_time=1.0)
        self.beat('aos', READ_LONG)

        self.say(f'The directrix is vertical, so it is {var("x", PAPER_BLUE)} equals. '
                 f'The axis of symmetry is horizontal, so it is {var("y", PAPER_BLUE)} equals.')
        self.play(Indicate(aos_item, color=PAPER_BLUE, scale_factor=1.15),
                  Indicate(directrix_item, color=PAPER_BLUE, scale_factor=1.15), run_time=1.3)
        self.beat('hold', READ_LONG)
        self.write_marks(self.problem.marks_file)
