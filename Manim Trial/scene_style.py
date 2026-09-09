"""Shared palette and caption line for Manim Trial scenes.

Colors and placement come from ANIMATION_STYLE_RECIPE.md. The earlier scenes
(gcf_division, solve_factors, two_step_equation) still carry their own copies;
new scenes import from here.
"""

import json
from pathlib import Path

from manim import Text, FadeIn, FadeOut

NAVY = '#101C30'
INK = '#F2F5FA'
GOLD = '#FFC66D'
BLUE = '#86C8FF'
MUTED = '#B2C0D4'

# The caption rides along the top: it says what is going on, so it should be the
# first thing read, not the last. Content therefore lives below about y = 2.5.
CAPTION_Y = 3.3
TITLE_Y = 2.75

# One knob for the whole clip's tempo. 1.0 is as written; 1.2 plays 20% faster.
PACE = 1.2


def label(words, font_size=25, color=MUTED):
    return Text(words, font='Segoe UI', font_size=font_size, color=color)


def banner(words):
    return label(words).move_to([0, TITLE_Y, 0])


class Narrated:
    """Scene mixin: a muted caption line, and PACE applied to every beat.

    Scaling happens here so scene code keeps writing the run_times it means.
    Only explicit run_times are scaled — animations left on their own default
    are untouched.
    """

    note = None
    elapsed = 0.
    marks = None
    _inner = False  # Scene.wait routes through Scene.play; don't scale or count twice.

    def play(self, *animations, **kwargs):
        if self._inner:
            super().play(*animations, **kwargs)
            return
        scaled = kwargs['run_time'] / PACE if 'run_time' in kwargs else 1.
        if 'run_time' in kwargs:
            kwargs['run_time'] = scaled
        self._inner = True
        try:
            super().play(*animations, **kwargs)
        finally:
            self._inner = False
        self.elapsed += scaled

    def wait(self, duration=1., **kwargs):
        scaled = duration / PACE
        self._inner = True
        try:
            super().wait(scaled, **kwargs)
        finally:
            self._inner = False
        self.elapsed += scaled

    def mark(self, name):
        """Record where the app should be able to pause. Pair with a hold."""
        if self.marks is None:
            self.marks = []
        self.marks.append({'name': name, 'time': round(self.elapsed, 2)})

    def write_marks(self, path):
        if self.marks:
            Path(path).write_text(json.dumps(self.marks, indent=2), encoding='utf-8')

    def say(self, words):
        fresh = label(words).move_to([0, CAPTION_Y, 0])
        if self.note is None:
            self.note = fresh
            self.add(fresh)
            return
        self.play(FadeOut(self.note), run_time=.25)
        self.note = fresh
        self.play(FadeIn(fresh), run_time=.35)

    def hush(self):
        """Clear the caption. Questions get the screen to themselves."""
        if self.note is not None:
            self.play(FadeOut(self.note), run_time=.25)
            self.note = None
