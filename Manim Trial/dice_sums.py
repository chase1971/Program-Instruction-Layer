"""Part 1 of the dice sampling distribution: every ordered way to roll each sum."""

from manim import (
    Scene, MathTex, VGroup, Line, FadeIn, FadeOut, GrowFromCenter, Indicate,
    LaggedStart, Transform, Create, RIGHT, config,
)

from dice import pair
from scene_style import Narrated, banner, label, NAVY, GOLD, BLUE, MUTED

config.background_color = NAVY

LABEL_X = -4.6
COMBO_X0 = -3.5
COMBO_PITCH = 1.02
COUNT_X = 3.3
# The title clears out once the chart forms, so the rows get the full height.
# Captions sit at the top now, so the whole chart hangs lower than it used to.
TOP_Y = 2.15
ROW_PITCH = .47
CHART_DIE = .38

BIG = .8
BIG_LABEL_X = -2.6
BIG_X0 = -.6
BIG_PITCH = 2.5


def ways(total):
    """Ordered (first, second) rolls that add to `total`."""
    return [(a, total - a) for a in range(1, 7) if 1 <= total - a <= 6]


def row_y(total):
    return TOP_Y - (total - 2) * ROW_PITCH


def chart_label(total):
    return MathTex(str(total), color=GOLD, font_size=34).move_to([LABEL_X, row_y(total), 0])


def chart_row(total):
    row = VGroup()
    for i, (first, second) in enumerate(ways(total)):
        combo = pair(first, second, size=CHART_DIE, buff=.06)
        combo.move_to([COMBO_X0 + i * COMBO_PITCH, row_y(total), 0])
        row.add(combo)
    return row


def count_label(total):
    return MathTex(str(len(ways(total))), color=BLUE,
                   font_size=34).move_to([COUNT_X, row_y(total), 0])


def chart_heads():
    return VGroup(
        label('SUM', font_size=19).move_to([LABEL_X, 2.62, 0]),
        label('EVERY ROLL THAT MAKES IT', font_size=19).move_to([-.95, 2.62, 0]),
        label('WAYS', font_size=19).move_to([COUNT_X, 2.62, 0]),
    )


def count_total():
    """The rule and the 36 that close out part 1's chart."""
    rule = Line([COUNT_X - .32, -2.45, 0], [COUNT_X + .32, -2.45, 0],
                color=MUTED, stroke_width=2)
    total = MathTex('36', color=GOLD, font_size=34).move_to([COUNT_X, -2.70, 0])
    return rule, total


class DiceSums(Narrated, Scene):
    def construct(self):
        title = banner('EVERY WAY TO ROLL EACH SUM')
        self.add(title)
        self.say('Two dice. White is the first die, blue is the second')

        two_label = MathTex('2', color=GOLD, font_size=60).move_to([BIG_LABEL_X, 1.4, 0])
        two_combo = pair(1, 1, size=BIG, buff=.2).move_to([BIG_X0, 1.4, 0])
        self.play(FadeIn(two_label), GrowFromCenter(two_combo), run_time=1.1)
        self.wait(.8)
        self.say('Only one way to land on 2 — both dice have to show 1')
        self.wait(1.8)

        three_label = MathTex('3', color=GOLD, font_size=60).move_to([BIG_LABEL_X, -.35, 0])
        first = pair(1, 2, size=BIG, buff=.2).move_to([BIG_X0, -.35, 0])
        second = pair(2, 1, size=BIG, buff=.2).move_to([BIG_X0 + BIG_PITCH, -.35, 0])
        self.say('A 3 can happen two ways')
        self.play(FadeIn(three_label), GrowFromCenter(first), run_time=1)
        self.play(GrowFromCenter(second), run_time=1)
        self.wait(.8)
        self.say('White 1 with blue 2 is a different roll from white 2 with blue 1')
        self.wait(2.4)

        self.say('Line up every sum and collect all of its rolls')
        heads = chart_heads()
        rows = {2: chart_row(2), 3: chart_row(3)}
        self.play(
            Transform(two_label, chart_label(2)),
            Transform(two_combo, rows[2][0]),
            Transform(three_label, chart_label(3)),
            Transform(first, rows[3][0]),
            Transform(second, rows[3][1]),
            FadeOut(title), FadeIn(heads),
            run_time=2,
        )
        # The transformed copies now sit on the chart geometry; swap in the real rows.
        self.remove(two_label, two_combo, three_label, first, second)
        self.add(chart_label(2), rows[2], chart_label(3), rows[3])
        self.wait(.6)

        self.say('Four, five, six — the lists keep getting longer')
        for total in (4, 5, 6):
            rows[total] = chart_row(total)
            self.play(FadeIn(chart_label(total)),
                      LaggedStart(*[FadeIn(c, shift=RIGHT * .25) for c in rows[total]],
                                  lag_ratio=.25),
                      run_time=1.1)
        self.wait(.5)

        self.say('Seven is the peak — six different rolls make it')
        rows[7] = chart_row(7)
        self.play(FadeIn(chart_label(7)),
                  LaggedStart(*[FadeIn(c, shift=RIGHT * .25) for c in rows[7]],
                              lag_ratio=.18),
                  run_time=1.8)
        self.play(Indicate(rows[7], color=GOLD, scale_factor=1.06), run_time=1.2)
        self.wait(.8)

        self.say('Past seven the lists shrink back down — a mirror image')
        builds = []
        for total in range(8, 13):
            rows[total] = chart_row(total)
            builds.append(VGroup(chart_label(total), rows[total]))
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * .25) for b in builds],
                              lag_ratio=.35), run_time=3)
        self.wait(1.2)

        self.say('Count the rolls in each row')
        counts = VGroup(*[count_label(t) for t in range(2, 13)])
        self.play(LaggedStart(*[FadeIn(c) for c in counts], lag_ratio=.12), run_time=2.4)
        self.wait(1)

        rule, total_rolls = count_total()
        self.play(Create(rule), run_time=.5)
        self.play(FadeIn(total_rolls), run_time=.7)
        self.say('36 equally likely rolls in all')
        self.wait(4)
