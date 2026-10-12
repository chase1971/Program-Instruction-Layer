"""Hyperbolas (pre-calc conics): the definition, and what the two foci do. Part 1 of the clip.

Same hyperbola as HyperbolaHorizontal, (x - 1)^2/25 - y^2/49 = 1: center (1, 0), a = 5, b = 7,
foci (1 - sqrt(74), 0) and (1 + sqrt(74), 0), vertices (-4, 0) and (6, 0). The clip opens on the
definition:

    a hyperbola is the set of all points where the absolute value of the difference of the
    distances to two fixed points (the foci) is constant.

Part 1 beats (mirrors ellipse_definition.py): the definition -> the two foci -> one point on the
hyperbola, its distance to each focus, and the absolute difference (10) -> the point travels the
right branch, the difference never changes -> the same on the left branch -> at the vertex the
difference is the distance between the vertices, so the constant is 2a.
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

import math  # noqa: E402

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    Brace,
    DecimalNumber,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    Indicate,
    Line,
    NumberPlane,
    ParametricFunction,
    ReplacementTransform,
    ValueTracker,
    Write,
    always_redraw,
    linear,
    smooth,
)

from equations_of_lines import READ_LONG, tex  # noqa: E402
from hyperbola_horizontal import PROBLEM, HyperbolaHorizontal  # noqa: E402
from hyperbola_standard_form import HyperbolaStandardForm  # noqa: E402
from parabola_walkthrough import (  # noqa: E402
    CURVE_COLOR,
    GRAPH_WIDTH,
    INK,
    LEFT_X,
    LIST_SIZE,
)
from scene_style import PAPER_BLUE, PAPER_GOLD, PAPER_MUTED  # noqa: E402

FIRST_COLOR = PAPER_BLUE        # focus 1 and its distance d1
SECOND_COLOR = PAPER_GOLD       # focus 2 and its distance d2
A_COLOR = '#6A1B9A'             # a: center to vertex, and the constant 2a
DIFF_COLOR = '#2E7D32'          # the absolute difference of the two
VIEW_X = (-9, 11)               # graph columns shown (the foci sit at -7.6 and 9.6)
VIEW_Y = (-6.5, 6.5)            # graph rows shown (the point stays inside them)
VIEW_CENTER_Y = -1.82
DEF_Y = 2.3                     # the definition row, above the readouts
ROW_Y = (1.55, 1.05, 0.55)      # d1, d2 and their difference
NUMBER_X = -0.9                 # left edge of the numbers
START_T = 0.7                   # where the chosen point starts on the right branch
T_LIMIT = 0.78                  # the point stays inside the graph rows
TOP_T = 0.78                    # the point goes up to here, then all the way down
VERTEX_T = 0.0                  # the right vertex (6, 0)


class HyperbolaDefinition(HyperbolaStandardForm, HyperbolaHorizontal):
    problem = PROBLEM

    def build_graph(self):
        scale = GRAPH_WIDTH / (VIEW_X[1] - VIEW_X[0])
        plane = NumberPlane(
            x_range=[*VIEW_X, 1], y_range=[*VIEW_Y, 1],
            x_length=GRAPH_WIDTH, y_length=scale * (VIEW_Y[1] - VIEW_Y[0]),
            axis_config={'color': PAPER_MUTED, 'stroke_width': 2},
            background_line_style={'stroke_color': '#CBD5E1', 'stroke_width': 1,
                                   'stroke_opacity': 1},
            faded_line_ratio=0,
        )
        plane.move_to([0, VIEW_CENTER_Y, 0])
        return plane

    def readout(self, label, color, measure, y):
        """'label = number' on one row; the number follows measure() as the point moves."""
        row = tex(label, size=LIST_SIZE, color=color)
        row.move_to([LEFT_X + row.width / 2, y, 0])
        number = DecimalNumber(measure(), num_decimal_places=2, font_size=LIST_SIZE + 4,
                               color=color)
        anchor = [NUMBER_X, y, 0]

        def follow(m):
            m.set_value(measure())
            m.move_to(anchor, aligned_edge=LEFT)

        number.add_updater(follow)
        number.move_to(anchor, aligned_edge=LEFT)
        return row, number

    def construct(self):
        p = self.problem
        h, k, a, b, c = p.h, p.k, p.a, p.b, p.c
        plane = self.build_graph()

        def c2p(x, y):
            return plane.c2p(x, y)

        foci = ((h - c, k), (h + c, k))
        tracker = ValueTracker(START_T)
        side = [1]                   # +1: the right branch, -1: the left branch

        def point(t=None, sign=None):
            t = tracker.get_value() if t is None else t
            sign = side[0] if sign is None else sign
            return h + sign * a * math.cosh(t), k + b * math.sinh(t)

        def d1():
            x, y = point()
            return math.hypot(x - foci[0][0], y - foci[0][1])

        def d2():
            x, y = point()
            return math.hypot(x - foci[1][0], y - foci[1][1])

        def gap():
            return abs(d1() - d2())

        focus_dots = [Dot(c2p(*f), color=col, radius=.1)
                      for f, col in zip(foci, (FIRST_COLOR, SECOND_COLOR))]
        focus_labels = [tex(name, size=28, color=col).next_to(dot, DOWN, buff=.1)
                        for name, col, dot in zip(('F_1', 'F_2'), (FIRST_COLOR, SECOND_COLOR),
                                                  focus_dots)]
        center_dot = Dot(c2p(h, k), color=INK, radius=.06)

        definition = tex('|', 'd_1', '-', 'd_2', '|', '=', r'\text{constant}', size=36)
        definition[1].set_color(FIRST_COLOR)
        definition[3].set_color(SECOND_COLOR)
        definition.move_to([0, DEF_Y, 0])
        finished = tex('|', 'd_1', '-', 'd_2', '|', '=', '2a', size=36)
        finished[1].set_color(FIRST_COLOR)
        finished[3].set_color(SECOND_COLOR)
        finished[6].set_color(A_COLOR)
        finished.move_to([0, DEF_Y, 0])

        to_first = always_redraw(lambda: Line(c2p(*point()), c2p(*foci[0]), color=FIRST_COLOR,
                                              stroke_width=5))
        to_second = always_redraw(lambda: Line(c2p(*point()), c2p(*foci[1]), color=SECOND_COLOR,
                                               stroke_width=5))
        dot = always_redraw(lambda: Dot(c2p(*point()), color=INK, radius=.1))
        first_row, first_num = self.readout('d_1=', FIRST_COLOR, d1, ROW_Y[0])
        second_row, second_num = self.readout('d_2=', SECOND_COLOR, d2, ROW_Y[1])
        gap_row, gap_num = self.readout('|d_1-d_2|=', DIFF_COLOR, gap, ROW_Y[2])

        # Each branch is drawn by the point: it grows over the stretch of t the point has covered.
        seen = {1: [START_T, START_T], -1: [START_T, START_T]}

        def branch_arc(sign):
            if side[0] == sign:
                t = tracker.get_value()
                seen[sign][0] = min(seen[sign][0], t)
                seen[sign][1] = max(seen[sign][1], t)
            lo, hi = seen[sign]
            return ParametricFunction(
                lambda t: c2p(*point(t, sign)),
                t_range=[lo, max(hi, lo + .02)], color=CURVE_COLOR, stroke_width=5)

        right_curve = always_redraw(lambda: branch_arc(1))
        left_curve = always_redraw(lambda: branch_arc(-1))

        # ---- 1. the definition, first ---------------------------------------------------------
        self.say('Part 1. A hyperbola is the set of all points where the absolute '
                 'difference of the distances to two fixed points, the foci, is constant.')
        self.play(FadeIn(definition), run_time=.8)
        self.beat('definition', READ_LONG + 4.5)

        # ---- 2. the two foci ------------------------------------------------------------------
        self.say('The foci are two fixed points on the transverse axis, the same distance from '
                 'the center.')
        self.play(FadeIn(plane), run_time=.6)
        self.play(FadeIn(center_dot), *[FadeIn(d, scale=1.6) for d in focus_dots],
                  *[Write(label) for label in focus_labels], run_time=.9)
        self.beat('foci', READ_LONG)

        # ---- 3. one point and its two distances -------------------------------------------------
        self.say('Choose any point on the hyperbola. Its distance to the first focus is the '
                 'length of this segment.')
        self.play(FadeIn(dot), Write(to_first), FadeIn(first_row), FadeIn(first_num), run_time=.9)
        self.beat('first-distance', READ_LONG)

        self.say('Its distance to the second focus is the length of this segment.')
        self.play(Write(to_second), FadeIn(second_row), FadeIn(second_num), run_time=.9)
        self.beat('second-distance', READ_LONG)

        self.say('Subtract the two distances. The absolute value makes the result positive. '
                 'For this point, the difference is $|15.80-5.80|=10$.')
        self.play(FadeIn(gap_row), FadeIn(gap_num), run_time=.8)
        self.play(Indicate(gap_num, color=DIFF_COLOR, scale_factor=1.2), run_time=1.0)
        self.beat('difference', READ_LONG + 1.5)

        # ---- 4. move the point along the branch: the difference never changes -------------------
        self.add(right_curve, left_curve)
        self.say('Now move the point along this branch. Each distance changes, but the '
                 'difference stays $10$.')
        self.play(tracker.animate.set_value(TOP_T), run_time=1.6, rate_func=smooth)
        self.play(tracker.animate.set_value(-T_LIMIT), run_time=7.0, rate_func=linear)
        self.beat('along', READ_LONG)

        # ---- 5. the other branch -----------------------------------------------------------------
        self.say('The same is true on the other branch. There, the second distance is the '
                 'larger one, and the difference is still $10$.')
        self.play(FadeOut(dot), FadeOut(to_first), FadeOut(to_second), run_time=.5)
        side[0] = -1
        tracker.set_value(START_T)
        self.play(FadeIn(dot), FadeIn(to_first), FadeIn(to_second), run_time=.6)
        self.play(tracker.animate.set_value(TOP_T), run_time=1.2, rate_func=smooth)
        self.play(tracker.animate.set_value(-T_LIMIT), run_time=6.0, rate_func=linear)
        right_curve.clear_updaters()   # the finished branches stay whole when the point moves on
        left_curve.clear_updaters()
        self.beat('other-branch', READ_LONG)

        # ---- 6. at the vertex the difference is the distance between the vertices -----------------
        axis = Brace(Line(c2p(h - a, k), c2p(h + a, k)), DOWN, buff=.1, color=A_COLOR)
        axis_label = tex('2a=10', size=26, color=A_COLOR)
        axis.put_at_tip(axis_label, buff=.04)
        self.say('At the vertex $(6,0)$, the distances are about $13.60$ and $3.60$. The '
                 'difference is the distance between the two vertices, so the constant is $2a$.')
        self.play(FadeOut(dot), FadeOut(to_first), FadeOut(to_second), run_time=.4)
        side[0] = 1
        tracker.set_value(VERTEX_T)
        self.play(FadeIn(dot), FadeIn(to_first), FadeIn(to_second), run_time=.5)
        self.play(FadeIn(axis), FadeIn(axis_label), run_time=.9)
        self.beat('vertex', READ_LONG + 2.0)

        self.play(ReplacementTransform(definition, finished), run_time=1.2)
        self.play(Indicate(finished[6], color=A_COLOR, scale_factor=1.3), run_time=1.1)
        # Part 2 starts at this step time: the portal cuts here, so its caption opens the part.
        self.beat('part-one-end', READ_LONG + 1.0)

        board = dict(plane=plane, c2p=c2p, point=point, tracker=tracker, foci=foci, side=side,
                     curves=(right_curve, left_curve), center_dot=center_dot,
                     focus_dots=focus_dots, focus_labels=focus_labels, dot=dot,
                     to_first=to_first, to_second=to_second, axis=Group(axis, axis_label),
                     rows=(first_row, second_row, gap_row), numbers=(first_num, second_num,
                                                                     gap_num))
        self.figure_part(board)
        self.write_marks('hyperbola_definition_marks.json')
