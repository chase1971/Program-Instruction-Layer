"""Animate fraction products with aligned terms and slash-and-pull cancellation."""

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


def slash_on(term):
    center = term.get_center()
    half_width = max(term.width * .55, .2)
    half_height = max(term.height * .55, .24)
    return Line(
        center + [-half_width, half_height, 0],
        center + [half_width, -half_height, 0],
        color=GOLD,
        stroke_width=4,
    )


def product_factor(value):
    value = str(value)
    return rf'({value})' if value.startswith('-') else value


def equation_row(expression):
    equals = tex('=')
    math = MathTex(expression, font_size=FONT, color=BLUE)
    return VGroup(equals, math).arrange(buff=.35).move_to([0, RESULT_Y, 0])


def aligned_problem(n1, d1, n2, d2):
    """Build a flat group whose two fraction bars share one horizontal row."""
    terms = {
        'left_top': tex(n1, GOLD).move_to([COL_L, WORK_Y + NUM_OFF, 0]),
        'left_bottom': tex(d1, GOLD).move_to([COL_L, WORK_Y - NUM_OFF, 0]),
        'right_top': tex(n2, BLUE).move_to([COL_R, WORK_Y + NUM_OFF, 0]),
        'right_bottom': tex(d2).move_to([COL_R, WORK_Y - NUM_OFF, 0]),
    }
    parts = {
        'left_bar': frac_bar(COL_L),
        'times': MathTex(r'\times', font_size=FONT, color=INK).move_to([0, WORK_Y, 0]),
        'right_bar': frac_bar(COL_R),
    }
    board = VGroup(
        terms['left_top'],
        parts['left_bar'],
        terms['left_bottom'],
        parts['times'],
        terms['right_top'],
        parts['right_bar'],
        terms['right_bottom'],
    )
    return board, terms, parts


class FractionTimesWhole(Narrated, Scene):
    def pull_cancel_pair(self, board, terms, values, reductions):
        """Show reduced top values above and reduced bottom values below."""
        marks = []
        replacements = []
        targets = []

        for key, new_value in reductions:
            term = terms[key]
            direction = UP if key.endswith('top') else DOWN
            color = term.get_color()
            replacement = tex(new_value, color).next_to(term, direction, buff=.25)
            marks.append(slash_on(term))
            replacements.append(replacement)
            targets.append(term.get_center())

        appear = [Create(mark) for mark in marks]
        appear.extend(FadeIn(replacement) for replacement in replacements)
        self.play(*appear, run_time=.75)
        self.wait(.3)

        pull = [FadeOut(mark) for mark in marks]
        pull.extend(FadeOut(terms[key]) for key, _ in reductions)
        pull.extend(
            replacement.animate.move_to(target)
            for replacement, target in zip(replacements, targets)
        )
        self.play(*pull, run_time=1.15, rate_func=smooth)

        for (key, _), replacement in zip(reductions, replacements):
            board.remove(terms[key])
            board.add(replacement)
            terms[key] = replacement
        for key, new_value in reductions:
            values[key] = str(new_value)

    def finish_product(self, values, result_spec, intermediate_spec=None,
                       mark_prefix=None):
        top_left = product_factor(values['left_top'])
        top_right = product_factor(values['right_top'])
        bottom_left = product_factor(values['left_bottom'])
        bottom_right = product_factor(values['right_bottom'])
        multiplication = equation_row(
            rf'\frac{{{top_left}\times {top_right}}}'
            rf'{{{bottom_left}\times {bottom_right}}}'
        )
        self.play(FadeIn(multiplication, shift=DOWN * .1), run_time=.85)
        self.wait(.6)
        if mark_prefix:
            self.mark(f'{mark_prefix}_products_shown')

        if isinstance(result_spec, tuple):
            numerator, denominator = result_spec
        else:
            numerator, denominator = result_spec, 1
        displayed_numerator, displayed_denominator = (
            intermediate_spec if intermediate_spec else (numerator, denominator)
        )
        fraction = equation_row(
            rf'\frac{{{displayed_numerator}}}{{{displayed_denominator}}}'
        )
        self.play(
            ReplacementTransform(multiplication, fraction),
            run_time=1.05,
            rate_func=smooth,
        )
        self.wait(.65)

        if intermediate_spec:
            simplified_expression = (
                str(numerator)
                if denominator == 1
                else rf'\frac{{{numerator}}}{{{denominator}}}'
            )
            simplified = equation_row(simplified_expression)
            self.play(
                ReplacementTransform(fraction, simplified),
                run_time=1.05,
                rate_func=smooth,
            )
            self.wait(.75)
            if mark_prefix:
                self.mark(f'{mark_prefix}_simplified')
            return simplified

        if denominator != 1:
            if mark_prefix:
                self.mark(f'{mark_prefix}_simplified')
            return fraction
        whole = equation_row(str(numerator))
        self.play(
            ReplacementTransform(fraction, whole),
            run_time=1.05,
            rate_func=smooth,
        )
        self.wait(.75)
        return whole

    def show_problem(self, n1, d1, n2, d2, result_spec, reductions=None,
                     whole_number=True, intermediate_spec=None, mark_prefix=None):
        board, terms, parts = aligned_problem(n1, d1, n2, d2)
        values = {
            'left_top': str(n1),
            'left_bottom': str(d1),
            'right_top': str(n2),
            'right_bottom': str(d2),
        }
        if whole_number:
            whole_target = terms['right_top'].get_center()
            terms['right_top'].move_to([COL_R, WORK_Y, 0])
            first_view = VGroup(
                terms['left_top'],
                parts['left_bar'],
                terms['left_bottom'],
                parts['times'],
                terms['right_top'],
            )
            self.play(FadeIn(first_view), run_time=.85)
            self.wait(.55)
            if mark_prefix:
                self.mark(f'{mark_prefix}_problem_shown')
            self.play(
                terms['right_top'].animate.move_to(whole_target),
                run_time=.85,
                rate_func=smooth,
            )
            self.wait(.2)
            self.play(
                Create(parts['right_bar']),
                FadeIn(terms['right_bottom'], shift=DOWN * .16),
                run_time=.85,
                rate_func=smooth,
            )
        else:
            self.play(FadeIn(board), run_time=.85)

        self.wait(.55)
        if mark_prefix:
            self.mark(f'{mark_prefix}_whole_rewritten')
        if reductions:
            self.pull_cancel_pair(board, terms, values, reductions)
            self.wait(.5)

        result = self.finish_product(
            values,
            result_spec,
            intermediate_spec=intermediate_spec,
            mark_prefix=mark_prefix,
        )
        self.play(FadeOut(board), FadeOut(result), run_time=.65)
        self.wait(.35)

    def construct(self):
        self.show_problem(
            1, 3, 15, 1, '5',
            intermediate_spec=(15, 3),
            mark_prefix='example_one',
        )
        self.show_problem(
            1, 3, 4, 1, (4, 3),
            mark_prefix='example_two',
        )
        self.show_problem(1, 3, 22, 1, (22, 3), mark_prefix='example_three')
        self.mark('example_one_done')
        self.wait(1.)

        self.show_problem(
            2, 7, 14, 1, '4',
            reductions=[('left_bottom', '1'), ('right_top', '2')],
        )
        self.show_problem(
            2, 7, -21, 1, '-6',
            reductions=[('left_bottom', '1'), ('right_top', '-3')],
        )
        self.show_problem(
            2, 7, 3, 8, (3, 28),
            reductions=[('left_top', '1'), ('right_bottom', '4')],
            whole_number=False,
        )
        self.mark('done')
        self.wait(2.)
        self.write_marks('fraction_times_whole_marks.json')
