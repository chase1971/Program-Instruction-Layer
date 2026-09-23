"""Related rates: draining cylinder problem. Water drains from an upright
cylindrical tank at a constant volumetric rate. Because the tank's radius
never changes with height, the water LEVEL also drops at a constant rate --
unlike the square and ladder clips, the flashes here land at perfectly even
intervals. That evenness is the whole point of the "constant dimension"
case: the cross-sectional area never changes, so dV/dt = area * dh/dt means
dh/dt has to be constant too.

Real numbers (radius 20 cm, draining 25 cm3/sec) only drop the level about
0.02 cm/sec -- too slow to watch -- so the fall here is sped up. The tank's
width never changes on screen, which is the reason the rate stays fixed too.
"""

import math

from manim import (
    Arrow, DecimalNumber, Ellipse, FadeIn, FadeOut, ManimColor, Rectangle,
    Scene, Text, ValueTracker, VGroup, always_redraw, config,
    interpolate_color, linear,
)

config.background_color = '#101C30'
INK, GOLD, BLUE, MUTED = '#F2F5FA', '#FFC66D', '#86C8FF', '#B2C0D4'
INK_C, GOLD_C = ManimColor(INK), ManimColor(GOLD)

REAL_RADIUS, REAL_DRAIN = 20, 25   # cm, cm^3/sec -- the textbook's numbers
H0, H1 = 15.0, 1.0                 # water level range shown, cm
DRAIN_TIME = 7.0                   # seconds of on-screen draining
UNIT = 0.22                        # scene units per cm of height

FLASH_DECAY = 0.14    # seconds for a whole-cm flash to fade back to resting
FLASH_GROW = 0.4      # peak font-size boost (fraction) at the moment of a flash
BASE_LEVEL_FONT = 60

TANK_LEFT, TANK_RIGHT = -4.7, -1.9
FLOOR_Y = -2.5
TANK_TOP = FLOOR_Y + H0 * UNIT + .5
TANK_MID_X = (TANK_LEFT + TANK_RIGHT) / 2
TANK_W = TANK_RIGHT - TANK_LEFT


def label(words, size=24, color=MUTED):
    return Text(words, font='Segoe UI', font_size=size, color=color)


class TankDrainRate(Scene):
    def construct(self):
        title = label('HOW FAST DOES THE WATER LEVEL DROP?', 28, INK).move_to([0, 3.35, 0])
        note = label('Draining at a constant rate \u2014 sped up here so you can watch it',
                      20).move_to([0, 2.8, 0])
        self.add(title)
        self.play(FadeIn(note), run_time=.6)
        self.wait(.3)

        tank = Rectangle(width=TANK_W, height=TANK_TOP - FLOOR_Y, color=MUTED,
                         stroke_width=2).move_to([TANK_MID_X, (FLOOR_Y + TANK_TOP) / 2, 0])
        rim = Ellipse(width=TANK_W, height=.3, color=MUTED, stroke_width=2).move_to(
            [TANK_MID_X, TANK_TOP, 0])
        radius_note = label(f'radius = {REAL_RADIUS} cm (constant)', 18, MUTED).move_to(
            [TANK_MID_X, TANK_TOP + .5, 0])

        h_tracker = ValueTracker(H0)

        def water_rect():
            h = max(h_tracker.get_value() * UNIT, .01)
            r = Rectangle(width=TANK_W, height=h, color=BLUE, fill_color=BLUE,
                         fill_opacity=.4, stroke_width=0)
            r.move_to([TANK_MID_X, FLOOR_Y + h / 2, 0])
            return r

        water = always_redraw(water_rect)

        drain_arrow = Arrow([TANK_MID_X, FLOOR_Y, 0], [TANK_MID_X, FLOOR_Y - .5, 0],
                            color=MUTED, stroke_width=3, buff=0, max_tip_length_to_length_ratio=.5)
        drain_label = label(f'{REAL_DRAIN} cm\u00b3/sec out', 18, MUTED).move_to(
            [TANK_MID_X, FLOOR_Y - .9, 0])

        level_caption = label('WATER LEVEL (cm)', 20).move_to([3.1, .0, 0])
        level_num = DecimalNumber(H0, num_decimal_places=2, font_size=BASE_LEVEL_FONT,
                                  color=INK).move_to([3.1, -.8, 0])

        last_floor = [int(H0)]
        since_flash = [999.0]

        def pulse_level(m, dt):
            h = h_tracker.get_value()
            m.set_value(h)
            floor_now = int(h)
            if floor_now != last_floor[0]:
                last_floor[0] = floor_now
                since_flash[0] = 0.0
            else:
                since_flash[0] += dt
            envelope = math.exp(-since_flash[0] / FLASH_DECAY)
            m.set_color(interpolate_color(INK_C, GOLD_C, envelope))
            m.font_size = BASE_LEVEL_FONT * (1 + FLASH_GROW * envelope)

        level_num.add_updater(pulse_level)

        self.play(FadeIn(tank), FadeIn(rim), FadeIn(radius_note), FadeIn(water),
                  FadeIn(drain_arrow), FadeIn(drain_label), FadeIn(level_caption),
                  FadeIn(level_num), run_time=.6)
        self.wait(.3)

        self.play(h_tracker.animate.set_value(H1), run_time=DRAIN_TIME, rate_func=linear)
        self.wait(.7)

        level_num.clear_updaters()
        self.play(FadeOut(VGroup(title, note, tank, rim, radius_note, water, drain_arrow,
                                 drain_label, level_caption, level_num)), run_time=.5)
