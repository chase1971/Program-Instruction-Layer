"""Parabolas (pre-calc conics): what the directrix is, and how it builds the equation.

Same parabola as ParabolaOpensUp, (x - 2)^2 = 12(y + 1): vertex (2, -1), p = 3, focus (2, 2),
directrix y = -4. The clip opens on the definition:

    a parabola is the set of all points the SAME distance from a fixed point (the focus) as from
    a fixed line (the directrix).

Beats: the definition -> the focus and directrix -> one point on the parabola (at the left edge,
both lengths are 6), why the length down is y + 4 (4 up to the x-axis, then y more) -> the point
moves, the parabola is traced, y + 4 shown again at a second point -> the definition again, with
the vertex (h, k) and p marked -> the graph clears and the general equation is derived in h, k, p one step at a time
(distance formula, square both sides, expand, cancel pairs), then this graph's.
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

import math  # noqa: E402

TAU = 2 * math.pi

from manim import (  # noqa: E402
    CurvedArrow,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Brace,
    Create,
    DashedLine,
    Dot,
    DecimalNumber,
    FadeIn,
    FadeOut,
    Group,
    Indicate,
    Line,
    ReplacementTransform,
    TransformFromCopy,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
    linear,
)

from equations_of_lines import READ_LONG, READ_SHORT, tex  # noqa: E402
from parabola_walkthrough import (  # noqa: E402
    CURVE_COLOR,
    GRAPH_X,
    INK,
    LEFT_X,
    LIST_SIZE,
    OPENS_UP,
    P_COLOR,
    ParabolaOpensUp,
)
from scene_style import PAPER_BLUE, PAPER_GOLD, PAPER_MUTED  # noqa: E402
from solve_steps import op_under, strike_pair  # noqa: E402

FOCUS_COLOR = PAPER_BLUE        # the focus and every distance to it
DIRECTRIX_COLOR = PAPER_GOLD    # the directrix and every distance to it
ROW_Y = (1.5, 0.85)             # the two live distances, above the graph
NUMBER_X = 0.9                  # left edge of the numbers
DEF_Y = 2.35                    # the definition row, above the graph
DERIVE_Y = (2.0, 1.6, .6)       # the two-row stage, the one-row lines, and this graph's equation
DERIVE_SIZE = 32
WORK_Y = .2                     # the (y-k-p)^2 worked out below the equation
RESULT_Y = -1.2                 # and what it multiplies out to


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

        def bracket(x, y0, y1, direction, text, color):
            """A curly bracket beside the vertical span y0..y1 at x, with its label."""
            brace = Brace(Line(c2p(x, y0), c2p(x, y1)), direction, buff=.02, color=color)
            label = tex(text, size=26, color=color)
            brace.put_at_tip(label, buff=.03)
            return brace, label

        focus_dot = found_dot(fx, fy).set_color(FOCUS_COLOR)
        focus_label = tex(r'\text{focus}', size=28, color=FOCUS_COLOR).next_to(focus_dot, UP,
                                                                               buff=.1)
        directrix_line = DashedLine(c2p(GRAPH_X[0], p.directrix), c2p(GRAPH_X[1], p.directrix),
                                    color=DIRECTRIX_COLOR, stroke_width=4, dash_length=.12)
        directrix_label = tex(r'\text{directrix}', size=28, color=DIRECTRIX_COLOR
                              ).next_to(c2p(6.6, p.directrix), DOWN, buff=.06)
        on_curve = lambda x: k + (x - h) ** 2 / p.c
        x_left, x_right, x_second = h - 6., h + 6., h + 5.

        definition = tex(r'\text{focus distance}', '=', r'\text{directrix distance}', size=30)
        definition[0].set_color(FOCUS_COLOR)
        definition[2].set_color(DIRECTRIX_COLOR)
        definition.move_to([0, DEF_Y, 0])

        # ---- 1. the definition, first --------------------------------------------------------
        self.say('Part 1. The definition of a parabola is the set of all points equally distant '
                 'from a fixed point, the focus, and a fixed line, the directrix.')
        self.play(FadeIn(definition), run_time=.8)
        self.beat('definition', READ_LONG + 3.5)

        # ---- 2. the two things it is built around ---------------------------------------------
        self.say('The focus is a fixed point, and the directrix is a fixed line.')
        self.play(FadeIn(plane), run_time=.6)
        self.play(FadeIn(focus_dot, scale=1.6), Write(focus_label), run_time=.7)
        self.play(Create(directrix_line), Write(directrix_label), run_time=.8)
        self.beat('setup', READ_LONG)

        # ---- 3. one point: measure to the focus, then straight down to the directrix -------------
        self.say('Choose any point on the parabola. Its distance to the focus is the length of this segment.')
        probe, xt = self.probe(plane, on_curve, x_left)
        to_focus, to_directrix, dot = probe[0], probe[1], probe[2]
        focus_row, directrix_row = probe[3], probe[4]
        focus_num, directrix_num = probe[5], probe[6]
        self.play(FadeIn(dot), Create(to_focus), FadeIn(focus_row), FadeIn(focus_num),
                  run_time=.8)
        self.beat('focus-length', READ_LONG)

        self.say('Its distance to the directrix is measured straight down, perpendicular to the directrix.')
        self.play(Create(to_directrix), FadeIn(directrix_row), FadeIn(directrix_num),
                  run_time=.8)
        self.beat('directrix-length', READ_LONG)

        # ---- 4. where the length down comes from: 4 + y ------------------------------------------
        y_left = on_curve(x_left)
        brace4, label4 = bracket(x_left, p.directrix, 0, LEFT, '4', DIRECTRIX_COLOR)
        brace_y, label_y = bracket(x_left, 0, y_left, LEFT, 'y', INK)
        total_left = tex('y+4', size=28, color=DIRECTRIX_COLOR).next_to(
            c2p(x_left, (y_left + p.directrix) / 2), RIGHT, buff=.1)
        self.say('The directrix is the line $y=-4$, so the distance from it up to the $x$-axis is $4$.')
        self.play(FadeIn(brace4), FadeIn(label4), run_time=.6)
        self.beat('four', READ_LONG)
        self.say('From the $x$-axis up to the point, the distance is $y$.')
        self.play(FadeIn(brace_y), FadeIn(label_y), run_time=.6)
        self.beat('y-up', READ_LONG)
        self.say('Therefore, the distance from the point to the directrix is $y+4$. Here, $2+4=6$.')
        self.play(FadeIn(total_left), run_time=.5)
        self.beat('y-plus-4', READ_LONG)

        # ---- 5. keep them equal and the parabola draws itself -------------------------------------
        curve = always_redraw(lambda: plane.plot(
            on_curve, x_range=[x_left, max(xt.get_value(), x_left + .02)],
            color=CURVE_COLOR, stroke_width=5))
        self.add(curve)
        self.say('Now move the point so that the two distances always stay equal. The path it '
                 'traces is the parabola.')
        self.play(FadeOut(VGroup(brace4, label4, brace_y, label_y, total_left)),
                  xt.animate.set_value(x_second), run_time=2.0, rate_func=linear)

        y_second = on_curve(x_second)
        brace4b, label4b = bracket(x_second, p.directrix, 0, RIGHT, '4', DIRECTRIX_COLOR)
        brace_yb, label_yb = bracket(x_second, 0, y_second, RIGHT, 'y', INK)
        total_second = tex('y+4', size=28, color=DIRECTRIX_COLOR).next_to(
            c2p(x_second, (y_second + p.directrix) / 2), LEFT, buff=.1)
        self.say('At every point on the curve, the distance to the directrix is $y+4$.')
        self.play(FadeIn(brace4b), FadeIn(label4b), FadeIn(brace_yb), FadeIn(label_yb),
                  FadeIn(total_second), run_time=.7)
        self.beat('again', READ_LONG)
        self.play(FadeOut(VGroup(brace4b, label4b, brace_yb, label_yb)),
                  xt.animate.set_value(x_right), run_time=.8, rate_func=linear)
        self.play(*[FadeOut(m) for m in probe[3:]], xt.animate.set_value(x_second), run_time=.7)
        self.freeze(probe)
        curve.clear_updaters()
        label_pt = tex('(x,y)', size=28, color=INK).next_to(
            c2p(x_second, y_second), UP + RIGHT, buff=.02)
        self.play(FadeIn(label_pt), run_time=.4)
        self.beat('trace', READ_LONG)

        # ---- 6. the definition again, now with the vertex and p marked -----------------------------
        self.say('So every point on the parabola is the same distance from the focus as from '
                 'the directrix.')
        self.play(Indicate(definition[0], color=FOCUS_COLOR, scale_factor=1.15),
                  Indicate(definition[2], color=DIRECTRIX_COLOR, scale_factor=1.15), run_time=1.2)
        self.beat('definition-again', READ_LONG)

        vertex_dot = found_dot(h, k).set_color(INK)
        vertex_label = tex('(h,k)', size=26, color=INK).next_to(vertex_dot, DOWN + RIGHT,
                                                                buff=.05)
        brace_up, label_up = bracket(h, k, fy, LEFT, 'p', P_COLOR)
        brace_dn, label_dn = bracket(h, p.directrix, k, LEFT, 'p', P_COLOR)
        self.say('Let the vertex be $(h,k)$. The focus is a distance $p$ above it, and the directrix is a distance $p$ below it.')
        self.play(FadeIn(vertex_dot), Write(vertex_label), FadeIn(brace_up), FadeIn(label_up),
                  FadeIn(brace_dn), FadeIn(label_dn), run_time=.9)
        self.beat('vertex-p', READ_LONG)
        # ---- 7. part 2: the grid goes, the figure is described in h, k and p ----------------------
        figure = Group(focus_dot, focus_label, directrix_line, directrix_label, curve, to_focus,
                       to_directrix, dot, label_pt, vertex_dot, vertex_label, brace_up, label_up,
                       brace_dn, label_dn)
        self.explain_figure(plane, total_second, figure, bracket, c2p, (h, k), (x_second, y_second))

        # ---- 8. the equation falls out of the definition -----------------------------------------
        # The next caption goes up first, so a Slow-mode hold on the figure is still the figure.
        self.derive()

        # ---- 9. why we care ----------------------------------------------------------------------
        self.say('The directrix is the rule that determines the shape of the parabola. The '
                 'farther it is from the focus, the wider the parabola.')
        self.beat('purpose', READ_LONG + 1.0)

        self.say('The focus is where a dish or a headlight sends everything, while the '
                 'directrix decides the shape.')
        self.beat('hold', READ_LONG)
        self.write_marks('parabola_directrix_marks.json')

    def stage(self, left, right, y, left_color=INK, right_color=INK):
        """The equation as two rows: the left side, then '= right side' under it, left-aligned."""
        top = tex(*left, size=DERIVE_SIZE, color=left_color).move_to([0, y, 0])
        bottom = tex(*right, size=DERIVE_SIZE, color=right_color).next_to(
            top, DOWN, buff=.3, aligned_edge=LEFT)
        return top, bottom

    def strike(self, *terms):
        """Slash the cancelling terms in red, one after the other."""
        slashes = strike_pair(*terms)
        for slash in slashes:
            self.play(Create(slash), run_time=.5)
        return slashes

    def explain_figure(self, plane, total, figure, bracket, c2p, vertex, point):
        """Part 2: drop the grid and the numbers, then show why the distance down is y - k + p."""
        slow = READ_LONG + 1.5
        h, k = vertex
        x2, y2 = point
        lift = UP * .5
        directrix_y = self.problem.directrix

        def lifted(*mobjects):
            return Group(*mobjects).shift(lift)

        self.say('Part 2. To build the equation, remove the grid and look only at the figure: '
                 'the vertex $(h,k)$, the focus, and the directrix.')
        self.play(FadeOut(plane), FadeOut(total), figure.animate.shift(lift), run_time=1.4)
        self.beat('figure', slow)

        self.say('The directrix is a distance $p$ below the vertex, so it is the line $y=k-p$.')
        line_label = tex('y=k-p', size=28, color=DIRECTRIX_COLOR).next_to(
            c2p(-3.4, directrix_y) + lift, DOWN, buff=.08)
        self.play(Indicate(figure[-2], color=P_COLOR, scale_factor=1.2), FadeIn(line_label),
                  run_time=1.2)
        self.beat('directrix-line', slow)

        self.say('The point $(x,y)$ is $y-k$ above the level of the vertex.')
        level = DashedLine(c2p(h, k) + lift, c2p(x2, k) + lift, color=PAPER_MUTED,
                           stroke_width=3, dash_length=.1)
        up_brace, up_label = (lifted(m) for m in bracket(x2, k, y2, RIGHT, 'y-k', INK))
        self.play(Create(level), run_time=.8)
        self.play(FadeIn(up_brace), FadeIn(up_label), run_time=.8)
        self.beat('y-minus-k', slow)

        self.say('From the level of the vertex down to the directrix is another $p$.')
        down_brace, down_label = (lifted(m) for m in bracket(x2, directrix_y, k, RIGHT, 'p',
                                                              P_COLOR))
        self.play(FadeIn(down_brace), FadeIn(down_label), run_time=.8)
        self.beat('p-down', slow)

        self.say('So the distance from $(x,y)$ down to the directrix is $(y-k)+p$, which is '
                 '$y-k+p$.')
        whole_brace, whole_label = (lifted(m) for m in bracket(x2, directrix_y, y2, LEFT, 'y-k+p',
                                                                DIRECTRIX_COLOR))
        whole_label.shift(DOWN * .75)  # below the (h,k) label, still beside its brace
        self.play(FadeIn(whole_brace), FadeIn(whole_label), run_time=1.0)
        self.beat('y-k-plus-p', slow + 1.0)

    def arrows(self, starts, ends, up, color=PAPER_GOLD):
        """Curved arrows from each start term to each end term, arcing above (up) or below."""
        edge = UP if up else DOWN
        angle = -TAU / 4 if up else TAU / 4
        made = VGroup()
        for start in starts:
            for end in ends:
                made.add(CurvedArrow(start.get_edge_center(edge) + edge * .05,
                                     end.get_edge_center(edge) + edge * .05,
                                     angle=angle, color=color, stroke_width=4, tip_length=.15))
        return made

    def expand_left(self, row_top, row_bottom, y):
        """(y-k-p)^2 worked out below the equation, treating y-k as one term, then put back."""
        slow = READ_LONG + 1.5
        self.say('Next, expand $(y-k-p)^2$. Treat $y-k$ as a single term.')
        self.play(Indicate(row_top[1], color=PAPER_GOLD, scale_factor=1.15), run_time=1.0)
        work = tex('(y-k-p)^2', size=DERIVE_SIZE).move_to([0, WORK_Y, 0])
        self.play(TransformFromCopy(row_top[1], work), run_time=1.2)
        self.beat('expand-term', slow)

        self.say('Squaring means multiplying the expression by itself.')
        two = tex(r'\big(', '(y-k)', '-p', r'\big)', r'\big(', '(y-k)', '-p', r'\big)',
                  size=DERIVE_SIZE).move_to([0, WORK_Y, 0])
        self.play(ReplacementTransform(work, two), run_time=1.2)
        self.beat('times-itself', slow)

        self.say('Distribute $y-k$ across each term in the second parentheses.')
        above = self.arrows([two[1]], [two[5], two[6]], up=True)
        self.play(*[Create(a) for a in above], run_time=1.2)
        first = tex('(y-k)^2', '-p(y-k)', size=DERIVE_SIZE).move_to([-.3, RESULT_Y, 0])
        self.play(FadeIn(first), run_time=1.0)
        self.beat('distribute-first', slow)

        self.say('Then distribute $-p$ across each term in the second parentheses.')
        below = self.arrows([two[2]], [two[5], two[6]], up=False)
        self.play(FadeOut(above), *[Create(a) for a in below], run_time=1.2)
        both = tex('(y-k)^2', '-p(y-k)', '-p(y-k)', '+p^2', size=DERIVE_SIZE).move_to(
            [0, RESULT_Y, 0])
        self.play(ReplacementTransform(first, both), run_time=1.2)
        self.beat('distribute-second', slow)

        self.say('Combine the like terms: $-p(y-k)-p(y-k)=-2p(y-k)$.')
        combined = tex('(y-k)^2', '-2p(y-k)', '+p^2', size=DERIVE_SIZE).move_to(
            [0, RESULT_Y, 0])
        self.play(FadeOut(below), ReplacementTransform(both, combined), run_time=1.2)
        self.beat('combine', slow)

        self.say('Substitute this back into the equation.')
        top5, bottom5 = self.stage(['(x-h)^2', '+(y-k)^2', '-2p(y-k)', '+p^2'],
                                   ['=(y-k+p)^2'], y)
        self.play(ReplacementTransform(row_top, top5), ReplacementTransform(row_bottom, bottom5),
                  FadeOut(Group(two, combined)), run_time=1.4)
        self.beat('expand-left', slow)
        return top5, bottom5

    def derive(self):
        """Distance to the focus = distance down to the directrix, simplified one step at a time."""
        slow = READ_LONG + 1.5
        y = DERIVE_Y[0]
        dist = r'\sqrt{(x-h)^2+(y-(k+p))^2}'
        dist2 = r'\sqrt{(x-h)^2+(y-k-p)^2}'

        self.say('If the focus is at $(h,k+p)$, then the distance from $(x,y)$ to the '
                 'focus is found by applying the distance formula.')
        top, bottom = self.stage([dist], ['=y-(k-p)'], y, FOCUS_COLOR, DIRECTRIX_COLOR)
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not self.note])),
                  run_time=.8)
        self.play(Write(top), run_time=1.5)
        self.beat('distance-formula', slow)

        self.say('Set this equal to the distance down to the directrix, which is $y-(k-p)$.')
        self.play(Write(bottom), run_time=1.2)
        self.beat('set-equal', slow)

        self.say('Distribute the negative signs on both sides.')
        top2, bottom2 = self.stage([dist2], ['=y-k+p'], y, FOCUS_COLOR, DIRECTRIX_COLOR)
        self.play(ReplacementTransform(top, top2), ReplacementTransform(bottom, bottom2),
                  run_time=1.2)
        self.beat('distribute', slow)

        self.say('Square both sides to eliminate the square root.')
        top3, bottom3 = self.stage([r'\left(' + dist2 + r'\right)^2'], ['=(y-k+p)^2'], y,
                                   FOCUS_COLOR, DIRECTRIX_COLOR)
        self.play(ReplacementTransform(top2, top3), ReplacementTransform(bottom2, bottom3),
                  run_time=1.2)
        self.beat('square', slow)

        self.say('Squaring a square root leaves just the expression underneath it.')
        top4, bottom4 = self.stage(['(x-h)^2', '+(y-k-p)^2'], ['=(y-k+p)^2'], y)
        self.play(ReplacementTransform(top3, top4), ReplacementTransform(bottom3, bottom4),
                  run_time=1.2)
        self.beat('unroot', slow)

        top5, bottom5 = self.expand_left(top4, bottom4, y)

        self.say('The right side expands the same way, with $+p$ in place of $-p$.')
        _, bottom6 = self.stage(['(x-h)^2', '+(y-k)^2', '-2p(y-k)', '+p^2'],
                                ['=', '(y-k)^2', '+2p(y-k)', '+p^2'], y)
        self.play(ReplacementTransform(bottom5, bottom6), run_time=1.4)
        self.beat('expand-right', slow)

        self.say('The term $(y-k)^2$ appears on both sides, so subtracting it from both sides cancels it.')
        first = self.strike(top5[1], bottom6[1])
        self.beat('cancel-square', slow)

        self.say('The term $p^2$ also appears on both sides, so it cancels as well.')
        second = self.strike(top5[3], bottom6[3])
        self.beat('cancel-p-squared', slow)

        self.say('This leaves the following equation.')
        kept = tex('(x-h)^2', '-2p(y-k)', '=', '2p(y-k)', size=DERIVE_SIZE).move_to(
            [0, DERIVE_Y[1], 0])
        self.play(TransformFromCopy(top5[0], kept[0]), TransformFromCopy(top5[2], kept[1]),
                  TransformFromCopy(bottom6[0], kept[2]), TransformFromCopy(bottom6[2], kept[3]),
                  FadeOut(Group(top5, bottom6, first, second)), run_time=1.4)
        self.beat('left-over', slow)

        self.say('Add $2p(y-k)$ to both sides.')
        add_left = op_under('+', '2p(y-k)', kept[1])
        add_right = op_under('+', '2p(y-k)', kept[3])
        self.play(FadeIn(add_left), FadeIn(add_right), run_time=.9)
        self.beat('add-both', slow)

        self.say('On the left, $-2p(y-k)+2p(y-k)=0$, so those terms cancel.')
        zero = self.strike(kept[1], add_left)
        self.beat('cancel-left', slow)

        self.say('On the right, $2p(y-k)+2p(y-k)=4p(y-k)$.')
        final = tex('(x-h)^2', '=', '4p(y-k)', size=DERIVE_SIZE + 8).move_to(
            [0, DERIVE_Y[1], 0])
        self.play(FadeOut(Group(kept, add_left, add_right, zero)), FadeIn(final), run_time=1.0)
        self.beat('four-p', slow)

        self.say('This is the standard form of the equation of a parabola that opens up.')
        self.play(Indicate(final, color=P_COLOR, scale_factor=1.08), run_time=1.2)
        self.beat('equation', slow)

        self.say('For this graph, $h=2$, $k=-1$, and $p=3$.')
        example = tex('(x-2)^2', '=', '12(y+1)', size=DERIVE_SIZE + 2).move_to(
            [0, DERIVE_Y[2], 0])
        self.play(FadeIn(example), run_time=.8)
        self.beat('example', slow)
