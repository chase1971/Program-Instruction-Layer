# Momentum handoff — Fraction-add-fractions Manim polish

**Written:** 2026-09-17 (Thursday, ~6:27 PM)

---

## 1. Objective and current phase

**Active thread:** Polishing the standalone Manim animation `Manim Trial/fraction_add_fractions.py`
(fraction addition with common denominators) — this is the source for the Q9 "add/subtract
fractions" help video referenced in the 2026-09-16 guided-practice handoffs, but **wiring it into
the student portal is a separate, still-deferred step** (not touched this session).

**Phase:** Two rounds of animation-detail changes made and rendered this session, both verified
headlessly (low-quality render → ffmpeg frame grabs viewed as images → final 1080p60 render →
`build_page.py` → HTTP 200 check). **Chase confirmed round 1** ("that looks good"). **Round 2 is
rendered and live but not yet reviewed by Chase** — that's the next step.

**Link Chase has:** `http://127.0.0.1:8765/scratch/fraction-add-fractions.html`

---

## 2. Chase's desired feel

- **Multiplier reveal:** the fraction bar and both numbers must stay completely still while the
  `factor×` label fades in — no shifting the numbers, no widening the bar. Numerator label fades
  in first, then the denominator label (sequential, not simultaneous).
- **Multiplier placement is "outside" each fraction, never in the crowded middle near the plus
  sign.** Left-hand fraction: multiplier prefixes the number (`3×2`), positioned to its left.
  Right-hand fraction: multiplier **suffixes** the number (`1×5`), positioned to its **right** —
  because the two fractions sit close together (like his handwritten work) and putting a second
  multiplier on the inside/left of the right fraction reads as awkward and cluttered.
- **Skip the multiplier animation entirely when a side is already at the common denominator**
  (scale would be ×1) — don't show a pointless `1×`.
- **The `factor×number` pair should morph directly into the product** (e.g. `3×2` → `6`), not
  fade out and pop in separately.
- **The combine-to-one-denominator step already matched his taste from round 1** — plus sign
  moves to the middle without morphing, one bar is drawn underneath, one shared denominator
  fades in. Untouched, still correct.
- **After the sum, the bar must shrink back to a normal single-fraction width.** He specifically
  did not want it to stay stretched to the "numerator + numerator" width once it's just one digit.
- **Wants a "reduce to lowest terms" step** added after the sum, but only when the sum is
  actually reducible — no extra step when it's already in lowest terms.
- **Pace: this scene 20% slower, no exceptions** — he initially considered exempting "easy" steps
  like the final sum, then explicitly retracted that: "just make everything twenty percent
  slower."
- **Trim redundant examples:** two whole-number-plus-fraction examples felt repetitive with each
  other; keep one whole+fraction example plus the negative-whole one, since the negative case
  actually shows something different.

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Per-scene `pace` class attribute on `Narrated` (`scene_style.py`), defaults to module `PACE` (1.2) | Lets `FractionAddFractions` override to `pace = 1.0` (20% slower) **without** slowing every other Manim scene (dice, fraction_times_whole, etc.) |
| `add_multiplier(parts, factor, side='left'\|'right')` | `'left'` prefixes `factor×number` positioned LEFT; `'right'` suffixes `number×factor` positioned RIGHT — one method, both placements |
| Skip multiplier+morph entirely when `scale == 1` | Matches "don't times the other side by anything" for 1/2 + 1/6 (right side already at denominator 6) |
| `morph_product` group-transforms `VGroup(factor_label, number)` straight into the product tex, then swaps mobject identity in place (`parts.top = new_top`) | Clean morph with no leftover fragment artifacts; verified via frame grabs |
| `morph_sum` now also takes `combined_bar` + `denominator_mobject`, computes `new_width = max(final_top.width, denominator_mobject.width) + .3` floored at `BAR_WIDTH`, and `Transform`s the bar down to that width in the same `self.play` as the numerator morph | "Bar should get smaller so it looks like a normal fraction bar" |
| `simplify_result(top, bottom, numerator, denominator, prefix)` — `math.gcd`, no-op + no mark if `gcf <= 1` | Verified: only `frac_two` (4/6→2/3) triggers `{prefix}_simplified`; both whole examples and `frac_one`/`frac_three` correctly skip it |
| Removed `show_whole_plus_fraction(3, 2, 5, 17, 'whole_two')` from `construct()` | "very repetitive with the one term" |
| Verify via `-ql` render → ffmpeg frame grabs (seek **after** `-i`, not before — before-`-i` seeking can land on the wrong keyframe and show a stale frame) → view as images with the Read tool → only then `-qh` final render + `build_page.py` | No GUI/preview ever opened (README.md rule); this is how correctness was confirmed both rounds without Chase watching video in-chat |

---

## 4. Rejected directions — do not redo

- Widening/shifting the fraction bar and numbers during the multiplier reveal — this was the
  *original* behavior Chase explicitly rejected round 1; do not reintroduce.
- Simultaneous fade-in of both multiplier labels — rejected in favor of sequential (top, then
  bottom).
- Showing a multiplier for a side already at the common denominator (the old `×1` case on the
  1/6 side) — rejected as pointless clutter.
- Putting the right-hand fraction's multiplier on its left/inside — rejected, reads as awkward
  because the two fractions sit close together; outside/right placement is correct for the right
  fraction specifically (left fraction's multiplier stays on its own outside, i.e. the left).
- Editing the shared module-level `PACE` constant in `scene_style.py` directly — rejected because
  it would silently change every other scene's speed; use the per-scene `pace` override instead.

---

## 5. Current implementation state (uncommitted)

`git status --short` for the touched paths:

```
 M "Manim Trial/fraction_add_fractions.py"
 M "Manim Trial/fraction_add_fractions_marks.json"
 M "Manim Trial/pyproject.toml"
 M "Manim Trial/scene_style.py"
 M "agent docs/scratch/fraction-add-fractions.html"
```

| File | Role |
|---|---|
| `Manim Trial/fraction_add_fractions.py` | All changes above; class-level `pace = 1.0`; `add_multiplier`/`morph_product`/`morph_sum`/`simplify_result` all reworked; `whole_two` example removed |
| `Manim Trial/scene_style.py` | `Narrated` gained `pace = PACE` class attr; `play`/`wait` read `self.pace` instead of the module global — additive, backward-compatible for every other scene |
| `Manim Trial/fraction_add_fractions_marks.json` | Regenerated by the final render — no `whole_two_*` marks; `frac_two` shows only one multiplier→morph gap (right side skipped); `frac_two_simplified` present, no other `*_simplified` marks |
| `agent docs/scratch/fraction-add-fractions.html` | Rebuilt via `Manim Trial/build_page.py`; served, verified HTTP 200 at `http://127.0.0.1:8765/scratch/fraction-add-fractions.html` |
| `Manim Trial/pyproject.toml` | Picked up an unrelated `[tool.basedpyright]` venv-path stanza — looks like tooling auto-edit, not something written intentionally this session; harmless, flagging for awareness only |
| `Manim Trial/media/videos/fraction_add_fractions/**` | Render output, gitignored, not tracked — both 480p15 (quick check) and 1080p60 (final) present |

### Verification performed
- `-ql` render exit code 0 both rounds.
- ffmpeg frame grabs at every mark timestamp, viewed as images, confirmed: no bar movement during
  multiplier reveal, sequential label fade, correct left/right multiplier placement, clean morphs,
  bar shrink after sum, simplify triggers only for 4/6→2/3, `whole_two` absent from marks.
- Final `-qh` render exit code 0, `build_page.py` rebuilt the page, HTTP 200 confirmed.
- **Not yet done:** Chase has not reviewed round 2 in the browser.

---

## 6. Open questions and constraints

- **Do not commit/push** unless Chase asks.
- **Never launch a GUI/preview player** — `Manim Trial/README.md` explicitly forbids `-p`/
  `--preview`; all verification must stay headless (frame grabs, not live playback).
- **Portal wiring is still deferred** — this animation is not yet connected to
  `fractionHelpTopics.ts` / the Q9 help panel in the Matrix app or student-portal. Don't start
  that unless Chase asks; today's session was scoped to the Manim source + preview page only.
- Calendar 2.0 frozen — standing constraint, unrelated here.
- Chase has only confirmed **round 1**. Round 2 (bar shrink, 20% slower pace, trimmed whole
  example, outside-right multiplier placement) is rendered and linked but **awaiting his review**.

---

## 7. Exact next step (fresh task)

Chase opens `http://127.0.0.1:8765/scratch/fraction-add-fractions.html` and reports what he
wants adjusted next. **Fix only what he reports** — do not re-open any decision listed in
§3/§4 above without him raising it again.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `Manim Trial/fraction_add_fractions.py` — the scene itself
3. `Manim Trial/scene_style.py` — shared `Narrated` mixin; note the per-scene `pace` override
4. `Manim Trial/README.md` § Agent rendering — render command, MiKTeX PATH, never preview
5. `Manim Trial/build_page.py` — how the scratch HTML page is rebuilt after a render
