"""Part 2: tip the chart into a histogram, then find the mean and standard deviation."""

import math

from manim import (
    Scene, MathTex, VGroup, Line, FunctionGraph, FadeIn, FadeOut, Create, Write,
    Transform, LEFT, RIGHT, UP, config,
)

from dice import pair
from dice_sums import (
    ways, chart_label, chart_row, count_label, chart_heads, count_total,
)
from scene_style import Narrated, label, NAVY, INK, GOLD, BLUE, MUTED

config.background_color = NAVY

HIST_X0 = -5.9
HIST_PITCH = 1.18
HIST_BASE = -2.05
BASE_Y = HIST_BASE - .16
CELL_H = .40
CELL_DIE = .30
SIGMA = 2.415
HOLD = 2.2   # every mark sits on a hold this long, so the app can stop late
SLIDE = 16   # far enough to clear the frame


def hx(total):
    return HIST_X0 + (total - 2) * HIST_PITCH


def cell_y(index):
    return HIST_BASE + .2 + index * CELL_H


def column_top(total):
    return cell_y(len(ways(total)) - 1) + .17


def bell(scene_x):
    """Normal density with the sums' own mean and sigma, scaled to the peak column."""
    total = 2 + (scene_x - HIST_X0) / HIST_PITCH
    height = column_top(7) - BASE_Y
    return BASE_Y + height * math.exp(-((total - 7) ** 2) / (2 * SIGMA ** 2))


class DiceStats(Narrated, Scene):
    def construct(self):
        self.stage = VGroup()
        self.open_on_part_one()
        self.tip_into_histogram()
        self.ask_distribution_type()
        self.expected_value()
        self.standard_deviation()
        self.close()
        self.write_marks('dice_stats_marks.json')

    # --- staging -------------------------------------------------------------

    def slide_off(self):
        self.play(self.stage.animate.shift(LEFT * SLIDE), run_time=.85)
        self.remove(self.stage)

    def slide_on(self):
        self.add(self.stage)
        self.play(self.stage.animate.shift(RIGHT * SLIDE), run_time=.85)

    def open_on_part_one(self):
        self.labels = {s: chart_label(s) for s in range(2, 13)}
        self.rows = {s: chart_row(s) for s in range(2, 13)}
        self.stage.add(*self.labels.values(), *self.rows.values())
        self.extras = VGroup(chart_heads(), *count_total(),
                             *[count_label(s) for s in range(2, 13)])
        self.add(self.stage, self.extras)
        self.say('36 equally likely rolls in all')
        self.wait(.9)

    # --- the chart falls over ------------------------------------------------

    def tip_into_histogram(self):
        self.say('Tip the whole chart onto its side')
        moves = [FadeOut(self.extras)]
        for total in range(2, 13):
            for i, combo in enumerate(self.rows[total]):
                target = pair(*ways(total)[i], size=CELL_DIE, buff=.04)
                target.move_to([hx(total), cell_y(i), 0])
                moves.append(Transform(combo, target))
            axis_label = MathTex(str(total), color=GOLD, font_size=30)
            axis_label.move_to([hx(total), HIST_BASE - .42, 0])
            moves.append(Transform(self.labels[total], axis_label))
        self.play(*moves, run_time=2.6)
        axis = Line([HIST_X0 - .7, BASE_Y, 0], [hx(12) + .7, BASE_Y, 0],
                    color=MUTED, stroke_width=2)
        self.play(Create(axis), run_time=.7)
        self.remove(axis)
        self.stage.add(axis)
        self.wait(.5)

    def ask_distribution_type(self):
        self.hush()
        question = label('What type of distribution is this?',
                         font_size=32, color=INK).move_to([0, 2.6, 0])
        self.play(FadeIn(question), run_time=.6)
        self.mark('distribution_question')
        self.wait(HOLD)
        self.play(FadeOut(question), run_time=.5)

        self.curve = FunctionGraph(bell, x_range=[HIST_X0 - .7, hx(12) + .7],
                                   color=GOLD, stroke_width=5)
        self.play(Create(self.curve), run_time=1.6)
        self.remove(self.curve)
        self.stage.add(self.curve)
        self.say('A normal distribution — symmetric, with its peak in the middle')
        self.wait(2.2)

    # --- the arithmetic ------------------------------------------------------

    def expected_value(self):
        self.hush()
        question = label('Now calculate the expected value of this probability distribution.',
                         font_size=31, color=INK).move_to([0, 2.6, 0])
        self.play(FadeIn(question), run_time=.6)
        self.mark('expected_value_question')
        self.wait(HOLD + .8)
        self.play(FadeOut(question), run_time=.5)
        self.slide_off()

        formula = MathTex(r'\mu', '=', r'\sum x \cdot P(x)', font_size=62)
        formula[0].set_color(GOLD)
        formula.move_to([0, 1.7, 0])
        self.play(Write(formula), run_time=1.3)
        self.say('Multiply each sum by its probability, then add all eleven together')
        self.wait(1.3)

        worked = MathTex(r'\frac{2(1) + 3(2) + 4(3) + \cdots + 12(1)}{36}',
                         font_size=46, color=MUTED).move_to([0, .25, 0])
        self.play(FadeIn(worked), run_time=1.1)
        self.wait(1.3)
        answer = MathTex('=', r'\frac{252}{36}', '=', '7', font_size=54)
        answer[3].set_color(GOLD)
        answer.move_to([0, -1.55, 0])
        self.play(Write(answer), run_time=1.4)
        self.wait(1.8)
        self.play(FadeOut(formula), FadeOut(worked), FadeOut(answer), run_time=.6)

        self.slide_on()
        centre = Line([hx(7), BASE_Y, 0], [hx(7), column_top(7) + .1, 0],
                      color=GOLD, stroke_width=4)
        self.play(Create(centre), run_time=.9)
        self.say('A normal distribution sits on its mean — and the peak is right at 7')
        self.wait(2.4)
        self.remove(centre)
        self.stage.add(centre)
        self.slide_off()

    def standard_deviation(self):
        self.say('We also want the spread')
        sigma = MathTex(r'\sigma', '=', r'\sqrt{\sum (x - \mu)^2 \cdot P(x)}', font_size=60)
        sigma[0].set_color(BLUE)
        sigma.move_to([0, .4, 0])
        self.play(Write(sigma), run_time=1.6)
        self.wait(1.6)

        result = MathTex(r'\sigma', r'\approx', '2.42', font_size=76)
        result[0].set_color(BLUE)
        result[2].set_color(BLUE)
        result.move_to([0, .4, 0])
        self.play(FadeOut(sigma), FadeIn(result), run_time=1.3)
        self.say('Straight out of the formula — no need to grind through it by hand')
        self.wait(2.2)
        self.play(FadeOut(result), run_time=.6)

    def close(self):
        card = VGroup(MathTex(r'\mu = 7', font_size=76, color=GOLD),
                      MathTex(r'\sigma \approx 2.42', font_size=76, color=BLUE))
        card[0].move_to([-2.6, .6, 0])
        card[1].move_to([2.6, .6, 0])
        self.play(FadeIn(card, shift=UP * .3), run_time=1.2)
        self.say('Rolling two dice, that is what theory predicts')
        self.wait(2.4)
        self.say('Next: what a sampling distribution is, and what changes')
        self.mark('part3_leadin')
        self.wait(3.2)
