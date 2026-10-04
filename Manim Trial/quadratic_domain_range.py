"""Vertex-form quadratics: highlight the square, domain all reals, range from a and k.

Two examples on one clip (portal tabs):
    f(x) = 2(x-1)^2 + 3   ->  a > 0, range [3, infinity)
    f(x) = -2(x-1)^2 + 3  ->  a < 0, range (-infinity, 3]

Per example: the square pulses (a quadratic), the domain appears, then the general vertex
form f(x) = a(x-h)^2 + k is written above the example. a and the example's 2 pulse together,
the 2 drops down to "2 > 0" and turns into "a > 0", and the range "[k, infinity)" is written.
Then k and the example's 3 pulse, and the 3 drops down and replaces k. Every caption is said
before the thing it describes appears, and is held long enough to read.

Marks include ex2_start for the second example tab.

PORTRAIT: drawn for the phone player in the 4:5 frame (portrait_frame.py), 6.4 x 8 units.
Every row is built once at its final spot and only fades in, so nothing re-stacks. Every
MathTex is given INK explicitly: its default is white, which vanishes on the paper
background (the first cut shipped that way -- only the pieces that got an accent colour
were visible).
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from manim import (  # noqa: E402
    FadeIn,
    FadeOut,
    Indicate,
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
    Narrated,
    apply_portal_paper_background,
)
from vector_projection_shadow import copy_into  # noqa: E402

apply_portal_paper_background()

INK = PAPER_INK
A_COLOR = PAPER_BLUE
K_COLOR = PAPER_GOLD
H = 1
K = 3
FORM_SIZE = 56
GENERAL_SIZE = 44
RULE_SIZE = 44
MAX_WIDTH = 5.8
# Row centres, top to bottom; the caption owns y > 2.95.
ROW_Y = dict(general=2.3, form=1.3, domain=.2, sign=-.9, range=-2.0)

# Seconds a caption is held after it lands, before the next beat. Sized to the caption.
READ_SHORT = 1.0
READ_LONG = 1.5


def tex(*parts, size=RULE_SIZE):
    return mathtex(*parts, font_size=size, color=INK)


def place(row, name):
    if row.width > MAX_WIDTH:
        row.scale(MAX_WIDTH / row.width)
    return row.move_to([0, ROW_Y[name], 0])


def var(letter, color):
    """A variable inside a caption: italic and coloured, so it is not read as the word 'a'."""
    return f'<span foreground="{color}"><i>{letter}</i></span>'


A_WORD = var('a', A_COLOR)
K_WORD = var('k', K_COLOR)


class QuadraticDomainRange(Narrated, Scene):
    caption_color = PAPER_INK  # PAPER_MUTED read washed out on the white frame
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9

    def build_rows(self, a_display: str, a_positive: bool):
        general = place(tex('f(x)', '=', 'a', '(x-h)^2', '+', 'k', size=GENERAL_SIZE), 'general')
        general[2].set_color(A_COLOR)
        general[5].set_color(K_COLOR)
        form = place(tex('f(x)', '=', a_display, rf'(x-{H})^2', '+', str(K), size=FORM_SIZE), 'form')
        form[2].set_color(A_COLOR)
        form[5].set_color(K_COLOR)
        domain = place(tex(r'\text{Domain: }', r'(-\infty,\infty)'), 'domain')
        sign = '>' if a_positive else '<'
        number = place(tex(a_display, sign, '0'), 'sign')
        number[0].set_color(A_COLOR)
        ineq = place(tex('a', sign, '0'), 'sign')
        ineq[0].set_color(A_COLOR)
        interval = ['[', 'k', r',\infty)'] if a_positive else [r'(-\infty,', 'k', ']']
        rng = place(tex(r'\text{Range: }', *interval), 'range')
        rng[2].set_color(K_COLOR)
        three = tex(str(K)).set_color(K_COLOR).move_to(rng[2])
        return general, form, domain, number, ineq, rng, three

    def beat(self, mark, seconds):
        """Hold the caption long enough to read, then record the pause point."""
        self.wait(seconds)
        self.mark(mark)

    def teach_example(self, a_display: str, a_positive: bool, prefix: str) -> VGroup:
        general, form, domain, number, ineq, rng, three = self.build_rows(a_display, a_positive)
        number_word = 'positive' if a_positive else 'negative'

        self.play(Write(form), run_time=1.3)
        self.beat(f'{prefix}_form', 1.0)

        self.say('The squared term means this is a quadratic.')
        self.play(Indicate(form[3], color=A_COLOR, scale_factor=1.3), run_time=1.1)
        self.beat(f'{prefix}_quadratic', READ_SHORT)

        self.say("A quadratic's domain is all real numbers.")
        self.play(FadeIn(domain), run_time=0.8)
        self.beat(f'{prefix}_domain', READ_LONG)

        self.say('Every quadratic can be written in vertex form.')
        self.play(Write(general), run_time=1.2)
        self.beat(f'{prefix}_vertex_form', READ_SHORT)

        self.say(f'The sign of {A_WORD} sets which way the range goes.')
        self.play(Indicate(general[2], color=A_COLOR, scale_factor=1.6),
                  Indicate(form[2], color=A_COLOR, scale_factor=1.6), run_time=1.3)
        self.beat(f'{prefix}_emphasize_a', READ_LONG)

        self.say(f'Here {A_WORD} is {a_display}, which is {number_word}.'.replace('-2', '−2'))
        self.play(copy_into(form[2], number[0]), FadeIn(VGroup(number[1], number[2])), run_time=1.2)
        self.wait(0.9)
        self.say(f'So {A_WORD} is {number_word}.')
        self.play(ReplacementTransform(number, ineq), run_time=1.0)
        self.beat(f'{prefix}_sign', READ_SHORT)

        direction = 'up from' if a_positive else 'down from'
        self.say(f'A {number_word} {A_WORD} sends the range {direction} {K_WORD}.')
        self.play(FadeIn(VGroup(rng[0], rng[1], rng[2], rng[3])), run_time=1.1)
        self.beat(f'{prefix}_range', READ_LONG)

        end = 'lowest' if a_positive else 'highest'
        self.say(f'{K_WORD} is the {end} point of the graph.')
        self.play(Indicate(general[5], color=K_COLOR, scale_factor=1.6),
                  Indicate(form[5], color=K_COLOR, scale_factor=1.6), run_time=1.3)
        self.beat(f'{prefix}_emphasize_k', READ_LONG)

        self.say(f'In this example {K_WORD} is {K}, so {K} replaces {K_WORD}.')
        self.play(FadeOut(rng[2]), copy_into(form[5], three), run_time=1.3)
        self.beat(f'{prefix}_interval', READ_LONG)

        self.say(f'The range depends on the sign of {A_WORD} and on {K_WORD}.')
        self.beat(f'{prefix}_hold', READ_LONG)
        return VGroup(general, form, domain, ineq, rng[0], rng[1], rng[3], three)

    def construct(self):
        first = self.teach_example('2', True, 'ex1')
        self.play(FadeOut(first), run_time=0.6)
        self.hush()
        self.wait(0.4)
        self.mark('ex2_start')
        self.teach_example('-2', False, 'ex2')
        self.write_marks('quadratic_domain_range_marks.json')
