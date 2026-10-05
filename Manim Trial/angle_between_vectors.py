"""Find the angle between two vectors by normalizing, then dotting.

Sequel to dot_product_directions.py. It opens on the question clip one closes on --
what if the vectors are different sizes? -- and answers it by deriving the formula:
shrink both vectors onto the circle of radius 1, dot the unit vectors, combine the
fractions into (u . v) / (||u|| ||v||), and recognize that as cos theta. The three
textbook problems are then worked by swinging one arrow at a time while the similarity
gauge follows it; the gauge stays empty until part (a)'s arithmetic fills it.

Every number written on screen comes from ANGLE_BETWEEN_PLAN.md. The angles used
below only draw the picture.

PORTRAIT: this clip is drawn for the phone player in a 4:5 frame (see portrait_frame.py),
6.4 x 8 units. The figure sits in a short band at the top (unit circle left, vertical
gauge right) and the written work stacks full-width underneath it, so the type can stay
large. The other six vector clips are still landscape.

History: a cheap-model draft of this clip was rejected (docs/CHEAP_MODEL_TRIAL.md).
This is the re-cut.
"""

# The frame must be set before any other project module is imported: they read
# config.frame_width at import time.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

import math  # noqa: E402

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN,
    LEFT,
    UP,
    Arc,
    Arrow,
    Circle,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowFromPoint,
    Line,
    ManimColor,
    Rectangle,
    Scene,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    TransformMatchingShapes,
    UpdateFromAlphaFunc,
    VGroup,
    VMobject,
    Write,
    interpolate_color,
)

from scene_layout import Region  # noqa: E402
from vector_portal_layout import fit_into  # noqa: E402
from scene_style import (  # noqa: E402
    portal_math,
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    PAPER_MUTED,
    VectorPortalScene,
    apply_portal_paper_background,
    label,
)

apply_portal_paper_background()
BLUE = PAPER_BLUE
GOLD = PAPER_GOLD
INK = PAPER_INK
MUTED = PAPER_MUTED

U_COLOR = BLUE
V_COLOR = '#E97B78'
W_COLOR = GOLD
NEGATIVE = V_COLOR

# Where theta sits for part (a): inside the wedge, clear of the horizontal axis.
THETA_A = math.radians(22)

# Directions of the textbook vectors u = 2i - 2j, v = 5i + 8j, w = 4i + 4j.
ANGLE_U = math.atan2(-2, 2)
ANGLE_V = math.atan2(8, 5)
ANGLE_W = math.atan2(4, 4)
LENGTH_U = math.hypot(2, -2)
LENGTH_V = math.hypot(5, 8)

# Frame is 6.4 x 8. Content stays inside +-EDGE sideways; the caption owns y > 2.95.
EDGE = 2.85
WORK_AREA = Region('WORK_AREA', -EDGE, EDGE, -3.75, -.6)

# Two views of one picture. FULL draws the vectors at their true lengths; UNIT zooms in
# on the circle of radius 1 once they are normalized. The zoom blends one into the other,
# so every arrow, arc and label is always built from the same origin and scale. FULL's
# scale is fitted so v (eight units tall) still clears the caption; its axes stop above
# WORK_AREA so the written work never lands on them.
FULL = dict(origin=(-1.4, .15), scale=.28, axes=(1.1, 1.8, .55, 2.3), arc=.5, theta=.8)
UNIT = dict(origin=(-1.4, 1.2), scale=1., axes=(1.25, 1.25, 1.1, 1.1), arc=.4, theta=.72)

# The gauge runs from -1 (opposite) through 0 (perpendicular) to 1 (same direction), so a
# fill grows from the middle: up and gold when positive, down and coral when not. It is
# vertical because the frame has more height than width.
GAUGE_X, GAUGE_Y = .9, 1.2
GAUGE_W, GAUGE_H = .34, 1.8
GAUGE_LABEL_X = GAUGE_X + GAUGE_W / 2 + .15
GAUGE_VALUE_CENTER = (1.75, -.02)
GAUGE_VALUE_MAX_WIDTH = 2.2

STROKE = 6
TIP_LABEL = .55


def blend(first, second, alpha):
    return {key: (1 - alpha) * np.array(first[key], dtype=float)
            + alpha * np.array(second[key], dtype=float) for key in first}


def lerp(start, end, alpha):
    return start + (end - start) * alpha


def origin_of(view):
    return np.array([*view['origin'], 0.])


def heading(angle):
    return np.array([math.cos(angle), math.sin(angle), 0.])


def point(view, angle, length):
    """Screen point `length` vector units from the view's origin, in direction `angle`."""
    return origin_of(view) + view['scale'] * length * heading(angle)


def make_axes(view):
    center = origin_of(view)
    left, right, down, up = view['axes']
    return VGroup(
        Line(center + [-left, 0, 0], center + [right, 0, 0], color=MUTED, stroke_width=2),
        Line(center + [0, -down, 0], center + [0, up, 0], color=MUTED, stroke_width=2),
        Dot(center, radius=.05, color=INK),
    )


def make_vector(view, angle, length, color):
    return Arrow(
        origin_of(view),
        point(view, angle, length),
        buff=0,
        color=color,
        stroke_width=STROKE,
        tip_length=.2,
        max_tip_length_to_length_ratio=.35,
        max_stroke_width_to_length_ratio=20,
    )


def make_tip_label(view, angle, length, tex, color, side=0.):
    """Label just past an arrow's tip; `side` nudges it counterclockwise (+) or clockwise (-)."""
    across = heading(angle + math.pi / 2)
    spot = point(view, angle, length) + .28 * heading(angle) + side * across
    return portal_math(tex, color=color, scale=TIP_LABEL).move_to(spot)


def make_unit_circle(view):
    ring = Circle(radius=view['scale'], color=MUTED, stroke_width=2, stroke_opacity=.75)
    return DashedVMobject(ring.move_to(origin_of(view)), num_dashes=56)


def make_angle(view, first, second):
    start, sweep = min(first, second), max(abs(second - first), 1e-3)
    return Arc(radius=view['arc'], start_angle=start, angle=sweep,
               arc_center=origin_of(view), color=MUTED, stroke_width=3)


def make_theta(view, direction, reach=None):
    reach = view['theta'] if reach is None else reach
    return portal_math(r'\theta', color=INK, scale=.6).move_to(
        origin_of(view) + reach * heading(direction))


def make_corner(vertex, first, second, size):
    """Square corner at `vertex` between two unit directions."""
    corner = VMobject(color=MUTED, stroke_width=3)
    corner.set_points_as_corners([
        vertex + size * first,
        vertex + size * (first + second),
        vertex + size * second,
    ])
    return corner


def make_gauge():
    center = [GAUGE_X, GAUGE_Y, 0]
    track = Rectangle(width=GAUGE_W, height=GAUGE_H, color=MUTED, stroke_width=3).move_to(center)
    middle = Line(track.get_left(), track.get_right(), color=MUTED, stroke_width=2)
    title = label('DIRECTIONAL\nSIMILARITY', 15, MUTED).move_to([1.85, 2.62, 0])
    entries = []
    for words, y in (('same direction', track.get_top()[1]),
                     ('perpendicular', GAUGE_Y),
                     ('opposite', track.get_bottom()[1])):
        text = label(words, 15, MUTED)
        entries.append(text.move_to([GAUGE_LABEL_X + text.width / 2, y, 0]))
    return VGroup(track, middle, title, *entries)


def make_fill(cosine):
    """The gauge fill for a cosine: grows from the middle toward -1 or 1."""
    height = max(abs(cosine) * GAUGE_H / 2, .03)
    color = GOLD if cosine >= 0 else NEGATIVE
    y = GAUGE_Y + math.copysign(height / 2, cosine)
    return Rectangle(width=GAUGE_W - .1, height=height, color=color, fill_color=color,
                     fill_opacity=.85, stroke_width=0).move_to([GAUGE_X, y, 0])


def make_gauge_value(tex, cosine):
    color = GOLD if cosine >= 0 else NEGATIVE
    value = portal_math(tex, color=color, scale=.6)
    if value.width > GAUGE_VALUE_MAX_WIDTH:
        value.scale(GAUGE_VALUE_MAX_WIDTH / value.width)
    return value.move_to([*GAUGE_VALUE_CENTER, 0])


def make_open_question():
    """Clip one's closing question, re-set for the narrow frame."""
    setup = label('Both speeds were exactly 1 mph.', 22, MUTED, max_width=5., wrap=True)
    question = label('What happens when the vectors are different sizes?', 28, GOLD,
                     max_width=5., wrap=True)
    return VGroup(setup, question).arrange(DOWN, buff=.5).move_to([0, .3, 0])


def make_derivation():
    """The formula, derived top to bottom: normalize, dot, combine, name it cos theta.

    Row 1 is the plain dot product; it becomes the left of row 2 once the vectors are unit
    length, so the column is laid out once and every row is born in its final place. Every
    step is its own line (the landscape layout ran three of them together sideways).
    """
    plain = portal_math(r'\mathbf u\cdot\mathbf v', color=INK, scale=.85)
    hats = portal_math(
        r'\hat{\mathbf u}=\frac{\mathbf u}{\|\mathbf u\|},\quad'
        r'\hat{\mathbf v}=\frac{\mathbf v}{\|\mathbf v\|}',
        color=MUTED, scale=.8,
    )
    dotted = portal_math(
        r'\hat{\mathbf u}\cdot\hat{\mathbf v}',
        r'=\frac{\mathbf u}{\|\mathbf u\|}\cdot\frac{\mathbf v}{\|\mathbf v\|}',
        color=INK, scale=.8,
    )
    combined = portal_math(
        r'=\frac{\mathbf u\cdot\mathbf v}{\|\mathbf u\|\,\|\mathbf v\|}',
        r'=\cos\theta',
        color=INK, scale=.85,
    )
    combined[1].set_color(GOLD)
    solved = portal_math(
        r'\theta=\arccos\!\left(\frac{\mathbf u\cdot\mathbf v}'
        r'{\|\mathbf u\|\,\|\mathbf v\|}\right)',
        color=INK, scale=.8,
    )
    column = VGroup(hats, dotted, combined, solved).arrange(
        DOWN, buff=.2, aligned_edge=LEFT)
    combined.align_to(dotted[1], LEFT)
    fit_into(column, WORK_AREA)
    plain.move_to(dotted[0]).align_to(dotted, LEFT)
    return plain, column


PAIR_TEX = {
    'u': r'\mathbf u=2\mathbf i-2\mathbf j',
    'v': r'\mathbf v=5\mathbf i+8\mathbf j',
    'w': r'\mathbf w=4\mathbf i+4\mathbf j',
}


def make_given(first, second):
    """The pair's vectors, one line, parked at the top-left of the work area."""
    given = portal_math(PAIR_TEX[first] + r',\quad ' + PAIR_TEX[second],
                        color=MUTED, scale=.62)
    room = WORK_AREA.width - .1
    if given.width > room:
        given.scale(room / given.width)
    return given.move_to([WORK_AREA.left + given.width / 2,
                          WORK_AREA.top - given.height / 2, 0])


def place_below(rows, anchor, factor=None):
    """Stack rows under `anchor`, left edges aligned, sized to what is left of the work area.

    The fitted scale is kept on `rows.fit_factor`, so the next problem reuses it and the
    given line above never has to move.
    """
    rows.arrange(DOWN, buff=.14, aligned_edge=LEFT)
    gap = .2
    if factor is None:
        room_w = WORK_AREA.width - .1
        room_h = anchor.get_bottom()[1] - gap - WORK_AREA.bottom
        factor = min(1.25, room_w / rows.width, room_h / rows.height)
    rows.scale(factor)
    rows.fit_factor = factor
    return rows.next_to(anchor, DOWN, buff=gap, aligned_edge=LEFT)


def make_problem_rows(anchor, dot, product, magnitudes, ratio, cosine, angle, degrees, factor=None):
    """Problem work, top to bottom. A long cosine row is split at its second fraction so the
    column is tall rather than wide -- that is what lets the type be large on a phone.

    `rows.result` is the row holding the boxed cosine, `rows.final` the angle row.
    """
    first_fraction = ratio.find(r'=\frac')
    split = ratio.rfind(r'=\frac')
    if split > first_fraction >= 0:
        cos_rows = [
            portal_math(ratio[:split], color=INK, scale=.68),
            portal_math(ratio[split:] + r'\;', cosine, color=INK, scale=.68),
        ]
    else:
        cos_rows = [portal_math(ratio, cosine, color=INK, scale=.68)]
    rows = VGroup(
        portal_math(dot, product, color=INK, scale=.68),
        portal_math(magnitudes, color=MUTED, scale=.64),
        *cos_rows,
        portal_math(angle, degrees, color=INK, scale=.68),
    )
    rows.result = cos_rows[-1]
    rows.final = rows[-1]
    for row in (rows.result, rows.final):
        row[1].set_color(GOLD)
    return place_below(rows, anchor, factor)


def make_unit_components(anchor):
    rows = VGroup(
        portal_math(r'\hat{\mathbf u}=\langle0.7071,-0.7071\rangle', color=U_COLOR),
        portal_math(r'\hat{\mathbf v}=\langle0.5300,0.8480\rangle', color=V_COLOR),
        portal_math(r'\hat{\mathbf w}=\langle0.7071,0.7071\rangle', color=W_COLOR),
    ).scale(.6).arrange(DOWN, buff=.14, aligned_edge=LEFT)
    return rows.move_to(anchor).align_to(anchor, LEFT).align_to(anchor, UP)


def make_payoff_rows(anchor):
    rows = VGroup(
        portal_math(r'\hat{\mathbf u}\cdot\hat{\mathbf v}\approx-0.22486',
                    r'\quad\theta\approx102.99^\circ', color=INK),
        portal_math(r'\hat{\mathbf v}\cdot\hat{\mathbf w}\approx0.97439',
                    r'\quad\theta\approx12.99^\circ', color=INK),
        portal_math(r'\hat{\mathbf u}\cdot\hat{\mathbf w}=0',
                    r'\quad\theta=90^\circ', color=INK),
    ).scale(.72)
    for row in rows:
        row[1].set_color(GOLD)
    return place_below(rows, anchor)


def rebuild(mobject, build):
    """Animate a mobject by rebuilding it from scratch every frame -- exact at every alpha."""
    return UpdateFromAlphaFunc(mobject, lambda m, alpha: m.become(build(alpha)))


class AngleBetweenVectors(VectorPortalScene, Scene):
    """Normalize, dot, read the cosine, then work the three textbook problems."""

    caption_color = PAPER_MUTED
    caption_wraps = True
    caption_font_size = 20
    pace = .9
    fill = None  # the gauge stays empty until part (a)'s arithmetic fills it

    def open_on_question(self):
        """Clip one's closing card, re-set for this frame, so the two clips still cut together."""
        card = make_open_question()
        self.add(card)
        self.wait(2.2)
        self.mark('open_question')
        self.play(FadeOut(card), run_time=.6)

    def draw_full_size(self):
        """Different lengths on screen, with the angle between them still theta."""
        self.say('Now the two vectors have different lengths.')
        self.axes = make_axes(FULL)
        self.first = make_vector(FULL, ANGLE_U, LENGTH_U, U_COLOR)
        self.second = make_vector(FULL, ANGLE_V, LENGTH_V, V_COLOR)
        u_label = make_tip_label(FULL, ANGLE_U, LENGTH_U, r'\mathbf u', U_COLOR)
        v_label = make_tip_label(FULL, ANGLE_V, LENGTH_V, r'\mathbf v', V_COLOR)
        self.play(FadeIn(self.axes), run_time=.5)
        self.play(Create(self.first), Create(self.second), run_time=1.2)
        self.play(FadeIn(u_label), FadeIn(v_label), run_time=.5)
        self.say('The angle between them is still θ.')
        self.arc = make_angle(FULL, ANGLE_U, ANGLE_V)
        self.theta = make_theta(FULL, THETA_A)
        self.play(Create(self.arc), FadeIn(self.theta), run_time=.8)
        self.wait(.8)

        self.say('We want their dot product. But clip one only worked at length 1.')
        self.plain, self.work = make_derivation()
        self.play(Write(self.plain), run_time=.9)
        self.wait(1.8)
        self.mark('different_lengths')
        return VGroup(u_label, v_label)

    def normalize(self, labels):
        """Shrink both arrows onto the circle of radius 1, then zoom in on it."""
        self.say('So make them length 1: divide each vector by its own length.')
        self.play(Write(self.work[0]), run_time=1.2)
        ghosts = VGroup(self.first.copy(), self.second.copy()).set_opacity(.22)
        self.add(ghosts)
        self.circle = make_unit_circle(FULL)
        self.play(FadeOut(labels), Create(self.circle), run_time=.7)
        self.play(
            rebuild(self.first, lambda a: make_vector(FULL, ANGLE_U, lerp(LENGTH_U, 1, a), U_COLOR)),
            rebuild(self.second, lambda a: make_vector(FULL, ANGLE_V, lerp(LENGTH_V, 1, a), V_COLOR)),
            run_time=1.8,
        )
        self.wait(.6)

        self.say('Zoom in. Same directions, same angle θ — now both length 1.')
        view = lambda a: blend(FULL, UNIT, a)
        self.play(
            FadeOut(ghosts),
            rebuild(self.axes, lambda a: make_axes(view(a))),
            rebuild(self.circle, lambda a: make_unit_circle(view(a))),
            rebuild(self.first, lambda a: make_vector(view(a), ANGLE_U, 1, U_COLOR)),
            rebuild(self.second, lambda a: make_vector(view(a), ANGLE_V, 1, V_COLOR)),
            rebuild(self.arc, lambda a: make_angle(view(a), ANGLE_U, ANGLE_V)),
            rebuild(self.theta, lambda a: make_theta(view(a), THETA_A)),
            run_time=1.8,
        )
        self.first_label = make_tip_label(UNIT, ANGLE_U, 1, r'\hat{\mathbf u}', U_COLOR)
        self.second_label = make_tip_label(UNIT, ANGLE_V, 1, r'\hat{\mathbf v}', V_COLOR, .22)
        self.play(FadeIn(self.first_label), FadeIn(self.second_label), run_time=.6)
        self.wait(1.2)
        self.mark('unit_vectors')

    def derive_formula(self):
        """Dot the unit vectors, combine the fractions, and recognize cos theta."""
        dotted, combined, solved = self.work[1], self.work[2], self.work[3]
        self.say('Now take the dot product of the two unit vectors.')
        self.play(TransformMatchingShapes(self.plain, dotted[0]), run_time=1.)
        self.play(TransformFromCopy(self.work[0], dotted[1]), run_time=1.3)
        self.wait(.8)
        self.say('The lengths are just numbers, so they combine into one fraction.')
        self.play(Write(combined[0]), run_time=1.2)
        self.wait(.8)
        self.say('From clip one: the dot product of unit vectors is cos θ.')
        self.play(Write(combined[1]), run_time=1.3)
        self.wait(.8)
        self.say('Undo the cosine to get the angle itself.')
        self.play(Write(solved), run_time=1.2)
        self.wait(1.8)
        self.mark('angle_formula')

    def standardize(self):
        """One scale for every pair, whatever the lengths were."""
        self.say('Dividing by the lengths standardizes them: direction alone is left.')
        self.gauge = make_gauge()
        self.play(FadeIn(self.gauge), run_time=.8)
        self.wait(.6)
        self.say('Every pair now reads on one scale, from −1 to 1.')
        self.wait(2.)
        self.mark('standardize')

    def land_result(self, rows, value_tex, cosine):
        """Box the computed cosine and fly it up onto the gauge."""
        box = SurroundingRectangle(rows.result[1], color=GOLD, buff=.08)
        self.play(Create(box), run_time=.4)
        value = make_gauge_value(value_tex, cosine)
        if self.fill is None:
            # Part (a): the gauge has been empty until now -- the arithmetic fills it.
            self.fill = make_fill(cosine)
            self.play(TransformFromCopy(rows.result[1], value),
                      GrowFromPoint(self.fill, [GAUGE_X, GAUGE_Y, 0]), run_time=1.3)
        else:
            self.play(FadeOut(self.value), TransformFromCopy(rows.result[1], value), run_time=1.1)
        self.value = value
        return box

    def write_rows(self, rows):
        for row in rows[:-1]:
            self.play(Write(row), run_time=.9)
            self.wait(.3)

    def problem_a(self):
        self.say('Part (a): u and v — the pair on screen.')
        self.play(FadeOut(self.work), run_time=.6)
        self.given = make_given('u', 'v')
        rows = make_problem_rows(
            self.given,
            r'\mathbf u\cdot\mathbf v=(2)(5)+(-2)(8)', r'=-6',
            r'\|\mathbf u\|\,\|\mathbf v\|=(2\sqrt2)(\sqrt{89})',
            r'\cos\theta=\frac{-6}{(2\sqrt2)(\sqrt{89})}=\frac{-3}{\sqrt{178}}',
            r'\approx-0.22486',
            r'\theta=\arccos(-0.22486)', r'\approx102.99^\circ',
        )
        self.rows_factor = rows.fit_factor
        self.play(FadeIn(self.given), run_time=.6)
        self.write_rows(rows)
        box = self.land_result(rows, r'\approx-0.22486', -0.22486)
        self.say('Negative: about 22% of v’s direction points against u.')
        self.wait(2.)
        self.say('A negative cosine means an obtuse angle: about 102.99°.')
        self.play(Write(rows.final), run_time=.9)
        self.wait(2.)
        self.mark('problem_a')
        return VGroup(rows, box)

    def swing(self, arrow, start, end, start_color, end_color, fixed):
        """Turn one unit arrow; the arc and the gauge fill follow it frame by frame."""
        start_color, end_color = ManimColor(start_color), ManimColor(end_color)
        turn = lambda a: lerp(start, end, a)
        return [
            rebuild(arrow, lambda a: make_vector(
                UNIT, turn(a), 1, interpolate_color(start_color, end_color, a))),
            rebuild(self.arc, lambda a: make_angle(UNIT, fixed, turn(a))),
            rebuild(self.fill, lambda a: make_fill(math.cos(turn(a) - fixed))),
        ]

    def problem_b(self, prior):
        self.say('Part (b): v and w. Swing u around to w.')
        self.play(FadeOut(prior), FadeOut(self.value), FadeOut(self.theta),
                  Transform(self.given, make_given('v', 'w')), run_time=.5)
        w_label = make_tip_label(UNIT, ANGLE_W, 1, r'\hat{\mathbf w}', W_COLOR, -.22)
        self.play(
            *self.swing(self.first, ANGLE_U, ANGLE_W, U_COLOR, W_COLOR, ANGLE_V),
            FadeTransform(self.first_label, w_label),
            run_time=2.,
        )
        self.first_label = w_label
        self.theta = make_theta(UNIT, ANGLE_W - .21)
        self.play(FadeIn(self.theta), run_time=.4)
        self.say('Almost the same direction, so the gauge nearly fills.')
        self.wait(1.2)
        rows = make_problem_rows(
            self.given,
            r'\mathbf v\cdot\mathbf w=(5)(4)+(8)(4)', r'=52',
            r'\|\mathbf v\|\,\|\mathbf w\|=(\sqrt{89})(4\sqrt2)',
            r'\cos\theta=\frac{52}{(\sqrt{89})(4\sqrt2)}=\frac{13}{\sqrt{178}}',
            r'\approx0.97439',
            r'\theta=\arccos(0.97439)', r'\approx12.99^\circ',
            factor=self.rows_factor,
        )
        self.write_rows(rows)
        box = self.land_result(rows, r'\approx0.97439', 1)
        self.say('Nearly all shared: an angle of about 12.99°.')
        self.play(Write(rows.final), run_time=.9)
        self.wait(2.)
        self.mark('problem_b')
        return VGroup(rows, box)

    def problem_c(self, prior):
        self.say('Part (c): u and w. Swing v back around to u.')
        self.play(FadeOut(prior), FadeOut(self.value), FadeOut(self.theta),
                  Transform(self.given, make_given('u', 'w')), run_time=.5)
        u_label = make_tip_label(UNIT, ANGLE_U, 1, r'\hat{\mathbf u}', U_COLOR)
        self.play(
            *self.swing(self.second, ANGLE_V, ANGLE_U, V_COLOR, U_COLOR, ANGLE_W),
            FadeTransform(self.second_label, u_label),
            run_time=2.2,
        )
        self.second_label = u_label
        center = origin_of(UNIT)
        square = make_corner(center, heading(ANGLE_U), heading(ANGLE_W), .25)
        quarter = label('90°', 18, MUTED).move_to(center + [.62, .2, 0])
        self.play(FadeOut(self.arc), Create(square), FadeIn(quarter), run_time=.7)
        self.arc = VGroup(square, quarter)
        self.say('A quarter turn apart: they share nothing, and the gauge sits at zero.')
        self.wait(1.6)
        self.say('Now let the arithmetic confirm the zero.')
        rows = make_problem_rows(
            self.given,
            r'\mathbf u\cdot\mathbf w=(2)(4)+(-2)(4)', r'=0',
            r'\|\mathbf u\|\,\|\mathbf w\|=(2\sqrt2)(4\sqrt2)',
            r'\cos\theta=\frac{0}{(2\sqrt2)(4\sqrt2)}', r'=0',
            r'\theta=\arccos(0)', r'=90^\circ',
            factor=self.rows_factor,
        )
        self.write_rows(rows)
        box = self.land_result(rows, '0', 1)
        self.play(Write(rows.final), run_time=.9)
        self.wait(2.)
        self.mark('problem_c')
        return VGroup(rows, box)

    def unit_vector_payoff(self, prior):
        self.say('Each unit-vector dot product is the cosine of its angle.')
        v_arrow = make_vector(UNIT, ANGLE_V, 1, V_COLOR)
        v_label = make_tip_label(UNIT, ANGLE_V, 1, r'\hat{\mathbf v}', V_COLOR, .22)
        self.play(FadeOut(prior), run_time=.5)
        components = make_unit_components(self.given)
        self.play(TransformMatchingShapes(self.given, components),
                  FadeIn(v_arrow), FadeIn(v_label), run_time=1.3)
        self.wait(.8)
        rows = make_payoff_rows(components)
        for row in rows:
            self.play(FadeIn(row, shift=DOWN * .15), run_time=.7)
            self.wait(.6)
        self.wait(2.2)
        self.mark('unit_vectors_payoff')
        self.write_marks('angle_between_vectors_marks.json')

    def construct(self):
        self.open_on_question()
        labels = self.draw_full_size()
        self.normalize(labels)
        self.derive_formula()
        self.standardize()
        prior = self.problem_a()
        prior = self.problem_b(prior)
        prior = self.problem_c(prior)
        self.unit_vector_payoff(prior)
