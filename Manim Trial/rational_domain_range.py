"""Graphing-form rationals: the denominator sets the domain, d sets the range.

Two examples on one clip (portal tabs):
    f(x) = 4/(x-5) + 3   ->  domain skips 5, range skips 3
    f(x) = -2/(x+3) + 1  ->  domain skips -3, range skips 1

DOMAIN, per example: the concrete example, then the general form, then "Finding domain"
and "Set x - c not equal to zero to find what value cannot be in the domain" before
x - c != 0 is written from the template denominator. The example's own denominator
replaces x - c; both sides are adjusted
to isolate x, and "x cannot be 5" is written. A number line gets an open circle on 5 and
arrows that run both ways but skip it, which is why the interval is split in two:
(-inf, c) U (c, inf). The 5 then fills both c slots.

RANGE, per example: "a/(x-c) can never be zero" is only said. "y cannot be d" is written,
turns into "y cannot be 3", and then the interval (-inf, d) U (d, inf) appears and the 3
fills both slots. No number line.

Solving for x copies SlopeInterceptForm.move_x: the operation goes under both sides in gold,
the cancelling pair is struck in red, and the new line is built from copies.
Asymptotes are never mentioned: students have not met them yet.

PORTRAIT: 4:5 frame (portrait_frame.py). Every row is built once at its final spot. Every
MathTex is given INK explicitly (the default is white on the white frame).
"""

from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    Line,
    MathTex,
    ReplacementTransform,
    Scene,
    VGroup,
    Write,
)

from math_notation import NEG, mathtex  # noqa: E402
from scene_style import (  # noqa: E402
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    PAPER_RED,
    Narrated,
    apply_portal_paper_background,
)
from scene_style import PORTAL_PAGE_WHITE  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

apply_portal_paper_background()

INK = PAPER_INK
C_COLOR = PAPER_BLUE
D_COLOR = PAPER_GOLD
NEQ = r'\neq'
FORM_SIZE = 50
GENERAL_SIZE = 40
RULE_SIZE = 38
MAX_WIDTH = 5.75
# Row centres, top to bottom; the caption owns y > 2.95.
ROW_Y = dict(
    general=2.45, form=1.05,
    step1=-0.3, step3=-1.55,
    never=-0.3,
    domain=-2.38, range=-3.22,
)
OP_COLOR = PAPER_GOLD  # what we do to both sides, as in slope_intercept_form.py
LINE_Y = -1.55
LINE_HALF = 2.0
INF_X = 2.52
INTERVAL_SIZE = 34

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


def shown(number: str) -> str:
    """A number as the caption prints it: a real minus sign."""
    return number.replace('-', '\u2212')


def as_tex(number: str) -> str:
    """A number as the equations print it: Chase's short negative."""
    return NEG + number[1:] if number.startswith('-') else number


C_WORD = var('c', C_COLOR)
D_WORD = var('d', D_COLOR)


def numerator(value, size):
    """(whole numerator, the digits the bar is centred on). A negative hangs left of the bar."""
    digits = value.lstrip('-')
    digit = tex(digits, size=size)
    if digits == value:
        return digit, digit
    neg = MathTex(NEG, font_size=size, color=INK).next_to(digit, LEFT, buff=0.1)
    return VGroup(neg, digit), digit


def fraction(top, anchor, bottom):
    """top over bottom with a division bar -> VGroup(top, bar, bottom)."""
    width = max(anchor.width, bottom.width) + 0.24
    bar = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=INK, stroke_width=3)
    top.next_to(bar, UP, buff=0.1)
    top.shift(RIGHT * (0 - anchor.get_center()[0]))
    bottom.next_to(bar, DOWN, buff=0.1)
    return VGroup(top, bar, bottom)


def function_row(size, a, prefix, number, tail_value):
    """f(x) = a / (prefix number) + tail. Parts: row[1][2][1] is c, row[2][1] is d."""
    top, anchor = numerator(a, size)
    bottom = tex('x', prefix[-1] + number, size=size)  # x alone, so it can flash
    bottom[1].set_color(C_COLOR)
    frac = fraction(top, anchor, bottom)
    lhs = tex('f(x)', '=', size=size)
    tail = tex('+', tail_value, size=size)
    tail[1].set_color(D_COLOR)
    row = VGroup(lhs, frac, tail).arrange(RIGHT, buff=0.18)
    axis = lhs[1].get_center()[1]
    frac.shift(UP * (axis - frac[1].get_center()[1]))
    tail.shift(UP * (axis - tail[0].get_center()[1]))
    return row


def operation(sign, digits):
    """'+5' or '-3' as the thing done to both sides: a full minus, never the short negative."""
    return tex(sign, digits).set_color(OP_COLOR)


def interval_row(label, first, second, size=INTERVAL_SIZE):
    """Domain: (-inf, first) U (second, inf); the two slots are parts 2 and 4."""
    return tex(label, r'(-\infty,', first, r')\cup(', second, r',\infty)', size=size)


class RationalDomainRange(Narrated, Scene):
    caption_color = PAPER_INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9

    def beat(self, mark, seconds):
        self.wait(seconds)
        self.mark(mark)

    def fill_slots(self, holder, final, source):
        """Morph the placeholder row into the filled one; the source value lands in both slots."""
        keep = (0, 1, 3, 5)
        right = source.copy()
        return [
            ReplacementTransform(VGroup(*[holder[i] for i in keep]),
                                 VGroup(*[final[i] for i in keep])),
            FadeOut(VGroup(holder[2], holder[4])),
            copy_into(source, final[2]),
            copy_into(right, final[4]),
        ]

    def number_line(self, c_text):
        left = Arrow([-0.17, LINE_Y, 0], [-LINE_HALF, LINE_Y, 0], buff=0, color=INK,
                     stroke_width=4, tip_length=0.2)
        right = Arrow([0.17, LINE_Y, 0], [LINE_HALF, LINE_Y, 0], buff=0, color=INK,
                      stroke_width=4, tip_length=0.2)
        circle = Circle(radius=0.14, color=C_COLOR, stroke_width=5)
        circle.set_fill(PORTAL_PAGE_WHITE, 1).move_to([0, LINE_Y, 0])
        label = tex(c_text).set_color(C_COLOR).move_to([0, LINE_Y - 0.42, 0])
        # No numbers in between -- just where the line runs out in each direction.
        minus_inf = tex(r'-\infty', size=34).move_to([-INF_X, LINE_Y, 0])
        plus_inf = tex(r'\infty', size=34).move_to([INF_X, LINE_Y, 0])
        return left, right, circle, label, minus_inf, plus_inf

    def teach_example(self, a, prefix, number, d, ex):
        minus = prefix.endswith('-')
        c_value = number if minus else '-' + number
        c_text = as_tex(c_value)
        bottom_words = 'x ' + ('\u2212' if minus else '+') + f' {number}'
        undo_sign = '+' if minus else '-'
        general = place(function_row(GENERAL_SIZE, 'a', 'x-', 'c', 'd'), 'general')
        form = place(function_row(FORM_SIZE, a, prefix, number, str(d)), 'form')
        form_bottom, form_d = form[1][2], form[2][1]
        general_bottom, general_d = general[1][2], general[2][1]

        # x and its term are separate parts, so the term can be struck and x copied down
        cond1 = place(tex('x', '-c', NEQ, '0'), 'step1')
        cond1[1].set_color(C_COLOR)
        cond2 = place(tex('x', prefix[-1] + number, NEQ, '0'), 'step1')
        cond2[1].set_color(C_COLOR)
        moved, zero_side = cond2[1], cond2[3]
        isolated = place(tex('x', NEQ, c_text), 'step3')
        isolated[2].set_color(C_COLOR)

        left, right, circle, label, minus_inf, plus_inf = self.number_line(c_text)
        domain = place(interval_row(r'\text{Domain: }', 'c', 'c'), 'domain')
        domain[2].set_color(C_COLOR)
        domain[4].set_color(C_COLOR)
        domain_done = place(interval_row(r'\text{Domain: }', c_text, c_text), 'domain')
        domain_done[2].set_color(C_COLOR)
        domain_done[4].set_color(C_COLOR)

        never = place(tex('y', NEQ, 'd'), 'never')
        never[2].set_color(D_COLOR)
        never_done = place(tex('y', NEQ, str(d)), 'never')
        never_done[2].set_color(D_COLOR)
        rng = place(interval_row(r'\text{Range: }', 'd', 'd'), 'range')
        rng[2].set_color(D_COLOR)
        rng[4].set_color(D_COLOR)
        rng_done = place(interval_row(r'\text{Range: }', str(d), str(d)), 'range')
        rng_done[2].set_color(D_COLOR)
        rng_done[4].set_color(D_COLOR)

        # ---- example, template, then finding domain ------------------------------------
        self.play(Write(form), run_time=1.3)
        self.beat(f'{ex}_form', 1.0)

        self.say('Rational functions in this class look like this.')
        self.play(Write(general), run_time=1.2)
        self.beat(f'{ex}_general', READ_SHORT)

        self.say('Finding domain.')
        self.beat(f'{ex}_finding_domain', READ_SHORT)

        self.say(
            f'Set x \u2212 {C_WORD} \u2260 0 to find what value cannot be in the domain.'
        )
        self.play(Indicate(general_bottom, color=C_COLOR, scale_factor=1.3),
                  copy_into(general_bottom, VGroup(cond1[0], cond1[1])),
                  FadeIn(VGroup(cond1[2], cond1[3])), run_time=1.3)
        self.beat(f'{ex}_template', READ_LONG)

        self.say(f'In this problem the bottom is {bottom_words}.')
        self.play(Indicate(form_bottom, color=C_COLOR, scale_factor=1.3),
                  ReplacementTransform(cond1, cond2), run_time=1.3)
        self.beat(f'{ex}_actual', READ_SHORT)

        # Solving is quick and silent -- the caption above stays up. Same pattern as
        # SlopeInterceptForm.move_x: the operation goes under both sides, the cancelling
        # pair is struck, and the new line is built from copies.
        op_left = operation(undo_sign, number).next_to(moved, DOWN, buff=0.3)
        op_right = operation(undo_sign, number).next_to(zero_side, DOWN, buff=0.3)
        strikes = VGroup(*[
            Line(term.get_corner([-1, -1, 0]) + [-0.08, -0.05, 0],
                 term.get_corner([1, 1, 0]) + [0.08, 0.05, 0],
                 color=PAPER_RED, stroke_width=6)
            for term in (moved, op_left)
        ])
        self.play(FadeIn(op_left, shift=DOWN * 0.15), FadeIn(op_right, shift=DOWN * 0.15),
                  run_time=0.6)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.5)
        self.play(
            FadeOut(VGroup(cond2, op_left, op_right, strikes)),
            copy_into(cond2[0], isolated[0]),
            FadeIn(isolated[1]),
            copy_into(op_right, isolated[2]),
            run_time=0.9,
        )
        self.play(isolated.animate.move_to([0, ROW_Y['step1'], 0]), run_time=0.35)
        self.beat(f'{ex}_x_value', 0.5)

        self.say(f'To write the domain, put an open circle on {shown(c_value)}.')
        self.play(FadeIn(circle), copy_into(isolated[2], label), run_time=1.1)
        self.beat(f'{ex}_circle', READ_LONG)

        self.say(f'The line runs from negative infinity to infinity, but it skips {shown(c_value)}.')
        self.play(GrowArrow(left), GrowArrow(right), FadeIn(VGroup(minus_inf, plus_inf)),
                  run_time=1.2)
        self.beat(f'{ex}_arrows', READ_LONG)

        self.say(f'Skipping {C_WORD} splits the domain into two intervals.')
        self.play(FadeIn(domain), run_time=1.0)
        self.beat(f'{ex}_domain_form', READ_LONG)

        self.say(f'Here {C_WORD} is {shown(c_value)}.')
        c_slot = tex(c_text).set_color(C_COLOR).move_to(label)
        self.play(*self.fill_slots(domain, domain_done, c_slot), FadeOut(c_slot), run_time=1.3)
        self.beat(f'{ex}_domain', READ_LONG)

        # ---- range: a/(x-c) is never zero, so y is never d (said, not written) ---------
        self.say(f'Now the range. The fraction a over x \u2212 {C_WORD} can never be zero.')
        self.play(FadeOut(VGroup(left, right, circle, label, minus_inf, plus_inf, isolated)),
                  Indicate(general[1], color=C_COLOR, scale_factor=1.15), run_time=1.3)
        self.beat(f'{ex}_zero', READ_LONG)

        self.say(f'So y can never be {D_WORD}.')
        self.play(Indicate(general_d, color=D_COLOR, scale_factor=1.6),
                  FadeIn(never), run_time=1.2)
        self.beat(f'{ex}_never', READ_LONG)

        self.say(f'In this example {D_WORD} is {d}, so y can never be {d}.')
        self.play(
            Indicate(form_d, color=D_COLOR, scale_factor=1.6),
            ReplacementTransform(never, never_done),
            run_time=1.3,
        )
        self.beat(f'{ex}_never_value', READ_LONG)

        self.say(f'Skip over {D_WORD}, just like we skipped over {C_WORD}.')
        self.play(FadeIn(rng), run_time=1.0)
        self.beat(f'{ex}_range_form', READ_LONG)

        self.say(f'Here {D_WORD} is {d}.')
        d_slot = tex(str(d)).set_color(D_COLOR).move_to(never_done[2])
        self.play(*self.fill_slots(rng, rng_done, d_slot), FadeOut(d_slot), run_time=1.3)
        self.beat(f'{ex}_range', READ_LONG)

        self.say(f'The domain comes from {C_WORD} and the range comes from {D_WORD}.')
        self.beat(f'{ex}_hold', READ_LONG)
        return VGroup(general, form, domain_done, never_done, rng_done)

    def construct(self):
        first = self.teach_example('4', 'x-', '5', 3, 'ex1')
        self.play(FadeOut(first), run_time=0.6)
        self.hush()
        self.wait(0.4)
        self.mark('ex2_start')
        self.teach_example('-2', 'x+', '3', 1, 'ex2')
        self.write_marks('rational_domain_range_marks.json')
