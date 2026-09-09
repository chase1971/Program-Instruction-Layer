"""Solve a two-step equation: undo the addition, then undo the multiplication."""

from manim import (
    Scene, MathTex, Text, VGroup, Line, FadeIn, FadeOut, Create,
    TransformFromCopy, DOWN, smooth, config,
)

config.background_color = '#101C30'

INK = '#F2F5FA'
GOLD = '#FFC66D'
BLUE = '#86C8FF'
MUTED = '#B2C0D4'

WORK_Y = 1.95
CAPTION_Y = -3.05


class TwoStepEquation(Scene):
    def construct(self):
        self.note = None
        title = Text('SOLVE THE TWO-STEP EQUATION', font='Segoe UI',
                     font_size=25, color=MUTED).move_to([0, 3.15, 0])
        # A single TeX expression keeps + and = on their natural baseline.
        original = MathTex('3x', '+', '7', '=', '22', color=INK, font_size=76)
        original.move_to([0, WORK_Y, 0])
        original[0].set_color(BLUE)
        self.add(title, original)
        self.change_note('Two operations are stacked on x: times 3, then plus 7')
        self.wait(1.8)

        self.change_note('Undo the addition: subtract 7 from both sides')
        minus_left = MathTex('-7', font_size=54, color=GOLD).next_to(original[2], DOWN, buff=.3)
        minus_right = MathTex('-7', font_size=54, color=GOLD).next_to(original[4], DOWN, buff=.3)
        self.play(FadeIn(minus_left, shift=DOWN*.15), run_time=.9)
        self.play(FadeIn(minus_right, shift=DOWN*.15), run_time=.9)
        self.wait(1.2)

        reduced = MathTex('3x', '=', '15', color=INK, font_size=76)
        reduced.move_to([0, -.2, 0])
        reduced[0].set_color(BLUE)
        self.change_note('7 minus 7 is zero, so the left side is just 3x')
        self.play(TransformFromCopy(original[0], reduced[0]), run_time=1.2)
        self.play(FadeIn(reduced[1]), run_time=.4)
        self.play(TransformFromCopy(VGroup(original[4], minus_right), reduced[2]), run_time=1.4)
        self.wait(1.2)

        # The completed line takes the working baseline and never moves again.
        self.play(FadeOut(original), FadeOut(minus_left), FadeOut(minus_right),
                  reduced.animate.move_to([0, WORK_Y, 0]), run_time=1.6, rate_func=smooth)
        self.wait(.5)

        self.change_note('Undo the multiplication: divide both sides by 3')
        bars = VGroup()
        divisors = VGroup()
        for term in (reduced[0], reduced[2]):
            y = reduced.get_bottom()[1] - .15
            bars.add(Line([term.get_left()[0]-.07, y, 0],
                          [term.get_right()[0]+.07, y, 0], color=INK, stroke_width=3))
            divisors.add(MathTex('3', font_size=60, color=GOLD).move_to([term.get_x(), y-.45, 0]))
        self.play(Create(bars[0]), run_time=.7)
        self.play(Create(bars[1]), run_time=.7)
        self.play(FadeIn(divisors, shift=DOWN*.25), run_time=.9)
        self.wait(1.2)

        answer = MathTex('x', '=', '5', color=GOLD, font_size=86).move_to([0, -1.6, 0])
        self.play(TransformFromCopy(VGroup(reduced[0], divisors[0]), answer[0]), run_time=1.4)
        self.play(FadeIn(answer[1]), run_time=.4)
        self.play(TransformFromCopy(VGroup(reduced[2], divisors[1]), answer[2]), run_time=1.4)
        self.wait(1.4)

        self.play(FadeOut(bars), FadeOut(divisors), run_time=.6)
        self.change_note('Check it in the equation you started with')
        check = MathTex('3(5)', '+', '7', '=', '22', color=MUTED, font_size=44)
        check.move_to([0, -2.5, 0])
        self.play(FadeIn(check), run_time=.9)
        self.wait(4)

    def change_note(self, words):
        fresh = Text(words, font='Segoe UI', font_size=25, color=MUTED)
        fresh.move_to([0, CAPTION_Y, 0])
        if self.note is None:
            self.note = fresh
            self.add(self.note)
            return
        self.play(FadeOut(self.note), run_time=.25)
        self.note = fresh
        self.play(FadeIn(self.note), run_time=.35)
