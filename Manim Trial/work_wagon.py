"""Work: pulling a wagon 100 ft with 50 lb on a handle at 30 degrees.

Clip seven of the vector series, after ramp_force.py -- Chase's worksheet problem 9.
First what work means: the energy a force transfers by moving something, force times
distance when the pull points exactly along the motion (50 lb for 100 ft is 5000 ft-lb).
Then the handle tilts to 30 degrees. Split F the way clips five and six split their
vectors: F1 along the ground moves the wagon, F2 straight up moves it nowhere. Only F1
does work, and F1 is F's shadow on PQ, so W = ||proj_PQ F|| ||PQ||. The shadow's length
is ||F|| cos theta (clip five), giving the worksheet's W = ||F|| ||PQ|| cos theta -- clip
two's dot product, so work is F . PQ, which the components check.

Verified numbers:
    cos 30 = sqrt(3)/2 = 0.86603,  sin 30 = 0.5
    ||proj_PQ F|| = 50 cos 30 = 25 sqrt(3) ~ 43.30 lb
    W = (50)(100) cos 30 = 2500 sqrt(3) ~ 4330.13 ft-lb   (straight pull: 5000 ft-lb)
    F = <25 sqrt(3), 25> ~ <43.30, 25>,  PQ = <100, 0>,  F . PQ ~ 4330.13
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

from angle_between_vectors import V_COLOR, heading, lerp, make_corner, rebuild
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

F_COLOR = BLUE
PQ_COLOR = V_COLOR
F1_COLOR = SHADOW  # the part along the motion is the pink shadow, as in clips three to six
F2_COLOR = GOLD
FORCE = 50.
DISTANCE = 100.
THETA = math.radians(30)
ALONG = FORCE * math.cos(THETA)  # ~43.30 lb

GROUND_Y = -1.6
P_X, Q_X = -5.35, -2.0  # the wagon's front travels from P to Q
WHEEL = .15
BODY = (1.2, .5)
PER_POUND = .04  # screen units per pound
AXLE_Y = GROUND_Y + 2 * WHEEL + BODY[1] / 2  # the handle leaves the wagon's front here
A = np.array([Q_X, AXLE_Y, 0.])  # where F is drawn once the wagon has arrived
F_TIP = A + PER_POUND * FORCE * heading(THETA)
F1_TIP = A + PER_POUND * ALONG * RIGHT

START = dict(x=P_X, phi=0.)
ARRIVED = dict(x=Q_X, phi=0.)
TILTED = dict(x=Q_X, phi=THETA)


def front(state):
    return np.array([state['x'], AXLE_Y, 0.])


def make_ground(_state):
    ground = Line([-6.75, GROUND_Y, 0], [.2, GROUND_Y, 0], color=MUTED, stroke_width=3)
    ticks = VGroup(*[Line([x, GROUND_Y - .12, 0], [x, GROUND_Y + .12, 0], color=MUTED, stroke_width=3)
                     for x in (P_X, Q_X)])
    names = VGroup(*[portal_math(name, color=INK, scale=.7).move_to([x, GROUND_Y - .42, 0])
                     for name, x in (('P', P_X), ('Q', Q_X))])
    return VGroup(ground, ticks, names).set_z_index(-2)


def make_wagon(state):
    body = Rectangle(width=BODY[0], height=BODY[1], color=INK, stroke_width=3).move_to(
        front(state) + BODY[0] / 2 * LEFT)
    wheels = VGroup(*[Circle(radius=WHEEL, color=INK, stroke_width=3).move_to(
        [state['x'] - BODY[0] / 2 + s * .42, GROUND_Y + WHEEL, 0]) for s in (-1, 1)])
    return VGroup(body, wheels).set_z_index(-1)


def make_f(state):
    start = front(state)
    return arrow(start, start + PER_POUND * FORCE * heading(state['phi']), F_COLOR).set_z_index(1)


def make_f_label(state):
    start = front(state)
    middle = start + PER_POUND * FORCE / 2 * heading(state['phi'])
    return portal_math(r'\mathbf F', r'=50\text{ lb}', color=F_COLOR).scale(.7).move_to(
        middle + .5 * heading(state['phi'] + math.pi / 2) + .15 * LEFT)


def make_angle(_state):
    arc = VGroup(*[Line(A + .55 * heading(THETA * k / 10), A + .55 * heading(THETA * (k + 1) / 10),
                        color=INK, stroke_width=2) for k in range(10)])
    mark = portal_math(r'30^\circ', color=INK).scale(.55).move_to(A + 1.0 * heading(THETA / 2))
    return VGroup(arc, mark)


def make_pq(_state):
    return arrow([P_X, GROUND_Y, 0], [Q_X, GROUND_Y, 0], PQ_COLOR, width=6)


def make_pq_label(_state):
    return portal_math(r'\|\overrightarrow{PQ}\|=100\text{ ft}', color=PQ_COLOR).scale(.65).move_to(
        [(P_X + Q_X) / 2, GROUND_Y - .45, 0])


def make_f1(_state):
    return arrow(A, F1_TIP, F1_COLOR, width=13).set_z_index(2)


def make_f2(_state):
    return arrow(F1_TIP, F_TIP, F2_COLOR)


def make_f1_label(_state):
    return portal_math(r'\mathbf F_1', color=F1_COLOR).scale(.8).move_to((A + F1_TIP) / 2 + .32 * DOWN + .2 * RIGHT)


def make_f2_label(_state):
    return portal_math(r'\mathbf F_2', color=F2_COLOR).scale(.8).move_to((F1_TIP + F_TIP) / 2 + .38 * RIGHT)


def make_corner_mark(_state):
    return make_corner(F1_TIP, LEFT, UP, .18)


# Draw order: shapes first, labels last.
PARTS = {
    'ground': make_ground, 'wagon': make_wagon, 'pq': make_pq, 'corner': make_corner_mark,
    'angle': make_angle, 'f2': make_f2, 'f1': make_f1, 'f': make_f,
    'f_label': make_f_label, 'pq_label': make_pq_label, 'f1_label': make_f1_label,
    'f2_label': make_f2_label,
}
MOVING = ('wagon', 'f', 'f_label')

PQ = r'\overrightarrow{PQ}'
PROJ = rf'\operatorname{{proj}}_{{{PQ}}}\mathbf F'
COLORS = {'F': F_COLOR, 'PQ': PQ_COLOR, '|F|': F_COLOR, '|PQ|': PQ_COLOR, 'F1': F1_COLOR,
          'F2': F2_COLOR, 'proj': F1_COLOR, '|proj|': F1_COLOR}
SYMBOLS = {'F': r'\mathbf F', 'PQ': PQ, '|F|': r'\|\mathbf F\|', '|PQ|': rf'\|{PQ}\|',
           'F1': r'\mathbf F_1', 'F2': r'\mathbf F_2', 'proj': PROJ, '|proj|': rf'\|{PROJ}\|'}


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


# The givens stay pinned top right; the work develops beneath them.
PINNED_TOP = CONTENT_TOP - .1
BELOW_PINNED = Region('BELOW_PINNED', WORK.left, WORK.right, WORK.bottom, 1.5)


def make_given():
    rows = VGroup(m('|F|', r'=50\text{ lb}', r',\;\;', r'\theta=30^\circ'),
                  m('|PQ|', r'=100\text{ ft}')).arrange(DOWN, buff=.3, aligned_edge=LEFT)
    rows[0][0].set_color(F_COLOR)
    return rows.move_to([WORK.left + .1, PINNED_TOP, 0], aligned_edge=UP + LEFT)


def settle(column):
    fit_into(column, BELOW_PINNED)
    return column.align_to([BELOW_PINNED.left + .1, 0, 0], LEFT).align_to(
        [0, BELOW_PINNED.top - .1, 0], UP)


def make_straight_work():
    rule = VGroup(label('Force along the motion:', font_size=24, color=INK),
                  label('work = force × distance', font_size=24, color=INK)
                  ).arrange(DOWN, buff=.12, aligned_edge=LEFT)
    formula = m('W', '=', '|F|', r'\,', '|PQ|')
    value = m('=', r'(50)(100)', '=', r'5000\text{ ft}\cdot\text{lb}')
    column = place(VGroup(rule, formula, value), buff=.35)
    line_up(formula, 1, value)
    return settle(column)


def make_definitions():
    """What the two pieces of the pull are, in words, each under its symbol."""
    rows = VGroup(*[VGroup(math, label(words, font_size=24, color=INK)).arrange(
        DOWN, buff=.16, aligned_edge=LEFT) for math, words in (
        (m('F1'), 'moves the wagon along: does work'),
        (m('F2'), 'lifts, but the wagon never rises: no work'),
        (m('F1', '=', 'proj'), 'F’s shadow on the direction of motion'))])
    return settle(place(rows, buff=.4))


def make_angled_work():
    formula = m('W', '=', '|proj|', r'\,', '|PQ|')
    shadow = m('|proj|', '=', r'\|\mathbf F\|\cos\theta')
    shadow_value = m('=', r'50\cos 30^\circ', r'\approx', r'43.30\text{ lb}')
    general = m('W', '=', r'\|\mathbf F\|\,\|\overrightarrow{PQ}\|\cos\theta')
    numbers = m('=', r'(50)(100)\cos 30^\circ')
    value = m('=', r'2500\sqrt3', r'\approx', r'4330.13\text{ ft}\cdot\text{lb}')
    column = place(VGroup(formula, shadow, shadow_value, general, numbers, value), buff=.3)
    line_up(shadow, 1, shadow_value)
    line_up(general, 1, numbers, value)
    return settle(column)


def make_check_work():
    intro = label('Clip two: that is a dot product, W = F · PQ.', font_size=24, color=INK)
    f = m('F', r'\approx', r'\langle 43.30,\ 25\rangle')
    pq = m('PQ', '=', r'\langle 100,\ 0\rangle')
    dot = m('F', r'\cdot', 'PQ', r'\approx', r'(43.30)(100)+(25)(0)')
    dot_value = m(r'\approx', r'4330.13')
    share = VGroup(m(r'\cos 30^\circ\approx 0.866'),
                   label('about 87% of what a level pull would do', font_size=24, color=INK)
                   ).arrange(DOWN, buff=.16, aligned_edge=LEFT)
    column = place(VGroup(intro, f, pq, dot, dot_value, share), buff=.3)
    line_up(dot, 3, dot_value)
    share.shift(DOWN * .15)
    return settle(column)


def make_answer():
    words = VGroup(*[label(line, font_size=26, color=INK) for line in (
        'Pulling the wagon 100 ft', 'with 50 lb at 30° does about', '4330 foot-pounds of work.')]
                   ).arrange(DOWN, buff=.14, aligned_edge=LEFT)
    column = place(VGroup(words, m('W', r'\approx', r'4330.13\text{ ft}\cdot\text{lb}')), buff=.4)
    return settle(column).shift(LEFT * .2 + DOWN * .3)  # room for the answer box


def make_summary():
    """What work is, and the three ways the worksheet writes it."""
    title = label('Work', font_size=30, color=GOLD)
    meaning = label('the energy a force transfers by moving something', font_size=26, color=INK)
    only = label('Only the part of the force along the motion counts.', font_size=24)
    rows = VGroup(m('W', '=', '|proj|', r'\,', '|PQ|'),
                  m('=', r'\|\mathbf F\|\,\|\overrightarrow{PQ}\|\cos\theta'),
                  m('=', 'F', r'\cdot', 'PQ'))
    place(rows, buff=.3)
    line_up(rows[0], 1, *rows[1:])
    units = label('force × distance, so the units are foot-pounds', font_size=24)
    card = VGroup(title, meaning, only, rows, units).arrange(DOWN, buff=.38)
    return fit_into(card, CENTER)


class WorkWagon(VectorPortalScene, Scene):
    caption_color = PAPER_MUTED
    """Worksheet problem 9: the work done pulling a wagon 100 ft at 30 degrees."""

    pace = .9

    def show(self, *names, run_time=.8, how=FadeIn):
        self.play(*[how(self.parts[name]) for name in names], run_time=run_time)
        self.shown.update(names)

    def morph(self, start, end, run_time=2.):
        """Rebuild the wagon and its pull from a state sliding from `start` to `end`."""
        self.play(*[rebuild(self.parts[name], lambda a, build=PARTS[name]: build(
            {key: lerp(start[key], end[key], a) for key in start})) for name in MOVING],
                  run_time=run_time)

    def meaning(self):
        self.shown = set()
        self.parts = {name: build(TILTED) for name, build in PARTS.items()}
        for name in MOVING:
            self.parts[name] = PARTS[name](START)
        self.work = make_straight_work()
        self.say('Work measures the energy a force transfers when it moves something.')
        self.show('ground', 'wagon', run_time=1.)
        self.wait(1.2)
        self.say('Pull a wagon with 50 lb, straight along the ground.')
        self.show('f', run_time=1., how=GrowArrow)
        self.show('f_label', run_time=.5)
        self.wait(.6)
        self.say('It moves from P to Q, 100 ft.')
        self.morph(START, ARRIVED, run_time=2.4)
        self.show('pq', run_time=.8, how=GrowArrow)
        self.show('pq_label', run_time=.5)
        self.wait(.8)
        self.say('When the pull points exactly along the motion, work is force times distance.')
        self.play(FadeIn(self.work[0]), run_time=.8)
        self.play(Write(self.work[1]), run_time=1.)
        self.wait(.6)
        self.play(Write(self.work[2]), run_time=1.1)
        self.wait(1.)
        self.say('Twice the pull, or twice the distance, and you have done twice the work.')
        self.wait(2.4)
        self.mark('straight_pull')

    def problem(self):
        self.given = make_given()
        self.say('Problem 9: the girl pulls with 50 lb, but the handle makes 30° with the ground.')
        self.play(FadeOut(self.work), run_time=.6)
        self.morph(ARRIVED, TILTED, run_time=1.8)
        self.show('angle', run_time=.6)
        self.play(Write(self.given), run_time=1.2)
        self.wait(1.2)
        self.say('How much work does she do moving it 100 ft? Does all 50 lb still count?')
        self.wait(2.4)
        self.mark('question')

    def pieces(self):
        self.card = card = make_definitions()
        self.say('Split F like the last two clips: one piece along the ground, one straight up.')
        self.show('f1', run_time=1., how=GrowArrow)
        self.show('f2', run_time=1., how=GrowArrow)
        self.show('corner', 'f1_label', 'f2_label', run_time=.6)
        self.wait(1.)
        self.say('F₁ points where the wagon goes. It is the part of the pull that moves it.')
        self.play(FadeIn(card[0]), Indicate(self.parts['f1'], color=F1_COLOR), run_time=1.)
        self.wait(1.6)
        self.say('F₂ tries to lift the wagon, but it never leaves the ground. F₂ does no work.')
        self.play(FadeIn(card[1]), Indicate(self.parts['f2'], color=F2_COLOR), run_time=1.)
        self.wait(1.8)
        self.say('And F₁ is F’s shadow on PQ: the projection of F onto the direction of motion.')
        self.play(FadeIn(card[2]), Indicate(self.parts['f1'], color=F1_COLOR), run_time=1.)
        self.wait(2.2)
        self.mark('pieces')
        self.play(FadeOut(card), run_time=.6)

    def solve(self):
        formula, shadow, shadow_value, general, numbers, value = self.work = make_angled_work()
        self.say('So work only counts the shadow: its length times the distance.')
        self.play(Write(formula), run_time=1.3)
        self.wait(1.)
        self.say('Clip five: the shadow’s length is ‖F‖ cos θ. Here about 43.30 lb.')
        self.play(Write(shadow), Indicate(self.parts['f1'], color=F1_COLOR), run_time=1.2)
        self.play(Write(shadow_value), run_time=1.)
        self.wait(1.4)
        self.say('Put that in, and you get the worksheet’s formula.')
        self.play(Write(general), run_time=1.2)
        self.wait(1.)
        self.say('Now the numbers: 50 lb, 100 ft, 30°.')
        self.play(Write(numbers), run_time=1.1)
        self.wait(.6)
        self.play(Write(value), run_time=1.2)
        self.wait(2.)
        self.mark('solve')

    def check(self):
        intro, f, pq, dot, dot_value, share = column = make_check_work()
        self.say('‖F‖ ‖PQ‖ cos θ is clip two’s dot product. So work is just F · PQ.')
        self.play(FadeOut(self.work), run_time=.6)
        self.play(FadeIn(intro), run_time=.8)
        self.wait(.6)
        self.say('Check it with components: F is 50 cos 30° ≈ 43.30 across and 50 sin 30° = 25 up.')
        self.play(Write(f), Indicate(self.parts['f'], color=F_COLOR), run_time=1.3)
        self.play(Write(pq), Indicate(self.parts['pq'], color=PQ_COLOR), run_time=1.)
        self.wait(.6)
        self.say('The 25 up meets the 0 in PQ and disappears. That is F₂ doing no work.')
        self.play(Write(dot), Indicate(self.parts['f2'], color=F2_COLOR), run_time=1.4)
        self.play(Write(dot_value), run_time=.8)
        self.wait(1.6)
        self.say('cos 30° is the share of the pull that moves the wagon: about 87%.')
        self.play(FadeIn(share), run_time=.9)
        self.wait(2.2)
        self.mark('check')
        self.work = column

    def answer(self):
        words, work = make_answer()
        self.say('So how much work is done moving the wagon 100 ft?')
        self.play(FadeOut(self.work), run_time=.6)
        self.play(FadeIn(words), run_time=1.)
        self.play(Write(work), run_time=1.)
        box = SurroundingRectangle(VGroup(words, work), color=PAPER_GOLD_STROKE, buff=.2)
        self.play(Create(box), Indicate(self.parts['f1'], color=F1_COLOR), run_time=1.)
        self.wait(2.4)
        self.mark('answer')
        self.work = VGroup(words, work, box)

    def summary(self):
        title, meaning, only, rows, units = make_summary()
        self.say('What work means, all in one place.')
        self.play(FadeOut(self.work), FadeOut(self.given),
                  *[FadeOut(self.parts[name]) for name in self.shown], run_time=.8)
        self.play(FadeIn(title), FadeIn(meaning), run_time=1.)
        self.wait(1.4)
        self.say('Only the part of the force along the motion does work: the projection.')
        self.play(FadeIn(only), Write(rows[0]), run_time=1.3)
        self.wait(1.6)
        self.say('Its length is ‖F‖ cos θ, which makes work a dot product.')
        self.play(Write(rows[1]), run_time=1.2)
        self.play(Write(rows[2]), run_time=1.)
        self.wait(1.6)
        self.say('Force in pounds times distance in feet: foot-pounds.')
        self.play(FadeIn(units), run_time=.8)
        self.wait(3.5)
        self.mark('summary')
        self.write_marks('work_wagon_marks.json')

    def construct(self):
        self.meaning()
        self.problem()
        self.pieces()
        self.solve()
        self.check()
        self.answer()
        self.summary()
