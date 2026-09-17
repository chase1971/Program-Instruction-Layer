"""Animate fraction sums as centered, single-owner equation transforms."""

from manim import FadeIn, FadeOut, MathTex, ReplacementTransform, Scene, VGroup, WHITE, config, smooth

from scene_style import Narrated

config.background_color = WHITE

INK = '#172033'
GOLD = '#A85D00'
BLUE = '#12669A'
FONT = 62
EQUATION_Y = .35


def equation(left, right=None):
    """Create one centered equation whose terms have stable, separate colors."""
    pieces = [MathTex(left, font_size=FONT, color=GOLD)]
    if right is not None:
        pieces.extend([
            MathTex('+', font_size=FONT, color=INK),
            MathTex(right, font_size=FONT, color=BLUE),
        ])
    return VGroup(*pieces).arrange(buff=.38).move_to([0, EQUATION_Y, 0])


def transition(scene, current, replacement):
    scene.play(
        ReplacementTransform(current, replacement),
        run_time=.9,
        rate_func=smooth,
    )
    scene.wait(.45)
    return replacement


class FractionAddFractions(Narrated, Scene):
    def show_whole_plus_fraction(self, whole, numerator, denominator, result, prefix):
        current = equation(str(whole), rf'\frac{{{numerator}}}{{{denominator}}}')
        self.play(FadeIn(current), run_time=.75)
        self.wait(.5)
        self.mark(f'{prefix}_problem_shown')

        current = transition(
            self,
            current,
            equation(rf'\frac{{{whole}}}{{1}}', rf'\frac{{{numerator}}}{{{denominator}}}'),
        )
        self.mark(f'{prefix}_whole_rewritten')
        current = transition(
            self,
            current,
            equation(
                rf'\frac{{{whole}\times {denominator}}}{{1\times {denominator}}}',
                rf'\frac{{{numerator}}}{{{denominator}}}',
            ),
        )
        current = transition(
            self,
            current,
            equation(
                rf'\frac{{{whole * denominator}}}{{{denominator}}}',
                rf'\frac{{{numerator}}}{{{denominator}}}',
            ),
        )
        self.mark(f'{prefix}_common_denominator')
        current = transition(
            self,
            current,
            equation(rf'\frac{{{whole * denominator}+{numerator}}}{{{denominator}}}'),
        )
        current = transition(self, current, equation(rf'\frac{{{result}}}{{{denominator}}}'))
        self.mark(f'{prefix}_summed')
        self.play(FadeOut(current), run_time=.55)
        self.wait(.3)

    def show_fraction_plus_fraction(self, n1, d1, n2, d2, result, denominator, prefix):
        left_scale = denominator // d1
        right_scale = denominator // d2
        current = equation(rf'\frac{{{n1}}}{{{d1}}}', rf'\frac{{{n2}}}{{{d2}}}')
        self.play(FadeIn(current), run_time=.75)
        self.wait(.5)
        self.mark(f'{prefix}_problem_shown')

        current = transition(
            self,
            current,
            equation(
                rf'\frac{{{n1}\times {left_scale}}}{{{d1}\times {left_scale}}}',
                rf'\frac{{{n2}\times {right_scale}}}{{{d2}\times {right_scale}}}',
            ),
        )
        current = transition(
            self,
            current,
            equation(
                rf'\frac{{{n1 * left_scale}}}{{{denominator}}}',
                rf'\frac{{{n2 * right_scale}}}{{{denominator}}}',
            ),
        )
        self.mark(f'{prefix}_common_denominator')
        current = transition(
            self,
            current,
            equation(rf'\frac{{{n1 * left_scale}+{n2 * right_scale}}}{{{denominator}}}'),
        )
        current = transition(self, current, equation(rf'\frac{{{result}}}{{{denominator}}}'))
        self.mark(f'{prefix}_summed')
        self.play(FadeOut(current), run_time=.55)
        self.wait(.3)

    def construct(self):
        self.show_whole_plus_fraction(2, 1, 3, 7, 'whole_one')
        self.show_whole_plus_fraction(3, 2, 5, 17, 'whole_two')
        self.show_whole_plus_fraction(-2, 1, 4, -7, 'whole_three')
        self.mark('whole_examples_done')
        self.wait(.75)

        self.show_fraction_plus_fraction(1, 3, 1, 4, 7, 12, 'frac_one')
        self.show_fraction_plus_fraction(1, 2, 1, 6, 4, 6, 'frac_two')
        self.show_fraction_plus_fraction(2, 5, 1, 3, 11, 15, 'frac_three')
        self.mark('done')
        self.wait(2.)
        self.write_marks('fraction_add_fractions_marks.json')
