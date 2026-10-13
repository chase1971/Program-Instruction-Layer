"""Part 2 of the Definition of a Hyperbola clip (the scene itself is hyperbola_definition.py).

Part 2: the grid and the numbers go; the figure is described in h, k, a, b and c (center, vertex,
focus). The point sits on the right branch, the vertex gives a, the focus gives c, and the right
triangle with legs a and b and hypotenuse c gives c^2 = a^2 + b^2 (a plus where the ellipse had a
minus).
"""

from manim import (
    DOWN,
    LEFT,
    DashedVMobject,
    RIGHT,
    UP,
    Arc,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    Indicate,
    Line,
    ReplacementTransform,
    RightAngle,
    Write,
    always_redraw,
)

from equations_of_lines import READ_LONG, tex
from parabola_walkthrough import INK
from scene_style import PAPER_BLUE, PAPER_GOLD

FIRST_COLOR = PAPER_BLUE        # focus 1 and its distance d1
SECOND_COLOR = PAPER_GOLD       # focus 2 and its distance d2
A_COLOR = '#6A1B9A'             # a: center to vertex
B_COLOR = '#00838F'             # b: the vertical leg at the vertex
C_COLOR = '#2E7D32'             # c: center to focus
FIGURE_SCALE = 1.1              # the figure grows this much once the grid is gone
FIGURE_CENTER = (0.0, -0.8)     # and the center sits here, low enough that b clears the caption
FORMULA_Y = -3.0                # the c, a, b row under the figure
GENERIC_T = 0.6                 # where the generic point (x, y) sits on the right branch
SLOW = READ_LONG + 1.5


class HyperbolaStandardForm:
    """Methods mixed into HyperbolaDefinition: they take the Part 1 board and carry on from it."""

    def figure_part(self, b):
        """Part 2. b is the board: everything Part 1 left on screen."""
        p = self.problem
        h, k, a, bb, c = p.h, p.k, p.a, p.b, p.c
        c2p, point, tracker, foci = b['c2p'], b['point'], b['tracker'], b['foci']
        anchor = c2p(h, k)
        shift = [FIGURE_CENTER[0] - anchor[0], FIGURE_CENTER[1] - anchor[1], 0]

        def at(x, y):
            return anchor + (c2p(x, y) - anchor) * FIGURE_SCALE + shift

        def moved(m):
            return anchor + (m.get_center() - anchor) * FIGURE_SCALE + shift

        def mid(p1, p2):
            return (at(*p1) + at(*p2)) / 2

        # ---- the grid and the numbers go; the figure grows -------------------------------------
        for live in (b['dot'], b['to_first'], b['to_second']):
            live.clear_updaters()
        for number in b['numbers']:
            number.clear_updaters()
        old = Group(b['plane'], b['dot'], b['to_first'], b['to_second'], b['axis'], *b['rows'],
                    *b['numbers'], b['finished'])
        grown = Group(*b['curves'], b['center_dot'], *b['focus_dots'])
        words = b['focus_labels']
        self.say('Part 2. Remove the grid and the numbers. We keep only the center $(h,k)$, the '
                 'foci, and a point $(x,y)$ on the hyperbola.')
        self.play(FadeOut(old), run_time=1.0)
        side = b['side']
        side[0] = 1
        tracker.set_value(GENERIC_T)
        self.play(grown.animate.scale(FIGURE_SCALE, about_point=anchor).shift(shift),
                  *[m.animate.move_to(moved(m)) for m in words], run_time=1.4)
        dot = always_redraw(lambda: Dot(at(*point()), color=INK, radius=.12))
        to_first = always_redraw(lambda: Line(at(*point()), at(*foci[0]), color=FIRST_COLOR,
                                              stroke_width=5))
        to_second = always_redraw(lambda: Line(at(*point()), at(*foci[1]), color=SECOND_COLOR,
                                               stroke_width=5))
        center_label = tex('(h,k)', size=26).next_to(at(h, k), DOWN, buff=.12)
        point_label = tex('(x,y)', size=28).next_to(at(*point()), UP + RIGHT, buff=.04)
        self.play(FadeIn(dot), Create(to_first), Create(to_second), Write(center_label),
                  Write(point_label), run_time=1.2)
        self.beat('figure', SLOW)

        px, py = point()
        near_first = (at(*foci[0]) * 2 + at(px, py)) / 3    # a third of the way in
        d_one = tex('d_1', size=28, color=FIRST_COLOR).move_to(near_first + UP * .3)
        d_two = tex('d_2', size=28, color=SECOND_COLOR).move_to(mid((px, py), foci[1])
                                                                + RIGHT * .35 + DOWN * .1)
        self.say('The point is a distance $d_1$ from the first focus and a distance $d_2$ from '
                 'the second focus.')
        self.play(FadeIn(d_one), FadeIn(d_two), run_time=.9)
        self.beat('d-labels', SLOW)

        # ---- a, c and b -------------------------------------------------------------------------
        def leg(start, end, color):
            return Line(at(*start), at(*end), color=color, stroke_width=7)

        vertices = [Dot(at(h + s * a, k), color=A_COLOR, radius=.1) for s in (-1, 1)]
        a_leg = leg((h, k), (h + a, k), A_COLOR)
        a_label = tex('a', size=30, color=A_COLOR).move_to(mid((h, k), (h + a, k)) + DOWN * .3)
        self.say('The vertex is a distance $a$ from the center, so the vertices are $(h-a,k)$ and '
                 '$(h+a,k)$.')
        self.play(FadeOut(Group(d_one, d_two, point_label)),
                  FadeIn(vertices[0], scale=1.5), FadeIn(vertices[1], scale=1.5), Create(a_leg),
                  FadeIn(a_label), run_time=1.2)
        self.beat('a', SLOW)

        c_leg = leg((h, k), (h + c, k), C_COLOR)
        c_label = tex('c', size=30, color=C_COLOR).move_to(mid((h + a, k), (h + c, k)) + DOWN * .3)
        self.say('The foci are a distance $c$ from the center, so they are at $(h-c,k)$ and '
                 '$(h+c,k)$.')
        self.play(FadeOut(Group(a_leg, a_label)), Create(c_leg), FadeIn(c_label), run_time=1.2)
        self.beat('c', SLOW)

        # ---- the right triangle: legs a and b, hypotenuse c, one piece at a time ------------------
        corner = (h + a, k + bb)
        radius = float(abs(at(h + c, k)[0] - at(h, k)[0]))
        corner_angle = float(Line(at(h, k), at(*corner)).get_angle())
        swing = DashedVMobject(
            Arc(radius=radius, start_angle=0, angle=corner_angle, arc_center=at(h, k),
                color=C_COLOR, stroke_width=4), num_dashes=22)
        self.say('Now swing an arc of radius $c$ up from the focus, centered at $(h,k)$. Every '
                 'point on this arc is a distance $c$ from the center.')
        self.play(Create(swing), run_time=1.8)
        self.beat('arc', SLOW + 1.0)

        b_leg = leg((h + a, k), corner, B_COLOR)
        corner_dot = Dot(at(*corner), color=INK, radius=.08)
        self.say('Draw a vertical line up from the vertex until it meets the arc.')
        self.play(Create(b_leg), FadeIn(corner_dot, scale=1.5), run_time=1.4)
        self.beat('vertical', SLOW)

        hyp = leg((h, k), corner, C_COLOR)
        hyp_label = tex('c', size=30, color=C_COLOR).move_to(mid((h, k), corner) + LEFT * .3
                                                            + UP * .15)
        self.say('Connect that point back to the center. This segment is also a radius of the '
                 'arc, so its length is $c$, the same as the center to the focus.')
        self.play(Create(hyp), FadeIn(hyp_label), run_time=1.4)
        self.beat('hypotenuse', SLOW + 1.0)

        a_leg = leg((h, k), (h + a, k), A_COLOR)
        a_label = tex('a', size=30, color=A_COLOR).move_to(mid((h, k), (h + a, k)) + DOWN * .3)
        b_label = tex('b', size=30, color=B_COLOR).move_to(mid((h + a, k), corner) + RIGHT * .3)
        square = RightAngle(Line(at(h + a, k), at(h, k)), Line(at(h + a, k), at(*corner)),
                            length=.25, color=INK, stroke_width=3)
        self.say('The vertical leg is called $b$. We now have a right triangle with legs $a$ and '
                 '$b$ and hypotenuse $c$.')
        self.play(Create(a_leg), FadeIn(a_label), FadeIn(b_label), FadeIn(square),
                  FadeOut(Group(c_leg, c_label)), run_time=1.4)
        self.beat('triangle', SLOW + 1.0)

        pyth = tex('a^2', '+', 'b^2', '=', 'c^2', size=40).move_to([0, FORMULA_Y, 0])
        for index, color in ((0, A_COLOR), (2, B_COLOR), (4, C_COLOR)):
            pyth[index].set_color(color)
        self.say('In a right triangle, the squares of the two legs add up to the square of the '
                 'hypotenuse. This is the Pythagorean theorem: $a^2+b^2=c^2$.')
        self.play(Write(pyth), Indicate(hyp_label, color=C_COLOR, scale_factor=1.3),
                  Indicate(a_label, color=A_COLOR, scale_factor=1.3),
                  Indicate(b_label, color=B_COLOR, scale_factor=1.3), run_time=1.4)
        self.beat('pythagorean', SLOW + 1.0)

        self.say('Rewritten, this is $c^2=a^2+b^2$. Here $c$ is the longest side, so $a^2$ and '
                 '$b^2$ add. For an ellipse it was $a^2-c^2=b^2$, with a minus sign.')
        formula = tex('c^2', '=', 'a^2', '+', 'b^2', size=40).move_to([0, FORMULA_Y, 0])
        for index, color in ((0, C_COLOR), (2, A_COLOR), (4, B_COLOR)):
            formula[index].set_color(color)
        self.play(ReplacementTransform(pyth, formula), run_time=1.3)
        self.play(Indicate(formula, color=C_COLOR, scale_factor=1.12), run_time=1.1)
        self.beat('hold', SLOW + 1.0)
        return formula
