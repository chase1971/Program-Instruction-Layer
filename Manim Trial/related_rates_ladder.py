"""Related rates: ladder problem. The foot of a 13 ft ladder is pulled away
from the wall at a constant rate, but the top does not slide down the wall
at a constant rate -- watch the height value flash gold on every whole foot,
and watch those flashes land closer together as the ladder falls, because
the top's rate of descent keeps climbing even though the foot's rate never
does.

2 ft/sec is a natural speed to watch directly, so this one plays in real
time -- no sped-up disclaimer needed, unlike the square problem's 3 in/min.
A marker calls out x = 5 ft, the exact distance the textbook question asks
about.
"""

import math

from manim import (
    DOWN, DecimalNumber, Dot, FadeIn, FadeOut, Line, ManimColor, Scene, Text,
    ValueTracker, VGroup, always_redraw, config, interpolate_color, linear,
)

config.background_color = '#101C30'
INK, GOLD, BLUE, MUTED = '#F2F5FA', '#FFC66D', '#86C8FF', '#B2C0D4'
INK_C, GOLD_C = ManimColor(INK), ManimColor(GOLD)

LADDER = 13.0
X0, X_ASK, X1 = 3.0, 5.0, 12.8   # foot's distance from the wall, ft
DXDT = 2.0                       # ft/sec -- matches the textbook rate exactly
UNIT = 0.28                      # scene units per foot

FLASH_DECAY = 0.14    # seconds for a whole-foot flash to fade back to resting
FLASH_GROW = 0.4      # peak font-size boost (fraction) at the moment of a flash
BASE_HEIGHT_FONT = 60
BASE_DIST_FONT = 44

WALL_X, FLOOR_Y = -4.5, -3.4


def label(words, size=24, color=MUTED):
    return Text(words, font='Segoe UI', font_size=size, color=color)


def height_of(x):
    return math.sqrt(LADDER ** 2 - x ** 2)


class LadderSlideRate(Scene):
    def construct(self):
        title = label('HOW FAST DOES THE TOP SLIDE DOWN?', 28, INK).move_to([0, 3.35, 0])
        note = label("A 13 ft ladder's foot is pulled away from the wall at a constant 2 ft/sec",
                      20).move_to([0, 2.8, 0])
        self.add(title)
        self.play(FadeIn(note), run_time=.6)
        self.wait(.3)

        x_tracker = ValueTracker(X0)

        wall = Line([WALL_X, FLOOR_Y, 0], [WALL_X, FLOOR_Y + height_of(X0) * UNIT + .5, 0],
                    color=MUTED, stroke_width=2)
        floor = Line([WALL_X, FLOOR_Y, 0], [WALL_X + X1 * UNIT + .5, FLOOR_Y, 0],
                     color=MUTED, stroke_width=2)

        def top_point():
            return [WALL_X, FLOOR_Y + height_of(x_tracker.get_value()) * UNIT, 0]

        def foot_point():
            return [WALL_X + x_tracker.get_value() * UNIT, FLOOR_Y, 0]

        ladder = always_redraw(lambda: Line(top_point(), foot_point(), color=BLUE, stroke_width=7))
        top_dot = always_redraw(lambda: Dot(top_point(), radius=.07, color=BLUE))
        foot_dot = always_redraw(lambda: Dot(foot_point(), radius=.07, color=BLUE))

        dist_caption = label('DISTANCE FROM WALL (ft)', 20).move_to([3.1, 1.35, 0])
        dist_num = DecimalNumber(X0, num_decimal_places=2, font_size=BASE_DIST_FONT,
                                  color=INK).move_to([3.1, .7, 0])
        height_caption = label('HEIGHT ON WALL (ft)', 20).move_to([3.1, -.5, 0])
        height_num = DecimalNumber(height_of(X0), num_decimal_places=2, font_size=BASE_HEIGHT_FONT,
                                    color=INK).move_to([3.1, -1.35, 0])

        dist_num.add_updater(lambda m: m.set_value(x_tracker.get_value()))

        last_floor = [int(height_of(X0))]
        since_flash = [999.0]

        def pulse_height(m, dt):
            h = height_of(x_tracker.get_value())
            m.set_value(h)
            floor_now = int(h)
            if floor_now != last_floor[0]:
                last_floor[0] = floor_now
                since_flash[0] = 0.0
            else:
                since_flash[0] += dt
            envelope = math.exp(-since_flash[0] / FLASH_DECAY)
            m.set_color(interpolate_color(INK_C, GOLD_C, envelope))
            m.font_size = BASE_HEIGHT_FONT * (1 + FLASH_GROW * envelope)

        height_num.add_updater(pulse_height)

        self.play(FadeIn(wall), FadeIn(floor), FadeIn(ladder), FadeIn(top_dot), FadeIn(foot_dot),
                  FadeIn(dist_caption), FadeIn(dist_num), FadeIn(height_caption), FadeIn(height_num),
                  run_time=.6)
        self.wait(.3)

        self.play(x_tracker.animate.set_value(X_ASK), run_time=(X_ASK - X0) / DXDT, rate_func=linear)

        ask_tick = Line([WALL_X + X_ASK * UNIT, FLOOR_Y, 0], [WALL_X + X_ASK * UNIT, FLOOR_Y + .18, 0],
                        color=GOLD, stroke_width=3)
        ask_label = label(f'x = {X_ASK:g} ft', 18, GOLD).move_to(
            [WALL_X + X_ASK * UNIT, FLOOR_Y - .3, 0])
        self.play(FadeIn(ask_tick), FadeIn(ask_label), run_time=.4)
        self.wait(.5)

        self.play(x_tracker.animate.set_value(X1), run_time=(X1 - X_ASK) / DXDT, rate_func=linear)
        self.wait(.7)

        dist_num.clear_updaters()
        height_num.clear_updaters()
        self.play(FadeOut(VGroup(title, note, wall, floor, ladder, top_dot, foot_dot,
                                  dist_caption, dist_num, height_caption, height_num,
                                  ask_tick, ask_label)), run_time=.5)
