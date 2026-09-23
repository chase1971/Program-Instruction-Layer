"""Related rates: rocket problem. A rocket launches straight up at a
constant vertical speed while you watch from a fixed point 30 miles away.
The angle of elevation to the rocket does NOT grow at a constant rate,
though -- tan(theta) = h/30 means dtheta/dt = 120/(900+h^2), so the angle
races upward right after launch (when the rocket is still near the horizon)
and grows slower and slower as it climbs, the same decelerating family as
the cone problem. A live arc at your position traces the angle directly.

The real 4 mi/min climb would take 20 minutes to reach the far end of this
clip -- far too slow to watch -- so the flight here is sped way up. The 30
mile distance and the tan(theta) = h/30 relationship stay exact. A marker
fades in at t = 12 min, the moment the textbook question asks about.
"""

import math

from manim import (
    Angle, DecimalNumber, Dot, FadeIn, FadeOut, Line, ManimColor, Scene,
    Text, Triangle, ValueTracker, VGroup, always_redraw, config,
    interpolate_color, linear,
)

config.background_color = '#101C30'
INK, GOLD, BLUE, MUTED = '#F2F5FA', '#FFC66D', '#86C8FF', '#B2C0D4'
INK_C, GOLD_C = ManimColor(INK), ManimColor(GOLD)

OBS_X, GROUND_Y = -5.3, -2.5
UNIT = 0.06                         # scene units per mile, SAME on both axes so the
                                     # drawn angle always equals the true elevation angle
DISTANCE = 30.0                     # mi, observer's fixed horizontal distance from the pad
CLIMB_RATE = 4.0                    # mi/min, the rocket's constant vertical speed
T_ASK_MIN = 12.0                    # minutes, the moment the textbook question asks about
STORY_MIN_TOTAL = 20.0              # minutes of simulated flight shown on screen
T_TOTAL = 6.5                       # seconds of on-screen climb
MIN_PER_SEC = STORY_MIN_TOTAL / T_TOTAL       # sped-up time scale
T_ASK = T_ASK_MIN / MIN_PER_SEC               # screen-seconds at which the marker fires

LAUNCH_X = OBS_X + DISTANCE * UNIT

FLASH_DECAY = 0.14    # seconds for a whole-degree flash to fade back to resting
FLASH_GROW = 0.4      # peak font-size boost (fraction) at the moment of a flash
BASE_ANGLE_FONT = 60
BASE_TIME_FONT = 44


def label(words, size=24, color=MUTED):
    return Text(words, font='Segoe UI', font_size=size, color=color)


def story_time_of(t):
    return MIN_PER_SEC * t


def height_of(t):
    return CLIMB_RATE * story_time_of(t)


def theta_of(t):
    return math.atan(height_of(t) / DISTANCE)


class RocketAngleRate(Scene):
    def construct(self):
        title = label('HOW FAST DOES THE ANGLE OF ELEVATION CHANGE?', 26, INK).move_to([0, 3.35, 0])
        note = label('Rocket climbs at a constant rate \u2014 sped up here so you can watch it',
                      20).move_to([0, 2.8, 0])
        self.add(title)
        self.play(FadeIn(note), run_time=.6)
        self.wait(.3)

        ground = Line([OBS_X - .5, GROUND_Y, 0], [LAUNCH_X + .5, GROUND_Y, 0],
                      color=MUTED, stroke_width=2)
        horiz_ref = Line([OBS_X, GROUND_Y, 0], [LAUNCH_X, GROUND_Y, 0])  # for Angle only, not drawn
        obs_dot = Dot([OBS_X, GROUND_Y, 0], color=MUTED, radius=.06)
        obs_label = label('YOU', 16, MUTED).move_to([OBS_X, GROUND_Y - .35, 0])
        launch_dot = Dot([LAUNCH_X, GROUND_Y, 0], color=MUTED, radius=.05)
        dist_note = label(f'{DISTANCE:g} mi to launch pad (fixed)', 18, MUTED).move_to(
            [(OBS_X + LAUNCH_X) / 2, GROUND_Y + .35, 0])

        t_tracker = ValueTracker(0)

        def rocket_pos():
            return [LAUNCH_X, GROUND_Y + height_of(t_tracker.get_value()) * UNIT, 0]

        rocket = always_redraw(lambda: Triangle(
            color=INK, fill_color=INK, fill_opacity=.6, stroke_width=2,
        ).scale(.22).move_to(rocket_pos()))
        sight_line = always_redraw(lambda: Line([OBS_X, GROUND_Y, 0], rocket_pos(),
                                                color=BLUE, stroke_width=3))
        angle_arc = always_redraw(lambda: Angle(
            horiz_ref, Line([OBS_X, GROUND_Y, 0], rocket_pos()), radius=.45,
            color=GOLD, stroke_width=3))

        time_caption = label('TIME SINCE LAUNCH (min)', 20).move_to([3.1, 1.35, 0])
        time_num = DecimalNumber(0, num_decimal_places=1, font_size=BASE_TIME_FONT,
                                  color=INK).move_to([3.1, .7, 0])
        angle_caption = label('ANGLE OF ELEVATION (deg)', 20).move_to([3.1, -.5, 0])
        angle_num = DecimalNumber(0, num_decimal_places=1, font_size=BASE_ANGLE_FONT,
                                   color=INK).move_to([3.1, -1.35, 0])

        time_num.add_updater(lambda m: m.set_value(story_time_of(t_tracker.get_value())))

        last_floor = [math.floor(math.degrees(theta_of(0)))]
        since_flash = [999.0]

        def pulse_angle(m, dt):
            deg = math.degrees(theta_of(t_tracker.get_value()))
            m.set_value(deg)
            floor_now = math.floor(deg)
            if floor_now != last_floor[0]:
                last_floor[0] = floor_now
                since_flash[0] = 0.0
            else:
                since_flash[0] += dt
            envelope = math.exp(-since_flash[0] / FLASH_DECAY)
            m.set_color(interpolate_color(INK_C, GOLD_C, envelope))
            m.font_size = BASE_ANGLE_FONT * (1 + FLASH_GROW * envelope)

        angle_num.add_updater(pulse_angle)

        ask_label = label(f'{T_ASK_MIN:g} min \u2014 the question', 16, GOLD).move_to([3.1, -2.15, 0])
        ask_label.set_opacity(0)
        shown = [False]

        def reveal_ask(m, dt):
            if not shown[0] and t_tracker.get_value() >= T_ASK:
                shown[0] = True
                m.set_opacity(1)

        ask_label.add_updater(reveal_ask)

        self.play(FadeIn(ground), FadeIn(obs_dot), FadeIn(obs_label), FadeIn(launch_dot),
                  FadeIn(dist_note), FadeIn(rocket), FadeIn(sight_line), FadeIn(angle_arc),
                  FadeIn(time_caption), FadeIn(time_num), FadeIn(angle_caption), FadeIn(angle_num),
                  run_time=.6)
        self.add(ask_label)
        self.wait(.3)

        self.play(t_tracker.animate.set_value(T_TOTAL), run_time=T_TOTAL, rate_func=linear)
        self.wait(.7)

        time_num.clear_updaters()
        angle_num.clear_updaters()
        ask_label.clear_updaters()
        self.play(FadeOut(VGroup(title, note, ground, obs_dot, obs_label, launch_dot, dist_note,
                                  rocket, sight_line, angle_arc, time_caption, time_num,
                                  angle_caption, angle_num, ask_label)), run_time=.5)
