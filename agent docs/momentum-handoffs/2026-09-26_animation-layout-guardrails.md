# Momentum handoff — animation layout guardrails, then the angle-between-vectors clip

**Written:** 2026-09-26
**App:** `Manim Trial`
**Next agent:** Opus 5 (Chase said so explicitly — you are not the cheap model being tested)

> The previous handoff in this thread is preserved at
> `agent docs/momentum-handoffs/2026-09-26_dot-product-similarity-animation.md`.
> Its rejected-directions list is still binding and is restated in § 5 below.

## Read first

1. **`Manim Trial/scene_style.py`** — 98 lines. Owns the palette, the top caption line,
   `PACE`, and the `Narrated` mixin with `mark()` / `write_marks()`. **The audit hooks into
   `mark()`** — that is the whole design, so read this before writing anything.
2. **`Manim Trial/dot_product_directions.py`** — 401 lines. The reference clip, revised and
   rendered this session. Its layout constants are the audit's first test fixture.
3. **`Manim Trial/ANIMATION_STYLE_RECIPE.md`** — visual and teaching-motion conventions.
4. **`Manim Trial/README.md`** — headless render, pause marks, and the `build_page.py`
   HTML delivery workflow.
5. **`Manim Trial/build_page.py`** — `PAGES` table; the slug in play is `dot-product-directions`.
6. **`agent docs/recipes/INDEX.md`** — has **no Manim row at all** today. The new recipe's
   row goes in this table; that missing row is a real routing gap, already logged.
7. **The textbook screenshot for the next clip** (Chase pasted it this session):
   `C:\Users\chase\.cursor\projects\c-Users-chase-Documents-Programs\assets\c__Users_chase_AppData_Roaming_Cursor_User_workspaceStorage_09d76da3e651a4e97d24a412fbec7f6c_images_image-985ed725-064b-4d73-9bc9-915f3b4873b3.png`

---

## 1. Objective and current phase

Three live threads, in priority order.

**A. Clip one — revised, delivered, not yet reviewed.** The east/north/northeast dot-product
clip now teaches directional similarity before the arithmetic. It is rendered and linked.
**Chase has not said whether he accepts it.** Do not re-cut it on your own initiative.

**B. Layout guardrails — approved, not started. This is the next build.** Chase wants to stop
paying Opus prices for these animations. He has handed this work to cheaper models before and
got back frames where, in his words, *"things like, don't align correctly or… things are
intersecting other things."* He approved building guardrails so a weaker model can do it.

**C. Clip two — content specified by Chase this session, not started.** The angle between two
vectors / cosine similarity, worked through the three problems in the screenshot. Full verified
spec in § 6. This clip is the intended **validation run** for thread B.

---

## 2. Why the guardrails are shaped this way — the reasoning to keep

Chase's exact motivation: *"I just can't really afford the tokens on Opus. To do this, cause
it's pretty taxing."* He asked whether a *"less intuitive model"* could be taught to do these.

The argument that won, and which the next agent should not relitigate: **a weaker model's
failures here are spatial-reasoning failures, not knowledge failures.** It can recite "don't
overlap the labels" and still stack a three-line fraction on top of a gauge, because it cannot
see the frame. So prose instruction is not the fix. The fix is to make collisions structurally
hard, and to turn "does this look right" into **numbers a blind model can act on**.

The lever already exists in the codebase: **`self.mark('name')` is called at exactly the
moments a frame must be readable** — a mark *is* a teaching hold. Hook the audit there and
every beat of every scene, including the ones already written, gets checked for free. This is
extending the existing mechanism, not adding a parallel one (root `AGENTS.md` rule 4). Grepped
`Manim Trial/*.py` for `overlap|audit|bounding|region` — **no matches**, so there is nothing
else to extend and no second implementation risk.

---

## 3. Accepted decisions

**Chase approved this option verbatim:** *"Full guardrails — layout audit inside `mark()`,
named layout regions, auto contact sheet, short recipe — then prove it by having a cheap model
build a fresh clip while I watch."* Those four components plus the validation run are decided.

Everything in § 4 below is **my design proposal**, worked out in conversation but not
separately ratified by Chase. It is a good starting point, not scripture — but do not throw it
out without a reason, and do not expand it into a framework.

---

## 4. Proposed design for the four components

### 4a. The audit — `Manim Trial/scene_audit.py`, called from `Narrated.mark()`

Keep it a separate module and keep `scene_style.py` small and single-purpose. `mark()` calls
into it; the audit collects findings on the scene and writes them out alongside the marks.

**The one rule that catches Chase's complaint with almost no false positives: text must never
touch text.** Every `Text` / `MathTex` / `Tex` bounding box versus every other one, requiring a
small gap (~0.08 scene units). Do **not** error on text-vs-shape pairs — an `Arrow`'s bounding
box spans its whole diagonal and a `SurroundingRectangle` overlaps its contents by design, so
those pairs generate nothing but noise.

Also check, for everything on screen:

- **Off-frame.** Frame is 14.22 × 8 scene units (x ∈ [−7.11, 7.11], y ∈ [−4, 4]). Require a
  margin, ~0.25.
- **The caption band.** `scene_style.CAPTION_Y` is 3.3 and the recipe reserves the top for it:
  nothing but the caption may sit above about y = 2.9. The caption itself is exempt — it is
  `self.note`, so it is identifiable.
- **Unreadably small type.** Flag `MathTex` scaled below roughly 0.5 and `Text` below about
  font size 15.

**Implementation subtleties that will cost the next agent an hour if not passed on:**

- Walk the scene to leaves, **but treat a whole `Text`/`MathTex` as one box — do not descend
  into it.** A `MathTex`'s submobjects are individual glyphs; per-glyph boxes would report
  thousands of meaningless "overlaps" inside a single fraction.
- Boxes come from `get_left()/get_right()/get_top()/get_bottom()`, or `width`/`height`.
- Indexed parts like `work[2][1]` are submobjects of one `MathTex`; the parent is the unit.
- Provide an escape hatch for deliberate text-on-text (none exists in today's scenes, but it
  will come up): something like `self.mark('name', allow=[(a, b)])`.

**Report shape matters more than the check.** The failing line should read close to:

    east_dot_northeast: WORK row 1 overlaps GAUGE_VALUE by 0.31 units
      -> lower work center to about -1.05, or scale the row to 0.66

That is the note I wrote by hand today after looking at a frame. A cheap model can act on that
without eyes; it cannot act on "the layout looks wrong." Print the block, and also write
`media/audit/<scene>_audit.json`.

Default to **non-fatal** (print and keep rendering, so one pass surfaces every beat's problems
at once) with a strict mode — env var, e.g. `MANIM_AUDIT_STRICT=1` — that raises, so an agent
loop gets a nonzero exit code to iterate against.

### 4b. Named layout regions — `Manim Trial/scene_layout.py`

Declare non-overlapping slots with real bounding boxes so panels cannot collide by
construction: a diagram panel (left), a work panel (right), a gauge slot (upper right), and a
full-width center used by closing cards. Plus a `fit_into(mobject, region)` that scales down
and centers if the content is too wide or tall. Today's clip has those positions as loose
constants (`WORK_CENTER`, `NORTHEAST_WORK_CENTER`, `METER_CENTER`, `NORTHEAST_LABEL_CENTER`) —
they are the raw material for the region definitions, and migrating that clip onto the regions
is the proof the API is usable.

### 4c. Contact sheet

A script that reads the marks JSON, pulls one frame per mark with `ffmpeg`, and montages them
into a single image with mark names burned in — so any model or Chase can check six beats in
one glance instead of scrubbing video. This is exactly how I found today's collision.

**Write inspection artifacts under `media/`** (e.g. `media/audit/`). `Manim Trial/.gitignore`
ignores `media/`, `.venv/`, `__pycache__/`, `*.log` — and nothing else. I created a `frames/`
folder this session and had to delete it because it would have been committed.

### 4d. The recipe

Short and procedural at rung 3, not a philosophy document. The loop it teaches:
write the beats → render draft (`-ql`, ~18s) → read the audit block → fix the reported numbers
→ contact sheet → final 1080p30 → `build_page.py` → hand over the `127.0.0.1:8765` link.
Add the row to `agent docs/recipes/INDEX.md` (and check `agent docs/INDEX.md` too — neither has
a Manim row today). Existing Manim guidance lives in `Manim Trial/ANIMATION_STYLE_RECIPE.md`;
**extend it or point at it, do not restate it** — content lives in exactly one file.

### 4e. The validation run — my proposed division of labor

Chase wants to watch a cheap model build a fresh clip. **Proposal:** Opus writes the beat spec
(teaching order, exact captions, verified numbers — § 6 is already that spec), and the cheap
model implements the layout and iterates against the audit. That splits the work where each
model is actually strong and protects Chase's lesson content from a weak model's math. Which
model to use is **undecided** — see § 7.

---

## 5. Rejected directions — do not rediscover

**New this session:**

- **Do not "fix" this with a prose document telling models to be careful about spacing.**
  That is what already failed. Guardrails are code.
- Do not build a second pause-mark or timing mechanism. `mark()` / `write_marks()` exists.
- Do not write inspection PNGs anywhere outside `media/`.
- Never create `.cursor/rules/*.mdc` — retired 2026-08-02.

**Carried forward from clip one, still binding for the whole series:**

- Do not open a clip with procedure: *"A dot product pairs matching directions, multiplies,
  then adds."* Meaning comes before mechanics.
- Do not build the teaching on **projection** before the book's order allows it. The order is
  dot product → **angle between vectors** (clip two) → projection. The existing
  `dot_product_projection.py` is good work that simply belongs later.
- Do not present `0` as merely a coordinate-calculation outcome — the no-commonality intuition
  must exist first, and the arithmetic confirms it.
- Do not call a raw dot product a pure similarity score. `u · v = ‖u‖‖v‖cos θ` is
  magnitude-weighted; only normalized vectors expose direction alone.
- Do not delete the earlier animations. `vector_projection_force.py` and
  `dot_product_projection.py` stay as later companions.

---

## 6. Clip two — Chase's spec, with numbers already verified

He described this in his own words this session. **All values below were computed and checked
this session; they are safe to put on screen.**

### The teaching order he asked for

1. Show the formula for the angle between two vectors:
   `cos θ = (u · v) / (‖u‖ ‖v‖)`, so `θ = arccos(…)`.
2. Show that this *is* just normalizing both vectors and taking their dot product:
   `(u/‖u‖) · (v/‖v‖) = û · v̂ = cos θ`. His words: the angle between two vectors
   *"just is really the dot product of two unit vectors."*
3. Explain that dividing by the magnitudes **standardizes** them, which is what lets the
   result be read as a percentage.
4. Then connect to right triangles — see the wording warning below.
5. Work the three problems from the screenshot.

### The wording warning — he said it inverted

His transcription: *"cosine is just the percentage of the hypotenuse to the adjacent side."*
**Cosine is adjacent ÷ hypotenuse.** Say it as: the adjacent side expressed as a fraction, or
percentage, **of the hypotenuse**. Get this right on screen; the intuition he is reaching for
is correct, only the order of the two words slipped.

### The three problems

Given `u = 2i − 2j`, `v = 5i + 8j`, `w = 4i + 4j`.

| | pair | dot | magnitudes | cos θ | θ |
|---|---|---|---|---|---|
| a | u, v | −6 | ‖u‖ = 2√2 ≈ 2.8284, ‖v‖ = √89 ≈ 9.4340 | −3/√178 ≈ −0.22486 | **≈ 102.99°** |
| b | v, w | 52 | ‖v‖ = √89 ≈ 9.4340, ‖w‖ = 4√2 ≈ 5.6569 | 52/(4√178) ≈ 0.97439 | **≈ 12.99°** |
| c | u, w | 0 | ‖u‖ = 2√2, ‖w‖ = 4√2 | 0 | **exactly 90°** |

Unit vectors, which is the point of the clip — their dot products reproduce the cosines exactly:

- `û = ⟨0.7071, −0.7071⟩`, `v̂ = ⟨0.5300, 0.8480⟩`, `ŵ = ⟨0.7071, 0.7071⟩`
- `û · v̂ = −0.22486` · `v̂ · ŵ = 0.97439` · `û · ŵ = 0` — each equals its `cos θ` above.

### Two things worth telling Chase

- **The screenshot's part (c) says "u and v", which duplicates part (a).** With **w** it gives
  exactly 90°, which is obviously the intended problem — and it lands as a callback to clip
  one's east-versus-north zero. Treat it as `u` and `w`, and mention the typo to him.
- **Clip two answers clip one's closing question.** Clip one ends on *"What happens when the
  vectors are different sizes?"* The answer is: normalize them. Open on that question so the
  two clips cut together, the way the dice series parts do.

---

## 7. Open questions and constraints

**Open:**

- **Clip one is unreviewed.** Chase has not said the revision is good. Ask before re-cutting it.
- **Which cheap model does the validation run is undecided.** He said *"a dumber model… that
  sounds rude, but like, a less intuitive model."* Available slugs include
  `composer-2.5-fast`, `gemini-3.8-flash-high`, `grok-4.7-high-fast`, `muse-spark-1.3-high`,
  `claude-sonnet-5-thinking-high`, `claude-opus-5-5-medium`. He wants to **watch** the run.
- Whether the existing clips get migrated onto the regions, or only new ones.

**Constraints:**

- **Never put anything on his screen without per-run permission.** No Manim `-p`/`--preview`,
  no player, no browser. Headless rendering and `py_compile` are fine unasked.
- Deliver review pages **only** as `http://127.0.0.1:8765/<name>.html` links — never a `C:\`
  path or `file:///`.
- **Do not commit or push.** A handoff is a continuation boundary. Programs root has unrelated
  dirty work from other sessions; leave it alone.
- Chase speaks every prompt through speech-to-text. Expect misheard technical terms; ask only
  when the literal transcription would produce something noticeably wrong. (This session:
  *"link one vectors"* meant **unit vectors**; the cosine inversion in § 6 is the same class.)
- File caps: hard 800 lines, extract before 700. `scene_style.py` is 98 lines with room, but
  the audit belongs in its own module anyway.
- Bump session tracking after each completed deliverable:
  `node scripts/append-session-scorecard.js --note "<what you finished>"`.

---

## 8. Current implementation state

### Clip one, as delivered this session

`Manim Trial/dot_product_directions.py` — **401 lines**, fully rewritten storyboard.

Beats: both travelers at 1 mph in words → 90° corner and the question → an empty
**directional-similarity gauge** (the clip's through-line) → only then components, the
arithmetic, and the zero flying up to sit under the gauge → friend turns northeast, 45° arc,
gauge fills partway with **no number on it** → components and calculation put ≈ 0.707 under the
gauge → `u · v = ‖u‖‖v‖cos θ` reduced to `cos θ` because both magnitudes are 1, restated as
`cos 90° = 0` and `cos 45° ≈ 0.707` → closing card alone on screen: *"Both speeds were exactly
1 mph. What happens when the vectors are different sizes?"*

- **63.1 s**, 1920×1080, 30 fps. `pace = .9`, intentionally slower than the earlier clips.
- Six marks in `dot_product_directions_marks.json`: `no_commonality` 14.0 ·
  `east_dot_north` 24.78 · `some_commonality` 33.22 · `east_dot_northeast` 46.56 ·
  `unit_vectors_only` 56.44 · `open_question` 62.5.
- Page rebuilt with a new blurb in `build_page.py`; returns **HTTP 200**, 3,888,068 bytes.
  `http://127.0.0.1:8765/scratch/dot-product-directions.html`
- `py_compile` clean, no lint findings, draft frames inspected at every mark.

### The collision I fixed — use it as the audit's regression test

The draft put the gauge readout on top of the first row of the northeast work: three stacked
fractions are much taller than they look, and the readout was a stacked fraction too. Fixes:
the readout became one line (`\approx 0.707`), and the northeast work got its own lower center
plus smaller type.

**This gives the audit a free, real regression test.** Temporarily set
`NORTHEAST_WORK_CENTER` back to `[2.9, -.6, 0]` and `make_meter_value` back to
`r'\frac{\sqrt2}{2}\approx0.707'`, and the audit **must** flag an overlap at the
`east_dot_northeast` mark. With the current values it **must** pass. If it does neither, the
checker is wrong — not the clip.

### Exact commands that work (PowerShell 5.x — no `&&`)

    # from Manim Trial, MiKTeX on PATH for the process:
    $env:PATH = (Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64') + ';' + $env:PATH

    # draft, ~18-28s
    & '.\.venv\Scripts\python.exe' -m manim -ql --disable_caching dot_product_directions.py DotProductDirections
    # final, ~36s
    & '.\.venv\Scripts\python.exe' -m manim -r 1920,1080 --fps 30 --disable_caching dot_product_directions.py DotProductDirections
    # one frame at a mark time
    ffmpeg -loglevel error -y -ss 46.0 -i media\videos\dot_product_directions\1080p30\DotProductDirections.mp4 -frames:v 1 out.png
    # rebuild every page, then verify
    & '.\.venv\Scripts\python.exe' build_page.py
    Invoke-WebRequest -Uri 'http://127.0.0.1:8765/scratch/dot-product-directions.html' -UseBasicParsing

The docs server (`node scripts/serve-programs-docs.js`) is already running and should be left
running.

### Git

Uncommitted and intentionally so: the three Manim scenes, their marks JSON, `build_page.py`.
Unrelated dirty work from other sessions sits elsewhere in Programs. No GitHub or
end-of-session action was requested or performed.

---

## 9. Exact next step

**Create `Manim Trial/scene_audit.py` and hook it into `Narrated.mark()` in
`scene_style.py`** — text-versus-text overlap, off-frame margin, the caption band above
y ≈ 2.9, and minimum readable type, reported as named offenders with the gap in scene units and
a suggested direction to move.

Prove it in one draft render of `dot_product_directions.py`: it must **pass** on the file as it
stands, and must **flag the `east_dot_northeast` overlap** when the two pre-fix values in § 8
are temporarily restored. Only after that behaves correctly, build the regions, the contact
sheet, and the recipe row — then bring Chase the model choice for the validation run on clip
two.
