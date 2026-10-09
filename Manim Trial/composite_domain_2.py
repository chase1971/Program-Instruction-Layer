"""Composite functions, example 2: f's domain carries straight into g(f(x)).

    f(x) = sqrt(x),  g(x) = 4x + 2   ->   g(f(x)) = 4 sqrt(x) + 2,  domain [0, infinity)

Same structure as composite_domain.py (example 1): each function beside its own domain, the
composite built by wrapping x in parentheses and flying f in, then the board is cleared. The
Domain of the composite starts from $y=4\\sqrt{x}+2$ alone (square root restriction), shown to
match f's domain; then f returns so the plug-in rule lands; g accepts all reals so the intervals
match. Final hold: g(f(x)) and Domain: [0, infinity).

Row helpers, sizes and the number line are shared with example 1 (composite_domain.py).
"""

from portrait_frame import apply_portrait_frame

apply_portrait_frame()

from manim import (  # noqa: E402
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
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
    LINE_Y,
    NL_ARROW_RUN,
    NL_BUILD_RUN,
    NL_WIDE_BUILD_RUN,
    READ_CAPTION_EXTRA,
    READ_LONG,
    READ_SHORT,
    ROW_Y,
    TAG_COLOR,
    domain_row,
    pair,
    row,
)
from scene_style import PAPER_INK, Narrated, apply_portal_paper_background  # noqa: E402
from tick_number_line import HALF, tick_number_line  # noqa: E402
from vector_projection_shadow import copy_into  # noqa: E402
from composite_problem_intro import COMPOSITE_INTRO_2, play_composite_problem_intro  # noqa: E402

apply_portal_paper_background()

LHS = r'g(f(x))'
SQRT = r'\sqrt{x}'
INSIDE_Y = -0.6
# Caption math: f is the function that gets plugged in, so it is the blue one.
F_WORD = '$@b f$'
G_WORD = '$g$'
X_WORD = '$x$'


class CompositeDomainTwo(Narrated, Scene):
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
        f_row = row('f(x)', '=', SQRT, y=0)
        f_row[2].set_color(G_COLOR)
        f_row, f_dom = pair(f_row, domain_row(r'[0,\infty)', 0), ROW_Y['f'])
        g_row, g_dom = pair(
            row('g(x)', '=', '4', 'x', '+', '2', y=0),
            domain_row(r'(-\infty,\infty)', 0), ROW_Y['g'])

        play_composite_problem_intro(self, COMPOSITE_INTRO_2, f_row, g_row)

        inside_row = row('x', r'\geq', '0', y=INSIDE_Y, size=FORM_SIZE)

        comp_y = -0.6
        c_full = row(LHS, '=', '4', '(', SQRT, ')', '+', '2', y=comp_y, size=COMP_SIZE)
        c_full[4].set_color(G_COLOR)
        left = c_full.get_left()[0]  # every composite row shares this head position
        c_x = row(LHS, '=', '4', 'x', '+', '2', y=comp_y, size=COMP_SIZE, left=left)
        c_paren = row(LHS, '=', '4', '(', 'x', ')', '+', '2', y=comp_y, size=COMP_SIZE, left=left)
        c_paren[4].set_color(TAG_COLOR)
        c4 = row(LHS, '=', '4', SQRT, '+', '2', y=-1.7, size=COMP_SIZE, left=left)
        c4[3].set_color(G_COLOR)

        # closing: composite on top; f returns mid-explanation only; final hold is composite + domain
        top_fn = row(LHS, '=', '4', SQRT, '+', '2', y=ROW_Y['top'], size=COMP_SIZE)
        top_fn[3].set_color(G_COLOR)
        y_row = row('y', '=', '4', SQRT, '+', '2', y=0)
        y_row[3].set_color(G_COLOR)
        y_row, y_dom = pair(y_row, domain_row(r'[0,\infty)', 0), ROW_Y['y_row'])
        f2 = row('f(x)', '=', SQRT, y=0)
        f2[2].set_color(G_COLOR)
        f2, f2_dom = pair(f2, domain_row(r'[0,\infty)', 0), ROW_Y['g_again'])
        c_dom = domain_row(r'[0,\infty)', ROW_Y['y_row'], size=36)

        # solving f: a proper number line (dot on 0, arrow to the right)
        solve_nl = tick_number_line(LINE_Y)
        solve_ray = solve_nl.from_point(0)
        minus_inf = row(r'-\infty', y=LINE_Y - 0.8, size=30).set_x(-HALF)
        plus_inf = row(r'\infty', y=LINE_Y - 0.8, size=30).set_x(HALF)
        number_line = VGroup(solve_nl.everything, minus_inf, plus_inf, solve_ray)

        nl_f = tick_number_line(ROW_Y['nl_g'])

        # ---- the two functions, each beside its own domain ------------------------------
        self.say('Start with the domain of each function.')
        self.beat('form', 1.0)

        # ---- domain of f: the inside of the root must be at least 0 ----------------------
        self.say('The inside of a square root must be at least $0$.')
        radicand = VGroup(*f_row[2].submobjects[2:])
        self.play(Indicate(radicand, color=G_COLOR, scale_factor=1.3), run_time=0.8)
        self.play(
            copy_into(radicand, inside_row[0]),
            FadeIn(VGroup(inside_row[1], inside_row[2])),
            run_time=1.1,
        )
        self.beat('f_inside', READ_LONG)

        self.say(f'Closed circle on $0$, because {X_WORD} can equal it.')
        self.play(solve_nl.build(), run_time=NL_BUILD_RUN)
        self.play(FadeIn(VGroup(minus_inf, plus_inf)), run_time=0.5)
        self.play(
            FadeIn(solve_ray[1]),
            solve_nl.ticks[0][1].animate.set_color(G_COLOR),
            run_time=1.0,
        )
        self.beat('f_circle', READ_LONG)

        self.say(f'{X_WORD} is at least $0$, so the arrow points right.')
        self.play(GrowArrow(solve_ray[0]), run_time=NL_ARROW_RUN)
        self.beat('f_arrow', READ_LONG)

        self.say(f'In interval notation, that is the domain of {F_WORD}.')
        self.play(FadeIn(f_dom[0]), copy_into(inside_row, f_dom[1]), run_time=1.1)
        self.play(FadeOut(VGroup(inside_row, number_line)), run_time=0.7)
        self.beat('f_domain', READ_LONG)

        self.say(f"A line has no restrictions, so {G_WORD}'s domain is all real numbers.")
        self.play(Indicate(g_row[3], color=G_COLOR, scale_factor=1.4), run_time=0.9)
        self.play(FadeIn(g_dom), run_time=0.8)
        self.beat('g_domain', READ_LONG)

        # ---- the composite: 4x + 2 -> 4(x) + 2 -> f flies in -----------------------------
        self.say(r'Another way to write a composite is $g(f(x))$.')
        self.wait(READ_LONG)
        self.say(r'That is the same as $(g\circ f)(x)$: $g$ composed with $@b f$.')
        self.wait(READ_CAPTION_EXTRA)
        self.play(Indicate(g_row[3], color=TAG_COLOR, scale_factor=1.4), run_time=1.0)
        self.play(FadeIn(c_x[0]), FadeIn(c_x[1]), copy_into(g_row[2:], c_x[2:]), run_time=1.1)
        self.beat('composite_x', READ_SHORT)

        self.say(f'Wrap the {X_WORD} in parentheses.')
        self.play(
            FadeOut(c_x[3]),
            FadeIn(c_paren[3:6]),
            ReplacementTransform(c_x[2], c_paren[2]),
            ReplacementTransform(c_x[4], c_paren[6]),
            ReplacementTransform(c_x[5], c_paren[7]),
            run_time=1.0,
        )
        self.swap_head(c_x, c_paren)
        self.beat('composite_paren', READ_SHORT)

        self.say(f'Replace {X_WORD} with {F_WORD}.')
        f_drop = f_row[2].copy()
        self.play(
            FadeOut(c_paren[4]),
            ReplacementTransform(f_drop, c_full[4]),
            ReplacementTransform(c_paren[2], c_full[2]),
            ReplacementTransform(c_paren[3], c_full[3]),
            ReplacementTransform(c_paren[5], c_full[5]),
            ReplacementTransform(c_paren[6], c_full[6]),
            ReplacementTransform(c_paren[7], c_full[7]),
            run_time=1.6,
        )
        self.swap_head(c_paren, c_full)
        self.beat('composite_written', READ_LONG)

        self.say('Drop the parentheses.')
        self.play(
            FadeIn(VGroup(c4[0], c4[1])),
            copy_into(VGroup(c_full[2], c_full[4], c_full[6], c_full[7]),
                      VGroup(c4[2], c4[3], c4[4], c4[5])),
            run_time=1.1,
        )
        self.beat('simplified', READ_LONG)

        # ---- clear the board: composite on top, y = ... alone for domain ----------------
        self.say(r'Now the domain of the composite. Start with $4\sqrt{x}+2$.')
        self.play(
            FadeOut(VGroup(f_row, f_dom, g_row, g_dom, c_full[2:])),
            FadeOut(VGroup(c_full[0], c_full[1])),
            *[ReplacementTransform(c4[i], top_fn[i]) for i in range(6)],
            FadeIn(VGroup(y_row[0], y_row[1])),
            copy_into(
                VGroup(top_fn[2], top_fn[3], top_fn[4], top_fn[5]),
                VGroup(y_row[2], y_row[3], y_row[4], y_row[5]),
            ),
            run_time=1.4,
        )
        self.beat('domain_intro', READ_SHORT)

        self.say('The inside of the square root must be at least $0$.')
        rad_y = VGroup(*y_row[3].submobjects[2:])
        self.play(Indicate(rad_y, color=G_COLOR, scale_factor=1.3), run_time=0.8)
        self.beat('y_inside', READ_SHORT)

        self.say(f'By itself, that gives domain $[0,\\infty)$, the same as {F_WORD}.')
        self.play(FadeIn(y_dom), run_time=1.0)
        self.play(nl_f.build(), run_time=NL_WIDE_BUILD_RUN)
        comp_ray = nl_f.from_point(0)
        self.play(copy_into(y_dom[1], comp_ray), run_time=1.2)
        self.beat('y_domain', READ_LONG)

        self.say('Any function plugged into another brings its domain with it.')
        self.beat('domain_follows', READ_LONG)

        self.say(f'Since {F_WORD} was plugged into {G_WORD}, bring its domain over.')
        self.play(FadeIn(f2), FadeIn(f2_dom), run_time=1.1)
        self.beat('f_back', READ_LONG)

        self.say(f'{G_WORD} accepts every number, so the domains match.')
        self.play(Indicate(comp_ray, color=G_COLOR, scale_factor=1.15), run_time=1.2)
        self.beat('same_domain', READ_LONG)

        self.say(f'The domain of the composite is $[0,\\infty)$, the same as {F_WORD}.')
        self.play(
            FadeOut(VGroup(y_row, y_dom, f2, f2_dom, nl_f.everything, comp_ray)),
            FadeIn(c_dom),
            run_time=1.3,
        )
        self.beat('hold', READ_LONG)
        self.write_marks('composite_domain_2_marks.json')
