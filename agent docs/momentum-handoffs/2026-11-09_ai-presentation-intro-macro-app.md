# Momentum handoff: AI presentation opening (title, background, Macro App, Part 2 divider) and slide polish

**Written:** 2026-11-09 (replaces the 2026-11-08 "second half" handoff; that content is archived in
`2026-11-08_ai-presentation-second-half.md`). Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify. Docs server `http://127.0.0.1:8765/`.
Deck: `http://127.0.0.1:8765/ai-presentations/v2-stage.html` (repo `AI presentations/`, see its `AGENTS.md`).
Give Chase that link as a clickable markdown link **every time you change the deck** (he asked).

## Objective and current phase

The talk is now **30 minutes** (his dean wanted 30 and is supportive, will critique the deck first,
wants it to be a **wake-up call**). Audience: VP of Instruction first, possibly the president or other
higher-ups. Goals: (1) credibility from what he has built, (2) show what other institutions are
piloting so Lone Star is not left behind, (3) ask for a more aggressive stance, looser restrictions,
financial support (Claude Code enterprise or reimbursement for his AI subscription), a pilot with data,
and end with the **Skills Hub** pitch. He is not on the campus AI Task Force; at the one meeting he
attended, campuses said legal departments blocked projects. Today the **opening (first half) was built
and polished**. The second half (research, colleges, Skills Hub, ask) exists from earlier handoffs; with
30 minutes he wants it to get **more room**, and he has not reworked it today.

### VP track now: 33 stops

title, how-i-got-here, macro-app, macro-calendar, macro-handout, macro-gradebook, macro-makeup,
**welcome (now the "Part 2" divider)**, math-portal, gj-why, gj-setup, gj-tutorial, gj-results,
gj-before-class, gj-ready, gj-adapt, gj-custom, gj-data, gj-homework, tutoring-research,
tutoring-homework, ai-tutor-next, tutoring-ai, tutoring-caution, ai-tutors-colleges,
ai-tutor-questions, peer-colleges, bowen, skills-hub, other-apps, animations, hub-first-build, the-ask.
The Public Overview track (8 stops) was **not** given the title slide or the Macro App slides.

## Chase's desired feel

- Title: **Time to Pilot AI**. Subtitle: "What I've built, what other colleges are doing, and what Lone
  Star should do next." Byline: **Damon McDaniel, Mathematics Professor, LSC-Montgomery** (his words:
  abbreviate to LSC, "-Montgomery").
- The home screen is a **launcher for different versions of presentations**; clicking "Present VP of
  Instruction" starts at the title slide.
- Credibility intro, about 3 minutes: early ChatGPT adopter, tiny programming background (started in
  programming, switched to math, 25+ years away), chronic elbow tendonitis, built accessibility tools,
  learned guardrails. He talks aloud about the copy-and-paste coding days; it is only in the notes.
  The health detail is **one line** on the slide; he may bring his hat with the presenter mouse to show
  how he uses a computer without his hands.
- The Macro App is proof of scale ("not a 100-line script"): **more than 350,000 lines** (approximate is
  fine; I counted about 390k in git-tracked non-test, non-vendor source). Tagline only: "A workflow
  accessibility app." Order: calendar, first day handout, gradebook, makeup exam. Pearson is a spoken
  mention under the calendar (no slide). Assignment Assistant is optional, notes only.
- **Do not expose how the gradebook works** (his college may not allow it). The slide says only "A full
  gradebook that talks to D2L" (image only); details are in the speaker notes.
- Wants slides **visual and big**: images enlarge to full screen on click, bigger text on the background
  slide, a larger video, no clutter. Subtitle lines that look like tags: he prefers plain white text.
- Idea kept for later, in the Library: Lone Star needs to **move from "AI can help you study" to a
  committee and real implementation**, courses that **require** AI (built around AI use), and a
  "paradigm shift" in how courses are taught, not "add AI and call it done." Saved as Library page
  `next-steps-thoughts` ("What Lone Star Should Do Next", section Reference, not in any track).

## Accepted decisions

- Home: logo, "Presentations", a button per track, Browse every page. The title slide is a real page
  (`id: "title"`, `titleSlide: true`) with logo, title, subtitle, byline.
- `welcome` is now a **Part 2 divider**: kicker "Part 2", title "Building Learning Tools with AI", no
  body. His reason: the "AI could not do math" line did not lead into what he did, because he is not
  using AI in math class itself.
- Engine and page features added today: `points big`, `image hero` (large, no text), click-to-zoom
  lightbox on every screenshot (closes only by Close button or Escape, never the backdrop), video options
  `rate`, `simple` (single Play/Pause/Replay button), `big`, `nochip`, speed buttons keep 1x/2x/4x/8x with
  the default highlighted, `callout mid` (centered vertically in a board), `chips light` (white card,
  black text).
- The makeup exam video is **processed**: 4K source downscaled to 1080p, top black bar cropped, student
  roster blurred for the whole clip, student ID field blurred only between t=4.5s and 7.5s, audio removed.
  It plays at 2x automatically. The original `C:\Users\chase\Videos\Make Up Exam.mp4` still shows real
  names.
- gj-tutorial video: caption and "Video" pill removed, defaults to 2x. `gj-results` title is now
  "Completing a Problem on Their Own". The "I do not have a control class..." callout moved from
  `gj-ready` to its speaker note. `gj-adapt` closing statement is centered; the Example Student chips
  card is white.
- Speaker notes (`site/shared/notes.js`, printable `site/notes.html`) were updated for every new slide.

## Rejected directions

- A Pearson slide (now a spoken mention). Macro App bullets and "I spent a summer building it". The
  "five of the things it does" line. "It was the first thing I built in the app." Gradebook sync wording
  (Pull/Push) and bullets.
- Any agent commentary on slides (see `AI presentations/AGENTS.md`).

## Current implementation state (all uncommitted)

`AI presentations` repo: modified `site/shared/content.js`, `site/shared/engine.js`,
`site/shared/notes.js`, `site/v2-stage.html`; new `site/media/macro-app-d2l.webp`, `macro-calendar.webp`,
`macro-gradebook.webp`, `macro-handout.webp`, `macro-makeup-exam.mp4`. Data loads in node, stops resolve,
`node --check` passes. Chase viewed the deck and said the Macro App slides "look good." I never took a
screenshot. The Programs root has unrelated dirty files from other sessions; do not touch them.

## Open questions and constraints

- **ChatGPT logo** on the How I Got Here slide (right side, like the Macro App screenshot) is **not done**:
  none on disk, and downloading needs his explicit permission. I asked once (OpenAI brand page vs. he
  supplies the file); he never answered. Ask once more or skip.
- Whether to add a matching **"Part 1"** divider (his message cut off at "Let's build it like"). Not built.
- With 30 minutes, the second half needs more room and likely rework. `the-ask` still reflects the old
  Copilot and risk-tier framing, and the Skills Hub is not yet the closing pitch he described. Check with
  him before rewriting.
- Add the title slide and the Macro App slides to the Public Overview track only if he asks.
- FERPA: showing real student names or IDs is risky, especially with a public version and an artifact
  link. Keep the blurs; the gradebook screenshot uses "Student 1, 2, 3". Do not suggest unblurring.
- The Claude artifact (`artifact/vp-presentation.html`) is **stale**; do not rebuild or republish unless
  he asks.
- `gj-adapt` still has a PLACEHOLDER student quote about animations going too fast (flagged in
  `content.js`).
- His OBS problem was a source and canvas size mismatch (4K display on a smaller canvas); the fix was Fit
  to Screen plus 1920x1080 output. If he re-records, process the new file the same way (blur names).
- Never open a browser or launch a GUI without asking (he asked to "bring up" the deck once; that was
  explicit). No em dashes. Windows PowerShell rules apply.

## Exact next step

Ask Chase what he wants next in the deck. Candidates he has raised: the ChatGPT logo (permission to
download, or his own file), a Part 1 divider, and giving the second half more room for 30 minutes. Start
from his reaction, then give him the deck link.
