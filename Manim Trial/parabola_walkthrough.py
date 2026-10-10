"""Parabolas (pre-calc conics): read everything off (x - h)^2 = 4p(y - k), then graph it.

Chase teaches a process, not formulas. Every clip in this module runs the same beats:
    x is squared -> it opens up or down -> the vertex (h, k), and why the signs flip when you plug
    in -> p from 4p -> p positive means up -> plot the vertex -> the focus is p from the vertex
    -> the focal width |4p| sends you half that far left and right of the focus -> draw the curve
    -> the directrix is p from the vertex the other way -> the axis of symmetry splits it.

Verified (Problem.__post_init__ re-checks it with Fraction):
    ParabolaOpensUp: (x - 2)^2 = 12(y + 1)
        vertex (2, -1), 4p = 12 so p = 3, opens up, focus (2, 2), focal width 12
        -> (-4, 2) and (8, 2), directrix y = -4, axis of symmetry x = 2

PORTRAIT 4:5 frame (portrait_frame.py), 6.4 x 8 units. Phase 1 is algebra on the full board;
phase 2 keeps the answers in a two-column list above the graph and fills it in as the graph
finds each one. Every MathTex goes through mathtex() with INK: its default is white, invisible
on paper.
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
    ReplacementTransform,
    Scene,
    VGroup,
    Write,
)

from equations_of_lines import READ_LONG, READ_SHORT, signed, tex, var  # noqa: E402
from math_notation import NEG  # noqa: E402
from scene_style import (  # noqa: E402
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    PAPER_MUTED,
    PAPER_RED,
    Narrated,
    apply_portal_paper_background,
)
from solve_steps import divide_bars  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

apply_portal_paper_background()

INK = PAPER_INK
PT_COLOR = PAPER_GOLD    # h and k: the vertex's numbers
P_COLOR = PAPER_BLUE     # p
CURVE_COLOR = PAPER_RED  # the parabola and the points that make it
MATH_SIZE = 52
FORM_SIZE = 44
LIST_SIZE = 30

# Phase 1 row centres (the caption owns y > 2.95).
PROBLEM_Y, FORM_Y, VERTEX_Y = 2.3, 1.2, 0.2
VERTEX_UP_Y = 1.2        # the vertex row slides up once the plug demo is cleared
FOUR_P_Y, P_Y, DIRECTION_Y = 0.0, -1.5, -2.6

# Phase 2: the answer list sits above the graph.
LIST_Y = (1.6, 1.08, 0.56, 0.04)
LEFT_X, RIGHT_X = -2.9, 0.05
GRAPH_X, GRAPH_Y = (-5, 9), (-5, 3)
GRAPH_WIDTH, GRAPH_CENTER_Y = 5.8, -2.05


@dataclass
class Problem:
    """(x - h)^2 = c(y - k): a vertical parabola that opens up (c > 0), h > 0 > k.

    The beats show the plug-in as y - (-k) -> y + k, so only a positive h and a negative k are
    built so far. c must be divisible by 4 so p is a whole number the graph can count.
    """
    h: int
    k: int
    c: int
    marks_file: str

    def __post_init__(self):
        if not (self.h > 0 > self.k):
            raise ValueError('Built for a positive h and a negative k only.')
        if self.c < 4 or self.c % 4:
            raise ValueError('c = 4p must be positive and divisible by 4.')
        self.p = Fraction(self.c, 4)
        self.p = int(self.p)
        self.focus = (self.h, self.k + self.p)
        self.width = abs(self.c)
        self.half = self.width // 2
        self.ends = ((self.h - self.half, self.focus[1]), (self.h + self.half, self.focus[1]))
        self.directrix = self.k - self.p
        for x, y in self.ends:   # both ends sit on the curve
            if Fraction(self.c) * (y - self.k) != (x - self.h) ** 2:
                raise ValueError('The focal-width ends are not on the parabola.')
        if (self.focus[1] - self.k) != -(self.directrix - self.k):
            raise ValueError('Focus and directrix must be p from the vertex.')


OPENS_UP = Problem(h=2, k=-1, c=12, marks_file='parabola_walkthrough_marks.json')


class ParabolaOpensUp(Narrated, Scene):
    caption_color = PAPER_INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9
    problem = OPENS_UP

    def beat(self, mark, seconds, allow=()):
        """Hold the caption long enough to read, then record the pause point."""
        self.wait(seconds)
        self.mark(mark, allow=allow)

    def list_row(self, label, *parts, x, y):
        """One answer-list row, left-aligned at x."""
        row = tex(rf'\text{{{label}: }}', *parts, size=LIST_SIZE)
        return row.move_to([x + row.width / 2, y, 0])

    def build_graph(self):
        """The grid, and a point/arrow factory that works in graph coordinates."""
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

        # ---- phase 1 rows, each built once at its final spot ---------------------------------
        problem = tex('(', 'x', '-', str(h), ')^2', '=', str(p.c), '(', 'y', '+', str(-k), ')',
                      size=MATH_SIZE).move_to([0, PROBLEM_Y, 0])
        form = tex('(', 'x', '-', 'h', ')^2', '=', '4p', '(', 'y', '-', 'k', ')',
                   size=FORM_SIZE).move_to([0, FORM_Y, 0])
        form[3].set_color(PT_COLOR)
        form[10].set_color(PT_COLOR)
        vertex = tex('(', 'h', ',', 'k', ')', '=', '(', str(h), ',', signed(k), ')',
                     size=FORM_SIZE).move_to([0, VERTEX_Y, 0])
        for i in (1, 3, 7, 9):
            vertex[i].set_color(PT_COLOR)
        raw = tex('(', 'x', '-', str(h), ')^2', '=', '4p', '(', 'y', '-', f'({signed(k)})', ')',
                  size=FORM_SIZE).move_to([0, FORM_Y, 0])
        plug = tex('(', 'x', '-', str(h), ')^2', '=', '4p', '(', 'y', '+', str(-k), ')',
                   size=FORM_SIZE).move_to([0, FORM_Y, 0])
        for row, spots in ((raw, (3, 10)), (plug, (3, 10))):
            for i in spots:
                row[i].set_color(PT_COLOR)
        four_p = tex('4p', '=', str(p.c), size=MATH_SIZE).move_to([0, FOUR_P_Y, 0])
        bars, divisors = divide_bars([four_p[0], four_p[2]], '4')
        p_row = tex('p', '=', str(p.p), size=MATH_SIZE).move_to([0, P_Y, 0])
        p_row[2].set_color(P_COLOR)
        direction = tex(r'\text{opens }', r'\text{up}', size=48).move_to([0, DIRECTION_Y, 0])
        direction[1].set_color(P_COLOR)

        # ---- phase 2: the answer list, and the graph -----------------------------------------
        fx, fy = p.focus
        vertex_item = self.list_row('Vertex', '(', str(h), ',', signed(k), ')',
                                    x=LEFT_X, y=LIST_Y[0])
        p_item = self.list_row('p', str(p.p), x=LEFT_X, y=LIST_Y[1])
        direction_item = self.list_row('Direction', r'\text{up}', x=LEFT_X, y=LIST_Y[2])
        focus_item = self.list_row('Focus', '(', str(fx), ',', str(fy), ')',
                                   x=LEFT_X, y=LIST_Y[3])
        width_item = self.list_row('Focal width', str(p.width), x=RIGHT_X, y=LIST_Y[0])
        directrix_item = self.list_row('Directrix', 'y', '=', signed(p.directrix),
                                       x=RIGHT_X, y=LIST_Y[1])
        aos_item = self.list_row('A.O.S.', 'x', '=', str(h), x=RIGHT_X, y=LIST_Y[2])

        plane = self.build_graph()

        def c2p(x, y):
            return plane.c2p(x, y)

        def dot(x, y, color):
            return Dot(c2p(x, y), color=color, radius=.09)

        def run(a, b, color=PAPER_GOLD):
            return Arrow(c2p(*a), c2p(*b), buff=0, color=color, stroke_width=5,
                         tip_length=.14, max_tip_length_to_length_ratio=.4)

        vertex_dot = dot(h, k, CURVE_COLOR)
        focus_dot = dot(fx, fy, P_COLOR)
        end_dots = VGroup(*[dot(x, y, CURVE_COLOR) for x, y in p.ends])
        up_arrow = run((h, k), p.focus)
        up_label = tex(str(p.p), size=28, color=PAPER_GOLD).next_to(up_arrow, RIGHT, buff=.08)
        side_arrows = VGroup(run(p.focus, p.ends[0]), run(p.focus, p.ends[1]))
        side_labels = VGroup(*[
            tex(str(p.half), size=28, color=PAPER_GOLD).next_to(a, UP, buff=.06)
            for a in side_arrows])
        down_arrow = run((h, k), (h, p.directrix))
        down_label = tex(str(p.p), size=28, color=PAPER_GOLD).next_to(down_arrow, RIGHT, buff=.08)
        curve = plane.plot(lambda x: k + (x - h) ** 2 / p.c, x_range=[h - 6.6, h + 6.6],
                           color=CURVE_COLOR, stroke_width=5)
        directrix_line = DashedLine(c2p(GRAPH_X[0], p.directrix), c2p(GRAPH_X[1], p.directrix),
                                    color=PAPER_BLUE, stroke_width=4, dash_length=.12)
        directrix_label = tex('y', '=', signed(p.directrix), size=28, color=PAPER_BLUE
                              ).next_to(c2p(7.2, p.directrix), UP, buff=.05)
        aos_line = DashedLine(c2p(h, GRAPH_Y[0]), c2p(h, GRAPH_Y[1]), color=PAPER_BLUE,
                              stroke_width=4, dash_length=.12)
        aos_label = tex('x', '=', str(h), size=28, color=PAPER_BLUE
                        ).next_to(c2p(h, 2.7), RIGHT, buff=.08)

        # ---- 1. which way does it open? --------------------------------------------------------
        self.say(f'Here is a parabola. The {var("x", PAPER_BLUE)} is squared, so it opens up or down.')
        self.play(FadeIn(problem), run_time=1.2)
        self.play(Indicate(problem[4], color=PAPER_BLUE, scale_factor=1.6), run_time=1.1)
        self.beat('problem', READ_LONG)

        # ---- 2. the vertex, and why the signs flip ---------------------------------------------
        self.say('The vertex is (h, k).')
        self.play(Write(form), run_time=1.3)
        self.play(Indicate(form[3], color=PT_COLOR, scale_factor=1.5),
                  Indicate(form[10], color=PT_COLOR, scale_factor=1.5), run_time=1.1)
        self.beat('form', READ_SHORT)

        self.say('The h and k values come out as the opposite of the numbers you see.')
        self.play(Indicate(problem[3], color=PT_COLOR, scale_factor=1.6),
                  Indicate(problem[9], color=PT_COLOR, scale_factor=1.6),
                  Indicate(problem[10], color=PT_COLOR, scale_factor=1.6), run_time=1.3)
        self.beat('opposites', READ_SHORT)

        self.say(f'So (h, k) equals ({h}, {k}).')
        self.play(FadeIn(vertex), run_time=1.2)
        self.beat('vertex', READ_LONG)

        self.say('Plug these values in, and you get the original expression.')
        self.play(Indicate(vertex[7], color=PT_COLOR, scale_factor=1.4),
                  Indicate(vertex[9], color=PT_COLOR, scale_factor=1.4), run_time=1.1)
        # The values fly up into the form that is already on screen: h and k are replaced in place.
        self.play(*[ReplacementTransform(form[i], raw[i]) for i in range(12) if i not in (3, 10)],
                  FadeOut(VGroup(form[3], form[10])),
                  copy_into(vertex[7], raw[3]), copy_into(vertex[9], raw[10]), run_time=1.8)
        self.beat('plug', READ_LONG)

        self.say('Subtracting a negative is the same as adding.')
        self.play(ReplacementTransform(raw, plug), run_time=1.4)
        self.play(Indicate(plug[9], color=PT_COLOR, scale_factor=1.5),
                  Indicate(plug[10], color=PT_COLOR, scale_factor=1.5), run_time=1.0)
        self.beat('plug-plus', READ_LONG)

        self.play(FadeOut(plug), vertex.animate.move_to([0, VERTEX_UP_Y, 0]), run_time=1.0)

        # ---- 3. p ----------------------------------------------------------------------------
        self.say(f'Now find p. The number in front is 4p, so divide {p.c} by 4.')
        self.play(Indicate(problem[6], color=P_COLOR, scale_factor=1.5), run_time=1.0)
        self.play(FadeIn(VGroup(four_p[0], four_p[1])), copy_into(problem[6], four_p[2]),
                  run_time=1.2)
        for bar, divisor in zip(bars, divisors):
            self.play(Create(bar), FadeIn(divisor, shift=DOWN * .15), run_time=.8)
        self.beat('divide', READ_LONG)

        self.say(f'So {var("p", PAPER_BLUE)} is {p.p}.')
        self.play(copy_into(VGroup(four_p[0], divisors[0]), p_row[0]), FadeIn(p_row[1]),
                  copy_into(VGroup(four_p[2], divisors[1]), p_row[2]), run_time=1.5)
        self.beat('p', READ_LONG)

        self.say(f'{var("p", PAPER_BLUE)} is positive, so it opens up.')
        self.play(Indicate(p_row[2], color=P_COLOR, scale_factor=1.5), run_time=1.0)
        self.play(FadeIn(direction), run_time=1.0)
        self.beat('direction', READ_LONG)

        # ---- 4. the graph and the answer list --------------------------------------------------
        self.say('Now graph it. We will keep our answers in a list.')
        self.play(
            copy_into(vertex, vertex_item), copy_into(p_row, p_item),
            copy_into(direction, direction_item),
            FadeOut(VGroup(four_p, bars, divisors, vertex, p_row, direction)),
            FadeIn(plane), run_time=1.8)
        self.beat('list', READ_LONG)

        self.say(f'Plot the vertex, ({h}, {k}).')
        self.play(FadeIn(vertex_dot, scale=1.6), run_time=1.0)
        self.beat('vertex-dot', READ_SHORT)

        # ---- 5. focus -------------------------------------------------------------------------
        self.say(f'{var("p", PAPER_BLUE)} tells us where the focus is. It is up {p.p} from '
                 f'the vertex.')
        self.play(Create(up_arrow), FadeIn(up_label), run_time=1.3)
        self.play(FadeIn(focus_dot, scale=1.6), run_time=.8)
        self.play(Write(focus_item), run_time=1.0)
        self.beat('focus', READ_LONG)

        # ---- 6. focal width -------------------------------------------------------------------
        self.say(f'The focal width, or latus rectum, is the absolute value of 4p. '
                 f'|4p| = {p.width}.')
        self.play(Write(width_item), run_time=1.2)
        self.beat('width', READ_LONG)

        self.say(f'Half of {p.width} is {p.half}. Go left {p.half} and right {p.half} from the '
                 f'focus, and put two more dots.')
        self.play(FadeOut(VGroup(up_arrow, up_label)), run_time=.5)
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
                 f'in the opposite direction. Down {p.p}.')
        self.play(Create(down_arrow), FadeIn(down_label), run_time=1.3)
        self.beat('directrix-down', READ_SHORT)

        self.say('Draw a dashed line there, parallel to the x-axis.')
        self.play(FadeOut(VGroup(down_arrow, down_label)), run_time=.4)
        self.play(Create(directrix_line), FadeIn(directrix_label), run_time=1.3)
        self.play(Write(directrix_item), run_time=1.0)
        self.beat('directrix', READ_LONG)

        # ---- 9. axis of symmetry --------------------------------------------------------------
        self.say('The axis of symmetry splits the parabola down the middle.')
        self.play(Create(aos_line), FadeIn(aos_label), run_time=1.3)
        self.play(Write(aos_item), run_time=1.0)
        self.beat('aos', READ_LONG)

        self.say(f'A vertical line is {var("x", PAPER_BLUE)} equals. '
                 f'A horizontal line is {var("y", PAPER_BLUE)} equals.')
        self.play(Indicate(aos_item, color=PAPER_BLUE, scale_factor=1.15),
                  Indicate(directrix_item, color=PAPER_BLUE, scale_factor=1.15), run_time=1.3)
        self.beat('hold', READ_LONG)
        self.write_marks(self.problem.marks_file)
