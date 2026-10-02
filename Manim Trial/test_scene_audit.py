"""Regression test for scene_audit, built on a real collision that really happened.

The draft of `dot_product_directions.py` stacked the gauge readout on top of the first row
of the northeast work: three stacked fractions are much taller than they look, and the
readout was a stacked fraction too. Two values fixed it -- the readout became one line, and
the work got its own lower center.

So the audit has a free, honest test. Rebuild that frame from the clip's own factory
functions and check both directions:

- shipped values  -> clean
- the two pre-fix values restored -> the overlap is flagged, naming both offenders

If it ever does neither, the checker is wrong, not the clip.

Run it (no render, no video -- seconds, not minutes):

    & '.\\.venv\\Scripts\\python.exe' test_scene_audit.py

MiKTeX must be on PATH for the process, same as a render:

    $env:PATH = (Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64') + ';' + $env:PATH
"""

import sys

from manim import DOWN, RIGHT, SurroundingRectangle

import dot_product_directions as clip
import scene_audit
from scene_layout import Region
from scene_style import CAPTION_Y, GOLD, label

SHIPPED_WORK_REGION = clip.NORTHEAST_WORK_REGION
SHIPPED_VALUE_TEX = r'\approx 0.707'
# What the draft had before the collision was fixed.
# A work region reaching up into the gauge readout: the draft's collision, rebuilt.
PRE_FIX_WORK_REGION = Region('PRE_FIX', .6, clip.FRAME_RIGHT, -3.4, 1.4)
PRE_FIX_VALUE_TEX = r'\frac{\sqrt2}{2}\approx0.707'

EAST_COMPONENTS = r'\text{you: }\langle1,0\rangle'
FRIEND_COMPONENTS = (
    r'\text{friend: }\left\langle\frac{\sqrt2}{2},\frac{\sqrt2}{2}\right\rangle'
)
CAPTION = 'About 0.707 — partly the same direction, not all the way.'


def east_dot_northeast_frame(work_region, value_tex):
    """Rebuild everything on screen at the `east_dot_northeast` mark.

    Mirrors `confirm_with_partial()`. The draft render is the source of truth for the
    clean case; this reconstruction is what makes the failing case repeatable.
    """
    saved = clip.NORTHEAST_WORK_REGION
    clip.NORTHEAST_WORK_REGION = work_region
    try:
        work = clip.make_northeast_work()
    finally:
        clip.NORTHEAST_WORK_REGION = saved

    east_arrow = clip.make_travel_arrow([1, 0], clip.YOU_COLOR)
    friend_arrow = clip.make_travel_arrow(
        [clip.NORTHEAST_COMPONENT, clip.NORTHEAST_COMPONENT], clip.FRIEND_COLOR,
    )
    friend_label = clip.place_northeast_label(clip.make_vector_label(
        FRIEND_COMPONENTS, friend_arrow, clip.FRIEND_COLOR, RIGHT,
    ))
    caption = label(CAPTION).move_to([0, CAPTION_Y, 0])
    return caption, [
        caption,
        clip.make_compass(),
        east_arrow,
        clip.make_vector_label(EAST_COMPONENTS, east_arrow, clip.YOU_COLOR, DOWN),
        friend_arrow,
        friend_label,
        clip.make_northeast_components(friend_arrow),
        work,
        SurroundingRectangle(work[2][2], color=GOLD, buff=.14),
        clip.make_meter(),
        clip.make_meter_fill(clip.NORTHEAST_COMPONENT),
        clip.make_meter_value(value_tex),
    ]


def audit(work_region, value_tex):
    caption, mobjects = east_dot_northeast_frame(work_region, value_tex)
    findings, boxes = scene_audit.audit_mobjects(mobjects, caption=caption)
    return findings, boxes


def describe(findings):
    return '\n'.join(f"    {f['kind']}: {f['message']}\n      -> {f['fix']}" for f in findings)


def test_shipped_frame_is_clean():
    findings, boxes = audit(SHIPPED_WORK_REGION, SHIPPED_VALUE_TEX)
    assert boxes, 'the audit found nothing on screen -- the walk is broken'
    assert not findings, f'shipped frame should be clean:\n{describe(findings)}'
    return f'{len(boxes)} elements checked, no findings'


def test_pre_fix_overlap_is_flagged():
    findings, _ = audit(PRE_FIX_WORK_REGION, PRE_FIX_VALUE_TEX)
    overlaps = [f for f in findings if f['kind'] == 'overlap']
    assert overlaps, (
        'the pre-fix values must be flagged as an overlap; '
        f'got: {describe(findings) or "nothing"}'
    )
    readout = [f for f in overlaps if '0.707' in f['message'] and 'sqrt2' in f['message']]
    assert readout, f'the flag must name the readout and the work row:\n{describe(overlaps)}'
    assert readout[0]['fix'], 'a flagged overlap must carry a numeric fix'
    return readout[0]['message']


def main():
    failures = 0
    for check in (test_shipped_frame_is_clean, test_pre_fix_overlap_is_flagged):
        try:
            print(f'PASS  {check.__name__}\n      {check()}')
        except Exception as problem:  # a crash in the checker is a failure, not a traceback
            failures += 1
            print(f'FAIL  {check.__name__}\n    {problem}')
    print('\n' + ('all checks passed' if not failures else f'{failures} check(s) failed'))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
