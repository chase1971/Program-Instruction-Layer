"""A phone-shaped (4:5) frame for clips drawn for the student portal's phone player.

Why: the portal shows the video as wide as the phone, about 375 px. A 14.2-unit-wide
landscape frame shrinks to ~26 px per unit there, so equations at font 28 land near 5 px
tall. A 6.4-unit-wide frame shows at ~58 px per unit, so the same font lands near 11 px.
The frame HEIGHT stays 8 units, so every vertical constant (CAPTION_Y, CAPTION_FLOOR, the
audit's margins) keeps its meaning; only horizontal room changes.

Call `apply_portrait_frame()` before importing any other project module. Modules such as
`vector_portal_layout` and `scene_audit` read `config.frame_width` at import time, so a
later call would leave them sized for the landscape frame.
"""

from manim import config

PORTRAIT_ASPECT = 4 / 5
FRAME_HEIGHT = 8.0


def apply_portrait_frame():
    """1080x1350 for a final render; 560x700 for the -ql / -qm drafts (libx264 needs even sizes)."""
    full = config.pixel_height >= 1000 or config.pixel_width >= 1000
    config.pixel_width = 1080 if full else 560
    config.pixel_height = 1350 if full else 700
    config.frame_height = FRAME_HEIGHT
    config.frame_width = FRAME_HEIGHT * PORTRAIT_ASPECT
