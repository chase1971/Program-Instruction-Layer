# Momentum handoff — Manim fraction × whole number animation

**Written:** 2026-09-16 (Wednesday, ~8:39 PM)

---

## 1. Objective and current phase

**Active thread:** Build a short Manim teaching clip in **Manim Trial** for multiplying a
fraction by a whole number — cancel-first, Gauss-Jordan context (same fraction applied to
separate row entries), then a second example with `2/7`.

**Phase:** First render with revised visuals is **done in code**; **Chase has not verified**
the latest version on the scratch page. Treat polish as open until he watches it.

**Separate paused work** (uncommitted, earlier today): guided practice home screen + TC preview
in Matrix app / student-portal / Macro App — see dated archive
`2026-09-16_guided-practice-paused-new-project.md` if that thread resumes. Do not conflate
repos or dirty files.

---

## 2. Chase's desired feel

### Pedagogy
- Teach: **put the whole number over 1**, then multiply (cancel first when possible, then tops)
- **Never chain more than two factors** — not `1/3 × 4 × 15 × 22`. Each problem is its own
  pair: `1/3 × 15`, then `1/3 × 4`, then `1/3 × 22` separately
- Gauss-Jordan framing: same fraction multiplied into **each entry one pair at a time** — not
  one giant product
- Example 2: `2/7 × 14`, `2/7 × (-21)` (negative on purpose), then `2/7 × 3/8` → `3/28`
- On-screen captions explain each step; top-caption style via `scene_style.Narrated`

### Visual quality (Chase rejected the first renders)
- Both factors must sit on the **same plane**: numerators aligned, **one shared horizontal bar
  row**, denominators aligned — **equal font size** throughout
- Whole number starts at numerator height; **bar + 1 animate in** underneath (not awkward
  side-by-side mismatched fractions)
- **Canceling is NOT a diagonal line between distant terms.** Correct pattern:
  1. **Slash through** the number being canceled
  2. Reduced value appears **below** it
  3. Slash disappears; reduced value **pulls up smoothly** into place (`smooth` easing)
- Opening caption: *"To multiply a fraction and a whole number, put the whole number over 1."*
- Match existing Manim Trial quality — read `gcf_division.py`, `two_step_equation.py`,
  `ANIMATION_STYLE_RECIPE.md`, `scene_style.py`

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| Scene file `Manim Trial/fraction_times_whole.py`, class `FractionTimesWhole` | Matches plan + README pattern |
| `Narrated` mixin + navy/gold/blue palette | Recipe + newer dice scenes |
| `aligned_grid()` for two-column fraction layout | Equal size, shared bar row |
| `pull_cancel()` slash → ghost below → pull up | Chase's explicit cancel visual |
| Work order example 1: 15 (cancel demo), then 4, then 22 | Clearest cancel first |
| `build_page.py` row → `fraction-times-whole.html` on 8765 | Standard delivery |
| Headless render only — no Manim preview | AGENTS.md GUI rule |

---

## 4. Rejected directions — do not redo

- **Row of chained × signs** (`1/3 × 4 × 15 × 22`) — Chase: multiply each pair separately
- **Side-by-side `manual_frac` groups** with mismatched num/den font sizes — looked awkward
- **Diagonal cancel lines between terms** that don't intersect the numbers — "doesn't even make
  sense"
- **Transform-in-place** without slash + below + pull-up — not how Chase envisions canceling
- **Bottom captions** — new scenes use top captions per recipe

---

## 5. Current implementation state (uncommitted)

### Manim Trial — this thread
| File | State |
|---|---|
| `fraction_times_whole.py` | New — ~163 lines; `aligned_grid`, `pull_cancel`, `show_product`, `show_frac_product` |
| `fraction_times_whole_marks.json` | Pause marks: `example_one_done`, `done` |
| `build_page.py` | PAGES row for `fraction-times-whole` |
| `README.md` | Animation examples bullet added |
| `media/videos/fraction_times_whole/1080p30/FractionTimesWhole.mp4` | Rendered (latest visual pass) |
| `agent docs/scratch/fraction-times-whole.html` | Built (~3.2 MB embedded MP4) |

### Delivery link
`http://127.0.0.1:8765/scratch/fraction-times-whole.html`

### Verification performed
- `py_compile` — pass
- Manim render `-qh --fps 30` — pass (after `DOWN` import fix)
- `build_page.py` — pass
- **Chase visual review of latest cancel/alignment pass — NOT DONE**

### Other uncommitted work (out of scope unless Chase says)
- Matrix app / student-portal guided practice files
- Macro App TC preview files
- See `git status` under those folders

---

## 6. Open questions and constraints

- **Do not commit/push** unless Chase asks
- **Do not launch Manim preview or open browser** without per-run permission
- **Calendar 2.0** frozen
- **Windows PowerShell** — no `&&`
- Chase may want **further polish** after watching — common feedback areas: slash angle/weight,
  timing, caption wording, whether to show intermediate `2/1 × 2/1` after cancel before final `4`
- If Chase says it still looks wrong, **watch the MP4 frame-by-frame** before guessing — don't
  reintroduce diagonal-between-terms lines

---

## 7. Exact next step (fresh task)

**Chase watches** `http://127.0.0.1:8765/scratch/fraction-times-whole.html` and reports what
still looks off. Fix only what he names — likely cancel timing, alignment nits, or caption text.

If he approves: optional end-of-session commit; no action required otherwise.

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `Manim Trial/ANIMATION_STYLE_RECIPE.md`
3. `Manim Trial/fraction_times_whole.py` + exemplars `gcf_division.py`, `scene_style.py`
4. `Manim Trial/README.md` § Agent rendering + `build_page.py` for re-delivery
