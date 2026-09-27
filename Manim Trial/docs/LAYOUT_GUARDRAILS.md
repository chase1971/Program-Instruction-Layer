# Manim layout guardrails

> **You might say:** *"things don't align correctly"* · *"things are intersecting other
> things"* · *"have a cheaper model make the animation"* · *"check the frames before you
> render the final"*
>
> **What it is:** the loop that keeps a Manim clip's frames readable without anyone looking
> at them — a layout audit that runs at every pause mark, named regions that keep panels
> apart by construction, and a contact sheet that shows every beat in one image.

**Exemplar files**

| File | Does |
|---|---|
| `Manim Trial/scene_audit.py` | the checks, and the report a model can act on |
| `Manim Trial/scene_style.py` | `Narrated.mark()` — where the audit is called from |
| `Manim Trial/scene_layout.py` | `DIAGRAM` · `WORK` · `GAUGE` · `CENTER`, and `fit_into` |
| `Manim Trial/contact_sheet.py` | one frame per mark, montaged, names burned in |
| `Manim Trial/dot_product_directions.py` | a clip whose every mark passes clean |
| `Manim Trial/test_scene_audit.py` · `test_scene_layout.py` | the checks on the checkers |

Visual and teaching-motion conventions are **not** here — they live in
`Manim Trial/ANIMATION_STYLE_RECIPE.md`. This file is only about things not colliding.

**These guardrails do not make a cheap model sufficient for this work.** They were tried that
way once and the result was rejected: `composer-2.5-fast` cleared every layout finding and
still produced a clip with no teaching motion and imprecise construction. Read
[CHEAP_MODEL_TRIAL.md](CHEAP_MODEL_TRIAL.md) before planning that again.

---

## Why it exists

A weaker model's failures here are **spatial**, not knowledge failures. It can recite
"don't overlap the labels" and still stack a three-line fraction on a gauge, because it
cannot see the frame. So the fix is not a document telling it to be careful — it is numbers
it can act on without eyes, produced automatically at the moments that matter.

`self.mark('name')` is already called at exactly those moments: a mark is a teaching hold, a
frame the viewer actually reads. The audit hooks there, so every beat of every scene —
including scenes written before any of this existed — is checked for free.

---

## The loop

1. **Write the beats.** Put content in a region: `fit_into(work, WORK)`. Keep the caption
   coming from `self.say()`, and call `self.mark('name')` on each hold.
2. **Draft render** (~18 s, no window opens):

       $env:PATH = (Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64') + ';' + $env:PATH
       & '.\.venv\Scripts\python.exe' -m manim -ql --disable_caching <scene>.py <SceneClass>

3. **Read the `[audit]` block** in the render output. Every mark prints `clean (n elements)`
   or its problems, each with a number to act on. The same thing lands in
   `media/audit/<SceneClass>_audit.json`.
4. **Apply the reported fix,** re-render, repeat until every mark says `clean`.
5. **Contact sheet** — look at the beats, because the audit only checks collisions, not
   whether the teaching reads:

       & '.\.venv\Scripts\python.exe' contact_sheet.py <scene_module>

6. **Final render** at 1920×1080 / 30 fps, then `build_page.py`, then hand Chase the
   `http://127.0.0.1:8765/scratch/<slug>.html` link. Both steps are in
   `Manim Trial/README.md`.

**Running as an agent loop?** Set `MANIM_AUDIT_STRICT=1` and the render raises at the first
offending mark, so a failing layout is a nonzero exit code. Leave it unset to see every
beat's problems in one pass.

---

## What the audit checks, and what it deliberately does not

- **Text never touches text.** Every `Text`/`MathTex`/`Tex` box against every other one,
  needing a small gap. This one rule catches almost everything Chase complains about.
- **Off frame**, with a margin.
- **The caption band** along the top, which only `self.note` may enter.
- **Type too small to read on a phone.**

**Text against shapes is not checked, on purpose.** An `Arrow`'s bounding box spans its
whole diagonal and a `SurroundingRectangle` overlaps its contents by design, so those pairs
produce nothing but noise. Look at the contact sheet for those.

The gap, the margin, the caption line and the type floors are **constants at the top of
`scene_audit.py`**. Read them there; never copy one into another file.

Deliberate text-on-text is allowed explicitly: `self.mark('name', allow=[(a, b)])`.

---

## Reading a finding

    east_dot_northeast @ 46.56s -- 1 problem
      overlap      MathTex '\langle1,0\rangle...' overlaps MathTex '\frac{\sqrt2}{2}...' by 0.25 units vertically
                   -> move MathTex '\langle1,0\rangle...' down 0.25 to center y = 0.34;
                      blocked: that move lands it on MathTex '(1)\left(\frac...' -- move them as one group, or shrink one

Elements are named by their own content, so no tagging is needed. Use `scene_audit.tag(mob,
'WORK row 1')` if a name would read better.

**The trap the report warns you about:** when a row was animated on its own —
`self.play(Write(work[0]))` — the parent `VGroup` never enters the scene, so the audit
cannot name it, and moving that one row would just create the next collision. When the fix
says *move them as one group*, change the group's center constant (e.g.
`NORTHEAST_WORK_CENTER`), not the row.

---

## Regions

`DIAGRAM` (left) · `WORK` (right) · `GAUGE` (upper right) are disjoint and may all be on
screen together. `CENTER` spans the frame for a beat that owns the screen alone — a closing
card, a title, a question — and must not be combined with the other three.

    from scene_layout import WORK, fit_into
    fit_into(make_work(), WORK)          # centers it, scaling down only if it does not fit

The four boxes are measured from `dot_product_directions.py`, whose frames were checked one
by one; `test_scene_layout.py` asserts that clip still fits them, so they cannot drift away
from a layout known to read well.

---

## Gotchas

- **Inspection artifacts go under `media/`** — that is what `Manim Trial/.gitignore`
  ignores. A `frames/` folder at the app root would get committed.
- **A draft render leaves a 480p15 file** beside the 1080p30 one. `contact_sheet.py` takes
  the newest; `build_page.py` takes the first it globs, so **render final before building
  the page.**
- **Never `-p` / `--preview`**, and never open a player or a browser — nothing reaches
  Chase's screen without per-run permission. Headless renders and these scripts are fine.
- The audit never fails a render on its own account: if the checker itself breaks it says so
  and the render continues — except under `MANIM_AUDIT_STRICT`, where a broken checker is a
  failure rather than a green light.

## Checking the checkers

    & '.\.venv\Scripts\python.exe' test_scene_audit.py; & '.\.venv\Scripts\python.exe' test_scene_layout.py

`test_scene_audit.py` rebuilds one real frame from `dot_product_directions.py` and asserts
the shipped values are clean **and** that the two values from the draft — the tall stacked
gauge readout and the higher work center — are flagged with a numeric fix. If it ever does
neither, the checker is wrong, not the clip.
