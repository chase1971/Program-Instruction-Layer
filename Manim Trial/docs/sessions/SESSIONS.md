## 2026-09-22 — Rocket and lighthouse related-rates clips (worksheet #8/#9)

**Files changed:** `related_rates_lighthouse.py` (new, ~155 lines), `related_rates_rocket.py`
(new, ~140 lines), `build_page.py` (+2 `PAGES` rows)

**What worked:** Built the two "angle" problems from `3.11 Related Rates` — lighthouse (#9) and
rocket (#8) — matching the established square/ladder/drain/cone style: same navy/gold/blue/muted
palette, same flash/pulse-on-whole-unit mechanism, same threshold-triggered "the question" marker,
same render → `build_page.py` → verify-200 → link pipeline. Lighthouse went through one revision:
initially the light started at P and swept only rightward; Chase asked for the lighthouse centered
in frame with the beam sweeping the full range so negative values (left of P) are visible too —
redone with a symmetric sweep and signed (`+`/`-`) distance/angle readouts. Rocket is a genuinely
new pattern: its question is framed by **elapsed time** ("after 12 mins"), not a spatial value, so
the marker fires on a time threshold instead of a position tick, and it introduces a live `Angle`
mobject arc at the observer's vertex to visualize the elevation angle directly (first use of
`Angle` in this folder — cone's live relationship visual was an `Arrow`, not an arc). Rocket is
also the first "decelerating" clip since cone (dtheta/dt shrinks as the rocket climbs), while
lighthouse joined square/ladder in the "accelerating" family.

**Current state:** Green — both scenes render at 1080p30, are wired into `PAGES`, and their pages
return 200 at `http://127.0.0.1:8765/scratch/related-rates-lighthouse.html` and
`.../related-rates-rocket.html`.

**File size flag:** None — both scene files are ~140-155 lines, consistent with the other
self-contained `related_rates_*.py` files.

**Next session:** All worksheet problems with a natural related-rates animation are now covered
(square #1, drain #5, cone #6, ladder #7, rocket #8, lighthouse #9). Problems #2-4 (circle,
sphere-melting, sphere-surface-area) and #10-11 (business/demand) remain unbuilt if Chase asks for
more; nothing pending was requested this session.
