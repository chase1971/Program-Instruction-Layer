"""Ray tracing: where a ray bounces is a vector projection.

A real-world use of the vector-projection series. A computer draws a 3D scene by
choosing a color for every pixel. Real light scatters everywhere and almost none of it
reaches the eye, so ray tracing runs it backward: one ray from the eye through each pixel,
followed until it hits a surface. The hit point knows its color and its normal n. For a
shiny surface the ray bounces, and the bounce is a projection: split the incoming d into a
part along n and a part along the surface, reverse the part along n, keep the rest.
    r = d - 2 proj_n d

Verified numbers (the hit point sits on the sphere at 45 degrees, so n is <-1, 1>):
    d = <5, -1>,  n = <-1, 1>,  d.n = -6,  ||n||^2 = 2
    proj_n d = (-6/2) <-1, 1> = <3, -3>,  d - proj = <2, 2>  (perpendicular to n)
    r = d - 2 proj_n d = <5, -1> - <6, -6> = <-1, 5>,  ||r||^2 = ||d||^2 = 26,  r.n = 6
The lamp sits along r from the hit point, so the bounced ray lands on it: a highlight.
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
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Scene,
    Square,
    SurroundingRectangle,
    VGroup,
    Write,
    config,
)

from math_notation import NEG, hanging_fraction, mathtex
from scene_layout import CENTER, WORK, fit_into
from scene_style import (
    PAPER, PAPER_BLUE, PAPER_GOLD, PAPER_INK, PAPER_MUTED, PAPER_RED, Narrated, label,
)

config.background_color = PAPER

D_COLOR = PAPER_BLUE       # the incoming ray
N_COLOR = PAPER_GOLD       # the normal
PROJ_COLOR = '#AD1457'     # the shadow of d on the normal line, as in the earlier clips
R_COLOR = '#2E7D32'        # the reflected ray
SKY = '#E3F2FD'

# --- the scene, side view ------------------------------------------------------------
SPHERE_C = np.array([.8, -1.2, 0.])
SPHERE_R = 1.3
FLOOR_Y = SPHERE_C[1] - SPHERE_R
FLOOR_L, FLOOR_R = -6.6, 6.6
SKY_TOP = 2.35
N_HAT = np.array([-1., 1., 0.]) / math.sqrt(2)      # normal at the hit point
T_HAT = np.array([1., 1., 0.]) / math.sqrt(2)       # along the surface there
HIT = SPHERE_C + SPHERE_R * N_HAT
EYE = HIT + np.array([-6., 1.2, 0.])
LAMP = HIT + .44 * np.array([-1., 5., 0.])          # straight along the bounce
SCREEN_X = -4.6
PIXELS = 9
PIXEL_PITCH = .4

# --- the vectors ---------------------------------------------------------------------
D_VEC = np.array([5., -1., 0.])
N_VEC = np.array([-1., 1., 0.])
PROJ_VEC = np.array([3., -3., 0.])
R_VEC = np.array([-1., 5., 0.])

# --- the close-up --------------------------------------------------------------------
SC = .5                                              # screen units per unit of vector
PC = np.array([-3.8, -.3, 0.])                       # the hit point, zoomed in


def num(n):
    return (NEG + str(abs(n))) if n < 0 else str(n)


def vec(a, b):
    return r'\langle ' + num(a) + r',\,' + num(b) + r'\rangle'


# --- tracing -------------------------------------------------------------------------
def first_hit(origin, u, sky_x=FLOOR_R):
    """Where a ray from origin along unit u first lands: (point, 'sphere' | 'floor' | 'sky')."""
    best, kind = math.inf, 'sky'
    oc = origin - SPHERE_C
    b = float(np.dot(oc, u))
    disc = b * b - float(np.dot(oc, oc)) + SPHERE_R ** 2
    if disc > 0:
        t = -b - math.sqrt(disc)
        if t > 1e-6:
            best, kind = t, 'sphere'
    if u[1] < -1e-9:
        t = (FLOOR_Y - origin[1]) / u[1]
        if 1e-6 < t < best and FLOOR_L <= origin[0] + t * u[0] <= FLOOR_R:
            best, kind = t, 'floor'
    if kind == 'sky':
        reach = [(sky_x - origin[0]) / u[0] if u[0] > 1e-9 else 12.]
        if u[1] > 1e-9:
            reach.append((SKY_TOP - origin[1]) / u[1])  # a ray into the sky stops short of the caption band
        best = min(reach)
    return origin + best * u, kind


def shade(point, kind):
    """Pixel color: the surface's own color, lit by how much it faces the lamp (n . L)."""
    if kind == 'sky':
        return SKY
    normal = (point - SPHERE_C) / SPHERE_R if kind == 'sphere' else np.array([0., 1., 0.])
    to_lamp = LAMP - point
    light = max(0., float(np.dot(normal, to_lamp / np.linalg.norm(to_lamp))))
    dark, bright = ((np.array([13, 43, 82]), np.array([144, 202, 249])) if kind == 'sphere'
                    else (np.array([71, 85, 105]), np.array([203, 213, 225])))
    rgb = dark + light * (bright - dark)
    return '#%02X%02X%02X' % tuple(int(v) for v in rgb)


def unit(v):
    return v / np.linalg.norm(v)


def arrow(start, end, color, width=6):
    return Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=.22,
                 max_tip_length_to_length_ratio=.3, max_stroke_width_to_length_ratio=20)


def tex(symbol, color, scale=.75):
    return MathTex(symbol, color=color).scale(scale)


# --- work rows -----------------------------------------------------------------------
PROJ = r'\operatorname{proj}_{\mathbf n}\mathbf d'
SYMBOLS = {'d': r'\mathbf d', 'n': r'\mathbf n', 'r': r'\mathbf r', 'proj': PROJ}
COLORS = {'d': D_COLOR, 'n': N_COLOR, 'r': R_COLOR, 'proj': PROJ_COLOR}


def m(*pieces):
    row = mathtex(*[SYMBOLS.get(p, p) for p in pieces], color=PAPER_INK).scale(.72)
    for part, piece in zip(row, pieces):
        if piece in COLORS:
            part.set_color(COLORS[piece])
    return row


# The fraction row is taller than the rest, so it gets more room above and below.
ROW_Y = [.8, .2, -.5, -1.3, -2.0, -2.6, -3.2]


def place_row(row, index, under=None, at=0):
    """Pin a row to the work column; a continuation row sits under piece `at` of `under`."""
    row.move_to([WORK.left + .1, ROW_Y[index], 0], aligned_edge=LEFT)
    if under is not None:
        row.shift(RIGHT * (under[at].get_x() - row[0].get_x()))
    return row


class RayTracingReflection(Narrated, Scene):
    caption_color = PAPER_MUTED

    # ---------------------------------------------------------------- scene pieces
    def build_scene(self):
        floor = Line([FLOOR_L, FLOOR_Y, 0], [FLOOR_R, FLOOR_Y, 0], color=PAPER_MUTED, stroke_width=4)
        sphere = Circle(radius=SPHERE_R, color=PAPER_BLUE, stroke_width=4, fill_color='#BBDEFB',
                        fill_opacity=.45).move_to(SPHERE_C)
        lamp = VGroup(Dot(LAMP, radius=.15, color=PAPER_GOLD), *[
            Line(LAMP + .24 * u, LAMP + .4 * u, color=PAPER_GOLD, stroke_width=3)
            for u in (np.array([math.cos(a), math.sin(a), 0.])
                      for a in np.linspace(0, 2 * math.pi, 9)[:-1])])
        eye = VGroup(Circle(radius=.24, color=PAPER_INK, stroke_width=3).move_to(EYE),
                     Dot(EYE + .06 * RIGHT, radius=.08, color=PAPER_INK))
        hit_y = EYE[1] + (HIT[1] - EYE[1]) * (SCREEN_X - EYE[0]) / (HIT[0] - EYE[0])
        self.pixel_centers = [np.array([SCREEN_X, hit_y + PIXEL_PITCH * (k - PIXELS // 2), 0.])
                              for k in range(PIXELS)]
        pixels = VGroup(*[Square(side_length=.34, color=PAPER_MUTED, stroke_width=2).move_to(c)
                          for c in self.pixel_centers])
        words = VGroup(
            label('eye', 20, PAPER_MUTED).next_to(eye, UP, buff=.15),
            label('screen', 20, PAPER_MUTED).next_to(pixels, UP, buff=.12),
            label('light', 20, PAPER_MUTED).next_to(lamp, UP, buff=.08),
        )
        self.floor, self.sphere, self.lamp, self.eye, self.pixels, self.words = (
            floor, sphere, lamp, eye, pixels, words)
        self.ov = [floor, sphere, lamp, eye, pixels, words]

    def trace(self):
        """One ray per pixel: line, hit point, hit kind, pixel color."""
        self.rays, self.dots, self.colors = [], [], []
        for c in self.pixel_centers:
            u = unit(c - EYE)
            end, kind = first_hit(EYE, u)
            self.rays.append(Line(EYE, end, color=PAPER_BLUE, stroke_width=2.5))
            self.dots.append(Dot(end, radius=.06, color=PAPER_INK) if kind != 'sky' else None)
            self.colors.append(shade(end, kind))
        self.center = PIXELS // 2

    # ---------------------------------------------------------------- beats
    def intro(self):
        self.say('A computer draws a 3D scene by picking a color for every pixel.')
        self.build_scene()
        self.play(FadeIn(self.floor), FadeIn(self.sphere), FadeIn(self.lamp), FadeIn(self.eye),
                  FadeIn(self.pixels), FadeIn(self.words), run_time=1.6)
        self.wait(1.6)
        self.mark('scene')

    def real_light(self):
        self.say('Real light leaves the lamp and scatters in every direction.')
        to_hit = math.degrees(math.atan2(HIT[0] - LAMP[0], LAMP[1] - HIT[1]))
        self.fan = []
        for a in (-48, -30, -12, to_hit, 30, 48):
            u = np.array([math.sin(math.radians(a)), -math.cos(math.radians(a)), 0.])
            end, _ = first_hit(LAMP + .4 * u, u)
            self.fan.append(Line(LAMP + .4 * u, end, color=PAPER_GOLD, stroke_width=2.5))
        self.play(LaggedStart(*[Create(r) for r in self.fan], lag_ratio=.15), run_time=2.)
        self.wait(1.)
        self.say('Only a sliver of it bounces into the eye. Simulating all of it is hopeless.')
        bounce = Line(HIT, EYE, color=PAPER_GOLD, stroke_width=5)
        others = [r for i, r in enumerate(self.fan) if i != 3]
        self.play(*[r.animate.set_stroke(opacity=.22) for r in others],
                  self.fan[3].animate.set_stroke(width=5), run_time=.8)
        self.play(Create(bounce), run_time=1.)
        self.wait(1.6)
        self.mark('real_light')
        self.say('So the computer runs it backward: from the eye, through each pixel.')
        self.play(FadeOut(*self.fan), FadeOut(bounce), run_time=.8)
        self.wait(.8)

    def backward(self):
        self.trace()
        self.say('It shoots one ray through each pixel and follows it until it hits something.')
        self.play(LaggedStart(*[Create(r) for r in self.rays], lag_ratio=.18), run_time=3.)
        dots = [d for d in self.dots if d is not None]
        self.play(*[FadeIn(d) for d in dots], run_time=.6)
        self.ov += self.rays + dots
        self.wait(1.6)
        self.mark('rays')

    def shade_pixels(self):
        self.say('Each pixel gets the color of what its ray hit, brighter where that spot faces the lamp.')
        self.play(LaggedStart(*[px.animate.set_fill(c, opacity=1)
                                for px, c in zip(self.pixels, self.colors)], lag_ratio=.15),
                  run_time=2.4)
        self.wait(2.)
        self.mark('pixels')

    def normal(self):
        self.say('At a hit point, we know what the surface is made of and which way it faces.')
        keep = self.center
        self.play(*[r.animate.set_stroke(opacity=.14) for i, r in enumerate(self.rays) if i != keep],
                  self.rays[keep].animate.set_stroke(width=5), run_time=.8)
        self.n_arrow = arrow(HIT, HIT + 1.05 * N_HAT, N_COLOR, width=7).set_z_index(2)
        self.n_label = tex(r'\mathbf n', N_COLOR).move_to(HIT + 1.05 * N_HAT + .32 * N_HAT + .12 * LEFT)
        self.tangent = DashedLine(HIT - .8 * T_HAT, HIT + .8 * T_HAT, color=PAPER_INK, stroke_width=2.5,
                                  dash_length=.1)
        self.ov += [self.n_arrow, self.n_label, self.tangent]
        self.play(Create(self.tangent), run_time=.7)
        self.wait(.5)
        self.say('The direction straight out of the surface is the normal, n.')
        self.play(GrowArrow(self.n_arrow), FadeIn(self.n_label), run_time=1.)
        self.wait(2.)
        self.mark('normal')

    def zoom(self):
        self.say('For a shiny surface the ray bounces. To find where, zoom in on the hit point.')
        ring = Circle(radius=.5, color=PAPER_RED, stroke_width=4).move_to(HIT)
        self.play(Create(ring), run_time=.9)
        self.wait(.8)
        self.ov.append(ring)
        self.play(FadeOut(*self.ov), run_time=.9)
        a, b = PC - 2.5 * T_HAT, PC + 2.5 * T_HAT
        back = Polygon(a, b, b - 1.5 * N_HAT, a - 1.5 * N_HAT, color=PAPER_MUTED, stroke_width=0,
                       fill_color='#E2E8F0', fill_opacity=.85).set_z_index(-3)
        self.surface = VGroup(back, Line(a, b, color=PAPER_INK, stroke_width=7).set_z_index(0),
                              label('surface', 20, PAPER_MUTED).move_to(a + .1 * DOWN + .2 * LEFT + .15 * DOWN))
        self.tail = PC - SC * D_VEC
        self.d_ray = arrow(self.tail, PC, D_COLOR, width=7).set_z_index(1)
        self.d_label = tex(r'\mathbf d', D_COLOR).move_to((self.tail + PC) / 2 + .35 * UP)
        self.close_dot = Dot(PC, radius=.07, color=PAPER_INK).set_z_index(3)
        self.n_line = DashedLine(PC - 2.5 * N_HAT, PC, color=N_COLOR, stroke_width=2.5,
                                 dash_length=.1)
        self.n_close = arrow(PC, PC + 1.0 * N_HAT, N_COLOR, width=7).set_z_index(2)
        self.n_close_label = tex(r'\mathbf n', N_COLOR).move_to(PC + 1.0 * N_HAT + .32 * N_HAT + .1 * LEFT)
        self.play(FadeIn(self.surface), FadeIn(self.n_line), run_time=.8)
        self.say('Up close the surface looks flat: the ray d comes in, n points straight out.')
        self.play(GrowArrow(self.d_ray), FadeIn(self.d_label), GrowArrow(self.n_close),
                  FadeIn(self.n_close_label), FadeIn(self.close_dot), run_time=1.4)
        self.wait(1.8)
        self.mark('closeup')

    def bounce_math(self):
        rows = {}
        rows['dn'] = place_row(m('d', '=', vec(5, -1), r'\;\;', 'n', '=', vec(-1, 1)), 0)
        rows['dot'] = place_row(m(r'\mathbf d\cdot\mathbf n', '=', NEG + '6', r',\;\;',
                                  r'\|\mathbf n\|^{2}', '=', '2'), 1)
        rows['proj1'] = place_row(m('proj', '=', hanging_fraction('6', '2'), 'n'), 2)
        rows['proj2'] = place_row(m('=', vec(3, -3)), 3, under=rows['proj1'], at=1)
        rows['r1'] = place_row(m('r', '=', 'd', '-', '2', 'proj'), 4)
        rows['r2'] = place_row(m('=', vec(5, -1), '-', '2', vec(3, -3)), 5, under=rows['r1'], at=1)
        rows['r3'] = place_row(m('=', vec(-1, 5)), 6, under=rows['r1'], at=1)

        # 1. slide d to the hit point
        self.say('Slide d over so its tail sits at the hit point.')
        d_copy = self.d_ray.copy()
        self.play(d_copy.animate.shift(SC * D_VEC), run_time=1.6)
        self.play(Write(rows['dn']), run_time=1.4)
        self.wait(1.2)

        # 2. the shadow on the normal line is the projection
        self.say('Its shadow on the normal line is the projection of d onto n.')
        d_tip = PC + SC * D_VEC
        foot = PC + SC * PROJ_VEC
        drop = DashedLine(d_tip, foot, color=PAPER_INK, stroke_width=2.5, dash_length=.1)
        proj = arrow(PC, foot, PROJ_COLOR, width=8).set_z_index(2)
        proj_label = tex(PROJ, PROJ_COLOR, .6).move_to(foot + .5 * RIGHT + .3 * DOWN)
        self.play(Create(drop), run_time=.9)
        self.play(GrowArrow(proj), FadeIn(proj_label), run_time=1.)
        self.wait(1.)
        self.play(Write(rows['dot']), run_time=1.2)
        self.wait(1.)
        self.play(Write(rows['proj1']), run_time=1.3)
        self.play(Write(rows['proj2']), run_time=1.1)
        self.wait(1.8)
        self.mark('projection')

        # 3. the mirror reverses that part: subtract it twice
        self.say('A mirror reverses the part along n and keeps the rest, so take it away twice.')
        r_tip = PC + SC * R_VEC
        twice = arrow(d_tip, r_tip, PROJ_COLOR, width=6).set_z_index(1)
        self.play(GrowArrow(twice), run_time=1.6)
        self.wait(1.)
        self.play(Write(rows['r1']), run_time=1.3)
        self.play(Write(rows['r2']), run_time=1.3)
        self.play(Write(rows['r3']), run_time=1.1)
        self.wait(1.2)
        r_arrow = arrow(PC, r_tip, R_COLOR, width=9).set_z_index(3)
        r_label = tex(r'\mathbf r', R_COLOR).move_to(r_tip + .4 * LEFT + .15 * UP)
        self.say('The bounced ray leaves along r.')
        self.play(GrowArrow(r_arrow), FadeIn(r_label), run_time=1.2)
        box = SurroundingRectangle(rows['r3'], color=PAPER_GOLD, buff=.12)
        self.play(Create(box), run_time=.8)
        self.wait(2.4)
        self.mark('bounce')
        self.close_up = [self.surface, self.n_line, self.d_ray, self.d_label, self.close_dot,
                         self.n_close, self.n_close_label, d_copy, drop, proj, proj_label,
                         twice, r_arrow, r_label, box, *rows.values()]

    def payoff(self):
        self.say('Back in the scene, the bounced ray flies straight to the lamp.')
        self.play(FadeOut(*self.close_up), run_time=.9)
        self.play(FadeIn(*self.ov[:len(self.ov) - 1]), run_time=1.)  # everything but the zoom ring
        bounce = arrow(HIT, LAMP + .42 * unit(HIT - LAMP), R_COLOR, width=7).set_z_index(3)
        self.play(GrowArrow(bounce), run_time=1.2)
        self.say('That pixel catches the lamp: a bright highlight.')
        self.play(Indicate(self.pixels[self.center], color=PAPER_GOLD, scale_factor=1.5),
                  self.pixels[self.center].animate.set_fill('#FFF3C4', opacity=1), run_time=1.2)
        self.wait(2.2)
        self.mark('highlight')
        self.play(FadeOut(*self.ov[:len(self.ov) - 1]), FadeOut(bounce), run_time=.9)

    def closing(self):
        self.say('The projection is what turns a ray coming in into a ray going out.')
        rows = VGroup(
            label('1   Shoot a ray from the eye through every pixel.', 30, PAPER_INK),
            label('2   Find the surface it hits, and the normal n there.', 30, PAPER_INK),
            mathtex(r'\text{3}\;\;\text{Bounce it: }', r'\mathbf r', '=', r'\mathbf d', '-', '2',
                    PROJ, color=PAPER_INK).scale(.95),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.55)
        rows[2][1].set_color(R_COLOR)
        rows[2][3].set_color(D_COLOR)
        rows[2][6].set_color(PROJ_COLOR)
        fit_into(rows, CENTER)
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=.6), run_time=2.4)
        self.wait(3.6)
        self.mark('closing')

    def construct(self):
        self.intro()
        self.real_light()
        self.backward()
        self.shade_pixels()
        self.normal()
        self.zoom()
        self.bounce_math()
        self.payoff()
        self.closing()
        self.write_marks('ray_tracing_reflection_marks.json')
