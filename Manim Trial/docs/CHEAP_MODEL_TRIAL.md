# Cheap-model trial — composer-2.5-fast on a Manim teaching clip

**Run:** 2026-09-26 · **Model under test:** `composer-2.5-fast` · **Clip:** `angle_between_vectors.py`
**Verdict: not good enough. These clips need a higher-tier model.**

---

## The verdict, stated plainly

`composer-2.5-fast` — **even with a higher-level model supplying a fully verified content
spec, and an automated layout audit feeding it numeric corrections at every beat** —
produces animations that are **inexact and not correctly composed**. The result is a
slideshow of accurate equations, not a taught animation.

Chase reviewed the output and rejected it. The clip is left on disk as it is.

**Be precise about what is wrong, or you will hunt in the wrong place:** the
**mathematics on screen is correct** — every value was checked. What is wrong is the
**animation craft**: elements placed approximately rather than deliberately, and essentially
no teaching motion. Do not go looking for arithmetic errors. There aren't any.

---

## What it was given — it was not under-briefed

| Supplied | What it provided |
|---|---|
| `ANGLE_BETWEEN_PLAN.md` | teaching order, exact captions, every number pre-verified, the wording traps, the textbook typo |
| `docs/LAYOUT_GUARDRAILS.md` | the render → read audit → fix → re-render loop |
| `scene_layout.py` | four named non-overlapping regions plus `fit_into()` |
| `scene_audit.py` | per-beat numeric findings: which element, how far it overlaps, the center coordinate or `.scale()` value that fixes it |
| `dot_product_directions.py` | a finished sibling clip, explicitly named as the model to imitate |
| `ANIMATION_STYLE_RECIPE.md` | the visual and teaching-motion conventions |

A higher-tier model wrote the spec; the cheap model was asked only to implement the layout
and iterate against the audit. That division was the whole point of the experiment.

---

## What it got right

Worth recording, because it says something real about where the line falls — and so the next
tool does not redo this part.

- **All mathematics correct.** `u·v = −6`, `θ ≈ 102.99°`; `v·w = 52`, `θ ≈ 12.99°`;
  `u·w = 0`, `θ = 90°` exactly. Magnitudes, cosines and the unit-vector dot products all
  match the verified table.
- **Avoided the one wording trap.** Cosine is on screen as *"the adjacent side as a fraction
  of the hypotenuse"* — the right way round.
- **Handled the textbook typo**: part (c) uses `w`, not a repeat of `v`.
- **Cleared every layout finding.** Ten problems across four beats on its second pass —
  overlapping gauge labels, type below the readable floor — all fixed from the reported
  numbers alone, reaching nine clean marks in three renders. Verified independently under
  `MANIM_AUDIT_STRICT=1`: exit 0.
- **Respected every hard constraint**: no window or preview opened, did not edit the
  checkers, did not touch clip one, wrote artifacts only under `media/`.

**So the guardrails worked.** Spatial correctness became mechanical and the cheap model
handled it. That is not where it failed.

---

## What is actually wrong with the output

Beat by beat, from the contact sheet:

- **No teaching motion anywhere.** The sibling clip turns an arrow to northeast, sweeps a
  45° arc, fills a gauge, and flies the computed zero up to sit beneath it. This clip writes
  static blocks of text onto a static diagram. Nothing transforms into anything.
- **Imprecise construction.** The diagram is a small bare axis cross; the vectors are not
  drawn to any considered scale; the `u` and `v` labels are crowded at the origin. The right
  triangle in the cosine beat is a crude shape rather than a constructed figure related to
  the vectors being discussed.
- **Prose dumped on screen.** The `standardize` beat is a paragraph of small muted text.
  That is a slide, not a beat.
- **Said twice.** The `right_triangle` beat states the cosine sentence as caption text *and*
  again as a labeled formula beside the triangle.
- **Continuity break.** The gauge's `opposite directions / same direction` legend is present
  through problem (a), then **disappears** for (b) and (c) — it was deleted to resolve an
  overlap rather than relocated. The audit accepted that, because an absent element cannot
  collide.
- **A stray artifact** sits to the left of the gauge track in problem (c).
- **Closing beat is too dense**: six lines of algebra appearing at once.

---

## Diagnosis — why it failed, and what was actually tested

The guardrails turn *"does this look right"* into numbers, and a weak model can act on
numbers. They say nothing about **choreography**, and choreography is where the teaching
quality lives.

**The spec left motion unspecified on purpose.** `ANGLE_BETWEEN_PLAN.md` says in so many
words *"Layout is not specified here"* — it gave teaching order, captions and numbers, and
left every transform decision to the cheap model. So what this run measured is
**content-spec-only**, and the finding is narrower than "cheap models can't do Manim":

> A cheap model can be trusted with spatial **correctness**. It cannot be trusted with
> storyboard **taste** or precise construction.

Two things were therefore **not** tested, and remain open if anyone wants to retry:

1. Specifying the choreography **transform by transform** in the spec.
2. Having the higher-tier model write `construct()` and the `self.play(...)` calls — where
   the taste lives, and comparatively few tokens — and letting the cheap model write only the
   `make_*` factory functions, which are mechanical and audit-checkable.

Neither is a prediction that they would work.

---

## Picking this up

- **The clip is left as-is.** It needs re-cutting for **choreography and precision**, not for
  mathematics.
- **Reuse the numbers in `ANGLE_BETWEEN_PLAN.md` exactly. Do not recompute them.** They are
  checked, including the sign on part (a) and the textbook typo on part (c).
- **Keep the audit in the loop.** It catches collisions regardless of who is writing — the
  overlap it now flags in `dot_product_directions.py`'s draft was shipped by a top-tier
  model and took a human eye to find.
- **Do not re-cut `dot_product_directions.py`** (clip one). It is awaiting Chase's review.
- The audit cannot see a *missing* element. If a fix deletes something to resolve an
  overlap, that is a regression it will report as clean — check the contact sheet.

**Files:** `angle_between_vectors.py` (465 lines, 9 marks, 61 s) ·
`angle_between_vectors_marks.json` · one `PAGES` row in `build_page.py` ·
contact sheet at `media/audit/angle_between_vectors_contact.jpg`.
Nothing is committed.

---

## Re-cut — 2026-09-27 (Opus)

`angle_between_vectors.py` was rewritten; the draft above is in git history (`c22a550`).
The placement bugs Chase saw came from three mechanical causes, worth knowing because the
audit cannot catch any of them:

1. **`fit_into` called on a group that mixed on-screen and new objects.** The axes had
   already been moved and scaled, and new arrows built at the raw `ORIGIN` were then fitted
   *together* with them, so from part (a) on the vectors no longer started at the axes' origin.
2. **The gauge was fitted into `GAUGE`, but the fill was still built from the raw
   `METER_CENTER` / `METER_WIDTH` constants.** So the fills landed on the heading, and the
   zero fill in (c) became the stray sliver to the left of the track.
3. **Hard-coded label sides.** The `u` label sat `UP` of an arrow pointing down-right, which
   put it at the origin.

The fix is structural: every diagram object is built from one `view` (origin + scale), and
motion is `rebuild(mob, lambda alpha: build(...))`, so arrows, arc, circle and gauge fill
are exact on every frame, and none of them is ever positioned after it is built.
