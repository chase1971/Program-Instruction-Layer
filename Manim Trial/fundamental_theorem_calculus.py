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
    """Show once, generally and at t=10, why triangle area matches p(t)=t^2."""

    def construct(self):
        velocity_axes = Axes(
            x_range=[0, 10.5, 2], y_range=[0, 21, 5],
            x_length=2.45, y_length=2.75,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([-1.5, .45, 0])
        position_axes = Axes(
            x_range=[0, 10.5, 2], y_range=[0, 105, 25],
            x_length=2.45, y_length=2.75,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([1.5, .45, 0])
        velocity_graph = velocity_axes.plot(
            lambda x: 2 * x, x_range=[0, 10], color=BLUE, stroke_width=5,
        )
        position_graph = position_axes.plot(
            lambda x: x * x, x_range=[0, 10], color=GOLD, stroke_width=5,
        )
        velocity_rule = tex('v(t)=2t', size=32).set_color(BLUE).move_to([-1.5, 2.25, 0])
        position_rule = tex('p(t)=t^2', size=32).set_color(GOLD).move_to([1.5, 2.25, 0])
        left_t = MathTex('t', color=INK, font_size=25).next_to(velocity_axes.x_axis.get_end(), DOWN, buff=.06)
        left_v = MathTex('v', color=INK, font_size=25).next_to(velocity_axes.y_axis.get_end(), RIGHT, buff=.05)
        right_t = MathTex('t', color=INK, font_size=25).next_to(position_axes.x_axis.get_end(), DOWN, buff=.06)
        right_p = MathTex('p', color=INK, font_size=25).next_to(position_axes.y_axis.get_end(), RIGHT, buff=.05)
        headings = VGroup(
            tex(r'\text{AREA UNDER }v(t)', size=26).move_to([-1.5, 2.75, 0]),
            tex(r'\text{POSITION }p(t)', size=26).move_to([1.5, 2.75, 0]),
        )
        self.add(
            headings, velocity_axes, position_axes,
            left_t, left_v, right_t, right_p, velocity_graph, position_graph,
            velocity_rule, position_rule,
        )

        self.say('Compare the area under $v(t)=2t$ with the position function $p(t)=t^2$.')
        self.hold('two_views', READ_LONG)

        def comparison(time, symbolic=False):
            height = 2 * time
            answer = time * time
            area = velocity_axes.get_area(
                velocity_graph, x_range=[0, time], color=FILL_BLUE, opacity=.52,
            )
            height_line = Line(
                velocity_axes.c2p(time, 0), velocity_axes.c2p(time, height),
                color=RED, stroke_width=5,
            )
            velocity_dot = Dot(velocity_axes.c2p(time, height), color=RED, radius=.07)
            position_dot = Dot(position_axes.c2p(time, answer), color=RED, radius=.07)
            position_drop = Line(
                position_axes.c2p(time, 0), position_axes.c2p(time, answer),
                color=RED, stroke_width=3,
            )
            if symbolic:
                left_formula = VGroup(
                    tex('A(T)', '=', r'\frac12(T)(2T)', size=28),
                    tex('=', 'T^2', size=31),
                ).arrange(DOWN, buff=.12).move_to([-1.5, -1.75, 0])
                right_formula = VGroup(
                    tex('p(T)-p(0)', size=28),
                    tex('=', 'T^2-0', '=', 'T^2', size=28),
                ).arrange(DOWN, buff=.12).move_to([1.5, -1.75, 0])
                equality_text = 'T^2'
            else:
                left_formula = VGroup(
                    tex('A(10)', '=', r'\frac12(10)(20)', size=27),
                    tex('=', '100', size=31),
                ).arrange(DOWN, buff=.12).move_to([-1.5, -1.75, 0])
                right_formula = VGroup(
                    tex('p(10)-p(0)', size=27),
                    tex('=', '10^2-0', '=', '100', size=26),
                ).arrange(DOWN, buff=.12).move_to([1.5, -1.75, 0])
                equality_text = r'100\text{ m}'
            left_formula[0][0].set_color(BLUE)
            right_formula[0][0].set_color(GOLD)
            equality = tex(
                r'\text{area}', '=', r'\text{position change}', '=', equality_text,
                size=37,
            ).move_to([0, -2.65, 0])
            equality[-1].set_color(BLUE)
            return VGroup(
                area, height_line, velocity_dot, position_drop, position_dot,
                left_formula, right_formula, equality,
            )

        general = comparison(6, symbolic=True)
        self.say(r'Triangle area equals $p(T)$: $\frac12(T)(2T)=T^2$.')
        self.play(FadeIn(general), run_time=1.3)
        self.hold('general_rule', READ_LONG)

        at_ten = comparison(10)
        self.say('At $T=10$, both triangle area and $p(10)-p(0)$ give $100$ meters.')
        self.play(ReplacementTransform(general, at_ten), run_time=1.35)
        self.hold('t_10', READ_LONG)

        self.write_marks('ftc_triangle_square_marks.json')


class FtcAddedArea(FtcScene):
    """Use v=t(10-t) to make A(t+h)-A(t) visible beside its position function."""

    def construct(self):
        velocity_axes = Axes(
            x_range=[0, 10.5, 2], y_range=[0, 27, 5],
            x_length=2.45, y_length=2.75,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([-1.5, .45, 0])
        position_axes = Axes(
            x_range=[0, 10.5, 2], y_range=[0, 175, 40],
            x_length=2.45, y_length=2.75,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([1.5, .45, 0])
        velocity = lambda x: x * (10 - x)
        position = lambda x: 5 * x * x - x * x * x / 3
        velocity_graph = velocity_axes.plot(velocity, x_range=[0, 10], color=BLUE, stroke_width=5)
        position_graph = position_axes.plot(position, x_range=[0, 10], color=GOLD, stroke_width=5)
        headings = VGroup(
            tex(r'\text{AREA }A(t)', size=26).move_to([-1.5, 2.75, 0]),
            tex(r'\text{POSITION }p(t)', size=26).move_to([1.5, 2.75, 0]),
        )
        velocity_rule = tex('v(t)=t(10-t)', size=29).set_color(BLUE).move_to([-1.5, 2.25, 0])
        position_rule = tex(r'p(t)=5t^2-\frac{t^3}{3}', size=27).set_color(GOLD).move_to([1.5, 2.18, 0])
        labels = VGroup(
            MathTex('t', color=INK, font_size=25).next_to(velocity_axes.x_axis.get_end(), DOWN, buff=.06),
            MathTex('t', color=INK, font_size=25).next_to(position_axes.x_axis.get_end(), DOWN, buff=.06),
        )
        self.add(
            headings, velocity_axes, position_axes, labels,
            velocity_graph, position_graph, velocity_rule, position_rule,
        )

        self.say('For $v(t)=t(10-t)$, the curved region has no rectangle or triangle area formula.')
        geometry_note = tex(r'\text{geometry formula?}', r'\quad\text{none}', size=35).move_to([0, -2.25, 0])
        geometry_note[1].set_color(RED)
        self.play(Write(geometry_note), run_time=1.0)
        self.hold('nonlinear_problem', READ_LONG)

        t0 = 4.0
        h = ValueTracker(2.0)
        old_area = velocity_axes.get_area(velocity_graph, x_range=[0, t0], color=FILL_BLUE, opacity=.38)
        strip = always_redraw(lambda: velocity_axes.get_area(
            velocity_graph,
            x_range=[t0, t0 + h.get_value()],
            color=FILL_GOLD,
            opacity=.72,
        ))
        left_line = Line(
            velocity_axes.c2p(t0, 0), velocity_axes.c2p(t0, velocity(t0)),
            color=GOLD, stroke_width=4,
        )
        width_brace = always_redraw(lambda: Line(
            velocity_axes.c2p(t0, -1.2), velocity_axes.c2p(t0 + h.get_value(), -1.2),
            color=RED, stroke_width=6,
        ))
        h_label = always_redraw(lambda: tex('h', size=34).set_color(RED).next_to(width_brace, DOWN, buff=.08))
        position_gain = always_redraw(lambda: position_axes.plot(
            position,
            x_range=[t0, t0 + h.get_value()],
            color=RED,
            stroke_width=7,
        ))
        position_start = Dot(position_axes.c2p(t0, position(t0)), color=RED, radius=.07)
        position_end = always_redraw(lambda: Dot(
            position_axes.c2p(t0 + h.get_value(), position(t0 + h.get_value())),
            color=RED,
            radius=.07,
        ))

        definition = tex('A(t)', '=', r'\text{area from }0\text{ to }t', size=34).move_to([0, -1.65, 0])
        definition[0].set_color(BLUE)
        self.say('Define $A(t)$ as area from zero to $t$. The point on the right is position $p(t)$.')
        self.play(FadeOut(geometry_note), FadeIn(old_area), FadeIn(position_start), Write(definition), run_time=1.25)
        self.hold('accumulated_area', READ_LONG)

        added = tex(
            r'\underbrace{A(t+h)-A(t)}_{\text{new area}}',
            '=', r'\text{gold strip}', size=31,
        ).move_to([0, -1.75, 0])
        added[0].set_color(GOLD)
        self.say('The gold strip is $A(t+h)-A(t)$. The red segment is the same position change.')
        self.play(
            ReplacementTransform(definition, added), FadeIn(strip), Create(left_line),
            Create(width_brace), FadeIn(h_label), Create(position_gain), FadeIn(position_end),
            run_time=1.35,
        )
        self.hold('added_strip', READ_LONG)

        rectangle = always_redraw(lambda: Rectangle(
            width=abs(velocity_axes.c2p(t0 + h.get_value(), 0)[0] - velocity_axes.c2p(t0, 0)[0]),
            height=abs(velocity_axes.c2p(0, velocity(t0))[1] - velocity_axes.c2p(0, 0)[1]),
            color=RED,
            stroke_width=4,
            fill_opacity=.06,
        ).move_to((velocity_axes.c2p(t0, 0) + velocity_axes.c2p(t0 + h.get_value(), velocity(t0))) / 2))

        approximation = tex('A(t+h)-A(t)', r'\approx', 'v(t)', 'h', size=34).move_to([0, -2.75, 0])
        approximation[2].set_color(BLUE)
        approximation[3].set_color(RED)
        self.say('For short $h$, the strip is almost a rectangle: height $v(t)$ times width $h$.')
        self.play(FadeIn(rectangle), Write(approximation), run_time=1.3)
        self.hold('strip_product', READ_LONG)

        quotient = tex(r'\frac{A(t+h)-A(t)}{h}', r'\approx', 'v(t)', size=38).move_to(approximation)
        quotient[2].set_color(BLUE)
        self.say('Divide by $h$: added area per added time is close to the height $v(t)$.')
        self.play(ReplacementTransform(approximation, quotient), run_time=1.05)
        self.hold('quotient')

        self.say('As $h$ shrinks, the strip and rectangle merge, making the approximation exact.')
        self.play(h.animate.set_value(.25), run_time=2.3, rate_func=linear)
        self.play(Indicate(left_line, color=BLUE, scale_factor=1.08), run_time=.8)
        self.hold('shrunk', READ_LONG)

        derivative = tex(r'\boxed{A^{\prime}(t)=v(t)=p^{\prime}(t)}', size=43).move_to([0, -2.75, 0])
        derivative.set_color(BLUE)
        self.say(r"$A^{\prime}(t)=v(t)$, and $p^{\prime}(t)=v(t)$ too. Therefore area equals position change.")
        self.play(ReplacementTransform(quotient, derivative), FadeOut(rectangle), run_time=1.1)
        self.hold('same_derivative', READ_LONG)

        changing = VGroup(
            old_area, strip, left_line, width_brace, h_label,
            position_gain, position_start, position_end, added, derivative,
        )
        table = VGroup(
            tex('t', r'A(t)', r'p(t)-p(0)', size=28).arrange(RIGHT, buff=.62).move_to([0, -1.35, 0]),
            tex('2', r'17.33', r'17.33', size=28).arrange(RIGHT, buff=.62).move_to([0, -1.78, 0]),
            tex('5', r'83.33', r'83.33', size=28).arrange(RIGHT, buff=.62).move_to([0, -2.18, 0]),
            tex('10', r'166.67', r'166.67', size=28).arrange(RIGHT, buff=.62).move_to([0, -2.58, 0]),
        )
        self.say('At $t=2$, $5$, and $10$, area and position change match. At ten seconds, both are about $166.67$ meters.')
        self.play(FadeOut(changing), FadeIn(table), run_time=1.25)
        self.hold('matching_values', READ_LONG)
        self.write_marks('ftc_added_area_marks.json')


class FtcSqueezeProof(FtcScene):
    """Turn the strip picture into a proof using lower and upper rectangles."""

    def construct(self):
        axes = Axes(
            x_range=[0, 5.2, 1], y_range=[0, 5.0, 1],
            x_length=5.1, y_length=3.25,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([0, .25, 0])
        labels = axis_labels(axes)
        fn = lambda x: .18 * (x - .5) ** 2 + 1.1
        graph = axes.plot(fn, x_range=[0, 5.0], color=BLUE, stroke_width=5)
        heading = tex(r'[t,t+h]', size=44).move_to([0, 2.3, 0])
        self.add(axes, labels, graph, heading)

        self.say('On the short interval $[t,t+h]$, record the lowest and highest velocities.')
        self.hold('interval', READ_LONG)

        t0 = 2.0
        h = ValueTracker(1.5)
        lower = always_redraw(lambda: Rectangle(
            width=axes.x_length * h.get_value() / 5.2,
            height=axes.y_length * fn(t0) / 5.0,
            stroke_color=GOLD,
            fill_color=FILL_GOLD,
            fill_opacity=.26,
            stroke_width=4,
        ).move_to(axes.c2p(t0 + h.get_value() / 2, fn(t0) / 2)))
        upper = always_redraw(lambda: Rectangle(
            width=axes.x_length * h.get_value() / 5.2,
            height=axes.y_length * fn(t0 + h.get_value()) / 5.0,
            stroke_color=RED,
            fill_opacity=0,
            stroke_width=4,
        ).move_to(axes.c2p(t0 + h.get_value() / 2, fn(t0 + h.get_value()) / 2)))
        strip = always_redraw(lambda: axes.get_area(
            graph,
            x_range=[t0, t0 + h.get_value()],
            color=FILL_BLUE,
            opacity=.48,
        ))

        self.say('The real added area is trapped between two rectangle areas.')
        self.play(FadeIn(lower), FadeIn(strip), FadeIn(upper), run_time=1.35)
        self.hold('rectangles', READ_LONG)

        bounds = tex('m_hh', r'\le', 'A(t+h)-A(t)', r'\le', 'M_hh', size=36).move_to([0, -2.22, 0])
        bounds[0].set_color(GOLD)
        bounds[4].set_color(RED)
        self.say('Lowest height times width is below; highest height times width is above.')
        self.play(Write(bounds), run_time=1.25)
        self.hold('area_bounds', READ_LONG)

        divided = tex('m_h', r'\le', r'\frac{A(t+h)-A(t)}{h}', r'\le', 'M_h', size=36).move_to(bounds)
        divided[0].set_color(GOLD)
        divided[4].set_color(RED)
        self.say('Divide every part by the positive width $h$.')
        self.play(ReplacementTransform(bounds, divided), run_time=1.05)
        self.hold('average_bounds')

        self.say('Continuity makes both rectangle heights approach $v(t)$ as $h$ shrinks.')
        self.play(h.animate.set_value(.18), run_time=2.35, rate_func=linear)
        self.hold('squeeze', READ_LONG)

        result = tex('v(t)', r'\le', r'A^{\prime}(t)', r'\le', 'v(t)', size=43).move_to(divided)
        result[0].set_color(BLUE)
        result[4].set_color(BLUE)
        self.say('The squeeze theorem forces the middle rate to equal $v(t)$.')
        self.play(ReplacementTransform(divided, result), run_time=1.1)
        final = tex(r'\boxed{A^{\prime}(t)=v(t)}', size=50).move_to(result)
        self.play(ReplacementTransform(result, final), run_time=.9)
        self.hold('hold', READ_LONG)
        self.write_marks('ftc_squeeze_proof_marks.json')


class FtcPositionConnection(FtcScene):
    """Finish the theorem and connect Riemann rectangles to position change."""

    def construct(self):
        area_rate = tex(r'A^{\prime}(t)', '=', 'v(t)', size=48).move_to([0, 2.15, 0])
        position_rate = tex(r's^{\prime}(t)', '=', 'v(t)', size=48).move_to([0, 1.18, 0])
        area_rate[0].set_color(GOLD)
        position_rate[0].set_color(BLUE)
        self.add(area_rate)

        self.say('We proved the area function has derivative $v(t)$.')
        self.hold('area_rate')

        self.say('Position also has derivative $v(t)$ because velocity is position rate.')
        self.play(Write(position_rate), run_time=1.05)
        self.hold('position_rate', READ_LONG)

        difference = tex(r'\frac{d}{dt}\bigl(s(t)-A(t)\bigr)', '=', '0', size=41).move_to([0, .02, 0])
        self.say('Subtract them: the derivative of their difference is zero.')
        self.play(Write(difference), run_time=1.2)
        self.hold('zero_derivative', READ_LONG)

        constant = tex('s(t)-A(t)', '=', 'C', size=48).move_to([0, -1.05, 0])
        constant[2].set_color(RED)
        self.say('So the difference is constant on the whole interval.')
        self.play(Write(constant), run_time=1.0)
        self.hold('constant')

        initial = tex('A(0)=0', r'\quad\Longrightarrow\quad', 'C=s(0)', size=40).move_to([0, -2.0, 0])
        initial[0].set_color(GOLD)
        self.say('Since accumulated area starts at zero, the constant is the initial position.')
        self.play(Write(initial), run_time=1.15)
        self.hold('initial_position', READ_LONG)

        answer = tex(r'\boxed{A(t)=s(t)-s(0)}', size=48).move_to([0, -2.85, 0])
        answer.set_color(BLUE)
        self.say('Therefore accumulated signed area equals change in position.')
        self.play(Write(answer), run_time=1.15)
        self.hold('theorem', READ_LONG)

        self.say('Riemann sums tell the same story: each rectangle is velocity times time.')
        self.play(
            FadeOut(VGroup(area_rate, position_rate, difference, constant, initial)),
            answer.animate.move_to([0, 2.15, 0]),
            run_time=.9,
        )
        axes = Axes(
            x_range=[0, 6, 1], y_range=[-2.5, 3.5, 1],
            x_length=5.15, y_length=3.2,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([0, -.15, 0])
        graph = axes.plot(lambda x: 2.2 * np.sin(.85 * x) + .35, x_range=[0, 5.8], color=BLUE, stroke_width=4)
        rectangles = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 5.8],
            dx=.58,
            input_sample_type='left',
            stroke_color=INK,
            stroke_width=1.4,
            fill_opacity=.55,
            color=[FILL_BLUE, FILL_GOLD],
        )
        labels = axis_labels(axes)
        self.play(Create(axes), Create(graph), FadeIn(rectangles), FadeIn(labels), run_time=1.6)
        self.hold('riemann_rectangles', READ_LONG)

        sum_line = tex(r'\sum v(t_i)\,\Delta t', r'\longrightarrow', r'\int_0^t v(u)\,du', size=38).move_to([0, -2.42, 0])
        self.say('Adding the rectangles approaches the exact signed area and exact position change.')
        self.play(Write(sum_line), run_time=1.3)
        self.hold('riemann_sum', READ_LONG)

        note = tex(r'\text{distance uses }|v(t)|', size=36).move_to([0, -3.28, 0])
        note.set_color(RED)
        self.say('Negative velocity gives negative area; total distance uses speed instead.')
        self.play(FadeIn(note), run_time=.8)
        self.hold('hold', READ_LONG)
        self.write_marks('ftc_position_connection_marks.json')
