"""FTC clip 5: side by side, top limit x versus top limit x^2.

PORTRAIT: built for the 1080 x 1350 student-portal player. Each caption is a Slow-mode step.
Same integrand 3p+1, same start at p=2. Raise x by the same amount on both sides and watch how much
farther the x^2 boundary travels, how much more area it sweeps, and why the rate gains a factor 2x.
"""

from fundamental_theorem_calculus import (
    BLUE, FILL_BLUE, FILL_GOLD, GOLD, INK, RED, FtcScene, tex,
)
from manim import (
    Axes, DOWN, FadeIn, FadeOut, LEFT, Line, MathTex, ValueTracker, VGroup, Write,
    always_redraw, linear,
)

LEFT_X, RIGHT_X = -1.55, 1.55
X0, X1 = 2.0, 2.5


def heading(text):
    return tex(text, size=30).move_to([0, 2.7, 0])


def f(p):
    return 3 * p + 1


class FtcEndpointCompare(FtcScene):
    """Top limit x on the left, top limit x^2 on the right, same change in x on both."""

    def construct(self):
        title = heading(r'\text{TOP LIMIT }x\text{ VERSUS }x^2')
        left_expr = tex(r'\frac{d}{dx}\int_2^{x}(3p+1)\,dp', size=26).move_to([LEFT_X, 1.95, 0])
        right_expr = tex(r'\frac{d}{dx}\int_2^{x^2}(3p+1)\,dp', size=26).move_to([RIGHT_X, 1.95, 0])
        left_expr[0].set_color(GOLD)
        right_expr[0].set_color(GOLD)

        def panel(cx):
            axes = Axes(
                x_range=[0, 8.8, 1], y_range=[0, 26, 5], x_length=2.6, y_length=2.0,
                axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
            ).move_to([cx, .45, 0])
            return axes, axes.plot(f, x_range=[0, 7.4], color=BLUE, stroke_width=4)

        left_axes, left_graph = panel(LEFT_X)
        right_axes, right_graph = panel(RIGHT_X)
        graphs = VGroup(left_axes, left_graph, right_axes, right_graph)

        x = ValueTracker(X0)

        def lo(u):
            return max(u, 2.03)

        def left_u():
            return x.get_value()

        def right_u():
            return x.get_value() ** 2

        def label(text, axes, u, color=INK):
            return MathTex(text, color=color, font_size=26).next_to(axes.c2p(u(), 0), DOWN, buff=.1)

        left_label = always_redraw(lambda: label('x', left_axes, left_u))
        right_label = always_redraw(lambda: label('x^2', right_axes, right_u))
        left_base = left_axes.get_area(left_graph, x_range=[2, 2.03], color=FILL_BLUE, opacity=.55)
        right_base = right_axes.get_area(right_graph, x_range=[2, X0 ** 2], color=FILL_BLUE, opacity=.55)

        def note(text, y, size=26, color=INK):
            return tex(r'\text{' + text + '}', size=size).move_to([0, y, 0]).set_color(color)

        # ---- the two problems
        self.say('Same integrand, same start. Only the top limit differs: $x$ left, $x^2$ right.')
        self.play(FadeIn(title), Write(left_expr), Write(right_expr), run_time=1.6)
        self.hold('two_problems', 3.4)

        self.say('Each area runs from $p=2$ to its boundary. At $x=2$ the boundaries are 2 and 4.')
        self.play(
            FadeIn(graphs), FadeIn(left_base), FadeIn(right_base), FadeIn(left_label), FadeIn(right_label),
            run_time=1.5,
        )
        self.hold('boundaries', 3.4)

        # ---- raise x by the same amount on both
        left_gold = always_redraw(lambda: left_axes.get_area(
            left_graph, x_range=[2, lo(left_u())], color=FILL_GOLD, opacity=.85,
        ))
        right_gold = always_redraw(lambda: right_axes.get_area(
            right_graph, x_range=[X0 ** 2, max(right_u(), X0 ** 2 + .03)], color=FILL_GOLD, opacity=.85,
        ))
        left_trail = always_redraw(lambda: Line(
            left_axes.c2p(X0, 0) + DOWN * .62, left_axes.c2p(max(left_u(), X0 + .02), 0) + DOWN * .62,
            color=RED, stroke_width=5,
        ))
        right_trail = always_redraw(lambda: Line(
            right_axes.c2p(X0 ** 2, 0) + DOWN * .62, right_axes.c2p(max(right_u(), X0 ** 2 + .02), 0) + DOWN * .62,
            color=RED, stroke_width=5,
        ))
        self.say('Raise $x$ by the same amount on both sides, from 2 to 2.5.')
        self.add(left_gold, right_gold, left_trail, right_trail)
        self.play(x.animate.set_value(X1), run_time=3.5, rate_func=linear)
        self.hold('raise_x', 3.0)

        moved_left = tex(r'\text{moved }0.5', size=26).move_to([LEFT_X, -1.75, 0]).set_color(RED)
        moved_right = tex(r'\text{moved }2.25', size=26).move_to([RIGHT_X, -1.75, 0]).set_color(RED)
        self.say('The left boundary moved 0.5. The right moved 2.25, over four times as far.')
        self.play(Write(moved_left), Write(moved_right), run_time=1.3)
        self.hold('moved', 3.4)

        more_area = note('same change in $x$, far more area on the right', -2.45, size=24)
        self.say('Same change in $x$, but the right side gains far more area.')
        self.play(Write(more_area), run_time=1.4)
        self.hold('more_area', 3.4)

        # ---- reset to x = 2 to read the rates
        self.say('Back to $x=2$. Rate is height at the boundary times boundary speed.')
        self.play(
            FadeOut(VGroup(moved_left, moved_right, more_area, left_trail, right_trail)),
            x.animate.set_value(X0), run_time=2.2, rate_func=linear,
        )
        self.hold('reset', 3.0)

        speed_left = tex(r'\text{boundary speed: }1', size=26).move_to([LEFT_X, -1.75, 0])
        speed_right = tex(r'\text{speed: }2x=4', size=26).move_to([RIGHT_X, -1.75, 0])
        speed_left.set_color(BLUE)
        speed_right.set_color(BLUE)
        speed_title = note('how fast the boundary moves', -2.3, size=26)
        self.say('Speed first: $x$ moves 1 per unit of $x$. $x^2$ moves $2x$, which is 4.')
        self.play(Write(speed_left), Write(speed_right), Write(speed_title), run_time=1.6)
        self.hold('speeds', 3.6)

        left_height = Line(left_axes.c2p(2, 0), left_axes.c2p(2, f(2)), color=RED, stroke_width=5)
        right_height = Line(right_axes.c2p(4, 0), right_axes.c2p(4, f(4)), color=RED, stroke_width=5)
        left_h_label = MathTex('7', color=RED, font_size=28).next_to(left_height, LEFT, buff=.08)
        right_h_label = MathTex('13', color=RED, font_size=28).next_to(right_height, LEFT, buff=.08)
        self.say('Height at each boundary: $3(2)+1=7$ on the left, $3(4)+1=13$ on the right.')
        self.play(
            FadeIn(left_height), FadeIn(right_height), FadeIn(left_h_label), FadeIn(right_h_label),
            FadeOut(VGroup(speed_title)), run_time=1.2,
        )
        self.hold('heights', 3.4)

        prod_left = tex('7', r'\cdot', '1', '=', '7', size=30).move_to([LEFT_X, -2.4, 0])
        prod_right = tex('13', r'\cdot', '4', '=', '52', size=30).move_to([RIGHT_X, -2.4, 0])
        prod_left[4].set_color(GOLD)
        prod_right[4].set_color(GOLD)
        self.say('Height times speed: $7\\cdot 1=7$ on the left, $13\\cdot 4=52$ on the right.')
        self.play(Write(prod_left), Write(prod_right), run_time=1.4)
        self.hold('products', 3.6)

        takeaway = note('the $x^2$ boundary rushes ahead, so area piles up faster', -3.15, size=24)
        factor = note('that extra factor $2x$ is the chain rule', -3.65, size=24)
        self.say('The $x^2$ boundary rushes ahead. That extra factor $2x$ is the chain rule.')
        self.play(Write(takeaway), run_time=1.3)
        self.play(Write(factor), run_time=1.0)
        self.hold('hold', 4.0)
        self.write_marks('ftc_endpoint_compare_marks.json')
