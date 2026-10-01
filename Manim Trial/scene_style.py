"""Shared palette and caption line for Manim Trial scenes.

Colors and placement come from ANIMATION_STYLE_RECIPE.md. The earlier scenes
(gcf_division, solve_factors, two_step_equation) still carry their own copies;
new scenes import from here.
"""

import json
from pathlib import Path

from manim import Text, FadeIn, FadeOut

from scene_audit import audit_mark, audit_summary

NAVY = '#101C30'
INK = '#F2F5FA'
GOLD = '#FFC66D'
BLUE = '#86C8FF'
MUTED = '#B2C0D4'

# Light theme: matches student-portal `video-examples.css` / portal-base `#ffffff` so MP4
# letterboxing blends with the app shell.
PORTAL_PAGE_WHITE = '#FFFFFF'
PAPER = PORTAL_PAGE_WHITE
PAPER_INK = '#1A2332'
PAPER_BLUE = '#1565C0'
PAPER_GOLD = '#B45309'
PAPER_GOLD_STROKE = '#92400E'
PAPER_SHADOW = '#C2185B'
PAPER_MUTED = '#475569'
PAPER_RED = '#C62828'

CAPTION_LINE_SPACING = 0.35

# The caption rides along the top: it says what is going on, so it should be the
# first thing read, not the last. Content therefore lives below about y = 2.5.
CAPTION_Y = 3.3
TITLE_Y = 2.75

# One knob for the whole clip's tempo. 1.0 is as written; 1.2 plays 20% faster.
PACE = 1.2


def label(words, font_size=25, color=MUTED, max_width=None):
    kwargs = dict(font='Segoe UI', font_size=font_size, color=color)
    if max_width is not None:
        return Text(
            words,
            width=max_width,
            line_spacing=CAPTION_LINE_SPACING,
            **kwargs,
        )
    return Text(words, **kwargs)


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
    pace = PACE  # per-scene override point; a subclass can set its own without touching PACE.
    caption_color = MUTED  # a light-theme scene sets PAPER_MUTED

    def play(self, *animations, **kwargs):
        if self._inner:
            super().play(*animations, **kwargs)
            return
        scaled = kwargs['run_time'] / self.pace if 'run_time' in kwargs else 1.
        if 'run_time' in kwargs:
            kwargs['run_time'] = scaled
        self._inner = True
        try:
            super().play(*animations, **kwargs)
        finally:
            self._inner = False
        self.elapsed += scaled

    def wait(self, duration=1., **kwargs):
        scaled = duration / self.pace
        self._inner = True
        try:
            super().wait(scaled, **kwargs)
        finally:
            self._inner = False
        self.elapsed += scaled

    def mark(self, name, allow=()):
        """Record where the app should be able to pause. Pair with a hold.

        A mark is a frame the viewer actually reads, so it is also where the layout
        audit runs. `allow` exempts deliberate text-on-text pairs: `allow=[(a, b)]`.
        """
        if self.marks is None:
            self.marks = []
        self.marks.append({'name': name, 'time': round(self.elapsed, 2)})
        audit_mark(self, name, allow)

    def tear_down(self):
        audit_summary(self)
        super().tear_down()

    def write_marks(self, path):
        if self.marks:
            Path(path).write_text(json.dumps(self.marks, indent=2), encoding='utf-8')

    def say(self, words):
        wrap = getattr(self, 'caption_wrap_width', None)
        size = getattr(self, 'caption_font_size', 25)
        fresh = label(
            words, font_size=size, color=self.caption_color, max_width=wrap,
        ).move_to([0, CAPTION_Y, 0])
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


def apply_portal_paper_background():
    """White frame matching the student portal video viewer."""
    from manim import config

    config.background_color = PORTAL_PAGE_WHITE


from vector_portal_layout import CAPTION_MAX_WIDTH as _PORTAL_CAPTION_WIDTH


class VectorPortalScene(Narrated):
    """Narrated clips for the vector-projections portal app (wrap + inset)."""

    caption_wrap_width = _PORTAL_CAPTION_WIDTH
    caption_font_size = 24
