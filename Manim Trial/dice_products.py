"""Part 4: the product of two dice — a spiky, gap-riddled, badly skewed population
whose sampling distribution still goes bell-shaped."""

import math
import random
from collections import Counter

from manim import (
    Scene, MathTex, VGroup, Line, DashedLine, Dot, RoundedRectangle, FunctionGraph,
    FadeIn, FadeOut, Create, Write, LaggedStart, Transform, UP, DOWN, LEFT, RIGHT,
    config,
)

from dice import die
from dice_stats import BASE_Y, HOLD, SLIDE
from scene_style import Narrated, label, NAVY, INK, GOLD, BLUE, MUTED

config.background_color = NAVY

SEED = 429            # chosen out of 600 candidates; see PART4_PLAN.md before changing
SAMPLES = 100
N = 4
MU_POP = 12.25
SIGMA_POP = 8.9423
SIGMA_MEAN = SIGMA_POP / math.sqrt(N)

# The value range is 1 to 36 now, so the axis is the one thing that changes from parts 2-3.
PROD_X0 = -5.9
PROD_PITCH = 11.8 / 35
AXIS_LABELS = (1, 6, 12, 18, 24, 30, 36)
GAPS = (7, 11, 13)
CELL_H = .40
CELL_W = .26

BIN = 2.
CENTERS = [2. + BIN * i for i in range(13)]
DOT_R = .075
DOT_PITCH = .17

WAYS = Counter(a * b for a in range(1, 7) for b in range(1, 7))


def px(value):
    return PROD_X0 + (value - 1) * PROD_PITCH


def cell_y(index):
    return BASE_Y + .22 + index * CELL_H


def dot_y(index):
    return BASE_Y + .14 + index * DOT_PITCH


def bin_of(value):
    return min(CENTERS, key=lambda c: abs(c - value))


def bell(sigma, height):
    def curve(scene_x):
        value = 1 + (scene_x - PROD_X0) / PROD_PITCH
        return BASE_Y + height * math.exp(-((value - MU_POP) ** 2) / (2 * sigma ** 2))
    return curve


def times_row(first, second, size=.5, font_size=44):
    """One die times another, with the product spelled out — white first, blue second."""
    row = VGroup(die(first, size, INK),
                 MathTex(r'\times', color=MUTED, font_size=font_size),
                 die(second, size, BLUE),
                 MathTex('=', color=MUTED, font_size=font_size),
                 MathTex(str(first * second), color=GOLD, font_size=font_size + 8))
    row.arrange(RIGHT, buff=size * .28)
    return row


def draw_samples():
    rng = random.Random(SEED)
    return [[(rng.randint(1, 6), rng.randint(1, 6)) for _ in range(N)]
            for _ in range(SAMPLES)]


def mean_of(rolls):
    return sum(a * b for a, b in rolls) / len(rolls)


class DiceProducts(Narrated, Scene):
    def construct(self):
        self.samples = draw_samples()
        self.heights = {c: 0 for c in CENTERS}
        self.stage = VGroup()
        self.pay_off_the_hook()
        self.build_axis()
        self.multiply_instead()
        self.fill_population()
        self.sit_on_the_gaps()
        self.parameters()
        self.ask_the_question()
        self.first_sample()
        self.two_more()
        self.rain()
        self.compare()
        self.results()
        self.predict()
        self.land_it()
        self.write_marks('dice_products_marks.json')

    # --- staging -------------------------------------------------------------

    def slide_off(self):
        self.play(self.stage.animate.shift(LEFT * SLIDE), run_time=.85)
        self.remove(self.stage)

    def slide_on(self):
        self.add(self.stage)
        self.play(self.stage.animate.shift(RIGHT * SLIDE), run_time=.85)

    # --- the setup -----------------------------------------------------------

    def pay_off_the_hook(self):
        caught = VGroup(
            label('The sum of two dice was already bell-shaped', font_size=34, color=INK),
            label('before we started. It never really tested anything.',
                  font_size=34, color=INK),
        ).arrange(DOWN, buff=.4).move_to([0, 1.5, 0])
        pick = VGroup(
            label('So pick a population that is genuinely ugly:', font_size=34, color=MUTED),
            label('multiply the two dice instead of adding them.', font_size=40, color=GOLD),
        ).arrange(DOWN, buff=.45).move_to([0, -1.1, 0])

        self.play(FadeIn(caught), run_time=1.0)
        self.wait(2.4)
        self.play(FadeIn(pick, shift=UP * .2), run_time=1.0)
        self.mark('the_switch')
        self.wait(2.8)
        self.play(FadeOut(caught), FadeOut(pick), run_time=.7)

    def build_axis(self):
        line = Line([px(1) - .7, BASE_Y, 0], [px(36) + .7, BASE_Y, 0],
                    color=MUTED, stroke_width=2)
        ticks = VGroup(*[MathTex(str(v), color=MUTED, font_size=26)
                         .move_to([px(v), BASE_Y - .35, 0]) for v in AXIS_LABELS])
        self.stage.add(line, ticks)
        self.add(self.stage)
        self.say('The products run from 1 all the way out to 36')
        self.wait(1.4)

    def multiply_instead(self):
        rows = VGroup(*[times_row(a, b) for a, b in ((1, 1), (2, 6), (3, 4), (6, 6))])
        for i, row in enumerate(rows):
            row.move_to([0, 1.85 - i * .82, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=UP * .2) for r in rows],
                              lag_ratio=.35), run_time=2.6)
        self.say('Two different rolls can land on the same product')
        self.wait(2.2)
        self.say('And 36 only happens one way — double sixes')
        self.wait(2.0)
        self.play(FadeOut(rows), run_time=.6)

    def fill_population(self):
        self.cells = VGroup()
        columns = []
        for value in sorted(WAYS):
            column = VGroup()
            for i in range(WAYS[value]):
                brick = RoundedRectangle(width=CELL_W, height=CELL_H - .09,
                                         corner_radius=.045, fill_color=GOLD,
                                         fill_opacity=1, stroke_width=0)
                brick.move_to([px(value), cell_y(i), 0])
                column.add(brick)
            columns.append(column)
            self.cells.add(column)
        self.say('All 36 rolls, stacked over the product each one makes')
        for start in range(0, len(columns), 6):
            chunk = columns[start:start + 6]
            self.play(LaggedStart(*[FadeIn(c, shift=UP * .25) for c in chunk],
                                  lag_ratio=.18), run_time=1.5)
        self.stage.add(self.cells)
        self.wait(1.2)

    def sit_on_the_gaps(self):
        self.say('Spiky, lopsided, and full of holes — nothing like a bell')
        self.wait(2.4)
        # The lines have to clear the tallest column, or they read as bricks themselves.
        markers = VGroup()
        for value in GAPS:
            markers.add(DashedLine([px(value), BASE_Y, 0], [px(value), BASE_Y + 1.8, 0],
                                   color=INK, stroke_width=2.5, stroke_opacity=.85,
                                   dash_length=.1),
                        MathTex(str(value), color=INK, font_size=32)
                        .move_to([px(value), BASE_Y + 2.1, 0]))
        self.play(LaggedStart(*[FadeIn(m) for m in markers], lag_ratio=.18), run_time=1.4)
        self.say('No 7. No 11. No 13. Eighteen values never come up at all')
        self.mark('the_gaps')
        self.wait(3.2)
        self.play(FadeOut(markers), run_time=.6)

    def parameters(self):
        self.say('The two formulas do not care how ugly the picture is')
        self.wait(1.6)
        self.slide_off()

        mu = MathTex(r'\mu', '=', r'\sum x \cdot P(x)', font_size=62)
        mu[0].set_color(GOLD)
        mu.move_to([0, 1.5, 0])
        self.play(Write(mu), run_time=1.3)
        self.wait(1.4)
        mu_answer = MathTex(r'\mu', '=', '12.25', font_size=76)
        mu_answer[0].set_color(GOLD)
        mu_answer[2].set_color(GOLD)
        mu_answer.move_to([0, 1.5, 0])
        self.play(FadeOut(mu), FadeIn(mu_answer), run_time=1.1)
        why = label('which is 3.5 squared — each die averages 3.5',
                    font_size=28, color=MUTED).move_to([0, .45, 0])
        self.play(FadeIn(why), run_time=.8)
        self.wait(2.2)

        sigma = MathTex(r'\sigma', '=', r'\sqrt{\sum (x - \mu)^2 \cdot P(x)}', font_size=58)
        sigma[0].set_color(BLUE)
        sigma.move_to([0, -1.5, 0])
        self.play(Write(sigma), run_time=1.5)
        self.wait(1.5)
        sigma_answer = MathTex(r'\sigma', r'\approx', '8.94', font_size=76)
        sigma_answer[0].set_color(BLUE)
        sigma_answer[2].set_color(BLUE)
        sigma_answer.move_to([0, -1.5, 0])
        self.play(FadeOut(sigma), FadeIn(sigma_answer), run_time=1.1)
        self.say('Straight out of the formula — a huge spread, and no wonder')
        self.wait(2.6)
        self.play(FadeOut(mu_answer), FadeOut(why), FadeOut(sigma_answer), run_time=.7)
        self.slide_on()

    def ask_the_question(self):
        self.hush()
        question = VGroup(
            label('This population is nowhere near normal.', font_size=34, color=INK),
            label('So what shape will its sampling distribution be?',
                  font_size=34, color=INK),
        ).arrange(DOWN, buff=.38).move_to([0, 1.9, 0])
        self.play(FadeIn(question), run_time=.7)
        self.mark('shape_question')
        self.wait(HOLD + .8)
        self.play(FadeOut(question), run_time=.5)
        self.play(FadeOut(self.cells), run_time=.9)
        self.stage.remove(self.cells)
        self.remove(self.cells)

    # --- the sampling distribution -------------------------------------------

    def drop(self, value, source):
        """Send one sample's mean down onto the axis as a dot."""
        center = bin_of(value)
        landed = Dot(radius=DOT_R, color=BLUE)
        landed.move_to([px(center), dot_y(self.heights[center]), 0])
        self.heights[center] += 1
        flying = Dot(radius=DOT_R, color=GOLD)
        flying.move_to(source.get_center() + DOWN * .42)
        self.add(flying)
        self.play(Transform(flying, landed), run_time=.9)
        self.remove(flying)
        self.stage.add(landed)
        self.add(landed)

    def first_sample(self):
        rolls = self.samples[0]
        panel = VGroup()
        for i, (a, b) in enumerate(rolls):
            row = times_row(a, b, size=.34, font_size=36)
            row.move_to([-2.3, 2.15 - i * .66, 0])
            # Line the four equations up on their equals signs; a two-digit
            # product otherwise pushes its whole row out of the stack.
            row.shift(RIGHT * (-1.95 - row[3].get_center()[0]))
            panel.add(row)
        self.say('Same routine as before: four rolls make one sample')
        self.play(LaggedStart(*[FadeIn(m) for m in panel], lag_ratio=.16), run_time=2.3)

        value = mean_of(rolls)
        avg = MathTex(r'\bar{x}', '=', f'{value:g}', color=GOLD, font_size=54)
        avg.move_to([2.2, 1.5, 0])
        self.play(FadeIn(avg), run_time=.9)
        self.say('Average the four products, and record that one number')
        self.wait(2.2)
        self.drop(value, avg[2])
        self.play(FadeOut(panel), FadeOut(avg), run_time=.6)

    def two_more(self):
        self.say('Take another sample, and another')
        for index in (1, 2):
            rolls = self.samples[index]
            row = VGroup(*[times_row(a, b, size=.28, font_size=32) for a, b in rolls])
            for i, combo in enumerate(row):
                combo.move_to([-4.05 + i * 2.7, 2.0, 0])
            value = mean_of(rolls)
            avg = MathTex(r'\bar{x} =', f'{value:g}', color=GOLD, font_size=50)
            avg.move_to([0, 1.0, 0])
            self.play(FadeIn(row), run_time=.7)
            self.play(FadeIn(avg), run_time=.5)
            self.drop(value, avg[1])
            self.play(FadeOut(row), FadeOut(avg), run_time=.4)

    def rain(self):
        self.say('Now do that a hundred times')
        pending = []
        for rolls in self.samples[3:]:
            center = bin_of(mean_of(rolls))
            spot = Dot(radius=DOT_R, color=BLUE)
            spot.move_to([px(center), dot_y(self.heights[center]), 0])
            self.heights[center] += 1
            pending.append(spot)
        for start in range(0, len(pending), 25):
            chunk = pending[start:start + 25]
            self.stage.add(*chunk)
            self.play(LaggedStart(*[FadeIn(d, shift=UP * .3) for d in chunk],
                                  lag_ratio=.05), run_time=1.7)
        self.say('Out of a population with holes in it — a bell')
        self.mark('the_bell')
        self.wait(2.8)

    def compare(self):
        peak = dot_y(max(self.heights.values()) - 1) - BASE_Y + .25
        narrow = FunctionGraph(bell(SIGMA_MEAN, peak),
                               x_range=[px(1) - .7, px(36) + .7],
                               color=BLUE, stroke_width=5)
        # Equal area, so the far wider population curve has to be correspondingly shorter.
        wide = FunctionGraph(bell(SIGMA_POP, peak * SIGMA_MEAN / SIGMA_POP),
                             x_range=[px(1) - .7, px(36) + .7],
                             color=GOLD, stroke_width=4)
        self.play(Create(narrow), run_time=1.3)
        self.say('Centered near 12.25, and far tighter than the population')
        self.wait(1.8)
        self.play(Create(wide), run_time=1.4)
        self.say('Gold is one product. Blue is the mean of four — same area, same axis')
        self.wait(2.8)
        self.hush()
        # The caption is hushed, so this can ride high — the blue curve peaks near y = 1.4.
        honest = VGroup(
            label('Look closely: the blue leans a little to the right.',
                  font_size=30, color=INK),
            label('Four draws from a population this skewed gets you close',
                  font_size=30, color=MUTED),
            label('to normal — not perfectly there.', font_size=30, color=MUTED),
        ).arrange(DOWN, buff=.28).move_to([0, 2.55, 0])
        self.play(FadeIn(honest), run_time=.9)
        self.mark('the_honest_tail')
        self.wait(3.4)
        self.play(FadeOut(honest), run_time=.5)
        self.stage.add(narrow, wide)
        self.play(FadeOut(self.stage), run_time=.9)
        self.remove(self.stage)

    # --- predict then check --------------------------------------------------

    def results(self):
        """The experiment's own numbers, before any theory is brought in."""
        values = [mean_of(rolls) for rolls in self.samples]
        self.observed = sum(values) / len(values)
        self.spread = math.sqrt(sum((v - self.observed) ** 2 for v in values)
                                / (len(values) - 1))

        self.head_left = label('Our 100 samples', font_size=28, color=GOLD)
        self.head_left.move_to([-1.3, 1.9, 0])
        self.rule = Line([-6.1, 1.5, 0], [6.1, 1.5, 0], color=MUTED, stroke_width=1.5)
        self.rows = VGroup(
            MathTex(r'\mu_{\bar{x}}', color=MUTED, font_size=54).move_to([-4.8, .7, 0]),
            MathTex(r'\sigma_{\bar{x}}', color=MUTED, font_size=54).move_to([-4.8, -.9, 0]),
        )
        self.got_mean = MathTex(f'{self.observed:.3f}', color=GOLD, font_size=54)
        self.got_mean.move_to([-1.3, .7, 0])
        self.got_sd = MathTex(f'{self.spread:.3f}', color=GOLD, font_size=54)
        self.got_sd.move_to([-1.3, -.9, 0])

        self.say('The same two numbers describe what the dots just built')
        self.play(FadeIn(self.rows), Create(self.rule), FadeIn(self.head_left), run_time=1.2)
        self.play(FadeIn(self.got_mean), FadeIn(self.got_sd), run_time=1.0)
        self.wait(2.4)

    def predict(self):
        head_right = label('Predicted in advance', font_size=28, color=BLUE)
        head_right.move_to([3.5, 1.9, 0])
        recall = MathTex(r'\text{the population:}\;\;\mu = 12.25\quad\sigma = 8.94',
                         color=MUTED, font_size=40)
        recall.move_to([0, -2.45, 0])

        self.say('And that ugly population still predicts both of them')
        self.play(FadeIn(head_right), FadeIn(recall), run_time=1.1)
        self.wait(2.0)

        pred_mean = MathTex('12.25', color=BLUE, font_size=54).move_to([3.5, .7, 0])
        near_mean = MathTex(r'\approx', color=MUTED, font_size=46).move_to([1.1, .7, 0])
        self.play(FadeIn(pred_mean), run_time=.8)
        self.play(FadeIn(near_mean), run_time=.5)
        self.say(f'The population mean carries straight across — {self.observed:.3f} sits on it')
        self.wait(2.6)

        naive = MathTex('8.94', color=BLUE, font_size=54).move_to([3.5, -.9, 0])
        self.play(FadeIn(naive), run_time=.8)
        self.say('So does the spread carry across the same way?')
        self.mark('sigma_question')
        self.wait(HOLD)

        strike = Line(naive.get_left() + LEFT * .18, naive.get_right() + RIGHT * .18,
                      color=GOLD, stroke_width=7)
        self.play(Create(strike), run_time=.7)
        self.say(f'No — 8.94 against {self.spread:.3f} is not close to anything')
        self.wait(2.6)
        self.play(FadeOut(naive), FadeOut(strike), run_time=.6)

        self.say('Averaging four still pulls the spread in by root n')
        fixed = MathTex('4.47', color=BLUE, font_size=54).move_to([3.5, -.9, 0])
        work = MathTex(r'\frac{\sigma}{\sqrt{n}} = \frac{8.94}{\sqrt{4}} = 4.47',
                       color=BLUE, font_size=40).move_to([3.5, -2.5, 0])
        near_sd = MathTex(r'\approx', color=MUTED, font_size=46).move_to([1.1, -.9, 0])
        self.play(FadeOut(recall), run_time=.5)
        self.play(FadeIn(fixed), FadeIn(work), run_time=1.0)
        self.play(FadeIn(near_sd), run_time=.5)
        self.wait(2.2)

        self.say(f'4.47 against {self.spread:.3f} — on a population it was never promised')
        self.mark('prediction_holds')
        self.wait(3.2)
        self.play(FadeOut(VGroup(self.head_left, head_right, self.rule, self.rows,
                                 self.got_mean, self.got_sd, pred_mean, fixed, work,
                                 near_mean, near_sd)), run_time=.8)
        self.hush()

    def land_it(self):
        recap = VGroup(
            label('The population was spiky, gappy and skewed.', font_size=34, color=INK),
            label('The sampling distribution went bell-shaped anyway,',
                  font_size=34, color=INK),
            label('and both formulas still landed.', font_size=34, color=INK),
        ).arrange(DOWN, buff=.34).move_to([0, 1.6, 0])
        name = label('The Central Limit Theorem', font_size=52, color=GOLD)
        name.move_to([0, -.45, 0])
        why = VGroup(
            label('It is why the normal curve turns up everywhere —',
                  font_size=32, color=MUTED),
            label('you are almost never looking at raw values.', font_size=32, color=MUTED),
            label('You are looking at averages.', font_size=32, color=BLUE),
        ).arrange(DOWN, buff=.3).move_to([0, -2.1, 0])

        self.play(FadeIn(recap), run_time=1.1)
        self.wait(3.0)
        self.play(FadeIn(name, shift=UP * .2), run_time=1.0)
        self.mark('the_theorem')
        self.wait(2.6)
        self.play(FadeIn(why), run_time=1.0)
        self.wait(3.6)
