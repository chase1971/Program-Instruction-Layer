"""Part 3: what a sampling distribution is, built from samples of four rolls."""

import math
import random

from manim import (
    Scene, MathTex, VGroup, Line, Dot, FunctionGraph, FadeIn, FadeOut, Create,
    Write, Transform, LaggedStart, UP, DOWN, LEFT, RIGHT, config,
)

from dice import pair
from dice_stats import hx, BASE_Y, HIST_X0, HIST_PITCH, HOLD
from scene_style import Narrated, label, NAVY, INK, GOLD, BLUE, MUTED

config.background_color = NAVY

SEED = 132            # picked so 100 samples land on a clean symmetric bell
SAMPLES = 100
N = 4
SIGMA_POP = 2.415
SIGMA_MEAN = SIGMA_POP / math.sqrt(N)
BIN = .5
CENTERS = [3.5 + BIN * i for i in range(15)]
DOT_R = .075
DOT_PITCH = .17


def draw_samples():
    rng = random.Random(SEED)
    return [[(rng.randint(1, 6), rng.randint(1, 6)) for _ in range(N)]
            for _ in range(SAMPLES)]


def mean_of(rolls):
    return sum(a + b for a, b in rolls) / len(rolls)


def bin_of(value):
    return min(CENTERS, key=lambda c: abs(c - value))


def dot_y(index):
    return BASE_Y + .14 + index * DOT_PITCH


def bell(sigma, height):
    def curve(scene_x):
        total = 2 + (scene_x - HIST_X0) / HIST_PITCH
        return BASE_Y + height * math.exp(-((total - 7) ** 2) / (2 * sigma ** 2))
    return curve


class DiceSampling(Narrated, Scene):
    def construct(self):
        self.samples = draw_samples()
        self.heights = {c: 0 for c in CENTERS}
        self.stage = VGroup()
        self.definition()
        self.build_axis()
        self.first_sample()
        self.two_more()
        self.rain()
        self.compare()
        self.results()
        self.predict()
        self.tease()
        self.write_marks('dice_sampling_marks.json')

    def definition(self):
        title = label('A sampling distribution', font_size=46, color=GOLD)
        title.move_to([0, 2.45, 0])
        steps = VGroup(
            label('1.   Take a sample — here, four rolls of the pair.',
                  font_size=32, color=INK),
            label('2.   Record one number from it — the mean of those four.',
                  font_size=32, color=INK),
            label('3.   Throw the sample away and do it again. And again.',
                  font_size=32, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.62).move_to([0, .75, 0])
        punch = label('Those recorded means, piled up, are the sampling distribution.',
                      font_size=34, color=GOLD).move_to([0, -1.4, 0])
        warning = label('Not a distribution of rolls — a distribution of means.',
                        font_size=32, color=BLUE).move_to([0, -2.4, 0])

        self.play(FadeIn(title), run_time=.8)
        self.wait(.5)
        for step in steps:
            self.play(FadeIn(step, shift=UP * .2), run_time=.75)
            self.wait(.55)
        self.play(FadeIn(punch), run_time=.9)
        self.say("One number out of every sample — that's the whole idea")
        self.wait(2.4)
        self.play(FadeIn(warning), run_time=.8)
        self.say('That distinction is the part people lose')
        self.wait(2.6)
        self.mark('definition')
        self.play(FadeOut(VGroup(title, steps, punch, warning)), run_time=.7)

    def build_axis(self):
        line = Line([HIST_X0 - .7, BASE_Y, 0], [hx(12) + .7, BASE_Y, 0],
                    color=MUTED, stroke_width=2)
        ticks = VGroup(*[MathTex(str(s), color=MUTED, font_size=26)
                         .move_to([hx(s), BASE_Y - .35, 0]) for s in range(2, 13)])
        self.stage.add(line, ticks)
        self.add(self.stage)
        self.say("Let's build one, on the same axis from 2 to 12")
        self.wait(1.5)

    def drop(self, value, source):
        """Send one sample's mean down onto the axis as a dot."""
        center = bin_of(value)
        landed = Dot(radius=DOT_R, color=BLUE)
        landed.move_to([hx(center), dot_y(self.heights[center]), 0])
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
            row = 2.45 - i * .62
            panel.add(pair(a, b, size=.32, buff=.05).move_to([-1.75, row, 0]),
                      MathTex('=', str(a + b), color=INK, font_size=42)
                      .move_to([-.95, row, 0]))
        self.play(LaggedStart(*[FadeIn(m) for m in panel], lag_ratio=.16), run_time=2.4)

        value = mean_of(rolls)
        avg = MathTex(r'\bar{x}', '=', f'{value:g}', color=GOLD, font_size=54)
        avg.move_to([1.7, 1.4, 0])
        self.play(FadeIn(avg), run_time=.9)
        self.say('Four rolls boil down to one number — the mean of that sample')
        self.wait(2.2)
        self.drop(value, avg[2])
        self.play(FadeOut(panel), FadeOut(avg), run_time=.6)

    def two_more(self):
        self.say('Take another sample, and another')
        for index in (1, 2):
            rolls = self.samples[index]
            row = VGroup(*[pair(a, b, size=.26, buff=.05) for a, b in rolls])
            for i, combo in enumerate(row):
                combo.move_to([-2.7 + i * 1.8, 1.9, 0])
            value = mean_of(rolls)
            avg = MathTex(r'\bar{x} =', f'{value:g}', color=GOLD, font_size=50)
            avg.move_to([0, .85, 0])
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
            spot.move_to([hx(center), dot_y(self.heights[center]), 0])
            self.heights[center] += 1
            pending.append(spot)
        for start in range(0, len(pending), 25):
            chunk = pending[start:start + 25]
            self.stage.add(*chunk)
            self.play(LaggedStart(*[FadeIn(d, shift=UP * .3) for d in chunk],
                                  lag_ratio=.05), run_time=1.7)
        self.wait(1.4)

    def compare(self):
        self.hush()
        question = label('Same center. So what happened to the spread?',
                         font_size=31, color=INK).move_to([0, 2.5, 0])
        self.play(FadeIn(question), run_time=.6)
        self.mark('spread_question')
        self.wait(HOLD)
        self.play(FadeOut(question), run_time=.45)

        peak = dot_y(max(self.heights.values()) - 1) - BASE_Y + .25
        narrow = FunctionGraph(bell(SIGMA_MEAN, peak),
                               x_range=[HIST_X0 - .7, hx(12) + .7],
                               color=BLUE, stroke_width=5)
        # Equal area, so the wider population curve has to be correspondingly shorter.
        wide = FunctionGraph(bell(SIGMA_POP, peak * SIGMA_MEAN / SIGMA_POP),
                             x_range=[HIST_X0 - .7, hx(12) + .7],
                             color=GOLD, stroke_width=4)
        self.play(Create(narrow), run_time=1.3)
        self.say('Still sitting on 7, but much tighter than before')
        self.wait(1.5)
        self.play(Create(wide), run_time=1.3)
        self.say('Gold is a single roll of the pair. Blue is the mean of four')
        self.wait(2.6)
        self.stage.add(narrow, wide)
        self.play(FadeOut(self.stage), run_time=.9)
        self.remove(self.stage)

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

        self.say('Two numbers describe what we just built — the mean of those means, and their spread')
        self.play(FadeIn(self.rows), Create(self.rule), FadeIn(self.head_left), run_time=1.2)
        self.play(FadeIn(self.got_mean), FadeIn(self.got_sd), run_time=1.0)
        self.say('Messy numbers, because a hundred samples is a hundred samples — not infinity')
        self.wait(2.8)

    def predict(self):
        head_right = label('Predicted in advance', font_size=28, color=BLUE)
        head_right.move_to([3.5, 1.9, 0])
        recall = MathTex(r'\text{from parts 1 and 2:}\;\;\mu = 7\quad\sigma = 2.42',
                         color=MUTED, font_size=40)
        recall.move_to([0, -2.45, 0])

        self.say('Here is the point of parts 1 and 2 — they let us predict both, in advance')
        self.play(FadeIn(head_right), FadeIn(recall), run_time=1.1)
        self.wait(2.2)

        pred_mean = MathTex('7', color=BLUE, font_size=54).move_to([3.5, .7, 0])
        near_mean = MathTex(r'\approx', color=MUTED, font_size=46).move_to([1.1, .7, 0])
        self.play(FadeIn(pred_mean), run_time=.8)
        self.play(FadeIn(near_mean), run_time=.5)
        self.say(f'The population mean carries straight across, and {self.observed:.3f} sits right on it')
        self.wait(2.6)

        naive = MathTex('2.42', color=BLUE, font_size=54).move_to([3.5, -.9, 0])
        self.play(FadeIn(naive), run_time=.8)
        self.say('So does the spread carry across the same way?')
        self.mark('sigma_question')
        self.wait(HOLD)

        strike = Line(naive.get_left() + LEFT * .18, naive.get_right() + RIGHT * .18,
                      color=GOLD, stroke_width=7)
        self.play(Create(strike), run_time=.7)
        self.say(f'No. 2.42 against {self.spread:.3f} is not close to anything')
        self.wait(2.6)
        self.play(FadeOut(naive), FadeOut(strike), run_time=.6)

        self.say('Averaging four rolls pulls the spread in — and dividing by root n is what measures that')
        fixed = MathTex('1.21', color=BLUE, font_size=54).move_to([3.5, -.9, 0])
        work = MathTex(r'\frac{\sigma}{\sqrt{n}} = \frac{2.42}{\sqrt{4}} = 1.21',
                       color=BLUE, font_size=40).move_to([3.5, -2.5, 0])
        near_sd = MathTex(r'\approx', color=MUTED, font_size=46).move_to([1.1, -.9, 0])
        self.play(FadeOut(recall), run_time=.5)
        self.play(FadeIn(fixed), FadeIn(work), run_time=1.0)
        self.play(FadeIn(near_sd), run_time=.5)
        self.wait(2.4)

        self.say(f'1.21 against {self.spread:.3f} — that one lines up')
        self.mark('prediction_fixed')
        self.wait(2.6)

        closing = VGroup(
            label('The blue column is what endlessly many samples would settle on.',
                  font_size=30, color=INK),
            label('A hundred samples got us this close to it.', font_size=30, color=INK),
        ).arrange(DOWN, buff=.35).move_to([0, -2.5, 0])
        self.play(FadeOut(work), run_time=.5)
        self.play(FadeIn(closing), run_time=.9)
        self.wait(3.0)
        self.play(FadeOut(VGroup(self.head_left, head_right, self.rule, self.rows,
                                 self.got_mean, self.got_sd, pred_mean, fixed,
                                 near_mean, near_sd, closing)), run_time=.8)
        self.hush()

    def tease(self):
        caught = label('Both predictions leaned on the population being bell-shaped.',
                       font_size=31, color=INK).move_to([0, 1.5, 0])
        coming = VGroup(
            label('Next: a population nowhere near normal —', font_size=36, color=GOLD),
            label('whose sampling distribution turns normal anyway.', font_size=36, color=GOLD),
        ).arrange(DOWN, buff=.45).move_to([0, -.4, 0])
        self.play(FadeIn(caught), run_time=.9)
        self.wait(2.2)
        self.play(FadeIn(coming), run_time=1.0)
        self.mark('part4_leadin')
        self.wait(3.0)
