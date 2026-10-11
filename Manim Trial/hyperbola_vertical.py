"""Hyperbolas (pre-calc conics): worksheet problem 2, (y+3)^2 - (x+2)^2 = 4, opens up and down.

Mirrors hyperbola_horizontal.py beat for beat (same layout, colours, captions, box, diagonals and
the right triangle for the foci). What changes:
  - The right side is 4, not 1, so the clip opens with the divide step: a fraction bar under every
    term, 4 under each bar (solve_steps.divide_bars), and those bars and 4s become the standard
    form. 4 over 4 is the 1 on the right.
  - y is the first term, so a^2 sits under y and the curve opens up and down. The transverse axis
    is vertical and the conjugate axis horizontal.
  - Both h and k are negative, so the center beat shows y - (-3) and x - (-2).
  - a = b = 2, so the box is a square and the asymptote slope is 2/2 = 1 (one extra beat).
  - c^2 = 8, so the root is simplified: c = 2 sqrt(2).
  - The diagonal pivots down onto the transverse axis once (the lower-right corner, clockwise like
    a clock hand). The other focus is just named and shown; the pivot is not repeated.

Verified (HyperbolaVerticalProblem.__post_init__ re-checks it with Fraction):
    (y+3)^2/4 - (x+2)^2/4 = 1; center (-2, -3); 4 under y -> a = 2 up and down;
    4 under x -> b = 2 left and right; y in front: vertical transverse axis
    vertices (-2, -5) and (-2, -1); box corners (-4, -5), (0, -5), (0, -1), (-4, -1)
    slope +/- a/b = +/- 1; c^2 = 4 + 4 = 8; foci (-2, -3 +/- 2 sqrt(2))
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

import math  # noqa: E402

import numpy as np  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from fractions import Fraction  # noqa: E402

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Create,
    DashedLine,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    NumberPlane,
    ParametricFunction,
    ReplacementTransform,
    Rotate,
    VGroup,
    Write,
    linear,
)

from ellipse_horizontal import ellipse_row  # noqa: E402
from equations_of_lines import READ_LONG, READ_SHORT, signed, tex  # noqa: E402
from hyperbola_horizontal import (  # noqa: E402
    ACROSS_Y,
    CENTER_Y,
    CONJUGATE_Y,
    FOCI_Y,
    FORM_ROW_Y,
    FORMULA_Y,
    HYPERBOLA_Y,
    LIST4,
    POINT_SLOPE_Y,
    ROW_SIZE,
    SLOPE_Y,
    TRANSVERSE_Y,
    UPDOWN_Y,
    VERTICES_Y,
    asymptote_endpoints,
    v,
)
from parabola_walkthrough import (  # noqa: E402
    CURVE_COLOR,
    LEFT_X,
    MATH_SIZE,
    P_COLOR,
    PT_COLOR,
    ParabolaOpensUp,
)
from scene_style import PAPER_BLUE, PAPER_GOLD, PAPER_INK, PAPER_MUTED  # noqa: E402
from solve_steps import divide_bars  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

INK = PAPER_INK
GRAPH_X, GRAPH_Y = (-8, 4), (-8, 2)   # centered on (-2, -3); 12 x 10 keeps the box big enough to read
GRAPH_W = 5.4
GRAPH_CENTER_Y = -1.42                # the grid hangs just under the four-row answer list
UPDOWN_ROW_Y, ACROSS_ROW_Y = ACROSS_Y, UPDOWN_Y   # up/down comes first here, then left/right


@dataclass
class HyperbolaVerticalProblem:
    """(y - k)^2 / a2 - (x - h)^2 / b2 = 1 after dividing by rhs: a hyperbola that opens up and down.

    The worksheet form is (y - k)^2 - (x - h)^2 = rhs with a2 = b2 = rhs, so one divide by rhs
    makes both denominators. h and k are negative so the center beat shows subtracting a negative.
    """
    h: int
    k: int
    a2: int
    b2: int
    marks_file: str

    def __post_init__(self):
        self.a, self.b = math.isqrt(self.a2), math.isqrt(self.b2)
        if self.a ** 2 != self.a2 or self.b ** 2 != self.b2:
            raise ValueError('The denominators must be perfect squares.')
        if self.a2 != self.b2:
            raise ValueError('Built for one divisor: the same number under both terms.')
        if self.h >= 0 or self.k >= 0:
            raise ValueError('Built for negative h and k: the beat shows y - (-k) and x - (-h).')
        self.rhs = self.a2
        self.vertices = ((self.h, self.k - self.a), (self.h, self.k + self.a))
        self.slope = Fraction(self.a, self.b)     # up a, over b
        self.c2 = self.a2 + self.b2               # a^2 + b^2 = c^2
        self.c = math.sqrt(self.c2)
        if self.c2 != 8:
            raise ValueError('Built for c^2 = 8: the root beat simplifies it to 2 sqrt(2).')
        for x, y in self.vertices:                # both vertices sit on the hyperbola
            if Fraction((y - self.k) ** 2, self.a2) - Fraction((x - self.h) ** 2, self.b2) != 1:
                raise ValueError('A vertex is not on the hyperbola.')
        # The box corner (h + b, k + a) lies on the asymptote y - k = (a/b)(x - h).
        if self.slope * self.b != self.a:
            raise ValueError('The box corner is not on the asymptote.')
        if self.slope != 1:
            raise ValueError('Built for slope 1: the slope beat simplifies a/b to 1.')


PROBLEM = HyperbolaVerticalProblem(h=-2, k=-3, a2=4, b2=4, marks_file='hyperbola_vertical_marks.json')


class HyperbolaVertical(ParabolaOpensUp):
    problem = PROBLEM

    def build_graph(self):
        scale = GRAPH_W / (GRAPH_X[1] - GRAPH_X[0])
        plane = NumberPlane(
            x_range=[*GRAPH_X, 1], y_range=[*GRAPH_Y, 1],
            x_length=GRAPH_W, y_length=scale * (GRAPH_Y[1] - GRAPH_Y[0]),
            axis_config={'color': PAPER_MUTED, 'stroke_width': 2},
            background_line_style={'stroke_color': '#CBD5E1', 'stroke_width': 1,
                                   'stroke_opacity': 1},
            faded_line_ratio=0,
        )
        plane.move_to([0, GRAPH_CENTER_Y, 0])
        return plane

    def adopt(self, group, *parts):
        """Morphs leave their targets on screen piece by piece; put the whole row back in one."""
        self.remove(*parts)
        self.add(group)

    def construct(self):
        p = self.problem
        h, k, a, b = p.h, p.k, p.a, p.b
        k_raw, h_raw = f'({signed(k)})', f'({signed(h)})'
        slope_tex = rf'\frac{{{p.a}}}{{{p.b}}}'
        two_root_two = r'2\sqrt{2}'
        t_end = min(math.acosh((GRAPH_Y[1] - k) / a), math.acosh((k - GRAPH_Y[0]) / a),
                    math.asinh((GRAPH_X[1] - h) / b), math.asinh((h - GRAPH_X[0]) / b))

        # ---- phase 1 rows, each built once at its final spot ---------------------------------
        given = ellipse_row(['(', 'y', '+', str(-k), ')^2'], ['(', 'x', '+', str(-h), ')^2'],
                            str(p.a2), str(p.b2), MATH_SIZE - 6, op='-')
        shown = ellipse_row(['(', 'y', '-', k_raw, ')^2'], ['(', 'x', '-', h_raw, ')^2'],
                            str(p.a2), str(p.b2), MATH_SIZE - 6, op='-')
        fit = min(1, 5.7 / shown.width)   # both negatives make this row wider than the horizontal clip's
        for row in (given, shown):
            row.scale(fit).move_to([0, HYPERBOLA_Y, 0])
            row[0][0][3].set_color(PT_COLOR)     # the 3 in (y + 3), the -3 in (y - (-3))
            row[2][0][3].set_color(PT_COLOR)     # the 2 in (x + 2), the -2 in (x - (-2))
        under_y, under_x = shown[0][2], shown[2][2]

        # The worksheet problem, written so its terms sit exactly where the fractions' tops will.
        orig = tex('(y+3)^2', '-', '(x+2)^2', '=', str(p.rhs), size=MATH_SIZE - 6)
        orig.scale(fit).move_to([0, given[0][0].get_center()[1], 0])
        bars, divisors = divide_bars([orig[0], orig[2], orig[4]], str(p.rhs),
                                     size=(MATH_SIZE - 6) * fit)

        form = ellipse_row(['(', 'y', '-', 'k', ')^2'], ['(', 'x', '-', 'h', ')^2'],
                           'a^2', 'b^2', ROW_SIZE, op='-').move_to([0, FORM_ROW_Y, 0])
        for piece in (form[0][0][3], form[2][0][3]):
            piece.set_color(PT_COLOR)        # k and h
        for piece in (form[0][2][0], form[2][2][0]):
            piece.set_color(P_COLOR)         # a^2 and b^2
        form_y = form[0][0]

        center = tex('(', 'h', ',', 'k', ')', '=', '(', signed(h), ',', signed(k), ')',
                     size=ROW_SIZE).move_to([0, CENTER_Y, 0])
        for i in (1, 3, 7, 9):
            center[i].set_color(PT_COLOR)
        updown = tex('a', '=', r'\sqrt{' + str(p.a2) + '}', '=', str(a),
                     r'\text{ up and down}', size=ROW_SIZE).move_to([0, UPDOWN_ROW_Y, 0])
        across = tex('b', '=', r'\sqrt{' + str(p.b2) + '}', '=', str(b),
                     r'\text{ left and right}', size=ROW_SIZE).move_to([0, ACROSS_ROW_Y, 0])
        for row in (across, updown):
            row[0].set_color(P_COLOR)
            row[4].set_color(P_COLOR)
        transverse = tex(r'\text{transverse axis: }', r'\text{vertical}',
                         size=ROW_SIZE).move_to([0, TRANSVERSE_Y, 0])
        conjugate = tex(r'\text{conjugate axis: }', r'\text{horizontal}',
                        size=ROW_SIZE).move_to([0, CONJUGATE_Y, 0])
        transverse[1].set_color(P_COLOR)
        conjugate[1].set_color(P_COLOR)

        # ---- phase 2: the answer list, and the graph -----------------------------------------
        (vx1, vy1), (vx2, vy2) = p.vertices
        center_item = self.list_row('Center', '(', signed(h), ',', signed(k), ')',
                                    x=LEFT_X, y=LIST4[0])
        vertices_item = self.list_row('Vertices', '(', signed(vx1), ',', signed(vy1), ')',
                                      r'\text{ and }', '(', signed(vx2), ',', signed(vy2), ')',
                                      x=LEFT_X, y=LIST4[1])
        foci_item = self.list_row('Foci', '(', signed(h), ',', signed(k), r'\pm', two_root_two,
                                  ')', x=LEFT_X, y=LIST4[2])
        asymptote_item = self.list_row('Asymptotes', 'y', '+', str(-k), '=', r'\pm', '(', 'x', '+',
                                       str(-h), ')', x=LEFT_X, y=LIST4[3])

        plane = self.build_graph()

        def c2p(x, y):
            return plane.c2p(x, y)

        def dot(x, y, color):
            return Dot(c2p(x, y), color=color, radius=.09)

        def run(start, end, color=PAPER_GOLD):
            return Arrow(c2p(*start), c2p(*end), buff=0, color=color, stroke_width=5,
                         tip_length=.14, max_tip_length_to_length_ratio=.4)

        def branch(sign, t0, t1, width=5):
            return ParametricFunction(
                lambda t: c2p(h + b * math.sinh(t), k + sign * a * math.cosh(t)),
                t_range=[t0, t1], color=CURVE_COLOR, stroke_width=width)

        center_dot = dot(h, k, CURVE_COLOR)
        updown_arrows = VGroup(run((h, k), p.vertices[0]), run((h, k), p.vertices[1]))
        updown_labels = VGroup(*[tex(str(a), size=28, color=PAPER_GOLD).next_to(arrow, RIGHT,
                                                                                 buff=.08)
                                 for arrow in updown_arrows])
        vertex_dots = VGroup(dot(*p.vertices[0], CURVE_COLOR), dot(*p.vertices[1], CURVE_COLOR))
        across_arrows = VGroup(run((h, k), (h - b, k)), run((h, k), (h + b, k)))
        across_labels = VGroup(*[tex(str(b), size=28, color=PAPER_GOLD).next_to(arrow, UP, buff=.06)
                                 for arrow in across_arrows])
        side_dots = VGroup(dot(h - b, k, P_COLOR), dot(h + b, k, P_COLOR))
        transverse_line = DashedLine(c2p(h, GRAPH_Y[0]), c2p(h, GRAPH_Y[1]), color=PAPER_BLUE,
                                     stroke_width=4, dash_length=.12)
        conjugate_line = DashedLine(c2p(GRAPH_X[0], k), c2p(GRAPH_X[1], k), color=PAPER_BLUE,
                                    stroke_width=4, dash_length=.12)
        transverse_label = tex(r'\text{transverse axis}', size=24, color=PAPER_BLUE)
        transverse_label.move_to(c2p(h, k + 4.2) + RIGHT * (transverse_label.width / 2 + .1))
        conjugate_label = tex(r'\text{conjugate axis}', size=24, color=PAPER_BLUE).move_to(
            c2p(h + 4, k) + DOWN * .22)
        corners = [(h - b, k - a), (h + b, k - a), (h + b, k + a), (h - b, k + a)]
        box = VGroup(*[DashedLine(c2p(*corners[i]), c2p(*corners[(i + 1) % 4]), color=INK,
                                  stroke_width=3, dash_length=.1) for i in range(4)])
        asymptotes = VGroup(*[
            DashedLine(c2p(*p1), c2p(*p2), color=PAPER_BLUE, stroke_width=4, dash_length=.1)
            for sign in (1, -1)
            for p1, p2 in [asymptote_endpoints(h, k, b, a, sign, *GRAPH_X, *GRAPH_Y)]
        ])
        curve_up = branch(1, -t_end, t_end)
        curve_down = branch(-1, -t_end, t_end)

        # ---- 1. the problem ----------------------------------------------------------------
        self.say(f'Since both {v("y")} and {v("x")} are squared and we are subtracting, '
                 f'this is a hyperbola.')
        self.play(FadeIn(orig), run_time=1.2)
        self.play(Indicate(orig[0], color=PAPER_BLUE, scale_factor=1.3),
                  Indicate(orig[2], color=PAPER_BLUE, scale_factor=1.3),
                  Indicate(orig[1], color=PAPER_BLUE, scale_factor=1.6), run_time=1.1)
        self.beat('problem', READ_LONG)

        # ---- 2. divide by the number on the right so it equals 1 ----------------------------
        self.say(f'A hyperbola equals 1. So divide every term by {p.rhs}.')
        self.play(Indicate(orig[4], color=PT_COLOR, scale_factor=1.5), run_time=1.0)
        for bar, divisor in zip(bars, divisors):
            self.play(Create(bar), FadeIn(divisor, shift=DOWN * .15), run_time=.8)
        self.beat('divide', READ_LONG)

        self.say(f'{p.rhs} divided by {p.rhs} is 1, so the right side is now 1.')
        self.play(
            ReplacementTransform(orig[0], given[0][0]), ReplacementTransform(bars[0], given[0][1]),
            ReplacementTransform(divisors[0], given[0][2]), ReplacementTransform(orig[1], given[1]),
            ReplacementTransform(orig[2], given[2][0]), ReplacementTransform(bars[1], given[2][1]),
            ReplacementTransform(divisors[1], given[2][2]), ReplacementTransform(orig[3], given[3][0]),
            ReplacementTransform(VGroup(orig[4], bars[2], divisors[2]), given[3][1]),
            run_time=1.8)
        self.adopt(given, given[0][0], given[0][1], given[0][2], given[1], given[2][0],
                   given[2][1], given[2][2], given[3][0], given[3][1])
        self.beat('one', READ_LONG)

        # ---- 3. the formula: a^2 is under the first term ------------------------------------
        self.say(f'For hyperbolas, {v("a")} squared is always under the first term. '
                 f'In our problem, that is {v("y")}.')
        self.play(FadeIn(form), run_time=1.2)
        self.play(Indicate(form[0][2], color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.beat('form', READ_LONG)

        self.say(f'The variable in front tells us the direction. '
                 f'With {v("y")} in front, it opens up and down.')
        self.play(Indicate(form_y, color=PAPER_BLUE, scale_factor=1.3), run_time=1.1)
        self.beat('y-front', READ_LONG)

        # ---- 4. the center -----------------------------------------------------------------
        self.say(f'The center is ({v("h")}, {v("k")}). Think of {v("y")} + {-k} as {v("y")} '
                 f'minus negative {-k}, and {v("x")} + {-h} the same way.')
        self.play(ReplacementTransform(given, shown), run_time=1.4)
        self.play(Indicate(shown[0][0][3], color=PT_COLOR, scale_factor=1.6),
                  Indicate(shown[2][0][3], color=PT_COLOR, scale_factor=1.6), run_time=1.1)
        self.beat('negative', READ_LONG)

        self.say(f'The {v("h")} and {v("k")} are the numbers being subtracted. '
                 f'So the center is ({h}, {k}).')
        self.play(Indicate(form[0][0][3], color=PT_COLOR, scale_factor=1.6),
                  Indicate(form[2][0][3], color=PT_COLOR, scale_factor=1.6), run_time=1.1)
        self.play(FadeOut(form), FadeIn(center), run_time=1.2)
        self.beat('center', READ_LONG)

        # ---- 5. under each variable ---------------------------------------------------------
        self.say(f'The {p.a2} under {v("y")} gives {v("a")} = {a}. Go {a} up and {a} down.')
        self.play(Indicate(under_y, color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.play(FadeIn(updown), run_time=1.2)
        self.beat('updown', READ_LONG)

        self.say(f'The {p.b2} under {v("x")} gives {v("b")} = {b}. Go {b} left and {b} right.')
        self.play(Indicate(under_x, color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.play(FadeIn(across), run_time=1.2)
        self.beat('across', READ_LONG)

        # ---- 6. the vertices and the two axes -----------------------------------------------
        self.say(f'The vertices go with the variable in front. Here that is {v("y")}: '
                 f'{a} up and {a} down.')
        self.play(Indicate(shown[0][0], color=PAPER_BLUE, scale_factor=1.3),
                  Indicate(updown, color=P_COLOR, scale_factor=1.1), run_time=1.2)
        self.beat('front', READ_LONG)

        self.say('The line through the vertices is the transverse axis. Ours is vertical.')
        self.play(FadeIn(transverse), run_time=1.0)
        self.beat('transverse', READ_LONG)

        self.say('The conjugate axis crosses it at the center. So ours is horizontal.')
        self.play(FadeIn(conjugate), run_time=1.0)
        self.beat('conjugate', READ_LONG)

        # ---- 7. the graph: center, vertices, axes -------------------------------------------
        self.say('Now graph it. We will keep our answers in a list.')
        self.play(
            copy_into(center, center_item),
            FadeOut(VGroup(shown, center, across, updown, transverse, conjugate)),
            FadeIn(plane), run_time=1.8)
        self.beat('list', READ_LONG)

        self.say(f'Plot the center, ({h}, {k}).')
        self.play(FadeIn(center_dot, scale=1.6), run_time=1.0)
        self.beat('center-dot', READ_SHORT)

        self.say(f'Go {a} up and {a} down from the center.')
        self.play(*[Create(arrow) for arrow in updown_arrows], FadeIn(updown_labels), run_time=1.3)
        self.play(FadeIn(vertex_dots, scale=1.6), run_time=.8)
        self.beat('updown-dots', READ_LONG)

        self.say(f'{v("y")} is in front, so these two points are the vertices.')
        self.play(Write(vertices_item), run_time=1.2)
        self.beat('vertices', READ_LONG)

        self.say('The line through the vertices is the transverse axis.')
        self.play(FadeOut(VGroup(updown_arrows, updown_labels)), run_time=.5)
        self.play(Create(transverse_line), FadeIn(transverse_label), run_time=1.4)
        self.beat('transverse-axis', READ_LONG)

        self.say(f'Now go {b} left and {b} right from the center. '
                 f'The conjugate axis is the line through these points.')
        self.play(*[Create(arrow) for arrow in across_arrows], FadeIn(across_labels), run_time=1.3)
        self.play(FadeIn(side_dots, scale=1.6), run_time=.8)
        self.play(Create(conjugate_line), FadeIn(conjugate_label), run_time=1.2)
        self.beat('conjugate-axis', READ_LONG)

        # ---- 8. the box, the diagonals, the curves ------------------------------------------
        self.say('Draw a dashed box around these four points.')
        self.play(FadeOut(VGroup(across_arrows, across_labels, transverse_line, transverse_label,
                                 conjugate_line, conjugate_label)), run_time=.6)
        self.play(*[Create(edge) for edge in box], run_time=1.6)
        self.beat('box', READ_LONG)

        self.say('Draw dashed diagonals through opposite corners of the box, '
                 'and extend them past the box. Those are the asymptotes.')
        self.play(*[Create(line) for line in asymptotes], run_time=1.6)
        self.beat('diagonals', READ_LONG)

        self.say('Now draw each curve from a vertex. Use the asymptotes as a guide. '
                 'The curves approach them but never cross them.')
        self.play(Create(curve_up), Create(curve_down), run_time=2.8)
        self.beat('curve', READ_LONG)

        # ---- 9. finding c: the box's right triangle, on the full graph -----------------------
        unit = plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]   # screen length of one graph unit
        corner = (h + b, k - a)                          # lower right: the diagonal swings down
        theta = math.atan2(a, b)
        swing = math.pi / 2 - theta                      # how far the diagonal turns to reach the axis

        def seg(start, end, color, width=6):
            return Line(c2p(*start), c2p(*end), color=color, stroke_width=width)

        corner_dot = Dot(c2p(*corner), color=INK, radius=.06)
        focus_down, focus_up = dot(h, k - p.c, PAPER_GOLD), dot(h, k + p.c, PAPER_GOLD)
        leg_a = seg((h, k), (h, k - a), INK)
        leg_b = seg((h, k - a), corner, PT_COLOR)
        hyp = seg((h, k), corner, P_COLOR, width=5)
        swing_arc = DashedVMobject(
            Arc(radius=p.c * unit, start_angle=-theta, angle=-swing, arc_center=c2p(h, k),
                color=PAPER_GOLD, stroke_width=5), num_dashes=24)
        lab_a = tex(str(a), size=28).move_to(c2p(h, k - a / 2) + LEFT * .25)
        lab_b = tex(str(b), size=28, color=PT_COLOR).move_to(c2p(h + b / 2, k - a) + UP * .2)   # above the leg: the curve runs just below it
        lab_c = tex('c', size=28, color=P_COLOR).move_to(
            c2p(h + b / 2, k - a / 2) + np.array([.22, .18, 0]))

        # Rows above the graph, where the answer list was; each is built once at its final spot.
        pyth = tex('a^2', '+', 'b^2', '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        plug = tex(str(p.a2), '+', str(p.b2), '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        total = tex(str(p.c2), '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        root = tex('c', '=', r'\sqrt{' + str(p.c2) + '}', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        simple = tex('c', '=', two_root_two, size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        pyth[2].set_color(PT_COLOR)
        pyth[4].set_color(P_COLOR)
        plug[2].set_color(PT_COLOR)
        plug[4].set_color(P_COLOR)
        total[2].set_color(P_COLOR)
        for row in (root, simple):
            row[0].set_color(P_COLOR)
            row[2].set_color(P_COLOR)
        vertices_row = tex(r'\text{vertices: }', '(', signed(h), ',', signed(k), r'\pm', str(a), ')',
                           size=ROW_SIZE).move_to([0, VERTICES_Y, 0])
        foci_row = tex(r'\text{foci: }', '(', signed(h), ',', signed(k), r'\pm', two_root_two, ')',
                       size=ROW_SIZE).move_to([0, FOCI_Y, 0])
        vertices_row[6].set_color(PT_COLOR)
        foci_row[6].set_color(P_COLOR)

        self.say(f'To find the foci, we need {v("c")}: the distance from the center to each focus.')
        self.play(FadeOut(VGroup(center_item, vertices_item)), run_time=1.0)
        self.beat('clear', READ_LONG)

        self.say(f'From the center to the vertex is {a}. That is {v("a")}.')
        self.play(Create(leg_a), FadeIn(lab_a), run_time=1.1)
        self.beat('leg-a', READ_SHORT)

        self.say(f'From the vertex over to the box corner is {b}. That is {v("b")}.')
        self.play(Create(leg_b), FadeIn(lab_b), FadeIn(corner_dot), run_time=1.1)
        self.beat('leg-b', READ_SHORT)

        self.say(f'The diagonal across the box closes a right triangle. Its longest side is {v("c")}.')
        self.play(Create(hyp), FadeIn(lab_c), run_time=1.3)
        self.beat('hyp', READ_LONG)

        self.say(f'Same as before: {v("a")} squared plus {v("b")} squared equals {v("c")} squared.')
        self.play(FadeIn(pyth), run_time=1.2)
        self.beat('pyth', READ_LONG)

        self.say(f'{v("a")} squared and {v("b")} squared are the numbers under {v("y")} '
                 f'and {v("x")}: {p.a2} and {p.b2}.')
        self.play(ReplacementTransform(pyth, plug), run_time=1.3)
        self.beat('plug', READ_LONG)

        self.say(f'{p.a2} plus {p.b2} is {p.c2}.')
        self.play(ReplacementTransform(plug, total), run_time=1.3)
        self.beat('total', READ_SHORT)

        self.say(f'Take the square root.')
        self.play(ReplacementTransform(total, root), run_time=1.3)
        self.beat('c-value', READ_SHORT)

        self.say(f'Simplify it: {p.c2} is 4 times 2, so {v("c")} is 2 times the square root of 2.')
        self.play(ReplacementTransform(root, simple), run_time=1.3)
        self.beat('c-simple', READ_LONG)

        # ---- 10. lay c along the transverse axis -----------------------------------------------
        # The blue diagonal is exactly c long. Pivoting a copy about the center keeps its length,
        # so wherever it lands on the axis is c from the center: that is the focus.
        pivot = hyp.copy()
        lab_c_axis = tex('c', size=28, color=P_COLOR).move_to(c2p(h, k - p.c * .85) + LEFT * .22)

        self.say(f'Now measure {v("c")} along the transverse axis. '
                 f'Pivot the diagonal down like a clock hand.')
        self.play(Create(transverse_line), run_time=1.0)
        self.play(Rotate(pivot, angle=-swing, about_point=c2p(h, k), rate_func=linear),
                  Create(swing_arc, rate_func=linear), run_time=2.2)
        self.play(FadeIn(lab_c_axis), FadeIn(focus_down, scale=1.6), run_time=.8)
        self.beat('swing', READ_LONG)

        self.say(f'The diagonal keeps its length, so its end is {v("c")} '
                 f'from the center. That point is a focus.')
        self.play(Indicate(focus_down, color=PAPER_BLUE, scale_factor=1.6), run_time=1.1)
        self.beat('focus', READ_LONG)

        # ---- 11. c follows the vertices ------------------------------------------------------
        self.say(f'{v("c")} always goes the same way as the vertices. '
                 f'These go up and down from the center.')
        self.play(FadeIn(vertices_row), run_time=1.2)
        self.play(Indicate(vertex_dots, color=PAPER_BLUE, scale_factor=1.5), run_time=1.1)
        self.beat('follows', READ_LONG)

        self.say(f'So the other focus is {v("c")} above the center.')
        self.play(FadeIn(foci_row), FadeIn(focus_up, scale=1.6), run_time=1.3)
        self.beat('foci', READ_LONG)

        # ---- 12. the asymptotes ---------------------------------------------------------------
        up_leg = seg((h, k), (h, k + a), PT_COLOR)
        over_leg = seg((h, k + a), (h + b, k + a), INK)
        up_label = tex(str(a), size=28, color=PT_COLOR).move_to(c2p(h, k + a / 2) + LEFT * .25)
        over_label = tex(str(b), size=28).move_to(c2p(h + b / 2, k + a) + UP * .2)
        slope_row = tex('m', '=', r'\pm', slope_tex, size=ROW_SIZE).move_to([0, SLOPE_Y, 0])
        slope_one = tex('m', '=', r'\pm', str(int(p.slope)), size=ROW_SIZE).move_to(
            [0, SLOPE_Y, 0])
        point_slope = tex('y', '-', 'k', '=', 'm', '(', 'x', '-', 'h', ')',
                          size=ROW_SIZE).move_to([0, POINT_SLOPE_Y, 0])
        point_slope[2].set_color(PT_COLOR)
        point_slope[8].set_color(PT_COLOR)
        plugged = tex('y', '-', k_raw, '=', r'\pm', str(int(p.slope)), '(', 'x', '-', h_raw, ')',
                      size=ROW_SIZE).move_to([0, POINT_SLOPE_Y, 0])
        plugged[2].set_color(PT_COLOR)
        plugged[9].set_color(PT_COLOR)
        tidy = tex('y', '+', str(-k), '=', r'\pm', '(', 'x', '+', str(-h), ')',
                   size=ROW_SIZE).move_to([0, POINT_SLOPE_Y, 0])
        tidy[2].set_color(PT_COLOR)
        tidy[8].set_color(PT_COLOR)

        self.say('Now the asymptotes. Start at the center. Go up, and then over, to reach the diagonal.')
        self.play(FadeOut(VGroup(root, simple, vertices_row, foci_row, swing_arc, transverse_line,
                                 pivot, lab_c_axis, leg_a, leg_b, hyp, lab_a, lab_b, lab_c)),
                  run_time=.8)
        self.play(Create(up_leg), FadeIn(up_label), run_time=1.0)
        self.play(Create(over_leg), FadeIn(over_label), run_time=1.0)
        self.beat('up-over', READ_LONG)

        self.say(f'The slope is up over over: {a} over {b}.')
        self.play(FadeIn(slope_row), run_time=1.2)
        self.beat('slope', READ_LONG)

        self.say(f'{a} over {b} is {int(p.slope)}. It is plus or minus, '
                 f'because the other diagonal slopes down.')
        self.play(ReplacementTransform(slope_row, slope_one), run_time=1.3)
        self.beat('slope-one', READ_LONG)

        self.say('Now use point-slope form, with the center as the point.')
        self.play(FadeIn(point_slope), run_time=1.2)
        self.beat('point-slope', READ_LONG)

        self.say(f'Plug in the center, ({h}, {k}), and the slope.')
        self.play(FadeOut(VGroup(up_leg, over_leg, up_label, over_label)), run_time=.6)
        self.play(ReplacementTransform(point_slope, plugged), run_time=1.3)
        self.beat('plugged', READ_LONG)

        self.say('Subtracting a negative is adding, and multiplying by 1 changes nothing.')
        self.play(ReplacementTransform(plugged, tidy), run_time=1.4)
        self.play(Indicate(tidy[1], color=PT_COLOR, scale_factor=1.6),
                  Indicate(tidy[7], color=PT_COLOR, scale_factor=1.6), run_time=1.0)
        self.beat('tidy', READ_LONG)

        # ---- 13. everything back together ---------------------------------------------------
        self.say('Now put all the answers together.')
        self.play(
            FadeOut(slope_one),
            copy_into(tidy, asymptote_item),
            FadeOut(tidy),
            FadeIn(VGroup(center_item, vertices_item)),
            run_time=1.8)
        self.play(Write(foci_item), run_time=1.2)
        self.beat('all', READ_LONG)

        self.say('Center, vertices, foci, and asymptotes. Every answer is on the graph.')
        self.play(Indicate(asymptote_item, color=PAPER_BLUE, scale_factor=1.12), run_time=1.3)
        self.beat('hold', READ_LONG)
        self.write_marks(self.problem.marks_file)
