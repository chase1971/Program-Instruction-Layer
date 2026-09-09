"""Factor a GCF: division bars, quotients, and merging common factors."""

from manim import (
    Scene, MathTex, Text, Line, FadeIn, FadeOut, Create, Write,
    Transform, TransformFromCopy, DOWN, smooth, config,
)
from solve_factors import solve_factors

config.background_color = '#101C30'

INK = '#F2F5FA'
GOLD = '#FFC66D'
BLUE = '#86C8FF'
MUTED = '#B2C0D4'


class GCFDivision(Scene):
    def construct(self):
        title = Text('FACTOR OUT THE GCF', font='Segoe UI', font_size=25,
                     color=MUTED).move_to([0, 3.15, 0])
        # A single TeX expression preserves normal baseline alignment of + and =.
        original = MathTex(r'6x^2', '+', '10x', '=0', color=INK, font_size=76)
        original.move_to([0, 1.95, 0])
        n1, plus, n2, equals = original
        self.add(title, original)

        def caption(words):
            return Text(words, font='Segoe UI', font_size=25,
                        color=MUTED).move_to([0, -3.05, 0])

        note = caption('Find what both terms have in common: 2x')
        self.add(note)
        self.wait(1.8)

        bar_y = min(n1.get_bottom()[1], n2.get_bottom()[1]) - .15
        def bar(term):
            return Line([term.get_left()[0]-.07, bar_y, 0],
                        [term.get_right()[0]+.07, bar_y, 0], color=INK, stroke_width=3)
        b1, b2 = bar(n1), bar(n2)
        self.play(Create(b1), run_time=.75)
        self.play(Create(b2), run_time=.75)
        d1 = MathTex('2x', color=GOLD, font_size=66).move_to([n1.get_x(), bar_y-.48, 0])
        d2 = MathTex('2x', color=GOLD, font_size=66).move_to([n2.get_x(), bar_y-.48, 0])
        next_note = caption('Divide each term by the same common factor')
        self.play(FadeOut(note), run_time=.2)
        note = next_note
        self.play(FadeIn(note), FadeIn(d1, shift=DOWN*.35), run_time=.9)
        self.play(FadeIn(d2, shift=DOWN*.35), run_time=.9)
        self.wait(1)

        # Reserve the completed equation's geometry before revealing any quotient.
        # Once 3x + 5 lands, it never moves or changes size again.
        final = MathTex('2x', '(', '3x', '+', '5', ')', '=0', color=INK, font_size=86)
        final[0].set_color(GOLD)
        final[2].set_color(BLUE)
        final[4].set_color(BLUE)
        final.move_to([0, -1.6, 0])
        q1, qp, q2 = final[2].copy(), final[3].copy(), final[4].copy()
        self.play(TransformFromCopy(n1, q1), run_time=1.1)
        self.play(FadeIn(qp), run_time=.4)
        self.play(TransformFromCopy(n2, q2), run_time=1.1)
        self.wait(1)

        self.play(FadeOut(note), run_time=.2)
        note = caption('Put the GCF you factored out in front of what is left')
        self.play(FadeOut(b1), FadeOut(b2), FadeIn(note),
                  run_time=.85)
        # Both divisors merge directly into the factor's final position.
        self.play(Transform(d1, final[0].copy()),
                  Transform(d2, final[0].copy()), run_time=2.2, rate_func=smooth)
        self.remove(d2)
        self.wait(.4)

        left_paren, right_paren = final[1].copy(), final[5].copy()
        self.play(Write(left_paren), Write(right_paren), run_time=1.2)
        self.play(TransformFromCopy(equals, final[6]), run_time=1.2)
        self.play(FadeOut(note), run_time=.2)
        note = caption('When we factor a GCF, we put it in front like this')
        self.play(FadeIn(note), run_time=.6)
        self.wait(3)
        # Consolidate the assembled pieces without changing their visible geometry.
        self.remove(d1, q1, qp, q2, left_paren, right_paren, final[6])
        self.add(final)
        solve_factors(self, final, original, title, note)
