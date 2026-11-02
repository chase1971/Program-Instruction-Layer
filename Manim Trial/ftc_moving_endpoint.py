"""FTC clip 4: problem 10, d/dx of the integral from 2 to x^2 of (3p+1) dp.

PORTRAIT: built for the 1080 x 1350 student-portal player. Each caption is a Slow-mode step.
Story: accumulation per unit of p times how fast the endpoint moves. Shared helpers come from
fundamental_theorem_calculus.py.
"""

from fundamental_theorem_calculus import (
    BLUE, FILL_BLUE, FILL_GOLD, GOLD, INK, RED, FtcScene, tex,
)
from manim import (
    Axes, DOWN, FadeIn, FadeOut, LEFT, Line, MathTex, ReplacementTransform, RIGHT, UP, ValueTracker, VGroup, Write, always_redraw, linear,
)

HOLD = 2.6


def heading(text):
    return tex(text, size=30).move_to([0, 2.6, 0])


class FtcMovingEndpoint(FtcScene):
    """Problem 10: a moving upper limit means height at the boundary times how fast it moves."""

    def construct(self):
        title = heading(r'\text{PROBLEM 10: A MOVING ENDPOINT}')
        expr = tex(r'\frac{d}{dx}', r'\int_2^{x^2}(3p+1)\,dp', size=40).move_to([0, 1.75, 0])
        expr[1].set_color(GOLD)

        def note(text, y=-2.4, size=28):
            return tex(r'\text{' + text + '}', size=size).move_to([0, y, 0])

        # ---- the problem
        self.say('Problem 10: differentiate an integral whose top limit is $x^2$, not $x$.')
        self.play(FadeIn(title), Write(expr), run_time=1.4)
        self.hold('problem', 3.4)

        # ---- why we need more than Part 1
        part_one = tex(r'\frac{d}{dx}\int_2^{x}(3p+1)\,dp', '=', '3x+1', size=36).move_to([0, .45, 0])
        part_one[2].set_color(BLUE)
        part_one_note = note('Part 1: top limit is x, answer is the height', y=-.35, size=28)
        self.say('Part 1 handles a top limit of plain $x$: the answer is the height, $3x+1$.')
        self.play(Write(part_one), Write(part_one_note), run_time=1.6)
        self.hold('part_one_case', 3.4)

        why = note('here the top is $x^2$, which moves faster than $x$', y=-1.3, size=28)
        why.set_color(RED)
        self.say('Our top limit $x^2$ moves faster than $x$, so Part 1 alone is not enough.')
        self.play(Write(why), run_time=1.3)
        self.hold('why_more', 3.4)
        self.play(FadeOut(VGroup(part_one, part_one_note, why)), run_time=.8)

        # ---- the accumulation picture
        f = lambda p: 3 * p + 1
        axes = Axes(
            x_range=[0, 7.4, 1], y_range=[0, 23, 5], x_length=5.0, y_length=2.3,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([0, -.15, 0])
        graph = axes.plot(f, x_range=[0, 7], color=BLUE, stroke_width=5)
        p_axis = MathTex('p', color=INK, font_size=26).next_to(axes.x_axis.get_end(), RIGHT, buff=.14)
        f_label = MathTex('3p+1', color=BLUE, font_size=28).next_to(axes.c2p(6.3, f(6.3)), UP, buff=.08)
        two = MathTex('2', color=INK, font_size=26).next_to(axes.c2p(2, 0), DOWN, buff=.08)
        x = ValueTracker(2)
        u = lambda: x.get_value() ** 2
        area = always_redraw(lambda: axes.get_area(
            graph, x_range=[2, u()], color=FILL_BLUE, opacity=.55,
        ))
        end_label = always_redraw(lambda: MathTex('x^2', color=INK, font_size=28).next_to(
            axes.c2p(u(), 0), DOWN, buff=.08,
        ))
        base = VGroup(axes, graph, p_axis, f_label, two)

        accumulation = note('integrand $3p+1$: amount per unit of $p$')
        self.say('Draw $3p+1$. At each $p$ it is the amount we pick up per unit of $p$.')
        self.play(FadeIn(base), Write(accumulation), run_time=1.5)
        self.hold('integrand', 3.2)

        total = note('the integral: area from $p=2$ up to the endpoint $x^2$')
        self.say('The integral adds it up from $p=2$ to the endpoint $p=x^2$. Call it $M(x)$.')
        self.play(FadeIn(area), FadeIn(end_label), ReplacementTransform(accumulation, total), run_time=1.4)
        self.hold('total', 3.0)

        story = note('picture a wire: $3p+1$ grams per meter at position $p$', size=26)
        self.say('Picture a wire, $3p+1$ grams per meter. A machine is at $p=x^2$ after $x$ seconds.')
        self.play(ReplacementTransform(total, story), run_time=1.0)
        self.play(x.animate.set_value(2.45), run_time=2.0, rate_func=linear)
        self.play(x.animate.set_value(2), run_time=1.4, rate_func=linear)
        self.hold('wire', HOLD)

        question = note('$M(x)$ = grams so far. How fast is it growing?', size=26)
        self.say('$M(x)$ is the grams processed so far. The derivative asks: grams per second?')
        self.play(ReplacementTransform(story, question), run_time=1.0)
        self.hold('question', 3.0)

        # ---- the two factors
        height = always_redraw(lambda: Line(
            axes.c2p(u(), 0), axes.c2p(u(), f(u())), color=RED, stroke_width=5,
        ))
        height_label = always_redraw(lambda: MathTex('3x^2+1', color=RED, font_size=26).next_to(
            height, UP, buff=.06,
        ).shift(LEFT * .5))
        factor_one = note('1: grams per meter at the boundary $=3x^2+1$')
        self.say('Two things set the rate. First: grams per meter at the boundary, $3x^2+1$.')
        self.play(
            FadeIn(height), FadeIn(height_label), ReplacementTransform(question, factor_one), run_time=1.3,
        )
        self.hold('factor_height', 3.2)

        speed = note('2: how fast the boundary moves $=2x$')
        speed_expr = tex(r'\frac{d}{dx}(x^2)=2x', size=34).move_to([0, -3.3, 0])
        speed_expr.set_color(BLUE)
        self.say('Second: how fast the boundary moves. The boundary $x^2$ moves at $2x$ per second.')
        self.play(ReplacementTransform(factor_one, speed), Write(speed_expr), run_time=1.3)
        self.play(x.animate.set_value(2.45), run_time=2.0, rate_func=linear)
        self.play(x.animate.set_value(2), run_time=1.4, rate_func=linear)
        self.hold('factor_speed', 3.0)

        # ---- multiply
        product = tex(r'\frac{dM}{dx}', '=', '(3x^2+1)', '(2x)', size=40).move_to([0, -2.3, 0])
        product[2].set_color(RED)
        product[3].set_color(BLUE)
        self.say('Multiply: grams per meter times meters per second is grams per second.')
        self.play(FadeOut(speed), FadeOut(speed_expr), Write(product), run_time=1.5)
        self.hold('multiply', 3.2)

        answer = tex('=', '2x(3x^2+1)', size=40).move_to([0, -3.2, 0])
        answer[1].set_color(GOLD)
        self.say('So the derivative is $2x(3x^2+1)$, which is $6x^3+2x$.')
        self.play(Write(answer), run_time=1.3)
        self.hold('answer', 3.4)

        # ---- numbers at x = 2
        self.play(FadeOut(VGroup(product, answer)), run_time=.7)
        check = VGroup(
            tex(r'\text{at }x=2\text{: boundary at }p=4', size=28),
            tex(r'3(4)+1=13\text{ grams per meter}', size=28),
            tex(r'2(2)=4\text{ meters per second}', size=28),
            tex('13', r'\cdot', '4', '=', '52', r'\text{ grams per second}', size=34),
        ).arrange(DOWN, buff=.14).move_to([0, -2.75, 0])
        check[3][4].set_color(GOLD)
        self.say('Try $x=2$: the machine is at $p=4$, 13 grams per meter, moving 4 per second.')
        self.play(Write(check[:3]), run_time=1.8)
        self.hold('numbers', 3.0)
        self.say('That is $13\\cdot 4=52$ grams per second.')
        self.play(Write(check[3]), run_time=1.2)
        self.hold('fifty_two', 3.2)

        # ---- rule
        rule = VGroup(
            tex(r'\text{rate of area growth}', '=', size=28),
            tex(r'\text{height at the boundary}', r'\times', r'\text{its speed}', size=28),
        ).arrange(DOWN, buff=.14).move_to([0, -2.3, 0])
        rule[1][0].set_color(RED)
        rule[1][2].set_color(BLUE)
        self.say('The pattern: growth rate = height at the boundary times boundary speed.')
        self.play(FadeOut(check), Write(rule), run_time=1.5)
        self.hold('rule', 3.4)

        chain = tex(
            r'\frac{d}{dx}\int_a^{g(x)} f(p)\,dp', '=', 'f(g(x))', r'\cdot', "g'(x)", size=34,
        ).move_to([0, -3.2, 0])
        chain[2].set_color(RED)
        chain[4].set_color(BLUE)
        self.say('In symbols: $f(g(x))\\cdot g^{\\prime}(x)$ with $f(p)=3p+1$ and $g(x)=x^2$.')
        self.play(Write(chain), run_time=1.6)
        self.hold('hold', 4.0)
        self.write_marks('ftc_moving_endpoint_marks.json')
