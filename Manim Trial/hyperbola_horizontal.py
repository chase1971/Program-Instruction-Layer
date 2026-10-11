"""Hyperbolas (pre-calc conics): worksheet problem 1, (x-1)^2/25 - y^2/49 = 1, opens left and right.

Mirrors ellipse_horizontal.py, but stresses what is different. For a hyperbola a^2 is always under
the FIRST term, whichever variable that is, so the variables can swap places (shown on the
formula) and the variable in front says which way the curve opens and where the vertices are. The
number under x still goes left and right and the number under y up and down. The line through the
vertices is the transverse axis; the conjugate axis crosses it at the center.

Graphing is Chase's way: plot the center and the vertices, go b up and down, draw a dashed box,
draw the dashed diagonals (the asymptotes), then the curves between them. c comes from the box's
right triangle (a, b, c) with a^2 + b^2 = c^2, the plus where the ellipse has a minus. The
asymptotes use the center in point-slope form with the slope +/- b/a (up b, over a).

Verified (HyperbolaProblem.__post_init__ re-checks it with Fraction):
    center (1, 0); 25 under x -> a = 5; 49 under y -> b = 7; x in front: horizontal transverse axis
    vertices (-4, 0) and (6, 0); box corners (-4, +/-7) and (6, +/-7); slope +/- 7/5
    c^2 = 25 + 49 = 74; foci (1 +/- sqrt(74), 0)
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
    Rotate,
    linear,
    NumberPlane,
    ParametricFunction,
    ReplacementTransform,
    Swap,
    VGroup,
    Write,
)

from ellipse_horizontal import ellipse_row  # noqa: E402
from equations_of_lines import READ_LONG, READ_SHORT, signed, tex, var  # noqa: E402
from parabola_walkthrough import (  # noqa: E402
    CURVE_COLOR,
    LEFT_X,
    MATH_SIZE,
    P_COLOR,
    PT_COLOR,
    ParabolaOpensUp,
)
from scene_style import PAPER_BLUE, PAPER_GOLD, PAPER_INK, PAPER_MUTED  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

INK = PAPER_INK
GRAPH_X, GRAPH_Y = (-10, 14), (-10, 10)   # wide enough to show asymptotes past the box and long branches
GRAPH_W = 5.4                             # same on-screen size; wider range = drawn zoomed out
GRAPH_CENTER_Y = -1.42                 # the grid hangs just under the four-row answer list

# Phase 1 row centres (the caption owns y > 2.95; the stacked fractions need the extra room).
HYPERBOLA_Y, CENTER_Y = 1.95, 0.55
ACROSS_Y, UPDOWN_Y, TRANSVERSE_Y, CONJUGATE_Y = -0.4, -1.2, -2.1, -2.9
ROW_SIZE = 44
FORM_ROW_Y = 0.4
LIST4 = (2.55, 2.1, 1.65, 1.05)   # center, vertices, foci, asymptotes
# Part 2 stays on the full graph; the algebra rows take the place of the answer list above it.
FORMULA_Y, VERTICES_Y, FOCI_Y = 2.35, 1.75, 1.15
SLOPE_Y, POINT_SLOPE_Y = 2.4, 1.35


@dataclass
class HyperbolaProblem:
    """(x - h)^2 / a2 - (y - k)^2 / b2 = 1: a hyperbola that opens left and right, k = 0.

    a2 and b2 are perfect squares so the graph can count whole steps, and a, b share no factor so
    the slope b/a needs no simplifying beat.
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
        if self.k != 0 or self.h <= 0:
            raise ValueError('Built for k = 0 and a positive h: the y beat shows y - 0.')
        if math.gcd(self.a, self.b) != 1:
            raise ValueError('The slope b/a must already be in lowest terms.')
        self.vertices = ((self.h - self.a, self.k), (self.h + self.a, self.k))
        self.slope = Fraction(self.b, self.a)
        self.c2 = self.a2 + self.b2          # a^2 + b^2 = c^2, left exact: c = sqrt(c2)
        self.c = math.sqrt(self.c2)
        for x, y in self.vertices:           # both vertices sit on the hyperbola
            if Fraction((x - self.h) ** 2, self.a2) - Fraction((y - self.k) ** 2, self.b2) != 1:
                raise ValueError('A vertex is not on the hyperbola.')
        # The box corner (h + a, k + b) lies on the asymptote y - k = (b/a)(x - h).
        if self.slope * self.a != self.b:
            raise ValueError('The box corner is not on the asymptote.')


PROBLEM = HyperbolaProblem(h=1, k=0, a2=25, b2=49, marks_file='hyperbola_horizontal_marks.json')


def v(letter):
    """A variable in a caption."""
    return var(letter, PAPER_BLUE)


def branch_t_limit(h, k, a, b, x_lo, x_hi, y_lo, y_hi):
    """Largest t so both hyperbola branches stay inside the graph window."""
    limits = []
    if x_hi > h + a:
        limits.append(math.acosh((x_hi - h) / a))
    if x_lo < h - a:
        limits.append(math.acosh((h - x_lo) / a))
    if y_hi > k:
        limits.append(math.asinh((y_hi - k) / b))
    if y_lo < k:
        limits.append(math.asinh((k - y_lo) / b))
    return min(limits)


def asymptote_endpoints(h, k, a, b, slope_sign, x_lo, x_hi, y_lo, y_hi):
    """Two corners of the graph window where the line y - k = slope_sign * (b/a)(x - h) crosses."""
    m = slope_sign * b / a
    pts = []
    for x in (x_lo, x_hi):
        y = k + m * (x - h)
        if y_lo <= y <= y_hi:
            pts.append((x, y))
    if m:
        for y in (y_lo, y_hi):
            x = h + (y - k) / m
            if x_lo <= x <= x_hi:
                pts.append((x, y))
    uniq = []
    for p in pts:
        if not any(abs(p[0] - q[0]) < 0.05 and abs(p[1] - q[1]) < 0.05 for q in uniq):
            uniq.append(p)
    if len(uniq) < 2:
        raise ValueError('Asymptote does not cross the graph window twice.')
    best = (uniq[0], uniq[1])
    best_d = 0.0
    for i, p in enumerate(uniq):
        for q in uniq[i + 1:]:
            d = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
            if d > best_d:
                best_d = d
                best = (p, q)
    return best


class HyperbolaHorizontal(ParabolaOpensUp):
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

    def construct(self):
        p = self.problem
        h, k, a, b = p.h, p.k, p.a, p.b
        slope = rf'\frac{{{p.slope.numerator}}}{{{p.slope.denominator}}}'
        t_end = branch_t_limit(h, k, a, b, *GRAPH_X, *GRAPH_Y)

        # ---- phase 1 rows, each built once at its final spot ---------------------------------
        given = ellipse_row(['(', 'x', '-', str(h), ')^2'], ['y^2'], str(p.a2), str(p.b2),
                            MATH_SIZE - 6, op='-')
        shown = ellipse_row(['(', 'x', '-', str(h), ')^2'], ['(', 'y', '-', str(k), ')^2'],
                            str(p.a2), str(p.b2), MATH_SIZE - 6, op='-')
        fit = min(1, 6.1 / shown.width)
        for row in (given, shown):
            row.scale(fit).move_to([0, HYPERBOLA_Y, 0])
        shown[0][0][3].set_color(PT_COLOR)     # the 1 in (x - 1)
        shown[2][0][3].set_color(PT_COLOR)     # the 0 in (y - 0)
        given[0][0][3].set_color(PT_COLOR)
        under_x = shown[0][2]
        form = ellipse_row(['(', 'x', '-', 'h', ')^2'], ['(', 'y', '-', 'k', ')^2'],
                           'a^2', 'b^2', ROW_SIZE, op='-').move_to([0, FORM_ROW_Y, 0])
        for piece in (form[0][0][3], form[2][0][3]):
            piece.set_color(PT_COLOR)        # h and k
        for piece in (form[0][2][0], form[2][2][0]):
            piece.set_color(P_COLOR)         # a^2 and b^2
        form_x, form_y = form[0][0], form[2][0]   # the two numerators swap places

        center = tex('(', 'h', ',', 'k', ')', '=', '(', str(h), ',', str(k), ')',
                     size=ROW_SIZE).move_to([0, CENTER_Y, 0])
        for i in (1, 3, 7, 9):
            center[i].set_color(PT_COLOR)
        across = tex('a', '=', r'\sqrt{' + str(p.a2) + '}', '=', str(a),
                     r'\text{ left and right}', size=ROW_SIZE).move_to([0, ACROSS_Y, 0])
        updown = tex('b', '=', r'\sqrt{' + str(p.b2) + '}', '=', str(b),
                     r'\text{ up and down}', size=ROW_SIZE).move_to([0, UPDOWN_Y, 0])
        for row in (across, updown):
            row[0].set_color(P_COLOR)
            row[4].set_color(P_COLOR)
        transverse = tex(r'\text{transverse axis: }', r'\text{horizontal}',
                         size=ROW_SIZE).move_to([0, TRANSVERSE_Y, 0])
        conjugate = tex(r'\text{conjugate axis: }', r'\text{vertical}',
                        size=ROW_SIZE).move_to([0, CONJUGATE_Y, 0])
        transverse[1].set_color(P_COLOR)
        conjugate[1].set_color(P_COLOR)

        # ---- phase 2: the answer list, and the graph -----------------------------------------
        (vx1, vy1), (vx2, vy2) = p.vertices
        center_item = self.list_row('Center', '(', str(h), ',', str(k), ')',
                                    x=LEFT_X, y=LIST4[0])
        vertices_item = self.list_row('Vertices', '(', signed(vx1), ',', signed(vy1), ')',
                                      r'\text{ and }', '(', signed(vx2), ',', signed(vy2), ')',
                                      x=LEFT_X, y=LIST4[1])
        foci_item = self.list_row('Foci', '(', str(h), r'\pm', r'\sqrt{' + str(p.c2) + '}', ',',
                                  str(k), ')', x=LEFT_X, y=LIST4[2])
        asymptote_item = self.list_row('Asymptotes', 'y', '-', str(k), '=', r'\pm', slope,
                                       '(', 'x', '-', str(h), ')', x=LEFT_X, y=LIST4[3])

        plane = self.build_graph()

        def c2p(x, y):
            return plane.c2p(x, y)

        def dot(x, y, color):
            return Dot(c2p(x, y), color=color, radius=.09)

        def run(start, end, color=PAPER_GOLD):
            return Arrow(c2p(*start), c2p(*end), buff=0, color=color, stroke_width=5,
                         tip_length=.14, max_tip_length_to_length_ratio=.4)

        def branch(sign, to_point, t0, t1, width=5):
            return ParametricFunction(
                lambda t: to_point(h + sign * a * math.cosh(t), k + b * math.sinh(t)),
                t_range=[t0, t1], color=CURVE_COLOR, stroke_width=width)

        center_dot = dot(h, k, CURVE_COLOR)
        across_arrows = VGroup(run((h, k), p.vertices[0]), run((h, k), p.vertices[1]))
        across_labels = VGroup(*[tex(str(a), size=28, color=PAPER_GOLD).next_to(arrow, UP, buff=.06)
                                 for arrow in across_arrows])
        vertex_left, vertex_right = dot(*p.vertices[0], CURVE_COLOR), dot(*p.vertices[1], CURVE_COLOR)
        vertex_dots = VGroup(vertex_left, vertex_right)
        updown_arrows = VGroup(run((h, k), (h, k - b)), run((h, k), (h, k + b)))
        updown_labels = VGroup(*[tex(str(b), size=28, color=PAPER_GOLD).next_to(arrow, RIGHT,
                                                                                 buff=.08)
                                 for arrow in updown_arrows])
        top_dot, bottom_dot = dot(h, k + b, P_COLOR), dot(h, k - b, P_COLOR)
        transverse_line = DashedLine(c2p(GRAPH_X[0], k), c2p(GRAPH_X[1], k), color=PAPER_BLUE,
                                     stroke_width=4, dash_length=.12)
        conjugate_line = DashedLine(c2p(h, GRAPH_Y[0]), c2p(h, GRAPH_Y[1]), color=PAPER_BLUE,
                                    stroke_width=4, dash_length=.12)
        transverse_label = tex(r'\text{transverse axis}', size=24, color=PAPER_BLUE).move_to(
            c2p(h + 8, k) + DOWN * .22)
        conjugate_label = tex(r'\text{conjugate axis}', size=24, color=PAPER_BLUE)
        conjugate_label.move_to(c2p(h, k + 7.5) + RIGHT * (conjugate_label.width / 2 + .1))
        corners = [(h - a, k - b), (h + a, k - b), (h + a, k + b), (h - a, k + b)]
        box = VGroup(*[DashedLine(c2p(*corners[i]), c2p(*corners[(i + 1) % 4]), color=INK,
                                  stroke_width=3, dash_length=.1) for i in range(4)])
        asymptotes = VGroup(*[
            DashedLine(c2p(*p1), c2p(*p2), color=PAPER_BLUE, stroke_width=4, dash_length=.1)
            for sign in (1, -1)
            for p1, p2 in [asymptote_endpoints(h, k, a, b, sign, *GRAPH_X, *GRAPH_Y)]
        ])
        curve_right = branch(1, c2p, -t_end, t_end)
        curve_left = branch(-1, c2p, -t_end, t_end)
        curves = VGroup(curve_left, curve_right)

        # ---- 1. the problem ----------------------------------------------------------------
        self.say(f'Since both {v("x")} and {v("y")} are squared and we are subtracting, '
                 f'this is a hyperbola.')
        self.play(FadeIn(given), run_time=1.2)
        self.play(Indicate(given[0][0], color=PAPER_BLUE, scale_factor=1.3),
                  Indicate(given[2][0], color=PAPER_BLUE, scale_factor=1.3),
                  Indicate(given[1], color=PAPER_BLUE, scale_factor=1.6), run_time=1.1)
        self.beat('problem', READ_LONG)

        # ---- 2. the formula: a^2 is under the first term ------------------------------------
        self.say(f'For hyperbolas, {v("a")} squared is always under the first term. '
                 f'In our problem, that is {v("x")}.')
        self.play(FadeIn(form), run_time=1.2)
        self.play(Indicate(form[0][2], color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.beat('form', READ_LONG)

        self.say(f'The variables can swap places, but {v("a")} squared stays under the first term. '
                 f'Only {v("x")} and {v("y")} move.')
        self.play(Swap(form_x, form_y), run_time=1.8)
        self.play(Indicate(form[0][2], color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.beat('swap', READ_LONG)

        self.say(f'The variable in front tells us the direction. '
                 f'With {v("y")} in front, it opens up and down.')
        self.play(Indicate(form_y, color=PAPER_BLUE, scale_factor=1.3), run_time=1.1)
        self.beat('y-front', READ_LONG)

        self.say(f'Our problem has {v("x")} in front, so it opens left and right.')
        self.play(Swap(form_x, form_y), run_time=1.8)
        self.play(Indicate(form_x, color=PAPER_BLUE, scale_factor=1.3), run_time=1.1)
        self.beat('x-front', READ_LONG)

        # ---- 3. the center -----------------------------------------------------------------
        self.say(f'The center is ({v("h")}, {v("k")}). Think of {v("y")} squared as '
                 f'{v("y")} minus 0, squared.')
        self.play(ReplacementTransform(given, shown), run_time=1.4)
        self.play(Indicate(shown[2][0][3], color=PT_COLOR, scale_factor=1.6), run_time=1.1)
        self.beat('zero', READ_LONG)

        self.say(f'The {v("h")} and {v("k")} are the numbers being subtracted. '
                 f'So the center is ({h}, {k}).')
        self.play(Indicate(form[0][0][3], color=PT_COLOR, scale_factor=1.6),
                  Indicate(form[2][0][3], color=PT_COLOR, scale_factor=1.6), run_time=1.1)
        self.play(FadeOut(form), FadeIn(center), run_time=1.2)
        self.beat('center', READ_LONG)

        # ---- 4. under each variable ---------------------------------------------------------
        self.say(f'The {p.a2} is under {v("x")}, so take its square root: '
                 f'{v("a")} = {a}. Go {a} left and {a} right.')
        self.play(Indicate(under_x, color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.play(FadeIn(across), run_time=1.2)
        self.beat('across', READ_LONG)

        self.say(f'The {p.b2} is under {v("y")}, so {v("b")} = {b}. Go {b} up and {b} down.')
        self.play(Indicate(shown[2][2], color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.play(FadeIn(updown), run_time=1.2)
        self.beat('updown', READ_LONG)

        # ---- 5. the vertices and the two axes -----------------------------------------------
        self.say(f'The vertices go with the variable in front. Here that is {v("x")}: '
                 f'{a} left and {a} right.')
        self.play(Indicate(shown[0][0], color=PAPER_BLUE, scale_factor=1.3),
                  Indicate(across, color=P_COLOR, scale_factor=1.1), run_time=1.2)
        self.beat('front', READ_LONG)

        self.say('The line through the vertices is the transverse axis. Ours is horizontal.')
        self.play(FadeIn(transverse), run_time=1.0)
        self.beat('transverse', READ_LONG)

        self.say('The conjugate axis crosses it at the center. So ours is vertical.')
        self.play(FadeIn(conjugate), run_time=1.0)
        self.beat('conjugate', READ_LONG)

        # ---- 6. the graph: center, vertices, axes ------------------------------------------------
        self.say('Now graph it. We will keep our answers in a list.')
        self.play(
            copy_into(center, center_item),
            FadeOut(VGroup(shown, center, across, updown, transverse, conjugate)),
            FadeIn(plane), run_time=1.8)
        self.beat('list', READ_LONG)

        self.say(f'Plot the center, ({h}, {k}).')
        self.play(FadeIn(center_dot, scale=1.6), run_time=1.0)
        self.beat('center-dot', READ_SHORT)

        self.say(f'Go {a} left and {a} right from the center.')
        self.play(*[Create(arrow) for arrow in across_arrows], FadeIn(across_labels), run_time=1.3)
        self.play(FadeIn(vertex_dots, scale=1.6), run_time=.8)
        self.beat('across-dots', READ_LONG)

        self.say(f'{v("x")} is in front, so these two points are the vertices.')
        self.play(Write(vertices_item), run_time=1.2)
        self.beat('vertices', READ_LONG)

        self.say('The line through the vertices is the transverse axis.')
        self.play(FadeOut(VGroup(across_arrows, across_labels)), run_time=.5)
        self.play(Create(transverse_line), FadeIn(transverse_label), run_time=1.4)
        self.beat('transverse-axis', READ_LONG)

        self.say(f'Now go {b} up and {b} down from the center. '
                 f'The conjugate axis is the line through these points.')
        self.play(*[Create(arrow) for arrow in updown_arrows], FadeIn(updown_labels), run_time=1.3)
        self.play(FadeIn(VGroup(top_dot, bottom_dot), scale=1.6), run_time=.8)
        self.play(Create(conjugate_line), FadeIn(conjugate_label), run_time=1.2)
        self.beat('conjugate-axis', READ_LONG)

        # ---- 7. the box, the diagonals, the curves -----------------------------------------
        self.say('Draw a dashed box around these four points.')
        self.play(FadeOut(VGroup(updown_arrows, updown_labels, transverse_line, transverse_label,
                                 conjugate_line, conjugate_label)), run_time=.6)
        self.play(*[Create(edge) for edge in box], run_time=1.6)
        self.beat('box', READ_LONG)

        self.say('Draw dashed diagonals through opposite corners of the box, '
                 'and extend them past the box. Those are the asymptotes.')
        self.play(*[Create(line) for line in asymptotes], run_time=1.6)
        self.beat('diagonals', READ_LONG)

        self.say('Now draw each curve from a vertex. Use the asymptotes as a guide. '
                 'The curves approach them but never cross them.')
        self.play(Create(curve_left), Create(curve_right), run_time=2.8)
        self.beat('curve', READ_LONG)

        # ---- 8. finding c: the box's right triangle, on the full graph -----------------------
        unit = plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]   # screen length of one graph unit
        corner = (h + a, k + b)
        theta = math.atan2(b, a)

        def seg(start, end, color, width=6):
            return Line(c2p(*start), c2p(*end), color=color, stroke_width=width)

        def swing_arc(start_angle, angle):
            return DashedVMobject(
                Arc(radius=p.c * unit, start_angle=start_angle, angle=angle,
                    arc_center=c2p(h, k), color=PAPER_GOLD, stroke_width=5), num_dashes=24)

        corner_dot = Dot(c2p(*corner), color=INK, radius=.06)
        focus_right, focus_left = dot(h + p.c, k, PAPER_GOLD), dot(h - p.c, k, PAPER_GOLD)
        leg_a = seg((h, k), (h + a, k), INK)
        leg_b = seg((h + a, k), corner, PT_COLOR)
        hyp = seg((h, k), corner, P_COLOR, width=5)
        swing_right = swing_arc(theta, -theta)
        lab_a = tex(str(a), size=28).move_to(c2p(h + a / 2, k) + DOWN * .2)
        lab_b = tex(str(b), size=28, color=PT_COLOR).move_to(c2p(h + a, k + b / 2) + LEFT * .25)
        lab_c = tex('c', size=28, color=P_COLOR).move_to(c2p(h + a / 2, k + b / 2) + np.array([-.22, .18, 0]))

        # Rows above the graph, where the answer list was; each is built once at its final spot.
        pyth = tex('a^2', '+', 'b^2', '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        plug = tex(str(p.a2), '+', str(p.b2), '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        total = tex(str(p.c2), '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        root = tex('c', '=', r'\sqrt{' + str(p.c2) + '}', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        pyth[2].set_color(PT_COLOR)
        pyth[4].set_color(P_COLOR)
        plug[2].set_color(PT_COLOR)
        plug[4].set_color(P_COLOR)
        total[2].set_color(P_COLOR)
        root[0].set_color(P_COLOR)
        root[2].set_color(P_COLOR)
        vertices_row = tex(r'\text{vertices: }', '(', str(h), r'\pm', str(a), ',', str(k), ')',
                           size=ROW_SIZE).move_to([0, VERTICES_Y, 0])
        foci_row = tex(r'\text{foci: }', '(', str(h), r'\pm', r'\sqrt{' + str(p.c2) + '}', ',',
                       str(k), ')', size=ROW_SIZE).move_to([0, FOCI_Y, 0])
        foci_row[4].set_color(P_COLOR)

        self.say(f'To find the foci, we need {v("c")}: the distance from the center to each focus.')
        self.play(FadeOut(VGroup(center_item, vertices_item)), run_time=1.0)
        self.beat('clear', READ_LONG)

        self.say(f'From the center to the vertex is {a}. That is {v("a")}.')
        self.play(Create(leg_a), FadeIn(lab_a), run_time=1.1)
        self.beat('leg-a', READ_SHORT)

        self.say(f'From the vertex up to the box corner is {b}. That is {v("b")}.')
        self.play(Create(leg_b), FadeIn(lab_b), FadeIn(corner_dot), run_time=1.1)
        self.beat('leg-b', READ_SHORT)

        self.say(f'The diagonal across the box closes a right triangle. Its longest side is {v("c")}.')
        self.play(Create(hyp), FadeIn(lab_c), run_time=1.3)
        self.beat('hyp', READ_LONG)

        self.say(f'Same as the ellipse, except this time it is plus: '
                 f'{v("a")} squared plus {v("b")} squared equals {v("c")} squared.')
        self.play(FadeIn(pyth), run_time=1.2)
        self.beat('pyth', READ_LONG)

        self.say(f'{v("a")} squared and {v("b")} squared are the numbers under {v("x")} '
                 f'and {v("y")}: {p.a2} and {p.b2}.')
        self.play(ReplacementTransform(pyth, plug), run_time=1.3)
        self.beat('plug', READ_LONG)

        self.say(f'{p.a2} plus {p.b2} is {p.c2}.')
        self.play(ReplacementTransform(plug, total), run_time=1.3)
        self.beat('total', READ_SHORT)

        self.say(f'Take the square root. Leave {v("c")} as an exact value.')
        self.play(ReplacementTransform(total, root), run_time=1.3)
        self.beat('c-value', READ_LONG)

        # ---- 9. lay c along the transverse axis -------------------------------------------------
        # The blue diagonal is exactly c long. Pivoting a copy about the center keeps its length,
        # so wherever it lands on the axis is c from the center: that is the focus.
        pivot_right = hyp.copy()
        lab_c_axis = tex('c', size=28, color=P_COLOR).move_to(c2p(h + p.c * .85, k) + DOWN * .2)

        self.say(f'Now measure {v("c")} along the transverse axis. '
                 f'Pivot the diagonal down like a clock hand.')
        self.play(Create(transverse_line), run_time=1.0)
        self.play(Rotate(pivot_right, angle=-theta, about_point=c2p(h, k), rate_func=linear),
                  Create(swing_right, rate_func=linear), run_time=2.2)
        self.play(FadeIn(lab_c_axis), FadeIn(focus_right, scale=1.6), run_time=.8)
        self.beat('swing', READ_LONG)

        self.say(f'The diagonal keeps its length, so its end is {v("c")} '
                 f'from the center. That point is a focus.')
        self.play(Indicate(focus_right, color=PAPER_BLUE, scale_factor=1.6), run_time=1.1)
        self.beat('focus', READ_LONG)

        # ---- 10. c follows the vertices ------------------------------------------------------
        self.say(f'{v("c")} always goes the same way as the vertices. '
                 f'These go left and right from the center.')
        self.play(FadeIn(vertices_row), run_time=1.2)
        self.play(Indicate(vertex_left, color=PAPER_BLUE, scale_factor=1.5),
                  Indicate(vertex_right, color=PAPER_BLUE, scale_factor=1.5), run_time=1.1)
        self.beat('follows', READ_LONG)

        self.say(f'So the other focus is {v("c")} to the left of the center.')
        self.play(FadeIn(foci_row), run_time=1.2)
        self.play(FadeIn(focus_left, scale=1.6), run_time=.8)
        self.beat('foci', READ_LONG)

        # ---- 10. the asymptotes ---------------------------------------------------------------
        up_leg = seg((h, k), (h, k + b), PT_COLOR)
        over_leg = seg((h, k + b), corner, INK)
        up_label = tex(str(b), size=28, color=PT_COLOR).move_to(c2p(h, k + b / 2) + LEFT * .25)
        over_label = tex(str(a), size=28).move_to(c2p(h + a / 2, k + b) + UP * .2)
        slope_row = tex('m', '=', r'\pm', slope, size=ROW_SIZE).move_to([0, SLOPE_Y, 0])
        point_slope = tex('y', '-', 'k', '=', 'm', '(', 'x', '-', 'h', ')',
                          size=ROW_SIZE).move_to([0, POINT_SLOPE_Y, 0])
        point_slope[2].set_color(PT_COLOR)
        point_slope[8].set_color(PT_COLOR)
        plugged = tex('y', '-', str(k), '=', r'\pm', slope, '(', 'x', '-', str(h), ')',
                      size=ROW_SIZE).move_to([0, POINT_SLOPE_Y, 0])
        plugged[2].set_color(PT_COLOR)
        plugged[9].set_color(PT_COLOR)

        self.say('Now the asymptotes. Start at the center. Go up, and then over, to reach the diagonal.')
        self.play(FadeOut(VGroup(root, vertices_row, foci_row, swing_right, transverse_line,
                                 pivot_right, lab_c_axis,
                                 leg_a, leg_b, hyp, lab_a, lab_b, lab_c)), run_time=.8)
        self.play(Create(up_leg), FadeIn(up_label), run_time=1.0)
        self.play(Create(over_leg), FadeIn(over_label), run_time=1.0)
        self.beat('up-over', READ_LONG)

        self.say(f'The slope is {b} over {a}. It is plus or minus, '
                 f'because the other diagonal slopes down.')
        self.play(FadeIn(slope_row), run_time=1.2)
        self.beat('slope', READ_LONG)

        self.say(f'Now use point-slope form, with the center as the point.')
        self.play(FadeIn(point_slope), run_time=1.2)
        self.beat('point-slope', READ_LONG)

        self.say(f'Plug in the center, ({h}, {k}), and the slope.')
        self.play(FadeOut(VGroup(up_leg, over_leg, up_label, over_label)), run_time=.6)
        self.play(ReplacementTransform(point_slope, plugged), run_time=1.3)
        self.beat('plugged', READ_LONG)

        # ---- 11. everything back together ---------------------------------------------------
        self.say('Now put all the answers together.')
        self.play(
            FadeOut(slope_row),
            copy_into(plugged, asymptote_item),
            FadeOut(plugged),
            FadeIn(VGroup(center_item, vertices_item)),
            run_time=1.8)
        self.play(Write(foci_item), run_time=1.2)
        self.beat('all', READ_LONG)

        self.say('Center, vertices, foci, and asymptotes. Every answer is on the graph.')
        self.play(Indicate(asymptote_item, color=PAPER_BLUE, scale_factor=1.12), run_time=1.3)
        self.beat('hold', READ_LONG)
        self.write_marks(self.problem.marks_file)
