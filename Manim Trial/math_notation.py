"""Chase's way of writing negatives, as the one place every scene gets it from.

The rules and why are in ANIMATION_STYLE_RECIPE.md, "Chase's notation". Build math with
`mathtex()` instead of `MathTex()` and a negative comes out right without thinking about it.

    from math_notation import mathtex, hanging_fraction, unsigned
    mathtex('-3y', '<', '2x', '+', '6')             # -3y gets the short negative dash
    mathtex('y', '>', hanging_fraction('2', '3') + 'x', '-', '2')   # negative on top
    Line(unsigned(term).get_left(), ...)            # a division bar the negative hangs off
"""

import re

from manim import MathTex, VGroup

# The negative sign: a short dash, about half a minus, on the minus sign's axis and at its
# thickness. The kern keeps it off the digit it belongs to. Only negatives get it -- a
# minus that subtracts stays a full minus, so the two read differently.
NEG = r'{\rule[0.228em]{0.4em}{0.045em}\mkern1.5mu}'
# \llap gives a fraction's negative zero width, so it hangs off the left of the bar.
HANGING_NEG = r'\llap{$' + NEG + '$}'
# What a '-' can follow and still be a negative rather than a subtraction.
OPERATORS = ('=', '<', '>', r'\leq', r'\geq', '+', '-')


def negatives(parts):
    """MathTex parts with every negative swapped for NEG.

    A '-' is a negative when it opens the expression or follows a relation or an operator;
    anywhere else it subtracts. A part that is a lone '-' is always the operator.
    """
    out = []
    for i, part in enumerate(parts):
        opens = i == 0 or parts[i - 1].strip() in OPERATORS
        if part.startswith('-') and len(part) > 1 and opens:
            part = NEG + part[1:]
        out.append(re.sub(r'([=<>(]\s*)-', lambda m: m.group(1) + NEG, part))
    return out


def mathtex(*parts, **kwargs):
    """MathTex with Chase's negatives. Use it everywhere MathTex would go."""
    return MathTex(*negatives(parts), **kwargs)


def hanging_fraction(top, bottom):
    """-top/bottom with the negative on the top number, hanging left of the bar.

    Room before it; the padding goes on the bottom number so the bar is not one digit wide
    and the negative stays attached to the top number.
    """
    return r'\,\frac{' + HANGING_NEG + top + r'}{\,' + bottom + r'\,}'


def unsigned(term):
    """The glyphs of a term after its leading negative -- what a drawn division bar spans."""
    glyphs = term.submobjects
    signed = term.get_tex_string().startswith(('-', NEG))
    return VGroup(*glyphs[1:]) if signed else VGroup(*glyphs)
