"""Layout audit: turn "does this frame look right" into numbers, for a model with no eyes.

`Narrated.mark()` calls `audit_mark()`, so every teaching hold in every scene is checked --
a mark is exactly the moment a frame has to be readable. Findings print during the render
and land in `media/audit/<Scene>_audit.json`.

What it checks, and nothing else:

- **Text never touches text.** Every Text/MathTex/Tex box against every other, needing a
  small gap. Text-vs-shape is deliberately not checked: an Arrow's box spans its diagonal
  and a SurroundingRectangle overlaps its contents by design, so those pairs are all noise.
- **Off frame**, with a margin.
- **The caption band** along the top, which only `self.note` may enter.
- **Unreadably small type.**

Non-fatal by default: one draft render surfaces every beat's problems at once. Set
`MANIM_AUDIT_STRICT=1` to raise at the first offending mark, which gives an agent loop a
nonzero exit code to iterate against.

Every finding carries a number to act on -- which element, how far it overlaps, and the
center coordinate or `.scale()` value that fixes it.
"""

import json
import math
import os
from pathlib import Path

from manim import DEFAULT_FONT_SIZE, config
from manim.mobject.text.tex_mobject import SingleStringMathTex
from manim.mobject.text.text_mobject import MarkupText, Text

# SingleStringMathTex is the base of both MathTex and Tex.
TEXT_TYPES = (SingleStringMathTex, Text, MarkupText)

EDGE_MARGIN = .25
TEXT_GAP = .08
# The caption rides at scene_style.CAPTION_Y = 3.3, and its own underside sits near 3.16, so
# the reserve to write to is y = 2.9. The hard line is a hair above that: the reference
# clip's gauge heading tops out at exactly 2.90 and is perfectly readable there, and a
# finding you fix by moving 0.00 units is a false positive.
CAPTION_FLOOR = 2.95
# Half a point of slack: font_size is recomputed from a height ratio, so a Text built at
# 15 can read back as 14.999. MathTex(...).scale(.5) lands on 24 and is meant to pass.
MIN_MATH_FONT_SIZE = 23.5
MIN_TEXT_FONT_SIZE = 14.5

AUDIT_DIR = Path('media/audit')
NAME_LIMIT = 34


class LayoutError(Exception):
    """Raised at an offending mark when MANIM_AUDIT_STRICT is set."""


class Box:
    """One thing a viewer sees, as a rectangle with a name worth printing.

    `group` is the arranged VGroup this text belongs to, when there is one. It matters for
    the fix: a row of a three-row `VGroup(...).arrange(DOWN)` must be moved by moving the
    whole group, or the arrangement it was built with breaks.
    """

    __slots__ = ('mob', 'name', 'is_text', 'left', 'right', 'bottom', 'top', 'font_size',
                 'group', 'group_edges')

    def __init__(self, mob, name, edges, font_size, group=None, group_edges=None):
        self.mob = mob
        self.name = name
        self.is_text = isinstance(mob, TEXT_TYPES)
        self.left, self.right, self.bottom, self.top = edges
        self.font_size = font_size
        self.group = group
        self.group_edges = group_edges

    def center(self, axis):
        return (self.bottom + self.top) / 2 if axis == 'y' else (self.left + self.right) / 2

    def extent(self, axis):
        return self.top - self.bottom if axis == 'y' else self.right - self.left

    def mover(self):
        """What actually has to move, and its name -- the group when there is one."""
        if self.group is None or self.group_edges is None:
            return self.name, self
        held = Box(self.mob, f'the group holding {self.name}', self.group_edges,
                   self.font_size)
        return held.name, held


def strict_mode():
    return os.environ.get('MANIM_AUDIT_STRICT', '') not in ('', '0', 'false', 'False')


def tag(mob, name):
    """Name a mobject for the audit report. Optional -- content is the default name."""
    mob.audit_tag = name
    return mob


def _shorten(words):
    words = ' '.join(str(words).split())
    return words if len(words) <= NAME_LIMIT else words[:NAME_LIMIT - 3] + '...'


def _name(mob, counts):
    tagged = getattr(mob, 'audit_tag', None)
    if tagged:
        return str(tagged)
    kind = type(mob).__name__
    if isinstance(mob, TEXT_TYPES):
        # original_text keeps Text's spacing; .text has had it stripped.
        words = (getattr(mob, 'tex_string', None) or getattr(mob, 'original_text', None)
                 or getattr(mob, 'text', ''))
        return f"{kind} '{_shorten(words)}'" if words else kind
    counts[kind] = counts.get(kind, 0) + 1
    return f'{kind} #{counts[kind]}'


def _units(mob, group=None):
    """Yield `(element, group)` for what a reader treats as one element.

    Never descends into a Text/MathTex: its submobjects are individual glyphs, and
    per-glyph boxes would report thousands of meaningless overlaps inside one fraction.
    A group with no text anywhere inside it is one shape, so a DashedLine reports once
    instead of once per dash. `group` is the nearest ancestor holding more than one piece
    of text, which is the thing a fix should move.
    """
    if isinstance(mob, TEXT_TYPES) or not any(
        isinstance(part, TEXT_TYPES) for part in mob.get_family()
    ):
        yield mob, group
        return
    holder = mob if _text_count(mob) > 1 else group
    for sub in mob.submobjects:
        yield from _units(sub, holder)


def _text_count(mob):
    """Separate pieces of text in this subtree, stopping at each one like `_units` does."""
    if isinstance(mob, TEXT_TYPES):
        return 1
    return sum(_text_count(sub) for sub in mob.submobjects)


def _edges(mob):
    try:
        edges = (
            float(mob.get_left()[0]), float(mob.get_right()[0]),
            float(mob.get_bottom()[1]), float(mob.get_top()[1]),
        )
    except Exception:
        return None
    if not any(math.isfinite(value) for value in edges):
        return None
    if edges[1] - edges[0] < 1e-6 and edges[3] - edges[2] < 1e-6:
        return None  # nothing on screen to collide with
    return edges


def _font_size(mob):
    if not isinstance(mob, TEXT_TYPES):
        return None
    try:
        size = float(mob.font_size)
    except Exception:
        return None
    return size if math.isfinite(size) and size > 0 else None


def boxes_for(mobjects):
    """Collect every on-screen element as a named box."""
    counts, found = {}, []
    for top in mobjects:
        for mob, group in _units(top):
            edges = _edges(mob)
            if edges is None:
                continue
            found.append(Box(
                mob, _name(mob, counts), edges, _font_size(mob),
                group=group, group_edges=_edges(group) if group is not None else None,
            ))
    return found


def _scale_now(box):
    return box.font_size / DEFAULT_FONT_SIZE if box.font_size else None


def _floor2(value):
    return math.floor(value * 100) / 100


def _room(box, axis, delta):
    """Would moving this box -- or the group it belongs to -- that far stay legal?"""
    _, target = box.mover()
    limit = (config.frame_height if axis == 'y' else config.frame_width) / 2 - EDGE_MARGIN
    half = target.extent(axis) / 2
    low, high = target.center(axis) - half + delta, target.center(axis) + half + delta
    if low < -limit or high > limit:
        return False
    return not (axis == 'y' and high > CAPTION_FLOOR)


def _move_fix(box, axis, delta):
    """Name what has to move and the center coordinate to move it to."""
    name, target = box.mover()
    if axis == 'y':
        way = 'down' if delta < 0 else 'up'
    else:
        way = 'left' if delta < 0 else 'right'
    return (f'move {name} {way} {abs(delta):.2f} to center {axis} = '
            f'{target.center(axis) + delta:.2f}')


def _readable_floor(box):
    return (MIN_MATH_FONT_SIZE if isinstance(box.mob, SingleStringMathTex)
            else MIN_TEXT_FONT_SIZE)


def _scale_fix(box, axis, push):
    """A `.scale()` value that shrinks the box clear of the collision instead.

    Never offered below the readable floor -- a fix that trades an overlap for type
    nobody can read on a phone is not a fix.
    """
    extent, now = box.extent(axis), _scale_now(box)
    if not extent or not now:
        return None
    factor = 1 - 2 * push / extent
    if not .4 <= factor < 1:
        return None
    wanted = _floor2(now * factor)
    if wanted * DEFAULT_FONT_SIZE < _readable_floor(box):
        return None
    return f'or scale {box.name} to {wanted:.2f}'


def _hits_after_move(box, axis, delta, texts):
    """Name the first text this box would land on if it moved on its own."""
    left, right, bottom, top = box.left, box.right, box.bottom, box.top
    if axis == 'x':
        left, right = left + delta, right + delta
    else:
        bottom, top = bottom + delta, top + delta
    for other in texts:
        if other.mob is box.mob:
            continue
        if (max(left, other.left) - min(right, other.right) < TEXT_GAP
                and max(bottom, other.bottom) - min(top, other.top) < TEXT_GAP):
            return other.name
    return None


def _overlap(a, b, texts):
    gap_x = max(a.left, b.left) - min(a.right, b.right)
    gap_y = max(a.bottom, b.bottom) - min(a.top, b.top)
    if gap_x >= TEXT_GAP or gap_y >= TEXT_GAP:
        return None
    push_x, push_y = TEXT_GAP - gap_x, TEXT_GAP - gap_y
    axis, push = ('y', push_y) if push_y <= push_x else ('x', push_x)
    near, far = (a, b) if a.center(axis) <= b.center(axis) else (b, a)
    options = [(near, -push), (far, push)]
    mover, delta = options[0]
    for box, shift in options:
        if _room(box, axis, shift):
            mover, delta = box, shift
            break
    fixes = [_move_fix(mover, axis, delta)]
    # A row animated on its own (Write(work[0])) has no group in the scene tree, so the
    # audit cannot name one. It can still say that moving the row alone won't do.
    if mover.group is None:
        landing = _hits_after_move(mover, axis, delta, texts)
        if landing:
            fixes.append(f'blocked: that move lands it on {landing} -- move them as one '
                         f'group, or shrink one')
    fixes.append(_scale_fix(mover, axis, push))
    return {
        'kind': 'overlap',
        'message': f'{a.name} overlaps {b.name} by {push:.2f} units '
                   f'{"vertically" if axis == "y" else "horizontally"}',
        'fix': '; '.join(fix for fix in fixes if fix),
    }


def _off_frame(box):
    half_x = config.frame_width / 2 - EDGE_MARGIN
    half_y = config.frame_height / 2 - EDGE_MARGIN
    for axis, low, high, limit, sides in (
        ('x', box.left, box.right, half_x, ('left', 'right')),
        ('y', box.bottom, box.top, half_y, ('bottom', 'top')),
    ):
        over_low, over_high = -limit - low, high - limit
        if max(over_low, over_high) <= 0:
            continue
        if over_low >= over_high:
            delta, edge, at = over_low, sides[0], low
        else:
            delta, edge, at = -over_high, sides[1], high
        return {
            'kind': 'off-frame',
            'message': f'{box.name} runs past the {edge} edge: {edge} at {at:.2f}, '
                       f'the margin stops at {math.copysign(limit, at):.2f}',
            'fix': _move_fix(box, axis, delta),
        }
    return None


def _in_caption_band(box):
    if box.top <= CAPTION_FLOOR:
        return None
    return {
        'kind': 'caption-band',
        'message': f'{box.name} reaches into the caption band: top at {box.top:.2f}, '
                   f'content must stay below {CAPTION_FLOOR:.2f}',
        'fix': _move_fix(box, 'y', CAPTION_FLOOR - box.top),
    }


def _too_small(box):
    if not box.font_size:
        return None
    math_type = isinstance(box.mob, SingleStringMathTex)
    floor = MIN_MATH_FONT_SIZE if math_type else MIN_TEXT_FONT_SIZE
    if box.font_size >= floor:
        return None
    if math_type:
        # Say both numbers in .scale() units: the message reports font size, and mixing
        # the two units is the one thing a model read as ambiguous in practice.
        fix = (f'scale {box.name} to at least 0.50 -- it is at '
               f'{_floor2(_scale_now(box) or 0):.2f} now')
    else:
        fix = f'raise {box.name} from font_size {box.font_size:.0f} to 15'
    return {
        'kind': 'small-type',
        'message': f'{box.name} is font size {box.font_size:.1f}, too small to read on a '
                   f'phone (floor {"24" if math_type else "15"})',
        'fix': fix,
    }


def _allowed(a, b, allow):
    return any(
        (a.mob is one and b.mob is two) or (a.mob is two and b.mob is one)
        for one, two in allow
    )


def audit_mobjects(mobjects, caption=None, allow=()):
    """Check one frame. Works on any list of mobjects, so it is testable without a render."""
    if caption is not None and type(caption).__name__ == 'VGroup':
        # a caption set from several pieces (words + LaTeX, see math_caption.py) is the
        # caption as a whole; its parts are not content
        mobjects = [mob for mob in mobjects if mob is not caption]
    boxes = boxes_for(mobjects)
    findings = []
    texts = [box for box in boxes if box.is_text]
    for index, a in enumerate(texts):
        for b in texts[index + 1:]:
            if not _allowed(a, b, allow):
                findings.append(_overlap(a, b, texts))
    for box in boxes:
        findings.append(_off_frame(box))
        findings.append(_too_small(box))
        if box.mob is not caption:
            findings.append(_in_caption_band(box))
    return [finding for finding in findings if finding], boxes


def _report(name, time, findings, count):
    if not findings:
        print(f'[audit] {name} @ {time}s -- clean ({count} elements)')
        return
    plural = '' if len(findings) == 1 else 's'
    print(f'[audit] {name} @ {time}s -- {len(findings)} problem{plural}')
    for finding in findings:
        print(f"  {finding['kind']:<12} {finding['message']}")
        if finding['fix']:
            print(f"               -> {finding['fix']}")


def audit_mark(scene, name, allow=()):
    """Audit the current frame at a teaching hold. Called from `Narrated.mark()`."""
    time = round(getattr(scene, 'elapsed', 0.), 2)
    try:
        findings, boxes = audit_mobjects(
            scene.mobjects, caption=getattr(scene, 'note', None), allow=allow,
        )
    except Exception as problem:  # a guardrail must never be the reason a render dies
        print(f'[audit] {name}: the audit itself failed ({problem!r}); render continues')
        if strict_mode():
            # A broken checker must never hand an agent loop a green light.
            raise LayoutError(f'{name}: the audit could not run: {problem!r}') from problem
        return []
    record = getattr(scene, 'audit_marks', None)
    if record is None:
        record = scene.audit_marks = []
    record.append({'name': name, 'time': time, 'findings': findings})
    _report(name, time, findings, len(boxes))
    write_report(scene)
    if findings and strict_mode():
        raise LayoutError(
            f'{name}: {len(findings)} layout problem(s) -- see the [audit] block above. '
            f'Unset MANIM_AUDIT_STRICT to see every mark in one pass.'
        )
    return findings


def report_path(scene):
    return AUDIT_DIR / f'{type(scene).__name__}_audit.json'


def write_report(scene):
    """Write the running report. Written per mark, so a strict abort still leaves it."""
    marks = getattr(scene, 'audit_marks', None)
    if not marks:
        return None
    out = report_path(scene)
    out.parent.mkdir(parents=True, exist_ok=True)
    total = sum(len(mark['findings']) for mark in marks)
    out.write_text(
        json.dumps(
            {'scene': type(scene).__name__, 'problems': total, 'marks': marks}, indent=2,
        ),
        encoding='utf-8',
    )
    return out


def audit_summary(scene):
    """One closing line, so a render log says pass or fail without scrolling back."""
    marks = getattr(scene, 'audit_marks', None)
    if not marks:
        return
    total = sum(len(mark['findings']) for mark in marks)
    where = write_report(scene)
    if total:
        bad = ', '.join(mark['name'] for mark in marks if mark['findings'])
        print(f'[audit] {total} layout problem(s) across {len(marks)} marks: {bad}')
    else:
        print(f'[audit] all {len(marks)} marks clean')
    print(f'[audit] report: {where}')
