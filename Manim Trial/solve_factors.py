"""Continue the GCF scene with the zero-product property and two solutions."""

from manim import (
    MathTex, Text, VGroup, Line, FadeIn, FadeOut, Transform,
    TransformFromCopy, Create, Write, UP, DOWN, smooth,
)

INK = '#F2F5FA'
GOLD = '#FFC66D'
BLUE = '#86C8FF'
MUTED = '#B2C0D4'


def solve_factors(scene, factored, original, title, note):
    def change_note(words):
        nonlocal note
        scene.play(FadeOut(note), run_time=.25)
        note = Text(words, font='Segoe UI', font_size=25, color=MUTED)
        note.move_to([0, -3.05, 0])
        scene.play(FadeIn(note), run_time=.35)

    scene.play(FadeOut(original, shift=UP*.5), FadeOut(title),
               factored.animate.move_to([0, 1.95, 0]), run_time=2, rate_func=smooth)
    title = Text('SET EACH FACTOR EQUAL TO ZERO', font='Segoe UI',
                 font_size=25, color=MUTED).move_to([0, 3.15, 0])
    scene.play(FadeIn(title), run_time=.5)
    change_note('A product is zero when at least one factor is zero')
    scene.wait(.8)

    left = MathTex('2x', '=', '0', font_size=72, color=INK).move_to([-3, .6, 0])
    right = MathTex('3x', '+', '5', '=', '0', font_size=72, color=INK).move_to([3, .6, 0])
    left[0].set_color(GOLD)
    right[0].set_color(BLUE)
    right[2].set_color(BLUE)
    # Move actual factors diagonally outward, then supply an equation for each.
    scene.play(Transform(factored[0], left[0]),
               Transform(factored[2], right[0]), Transform(factored[3], right[1]),
               Transform(factored[4], right[2]),
               FadeOut(factored[1]), FadeOut(factored[5]), FadeOut(factored[6]),
               run_time=2.3, rate_func=smooth)
    scene.play(Write(left[1:]), Write(right[3:]), run_time=1.2)
    scene.remove(factored, *factored, left[1:], right[3:])
    scene.add(left, right)
    scene.wait(1)

    change_note('For 2x = 0, divide both sides by 2')
    bars = VGroup()
    divisors = VGroup()
    for term in (left[0], left[2]):
        y = left.get_bottom()[1] - .13
        bars.add(Line([term.get_left()[0]-.06, y, 0],
                      [term.get_right()[0]+.06, y, 0], color=INK, stroke_width=3))
        divisors.add(MathTex('2', font_size=54, color=GOLD).move_to([term.get_x(), y-.38, 0]))
    scene.play(Create(bars), run_time=.8)
    scene.play(FadeIn(divisors, shift=DOWN*.2), run_time=.8)
    answer_left = MathTex('x', '=', '0', color=GOLD, font_size=78).move_to([-3, -1.6, 0])
    scene.play(TransformFromCopy(left[0], answer_left[0]),
               FadeIn(answer_left[1]), TransformFromCopy(left[2], answer_left[2]), run_time=1.5)
    scene.wait(.8)
    scene.play(FadeOut(bars), FadeOut(divisors), run_time=.5)

    change_note('For 3x + 5 = 0, subtract 5 from both sides')
    minus_a = MathTex('-5', font_size=54, color=BLUE).next_to(right[2], DOWN, buff=.3)
    minus_b = MathTex('-5', font_size=54, color=BLUE).next_to(right[4], DOWN, buff=.3)
    scene.play(FadeIn(minus_a, shift=DOWN*.15), FadeIn(minus_b, shift=DOWN*.15), run_time=1)
    scene.wait(1)
    reduced = MathTex('3x', '=', '-5', font_size=72, color=INK).move_to([3, -.95, 0])
    reduced[0].set_color(BLUE)
    scene.play(TransformFromCopy(right[0], reduced[0]), FadeIn(reduced[1]),
               TransformFromCopy(VGroup(right[4], minus_b), reduced[2]), run_time=1.4)
    scene.play(FadeOut(right), FadeOut(minus_a), FadeOut(minus_b),
               reduced.animate.move_to([3, .6, 0]), run_time=1.3)

    change_note('Then divide both sides by 3')
    bars = VGroup()
    divisors = VGroup()
    for term in (reduced[0], reduced[2]):
        y = reduced.get_bottom()[1] - .13
        bars.add(Line([term.get_left()[0]-.06, y, 0],
                      [term.get_right()[0]+.06, y, 0], color=INK, stroke_width=3))
        divisors.add(MathTex('3', font_size=54, color=BLUE).move_to([term.get_x(), y-.38, 0]))
    scene.play(Create(bars), FadeIn(divisors, shift=DOWN*.2), run_time=1)
    answer_right = MathTex('x', '=', r'-\frac{5}{3}', font_size=78, color=BLUE)
    answer_right.move_to([3, -1.6, 0])
    scene.play(TransformFromCopy(reduced[0], answer_right[0]),
               FadeIn(answer_right[1]),
               TransformFromCopy(VGroup(reduced[2], divisors[1]), answer_right[2]), run_time=1.6)
    scene.wait(1)
    scene.play(FadeOut(left), FadeOut(reduced), FadeOut(bars), FadeOut(divisors), run_time=.8)
    change_note('Either value makes the original product equal zero')
    either = Text('or', font='Segoe UI', font_size=30, color=MUTED).move_to([0, -1.6, 0])
    scene.play(FadeIn(either), run_time=.5)
    scene.wait(4)
