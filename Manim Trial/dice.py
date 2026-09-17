"""Dice drawing for the sampling-distribution animations."""

from manim import VGroup, RoundedRectangle, Dot, RIGHT

from scene_style import NAVY, INK, BLUE

# Pip positions in units of a quarter face, so they scale with the die.
PIPS = {
    1: [(0, 0)],
    2: [(-1, 1), (1, -1)],
    3: [(-1, 1), (0, 0), (1, -1)],
    4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
    5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
    6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)],
}


def die(face, size=.6, color=INK):
    body = RoundedRectangle(width=size, height=size, corner_radius=size * .16,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    group = VGroup(body)
    for x, y in PIPS[face]:
        pip = Dot(radius=size * .105, color=NAVY)
        pip.move_to(body.get_center() + [x * size * .27, y * size * .27, 0])
        group.add(pip)
    return group


def pair(first, second, size=.6, buff=.08):
    """White first die, blue second die — so (a, b) reads differently from (b, a)."""
    a = die(first, size, INK)
    b = die(second, size, BLUE)
    b.next_to(a, RIGHT, buff=buff)
    return VGroup(a, b)
