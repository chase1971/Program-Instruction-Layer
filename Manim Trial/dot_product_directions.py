"""Introduce the dot product as a measure of shared direction.

The clip teaches in classroom order: first see that east and north have nothing
in common, and only then let the arithmetic produce zero; repeat the pattern
with northeast for a partial match. It closes by limiting that clean similarity
reading to unit vectors and asking what happens when the magnitudes differ --
the hook for the follow-up clip.
"""

import math

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    Scene,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
    config,
)

from scene_style import (
    portal_math,
    PAPER,
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    PAPER_MUTED,
    VectorPortalScene,
    apply_portal_paper_background,
    label,
)
from scene_layout import Region
from vector_portal_layout import CENTER, FRAME_RIGHT, cs as _cs, fit_into, ms as _ms

apply_portal_paper_background()
BLUE = PAPER_BLUE
GOLD = PAPER_GOLD
INK = PAPER_INK
MUTED = PAPER_MUTED

# Everything below ``say()`` captions — diagram, gauge, formulas, closing cards — is
# drawn at vector_portal_layout.CONTENT_SCALE.
YOU_COLOR = BLUE
FRIEND_COLOR = '#E97B78'
# Diagram sits low and left: the frame has room on both sides, and the freed
# middle band is what keeps the labels, gauge and work from colliding.
ORIGIN = [-5.7, -2.6, 0]
ARROW_LENGTH = _cs(2.65)
NORTHEAST_COMPONENT = math.sqrt(2) / 2
# Left edge of the long northeast labels: just right of the NORTH axis, above the arrow tip.
NORTHEAST_LABEL_LEFT = ORIGIN[0] + .3
NORTHEAST_LABEL_Y = .8
WORK_CENTER = [3.4, -1.3, 0]
# The northeast work is three stacked fractions tall, so it sits lower than the
# perpendicular work to stay clear of the gauge readout.
NORTHEAST_WORK_REGION = Region('NORTHEAST_WORK', .6, FRAME_RIGHT, -3.4, .35)

# The similarity gauge is the clip's through-line: it appears empty for the
# perpendicular pair and is still on screen when northeast fills it partway.
METER_WIDTH = _cs(3.7)
METER_HEIGHT = _cs(0.42)
METER_CENTER = [3.15, 2.05, 0]


def make_compass():
    """Create simple east and north reference axes."""
    horizontal = Line(
        [ORIGIN[0] - _cs(.35), ORIGIN[1], 0],
        [ORIGIN[0] + _cs(3.35), ORIGIN[1], 0],
        color=MUTED,
        stroke_width=_cs(3),
    )
    vertical = Line(
        [ORIGIN[0], ORIGIN[1] - _cs(.35), 0],
        [ORIGIN[0], ORIGIN[1] + _cs(3.35), 0],
        color=MUTED,
        stroke_width=_cs(3),
    )
    east = label('EAST', round(_cs(18))).next_to(horizontal, RIGHT, buff=_cs(.08))
    north = label('NORTH', round(_cs(18))).next_to(vertical, UP, buff=_cs(.08))
    start = Dot(ORIGIN, radius=_cs(.06), color=INK)
    return VGroup(horizontal, vertical, east, north, start)


def make_travel_arrow(direction, color):
    """Create a unit-speed arrow in a compass direction."""
    tip = [
        ORIGIN[0] + ARROW_LENGTH * direction[0],
        ORIGIN[1] + ARROW_LENGTH * direction[1],
        0,
    ]
    return Arrow(
        ORIGIN,
        tip,
        buff=0,
        color=color,
        stroke_width=_cs(8),
        max_tip_length_to_length_ratio=.12,
    )


def make_vector_label(tex, arrow, color, side):
    """Place a label beside its arrow."""
    vector_label = portal_math(tex, color=color, scale=_ms(.7))
    vector_label.next_to(arrow, side, buff=_cs(.18))
    return vector_label


def place_northeast_label(vector_label):
    """Park a northeast label up-left of the arrow tip, clear of the gauge and work."""
    vector_label.move_to([0, NORTHEAST_LABEL_Y, 0])
    vector_label.align_to([NORTHEAST_LABEL_LEFT, 0, 0], LEFT)
    return vector_label


def make_right_angle():
    """Create the square corner that marks a quarter turn between directions."""
    size = _cs(.42)
    across = Line(
        [ORIGIN[0] + size, ORIGIN[1], 0],
        [ORIGIN[0] + size, ORIGIN[1] + size, 0],
        color=MUTED,
        stroke_width=3,
    )
    over = Line(
        [ORIGIN[0] + size, ORIGIN[1] + size, 0],
        [ORIGIN[0], ORIGIN[1] + size, 0],
        color=MUTED,
        stroke_width=3,
    )
    corner = label('90°', round(_cs(20)), MUTED).move_to(
        [ORIGIN[0] + _cs(.72), ORIGIN[1] + _cs(.72), 0],
    )
    return VGroup(across, over, corner)


def make_half_angle():
    """Create the 45-degree arc between east and northeast."""
    arc = Arc(
        radius=_cs(.72),
        start_angle=0,
        angle=math.pi / 4,
        arc_center=ORIGIN,
        color=MUTED,
        stroke_width=_cs(3),
    )
    amount = label('45°', round(_cs(20)), MUTED).move_to(
        [ORIGIN[0] + _cs(1.22), ORIGIN[1] + _cs(.34), 0],
    )
    return VGroup(arc, amount)


def make_meter():
    """Create the empty directional-similarity gauge."""
    track = Rectangle(
        width=METER_WIDTH,
        height=METER_HEIGHT,
        color=MUTED,
        stroke_width=3,
    ).move_to(METER_CENTER)
    heading = label('DIRECTIONAL SIMILARITY', round(_cs(18)), MUTED).next_to(
        track, UP, buff=_cs(.16),
    )
    low = label('nothing shared', round(_cs(15)), MUTED)
    low.next_to(track, DOWN, buff=_cs(.14)).align_to(track, LEFT)
    high = label('same direction', round(_cs(15)), MUTED)
    high.next_to(track, DOWN, buff=_cs(.14)).align_to(track, RIGHT)
    return VGroup(track, heading, low, high)


def make_meter_fill(fraction):
    """Create the gold portion of the gauge. Zero leaves a sliver at the left."""
    width = max(fraction * METER_WIDTH, .05)
    fill = Rectangle(
        width=width,
        height=METER_HEIGHT - .1,
        color=GOLD,
        fill_color=GOLD,
        fill_opacity=.85,
        stroke_width=0,
    )
    left_edge = METER_CENTER[0] - METER_WIDTH / 2
    return fill.move_to([left_edge + width / 2, METER_CENTER[1], 0])


def make_meter_value(tex):
    """Place the computed similarity beneath the gauge it confirms.

    Kept to one line of type -- a stacked fraction here would reach the work.
    """
    value = portal_math(tex, color=GOLD).scale(_ms(.85))
    return value.move_to([METER_CENTER[0], METER_CENTER[1] - _cs(.8), 0])


def make_northeast_components(northeast_arrow):
    """Show the equal coordinate components of a one-unit northeast vector."""
    tip = northeast_arrow.get_end()
    corner = [tip[0], ORIGIN[1], 0]
    east_component = DashedLine(ORIGIN, corner, color=GOLD, dash_length=.12)
    north_component = DashedLine(corner, tip, color=GOLD, dash_length=.12)
    east_label = portal_math(
        r'\frac{\sqrt2}{2}\text{ east}', color=GOLD,
    ).scale(_ms(.55))
    # Beyond the corner, above the axis: directly over the dashed run it crosses the arrow.
    east_label.move_to([corner[0] + _cs(.75), ORIGIN[1] + _cs(.5), 0])
    north_label = portal_math(
        r'\frac{\sqrt2}{2}\text{ north}', color=GOLD,
    ).scale(_ms(.55)).next_to(north_component, RIGHT, buff=_cs(.1))
    north_label.shift(UP * _cs(.55))
    return VGroup(east_component, north_component, east_label, north_label)


def make_perpendicular_work():
    """Create the component calculation for east dot north."""
    symbolic = portal_math(
        r'\langle 1,0\rangle\cdot\langle 0,1\rangle',
        color=INK,
    ).scale(_ms(.85))
    named = portal_math(
        r'(\text{east})(\text{east})+(\text{north})(\text{north})',
        color=MUTED,
    ).scale(_ms(.5))
    numeric = portal_math(
        r'(1)(0)+(0)(1)', r'=0', color=INK,
    ).scale(_ms(.9))
    numeric[1].set_color(GOLD)
    work = VGroup(symbolic, named, numeric)
    work.arrange(DOWN, buff=_cs(.34), aligned_edge=LEFT)
    return work.move_to(WORK_CENTER)


def make_northeast_work():
    """Create the component calculation for east dot northeast."""
    vectors = portal_math(
        r'\langle1,0\rangle\cdot'
        r'\left\langle\frac{\sqrt2}{2},\frac{\sqrt2}{2}\right\rangle',
        color=INK,
    ).scale(_ms(.68))
    products = portal_math(
        r'(1)\left(\frac{\sqrt2}{2}\right)'
        r'+(0)\left(\frac{\sqrt2}{2}\right)',
        color=INK,
    ).scale(_ms(.66))
    simplified = portal_math(
        r'\frac{\sqrt2}{2}+0',
        r'\;=\;',
        r'\frac{\sqrt2}{2}\approx0.707',
        color=INK,
    ).scale(_ms(.72))
    simplified[2].set_color(GOLD)
    work = VGroup(vectors, products, simplified)
    work.arrange(DOWN, buff=_cs(.2), aligned_edge=LEFT)
    return fit_into(work, NORTHEAST_WORK_REGION, buff=0, grow=1.0)


def make_unit_vector_note():
    """State the general dot product, then reduce it for unit vectors."""
    general = portal_math(
        r'\mathbf u\cdot\mathbf v=\|\mathbf u\|\,\|\mathbf v\|\cos\theta',
        color=INK,
    ).scale(_ms(.9))
    unit = portal_math(r'\|\mathbf u\|=\|\mathbf v\|=1', color=BLUE).scale(_ms(.8))
    reduced = portal_math(r'\mathbf u\cdot\mathbf v=\cos\theta', color=GOLD).scale(_ms(.95))
    rows = VGroup(general, unit, reduced).arrange(DOWN, buff=_cs(.45))
    return rows.move_to([0, .6, 0])


def make_case_summary():
    """Restate both results as the cosine of the angle between the directions."""
    rows = VGroup(
        portal_math(r'\text{east and north: }', r'\cos 90^\circ=0', color=INK),
        portal_math(
            r'\text{east and northeast: }',
            r'\cos 45^\circ=\frac{\sqrt2}{2}\approx0.707',
            color=INK,
        ),
    ).arrange(DOWN, buff=_cs(.45), aligned_edge=LEFT)
    rows[0][1].set_color(FRIEND_COLOR)
    rows[1][1].set_color(GOLD)
    rows.scale(_ms(.75))
    return rows.move_to([0, -2.55, 0])


def make_open_question():
    """Create the closing question that the next clip answers."""
    setup = label('Both speeds were exactly 1 mph.', round(_cs(28)), MUTED)
    question = label(
        'What happens when the vectors are different sizes?', round(_cs(34)), GOLD,
    )
    cards = VGroup(setup, question).arrange(DOWN, buff=_cs(.6))
    fit_into(cards, CENTER, grow=1.0)
    return cards


class DotProductDirections(VectorPortalScene, Scene):
    caption_color = PAPER_MUTED
    """Teach the dot product as shared direction, then confirm it with numbers."""

    pace = .9

    def show_travelers(self):
        """Put both 1 mph travelers on the compass before any algebra."""
        self.say('You travel east at 1 mph. Your friend travels north at 1 mph.')
        self.compass = make_compass()
        self.east_arrow = make_travel_arrow([1, 0], YOU_COLOR)
        self.friend_arrow = make_travel_arrow([0, 1], FRIEND_COLOR)
        self.east_label = make_vector_label(
            r'\text{you: 1 mph east}', self.east_arrow, YOU_COLOR, DOWN,
        )
        self.friend_label = make_vector_label(
            r'\text{friend: 1 mph north}', self.friend_arrow, FRIEND_COLOR, RIGHT,
        )
        self.play(FadeIn(self.compass), run_time=.6)
        self.play(
            LaggedStart(
                Create(self.east_arrow),
                Create(self.friend_arrow),
                lag_ratio=.35,
            ),
            run_time=1.6,
        )
        self.play(FadeIn(self.east_label), FadeIn(self.friend_label), run_time=.7)
        self.wait(1.5)

    def see_no_commonality(self):
        """Establish the missing shared direction before computing anything."""
        self.say('Do these two directions have anything in common?')
        corner = make_right_angle()
        self.play(Create(corner[0]), Create(corner[1]), FadeIn(corner[2]), run_time=.9)
        self.wait(1.2)
        self.say('Going east and going north share nothing at all.')
        self.meter = make_meter()
        self.meter_fill = make_meter_fill(0)
        self.play(FadeIn(self.meter), run_time=.8)
        self.play(FadeIn(self.meter_fill), run_time=.5)
        self.wait(1.0)
        self.say('That is what the dot product measures. Let the arithmetic agree.')
        self.wait(2.0)
        self.mark('no_commonality')
        return corner

    def confirm_with_zero(self):
        """Let the component calculation produce the zero the gauge predicted."""
        self.say('Write each direction as how far east and how far north.')
        east_components = make_vector_label(
            r'\text{you: }\langle1,0\rangle', self.east_arrow, YOU_COLOR, DOWN,
        )
        friend_components = make_vector_label(
            r'\text{friend: }\langle0,1\rangle', self.friend_arrow, FRIEND_COLOR, RIGHT,
        )
        self.play(
            ReplacementTransform(self.east_label, east_components),
            ReplacementTransform(self.friend_label, friend_components),
            run_time=1.0,
        )
        self.east_label = east_components
        self.friend_label = friend_components

        work = make_perpendicular_work()
        self.play(Write(work[0]), run_time=.9)
        self.play(Write(work[1]), run_time=.9)
        self.play(Write(work[2]), run_time=1.0)
        zero_box = SurroundingRectangle(work[2][1], color=GOLD, buff=_cs(.14))
        self.play(Create(zero_box), run_time=.4)
        self.wait(1.2)

        self.say('The zero is that shared nothing, written as a number.')
        self.meter_value = make_meter_value('0')
        self.play(TransformFromCopy(work[2][1], self.meter_value), run_time=1.1)
        self.wait(2.0)
        self.mark('east_dot_north')
        return VGroup(work, zero_box)

    def turn_friend_northeast(self, corner, work_group):
        """Swap north for northeast and see the partial match before the numbers."""
        self.say('Now your friend turns northeast, still at a total speed of 1 mph.')
        self.play(
            FadeOut(work_group),
            FadeOut(corner),
            FadeOut(self.meter_value),
            run_time=.6,
        )
        northeast_arrow = make_travel_arrow(
            [NORTHEAST_COMPONENT, NORTHEAST_COMPONENT], FRIEND_COLOR,
        )
        northeast_label = make_vector_label(
            r'\text{friend: 1 mph northeast}', northeast_arrow, FRIEND_COLOR, RIGHT,
        )
        place_northeast_label(northeast_label)
        self.play(ReplacementTransform(self.friend_arrow, northeast_arrow), run_time=1.2)
        self.play(ReplacementTransform(self.friend_label, northeast_label), run_time=.7)
        self.friend_arrow = northeast_arrow
        self.friend_label = northeast_label

        angle = make_half_angle()
        self.play(Create(angle[0]), FadeIn(angle[1]), run_time=.8)
        self.say('Northeast is halfway toward east, so now they do share direction.')
        grown = make_meter_fill(NORTHEAST_COMPONENT)
        self.play(ReplacementTransform(self.meter_fill, grown), run_time=1.1)
        self.meter_fill = grown
        self.wait(2.0)
        self.mark('some_commonality')
        return angle

    def confirm_with_partial(self, angle):
        """Let the calculation put a number on the partly shared direction."""
        self.say('A 1 mph northeast vector has equal east and north components.')
        components = make_northeast_components(self.friend_arrow)
        northeast_components = make_vector_label(
            r'\text{friend: }\left\langle\frac{\sqrt2}{2},'
            r'\frac{\sqrt2}{2}\right\rangle',
            self.friend_arrow,
            FRIEND_COLOR,
            RIGHT,
        )
        place_northeast_label(northeast_components)
        self.play(FadeOut(angle), run_time=.4)
        self.play(
            Create(components[0]),
            Create(components[1]),
            FadeIn(components[2]),
            FadeIn(components[3]),
            ReplacementTransform(self.friend_label, northeast_components),
            run_time=1.3,
        )
        self.friend_label = northeast_components
        self.wait(1.2)

        work = make_northeast_work()
        self.play(Write(work[0]), run_time=1.0)
        self.play(Write(work[1]), run_time=1.1)
        self.play(Write(work[2]), run_time=1.1)
        result_box = SurroundingRectangle(work[2][2], color=GOLD, buff=_cs(.14))
        self.play(Create(result_box), run_time=.4)
        self.wait(1.0)

        self.say('About 0.707 — partly the same direction, not all the way.')
        value = make_meter_value(r'\approx 0.707')
        self.play(TransformFromCopy(work[2][2], value), run_time=1.1)
        self.meter_value = value
        self.wait(2.2)
        self.mark('east_dot_northeast')
        return VGroup(
            self.compass, self.east_arrow, self.east_label, self.friend_arrow,
            self.friend_label, components, work, result_box,
            self.meter, self.meter_fill, self.meter_value,
        )

    def close_on_unit_vectors(self, screen_objects):
        """Limit the clean reading to unit vectors, then leave the open question."""
        self.say('This reads as pure direction only because both speeds are exactly 1.')
        self.play(FadeOut(screen_objects), run_time=.7)
        note = make_unit_vector_note()
        self.play(Write(note[0]), run_time=1.2)
        self.play(FadeIn(note[1]), run_time=.7)
        self.play(Write(note[2]), run_time=.9)
        self.wait(1.4)
        summary = make_case_summary()
        self.play(
            LaggedStart(*[FadeIn(row, shift=RIGHT * .2) for row in summary], lag_ratio=.35),
            run_time=1.2,
        )
        self.wait(2.2)
        self.mark('unit_vectors_only')

        self.hush()
        self.play(FadeOut(note), FadeOut(summary), run_time=.7)
        question = make_open_question()
        self.play(FadeIn(question[0]), run_time=.7)
        self.play(Write(question[1]), run_time=1.3)
        self.wait(2.5)
        self.mark('open_question')
        self.write_marks('dot_product_directions_marks.json')

    def construct(self):
        self.show_travelers()
        corner = self.see_no_commonality()
        work_group = self.confirm_with_zero()
        angle = self.turn_friend_northeast(corner, work_group)
        screen_objects = self.confirm_with_partial(angle)
        self.close_on_unit_vectors(screen_objects)
