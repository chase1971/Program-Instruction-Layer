"""FTC clip 3: state the theorem, take Part 1 and Part 2 apart piece by piece, then redo the car.

PORTRAIT: built for the 1080 x 1350 student-portal player. Each caption is a Slow-mode step.
Shared helpers (tex, colors, FtcScene) come from fundamental_theorem_calculus.py.
"""

from fundamental_theorem_calculus import (
    BLUE, FILL_BLUE, FILL_GOLD, GOLD, INK, READ_LONG, RED, FtcScene, tex,
)
from manim import (
    Axes, FadeIn, FadeOut, LEFT, Line, MathTex, ReplacementTransform, RIGHT, DOWN,
    SurroundingRectangle, UR, ValueTracker, VGroup, Write, always_redraw, linear,
)

HOLD = 2.6


def heading(text):
    return tex(text, size=30).move_to([0, 2.6, 0])


class FtcTheoremStatement(FtcScene):
    """Parts 1 and 2 of the Fundamental Theorem, explained piece by piece, then the nonlinear car.

    Two portal tabs: FtcTheoremPart1 (3a) and FtcTheoremPart2 (3b) each render one half.
    """

    def construct(self):
        self.part_one()
        self.part_two()
        self.worked_example()
        self.write_marks('ftc_theorem_statement_marks.json')

    def caption_step_times(self):
        """Pause on the finished board, before any board-clearing FadeOut that precedes the next say()."""
        marks = [m['time'] for m in self.marks or []]
        return [
            round(min([s] + [m - .04 for m in marks if s - 1.5 < m - .04 < s]), 2)
            for s in super().caption_step_times()
        ]

    # ---------------------------------------------------------------- Part 1
    def part_one(self):
        title = heading(r'\text{FUNDAMENTAL THEOREM, PART 1}')
        lines = VGroup(
            tex(r'\text{If }f\text{ is continuous on }[a,b]\text{, then the area function}', size=26),
            tex('A(x)', '=', r'\int_a^x f(t)\,dt', r'\quad a\le x\le b\text{,}', size=32),
            tex(r'\text{is continuous on }[a,b]\text{ and differentiable on }(a,b)\text{.}', size=26),
            tex(r'\text{The area function satisfies }', r'A^{\prime}(x)=f(x)', r'\text{.}', size=28),
            tex(r'\text{Equivalently, }', r'\frac{d}{dx}\int_a^x f(t)\,dt=f(x)', r'\text{,}', size=28),
            tex(r'\text{so the area function of }f\text{ is an antiderivative}', size=26),
            tex(r'\text{of }f\text{ on }[a,b]\text{.}', size=26),
        ).arrange(DOWN, buff=.26).move_to([0, .05, 0])
        lines[1][0].set_color(GOLD)
        lines[3][1].set_color(BLUE)
        lines[4][1].set_color(BLUE)
        
        self.say('Here is Part 1 in full. Then we take it apart one piece at a time.')
        self.play(FadeIn(title), run_time=.6)
        for line in lines:
            self.play(Write(line), run_time=1.3)
        self.hold('part_one_full', 5.0)
        self.play(FadeOut(lines), run_time=.8)

        f = lambda x: x * (10 - x)
        axes = Axes(
            x_range=[0, 10.5, 2], y_range=[0, 27, 5], x_length=5.0, y_length=2.3,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([0, .75, 0])
        graph = axes.plot(f, x_range=[0, 10], color=BLUE, stroke_width=5)
        t_axis = MathTex('t', color=INK, font_size=26).next_to(axes.x_axis.get_end(), RIGHT, buff=.14)
        f_label = MathTex('f', color=BLUE, font_size=30).next_to(axes.c2p(9.2, f(9.2)), UR, buff=.05)
        a_label = MathTex('a', color=INK, font_size=28).next_to(axes.c2p(0, 0), DOWN, buff=.08)
        b_label = MathTex('b', color=INK, font_size=28).next_to(axes.c2p(10, 0), DOWN, buff=.08)
        base = VGroup(axes, graph, t_axis, f_label, a_label, b_label)

        def piece(*parts, size=36, y=-2.2):
            return tex(*parts, size=size).move_to([0, y, 0])

        cond_piece = piece(r'f\text{ continuous on }[a,b]', size=32)
        self.say('First piece: $f$ is continuous on $[a,b]$. Its graph is one unbroken curve from $a$ to $b$.')
        self.play(FadeIn(base), Write(cond_piece), run_time=1.5)
        self.hold('continuous', HOLD)

        x = ValueTracker(6)
        h = ValueTracker(1.3)
        area = always_redraw(lambda: axes.get_area(
            graph, x_range=[0, x.get_value()], color=FILL_BLUE, opacity=.55,
        ))
        x_label = always_redraw(lambda: MathTex('x', color=INK, font_size=28).next_to(
            axes.c2p(x.get_value(), 0), DOWN, buff=.08,
        ))
        area_piece = piece('A(x)', '=', r'\int_a^x f(t)\,dt')
        area_piece[0].set_color(GOLD)
        self.say('$A(x)$ is the area under $f$ from $a$ up to $x$. The integral adds up thin slices of height $f(t)$.')
        self.play(FadeIn(area), FadeIn(x_label), ReplacementTransform(cond_piece, area_piece), run_time=1.4)
        self.hold('area_function', 3.0)

        self.say('Slide $x$ to the right and more area piles up. So $A$ is a function of $x$.')
        self.play(x.animate.set_value(8.5), run_time=2.6, rate_func=linear)
        self.play(x.animate.set_value(6), run_time=1.6, rate_func=linear)
        self.hold('slide_x', HOLD)

        strip = always_redraw(lambda: axes.get_area(
            graph, x_range=[x.get_value(), x.get_value() + h.get_value()], color=FILL_GOLD, opacity=.85,
        ))
        width = always_redraw(lambda: Line(
            axes.c2p(x.get_value(), -3.4), axes.c2p(x.get_value() + h.get_value(), -3.4),
            color=RED, stroke_width=5,
        ))
        h_label = always_redraw(lambda: MathTex('h', color=RED, font_size=28).next_to(width, DOWN, buff=.06))
        strip_piece = piece('A(x+h)-A(x)', r'\approx', 'f(x)', 'h')
        strip_piece[0].set_color(GOLD)
        strip_piece[2].set_color(BLUE)
        strip_piece[3].set_color(RED)
        self.say('Add a thin strip of width $h$. Its area $A(x+h)-A(x)$ is about height $f(x)$ times $h$.')
        self.play(
            FadeIn(strip), FadeIn(width), FadeIn(h_label),
            ReplacementTransform(area_piece, strip_piece), run_time=1.5,
        )
        self.hold('strip', 3.0)

        quotient = piece(r'\frac{A(x+h)-A(x)}{h}', r'\approx', 'f(x)', size=38)
        quotient[2].set_color(BLUE)
        self.say('Divide by $h$: area gained per unit of $x$ is about $f(x)$. Shrink $h$ and it becomes exact.')
        self.play(ReplacementTransform(strip_piece, quotient), run_time=1.0)
        self.play(h.animate.set_value(.15), run_time=3.0, rate_func=linear)
        self.hold('shrink_h', HOLD)

        limit_piece = piece(r'\lim_{h\to 0}', r'\frac{A(x+h)-A(x)}{h}', '=', 'f(x)', size=38)
        limit_piece[3].set_color(BLUE)
        self.say('Let $h$ go to 0 and the approximation becomes exact: the limit equals $f(x)$.')
        self.play(
            ReplacementTransform(quotient, limit_piece),
            h.animate.set_value(.04),
            run_time=2.0, rate_func=linear,
        )
        self.hold('limit', HOLD)

        slope_piece = piece(r'A^{\prime}(x)', '=', 'f(x)', size=44)
        slope_piece[0].set_color(GOLD)
        slope_piece[2].set_color(BLUE)
        self.say('That exact rate is the derivative: $A^{\\prime}(x)=f(x)$. The next clip proves it.')
        self.play(ReplacementTransform(limit_piece, slope_piece), run_time=1.4)
        self.hold('slope', 3.0)

        anti_note = tex(r'\text{so }A\text{ is an antiderivative of }f', size=30).move_to([0, -3.2, 0])
        self.say('A function whose derivative is $f$ is an antiderivative of $f$. The area function is one.')
        self.play(Write(anti_note), run_time=1.2)
        self.hold('antiderivative', 3.2)

        # ---- the "d/dx of the integral" form, read in two moves
        expr = tex(r'\frac{d}{dx}', r'\int_a^x f(t)\,dt', '=', 'f(x)', size=38).move_to([0, 1.75, 0])
        expr[1].set_color(GOLD)
        expr[3].set_color(BLUE)

        def side_note(text):
            return tex(r'\text{' + text + '}', size=28).move_to([0, -2.4, 0])

        def red_box(mob):
            return SurroundingRectangle(mob, color=RED, buff=.14, stroke_width=3)

        self.say('Part 1 has one more form, shown above. Read it as two moves: the integral first, then the derivative.')
        self.play(
            FadeOut(VGroup(strip, width, h_label, slope_piece, anti_note)),
            base.animate.shift(DOWN * .9),
            FadeIn(expr),
            run_time=1.4,
        )
        self.hold('derivative_form', HOLD)

        box = red_box(expr[1])
        note = side_note('integral: the area so far, A(x)')
        self.say('Move 1, the integral: collect all the area under $f$ from $a$ up to $x$. That is $A(x)$.')
        self.play(FadeIn(box), Write(note), run_time=1.1)
        self.hold('move_integral', 3.0)

        grow = always_redraw(lambda: axes.get_area(
            graph, x_range=[x.get_value(), x.get_value() + .3], color=FILL_GOLD, opacity=.85,
        ))
        box_d = red_box(expr[0])
        note_d = side_note('d/dx: how fast that area grows')
        self.say('Move 2, the derivative: ask how fast that area grows as $x$ moves to the right.')
        self.play(ReplacementTransform(box, box_d), ReplacementTransform(note, note_d), FadeIn(grow), run_time=1.1)
        self.play(x.animate.set_value(7.5), run_time=2.0, rate_func=linear)
        self.play(x.animate.set_value(6), run_time=1.4, rate_func=linear)
        self.hold('move_derivative', HOLD)

        height = always_redraw(lambda: Line(
            axes.c2p(x.get_value(), 0), axes.c2p(x.get_value(), f(x.get_value())),
            color=RED, stroke_width=5,
        ))
        height_label = always_redraw(lambda: MathTex('f(x)', color=BLUE, font_size=28).next_to(
            height, LEFT, buff=.08,
        ))
        box_f = red_box(expr[3])
        note_f = side_note('growth rate = height of the curve = f(x)')
        self.say('The growth rate at $x$ is the height of the curve at $x$, which is $f(x)$. That is why the right side is $f(x)$.')
        self.play(
            ReplacementTransform(box_d, box_f), ReplacementTransform(note_d, note_f),
            FadeOut(grow), FadeIn(height), FadeIn(height_label), run_time=1.2,
        )
        self.hold('rate_is_height', 3.0)

        undo = tex('f', r'\xrightarrow{\ \int\ }', 'A', r'\xrightarrow{\ d/dx\ }', 'f', size=34).move_to([0, -2.4, 0])
        undo[0].set_color(BLUE)
        undo[2].set_color(GOLD)
        undo[4].set_color(BLUE)
        self.say('So integrating and then differentiating undoes itself: you land back on $f$.')
        self.play(FadeOut(box_f), ReplacementTransform(note_f, undo), run_time=1.2)
        self.hold('undo', 3.2)

        self.play(FadeOut(VGroup(
            base, area, x_label, expr, height, height_label, undo, title,
        )), run_time=.9)

    # ---------------------------------------------------------------- Part 2
    def part_two(self):
        title = heading(r'\text{FUNDAMENTAL THEOREM, PART 2}')
        cond = tex(r'\text{If }f\text{ is continuous on }[a,b]\text{ and }F\text{ is any}', size=26).move_to([0, 1.9, 0])
        given = tex(r'\text{antiderivative of }f\text{ on }[a,b]\text{, then}', size=26).move_to([0, 1.3, 0])
        result = tex(r'\int_a^b', 'f(x)', r'\,dx', '=', 'F(b)', '-', 'F(a)', size=42).move_to([0, .0, 0])
        short = tex('=', r'F(x)\Big|_a^b', size=42).move_to([0, -1.2, 0])
        result[4].set_color(GOLD)
        result[6].set_color(GOLD)
        short[1].set_color(GOLD)

        def note(text, size=28):
            return tex(r'\text{' + text + '}', size=size).move_to([0, -2.4, 0])

        def box(mob):
            return SurroundingRectangle(mob, color=RED, buff=.09, stroke_width=3)

        self.say('Part 2 in full: for continuous $f$ with antiderivative $F$, the integral is $F(b)-F(a)$.')
        self.play(FadeIn(title), Write(cond), run_time=1.0)
        self.play(Write(given), run_time=1.1)
        self.play(Write(result), run_time=1.6)
        self.play(Write(short), run_time=1.1)
        self.hold('part_two_full', 3.5)

        pieces = [
            ('limits', result[0], 'limits of integration: start at a, stop at b',
             'The numbers $a$ and $b$ are the limits of integration: where the area starts and where it stops.'),
            ('integrand', result[1], 'integrand: the function whose area we want',
             'The integrand $f(x)$ is the function whose area we are adding up.'),
            ('variable', result[2], 'dx: x is the variable we integrate over',
             'The $dx$ says $x$ is the variable we sweep through. Any letter works.'),
            ('antiderivative', VGroup(*result[4:7]), 'F is any antiderivative of f, so F\'(x)=f(x)',
             '$F$ is any antiderivative of $f$, a function whose derivative is $f$.'),
            ('top_limit', result[4], 'plug in the top limit b',
             'The first term plugs the top limit $b$ into $F$.'),
            ('bottom_limit', result[6], 'minus: plug in the bottom limit a',
             'Then subtract what we get from plugging the bottom limit $a$ into $F$.'),
            ('shorthand', short[1], 'shorthand: plug in b, plug in a, subtract',
             'This bar is shorthand. $F(x)$ with $a$ and $b$ on the bar means plug in $b$, plug in $a$, and subtract.'),
        ]
        current_box = None
        current_note = None
        for name, target, label, caption in pieces:
            new_box, new_note = box(target), note(label)
            self.say(caption)
            if current_box is None:
                self.play(Write(new_box), FadeIn(new_note), run_time=.9)
            else:
                self.play(
                    ReplacementTransform(current_box, new_box),
                    ReplacementTransform(current_note, new_note), run_time=.9,
                )
            current_box, current_note = new_box, new_note
            self.hold(name, 3.0)

        meaning = note('F(b)-F(a) is the total area added from a to b', size=28)
        self.say('Why it works: $A$ and $F$ are antiderivatives of $f$, so they differ by a constant.')
        self.play(FadeOut(current_box), ReplacementTransform(current_note, meaning), run_time=1.0)
        self.hold('why', 3.2)
        constant = tex(r'\text{that constant cancels in the subtraction}', size=28).move_to([0, -3.2, 0])
        self.say('In $F(b)-F(a)$ that constant cancels, leaving the area added between $a$ and $b$.')
        self.play(Write(constant), run_time=1.1)
        self.hold('cancels', 3.2)
        self.play(FadeOut(VGroup(title, cond, given, result, short, meaning, constant)), run_time=.9)

    # ---------------------------------------------------------------- example
    def worked_example(self):
        title = heading(r'\text{OUR CAR: }v(t)=t(10-t)')
        integral = tex(r'\int_0^{10}t(10-t)\,dt', size=42).move_to([0, 1.6, 0])
        antiderivative = tex('F(t)', '=', r'5t^2-\frac{t^3}{3}', size=38).move_to([0, .35, 0])
        bar = tex(r'\int_0^{10}t(10-t)\,dt', '=', r'\left(5t^2-\frac{t^3}{3}\right)\Big|_0^{10}', size=36)
        bar.move_to([0, -.85, 0])
        plug = tex('=', 'F(10)', '-', 'F(0)', size=38).move_to([0, -1.85, 0])
        answer = tex('=', r'\left(500-\tfrac{1000}{3}\right)-0', '=', '166.67', size=36).move_to([0, -2.85, 0])
        antiderivative[0].set_color(GOLD)
        plug[1].set_color(GOLD)
        plug[3].set_color(GOLD)
        answer[3].set_color(BLUE)

        self.say('Now redo the car with the theorem. The distance is the integral of $v$ from $0$ to $10$.')
        self.play(FadeIn(title), Write(integral), run_time=1.3)
        self.hold('example_integral', HOLD)

        self.say('Step 1: find an antiderivative $F$ of the integrand.')
        self.play(Write(antiderivative), run_time=1.3)
        self.hold('example_antiderivative', 3.0)

        self.say('Step 2: evaluate it from $0$ to $10$. Draw the bar next to $F$ and put $0$ and $10$ on it.')
        self.play(Write(bar), run_time=1.6)
        self.hold('example_bar', 3.2)

        self.say('Plug in the top limit $10$, then subtract what you get from the bottom limit $0$.')
        self.play(Write(plug), run_time=1.3)
        self.hold('example_plug', 3.0)

        self.say('Simplify: $500-333.33-0=166.67$.')
        self.play(Write(answer), run_time=1.6)
        self.hold('example_answer', 3.2)

        f = lambda x: x * (10 - x)
        axes = Axes(
            x_range=[0, 10.5, 2], y_range=[0, 27, 5], x_length=4.6, y_length=2.2,
            axis_config={'color': INK, 'stroke_width': 2, 'include_ticks': False},
        ).move_to([0, 1.0, 0])
        graph = axes.plot(f, x_range=[0, 10], color=BLUE, stroke_width=5)
        shade = axes.get_area(graph, x_range=[0, 10], color=FILL_BLUE, opacity=.55)
        t_axis = MathTex('t', color=INK, font_size=26).next_to(axes.x_axis.get_end(), RIGHT, buff=.14)
        v_axis = MathTex('v', color=INK, font_size=26).next_to(axes.y_axis.get_end(), RIGHT, buff=.06)
        ten = MathTex('10', color=INK, font_size=26).next_to(axes.c2p(9.2, 0), DOWN, buff=.1)
        total = tex(r'\int_0^{10}t(10-t)\,dt', '=', '166.67', r'\text{ meters}', size=38).move_to([0, -1.5, 0])
        total[2].set_color(BLUE)
        meaning = tex(r'\text{total distance driven = area under the curve}', size=28).move_to([0, -2.6, 0])
        self.say('Summary: the car drives 166.67 meters in 10 seconds, the area under the curve.')
        self.play(
            FadeOut(VGroup(integral, antiderivative, bar, plug, answer)),
            FadeIn(VGroup(axes, graph, shade, t_axis, v_axis, ten)),
            run_time=1.4,
        )
        self.play(Write(total), run_time=1.3)
        self.play(Write(meaning), run_time=1.3)
        self.hold('hold', 4.0)


class FtcTheoremPart1(FtcTheoremStatement):
    """Portal tab 3a: Part 1 piece by piece, ending on the d/dx-of-the-integral form."""

    def construct(self):
        self.part_one()
        self.write_marks('ftc_theorem_part1_marks.json')


class FtcTheoremPart2(FtcTheoremStatement):
    """Portal tab 3b: Part 2 piece by piece, then the nonlinear car."""

    def construct(self):
        self.part_two()
        self.worked_example()
        self.write_marks('ftc_theorem_part2_marks.json')
