"""Explain the dot product as projection multiplied by the other vector's length.

This companion to vector_projection_force.py keeps the same 8 N, 22 N, and
50-degree example. It turns the projected 14.14 N component into one side of
an area model and the 8 N reference magnitude into the other side, making the
dot product's 113.13 N-squared result visible.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Brace,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromCenter,
    LaggedStart,
    MathTex,
    Rectangle,
    Scene,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
    config,
)

from scene_style import BLUE, GOLD, INK, MUTED, NAVY, Narrated, label
from vector_projection_force import (
    ANGLE_DEGREES,
    PROJECTED_FORCE,
    PROJECTION_MAGNITUDE,
    REFERENCE_FORCE,
    make_angle_marker,
    make_force_diagram,
    make_projection,
)

config.background_color = NAVY

DOT_PRODUCT = PROJECTION_MAGNITUDE * REFERENCE_FORCE
AREA_WIDTH = 5.0
AREA_HEIGHT = 2.35


def make_dot_product_equation():
    """Create the conceptual and numerical dot-product equations."""
    conceptual = MathTex(
        r'\mathbf u\cdot\mathbf v',
        r'=',
        r'\left(\|\mathbf u\|\cos\theta\right)',
        r'\|\mathbf v\|',
        color=INK,
    ).scale(.95)
    conceptual.set_color_by_tex(r'\|\mathbf u\|\cos\theta', GOLD)
    conceptual.set_color_by_tex(r'\|\mathbf v\|', '#E97B78')

    numeric = MathTex(
        rf'=({PROJECTED_FORCE}\cos({ANGLE_DEGREES}^\circ))({REFERENCE_FORCE})',
        color=INK,
    ).scale(.88)
    projected = MathTex(
        rf'=({PROJECTION_MAGNITUDE:.2f}\text{{ N}})({REFERENCE_FORCE}\text{{ N}})',
        color=INK,
    ).scale(.88)
    result = MathTex(
        rf'\approx {DOT_PRODUCT:.2f}\text{{ N}}^2',
        color=GOLD,
    ).scale(1.05)
    equations = VGroup(conceptual, numeric, projected, result)
    equations.arrange(DOWN, buff=.3, aligned_edge=LEFT)
    equations.move_to([2.3, -.05, 0])
    return equations, result


def make_area_model():
    """Create a rectangle whose side lengths represent the two factors."""
    rectangle = Rectangle(
        width=AREA_WIDTH,
        height=AREA_HEIGHT,
        color=GOLD,
        fill_color=GOLD,
        fill_opacity=.12,
        stroke_width=4,
    ).move_to([0, -.55, 0])
    width_brace = Brace(rectangle, DOWN, color=GOLD)
    width_label = MathTex(
        rf'{PROJECTION_MAGNITUDE:.2f}\text{{ N}}',
        color=GOLD,
    ).scale(.72).next_to(width_brace, DOWN, buff=.08)
    height_brace = Brace(rectangle, LEFT, color='#E97B78')
    height_label = MathTex(
        rf'{REFERENCE_FORCE}\text{{ N}}',
        color='#E97B78',
    ).scale(.72).next_to(height_brace, LEFT, buff=.1)
    area_label = VGroup(
        label('ALIGNMENT WEIGHTED BY BOTH LENGTHS', 20, MUTED),
        MathTex(rf'{DOT_PRODUCT:.2f}\text{{ N}}^2', color=INK).scale(1.0),
    ).arrange(DOWN, buff=.2).move_to(rectangle)
    return rectangle, width_brace, width_label, height_brace, height_label, area_label


def make_comparison():
    """Contrast projection, dot product, and cosine similarity."""
    rows = VGroup(
        MathTex(
            r'\text{projection: }',
            rf'{PROJECTION_MAGNITUDE:.2f}\text{{ N}}',
            color=INK,
        ),
        MathTex(
            r'\text{dot product: }',
            rf'{DOT_PRODUCT:.2f}\text{{ N}}^2',
            color=INK,
        ),
        MathTex(
            r'\text{cosine similarity: }',
            rf'\cos({ANGLE_DEGREES}^\circ)\approx0.643',
            color=INK,
        ),
    ).arrange(DOWN, buff=.34, aligned_edge=LEFT)
    rows[0][1].set_color(GOLD)
    rows[1][1].set_color(BLUE)
    rows[2][1].set_color('#E97B78')
    return rows.move_to([0, -.2, 0])


class DotProductProjection(Narrated, Scene):
    """Animate the dot product as projected amount times reference length."""

    def introduce_vectors(self):
        self.say('The dot product starts by asking how much the vectors point together.')
        diagram, v_arrow, u_arrow = make_force_diagram()
        angle = make_angle_marker()
        self.play(
            LaggedStart(GrowArrow(v_arrow), GrowArrow(u_arrow), lag_ratio=.35),
            run_time=1.5,
        )
        labels = VGroup(*[part for part in diagram if part not in (v_arrow, u_arrow)])
        self.play(FadeIn(labels), Create(angle), run_time=.7)
        self.wait(1.0)
        return diagram, angle, v_arrow

    def recover_projection(self):
        self.say('First, project the 22 N force onto the 8 N force direction.')
        projection, drop, right_angle, projection_label = make_projection()
        self.play(
            Create(drop),
            FadeIn(right_angle),
            GrowArrow(projection),
            Write(projection_label),
            run_time=1.2,
        )
        value = MathTex(
            rf'{PROJECTED_FORCE}\cos({ANGLE_DEGREES}^\circ)'
            rf'\approx{PROJECTION_MAGNITUDE:.2f}\text{{ N}}',
            color=GOLD,
        ).scale(.72).move_to([2.65, .2, 0])
        self.play(Write(value), run_time=.8)
        self.wait(1.2)
        self.mark('projection')
        return VGroup(projection, drop, right_angle, projection_label, value)

    def explain_product(self, screen_objects):
        self.say('Then multiply that projected amount by the length of the other vector.')
        self.play(FadeOut(screen_objects), run_time=.7)
        equations, result = make_dot_product_equation()
        self.play(Write(equations[0]), run_time=1.1)
        self.play(Write(equations[1]), run_time=.7)
        self.play(Write(equations[2]), run_time=.7)
        self.play(Write(result), run_time=.7)
        result_box = SurroundingRectangle(result, color=GOLD, buff=.16)
        self.play(Create(result_box), run_time=.4)
        self.wait(1.3)
        self.mark('dot_product')
        return VGroup(equations, result_box)

    def show_area_model(self, equation_group):
        self.say('You can picture the multiplication as an area made from the two lengths.')
        model = make_area_model()
        self.play(FadeOut(equation_group), run_time=.6)
        self.play(GrowFromCenter(model[0]), run_time=.8)
        self.play(
            TransformFromCopy(model[0], model[1]),
            TransformFromCopy(model[0], model[3]),
            FadeIn(model[2]),
            FadeIn(model[4]),
            run_time=.8,
        )
        self.play(FadeIn(model[5]), run_time=.7)
        self.wait(1.5)
        self.mark('area_model')
        return VGroup(*model)

    def distinguish_quantities(self, area_model):
        self.say('Projection, dot product, and cosine similarity answer different questions.')
        self.play(FadeOut(area_model), run_time=.6)
        comparison = make_comparison()
        self.play(
            LaggedStart(*[FadeIn(row, shift=RIGHT * .2) for row in comparison], lag_ratio=.3),
            run_time=1.4,
        )
        self.wait(1.2)
        self.say('The dot product is an alignment score weighted by both vector lengths.')
        final_box = SurroundingRectangle(comparison[1], color=BLUE, buff=.18)
        self.play(Create(final_box), run_time=.5)
        self.wait(2.0)
        self.mark('comparison')
        self.write_marks('dot_product_projection_marks.json')

    def construct(self):
        diagram, angle, _ = self.introduce_vectors()
        projection_group = self.recover_projection()
        screen_objects = VGroup(diagram, angle, projection_group)
        equation_group = self.explain_product(screen_objects)
        area_model = self.show_area_model(equation_group)
        self.distinguish_quantities(area_model)
