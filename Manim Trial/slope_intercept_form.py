"""Get a line from standard form into slope-intercept form, on a white background.

The first clips in the light theme (scene_style PAPER palette): the navy clips were hard to
read on the classroom projector, and these are headed for the student portal.

Teaching order, as Chase laid it out -- every clip in this module runs the same beats:
    goal is y = mx + b; x and y need to be on opposite sides, so move the x term first,
    then divide by the number next to y.
    move the x term to both sides -> it cancels on the left
    the constant and the x term are not like terms, so write them x term first
    divide EVERY term by the number next to y, then simplify
    a negative slope gets its negative moved to the top number (Chase's graphing
    convention -- stated on screen without a reason)
    an inequality keeps its sign through slope-intercept form, and flips when every term
    is divided by a negative number

Each scene is one Problem. Verified:
    SlopeInterceptForm:   -2x - 3y < 6  ->  -3y < 2x + 6   ->  y > -(2/3)x - 2
                          check (0, 0): 0 < 6 and 0 > -2, both true
    SlopeInterceptYFirst: -2y + 5x = -8 ->  -2y = -5x - 8  ->  y = (5/2)x + 4
                          check x = 2: y = 9, and -18 + 10 = -8
    SlopeInterceptMoveConstant: 2y + 8 > -6x -> 2y > -6x - 8 -> y > -3x - 4
                          check (0, 0): 8 > 0 and 0 > -4, both true
"""

from dataclasses import dataclass

from manim import (
    DOWN, UP, Arrow, Axes, Create, DashedLine, Dot, FadeIn, FadeOut, Indicate, Line,
    Polygon, ReplacementTransform, Scene, SurroundingRectangle, VGroup, Write, config, smooth,
)

from math_notation import hanging_fraction, mathtex, unsigned
from vector_projection_shadow import copy_into
from scene_style import (
    PAPER, PAPER_BLUE, PAPER_GOLD, PAPER_INK, PAPER_MUTED, PAPER_RED, Narrated, label,
)

config.background_color = PAPER

INK = PAPER_INK
X_COLOR = PAPER_BLUE   # x terms
OP_COLOR = PAPER_GOLD  # what we do to both sides
MATH_SIZE = 72
TOP_Y = 1.9
ROW2_Y = -.35
GRAPH_HEIGHT = 6.
GRAPH_RIGHT = 6.6  # the graph hugs the right edge; the boxed answer and notes sit left


def line_through_box(slope, b, window):
    """Where y = slope x + b enters and leaves the graph window, as two (x, y) points."""
    x_lo, x_hi, y_lo, y_hi = window
    hits = [(x, slope * x + b) for x in (x_lo, x_hi) if y_lo <= slope * x + b <= y_hi]
    if slope:
        hits += [((y - b) / slope, y) for y in (y_lo, y_hi) if x_lo < (y - b) / slope < x_hi]
    hits.sort()
    return hits[0], hits[-1]


def half_plane(corners, slope, b, above):
    """The part of the window's rectangle on one side of the line -- what gets shaded."""
    def inside(point):
        gap = point[1] - (slope * point[0] + b)
        return gap >= 0 if above else gap <= 0

    kept = []
    for here, there in zip(corners, corners[1:] + corners[:1]):
        if inside(here):
            kept.append(here)
        if inside(here) != inside(there):  # this edge crosses the line
            t = ((slope * here[0] + b) - here[1]) / ((there[1] - here[1]) - slope * (there[0] - here[0]))
            kept.append((here[0] + t * (there[0] - here[0]), here[1] + t * (there[1] - here[1])))
    return kept


@dataclass
class Problem:
    """Everything that differs between clips. Captions are the words Chase would say."""
    start: tuple          # (term, term, relation, right side); one of the first two is the y
                          # term. The relation is '=' or an inequality: '<', '>', r'\leq', r'\geq'
    x_at: int             # which term of start is the x term (3 when it is already on the right)
    op: str               # what goes under the moved term and the right side, e.g. '+2x'
    op_caption: str
    cancel_caption: str
    right: tuple          # the right side as it first comes down: term, sign, term
    swapped: tuple        # the same, x term first: x term, sign, constant (None if it already is)
    like_caption: str
    swap_caption: str
    divisor: str
    simplify_captions: tuple  # y term, x term, constant
    answer: tuple         # ('y', relation, slope x, sign, intercept) -- the relation flipped
                          # when this is an inequality and the divisor is negative
    top_answer: tuple     # the answer with the negative on the top number, or None
    m: str
    b: str
    closing: str
    marks_file: str
    rise_run: tuple = None  # the slope as Chase graphs it: (rise, run), run always positive
    intercept: float = 0.
    window: tuple = (-6, 6, -6, 4)  # graph x_lo, x_hi, y_lo, y_hi -- room for the rise
    moved_at: int = None  # which of the first two terms moves in step 1; defaults to x_at
    sides_caption: str = "To get there, the x's and the y's must be on opposite sides."
    first_step: str = '1.  Move the x term over first'
    divide_caption: str = None  # defaults to 'Step 2: divide by <divisor>, the number next to y.'
    brief: bool = False  # Chase's short version: no goal/plan intro, captions only on the steps,
                         # the cancel / bring-down / simplify happen silently, straight to graph
    intro: bool = None   # show the goal/plan panel first; defaults to "not brief"

    def __post_init__(self):
        if self.intro is None:
            self.intro = not self.brief


NEGATIVE_SLOPE = Problem(
    start=('-2x', '-3y', '<', '6'), x_at=0, op='+2x', brief=True, intro=True,
    op_caption='Step 1: move the 2x by adding 2x to both sides.',
    cancel_caption=None,
    right=('6', '+', '2x'), swapped=('2x', '+', '6'),
    like_caption=None,
    swap_caption=None,
    divisor='-3', divide_caption='Step 2: divide each term by -3.',
    simplify_captions=(None, None, None),
    answer=('y', '>', r'-\frac{2}{3}x', '-', '2'),
    top_answer=('y', '>', hanging_fraction('2', '3') + 'x', '-', '2'),
    m='m = ' + hanging_fraction('2', '3'), b='b = -2',
    closing=None,
    marks_file='slope_intercept_form_marks.json',
    rise_run=(-2, 3), intercept=-2,
)

Y_FIRST = Problem(
    start=('-2y', '+5x', r'\geq', '-8'), x_at=1, op='-5x', brief=True,
    op_caption='Step 1: move the 5x by subtracting 5x from both sides.',
    cancel_caption=None,
    right=('-8', '-', '5x'), swapped=('-5x', '-', '8'),
    like_caption=None,
    swap_caption=None,
    divisor='-2', divide_caption='Step 2: divide each term by -2.',
    simplify_captions=(None, None, None),
    answer=('y', r'\leq', r'\frac{5}{2}x', '+', '4'),
    top_answer=None,
    m=r'm = \frac{5}{2}', b='b = 4',
    closing=None,
    marks_file='slope_intercept_y_first_marks.json',
    rise_run=(5, 2), intercept=4, window=(-7, 5, -3, 11),
)

MOVE_CONSTANT = Problem(
    start=('2y', '+8', '>', '-6x'), x_at=3, moved_at=1, op='-8', brief=True,
    op_caption='Step 1: move the 8 by subtracting 8 from both sides.',
    cancel_caption=None,
    right=('-6x', '-', '8'), swapped=None,
    like_caption=None,
    swap_caption=None,
    divisor='2', divide_caption='Step 2: divide each term by 2.',
    simplify_captions=(None, None, None),
    answer=('y', '>', '-3x', '-', '4'),
    top_answer=None,
    m='m = -3', b='b = -4',
    closing=None,
    marks_file='slope_intercept_move_constant_marks.json',
    rise_run=(-3, 1), intercept=-4, window=(-4, 4, -8, 2),
)


def tex(*parts, size=MATH_SIZE, color=INK):
    return mathtex(*parts, font_size=size, color=color)


def under(term, text, color=OP_COLOR, size=54, buff=.3):
    return tex(text, size=size, color=color).next_to(term, DOWN, buff=buff)


class SlopeInterceptForm(Narrated, Scene):
    caption_color = PAPER_MUTED
    problem = NEGATIVE_SLOPE

    def say(self, words):
        if words:  # a None caption means the beat plays silently
            super().say(words)

    def goal(self):
        self.say('Goal: rewrite the equation in slope-intercept form.')
        form = tex('y', '=', 'm', 'x', '+', 'b', size=96).move_to([0, 1.5, 0])
        form[2].set_color(X_COLOR)
        form[5].set_color(OP_COLOR)
        slope = label('m is the slope', font_size=30, color=X_COLOR)
        intercept = label('b is the y-intercept', font_size=30, color=OP_COLOR)
        names = VGroup(slope, intercept).arrange(DOWN, buff=.3).move_to([0, .05, 0])
        self.play(Write(form), run_time=1.4)
        self.play(FadeIn(names, shift=UP * .15), run_time=.9)
        self.wait(2.)
        self.mark('goal')

        relation = self.problem.start[2]
        if relation != '=':
            self.say('This is an inequality, so keep the inequality sign where the = goes.')
            kept = tex(relation, size=96).move_to(form[1])
            self.play(ReplacementTransform(form[1], kept), run_time=1.)
            form.submobjects[1] = kept
            self.wait(1.8)
            self.mark('keep_inequality')

        self.say(self.problem.sides_caption)
        lines = [self.problem.first_step,
                 '2.  Divide every term by the number next to y']
        if relation != '=':
            lines.append('If that number is negative, flip the inequality sign')
        steps = VGroup(*[label(words, font_size=32, color=INK) for words in lines])
        steps.arrange(DOWN, aligned_edge=[-1, 0, 0], buff=.35)
        if len(steps) == 3:  # the flip rule belongs to step 2, so it sits indented under it
            steps[2].shift([.55, 0, 0])
        steps.move_to([0, -2.1, 0])
        self.wait(1.)
        for step in steps:
            self.play(FadeIn(step, shift=UP * .15), run_time=.9)
            self.wait(1.2)
        self.wait(1.)
        self.mark('plan')
        self.play(FadeOut(form), FadeOut(names), FadeOut(steps), run_time=.8)

    def move_x(self):
        p = self.problem
        self.say("Let's try it." if p.intro else p.op_caption)
        moved_at = p.x_at if p.moved_at is None else p.moved_at
        start = tex(*p.start).move_to([0, TOP_Y, 0])
        moved, y_start, right_start = start[moved_at], start[1 - moved_at], start[3]
        start[p.x_at].set_color(X_COLOR)
        self.play(Write(start), run_time=1.4)
        self.wait(1.)
        self.mark('start')

        if p.intro:
            self.say(p.op_caption)
        op_left = under(moved, p.op)
        op_right = under(right_start, p.op)
        self.play(FadeIn(op_left, shift=DOWN * .15), run_time=.9)
        self.play(FadeIn(op_right, shift=DOWN * .15), run_time=.9)
        self.wait(1.4)
        self.mark('move_x')

        self.say(p.cancel_caption)
        strikes = VGroup(*[
            Line(term.get_corner([-1, -1, 0]) + [-.08, -.05, 0],
                 term.get_corner([1, 1, 0]) + [.08, .05, 0],
                 color=PAPER_RED, stroke_width=6)
            for term in (moved, op_left)
        ])
        self.play(Create(strikes[0]), run_time=.6)
        self.play(Create(strikes[1]), run_time=.6)
        self.wait(.6)
        # The whole second line is centered, so build it once and split it into sides.
        y_term = p.start[1 - moved_at]
        line = tex(y_term, p.start[2], *p.right).move_to([0, ROW2_Y, 0])
        line[2 if 'x' in p.right[0] else 4].set_color(X_COLOR)
        left, right = VGroup(line[0], line[1]), VGroup(line[2], line[3], line[4])
        self.play(copy_into(y_start, left[0]), FadeIn(left[1]), run_time=1.2)
        self.wait(.8)

        self.say(p.like_caption)
        self.play(copy_into(right_start, right[0]), run_time=1.)
        self.play(copy_into(op_right, VGroup(right[1], right[2])), run_time=1.)
        self.wait(1.6)
        self.mark('not_like_terms')

        if p.swapped:
            self.row = VGroup(left[0], left[1], *self.swap(y_term, right))
        else:
            self.row = VGroup(*line)
        self.play(FadeOut(start), FadeOut(op_left), FadeOut(op_right), FadeOut(strikes),
                  self.row.animate.move_to([0, TOP_Y, 0]),
                  run_time=1.4, rate_func=smooth)
        self.wait(.6)

    def swap(self, y_term, right):
        """Write the right side x term first; returns its three new pieces."""
        p = self.problem
        self.say(p.swap_caption)
        swapped = tex(y_term, p.start[2], *p.swapped).move_to([0, ROW2_Y, 0])
        swapped[2].set_color(X_COLOR)
        self.play(ReplacementTransform(right[2], swapped[2], path_arc=-2.2),
                  ReplacementTransform(right[0], swapped[4], path_arc=-2.2),
                  ReplacementTransform(right[1], swapped[3]), run_time=1.4)
        self.wait(1.6)
        self.mark('x_moved')
        return swapped[2], swapped[3], swapped[4]

    def divide(self):
        p = self.problem
        y_term, eq, x_term, sign, const = self.row
        step_words = p.divide_caption or f'Step 2: divide by {p.divisor}, the number next to y.'
        self.say(step_words)
        bar_y = self.row.get_bottom()[1] - .15
        bars, divisors = VGroup(), VGroup()
        for term in (y_term, x_term, const):
            body = unsigned(term)
            bars.add(Line([body.get_left()[0] - .08, bar_y, 0],
                          [body.get_right()[0] + .08, bar_y, 0], color=INK, stroke_width=4))
            divisor = tex(p.divisor, size=60, color=OP_COLOR).move_to([0, bar_y - .5, 0])
            divisor.shift([body.get_x() - unsigned(divisor[0]).get_x(), 0, 0])
            divisors.add(divisor)
        for bar, divisor in zip(bars, divisors):
            self.play(Create(bar), FadeIn(divisor, shift=DOWN * .15), run_time=.8)
        self.wait(.8)
        if not p.brief:
            self.say(f'Make sure you divide EVERY term by {p.divisor}, not just the y term.')
            self.play(*[Indicate(d, color=OP_COLOR, scale_factor=1.25) for d in divisors],
                      run_time=1.2)
            self.wait(1.6)
        self.mark('divide_every_term')

        answer = tex(*p.answer, size=80)
        answer[2].set_color(X_COLOR)
        answer.move_to([0, -.95, 0])

        y_words, x_words, const_words = p.simplify_captions
        self.say(y_words)
        flips = answer[1].get_tex_string() != eq.get_tex_string()
        self.play(copy_into(VGroup(y_term, divisors[0]), answer[0]),
                  *([] if flips else [FadeIn(answer[1])]), run_time=1.3)
        self.wait(1.)
        if flips:
            self.say(f'We divided by a negative, {p.divisor}, so flip the inequality sign.')
            self.play(Indicate(eq, color=PAPER_RED, scale_factor=1.4), run_time=1.)
            answer[1].set_color(PAPER_RED)
            self.play(copy_into(eq, answer[1]), run_time=1.2)
            self.wait(1.6)
            self.mark('flip')
            self.play(answer[1].animate.set_color(INK), run_time=.5)
            if p.brief:  # the flip is done; the rest is still step 2
                self.say(step_words)
        self.say(x_words)
        self.play(copy_into(VGroup(x_term, divisors[1]), answer[2]), run_time=1.3)
        self.wait(1.4)
        self.say(const_words)
        self.play(copy_into(VGroup(sign, const, divisors[2]), VGroup(answer[3], answer[4])),
                  run_time=1.3)
        self.wait(1.6)
        self.mark('simplified')
        self.answer = answer

    def negative_on_top(self):
        # Chase's convention: the negative rides on the top number, so every slope reads
        # the same way when graphing. No reason given on screen -- students see it.
        self.say('Move the negative to the top number.')
        answer = tex(*self.problem.top_answer, size=80)
        answer[2].set_color(X_COLOR)
        answer.move_to(self.answer)
        self.play(*[ReplacementTransform(old, new) for old, new in zip(self.answer, answer)],
                  run_time=1.3)
        self.wait(1.6)
        self.mark('negative_on_top')
        self.answer = answer

    def finish(self):
        p = self.problem
        if p.top_answer:
            self.negative_on_top()
        answer = self.answer
        self.say(None if p.brief else "That's slope-intercept form.")
        box = SurroundingRectangle(answer, color=INK, buff=.25, stroke_width=4)
        self.box = box
        self.play(Create(box), run_time=.9)
        self.wait(.6)
        if p.brief:
            self.wait(1.)
            self.mark('answer')
            return
        slope = tex(p.m, size=46, color=X_COLOR)
        intercept = tex(p.b, size=46, color=OP_COLOR)
        slope_word = label('slope', font_size=28, color=X_COLOR)
        intercept_word = label('y-intercept', font_size=28, color=OP_COLOR)
        left = VGroup(slope, slope_word).arrange(buff=.25)
        right = VGroup(intercept, intercept_word).arrange(buff=.25)
        VGroup(left, right).arrange(buff=1.).next_to(box, DOWN, buff=.3)
        self.say(p.closing)
        self.play(Indicate(answer[2], color=X_COLOR), FadeIn(left, shift=UP * .15), run_time=1.1)
        self.play(Indicate(VGroup(answer[3], answer[4]), color=OP_COLOR),
                  FadeIn(right, shift=UP * .15), run_time=1.1)
        self.wait(2.5)
        self.mark('answer')

    def graph(self):
        # An inequality ends on its graph: dashed or solid by the sign, shaded above or below.
        p = self.problem
        relation = self.answer[1].get_tex_string()
        if relation == '=':
            return
        strict = relation in ('<', '>')
        above = relation in ('>', r'\geq')
        keep = set(VGroup(self.answer, self.box).get_family())
        others = [m for m in self.mobjects if m not in keep and m is not self.note]
        self.say('Now graph it.')
        self.play(*[FadeOut(m) for m in others],
                  VGroup(self.answer, self.box).animate.scale(.72).move_to([-3.7, 1.7, 0]),
                  run_time=1.2)

        x_lo, x_hi, y_lo, y_hi = p.window
        unit = GRAPH_HEIGHT / (y_hi - y_lo)  # same unit both ways, so the slope looks true
        axes = Axes(x_range=[x_lo, x_hi, 1], y_range=[y_lo, y_hi, 1],
                    x_length=unit * (x_hi - x_lo), y_length=GRAPH_HEIGHT, tips=False, axis_config={'color': PAPER_MUTED, 'stroke_width': 2,
                                             'tick_size': .05})
        axes.move_to([0, -.45, 0]).shift([GRAPH_RIGHT - axes.get_right()[0], 0, 0])
        self.play(Create(axes), run_time=1.)
        b = p.intercept
        start = Dot(axes.c2p(0, b), color=OP_COLOR, radius=.09)
        self.say(f'Start at the y-intercept, {b:g}.')
        self.play(FadeIn(start, scale=1.5), run_time=.7)
        self.wait(1.)

        rise, run = p.rise_run
        corner, end = axes.c2p(0, b + rise), axes.c2p(run, b + rise)
        steps = VGroup(Arrow(axes.c2p(0, b), corner, buff=0, color=X_COLOR, stroke_width=5),
                       Arrow(corner, end, buff=0, color=X_COLOR, stroke_width=5))
        rise_label = tex(f'{rise:g}', size=42, color=X_COLOR).next_to(steps[0], [-1, 0, 0], buff=.12)
        run_label = tex(f"{run:g}", size=42, color=X_COLOR).next_to(
            steps[1], DOWN if rise < 0 else UP, buff=.12)  # outside the rise-run triangle
        way = 'down' if rise < 0 else 'up'
        self.say(f'The slope is {rise:g}/{run:g}: go {way} {abs(rise):g}, then right {run:g}.')
        self.play(Create(steps[0]), FadeIn(rise_label), run_time=.9)
        self.play(Create(steps[1]), FadeIn(run_label), run_time=.9)
        self.play(FadeIn(Dot(end, color=OP_COLOR, radius=.09), scale=1.5), run_time=.5)
        self.wait(1.)

        slope = rise / run
        box = [(x_lo, y_lo), (x_hi, y_lo), (x_hi, y_hi), (x_lo, y_hi)]
        a, z = [axes.c2p(*corner) for corner in line_through_box(slope, b, p.window)]
        sign = {'<': '<', '>': '>', r'\leq': '≤', r'\geq': '≥'}[relation]
        if strict:
            self.say(f'The sign is {sign}, with no equal part, so the line is dashed.')
            line = DashedLine(a, z, color=INK, stroke_width=5, dash_length=.18)
        else:
            self.say(f'The sign is {sign}, so the line itself counts: draw it solid.')
            line = Line(a, z, color=INK, stroke_width=5)
        line_note = label('dashed line' if strict else 'solid line', font_size=30, color=INK)
        line_note.move_to([-3.7, -.1, 0])
        self.play(Create(line), FadeIn(line_note), run_time=1.3)
        self.wait(1.4)
        self.mark('line')

        side = [(x, y) for x, y in half_plane(box, slope, b, above)]
        shade = Polygon(*[axes.c2p(x, y) for x, y in side],
                        stroke_width=0, fill_color=X_COLOR, fill_opacity=.18)
        shade_words = ('greater than' if above else 'less than') + ('' if strict else ' or equal to')
        self.say(f'y is {shade_words} the line, so shade {"above" if above else "below"} it.')
        shade_note = label(f'shade {"above" if above else "below"}', font_size=30, color=X_COLOR)
        shade_note.next_to(line_note, DOWN, buff=.35)
        self.bring_to_back(shade)
        self.play(FadeIn(shade), FadeIn(shade_note), run_time=1.3)
        self.wait(4.)
        self.mark('graph')

    def construct(self):
        if self.problem.intro:
            self.goal()
        self.move_x()
        self.divide()
        self.finish()
        self.graph()
        self.write_marks(self.problem.marks_file)


class SlopeInterceptYFirst(SlopeInterceptForm):
    """-2y + 5x = -8: the x term sits second, and the slope comes out positive."""
    problem = Y_FIRST


class SlopeInterceptMoveConstant(SlopeInterceptForm):
    """2y + 8 > -6x: x is already across from y, so the 8 moves; divide by 2, no flip."""
    problem = MOVE_CONSTANT
