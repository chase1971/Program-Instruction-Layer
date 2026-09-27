"""Find the angle between two vectors by normalizing, then dotting.

Sequel to dot_product_directions.py: clip one ended on different vector sizes;
this clip answers that question with cos theta = (u dot v) / (||u|| ||v||), shows
that dividing by the magnitudes is normalization, connects cosine to right
triangles, and works the three textbook problems with u, v, and w.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    Scene,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
    config,
)

from scene_layout import CENTER, DIAGRAM, GAUGE, WORK, fit_into
from scene_style import BLUE, GOLD, INK, MUTED, NAVY, Narrated, label

config.background_color = NAVY

U_COLOR = BLUE
V_COLOR = '#E97B78'
W_COLOR = GOLD
ORIGIN = [-2.4, -1.1, 0]
VECTOR_SCALE = .38

METER_WIDTH = 3.4
METER_HEIGHT = .38
METER_CENTER = [3.35, 2.35, 0]

# Verified textbook values — do not recompute.
U = (2, -2)
V = (5, 8)
W = (4, 4)
U_HAT = (0.7071, -0.7071)
V_HAT = (0.5300, 0.8480)
W_HAT = (0.7071, 0.7071)


def make_axes():
    horizontal = Line(
        [ORIGIN[0] - .4, ORIGIN[1], 0],
        [ORIGIN[0] + 3.6, ORIGIN[1], 0],
        color=MUTED,
        stroke_width=2,
    )
    vertical = Line(
        [ORIGIN[0], ORIGIN[1] - .4, 0],
        [ORIGIN[0], ORIGIN[1] + 3.2, 0],
        color=MUTED,
        stroke_width=2,
    )
    start = Dot(ORIGIN, radius=.06, color=INK)
    return VGroup(horizontal, vertical, start)


def make_vector_arrow(components, color):
    tip = [
        ORIGIN[0] + VECTOR_SCALE * components[0],
        ORIGIN[1] + VECTOR_SCALE * components[1],
        0,
    ]
    return Arrow(
        ORIGIN,
        tip,
        buff=0,
        color=color,
        stroke_width=7,
        max_tip_length_to_length_ratio=.12,
    )


def vector_label(tex, arrow, color, side=RIGHT):
    tag = MathTex(tex, color=color).scale(.62)
    tag.next_to(arrow, side, buff=.14)
    return tag


def make_angle_arc(start_angle, sweep, radius=.65):
    arc = Arc(
        radius=radius,
        start_angle=start_angle,
        angle=sweep,
        arc_center=ORIGIN,
        color=MUTED,
        stroke_width=3,
    )
    return arc


def make_right_angle_at(corner_point):
    size = .38
    cx, cy = corner_point[0], corner_point[1]
    across = Line([cx, cy, 0], [cx, cy + size, 0], color=MUTED, stroke_width=3)
    over = Line([cx, cy + size, 0], [cx - size, cy + size, 0], color=MUTED, stroke_width=3)
    return VGroup(across, over)


def make_right_angle_marker():
    return make_right_angle_at(ORIGIN)


def make_right_triangle_diagram():
    """Adjacent over hypotenuse — cosine as a fraction of the hypotenuse."""
    corner_point = [-1.0, -1.0, 0]
    base = Line(corner_point, [1.2, -1.0, 0], color=INK, stroke_width=4)
    rise = Line([1.2, -1.0, 0], [1.2, .85, 0], color=INK, stroke_width=4)
    hyp = Line(corner_point, [1.2, .85, 0], color=GOLD, stroke_width=4)
    corner = make_right_angle_at([1.2, -1.0, 0])
    adj = label('adjacent', 18, BLUE).next_to(base, DOWN, buff=.12)
    hyp_l = label('hypotenuse', 18, GOLD).next_to(hyp, LEFT, buff=.12).shift(UP * .25)
    ratio = MathTex(
        r'\cos\theta=\frac{\text{adjacent}}{\text{hypotenuse}}',
        color=GOLD,
    ).scale(.68).next_to(base, DOWN, buff=.75)
    group = VGroup(base, rise, hyp, corner, adj, hyp_l, ratio)
    return fit_into(group, DIAGRAM)


def make_meter():
    track = Rectangle(
        width=METER_WIDTH,
        height=METER_HEIGHT,
        color=MUTED,
        stroke_width=3,
    ).move_to(METER_CENTER)
    heading = label('COSINE READOUT', 17, MUTED).next_to(track, UP, buff=.14)
    low = label('opposite directions', 15, MUTED)
    low.next_to(track, DOWN, buff=.12).align_to(track, LEFT)
    high = label('same direction', 15, MUTED)
    high.next_to(track, DOWN, buff=.12).align_to(track, RIGHT)
    return VGroup(track, heading, low, high)


def make_meter_fill(fraction):
    width = max(abs(fraction) * METER_WIDTH, .05)
    fill = Rectangle(
        width=width,
        height=METER_HEIGHT - .1,
        color=GOLD if fraction >= 0 else '#E97B78',
        fill_color=GOLD if fraction >= 0 else '#E97B78',
        fill_opacity=.85,
        stroke_width=0,
    )
    left_edge = METER_CENTER[0] - METER_WIDTH / 2
    center_x = left_edge + width / 2 if fraction >= 0 else left_edge + METER_WIDTH - width / 2
    return fill.move_to([center_x, METER_CENTER[1], 0])


def make_meter_value(tex):
    value = MathTex(tex, color=GOLD).scale(.78)
    return value.move_to([METER_CENTER[0], 1.22, 0])


def make_open_question():
    setup = label('Both speeds were exactly 1 mph.', 26, MUTED)
    question = label('What happens when the vectors are different sizes?', 32, GOLD)
    card = VGroup(setup, question).arrange(DOWN, buff=.55)
    return fit_into(card, CENTER)


def make_angle_formula():
    rows = VGroup(
        MathTex(
            r'\cos\theta=\frac{\mathbf u\cdot\mathbf v}{\|\mathbf u\|\,\|\mathbf v\|}',
            color=INK,
        ).scale(.88),
        MathTex(
            r'\theta=\arccos\!\left(\frac{\mathbf u\cdot\mathbf v}{\|\mathbf u\|\,\|\mathbf v\|}\right)',
            color=GOLD,
        ).scale(.78),
    ).arrange(DOWN, buff=.38, aligned_edge=LEFT)
    return fit_into(rows, WORK)


def make_normalization_work():
    rows = VGroup(
        MathTex(
            r'\frac{\mathbf u}{\|\mathbf u\|}\cdot\frac{\mathbf v}{\|\mathbf v\|}',
            r'=\hat{\mathbf u}\cdot\hat{\mathbf v}',
            r'=\cos\theta',
            color=INK,
        ).scale(.78),
        MathTex(
            r'\text{Normalize both vectors, then dot them.}',
            color=MUTED,
        ).scale(.55),
    ).arrange(DOWN, buff=.35, aligned_edge=LEFT)
    rows[0][2].set_color(GOLD)
    return fit_into(rows, WORK)


def make_standardize_note():
    rows = VGroup(
        label('Dividing by the magnitudes standardizes the vectors.', 22, INK),
        label('The result reads as direction alone — a percentage, not a size.', 20, MUTED),
        MathTex(
            r'\hat{\mathbf u}\cdot\hat{\mathbf v}\in[-1,1]',
            color=GOLD,
        ).scale(.85),
    ).arrange(DOWN, buff=.32)
    return fit_into(rows, WORK)


def make_cosine_percentage():
    rows = VGroup(
        label('Cosine is the adjacent side', 22, INK),
        label('expressed as a fraction of the hypotenuse.', 22, GOLD),
        MathTex(r'\cos\theta=\frac{\text{adjacent}}{\text{hypotenuse}}', color=GOLD).scale(.82),
    ).arrange(DOWN, buff=.28)
    return fit_into(rows, WORK)


def given_vectors():
    return MathTex(
        r'\mathbf u=2\mathbf i-2\mathbf j,\quad'
        r'\mathbf v=5\mathbf i+8\mathbf j,\quad'
        r'\mathbf w=4\mathbf i+4\mathbf j',
        color=MUTED,
    ).scale(.62)


def make_problem_work(part, pair_tex, dot_val, mag_tex, cos_tex, theta_tex):
    header = MathTex(rf'\text{{({part}) }}{pair_tex}', color=INK).scale(.68)
    dot_line = MathTex(rf'\mathbf u\cdot\mathbf v={dot_val}', color=INK).scale(.66)
    if part == 'b':
        dot_line = MathTex(rf'\mathbf v\cdot\mathbf w={dot_val}', color=INK).scale(.66)
    if part == 'c':
        dot_line = MathTex(rf'\mathbf u\cdot\mathbf w={dot_val}', color=INK).scale(.66)
    mags = MathTex(mag_tex, color=MUTED).scale(.58)
    cosine = MathTex(cos_tex, color=INK).scale(.66)
    angle = MathTex(theta_tex, color=GOLD).scale(.72)
    rows = VGroup(header, dot_line, mags, cosine, angle)
    rows.arrange(DOWN, buff=.22, aligned_edge=LEFT)
    return fit_into(rows, WORK)


def make_unit_vector_payoff():
    rows = VGroup(
        MathTex(r'\hat{\mathbf u}=\langle0.7071,-0.7071\rangle', color=MUTED).scale(.72),
        MathTex(
            r'\hat{\mathbf v}=\langle0.5300,0.8480\rangle,\;'
            r'\hat{\mathbf w}=\langle0.7071,0.7071\rangle',
            color=MUTED,
        ).scale(.68),
        MathTex(r'\hat{\mathbf u}\cdot\hat{\mathbf v}=-0.22486', color=INK).scale(.72),
        MathTex(r'\hat{\mathbf v}\cdot\hat{\mathbf w}=0.97439', color=INK).scale(.72),
        MathTex(r'\hat{\mathbf u}\cdot\hat{\mathbf w}=0', color=INK).scale(.72),
        MathTex(
            r'\text{Each unit-vector dot product equals its }\cos\theta.',
            color=GOLD,
        ).scale(.65),
    ).arrange(DOWN, buff=.22, aligned_edge=LEFT)
    return fit_into(rows, WORK)


class AngleBetweenVectors(Narrated, Scene):
    """Teach the angle formula as normalized dot products, then work three problems."""

    pace = .95

    def open_on_question(self):
        self.hush()
        card = make_open_question()
        self.play(FadeIn(card[0]), run_time=.7)
        self.play(Write(card[1]), run_time=1.2)
        self.wait(2.2)
        self.mark('open_question')
        self.play(FadeOut(card), run_time=.6)
        return card

    def show_formula(self):
        self.say('Normalize by dividing each vector by its magnitude.')
        self.axes = make_axes()
        self.u_arrow = make_vector_arrow(U, U_COLOR)
        self.v_arrow = make_vector_arrow(V, V_COLOR)
        self.u_label = vector_label(r'\mathbf u', self.u_arrow, U_COLOR, UP)
        self.v_label = vector_label(r'\mathbf v', self.v_arrow, V_COLOR, RIGHT)
        diagram = VGroup(self.axes, self.u_arrow, self.v_arrow, self.u_label, self.v_label)
        fit_into(diagram, DIAGRAM)
        formula = make_angle_formula()
        self.play(FadeIn(self.axes), run_time=.5)
        self.play(Create(self.u_arrow), Create(self.v_arrow), run_time=1.0)
        self.play(FadeIn(self.u_label), FadeIn(self.v_label), run_time=.6)
        self.play(Write(formula[0]), run_time=1.0)
        self.play(Write(formula[1]), run_time=1.1)
        self.wait(2.0)
        self.mark('angle_formula')
        return formula

    def show_normalization(self, formula):
        self.say('That fraction is just dotting the two unit vectors.')
        work = make_normalization_work()
        self.play(FadeOut(formula), run_time=.4)
        self.play(Write(work[0]), run_time=1.2)
        self.play(FadeIn(work[1]), run_time=.7)
        self.wait(2.0)
        self.mark('unit_dot_product')
        return work

    def show_standardization(self, work):
        self.say('Standardizing lets the number express direction alone.')
        note = make_standardize_note()
        self.meter = make_meter()
        self.meter_fill = make_meter_fill(.5)
        gauge = VGroup(self.meter, self.meter_fill)
        fit_into(gauge, GAUGE)
        self.play(FadeOut(work), run_time=.4)
        self.play(FadeIn(gauge), run_time=.7)
        self.play(LaggedStart(*[FadeIn(row) for row in note], lag_ratio=.35), run_time=1.1)
        self.wait(2.0)
        self.mark('standardize')
        return note

    def show_right_triangle(self, note):
        self.say('Cosine is the adjacent side as a fraction of the hypotenuse.')
        triangle = make_right_triangle_diagram()
        caption = make_cosine_percentage()
        self.play(FadeOut(note), FadeOut(self.u_label), FadeOut(self.v_label), run_time=.5)
        self.play(Create(triangle[0]), Create(triangle[1]), Create(triangle[2]), run_time=.9)
        self.play(FadeIn(triangle[3]), FadeIn(triangle[4]), FadeIn(triangle[5]), run_time=.7)
        self.play(Write(triangle[6]), run_time=.9)
        self.play(FadeIn(caption), run_time=.7)
        self.wait(2.0)
        self.mark('right_triangle')
        return triangle, caption

    def clear_diagram_extras(self, *groups):
        self.play(*[FadeOut(g) for g in groups if g is not None], run_time=.5)

    def set_pair(self, first, second, first_comp, second_comp, first_color, second_color):
        self.play(
            FadeOut(self.u_arrow),
            FadeOut(self.v_arrow),
            run_time=.3,
        )
        a = make_vector_arrow(first_comp, first_color)
        b = make_vector_arrow(second_comp, second_color)
        la = vector_label(first, a, first_color, UP)
        lb = vector_label(second, b, second_color, RIGHT)
        group = VGroup(a, b, la, lb)
        fit_into(VGroup(self.axes, a, b, la, lb), DIAGRAM)
        self.play(Create(a), Create(b), FadeIn(la), FadeIn(lb), run_time=.9)
        return a, b, la, lb

    def show_meter(self, cos_tex, fraction):
        value = make_meter_value(cos_tex)
        fill = make_meter_fill(fraction)
        self.play(ReplacementTransform(self.meter_fill, fill), run_time=.7)
        self.meter_fill = fill
        self.play(FadeIn(value), run_time=.6)
        return value

    def trim_meter_for_problems(self):
        """Drop the end labels so the readout and given vectors fit in GAUGE."""
        if hasattr(self, '_meter_trimmed') and self._meter_trimmed:
            return
        self.play(FadeOut(self.meter[2]), FadeOut(self.meter[3]), run_time=.3)
        self._meter_trimmed = True

    def work_problem_a(self, triangle, caption):
        self.say('Part (a): u and v. A negative cosine means an obtuse angle.')
        self.clear_diagram_extras(triangle, caption)
        self.trim_meter_for_problems()
        given = given_vectors().move_to([3.35, 1.72, 0])
        self.play(FadeIn(given), run_time=.6)
        a, b, la, lb = self.set_pair(
            r'\mathbf u', r'\mathbf v', U, V, U_COLOR, V_COLOR,
        )
        work = make_problem_work(
            'a',
            r'\mathbf u\text{ and }\mathbf v',
            '-6',
            r'\|\mathbf u\|=2\sqrt2\approx2.8284,\;\|\mathbf v\|=\sqrt{89}\approx9.4340',
            r'\cos\theta=\frac{-6}{(2\sqrt2)(\sqrt{89})}=\frac{-3}{\sqrt{178}}\approx-0.22486',
            r'\theta\approx102.99^\circ',
        )
        self.play(LaggedStart(*[Write(row) for row in work], lag_ratio=.25), run_time=2.0)
        meter_val = self.show_meter(r'\cos\theta\approx-0.22486', -.22486)
        self.wait(2.0)
        self.mark('problem_a')
        return VGroup(given, a, b, la, lb, work, meter_val)

    def work_problem_b(self, prior):
        self.say('Part (b): v and w — almost the same direction.')
        self.play(FadeOut(prior), run_time=.5)
        a, b, la, lb = self.set_pair(
            r'\mathbf v', r'\mathbf w', V, W, V_COLOR, W_COLOR,
        )
        work = make_problem_work(
            'b',
            r'\mathbf v\text{ and }\mathbf w',
            '52',
            r'\|\mathbf v\|=\sqrt{89}\approx9.4340,\;\|\mathbf w\|=4\sqrt2\approx5.6569',
            r'\cos\theta=\frac{52}{(\sqrt{89})(4\sqrt2)}=\frac{13}{\sqrt{178}}\approx0.97439',
            r'\theta\approx12.99^\circ',
        )
        self.play(LaggedStart(*[Write(row) for row in work], lag_ratio=.25), run_time=2.0)
        meter_val = self.show_meter(r'\cos\theta\approx0.97439', .97439)
        self.wait(2.0)
        self.mark('problem_b')
        return VGroup(a, b, la, lb, work, meter_val)

    def work_problem_c(self, prior):
        self.say('Part (c): u and w share nothing — perpendicular directions.')
        self.play(FadeOut(prior), run_time=.5)
        a, b, la, lb = self.set_pair(
            r'\mathbf u', r'\mathbf w', U, W, U_COLOR, W_COLOR,
        )
        corner = make_right_angle_marker()
        fit_into(VGroup(self.axes, a, b, la, lb, corner), DIAGRAM)
        self.play(Create(corner[0]), Create(corner[1]), run_time=.6)
        self.wait(1.2)
        self.say('Now let the arithmetic confirm the right angle.')
        work = make_problem_work(
            'c',
            r'\mathbf u\text{ and }\mathbf w',
            '0',
            r'\|\mathbf u\|=2\sqrt2,\;\|\mathbf w\|=4\sqrt2',
            r'\cos\theta=0',
            r'\theta=90^\circ',
        )
        self.play(LaggedStart(*[Write(row) for row in work], lag_ratio=.25), run_time=1.8)
        meter_val = self.show_meter(r'\cos\theta=0', 0)
        self.wait(2.0)
        self.mark('problem_c')
        return VGroup(a, b, la, lb, corner, work, meter_val)

    def unit_vector_payoff(self, prior):
        self.say('Unit-vector dot products reproduce those cosines exactly.')
        self.play(FadeOut(prior), FadeOut(self.meter), FadeOut(self.meter_fill), run_time=.5)
        payoff = make_unit_vector_payoff()
        self.play(LaggedStart(*[Write(row) for row in payoff], lag_ratio=.3), run_time=2.0)
        self.wait(2.2)
        self.mark('unit_vectors_payoff')
        self.write_marks('angle_between_vectors_marks.json')

    def construct(self):
        self.open_on_question()
        formula = self.show_formula()
        work = self.show_normalization(formula)
        note = self.show_standardization(work)
        triangle, caption = self.show_right_triangle(note)
        prior = self.work_problem_a(triangle, caption)
        prior = self.work_problem_b(prior)
        prior = self.work_problem_c(prior)
        self.unit_vector_payoff(prior)
