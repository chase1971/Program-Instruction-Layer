"""Inline a rendered MP4 into a served HTML page.

Chase can only open pages at http://127.0.0.1:8765/, never a C:\\ path, so the video
travels as a base64 data URI inside the HTML itself. Add a row to PAGES and run:

    & '.\\.venv\\Scripts\\python.exe' build_page.py

Then confirm the page answers 200 before handing over the link.
"""

import base64
import glob
import json
import pathlib

SCRATCH = pathlib.Path(r'..\agent docs\scratch')

# folder, scene class, page slug, on-page heading, browser tab title, marks file, blurb
PAGES = [
    ('combine_parts', 'DiceSeries', 'dice-series',
     'Two dice &mdash; all four parts', 'Two dice, complete series',
     'dice_series_marks.json',
     'Parts 1 to 4 stitched into one 4:27 run: every ordered roll behind each sum, the '
     'histogram with &mu;&nbsp;=&nbsp;7 and &sigma;&nbsp;&asymp;&nbsp;2.42, the sampling '
     'distribution of the mean, then the product of two dice &mdash; a population nowhere '
     'near normal whose sampling distribution goes normal anyway. Straight cuts: each part '
     'was written to open on the one before it. Rebuild with combine_parts.py.'),
    ('dice_sums', 'DiceSums', 'dice-sums',
     'Part 1 &mdash; every way to roll each sum', 'Two dice, part 1', None,
     'Each sum from 2 to 12 collects its ordered rolls, ending on 36.'),
    ('dice_stats', 'DiceStats', 'dice-stats',
     'Part 2', 'Two dice, part 2', 'dice_stats_marks.json',
     'The chart tips onto its side, a normal curve lays over it, then '
     '&mu;&nbsp;=&nbsp;7 and &sigma;&nbsp;&asymp;&nbsp;2.42.'),
    ('dice_sampling', 'DiceSampling', 'dice-sampling',
     'Part 3 &mdash; the sampling distribution', 'Two dice, part 3',
     'dice_sampling_marks.json',
     'Four rolls of the pair make one sample. A hundred sample means rain onto the '
     'same axis, and the theory from parts 1 and 2 predicts where they land.'),
    ('dice_products', 'DiceProducts', 'dice-products',
     'Part 4 &mdash; a population nowhere near normal', 'Two dice, part 4',
     'dice_products_marks.json',
     'The product of two dice is spiky, gap-riddled and badly skewed &mdash; no 7, no 11, '
     'no 13. A hundred sample means still pile into a bell, and &sigma;/&radic;n still '
     'predicts the spread. That is the Central Limit Theorem.'),
]

STYLE = (
    'body{margin:0;background:#101c30;color:#f2f5fa;font:20px Segoe UI,sans-serif;'
    'text-align:center}'
    'main{max-width:1150px;margin:20px auto;padding:16px}video{width:100%;border-radius:12px}'
    'button{font:inherit;padding:18px 30px;margin:12px 6px;border:0;border-radius:10px;'
    'background:#ffc66d;color:#101c30;cursor:pointer;min-width:145px}'
    'a{color:#86c8ff}p{line-height:1.6}small{color:#b2c0d4}'
    'ul{display:inline-block;text-align:left;color:#b2c0d4;font-size:18px}'
)

SCRIPT = (
    'const movie=document.getElementById("movie");'
    'document.getElementById("play").onclick=()=>'
    '{if(movie.paused)movie.play();else movie.pause()};'
    'document.getElementById("replay").onclick=()=>{movie.currentTime=0;movie.play()};'
)


def mark_list(marks_file):
    """Pause points, so Chase can see where an embedding app is allowed to stop."""
    if not marks_file:
        return ''
    path = pathlib.Path(marks_file)
    if not path.exists():
        return ''
    marks = json.loads(path.read_text(encoding='utf-8'))
    items = ''.join(f"<li><b>{m['name'].replace('_', ' ')}</b> &mdash; {m['time']}s</li>"
                    for m in marks)
    return ('<p><small>Pause points (each sits on a 2s hold):</small></p>'
            f'<ul>{items}</ul>')


def build(folder, klass, slug, heading, tab, marks_file, blurb):
    found = glob.glob(rf'media\videos\{folder}\**\{klass}.mp4', recursive=True)
    if not found:
        return f'{slug}: no render found — render the scene first'
    video = pathlib.Path(found[0])
    data = base64.b64encode(video.read_bytes()).decode('ascii')
    html = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{tab}</title><style>{STYLE}</style><main><h1>{heading}</h1>'
        '<video id="movie" playsinline preload="metadata" controls>'
        f'<source src="data:video/mp4;base64,{data}" type="video/mp4"></video>'
        '<div><button id="play">Play / Pause</button>'
        '<button id="replay">Replay</button></div>'
        f'<p>{blurb}</p>{mark_list(marks_file)}'
        f'<p><small>Animation study &middot; source: Manim Trial/{folder}.py</small></p>'
        f'<a href="/pages.html">&larr; All pages</a></main><script>{SCRIPT}</script></html>'
    )
    out = SCRATCH / f'{slug}.html'
    out.write_text(html, encoding='utf-8')
    return f'{slug}: {out.stat().st_size:,} bytes'


if __name__ == '__main__':
    for row in PAGES:
        print(build(*row))
