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
    ('related_rates_lighthouse', 'LighthouseSweepRate', 'related-rates-lighthouse',
     'Related rates &mdash; lighthouse problem', 'Lighthouse problem, related rates', None,
     'A lighthouse sits on an island 3 km from the nearest point P on a straight '
     'shoreline, centered in the frame, and its beam sweeps at a constant angular '
     'rate all the way from one side of P to the other. The point where the beam '
     "hits the shore does not move at a constant rate, though &mdash; it's x = "
     '3&times;tan(&theta;), negative to the left of P and positive to the right '
     '&mdash; so the point crawls slowly as it passes under the lighthouse and '
     'accelerates hard toward either end as the beam nears parallel to the shore. '
     'Marks x&nbsp;=&nbsp;1&nbsp;km, the distance the textbook question asks about. '
     'The real 4 rev/min sweep (8&pi;/60&nbsp;&approx;&nbsp;0.42 rad/sec) would cover '
     'this whole range in a couple of seconds &mdash; too fast to watch the '
     'crawl-then-blur happen at both ends &mdash; so it is slowed to roughly a third '
     'of real speed here; the 3 km distance and the tangent relationship stay exact.'),
    ('related_rates_cone', 'ConeLevelRate', 'related-rates-cone',
     'Related rates &mdash; conical tank problem', 'Cone problem, related rates', None,
     "Water pours into a downward-pointing cone at a constant rate. The surface "
     "radius is proportional to the depth (similar triangles, r/h = R/H) &mdash; a "
     'blue arrow shows that radius directly as it grows. Because the cross-section '
     "widens as the water rises, the depth's rise rate does the opposite of the "
     'square and ladder clips: flashes start fast near the point and land farther '
     'apart as the water climbs. Marks h&nbsp;=&nbsp;4&nbsp;cm, the depth the '
     'textbook question asks about. Sped up 1.5&times; from the real 10 cm&sup3;/sec '
     'pour-in rate.'),
    ('related_rates_drain', 'TankDrainRate', 'related-rates-drain',
     'Related rates &mdash; draining tank problem', 'Draining tank problem, related rates', None,
     "Water drains from an upright cylindrical tank at a constant rate. Because the "
     "tank's radius never changes with height, the water level flashes gold at even, "
     'steady intervals &mdash; not speeding up like the square or ladder clips. That '
     'evenness is the whole point of the &ldquo;constant dimension&rdquo; case: fixed '
     'cross-sectional area means a fixed rate of drop. Sped up from the real ~0.02 '
     'cm/sec drain rate so the pattern is visible in a few seconds.'),
    ('related_rates_ladder', 'LadderSlideRate', 'related-rates-ladder',
     'Related rates &mdash; ladder problem', 'Ladder problem, related rates', None,
     "A 13 ft ladder's foot is pulled away from the wall at a constant 2 ft/sec. "
     'The height on the wall flashes gold on every whole foot &mdash; the flashes '
     "land closer together as the ladder falls, because the top's rate of descent "
     "keeps climbing even though the foot's rate never does. Marks x&nbsp;=&nbsp;5 ft, "
     'the distance the textbook question asks about. Plays in real time.'),
    ('related_rates_square', 'SquareAreaRate', 'related-rates-square',
     'Related rates &mdash; square problem', 'Square problem, related rates', None,
     'A square\'s side grows at a constant rate. The area value ticks up and flashes '
     'gold every time it crosses a whole number &mdash; the flashes land closer '
     'together as the clip goes on, because the area\'s rate keeps climbing even '
     'though the side\'s rate never does. Sped up from the textbook\'s 3 in/min so '
     'the pattern is visible in a few seconds; the side still runs up to 9 in.'),
    ('fraction_add_fractions', 'FractionAddFractions', 'fraction-add-fractions',
     'Add fractions with common denominators', 'Fraction addition help',
     'fraction_add_fractions_marks.json',
     'Three whole-plus-fraction sums (including one negative whole) and three '
     'fraction-plus-fraction sums. Each shows rewriting a whole over 1, scaling '
     'to a common denominator, then adding the tops.'),
    ('fraction_times_whole', 'FractionTimesWhole', 'fraction-times-whole',
     'Multiply a fraction by a whole number', 'Fraction times whole number',
     'fraction_times_whole_marks.json',
     'Write a whole number as a fraction, cancel common factors first, then multiply '
     'the tops. Each product is two factors only &mdash; &frac13;&times;15, then '
     '&frac13;&times;4, then &frac13;&times;22. Example&nbsp;2: &frac27; with a '
     'negative whole, then &frac27;&times;&frac38; simplified to &frac{3}{28}.'),
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
