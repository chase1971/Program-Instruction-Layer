"""Ellipses (pre-calc conics): the definition, and what the two foci do.

Same ellipse as EllipseHorizontal, x^2/9 + (y - 3)^2/4 = 1: center (0, 3), a = 3, b = 2,
foci (-sqrt(5), 3) and (sqrt(5), 3). The clip opens on the definition:

    an ellipse is the set of all points whose distances to two fixed points (the foci) add up to
    the same constant.

Part 1 beats: the definition -> the two foci -> one point on the ellipse, its distance to each
focus, and their sum (6) -> the point travels the whole ellipse, the sum never changes (the two
segments are the string of a pins-and-string drawing) -> at the vertex the sum is the whole major
axis, so the constant is 2a.
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

import math  # noqa: E402

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    UP,
    Brace,
    Dot,
    DecimalNumber,
    FadeIn,
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

from ellipse_horizontal import GRAPH_X, PROBLEM, EllipseHorizontal  # noqa: E402
from equations_of_lines import READ_LONG, tex  # noqa: E402
from parabola_walkthrough import (  # noqa: E402
    CURVE_COLOR,
    GRAPH_WIDTH,
    INK,
    LEFT_X,
    LIST_SIZE,
)
from ellipse_standard_form import (  # noqa: E402
    A_COLOR,
    FIRST_COLOR,
    SECOND_COLOR,
    EllipseStandardForm,
)
from scene_style import PAPER_MUTED  # noqa: E402

SUM_COLOR = '#2E7D32'           # the sum of the two
VIEW_Y = (-0.5, 6)              # graph rows shown (the ellipse spans 1..5)
VIEW_CENTER_Y = -1.75
DEF_Y = 2.3                     # the definition row, above the readouts
ROW_Y = (1.55, 1.05, 0.55)      # d1, d2 and their sum
NUMBER_X = -1.2                 # left edge of the numbers
START_T = 2.4                   # where the chosen point starts on the ellipse (radians)
VERTEX_T = 2 * math.pi          # the right vertex (3, 3)


class EllipseDefinition(EllipseStandardForm, EllipseHorizontal):
    problem = PROBLEM

    def build_graph(self):
        scale = GRAPH_WIDTH / (GRAPH_X[1] - GRAPH_X[0])
        plane = NumberPlane(
            x_range=[*GRAPH_X, 1], y_range=[*VIEW_Y, 1],
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

        def point(t=None):
            t = tracker.get_value() if t is None else t
            return h + a * math.cos(t), k + b * math.sin(t)

        def d1():
            x, y = point()
            return math.hypot(x - foci[0][0], y - foci[0][1])

        def d2():
            x, y = point()
            return math.hypot(x - foci[1][0], y - foci[1][1])

        def total():
            return d1() + d2()

        focus_dots = [Dot(c2p(*f), color=col, radius=.1)
                      for f, col in zip(foci, (FIRST_COLOR, SECOND_COLOR))]
        focus_labels = [tex(name, size=28, color=col).next_to(dot, DOWN, buff=.1)
                        for name, col, dot in zip(('F_1', 'F_2'), (FIRST_COLOR, SECOND_COLOR),
                                                  focus_dots)]
        center_dot = Dot(c2p(h, k), color=INK, radius=.06)

        definition = tex('d_1', '+', 'd_2', '=', r'\text{constant}', size=36)
        definition[0].set_color(FIRST_COLOR)
        definition[2].set_color(SECOND_COLOR)
        definition.move_to([0, DEF_Y, 0])
        finished = tex('d_1', '+', 'd_2', '=', '2a', size=36)
        finished[0].set_color(FIRST_COLOR)
        finished[2].set_color(SECOND_COLOR)
        finished[4].set_color(A_COLOR)
        finished.move_to([0, DEF_Y, 0])

        to_first = always_redraw(lambda: Line(c2p(*point()), c2p(*foci[0]), color=FIRST_COLOR,
                                              stroke_width=5))
        to_second = always_redraw(lambda: Line(c2p(*point()), c2p(*foci[1]), color=SECOND_COLOR,
                                               stroke_width=5))
        dot = always_redraw(lambda: Dot(c2p(*point()), color=INK, radius=.1))
        first_row, first_num = self.readout('d_1=', FIRST_COLOR, d1, ROW_Y[0])
        second_row, second_num = self.readout('d_2=', SECOND_COLOR, d2, ROW_Y[1])
        sum_row, sum_num = self.readout('d_1+d_2=', SUM_COLOR, total, ROW_Y[2])

        def ellipse_arc(t_end):
            return ParametricFunction(
                lambda t: c2p(*point(t)),
                t_range=[START_T, max(t_end, START_T + .02)], color=CURVE_COLOR, stroke_width=5)

        curve = always_redraw(lambda: ellipse_arc(min(tracker.get_value(), START_T + 2 * math.pi)))

        # ---- 1. the definition, first ---------------------------------------------------------
        self.say('Part 1. By definition, an ellipse is the set of all points where the '
                 'sum of the distances to two fixed points, the foci, is constant.')
        self.play(FadeIn(definition), run_time=.8)
        self.beat('definition', READ_LONG + 3.5)

        # ---- 2. the two foci ------------------------------------------------------------------
        self.say('The foci are two fixed points on the major axis, the same distance from the center.')
        self.play(FadeIn(plane), run_time=.6)
        self.play(FadeIn(center_dot), *[FadeIn(d, scale=1.6) for d in focus_dots],
                  *[Write(label) for label in focus_labels], run_time=.9)
        self.beat('foci', READ_LONG)

        # ---- 3. one point and its two distances -------------------------------------------------
        self.say('Choose any point on the ellipse. Its distance to the first focus is the length '
                 'of this segment.')
        self.play(FadeIn(dot), Write(to_first), FadeIn(first_row), FadeIn(first_num), run_time=.9)
        self.beat('first-distance', READ_LONG)

        self.say('Its distance to the second focus is the length of this segment.')
        self.play(Write(to_second), FadeIn(second_row), FadeIn(second_num), run_time=.9)
        self.beat('second-distance', READ_LONG)

        self.say('Add the two distances. For this point, the sum is $6$.')
        self.play(FadeIn(sum_row), FadeIn(sum_num), run_time=.8)
        self.play(Indicate(sum_num, color=SUM_COLOR, scale_factor=1.2), run_time=1.0)
        self.beat('sum', READ_LONG)

        # ---- 4. move the point all the way around: the sum never changes -------------------------
        self.add(curve)
        self.say('Now move the point around the ellipse. Each distance changes, but the sum stays $6$.')
        self.play(tracker.animate.set_value(START_T + 2 * math.pi), run_time=9.0, rate_func=linear)
        curve.clear_updaters()   # the finished ellipse stays whole when the point moves back
        self.beat('around', READ_LONG)

        self.say('This is how an ellipse is drawn with string: pin the ends at the foci, pull the '
                 'string tight with a pencil, and trace.')
        self.play(Indicate(to_first, color=FIRST_COLOR, scale_factor=1.04),
                  Indicate(to_second, color=SECOND_COLOR, scale_factor=1.04), run_time=1.4)
        self.beat('string', READ_LONG + 1.0)

        # ---- 5. at the vertex the sum is the whole major axis -----------------------------------
        axis = Brace(Line(c2p(h - a, k), c2p(h + a, k)), UP, buff=.12, color=A_COLOR)
        axis_label = tex('2a=6', size=28, color=A_COLOR)
        axis.put_at_tip(axis_label, buff=.04)
        self.say('At the vertex $(3,3)$, the distances are about $5.24$ and $0.76$. The sum is '
                 'the length of the major axis, so the constant is $2a$.')
        self.play(tracker.animate.set_value(VERTEX_T), run_time=1.6, rate_func=smooth)
        self.play(FadeIn(axis), FadeIn(axis_label), run_time=.9)
        self.beat('vertex', READ_LONG + 2.0)

        self.play(ReplacementTransform(definition, finished), run_time=1.2)
        self.play(Indicate(finished[4], color=A_COLOR, scale_factor=1.3), run_time=1.1)
        # Part 2 starts at this step time: the portal cuts here, so its caption opens the part.
        self.beat('part-one-end', READ_LONG + 1.0)

        board = dict(plane=plane, c2p=c2p, point=point, tracker=tracker, foci=foci, curve=curve,
                     center_dot=center_dot, focus_dots=focus_dots, focus_labels=focus_labels,
                     dot=dot, to_first=to_first, to_second=to_second,
                     axis=Group(axis, axis_label), rows=(first_row, second_row, sum_row),
                     numbers=(first_num, second_num, sum_num))
        kept = self.figure_part(board)
        self.algebra_part(kept)
        self.write_marks('ellipse_definition_marks.json')
