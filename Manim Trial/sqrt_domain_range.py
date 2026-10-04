"""Square-root functions: the inside must be >= 0 for the domain, a and d set the range.

Two examples on one clip (portal tabs):
    f(x) = 2*sqrt(3x - 1) + 3    ->  domain [1/3, inf),  range [3, inf)
    f(x) = -2*sqrt(2 - x) + 1    ->  domain (-inf, 2],   range (-inf, 1]

DOMAIN, per example: the inside of the root must be greater than or equal to zero, so it is
copied down as "inside >= 0" and solved quickly and silently (the operation under both sides in
gold, the cancelling pair struck in red, as in SlopeInterceptForm.move_x). The second example
divides by a negative, so the sign flips (red, as in SlopeInterceptForm.divide). A number line
gets a closed circle on the answer and an arrow toward the solutions, then the interval is
written with c as the endpoint and c is replaced by the number.

RANGE, per example: identical to quadratic_domain_range.py with d in place of k -- the sign of
a sets the direction, d is the end of the range. The b of a*sqrt(b(x-c))+d is left out.

PORTRAIT: 4:5 frame (portrait_frame.py). Rows are built once at their final spot. Every
MathTex is given INK explicitly (the default is white on the white frame).
"""

from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from manim import (  # noqa: E402
    DOWN,
    Arrow,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    Line,
    ReplacementTransform,
    Scene,
    VGroup,
    Write,
)

from math_notation import mathtex  # noqa: E402
from scene_style import (  # noqa: E402
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    PAPER_RED,
    PORTAL_PAGE_WHITE,
    Narrated,
    apply_portal_paper_background,
)
from solve_steps import divide_bars, op_under, strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

apply_portal_paper_background()

INK = PAPER_INK
A_COLOR = PAPER_BLUE
C_COLOR = PAPER_BLUE
D_COLOR = PAPER_GOLD
OP_COLOR = PAPER_GOLD
FORM_SIZE = 50
GENERAL_SIZE = 44
RULE_SIZE = 44
STEP_SIZE = 42
OP_SIZE = 34
MAX_WIDTH = 5.8
# Row centres, top to bottom; the caption owns y > 2.95.
ROW_Y = dict(form=2.4, s3_top=1.35, general=1.4, s1=1.5, s2=0.45, s3=-0.95, sign=0.35, domain=-1.3, range=-2.5)
LINE_Y = 0.6
LINE_HALF = 2.1
INF_X = 2.62

READ_SHORT = 1.0
READ_LONG = 1.5


def tex(*parts, size=RULE_SIZE):
    return mathtex(*parts, font_size=size, color=INK)


def place(row, name):
    if row.width > MAX_WIDTH:
        row.scale(MAX_WIDTH / row.width)
    return row.move_to([0, ROW_Y[name], 0])


def var(letter, color):
    """A variable inside a caption: italic and coloured, so it is not read as a word."""
    return f'<span foreground="{color}"><i>{letter}</i></span>'


def shown(text: str) -> str:
    return text.replace('-', '−')


A_WORD = var('a', A_COLOR)
C_WORD = var('c', C_COLOR)
D_WORD = var('d', D_COLOR)

# One entry per example. `inside` is the radicand split into parts; `moved` is the index of the
# part that is undone; `op` is what is done to both sides. After that the line is a*x ? n and is
# divided by `div`. flips: dividing by a negative.
EXAMPLES = dict(
    ex1=dict(
        a='2', d='3', inside=('3x', '-1'), moved=1, op=('+', '1'), keep=0,
        s2=('3x', r'\geq', '1'), div='3', s3=('x', r'\geq', r'\frac{1}{3}'),
        point=r'\frac{1}{3}', point_words='1/3', right=True,
        radicand=r'3x-1', words='3x − 1',
    ),
    ex2=dict(
        a='-2', d='1', inside=('2', '-x'), moved=0, op=('-', '2'), keep=1,
        s2=('-x', r'\geq', '-2'), div='-1', s3=('x', r'\leq', '2'),
        point='2', point_words='2', right=False,
        radicand=r'2-x', words='2 − x',
    ),
)


class SqrtDomainRange(Narrated, Scene):
    caption_color = PAPER_INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9

    def beat(self, mark, seconds):
        self.wait(seconds)
        self.mark(mark)

    def function_row(self, a, radicand, d, size):
        row = place(tex('f(x)', '=', a, rf'\sqrt{{{radicand}}}', '+', d, size=size), 'form')
        row[2].set_color(A_COLOR)
        row[5].set_color(D_COLOR)
        return row

    def number_line(self, point, right):
        line = Line([-LINE_HALF, LINE_Y, 0], [LINE_HALF, LINE_Y, 0], color=INK, stroke_width=4)
        end = LINE_HALF if right else -LINE_HALF
        ray = Arrow([0, LINE_Y, 0], [end, LINE_Y, 0], buff=0, color=C_COLOR, stroke_width=9,
                    tip_length=0.28)
        dot = Circle(radius=0.15, color=C_COLOR, stroke_width=5)
        dot.set_fill(C_COLOR, 1).move_to([0, LINE_Y, 0])
        label = tex(point).set_color(C_COLOR).move_to([0, LINE_Y - 0.85, 0])
        minus_inf = tex(r'-\infty', size=34).move_to([-INF_X, LINE_Y, 0])
        plus_inf = tex(r'\infty', size=34).move_to([INF_X, LINE_Y, 0])
        return line, ray, dot, label, minus_inf, plus_inf

    def solve(self, cfg, ex):
        """Quick and silent: the caption above stays up while the inequality is solved."""
        s1 = place(tex(*cfg['inside'], r'\geq', '0', size=STEP_SIZE), 's1')
        moved, rest = s1[cfg['moved']], s1[cfg['keep']]
        greater, zero = s1[2], s1[3]
        s2 = place(tex(*cfg['s2'], size=STEP_SIZE), 's2')
        s3 = place(tex(*cfg['s3'], size=STEP_SIZE), 's3')
        s3[2].set_color(C_COLOR)
        return s1, moved, rest, greater, zero, s2, s3

    def teach_example(self, cfg, ex):
        a, d, right = cfg['a'], cfg['d'], cfg['right']
        a_positive = not a.startswith('-')
        number_word = 'positive' if a_positive else 'negative'
        flips = not right

        form = self.function_row(a, cfg['radicand'], d, FORM_SIZE)
        general = place(tex('f(x)', '=', 'a', r'\sqrt{\cdots}', '+', 'd', size=GENERAL_SIZE),
                        'general')
        general[2].set_color(A_COLOR)
        general[5].set_color(D_COLOR)

        radicand = VGroup(*form[3].submobjects[2:])  # the inside only: [0] is the radical, [1] the bar over it
        s1, moved, rest, greater, zero, s2, s3 = self.solve(cfg, ex)
        line, ray, dot, label, minus_inf, plus_inf = self.number_line(cfg['point'], right)

        interval = ['[', 'c', r',\infty)'] if right else [r'(-\infty,', 'c', ']']
        domain = place(tex(r'\text{Domain: }', *interval), 'domain')
        domain[2].set_color(C_COLOR)
        final = [cfg['point'] if i == 'c' else i for i in interval]
        domain_done = place(tex(r'\text{Domain: }', *final), 'domain')
        domain_done[2].set_color(C_COLOR)

        sign = '>' if a_positive else '<'
        number = place(tex(a, sign, '0'), 'sign')
        number[0].set_color(A_COLOR)
        ineq = place(tex('a', sign, '0'), 'sign')
        ineq[0].set_color(A_COLOR)
        range_interval = ['[', 'd', r',\infty)'] if a_positive else [r'(-\infty,', 'd', ']']
        rng = place(tex(r'\text{Range: }', *range_interval), 'range')
        rng[2].set_color(D_COLOR)
        value = tex(d).set_color(D_COLOR).move_to(rng[2])

        # ---- domain: the inside is >= 0, solve it ------------------------------------------
        self.play(Write(form), run_time=1.3)
        self.beat(f'{ex}_form', 1.0)

        self.say('The inside of a square root must be greater than or equal to zero.')
        # The inside only slides down (a copy, translated and scaled -- no morph), then the
        # real row takes its place.
        inside = VGroup(s1[0], s1[1])
        slide = radicand.copy()
        self.play(Indicate(radicand, color=C_COLOR, scale_factor=1.2), run_time=0.8)
        self.play(slide.animate.scale(inside.width / radicand.width).move_to(inside),
                  FadeIn(VGroup(greater, zero)), run_time=1.0)
        self.remove(slide)
        self.add(inside)
        self.beat(f'{ex}_inside', READ_LONG)

        self.say(f'Solve it for x. The inside is {cfg["words"]}.')
        op_sign, op_number = cfg['op']
        op_left = op_under(op_sign, op_number, moved, OP_SIZE)
        op_right = op_under(op_sign, op_number, zero, OP_SIZE)
        strikes = strike_pair(moved, op_left)
        self.play(FadeIn(op_left, shift=DOWN * 0.15), FadeIn(op_right, shift=DOWN * 0.15),
                  run_time=0.7)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.5)
        self.play(copy_into(rest, s2[0]), FadeIn(s2[1]),
                  copy_into(VGroup(zero, op_right), s2[2]), run_time=1.0)
        self.wait(0.4)

        if flips:
            self.say('Divide by negative one. Dividing by a negative flips the inequality.')
        bars, divisors = divide_bars([s2[0], s2[2]], cfg['div'], OP_SIZE)
        for bar, divisor in zip(bars, divisors):
            self.play(Create(bar), FadeIn(divisor, shift=DOWN * 0.15), run_time=0.7)
        self.play(copy_into(VGroup(s2[0], divisors[0]), s3[0]), run_time=0.9)
        if flips:
            self.play(Indicate(s2[1], color=PAPER_RED, scale_factor=1.5), run_time=1.0)
            s3[1].set_color(PAPER_RED)
            self.play(copy_into(s2[1], s3[1]), run_time=1.1)
            self.wait(0.8)
            self.play(s3[1].animate.set_color(INK), run_time=0.5)
        else:
            self.play(FadeIn(s3[1]), run_time=0.5)
        self.play(copy_into(VGroup(s2[2], divisors[1]), s3[2]), run_time=0.9)
        self.beat(f'{ex}_solved', 0.8)

        # ---- number line, then the interval ------------------------------------------------
        direction = 'right' if right else 'left'
        how = 'at least' if right else 'at most'
        self.say(f'Closed circle on {shown(cfg["point_words"])}, because x can equal it.')
        self.play(FadeOut(VGroup(s1, op_left, op_right, strikes, s2, bars, divisors)),
                  s3.animate.move_to([0, ROW_Y['s3_top'], 0]), run_time=0.9)
        self.play(Create(line), FadeIn(VGroup(minus_inf, plus_inf)), run_time=0.8)
        self.play(FadeIn(dot), copy_into(s3[2], label), run_time=1.0)
        self.beat(f'{ex}_circle', READ_LONG)

        self.say(f'x is {how} {shown(cfg["point_words"])}, so the arrow points {direction}.')
        self.play(GrowArrow(ray), run_time=1.1)
        self.beat(f'{ex}_arrow', READ_LONG)

        self.say(f'Write it as an interval. The endpoint is {C_WORD}.')
        self.play(FadeIn(domain), run_time=1.0)
        self.beat(f'{ex}_domain_form', READ_LONG)

        self.say(f'Here {C_WORD} is {shown(cfg["point_words"])}.')
        self.play(ReplacementTransform(VGroup(domain[0], domain[1], domain[3]),
                                       VGroup(domain_done[0], domain_done[1], domain_done[3])),
                  FadeOut(domain[2]), copy_into(label, domain_done[2]), run_time=1.3)
        self.beat(f'{ex}_domain', READ_LONG)

        # ---- range: same as the quadratic, with d -----------------------------------------
        self.say('The range works like it did for quadratics.')
        self.play(FadeOut(VGroup(s3, line, ray, dot, label, minus_inf, plus_inf)),
                  Write(general), run_time=1.3)
        self.beat(f'{ex}_range_intro', READ_SHORT)

        self.say(f'The sign of {A_WORD} sets which way the range goes.')
        self.play(Indicate(general[2], color=A_COLOR, scale_factor=1.6),
                  Indicate(form[2], color=A_COLOR, scale_factor=1.6), run_time=1.3)
        self.beat(f'{ex}_emphasize_a', READ_LONG)

        self.say(f'Here {A_WORD} is {shown(a)}, which is {number_word}.')
        self.play(copy_into(form[2], number[0]), FadeIn(VGroup(number[1], number[2])),
                  run_time=1.2)
        self.wait(0.9)
        self.say(f'So {A_WORD} is {number_word}.')
        self.play(ReplacementTransform(number, ineq), run_time=1.0)
        self.beat(f'{ex}_sign', READ_SHORT)

        updown = 'up from' if a_positive else 'down from'
        self.say(f'A {number_word} {A_WORD} sends the range {updown} {D_WORD}.')
        self.play(FadeIn(VGroup(rng[0], rng[1], rng[2], rng[3])), run_time=1.1)
        self.beat(f'{ex}_range', READ_LONG)

        end = 'lowest' if a_positive else 'highest'
        self.say(f'{D_WORD} is the {end} point of the graph.')
        self.play(Indicate(general[5], color=D_COLOR, scale_factor=1.6),
                  Indicate(form[5], color=D_COLOR, scale_factor=1.6), run_time=1.3)
        self.beat(f'{ex}_emphasize_d', READ_LONG)

        self.say(f'In this example {D_WORD} is {d}, so {d} replaces {D_WORD}.')
        self.play(FadeOut(rng[2]), copy_into(form[5], value), run_time=1.3)
        self.beat(f'{ex}_interval', READ_LONG)

        self.say(f'The domain comes from the inside. The range comes from {A_WORD} and {D_WORD}.')
        self.beat(f'{ex}_hold', READ_LONG)
        return VGroup(general, form, domain_done, ineq, rng[0], rng[1], rng[3], value)

    def construct(self):
        first = self.teach_example(EXAMPLES['ex1'], 'ex1')
        self.play(FadeOut(first), run_time=0.6)
        self.hush()
        self.wait(0.4)
        self.mark('ex2_start')
        self.teach_example(EXAMPLES['ex2'], 'ex2')
        self.write_marks('sqrt_domain_range_marks.json')
