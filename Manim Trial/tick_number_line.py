"""A proper number line: arrowed axis, a tick and a label at every integer, and highlight pieces.

    nl = tick_number_line(y)
    nl.build()              animation (play it with run_time=) that writes the line left to right, -7 ... 7 in order
    nl.axis                 the double-arrowed axis
    nl.everything           axis + every tick, as one group (to fade out)
    nl.all_reals()          a gold double arrow laid along the whole line
    nl.from_two()           a blue closed circle on 2 and an arrow to the right

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


def _tick(n, y):
    mark = Line([n * UNIT, y - 0.1, 0], [n * UNIT, y + 0.1, 0], color=PAPER_INK, stroke_width=3)
    label = mathtex(str(n), font_size=LABEL_SIZE, color=PAPER_INK).move_to([n * UNIT, y - 0.38, 0])
    return VGroup(mark, label)


def tick_number_line(y):
    ticks = {n: _tick(n, y) for n in range(-REACH, REACH + 1)}

    def all_reals():
        return DoubleArrow([-HALF, y, 0], [HALF, y, 0], buff=0, color=PAPER_GOLD,
                           stroke_width=8, tip_length=0.25)

    def from_two():
        dot = Circle(radius=0.12, color=PAPER_BLUE, stroke_width=5)
        dot.set_fill(PAPER_BLUE, 1).move_to([2 * UNIT, y, 0])
        ray = Arrow([2 * UNIT, y, 0], [HALF, y, 0], buff=0, color=PAPER_BLUE, stroke_width=8,
                    tip_length=0.25)
        return VGroup(ray, dot)

    axis = DoubleArrow([-HALF, y, 0], [HALF, y, 0], buff=0, color=PAPER_INK, stroke_width=4,
                       tip_length=0.2)
    ordered = [ticks[n] for n in range(-REACH, REACH + 1)]

    def build():
        """Write the line left to right: the axis extends as -7 ... 7 are set down in order."""
        return AnimationGroup(
            Create(axis, rate_func=linear),
            LaggedStart(*[FadeIn(tick) for tick in ordered], lag_ratio=0.5),
        )

    return SimpleNamespace(
        y=y,
        ticks=ticks,
        zero=ticks[0],
        axis=axis,
        build=build,
        all_reals=all_reals,
        from_two=from_two,
        everything=VGroup(axis, *ordered),
    )
