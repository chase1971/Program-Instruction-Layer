"""A caption line with real LaTeX inside it: `Solve for $x$. Then $x+4$ is linear.`

Everything between a pair of dollar signs is set with MathTex; the words around it are set
with the caption font. Words wrap at `max_width` and each line is centered, so a caption that
mentions a variable or a number looks the same as one that does not.

Math is scaled so its x-height matches the caption font's, and every piece sits on one shared
baseline (a word with a descender, like "square", is not centered on its box).

`$@b g$` sets that math in the accent colour (blue: the colour g wears on the board).

Used by `scene_style.label()` whenever the caption text contains a `$`.
"""

import re

from manim import DOWN, MathTex, Text, VGroup

SUPERSAMPLE = 4
LINE_GAP = 0.14
ACCENT_MARK = '@b '
ACCENT = '#1565C0'  # PAPER_BLUE
MATH_DESCENDERS = set('fgjpqy,;()[]|')

CHUNK = re.compile(r'(?:\$[^$]*\$|[^\s$])+')
PIECE = re.compile(r'(\$[^$]*\$)')


def _text(words, font_size, color):
    return Text(words, font='Segoe UI', font_size=font_size * SUPERSAMPLE,
                color=color).scale(1 / SUPERSAMPLE)


class _Metrics:
    """Sizes measured once per caption: the math scale and how far descenders hang."""

    def __init__(self, font_size, color):
        text_x = _text('x', font_size, color)
        math_x = MathTex('x', font_size=font_size)
        self.math_size = font_size * text_x.height / math_x.height
        self.text_desc = _text('g', font_size, color).height - text_x.height
        math_g = MathTex('g', font_size=self.math_size)
        self.math_desc = math_g.height - MathTex('x', font_size=self.math_size).height
        self.space = text_x.width * 0.9


LEVELLED = str.maketrans({'g': 'o', 'p': 'o', 'q': 'o', 'y': 'o', 'j': 'i', ',': '.', ';': '.'})


def _text_depth(piece, font_size, color):
    """How far a plain-text piece hangs below its baseline: its height minus the height it
    would have with every descender swapped for a letter that sits on the baseline."""
    levelled = piece.translate(LEVELLED)
    if levelled == piece:
        return 0.0
    return _text(piece, font_size, color).height - _text(levelled, font_size, color).height


def _sit_on_baseline(piece, depth):
    """Move `piece` so its baseline is y = 0 (a descender hangs below it)."""
    piece.align_to([0, -depth, 0], DOWN)
    return piece


def _word(chunk, font_size, color, metrics):
    """One whitespace-free chunk: plain pieces and $math$ pieces glued on one baseline."""
    pieces = []
    for piece in PIECE.split(chunk):
        if not piece:
            continue
        if piece.startswith('$'):
            body, tint = piece[1:-1], color
            if body.startswith(ACCENT_MARK):
                body, tint = body[len(ACCENT_MARK):], ACCENT
            mob = MathTex(body, font_size=metrics.math_size, color=tint)
            _sit_on_baseline(mob, metrics.math_desc if MATH_DESCENDERS & set(body) else 0.0)
        else:
            mob = _text(piece, font_size, color)
            _sit_on_baseline(mob, _text_depth(piece, font_size, color))
        pieces.append(mob)
    cursor = 0.0
    for mob in pieces:
        mob.shift([cursor - mob.get_left()[0], 0, 0])
        cursor = mob.get_right()[0] + 0.015
    return VGroup(*pieces)


def math_caption(words, font_size, color, max_width):
    metrics = _Metrics(font_size, color)
    chunks = [_word(chunk, font_size, color, metrics) for chunk in CHUNK.findall(words)]
    lines, line, width = [], [], 0.0
    for chunk in chunks:
        needed = chunk.width + (metrics.space if line else 0)
        if line and width + needed > max_width:
            lines.append(line)
            line, width = [], 0.0
            needed = chunk.width
        line.append(chunk)
        width += needed
    lines.append(line)

    rows = []
    for line in lines:
        cursor = 0.0
        for chunk in line:
            chunk.shift([cursor - chunk.get_left()[0], 0, 0])
            cursor = chunk.get_right()[0] + metrics.space
        row = VGroup(*line)
        row.shift([-row.get_center()[0], 0, 0])  # centered; y stays on the baseline
        rows.append(row)
    pitch = metrics.text_desc + _text('H', font_size, color).height + LINE_GAP
    for index, row in enumerate(rows):
        row.shift([0, -index * pitch, 0])
    block = VGroup(*rows)
    block.shift([-block.get_center()[0], -block.get_center()[1], 0])
    return block
