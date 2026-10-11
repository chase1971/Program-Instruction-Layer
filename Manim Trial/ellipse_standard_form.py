"""Parts 2 and 3 of the Definition of an Ellipse clip (the scene itself is ellipse_definition.py).

Part 2: the grid and the numbers go; the figure is described in h, k, a, b and c (center, vertex,
co-vertex, focus), the point moves to the co-vertex to show each focus distance is a there, and
the right triangle gives a^2 - c^2 = b^2.

Part 3: the distance formula for d1 and d2, then d1 + d2 = 2a is simplified one move at a time
(with X = x - h and Y = y - k, each a single term) down to the standard form.
"""

import math

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    Indicate,
    Line,
    ReplacementTransform,
    RightAngle,
    VGroup,
    Write,
    always_redraw,
    smooth,
)

from ellipse_horizontal import ellipse_row
from equations_of_lines import READ_LONG, tex
from parabola_walkthrough import INK
from scene_style import PAPER_BLUE, PAPER_GOLD
from solve_steps import strike_pair

FIRST_COLOR = PAPER_BLUE        # focus 1 and its distance d1
SECOND_COLOR = PAPER_GOLD       # focus 2 and its distance d2
A_COLOR = '#6A1B9A'             # a: center to vertex, and the constant 2a
B_COLOR = '#00838F'             # b: center to co-vertex
C_COLOR = '#2E7D32'             # c: center to focus
FIGURE_SCALE = 1.4              # the figure grows this much once the grid is gone
FIGURE_CENTER = (0.0, -0.1)     # and the center sits here
TRIANGLE_Y = -2.6               # the b, c, a row under the figure (and later under the algebra)
WORK_Y = 0.75                   # the algebra rows
WORK_SIZE = 30
GENERIC_T = 0.9                 # where the generic point (x, y) sits on the ellipse (radians)
CO_VERTEX_T = math.pi / 2
SLOW = READ_LONG + 1.5


class EllipseStandardForm:
    """Methods mixed into EllipseDefinition: they take the Part 1 board and carry on from it."""

    def work(self, *lines, y=WORK_Y):
        """The equation as left-aligned rows; a row is one string or a list of separate pieces."""
        rows = VGroup(*[tex(*([line] if isinstance(line, str) else line), size=WORK_SIZE)
                        for line in lines])
        return rows.arrange(DOWN, buff=.3, aligned_edge=LEFT).move_to([0, y, 0])

    def strike(self, *terms):
        """Slash the cancelling terms in red, one after the other."""
        slashes = strike_pair(*terms)
        for slash in slashes:
            self.play(Create(slash), run_time=.5)
        return slashes

    def step(self, old, new, caption, mark, extra=(), run_time=1.3):
        """One algebra move: say it, replace the rows, hold."""
        self.say(caption)
        self.play(ReplacementTransform(old, new), *extra, run_time=run_time)
        self.beat(mark, SLOW)
        return new

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

        # ---- the grid and the numbers go; the figure grows -------------------------------------
        for live in (b['dot'], b['to_first'], b['to_second']):
            live.clear_updaters()
        for number in b['numbers']:
            number.clear_updaters()
        old = Group(b['plane'], b['dot'], b['to_first'], b['to_second'], b['axis'], *b['rows'],
                    *b['numbers'])
        grown = Group(b['curve'], b['center_dot'], *b['focus_dots'])
        words = b['focus_labels']
        self.say('Part 2. To build the equation, remove the grid and the numbers and look only '
                 'at the figure: the center $(h,k)$, the foci, and a point $(x,y)$ on the ellipse.')
        self.play(FadeOut(old), run_time=1.0)
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

        def mid(p1, p2):
            return (at(*p1) + at(*p2)) / 2

        px, py = point()
        near_first = (at(*foci[0]) * 2 + at(px, py)) / 3    # a third of the way in, clear of b
        d_one = tex('d_1', size=28, color=FIRST_COLOR).move_to(near_first + UP * .3)
        d_two = tex('d_2', size=28, color=SECOND_COLOR).move_to(mid((px, py), foci[1])
                                                                + RIGHT * .3 + DOWN * .1)
        self.say('The point is a distance $d_1$ from the first focus and a distance $d_2$ from '
                 'the second focus.')
        self.play(FadeIn(d_one), FadeIn(d_two), run_time=.9)
        self.beat('d-labels', SLOW)

        # ---- a, c and b -------------------------------------------------------------------------
        def leg(start, end, color):
            return Line(at(*start), at(*end), color=color, stroke_width=7)

        vertices = [Dot(at(h + s * a, k), color=A_COLOR, radius=.1) for s in (-1, 1)]
        a_leg = leg((h, k), (h + a, k), A_COLOR)
        a_label = tex('a', size=30, color=A_COLOR).move_to(mid((h, k), (h + a, k)) + UP * .3)
        self.say('The vertex is a distance $a$ from the center, so the vertices are $(h-a,k)$ and '
                 '$(h+a,k)$.')
        self.play(FadeIn(vertices[0], scale=1.5), FadeIn(vertices[1], scale=1.5), Create(a_leg),
                  FadeIn(a_label), run_time=1.2)
        self.beat('a', SLOW)

        c_leg = leg((h, k), (h + c, k), C_COLOR)
        c_label = tex('c', size=30, color=C_COLOR).move_to(mid((h, k), (h + c, k)) + UP * .3)
        self.say('The foci are a distance $c$ from the center, so they are at $(h-c,k)$ and '
                 '$(h+c,k)$.')
        self.play(FadeOut(Group(a_leg, a_label, *vertices)), Create(c_leg), FadeIn(c_label),
                  run_time=1.2)
        self.beat('c', SLOW)

        co_dot = Dot(at(h, k + bb), color=B_COLOR, radius=.1)
        b_leg = leg((h, k), (h, k + bb), B_COLOR)
        b_label = tex('b', size=30, color=B_COLOR).move_to(mid((h, k), (h, k + bb)) + LEFT * .3)
        self.say('The co-vertex is a distance $b$ above the center.')
        self.play(FadeIn(co_dot, scale=1.5), Create(b_leg), FadeIn(b_label), run_time=1.2)
        self.beat('b', SLOW)

        # ---- the point at the co-vertex: each distance is a ---------------------------------------
        self.say('Move the point to the co-vertex. By symmetry the two distances are equal, and '
                 'together they add up to $2a$, so each one is $a$.')
        self.play(FadeOut(Group(d_one, d_two, point_label)),
                  tracker.animate.set_value(CO_VERTEX_T), run_time=1.6, rate_func=smooth)
        a_one = tex('a', size=30, color=A_COLOR).move_to(mid((0, k + bb), foci[0]) + LEFT * .3
                                                         + UP * .15)
        a_two = tex('a', size=30, color=A_COLOR).move_to(mid((0, k + bb), foci[1]) + RIGHT * .3
                                                         + UP * .15)
        self.play(FadeIn(a_one), FadeIn(a_two), run_time=.8)
        self.beat('each-a', SLOW)

        corner = at(h, k)
        square = RightAngle(Line(corner, at(h + c, k)), Line(corner, at(h, k + bb)), length=.25,
                            color=INK, stroke_width=3)
        self.say('Together with the center, this forms a right triangle with legs $b$ and $c$ and '
                 'hypotenuse $a$.')
        self.play(FadeIn(square), Indicate(a_two, color=A_COLOR, scale_factor=1.3),
                  Indicate(b_label, color=B_COLOR, scale_factor=1.3),
                  Indicate(c_label, color=C_COLOR, scale_factor=1.3), run_time=1.4)
        self.beat('triangle', SLOW)

        pyth = tex('b^2', '+', 'c^2', '=', 'a^2', size=40).move_to([0, TRIANGLE_Y, 0])
        formula = tex('a^2', '-', 'c^2', '=', 'b^2', size=40).move_to([0, TRIANGLE_Y, 0])
        for row in (pyth, formula):
            for index, color in ((0, B_COLOR), (2, C_COLOR), (4, A_COLOR)):
                row[index].set_color(color)
        formula[0].set_color(A_COLOR)
        formula[2].set_color(C_COLOR)
        formula[4].set_color(B_COLOR)
        self.say('By the Pythagorean theorem, $b^2+c^2=a^2$.')
        self.play(Write(pyth), run_time=1.3)
        self.beat('pythagorean', SLOW)

        self.say('Subtract $c^2$ from both sides. This gives $a^2-c^2=b^2$.')
        self.play(ReplacementTransform(pyth, formula), run_time=1.3)
        self.beat('a2-c2', SLOW)
        return dict(figure=Group(grown, *words, dot, to_first, to_second, center_label, c_leg,
                                 c_label, co_dot, b_leg, b_label, a_one, a_two, square),
                    formula=formula)

    def algebra_part(self, kept):
        """Part 3: d1 + d2 = 2a down to the standard form. `kept` is what stays from Part 2."""
        kept['figure'].clear_updaters()    # always_redraw would undo the fade
        # The part opens on the figure with a joke warning; the next caption goes up before the wipe.
        self.say('Part 3. Warning: a lot of algebra ahead. You do not need to know this. But if '
                 'you are curious, this is how the formula is derived.')
        self.beat('warning', SLOW + 2.0)      # the part's opening frame: long enough to read it

        self.say('By the distance formula, $d_1$ and $d_2$ are the following.')
        dists = self.work(['d_1', r'=\sqrt{(x-(h-c))^2+(y-k)^2}'],
                          ['d_2', r'=\sqrt{(x-(h+c))^2+(y-k)^2}'])
        dists[0][0].set_color(FIRST_COLOR)
        dists[1][0].set_color(SECOND_COLOR)
        self.play(FadeOut(kept['figure']), FadeIn(dists), run_time=1.2)
        self.beat('distances', SLOW)

        root1, root2 = r'\sqrt{(x-h+c)^2+(y-k)^2}', r'\sqrt{(x-h-c)^2+(y-k)^2}'
        start = self.work(root1, '+' + root2 + '=2a')
        self.step(dists, start, 'Substitute these into $d_1+d_2=2a$.', 'substitute')

        r1, r2 = r'\sqrt{(X+c)^2+Y^2}', r'\sqrt{(X-c)^2+Y^2}'
        rows = self.work(r1, '+' + r2 + '=2a')
        rows = self.step(start, rows, 'To simplify the algebra, let $X=x-h$ and $Y=y-k$.', 'xy')

        rows = self.step(rows, self.work(r1, '=2a-' + r2),
                         'Subtract the second square root from both sides.', 'isolate')
        rows = self.step(rows, self.work(r'\left(' + r1 + r'\right)^2',
                                         r'=\left(2a-' + r2 + r'\right)^2'),
                         'Square both sides.', 'square')
        rows = self.step(rows, self.work('(X+c)^2+Y^2', '=4a^2-4a' + r2, '+(X-c)^2+Y^2'),
                         'Squaring a square root leaves the expression underneath it. Expand the '
                         'square on the right side.', 'unroot')
        left = self.work(['X^2', '+2cX', '+c^2', '+Y^2'], '=4a^2-4a' + r2,
                         ['+X^2', '-2cX', '+c^2', '+Y^2'])
        rows = self.step(rows, left, 'Expand $(X+c)^2$ and $(X-c)^2$.', 'expand')

        self.say('The terms $X^2$, $c^2$, and $Y^2$ appear on both sides, so they cancel.')
        top, bottom = rows[0], rows[2]
        slashes = [self.strike(top[i], bottom[i]) for i in (0, 2, 3)]
        # (the right-hand copy of each term is in the same slot of the third row)
        self.beat('cancel', SLOW)
        rows = self.step(Group(rows, *slashes),
                         self.work('2cX', '=4a^2-4a' + r2 + '-2cX'),
                         'This leaves the following equation.', 'left-over')
        rows = self.step(rows, self.work('4cX', '=4a^2-4a' + r2),
                         'Add $2cX$ to both sides.', 'add-2cx')
        rows = self.step(rows, self.work('4cX-4a^2', '=-4a' + r2),
                         'Subtract $4a^2$ from both sides.', 'minus-4a2')
        rows = self.step(rows, self.work('a^2-cX', '=a' + r2),
                         'Divide both sides by $-4$.', 'divide')
        rows = self.step(rows, self.work('(a^2-cX)^2', r'=\left(a' + r2 + r'\right)^2'),
                         'Square both sides.', 'square-again')
        rows = self.step(rows, self.work('a^4-2a^2cX+c^2X^2',
                                         '=a^2X^2-2a^2cX+a^2c^2+a^2Y^2'),
                         'Expand both sides.', 'expand-again')
        rows = self.step(rows, self.work('a^4+c^2X^2', '=a^2X^2+a^2c^2+a^2Y^2'),
                         'The term $-2a^2cX$ appears on both sides, so it cancels.', 'cancel-again')
        rows = self.step(rows, self.work('a^4-a^2c^2', '=a^2X^2-c^2X^2+a^2Y^2'),
                         'Subtract $c^2X^2$ and $a^2c^2$ from both sides.', 'collect')
        rows = self.step(rows, self.work('a^2(a^2-c^2)', '=(a^2-c^2)X^2+a^2Y^2'),
                         'Factor $a^2$ out of the left side and $X^2$ out of the first two terms '
                         'on the right.', 'factor')
        rows = self.step(rows, self.work('a^2b^2', '=b^2X^2+a^2Y^2'),
                         'From the figure, $a^2-c^2=b^2$. Substitute $b^2$.', 'substitute-b',
                         extra=[Indicate(kept['formula'], color=B_COLOR, scale_factor=1.15)])

        fractions = ellipse_row(['X^2'], ['Y^2'], 'a^2', 'b^2', 44).move_to([0, WORK_Y, 0])
        rows = self.step(rows, fractions, 'Divide both sides by $a^2b^2$.', 'divide-ab')
        standard = ellipse_row(['(', 'x', '-', 'h', ')^2'], ['(', 'y', '-', 'k', ')^2'],
                               'a^2', 'b^2', 44)
        standard.scale(min(1, 6.1 / standard.width)).move_to([0, WORK_Y, 0])
        self.step(rows, standard, 'Replace $X$ with $x-h$ and $Y$ with $y-k$.', 'standard')

        self.say('This is the standard form of an ellipse with a horizontal major axis. The '
                 'derivation for a vertical major axis is similar.')
        self.play(Indicate(standard, color=A_COLOR, scale_factor=1.08), run_time=1.2)
        self.beat('hold', SLOW + 1.0)

