"""Export only the existing angle problem's formulas, with original geometry.

Run headlessly from Manim Trial. No Scene.play, video, or new typesetting layout.
The portal uses the transparent frame as an alpha mask so only its color changes.
"""

import ast
import json
from pathlib import Path

from manim import Camera, VGroup, WHITE, config

import angle_between_vectors as source


def export():
    root = Path(__file__).resolve().parent
    output = root.parent / 'School Scrips/student-portal/src/features/visual-test'
    output.mkdir(parents=True, exist_ok=True)
    tree = ast.parse((root / 'angle_between_vectors.py').read_text(encoding='utf-8-sig'))
    method = next(node for node in ast.walk(tree)
                  if isinstance(node, ast.FunctionDef) and node.name == 'problem_a')
    call = next(node for node in ast.walk(method)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == 'make_problem_rows')
    arguments = [ast.literal_eval(arg) for arg in call.args[1:]]
    given = source.make_given()
    rows = source.make_problem_rows(given, *arguments)
    formulas = VGroup(given, rows)
    camera = Camera(pixel_width=1920, pixel_height=1080, background_opacity=0)
    camera.capture_mobjects([formulas.set_color(WHITE)])
    camera.get_image().save(output / 'angle-formulas.png')
    metadata = {
        'source': 'angle_between_vectors.py: AngleBetweenVectors.problem_a',
        'frameWidth': 1920, 'frameHeight': 1080,
        'sceneFrameWidth': config.frame_width,
        'fitFactor': float(rows.fit_factor),
        'givenFontSize': float(given.font_size),
        'rowFontSizes': [float(row.font_size) for row in rows],
        'rowGlyphHeightsAt360': [float(row.height / config.frame_width * 360) for row in rows],
        'formulas': arguments,
    }
    (output / 'angle-formulas.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    export()
