"""Composite functions: g carries its own domain into (f o g)(x).

One example on one clip:
    f(x) = x^2 + 6,  g(x) = sqrt(x - 2)   ->   (f o g)(x) = x + 4,  domain [2, infinity)

Beats: f and g each sit beside their own domain (centered, with a gap). g's inside >= 0 is
solved below with "Solve for x" (operation under both sides) and the solved line morphs into
g's domain. The composite is built from x^2: x gets parentheses, then a copy of g flies down
into them while they widen; it is squared and simplified to x + 4.

Then the board is cleared: (f o g)(x) = x + 4 on top with y = x + 4 under it and ITS domain beside that
(all reals; "this isn't the domain of the composite"). g comes back with its domain; both number
lines merge onto a third, everything else is cleared, the overlap pulses and the answer is
[2, infinity).

Captions use real LaTeX for every variable and number ($...$, see math_caption.py).

PORTRAIT: 4:5 frame (portrait_frame.py). Every MathTex is given INK explicitly. The clip
ends on a held full board, never a fade.
"""

from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from manim import (  # noqa: E402
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
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
from solve_steps import op_under, strike_pair  # noqa: E402
from tick_number_line import HALF, tick_number_line  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402
from composite_problem_intro import COMPOSITE_INTRO_1, play_composite_problem_intro  # noqa: E402

apply_portal_paper_background()

INK = PAPER_INK
G_COLOR = PAPER_BLUE
TAG_COLOR = PAPER_GOLD
FORM_SIZE = 42
DOM_SIZE = 28
STEP_SIZE = 42
OP_SIZE = 32
COMP_SIZE = 40
MAX_WIDTH = 5.6
PAIR_GAP = 0.45

# Row centres, top to bottom; the caption owns y > 2.95. The solve rows (inside / solved) borrow
# the space the composite work uses later: they are faded out before it appears.
ROW_Y = dict(
    f=2.45, g=1.15,
    inside=0.3, solved=-0.7,
    comp=-0.6, c4=-1.7,
    top=2.3, y_row=1.35, nl_all=0.4, g_again=-0.65, nl_g=-1.75, nl_merge=-2.85,
    nl_final=0.9, c_dom=-0.35,
)
LINE_Y = -1.9

READ_SHORT = 1.0
READ_LONG = 1.5
READ_CAPTION_EXTRA = 2.5  # longer teaching captions before the next beat

NL_BUILD_RUN = 1.1  # tick_number_line.build() — domain solve rows
NL_WIDE_BUILD_RUN = 1.4  # wider merge / all-reals lines
NL_ARROW_RUN = 0.55
NL_HIGHLIGHT_RUN = 0.5  # all_reals, all_but gold arrow

LHS = r'(f\circ g)(x)'
SQRT = r'\sqrt{x-2}'

# Caption math: $...$ is typeset with LaTeX. g is blue, as it is on the board.
G_WORD = '$@b g$'
F_WORD = '$f$'
X_WORD = '$x$'


def row(*parts, y, size=FORM_SIZE, left=None):
    """A line of math at row height `y`: centered, or left-aligned at `left` when given."""
    line = mathtex(*parts, font_size=size, color=INK)
    if line.width > MAX_WIDTH:
        line.scale(MAX_WIDTH / line.width)
    if left is None:
        return line.move_to([0, y, 0])
    return line.move_to([left, y, 0], aligned_edge=LEFT)


def domain_row(interval, y, size=DOM_SIZE):
    return row(r'\text{Domain: }', interval, y=y, size=size)


def pair(fn, dom, y):
    """Function with its domain beside it, the two centered together as one unit."""
    unit = VGroup(fn, dom).arrange(RIGHT, buff=PAIR_GAP)
    if unit.width > MAX_WIDTH:
        unit.scale(MAX_WIDTH / unit.width)
    unit.move_to([0, y, 0])
    return fn, dom


class CompositeDomain(Narrated, Scene):
    caption_color = PAPER_INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9

    def beat(self, mark, seconds):
        self.wait(seconds)
        self.mark(mark)

    def swap_head(self, old, new):
        """Two rows share an identical left-aligned head; hand it over without a double print."""
        self.remove(old[0], old[1])
        self.add(new[0], new[1])

    def construct(self):
        # ---- every row, built once at its final spot -----------------------------------
        f_row, f_dom = pair(
            row('f(x)', '=', 'x^2', '+', '6', y=0),
            domain_row(r'(-\infty,\infty)', 0), ROW_Y['f'])
        g_row = row('g(x)', '=', SQRT, y=0)
        g_row[2].set_color(G_COLOR)
        g_row, g_dom = pair(g_row, domain_row(r'[2,\infty)', 0), ROW_Y['g'])

        play_composite_problem_intro(self, COMPOSITE_INTRO_1, f_row, g_row)

        inside_row = row('x', '-2', r'\geq', '0', y=ROW_Y['inside'], size=STEP_SIZE)
        moved, zero = inside_row[1], inside_row[3]
        solved = row('x', r'\geq', '2', y=ROW_Y['solved'], size=STEP_SIZE)

        comp_y = ROW_Y['comp']
        c_full = row(LHS, '=', '(', SQRT, ')^2', '+', '6', y=comp_y, size=COMP_SIZE)
        c_full[3].set_color(G_COLOR)
        left = c_full.get_left()[0]  # every composite row shares this head position
        c_x = row(LHS, '=', 'x^2', '+', '6', y=comp_y, size=COMP_SIZE, left=left)
        c_paren = row(LHS, '=', '(', 'x', ')^2', '+', '6', y=comp_y, size=COMP_SIZE, left=left)
        c_paren[3].set_color(TAG_COLOR)
        c3 = row(LHS, '=', 'x-2', '+', '6', y=comp_y, size=COMP_SIZE, left=left)
        c4 = row(LHS, '=', 'x+4', y=ROW_Y['c4'], size=COMP_SIZE, left=left)

        # the closing board: (f o g)(x) on top, y = x + 4 beside ITS domain, g beside its domain
        top_fn = row(LHS, '=', 'x+4', y=ROW_Y['top'], size=COMP_SIZE)
        y_row, y_dom = pair(
            row('y', '=', 'x+4', y=0), domain_row(r'(-\infty,\infty)', 0), ROW_Y['y_row'])
        g2 = row('g(x)', '=', SQRT, y=0)
        g2[2].set_color(G_COLOR)
        g2, g2_dom = pair(g2, domain_row(r'[2,\infty)', 0), ROW_Y['g_again'])
        c_dom = domain_row(r'[2,\infty)', ROW_Y['c_dom'], size=36)

        # solving g: a proper number line under the answer (dot on 2, arrow to the right)
        solve_nl = tick_number_line(LINE_Y)
        solve_ray = solve_nl.from_two()
        minus_inf = row(r'-\infty', y=LINE_Y - 0.8, size=30).set_x(-HALF)
        plus_inf = row(r'\infty', y=LINE_Y - 0.8, size=30).set_x(HALF)
        number_line = VGroup(solve_nl.everything, minus_inf, plus_inf, solve_ray)

        # the closing board: all reals, then g's domain, then both merged onto a third line
        nl_all = tick_number_line(ROW_Y['nl_all'])
        nl_g = tick_number_line(ROW_Y['nl_g'])
        nl_merge = tick_number_line(ROW_Y['nl_merge'])

        # ---- the two functions, each beside its own domain ------------------------------
        self.say('Start with the domain of each function.')
        self.beat('form', 1.0)

        self.say(f'The squared term means {F_WORD} is a quadratic.')
        self.play(Indicate(f_row[2], color=G_COLOR, scale_factor=1.3), run_time=1.1)
        self.beat('f_quadratic', READ_SHORT)

        self.say("A quadratic's domain is all real numbers.")
        self.play(FadeIn(f_dom), run_time=0.8)
        self.beat('f_domain', READ_LONG)

        # ---- domain of g: solve inside >= 0 ---------------------------------------------
        self.say('The inside of a square root must be at least $0$.')
        radicand = VGroup(*g_row[2].submobjects[2:])
        self.play(Indicate(radicand, color=G_COLOR, scale_factor=1.2), run_time=0.8)
        self.play(
            copy_into(radicand, VGroup(inside_row[0], moved)),
            FadeIn(VGroup(inside_row[2], zero)),
            run_time=1.1,
        )
        self.beat('g_inside', READ_LONG)

        self.say(f'Solve for {X_WORD}.')
        op_left = op_under('+', '2', moved, OP_SIZE)
        op_right = op_under('+', '2', zero, OP_SIZE)
        strikes = strike_pair(moved, op_left)
        self.play(
            FadeIn(op_left, shift=DOWN * 0.15),
            FadeIn(op_right, shift=DOWN * 0.15),
            run_time=0.7,
        )
        self.beat('g_op', 0.6)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.5)
        self.play(
            copy_into(inside_row[0], solved[0]),
            FadeIn(solved[1]),
            copy_into(VGroup(zero, op_right), solved[2]),
            run_time=1.1,
        )
        self.beat('g_solved', READ_LONG)

        self.say(f'Closed circle on $2$, because {X_WORD} can equal it.')
        self.play(solve_nl.build(), run_time=NL_BUILD_RUN)
        self.play(FadeIn(VGroup(minus_inf, plus_inf)), run_time=0.5)
        self.play(
            FadeIn(solve_ray[1]),
            solve_nl.ticks[2][1].animate.set_color(G_COLOR),
            run_time=1.0,
        )
        self.beat('g_circle', READ_LONG)

        self.say(f'{X_WORD} is at least $2$, so the arrow points right.')
        self.play(GrowArrow(solve_ray[0]), run_time=NL_ARROW_RUN)
        self.beat('g_arrow', READ_LONG)

        self.say(f'In interval notation, that is the domain of {G_WORD}.')
        self.play(FadeIn(g_dom[0]), copy_into(solved, g_dom[1]), run_time=1.1)
        self.play(
            FadeOut(VGroup(inside_row, op_left, op_right, strikes, solved, number_line)),
            run_time=0.7,
        )
        self.beat('g_domain', READ_LONG)

        # ---- the composite: x^2 -> (x)^2 -> g flies in ----------------------------------
        self.say(r'The $\circ$ in $(f\circ g)(x)$ means $f$ composed with $@b g$.')
        self.wait(READ_LONG)
        self.say(f'This means {G_WORD} replaces every {X_WORD} in {F_WORD}.')
        self.wait(READ_CAPTION_EXTRA)
        self.play(Indicate(f_row[2], color=TAG_COLOR, scale_factor=1.3), run_time=1.0)
        self.play(FadeIn(c_x[0]), FadeIn(c_x[1]), copy_into(f_row[2:], c_x[2:]), run_time=1.1)
        self.beat('composite_x', READ_SHORT)

        self.say(f'Wrap the {X_WORD} in parentheses.')
        self.play(
            FadeOut(c_x[2]),
            FadeIn(c_paren[2:5]),
            ReplacementTransform(c_x[3], c_paren[5]),
            ReplacementTransform(c_x[4], c_paren[6]),
            run_time=1.0,
        )
        self.swap_head(c_x, c_paren)
        self.beat('composite_paren', READ_SHORT)

        self.say(f'Replace {X_WORD} with {G_WORD}.')
        g_drop = g_row[2].copy()
        self.play(
            FadeOut(c_paren[3]),
            ReplacementTransform(g_drop, c_full[3]),
            ReplacementTransform(c_paren[2], c_full[2]),
            ReplacementTransform(c_paren[4], c_full[4]),
            ReplacementTransform(c_paren[5], c_full[5]),
            ReplacementTransform(c_paren[6], c_full[6]),
            run_time=1.6,
        )
        self.swap_head(c_paren, c_full)
        self.beat('composite_written', READ_LONG)

        # ---- simplify: square, then combine ---------------------------------------------
        self.say('Squaring cancels the square root, leaving $x-2$.')
        cancel = strike_pair(c_full[3].submobjects[0], c_full[4].submobjects[-1])
        self.play(Create(cancel[0]), Create(cancel[1]), run_time=0.9)
        self.beat('cancel', READ_SHORT)
        inner = VGroup(*c_full[3].submobjects[2:])
        self.play(
            FadeOut(c_full[2]),
            FadeOut(c_full[4]),
            FadeOut(cancel),
            copy_into(inner, c3[2]),
            FadeOut(c_full[3]),
            ReplacementTransform(c_full[5], c3[3]),
            ReplacementTransform(c_full[6], c3[4]),
            run_time=1.2,
        )
        self.swap_head(c_full, c3)
        self.beat('squared', READ_SHORT)

        self.say('Combine the numbers: $-2+6=4$.')
        self.play(
            FadeIn(VGroup(c4[0], c4[1])),
            copy_into(VGroup(c3[2], c3[3], c3[4]), c4[2]),
            run_time=1.1,
        )
        self.beat('simplified', READ_LONG)

        # ---- clear the board: (f o g)(x) on top, y = x + 4 underneath -------------------
        self.say('Now the domain of the composite. Start with the result, $x+4$.')
        self.play(
            FadeOut(VGroup(f_row, f_dom, g_row, g_dom, c3)),
            FadeIn(VGroup(y_row[0], y_row[1])),
            copy_into(c4[2], y_row[2]),
            ReplacementTransform(c4[0], top_fn[0]),
            ReplacementTransform(c4[1], top_fn[1]),
            ReplacementTransform(c4[2], top_fn[2]),
            run_time=1.4,
        )
        self.beat('domain_intro', READ_SHORT)

        self.say('$x+4$ is linear, so by itself its domain is all real numbers.')
        self.play(FadeIn(y_dom), run_time=1.0)
        self.beat('domain_linear', READ_LONG)

        self.say('On a number line, that is every number in both directions.')
        self.play(nl_all.build(), run_time=NL_WIDE_BUILD_RUN)
        all_reals = nl_all.all_reals()
        self.play(Create(all_reals), run_time=NL_HIGHLIGHT_RUN)
        self.beat('nl_all', READ_LONG)

        self.say("This isn't the actual domain of the composite.")
        self.beat('not_composite', READ_SHORT)

        self.say('Any function plugged into another brings its domain with it.')
        self.beat('domain_follows', READ_LONG)

        self.say(f'Since {G_WORD} was plugged into {F_WORD}, bring its domain into the composite.')
        self.play(FadeIn(g2), FadeIn(g2_dom), run_time=1.1)
        self.play(nl_g.build(), run_time=NL_WIDE_BUILD_RUN)
        g_ray = nl_g.from_two()
        self.play(copy_into(g2_dom[1], g_ray), run_time=1.2)
        self.beat('g_back', READ_LONG)

        self.say('The domain of the composite is where the two lines overlap.')
        self.play(nl_merge.build(), run_time=NL_WIDE_BUILD_RUN)
        merged_all = nl_merge.all_reals()
        merged_g = nl_merge.from_two()
        self.play(
            ReplacementTransform(all_reals.copy(), merged_all),
            ReplacementTransform(g_ray.copy(), merged_g),
            run_time=1.8,
        )
        self.beat('merge', READ_LONG)

        # ---- clean up: only (f o g)(x) and the merged line, moved up beneath it ---------
        merged = VGroup(nl_merge.everything, merged_all, merged_g)
        self.play(
            FadeOut(VGroup(y_row, y_dom, nl_all.everything, all_reals,
                           g2, g2_dom, nl_g.everything, g_ray)),
            merged.animate.shift(UP * (ROW_Y['nl_final'] - ROW_Y['nl_merge'])),
            run_time=1.6,
        )
        self.beat('cleanup', READ_SHORT)

        self.play(Indicate(merged_g, color=G_COLOR, scale_factor=1.15), run_time=1.2)
        self.play(Indicate(merged_g, color=G_COLOR, scale_factor=1.15), run_time=1.2)
        self.beat('overlap', READ_SHORT)

        self.play(FadeOut(merged_all), run_time=1.0)
        self.say('The domain of the composite is $[2,\\infty)$.')
        self.play(FadeIn(c_dom), run_time=1.3)
        self.beat('hold', READ_LONG)
        self.write_marks('composite_domain_marks.json')
