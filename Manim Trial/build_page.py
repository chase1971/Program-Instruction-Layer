"""Inline a rendered MP4 into a served HTML page.

Chase can only open pages at http://127.0.0.1:8765/, never a C:\\ path, so the video
travels as a base64 data URI inside the HTML itself. Add a row to PAGES and run:

    & '.\\.venv\\Scripts\\python.exe' build_page.py

Then confirm the page answers 200 before handing over the link.
"""

import base64
import glob
import pathlib

SCRATCH = pathlib.Path(r'..\agent docs\scratch')

# folder, scene class, page slug, on-page heading, browser tab title, marks file, blurb.
# The blurb is a record of what the clip covers -- it is never rendered: Chase wants no
# text under the player, only the Play/Replay and Previous/Next buttons.
PAGES = [
    ('slope_intercept_form', 'SlopeInterceptMoveConstant', 'slope-intercept-move-constant',
     'Slope-intercept form &mdash; when x is already across', 'Slope-intercept form 3',
     'slope_intercept_move_constant_marks.json',
     '2y&nbsp;+&nbsp;8&nbsp;&gt;&nbsp;&minus;6x: x and y are already on opposite sides, so '
     'step 1 moves the 8 instead (subtract 8 from both sides); the right side '
     '&minus;6x&nbsp;&minus;&nbsp;8 is already x term first, so no swap. Divide every term '
     'by 2 &mdash; positive, so no flip: y&nbsp;&gt;&nbsp;&minus;3x&nbsp;&minus;&nbsp;4. '
     'Graph: intercept &minus;4, down 3 right 1, dashed line, shade above.'),
    ('slope_intercept_form', 'SlopeInterceptYFirst', 'slope-intercept-y-first',
     'Slope-intercept form &mdash; when y comes first', 'Slope-intercept form 2',
     'slope_intercept_y_first_marks.json',
     '&minus;2y&nbsp;+&nbsp;5x&nbsp;&ge;&nbsp;&minus;8, same beats as the first clip: subtract '
     '5x from both sides, write the right side x term first as &minus;5x&nbsp;&minus;&nbsp;8, '
     'divide every term by &minus;2 and flip &ge; to &le;. Negative over negative gives a '
     'positive slope: y&nbsp;&le;&nbsp;&frac52;x&nbsp;+&nbsp;4. Graph: intercept 4, up 5 '
     'right 2, solid line, shade below.'),
    ('slope_intercept_form', 'SlopeInterceptForm', 'slope-intercept-form',
     'Slope-intercept form &mdash; an inequality', 'Slope-intercept form',
     'slope_intercept_form_marks.json',
     'First clip on a white background. The goal is slope-intercept form, keeping the '
     'inequality sign where the = goes; move the x term first, then divide every term by '
     'the number next to y, flipping the sign if that number is negative. '
     '&minus;2x&nbsp;&minus;&nbsp;3y&nbsp;&lt;&nbsp;6: add 2x, write the right side '
     '2x&nbsp;+&nbsp;6, divide every term by &minus;3 and flip &lt; to &gt;, giving '
     'y&nbsp;&gt;&nbsp;&minus;&frac23;x&nbsp;&minus;&nbsp;2, then move the negative to the '
     'top number (Chase&rsquo;s convention, no reason given on screen). Ends on the graph: '
     'intercept, down 2 right 3, dashed line (strict), shade above.'),
    ('angle_between_vectors', 'AngleBetweenVectors', 'angle-between-vectors',
     'Angle between vectors &mdash; normalize, then dot', 'Angle between vectors',
     'angle_between_vectors_marks.json',
     'Sequel to the introductory dot-product clip: when the vectors are different '
     'sizes, shrink both to length 1 and dot the unit vectors. '
     '(u/&#8741;u&#8741;)&middot;(v/&#8741;v&#8741;) combines into '
     '(u&middot;v)/(&#8741;u&#8741;&#8741;v&#8741;), which is cos&nbsp;&theta;. Three '
     'textbook pairs follow, each swinging one arrow while the similarity gauge '
     'follows it &mdash; including u with w at exactly 90&deg;.'),
    ('vector_projection_shadow', 'VectorProjectionShadow', 'vector-projection-shadow',
     'Vector projection &mdash; the shadow u casts on v', 'Vector projection, the idea',
     'vector_projection_shadow_marks.json',
     'Light shines perpendicular to v, and the shadow u casts on v&rsquo;s line is '
     'proj<sub>v</sub>u. First u is longer than v and the shadow runs past v&rsquo;s tip; '
     'then v is longer and the shadow lands inside it. Stretching v alone never moves the '
     'shadow &mdash; v only supplies a direction. Then two panels. First the length: '
     'SOH CAH TOA turns ADJ into the shadow and HYP into &#8741;u&#8741;, and the '
     '&#8741;u&#8741;&rsquo;s cancel to leave u&middot;v/&#8741;v&#8741;. Then the vector: '
     'the unit vector v&#770; stretches to that length, giving '
     'proj<sub>v</sub>u&nbsp;=&nbsp;(u&middot;v/&#8741;v&#8741;&sup2;)&nbsp;v.'),
    ('vector_decomposition', 'VectorDecomposition', 'vector-decomposition',
     'Decomposing a vector &mdash; along v and across v', 'Vector decomposition',
     'vector_decomposition_marks.json',
     'What decomposing means: u&nbsp;=&nbsp;3i&nbsp;+&nbsp;4j is already u split into two '
     'perpendicular pieces along the axes. The perpendicular reference then swings around '
     'u, since any pair works, and settles on v&rsquo;s direction: w<sub>1</sub> along v, '
     'w<sub>2</sub> straight across it. w<sub>1</sub> is the part of u that goes in '
     'v&rsquo;s direction (a copy of v shrinks onto it); w<sub>2</sub> is the part that has '
     'nothing to do with v (climb it and u&rsquo;s shadow on v never moves). On a ramp along '
     'v only w<sub>1</sub> moves you, and w<sub>1</sub> is clip three&rsquo;s shadow. Then the worksheet problem, u&nbsp;=&nbsp;3i&nbsp;+&nbsp;4j and '
     'v&nbsp;=&nbsp;10i&nbsp;+&nbsp;2j, in three steps: project to get '
     'w<sub>1</sub>&nbsp;=&nbsp;&lang;95/26,&nbsp;19/26&rang;, subtract to get '
     'w<sub>2</sub>&nbsp;=&nbsp;&lang;&minus;17/26,&nbsp;85/26&rang;, and check that '
     'w<sub>2</sub>&middot;v&nbsp;=&nbsp;0 and the pieces add back to u.'),
    ('force_decomposition', 'ForceDecomposition', 'force-decomposition',
     'The force problem &mdash; decompose, project, name the pieces', 'Force decomposition',
     'force_decomposition_marks.json',
     'Two forces of 8 N and 22 N meet at 50&deg;: how much of the 22 N force acts in the '
     '8 N force&rsquo;s direction? Split u into u<sub>1</sub> along v and u<sub>2</sub> '
     'across it; the question asks for the length of u<sub>1</sub>, u&rsquo;s shadow on v. '
     'Changing v&rsquo;s size never moves the shadow. The projection formula with '
     'u&middot;v&nbsp;=&nbsp;&#8741;u&#8741;&#8741;v&#8741;cos&nbsp;&theta; gives '
     'u<sub>1</sub>&nbsp;&asymp;&nbsp;1.768v (v stretched to the shadow&rsquo;s length), so '
     '&#8741;u<sub>1</sub>&#8741;&nbsp;&asymp;&nbsp;14.14&nbsp;N; the &#8741;v&#8741;&rsquo;s cancel to '
     '22&nbsp;cos&nbsp;50&deg;. Then u<sub>2</sub>&nbsp;=&nbsp;u&nbsp;&minus;&nbsp;u<sub>1</sub>&nbsp;&asymp;&nbsp;&lang;0,&nbsp;16.85&rang;, '
     'and a closing card names the pieces: parallel component (projection of u onto v) and '
     'orthogonal component (rejection vector).'),
    ('ramp_force', 'RampForce', 'ramp-force',
     'The wagon on a hill &mdash; projection onto a ramp', 'Ramp force',
     'ramp_force_marks.json',
     'Worksheet problem 7: a 100 lb wagon on a 20&deg; hill. The weight '
     'w&nbsp;=&nbsp;&lang;0,&nbsp;&minus;100&rang; splits into w<sub>1</sub> along the ramp (rolls the '
     'wagon) and w<sub>2</sub> into the hill (the hill pushes back). w<sub>1</sub> is w&rsquo;s shadow on '
     'the ramp, so project onto the unit vector r&nbsp;=&nbsp;&lang;cos&nbsp;20&deg;,&nbsp;sin&nbsp;20&deg;&rang;: '
     'w&middot;r&nbsp;=&nbsp;&minus;100&nbsp;sin&nbsp;20&deg;&nbsp;&asymp;&nbsp;&minus;34.20, the minus sign meaning '
     'down the hill, so holding it takes about 34.2 lb up the hill. Closes on the shortcut: '
     'Force to remain stationary = Weight &times; sin&nbsp;&theta;.'),
    ('work_wagon', 'WorkWagon', 'work-wagon',
     'Work &mdash; only the part of the pull along the motion counts', 'Work',
     'work_wagon_marks.json',
     'Worksheet problem 9. Work is the energy a force transfers by moving something: pull '
     '50 lb straight along the ground for 100 ft and W&nbsp;=&nbsp;&#8741;F&#8741;&#8741;PQ&#8741;&nbsp;=&nbsp;5000 ft&middot;lb. '
     'Tilt the handle to 30&deg; and F splits into F<sub>1</sub> along the ground (does work) and '
     'F<sub>2</sub> straight up (the wagon never rises: no work). F<sub>1</sub> is F&rsquo;s shadow on PQ, so '
     'W&nbsp;=&nbsp;&#8741;proj<sub>PQ</sub>F&#8741;&#8741;PQ&#8741;&nbsp;=&nbsp;&#8741;F&#8741;&#8741;PQ&#8741;cos&nbsp;&theta;'
     '&nbsp;=&nbsp;2500&radic;3&nbsp;&asymp;&nbsp;4330.13 ft&middot;lb, checked as the dot product F&middot;PQ. '
     'Closing card: what work means, its three forms, and foot-pounds.'),
    ('vector_projection_force', 'VectorProjectionForce', 'vector-projection-force',
     'Vector projection &mdash; the shadow of a force', 'Vector projection explained',
     'vector_projection_force_marks.json',
     'Two forces of 8 N and 22 N meet at a 50&deg; angle. Perpendicular light casts '
     'the 22 N force onto the direction established by the 8 N force, making the '
     'projection visible as a shadow. Its length is '
     '22cos(50&deg;)&nbsp;&asymp;&nbsp;14.14 N.'),
    ('dot_product_projection', 'DotProductProjection', 'dot-product-projection',
     'Dot product &mdash; projection weighted by length', 'Dot product explained',
     'dot_product_projection_marks.json',
     'The 22 N force first projects 14.14 N onto the 8 N force direction. The dot '
     'product then multiplies that projected amount by the other vector&rsquo;s '
     '8 N magnitude: 14.14&times;8&nbsp;&asymp;&nbsp;113.13 N&sup2;. An area model '
     'makes that multiplication visible and distinguishes it from projection and '
     'cosine similarity.'),
    ('dot_product_directions', 'DotProductDirections', 'dot-product-directions',
     'Dot product &mdash; east, north, and northeast', 'Introductory dot product',
     'dot_product_directions_marks.json',
     'The dot product as directional similarity, seen before it is calculated. You '
     'travel east at 1 mph and a friend travels north: the two directions share '
     'nothing, so the similarity gauge sits empty &mdash; and only then does the '
     'component arithmetic produce the zero that says the same thing. The friend '
     'turns northeast, still 1 mph, the gauge fills most of the way, and the '
     'calculation puts &radic;2/2&nbsp;&asymp;&nbsp;0.707 on it. The clip closes on '
     'the limit of that reading: u&middot;v&nbsp;=&nbsp;&#8741;u&#8741;&#8741;v&#8741;cos&nbsp;&theta; '
     'collapses to cos&nbsp;&theta; only because both magnitudes are 1 &mdash; so '
     'what happens when the vectors are different sizes? That question is the hook '
     'for the follow-up clip.'),
    ('related_rates_rocket', 'RocketAngleRate', 'related-rates-rocket',
     'Related rates &mdash; rocket problem', 'Rocket problem, related rates', None,
     'A rocket launches straight up at a constant speed while you watch from a fixed '
     "point 30 miles away. The angle of elevation doesn't grow at a constant rate, "
     'though: tan(&theta;) = h/30 means the angle races upward right after launch, '
     'while the rocket is still near the horizon, then grows slower and slower as it '
     'climbs &mdash; flashes start fast and land farther apart, the same decelerating '
     'family as the cone problem. A live arc at your position traces the angle '
     'directly. Marks t&nbsp;=&nbsp;12&nbsp;min, the moment the textbook question asks '
     'about. The real 4 mi/min climb would take the full 20 simulated minutes to play '
     'out &mdash; far too slow to watch &mdash; so the flight is sped way up; the 30 '
     'mile distance and the tangent relationship stay exact.'),
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

# Clips that play in order: slug -> the slug that follows it. Each page gets a Next
# button to its successor and a Previous button back to its predecessor.
SERIES = {
    'dot-product-directions': 'angle-between-vectors',
    'angle-between-vectors': 'vector-projection-shadow',
    'vector-projection-shadow': 'vector-decomposition',
    'vector-decomposition': 'force-decomposition',
    'force-decomposition': 'ramp-force',
    'ramp-force': 'work-wagon',
    'slope-intercept-form': 'slope-intercept-y-first',
    'slope-intercept-y-first': 'slope-intercept-move-constant',
}

STYLE = (
    'body{margin:0;background:#101c30;color:#f2f5fa;font:20px Segoe UI,sans-serif;'
    'text-align:center}'
    'main{max-width:1150px;margin:20px auto;padding:16px}video{width:100%;border-radius:12px}'
    'button,a.step{font:inherit;display:inline-block;text-decoration:none;'
    'box-sizing:border-box;padding:18px 30px;margin:12px 6px;border:0;border-radius:10px;'
    'background:#ffc66d;color:#101c30;cursor:pointer;min-width:145px}'
    'a.step{background:#86c8ff}'
    'a{color:#86c8ff}p{line-height:1.6}small{color:#b2c0d4}'
    'ul{display:inline-block;text-align:left;color:#b2c0d4;font-size:18px}'
)

SCRIPT = (
    'const movie=document.getElementById("movie");'
    'document.getElementById("play").onclick=()=>'
    '{if(movie.paused)movie.play();else movie.pause()};'
    'document.getElementById("replay").onclick=()=>{movie.currentTime=0;movie.play()};'
)


def series_buttons(slug):
    """Previous / Next links for a clip that belongs to a SERIES chain."""
    before = next((prior for prior, after in SERIES.items() if after == slug), None)
    after = SERIES.get(slug)
    links = ''
    if before:
        links += f'<a class="step" href="{before}.html">&larr; Previous clip</a>'
    if after:
        links += f'<a class="step" href="{after}.html">Next clip &rarr;</a>'
    return f'<div>{links}</div>' if links else ''


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
        f'{series_buttons(slug)}'
        f'<a href="/pages.html">&larr; All pages</a></main><script>{SCRIPT}</script></html>'
    )
    out = SCRATCH / f'{slug}.html'
    out.write_text(html, encoding='utf-8')
    return f'{slug}: {out.stat().st_size:,} bytes'


SERIES_PAGE = ('vector-series', 'Vectors &mdash; the whole series', 'Vector series')

# Each player borrows its video from that clip's own page, so this page stays a few KB
# and never goes stale when a clip is re-rendered. Loads in order, so clip 1 is ready first.
SERIES_SCRIPT = (
    'const players=[...document.querySelectorAll("video")];'
    'players.forEach((v,i)=>{'
    'document.getElementById("play"+i).onclick=()=>{if(v.paused)v.play();else v.pause()};'
    'document.getElementById("replay"+i).onclick=()=>{v.currentTime=0;v.play()};'
    'v.onplay=()=>players.forEach(o=>{if(o!==v)o.pause()})});'
    '(async()=>{for(const v of players){const b=document.getElementById("play"+players.indexOf(v));'
    'try{const page=await(await fetch(v.dataset.page)).text();'
    'const at=page.indexOf("data:video/mp4;base64,");'
    'const uri=page.slice(at,page.indexOf(\'"\',at));'
    'v.src=URL.createObjectURL(await(await fetch(uri)).blob());b.textContent="Play / Pause"}'
    'catch(e){b.textContent="Could not load this clip"}}})();'
)


def series_order(first='dot-product-directions'):
    order = [first]
    while order[-1] in SERIES:
        order.append(SERIES[order[-1]])
    return order


def build_series():
    """One page, every SERIES clip stacked in order, each with its own player."""
    slug, heading, tab = SERIES_PAGE
    headings = {row[2]: row[3] for row in PAGES}
    sections = ''.join(
        f'<section><h2>{number}. {headings[clip]}</h2>'
        f'<video data-page="{clip}.html" playsinline controls></video>'
        f'<div><button id="play{number - 1}">Loading&hellip;</button>'
        f'<button id="replay{number - 1}">Replay</button></div></section>'
        for number, clip in enumerate(series_order(), start=1))
    html = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{tab}</title><style>{STYLE}section{{margin:0 0 56px}}</style>'
        f'<main><h1>{heading}</h1>{sections}'
        f'<a href="/pages.html">&larr; All pages</a></main><script>{SERIES_SCRIPT}</script></html>'
    )
    out = SCRATCH / f'{slug}.html'
    out.write_text(html, encoding='utf-8')
    return f'{slug}: {out.stat().st_size:,} bytes'


if __name__ == '__main__':
    for row in PAGES:
        print(build(*row))
    print(build_series())
