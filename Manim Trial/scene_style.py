"""Shared palette and caption line for Manim Trial scenes.

Colors and placement come from ANIMATION_STYLE_RECIPE.md. The earlier scenes
(gcf_division, solve_factors, two_step_equation) still carry their own copies;
new scenes import from here.
"""

import json
import re
from pathlib import Path

from manim import MarkupText, MathTex, Text, FadeIn, FadeOut

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
CAPTION_MAX_GROW = 1.3

# The caption rides along the top: it says what is going on, so it should be the
# first thing read, not the last. Content therefore lives below about y = 2.5.
CAPTION_Y = 3.3
TITLE_Y = 2.75

# One knob for the whole clip's tempo. 1.0 is as written; 1.2 plays 20% faster.
PACE = 1.2


CAPTION_SUPERSAMPLE = 4


def wrap_words(words, max_width, **kwargs):
    """Break `words` into lines no wider than max_width, measured with the real font."""
    lines, current = [], ''
    kind = MarkupText if '<' in words else Text
    # Split on spaces outside <...> so a tag with attributes stays in one piece.
    for word in re.split(r'\s+(?![^<]*>)', words.strip()):
        trial = f'{current} {word}'.strip()
        if current and kind(trial, **kwargs).width > max_width:
            lines.append(current)
            current = word
        else:
            current = trial
    lines.append(current)
    return '\n'.join(lines)


def label(words, font_size=25, color=MUTED, max_width=None, wrap=False):
    if '$' in words:
        from math_caption import math_caption
        return math_caption(words, font_size, color, max_width or 5.9)
    kwargs = dict(font='Segoe UI', font_size=font_size, color=color)
    if wrap and max_width is not None:
        # Narrow (portrait) frames: break into lines at full size instead of shrinking one
        # long line until it cannot be read.
        # Set the text at 4x and shrink it: Pango snaps glyph advances to whole pixels at
        # small sizes, which made the gaps between words uneven.
        big = {**kwargs, 'font_size': font_size * CAPTION_SUPERSAMPLE}
        # Markup (<i>a</i>) is allowed in a wrapped caption, so a variable can be set in italics.
        kind = MarkupText if '<' in words else Text
        return kind(wrap_words(words, max_width * CAPTION_SUPERSAMPLE, **big),
                    line_spacing=CAPTION_LINE_SPACING, **big).scale(1 / CAPTION_SUPERSAMPLE)
    if max_width is not None:
        # Fit to max_width, but never stretch a short caption past CAPTION_MAX_GROW: Text's
        # own width= argument stretches to exactly max_width, which blows a three-word
        # caption up off the top of the frame.
        text = Text(words, line_spacing=CAPTION_LINE_SPACING, **kwargs)
        text.scale(min(max_width / text.width, CAPTION_MAX_GROW))
        return text
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
        steps = self.caption_step_times()
        if steps:
            steps_path = Path(path).with_name(Path(path).stem.replace('_marks', '_steps') + '.json')
            steps_path.write_text(json.dumps(steps), encoding='utf-8')

    def caption_step_times(self):
        """Slow-mode pause times: one per caption, at the end of its beat.

        A caption's beat ends the instant the next `say()` starts (before its fade-out), so the
        frame is the finished board with that caption still up. The last step is the final
        mark (the hold). Portal Slow mode pauses here, one Next per caption.
        """
        starts = getattr(self, 'caption_starts', None)
        if not starts or not self.marks:
            return []
        gap = 0.04  # stop just before the next caption begins to fade out
        steps = [round(t - gap, 2) for t in starts[1:]]
        steps.append(self.marks[-1]['time'])
        # A long run with no caption change (board work only) keeps its own marks as steps.
        long_gap = 8.0
        extra = []
        previous = 0.
        for step in steps:
            if step - previous > long_gap:
                extra += [m['time'] for m in self.marks if previous + 2 < m['time'] < step - 2]
            previous = step
        return sorted(set(steps + extra))

    def say(self, words):
        if getattr(self, 'caption_starts', None) is None:
            self.caption_starts = []
        self.caption_starts.append(round(self.elapsed, 2))
        wrap = getattr(self, 'caption_wrap_width', None)
        size = getattr(self, 'caption_font_size', 25)
        fresh = label(
            words, font_size=size, color=self.caption_color, max_width=wrap,
            wrap=getattr(self, 'caption_wraps', False),
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
from vector_portal_layout import PORTAL_MATH_SCALE


def portal_math(*args, scale=1.0, **kwargs):
    """Portal clip equations — scaled by PORTAL_MATH_SCALE (default +15%)."""
    return MathTex(*args, **kwargs).scale(scale * PORTAL_MATH_SCALE)


class VectorPortalScene(Narrated):
    """Narrated clips for the vector-projections portal app (wrap + inset)."""

    caption_wrap_width = _PORTAL_CAPTION_WIDTH
    caption_font_size = 24
