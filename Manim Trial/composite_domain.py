"""Composite functions: g carries its own domain into (f o g)(x).

One example on one clip:
    f(x) = x^2 + 6,  g(x) = sqrt(x - 2)   ->   (f o g)(x) = x + 4,  domain [2, infinity)

Beats: the domain of f (a quadratic: all reals); the domain of g (the inside must be >= 0,
solved quickly and silently with the house operation-under-both-sides style, as in
sqrt_domain_range.py); then the composite -- g is put in for x in f (a copy of g slides into the
slot, no morph), and a gold "x >= 2" tag appears under it because g brings its own domain along.
The square cancels the root and the work simplifies to x + 4. Read alone, x + 4 accepts every
number, so the tag slides down beside the result: the composite's domain is [2, infinity).

PORTRAIT: 4:5 frame (portrait_frame.py). Rows are built once at their final spot and only fade
in. Every MathTex is given INK explicitly (the default is white on the white frame). The clip
ends on a held full board, never a fade.
"""

from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
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
from solve_steps import op_under, strike_pair  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402

apply_portal_paper_background()

INK = PAPER_INK
G_COLOR = PAPER_BLUE
TAG_COLOR = PAPER_GOLD
FORM_SIZE = 46
RULE_SIZE = 40
STEP_SIZE = 40
OP_SIZE = 32
MAX_WIDTH = 5.8
# Row centres, top to bottom; the caption owns y > 2.95. s1/s2 (the solve) borrow the space the
# composite work uses later: they are faded out before it appears.
ROW_Y = dict(f=2.45, f_dom=1.8, g=1.0, g_dom=.35, s1=.35, s2=-.95,
             c2=-.55, tag=-1.15, c3=-1.85, c4=-2.55, c_dom=-3.3)

READ_SHORT = 1.0
READ_LONG = 1.5

LHS = r'(f\circ g)(x)'
SQRT = r'\sqrt{x-2}'


def tex(*parts, size=RULE_SIZE):
    return mathtex(*parts, font_size=size, color=INK)


def place(row, name):
    if row.width > MAX_WIDTH:
        row.scale(MAX_WIDTH / row.width)
    return row.move_to([0, ROW_Y[name], 0])


def var(letter, color):
    """A variable inside a caption: italic and coloured, so it is not read as a word."""
    return f'<span foreground="{color}"><i>{letter}</i></span>'


G_WORD = var('g', G_COLOR)
F_WORD = var('f', INK)
X_WORD = var('x', INK)


class CompositeDomain(Narrated, Scene):
    caption_color = PAPER_INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9

    def beat(self, mark, seconds):
        self.wait(seconds)
        self.mark(mark)

    def construct(self):
        # ---- every row, built once at its final spot -----------------------------------
        f_row = place(tex('f(x)', '=', 'x^2', '+', '6', size=FORM_SIZE), 'f')
        g_row = place(tex('g(x)', '=', SQRT, size=FORM_SIZE), 'g')
        g_row[2].set_color(G_COLOR)
        f_dom = place(tex(r'\text{Domain: }', r'(-\infty,\infty)'), 'f_dom')
        g_dom = place(tex(r'\text{Domain: }', r'[2,\infty)'), 'g_dom')

        inside_row = place(tex('x', '-2', r'\geq', '0', size=STEP_SIZE), 's1')
        moved, zero = inside_row[1], inside_row[3]
        solved = place(tex('x', r'\geq', '2', size=STEP_SIZE), 's2')

        c2 = place(tex(LHS, '=', '(', SQRT, ')^2', '+', '6', size=FORM_SIZE - 4), 'c2')
        c2[3].set_color(G_COLOR)
        slot = tex('x', size=FORM_SIZE - 4).set_color(TAG_COLOR).move_to(c2[3])
        tag = tex(r'x\geq 2', size=36).set_color(TAG_COLOR)
        tag.move_to([c2[3].get_center()[0], ROW_Y['tag'], 0])
        c3 = tex(LHS, '=', 'x-2', '+', '6', size=FORM_SIZE - 4)
        c3.move_to([0, ROW_Y['c3'], 0]).align_to(c2, LEFT)
        c4 = tex(LHS, '=', 'x+4', size=FORM_SIZE - 4)
        c4.move_to([0, ROW_Y['c4'], 0]).align_to(c2, LEFT)
        tag_end = tag.copy().next_to(c4, buff=0.4).set_y(ROW_Y['c4'])
        c_dom = place(tex(r'\text{Domain: }', r'[2,\infty)'), 'c_dom')

        # ---- the two functions ---------------------------------------------------------
        self.say('Start with the domain of each function.')
        self.play(Write(f_row), Write(g_row), run_time=1.4)
        self.beat('form', 1.0)

        # ---- domain of f ---------------------------------------------------------------
        self.say(f'The squared term means {F_WORD} is a quadratic.')
        self.play(Indicate(f_row[2], color=G_COLOR, scale_factor=1.3), run_time=1.1)
        self.beat('f_quadratic', READ_SHORT)

        self.say("A quadratic's domain is all real numbers.")
        self.play(FadeIn(f_dom), run_time=0.8)
        self.beat('f_domain', READ_LONG)

        # ---- domain of g: the inside must be >= 0 --------------------------------------
        self.say('The inside of a square root must be at least 0.')
        radicand = VGroup(*g_row[2].submobjects[2:])
        inside = VGroup(inside_row[0], inside_row[1])
        slide = radicand.copy()
        self.play(Indicate(radicand, color=G_COLOR, scale_factor=1.2), run_time=0.8)
        self.play(slide.animate.scale(inside.width / radicand.width).move_to(inside),
                  FadeIn(VGroup(inside_row[2], zero)), run_time=1.0)
        self.remove(slide)
        self.add(inside)
        self.beat('g_inside', READ_LONG)

        self.say('Add 2 to both sides to solve for x.')
        op_left = op_under('+', '2', moved, OP_SIZE)
        op_right = op_under('+', '2', zero, OP_SIZE)
        strikes = strike_pair(moved, op_left)
        self.play(FadeIn(op_left, shift=DOWN * 0.15), FadeIn(op_right, shift=DOWN * 0.15),
                  run_time=0.7)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.5)
        self.play(copy_into(inside_row[0], solved[0]), FadeIn(solved[1]),
                  copy_into(VGroup(zero, op_right), solved[2]), run_time=1.0)
        self.beat('g_solved', 0.8)

        self.say(f'So x is 2 or more. That is the domain of {G_WORD}.')
        self.play(FadeOut(VGroup(inside_row, op_left, op_right, strikes, solved)), run_time=0.7)
        self.play(FadeIn(g_dom), run_time=0.9)
        self.beat('g_domain', READ_LONG)

        # ---- the composite: put g in for x ---------------------------------------------
        self.say(f'Now the composite: put {G_WORD} in for every {X_WORD} in {F_WORD}.')
        self.play(Indicate(f_row[2], color=TAG_COLOR, scale_factor=1.3), run_time=1.0)
        self.play(FadeIn(VGroup(c2[0], c2[1], c2[2], c2[4], c2[5], c2[6])), FadeIn(slot),
                  run_time=1.1)
        self.beat('composite_setup', READ_SHORT)

        self.say(f'Here {G_WORD} takes the place of {X_WORD}.')
        drop = g_row[2].copy()
        self.play(drop.animate.scale(c2[3].width / g_row[2].width).move_to(c2[3]),
                  FadeOut(slot), run_time=1.2)
        self.remove(drop)
        self.add(c2[3])
        self.beat('g_drops_in', READ_SHORT)

        self.say(f'{G_WORD} brings its domain along: x must be 2 or more.')
        self.play(Indicate(g_dom[1], color=TAG_COLOR, scale_factor=1.3), run_time=0.9)
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.9)
        self.beat('g_tag', READ_LONG)

        # ---- simplify ------------------------------------------------------------------
        self.say('Squaring undoes the square root, leaving x − 2.')
        self.play(Indicate(VGroup(c2[3], c2[4]), color=G_COLOR, scale_factor=1.15),
                  run_time=1.0)
        inner = VGroup(*c2[3].submobjects[2:])
        self.play(FadeIn(VGroup(c3[0], c3[1], c3[3], c3[4])), copy_into(inner, c3[2]),
                  run_time=1.1)
        self.beat('squared', READ_SHORT)

        self.say('Combine the numbers: −2 plus 6 is 4.')
        self.play(FadeIn(VGroup(c4[0], c4[1])),
                  copy_into(VGroup(c3[2], c3[3], c3[4]), c4[2]), run_time=1.1)
        self.beat('simplified', READ_LONG)

        # ---- the domain depends on g's domain too ---------------------------------------
        self.say('By itself, x + 4 accepts every number.')
        self.play(Indicate(c4[2], color=G_COLOR, scale_factor=1.2), run_time=1.0)
        self.beat('domain_trap', READ_SHORT)

        self.say(f'But {G_WORD} came in with x ≥ 2, and it still applies.')
        carry = tag.copy()
        self.play(carry.animate.move_to(tag_end), run_time=1.2)
        self.play(Indicate(carry, color=TAG_COLOR, scale_factor=1.3), run_time=0.9)
        self.beat('domain_carry', READ_LONG)

        self.say(f'The domain depends on the result and on {G_WORD}.')
        self.play(FadeIn(c_dom), run_time=1.0)
        self.beat('composite_domain', READ_LONG)

        self.say('The domain of the composite is 2 or more.')
        self.beat('hold', READ_LONG)
        self.write_marks('composite_domain_marks.json')
