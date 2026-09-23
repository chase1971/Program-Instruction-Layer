# Momentum handoff

**Written:** 2026-09-22 (Tuesday), ~9:01 PM CT
**Topic:** Manim related-rates animations for `M2413\Unit 3 Derivative Applications\Blank\3.11 Related Rates.docx`

---

## 1. Objective and current phase

Chase is building short Manim animations for the problems in his `3.11 Related Rates`
worksheet, one problem at a time, reviewing each before moving to the next. Four are done
and delivered. He named three problems up front (draining, triangle, lighthouse) plus the
original square problem that set the style; **the lighthouse problem is the one outstanding
item from his original list.**

## 2. Chase's desired feel (his language, his priorities)

- **Short.** "Five second video or something, maybe ten second video." Every clip so far lands
  ~9-11s including intro/outro fades.
- **Visual only, minimal text.** "I just want to create an animation that shows what it's doing
  and what we're trying to find." No derivation steps, no wall of captions — one title
  (phrased as a question, e.g. "HOW FAST DOES THE AREA GROW?"), one small setup note, then let
  the visual run.
- **The signature effect he loves:** a numeric readout that ticks up/down continuously and
  flashes a different color (gold) the instant it crosses a whole number, with a brief
  size-pulse, decaying back to the resting color. He described this from something he'd done
  before with a *count* that speeds up as a rate increases — "you can see that pulse just get
  faster and faster and faster." **This must be driven by the actual math of each problem, not
  faked** — see the cylinder problem below, where he'd likely still want the same mechanism
  even though it produces *even*, non-accelerating flashes, because that's what the calculus
  actually says.
- **Tie back to the exact number the problem asks about.** Ladder problem marks x = 5 ft; cone
  problem marks h = 4 cm. A small gold marker/tick fades in (or the sequence briefly pauses)
  right at that value.
- **One problem at a time.** Build, render, deliver a link, wait for his go-ahead before
  starting the next.

## 3. Accepted decisions (established pattern — reuse, don't reinvent)

- **Layout:** diagram/geometry on the left half of the frame; a numbers panel on the right at
  roughly x=3.1, with a plain (non-pulsing) tracked quantity stacked above the pulsing "answer"
  quantity. Title at y≈3.35, one setup note at y≈2.8 (Segoe UI, muted color), per
  `ANIMATION_STYLE_RECIPE.md`'s caption-at-top convention.
- **Palette:** navy `#101C30` background, ink `#F2F5FA` text, gold `#FFC66D` for flashes/markers,
  blue `#86C8FF` for the moving geometry, muted `#B2C0D4` for static labels — same constants
  duplicated at the top of every new scene file (existing convention; scenes are self-contained,
  don't share a style import for this).
- **Flash/pulse mechanism (copy this exactly into any new scene):**
  ```python
  last_floor = [int(start_value)]
  since_flash = [999.0]

  def pulse(m, dt):
      v = <compute current value from a ValueTracker or elapsed-time formula>
      m.set_value(v)
      floor_now = int(v)
      if floor_now != last_floor[0]:
          last_floor[0] = floor_now
          since_flash[0] = 0.0
      else:
          since_flash[0] += dt
      envelope = math.exp(-since_flash[0] / FLASH_DECAY)   # FLASH_DECAY ~0.14
      m.set_color(interpolate_color(INK_C, GOLD_C, envelope))
      m.font_size = BASE_FONT * (1 + FLASH_GROW * envelope)  # FLASH_GROW ~0.4

  decimal_number.add_updater(pulse)
  ```
  Critical gotcha: **set `m.font_size = target` (absolute), never `m.scale(factor)`** — manim's
  `DecimalNumber.set_value` preserves whatever size/color was set the previous frame, so a
  relative `.scale()` call compounds every frame and runs away. The `font_size` property setter
  computes its own ratio from `self.height/self.initial_height`, so assigning an absolute target
  every frame is safe and non-drifting.
- **Color interpolation gotcha:** `interpolate_color` needs `ManimColor` objects, not raw hex
  strings — wrap once at module load: `INK_C, GOLD_C = ManimColor(INK), ManimColor(GOLD)`.
  Passing plain strings raises `AttributeError: 'str' object has no attribute 'interpolate'`.
- **Real-time vs. sped-up:** use the problem's real rate directly with no disclaimer when it's
  human-watchable (ladder's 2 ft/sec). When the real rate is imperceptibly slow (square's
  3 in/min; cylinder's ~0.02 cm/sec), pick a faster illustrative rate/range and say so in the
  on-screen note ("sped up here so you can watch it") — but always **keep the actual proportions
  and relationships honest** (e.g. cone kept true 30:10 height:radius ratio; cylinder kept a
  genuinely constant cross-section).
- **"What the question asks" marker:** either a brief pause with a fade-in tick+label (ladder's
  x=5ft), or a continuous animation with a one-shot triggered reveal via a small closure flag +
  per-frame updater that fires once a threshold is crossed and then no-ops (cone's h=4cm) — the
  second approach is smoother, prefer it for future problems.
- **Delivery pipeline (same every time):**
  1. Write `related_rates_<name>.py` in `Manim Trial/` (self-contained scene file).
  2. Render: prepend MiKTeX to PATH, then
     `.\.venv\Scripts\python.exe -m manim -qh --fps 30 --disable_caching related_rates_<name>.py <ClassName>`
     from inside `Manim Trial/`.
  3. Optional sanity check: grab a frame or two with
     `C:\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe -y -ss <sec> -i <mp4> -frames:v 1 -update 1 preview.jpg`
     (ffmpeg is **not** on PATH in a fresh shell — found via `where.exe ffmpeg`, not
     `Get-Command`), read it with the Read tool, then delete the temp jpg.
  4. Add a row to `PAGES` in `build_page.py` (folder, class, slug, heading, tab title, marks
     file or `None`, blurb), then run `.\.venv\Scripts\python.exe build_page.py`.
  5. Verify `Invoke-WebRequest http://127.0.0.1:8765/scratch/<slug>.html` returns 200.
  6. Hand Chase only the `http://127.0.0.1:8765/...` link — never a `C:\` path — per the
     html-delivery rule.

## 4. Rejected directions / things not to redo

- Don't force an accelerating-pulse effect onto a problem where the math says the rate is
  constant (cylinder) — that would misrepresent the calculus. Even spacing is the correct,
  intentional result there and was called out explicitly to Chase.
- Don't pause the whole animation with two `self.play` legs to mark a specific value unless the
  pause itself adds something — the cone problem's continuous per-frame trigger (fade in once
  threshold crossed, no pause) is the better pattern going forward.
- Don't try to literally simulate real time when the real rate spans multiple orders of
  magnitude within the visible range (this will matter for the lighthouse problem — see below).

## 5. Current implementation state

All four scenes live in `C:\Users\chase\Documents\Programs\Manim Trial\`, are rendered at
1080p30, wired into `build_page.py`, and verified live at `http://127.0.0.1:8765/scratch/...`:

| File | Class | Worksheet problem | Page slug | Behavior shown |
|---|---|---|---|---|
| `related_rates_square.py` | `SquareAreaRate` | #1, square (side grows 3 in/min, find dA/dt) | `related-rates-square` | Accelerating flashes (area = side²) |
| `related_rates_ladder.py` | `LadderSlideRate` | #7, 13ft ladder sliding | `related-rates-ladder` | Accelerating flashes; marks x=5ft; plays in real time (2 ft/sec) |
| `related_rates_drain.py` | `TankDrainRate` | #5, cylindrical tank draining (constant radius) | `related-rates-drain` | **Even/constant** flashes — built first by mistake when Chase actually meant #6, but is a legitimate, separate worksheet problem and was not asked to be removed |
| `related_rates_cone.py` | `ConeLevelRate` | #6, conical tank filling (proportional dimensions) | `related-rates-cone` | **Decelerating** flashes; live radius arrow showing r=h/3; marks h=4cm |

`build_page.py`'s `PAGES` list currently has these four entries plus the pre-existing
fraction/dice entries (untouched). The file is open and focused in Chase's IDE right now
(cursor was on line 20, inside the `PAGES` list) — that's just from reviewing the last edit,
nothing is mid-edit there.

No git commit/push has been made this session (per the "don't commit mid-session" rule) — only
do that if Chase says "put on GitHub" or asks for end-of-session.

## 6. Open questions and constraints

- **Not yet confirmed:** whether Chase still wants the lighthouse problem next, or has a
  different priority now — but it's the one item from his original three-item list
  (draining, triangle, lighthouse) not yet built, so treat it as the standing ask unless he
  says otherwise.
- Standard accessibility rules apply throughout: never open a player/window, never hand Chase
  a `C:\` path — links only, via the localhost:8765 scratch pages.
- Each scene file is small (~100-140 lines) and self-contained; no file-size or orchestrator
  concerns.

## 7. Exact next step (proposal, not yet worked out with Chase)

Build the **lighthouse problem** (worksheet problem #9): *"A lighthouse is located on a small
island 3 km away from the nearest point P on a straight shoreline. The light makes four
revolutions per minute. How fast is the point of light moving away from P along the shoreline
when the light is 1 km from P?"*

Setup (derived here, not yet reviewed with Chase — verify before treating as final):
- Let θ = angle between the beam and the perpendicular from the lighthouse to shore P.
- `x = 3 tan(θ)` km (distance of the light's point along the shore from P).
- `dθ/dt = 4 rev/min × 2π = 8π rad/min` — **constant** angular speed (the beam sweeps at a
  steady rate; this is the "constant rate" driver here, analogous to `ds/dt` in the square
  problem or `dV/dt` in the drain problems).
- `dx/dt = 3 sec²(θ) · dθ/dt`, which **grows without bound** as θ→90° (the beam nears parallel
  to shore) — same accelerating-flash family as the square/ladder clips, driven by `sec²θ`
  instead of a linear/quadratic term.
- At x = 1 km: `tan θ = 1/3`, `sec²θ = 1 + 1/9 = 10/9`, giving `dx/dt = 3·(10/9)·8π = 80π/3 ≈
  83.8 km/min` — the textbook's answer, worth marking with a threshold-triggered "x = 1 km"
  reveal like the cone problem's h=4cm marker.
- **Not yet solved:** the real angular rate (8π rad/min ≈ 25 rad/min) is way too fast to render
  at 1:1 while `x` still barely moves near θ=0 (light near P, sweeping across a huge range of x
  slowly in real terms, then blowing up) — this needs its own time-scaling pass (likely: drive
  the animation directly off θ increasing linearly in animation-time, similar to how the cone
  problem drove things off volume/time rather than depth, then derive x(θ) and dx/dt(θ) each
  frame for the pulse). Work out a start/end θ range (or x range) that gives a watchable ~8-10s
  clip with a clearly visible acceleration, the same way h0=3/h1=10 was chosen for the cone.
- Visual: lighthouse on an island, a rotating beam line sweeping toward a horizontal shoreline,
  the beam's shore-intersection point sliding away from P; numbers panel with "ANGLE (deg)" or
  similar plain readout plus "DISTANCE FROM P (km)" as the pulsing quantity; mark x=1km.

Then follow the same render → build_page.py → verify 200 → link pipeline as the other four.
