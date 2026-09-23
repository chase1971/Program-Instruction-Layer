"""Related rates: conical tank problem. Water pours into a downward-pointing
cone at a constant volumetric rate. Unlike the cylinder, the cone's radius
at the surface is proportional to the depth (similar triangles: r/h = R/H),
so the cross-sectional area GROWS as the water rises. That means the level's
rise rate does the opposite of the square and ladder clips: the flashes
start fast, near the narrow point, and land farther and farther apart as the
water climbs into the wider part of the cone.

A small blue arrow at the water's surface shows the current radius directly,
so the r = h/3 relationship is visible while it happens, not just implied.
A marker fades in once the water passes h = 4 cm, the depth the textbook
question asks about.

Real numbers (10 cm3/sec into a 30 cm cone with a 10 cm base radius) are
sped up 1.5x so the deceleration is easy to watch.
"""

import math

from manim import (
    Arrow, DashedLine, DecimalNumber, Ellipse, FadeIn, FadeOut, Line,
    ManimColor, Polygon, Scene, Text, ValueTracker, VGroup, always_redraw,
    config, interpolate_color, linear,
)

config.background_color = '#101C30'
INK, GOLD, BLUE, MUTED = '#F2F5FA', '#FFC66D', '#86C8FF', '#B2C0D4'
INK_C, GOLD_C = ManimColor(INK), ManimColor(GOLD)

H_FULL, R_FULL = 30.0, 10.0        # cone's real full height and base radius, cm
H0, H1 = 3.0, 10.0                 # water depth range shown, cm
H_ASK = 4.0                        # the depth the textbook question asks about
REAL_DVDT = 10.0                   # cm^3/sec -- the textbook's pour-in rate
SPEEDUP = 1.5
UNIT = 0.13                        # scene units per cm, same for height and radius

FLASH_DECAY = 0.14    # seconds for a whole-cm flash to fade back to resting
FLASH_GROW = 0.4      # peak font-size boost (fraction) at the moment of a flash
BASE_DEPTH_FONT = 60
BASE_RADIUS_FONT = 44

CONE_X = -3.6
FLOOR_Y = -3.3

Q = REAL_DVDT * SPEEDUP
V0 = math.pi * H0 ** 3 / 27
V1 = math.pi * H1 ** 3 / 27
T_TOTAL = (V1 - V0) / Q


def label(words, size=24, color=MUTED):
    return Text(words, font='Segoe UI', font_size=size, color=color)


def depth_at(t):
    volume = V0 + Q * t
    return (27 * volume / math.pi) ** (1 / 3)


def radius_of(h):
    return h * (R_FULL / H_FULL)


class ConeLevelRate(Scene):
    def construct(self):
        title = label('HOW FAST DOES THE WATER LEVEL RISE?', 28, INK).move_to([0, 3.35, 0])
        note = label('Poured in at a constant rate \u2014 sped up here so you can watch it',
                      20).move_to([0, 2.8, 0])
        self.add(title)
        self.play(FadeIn(note), run_time=.6)
        self.wait(.3)

        top_y = FLOOR_Y + H_FULL * UNIT
        half_w = R_FULL * UNIT
        apex = [CONE_X, FLOOR_Y, 0]
        cone_left = Line(apex, [CONE_X - half_w, top_y, 0], color=MUTED, stroke_width=2)
        cone_right = Line(apex, [CONE_X + half_w, top_y, 0], color=MUTED, stroke_width=2)
        rim = Ellipse(width=2 * half_w, height=.25, color=MUTED, stroke_width=2).move_to(
            [CONE_X, top_y, 0])
        dims_note = label(f'H = {H_FULL:g} cm, R = {R_FULL:g} cm (r/h = R/H stays fixed)',
                          18, MUTED).move_to([CONE_X, top_y + .45, 0])

        t_tracker = ValueTracker(0)

        def water_triangle():
            h = max(depth_at(t_tracker.get_value()), .02)
            r = radius_of(h) * UNIT
            surface_y = FLOOR_Y + h * UNIT
            return Polygon(apex, [CONE_X - r, surface_y, 0], [CONE_X + r, surface_y, 0],
                          color=BLUE, fill_color=BLUE, fill_opacity=.4, stroke_width=0)

        water = always_redraw(water_triangle)

        def radius_arrow():
            h = max(depth_at(t_tracker.get_value()), .02)
            r = radius_of(h) * UNIT
            surface_y = FLOOR_Y + h * UNIT
            return Arrow([CONE_X, surface_y, 0], [CONE_X + r, surface_y, 0], color=BLUE,
                        stroke_width=3, buff=0, max_tip_length_to_length_ratio=.35)

        r_arrow = always_redraw(radius_arrow)

        radius_caption = label('SURFACE RADIUS (cm)', 20).move_to([3.1, 1.35, 0])
        radius_num = DecimalNumber(radius_of(H0), num_decimal_places=2,
                                   font_size=BASE_RADIUS_FONT, color=BLUE).move_to([3.1, .7, 0])
        depth_caption = label('WATER DEPTH (cm)', 20).move_to([3.1, -.5, 0])
        depth_num = DecimalNumber(H0, num_decimal_places=2, font_size=BASE_DEPTH_FONT,
                                  color=INK).move_to([3.1, -1.35, 0])

        radius_num.add_updater(lambda m: m.set_value(radius_of(depth_at(t_tracker.get_value()))))

        last_floor = [int(H0)]
        since_flash = [999.0]

        def pulse_depth(m, dt):
            h = depth_at(t_tracker.get_value())
            m.set_value(h)
            floor_now = int(h)
            if floor_now != last_floor[0]:
                last_floor[0] = floor_now
                since_flash[0] = 0.0
            else:
                since_flash[0] += dt
            envelope = math.exp(-since_flash[0] / FLASH_DECAY)
            m.set_color(interpolate_color(INK_C, GOLD_C, envelope))
            m.font_size = BASE_DEPTH_FONT * (1 + FLASH_GROW * envelope)

        depth_num.add_updater(pulse_depth)

        ask_y = FLOOR_Y + H_ASK * UNIT
        ask_tick = DashedLine([CONE_X - half_w * .55, ask_y, 0], [CONE_X + half_w * .55, ask_y, 0],
                             color=GOLD, stroke_width=2)
        ask_label = label(f'h = {H_ASK:g} cm \u2014 the question', 16, GOLD).move_to(
            [CONE_X + half_w + 1.05, ask_y, 0])
        ask_group = VGroup(ask_tick, ask_label)
        ask_group.set_opacity(0)
        shown = [False]

        def reveal_ask(m, dt):
            if not shown[0] and depth_at(t_tracker.get_value()) >= H_ASK:
                shown[0] = True
                m.set_opacity(1)

        ask_group.add_updater(reveal_ask)

        self.play(FadeIn(cone_left), FadeIn(cone_right), FadeIn(rim), FadeIn(dims_note),
                  FadeIn(water), FadeIn(r_arrow), FadeIn(radius_caption), FadeIn(radius_num),
                  FadeIn(depth_caption), FadeIn(depth_num), run_time=.6)
        self.add(ask_group)
        self.wait(.3)

        self.play(t_tracker.animate.set_value(T_TOTAL), run_time=T_TOTAL, rate_func=linear)
        self.wait(.7)

        radius_num.clear_updaters()
        depth_num.clear_updaters()
        ask_group.clear_updaters()
        self.play(FadeOut(VGroup(title, note, cone_left, cone_right, rim, dims_note, water,
                                 r_arrow, radius_caption, radius_num, depth_caption, depth_num,
                                 ask_group)), run_time=.5)
