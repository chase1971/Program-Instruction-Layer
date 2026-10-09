"""Problem statement at the start of each Composite Examples clip.

Directions sit in the caption bar (same as every other beat). f(x) and g(x) write on the
board at their work positions and stay for "Start with the domain of each function."
"""

from dataclasses import dataclass

from manim import Write

READ_SHORT = 1.0
READ_LONG = 1.5


@dataclass(frozen=True)
class CompositeIntroSpec:
    """Caption text: Find … and find the domain."""

    caption: str  # mixed text and $...$ math, like the rest of the clip


COMPOSITE_INTRO_1 = CompositeIntroSpec(
    caption=r'Find $(f\circ g)(x)$ and find the domain.',
)
COMPOSITE_INTRO_2 = CompositeIntroSpec(
    caption=r'Find $g(f(x))$ and find the domain.',
)
COMPOSITE_INTRO_3 = CompositeIntroSpec(
    caption=r'Find $(f\circ g)(x)$ and find the domain.',
)


def play_composite_problem_intro(scene, spec: CompositeIntroSpec, f_row, g_row):
    """Caption directions, then the two given functions on the board."""
    scene.say(spec.caption)
    scene.wait(READ_SHORT)
    scene.mark('problem_title')

    scene.play(Write(f_row), Write(g_row), run_time=1.2)
    scene.wait(READ_LONG)
    scene.mark('problem_intro')
    scene.wait(READ_SHORT)
