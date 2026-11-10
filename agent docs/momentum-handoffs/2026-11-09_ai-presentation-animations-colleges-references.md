# Momentum handoff: AI presentation, animations wall, college section, References

**Written:** 2026-11-09 (replaces the earlier 2026-11-09 "intro and Macro App" handoff; that content is
archived in `2026-11-09_ai-presentation-intro-macro-app.md`). Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify. Docs server `http://127.0.0.1:8765/` (it was found off once
today; restart with `node scripts/serve-programs-docs.js` from Programs root, no browser).
Deck: `http://127.0.0.1:8765/ai-presentations/v2-stage.html` (repo `AI presentations/`, read its `AGENTS.md`).
Give Chase the deck link as a clickable markdown link every time you change the deck.

## Objective and current phase

A 30-minute talk for the VP of Instruction (a wake-up call: Lone Star is behind; ask for a pilot, looser
restrictions, support, and end on the Skills Hub). Today: the **Animation Tutorials** wall, a rebuilt
**colleges section** (the "we are behind" part), a security reference, a **References** panel separate from
the Library, scaling fixes, and a consistent Macro App layout. The second half (Skills Hub, other apps, the
ask) is untouched today. `the-ask` still reflects the old Copilot and risk-tier framing; check with him
before rewriting.

### VP track now: 34 stops

title, how-i-got-here, macro-app, macro-calendar, macro-handout, macro-gradebook, macro-makeup, welcome
(the "Part 2" divider), math-portal, gj-why, gj-setup, gj-tutorial, gj-results, gj-before-class, gj-ready,
gj-adapt, gj-custom, gj-data, gj-homework, **animations (slide 20)**, **ai-tutor-next (Looking Forward,
21)**, **colleges-1 to colleges-9 (22 to 30)**, skills-hub, other-apps, hub-first-build, the-ask.
The Public Overview track is unchanged.

## Chase's desired feel

- Slides must **fit the theme** (yellow kicker line above the title, same type), never bare or temporary.
  He called out a slide built "as if you don't know what the slides look like."
- **Do not go ahead of him.** He said "you went way too far ahead in the slides." Do what was asked.
- Animation tutorials: just show what animation can do, small clips, auto-playing, no controls, 2x speed.
- Colleges: list breadth. "Here's a college, a field of study, how they use AI, explain the pilot."
  Two colleges per slide, all text on screen at once, one press moves to the next pair. More colleges may
  follow when he gets more transcripts. Purpose: convince them Lone Star is behind and these schools are
  trying things "that couldn't be done before. That's where you find innovation."
- Security argument (his, label it his): breaches happen everywhere, including Lone Star (and with or
  without AI), so security is a reason to get involved with AI and test on purpose, not a reason to stay
  away. He is **not** claiming to do that security work. Available as a tangent, not a slide.
- Alabama State is a highlight (low-income school, no-code staff built advising tools, security cautious).
- The References panel is for tangents that support arguments but are not in the presentation.

## Accepted decisions

- **Animation Tutorials** (`animations`, kicker "Also Built", title "Animation Tutorials"): a video "wall"
  of 10 clips from the portal and Manim files, two rows, auto-play, loop, muted, **2x**. Row 1 (portrait):
  rational function ex 1, conics parabola opens up, equations of lines problem 1, FTC part 1, composite
  ex 1, quadratic domain/range. Row 2 (wide): linear inequality ex 1, work wagon, related rates, parametric
  form. The **related rates tile is a playlist** of six clips (ladder, cone, drain, lighthouse, rocket,
  square) that play back to back. Block type `wall` (`clips:` of `[src or [srcs], aspectRatio]`, `rate`, `h`).
  The first screen recording was dropped; the portal files are used.
- **Looking Forward** (`ai-tutor-next`): no pills, no numbers; three stepped bullets: homework that checks
  the answer; guided practice; "Bringing AI into learning" (he used AI to build tools but nothing the
  students interact with is AI; next is how to incorporate AI into learning). AI tutor talk is saved for
  later, not here.
- **Cut from the track, kept in References:** tutoring-research, tutoring-homework, tutoring-ai,
  tutoring-caution (2011 VanLehn is old; the research is for a proposal), the five background pages, the old
  ai-tutors-colleges, ai-tutor-questions, peer-colleges, bowen, next-steps-thoughts.
- **College slides:** `site/shared/colleges.js` (block type `colleges`, 18 cards in nine pairs). Order:
  Harford + Ferris State; Texas university + Maryville; SUNY + Kean/Middlesex; UW Stevens Point (media) +
  (graphic design); FGCU + the sustainability game course; Santa Monica + LaGuardia; UTSA + Alabama State;
  Agnes Scott + Clark Atlanta; Northern Arizona (policy study) + Georgetown. Title "Colleges Trying New
  Things With AI". The last slide has a link line to the security page.
- **Georgetown card** says "An enterprise Gemini license, built into email and documents, and a staff
  position for AI and digital learning." Whether students have licenses is unknown (speaker note only).
- **Library vs References:** Library = presentation pages only (40, sections story, evidence, field, path,
  reference/glossary). **References** is a new button (home screen and bottom bar) opening four groups:
  Research on Tutoring and AI Tutors (9), Security (1), AACU Session Summaries (22, generated), Earlier
  Slides and Thoughts (5). Sections with `ref: true` in `content.js` are excluded from Library.
- **Security reference:** `site/shared/security.js`, page `security-incidents` (about 40 sourced rows,
  tracking params stripped). Speaker note holds his argument.
- **Session summaries:** `site/shared/sessions.js`, generated from
  `School Scrips/School documents/aacu-session-summaries.html` by a script (not saved in the repo; it lived
  in the scratchpad; regenerate from the HTML if the summaries change). "For the pitch" lines dropped.
- **Scaling:** the A-/A+ zoom (`--zoom`) now scales videos, the wall, hero images, and all screenshots
  (width no longer capped at the column). At large zoom the slide scrolls.
- **Macro App slides:** all five use image on the right (`side: true, nochip: true`), text on the left, same
  width and place; makeup video `big: true`. Macro App and Gradebook slides have no left-column text yet.

## Rejected directions and corrections

- A bare, full-screen, toolbar-less video slide (it broke out of the presentation); a separate "Math
  Animations" divider. Screen recording instead of the original Manim/portal files.
- Research slides on this talk. The agent-voiced "For the pitch" and "Files" commentary on session pages.
- Putting caveats or agent commentary on slides (see the deck AGENTS.md). Em dashes.
- Bug to remember: a block property named `rows` collides with the engine's grid-row style; use another name.

## Current implementation state (all uncommitted, AI presentations repo)

Modified: `site/shared/content.js`, `engine.js`, `notes.js`, `site/v2-stage.html`, `notes.html`, `v1`-`v5`
html (script tags). New: `site/shared/colleges.js`, `security.js`, `sessions.js`; `site/media/anim-*.mp4`
(9), `rr-1..6-*.mp4`, plus the earlier Macro App media. Syntax checks pass; all 34 stops resolve. Verified
with headless Chrome screenshots only (no window): wall, colleges 1/7/9, security page, a session page, the
Macro App slides, zoom at 1.4x. **Not verified:** the References panel click, the related rates playlist
advancing, the A-/A+ buttons themselves, the makeup video width after `big: true`, colleges 2 to 6 and 8,
Looking Forward. The Claude artifact (`artifact/vp-presentation.html`) is **stale** and its build does not
include the new files; do not rebuild unless asked.

## Open questions and constraints

- **University of South Dakota Sanford School of Medicine** (Paula Hawks, self-directed learning and AI):
  Chase will get the transcript; then add a college card and session page. Only the abstract exists now.
- Whether to move the Northern Arizona policy card to the first college slide (strongest "associate's
  colleges are behind" point); it is on slide 30 now.
- The **D2L row on the security page quotes Lone Star's own help page** (confirmed verbatim). He chose to
  keep it unless told otherwise; mention if he asks about audience reaction.
- Two security rows lack links (St. Thomas Houston, GAO). The list is his pasted research, mostly unchecked.
- ChatGPT logo on How I Got Here: never resolved. A "Part 1" divider: not built. `gj-adapt` still has a
  placeholder student quote. Only Chase's words go on slides.
- He has about 30 more conference videos; he may send transcripts to extract which sessions have AI use in
  the classroom, then expand the colleges section.
- Never open a browser or launch a GUI without asking (headless Chrome screenshots are fine). Never commit
  or push mid-session. FERPA: keep the blurs on the makeup exam video. Windows PowerShell rules apply.

## Exact next step

Ask Chase what he wants next in the deck. Likely candidates: view slides 20 to 30 and react; text for the
empty left column of the Macro App and Gradebook slides; moving the Northern Arizona card; adding the
University of South Dakota card when the transcript arrives. Then give him the deck link.
