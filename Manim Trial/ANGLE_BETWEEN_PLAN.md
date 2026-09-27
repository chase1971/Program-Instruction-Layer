# Clip two plan — the angle between two vectors

The spec `angle_between_vectors.py` is built from, in the same role `PART4_PLAN.md` played
for dice part 4: verified numbers, the teaching order Chase asked for, and the traps.

**Layout is not specified here.** Follow `docs/LAYOUT_GUARDRAILS.md`: put content in a
region, call `self.mark()` on each hold, and iterate until every mark reports clean.

---

## What this clip is for

It answers the question clip one closes on. `dot_product_directions.py` ends with *"Both
speeds were exactly 1 mph. What happens when the vectors are different sizes?"* — so this
clip **opens on that question** and answers it: you normalize them. The two clips should cut
together the way the dice parts do.

Chase's own framing of the idea: the angle between two vectors *"just is really the dot
product of two unit vectors."*

---

## Teaching order — as he asked for it

1. **Open on clip one's question.** Different sizes. What now?
2. **The formula:** `cos θ = (u · v) / (‖u‖ ‖v‖)`, so `θ = arccos( (u · v) / (‖u‖ ‖v‖) )`.
3. **Show that this *is* just normalizing both vectors and dotting them:**
   `(u/‖u‖) · (v/‖v‖) = û · v̂ = cos θ`.
4. **Dividing by the magnitudes standardizes them** — that is what lets the result be read
   as a percentage rather than a size-dependent number.
5. **Connect to right triangles** — read the wording warning below before writing this beat.
6. **Work the three problems** from the textbook screenshot.

Clip one already established that `u · v = ‖u‖‖v‖cos θ` collapses to `cos θ` when both
magnitudes are 1. This clip is the general case. Do not re-teach the dot product itself.

---

## The wording warning — he said it inverted

He said: *"cosine is just the percentage of the hypotenuse to the adjacent side."*

**Cosine is adjacent ÷ hypotenuse.** The intuition he is reaching for is right; the two
words slipped. On screen, say it as **the adjacent side expressed as a fraction — or
percentage — of the hypotenuse**. Get this right; it is the one line in the clip that would
teach something false.

---

## The three problems

Given `u = 2i − 2j`, `v = 5i + 8j`, `w = 4i + 4j`.

| | pair | dot | magnitudes | cos θ | θ |
|---|---|---|---|---|---|
| a | u, v | −6 | `‖u‖ = 2√2 ≈ 2.8284`, `‖v‖ = √89 ≈ 9.4340` | `−3/√178 ≈ −0.22486` | **≈ 102.99°** |
| b | v, w | 52 | `‖v‖ = √89 ≈ 9.4340`, `‖w‖ = 4√2 ≈ 5.6569` | `13/√178 ≈ 0.97439` | **≈ 12.99°** |
| c | u, w | 0 | `‖u‖ = 2√2`, `‖w‖ = 4√2` | `0` | **exactly 90°** |

Unit vectors — the point of the clip. Their dot products reproduce the cosines exactly:

- `û = ⟨0.7071, −0.7071⟩` · `v̂ = ⟨0.5300, 0.8480⟩` · `ŵ = ⟨0.7071, 0.7071⟩`
- `û · v̂ = −0.22486` · `v̂ · ŵ = 0.97439` · `û · ŵ = 0`

Each equals its `cos θ` in the table. Showing that is the payoff beat.

**Every value above was computed and checked. Put these on screen; do not recompute them,
and do not invent any number that is not here.** Signs matter: part (a) is negative, which
is why its angle is obtuse — worth showing, not hiding.

**Part (c) is a typo in the textbook.** The screenshot's part (c) says "u and v", which just
repeats part (a). With **w** it gives exactly 90°, which is obviously the intended problem,
and it lands as a callback to clip one's east-versus-north zero. Treat it as `u` and `w`.

---

## Traps

- **Do not build the teaching on projection.** The book's order is dot product → angle
  between vectors → projection. `dot_product_projection.py` is good work that belongs later.
- **Do not call a raw dot product a similarity score.** `u · v = ‖u‖‖v‖cos θ` is
  magnitude-weighted; only after normalizing does the number express direction alone. That
  distinction is the whole reason this clip exists.
- **Do not present the zero in part (c) as just an arithmetic outcome.** The
  no-commonality intuition comes first, the arithmetic confirms it — same order as clip one.
- **Do not re-cut clip one.** It is awaiting review.
- American spellings on screen — "center", never "centre".
