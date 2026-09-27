"""Explain vector projection as the shadow of one force onto another.

The scene uses the 8 N and 22 N force problem from Chase's reference image.
It first establishes that the 8 N vector supplies a direction, then shines
perpendicular light across the 22 N vector to reveal its 14.14 N projection.
"""

import math

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Scene,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
    config,
)

from scene_style import BLUE, GOLD, INK, MUTED, NAVY, Narrated, label

config.background_color = NAVY

ANGLE_DEGREES = 50
REFERENCE_FORCE = 8
PROJECTED_FORCE = 22
PROJECTION_MAGNITUDE = PROJECTED_FORCE * math.cos(math.radians(ANGLE_DEGREES))

ORIGIN = [-4.6, -1.55, 0]
FORCE_SCALE = 0.2
U_LENGTH = PROJECTED_FORCE * FORCE_SCALE
V_LENGTH = REFERENCE_FORCE * FORCE_SCALE
ANGLE_RADIANS = math.radians(ANGLE_DEGREES)
U_TIP = [
    ORIGIN[0] + U_LENGTH * math.cos(ANGLE_RADIANS),
    ORIGIN[1] + U_LENGTH * math.sin(ANGLE_RADIANS),
    0,
]
PROJECTION_TIP = [U_TIP[0], ORIGIN[1], 0]


def make_force_diagram():
    """Return the two force arrows and their labels."""
    v_tip = [ORIGIN[0] + V_LENGTH, ORIGIN[1], 0]
    v_arrow = Arrow(
        ORIGIN, v_tip, buff=0, color='#E97B78', stroke_width=7,
        max_tip_length_to_length_ratio=.18,
    )
    u_arrow = Arrow(
        ORIGIN, U_TIP, buff=0, color=BLUE, stroke_width=7,
        max_tip_length_to_length_ratio=.09,
    )
    origin_dot = Line(ORIGIN, ORIGIN, color=INK, stroke_width=12)
    v_label = MathTex(r'\mathbf v', r'=8\text{ N}', color='#E97B78').scale(.72)
    v_label.next_to(v_arrow, DOWN, buff=.18)
    u_label = MathTex(r'\mathbf u', r'=22\text{ N}', color=BLUE).scale(.72)
    u_label.next_to(u_arrow.get_center(), LEFT, buff=.22)
    return VGroup(v_arrow, u_arrow, origin_dot, v_label, u_label), v_arrow, u_arrow


def make_angle_marker():
    """Build a compact 50-degree marker at the common tail."""
    radius = .75
    start = [ORIGIN[0] + radius, ORIGIN[1], 0]
    middle = [
        ORIGIN[0] + radius * math.cos(ANGLE_RADIANS / 2),
        ORIGIN[1] + radius * math.sin(ANGLE_RADIANS / 2),
        0,
    ]
    end = [
        ORIGIN[0] + radius * math.cos(ANGLE_RADIANS),
        ORIGIN[1] + radius * math.sin(ANGLE_RADIANS),
        0,
    ]
    arc = Line(start, middle, color=INK, stroke_width=2)
    arc.append_points(Line(middle, end).get_points())
    angle_label = MathTex(r'50^\circ', color=INK).scale(.55)
    angle_label.move_to([ORIGIN[0] + 1.03, ORIGIN[1] + .47, 0])
    return VGroup(arc, angle_label)


def make_light_rays():
    """Create vertical rays that cast u's shadow onto v's direction."""
    rays = VGroup()
    for proportion in (.18, .34, .50, .66, .82, 1.0):
        point = [
            ORIGIN[0] + proportion * (U_TIP[0] - ORIGIN[0]),
            ORIGIN[1] + proportion * (U_TIP[1] - ORIGIN[1]),
            0,
        ]
        ray_start = [point[0], point[1] + 1.0, 0]
        ray_end = [point[0], ORIGIN[1] + .04, 0]
        rays.add(
            Arrow(
                ray_start, ray_end, buff=0, color=GOLD, stroke_width=2.5,
                max_tip_length_to_length_ratio=.08,
            )
        )
    light = VGroup(
        Polygon(
            [-.32, .0, 0], [.32, .0, 0], [.18, -.28, 0], [-.18, -.28, 0],
            color=GOLD, fill_color=GOLD, fill_opacity=.2,
        ),
        Text('LIGHT', font='Segoe UI', font_size=18, color=GOLD).shift(UP * .15),
    ).move_to([3.8, 2.2, 0])
    return rays, light


def make_projection():
    """Create the shadow vector and perpendicular drop line."""
    projection = Arrow(
        ORIGIN, PROJECTION_TIP, buff=0, color=GOLD, stroke_width=9,
        max_tip_length_to_length_ratio=.12,
    )
    drop = DashedLine(U_TIP, PROJECTION_TIP, color=MUTED, dash_length=.12)
    right_angle = VGroup(
        Line(
            [PROJECTION_TIP[0] - .22, PROJECTION_TIP[1], 0],
            [PROJECTION_TIP[0] - .22, PROJECTION_TIP[1] + .22, 0],
            color=MUTED,
        ),
        Line(
            [PROJECTION_TIP[0] - .22, PROJECTION_TIP[1] + .22, 0],
            [PROJECTION_TIP[0], PROJECTION_TIP[1] + .22, 0],
            color=MUTED,
        ),
    )
    projection_label = MathTex(
        r'\operatorname{proj}_{\mathbf v}\mathbf u', color=GOLD,
    ).scale(.65)
    projection_label.next_to(projection, UP, buff=.12).shift(RIGHT * .85)
    return projection, drop, right_angle, projection_label


def make_formula():
    """Build the symbolic and numerical projection calculation."""
    heading = label('LENGTH OF THE SHADOW', 20, GOLD)
    symbolic = MathTex(
        r'\left\|\operatorname{proj}_{\mathbf v}\mathbf u\right\|',
        r'=',
        r'\|\mathbf u\|\cos(\theta)',
        color=INK,
    ).scale(.7)
    numeric = MathTex(
        r'=22\cos(50^\circ)', color=INK,
    ).scale(.82)
    result = MathTex(
        rf'\approx {PROJECTION_MAGNITUDE:.2f}\text{{ N}}', color=GOLD,
    ).scale(.95)
    formula = VGroup(heading, symbolic, numeric, result).arrange(
        DOWN, buff=.25, aligned_edge=LEFT,
    )
    formula.move_to([3.25, -.1, 0])
    return formula, result


class VectorProjectionForce(Narrated, Scene):
    """Animate the force projection problem as a cast-shadow model."""

    def introduce_problem(self):
        self.say('Two forces act from the same point, separated by 50 degrees.')
        diagram, v_arrow, u_arrow = make_force_diagram()
        angle = make_angle_marker()
        self.play(
            LaggedStart(GrowArrow(v_arrow), GrowArrow(u_arrow), lag_ratio=.35),
            run_time=1.5,
        )
        labels = VGroup(*[part for part in diagram if part not in (v_arrow, u_arrow)])
        self.play(FadeIn(labels), Create(angle), run_time=.8)
        self.wait(1.2)
        return diagram, angle

    def frame_the_question(self, diagram):
        self.say('How much of the 22 N force acts in the direction of the 8 N force?')
        question = label(
            'The red vector gives us the direction we care about.', 23, INK,
        ).move_to([2.7, 1.25, 0])
        box = SurroundingRectangle(question, color='#E97B78', buff=.22)
        self.play(FadeIn(question), Create(box), run_time=.7)
        self.wait(1.4)
        self.play(FadeOut(question), FadeOut(box), run_time=.4)
        self.mark('question')
        return diagram

    def cast_shadow(self):
        self.say('Imagine light shining perpendicular to that direction.')
        rays, light = make_light_rays()
        self.play(FadeIn(light), run_time=.5)
        self.play(
            LaggedStart(*[GrowArrow(ray) for ray in rays], lag_ratio=.12),
            run_time=1.8,
        )
        self.wait(.7)

        projection, drop, right_angle, projection_label = make_projection()
        self.say("The 22 N vector's shadow is its projection onto that direction.")
        self.play(
            Create(drop),
            FadeIn(right_angle),
            GrowArrow(projection),
            run_time=1.2,
        )
        self.play(Write(projection_label), run_time=.6)
        self.wait(1.5)
        self.mark('shadow_revealed')
        self.play(FadeOut(rays), FadeOut(light), run_time=.7)
        return projection, drop, right_angle, projection_label

    def calculate_shadow(self, projection_parts):
        self.say('Cosine gives the length of this adjacent, or horizontal, part.')
        formula, result = make_formula()
        self.play(
            AnimationGroup(
                FadeIn(formula[0]),
                Write(formula[1]),
                lag_ratio=.3,
            ),
            run_time=1.2,
        )
        self.play(Write(formula[2]), run_time=.7)
        self.play(Write(result), run_time=.7)
        self.play(
            SurroundingRectangle(result, color=GOLD, buff=.16).animate.set_stroke(width=4),
            run_time=.5,
        )
        self.wait(1.5)
        self.mark('calculation')
        return formula

    def conclude(self, formula):
        self.say('About 14.14 N of the blue force acts in the red direction.')
        conclusion = VGroup(
            label('The projection is not a new force.', 24, INK),
            label(
                'It is the part of the 22 N force aligned with the chosen direction.',
                22,
                MUTED,
            ),
        ).arrange(DOWN, buff=.18)
        conclusion.move_to([1.8, -2.75, 0])
        self.play(FadeIn(conclusion), run_time=.7)
        self.wait(2.2)
        self.mark('meaning')
        self.write_marks('vector_projection_force_marks.json')

    def construct(self):
        diagram, angle = self.introduce_problem()
        self.frame_the_question(diagram)
        projection_parts = self.cast_shadow()
        formula = self.calculate_shadow(projection_parts)
        self.conclude(formula)
