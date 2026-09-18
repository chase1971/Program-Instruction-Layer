"""Animate fraction sums with explicit movement and limited product morphs."""

import math
from dataclasses import dataclass

from manim import (
    Create, FadeIn, FadeOut, LEFT, Line, MathTex, RIGHT, Scene, Transform,
    UP, VGroup, WHITE, config, smooth,
)

from scene_style import Narrated

config.background_color = WHITE

INK = '#172033'
GOLD = '#A85D00'
BLUE = '#12669A'
FONT = 62
LEFT_X = -1.25
RIGHT_X = 1.25
MIDDLE_Y = .35
TOP_Y = .76
BOTTOM_Y = -.06
BAR_WIDTH = .92


def tex(value, color=INK):
    return MathTex(str(value), font_size=FONT, color=color)


def bar(x, width=BAR_WIDTH):
    return Line(
        [x - width / 2, MIDDLE_Y, 0],
        [x + width / 2, MIDDLE_Y, 0],
        color=INK,
        stroke_width=3,
    )


@dataclass
class FractionParts:
    top: MathTex
    line: Line
    bottom: MathTex


def fraction(x, numerator, denominator, color):
    return FractionParts(
        top=tex(numerator, color).move_to([x, TOP_Y, 0]),
        line=bar(x),
        bottom=tex(denominator, color).move_to([x, BOTTOM_Y, 0]),
    )


class FractionAddFractions(Narrated, Scene):
    pace = 1.0  # 20% slower than the shared Narrated default (1.2).

    def show_fraction(self, parts):
        self.play(
            FadeIn(parts.top),
            Create(parts.line),
            FadeIn(parts.bottom),
            run_time=.8,
        )

    def add_multiplier(self, parts, factor, side='left'):
        """Fade the multiplier in beside the numerator, then the denominator.

        Neither number moves and the bar never changes — only the multiplier
        label appears, on the outside of the fraction: `side='left'` prefixes
        `factor×number` (for a fraction on the left of the plus sign), `side='right'`
        suffixes `number×factor` (for a fraction on the right, away from the plus).
        """
        direction = LEFT if side == 'left' else RIGHT
        expr = rf'{factor}\times' if side == 'left' else rf'\times{factor}'
        top_factor = tex(expr, parts.top.get_color())
        top_factor.next_to(parts.top, direction, buff=.08)
        self.play(FadeIn(top_factor), run_time=.5)
        bottom_factor = tex(expr, parts.bottom.get_color())
        bottom_factor.next_to(parts.bottom, direction, buff=.08)
        self.play(FadeIn(bottom_factor), run_time=.5)
        self.wait(.5)
        return top_factor, bottom_factor

    def morph_product(self, parts, top_factor, bottom_factor, numerator, denominator):
        """Morph each `factor×number` pair directly into its product. Bar untouched."""
        x = parts.line.get_center()[0]
        new_top = tex(numerator, parts.top.get_color()).move_to([x, TOP_Y, 0])
        new_bottom = tex(denominator, parts.bottom.get_color()).move_to([x, BOTTOM_Y, 0])
        self.play(
            Transform(VGroup(top_factor, parts.top), new_top),
            Transform(VGroup(bottom_factor, parts.bottom), new_bottom),
            run_time=1.15,
            rate_func=smooth,
        )
        self.remove(top_factor, parts.top, bottom_factor, parts.bottom)
        self.add(new_top, new_bottom)
        parts.top = new_top
        parts.bottom = new_bottom
        self.wait(.65)

    def combine_over_one_denominator(self, left, plus, right, denominator):
        """Move the two existing numerators together; do not morph this step."""
        target_terms = VGroup(
            left.top.copy(),
            plus.copy(),
            right.top.copy(),
        ).arrange(buff=.2).move_to([0, TOP_Y, 0])
        combined_width = max(target_terms.width + .28, BAR_WIDTH)
        combined_bar = bar(0, combined_width)
        combined_bottom = tex(denominator, INK).move_to([0, BOTTOM_Y, 0])
        self.play(
            left.top.animate.move_to(target_terms[0].get_center()),
            plus.animate.move_to(target_terms[1].get_center()),
            right.top.animate.move_to(target_terms[2].get_center()),
            FadeOut(left.line),
            FadeOut(left.bottom),
            FadeOut(right.line),
            FadeOut(right.bottom),
            Create(combined_bar),
            FadeIn(combined_bottom),
            run_time=1.25,
            rate_func=smooth,
        )
        self.wait(.75)
        return combined_bar, combined_bottom

    def morph_sum(self, left_top, plus, right_top, result, combined_bar, denominator_mobject):
        """Morph the visible numerator addition into its result.

        The wide bar (sized to fit `numerator + numerator`) shrinks with it, down
        to a normal single-fraction bar width.
        """
        final_top = tex(result, BLUE).move_to([0, TOP_Y, 0])
        new_width = max(final_top.width, denominator_mobject.width) + .3
        new_bar = bar(0, max(new_width, BAR_WIDTH))
        self.play(
            Transform(left_top, final_top),
            Transform(combined_bar, new_bar),
            FadeOut(plus),
            FadeOut(right_top),
            run_time=1.15,
            rate_func=smooth,
        )
        self.wait(.85)

    def simplify_result(self, top, bottom, numerator, denominator, prefix):
        """If the sum reduces, morph it into lowest terms. No-op if already lowest."""
        gcf = math.gcd(abs(numerator), denominator)
        if gcf <= 1:
            return
        x = top.get_center()[0]
        reduced_top = tex(numerator // gcf, BLUE).move_to([x, TOP_Y, 0])
        reduced_bottom = tex(denominator // gcf, INK).move_to([x, BOTTOM_Y, 0])
        self.wait(.4)
        self.play(
            Transform(top, reduced_top),
            Transform(bottom, reduced_bottom),
            run_time=1.,
            rate_func=smooth,
        )
        self.wait(.75)
        self.mark(f'{prefix}_simplified')

    def clear_problem(self):
        visible = list(self.mobjects)
        self.play(*(FadeOut(item) for item in visible), run_time=.65)
        self.wait(.4)

    def show_whole_plus_fraction(self, whole, numerator, denominator, result, prefix):
        whole_term = tex(whole, GOLD).move_to([LEFT_X, MIDDLE_Y, 0])
        plus = tex('+').move_to([0, MIDDLE_Y, 0])
        right = fraction(RIGHT_X, numerator, denominator, BLUE)
        self.play(FadeIn(whole_term), FadeIn(plus), run_time=.75)
        self.show_fraction(right)
        self.wait(.65)
        self.mark(f'{prefix}_problem_shown')

        left = FractionParts(whole_term, bar(LEFT_X), tex(1, GOLD).move_to([LEFT_X, BOTTOM_Y, 0]))
        self.play(
            whole_term.animate.move_to([LEFT_X, TOP_Y, 0]),
            run_time=.9,
            rate_func=smooth,
        )
        self.play(Create(left.line), FadeIn(left.bottom), run_time=.75)
        self.wait(.65)
        self.mark(f'{prefix}_whole_rewritten')

        top_factor, bottom_factor = self.add_multiplier(left, denominator)
        self.mark(f'{prefix}_multiplier_shown')
        self.morph_product(
            left,
            top_factor,
            bottom_factor,
            whole * denominator,
            denominator,
        )
        self.mark(f'{prefix}_common_denominator')
        combined_bar, combined_bottom = self.combine_over_one_denominator(left, plus, right, denominator)
        self.mark(f'{prefix}_ready_to_add')
        self.morph_sum(left.top, plus, right.top, result, combined_bar, combined_bottom)
        self.mark(f'{prefix}_summed')
        self.simplify_result(left.top, combined_bottom, result, denominator, prefix)
        self.clear_problem()

    def show_fraction_plus_fraction(self, n1, d1, n2, d2, result, denominator, prefix):
        left = fraction(LEFT_X, n1, d1, GOLD)
        plus = tex('+').move_to([0, MIDDLE_Y, 0])
        right = fraction(RIGHT_X, n2, d2, BLUE)
        self.show_fraction(left)
        self.play(FadeIn(plus), run_time=.4)
        self.show_fraction(right)
        self.wait(.65)
        self.mark(f'{prefix}_problem_shown')

        left_scale = denominator // d1
        right_scale = denominator // d2
        left_factors = self.add_multiplier(left, left_scale) if left_scale != 1 else None
        right_factors = (
            self.add_multiplier(right, right_scale, side='right') if right_scale != 1 else None
        )
        self.mark(f'{prefix}_multipliers_shown')
        if left_factors:
            self.morph_product(left, *left_factors, n1 * left_scale, denominator)
        if right_factors:
            self.morph_product(right, *right_factors, n2 * right_scale, denominator)
        self.mark(f'{prefix}_common_denominator')
        combined_bar, combined_bottom = self.combine_over_one_denominator(left, plus, right, denominator)
        self.mark(f'{prefix}_ready_to_add')
        self.morph_sum(left.top, plus, right.top, result, combined_bar, combined_bottom)
        self.mark(f'{prefix}_summed')
        self.simplify_result(left.top, combined_bottom, result, denominator, prefix)
        self.clear_problem()

    def construct(self):
        self.show_whole_plus_fraction(2, 1, 3, 7, 'whole_one')
        self.show_whole_plus_fraction(-2, 1, 4, -7, 'whole_three')
        self.mark('whole_examples_done')
        self.wait(.75)

        self.show_fraction_plus_fraction(1, 3, 1, 4, 7, 12, 'frac_one')
        self.show_fraction_plus_fraction(1, 2, 1, 6, 4, 6, 'frac_two')
        self.show_fraction_plus_fraction(2, 5, 1, 3, 11, 15, 'frac_three')
        self.mark('done')
        self.wait(2.)
        self.write_marks('fraction_add_fractions_marks.json')
