# Part 4 plan — a population that is nowhere near normal

Handoff doc. Everything a fresh agent needs to build part 4 of the two-dice series
without re-deriving anything. Written 2026-09-09, straight after part 3 shipped.

---

## The one-sentence goal

Parts 1–3 used the sum of two dice, which is already bell-shaped, so it was never a fair
test. Part 4 uses the **product of two dice** — a spiky, gap-riddled, badly skewed
population — and shows that the sampling distribution of its mean *still* goes bell-shaped
and the same two formulas *still* predict it. That is the Central Limit Theorem, earned
rather than asserted.

Part 3 ends on exactly this hook, so part 4 has to open by paying it off:

> Both predictions leaned on the population being bell-shaped.
> Next: a population nowhere near normal — whose sampling distribution turns normal anyway.

---

## What already exists

| File | What it is |
|---|---|
| `dice_sums.py` | Part 1 — every ordered roll behind each sum 2–12, ending on 36 |
| `dice_stats.py` | Part 2 — chart tips into a histogram, normal curve overlay, μ = 7 and σ = 2.42 |
| `dice_sampling.py` | Part 3 — samples of four rolls, 100 sample means, σ/√n, predict-then-check table |
| `scene_style.py` | Palette, caption line, `PACE`, pause marks. **Import from here, do not re-declare** |
| `dice.py` | `die(face, size)` and `pair(a, b, size, buff)` — white first die, blue second |
| `build_page.py` | Base64-inlines a rendered MP4 into a served HTML page. Add a row and run it |
| `ANIMATION_STYLE_RECIPE.md` | The visual language. Read this before writing any scene |

New scene should be **`dice_products.py`**, class **`DiceProducts`**.

---

## Hard numbers, already verified

Population = product of two fair dice. 18 distinct values out of 36 equally likely rolls.

| Product | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 | 10 | 12 | 15 | 16 | 18 | 20 | 24 | 25 | 30 | 36 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ways | 1 | 2 | 2 | 3 | 2 | 4 | 2 | 1 | 2 | 4 | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 1 |

Missing entirely (the gaps are the whole point visually):
**7, 11, 13, 14, 17, 19, 21, 22, 23, 26, 27, 28, 29, 31, 32, 33, 34, 35**

- **μ = 12.25** exactly. It is 3.5², because E[AB] = E[A]E[B] for independent dice.
- **σ = 8.9423.** From E[A²B²] = (91/6)² = 230.0278, minus μ² = 150.0625, giving
  variance 79.9653.
- **σ / √4 = 4.4712** — the prediction part 4 has to test.

### Use seed 429

`random.Random(429)`, 100 samples of n = 4 products, binned at width 2.0 on centers
2, 4, 6, … 26 gives:

```
counts: [0, 4, 7, 12, 20, 19, 13, 11, 6, 4, 2, 1, 1]
observed mean 12.383     observed sd 4.482     peak column 20 dots
```

Observed 4.482 against the predicted 4.4712 is about as close as 100 samples gets, and the
peak of 20 dots matches part 3's height so the two clips look like siblings. Chosen out of
600 candidates scored on center, spread, and unimodality — **do not swap the seed without
re-running that search**, or you risk handing Chase a lopsided draw in front of a class.

Note the mild right tail in those counts. That is real and worth keeping: n = 4 out of a
badly skewed population gets you *close* to normal, not perfectly there. Do not fake it
away. If anything, call it out.

---

## Layout

Reuse parts 2–3's baseline so all four clips cut together. The axis is the only thing that
changes, because the value range is 1–36 instead of 2–12.

```python
BASE_Y = -2.21          # import from dice_stats, same floor as parts 2 and 3
PROD_X0 = -5.9
PROD_PITCH = 11.8 / 35  # = 0.3371, so value 1 sits at -5.9 and 36 at +5.9

def px(value):
    return PROD_X0 + (value - 1) * PROD_PITCH
```

- **Population histogram**: stacked cells, max height 4, `CELL_H = .40` → 1.6 tall, topping
  out near y = −0.6. Label only 1, 6, 12, 18, 24, 30, 36 on the axis; all 36 ticks is noise.
- **Sampling dots**: bin width 2.0, `DOT_R = .075`, `DOT_PITCH = .17`. A 20-dot column is
  3.4 units, topping out near y = 1.2, which clears the caption.
- **Captions live at the top** (`CAPTION_Y = 3.3`). Content stays below about y = 2.5.
  This tripped part 3 up twice — see pitfalls.
- Copy part 3's `bell(sigma, height)` helper and swap the 7 for 12.25. For an equal-area
  comparison the population curve's height must be the sampling curve's height times
  4.4712 / 8.9423, i.e. half.

---

## The beats

1. **Pay off the hook.** Caption: the sum of two dice was bell-shaped from the start, so it
   never really tested anything. Now pick something ugly.

2. **Build the population.** Multiply the two dice instead of adding them. Show three or
   four pairs resolving to products — include (2,6) and (3,4) both landing on 12 so the
   collisions read, and include (6,6) → 36 for the far edge. Then fill the whole histogram
   on the 1–36 axis.

3. **Sit on how wrong it looks.** The gaps are the star: no 7, no 11, no 13. Caption should
   name it plainly — spiky, lopsided, holes all through it, nothing like a bell. Give this
   a real hold; it is the setup for the entire clip.

4. **State μ and σ.** μ = 12.25 and σ = 8.94. Formula and answer only — Chase does not want
   the standard deviation ground out by hand. Part 2's `standard_deviation()` is the
   pattern to copy.

5. **Question, on a pause mark.** Something like "This is nowhere near normal. So what
   shape will the sampling distribution be?" Let it clear the screen before answering —
   questions get the frame to themselves and must come and go, never sit there statically.

6. **Sample and rain.** Four products per sample, averaged. Show the first sample slowly
   with dice art, one or two faster, then the remaining 97 in `LaggedStart` batches, exactly
   as `dice_sampling.rain()` does. The bell appearing out of that comb is the payoff shot.

7. **Overlay both curves at equal area.** Wide flat population against the tight tall
   sampling distribution, same axis. Caption the honest bit: the tail leans slightly right,
   because four draws from something this skewed only gets you *close* to normal.

8. **Predict-then-check table.** Reuse `dice_sampling.results()` and `predict()` almost
   verbatim — this structure is what finally landed with Chase, so do not redesign it:
   - Two columns: "Our 100 samples" in gold, "Predicted in advance" in blue.
   - Rows labelled `μx̄` and `σx̄`; observed values to **three decimals** (12.383, 4.482) so
     they read as real data and not as invented round numbers.
   - Mean transfers: 12.383 ≈ 12.25. Fine.
   - **Then let the naive prediction fail.** Put σ = 8.94 in the predicted column, pause on
     "does the spread carry across?", then strike it through against 4.482.
   - Only then bring in σ/√n = 8.94/√4 = 4.47, and show 4.482 ≈ 4.47.

9. **Land the theorem.** The population was spiky, gappy and skewed. The sampling
   distribution still went bell-shaped and both formulas still worked. Name it: this is why
   the normal distribution turns up everywhere — you are almost never looking at raw
   values, you are looking at averages.

10. **Optional closer.** Jump n from 4 to 16 and let the bell pull in further and
    straighten out its tail. Only add this if the clip is still under ~90 seconds.

---

## Conventions you must not get wrong

- **Read `C:\Users\chase\Documents\Programs\AGENTS.md` first.** Especially: never put
  anything on Chase's screen without asking. Rendering headless is fine; opening a video
  player or a browser window is not.
- **PowerShell 5.x.** `&&` and `||` are invalid. Use `;` or separate calls. No `curl`.
- Render:
  ```powershell
  $env:PATH = (Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64') + ';' + $env:PATH
  & '.\.venv\Scripts\python.exe' -m manim -qh --fps 30 --disable_caching dice_products.py DiceProducts
  ```
  Pipe through `Select-String -Pattern "Rendered|Traceback|error:"`; raw Manim output is
  enormous and will burn the context window.
- **Deliver as a served page, never a file path.** Add a row to `build_page.py`, run it,
  confirm 200 from `http://127.0.0.1:8765/scratch/dice-products.html`, and give Chase only
  that URL. A `C:\` path or a `file:///` URL is useless to him.
- Call `self.mark('name')` on every hold you want the app to be able to pause at, and
  `self.write_marks('dice_products_marks.json')` at the end of `construct`.
- **American spellings on screen.** "center", never "centre".
- No ephemeral success feedback anywhere in the HTML page.

---

## Pitfalls that already cost render cycles

- **Captions moved to the top on 2026-09-09.** Anything placed above roughly y = 2.5 will
  collide with them. Grepping for literal coordinates is not enough — `dice_sums.chart_heads()`
  had `y = 3.12` buried inside a helper and it slipped through.
- **`Transform` between two different formulas looks like mush.** Use
  `FadeOut(old), FadeIn(new)` for formula-to-answer swaps. Part 2 had to be re-rendered
  over this.
- **Do not `add()` a mobject and then also put it in a `VGroup` you animate.** It ends up in
  the scene twice and stops moving with the group. `self.remove(x)` before `group.add(x)`.
- **Review with frame grabs, not by eye.** Decode the MP4 with `av`, tile ~20 frames into a
  contact sheet for layout and pacing, then take full-resolution crops of any dense region
  to judge whether dice pips and small labels are actually legible. Contact sheets alone
  will not tell you.
- **Check text width.** A single `label()` over about 70 characters runs off the 14.2-unit
  frame and gets clipped at both ends. Split it into a `VGroup` of two lines.
- `scene_style.label()` renders with `Text`, not LaTeX — so apostrophes are safe and you can
  type `μ` and `σ` directly in prose lines.

---

## Done when

- `dice_products.py` renders clean at `-qh --fps 30`.
- `dice_products_marks.json` written, with a mark on every question hold.
- Page live and returning 200 at `http://127.0.0.1:8765/scratch/dice-products.html`.
- A row added to `README.md` for the new scene.
- Frame-grab review done on the population histogram (are the gaps obvious?) and on the
  comparison table (do the columns collide?).
- Session scorecard bumped per `agent docs/SESSION_TRACKING.md`.
