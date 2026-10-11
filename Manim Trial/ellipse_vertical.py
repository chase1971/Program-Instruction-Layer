"""Ellipses (pre-calc conics): worksheet problem 2, (x-2)^2/9 + (y+1)^2/16 = 1, a vertical ellipse.

Mirrors ellipse_horizontal.py beat for beat (same layout, colours, captions, and the zoomed right
triangle for the foci). What changes: the bigger number sits under y, so the major axis is vertical,
the vertices are above and below the center, and the foci are too. The center is off the origin
and k is negative, so the y + 1 beat shows y - (-1).

Naming: a is always the bigger (major) half-length and b the smaller, so the same right triangle
b^2 + c^2 = a^2 and the same c^2 = a^2 - b^2 hold. In a vertical ellipse a^2 sits under y.

Verified (EllipseVerticalProblem.__post_init__ re-checks it with Fraction):
    center (2, -1); 9 under x -> 3 left and right; 16 under y -> 4 up and down
    major axis vertical; vertices (2, -5) and (2, 3); co-vertices (-1, -1) and (5, -1)
    c^2 = 16 - 9 = 7; foci (2, -1 +/- sqrt(7))
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
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    NumberPlane,
    ParametricFunction,
    ReplacementTransform,
    VGroup,
    Write,
)

from ellipse_horizontal import ellipse_row  # noqa: E402
from equations_of_lines import READ_LONG, READ_SHORT, signed, tex, var  # noqa: E402
from parabola_walkthrough import (  # noqa: E402
    CURVE_COLOR,
    GRAPH_WIDTH,
    LEFT_X,
    MATH_SIZE,
    P_COLOR,
    PT_COLOR,
    ParabolaOpensUp,
)
from scene_style import PAPER_BLUE, PAPER_GOLD, PAPER_INK, PAPER_MUTED  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

INK = PAPER_INK
GRAPH_X, GRAPH_Y = (-5, 9), (-6, 4)   # the ellipse spans x -1..5 and y -5..3
GRAPH_CENTER_Y = -1.65                # the grid hangs just under the five-row answer list

# Phase 1 row centres (the caption owns y > 2.95; the stacked fractions need the extra room).
ELLIPSE_Y, CENTER_Y = 1.95, 0.55
ACROSS_Y, UPDOWN_Y, MAJOR_Y = -0.65, -1.75, -2.9
ROW_SIZE = 44
FORM_ROW_Y = 0.4
LIST5 = (2.5, 2.05, 1.6, 1.15, 0.7)   # five answer rows, tight so the tall graph fits below
# Foci derivation: the zoomed ellipse and the rows above it. The ellipse is 8 tall, so the zoom is
# barely over 1 - it only has to fit under the three rows.
ZOOM = 1.05
ZOOM_CENTER_Y = -1.85
FORMULA_Y, VERTICES_Y, FOCI_Y = 2.2, 1.3, 0.45


@dataclass
class EllipseVerticalProblem:
    """(x - h)^2 / b2 + (y - k)^2 / a2 = 1 with a2 > b2: a vertical ellipse.

    a2 and b2 are perfect squares so the graph can count whole steps.
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
        if self.a2 <= self.b2:
            raise ValueError('Built for a vertical ellipse: the bigger number is under y.')
        if self.k >= 0:
            raise ValueError('Built for a negative k: the beat shows y - (-k).')
        self.vertices = ((self.h, self.k - self.a), (self.h, self.k + self.a))
        self.co_vertices = ((self.h - self.b, self.k), (self.h + self.b, self.k))
        self.c2 = self.a2 - self.b2          # a^2 - b^2 = c^2, left exact: c = sqrt(c2)
        self.c = math.sqrt(self.c2)
        if self.b2 + self.c2 != self.a2:
            raise ValueError('The right triangle b, c, a does not close.')
        for x, y in self.vertices + self.co_vertices:   # all four sit on the ellipse
            if Fraction((x - self.h) ** 2, self.b2) + Fraction((y - self.k) ** 2, self.a2) != 1:
                raise ValueError('A vertex or co-vertex is not on the ellipse.')


PROBLEM = EllipseVerticalProblem(h=2, k=-1, a2=16, b2=9, marks_file='ellipse_vertical_marks.json')


class EllipseVertical(ParabolaOpensUp):
    problem = PROBLEM

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
        h, k, a, b = p.h, p.k, p.a, p.b
        k_raw = f'({signed(k)})'

        # ---- phase 1 rows, each built once at its final spot ---------------------------------
        given = ellipse_row(['(', 'x', '-', str(h), ')^2'], ['(', 'y', '+', str(-k), ')^2'],
                            str(p.b2), str(p.a2), MATH_SIZE - 6)
        shown = ellipse_row(['(', 'x', '-', str(h), ')^2'], ['(', 'y', '-', k_raw, ')^2'],
                            str(p.b2), str(p.a2), MATH_SIZE - 6)
        fit = min(1, 6.1 / shown.width)
        for row in (given, shown):
            row.scale(fit).move_to([0, ELLIPSE_Y, 0])
        for row in (given, shown):
            row[0][0][3].set_color(PT_COLOR)   # the 2 in (x - 2)
            row[2][0][3].set_color(PT_COLOR)   # the 1 in (y + 1), the -1 in (y - (-1))
        under_x, under_y = shown[0][2], shown[2][2]
        form = ellipse_row(['(', 'x', '-', 'h', ')^2'], ['(', 'y', '-', 'k', ')^2'],
                           'b^2', 'a^2', ROW_SIZE).move_to([0, FORM_ROW_Y, 0])
        for piece in (form[0][0][3], form[2][0][3]):
            piece.set_color(PT_COLOR)        # h and k
        for piece in (form[0][2][0], form[2][2][0]):
            piece.set_color(P_COLOR)         # b^2 and a^2

        center = tex('(', 'h', ',', 'k', ')', '=', '(', str(h), ',', signed(k), ')',
                     size=ROW_SIZE).move_to([0, CENTER_Y, 0])
        for i in (1, 3, 7, 9):
            center[i].set_color(PT_COLOR)
        across = tex('b', '=', r'\sqrt{' + str(p.b2) + '}', '=', str(b), r'\text{ left and right}',
                     size=ROW_SIZE).move_to([0, ACROSS_Y, 0])
        updown = tex('a', '=', r'\sqrt{' + str(p.a2) + '}', '=', str(a), r'\text{ up and down}',
                     size=ROW_SIZE).move_to([0, UPDOWN_Y, 0])
        for row in (across, updown):
            row[0].set_color(P_COLOR)
            row[4].set_color(P_COLOR)
        major = tex(r'\text{major axis: }', r'\text{vertical}',
                    size=ROW_SIZE).move_to([0, MAJOR_Y, 0])
        major[1].set_color(P_COLOR)

        # ---- phase 2: the answer list, and the graph -----------------------------------------
        (vx1, vy1), (vx2, vy2) = p.vertices
        (cx1, cy1), (cx2, cy2) = p.co_vertices
        center_item = self.list_row('Center', '(', str(h), ',', signed(k), ')',
                                    x=LEFT_X, y=LIST5[0])
        major_item = self.list_row('Major axis', r'\text{vertical}', x=LEFT_X, y=LIST5[1])
        vertices_item = self.list_row('Vertices', '(', str(vx1), ',', signed(vy1), ')',
                                      r'\text{ and }', '(', str(vx2), ',', signed(vy2), ')',
                                      x=LEFT_X, y=LIST5[2])
        co_item = self.list_row('Co-vertices', '(', signed(cx1), ',', signed(cy1), ')',
                                r'\text{ and }', '(', signed(cx2), ',', signed(cy2), ')',
                                x=LEFT_X, y=LIST5[3])
        foci_item = self.list_row('Foci', '(', str(h), ',', signed(k), r'\pm',
                                  r'\sqrt{' + str(p.c2) + '}', ')', x=LEFT_X, y=LIST5[4])

        plane = self.build_graph()

        def c2p(x, y):
            return plane.c2p(x, y)

        def dot(x, y, color):
            return Dot(c2p(x, y), color=color, radius=.09)

        def run(start, end, color=PAPER_GOLD):
            return Arrow(c2p(*start), c2p(*end), buff=0, color=color, stroke_width=5,
                         tip_length=.14, max_tip_length_to_length_ratio=.4)

        center_dot = dot(h, k, CURVE_COLOR)
        updown_arrows = VGroup(run((h, k), p.vertices[0]), run((h, k), p.vertices[1]))
        updown_labels = VGroup(*[tex(str(a), size=28, color=PAPER_GOLD).next_to(arrow, RIGHT,
                                                                                 buff=.08)
                                 for arrow in updown_arrows])
        vertex_dots = VGroup(*[dot(x, y, CURVE_COLOR) for x, y in p.vertices])
        across_arrows = VGroup(run((h, k), p.co_vertices[0]), run((h, k), p.co_vertices[1]))
        across_labels = VGroup(*[tex(str(b), size=28, color=PAPER_GOLD).next_to(arrow, UP, buff=.06)
                                 for arrow in across_arrows])
        co_dots = VGroup(*[dot(x, y, P_COLOR) for x, y in p.co_vertices])
        curve = ParametricFunction(
            lambda t: c2p(h + b * math.cos(t), k + a * math.sin(t)),
            t_range=[0, 2 * math.pi], color=CURVE_COLOR, stroke_width=5)

        # ---- 1. the problem ----------------------------------------------------------------
        self.say(f'Since both {var("x", PAPER_BLUE)} and {var("y", PAPER_BLUE)} '
                 f'are squared and we are adding, this is an ellipse.')
        self.play(FadeIn(given), run_time=1.2)
        self.play(Indicate(given[0][0], color=PAPER_BLUE, scale_factor=1.3),
                  Indicate(given[2][0], color=PAPER_BLUE, scale_factor=1.3), run_time=1.1)
        self.beat('problem', READ_LONG)

        self.say(f'For ellipses, {var("a", PAPER_BLUE)} is always the bigger number. '
                 f'{p.a2} is bigger, so {var("a", PAPER_BLUE)} squared goes under {var("y", PAPER_BLUE)}.')
        self.play(FadeIn(form), run_time=1.2)
        self.beat('form', READ_LONG)

        # ---- 2. the center -----------------------------------------------------------------
        self.say(f'The center is (h, k). Think of {var("y", PAPER_BLUE)} + {-k} as '
                 f'{var("y", PAPER_BLUE)} minus negative {-k}.')
        self.play(ReplacementTransform(given, shown), run_time=1.4)
        self.play(Indicate(shown[0][0][3], color=PT_COLOR, scale_factor=1.6),
                  Indicate(shown[2][0][3], color=PT_COLOR, scale_factor=1.6), run_time=1.1)
        self.beat('negative', READ_LONG)

        self.say(f'The h and k are the numbers being subtracted. So the center is ({h}, {k}).')
        self.play(Indicate(form[0][0][3], color=PT_COLOR, scale_factor=1.6),
                  Indicate(form[2][0][3], color=PT_COLOR, scale_factor=1.6), run_time=1.1)
        self.play(FadeOut(form), FadeIn(center), run_time=1.2)
        self.beat('center', READ_LONG)

        # ---- 3. under each variable ---------------------------------------------------------
        self.say(f'The {p.b2} is under {var("x", PAPER_BLUE)}, so take its square root: '
                 f'{var("b", PAPER_BLUE)} = {b}. Go {b} left and {b} right.')
        self.play(Indicate(under_x, color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.play(FadeIn(across), run_time=1.2)
        self.beat('across', READ_LONG)

        self.say(f'The {p.a2} is under {var("y", PAPER_BLUE)}, so {var("a", PAPER_BLUE)} = {a}. '
                 f'Go {a} up and {a} down.')
        self.play(Indicate(under_y, color=P_COLOR, scale_factor=1.5), run_time=1.1)
        self.play(FadeIn(updown), run_time=1.2)
        self.beat('updown', READ_LONG)

        # ---- 4. the major axis --------------------------------------------------------------
        self.say(f'The bigger number is the longer way. That is the major axis. '
                 f'{p.a2} is bigger, so it is vertical.')
        self.play(Indicate(under_y, color=P_COLOR, scale_factor=1.5),
                  Indicate(updown, color=P_COLOR, scale_factor=1.1), run_time=1.2)
        self.play(FadeIn(major), run_time=1.0)
        self.beat('major', READ_LONG)

        # ---- 5. the graph and the answer list ------------------------------------------------
        self.say('Now graph it. We will keep our answers in a list.')
        self.play(
            copy_into(center, center_item), copy_into(major, major_item),
            FadeOut(VGroup(shown, center, across, updown, major)),
            FadeIn(plane), run_time=1.8)
        self.beat('list', READ_LONG)

        self.say(f'Plot the center, ({h}, {k}).')
        self.play(FadeIn(center_dot, scale=1.6), run_time=1.0)
        self.beat('center-dot', READ_SHORT)

        self.say(f'Go {a} up and {a} down from the center.')
        self.play(*[Create(arrow) for arrow in updown_arrows], FadeIn(updown_labels), run_time=1.3)
        self.play(FadeIn(vertex_dots, scale=1.6), run_time=.8)
        self.beat('updown-dots', READ_LONG)

        self.say('These two points are on the major axis, so they are the vertices.')
        self.play(Write(vertices_item), run_time=1.2)
        self.beat('vertices', READ_LONG)

        self.say(f'Now go {b} left and {b} right from the center.')
        self.play(FadeOut(VGroup(updown_arrows, updown_labels)), run_time=.5)
        self.play(*[Create(arrow) for arrow in across_arrows], FadeIn(across_labels), run_time=1.3)
        self.play(FadeIn(co_dots, scale=1.6), run_time=.8)
        self.beat('across-dots', READ_LONG)

        self.say('These two are not on the major axis. They are the co-vertices.')
        self.play(Write(co_item), run_time=1.2)
        self.beat('co-vertices', READ_LONG)

        # ---- 6. the curve -------------------------------------------------------------------
        self.say('Now draw the ellipse through the four points.')
        self.play(FadeOut(VGroup(across_arrows, across_labels)), run_time=.5)
        self.play(Create(curve), run_time=2.2)
        self.beat('curve', READ_LONG)

        # ---- 7. finding c: zoom in on a right triangle ----------------------------------------
        zs = GRAPH_WIDTH / (GRAPH_X[1] - GRAPH_X[0]) * ZOOM

        def zp(x, y):
            return np.array([(x - h) * zs, (y - k) * zs + ZOOM_CENTER_Y, 0])

        def zdot(x, y, color):
            return Dot(zp(x, y), color=color, radius=.1)

        def zline(start, end, color, width=6):
            return Line(zp(*start), zp(*end), color=color, stroke_width=width)

        z_curve = ParametricFunction(
            lambda t: zp(h + b * math.cos(t), k + a * math.sin(t)),
            t_range=[0, 2 * math.pi], color=CURVE_COLOR, stroke_width=6)
        z_center = zdot(h, k, CURVE_COLOR)
        z_vertices = VGroup(*[zdot(x, y, CURVE_COLOR) for x, y in p.vertices])
        z_co = VGroup(*[zdot(x, y, P_COLOR) for x, y in p.co_vertices])
        fy = p.c
        focus_up, focus_down = zdot(h, k + fy, PAPER_GOLD), zdot(h, k - fy, PAPER_GOLD)
        graph_foci = VGroup(dot(h, k + fy, PAPER_GOLD), dot(h, k - fy, PAPER_GOLD))
        leg_b = zline((h, k), p.co_vertices[1], PT_COLOR)
        leg_c = zline((h, k), (h, k + fy), P_COLOR)
        axis_line = DashedLine(zp(h, k - 4.1), zp(h, k + 4.1), color=PAPER_BLUE, stroke_width=4,
                               dash_length=.12)
        hyp = zline(p.co_vertices[1], (h, k + fy), INK, width=5)
        lab_b = tex(str(b), size=32, color=PT_COLOR).move_to(zp(h + b / 2, k) + DOWN * .3)
        lab_c = tex('c', size=32, color=P_COLOR).move_to(zp(h, k + fy / 2) + LEFT * .28)
        lab_a = tex(str(a), size=32).move_to(zp(h + b / 2, k + fy / 2) + np.array([.3, .15, 0]))

        # Rows above the zoomed ellipse; each is built once at its final spot.
        pyth = tex('b^2', '+', 'c^2', '=', 'a^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        formula = tex('a^2', '-', 'b^2', '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        plug = tex(str(p.a2), '-', str(p.b2), '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        seven = tex(str(p.c2), '=', 'c^2', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        root = tex('c', '=', r'\sqrt{' + str(p.c2) + '}', size=ROW_SIZE).move_to([0, FORMULA_Y, 0])
        pyth[0].set_color(PT_COLOR)
        pyth[2].set_color(P_COLOR)
        formula[2].set_color(PT_COLOR)
        formula[4].set_color(P_COLOR)
        plug[2].set_color(PT_COLOR)
        plug[4].set_color(P_COLOR)
        seven[2].set_color(P_COLOR)
        root[0].set_color(P_COLOR)
        root[2].set_color(P_COLOR)
        vertices_row = tex(r'\text{vertices: }', '(', str(h), ',', signed(k), r'\pm', str(a), ')',
                           size=ROW_SIZE).move_to([0, VERTICES_Y, 0])
        foci_row = tex(r'\text{foci: }', '(', str(h), ',', signed(k), r'\pm',
                       r'\sqrt{' + str(p.c2) + '}', ')',
                       size=ROW_SIZE).move_to([0, FOCI_Y, 0])
        vertices_row[6].set_color(PT_COLOR)
        foci_row[6].set_color(P_COLOR)

        # Transform reshapes its source in place, so keep untouched copies to come back to.
        home = {name: mob.copy() for name, mob in (
            ('curve', curve), ('center', center_dot), ('vertices', vertex_dots), ('co', co_dots))}

        self.say('To find c, we need a closer look. Put the answers away for now.')
        self.play(
            FadeOut(VGroup(center_item, major_item, vertices_item, co_item, plane)),
            ReplacementTransform(curve, z_curve), ReplacementTransform(center_dot, z_center),
            ReplacementTransform(vertex_dots, z_vertices), ReplacementTransform(co_dots, z_co),
            run_time=1.8)
        self.beat('zoom', READ_LONG)

        self.say(f'From the center over to the co-vertex is {b}.')
        self.play(Create(leg_b), FadeIn(lab_b), run_time=1.1)
        self.beat('leg-b', READ_SHORT)

        self.say('The foci sit on the major axis, so draw a dashed line along it.')
        self.play(Create(axis_line), run_time=1.3)
        self.beat('axis', READ_SHORT)

        self.say(f'From the co-vertex, draw a line {a} long, like center to vertex. '
                 f'It must hit the major axis.')
        self.play(Create(hyp), FadeIn(lab_a), run_time=1.3)
        self.play(FadeIn(focus_up, scale=1.6), run_time=.8)
        self.beat('hyp', READ_LONG)

        self.say(f'Where it lands is {var("c", PAPER_BLUE)} from the center.')
        self.play(Create(leg_c), FadeIn(lab_c), run_time=1.1)
        self.beat('leg-c', READ_LONG)

        self.say(f'That makes a right triangle: {var("b", PAPER_GOLD)} squared plus '
                 f'{var("c", PAPER_BLUE)} squared equals {var("a", PAPER_INK)} squared.')
        self.play(FadeIn(pyth), run_time=1.2)
        self.beat('pyth', READ_LONG)

        self.say(f'Subtract {var("b", PAPER_GOLD)} squared from both sides: '
                 f'{var("a", PAPER_INK)} squared minus {var("b", PAPER_GOLD)} squared '
                 f'equals {var("c", PAPER_BLUE)} squared.')
        self.play(ReplacementTransform(pyth, formula), run_time=1.5)
        self.beat('formula', READ_LONG)

        self.say(f'{var("a", PAPER_INK)} squared and {var("b", PAPER_GOLD)} squared are the '
                 f'numbers under y and x: {p.a2} and {p.b2}.')
        self.play(ReplacementTransform(formula, plug), run_time=1.3)
        self.beat('plug', READ_LONG)

        self.say(f'{p.a2} minus {p.b2} is {p.c2}.')
        self.play(ReplacementTransform(plug, seven), run_time=1.3)
        self.beat('seven', READ_SHORT)

        self.say(f'Take the square root. Leave {var("c", PAPER_BLUE)} as an exact value.')
        self.play(ReplacementTransform(seven, root), run_time=1.3)
        self.beat('c-value', READ_LONG)

        # ---- 8. c follows the vertices ------------------------------------------------------
        self.say(f'{var("c", PAPER_BLUE)} always goes the same way as the vertices. '
                 f'These go up and down from the center.')
        self.play(FadeIn(vertices_row), run_time=1.2)
        self.play(Indicate(z_vertices, color=PAPER_BLUE, scale_factor=1.5), run_time=1.1)
        self.beat('follows', READ_LONG)

        self.say(f'So attach {var("c", PAPER_BLUE)} to the center the same way, up and down.')
        self.play(FadeIn(foci_row), FadeIn(focus_down, scale=1.6), run_time=1.3)
        self.beat('foci', READ_LONG)

        # ---- 9. everything back together ---------------------------------------------------
        self.say('Now put all the answers together.')
        self.play(
            FadeOut(VGroup(root, vertices_row, foci_row, axis_line, leg_b, leg_c, hyp, lab_a, lab_b, lab_c)),
            ReplacementTransform(z_curve, home['curve']),
            ReplacementTransform(z_center, home['center']),
            ReplacementTransform(z_vertices, home['vertices']),
            ReplacementTransform(z_co, home['co']),
            ReplacementTransform(VGroup(focus_up, focus_down), graph_foci),
            FadeIn(VGroup(plane, center_item, major_item, vertices_item, co_item)),
            run_time=2.0)
        self.play(Write(foci_item), run_time=1.2)
        self.beat('all', READ_LONG)

        self.say('Center, vertices, co-vertices, and foci. Every answer is on the graph.')
        self.play(Indicate(foci_item, color=PAPER_BLUE, scale_factor=1.12), run_time=1.3)
        self.beat('hold', READ_LONG)
        self.write_marks(self.problem.marks_file)
