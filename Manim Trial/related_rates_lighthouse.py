"""Related rates: lighthouse problem. A lighthouse sits on an island 3 km
from the nearest point P on a straight shoreline, centered in the frame.
Its beam sweeps at a constant angular rate all the way from one side of P
to the other -- passing directly under the lighthouse at the midpoint --
but the point where it hits the shore does not move at a constant rate.
x = 3*tan(theta) is negative when the beam points left of P, positive when
it points right, and it blows up near either end as the beam swings toward
parallel to the shore.

The real sweep (4 rev/min = 8*pi/60 rad/sec ~ 0.42 rad/sec) would cover this
whole range in only a couple of seconds -- too fast to watch the crawl into
P and the blur back out at both ends -- so the sweep here is slowed to
roughly a third of real speed. The 3 km island distance and the
x = 3*tan(theta) relationship stay exact.
"""

import math

from manim import (
    DecimalNumber, Dot, FadeIn, FadeOut, Line, ManimColor, Scene, Text,
    Triangle, ValueTracker, VGroup, always_redraw, config, interpolate_color,
    linear,
)

config.background_color = '#101C30'
INK, GOLD, BLUE, MUTED = '#F2F5FA', '#FFC66D', '#86C8FF', '#B2C0D4'
INK_C, GOLD_C = ManimColor(INK), ManimColor(GOLD)

P_X, SHORE_Y = -2.6, -2.5
UNIT = 0.7                          # scene units per km, both axes
X_ISLAND = 3.0                      # km, island's fixed perpendicular distance to shore
X_RANGE = 5.3                       # km, sweep extent shown on EACH side of P
X_ASK = 1.0                         # km, the distance the question asks about
T_TOTAL = 6.5                       # seconds of on-screen sweep
THETA_RANGE = math.atan(X_RANGE / X_ISLAND)   # radians, half-angle each side of perpendicular
THETA0 = -THETA_RANGE
OMEGA = (2 * THETA_RANGE) / T_TOTAL           # rad/sec -- constant sweep rate used on screen

ISLAND_Y = SHORE_Y + X_ISLAND * UNIT

FLASH_DECAY = 0.14    # seconds for a whole-km flash to fade back to resting
FLASH_GROW = 0.4      # peak font-size boost (fraction) at the moment of a flash
BASE_DIST_FONT = 60
BASE_ANGLE_FONT = 44


def label(words, size=24, color=MUTED):
    return Text(words, font='Segoe UI', font_size=size, color=color)


def theta_of(t):
    return THETA0 + OMEGA * t


def x_of(t):
    return X_ISLAND * math.tan(theta_of(t))


class LighthouseSweepRate(Scene):
    def construct(self):
        title = label('HOW FAST DOES THE LIGHT MOVE ALONG SHORE?', 28, INK).move_to([0, 3.35, 0])
        note = label('Beam sweeps at a constant rate \u2014 slowed down here so you can watch it',
                      20).move_to([0, 2.8, 0])
        self.add(title)
        self.play(FadeIn(note), run_time=.6)
        self.wait(.3)

        shore = Line([P_X - X_RANGE * UNIT - .4, SHORE_Y, 0],
                     [P_X + X_RANGE * UNIT + .4, SHORE_Y, 0], color=MUTED, stroke_width=2)
        p_dot = Dot([P_X, SHORE_Y, 0], color=MUTED, radius=.06)
        p_label = label('P', 18, MUTED).move_to([P_X, SHORE_Y - .35, 0])

        island = Triangle(color=MUTED, fill_color=MUTED, fill_opacity=.35,
                           stroke_width=2).scale(.32).move_to([P_X, ISLAND_Y - .05, 0])
        lighthouse_dot = Dot([P_X, ISLAND_Y, 0], color=INK, radius=.07)
        perp_line = Line([P_X, SHORE_Y, 0], [P_X, ISLAND_Y, 0], color=MUTED, stroke_width=2)
        dims_note = label(f'{X_ISLAND:g} km to P (fixed)', 18, MUTED).move_to(
            [P_X, ISLAND_Y + .4, 0])

        t_tracker = ValueTracker(0)

        def light_pos():
            return [P_X + x_of(t_tracker.get_value()) * UNIT, SHORE_Y, 0]

        beam = always_redraw(lambda: Line([P_X, ISLAND_Y, 0], light_pos(), color=BLUE,
                                          stroke_width=3))
        light_dot = always_redraw(lambda: Dot(light_pos(), color=BLUE, radius=.09))

        angle_caption = label('ANGLE FROM PERPENDICULAR (deg)', 20).move_to([3.1, 1.35, 0])
        angle_num = DecimalNumber(math.degrees(theta_of(0)), num_decimal_places=1,
                                   font_size=BASE_ANGLE_FONT, color=BLUE,
                                   include_sign=True).move_to([3.1, .7, 0])
        dist_caption = label('DISTANCE FROM P (km)', 20).move_to([3.1, -.5, 0])
        dist_num = DecimalNumber(x_of(0), num_decimal_places=2, font_size=BASE_DIST_FONT,
                                  color=INK, include_sign=True).move_to([3.1, -1.35, 0])

        angle_num.add_updater(lambda m: m.set_value(math.degrees(theta_of(t_tracker.get_value()))))

        last_floor = [math.floor(x_of(0))]
        since_flash = [999.0]

        def pulse_dist(m, dt):
            x = x_of(t_tracker.get_value())
            m.set_value(x)
            floor_now = math.floor(x)
            if floor_now != last_floor[0]:
                last_floor[0] = floor_now
                since_flash[0] = 0.0
            else:
                since_flash[0] += dt
            envelope = math.exp(-since_flash[0] / FLASH_DECAY)
            m.set_color(interpolate_color(INK_C, GOLD_C, envelope))
            m.font_size = BASE_DIST_FONT * (1 + FLASH_GROW * envelope)

        dist_num.add_updater(pulse_dist)

        ask_x = P_X + X_ASK * UNIT
        ask_tick = Line([ask_x, SHORE_Y, 0], [ask_x, SHORE_Y + .18, 0], color=GOLD, stroke_width=3)
        ask_label = label(f'x = {X_ASK:g} km \u2014 the question', 16, GOLD).move_to(
            [ask_x, SHORE_Y - .55, 0])
        ask_group = VGroup(ask_tick, ask_label)
        ask_group.set_opacity(0)
        shown = [False]

        def reveal_ask(m, dt):
            if not shown[0] and x_of(t_tracker.get_value()) >= X_ASK:
                shown[0] = True
                m.set_opacity(1)

        ask_group.add_updater(reveal_ask)

        self.play(FadeIn(shore), FadeIn(p_dot), FadeIn(p_label), FadeIn(island),
                  FadeIn(lighthouse_dot), FadeIn(perp_line), FadeIn(dims_note),
                  FadeIn(beam), FadeIn(light_dot), FadeIn(angle_caption), FadeIn(angle_num),
                  FadeIn(dist_caption), FadeIn(dist_num), run_time=.6)
        self.add(ask_group)
        self.wait(.3)

        self.play(t_tracker.animate.set_value(T_TOTAL), run_time=T_TOTAL, rate_func=linear)
        self.wait(.7)

        angle_num.clear_updaters()
        dist_num.clear_updaters()
        ask_group.clear_updaters()
        self.play(FadeOut(VGroup(title, note, shore, p_dot, p_label, island, lighthouse_dot,
                                  perp_line, dims_note, beam, light_dot, angle_caption, angle_num,
                                  dist_caption, dist_num, ask_group)), run_time=.5)
