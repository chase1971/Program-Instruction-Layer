"""FTC clip 6: the average value of a function, using the hiking-trail elevation example.

PORTRAIT: built for the 1080 x 1350 student-portal player. Each caption is a Slow-mode step.
Story: average of a finite list = sum / count, so average of a function = integral / length.
A rectangle of height f-bar over [a, b] has the same net area as the region under the curve.
Example: f(x)=60x^3-650x^2+1200x+4500 on [0, 5] gives 3958 1/3 ft.
"""

from fundamental_theorem_calculus import (
    BLUE, FILL_BLUE, FILL_GOLD, GOLD, INK, RED, FtcScene, tex,
)
from manim import (
    Axes, DashedLine, DOWN, FadeIn, FadeOut, MathTex, RIGHT, ReplacementTransform,
    ValueTracker, VGroup, Write, always_redraw, linear,
)

A, B = 0.0, 5.0
AVERAGE = 3958 + 1 / 3
START_HEIGHT = 5400


def f(x):
    return 60 * x ** 3 - 650 * x ** 2 + 1200 * x + 4500


class FtcAverageValue(FtcScene):
    """Slide a rectangle's height until its area matches the area under the trail profile."""

    def construct(self):
        title = tex(r'\text{AVERAGE VALUE OF A FUNCTION}', size=30).move_to([0, 2.75, 0])

        def note(text, y, size=26, color=INK):
            return tex(r'\text{' + text + '}', size=size).move_to([0, y, 0]).set_color(color)

        definition = tex(
            r'\bar f', '=', r'\frac{1}{b-a}', r'\int_a^b f(x)\,dx', size=38,
        ).move_to([0, 1.9, 0])
        definition[0].set_color(GOLD)
        definition[3].set_color(BLUE)

        # ---- the definition, as the average of a finite list
        finite = tex(r'\text{average of numbers}=\frac{\text{sum}}{\text{how many}}', size=28).move_to([0, 1.0, 0])
        self.say('The average of a list of numbers is the sum divided by how many there are.')
        self.play(FadeIn(title), Write(finite), run_time=1.5)
        self.hold('finite_average', 3.4)

        self.say('For a function, the integral is the total, and $b-a$ is how long it runs.')
        self.play(Write(definition), run_time=1.6)
        self.hold('definition', 3.6)
        self.play(FadeOut(finite), run_time=.5)

        # ---- the example
        problem = tex(r'f(x)=60x^3-650x^2+1200x+4500', size=26).move_to([0, 1.25, 0])
        problem[0].set_color(BLUE)
        domain = note('elevation in feet, $x$ in miles, $0\\le x\\le 5$', .55, size=24)
        self.say('Example: a hiking trail has elevation $f(x)$ feet, with $x$ miles along the trail, $0\\le x\\le5$.')
        self.play(ReplacementTransform(definition, problem), Write(domain), run_time=1.5)
        self.hold('problem', 3.6)

        axes = Axes(
            x_range=[0, 5.7, 1], y_range=[0, 6500, 1000], x_length=5.0, y_length=2.4,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([.1, -.55, 0])
        graph = axes.plot(f, x_range=[A, B], color=BLUE, stroke_width=5)
        x_axis_label = MathTex('x', color=INK, font_size=26).next_to(axes.x_axis.get_end(), RIGHT, buff=.12)
        y_axis_label = MathTex('f', color=INK, font_size=26).next_to(axes.y_axis.get_end(), RIGHT, buff=.06)
        zero = MathTex('0', color=INK, font_size=24).next_to(axes.c2p(0, 0), DOWN, buff=.08)
        five = MathTex('5', color=INK, font_size=24).next_to(axes.c2p(5, 0), DOWN, buff=.08)
        base = VGroup(axes, graph, x_axis_label, y_axis_label, zero, five)
        area = axes.get_area(graph, x_range=[A, B], color=FILL_BLUE, opacity=.5)

        self.say('Graph the trail. It climbs a little, then falls from about 5000 feet to under 2000.')
        self.play(FadeOut(domain), problem.animate.move_to([0, 2.25, 0]), FadeIn(base), run_time=1.6)
        self.hold('graph', 3.2)

        integral_line = tex(r'\int_0^5 f(x)\,dx', r'=\text{net area under the curve}', size=28).move_to([0, -2.45, 0])
        integral_line[0].set_color(BLUE)
        self.say('The integral from $0$ to $5$ is the net area of the region under the curve.')
        self.play(FadeIn(area), Write(integral_line), run_time=1.5)
        self.hold('net_area', 3.4)

        # ---- the rectangle with the same area
        height = ValueTracker(START_HEIGHT)
        rect = always_redraw(lambda: axes.get_area(
            axes.plot(lambda _x: height.get_value(), x_range=[A, B]),
            x_range=[A, B], color=FILL_GOLD, opacity=.55,
        ))
        top_line = always_redraw(lambda: DashedLine(
            axes.c2p(A, height.get_value()), axes.c2p(B + .25, height.get_value()),
            color=GOLD, stroke_width=4,
        ))
        height_label = always_redraw(lambda: MathTex(r'\bar f', color=GOLD, font_size=28).next_to(
            axes.c2p(B + .25, height.get_value()), RIGHT, buff=.08,
        ))
        same_area = tex(r'\text{rectangle height}=\bar f', size=28).move_to([0, -2.45, 0])
        same_area[0].set_color(GOLD)
        self.say('Now build a rectangle on the same base, $0$ to $5$, with some height $\\bar f$.')
        self.add(rect, top_line, height_label)
        self.play(FadeIn(rect), FadeIn(top_line), FadeIn(height_label), ReplacementTransform(integral_line, same_area), run_time=1.4)
        self.hold('rectangle', 3.4)

        self.say('Lower the height until the rectangle has the same area as the region.')
        self.play(height.animate.set_value(AVERAGE), run_time=4.0, rate_func=linear)
        self.hold('match', 3.6)

        trade = note('area above the line fills the dip below it', -2.45, size=26)
        self.say('The gold above the curve fills the gap below it. The areas match, so $\\bar f$ is the average height.')
        self.play(ReplacementTransform(same_area, trade), run_time=1.2)
        self.hold('balance', 3.6)

        # ---- the relationship
        equal = tex(r'(b-a)\,\bar f', '=', r'\int_a^b f(x)\,dx', size=34).move_to([0, -2.45, 0])
        equal[0].set_color(GOLD)
        equal[2].set_color(BLUE)
        self.say('Rectangle area is $(b-a)\\bar f$. Setting it equal to the integral and dividing by $b-a$ gives the definition.')
        self.play(ReplacementTransform(trade, equal), run_time=1.5)
        self.hold('relationship', 4.0)

        # ---- compute it (graph clears so the algebra has room)
        self.play(FadeOut(VGroup(equal, rect, top_line, height_label, area, base)), run_time=.8)
        step1 = tex(
            r'\bar f', '=', r'\frac15', r'\int_0^5(60x^3-650x^2+1200x+4500)\,dx', size=28,
        ).move_to([0, 1.2, 0])
        step1[0].set_color(GOLD)
        self.say('Use the definition with $a=0$ and $b=5$.')
        self.play(Write(step1), run_time=1.6)
        self.hold('set_up', 3.6)

        step2 = tex(
            '=', r'\frac15', r'\left(15x^4-\frac{650}{3}x^3+600x^2+4500x\right)\Big|_0^5', size=28,
        ).move_to([0, .1, 0])
        step2_note = note('Fundamental Theorem: antiderivative at 5 minus at 0', -.8, size=24, color=BLUE)
        self.say('The Fundamental Theorem: find the antiderivative, then evaluate at $5$ minus at $0$.')
        self.play(Write(step2), Write(step2_note), run_time=1.8)
        self.hold('antiderivative', 4.0)

        step3 = tex('=', r'3958\frac13', size=36).move_to([0, -1.7, 0])
        step3[1].set_color(GOLD)
        self.say(r'Simplify: the average elevation is $3958\frac13$ feet.')
        self.play(Write(step3), run_time=1.4)
        self.hold('answer', 3.6)

        final_rect = axes.get_area(
            axes.plot(lambda _x: AVERAGE, x_range=[A, B]),
            x_range=[A, B], color=FILL_GOLD, opacity=.45,
        )
        final_line = DashedLine(axes.c2p(A, AVERAGE), axes.c2p(B + .25, AVERAGE), color=GOLD, stroke_width=4)
        final_label = MathTex(r'\bar f', color=GOLD, font_size=28).next_to(
            axes.c2p(B + .25, AVERAGE), RIGHT, buff=.08,
        )
        summary = note('average elevation is slightly less than 3960 ft', -3.1, size=26)
        self.say('Back on the graph: the trail averages a little under 3960 feet.')
        self.play(
            FadeOut(VGroup(step1, step2, step2_note)), step3.animate.move_to([0, -2.45, 0]),
            FadeIn(base), FadeIn(area), FadeIn(final_rect), FadeIn(final_line), FadeIn(final_label),
            run_time=1.6,
        )
        self.play(Write(summary), run_time=1.2)
        self.hold('hold', 4.0)
        self.write_marks('ftc_average_value_marks.json')
