# Momentum handoff — redo unit-vector dot-product similarity animation

**Written:** 2026-09-26
**App:** `Manim Trial`

> The previous Macro App launch-regression handoff is preserved at
> `agent docs/momentum-handoffs/2026-09-26_macro-app-launch-regression.md`.

## Read first

1. **`Manim Trial/ANIMATION_STYLE_RECIPE.md`** — visual and teaching-motion conventions.
2. **`Manim Trial/README.md`** — headless render and HTML delivery workflow.
3. **`Manim Trial/dot_product_directions.py`** — newest animation to revise in place.
4. **`Manim Trial/scene_style.py`** — palette, captions, pace, and pause marks.
5. **`Manim Trial/build_page.py`** — page registration; current page slug is `dot-product-directions`.

## 1. Objective and current phase

Redo the newest East–North–Northeast dot-product animation so it follows Chase's
actual classroom explanation instead of leading with the component algorithm.

The first animation should establish dot product as an expression of **how similar
two vectors are in direction**, using vectors whose magnitudes are both 1. It should
end by explicitly limiting that interpretation to unit vectors and asking:

> What happens when the vectors have different sizes?

That unanswered question is the bridge into a **second animation**, which should not
be designed or implemented until the revised first animation is accepted.

## 2. Chase's desired teaching sequence

Use this order:

1. Show one traveler going east and the other going north.
2. Establish visually and verbally that they share **no directional commonality**.
3. Only then calculate the dot product and get zero.
4. Interpret the zero as the mathematical representation of that complete lack of
   directional similarity — not merely as an arithmetic result.
5. Change the second traveler to northeast while both speeds remain 1 mph.
6. Establish visually that east and northeast now share some directional commonality.
7. Calculate the dot product and interpret approximately `0.707` as partial directional
   similarity.
8. End by explaining that this clean similarity interpretation works because both
   vectors are **unit vectors** (magnitude 1).
9. Close on the question of unequal vector sizes, setting up animation two.

The language Chase is reaching for:

- “Obviously, if I’m going north and east, I share no commonality between the directions.”
- “The zero represents that there is nothing similar between the two vectors.”
- “The dot product is looking at the similarity between the two.”
- Then qualify: for general vectors, raw dot product includes magnitude; pure directional
  similarity is only exposed directly here because both magnitudes equal 1.

## 3. Mathematical framing that is accepted

- Raw dot product:
  `u · v = ||u|| ||v|| cos(theta)`
- It is **magnitude-weighted directional similarity** in general.
- With unit vectors, `||u|| = ||v|| = 1`, so the dot product equals `cos(theta)` and can
  be read directly as directional similarity.
- East unit vector dot north unit vector is `0`.
- East unit vector dot northeast unit vector is `sqrt(2)/2 ≈ 0.707`.
- Avoid claiming that raw dot product ignores magnitude. It does not.
- Avoid using projection as the teaching foundation in this first clip. The book order is:
  dot product, angle between vectors, then projection.

## 4. Rejected directions — do not rediscover

- **Do not begin with**
  “A dot product pairs matching directions, multiplies, then adds.”
  That is the current clip's opening and explains procedure before meaning.
- **Do not begin with projection** or describe the dot product as projected amount times
  the other vector's length. The earlier clip did that well, but it conflicts with the
  desired book sequence.
- **Do not present `0` as only a coordinate-calculation outcome.** The no-commonality
  intuition must exist first, and the arithmetic must confirm it.
- **Do not call every raw dot product a pure similarity score.** Magnitudes affect it
  unless vectors are normalized.
- Do not delete the earlier animations; they may remain useful as later companions.

## 5. Current implementation state

### Newest clip to revise

- `Manim Trial/dot_product_directions.py` — 297 lines.
- Current runtime: about **40.9 seconds**, intentionally slower than the earlier clips.
- Current pause marks:
  - `east_dot_north`: 17.00s
  - `east_dot_northeast`: 31.22s
  - `meaning`: 40.33s
- Rendered successfully at **1920×1080, 30 fps**.
- HTML review page:
  `http://127.0.0.1:8765/scratch/dot-product-directions.html`
- Page returned HTTP 200.
- Python compilation and IDE lint checks passed.

The visual layout is now clean after moving the northeast labels. The needed change is
primarily the **storyboard, caption order, and interpretation**, not a fresh visual system.

### Earlier clips to preserve

- `Manim Trial/vector_projection_force.py`
  - Light-and-shadow projection explanation for the 8 N / 22 N / 50° problem.
- `Manim Trial/dot_product_projection.py`
  - Dot product explained as projection times the other vector's magnitude.
  - Chase liked the animation, but it belongs later in the instructional sequence.
- Both are registered in `Manim Trial/build_page.py` and rendered successfully.

### Git / working tree

- Programs root contains unrelated dirty work from other sessions. Do not clean, revert,
  commit, or push it.
- Relevant uncommitted files include the three Manim scenes, mark JSON files, and
  `Manim Trial/build_page.py`.
- No GitHub or end-of-session action was requested.

## 6. Constraints

- Modify the existing `dot_product_directions.py`; do not create another competing intro.
- Preserve the established navy/gold/blue/white style and top captions.
- Keep the slightly slower pace and app-friendly pause marks.
- Headless rendering is allowed. Never preview/open a GUI or browser without per-run permission.
- Deliver review pages only through the `127.0.0.1:8765` HTML link.
- Chase uses speech-to-text; “link one vectors” in the latest prompt meant **unit vectors**.
- The second animation is only a future bridge right now.

## 7. Exact next step

Revise the storyboard in `Manim Trial/dot_product_directions.py` so the visual
east-vs-north lack of commonality appears **before** the formula and calculation.
Then make the northeast case repeat the same intuition-first pattern. End with a clear
unit-vector qualification and the unanswered unequal-magnitude question. Render headlessly,
inspect frames for overlap/readability, rebuild the existing `dot-product-directions` page,
and give Chase that same link for review.
