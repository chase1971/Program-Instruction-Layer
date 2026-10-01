"""Tighter layout for vector-projection portal clips (portrait-first).

Mirrors `scene_layout` with extra horizontal inset so captions and diagrams stay
inside the phone player without CSS crop-zoom. Import this module from the seven
portal vector scenes only — other PAPER clips keep `scene_layout`.
"""

from scene_audit import CAPTION_FLOOR, EDGE_MARGIN
from scene_layout import Region

from manim import config

# Extra inset per side beyond the audit edge margin (~30px at 1080p width).
VECTOR_H_INSET = 0.30

PORTAL_MATH_SCALE = 1.15

# Extra gap below the caption band before diagram/work content.
CONTENT_TOP = CAPTION_FLOOR - 0.18
FRAME_RIGHT = config.frame_width / 2 - EDGE_MARGIN - VECTOR_H_INSET
FRAME_BOTTOM = -(config.frame_height / 2 - EDGE_MARGIN)

CAPTION_SIDE_INSET = EDGE_MARGIN + VECTOR_H_INSET
CAPTION_MAX_WIDTH = config.frame_width - 2 * CAPTION_SIDE_INSET - 0.2

DEFAULT_GROW = 1.15

DIAGRAM = Region('DIAGRAM', -FRAME_RIGHT, 0.55, FRAME_BOTTOM, 2.40)
WORK = Region('WORK', 1.0, FRAME_RIGHT, FRAME_BOTTOM, 0.80)
GAUGE = Region('GAUGE', 1.0, FRAME_RIGHT, 1.00, CONTENT_TOP)
CENTER = Region('CENTER', -FRAME_RIGHT, FRAME_RIGHT, FRAME_BOTTOM, CONTENT_TOP)

PANELS = (DIAGRAM, WORK, GAUGE)
REGIONS = PANELS + (CENTER,)


def fit_into(mobject, region, buff=0.1, grow=DEFAULT_GROW):
    """Shrink to fit, then grow up to `grow` when there is headroom."""
    room_width = region.width - 2 * buff
    room_height = region.height - 2 * buff
    factor = 1.0
    if mobject.width > room_width > 0:
        factor = room_width / mobject.width
    if mobject.height > 0 and mobject.height * factor > room_height > 0:
        factor = min(factor, room_height / mobject.height)
    if factor < 1:
        mobject.scale(factor)
    elif grow > 1 and mobject.width > 0 and mobject.height > 0:
        grow_factor = min(
            grow,
            room_width / mobject.width if room_width > 0 else grow,
            room_height / mobject.height if room_height > 0 else grow,
        )
        if grow_factor > 1:
            mobject.scale(grow_factor)
    mobject.move_to(region.center)
    return mobject
