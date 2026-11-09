# Momentum handoff: AI presentation VP track through slide 11; Math Portal rename

**Written:** 2026-11-07 (fourth handoff today; replaces the "opening slides and customization polish" one).
Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify. Docs server on `http://127.0.0.1:8765/`.
Deck: `http://127.0.0.1:8765/scratch/presentation-skeletons/v2-stage.html` (VP track `#t=vp&s=0`).
VP track now **ends on slide 11** (`gj-data`).

## Objective and current phase

Chase is preparing a ~20 minute pitch to Lone Star College's **Vice President of Instruction**
(plus a public LinkedIn version) as a Wikipedia-like HTML site with presentation tracks, in the
**Stage** layout. This chat finished a full slide-by-slide pass of the Gauss-Jordan evidence
section through the data slide, plus a student-facing rename of Student Portal → **Math Portal**.

**Phase:** VP track is cut to **11 stops** (welcome → gj-data). Later pitch pages
(`gj-homework`, side-by-side, Skills Hub, ask, etc.) still exist in the page library but are
**not** on the VP or public tracks. Next real content when Chase is ready: guided-practice
**homework** (Precalculus data after Wednesday), then the rest of the pitch.

## Chase's desired feel (his words where they matter)

- Each point **slides in** on its own press and **stays**. Data uses `board` pages so everything
  stays on screen.
- **No boxed text** that looks like a footnote. Callouts in Stage are plain statement text.
- **No on-screen text aimed at him.** Speaker notes stay hidden.
- **Title case** for headings (Chicago: a, an, the, and, or, from, with, before lowercase). He
  writes **vs.** not "versus".
- **Comparisons are contrasting pairs** (`pairs: true`), back and forth. Neutral column titles
  (light blue, larger), never red, no vendor names on the customization slide.
- Pictures visible when the slide opens; points build beside them. Pictures scale with A−/A+.
- **Honesty:** keep percentages; drop raw "N of M" fractions that confuse (different surveys).
  No control class yet, so do not claim the app alone produced better results. Prefer "hard /
  slow", not absolute publisher claims.
- Supplement, not replacement. Experiment framing. No student names. No em dashes.
- Never put anything on his screen without asking (headless screenshots only).

## Accepted decisions (VP track, 11 stops)

0. `welcome` — title + one lead line. No kicker/tagline/stats.
1. `math-portal` "Math Portal" (board 2) — teacher console screenshot right; 4 points left.
2. `gj-why` "Learning from an App" — experiment / supplement framing.
3. `gj-setup` "Gauss-Jordan Elimination Method Tutorial" — tagline "Can students learn how to use
   the Gauss-Jordan method for solving systems?"; "I only introduced…"; after tutorial, new
   problem alone with no help; live **CHASE1** screenshot `media/gj-tutorial-home.webp` (phone
   landscape, no Teacher Console chrome; shows Tutorial complete state). Dropped
   `row-operation` glossary term (plain "row operations").
4. `gj-tutorial` — You lost me was **not** active in any of his implementations (added later);
   Autosolve walks a summary after finish without redoing.
5. `gj-results` — 117 students; donut 42+41+34=117 (71%); 81% never seen (no 93/115).
6. `gj-before-class` — summary/tagline: **"Teaching after the app."**
7. `gj-ready` — keep title "It Got Them Ready for the Lesson"; rings + **87%** + **82%** on one
   row (no under-rings note); quotes below; callout: no control class, would like to teach once
   without the app and compare. Survey Ns verified from Excel: 78 = follow-up (confidence /
   easier); 108 = earlier "would use more apps" question. Percentages stay; fractions off slides.
8. `gj-adapt` — lead before quotes: students gave change feedback and he could change things
   quickly; then feedback→fix pairs; AI callout. Item 2 pause/replay still **PLACEHOLDER** quote.
9. `gj-custom` "Publisher Platforms **vs.** Apps I Build" — algorithm/random-version publisher
   point; he chooses predictable problem types; built the way he teaches + videos/examples.
10. `gj-data` — chips + class bars; expanded callout on individual review, whole-class aggregate,
    using that to guide reteaching; written feedback as third view. **VP track ends here.**

Also in this chat (separate deliverable): student-portal student-facing name is **Math Portal**
via `src/config/portalBranding.ts` (header, tab title, welcome). Repo/package stay
`student-portal`. **Not deployed** until he asks for Netlify.

## Rejected directions (do not rediscover)

- Presenter-facing on-slide how-to; boxed callouts; unpaired publisher/app columns; red headers;
  vendor names on customization; absolute "cannot" publisher claims; "that was all the teaching
  I did" on setup (he says it verbally); "93 of 115" / "68 of 78" / "89 of 108" on slides;
  under-rings "this includes the lesson itself"; short "three views" callout; ending the pitch
  on a Coming soon homework slide (removed from track); TC-embed screenshots with white frame /
  fake notch pill as "what students see" (use live portal capture instead); practice-link
  capture with Practice mode banner for the deck.

## Current implementation state

**Presentation** (`agent docs/scratch/presentation-skeletons/`, uncommitted):
- `shared/content.js` — VP/public tracks end at `gj-data`; later pages still in library.
- `media/gj-tutorial-home.webp` (+ `.png`) — CHASE1 live capture at 812×360 @2x.
- `media/math-portal-teacher-console.webp` — earlier.
- Engine/CSS: image block, `cmp-pairs`, board layout, rings/donut/fixes unchanged in spirit.

**Student portal** (`School Scrips/student-portal/`, uncommitted unless already dirty elsewhere):
- `src/config/portalBranding.ts` → `PORTAL_DISPLAY_NAME = 'Math Portal'`
- Wired in `PortalHeader`, `portalHomeIntro`, `PortalHomeIntro`, `index.html`, `main.tsx`.

**Source data (numbers):** `C:\Users\chase\My Drive\M1324\GaussJordan_Combined_Raw_Data(3).xlsx`
and the experiment report docx.

## Open questions and constraints

- **Real pause/replay quote** for `gj-adapt` item 2 — still on paper; do not invent.
- Homework / side-by-side / Skills Hub / ask — library pages only until Chase extends the track.
- Byline, LSC logo Marketing OK, ask ladder / legal — unchanged from earlier handoffs.
- Rules: no em dashes; ask before GUI; no Netlify unless he says so in that message.
- Screenshot tip: `/?s=CHASE1#/matrix-tutorial` via headless Edge/Playwright; TC `previewNotch`
  is overlay-only, not real student chrome.

## Exact next step

Do not invent the next section. Wait for Chase: either continue the pitch after slide 11
(homework / Skills Hub / ask) with material he provides, or other work he names. Deck link
above if he is still reviewing.

## Read first

1. This file.
2. `agent docs/scratch/presentation-skeletons/shared/content.js`, then `v2-stage.html`.
3. If Math Portal branding: `School Scrips/student-portal/src/config/portalBranding.ts`.
4. `agent docs/rules/html-delivery.md` (links are `http://127.0.0.1:8765/...`).
