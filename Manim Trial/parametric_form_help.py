"""Matrix-app help clip: a reduced 2x3 augmented matrix with a zero row -> parametric form.

[1 3 | 7; 0 0 | 0]  ->  x = 7 - 3t, y = t.  The free variable is always y = t, matching the
homework answer format. Instruction text lives in the Matrix app (parametricHelpTutorial.ts),
so the clip has no captions; each `mark` is a hold the app pauses on.
"""

from manim import (
    Create, FadeIn, FadeOut, Indicate, Line, Scene, VGroup, WHITE, config, smooth,
)

from math_notation import mathtex
from scene_style import Narrated
from solve_steps import op_under, strike_pair

config.background_color = WHITE

INK = '#172033'
GOLD = '#A85D00'
BLUE = '#12669A'
FONT = 66
COL_X = (-1.7, 0.0, 1.9)
ROW_Y = (2.4, 1.4)
BAR_X = 1.0
EQ_Y = 0.45
SOLVED_Y = -1.15
FREE_Y = -2.2
ANSWER_Y = -0.1
EQUALS_X = -0.9  # the = in every stacked equation lines up here


def tex(*parts, color=INK, size=FONT):
    return mathtex(*parts, font_size=size, color=color)


def bracket(x, top, bottom, opening):
    """A square bracket made of three strokes, opening toward the matrix."""
    tip = .22 if opening else -.22
    return VGroup(
        Line([x + tip, top, 0], [x, top, 0], color=INK, stroke_width=5),
        Line([x, top, 0], [x, bottom, 0], color=INK, stroke_width=5),
        Line([x, bottom, 0], [x + tip, bottom, 0], color=INK, stroke_width=5),
    )


def align_equals(row, equals_index):
    """Shift a row sideways so its = sits on the shared column."""
    row.shift([EQUALS_X - row[equals_index].get_center()[0], 0, 0])
    return row


class ParametricFormHelp(Narrated, Scene):
    pace = 1.0

    def build_matrix(self):
        values = (('1', '3', '7'), ('0', '0', '0'))
        self.cells = [
            [tex(v).move_to([COL_X[c], ROW_Y[r], 0]) for c, v in enumerate(row)]
            for r, row in enumerate(values)
        ]
        top, bottom = ROW_Y[0] + .45, ROW_Y[1] - .45
        self.frame_marks = VGroup(
            bracket(COL_X[0] - .85, top, bottom, True),
            bracket(COL_X[2] + .85, top, bottom, False),
            Line([BAR_X, top, 0], [BAR_X, bottom, 0], color=INK, stroke_width=3),
        )

    def show_matrix(self):
        self.build_matrix()
        everything = VGroup(*[cell for row in self.cells for cell in row])
        self.play(Create(self.frame_marks), FadeIn(everything), run_time=1.1)
        self.wait(1.)
        self.mark('matrix_shown')

    def drop_zero_row(self):
        zero_row = VGroup(*self.cells[1])
        note = tex('0', '=', '0', color=GOLD, size=54).move_to([4.6, ROW_Y[1], 0])
        self.play(FadeIn(note), run_time=.6)
        self.wait(.6)
        slash = Line(
            [COL_X[0] - .55, ROW_Y[1], 0], [COL_X[2] + .55, ROW_Y[1], 0],
            color='#C62828', stroke_width=6,
        )
        self.play(Create(slash), run_time=.7)
        self.wait(.5)
        self.play(FadeOut(VGroup(zero_row, slash, note)), run_time=.7)
        self.wait(.8)
        self.mark('zero_row_dropped')

    def write_equation(self):
        self.eq = tex('x', '+', '3', 'y', '=', '7').move_to([0, EQ_Y, 0])
        coefficient, seven = self.cells[0][1].copy(), self.cells[0][2].copy()
        self.play(Indicate(VGroup(*self.cells[0]), color=GOLD, scale_factor=1.15), run_time=.8)
        self.play(
            FadeIn(VGroup(self.eq[0], self.eq[1], self.eq[3], self.eq[4])),
            coefficient.animate.move_to(self.eq[2]),
            seven.animate.move_to(self.eq[5]),
            run_time=1.2, rate_func=smooth,
        )
        self.remove(coefficient, seven)
        self.add(self.eq[2], self.eq[5])
        self.wait(1.)
        self.mark('equation_written')

    def name_free_variable(self):
        self.free = align_equals(tex('y', '=', 't', color=BLUE), 1).set_y(FREE_Y)
        self.play(Indicate(self.eq[3], color=GOLD, scale_factor=1.6), run_time=.9)
        self.play(FadeIn(self.free), run_time=.8)
        self.wait(1.)
        self.mark('free_variable')

    def substitute(self):
        t_piece = self.free[2].copy().set_color(BLUE)
        # y hangs below the baseline, so sit the t on the 3's baseline instead of centering it.
        landing = t_piece.copy().move_to(self.eq[3])
        landing.shift([0, self.eq[2].get_bottom()[1] - landing.get_bottom()[1], 0])
        self.play(
            t_piece.animate.move_to(landing),
            self.eq[3].animate.set_opacity(0),
            run_time=1., rate_func=smooth,
        )
        self.eq_t = t_piece
        self.wait(1.)
        self.mark('substituted')

    def solve_for_x(self):
        three_t = VGroup(self.eq[2], self.eq_t)
        under_left = op_under('-', '3t', three_t, size=FONT)
        under_right = op_under('-', '3t', self.eq[5], size=FONT)
        self.play(FadeIn(under_left), FadeIn(under_right), run_time=.8)
        self.wait(.6)
        strike = strike_pair(three_t, under_left)
        self.play(Create(strike), run_time=.8)
        self.wait(.5)
        solved = align_equals(tex('x', '=', '7', '-', '3t'), 1).set_y(SOLVED_Y)
        seven_copy = self.eq[5].copy()
        minus_three_t = under_right.copy()
        self.play(
            FadeIn(solved[0]), FadeIn(solved[1]),
            seven_copy.animate.move_to(solved[2]),
            minus_three_t.animate.move_to(VGroup(solved[3], solved[4])),
            run_time=1.2, rate_func=smooth,
        )
        self.remove(seven_copy, minus_three_t)
        self.add(solved[2], solved[3], solved[4])
        self.solved = solved
        self.play(
            FadeOut(VGroup(
                self.eq[0], self.eq[1], self.eq[2], self.eq[3], self.eq[4], self.eq[5],
                self.eq_t, under_left, under_right, strike,
                self.frame_marks, *self.cells[0],
            )),
            run_time=.6,
        )
        self.wait(1.)
        self.mark('solved')

    def finish(self):
        answer = tex('(', 'x', ',', 'y', ')', '=', '(', '7', '-', '3t', ',', 't', ')')
        answer.move_to([0, ANSWER_Y, 0])
        # Each piece of the two rows travels into its slot in the coordinate.
        x_letter, y_letter = self.solved[0], self.free[0]
        flights = [
            (x_letter, answer[1]), (y_letter, answer[3]),
            (self.solved[2], answer[7]), (self.solved[3], answer[8]),
            (self.solved[4], answer[9]), (self.free[2], answer[11]),
        ]
        copies = [(src.copy(), dest) for src, dest in flights]
        shapes = {1, 3, 7, 8, 9, 11}
        self.play(
            FadeIn(VGroup(*[answer[i] for i in range(13) if i not in shapes])),
            *[copy.animate.move_to(dest) for copy, dest in copies],
            run_time=1.6, rate_func=smooth,
        )
        self.remove(*[copy for copy, _ in copies])
        self.add(*[answer[i] for i in shapes])
        self.wait(.6)
        self.play(FadeOut(VGroup(self.solved, self.free)), run_time=.6)
        self.play(Indicate(answer, color=GOLD, scale_factor=1.08), run_time=.8)
        self.wait(1.5)
        self.mark('hold')

    def construct(self):
        self.show_matrix()
        self.drop_zero_row()
        self.write_equation()
        self.name_free_variable()
        self.substitute()
        self.solve_for_x()
        self.finish()
        self.write_marks('parametric_form_help_marks.json')
