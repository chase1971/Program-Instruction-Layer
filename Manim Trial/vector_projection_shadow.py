"""What a vector projection is: the shadow one vector casts on another's line.

Clip three of the dot-product series, and the concept clip that comes before
vector_projection_force.py's worked problem. Light shines perpendicular to v, and
u's shadow on v's line is proj_v u. The picture is then changed live -- first u
longer than v (the shadow runs past v's tip), then v longer than u (it lands
inside v), then only v's length changes and the shadow does not move, because v
supplies nothing but a direction. It closes by building the textbook formula
proj_v u = (u . v / ||v||^2) v in two panels: SOH CAH TOA gives the shadow's
length, u . v / ||v||; multiplying that length by v's unit vector gives the vector.

No numbers appear on screen, so nothing here needs verifying -- the lengths below
only draw the picture.
"""

import math

import numpy as np
from manim import (
    DL,
    DOWN,
    LEFT,
    RIGHT,
    UR,
    Arc,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Line,
        Polygon,
    ReplacementTransform,
    Scene,
    SurroundingRectangle,
    VGroup,
    Write,
    config,
)

from angle_between_vectors import V_COLOR, heading, lerp, make_corner, rebuild
from vector_portal_layout import CONTENT_TOP, WORK, Region, fit_into
from scene_style import (
    portal_math,
    PAPER,
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_GOLD_STROKE,
    PAPER_INK,
    PAPER_MUTED,
    PAPER_SHADOW,
    VectorPortalScene,
    apply_portal_paper_background,
)

apply_portal_paper_background()
BLUE = PAPER_BLUE
GOLD = PAPER_GOLD
GOLD_STROKE = PAPER_GOLD_STROKE
INK = PAPER_INK
MUTED = PAPER_MUTED

U_COLOR = BLUE
SHADOW = PAPER_SHADOW

# v lies along a tilted line so "perpendicular to v" can't be mistaken for "straight down".
ORIGIN = np.array([-5.6, -2.6, 0.])
TILT = math.radians(15)
ALONG = heading(TILT)
NORMAL = heading(TILT + math.pi / 2)

LONG_U = dict(u=5.0, v=2.6, theta=math.radians(40))
LONG_V = dict(u=4.0, v=6.0, theta=math.radians(40))
SHORT_V = dict(u=4.0, v=1.9, theta=math.radians(40))


def blend(first, second, alpha):
    return {key: lerp(first[key], second[key], alpha) for key in first}


def u_tip(state):
    return ORIGIN + state['u'] * heading(TILT + state['theta'])


def shadow_length(state):
    return state['u'] * math.cos(state['theta'])


def foot(state):
    return ORIGIN + shadow_length(state) * ALONG


def beam_height(state):
    return state['u'] * math.sin(state['theta']) + .55


def arrow(start, end, color, width=7):
    return Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=.26,
                 max_tip_length_to_length_ratio=.3, max_stroke_width_to_length_ratio=20)


def make_line(_state):
    return DashedLine(ORIGIN - .4 * ALONG, ORIGIN + 6.5 * ALONG, color=MUTED,
                      dash_length=.12, stroke_opacity=.6)


def make_v(state):
    # On top of the (wider) shadow, which lies along the same line.
    return arrow(ORIGIN, ORIGIN + state['v'] * ALONG, V_COLOR, width=6).set_z_index(1)


def make_v_label(state):
    return portal_math(r'\mathbf v', color=V_COLOR, scale=.85).move_to(
        ORIGIN + (state['v'] - .15) * ALONG + .38 * NORMAL)


def make_u(state):
    return arrow(ORIGIN, u_tip(state), U_COLOR)


def make_u_label(state):
    direction = TILT + state['theta']
    return portal_math(r'\mathbf u', color=U_COLOR).scale(.85).move_to(
        ORIGIN + .55 * state['u'] * heading(direction) + .35 * heading(direction + math.pi / 2))


def make_arc(state):
    return Arc(radius=.75, start_angle=TILT, angle=state['theta'], arc_center=ORIGIN,
               color=MUTED, stroke_width=3)


def make_theta(state):
    return portal_math(r'\theta', color=INK).scale(.7).move_to(
        ORIGIN + 1.08 * heading(TILT + state['theta'] / 2))


def make_beam(state):
    """The column of light falling perpendicular to v, exactly as wide as the shadow."""
    top = beam_height(state) * NORMAL
    beam = Polygon(ORIGIN, foot(state), foot(state) + top, ORIGIN + top, stroke_width=0)
    # Behind the arrows (FadeIn would otherwise add it on top); fainter than .25, gold on
    # navy reads as gray.
    return beam.set_fill(GOLD_STROKE, opacity=.32).set_z_index(-1)


def make_lamp(state):
    lamp = Polygon([-.34, -.12, 0], [.34, -.12, 0], [.2, .14, 0], [-.2, .14, 0],
                   color=GOLD_STROKE, fill_color=GOLD_STROKE, fill_opacity=.9, stroke_width=2)
    lamp.rotate(TILT)
    middle = ORIGIN + shadow_length(state) / 2 * ALONG
    return lamp.move_to(middle + (beam_height(state) + .2) * NORMAL)


def make_drop(state):
    return DashedLine(u_tip(state), foot(state), color=INK, dash_length=.1, stroke_width=2.5)


def make_right_angle(state):
    return make_corner(foot(state), -ALONG, NORMAL, .2)


def make_shadow(state):
    return arrow(ORIGIN, foot(state), SHADOW, width=14)


def make_shadow_label(state):
    return portal_math(r'\operatorname{proj}_{\mathbf v}\mathbf u', color=SHADOW).scale(.8).move_to(
        ORIGIN + shadow_length(state) / 2 * ALONG - .55 * NORMAL)


# No gauge in this clip, so the formula may use the whole right side, WORK plus GAUGE.
RIGHT_SIDE = Region('RIGHT_SIDE', WORK.left, WORK.right, WORK.bottom, CONTENT_TOP)

# Draw order: light first so the arrows sit on top of it.
PARTS = {
    'beam': make_beam, 'lamp': make_lamp, 'line': make_line,
    'arc': make_arc, 'theta': make_theta,
    'drop': make_drop, 'corner': make_right_angle,
    'shadow': make_shadow, 'shadow_label': make_shadow_label,
    'v': make_v, 'v_label': make_v_label, 'u': make_u, 'u_label': make_u_label,
}


PROJ_LENGTH = r'\|\operatorname{proj}_{\mathbf v}\mathbf u\|'
DOT = r'\mathbf u\cdot\mathbf v'
U_LENGTH = r'\|\mathbf u\|'
V_LENGTH = r'\|\mathbf v\|'


def tex(source, color=INK):
    return portal_math(source, color=color).scale(.85)


def fraction(top, bottom):
    """A fraction built from pieces, so the top and bottom can each move on their own."""
    width = max(top.width, bottom.width) + .14
    bar = Line(LEFT * width / 2, RIGHT * width / 2, color=INK, stroke_width=3)
    return VGroup(top, bar, bottom).arrange(DOWN, buff=.1)


def row(*parts):
    return VGroup(*parts).arrange(RIGHT, buff=.22)  # room for a result box beside '='


def line_up(anchor, *rows):
    """Continuation rows start with '='; put it under the anchor row's '='."""
    for continued in rows:
        continued.shift(RIGHT * (anchor[1].get_x() - continued[0].get_x()))


def make_length_panel():
    """Panel 1: SOH CAH TOA turned into the length of the shadow.

    `trig` and `named` share a slot -- the words ADJ and HYP turn into the lengths.
    """
    trig = row(tex(r'\cos\theta'), tex('='),
               fraction(tex(r'\text{ADJ}', SHADOW), tex(r'\text{HYP}', U_COLOR)))
    named = row(tex(r'\cos\theta'), tex('='),
                fraction(tex(PROJ_LENGTH, SHADOW), tex(U_LENGTH, U_COLOR)))
    solved = row(tex(PROJ_LENGTH, SHADOW), tex('='), tex(U_LENGTH, U_COLOR), tex(r'\cos\theta'))
    swapped = row(tex(PROJ_LENGTH, SHADOW), tex('='), tex(U_LENGTH, U_COLOR),
                  fraction(tex(DOT), row(tex(U_LENGTH, U_COLOR), tex(V_LENGTH))))
    cancelled = row(tex('='), fraction(tex(DOT), tex(V_LENGTH)))
    column = VGroup(named, solved, swapped, cancelled).arrange(DOWN, buff=.42, aligned_edge=LEFT)
    line_up(swapped, cancelled)
    trig.move_to(named).align_to(named, LEFT)
    fit_into(VGroup(column, trig), RIGHT_SIDE)
    return trig, named, solved, swapped, cancelled


def make_vector_panel():
    """Panel 2: a length and a direction multiply into the projection vector."""
    length = row(tex(PROJ_LENGTH, SHADOW), tex('='), fraction(tex(DOT), tex(V_LENGTH)))
    unit = row(tex(r'\hat{\mathbf v}', GOLD), tex('='),
               fraction(tex(r'\mathbf v', V_COLOR), tex(V_LENGTH)))
    product = row(tex(r'\operatorname{proj}_{\mathbf v}\mathbf u', SHADOW), tex('='),
                  tex(PROJ_LENGTH, SHADOW), tex(r'\hat{\mathbf v}', GOLD))
    filled = row(tex('='), fraction(tex(DOT), tex(V_LENGTH)),
                 fraction(tex(r'\mathbf v', V_COLOR), tex(V_LENGTH)))
    formula = row(tex('='), fraction(tex(DOT), tex(r'\|\mathbf v\|^{2}')),
                  tex(r'\mathbf v', V_COLOR))
    column = VGroup(length, unit, product, filled, formula)
    column.arrange(DOWN, buff=.4, aligned_edge=LEFT)
    line_up(product, filled, formula)
    return fit_into(column, RIGHT_SIDE)


def copy_into(source, target):
    """Morph a copy of `source` into `target`, leaving `target` itself on screen.

    TransformFromCopy leaves the morphed copy behind instead, padded with duplicate
    parts to match the target's shape -- later fades and strikes then miss it.
    """
    return ReplacementTransform(source.copy(), target)


def strike(mobject):
    return Line(mobject.get_corner(DL), mobject.get_corner(UR), color=GOLD, stroke_width=4)


class VectorProjectionShadow(VectorPortalScene, Scene):
    caption_color = PAPER_MUTED
    """Light perpendicular to v; u's shadow on v's line is the projection."""

    pace = .9

    def show(self, *names, run_time=.8, how=FadeIn):
        self.play(*[how(self.parts[name]) for name in names], run_time=run_time)

    def morph(self, start, end, names, run_time=2.2):
        """Rebuild the named parts from a state sliding from `start` to `end`."""
        self.play(*[rebuild(self.parts[name], lambda a, build=PARTS[name]:
                            build(blend(start, end, a))) for name in names],
                  run_time=run_time)

    def ask(self):
        self.say('u points partly along v. How much of u points along v?')
        self.parts = {name: build(LONG_U) for name, build in PARTS.items()}
        self.show('line', run_time=.5)
        self.show('v', 'u', run_time=1.2, how=GrowArrow)
        self.show('v_label', 'u_label', 'arc', 'theta', run_time=.7)
        self.wait(1.8)
        self.mark('question')

    def cast_shadow(self):
        self.say('Shine a light straight at v’s line, perpendicular to v.')
        self.show('lamp', run_time=.5)
        self.show('beam', run_time=1.)
        self.wait(.6)
        self.say('Where the light is blocked, u leaves a shadow on v’s line.')
        self.show('drop', 'corner', run_time=.8, how=Create)
        self.show('shadow', run_time=1.1, how=GrowArrow)
        self.wait(.6)
        self.say('That shadow is the projection of u onto v.')
        self.show('shadow_label', run_time=.7, how=Write)
        self.wait(1.6)
        self.mark('shadow')
        self.say('Here u is longer than v, so the shadow runs past v’s tip.')
        self.wait(2.4)
        self.mark('u_longer')

    def swap_lengths(self):
        self.say('Now make u shorter and v longer.')
        self.morph(LONG_U, LONG_V, list(PARTS))
        self.say('The shadow shrinks with u, and now it lands inside v.')
        self.wait(2.4)
        self.mark('v_longer')

    def only_direction(self):
        self.say('Change only v’s length, and watch the shadow.')
        self.morph(LONG_V, SHORT_V, ['v', 'v_label'], run_time=1.6)
        self.morph(SHORT_V, LONG_V, ['v', 'v_label'], run_time=1.6)
        self.say('It never moves. v only supplies the direction.')
        self.wait(2.4)
        self.mark('direction_only')

    def length_panel(self):
        """Why the shadow's length is u.v / ||v||, starting from SOH CAH TOA."""
        parts = self.parts
        self.say('Take the light away and look at the right triangle.')
        self.play(FadeOut(parts['lamp']), FadeOut(parts['beam']),
                  parts['v'].animate.set_opacity(.25), parts['v_label'].animate.set_opacity(.25),
                  run_time=.9)
        self.wait(.6)
        trig, named, solved, swapped, cancelled = make_length_panel()
        self.say('Think SOH CAH TOA: cosine is the adjacent side over the hypotenuse.')
        # Wider words than the single letter u, so they sit further off the arrow.
        off_u = .4 * heading(TILT + LONG_V['theta'] + math.pi / 2)
        hyp = tex(r'\text{HYP}', U_COLOR).move_to(parts['u_label']).shift(off_u)
        adj = tex(r'\text{ADJ}', SHADOW).move_to(parts['shadow_label'])
        self.play(FadeTransform(parts['u_label'], hyp),
                  FadeTransform(parts['shadow_label'], adj), run_time=1.)
        self.play(Write(trig), run_time=1.2)
        self.wait(1.4)

        self.say('The adjacent side is the projection. The hypotenuse is u’s length.')
        u_length = tex(U_LENGTH, U_COLOR).move_to(hyp)
        shadow_length_label = tex(PROJ_LENGTH, SHADOW).move_to(adj)
        self.play(FadeTransform(adj, shadow_length_label),
                  *[FadeTransform(old, new) for old, new in zip(trig[2], named[2])],
                  run_time=1.3)
        self.remove(*trig[:2])
        self.add(*named[:2])
        self.wait(.6)
        self.play(FadeTransform(hyp, u_length), run_time=.9)
        self.wait(1.4)

        self.say('Multiply both sides by ‖u‖.')
        self.play(copy_into(named[2][0], solved[0]), FadeIn(solved[1]),
                  copy_into(named[2][2], solved[2]),
                  copy_into(named[0], solved[3]), run_time=1.4)
        self.wait(1.2)

        self.say('From clip two, cos θ is u·v over ‖u‖ ‖v‖.')
        self.play(*[copy_into(old, new) for old, new in zip(solved[:3], swapped[:3])],
                  run_time=1.)
        self.play(copy_into(solved[3], swapped[3]), run_time=1.2)
        self.wait(1.)

        self.say('The ‖u‖ on top cancels the ‖u‖ underneath.')
        strikes = VGroup(strike(swapped[2]), strike(swapped[3][2][0]))
        self.play(Create(strikes), run_time=.8)
        self.play(Write(cancelled), run_time=1.)
        box = SurroundingRectangle(cancelled[1], color=GOLD_STROKE, buff=.12)
        self.play(Create(box), run_time=.5)
        self.say('So the length of the shadow is u·v over ‖v‖.')
        self.wait(2.4)
        self.mark('projection_length')
        return VGroup(named, solved, swapped, cancelled, strikes, box), shadow_length_label

    def vector_panel(self, length_work, shadow_length_label):
        """A length is not yet a vector: give it v's direction."""
        parts = self.parts
        named, solved, swapped, cancelled, strikes, box = length_work
        length, unit, product, filled, formula = make_vector_panel()
        self.say('That is only a length. The projection is an arrow, so it needs a direction.')
        self.play(FadeOut(VGroup(named, solved, swapped[1:], strikes, box)),
                  ReplacementTransform(VGroup(swapped[0], cancelled[0], cancelled[1]), length),
                  parts['v'].animate.set_opacity(1), parts['v_label'].animate.set_opacity(1),
                  run_time=1.2)
        self.wait(1.)

        self.say('Its direction is v’s, shrunk to length 1: the unit vector v̂.')
        pointer = arrow(ORIGIN, ORIGIN + ALONG, GOLD, width=8).set_z_index(2)
        pointer_label = tex(r'\hat{\mathbf v}', GOLD).move_to(ORIGIN + .45 * ALONG - .5 * NORMAL)
        self.play(shadow_length_label.animate.shift(.35 * ALONG - .1 * NORMAL),
                  parts['shadow'].animate.set_opacity(.25), run_time=.6)
        self.play(GrowArrow(pointer), FadeIn(pointer_label), run_time=.9)
        self.play(Write(unit), run_time=1.)
        self.wait(1.2)

        self.say('Stretch v̂ to the shadow’s length: length times direction.')
        full = shadow_length(LONG_V)
        self.play(rebuild(pointer, lambda a: arrow(ORIGIN, ORIGIN + lerp(1, full, a) * ALONG,
                                                   GOLD, width=8)), run_time=1.6)
        self.play(FadeOut(pointer), parts['shadow'].animate.set_opacity(1), run_time=.6)
        self.play(Write(product[:2]), copy_into(length[0], product[2]),
                  copy_into(unit[0], product[3]), run_time=1.3)
        self.wait(1.2)

        self.say('Put in what the length and the direction each equal.')
        self.play(FadeIn(filled[0]), copy_into(length[2], filled[1]),
                  copy_into(unit[2], filled[2]), run_time=1.4)
        self.wait(1.)
        self.say('The two ‖v‖’s multiply into ‖v‖²: the projection formula.')
        self.play(Write(formula), run_time=1.2)
        self.play(Create(SurroundingRectangle(formula[1:], color=GOLD_STROKE, buff=.12)), run_time=.5)
        self.wait(2.6)
        self.mark('projection_vector')
        self.write_marks('vector_projection_shadow_marks.json')

    def construct(self):
        self.ask()
        self.cast_shadow()
        self.swap_lengths()
        self.only_direction()
        length_work, label = self.length_panel()
        self.vector_panel(length_work, label)
