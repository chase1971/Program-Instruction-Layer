"""The 8 N / 22 N force problem, worked piece by piece as a decomposition.

Clip five of the vector series, after vector_decomposition.py; it replaces the older
standalone vector_projection_force.py. The question -- how much of the 22 N force acts
in the 8 N force's direction? -- is asked, then answered by splitting u into u1 along v
and u2 across v. u1 is u's shadow on v, v's size never moves that shadow, and the
projection formula gives u1 from lengths and an angle alone. The ||v||'s cancel down to
22 cos 50, which is why the 8 never mattered. Then u2 = u - u1, and a closing card
names the pieces the way Chase's notes do: parallel component / projection of u onto v,
orthogonal component / rejection vector.

Verified numbers (v along the x-axis):
    cos 50 = 0.64279,  sin 50 = 0.76604
    u = <22 cos 50, 22 sin 50> ~ <14.14, 16.85>,  v = <8, 0>
    u.v = 22 * 8 * cos 50 ~ 113.13,  ||v||^2 = 64,  113.13 / 64 ~ 1.768
    ||u1|| = 1.768 * 8 ~ 14.14 N = 22 cos 50,  u2 = u - u1 ~ <0, 16.85>,  ||u2|| ~ 16.85 N
"""

import math

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    Line,
        Scene,
    SurroundingRectangle,
    VGroup,
    Write,
    config,
)

from angle_between_vectors import V_COLOR, heading, lerp, make_corner, rebuild
from vector_portal_layout import CENTER, CONTENT_TOP, WORK, fit_into
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
from vector_decomposition import arrow, place, settle
from vector_projection_shadow import SHADOW, fraction, strike

apply_portal_paper_background()
BLUE = PAPER_BLUE
GOLD = PAPER_GOLD
INK = PAPER_INK
MUTED = PAPER_MUTED

U_COLOR = BLUE
U1_COLOR = SHADOW  # the part along v is the pink shadow, as in clips three and four
U2_COLOR = GOLD
U_NEWTONS = 22.
V_NEWTONS = 8.
THETA = math.radians(50)
ALONG = U_NEWTONS * math.cos(THETA)   # ~14.14 N, the answer
ACROSS = U_NEWTONS * math.sin(THETA)  # ~16.85 N
SCALE = ALONG / V_NEWTONS             # ~1.768: stretch v by this to reach the shadow

ORIGIN = np.array([-5.5, -2.55, 0.])
PER_NEWTON = .25  # screen units per newton
EAST = RIGHT
U_TIP = ORIGIN + PER_NEWTON * U_NEWTONS * heading(THETA)
U1_TIP = ORIGIN + PER_NEWTON * ALONG * EAST


def v_tip(state):
    return ORIGIN + PER_NEWTON * state['v'] * EAST


def make_u(_state):
    return arrow(ORIGIN, U_TIP, U_COLOR)


def make_u_label(_state):
    side = heading(THETA + math.pi / 2)
    return portal_math(r'\mathbf u', r'=22\text{ N}', color=U_COLOR, scale=.75).move_to(
        (ORIGIN + U_TIP) / 2 + .8 * side)


def make_v(state):
    return arrow(ORIGIN, v_tip(state), V_COLOR, width=6).set_z_index(1)


def make_v_label(state):
    return portal_math(r'\mathbf v', rf'={state["v"]:.0f}\text{{ N}}', color=V_COLOR).scale(.75).move_to(
        (ORIGIN + v_tip(state)) / 2 + .45 * DOWN)


def make_angle(_state):
    arc = VGroup(*[Line(ORIGIN + .75 * heading(THETA * k / 12), ORIGIN + .75 * heading(THETA * (k + 1) / 12),
                        color=INK, stroke_width=2) for k in range(12)])
    mark = portal_math(r'50^\circ', color=INK).scale(.6).move_to(ORIGIN + 1.2 * heading(THETA / 2))
    return VGroup(arc, mark)


def make_u1(_state):
    return arrow(ORIGIN, U1_TIP, U1_COLOR, width=13)


def make_u2(_state):
    return arrow(U1_TIP, U_TIP, U2_COLOR)


def make_u1_label(_state):
    return portal_math(r'\mathbf u_1', color=U1_COLOR).scale(.8).move_to(U1_TIP + np.array([-.75, .4, 0]))


def make_u2_label(_state):
    return portal_math(r'\mathbf u_2', color=U2_COLOR).scale(.8).move_to((U1_TIP + U_TIP) / 2 + .5 * EAST)


def make_right_angle(_state):
    return make_corner(U1_TIP, LEFT, UP, .2)


# Draw order: arrows first, labels last.
PARTS = {
    'angle': make_angle, 'corner': make_right_angle,
    'u1': make_u1, 'u2': make_u2, 'v': make_v, 'u': make_u,
    'u_label': make_u_label, 'v_label': make_v_label,
    'u1_label': make_u1_label, 'u2_label': make_u2_label,
}

EIGHT = dict(v=V_NEWTONS)
TWENTY = dict(v=20.)
FOUR = dict(v=4.)

PROJ = r'\operatorname{proj}_{\mathbf v}\mathbf u'
FORMULA = r'\left(\frac{\mathbf u\cdot\mathbf v}{\|\mathbf v\|^{2}}\right)'
COLORS = {'u': U_COLOR, 'v': V_COLOR, 'u1': U1_COLOR, 'u2': U2_COLOR, 'proj': U1_COLOR,
          '|u1|': U1_COLOR, '|u2|': U2_COLOR, '|proj|': U1_COLOR}
SYMBOLS = {'u': r'\mathbf u', 'v': r'\mathbf v', 'u1': r'\mathbf u_1', 'u2': r'\mathbf u_2',
           'proj': PROJ, '|u1|': r'\|\mathbf u_1\|', '|u2|': r'\|\mathbf u_2\|',
           '|proj|': rf'\|{PROJ}\|'}


def m(*pieces):
    """One row of math. A piece named in SYMBOLS is that vector, in its color."""
    row = portal_math(*[SYMBOLS.get(piece, piece) for piece in pieces], color=INK).scale(.75)
    for part, piece in zip(row, pieces):
        if piece in COLORS:
            part.set_color(COLORS[piece])
    return row


def t(source):
    return portal_math(source, color=INK).scale(.75)


def line_up(anchor, index, *rows):
    """Continuation rows start with '='; put it under the anchor row's piece `index`."""
    for continued in rows:
        continued.shift(RIGHT * (anchor[index].get_x() - continued[0].get_x()))


def make_given():
    given = m(r'\|\mathbf u\|=22\text{ N}', r',\;\;', r'\|\mathbf v\|=8\text{ N}', r',\;\;',
              r'\theta=50^\circ')
    given[0].set_color(U_COLOR)
    given[2].set_color(V_COLOR)
    return given.move_to([WORK.left + .1, CONTENT_TOP - .1, 0], aligned_edge=UP + LEFT)


def make_definitions():
    """What the two pieces are, in words, each under its symbol -- clip four's card."""
    rows = VGroup(*[VGroup(math, label(words, font_size=24, color=INK)).arrange(
        DOWN, buff=.16, aligned_edge=LEFT) for math, words in (
        (m('u1'), 'the part of u that goes in v’s direction'),
        (m('u2'), 'the part of u that has nothing to do with v'),
        (m('u', '=', 'u1', '+', 'u2'), 'together: the whole 22 N force'),
        (m(r'\text{How much?}', r'\;\to\;', '|u1|'), 'what the question asks for'))])
    return settle(place(rows, buff=.42))


def make_formula_work():
    proj = m('u1', '=', 'proj', '=', FORMULA, 'v')
    dot = m(r'\mathbf u\cdot\mathbf v', '=', r'\|\mathbf u\|\,\|\mathbf v\|\cos\theta')
    numbers = m('=', r'(22)(8)\cos 50^\circ', r'\approx 113.13')
    square = m(r'\|\mathbf v\|^{2}', '=', '8^{2}', '=', '64')
    scaled = m('u1', r'\approx', r'\frac{113.13}{64}', 'v', r'\approx', '1.768', 'v')
    length = m('|u1|', r'\approx', r'1.768\,(8\text{ N})', r'\approx', r'14.14\text{ N}')
    column = place(VGroup(proj, dot, numbers, square, scaled, length), buff=.32)
    line_up(dot, 1, numbers)
    return settle(column)


def make_cancel_work():
    """||u1|| = (u.v / ||v||^2) ||v||, with u.v opened up so the ||v||'s can be struck."""
    start = m('|u1|', '=', r'\frac{\mathbf u\cdot\mathbf v}{\|\mathbf v\|^{2}}\,\|\mathbf v\|')
    top = VGroup(t(r'\|\mathbf u\|'), t(r'\|\mathbf v\|'), t(r'\cos\theta')).arrange(RIGHT, buff=.08)
    bottom = VGroup(t(r'\|\mathbf v\|'), t(r'\|\mathbf v\|')).arrange(RIGHT, buff=.08)
    opened = VGroup(t('='), fraction(top, bottom), t(r'\|\mathbf v\|')).arrange(RIGHT, buff=.14)
    short = m('=', r'\|\mathbf u\|\cos\theta')
    value = m('=', r'22\cos 50^\circ', r'\approx', r'14.14\text{ N}')
    value[3].set_color(U1_COLOR)
    share = VGroup(m(r'\cos 50^\circ\approx 0.643'),
                   label('about 64% of u’s length lies along v', font_size=24, color=INK)
                   ).arrange(DOWN, buff=.16, aligned_edge=LEFT)
    column = place(VGroup(start, opened, short, value, share))
    line_up(start, 1, opened, short, value)
    share.shift(DOWN * .15)
    settle(column)
    struck = [top[1], bottom[0], bottom[1], opened[2]]
    return column, struck


def make_rejection_work():
    setup = VGroup(label('Put v along the x-axis:', font_size=24, color=INK),
                   m('v', '=', r'\langle 8,\,0\rangle')).arrange(RIGHT, buff=.3)
    u = m('u', '=', r'\langle 22\cos 50^\circ,\ 22\sin 50^\circ\rangle')
    u_value = m(r'\approx', r'\langle 14.14,\ 16.85\rangle')
    u1 = m('u1', r'\approx', r'\langle 14.14,\ 0\rangle')
    u2 = m('u2', '=', 'u', '-', 'u1', r'\approx', r'\langle 0,\ 16.85\rangle')
    check = m('u2', r'\cdot', 'v', r'\approx', r'(0)(8)+(16.85)(0)', '=', '0')
    column = place(VGroup(setup, u, u_value, u1, u2, check), buff=.34)
    line_up(u, 1, u_value)
    return settle(column)


def make_answer():
    words = VGroup(label('About 14.14 N of the 22 N force', font_size=26, color=INK),
                   label('acts in the direction of the 8 N force.', font_size=26, color=INK)
                   ).arrange(DOWN, buff=.14, aligned_edge=LEFT)
    column = place(VGroup(words, m('|proj|', '=', '|u1|', r'\approx', r'14.14\text{ N}')), buff=.4)
    return settle(column).shift(LEFT * .2)  # room for the answer box on the right


def make_summary():
    """Chase's formal definition, with this problem's numbers beside each piece."""
    title = label('Projection and decomposition', font_size=30, color=GOLD)
    split = VGroup(m('u', '=', 'u1', '+', 'u2'),
                   label('u and v nonzero', font_size=22)).arrange(RIGHT, buff=.4)
    blocks = [split]
    for math, here, words in (
            (m('u1', '=', 'proj', '=', FORMULA, 'v'), 'here: 14.14 N along v',
             'the parallel component of u (with v), or the projection of u onto v'),
            (m('u2', '=', 'u', '-', 'u1'), 'here: 16.85 N across v',
             'the orthogonal component of u (with v), or the rejection vector'),
            (m('|proj|'), 'here: 14.14 N',
             'how much of u lies in v’s direction, ignoring the perpendicular part')):
        top = VGroup(math, label(here, font_size=22)).arrange(RIGHT, buff=.45)
        blocks.append(VGroup(top, label(words, font_size=24, color=INK)).arrange(
            DOWN, buff=.14, aligned_edge=LEFT))
    body = place(VGroup(*blocks), buff=.4)
    return fit_into(VGroup(title, body).arrange(DOWN, buff=.4), CENTER)


class ForceDecomposition(VectorPortalScene, Scene):
    caption_color = PAPER_MUTED
    """How much of the 22 N force acts along the 8 N force: decompose, project, name."""

    pace = .9

    def show(self, *names, run_time=.8, how=FadeIn):
        self.play(*[how(self.parts[name]) for name in names], run_time=run_time)
        self.shown.update(names)

    def hide(self, *names, run_time=.6):
        self.play(*[FadeOut(self.parts[name]) for name in names], run_time=run_time)
        self.shown.difference_update(names)

    def morph(self, start, end, run_time=2.):
        """Rebuild v and its label from a state sliding from `start` to `end`."""
        self.play(*[rebuild(self.parts[name], lambda a, build=PARTS[name]: build(
            {key: lerp(start[key], end[key], a) for key in start})) for name in ('v', 'v_label')],
                  run_time=run_time)

    def problem(self):
        self.shown = set()
        self.parts = {name: build(EIGHT) for name, build in PARTS.items()}
        self.given = make_given()
        self.say('Two forces push on the same point: 8 N and 22 N, 50° apart.')
        self.show('v', run_time=.9, how=GrowArrow)
        self.show('u', run_time=1.1, how=GrowArrow)
        self.show('v_label', 'u_label', 'angle', run_time=.7)
        self.play(Write(self.given), run_time=1.)
        self.wait(1.)
        self.say('How much of the 22 N force acts in the same direction as the 8 N force?')
        self.wait(2.4)
        self.mark('question')

    def pieces(self):
        self.card = card = make_definitions()
        self.say('Split u like last clip: one piece along v, one piece straight across it.')
        self.show('u1', run_time=1., how=GrowArrow)
        self.show('u2', run_time=1., how=GrowArrow)
        self.show('corner', 'u1_label', 'u2_label', run_time=.6)
        self.wait(1.)
        self.say('u₁ is the part of the 22 N push that goes where the 8 N push goes.')
        self.play(FadeIn(card[0]), Indicate(self.parts['u1'], color=U1_COLOR), run_time=1.)
        self.wait(1.4)
        self.say('u₂ pushes straight across v. It does nothing in v’s direction.')
        self.play(FadeIn(card[1]), Indicate(self.parts['u2'], color=U2_COLOR), run_time=1.)
        self.wait(1.4)
        self.say('Every bit of u is in one piece or the other.')
        self.play(FadeIn(card[2]), Indicate(self.parts['u'], color=U_COLOR), run_time=1.)
        self.wait(1.2)
        self.say('So the question is really asking one thing: how long is u₁?')
        self.play(FadeIn(card[3]), run_time=.8)
        self.wait(2.)
        self.mark('pieces')

    def shadow(self):
        self.say('u₁ is u’s shadow on v from clip three: the projection of u onto v.')
        self.play(Indicate(self.parts['u1'], color=U1_COLOR), run_time=1.)
        self.wait(1.4)
        self.say('We want its length.')
        self.wait(1.4)
        self.mark('shadow')
        self.play(FadeOut(self.card), run_time=.6)

    def direction_only(self):
        self.say('Does the 8 matter? Change v’s size and watch the shadow.')
        self.wait(.6)
        self.morph(EIGHT, TWENTY, run_time=2.)
        self.wait(.5)
        self.morph(TWENTY, FOUR, run_time=2.2)
        self.wait(.5)
        self.morph(FOUR, EIGHT, run_time=1.2)
        self.say('The shadow never moves. v only tells us which direction to measure in.')
        self.play(Indicate(self.parts['u1'], color=U1_COLOR), run_time=1.)
        self.wait(1.8)
        self.mark('direction_only')

    def formula(self):
        proj, dot, numbers, square, scaled, length = self.work = make_formula_work()
        self.say('The projection formula from clip three gives u₁.')
        self.play(Write(proj), run_time=1.4)
        self.wait(1.)
        self.say('We have no components, only lengths and an angle. Clip two’s dot product uses exactly those.')
        self.play(Write(dot), run_time=1.2)
        self.wait(.8)
        self.play(Write(numbers), run_time=1.2)
        self.wait(.6)
        self.say('Square v’s length.')
        self.play(Write(square), run_time=1.)
        self.wait(.6)
        self.say('Divide: u₁ is v times about 1.768.')
        self.play(Write(scaled), run_time=1.3)
        self.wait(1.)
        self.mark('scale')

    def stretch_v(self):
        """What 1.768 means: stretch v by it and v is exactly as long as the shadow."""
        scaled, length = self.work[4], self.work[5]
        self.say('What is 1.768? It is how much to stretch v so it matches the shadow.')
        self.play(Indicate(scaled[5], color=GOLD), run_time=1.)
        below = .4 * DOWN
        self.hide('v_label', 'u1_label', run_time=.4)
        copy = make_v(EIGHT)
        self.play(copy.animate.shift(below), run_time=.6)
        self.play(rebuild(copy, lambda a: arrow(ORIGIN + below, ORIGIN + below + PER_NEWTON * V_NEWTONS
                                                * lerp(1, SCALE, a) * EAST, V_COLOR, width=6)), run_time=1.6)
        self.say('Last clip v was longer than its shadow, so we shrank it. Here v is shorter: stretch it.')
        self.play(copy.animate.set_color(U1_COLOR), run_time=.4)
        self.play(copy.animate.shift(-below), run_time=.6)
        self.play(FadeOut(copy), run_time=.3)
        self.show('v_label', 'u1_label', run_time=.4)
        self.wait(1.)
        self.say('So u₁’s length is 1.768 times v’s 8 N: about 14.14 N.')
        self.play(Write(length), run_time=1.3)
        self.wait(2.)
        self.mark('length')

    def cancel(self):
        column, struck = make_cancel_work()
        start, opened, short, value, share = column
        self.say('Why did the 8 not matter? Take the length of u₁ and write u · v out.')
        self.play(FadeOut(self.work), run_time=.6)
        self.play(Write(start), run_time=1.2)
        self.wait(.6)
        self.play(Write(opened), run_time=1.3)
        self.wait(.8)
        self.say('Every ‖v‖ cancels. The size of v drops out completely.')
        self.lines = VGroup(*[strike(piece) for piece in struck])
        self.play(*[Create(line) for line in self.lines], run_time=1.2)
        self.wait(.8)
        self.play(Write(short), run_time=1.)
        self.play(Write(value), run_time=1.2)
        self.wait(1.)
        self.say('cos 50° is the share of u that lies along v: about 64% of 22 N.')
        self.play(FadeIn(share), run_time=.9)
        self.wait(2.2)
        self.mark('cancel')
        self.work = VGroup(column)

    def rejection(self):
        setup, u, u_value, u1, u2, check = make_rejection_work()
        self.say('Now u₂, what is left of u: u₂ = u − u₁.')
        self.play(FadeOut(self.work), FadeOut(self.lines), run_time=.6)
        self.play(FadeIn(setup), run_time=.8)
        self.wait(.6)
        self.say('Write u in parts: 22 cos 50° across, 22 sin 50° up.')
        self.play(Write(u), run_time=1.2)
        self.play(Write(u_value), run_time=1.)
        self.wait(.8)
        self.say('u₁ is the shadow: 14.14 across, nothing up.')
        self.play(Write(u1), Indicate(self.parts['u1'], color=U1_COLOR), run_time=1.1)
        self.wait(.8)
        self.say('Subtract: u₂ is 16.85 N pushing straight across v.')
        self.play(Write(u2), Indicate(self.parts['u2'], color=U2_COLOR), run_time=1.3)
        self.wait(1.)
        self.say('Check: u₂ · v = 0. u₂ adds nothing along v.')
        self.play(Write(check), Indicate(self.parts['corner'], color=INK, scale_factor=1.6), run_time=1.3)
        self.wait(2.)
        self.mark('rejection')
        self.work = VGroup(setup, u, u_value, u1, u2, check)

    def answer(self):
        words, length = make_answer()
        self.say('So, how much of the 22 N force acts in the direction of the 8 N force?')
        self.play(FadeOut(self.work), run_time=.6)
        self.play(FadeIn(words), run_time=1.)
        self.play(Write(length), run_time=1.)
        box = SurroundingRectangle(VGroup(words, length), color=PAPER_GOLD_STROKE, buff=.2)
        self.play(Create(box), Indicate(self.parts['u1'], color=U1_COLOR), run_time=1.)
        self.wait(2.4)
        self.mark('answer')
        self.work = VGroup(words, length, box)

    def summary(self):
        title, body = make_summary()
        split, parallel, orthogonal, magnitude = body
        self.say('Now the names for what we just did.')
        self.play(FadeOut(self.work), FadeOut(self.given),
                  *[FadeOut(self.parts[name]) for name in self.shown], run_time=.8)
        self.play(FadeIn(title), Write(split), run_time=1.)
        self.wait(1.)
        self.say('u₁ is the parallel component of u, also called the projection of u onto v.')
        self.play(FadeIn(parallel), run_time=1.)
        self.wait(2.4)
        self.say('u₂ is the orthogonal component of u, also called the rejection vector.')
        self.play(FadeIn(orthogonal), run_time=1.)
        self.wait(2.4)
        self.say('And the projection’s length tells you how much of one vector lies in another’s direction.')
        self.play(FadeIn(magnitude), run_time=1.)
        self.wait(3.5)
        self.mark('summary')
        self.write_marks('force_decomposition_marks.json')

    def construct(self):
        self.problem()
        self.pieces()
        self.shadow()
        self.direction_only()
        self.formula()
        self.stretch_v()
        self.cancel()
        self.rejection()
        self.answer()
        self.summary()
