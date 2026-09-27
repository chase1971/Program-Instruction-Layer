"""Named layout regions, so panels cannot collide by construction.

`scene_audit.py` catches a collision after it happens. These regions stop most of them
from happening: put the diagram in DIAGRAM, the written work in WORK, a gauge or readout
in GAUGE, and a closing card in CENTER, and the panels are already clear of each other and
of the caption band.

The four boxes are not invented. They are measured from `dot_product_directions.py`, whose
layout was checked frame by frame -- its diagram lands inside DIAGRAM, its work inside WORK,
its gauge and readout inside GAUGE, and its closing cards inside CENTER, with room to
spare. `test_scene_layout.py` asserts exactly that, so the regions cannot drift away from a
layout known to read well.

    from scene_layout import WORK, fit_into
    fit_into(make_work(), WORK)

DIAGRAM, WORK and GAUGE are disjoint and may all be on screen at once. CENTER spans the
frame and is for beats where it is the only thing on screen -- closing cards, a title, a
question. Do not combine CENTER with the others.

Edges come from `scene_audit`, so the frame margin and the caption band are defined once.
"""

from scene_audit import CAPTION_FLOOR, EDGE_MARGIN

from manim import config

# A hair under the audit's hard line, so a mobject filling a region to its top edge cannot
# trip the caption-band check on a rounding error.
CONTENT_TOP = CAPTION_FLOOR - .05
FRAME_RIGHT = config.frame_width / 2 - EDGE_MARGIN
FRAME_BOTTOM = -(config.frame_height / 2 - EDGE_MARGIN)


class Region:
    """A named rectangle in scene units."""

    def __init__(self, name, left, right, bottom, top):
        self.name = name
        self.left, self.right, self.bottom, self.top = left, right, bottom, top

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.top - self.bottom

    @property
    def center(self):
        return [(self.left + self.right) / 2, (self.bottom + self.top) / 2, 0]

    def overlaps(self, other):
        return (min(self.right, other.right) - max(self.left, other.left) > 0
                and min(self.top, other.top) - max(self.bottom, other.bottom) > 0)

    def holds(self, mobject, slack=0.):
        """Is this mobject entirely inside the region?"""
        return (mobject.get_left()[0] >= self.left - slack
                and mobject.get_right()[0] <= self.right + slack
                and mobject.get_bottom()[1] >= self.bottom - slack
                and mobject.get_top()[1] <= self.top + slack)

    def __repr__(self):
        return (f'Region({self.name}, x [{self.left:.2f},{self.right:.2f}], '
                f'y [{self.bottom:.2f},{self.top:.2f}])')


# The picture: compass, arrows, vectors, anything being drawn rather than written.
DIAGRAM = Region('DIAGRAM', -FRAME_RIGHT, .55, FRAME_BOTTOM, 2.55)
# The written work, developing downward like handwriting.
WORK = Region('WORK', 1.0, FRAME_RIGHT, FRAME_BOTTOM, .95)
# A gauge, meter or running readout, above the work and clear of the caption.
GAUGE = Region('GAUGE', 1.0, FRAME_RIGHT, 1.15, CONTENT_TOP)
# Closing cards, titles, a question alone on screen. Not to be combined with the above.
CENTER = Region('CENTER', -FRAME_RIGHT, FRAME_RIGHT, FRAME_BOTTOM, CONTENT_TOP)

PANELS = (DIAGRAM, WORK, GAUGE)
REGIONS = PANELS + (CENTER,)


def fit_into(mobject, region, buff=.1):
    """Center a mobject in a region, scaling it down if it does not fit. Returns it."""
    room_width, room_height = region.width - 2 * buff, region.height - 2 * buff
    factor = 1.
    if mobject.width > room_width > 0:
        factor = room_width / mobject.width
    if mobject.height > 0 and mobject.height * factor > room_height > 0:
        factor = room_height / mobject.height
    if factor < 1:
        mobject.scale(factor)
    mobject.move_to(region.center)
    return mobject
