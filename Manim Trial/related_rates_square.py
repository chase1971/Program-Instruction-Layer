"""Related rates warm-up: a square's side grows at a constant rate, but its
area does not. Watch the area value tick up and flash gold every time it
crosses a whole number — the flashes land closer and closer together,
because the area's rate of change keeps climbing even though the side's
rate never does.

Real numbers from the textbook problem (3 in/min, side reaching 9 in) would
take minutes to watch, so the growth here is sped up. The side still runs
from a small value up to 9 in, matching the problem's "when the side is 9
inches" question.
"""

import math

from manim import (
    DOWN, LEFT, DecimalNumber, FadeIn, FadeOut, ManimColor, Scene, Square,
    Text, ValueTracker, VGroup, always_redraw, config, interpolate_color,
    linear,
)

config.background_color = '#101C30'
INK, GOLD, BLUE, MUTED = '#F2F5FA', '#FFC66D', '#86C8FF', '#B2C0D4'
INK_C, GOLD_C = ManimColor(INK), ManimColor(GOLD)

S0, S1 = 0.5, 9.0     # side length range, inches
GROW_TIME = 7.0       # seconds of on-screen growth
UNIT = 0.4            # scene units per inch, so a 9 in side reads as 3.6 units

FLASH_DECAY = 0.14    # seconds for a whole-number flash to fade back to resting
FLASH_GROW = 0.4      # peak font-size boost (fraction) at the moment of a flash
BASE_AREA_FONT = 60
BASE_SIDE_FONT = 44


def label(words, size=24, color=MUTED):
    return Text(words, font='Segoe UI', font_size=size, color=color)


class SquareAreaRate(Scene):
    def construct(self):
        title = label('HOW FAST DOES THE AREA GROW?', 28, INK).move_to([0, 3.35, 0])
        note = label('Side length grows at a constant rate \u2014 sped up here so you can watch it',
                      20).move_to([0, 2.8, 0])
        self.add(title)
        self.play(FadeIn(note), run_time=.6)
        self.wait(.3)

        corner = [-5.3, -2.3, 0]
        s_tracker = ValueTracker(S0)

        square = always_redraw(lambda: Square(
            side_length=max(s_tracker.get_value() * UNIT, 0.03),
            color=BLUE, fill_color=BLUE, fill_opacity=.28, stroke_width=3,
        ).move_to(corner, aligned_edge=DOWN + LEFT))

        side_caption = label('SIDE LENGTH (in)', 20).move_to([3.1, 1.35, 0])
        side_num = DecimalNumber(S0, num_decimal_places=2, font_size=BASE_SIDE_FONT,
                                  color=INK).move_to([3.1, .7, 0])
        area_caption = label('AREA (in\u00b2)', 20).move_to([3.1, -.5, 0])
        area_num = DecimalNumber(S0 ** 2, num_decimal_places=2, font_size=BASE_AREA_FONT,
                                  color=INK).move_to([3.1, -1.35, 0])

        side_num.add_updater(lambda m: m.set_value(s_tracker.get_value()))

        last_floor = [int(S0 ** 2)]
        since_flash = [999.0]

        def pulse_area(m, dt):
            area = s_tracker.get_value() ** 2
            m.set_value(area)
            floor_now = int(area)
            if floor_now != last_floor[0]:
                last_floor[0] = floor_now
                since_flash[0] = 0.0
            else:
                since_flash[0] += dt
            envelope = math.exp(-since_flash[0] / FLASH_DECAY)
            m.set_color(interpolate_color(INK_C, GOLD_C, envelope))
            m.font_size = BASE_AREA_FONT * (1 + FLASH_GROW * envelope)

        area_num.add_updater(pulse_area)

        self.play(FadeIn(square), FadeIn(side_caption), FadeIn(side_num),
                  FadeIn(area_caption), FadeIn(area_num), run_time=.6)
        self.wait(.3)

        self.play(s_tracker.animate.set_value(S1), run_time=GROW_TIME, rate_func=linear)
        self.wait(.7)

        side_num.clear_updaters()
        area_num.clear_updaters()
        self.play(FadeOut(VGroup(title, note, square, side_caption, side_num,
                                  area_caption, area_num)), run_time=.5)
