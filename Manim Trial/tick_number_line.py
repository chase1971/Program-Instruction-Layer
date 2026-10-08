"""A proper number line: arrowed axis, a tick and a label at every integer, and highlight pieces.

    nl = tick_number_line(y)
    nl.build()              animation (play it with run_time=) that writes the line left to right, -7 ... 7 in order
    nl.axis                 the double-arrowed axis
    nl.everything           axis + every tick, as one group (to fade out)
    nl.all_reals()          a gold double arrow laid along the whole line
    nl.from_two()           a blue closed circle on 2 and an arrow to the right
    nl.from_point(n)        the same, starting at any integer n (direction=-1: arrow to the left)
    nl.all_but(n)           the gold all-reals arrow with an open circle (a hole) on n
    nl.hole(n)              just the open circle
    tick_number_line(y, lo, hi, step)   a wider/coarser line, e.g. lo=-16, hi=4, step=2

Two lines built with the same call have the same length and the same values, so one can be
merged onto the other. Labels go through `mathtex`, so a negative is Chase's short dash.
"""

from types import SimpleNamespace

from manim import (
    AnimationGroup,
    Arrow,
    Circle,
    Create,
    DoubleArrow,
    FadeIn,
    LaggedStart,
    Line,
    VGroup,
    linear,
)

from math_notation import mathtex
from scene_style import PAPER_BLUE, PAPER_GOLD, PAPER_INK

UNIT = 0.34
REACH = 7
HALF = 2.65
LABEL_SIZE = 24


def _tick(x, label_text, y):
    mark = Line([x, y - 0.1, 0], [x, y + 0.1, 0], color=PAPER_INK, stroke_width=3)
    label = mathtex(label_text, font_size=LABEL_SIZE, color=PAPER_INK).move_to([x, y - 0.38, 0])
    return VGroup(mark, label)


def tick_number_line(y, lo=-REACH, hi=REACH, step=1):
    mid = (lo + hi) / 2
    unit = 2 * REACH * UNIT / (hi - lo)

    def pos(n):
        return (n - mid) * unit

    values = list(range(lo, hi + 1, step))
    ticks = {n: _tick(pos(n), str(n), y) for n in values}

    def all_reals():
        return DoubleArrow([-HALF, y, 0], [HALF, y, 0], buff=0, color=PAPER_GOLD,
                           stroke_width=8, tip_length=0.25)

    def from_point(n, direction=1):
        dot = Circle(radius=0.12, color=PAPER_BLUE, stroke_width=5)
        dot.set_fill(PAPER_BLUE, 1).move_to([pos(n), y, 0])
        ray = Arrow([pos(n), y, 0], [direction * HALF, y, 0], buff=0, color=PAPER_BLUE,
                    stroke_width=8, tip_length=0.25)
        return VGroup(ray, dot)

    def hole(n, color=PAPER_INK):
        ring = Circle(radius=0.12, color=color, stroke_width=5)
        return ring.set_fill('#FFFFFF', 1).move_to([pos(n), y, 0])

    def all_but(n):
        return VGroup(all_reals(), hole(n, PAPER_GOLD))

    def from_two():
        return from_point(2)

    axis = DoubleArrow([-HALF, y, 0], [HALF, y, 0], buff=0, color=PAPER_INK, stroke_width=4,
                       tip_length=0.2)
    ordered = [ticks[n] for n in values]

    def build():
        """Write the line left to right: the axis extends as -7 ... 7 are set down in order."""
        return AnimationGroup(
            Create(axis, rate_func=linear),
            LaggedStart(*[FadeIn(tick) for tick in ordered], lag_ratio=0.5),
        )

    return SimpleNamespace(
        y=y,
        pos=pos,
        ticks=ticks,
        zero=ticks.get(0),
        hole=hole,
        all_but=all_but,
        axis=axis,
        build=build,
        all_reals=all_reals,
        from_point=from_point,
        from_two=from_two,
        everything=VGroup(axis, *ordered),
    )
