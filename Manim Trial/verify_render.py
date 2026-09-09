"""Headless installation check: typeset and animate a simple division."""

from manim import DOWN, FadeIn, MathTex, Scene, TransformMatchingTex


class DivisionCheck(Scene):
    def construct(self):
        original = MathTex(r"\frac{6a^4}{3a^2}").scale(2)
        result = MathTex(r"2a^2").scale(2)
        condition = MathTex(r"a\ne0").scale(0.7).to_edge(DOWN)
        self.play(FadeIn(original), FadeIn(condition))
        self.wait(0.5)
        self.play(TransformMatchingTex(original, result))
        self.wait(0.5)
