# Momentum handoff: AI presentation site, opening slides and customization polish

**Written:** 2026-11-07 (third handoff today; replaces the "GJ section built with real data" one).
Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify. Docs server on `http://127.0.0.1:8765/`.
Deck: `http://127.0.0.1:8765/scratch/presentation-skeletons/v2-stage.html` (VP track `#t=vp&s=0`).

## Objective and current phase

Chase is preparing a ~20 minute pitch to Lone Star College's **Vice President of Instruction**
(plus a public LinkedIn version) as a Wikipedia-like HTML site with presentation tracks, in the
**Stage** layout. The Gauss-Jordan (GJ) evidence section has real data. This chat polished the
opening and the customization slides from Chase's slide-by-slide feedback.

**Phase:** Chase is walking the VP track slide by slide and giving fixes. Last touched: slide 3
(`gj-why`). Remaining real content still to come: guided-practice **homework** (Precalculus, data
after Wednesday), the static vs dynamic recordings, the **Skills Hub** pitch, peer colleges, legal
tiers, the ask.

## Chase's desired feel (his words where they matter)

- Each point **slides in** on its own press and **stays**. Data uses `board` pages so everything
  stays on screen.
- **No boxed text.** A box "looks like a footnote"; he wants it "part of the conversation". Callouts
  in Stage are now plain white statement text.
- **No on-screen text aimed at him** (how-to-use lines, draft labels, "Start here", taglines he
  did not ask for). "I'll have my own notes." Speaker notes stay hidden (notes toggle only).
- **Title case** for all headings, Chicago style (a, an, the, and, or, from, with, before stay
  lowercase). He finds sentence case titles odd.
- **Comparisons are contrasting pairs:** one publisher point, then the app point that answers it,
  side by side on the same row, building back and forth. Not a table with row labels, not one
  whole column then the other.
- Column titles: light blue, larger than points, no box ("not like a button"). Same color both
  sides (neutral, never red).
- Pictures should be visible while he talks: picture shows when the slide opens, points come down
  beside it. Pictures scale with the A−/A+ text size control.
- **Honesty matters.** He accepted my critique: MyLab "Help Me Solve This" does walk steps, you
  *can* build your own problems (just hard, needs the builder's syntax), ALEKS is McGraw Hill and
  adaptive. Use "hard / slow / takes effort", never "cannot / impossible" unless he confirms it.
  No vendor names on the customization slide (just "Publisher Platforms").
- Supplement, not replacement. Experiment framing: "How well can an app teach a concept by itself?"
  Don't say "flipped"; not a missed-class tool.
- No student names anywhere.

## Accepted decisions (VP track order now)

0. `welcome` "Building Learning Tools with AI": title + one line ("more than 10 tools ... tutorials,
   guided homework, and animations"). No kicker, no tagline, no stats, no how-to line. Chase does
   not want an exact tool count.
1. `math-portal` "Math Portal" (board 2), summary "The app my classes use." Teacher console
   screenshot on the **right**, visible at build 0; 4 points on the left, builds 1 to 4 (one place
   for everything; own link, saved under a code not a name; add/remove tools, AI exit tickets and
   surveys in minutes; everything comes back to the teacher console). Phone screenshot dropped (the
   portal is inside the console shot). Student Portal is being renamed Math Portal. Chase may give
   the audience a link to try it.
2. `gj-why` "Learning from an App", summary "How well can an app teach a concept by itself?"
   Points: guided step-by-step tutorial, students take part in every step (tap/click, not watch);
   built phone first, works anywhere, laptops too; goal: teaches, keeps students active, supports
   self-directed learning; "So the experiment asked: can an app work as a teaching tool on its own,
   for a topic students have never seen?"; not designed to replace instruction, designed to
   supplement it. (Removed: the "most software checks answers / videos" comparison, and "without
   an instructor in the room".)
3. to 8. GJ section unchanged in substance: `gj-setup`, `gj-tutorial`, `gj-results`,
   `gj-before-class`, `gj-ready`, then:
9. `gj-adapt` "Customizable and Flexible Apps" (board 2): three feedback to "What I changed" pairs
   + plain-text AI line. Item 2 is a **PLACEHOLDER quote** ("The animations went too fast for me
   to follow.", marked `// PLACEHOLDER`) leading to "Pause, play, and replay controls built into
   every animation."
10. `gj-custom` "Publisher Platforms or Apps I Build" (board 1, both tracks): `compare` with
   `pairs: true`, 6 pairs: mostly fixed / dynamic, tell AI; building own is slow, builder syntax /
   describe problems with rules like no fractional answers; random slot, may repeat / I choose the
   mix (two with one solution, one with infinitely many); book's examples / built around how I
   teach, links to my videos; change requests take years / ready by next class; students no
   feedback channel / feedback from inside the app. Speaker note holds his ALEKS calculus story
   (asked for a change, "add it later", his class never got it). Customization only.
11. `gj-data`, 12. `gj-homework` (placeholder), 13. `side-by-side` (publisher point now "One answer
   box for the whole problem, so it cannot tell which step went wrong"), then later placeholders.

Public track: welcome, math-portal, gj-why, gj-tutorial, gj-results, gj-adapt, gj-custom,
side-by-side, homework-apps.

**Saved for the homework section:** Chase built the GJ homework by telling AI the mix (first three:
two with exactly one solution, the second infinitely many; then three more, one of each type), then
"build 20 problems and pick randomly", with rules like no fractional answers. Good example of how
easy building is compared to publisher builders.

## Rejected directions (do not rediscover)

- Any presenter-facing text on slides; "Start here" kicker; welcome tagline; placeholder stats.
- Boxed callouts (footnote look). Row-label tables ("Who it fits / Fixing a problem").
- Showing all publisher points then all app points; unpaired, unmatched bullets.
- Button-looking column headers; red/colored publisher headers; vendor names in the comparison.
- Absolute claims about publishers ("cannot", "only publisher problems", "no step help").
- Two portal screenshots; "How students get the tools" as the title; "I built it this semester"
  on the slide (it is in the speaker note).
- Earlier: missed-class framing, "flipped", swapping media stacks, label-shifted bars, dashboard
  screenshots with names, invented claims, rejected titles from earlier handoffs.

## Current implementation state

Folder `agent docs/scratch/presentation-skeletons/` (all uncommitted):
- `shared/content.js`: pages, tracks, glossary. New pages `math-portal`, `gj-custom`.
- `shared/engine.js`: new `image` block (`src`, `alt`, `size` in em, `tall`); `compare` gained
  `pairs: true` (grid rows, builds alternate left/right).
- `shared/base.css`: `.shot` image styles (em sized, so A−/A+ scale them); `.cmp-pairs` grid.
- `v2-stage.html`: callouts restyled to plain text; `.cmp-pairs .cmp-head` light blue 1.5em;
  start page "Skeleton draft" line removed.
- `media/math-portal-teacher-console.webp` (from Chase's screenshot; shows class sections, no
  student names).

**Verification:** `node --check` on edited JS; headless Edge screenshots (no window) at 1366x768
and 1920x1080 for every changed slide: all fit at 100%. At 140% text size the Math Portal slide
overflows the bottom on 1366x768 (expected; same as text). Method: copy `v2-stage.html` to temp
`zz-shot.html` with injected `transition/animation:none` and a `requestAnimationFrame` override,
screenshot `#t=vp&s=N&b=99`, delete the copy. Real-browser look is Chase's to judge.

## Open questions and constraints

- **Real pause/replay quote:** Chase has it on paper. Swap it into `gj-adapt` item 2. If never
  found, cut the quote and keep the fix (do not present invented words as a student's).
- **Check fix causality** on `gj-adapt`: did each fix come after its comment? (I raised it; he has
  not answered.)
- **Bias points I raised that he agreed with but are not on slides yet:** publisher strengths
  (big banks, accessibility, support, LMS integration) as a lead-in to the ask; how he checks
  AI-made problems; instructor-as-evaluator bias. Proposals only.
- `gj-why` point 4 repeats the tagline's question; I offered to trim it, no answer yet.
- Homework section after Wednesday's Precalc data; Skills Hub pitch text from Chase.
- Byline: slides carry no author name (start page shows "Chase" from meta.author). Ask before
  changing.
- Logo on the public version needs LSC Marketing OK. Ask ladder and legal constraints unchanged:
  legal/IT review → fellowship with course release → pilot → permanent role; do not claim Copilot
  cannot code.
- Rules: no em dashes; never put anything on his screen without asking (headless screenshots only);
  no Netlify deploy unless he says so in that message.

## Exact next step

Continue Chase's slide-by-slide pass: ask nothing up front; wait for his feedback on the next slide
(slide 4, `gj-setup` "The App Was Their Introduction"), apply it, verify with a headless
screenshot, and give him the `#t=vp&s=N` link.

## Read first

1. This file.
2. `agent docs/scratch/presentation-skeletons/shared/content.js`, then `v2-stage.html`.
3. `agent docs/rules/html-delivery.md` (links are `http://127.0.0.1:8765/...`).
