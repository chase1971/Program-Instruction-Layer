"""Animate fraction sums with common denominators — whole + fraction, then fraction + fraction."""

from manim import (
    Create, DOWN, FadeIn, FadeOut, Line, MathTex, ReplacementTransform,
    Scene, UP, VGroup, WHITE, config, smooth,
)

from scene_style import Narrated

config.background_color = WHITE

INK = '#172033'
GOLD = '#A85D00'
BLUE = '#12669A'
WORK_Y = .55
RESULT_Y = -1.35
FONT = 62
BAR_HALF = .44
NUM_OFF = .38
COL_L = -1.05
COL_R = 1.05


def tex(value, color=INK):
    return MathTex(str(value), font_size=FONT, color=color)


def frac_bar(x):
    return Line(
        [x - BAR_HALF, WORK_Y, 0],
        [x + BAR_HALF, WORK_Y, 0],
        color=INK,
        stroke_width=3,
    )


def signed(value):
    value = str(value)
    return rf'({value})' if value.startswith('-') else value


def equation_row(expression):
    equals = tex('=')
    math = MathTex(expression, font_size=FONT, color=BLUE)
    return VGroup(equals, math).arrange(buff=.35).move_to([0, RESULT_Y, 0])


def aligned_fraction(x, n, d, top_color=GOLD, bottom_color=GOLD):
    terms = {
        'top': tex(n, top_color).move_to([x, WORK_Y + NUM_OFF, 0]),
        'bottom': tex(d, bottom_color).move_to([x, WORK_Y - NUM_OFF, 0]),
    }
    bar = frac_bar(x)
    return VGroup(terms['top'], bar, terms['bottom']), terms, bar


class FractionAddFractions(Narrated, Scene):
    def show_scale_factor(self, x, factor, color=GOLD):
        """Flash a multiplier beside the numerator and denominator."""
        top = tex(f'\\times {factor}', color).move_to([x + .95, WORK_Y + NUM_OFF, 0])
        bottom = tex(f'\\times {factor}', color).move_to([x + .95, WORK_Y - NUM_OFF, 0])
        self.play(FadeIn(top), FadeIn(bottom), run_time=.55)
        self.wait(.25)
        self.play(FadeOut(top), FadeOut(bottom), run_time=.35)
        return top, bottom

    def rewrite_whole(self, whole_value, terms, bar):
        """Turn a whole number into a fraction over 1."""
        whole = terms['top']
        whole_target = whole.get_center()
        whole.move_to([COL_L, WORK_Y, 0])
        self.play(FadeIn(whole), run_time=.55)
        self.wait(.35)
        self.play(
            whole.animate.move_to(whole_target),
            run_time=.85,
            rate_func=smooth,
        )
        self.wait(.15)
        bottom = tex('1', GOLD).move_to([COL_L, WORK_Y - NUM_OFF, 0])
        self.play(
            Create(bar),
            FadeIn(bottom, shift=DOWN * .16),
            run_time=.85,
            rate_func=smooth,
        )
        terms['top'] = whole
        terms['bottom'] = bottom
        self.wait(.45)

    def finish_sum(self, numerator, denominator, mark_prefix=None):
        if denominator == 1:
            expression = str(numerator)
        else:
            expression = rf'\frac{{{signed(numerator)}}}{{{denominator}}}'
        result = equation_row(expression)
        self.play(FadeIn(result, shift=DOWN * .1), run_time=.85)
        self.wait(.65)
        if mark_prefix:
            self.mark(f'{mark_prefix}_summed')
        return result

    def show_whole_plus_fraction(self, whole, n, d, result_num, result_den,
                                 mark_prefix=None):
        left_whole = tex(whole, GOLD).move_to([COL_L, WORK_Y, 0])
        plus = MathTex('+', font_size=FONT, color=INK).move_to([0, WORK_Y, 0])
        right, right_terms, right_bar = aligned_fraction(COL_R, n, d)
        board = VGroup(left_whole, plus, right)
        self.play(FadeIn(board), run_time=.85)
        self.wait(.45)
        if mark_prefix:
            self.mark(f'{mark_prefix}_problem_shown')

        left_terms = {'top': left_whole, 'bottom': None}
        left_bar = frac_bar(COL_L)
        self.rewrite_whole(whole, left_terms, left_bar)
        if mark_prefix:
            self.mark(f'{mark_prefix}_whole_rewritten')

        self.show_scale_factor(COL_L, d)
        new_top = tex(whole * d, GOLD).move_to(left_terms['top'].get_center())
        new_bottom = tex(d, GOLD).move_to(left_terms['bottom'].get_center())
        self.play(
            ReplacementTransform(left_terms['top'], new_top),
            ReplacementTransform(left_terms['bottom'], new_bottom),
            run_time=.95,
            rate_func=smooth,
        )
        left_terms['top'] = new_top
        left_terms['bottom'] = new_bottom
        self.wait(.45)
        if mark_prefix:
            self.mark(f'{mark_prefix}_scaled')

        result = self.finish_sum(result_num, result_den, mark_prefix=mark_prefix)
        self.play(FadeOut(board), FadeOut(result), run_time=.65)
        self.wait(.35)

    def show_fraction_plus_fraction(self, n1, d1, n2, d2, result_num, result_den,
                                    mark_prefix=None):
        left, left_terms, _ = aligned_fraction(COL_L, n1, d1)
        plus = MathTex('+', font_size=FONT, color=INK).move_to([0, WORK_Y, 0])
        right, right_terms, _ = aligned_fraction(COL_R, n2, d2, BLUE, INK)
        board = VGroup(left, plus, right)
        self.play(FadeIn(board), run_time=.85)
        self.wait(.45)
        if mark_prefix:
            self.mark(f'{mark_prefix}_problem_shown')

        left_scale = result_den // d1
        right_scale = result_den // d2
        self.show_scale_factor(COL_L, left_scale)
        self.show_scale_factor(COL_R, right_scale)
        if mark_prefix:
            self.mark(f'{mark_prefix}_scaled')

        new_left_top = tex(n1 * left_scale, GOLD).move_to(left_terms['top'].get_center())
        new_left_bottom = tex(result_den, GOLD).move_to(left_terms['bottom'].get_center())
        new_right_top = tex(n2 * right_scale, BLUE).move_to(right_terms['top'].get_center())
        new_right_bottom = tex(result_den, INK).move_to(right_terms['bottom'].get_center())
        self.play(
            ReplacementTransform(left_terms['top'], new_left_top),
            ReplacementTransform(left_terms['bottom'], new_left_bottom),
            ReplacementTransform(right_terms['top'], new_right_top),
            ReplacementTransform(right_terms['bottom'], new_right_bottom),
            run_time=1.05,
            rate_func=smooth,
        )
        self.wait(.45)

        result = self.finish_sum(result_num, result_den, mark_prefix=mark_prefix)
        self.play(FadeOut(board), FadeOut(result), run_time=.65)
        self.wait(.35)

    def construct(self):
        self.show_whole_plus_fraction(2, 1, 3, 7, 3, mark_prefix='whole_one')
        self.show_whole_plus_fraction(3, 2, 5, 17, 5, mark_prefix='whole_two')
        self.show_whole_plus_fraction(-2, 1, 4, -7, 4, mark_prefix='whole_three')
        self.mark('whole_examples_done')
        self.wait(.75)

        self.show_fraction_plus_fraction(1, 3, 1, 4, 7, 12, mark_prefix='frac_one')
        self.show_fraction_plus_fraction(1, 2, 1, 6, 4, 6, mark_prefix='frac_two')
        self.show_fraction_plus_fraction(2, 5, 1, 3, 11, 15, mark_prefix='frac_three')
        self.mark('done')
        self.wait(2.)
        self.write_marks('fraction_add_fractions_marks.json')
