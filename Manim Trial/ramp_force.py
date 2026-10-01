"""The wagon on a hill: how much force keeps it from rolling down?

Clip six of the vector series, after force_decomposition.py -- Chase's worksheet
problem 7. A 100 lb wagon sits on a hill with a 20 degree grade. Its weight points
straight down, so split it the way clip five split u: w1 along the ramp (the part that
rolls the wagon) and w2 straight into the hill (the hill pushes back on it). w1 is w's
shadow on the ramp, so it is proj_r w with r a unit vector up the ramp -- the ramp's
length never matters, only its direction. The dot product comes out negative, which
says w1 points down the hill; holding the wagon takes the same size push up the hill.
Every ramp works the same way, which closes on Chase's shortcut:
Force to remain stationary = Weight x sin(theta).

Verified numbers:
    sin 20 = 0.34202,  cos 20 = 0.93969
    w = <0, -100>,  r = <cos 20, sin 20> ~ <0.940, 0.342>,  ||r||^2 = 1
    w.r = (0)(cos 20) + (-100)(sin 20) = -100 sin 20 ~ -34.20
    proj_r w = (w.r) r ~ -34.20 r ~ <-32.14, -11.70>,  ||proj_r w|| ~ 34.20 lb
    w2 = w - w1 ~ <32.14, -88.30>,  ||w2|| = 100 cos 20 ~ 93.97 lb,  w2.r = 0
"""

import math

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    Line,
    Rectangle,
    Scene,
    SurroundingRectangle,
    VGroup,
    Write,
    config,
)

from angle_between_vectors import V_COLOR, heading, make_corner
from vector_portal_layout import CENTER, CONTENT_TOP, WORK, Region, fit_into
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
from vector_decomposition import arrow, place
from vector_projection_shadow import SHADOW

apply_portal_paper_background()
BLUE = PAPER_BLUE
GOLD = PAPER_GOLD
INK = PAPER_INK
MUTED = PAPER_MUTED

W_COLOR = BLUE
R_COLOR = V_COLOR
W1_COLOR = SHADOW  # the part along the ramp is the pink shadow, as in clips three to five
W2_COLOR = GOLD
F_COLOR = '#9BE39B'  # the push that holds the wagon
WEIGHT = 100.
THETA = math.radians(20)
ALONG = WEIGHT * math.sin(THETA)   # ~34.20 lb, the answer
INTO = WEIGHT * math.cos(THETA)    # ~93.97 lb

UP_RAMP = heading(THETA)
DOWN_RAMP = -UP_RAMP
INTO_HILL = np.array([math.sin(THETA), -math.cos(THETA), 0.])  # perpendicular, into the ramp
OUT_OF_HILL = -INTO_HILL

FOOT = np.array([-6.55, -2.3, 0.])  # bottom of the hill, where the 20 degree angle sits
TOP = FOOT + 7.2 * UP_RAMP
PER_POUND = .03  # screen units per pound
WAGON_AT = 5.  # distance up the ramp from the foot
WHEEL = .13
BODY_HEIGHT = .46
P = FOOT + WAGON_AT * UP_RAMP + (2 * WHEEL + BODY_HEIGHT / 2) * OUT_OF_HILL  # wagon center
W_TIP = P + PER_POUND * WEIGHT * DOWN
W1_TIP = P + PER_POUND * ALONG * DOWN_RAMP
F_TIP = P + PER_POUND * ALONG * UP_RAMP
R_START = FOOT + 1.9 * UP_RAMP
R_LENGTH = 1.3  # a unit vector, drawn at whatever size reads


def make_hill(_state):
    ramp = Line(FOOT, TOP, color=MUTED, stroke_width=4)
    ground = Line(FOOT, FOOT + 7.2 * math.cos(THETA) * RIGHT, color=MUTED, stroke_width=3)
    return VGroup(ground, ramp).set_z_index(-2)


def make_angle(_state):
    arc = VGroup(*[Line(FOOT + 1.1 * heading(THETA * k / 10), FOOT + 1.1 * heading(THETA * (k + 1) / 10),
                        color=INK, stroke_width=2) for k in range(10)])
    mark = portal_math(r'20^\circ', color=INK, scale=.6).move_to(FOOT + 1.6 * heading(THETA / 2))
    return VGroup(arc, mark)


def make_wagon(_state):
    body = Rectangle(width=1.25, height=BODY_HEIGHT, color=INK, stroke_width=3).rotate(THETA).move_to(P)
    base = P + (BODY_HEIGHT / 2 + WHEEL) * INTO_HILL
    wheels = VGroup(*[Circle(radius=WHEEL, color=INK, stroke_width=3).move_to(base + s * .4 * UP_RAMP)
                      for s in (-1, 1)])
    handle = Line(P + .62 * UP_RAMP, P + 1.1 * UP_RAMP + .3 * OUT_OF_HILL, color=INK, stroke_width=3)
    return VGroup(body, wheels, handle).set_z_index(-1)


def make_w(_state):
    return arrow(P, W_TIP, W_COLOR)


def make_w_label(_state):
    return portal_math(r'\mathbf w', r'=100\text{ lb}', color=W_COLOR).scale(.7).next_to(
        (P + W_TIP) / 2 + .15 * DOWN, RIGHT, buff=.2)


def make_w1(_state):
    return arrow(P, W1_TIP, W1_COLOR, width=13).set_z_index(1)


def make_w2(_state):
    return arrow(W1_TIP, W_TIP, W2_COLOR)


def make_w1_label(_state):
    return portal_math(r'\mathbf w_1', color=W1_COLOR).scale(.8).move_to(W1_TIP + .55 * OUT_OF_HILL + .25 * LEFT)


def make_w2_label(_state):
    return portal_math(r'\mathbf w_2', color=W2_COLOR).scale(.8).move_to((W1_TIP + W_TIP) / 2 + .45 * LEFT)


def make_corner_mark(_state):
    return make_corner(W1_TIP, UP_RAMP, INTO_HILL, .2)


def make_r(_state):
    return arrow(R_START, R_START + R_LENGTH * UP_RAMP, R_COLOR, width=6).set_z_index(1)


def make_r_label(_state):
    return portal_math(r'\mathbf r', color=R_COLOR).scale(.8).move_to(
        R_START + .5 * R_LENGTH * UP_RAMP + .42 * OUT_OF_HILL)


def make_r_legs(_state):
    """cos 20 across, sin 20 up: a unit vector at 20 degrees, as on clip two's unit circle."""
    tip = R_START + R_LENGTH * UP_RAMP
    corner = np.array([tip[0], R_START[1], 0.])
    across = DashedLine(R_START, corner, color=MUTED, stroke_width=2.5, dash_length=.08)
    up = DashedLine(corner, tip, color=MUTED, stroke_width=2.5, dash_length=.08)
    cos = portal_math(r'\cos 20^\circ', color=INK).scale(.5).next_to(across, DOWN, buff=.1)
    sin = portal_math(r'\sin 20^\circ', color=INK).scale(.5).next_to(up, RIGHT, buff=.1)
    return VGroup(across, up, cos, sin)


def make_f(_state):
    return arrow(P, F_TIP, F_COLOR, width=9).set_z_index(1)


def make_f_label(_state):
    return portal_math(r'\approx 34.2\text{ lb}', color=F_COLOR).scale(.7).next_to(
        F_TIP + .3 * UP, RIGHT, buff=.2)  # clear of the wagon's handle


# Draw order: shapes first, labels last.
PARTS = {
    'hill': make_hill, 'angle': make_angle, 'wagon': make_wagon, 'corner': make_corner_mark,
    'r_legs': make_r_legs, 'r': make_r, 'w2': make_w2, 'w1': make_w1, 'w': make_w, 'f': make_f,
    'w_label': make_w_label, 'w1_label': make_w1_label, 'w2_label': make_w2_label,
    'r_label': make_r_label, 'f_label': make_f_label,
}

PROJ = r'\operatorname{proj}_{\mathbf r}\mathbf w'
FORMULA = r'\left(\frac{\mathbf w\cdot\mathbf r}{\|\mathbf r\|^{2}}\right)'
COLORS = {'w': W_COLOR, 'r': R_COLOR, 'w1': W1_COLOR, 'w2': W2_COLOR, 'proj': W1_COLOR,
          '|proj|': W1_COLOR, 'F': F_COLOR}
SYMBOLS = {'w': r'\mathbf w', 'r': r'\mathbf r', 'w1': r'\mathbf w_1', 'w2': r'\mathbf w_2',
           'proj': PROJ, '|proj|': rf'\|{PROJ}\|', 'F': r'\text{Force}'}


def m(*pieces):
    """One row of math. A piece named in SYMBOLS is that vector, in its color."""
    row = portal_math(*[SYMBOLS.get(piece, piece) for piece in pieces], color=INK).scale(.75)
    for part, piece in zip(row, pieces):
        if piece in COLORS:
            part.set_color(COLORS[piece])
    return row


def line_up(anchor, index, *rows):
    """Continuation rows start with '='; put it under the anchor row's piece `index`."""
    for continued in rows:
        continued.shift(RIGHT * (anchor[index].get_x() - continued[0].get_x()))


# The worksheet's blanks (a) and (b) stay pinned top right; the work develops beneath them.
PINNED_TOP = CONTENT_TOP - .1
BELOW_PINNED = Region('BELOW_PINNED', WORK.left, WORK.right, WORK.bottom, .9)


def pin(row, index):
    return row.move_to([WORK.left + .1, PINNED_TOP - .75 * index, 0], aligned_edge=UP + LEFT)


def make_given():
    return pin(m(r'\text{Weight}=100\text{ lb}', r',\;\;', r'\theta=20^\circ'), 0)


def make_answer_a():
    return pin(m(r'\text{(a)}\;\;', 'w', '=', r'\langle 0,\,-100\rangle'), 1)


def make_answer_b():
    return pin(m(r'\text{(b)}\;\;', 'r', '=', r'\langle \cos 20^\circ,\,\sin 20^\circ\rangle'), 2)


def settle(column):
    fit_into(column, BELOW_PINNED)
    return column.align_to([BELOW_PINNED.left + .1, 0, 0], LEFT).align_to(
        [0, BELOW_PINNED.top - .1, 0], UP)


def make_definitions():
    """What the two pieces of the weight are, in words, each under its symbol."""
    rows = VGroup(*[VGroup(math, label(words, font_size=24, color=INK)).arrange(
        DOWN, buff=.16, aligned_edge=LEFT) for math, words in (
        (m('w1'), 'pulls the wagon down the hill'),
        (m('w2'), 'presses it into the hill; the hill pushes back'),
        (m(r'\text{How much?}', r'\;\to\;', r'\|\mathbf w_1\|'), 'the push we have to match'))])
    return settle(place(rows, buff=.4))


def make_projection_work():
    proj = m('proj', '=', FORMULA, 'r')
    unit = m(r'\|\mathbf r\|^{2}', '=', '1', r'\;\;\Rightarrow\;\;', 'proj', '=', r'(\mathbf w\cdot\mathbf r)', 'r')
    dot = m(r'\mathbf w\cdot\mathbf r', '=', r'(0)(\cos 20^\circ)+(-100)(\sin 20^\circ)')
    value = m('=', r'-100\sin 20^\circ', r'\approx', r'-34.20')
    result = m('proj', r'\approx', r'-34.20\,', 'r')
    length = m(r'\text{(c)}\;\;', '|proj|', r'\approx', r'34.20\text{ lb}')
    column = place(VGroup(proj, unit, dot, value, result, length), buff=.3)
    line_up(dot, 1, value)
    return settle(column)


def make_answer():
    words = VGroup(label('It takes about 34.2 lb, pushing up the hill,', font_size=26, color=INK),
                   label('to keep the wagon from rolling down.', font_size=26, color=INK)
                   ).arrange(DOWN, buff=.14, aligned_edge=LEFT)
    column = place(VGroup(words, m('F', r'\approx', r'34.2\text{ lb}')), buff=.4)
    return settle(column).shift(LEFT * .2 + DOWN * .3)  # room for the answer box


def make_shortcut():
    """Any weight W on any ramp at angle theta: the dot product is always -W sin theta."""
    title = label('Every ramp works the same way', font_size=30, color=GOLD)
    setup = m('w', '=', r'\langle 0,\,-W\rangle', r',\qquad', 'r', '=', r'\langle\cos\theta,\,\sin\theta\rangle')
    dot = m(r'\mathbf w\cdot\mathbf r', '=', r'(0)(\cos\theta)+(-W)(\sin\theta)', '=', r'-W\sin\theta')
    length = m(r'\|\mathbf r\|=1', r'\;\;\Rightarrow\;\;', '|proj|', '=', r'W\sin\theta')
    rule = portal_math(r'\text{Force to remain stationary}', '=', r'\text{Weight}\times\sin\theta',
                   color=INK).scale(.95)
    rule[0].set_color(F_COLOR)
    where = label('where θ is the angle of the ramp', font_size=24)
    check = m(r'100\times\sin 20^\circ', r'\approx', r'34.2\text{ lb}')
    work = place(VGroup(setup, dot, length), buff=.3)
    boxed = VGroup(rule, where).arrange(DOWN, buff=.18)
    card = VGroup(title, work, boxed, check).arrange(DOWN, buff=.42)
    return fit_into(card, CENTER)


class RampForce(VectorPortalScene, Scene):
    caption_color = PAPER_MUTED
    """Worksheet problem 7: the force that holds a 100 lb wagon on a 20 degree hill."""

    pace = .9

    def show(self, *names, run_time=.8, how=FadeIn):
        self.play(*[how(self.parts[name]) for name in names], run_time=run_time)
        self.shown.update(names)

    def hide(self, *names, run_time=.6):
        self.play(*[FadeOut(self.parts[name]) for name in names], run_time=run_time)
        self.shown.difference_update(names)

    def problem(self):
        self.shown = set()
        self.parts = {name: build({}) for name, build in PARTS.items()}
        self.given = make_given()
        self.say('A wagon with two kids in it weighs 100 lb. It sits on a hill with a 20° grade.')
        self.show('hill', run_time=1., how=Create)
        self.show('angle', 'wagon', run_time=.9)
        self.play(Write(self.given), run_time=1.)
        self.wait(1.2)
        self.say('What force keeps the wagon from rolling down the hill?')
        self.wait(2.4)
        self.mark('question')

    def weight(self):
        self.answer_a = make_answer_a()
        self.say('Gravity pulls the wagon straight down with its whole weight: 100 lb.')
        self.show('w', run_time=1.1, how=GrowArrow)
        self.show('w_label', run_time=.5)
        self.wait(.8)
        self.say('Straight down means nothing sideways: 0 across, −100 up.')
        self.play(Write(self.answer_a), run_time=1.2)
        self.wait(1.2)
        self.say('But the wagon can only roll along the hill, not straight down through it.')
        self.wait(2.2)
        self.mark('weight')

    def pieces(self):
        self.card = card = make_definitions()
        self.say('So split w like last clip: one piece along the ramp, one straight into it.')
        self.show('w1', run_time=1., how=GrowArrow)
        self.show('w2', run_time=1., how=GrowArrow)
        self.show('corner', 'w1_label', 'w2_label', run_time=.6)
        self.wait(1.)
        self.say('w₁ runs along the ramp. It is the part of the weight that rolls the wagon down.')
        self.play(FadeIn(card[0]), Indicate(self.parts['w1'], color=W1_COLOR), run_time=1.)
        self.wait(1.6)
        self.say('w₂ pushes into the hill. The hill pushes right back, so w₂ never moves the wagon.')
        self.play(FadeIn(card[1]), Indicate(self.parts['w2'], color=W2_COLOR), run_time=1.)
        self.wait(1.8)
        self.say('To hold the wagon still, we only have to cancel w₁. How long is it?')
        self.play(FadeIn(card[2]), run_time=.8)
        self.wait(2.)
        self.mark('pieces')

    def shadow(self):
        self.say('w₁ is w’s shadow on the ramp: the projection of w onto the ramp’s direction.')
        self.play(Indicate(self.parts['w1'], color=W1_COLOR), run_time=1.)
        self.wait(2.)
        self.mark('shadow')
        self.play(FadeOut(self.card), run_time=.6)

    def ramp_vector(self):
        self.answer_b = make_answer_b()
        self.say('To project, we need a vector r pointing up the ramp.')
        self.show('r', run_time=1., how=GrowArrow)
        self.show('r_label', run_time=.4)
        self.wait(.8)
        self.say('Its length doesn’t matter; last clip, v’s size never moved the shadow. Only its direction does.')
        self.wait(2.4)
        self.say('So make r a unit vector at 20°: cos 20° across, sin 20° up, like clip two’s unit circle.')
        self.show('r_legs', run_time=1.)
        self.play(Write(self.answer_b), run_time=1.4)
        self.wait(2.)
        self.mark('ramp_vector')
        self.hide('r_legs', run_time=.5)

    def project(self):
        proj, unit, dot, value, result, length = self.work = make_projection_work()
        self.say('Now the projection formula from clip three.')
        self.play(Write(proj), run_time=1.4)
        self.wait(1.)
        self.say('r has length 1, so the bottom is 1 and drops out.')
        self.play(Write(unit), run_time=1.4)
        self.wait(1.)
        self.say('Dot w with r. The 0 wipes out the cosine; only the sine survives.')
        self.play(Write(dot), run_time=1.3)
        self.wait(.8)
        self.play(Write(value), run_time=1.1)
        self.wait(1.)
        self.say('So w₁ is r times −34.20.')
        self.play(Write(result), run_time=1.1)
        self.wait(1.)
        self.mark('projection')

    def minus_sign(self):
        result, length = self.work[4], self.work[5]
        self.say('Why negative? r points up the hill, and w₁ points the opposite way: down the hill.')
        self.play(
            Indicate(result[2], color=PAPER_GOLD_STROKE),
            Indicate(self.parts['r'], color=R_COLOR),
            run_time=1.,
        )
        self.play(Indicate(self.parts['w1'], color=W1_COLOR), run_time=1.)
        self.wait(1.2)
        self.say('The size is what we need: w₁ pulls about 34.20 lb down the hill.')
        self.play(Write(length), run_time=1.3)
        self.wait(2.2)
        self.mark('length')

    def answer(self):
        words, force = make_answer()
        self.say('To keep the wagon still, push back just as hard the other way: up the hill.')
        self.show('f', run_time=1.1, how=GrowArrow)
        self.show('f_label', run_time=.5)
        self.wait(1.)
        self.play(FadeOut(self.work), run_time=.6)
        self.play(FadeIn(words), run_time=1.)
        self.play(Write(force), run_time=1.)
        box = SurroundingRectangle(VGroup(words, force), color=PAPER_GOLD_STROKE, buff=.2)
        self.play(Create(box), Indicate(self.parts['f'], color=F_COLOR), run_time=1.)
        self.wait(2.4)
        self.mark('answer')
        self.work = VGroup(words, force, box)

    def shortcut(self):
        title, work, boxed, check = make_shortcut()
        setup, dot, length = work
        self.say('Every ramp problem goes the same way, so there is a shortcut.')
        self.play(FadeOut(self.work), FadeOut(self.given), FadeOut(self.answer_a), FadeOut(self.answer_b),
                  *[FadeOut(self.parts[name]) for name in self.shown], run_time=.8)
        self.play(FadeIn(title), run_time=.6)
        self.say('Weight always points straight down, and the ramp vector is always a unit vector.')
        self.play(Write(setup), run_time=1.3)
        self.wait(1.4)
        self.say('The 0 always wipes out the cosine, so the dot product is always −Weight × sin θ.')
        self.play(Write(dot), run_time=1.4)
        self.wait(1.6)
        self.say('r has length 1, so the projection’s length is just Weight × sin θ.')
        self.play(Write(length), run_time=1.2)
        self.wait(1.4)
        self.say('That is the force that keeps anything from sliding down a ramp.')
        box = SurroundingRectangle(boxed, color=PAPER_GOLD_STROKE, buff=.2)
        self.play(FadeIn(boxed), Create(box), run_time=1.2)
        self.wait(2.)
        self.say('Our wagon: 100 × sin 20° ≈ 34.2 lb, the same answer.')
        self.play(Write(check), run_time=1.2)
        self.wait(3.5)
        self.mark('shortcut')
        self.write_marks('ramp_force_marks.json')

    def construct(self):
        self.problem()
        self.weight()
        self.pieces()
        self.shadow()
        self.ramp_vector()
        self.project()
        self.minus_sign()
        self.answer()
        self.shortcut()
