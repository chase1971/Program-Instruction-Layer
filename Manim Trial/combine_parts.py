"""Stitch the four two-dice parts into one continuous video.

The parts were written to cut together — part 2 reconstructs part 1's final frame,
and each part opens on the one before it — so this is a straight concatenation with
no transitions. Every part renders 1920x1080 at 30 fps from the same Manim pipeline,
so the streams are copied rather than re-encoded: lossless, and a few seconds to run.

    & '.\\.venv\\Scripts\\python.exe' combine_parts.py

Writes the stitched MP4 where build_page.py's own glob already looks for it, plus a
merged marks sidecar whose times are offset into the combined timeline. Re-run this
after re-rendering any part, then re-run build_page.py.
"""

import json
import pathlib
import subprocess
import sys

import av

# Running order. Part 1 records no marks, hence the None.
PARTS = [
    ('dice_sums', 'DiceSums', None),
    ('dice_stats', 'DiceStats', 'dice_stats_marks.json'),
    ('dice_sampling', 'DiceSampling', 'dice_sampling_marks.json'),
    ('dice_products', 'DiceProducts', 'dice_products_marks.json'),
]

# Under this script's own name, so build_page.py's media\videos\{folder}\**\{klass}.mp4
# glob finds it unchanged AND the page footer credits the file that really made it.
OUT = pathlib.Path(r'media\videos\combine_parts\1080p30\DiceSeries.mp4')
MARKS = pathlib.Path('dice_series_marks.json')


def probe(path):
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        return (stream.width, stream.height, float(stream.average_rate),
                float(stream.duration * stream.time_base))


def gather():
    """Locate every part's 1080p30 render and refuse to stitch a mismatched set."""
    found = []
    for folder, klass, marks in PARTS:
        path = pathlib.Path('media/videos') / folder / '1080p30' / f'{klass}.mp4'
        if not path.exists():
            sys.exit(f'missing: {path} — render {klass} at -qh --fps 30 first')
        width, height, fps, duration = probe(path)
        if (width, height, round(fps)) != (1920, 1080, 30):
            sys.exit(f'{path} is {width}x{height} at {fps:g} fps — re-render at -qh --fps 30')
        found.append((path, duration, marks))
    return found


def merge_marks(found):
    """Shift each part's pause marks into the combined timeline.

    Offsets are the parts' real durations, so every part starts where it actually
    starts. Times inside a part still come from Narrated.elapsed, which runs about
    1% short of the encoded length — well inside the 2.2s hold each mark sits on.
    """
    merged = []
    start = 0.
    for index, (_, duration, marks_file) in enumerate(found, 1):
        if marks_file and pathlib.Path(marks_file).exists():
            for mark in json.loads(pathlib.Path(marks_file).read_text(encoding='utf-8')):
                # ASCII only: whatever reads this sidecar should not need UTF-8.
                merged.append({'name': f"part {index}: {mark['name']}",
                               'time': round(start + mark['time'], 2)})
        start += duration
    MARKS.write_text(json.dumps(merged, indent=2), encoding='utf-8')
    return merged


def stitch(found):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    listing = OUT.parent / 'parts.txt'
    listing.write_text(''.join(f"file '{p.resolve().as_posix()}'\n" for p, _, _ in found),
                       encoding='utf-8')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
                    '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', str(OUT)],
                   check=True)
    listing.unlink()


if __name__ == '__main__':
    parts = gather()
    expected = sum(duration for _, duration, _ in parts)
    stitch(parts)
    marks = merge_marks(parts)
    width, height, fps, duration = probe(OUT)
    print(f'{OUT}  {width}x{height} at {fps:g} fps')
    print(f'  {duration:.2f}s  ({int(duration // 60)}m {duration % 60:04.1f}s), '
          f'expected {expected:.2f}s, drift {duration - expected:+.2f}s')
    print(f'  {OUT.stat().st_size / 1024 / 1024:.1f} MB, {len(marks)} pause marks '
          f'-> {MARKS}')
