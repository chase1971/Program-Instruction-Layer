# Momentum handoff: AI presentation second half (research, AI tutoring, colleges, Skills Hub); Matrix app layout fixes

**Written:** 2026-11-08 (replaces the 2026-11-07 "VP track through slide 11" handoff).
Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify. Docs server on `http://127.0.0.1:8765/` (restarted today).

**The deck moved.** It is no longer under `agent docs/scratch/presentation-skeletons/` (older
handoffs and `SESSIONS.md` entries still say that path). It lives in its own git repo:
**`AI presentations/`** (see its `README.md`).
- Open it: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=0`
- I added a mount to `scripts/serve-programs-docs.js`: `/ai-presentations/<file>` serves
  `AI presentations/site/<file>`. Without it the deck 404s (that folder is not a served root).
- Content `site/shared/content.js`, engine `site/shared/engine.js`, styles `site/shared/base.css`.
- The Claude artifact copy (`artifact/build.js`, then republish) is **stale**. Chase asked for the
  HTML, not the artifact. Do not rebuild or republish unless he asks.

## Objective and current phase

Chase is preparing a talk of **no more than 20 minutes** for Lone Star College's Vice President
of Instruction (plus a public version). The first half (Gauss-Jordan tutorial evidence, 11 stops)
was about 10 minutes and is considered done. Today the **second half was built**: research,
AI tutoring, other colleges, Bowen, the Skills Hub, and the ask. He said plainly: "just put stuff
there and then I'll work out how I want it to be actually displayed later." Content and order are
drafts; he wants to look at them and react.

Chase is waiting until **Wednesday** for guided-practice homework results, so `gj-homework`
("Coming soon.") stays a placeholder.

### VP track now: 22 stops

welcome, math-portal, gj-why, gj-setup, gj-tutorial, gj-results, gj-before-class, gj-ready,
gj-adapt, gj-custom, gj-data, **gj-homework, tutoring-research, ai-tutor-next,
ai-tutors-colleges, peer-colleges, bowen, skills-hub, other-apps, animations, hub-first-build,
the-ask.** (Stops 12 to 22 are new or rebuilt today; `#t=vp&s=11` is the first of them.)

Cut from the track (pages still in the library, nothing deleted): `side-by-side`,
`five-years`, `copilot-vs-agent`, `legal-tiers`, `how-i-build`. The public track is unchanged.

## Chase's desired feel (his words where they carry meaning)

- Wants to **see** things, then decide: "I just want to see what it looks like." "I'm probably
  going to change it."
- **List it off.** For other colleges: "I want a literal list of different colleges, just list it
  off, different programs, majors, areas of discipline from those transcripts." The point is
  breadth: "seeing a whole bunch of these colleges and all these different disciplines should make
  it be like, oh wow, this is actually accelerating more than maybe they know."
- Subtitle lines under titles look like **tags**; he prefers **regular white text** (lead blocks).
- Bowen thread (his own argument, label it his): AI companions get better every year, so what is
  the teacher's role, "otherwise we will be replaced." He is unsure whether it belongs before the
  Hub or at the end.
- Wants the Hub to start with **animations** (cheaper than apps), shown as a live D2L-style page.
- Standing rules still apply: no em dashes, title case headings, no boxed footnote-style text,
  no on-screen text aimed at him, never put anything on his screen without asking.

## Accepted decisions (Chase confirmed)

- Tutorial **video** embedded with custom controls: Back 5s, Play/Pause, Next 5s, 1x/2x/4x/8x.
  File moved (not copied) to `site/media/gj-tutorial.mp4`; original removed from his Videos folder.
- Home-screen screenshot replaced with his new one; all four corners made transparent and edge
  strips cleaned (`site/media/gj-tutorial-home.webp` and `.png`). Original in the old session's
  scratchpad only.
- `gj-adapt`: "What I changed" label larger; closing line now "Because I build these apps with AI,
  making changes is quick and simple. I can adapt it to student feedback or make improvements
  based on the data."
- `gj-data`: subtitle removed; opens with the paragraph "I can review an individual student...";
  card title "Example Student".
- `gj-homework` stays; side-by-side, five years, Copilot, risk tiers cut.
- Other apps slide: no graphic, no placeholder numbers, no glossary link; Logic homework tagged
  **Finite Math** (his words), Transformations, Probability, Factoring.
- Animation tutorials slide (rational functions, linear inequalities, conics, calculus and
  vectors): "they take less time than apps, so they are where I would start for the Skills Hub."
- `peer-colleges` rewritten as a three-column list (community colleges and systems, by discipline,
  campus-wide) from `School Scrips/School documents/aacu-session-summaries.html`.
- New `bowen` slide: 72% (teens have **tried** an AI companion, Common Sense Media 2025),
  27% (**graduates** who strongly agreed professors cared, Gallup-Purdue 2014), $699 (Harvard
  Business School program with AI professor avatars).
- `skills-hub` uses his D2L mockup image (`site/media/skills-hub-mockup.webp`, small, 584px wide).
- `hub-first-build` embeds his live sandbox page: copied from
  `My Drive/M2412/Unit 3 (10.2 - 10.7)/Conics/animations/` into `site/demos/conics-animations/`.

## Proposals Chase has not confirmed

- **Order:** Bowen placed before the Skills Hub as the "why now"; `other-apps` and `animations`
  moved after the Hub as "what I have to start with." He said he would work out placement.
- **AI facilitator role as "where this leads," not an ask today.** I asked; he did not answer.
- `ai-tutor-next` points (policy, student data/FERPA, accuracy, support and cost) are **my
  placeholder questions**, not his stated list. Marked as draft in the speaker note.
- Adding Equations of Lines and Domain/Range apps to `other-apps` (they exist in the portal).

## Rejected directions and corrections (do not rediscover)

- **There is no New York Times study.** Chase said he "made up" the NYT. The study is
  **Harvard** (Kestin et al., Scientific Reports, June 2025, physics, 194 students). Scott
  D'Amico cited it without naming it; the second study he cited is Bastani et al., PNAS 2025
  (Turkey, ~1,000 high school math students). Matching D'Amico's unnamed studies to these papers
  is an inference noted in the summaries page.
- Chase misremembered the Bowen stats slightly: **tried**, not "created," a companion; the 27% is
  **graduates**, not students. Speaker note on `bowen` says so.
- **Do not state VanLehn 2011 numbers on a slide.** Abstract-level only: about 0.76 for computer
  tutors that respond at each step vs 0.79 for human tutors, but I could not confirm which
  category 0.76 belongs to. The speaker note says to check the paper.
- The Harvard trial is one course at one school with short-term tests; Harford's results are
  student perceptions with no sample size. Do not overclaim.
- Portal "white corners" were first misread as a live-app CSS bug. The white was in the
  **screenshot image**. Two CSS edits I made in `student-portal/src/styles/portal-base.css`
  (a navy strip on `.portal-content-panel:has(.portal-quiz)`, header/footer radius left as
  originally rounded) did not change what he saw ("no change at all") and are probably
  unnecessary. They are uncommitted; consider reverting after telling him.

## Current implementation state (all uncommitted)

**AI presentations** (own repo): `site/shared/content.js` (pages, track), `site/shared/engine.js`
(custom video controls, new `embed` and `roster` block types), `site/shared/base.css`,
`site/media/` (gj-tutorial.mp4 7 MB, home and Skills Hub images), `site/demos/conics-animations/`
(**66 MB**, nine mp4 files). Ask Chase before committing; the demo folder is large.

**Programs root:** `scripts/serve-programs-docs.js` (the `/ai-presentations/` mount).

**School Scrips/Matrix app** (Part 2 tutorial and Auto Solve layout, **not viewed in the app**):
- `guided-practice/GuidedPracticeHelpTrigger.tsx`: optional `labelMaxWidthPx`.
- `part-2-step-4-multiply-help.tsx`: step 4 multiply help label capped at 84px (about 55px
  narrower); step 5 add-help anchored left, under the "Write the sum out in Part C" box.
- `guided-practice/useViewportAnchorPosition.ts`: new `alignLeft` option.
- `matrix-auto-solver.tsx`: explanation box max width 400px (was 672px); row replacement gets
  `minContentHeightPx` 160 (**an estimate**; adjust one constant,
  `AUTO_SOLVE_ROW_REPLACEMENT_MIN_HEIGHT_PX`, if the Play/Pause bar sits too high or low).
- `row-multiply-then-add-animation.tsx`: new optional `minContentHeightPx` prop.

**student-portal:** `src/styles/portal-base.css` (see Rejected directions).

**Verification done:** the content file loads in node, all 22 track stops resolve to pages, no
em dashes, deck files return 200 from the server. **Not done:** no browser check of the new
slides (conics iframe is set to 4:3 and untested; roster columns and the image size untested),
no check of the Matrix app edits, no type-check of the Matrix edits.

## Open questions and constraints

- Which stops are too long? Time budget target about 20 minutes; roughly 10 were built before
  today. Chase has not yet seen the new slides.
- `the-ask` (Tools, Time, Pilot, Vision) was **not touched** and still refers to "one review of a
  defined tool set," while the Copilot and risk-tier slides were cut. It may need to change.
- More conference videos coming: the peer lists should grow; more rows go in `content.js`.
- D2L widget access and what is allowed in D2L are unresolved (Chase's own question for IT).
- Never open the browser, launch a GUI, or change display config without asking first.

## Exact next step

Chase reviews stops 12 to 22 at `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=11`
and says what to rework. Start from his reaction; do not rebuild the artifact. If he wants a
visual check first, ask permission once to open the deck in the browser pane, then check the
conics iframe shape, the roster columns, and the Skills Hub image.
