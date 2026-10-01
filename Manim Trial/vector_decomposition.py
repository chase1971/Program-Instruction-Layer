"""Decomposing a vector into orthogonal components relative to another vector.

Clip four of the dot-product series, after vector_projection_shadow.py. It opens on
what "decompose" means with a decomposition students already know -- u = 3i + 4j is
u split along the x and y axes -- then rotates that perpendicular reference around u
to show any perpendicular pair works, and settles it on v's direction. Why we do it
(only the part along v acts along v), then the tie back to clip three: w1 is u's
shadow on v. Then the worksheet problem, u = 3i + 4j and v = 10i + 2j, in three
steps: project, subtract, check.

Verified numbers (exact fractions):
    u.v = 30 + 8 = 38,  ||v||^2 = 104,  38/104 = 19/52
    w1 = (19/52)<10, 2> = <95/26, 19/26> ~ <3.65, 0.73>
    w2 = <3, 4> - w1 = <78/26 - 95/26, 104/26 - 19/26> = <-17/26, 85/26> ~ <-0.65, 3.27>
    w2.v = (-170 + 170)/26 = 0,  w1 + w2 = <78/26, 104/26> = <3, 4>
"""

import math

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Indicate,
    Line,
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
    VectorPortalScene,
    apply_portal_paper_background,
    label,
)
from vector_projection_shadow import SHADOW, copy_into

apply_portal_paper_background()
BLUE = PAPER_BLUE
GOLD = PAPER_GOLD
INK = PAPER_INK
MUTED = PAPER_MUTED

U_COLOR = BLUE
W1_COLOR = SHADOW  # the piece along v is clip three's pink shadow
W2_COLOR = GOLD
U = np.array([3., 4.])
V = np.array([10., 2.])
PHI_V = math.atan2(V[1], V[0])
SCALE = np.dot(U, V) / np.dot(V, V)  # 19/52: w1 = SCALE * v
NOTE_SPOT = np.array([-3.3, -3.25, 0])  # under the diagram, clear of the work

# One state draws the whole diagram. `phi` is the direction of the perpendicular
# reference (0 = the x and y axes); every other key places or scales the picture.
BIG = dict(ox=-3.4, oy=-2.35, scale=1.05, phi=0., x0=-1., x1=4.8, y0=-.8, y1=4.7,
           reach1=4.9, reach2=4.6, axes_op=1.)
TILTED = dict(BIG, phi=math.radians(35), axes_op=.35)
LOW = dict(TILTED, phi=math.radians(-15))
FAR = dict(ox=-6.05, oy=-2.2, scale=.62, phi=math.radians(-15), x0=-1.1, x1=10.9,
           y0=-.9, y1=4.9, reach1=11., reach2=4.6, axes_op=.35)
ALONG_V = dict(FAR, phi=PHI_V)


def blend(first, second, alpha):
    return {key: lerp(first[key], second[key], alpha) for key in first}


def to_screen(state, xy):
    return np.array([state['ox'] + state['scale'] * xy[0], state['oy'] + state['scale'] * xy[1], 0.])


def frame(state):
    """The reference's two unit directions, in data coordinates."""
    phi = state['phi']
    return np.array([math.cos(phi), math.sin(phi)]), np.array([-math.sin(phi), math.cos(phi)])


def pieces(state):
    """u's two components against the reference: w1 along e1, w2 along e2."""
    e1, e2 = frame(state)
    return np.dot(U, e1) * e1, np.dot(U, e2) * e2


def arrow(start, end, color, width=7):
    return Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=.24,
                 max_tip_length_to_length_ratio=.3, max_stroke_width_to_length_ratio=20)


def make_axes(state):
    s = lambda x, y: to_screen(state, (x, y))
    style = dict(buff=0, color=MUTED, stroke_width=2.5, tip_length=.18,
                 max_tip_length_to_length_ratio=.5)
    return VGroup(Arrow(s(state['x0'], 0), s(state['x1'], 0), **style),
                  Arrow(s(0, state['y0']), s(0, state['y1']), **style)
                  ).set_opacity(state['axes_op']).set_z_index(-2)


def make_cross(state):
    """The chosen perpendicular reference: two dashed lines through the origin."""
    e1, e2 = frame(state)
    return VGroup(*[DashedLine(to_screen(state, -.8 * e), to_screen(state, reach * e), color=INK,
                               dash_length=.12, stroke_width=2, stroke_opacity=.55)
                    for e, reach in ((e1, state['reach1']), (e2, state['reach2']))]
                  ).set_z_index(-1)


def make_u(state):
    return arrow(to_screen(state, (0, 0)), to_screen(state, U), U_COLOR)


def make_u_label(state):
    spot = to_screen(state, .55 * U) + .38 * np.array([-.8, .6, 0])
    return portal_math(r'\mathbf u', color=U_COLOR, scale=.85).move_to(spot)


def make_v(state):
    return arrow(to_screen(state, (0, 0)), to_screen(state, V), V_COLOR, width=6).set_z_index(1)


def make_v_label(state):
    return portal_math(r'\mathbf v', color=V_COLOR).scale(.85).move_to(
        to_screen(state, V) + np.array([-.25, .38, 0]))


def make_w1(state):
    w1, _ = pieces(state)
    return arrow(to_screen(state, (0, 0)), to_screen(state, w1), W1_COLOR, width=13)


def make_w2(state):
    w1, _ = pieces(state)
    return arrow(to_screen(state, w1), to_screen(state, U), W2_COLOR)


def w1_spot(state):
    w1, _ = pieces(state)
    _, e2 = frame(state)
    return to_screen(state, w1 / 2) - .45 * np.array([*e2, 0])


def w2_spot(state):
    w1, _ = pieces(state)
    e1, _ = frame(state)
    side = 1 if np.dot(U, e1) >= 0 else -1
    return to_screen(state, (w1 + U) / 2) + .5 * side * np.array([*e1, 0])


def make_i_label(state):
    return portal_math(r'3\mathbf i', color=W1_COLOR).scale(.8).move_to(w1_spot(state))


def make_j_label(state):
    return portal_math(r'4\mathbf j', color=W2_COLOR).scale(.8).move_to(w2_spot(state))


def make_w1_label(state):
    return portal_math(r'\mathbf w_1', color=W1_COLOR).scale(.8).move_to(w1_spot(state))


def make_w2_label(state):
    return portal_math(r'\mathbf w_2', color=W2_COLOR).scale(.8).move_to(w2_spot(state))


def make_right_angle(state):
    w1, w2 = pieces(state)
    e1, e2 = frame(state)
    toward_origin = -np.sign(np.dot(U, e1)) * e1
    toward_u = np.sign(np.dot(U, e2)) * e2
    return make_corner(to_screen(state, w1), np.array([*toward_origin, 0]),
                       np.array([*toward_u, 0]), .2)


# Draw order: reference lines under the arrows, labels last.
PARTS = {
    'axes': make_axes, 'cross': make_cross, 'corner': make_right_angle,
    'w1': make_w1, 'w2': make_w2, 'v': make_v, 'u': make_u,
    'u_label': make_u_label, 'v_label': make_v_label,
    'i_label': make_i_label, 'j_label': make_j_label,
    'w1_label': make_w1_label, 'w2_label': make_w2_label,
}

COLORS = {'u': U_COLOR, 'v': V_COLOR, 'w1': W1_COLOR, 'w2': W2_COLOR}
SYMBOLS = {'u': r'\mathbf u', 'v': r'\mathbf v', 'w1': r'\mathbf w_1', 'w2': r'\mathbf w_2'}


def m(*pieces):
    """One row of math. A piece named 'u', 'v', 'w1' or 'w2' is that vector, in its color."""
    row = portal_math(*[SYMBOLS.get(piece, piece) for piece in pieces], color=INK).scale(.75)
    for part, piece in zip(row, pieces):
        if piece in COLORS:
            part.set_color(COLORS[piece])
    return row


def line_up(anchor, index, *rows):
    """Continuation rows start with '='; put it under the anchor row's '=' (piece `index`)."""
    for continued in rows:
        continued.shift(RIGHT * (anchor[index].get_x() - continued[0].get_x()))


GIVEN_U = r'3\mathbf i+4\mathbf j'
GIVEN_V = r'10\mathbf i+2\mathbf j'
W1_EXACT = r'\left\langle\frac{95}{26},\frac{19}{26}\right\rangle'
W2_EXACT = r'\left\langle-\frac{17}{26},\frac{85}{26}\right\rangle'


def make_given():
    short = m('u', '=', GIVEN_U)
    full = m('u', '=', GIVEN_U, r',\quad', 'v', '=', GIVEN_V)
    top_left = np.array([WORK.left + .1, CONTENT_TOP - .1, 0])
    for row in (short, full):
        row.move_to(top_left, aligned_edge=UP + LEFT)
    return short, full


# Written work goes under the given row, on the whole right side (this clip has no gauge).
BELOW_GIVEN = Region('BELOW_GIVEN', WORK.left, WORK.right, WORK.bottom, CONTENT_TOP - .75)


def place(column, buff=.36):
    """Stack rows downward like handwriting, top-left of the work area."""
    column.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    return column


def settle(column):
    fit_into(column, BELOW_GIVEN)
    return column.align_to([BELOW_GIVEN.left + .1, 0, 0], LEFT).align_to(
        [0, BELOW_GIVEN.top - .1, 0], UP)


def make_definitions():
    """What the two pieces are, in words, each under its symbol like the plan's steps."""
    rows = VGroup(*[VGroup(math, label(words, font_size=24, color=INK)).arrange(
        DOWN, buff=.16, aligned_edge=LEFT) for math, words in (
        (m('w1'), 'the part of u that goes in v’s direction'),
        (m('w2'), 'the part of u that has nothing to do with v'),
        (m('u', '=', 'w1', '+', 'w2'), 'every bit of u is in one or the other'))])
    return settle(place(rows, buff=.5))


def make_plan():
    steps = VGroup()
    for words, math in (('1.  Along v: project u onto v', m('w1', '=', r'\frac{\mathbf u\cdot\mathbf v}{\|\mathbf v\|^{2}}', 'v')),
                        ('2.  Across v: what is left over', m('w2', '=', 'u', '-', 'w1')),
                        ('3.  Check: perpendicular means dot = 0', m('w2', r'\cdot', 'v', '=', '0'))):
        steps.add(VGroup(label(words, font_size=24, color=INK), math).arrange(
            DOWN, buff=.18, aligned_edge=LEFT))
    for step in steps:
        step[1].shift(RIGHT * .45)
    return settle(place(steps, buff=.45))


def make_step_one():
    dot = m('u', r'\cdot', 'v', '=', '(3)(10)+(4)(2)', '=', '38')
    square = m(r'\|\mathbf v\|^{2}', '=', '10^{2}+2^{2}', '=', '104')
    scaled = m('w1', '=', r'\frac{38}{104}', 'v', '=', r'\frac{19}{52}\langle 10,2\rangle')
    result = m('=', W1_EXACT, r'\approx\langle 3.65,\ 0.73\rangle')
    column = place(VGroup(dot, square, scaled, result))
    line_up(scaled, 1, result)
    return settle(column)


def make_scale_note():
    """Under the diagram: 19/52 is the shadow's length over v's length."""
    return m(r'\frac{19}{52}', '=', r'\frac{\|\mathbf w_1\|}{\|\mathbf v\|}',
             r'\approx\frac{3.73}{10.20}', r'\approx 0.37').move_to(NOTE_SPOT)


def make_step_two():
    w1 = m('w1', '=', W1_EXACT)
    setup = m('w2', '=', 'u', '-', 'w1')
    values = m('=', r'\langle 3,4\rangle', '-', W1_EXACT)
    common = m('=', r'\left\langle\frac{78-95}{26},\frac{104-19}{26}\right\rangle')
    result = m('=', W2_EXACT, r'\approx\langle -0.65,\ 3.27\rangle')
    column = place(VGroup(w1, setup, values, common, result))
    line_up(setup, 1, values, common, result)
    return settle(column)


def make_step_three():
    w1 = m('w1', '=', W1_EXACT)
    w2 = m('w2', '=', W2_EXACT)
    dot = m('w2', r'\cdot', 'v', '=', r'-\frac{17}{26}(10)+\frac{85}{26}(2)')
    zero = m('=', r'\frac{-170+170}{26}', '=', '0')
    total = m('w1', '+', 'w2', '=', r'\left\langle\frac{78}{26},\frac{104}{26}\right\rangle',
              '=', r'\langle 3,4\rangle')
    column = place(VGroup(w1, w2, dot, zero, total))
    line_up(dot, 3, zero)
    return settle(column)


def make_answer():
    split = m('u', '=', 'w1', '+', 'w2')
    along = VGroup(m('w1', '=', r'\frac{95}{26}\mathbf i+\frac{19}{26}\mathbf j'),
                   label('along v', font_size=22)).arrange(RIGHT, buff=.35)
    across = VGroup(m('w2', '=', r'-\frac{17}{26}\mathbf i+\frac{85}{26}\mathbf j'),
                    label('perpendicular to v', font_size=22)).arrange(RIGHT, buff=.35)
    column = place(VGroup(split, along, across), buff=.45).scale(.9)
    return settle(column)


class VectorDecomposition(VectorPortalScene, Scene):
    caption_color = PAPER_MUTED
    """Split u into a piece along v and a piece perpendicular to v, then work the problem."""

    pace = .9

    def show(self, *names, run_time=.8, how=FadeIn):
        self.play(*[how(self.parts[name]) for name in names], run_time=run_time)
        self.shown.update(names)

    def hide(self, *names, run_time=.6):
        self.play(*[FadeOut(self.parts[name]) for name in names], run_time=run_time)
        self.shown.difference_update(names)

    def morph(self, start, end, run_time=2.2):
        """Rebuild every part on screen from a state sliding from `start` to `end`."""
        self.play(*[rebuild(self.parts[name], lambda a, build=PARTS[name]:
                            build(blend(start, end, a))) for name in PARTS if name in self.shown],
                  run_time=run_time)
        self.state = end

    def rebuild_now(self, state):
        """Rebuild the parts not on screen, so they fade in where they now belong."""
        for name, build in PARTS.items():
            if name not in self.shown:
                self.parts[name] = build(state)

    def meaning(self):
        self.shown = set()
        self.parts = {name: build(BIG) for name, build in PARTS.items()}
        self.given, self.given_full = make_given()
        self.say('What does it mean to decompose a vector?')
        self.show('axes', run_time=.6)
        self.show('u', run_time=1., how=GrowArrow)
        self.show('u_label', run_time=.5)
        self.play(Write(self.given), run_time=.9)
        self.wait(1.2)
        self.say('Decompose: split u into two perpendicular pieces that add back to u.')
        self.wait(1.4)
        self.say('You already know one: 3 along the x-axis, then 4 up the y-axis.')
        self.show('w1', run_time=1., how=GrowArrow)
        self.show('i_label', run_time=.5)
        self.show('w2', run_time=1., how=GrowArrow)
        self.show('j_label', 'corner', run_time=.6)
        self.wait(1.)
        self.say('So u = 3i + 4j is u decomposed along the x and y axes.')
        self.play(Indicate(self.given[2], color=GOLD), run_time=1.)
        self.wait(1.6)
        self.mark('axes_decomposition')

    def any_pair(self):
        self.say('The axes are only one choice. Any perpendicular pair of directions works.')
        self.hide('i_label', 'j_label', run_time=.5)
        self.show('cross', run_time=.6)
        self.morph(BIG, TILTED, run_time=2.4)
        self.wait(.6)
        self.morph(TILTED, LOW, run_time=2.4)
        self.say('Each choice gives new pieces, still at a right angle, still adding to u.')
        self.wait(2.2)
        self.mark('any_pair')

    def choose_v(self):
        self.say('This problem picks the reference for us: the direction of v.')
        self.play(ReplacementTransform(self.given, self.given_full[:3]),
                  FadeIn(self.given_full[3:]), run_time=.9)
        self.morph(LOW, FAR, run_time=1.8)
        self.rebuild_now(FAR)
        self.show('v', run_time=1.1, how=GrowArrow)
        self.show('v_label', run_time=.4)
        self.morph(FAR, ALONG_V, run_time=2.)
        self.rebuild_now(ALONG_V)
        self.show('w1_label', 'w2_label', run_time=.6)
        self.say('Now u splits into two pieces: w₁ along v, and w₂ straight across it.')
        self.wait(2.)
        self.mark('along_v')

    def shrink_copy_of_v(self):
        """Slide a copy of v out beside its line and shrink it to w1's length."""
        state = ALONG_V
        _, e2 = frame(state)
        self.below = below = -.34 * np.array([*e2, 0])
        zero = to_screen(state, (0, 0))
        self.hide('w1_label', run_time=.4)
        copy = make_v(state)
        self.play(copy.animate.shift(below), run_time=.7)
        self.play(rebuild(copy, lambda a: arrow(zero + below, to_screen(state, lerp(1, SCALE, a) * V)
                                                + below, V_COLOR, width=6)), run_time=1.6)
        return copy

    def land_on_w1(self, copy):
        """The shrunk copy turns pink and lifts onto w1: it was w1 all along."""
        self.play(copy.animate.set_color(W1_COLOR), run_time=.4)
        self.play(copy.animate.shift(-self.below), run_time=.7)
        self.play(FadeOut(copy), run_time=.3)
        self.show('w1_label', run_time=.4)

    def define_pieces(self):
        """Say what w1 and w2 are, and show it: w1 is v shrunk; w2 never moves u's shadow."""
        p, state = self.parts, ALONG_V
        self.card = card = make_definitions()
        w1, _ = pieces(state)
        zero = to_screen(state, (0, 0))

        self.say('w₁ is the part of u that goes in v’s direction.')
        self.play(FadeIn(card[0]), run_time=.8)
        copy = self.shrink_copy_of_v()
        self.say('It points exactly where v points. It is v, shrunk to fit inside u.')
        self.land_on_w1(copy)
        self.wait(1.)

        self.say('w₂ is the part of u that has nothing to do with v.')
        self.play(FadeIn(card[1]), run_time=.8)
        self.wait(.8)
        self.say('Slide along w₁, and your shadow on v slides with you.')
        base, top = to_screen(state, w1), to_screen(state, U)
        climber = Dot(zero, radius=.08, color=INK).set_z_index(3)
        shadow = Circle(radius=.15, color=W1_COLOR, stroke_width=4).move_to(zero).set_z_index(3)
        self.play(FadeIn(climber), FadeIn(shadow), run_time=.4)
        self.play(climber.animate.move_to(base), shadow.animate.move_to(base), run_time=1.6)
        self.say('Climb w₂, and the shadow does not move at all.')
        self.play(climber.animate.move_to(top), run_time=1.8)
        self.wait(1.)
        self.play(Indicate(p['corner'], color=INK, scale_factor=1.6), run_time=.9)
        self.play(FadeOut(climber), FadeOut(shadow), run_time=.4)

        self.say('Together they rebuild u. Every bit of u is in one piece or the other.')
        self.play(FadeIn(card[2]), run_time=.8)
        self.play(Indicate(p['u'], color=U_COLOR), run_time=1.)
        self.wait(1.8)
        self.mark('pieces_defined')

    def why(self):
        p = self.parts
        self.say('Why do this? Often only one direction matters. Picture a ramp along v.')
        self.wait(1.6)
        self.say('Push with u, and only w₁ moves you along the ramp.')
        self.play(p['w2'].animate.set_opacity(.2), p['w2_label'].animate.set_opacity(.2),
                  run_time=.6)
        self.wait(1.6)
        self.say('w₂ just presses into the ramp. It moves you none of the way along it.')
        self.play(p['w2'].animate.set_opacity(1), p['w2_label'].animate.set_opacity(1),
                  p['w1'].animate.set_opacity(.2), p['w1_label'].animate.set_opacity(.2),
                  run_time=.6)
        self.wait(1.6)
        self.play(p['w1'].animate.set_opacity(1), p['w1_label'].animate.set_opacity(1),
                  run_time=.5)
        self.mark('why')

    def shadow(self):
        self.say('w₁ is u’s shadow on v from clip three: the projection of u onto v.')
        self.play(Indicate(self.parts['w1'], color=W1_COLOR), run_time=1.)
        self.wait(1.4)
        self.say('And w₂ drops from u’s tip straight down to it.')
        self.play(Indicate(self.parts['w2'], color=W2_COLOR), run_time=1.)
        self.wait(1.4)
        self.mark('shadow')

    def plan(self):
        plan = make_plan()
        self.say('That gives a plan for any problem like this one.')
        self.play(FadeOut(self.card), run_time=.6)
        for step, words in zip(plan, ('Step 1: project u onto v. That is w₁.',
                                      'Step 2: since w₁ + w₂ = u, w₂ is u − w₁.',
                                      'Step 3: check. Perpendicular vectors dot to 0.')):
            self.say(words)
            self.play(FadeIn(step[0]), Write(step[1]), run_time=1.1)
            self.wait(1.)
        self.wait(1.)
        self.mark('plan')
        self.play(FadeOut(plan), run_time=.6)

    def step_one(self):
        dot, square, scaled, result = make_step_one()
        self.say('Step 1. Dot u with v: multiply matching parts and add.')
        self.play(Write(dot), run_time=1.4)
        self.wait(.8)
        self.say('Square v’s length.')
        self.play(Write(square), run_time=1.1)
        self.wait(.8)
        self.say('Scale v by u·v over ‖v‖², then reduce the fraction.')
        self.play(Write(scaled), run_time=1.4)
        self.wait(.8)
        self.explain_scale(scaled)
        self.say('Multiply 19/52 into each part of v and simplify.')
        self.play(Write(result), run_time=1.3)
        self.play(Indicate(self.parts['w1'], color=W1_COLOR), run_time=1.)
        self.say('About 3.65 across and 0.73 up: the pink shadow along v.')
        self.wait(2.)
        self.mark('step_one')
        return dot, square, scaled, result

    def explain_scale(self, scaled):
        """What 19/52 means: how far to shrink v so it is exactly as long as the shadow."""
        self.say('What is 19/52? It is how much to shrink v so it matches the shadow.')
        self.play(Indicate(scaled[5], color=GOLD), run_time=1.)
        copy = self.shrink_copy_of_v()
        self.scale_note = note = make_scale_note()
        self.say('The shadow is about 37% as long as v, so w₁ is 19/52 of v.')
        self.play(Write(note), run_time=1.4)
        self.land_on_w1(copy)
        self.wait(1.2)
        self.say('Like a unit vector, which shrinks v to length 1. Here: to the shadow’s length.')
        self.wait(2.6)
        self.mark('scale_factor')

    def step_two(self, previous):
        dot, square, scaled, result = previous
        w1, setup, values, common, answer = make_step_two()
        self.say('Step 2. What is left of u after w₁ is w₂.')
        self.play(FadeOut(VGroup(dot, square, scaled[2:], result[0], result[2], self.scale_note)),
                  ReplacementTransform(VGroup(scaled[:2], result[1]), w1), run_time=1.)
        self.play(Write(setup), run_time=1.)
        self.wait(.6)
        self.play(Write(values), run_time=1.3)
        self.wait(.8)
        self.say('Write 3 and 4 over 26 so the fractions subtract.')
        self.play(Write(common), run_time=1.4)
        self.wait(1.)
        self.play(Write(answer), run_time=1.3)
        self.say('That is w₂, the gold piece from w₁’s tip up to u’s tip.')
        self.play(Indicate(self.parts['w2'], color=W2_COLOR), run_time=1.)
        self.wait(2.)
        self.mark('step_two')
        return w1, setup, values, common, answer

    def step_three(self, previous):
        w1, setup, values, common, answer = previous
        w1_row, w2_row, dot, zero, total = make_step_three()
        self.say('Step 3. Check: if w₂ is perpendicular to v, then w₂ · v = 0.')
        self.play(FadeOut(VGroup(values, common, answer[0], answer[2], setup[2:])),
                  ReplacementTransform(w1, w1_row),
                  ReplacementTransform(VGroup(setup[:2], answer[1]), w2_row), run_time=1.)
        self.play(Write(dot), run_time=1.3)
        self.wait(.6)
        self.play(Write(zero), run_time=1.1)
        self.play(Indicate(self.parts['corner'], color=INK, scale_factor=1.6), run_time=1.)
        self.wait(1.)
        self.say('And the two pieces add back to u.')
        self.play(Write(total), run_time=1.4)
        self.play(Indicate(self.parts['u'], color=U_COLOR), run_time=1.)
        self.wait(2.)
        self.mark('check')
        return VGroup(w1_row, w2_row, dot, zero, total)

    def answer(self, previous):
        split, along, across = make_answer()
        self.say('u decomposed: one piece along v, one piece perpendicular to v.')
        self.play(FadeOut(previous[2:]), copy_into(previous[0], along[0]),
                  copy_into(previous[1], across[0]), FadeOut(previous[:2]), run_time=1.2)
        self.play(Write(split), FadeIn(along[1]), FadeIn(across[1]), run_time=1.)
        box = SurroundingRectangle(VGroup(along, across), color=PAPER_GOLD_STROKE, buff=.18)
        self.play(Create(box), run_time=.6)
        self.wait(3.)
        self.mark('answer')
        self.write_marks('vector_decomposition_marks.json')

    def construct(self):
        self.meaning()
        self.any_pair()
        self.choose_v()
        self.define_pieces()
        self.why()
        self.shadow()
        self.plan()
        work = self.step_one()
        work = self.step_two(work)
        work = self.step_three(work)
        self.answer(work)
