"""Four portal clips explaining why accumulated velocity area equals position change.

The clips follow the proof in four visual stages:
1. The triangle under v(t)=2t has both a time base and a time-dependent height.
2. A thin added-area strip has area approximately v(t)h.
3. Lower and upper rectangles squeeze the strip's average height to v(t).
4. The area and position functions have the same derivative, so they differ by a constant.

PORTRAIT: built for the 1080 x 1350 student-portal player. Each caption is a Slow-mode
step, and every scene ends on a complete readable board.
"""

from portrait_frame import apply_portrait_frame

apply_portrait_frame()

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    Axes,
    Create,
    DecimalNumber,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    Indicate,
    LEFT,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    Scene,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    linear,
)

from math_notation import mathtex  # noqa: E402
from scene_style import (  # noqa: E402
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    PAPER_RED,
    Narrated,
    apply_portal_paper_background,
)

apply_portal_paper_background()

INK = PAPER_INK
BLUE = PAPER_BLUE
GOLD = PAPER_GOLD
RED = PAPER_RED
FILL_BLUE = '#90CAF9'
FILL_GOLD = '#FFCC80'
READ_SHORT = 0.9
READ_LONG = 1.35
MAX_WIDTH = 5.75


def tex(*parts, size=42):
    result = mathtex(*parts, font_size=size, color=INK)
    if result.width > MAX_WIDTH:
        result.scale(MAX_WIDTH / result.width)
    return result


def axis_labels(axes, x_label='t', y_label='v(t)'):
    x = MathTex(x_label, color=INK, font_size=30).next_to(axes.x_axis.get_end(), DOWN, buff=.08)
    y = MathTex(y_label, color=INK, font_size=30).next_to(axes.y_axis.get_end(), RIGHT, buff=.08)
    return VGroup(x, y)


class FtcScene(Narrated, Scene):
    caption_color = INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.92

    def hold(self, name, seconds=READ_SHORT):
        self.wait(seconds)
        self.mark(name)


class FtcTriangleSquare(FtcScene):
    """Derive s(t)=t^2 from the triangle under v(t)=2t, then check both at t=10."""

    def construct(self):
        def make_axes(cx, ymax, ystep):
            return Axes(
                x_range=[0, 10.5, 2], y_range=[0, ymax, ystep],
                x_length=2.45, y_length=2.75,
                axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
            ).move_to([cx, .45, 0])

        def small(label, anchor, direction, buff=.06):
            return MathTex(label, color=INK, font_size=25).next_to(anchor, direction, buff=buff)

        velocity_axes = make_axes(0, 21, 5)
        position_axes = make_axes(1.38, 105, 25)
        velocity_graph = velocity_axes.plot(
            lambda x: 2 * x, x_range=[0, 10], color=BLUE, stroke_width=5,
        )
        velocity_rule = tex('v(t)=2t', size=32).set_color(BLUE).move_to([0, 2.25, 0])
        velocity_heading = tex(r'\text{AREA UNDER }v(t)', size=26).move_to([0, 2.75, 0])
        left_t = small('t', velocity_axes.x_axis.get_end(), RIGHT, .14)
        left_v = small('v', velocity_axes.y_axis.get_end(), RIGHT, .05)
        left = VGroup(velocity_heading, velocity_axes, velocity_graph, velocity_rule, left_t, left_v)
        self.add(left)

        def triangle_parts(time):
            axes = velocity_axes
            area = axes.get_area(velocity_graph, x_range=[0, time], color=FILL_BLUE, opacity=.52)
            height_line = Line(axes.c2p(time, 0), axes.c2p(time, 2 * time), color=RED, stroke_width=5)
            dot = Dot(axes.c2p(time, 2 * time), color=RED, radius=.07)
            base_label = small('T' if time == 6 else '10', axes.c2p(time, 0), DOWN)
            height_label = small('2T' if time == 6 else '20', height_line, RIGHT, .08)
            return area, height_line, dot, base_label, height_label

        def area_lines(time, cx):
            if time == 6:
                first = tex('A(T)', '=', r'\int_0^T 2t\,dt', size=28)
                second = tex('=', r'\frac12(T)(2T)', '=', 'T^2', size=28)
            else:
                first = tex('A(10)', '=', r'\int_0^{10} 2t\,dt', size=26)
                second = tex('=', r'\frac12(10)(20)', '=', '100', size=26)
            first[0].set_color(BLUE)
            first.move_to([cx, -1.65, 0])
            second.move_to([cx, -2.45, 0])
            return first, second

        self.say('A car moves with velocity $v(t)=2t$. We want the area under it from $0$ to $T$.')
        self.hold('velocity', READ_LONG)

        area, height_line, vdot, base_label, height_label = triangle_parts(6)
        self.say('From $0$ to $T$ the area is a triangle with base $T$ and height $2T$.')
        self.play(FadeIn(area), Create(height_line), FadeIn(vdot), run_time=1.1)
        self.play(FadeIn(base_label), FadeIn(height_label), run_time=.5)
        self.hold('triangle', READ_SHORT)

        line_one, line_two = area_lines(6, 0)
        self.say('The area function is the integral of $v$ from $0$ to $T$.')
        self.play(Write(line_one), run_time=1.2)
        self.hold('integral', READ_LONG)

        self.say(r'Triangle area is $\frac12$ base times height, so we get $T^2$.')
        self.play(Write(line_two), run_time=1.4)
        self.play(Indicate(line_two[-1], color=BLUE, scale_factor=1.25), run_time=.9)
        self.hold('area_formula', READ_LONG)

        position_heading = tex(r'\text{POSITION }s(t)', size=26).move_to([1.5, 2.75, 0])
        position_rule = tex('s(t)=t^2', size=32).set_color(GOLD).move_to([1.5, 2.25, 0])
        position_graph = position_axes.plot(
            lambda x: x * x, x_range=[0, 10], color=GOLD, stroke_width=5,
        )
        right_t = small('t', position_axes.x_axis.get_end(), RIGHT, .14)
        right_s = small('s', position_axes.y_axis.get_end(), RIGHT, .05)
        position_dot = Dot(position_axes.c2p(6, 36), color=RED, radius=.07)
        position_drop = Line(position_axes.c2p(6, 0), position_axes.c2p(6, 36), color=RED, stroke_width=3)

        left_all = VGroup(
            left, area, height_line, vdot, base_label, height_label, line_one, line_two,
        )
        self.say('This area function is the position function: $s(t)=t^2$.')
        self.play(left_all.animate.shift(LEFT * 1.5), run_time=1.0)
        self.play(
            FadeIn(position_heading), FadeIn(position_axes), FadeIn(right_t), FadeIn(right_s),
            run_time=.8,
        )
        self.play(Create(position_graph), run_time=1.5)
        self.play(Write(position_rule), FadeIn(position_drop), FadeIn(position_dot), run_time=1.0)
        self.hold('position', READ_LONG)

        n_area, n_line, n_dot, n_base, n_height = triangle_parts(10)
        n_first, n_second = area_lines(10, -1.5)
        ten_dot = Dot(position_axes.c2p(10, 100), color=RED, radius=.07)
        ten_drop = Line(position_axes.c2p(10, 0), position_axes.c2p(10, 100), color=RED, stroke_width=3)
        right_first = tex('s(10)-s(0)', size=26)
        right_second = tex('=', '10^2-0', '=', '100', size=26)
        right_first[0].set_color(GOLD)
        right_first.move_to([1.5, -1.65, 0])
        right_second.move_to([1.5, -2.45, 0])
        equality = tex(
            r'\text{area}', '=', r'\text{position change}', '=', r'100\text{ m}', size=37,
        ).move_to([0, -3.25, 0])
        equality[-1].set_color(BLUE)
        self.say('At $T=10$, the area and $s(10)-s(0)$ both give $100$ meters.')
        self.play(
            ReplacementTransform(area, n_area), ReplacementTransform(height_line, n_line),
            ReplacementTransform(vdot, n_dot), ReplacementTransform(base_label, n_base),
            ReplacementTransform(height_label, n_height),
            ReplacementTransform(line_one, n_first), ReplacementTransform(line_two, n_second),
            ReplacementTransform(position_drop, ten_drop), ReplacementTransform(position_dot, ten_dot),
            run_time=1.4,
        )
        self.play(Write(right_first), run_time=.8)
        self.play(Write(right_second), run_time=1.0)
        self.play(FadeIn(equality), run_time=.9)
        self.hold('t_10', READ_LONG)

        self.write_marks('ftc_triangle_square_marks.json')


class FtcAddedArea(FtcScene):
    """No geometry formula for v=t(10-t): Riemann sums, the limit, then s(10)-s(0)."""

    def construct(self):
        velocity = lambda x: x * (10 - x)
        position = lambda x: 5 * x * x - x * x * x / 3
        riemann_sum = lambda dx: sum(velocity(i * dx) * dx for i in range(round(10 / dx)))

        axes = Axes(
            x_range=[0, 10.5, 2], y_range=[0, 27, 5],
            x_length=5.0, y_length=2.9,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([0, .35, 0])
        graph = axes.plot(velocity, x_range=[0, 10], color=BLUE, stroke_width=5)
        heading = tex(r'\text{VELOCITY }v(t)', size=28).move_to([0, 2.75, 0])
        rule = tex('v(t)=t(10-t)', size=32).set_color(BLUE).move_to([0, 2.25, 0])
        t_label = MathTex('t', color=INK, font_size=26).next_to(axes.x_axis.get_end(), RIGHT, buff=.14)
        v_label = MathTex('v', color=INK, font_size=26).next_to(axes.y_axis.get_end(), RIGHT, buff=.06)
        chart = VGroup(axes, graph)
        self.add(chart, heading, rule, t_label, v_label)

        def rectangles(dx, stroke=1.5):
            return axes.get_riemann_rectangles(
                graph, x_range=[0, 10], dx=dx, input_sample_type='left',
                color=FILL_BLUE, fill_opacity=.6, stroke_width=stroke, stroke_color=INK,
            )

        def readout(n, dx, text):
            row = tex(f'n={n}', rf'\quad\Delta t={dx}', rf'\quad\text{{sum}}\approx {text}', size=30)
            row[2].set_color(BLUE)
            return row.move_to([0, -1.85, 0])

        self.say('A car moves with velocity $v(t)=t(10-t)$. How far does it travel in 10 seconds?')
        self.hold('problem', READ_LONG)

        no_formula = tex(r'\text{geometry formula for this area?}', r'\quad\text{none}', size=28).move_to([0, -1.85, 0])
        no_formula[1].set_color(RED)
        self.say('Distance is the area under the curve, but this curved region has no geometry formula.')
        shade = axes.get_area(graph, x_range=[0, 10], color=FILL_BLUE, opacity=.3)
        self.play(FadeIn(shade), Write(no_formula), run_time=1.2)
        self.hold('no_formula', READ_LONG)

        n_five = rectangles(2)
        row = readout(5, 2, f'{riemann_sum(2):.2f}')
        self.say('So we approximate it with rectangles of width $\\Delta t$ and height $v(t_i)$.')
        self.play(FadeOut(no_formula), FadeOut(shade), FadeIn(n_five), FadeIn(row), run_time=1.4)
        self.hold('rectangles', READ_LONG)

        product = tex(r'v(t_i)\,\Delta t', r'=\text{velocity}\times\text{time}=\text{distance}', size=30).move_to([0, -2.75, 0])
        product[0].set_color(BLUE)
        marked = n_five[2]
        self.say('Each rectangle is velocity times time, a short distance. Their sum approximates the total.')
        self.play(marked.animate.set_fill(GOLD, opacity=.85), Write(product), run_time=1.2)
        self.hold('one_rectangle', READ_LONG)

        self.say('Use more, thinner rectangles, and the fit gets better.')
        current, current_row = n_five, row
        self.play(FadeOut(product), run_time=.5)
        for n, dx in [(10, 1), (20, .5), (40, .25)]:
            nxt, nxt_row = rectangles(dx), readout(n, dx, f'{riemann_sum(dx):.2f}')
            self.play(
                ReplacementTransform(current, nxt), ReplacementTransform(current_row, nxt_row),
                run_time=1.1,
            )
            self.wait(.35)
            current, current_row = nxt, nxt_row
        self.hold('shrinking', READ_SHORT)

        limit_rects = rectangles(.1, stroke=0)
        limit_line = tex(r'\lim_{n\to\infty}\sum_{i=1}^{n}v(t_i)\,\Delta t', size=32).move_to([0, -1.9, 0])
        self.say(r'Instead of stopping at a finite number, take the limit as $\Delta t\to 0$.')
        self.play(ReplacementTransform(current, limit_rects), ReplacementTransform(current_row, limit_line), run_time=1.5)
        self.hold('limit', READ_LONG)

        integral = tex(r'=\int_0^{10}v(t)\,dt', size=36).move_to([0, -2.95, 0])
        integral.set_color(BLUE)
        self.say('That limit is the definite integral of $v$ from $0$ to $10$.')
        self.play(Write(integral), run_time=1.2)
        self.hold('integral', READ_LONG)

        displacement = tex(
            r'\int_0^{10}v(t)\,dt', '=', 's(10)-s(0)', size=34,
        ).move_to([0, -1.6, 0])
        displacement[0].set_color(BLUE)
        displacement[2].set_color(GOLD)
        definition = tex(
            r'\text{displacement}=\text{final position}-\text{initial position}', size=26,
        ).move_to([0, -2.7, 0])
        self.say('We saw that displacement is final position minus initial position: $s(10)-s(0)$.')
        self.play(
            FadeOut(limit_line), FadeOut(integral), FadeIn(displacement), Write(definition),
            run_time=1.5,
        )
        self.hold('displacement', READ_LONG)

        unknown = tex('s(t)', '=', '?', size=36).move_to([0, -2.7, 0])
        unknown[0].set_color(GOLD)
        unknown[2].set_color(RED)
        self.say('To calculate $s(10)$ and $s(0)$, we need the position function $s(t)$.')
        self.play(ReplacementTransform(definition, unknown), run_time=1.0)
        self.hold('need_position', READ_LONG)

        antiderivative = tex(r's^{\prime}(t)=v(t)', size=36).move_to([0, -2.7, 0])
        antiderivative.set_color(GOLD)
        self.say('We get it with the antiderivative: $s(t)$ is the function whose derivative is $v(t)$.')
        self.play(ReplacementTransform(unknown, antiderivative), run_time=1.0)
        self.hold('antiderivative', READ_LONG)

        rule_s = tex(r's(t)=5t^2-\frac{t^3}{3}', size=34).set_color(GOLD).move_to([0, -2.7, 0])
        result = tex('s(10)-s(0)', '=', '166.67-0', '=', '166.67', size=30).move_to([0, -3.45, 0])
        result[0].set_color(GOLD)
        self.say('Its derivative is $10t-t^2=v(t)$, and $s(10)-s(0)=166.67$, matching our sums.')
        self.play(ReplacementTransform(antiderivative, rule_s), run_time=1.0)
        self.play(Write(result), run_time=1.2)
        self.hold('solution', READ_LONG)
        self.write_marks('ftc_added_area_marks.json')


class FtcSqueezeProof(FtcScene):
    """The proof on v=t(10-t): the added strip, then the squeeze gives A'(t)=v(t)."""

    def construct(self):
        velocity = lambda x: x * (10 - x)
        axes = Axes(
            x_range=[0, 10.5, 2], y_range=[0, 27, 5],
            x_length=5.0, y_length=2.9,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([0, .35, 0])
        graph = axes.plot(velocity, x_range=[0, 10], color=BLUE, stroke_width=5)
        heading = tex(r'\text{VELOCITY }v(t)', size=28).move_to([0, 2.75, 0])
        rule = tex('v(t)=t(10-t)', size=32).set_color(BLUE).move_to([0, 2.25, 0])
        t_label = MathTex('t', color=INK, font_size=26).next_to(axes.x_axis.get_end(), RIGHT, buff=.14)
        v_label = MathTex('v', color=INK, font_size=26).next_to(axes.y_axis.get_end(), RIGHT, buff=.06)
        self.add(axes, graph, heading, rule, t_label, v_label)

        t0 = 2.0
        h = ValueTracker(2.0)
        bottom = lambda value: axes.c2p(value, 0)
        old_area = axes.get_area(graph, x_range=[0, t0], color=FILL_BLUE, opacity=.45)
        strip = always_redraw(lambda: axes.get_area(
            graph, x_range=[t0, t0 + h.get_value()], color=FILL_GOLD, opacity=.8,
        ))
        t_mark = tex('t', size=28).next_to(bottom(t0), DOWN, buff=.08, aligned_edge=RIGHT)
        end_mark = always_redraw(lambda: tex('t+h', size=28).next_to(
            bottom(t0 + h.get_value()), DOWN, buff=.08, aligned_edge=LEFT,
        ))

        def box(height_at, color, fill):
            return always_redraw(lambda: Rectangle(
                width=abs(bottom(t0 + h.get_value())[0] - bottom(t0)[0]),
                height=abs(axes.c2p(0, height_at(h.get_value()))[1] - axes.c2p(0, 0)[1]),
                stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill,
            ).move_to((bottom(t0) + axes.c2p(t0 + h.get_value(), height_at(h.get_value()))) / 2))

        self.say('A car moves with velocity $v(t)=t(10-t)$. Let $A(t)$ be the area under it from $0$ to $t$.')
        definition = tex('A(t)', '=', r'\int_0^t v(u)\,du', size=34).move_to([0, -1.85, 0])
        definition[0].set_color(BLUE)
        self.play(FadeIn(old_area), FadeIn(t_mark), Write(definition), run_time=1.3)
        self.hold('accumulated_area', READ_LONG)

        added = tex('A(t+h)-A(t)', '=', r'\text{gold strip}', size=34).move_to([0, -1.85, 0])
        added[0].set_color(GOLD)
        self.say('Now let time run a little longer, by $h$. The new gold strip has area $A(t+h)-A(t)$.')
        self.play(
            ReplacementTransform(definition, added), FadeIn(strip), FadeIn(end_mark), run_time=1.3,
        )
        self.hold('added_strip', READ_LONG)

        guess = box(lambda _: velocity(t0), RED, .08)
        approximation = tex('A(t+h)-A(t)', r'\approx', 'v(t)', 'h', size=36).move_to([0, -2.75, 0])
        approximation[2].set_color(BLUE)
        approximation[3].set_color(RED)
        self.say('For short $h$ the strip is almost a rectangle: height $v(t)$ times width $h$.')
        self.play(FadeIn(guess), Write(approximation), run_time=1.3)
        self.hold('strip_product', READ_LONG)

        quotient = tex(r'\frac{A(t+h)-A(t)}{h}', r'\approx', 'v(t)', size=40).move_to(approximation)
        quotient[2].set_color(BLUE)
        self.say('Divide by $h$: added area per added time is close to $v(t)$.')
        self.play(ReplacementTransform(approximation, quotient), run_time=1.05)
        self.hold('quotient', READ_LONG)

        self.say('But "close" is not a proof. So we trap the strip between two rectangles.')
        self.play(FadeOut(guess), FadeOut(added), run_time=.6)
        lower = box(lambda _: velocity(t0), GOLD, .22)
        upper = box(lambda size: velocity(t0 + size), RED, 0)
        self.play(FadeIn(lower), FadeIn(upper), run_time=1.2)
        self.hold('rectangles', READ_LONG)

        bounds = tex('m_hh', r'\le', 'A(t+h)-A(t)', r'\le', 'M_hh', size=36).move_to([0, -1.85, 0])
        bounds[0].set_color(GOLD)
        bounds[4].set_color(RED)
        self.say('Lowest height times width is below the strip. Highest height times width is above.')
        self.play(FadeOut(quotient), Write(bounds), run_time=1.25)
        self.hold('area_bounds', READ_LONG)

        divided = tex('m_h', r'\le', r'\frac{A(t+h)-A(t)}{h}', r'\le', 'M_h', size=36).move_to([0, -2.75, 0])
        divided[0].set_color(GOLD)
        divided[4].set_color(RED)
        self.say('Divide every part by the positive width $h$.')
        self.play(Write(divided), run_time=1.05)
        self.hold('average_bounds', READ_LONG)

        self.say('Continuity makes both rectangle heights approach $v(t)$ as $h$ shrinks.')
        self.play(h.animate.set_value(.2), run_time=4.5, rate_func=linear)
        self.hold('squeeze', 2.5)

        result = tex('v(t)', r'\le', r'A^{\prime}(t)', r'\le', 'v(t)', size=40).move_to([0, -2.5, 0])
        result[0].set_color(BLUE)
        result[4].set_color(BLUE)
        self.say('Both bounds become $v(t)$, so the squeeze theorem traps the middle rate between them.')
        self.play(FadeOut(bounds), ReplacementTransform(divided, result), run_time=2.0)
        self.hold('trapped', 3.0)

        final = tex(r'\boxed{A^{\prime}(t)=v(t)}', size=50).move_to([0, -3.25, 0])
        self.say('So the rate the area grows is exactly the velocity: $A^{\prime}(t)=v(t)$.')
        self.play(Write(final), run_time=1.8)
        self.hold('hold', 3.0)
        self.write_marks('ftc_squeeze_proof_marks.json')
