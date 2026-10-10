"""Chase's way of solving an equation or inequality on screen, as one shared set of helpers.

Pattern (from SlopeInterceptForm.move_x / .divide -- copy it, never reinvent it):

    ADD / SUBTRACT   the operation goes UNDER both sides in gold ("+1" under the -1 and under
                     the 0), the cancelling pair is struck in red, and the next line is built
                     from copies (copy_into) of what is left.
    DIVIDE           NEVER a division sign. A fraction bar is drawn under EVERY term and the
                     divisor goes under each bar, in gold. The next line is built from copies.
    MULTIPLY         The multiplier in gold in front of BOTH sides, then the cancelling pair
                     (multiplier digit and the fraction's denominator, then any two negatives)
                     struck in red with strike_pair. See ANIMATION_STYLE_RECIPE.md "Multiply
                     both sides"; exemplars equations_of_lines.py and parabola_opens_left.py.
    FLIP             Dividing or multiplying an inequality by a negative: the old sign pulses red,
                     the new sign is copied in red, then settles to ink.

    from solve_steps import op_under, strike_pair, divide_bars
"""

from manim import DOWN, Create, FadeIn, Line, VGroup

from math_notation import mathtex, unsigned
from scene_style import PAPER_GOLD, PAPER_INK, PAPER_RED

OP_COLOR = PAPER_GOLD


def op_under(sign, number, under, size=34):
    """'+1' / '-2' in gold just below a term (a full minus: it is an operation, not a negative)."""
    return mathtex(sign, number, font_size=size, color=PAPER_INK).set_color(OP_COLOR).next_to(
        under, DOWN, buff=0.12)


def strike_pair(*terms):
    """Red slashes through the cancelling terms (the term and the operation under it)."""
    return VGroup(*[
        Line(term.get_corner([-1, -1, 0]) + [-0.08, -0.05, 0],
             term.get_corner([1, 1, 0]) + [0.08, 0.05, 0],
             color=PAPER_RED, stroke_width=6)
        for term in terms
    ])


def divide_bars(terms, divisor, size=34, gap=0.12):
    """A fraction bar under each term with the divisor under the bar.

    Returns (bars, divisors), both VGroups, one entry per term. Add them with
    `Create(bar), FadeIn(divisor, shift=DOWN * .15)`. A negative term's bar starts after its
    negative sign (`unsigned`), as in the slope-intercept clips.
    """
    bars, divisors = VGroup(), VGroup()
    for term in terms:
        body = unsigned(term)
        y = term.get_bottom()[1] - gap
        bars.add(Line([body.get_left()[0] - .08, y, 0], [body.get_right()[0] + .08, y, 0],
                      color=PAPER_INK, stroke_width=4))
        label = mathtex(divisor, font_size=size, color=PAPER_INK).set_color(OP_COLOR)
        label.move_to([body.get_center()[0], y - gap - label.height / 2, 0])
        divisors.add(label)
    return bars, divisors
