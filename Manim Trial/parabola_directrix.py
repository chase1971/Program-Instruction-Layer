"""Parabolas (pre-calc conics): what the directrix is, and how it graphs a parabola.

Same parabola as ParabolaOpensUp, (x - 2)^2 = 12(y + 1): vertex (2, -1), p = 3, focus (2, 2),
directrix y = -4. This clip never touches the equation. It shows the definition on the graph:

    a parabola is every point that is the SAME distance from the focus as from the directrix.

Beats: the focus and directrix -> one point on the parabola, its length to the focus and its
straight-down length to the directrix (equal) -> keep them equal while the point moves and the
parabola is traced -> why the directrix matters.
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

import math  # noqa: E402

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedLine,
    Dot,
    DecimalNumber,
    FadeIn,
    FadeOut,
    Line,
    ValueTracker,
    Write,
    always_redraw,
    linear,
)

from equations_of_lines import READ_LONG, READ_SHORT, tex  # noqa: E402
from parabola_walkthrough import (  # noqa: E402
    CURVE_COLOR,
    GRAPH_X,
    GRAPH_Y,
    INK,
    LEFT_X,
    LIST_SIZE,
    OPENS_UP,
    ParabolaOpensUp,
)
from scene_style import PAPER_BLUE, PAPER_GOLD  # noqa: E402

FOCUS_COLOR = PAPER_BLUE        # the focus and every distance to it
DIRECTRIX_COLOR = PAPER_GOLD    # the directrix and every distance to it
ROW_Y = (1.5, 0.85)             # the two live distances, above the graph
NUMBER_X = 0.9                  # left edge of the numbers
DEF_Y = 2.35                    # the definition row, above the graph
DERIVE_Y = (1.75, 1.15, .55)    # the derivation rows; the last one is replaced step by step
DERIVE_SIZE = 36


class ParabolaDirectrix(ParabolaOpensUp):
    problem = OPENS_UP

    def probe(self, plane, y_of_x, x0):
        """A point on the graph, a segment to the focus, a segment to the directrix, two readouts.

        Returns (mobjects, tracker). The tracker is the point's x; its y is y_of_x(x).
        """
        p = self.problem
        fx, fy = p.focus

        def c2p(x, y):
            return plane.c2p(x, y)

        xt = ValueTracker(x0)

        def point():
            x = xt.get_value()
            return x, y_of_x(x)

        def d_focus():
            x, y = point()
            return math.hypot(x - fx, y - fy)

        def d_directrix():
            return point()[1] - p.directrix

        to_focus = always_redraw(lambda: Line(c2p(*point()), c2p(fx, fy), color=FOCUS_COLOR,
                                              stroke_width=5))
        to_directrix = always_redraw(lambda: Line(c2p(*point()), c2p(point()[0], p.directrix),
                                                  color=DIRECTRIX_COLOR, stroke_width=5))
        dot = always_redraw(lambda: Dot(c2p(*point()), color=INK, radius=.1))

        rows, numbers = [], []
        for label, color, measure, y in (('to the focus: ', FOCUS_COLOR, d_focus, ROW_Y[0]),
                                         ('to the directrix: ', DIRECTRIX_COLOR, d_directrix,
                                          ROW_Y[1])):
            row = tex(rf'\text{{{label}}}', size=LIST_SIZE, color=color)
            row.move_to([LEFT_X + row.width / 2, y, 0])
            number = DecimalNumber(measure(), num_decimal_places=2, font_size=LIST_SIZE + 4,
                                   color=color)
            anchor = [NUMBER_X, y, 0]

            def follow(m, measure=measure, anchor=anchor):
                m.set_value(measure())
                m.move_to(anchor, aligned_edge=LEFT)

            number.add_updater(follow)
            number.move_to(anchor, aligned_edge=LEFT)
            rows.append(row)
            numbers.append(number)
        return (to_focus, to_directrix, dot, *rows, *numbers), xt

    def freeze(self, mobjects):
        """Stop a probe updating so it can fade out (always_redraw would undo the fade)."""
        for m in mobjects:
            m.clear_updaters()

    def construct(self):
        p = self.problem
        h, k = p.h, p.k
        fx, fy = p.focus
        plane = self.build_graph()

        def c2p(x, y):
            return plane.c2p(x, y)

        def found_dot(x, y):
                return Dot(c2p(x, y), color=CURVE_COLOR, radius=.09)

        focus_dot = found_dot(fx, fy).set_color(FOCUS_COLOR)
        focus_label = tex(r'\text{focus}', size=28, color=FOCUS_COLOR).next_to(focus_dot, UP,
                                                                               buff=.1)
        directrix_line = DashedLine(c2p(GRAPH_X[0], p.directrix), c2p(GRAPH_X[1], p.directrix),
                                    color=DIRECTRIX_COLOR, stroke_width=4, dash_length=.12)
        directrix_label = tex(r'\text{directrix}', size=28, color=DIRECTRIX_COLOR
                              ).next_to(c2p(6.6, p.directrix), DOWN, buff=.06)
        curve = plane.plot(lambda x: k + (x - h) ** 2 / p.c, x_range=[h - 6., h + 6.],
                           color=CURVE_COLOR, stroke_width=5)

        # ---- 1. the two things a parabola is built around ------------------------------------
        self.say('Every parabola has a point called the focus and a line called the directrix.')
        self.play(FadeIn(plane), run_time=1.0)
        self.play(FadeIn(focus_dot, scale=1.6), Write(focus_label), run_time=1.0)
        self.play(Create(directrix_line), Write(directrix_label), run_time=1.3)
        self.beat('setup', READ_LONG)

        # ---- 2. one point: measure to the focus, then straight down to the directrix -------------
        self.say('Take a point. Measure from the focus to the point.')
        on_curve = lambda x: k + (x - h) ** 2 / p.c
        probe, xt = self.probe(plane, on_curve, h - 6.)
        to_focus, to_directrix, dot = probe[0], probe[1], probe[2]
        focus_row, directrix_row = probe[3], probe[4]
        focus_num, directrix_num = probe[5], probe[6]
        self.play(FadeIn(dot), Create(to_focus), FadeIn(focus_row), FadeIn(focus_num),
                  run_time=1.3)
        self.beat('focus-length', READ_LONG)

        self.say('Now measure straight down to the directrix, at a right angle.')
        self.play(Create(to_directrix), FadeIn(directrix_row), FadeIn(directrix_num),
                  run_time=1.3)
        self.beat('directrix-length', READ_LONG)

        self.say('This point is where the two lengths are equal.')
        self.beat('equal', READ_LONG)

        # ---- 3. keep them equal and the parabola draws itself -----------------------------------
        self.say('Now move the point, but always keep the two lengths equal. The path it traces '
                 'is the parabola.')
        self.play(xt.animate.set_value(h + 6.), Create(curve), run_time=3.5, rate_func=linear)
        self.beat('trace', READ_LONG)

        # ---- 4. the definition, stated -----------------------------------------------------------
        self.play(*[FadeOut(m) for m in probe[3:]],
                  xt.animate.set_value(h + 4.), run_time=.9)   # park on (6, 1/3), clear of the edge
        self.freeze(probe)
        label_pt = tex('(x,y)', size=28, color=INK).next_to(c2p(h + 4., on_curve(h + 4.)), UP,
                                                            buff=.12)
        label_gold = tex('y+4', size=28, color=DIRECTRIX_COLOR).next_to(
            c2p(h + 4., (on_curve(h + 4.) + p.directrix) / 2), RIGHT, buff=.1)
        self.play(FadeIn(label_pt), FadeIn(label_gold), run_time=.6)

        definition = tex(r'\text{focus distance}', '=', r'\text{directrix distance}', size=30)
        definition[0].set_color(FOCUS_COLOR)
        definition[2].set_color(DIRECTRIX_COLOR)
        definition.move_to([0, DEF_Y, 0])
        self.say('This is the definition of a parabola: every point that is the same distance '
                 'from the focus as from the directrix.')
        self.play(FadeIn(definition), run_time=1.0)
        self.beat('definition', READ_LONG + 1.0)

        # ---- 5. the equation falls out of the definition -----------------------------------------
        dist = tex(r'\sqrt{(x-2)^2+(y-2)^2}', '=', 'y+4', size=DERIVE_SIZE)
        dist[0].set_color(FOCUS_COLOR)
        dist[2].set_color(DIRECTRIX_COLOR)
        dist.move_to([0, DERIVE_Y[0], 0])
        squared = tex('(x-2)^2+(y-2)^2', '=', '(y+4)^2', size=DERIVE_SIZE).move_to(
            [0, DERIVE_Y[1], 0])
        expanded = tex('(x-2)^2+y^2-4y+4', '=', 'y^2+8y+16', size=DERIVE_SIZE - 4).move_to(
            [0, DERIVE_Y[2], 0])
        cancelled = tex('(x-2)^2-4y+4', '=', '8y+16', size=DERIVE_SIZE).move_to(
            [0, DERIVE_Y[2], 0])
        isolated = tex('(x-2)^2', '=', '12y+12', size=DERIVE_SIZE).move_to([0, DERIVE_Y[2], 0])
        factored = tex('(x-2)^2', '=', '12(y+1)', size=DERIVE_SIZE + 6).move_to(
            [0, DERIVE_Y[2], 0])

        self.say('Now use it. The distance to the focus comes from the distance formula. The '
                 'distance down to the directrix is y plus 4. Set them equal.')
        self.play(Write(dist), run_time=1.8)
        self.beat('set-equal', READ_LONG + 1.0)

        self.say('Square both sides to get rid of the square root.')
        self.play(Write(squared), run_time=1.4)
        self.beat('square', READ_LONG)

        self.say('Expand the squares.')
        self.play(Write(expanded), run_time=1.4)
        self.beat('expand', READ_LONG)

        self.say('The y squared terms are on both sides, so they cancel. Then combine what is '
                 'left.')
        self.play(FadeOut(expanded), FadeIn(cancelled), run_time=1.0)
        self.beat('cancel', READ_LONG)
        self.play(FadeOut(cancelled), FadeIn(isolated), run_time=1.0)
        self.beat('combine', READ_LONG)

        self.say('Factor out 12. This is the equation of the parabola, (x minus 2) squared equals '
                 '12 times (y plus 1).')
        self.play(FadeOut(isolated), FadeIn(factored), run_time=1.0)
        self.beat('equation', READ_LONG + 1.0)

        # ---- 6. why we care ----------------------------------------------------------------------
        self.say('So the directrix is the rule that builds the equation and shapes the parabola. '
                 'The farther it is from the focus, the wider the parabola.')
        self.beat('purpose', READ_LONG + 1.0)

        self.say('The focus is where a dish or a headlight sends everything. The directrix is '
                 'what decides the shape.')
        self.beat('hold', READ_LONG)
        self.write_marks('parabola_directrix_marks.json')
