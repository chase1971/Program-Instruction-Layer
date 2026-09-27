"""One image of every pause mark, so six beats can be checked in a glance.

Scrubbing a video to find a collision is how an hour disappears. This pulls the frame at
each mark, montages them with the mark name burned in, and writes the sheet under
`media/audit/`. This is how the `east_dot_northeast` collision was found in the first place.

    & '.\\.venv\\Scripts\\python.exe' contact_sheet.py dot_product_directions
    & '.\\.venv\\Scripts\\python.exe' contact_sheet.py dot_product_directions --page

Needs the scene rendered first. Reads the marks file and scene class from
`build_page.PAGES`, so there is no second registry to keep in step. When `scene_audit` has
written a report, each tile also says how many layout problems that beat has.

`--page` additionally writes a served HTML page, because a `.jpg` on disk is not something
Chase can open -- he gets `http://127.0.0.1:8765/scratch/<slug>-contact.html`.
"""

import base64
import glob
import json
import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

from build_page import PAGES, SCRATCH, STYLE

AUDIT_DIR = pathlib.Path('media/audit')
FRAME_DIR = AUDIT_DIR / 'frames'
# A mark is recorded at the end of its hold, so sample a hair earlier to be safely inside
# the held frame rather than on the boundary of the next animation.
LEAD = .15
COLUMNS = 3
THUMB_WIDTH = 640
LABEL_HEIGHT = 34
PAD = 6
INK = '#F2F5FA'
NAVY = '#101C30'
GOLD = '#FFC66D'
FONT_PATH = r'C:\Windows\Fonts\segoeui.ttf'


def row_for(folder):
    for row in PAGES:
        if row[0] == folder:
            return {'folder': row[0], 'klass': row[1], 'slug': row[2], 'marks': row[5]}
    return {'folder': folder, 'klass': None, 'slug': folder.replace('_', '-'),
            'marks': f'{folder}_marks.json'}


def find_video(folder, klass):
    """The most recently rendered file -- a draft leaves 480p15 beside an older 1080p30.

    Newest, not biggest: in a fix-and-recheck loop the draft you just rendered is the one
    you want to look at, and a stale 1080p frame would send you chasing a fixed collision.
    """
    found = glob.glob(rf'media\videos\{folder}\**\{klass or "*"}.mp4', recursive=True)
    return max(found, key=lambda path: pathlib.Path(path).stat().st_mtime) if found else None


def load_marks(marks_file):
    path = pathlib.Path(marks_file) if marks_file else None
    if not path or not path.exists():
        return []
    return json.loads(path.read_text(encoding='utf-8'))


def load_problems(klass):
    """Layout problems per mark, from the audit report, when there is one."""
    path = AUDIT_DIR / f'{klass}_audit.json'
    if not klass or not path.exists():
        return {}
    report = json.loads(path.read_text(encoding='utf-8'))
    return {mark['name']: len(mark['findings']) for mark in report.get('marks', [])}


def grab_frame(video, at, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{max(at - LEAD, 0):.2f}',
         '-i', video, '-frames:v', '1', str(out)],
        check=True,
    )
    return out


def _font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


def montage(tiles, out):
    """Lay the frames out in a grid with each mark's name under it."""
    columns = min(COLUMNS, len(tiles))
    rows = -(-len(tiles) // columns)
    first = Image.open(tiles[0][0])
    thumb_height = round(THUMB_WIDTH * first.height / first.width)
    cell_width, cell_height = THUMB_WIDTH + PAD, thumb_height + LABEL_HEIGHT + PAD
    sheet = Image.new('RGB', (cell_width * columns + PAD, cell_height * rows + PAD), NAVY)
    draw = ImageDraw.Draw(sheet)
    name_font, note_font = _font(23), _font(19)
    for index, (frame, name, time, problems) in enumerate(tiles):
        x = PAD + (index % columns) * cell_width
        y = PAD + (index // columns) * cell_height
        shot = Image.open(frame).convert('RGB').resize((THUMB_WIDTH, thumb_height))
        sheet.paste(shot, (x, y))
        draw.text((x + 2, y + thumb_height + 5), name.replace('_', ' '),
                  font=name_font, fill=INK)
        note = f'{time}s' if not problems else f'{time}s  ·  {problems} layout problem(s)'
        draw.text((x + THUMB_WIDTH - draw.textlength(note, font=note_font) - 2,
                   y + thumb_height + 7), note, font=note_font,
                  fill=GOLD if problems else INK)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    return out


def write_page(sheet, slug, klass, tiles):
    """Inline the sheet into a served page, the only form Chase can actually open."""
    data = base64.b64encode(pathlib.Path(sheet).read_bytes()).decode('ascii')
    beats = ''.join(
        f"<li><b>{name.replace('_', ' ')}</b> &mdash; {time}s"
        + (f' &mdash; {problems} layout problem(s)' if problems else '')
        + '</li>'
        for _, name, time, problems in tiles
    )
    html = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{klass or slug} contact sheet</title><style>{STYLE}'
        'img{width:100%;border-radius:12px}</style>'
        f'<main><h1>{slug} &mdash; one frame per mark</h1>'
        f'<img alt="contact sheet" src="data:image/jpeg;base64,{data}">'
        f'<ul>{beats}</ul>'
        f'<p><small>Animation study &middot; source: Manim Trial/{slug}</small></p>'
        '<a href="/pages.html">&larr; All pages</a></main></html>'
    )
    out = SCRATCH / f'{slug}-contact.html'
    out.write_text(html, encoding='utf-8')
    return out


def build(folder, page=False):
    row = row_for(folder)
    video = find_video(row['folder'], row['klass'])
    if not video:
        return f'{folder}: no render found — render the scene first'
    marks = load_marks(row['marks'])
    if not marks:
        return f'{folder}: no marks file ({row["marks"]}) — nothing to sheet'
    problems = load_problems(row['klass'])
    tiles = [
        (grab_frame(video, mark['time'], FRAME_DIR / f'{folder}_{mark["name"]}.png'),
         mark['name'], mark['time'], problems.get(mark['name'], 0))
        for mark in marks
    ]
    sheet = montage(tiles, AUDIT_DIR / f'{folder}_contact.jpg')
    told = f'{folder}: {len(tiles)} beats -> {sheet}'
    if page:
        told += f'\n  http://127.0.0.1:8765/scratch/{write_page(sheet, row["slug"], row["klass"], tiles).stem}.html'
    return told


if __name__ == '__main__':
    names = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    if not names:
        print(__doc__)
        sys.exit(1)
    for name in names:
        print(build(name, page='--page' in sys.argv))
