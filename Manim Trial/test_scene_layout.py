"""Checks that keep the layout regions honest.

The regions are only worth having if they are disjoint, and only trustworthy if a layout
already known to read well fits inside them. Both are asserted against
`dot_product_directions.py`, which was checked frame by frame -- not against a guess.

Run it (no render):

    & '.\\.venv\\Scripts\\python.exe' test_scene_layout.py

MiKTeX must be on PATH for the process, same as a render.
"""

import sys

from manim import DOWN, RIGHT, VGroup

import dot_product_directions as clip
import scene_layout
from scene_layout import CENTER, DIAGRAM, GAUGE, PANELS, REGIONS, WORK, fit_into


def diagram_content():
    """Everything the reference clip draws on the left: compass, both arrows, labels."""
    east_arrow = clip.make_travel_arrow([1, 0], clip.YOU_COLOR)
    friend_arrow = clip.make_travel_arrow(
        [clip.NORTHEAST_COMPONENT, clip.NORTHEAST_COMPONENT], clip.FRIEND_COLOR,
    )
    friend_label = clip.make_vector_label(
        r'\text{friend: }\left\langle\frac{\sqrt2}{2},\frac{\sqrt2}{2}\right\rangle',
        friend_arrow, clip.FRIEND_COLOR, RIGHT,
    ).move_to(clip.NORTHEAST_LABEL_CENTER)
    return VGroup(
        clip.make_compass(),
        east_arrow,
        clip.make_vector_label(
            r'\text{you: }\langle1,0\rangle', east_arrow, clip.YOU_COLOR, DOWN,
        ),
        friend_arrow,
        friend_label,
        clip.make_northeast_components(friend_arrow),
        clip.make_right_angle(),
        clip.make_half_angle(),
    )


def work_variants():
    """Each work panel is shown alone; the union bbox is not a real frame."""
    return (clip.make_perpendicular_work(), clip.make_northeast_work())


def gauge_content():
    return VGroup(
        clip.make_meter(),
        clip.make_meter_fill(clip.NORTHEAST_COMPONENT),
        clip.make_meter_value(r'\approx 0.707'),
    )


def center_content():
    return VGroup(
        clip.make_unit_vector_note(), clip.make_case_summary(), clip.make_open_question(),
    )


def test_panels_are_disjoint():
    for index, region in enumerate(PANELS):
        for other in PANELS[index + 1:]:
            assert not region.overlaps(other), f'{region.name} overlaps {other.name}'
    return ' + '.join(region.name for region in PANELS) + ' never collide'


def test_regions_stay_on_frame_and_below_the_caption():
    for region in REGIONS:
        assert region.left >= -scene_layout.FRAME_RIGHT, f'{region.name} runs off the left'
        assert region.right <= scene_layout.FRAME_RIGHT, f'{region.name} runs off the right'
        assert region.bottom >= scene_layout.FRAME_BOTTOM, f'{region.name} runs off the bottom'
        assert region.top <= scene_layout.CONTENT_TOP, f'{region.name} enters the caption band'
        assert region.width > 0 and region.height > 0, f'{region.name} is inside out'
    return f'{len(REGIONS)} regions on frame, all clear of the caption band'


# The reference gauge fills its band right to the ceiling and tops out 0.0009 units above
# it -- about a tenth of a pixel at 1080p, and still far below the audit's caption line.
# Tolerated here rather than bending CONTENT_TOP to one data point.
TOUCHING = .01


def test_reference_clip_fits_its_regions():
    """The proof the boxes are usable: a layout that reads well already lives inside them."""
    for build, region in (
        (diagram_content, DIAGRAM),
        (gauge_content, GAUGE),
        (center_content, CENTER),
    ):
        content = build()
        fit_into(content, region)
        assert region.holds(content, slack=TOUCHING), (
            f"the reference clip's {region.name.lower()} content does not fit {region!r}: "
            f'x [{content.get_left()[0]:.2f},{content.get_right()[0]:.2f}] '
            f'y [{content.get_bottom()[1]:.2f},{content.get_top()[1]:.2f}]'
        )
    for index, content in enumerate(work_variants()):
        fit_into(content, WORK)
        assert WORK.holds(content, slack=TOUCHING), (
            f'the reference clip work panel {index} does not fit {WORK!r}: '
            f'x [{content.get_left()[0]:.2f},{content.get_right()[0]:.2f}]'
        )
    return 'diagram, work, gauge and closing cards all fit after fit_into'


def test_fit_into_shrinks_and_centers_oversized_content():
    oversized = clip.make_unit_vector_note().scale(3)
    fit_into(oversized, WORK)
    assert WORK.holds(oversized), f'fit_into left content outside WORK: {oversized.width:.2f} wide'
    assert abs(oversized.get_center()[0] - WORK.center[0]) < 1e-6, 'fit_into did not center it'
    untouched = clip.make_meter_value('0')
    before = untouched.width
    fit_into(untouched, GAUGE)
    assert abs(untouched.width - before) < 1e-6, 'fit_into scaled content that already fit'
    return 'oversized content shrinks to fit; content that already fits is not touched'


CHECKS = (
    test_panels_are_disjoint,
    test_regions_stay_on_frame_and_below_the_caption,
    test_reference_clip_fits_its_regions,
    test_fit_into_shrinks_and_centers_oversized_content,
)


def _portal_suite():
    import vector_portal_layout as portal_layout
    from vector_portal_layout import CENTER as P_CENTER
    from vector_portal_layout import DIAGRAM as P_DIAGRAM
    from vector_portal_layout import GAUGE as P_GAUGE
    from vector_portal_layout import PANELS as P_PANELS
    from vector_portal_layout import REGIONS as P_REGIONS
    from vector_portal_layout import WORK as P_WORK
    from vector_portal_layout import fit_into as portal_fit_into

    def portal_panels_disjoint():
        for index, region in enumerate(P_PANELS):
            for other in P_PANELS[index + 1:]:
                assert not region.overlaps(other), f'{region.name} overlaps {other.name}'
        return 'portal ' + ' + '.join(r.name for r in P_PANELS) + ' never collide'

    def portal_on_frame():
        for region in P_REGIONS:
            assert region.left >= -portal_layout.FRAME_RIGHT, f'{region.name} off left'
            assert region.right <= portal_layout.FRAME_RIGHT, f'{region.name} off right'
            assert region.bottom >= portal_layout.FRAME_BOTTOM, f'{region.name} off bottom'
            assert region.top <= portal_layout.CONTENT_TOP, f'{region.name} in caption band'
        return f'portal {len(P_REGIONS)} regions on frame'

    def portal_reference_fits():
        for build, region in (
            (diagram_content, P_DIAGRAM),
            (gauge_content, P_GAUGE),
            (center_content, P_CENTER),
        ):
            content = build()
            portal_fit_into(content, region)
            assert region.holds(content, slack=TOUCHING), (
                f'portal {region.name} does not fit: '
                f'x [{content.get_left()[0]:.2f},{content.get_right()[0]:.2f}]'
            )
        for index, content in enumerate(work_variants()):
            portal_fit_into(content, P_WORK)
            assert P_WORK.holds(content, slack=TOUCHING), (
                f'portal work panel {index} does not fit: '
                f'x [{content.get_left()[0]:.2f},{content.get_right()[0]:.2f}]'
            )
        return 'portal reference clip fits'

    def test_portal_fit_into_shrink():
        oversized = clip.make_unit_vector_note().scale(3)
        portal_fit_into(oversized, P_WORK)
        assert P_WORK.holds(oversized), 'portal fit_into left content outside WORK'
        return 'portal fit_into shrinks oversized content'

    return (
        ('portal_panels_disjoint', portal_panels_disjoint),
        ('portal_on_frame', portal_on_frame),
        ('portal_reference_fits', portal_reference_fits),
        ('test_portal_fit_into_shrink', test_portal_fit_into_shrink),
    )


def main():
    failures = 0
    for check in CHECKS:
        try:
            print(f'PASS  {check.__name__}\n      {check()}')
        except Exception as problem:
            failures += 1
            print(f'FAIL  {check.__name__}\n    {problem}')
    for name, check in _portal_suite():
        try:
            print(f'PASS  {name}\n      {check()}')
        except Exception as problem:
            failures += 1
            print(f'FAIL  {name}\n    {problem}')
    print('\n' + ('all checks passed' if not failures else f'{failures} check(s) failed'))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
