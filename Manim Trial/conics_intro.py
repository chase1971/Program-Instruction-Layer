"""Conic sections, where they come from (M2412): slice a double-napped cone, get four curves.

One continuous slice, tilted a little at a time (cone slope 1, so the slice's slope is the tilt):
    plane z = k x + h through the cone x^2 + y^2 = z^2, h > 0 fixed
    k = 0        flat across            -> circle
    0 < k < 1    shallower than a side  -> ellipse
    k = 1        parallel to a side     -> parabola
    k > 1        steeper than a side    -> hyperbola (cuts both nappes: two branches)
On the cone, polar angle t around the axis: the upper nappe has r = h / (1 - k cos t) (needs
1 - k cos t > 0), the lower nappe r = -h / (1 + k cos t) (needs 1 + k cos t < 0), and z = +/- r.

PORTRAIT: 4:5 frame (portrait_frame.py). The 3D scene pins the caption and the shape name to the
screen (`caption_ready`). The beats run in Chase's order: the cone, a flat slice, a tilted slice,
parallel to the side, steeper, then a finished summary board that the clip ends on.
"""

# The frame must be set before any other project module is imported.
from portrait_frame import apply_portrait_frame

apply_portrait_frame()

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DEGREES,
    PI,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    ParametricFunction,
    Surface,
    ThreeDScene,
    ValueTracker,
    VGroup,
    VMobject,
    always_redraw,
    smooth,
)

from scene_style import (  # noqa: E402
    PAPER_BLUE,
    PAPER_GOLD,
    PAPER_INK,
    PAPER_RED,
    Narrated,
    apply_portal_paper_background,
    label,
)

apply_portal_paper_background()

ZMAX = 2.3          # how far up and down the drawn cone reaches
HEIGHT = 1.2        # the slice always passes through (0, 0, HEIGHT)
PLANE_HALF = 1.9    # half the side of the drawn slice
NAME_Y = -3.35      # the shape's name, pinned to the screen
READ_SHORT = 1.0
READ_LONG = 1.5

NAME_SIZE = 38


def cone_nappe(sign):
    """One cone (z = sign * r), translucent so the slice shows through it."""
    nappe = Surface(
        lambda u, v: np.array([v * np.cos(u), v * np.sin(u), sign * v]),
        u_range=[0, 2 * PI], v_range=[0, ZMAX], resolution=(36, 8),
        fill_color=PAPER_BLUE, fill_opacity=0.22,
        stroke_color=PAPER_BLUE, stroke_width=0.6, stroke_opacity=0.55,
        checkerboard_colors=False,
    )
    return nappe


def slice_runs(tilt_degrees):
    """The cut as runs of 3D points, one run per connected piece of the curve."""
    k = float(np.tan(np.radians(tilt_degrees)))
    runs, run = [], []

    def flush():
        nonlocal run
        if len(run) > 1:
            runs.append(run)
        run = []

    # t starts at pi (the middle of every piece) so no piece wraps past the ends of the sweep.
    for nappe in ('upper', 'lower'):
        for t in np.linspace(PI, 3 * PI, 721):
            c = np.cos(t)
            if nappe == 'upper':
                bottom = 1 - k * c
                r = HEIGHT / bottom if bottom > 1e-3 else None
                z = r
            else:
                bottom = 1 + k * c
                r = -HEIGHT / bottom if bottom < -1e-3 else None
                z = -r if r is not None else None
            if r is None or abs(z) > ZMAX:
                flush()
                continue
            run.append([r * c, r * np.sin(t), z])
        flush()
    return runs


def slice_curve(tilt_degrees):
    curve = VGroup()
    for run in slice_runs(tilt_degrees):
        piece = VMobject(stroke_color=PAPER_INK, stroke_width=7)
        piece.set_points_as_corners(run)
        curve.add(piece)
    return curve


def slice_plane(tilt_degrees):
    """The cutting plane z = x tan(tilt) + HEIGHT, drawn as a square tilted about (0, 0, HEIGHT)."""
    a = np.radians(tilt_degrees)
    return Surface(
        lambda u, v: np.array([u * np.cos(a), v, u * np.sin(a) + HEIGHT]),
        u_range=[-2.2, min(PLANE_HALF, (ZMAX + 0.1 - HEIGHT) / max(np.sin(a), 0.01))], v_range=[-PLANE_HALF, PLANE_HALF], resolution=(2, 2),
        fill_color=PAPER_GOLD, fill_opacity=0.32,
        stroke_color=PAPER_GOLD, stroke_width=1.5, checkerboard_colors=False,
    )


class ConicsIntro(Narrated, ThreeDScene):
    caption_color = PAPER_INK
    caption_wraps = True
    caption_font_size = 20
    caption_wrap_width = 5.9
    pace = 0.9

    def caption_ready(self, caption):
        self.add_fixed_in_frame_mobjects(caption)

    def mark(self, name, allow=()):
        """Record the pause point. The layout audit reads flat boxes, which a 3D scene has none of."""
        if self.marks is None:
            self.marks = []
        self.marks.append({'name': name, 'time': round(self.elapsed, 2)})

    def beat(self, mark, seconds):
        """Hold the caption long enough to read, then record the pause point."""
        self.wait(seconds)
        self.mark(mark)

    def name_tag(self, words):
        tag = label(words, font_size=NAME_SIZE, color=PAPER_INK).move_to([0, NAME_Y, 0])
        self.add_fixed_in_frame_mobjects(tag)
        return tag

    def swap_tag(self, tag, words):
        """Replace the shape's name with a new one (None to just clear it)."""
        if tag is not None:
            self.play(FadeOut(tag), run_time=0.25)
        if words is None:
            return None
        fresh = self.name_tag(words)
        self.play(FadeIn(fresh), run_time=0.35)
        return fresh

    def construct(self):
        self.set_camera_orientation(phi=76 * DEGREES, theta=-62 * DEGREES, zoom=0.95,
                                    frame_center=[0, 0, -0.35])
        upper, lower = cone_nappe(1), cone_nappe(-1)

        # 1 -- the double cone ------------------------------------------------------------
        self.say('Conics come from slicing a double cone: two cones, tip to tip.')
        self.play(Create(upper), Create(lower), run_time=2.0)
        self.mark('cone_form')
        self.move_camera(theta=-82 * DEGREES, run_time=2.5, rate_func=smooth)
        self.beat('cone_hold', READ_SHORT)

        # 2 -- slice straight across: circle ------------------------------------------------
        tilt = ValueTracker(0)
        plane = always_redraw(lambda: slice_plane(tilt.get_value()))
        curve = always_redraw(lambda: slice_curve(tilt.get_value()))
        self.say('Slice straight across, level with the floor.')
        self.play(FadeIn(plane), run_time=1.0)
        self.play(FadeIn(curve), run_time=1.2)
        self.add(plane, curve)
        tag = self.swap_tag(None, 'Circle')
        self.beat('circle', READ_LONG)

        # 3 -- tilt a little: ellipse -------------------------------------------------------
        self.say('Tilt the slice a little and the circle stretches into an ellipse.')
        tag = self.swap_tag(tag, None)
        self.play(tilt.animate.set_value(18), run_time=3.0, rate_func=smooth)
        tag = self.swap_tag(tag, 'Ellipse')
        self.beat('ellipse', READ_LONG)

        # 4 -- parallel to a side: parabola -------------------------------------------------
        self.say('Keep tilting until the slice is parallel to the side of the cone.')
        tag = self.swap_tag(tag, None)
        self.play(tilt.animate.set_value(45), run_time=2.5, rate_func=smooth)
        self.move_camera(theta=-58 * DEGREES, run_time=1.5, rate_func=smooth)
        side = Line([0, 0, 0], [ZMAX, 0, ZMAX], color=PAPER_RED, stroke_width=7)
        self.play(Create(side), run_time=0.8)
        self.play(Indicate(side, color=PAPER_RED, scale_factor=1.0), run_time=1.0)
        self.say('Now the slice never closes up. That curve is a parabola.')
        tag = self.swap_tag(tag, 'Parabola')
        self.beat('parabola', READ_LONG)
        self.play(FadeOut(side), run_time=0.4)

        # 5 -- steeper than a side: hyperbola -----------------------------------------------
        self.say('Tilt steeper than the side and the slice cuts both cones.')
        tag = self.swap_tag(tag, None)
        self.play(tilt.animate.set_value(68), run_time=3.0, rate_func=smooth)
        self.move_camera(theta=-64 * DEGREES, run_time=1.5, rate_func=smooth)
        self.wait(READ_SHORT)
        self.say('Two separate branches: a hyperbola.')
        tag = self.swap_tag(tag, 'Hyperbola')
        self.beat('hyperbola', READ_LONG)

        # 6 -- the four curves, finished board -------------------------------------------------
        self.say('Circle, ellipse, parabola, hyperbola: the four conic sections.')
        tag = self.swap_tag(tag, None)
        self.play(FadeOut(upper), FadeOut(lower), FadeOut(plane), FadeOut(curve), run_time=0.8)
        board = self.summary_board()
        self.play(FadeIn(board), run_time=1.0)
        self.beat('hold', READ_LONG)
        self.write_marks('conics_intro_marks.json')

    def summary_board(self):
        """Flat 2D picture of each curve with its name, pinned to the screen."""
        def hyperbola():
            sides = VGroup()
            for sign in (1, -1):
                sides.add(ParametricFunction(
                    lambda s, sign=sign: np.array([sign * 0.45 * np.cosh(s), 0.6 * np.sinh(s), 0]),
                    t_range=[-1.0, 1.0], color=PAPER_INK, stroke_width=6))
            return sides

        shapes = [
            ('Circle', Circle(radius=0.62, color=PAPER_INK, stroke_width=6)),
            ('Ellipse', Circle(radius=0.62, color=PAPER_INK, stroke_width=6)
             .stretch(1.5, 0).stretch(0.8, 1)),
            ('Parabola', ParametricFunction(
                lambda s: np.array([s, 0.7 * s * s - 0.6, 0]), t_range=[-1.0, 1.0],
                color=PAPER_INK, stroke_width=6)),
            ('Hyperbola', hyperbola()),
        ]
        board = VGroup()
        for index, (name, shape) in enumerate(shapes):
            cx = -1.65 if index % 2 == 0 else 1.65
            cy = 1.0 if index < 2 else -1.5
            shape.move_to([cx, cy, 0])
            tag = label(name, font_size=30, color=PAPER_BLUE).move_to([cx, cy - 1.05, 0])
            board.add(shape, tag)
        self.add_fixed_in_frame_mobjects(board)
        return board
