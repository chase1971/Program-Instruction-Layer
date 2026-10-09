"""Composite functions, example 3: a rational function with a square root plugged in.

    f(x) = 1/(x - 4),  g(x) = sqrt(2 - x)
        ->  (f o g)(x) = 1/(sqrt(2 - x) - 4),  domain (-inf, -14) U (-14, 2]

Same structure as examples 1 and 2 (composite_domain.py / composite_domain_2.py): each function
beside its own domain, the composite built by wrapping x in parentheses and flying g in, then the
board is cleared. Here the composite has a restriction of its OWN: call it y and the bottom can't
be zero, which rules out x = -14 (solved on screen). g brings x <= 2 with it, and the two number
lines merge: everything except -14, but only up to 2.

Row helpers and sizes are shared with example 1. The fraction rows are built from a numerator, a
bar and a denominator so the denominator can be taken apart (x -> (x) -> sqrt(2 - x)).
"""

from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from types import SimpleNamespace  # noqa: E402

from manim import (  # noqa: E402
    DOWN,
    UP,
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

from composite_domain import (  # noqa: E402
    COMP_SIZE,
    FORM_SIZE,
    G_COLOR,
    INK,
    NL_ARROW_RUN,
    NL_BUILD_RUN,
    NL_HIGHLIGHT_RUN,
    NL_WIDE_BUILD_RUN,
    OP_SIZE,
    READ_CAPTION_EXTRA,
    READ_LONG,
    READ_SHORT,
    ROW_Y,
    STEP_SIZE,
    TAG_COLOR,
    domain_row,
    pair,
    row,
)
from math_notation import mathtex  # noqa: E402
from scene_style import PAPER_INK, PAPER_RED, Narrated, apply_portal_paper_background  # noqa: E402
from solve_steps import divide_bars, op_under, strike_pair  # noqa: E402
from tick_number_line import HALF, tick_number_line  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402
from composite_problem_intro import COMPOSITE_INTRO_3, play_composite_problem_intro  # noqa: E402

apply_portal_paper_background()

LHS = r'(f\circ g)(x)'
SQRT = r'\sqrt{2-x}'
F_DOM = r'(-\infty,4)\cup(4,\infty)'
Y_DOM = r'(-\infty,-14)\cup(-14,\infty)'
C_DOM = r'(-\infty,-14)\cup(-14,2]'
WIDE = dict(lo=-16, hi=4, step=2)  # the closing lines have to reach -14

# Row centres. The solve slots are reused: phase A, then phase B once the first rows are faded.
F_Y, G_Y = 2.35, 1.1
SOLVE_Y = dict(f_inside=0.35, f_solved=-0.65, g_inside=0.6, g_solved1=-0.45, g_solved2=-1.8)
G_LINE_Y = -2.65
TOP_Y, Y_ROW_Y = 2.4, 1.05
SLOT_A, SLOT_B, SLOT_C = 0.05, -0.85, -2.25
NL_ALL_Y, G_AGAIN_Y, NL_G_Y, NL_MERGE_Y = -0.15, -1.2, -2.05, -3.1
NL_FINAL_Y, C_DOM_Y = 1.0, -0.35
COMP_Y, C4_Y = -0.5, -2.1

G_WORD = '$@b g$'
F_WORD = '$f$'
X_WORD = '$x$'
Y_WORD = '$y$'


def frac_row(den_parts, y, left, size=COMP_SIZE):
    """`(f o g)(x) = 1 / den`: head, then numerator, bar and denominator as separate pieces."""
    head = row(LHS, '=', y=y, size=size, left=left)
    den = mathtex(*den_parts, font_size=size, color=INK)
    num = mathtex('1', font_size=size, color=INK)
    axis = head[1].get_center()[1]
    start = head.get_right()[0] + 0.2
    width = den.width + 0.1
    bar = Line([start, axis, 0], [start + width, axis, 0], color=INK, stroke_width=4)
    den.move_to([start + width / 2, axis - 0.1 - den.height / 2, 0])
    num.move_to([start + width / 2, axis + 0.1 + num.height / 2, 0])
    return SimpleNamespace(head=head, num=num, bar=bar, den=den, frac=VGroup(num, bar, den),
                           everything=VGroup(head, num, bar, den))


class CompositeDomainThree(Narrated, Scene):
    caption_color = PAPER_INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9

    def beat(self, mark, seconds):
        self.wait(seconds)
        self.mark(mark)

    def swap_head(self, old, new):
        """Rows share an identical left-aligned head; hand it over without a double print."""
        self.remove(old.head)
        self.add(new.head)

    def construct(self):
        # ---- the two functions, each beside its own domain -------------------------------
        f_row, f_dom = pair(
            row('f(x)', '=', r'\frac{1}{x-4}', y=0), domain_row(F_DOM, 0), F_Y)
        g_row = row('g(x)', '=', SQRT, y=0)
        g_row[2].set_color(G_COLOR)
        g_row, g_dom = pair(g_row, domain_row(r'(-\infty,2]', 0), G_Y)

        play_composite_problem_intro(self, COMPOSITE_INTRO_3, f_row, g_row)

        # ---- solving f: bottom can't be 0 ------------------------------------------------
        fin_row = row('x', '-4', r'\neq', '0', y=SOLVE_Y['f_inside'], size=STEP_SIZE)
        fin_moved, fin_zero = fin_row[1], fin_row[3]
        fin_solved = row('x', r'\neq', '4', y=SOLVE_Y['f_solved'], size=STEP_SIZE)
        f_nl = tick_number_line(-1.9)
        f_nl_all = f_nl.all_but(4)
        f_minus = row(r'-\infty', y=-2.7, size=30).set_x(-HALF)
        f_plus = row(r'\infty', y=-2.7, size=30).set_x(HALF)
        f_line = VGroup(f_nl.everything, f_minus, f_plus, f_nl_all)

        # ---- solving g: inside >= 0, with a flip ------------------------------------------
        gin_row = row('2', '-x', r'\geq', '0', y=SOLVE_Y['g_inside'], size=STEP_SIZE)
        gin_moved, gin_zero = gin_row[0], gin_row[3]
        g_s1 = row('-x', r'\geq', '-2', y=SOLVE_Y['g_solved1'], size=STEP_SIZE)
        g_s2 = row('x', r'\leq', '2', y=SOLVE_Y['g_solved2'], size=STEP_SIZE)
        g_nl = tick_number_line(G_LINE_Y)
        g_ray0 = g_nl.from_point(2, -1)
        g_minus = row(r'-\infty', y=G_LINE_Y - 0.8, size=30).set_x(-HALF)
        g_plus = row(r'\infty', y=G_LINE_Y - 0.8, size=30).set_x(HALF)
        g_line = VGroup(g_nl.everything, g_minus, g_plus, g_ray0)

        # ---- the composite, in stages (all share one left head position) -----------------
        probe = frac_row([SQRT, '-', '4'], COMP_Y, 0)
        left = -(probe.everything.width / 2)
        c_x = frac_row(['x', '-', '4'], COMP_Y, left)
        c_paren = frac_row(['(', 'x', ')', '-', '4'], COMP_Y, left)
        c_paren.den[1].set_color(TAG_COLOR)
        c_full = frac_row(['(', SQRT, ')', '-', '4'], COMP_Y, left)
        c_full.den[1].set_color(G_COLOR)
        c4 = frac_row([SQRT, '-', '4'], C4_Y, left)
        c4.den[0].set_color(G_COLOR)
        top = frac_row([SQRT, '-', '4'], TOP_Y, left)
        top.den[0].set_color(G_COLOR)

        # ---- the closing board ------------------------------------------------------------
        y_row, y_dom = pair(
            row('y', '=', r'\frac{1}{\sqrt{2-x}-4}', y=0), domain_row(Y_DOM, 0), Y_ROW_Y)

        yin = row(SQRT, '-4', r'\neq', '0', y=SLOT_A, size=STEP_SIZE)
        yin[0].set_color(G_COLOR)
        y_moved, y_zero = yin[1], yin[3]
        y_s1 = row(SQRT, r'\neq', '4', y=SLOT_B, size=STEP_SIZE)
        y_s1[0].set_color(G_COLOR)
        y_s2 = row('2', '-x', r'\neq', '16', y=SLOT_A, size=STEP_SIZE)
        y_s2m, y_s2z = y_s2[0], y_s2[3]
        y_s3 = row('-x', r'\neq', '14', y=SLOT_B, size=STEP_SIZE)
        y_s4 = row('x', r'\neq', '-14', y=SLOT_C, size=STEP_SIZE)

        nl_all = tick_number_line(NL_ALL_Y, **WIDE)
        nl_g = tick_number_line(NL_G_Y, **WIDE)
        nl_merge = tick_number_line(NL_MERGE_Y, **WIDE)
        g2 = row('g(x)', '=', SQRT, y=0)
        g2[2].set_color(G_COLOR)
        g2, g2_dom = pair(g2, domain_row(r'(-\infty,2]', 0), G_AGAIN_Y)
        c_dom = domain_row(C_DOM, C_DOM_Y, size=36)

        # ===================================================================================
        self.say('Start with the domain of each function.')
        self.beat('form', 1.0)

        # ---- domain of f ------------------------------------------------------------------
        self.say("A fraction can't have a zero in the bottom.")
        bottom = VGroup(*f_row[2].submobjects[2:])
        self.play(Indicate(bottom, color=G_COLOR, scale_factor=1.3), run_time=0.9)
        self.play(
            copy_into(bottom, VGroup(fin_row[0], fin_moved)),
            FadeIn(VGroup(fin_row[2], fin_zero)),
            run_time=1.1,
        )
        self.beat('f_inside', READ_LONG)

        self.say(f'Solve for {X_WORD}.')
        op_l = op_under('+', '4', fin_moved, OP_SIZE)
        op_r = op_under('+', '4', fin_zero, OP_SIZE)
        strikes = strike_pair(fin_moved, op_l)
        self.play(FadeIn(op_l, shift=DOWN * 0.15), FadeIn(op_r, shift=DOWN * 0.15), run_time=0.7)
        self.beat('f_op', 0.6)
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=0.5)
        self.play(
            copy_into(fin_row[0], fin_solved[0]),
            FadeIn(fin_solved[1]),
            copy_into(VGroup(fin_zero, op_r), fin_solved[2]),
            run_time=1.1,
        )
        self.beat('f_solved', READ_LONG)

        self.say(f"Open circle on $4$, because {X_WORD} can't equal it.")
        self.play(f_nl.build(), run_time=NL_BUILD_RUN)
        self.play(FadeIn(VGroup(f_minus, f_plus)), run_time=0.5)
        self.play(FadeIn(f_nl_all[1]), run_time=0.9)
        self.beat('f_circle', READ_LONG)

        self.say(f'{X_WORD} can be any other number, so the arrows go both ways.')
        self.play(Create(f_nl_all[0]), run_time=NL_HIGHLIGHT_RUN + 0.15)
        self.bring_to_front(f_nl_all[1])
        self.beat('f_arrows', READ_LONG)

        self.say(f'In interval notation, that is the domain of {F_WORD}.')
        self.play(FadeIn(f_dom[0]), copy_into(fin_solved, f_dom[1]), run_time=1.1)
        self.play(
            FadeOut(VGroup(fin_row, op_l, op_r, strikes, fin_solved, f_line)), run_time=0.7)
        self.beat('f_domain', READ_LONG)

        # ---- domain of g: inside >= 0, flip -----------------------------------------------
        self.say('The inside of a square root must be at least $0$.')
        radicand = VGroup(*g_row[2].submobjects[2:])
        self.play(Indicate(radicand, color=G_COLOR, scale_factor=1.2), run_time=0.8)
        self.play(
            copy_into(radicand, VGroup(gin_moved, gin_row[1])),
            FadeIn(VGroup(gin_row[2], gin_zero)),
            run_time=1.1,
        )
        self.beat('g_inside', READ_LONG)

        self.say(f'Solve for {X_WORD}.')
        gop_l = op_under('-', '2', gin_moved, OP_SIZE)
        gop_r = op_under('-', '2', gin_zero, OP_SIZE)
        gstrikes = strike_pair(gin_moved, gop_l)
        self.play(FadeIn(gop_l, shift=DOWN * 0.15), FadeIn(gop_r, shift=DOWN * 0.15), run_time=0.7)
        self.beat('g_op', 0.6)
        self.play(Create(gstrikes[0]), Create(gstrikes[1]), run_time=0.5)
        self.play(
            copy_into(gin_row[1], g_s1[0]),
            FadeIn(g_s1[1]),
            copy_into(VGroup(gin_zero, gop_r), g_s1[2]),
            run_time=1.1,
        )
        self.beat('g_s1', READ_LONG)

        self.say('Divide both sides by $-1$.')
        bars, divisors = divide_bars([g_s1[0], g_s1[2]], '-1')
        self.play(
            *[Create(b) for b in bars],
            *[FadeIn(d, shift=DOWN * 0.15) for d in divisors],
            run_time=0.9,
        )
        self.beat('g_bars', READ_SHORT)

        self.say('Dividing by a negative flips the inequality.')
        self.play(Indicate(g_s1[1], color=PAPER_RED, scale_factor=1.5), run_time=1.0)
        g_s2[1].set_color(PAPER_RED)
        self.play(
            copy_into(VGroup(g_s1[0], divisors[0]), g_s2[0]),
            FadeIn(g_s2[1]),
            copy_into(VGroup(g_s1[2], divisors[1]), g_s2[2]),
            run_time=1.1,
        )
        self.play(g_s2[1].animate.set_color(INK), run_time=0.5)
        self.beat('g_solved', READ_LONG)

        self.say(f'Closed circle on $2$, because {X_WORD} can equal it.')
        self.play(g_nl.build(), run_time=NL_BUILD_RUN)
        self.play(FadeIn(VGroup(g_minus, g_plus)), run_time=0.5)
        self.play(
            FadeIn(g_ray0[1]),
            g_nl.ticks[2][1].animate.set_color(G_COLOR),
            run_time=1.0,
        )
        self.beat('g_circle', READ_LONG)

        self.say(f'{X_WORD} is at most $2$, so the arrow points left.')
        self.play(GrowArrow(g_ray0[0]), run_time=NL_ARROW_RUN)
        self.beat('g_arrow', READ_LONG)

        self.say(f'In interval notation, that is the domain of {G_WORD}.')
        self.play(FadeIn(g_dom[0]), copy_into(g_s2, g_dom[1]), run_time=1.1)
        self.play(
            FadeOut(VGroup(gin_row, gop_l, gop_r, gstrikes, g_s1, bars, divisors, g_s2, g_line)),
            run_time=0.7,
        )
        self.beat('g_domain', READ_LONG)

        # ---- the composite: 1/(x-4) -> 1/((x)-4) -> g flies in -----------------------------
        self.say(r'The $\circ$ in $(f\circ g)(x)$ means $f$ composed with $@b g$.')
        self.wait(READ_LONG)
        self.say(f'This means {G_WORD} replaces every {X_WORD} in {F_WORD}.')
        self.wait(READ_CAPTION_EXTRA)
        self.play(Indicate(f_row[2], color=TAG_COLOR, scale_factor=1.2), run_time=1.0)
        self.play(FadeIn(c_x.head), copy_into(f_row[2], c_x.frac), run_time=1.1)
        self.beat('composite_x', READ_SHORT)

        self.say(f'Wrap the {X_WORD} in parentheses.')
        self.play(
            ReplacementTransform(c_x.num, c_paren.num),
            ReplacementTransform(c_x.bar, c_paren.bar),
            ReplacementTransform(c_x.den[0], c_paren.den[1]),
            ReplacementTransform(c_x.den[1], c_paren.den[3]),
            ReplacementTransform(c_x.den[2], c_paren.den[4]),
            FadeIn(c_paren.den[0]),
            FadeIn(c_paren.den[2]),
            run_time=1.0,
        )
        self.swap_head(c_x, c_paren)
        self.beat('composite_paren', READ_SHORT)

        self.say(f'Replace {X_WORD} with {G_WORD}.')
        g_drop = g_row[2].copy()
        self.play(
            FadeOut(c_paren.den[1]),
            ReplacementTransform(g_drop, c_full.den[1]),
            ReplacementTransform(c_paren.num, c_full.num),
            ReplacementTransform(c_paren.bar, c_full.bar),
            ReplacementTransform(c_paren.den[0], c_full.den[0]),
            ReplacementTransform(c_paren.den[2], c_full.den[2]),
            ReplacementTransform(c_paren.den[3], c_full.den[3]),
            ReplacementTransform(c_paren.den[4], c_full.den[4]),
            run_time=1.6,
        )
        self.swap_head(c_paren, c_full)
        self.beat('composite_written', READ_LONG)

        self.say('Drop the parentheses.')
        self.play(
            FadeIn(c4.head),
            copy_into(c_full.num, c4.num),
            copy_into(c_full.bar, c4.bar),
            copy_into(c_full.den[1], c4.den[0]),
            copy_into(c_full.den[3], c4.den[1]),
            copy_into(c_full.den[4], c4.den[2]),
            run_time=1.1,
        )
        self.beat('simplified', READ_LONG)

        # ---- clear the board: the composite rises to the top -------------------------------
        self.say('Now the domain of the composite.')
        self.play(
            FadeOut(VGroup(f_row, f_dom, g_row, g_dom, c_full.everything)),
            ReplacementTransform(c4.head, top.head),
            ReplacementTransform(c4.num, top.num),
            ReplacementTransform(c4.bar, top.bar),
            ReplacementTransform(c4.den, top.den),
            run_time=1.4,
        )
        self.beat('domain_intro', READ_SHORT)

        # ---- the composite has a restriction of its own ------------------------------------
        self.say(f'Call the result {Y_WORD}, as if it were its own function.')
        self.play(
            FadeIn(VGroup(y_row[0], y_row[1])),
            copy_into(top.frac, y_row[2]),
            run_time=1.2,
        )
        self.beat('y_row', READ_SHORT)

        self.say("Its bottom can't be $0$.")
        y_bottom = VGroup(*y_row[2].submobjects[2:])
        self.play(Indicate(y_bottom, color=G_COLOR, scale_factor=1.15), run_time=0.9)
        self.play(
            copy_into(y_bottom, VGroup(yin[0], y_moved)),
            FadeIn(VGroup(yin[2], y_zero)),
            run_time=1.1,
        )
        self.beat('y_bottom', READ_LONG)

        self.say('Add $4$ to both sides.')
        yop_l = op_under('+', '4', y_moved, OP_SIZE)
        yop_r = op_under('+', '4', y_zero, OP_SIZE)
        ystrikes = strike_pair(y_moved, yop_l)
        self.play(FadeIn(yop_l, shift=DOWN * 0.15), FadeIn(yop_r, shift=DOWN * 0.15),
                  run_time=0.7)
        self.beat('y_op', 0.6)
        self.play(Create(ystrikes[0]), Create(ystrikes[1]), run_time=0.5)
        self.play(
            copy_into(yin[0], y_s1[0]),
            FadeIn(y_s1[1]),
            copy_into(VGroup(y_zero, yop_r), y_s1[2]),
            run_time=1.1,
        )
        self.beat('y_s1', READ_LONG)

        self.say('Square both sides to remove the root.')
        self.play(Indicate(y_s1[0], color=G_COLOR, scale_factor=1.2), run_time=0.9)
        self.play(
            FadeOut(VGroup(yin, yop_l, yop_r, ystrikes)),
            copy_into(VGroup(*y_s1[0].submobjects[2:]), VGroup(y_s2[0], y_s2[1])),
            FadeIn(y_s2[2]),
            copy_into(y_s1[2], y_s2[3]),
            run_time=1.2,
        )
        self.play(FadeOut(y_s1), run_time=0.5)
        self.beat('y_s2', READ_LONG)

        self.say('Subtract $2$ from both sides.')
        yop2_l = op_under('-', '2', y_s2m, OP_SIZE)
        yop2_r = op_under('-', '2', y_s2z, OP_SIZE)
        ystrikes2 = strike_pair(y_s2m, yop2_l)
        self.play(FadeIn(yop2_l, shift=DOWN * 0.15), FadeIn(yop2_r, shift=DOWN * 0.15),
                  run_time=0.7)
        self.beat('y_op2', 0.6)
        self.play(Create(ystrikes2[0]), Create(ystrikes2[1]), run_time=0.5)
        self.play(
            copy_into(y_s2[1], y_s3[0]),
            FadeIn(y_s3[1]),
            copy_into(VGroup(y_s2z, yop2_r), y_s3[2]),
            run_time=1.1,
        )
        self.beat('y_s3', READ_LONG)

        self.say('Divide both sides by $-1$.')
        ybars, ydivs = divide_bars([y_s3[0], y_s3[2]], '-1')
        self.play(
            *[Create(b) for b in ybars],
            *[FadeIn(d, shift=DOWN * 0.15) for d in ydivs],
            run_time=0.9,
        )
        self.play(
            copy_into(VGroup(y_s3[0], ydivs[0]), y_s4[0]),
            FadeIn(y_s4[1]),
            copy_into(VGroup(y_s3[2], ydivs[1]), y_s4[2]),
            run_time=1.1,
        )
        self.beat('y_s4', READ_SHORT)

        self.say(f"So {X_WORD} can't be $-14$.")
        self.play(Indicate(y_s4[2], color=PAPER_RED, scale_factor=1.3), run_time=1.0)
        self.beat('y_cant', READ_LONG)

        self.say(f'Every other number works, so that is the domain of {Y_WORD}.')
        self.play(FadeIn(y_dom[0]), copy_into(y_s4, y_dom[1]), run_time=1.2)
        self.play(
            FadeOut(VGroup(y_s2, yop2_l, yop2_r, ystrikes2, y_s3, ybars, ydivs, y_s4)),
            run_time=0.7,
        )
        self.beat('y_domain', READ_LONG)

        # ---- number lines: all but -14, then g's, then the overlap ---------------------------
        self.say('On a number line: every number except $-14$.')
        self.play(nl_all.build(), run_time=NL_WIDE_BUILD_RUN)
        all_but = nl_all.all_but(-14)
        self.play(Create(all_but[0]), run_time=NL_HIGHLIGHT_RUN)
        self.play(FadeIn(all_but[1]), run_time=0.4)
        self.beat('nl_all', READ_LONG)

        self.say("This isn't the actual domain of the composite.")
        self.beat('not_composite', READ_SHORT)

        self.say('Any function plugged into another brings its domain with it.')
        self.beat('domain_follows', READ_LONG)

        self.say(f'Since {G_WORD} was plugged into {F_WORD}, bring its domain into the composite.')
        self.play(FadeIn(g2), FadeIn(g2_dom), run_time=1.1)
        self.play(nl_g.build(), run_time=NL_WIDE_BUILD_RUN)
        g_ray = nl_g.from_point(2, -1)
        self.play(copy_into(g2_dom[1], g_ray), run_time=1.2)
        self.beat('g_back', READ_LONG)

        self.say('The composite domain is where the lines overlap.')
        self.play(nl_merge.build(), run_time=NL_WIDE_BUILD_RUN)
        merged_all = nl_merge.all_but(-14)
        merged_g = nl_merge.from_point(2, -1)
        merged_hole = nl_merge.hole(-14, G_COLOR)
        self.play(
            ReplacementTransform(all_but.copy(), merged_all),
            ReplacementTransform(g_ray.copy(), merged_g),
            run_time=1.8,
        )
        self.beat('merge', READ_LONG)

        # ---- clean up: only (f o g)(x) and the merged line, moved up beneath it --------------
        merged = VGroup(nl_merge.everything, merged_all, merged_g)
        self.play(
            FadeOut(VGroup(y_row, y_dom, nl_all.everything, all_but,
                           g2, g2_dom, nl_g.everything, g_ray)),
            merged.animate.shift(UP * (NL_FINAL_Y - NL_MERGE_Y)),
            run_time=1.6,
        )
        merged_hole.shift(UP * (NL_FINAL_Y - NL_MERGE_Y))
        self.beat('cleanup', READ_SHORT)

        self.play(Indicate(merged_g, color=G_COLOR, scale_factor=1.15), run_time=1.2)
        self.play(Indicate(merged_g, color=G_COLOR, scale_factor=1.15), run_time=1.2)
        self.beat('overlap', READ_SHORT)

        self.play(FadeOut(merged_all), FadeIn(merged_hole), run_time=1.0)
        self.say(f'The domain of the composite is ${C_DOM}$.')
        self.play(FadeIn(c_dom), run_time=1.3)
        self.beat('hold', READ_LONG)
        self.write_marks('composite_domain_3_marks.json')
