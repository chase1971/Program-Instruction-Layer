# Momentum handoff: AI presentation site (Stage layout, Lone Star branded)

**Written:** 2026-11-07. Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify. Docs server on `http://127.0.0.1:8765/`.

## Objective and current phase

Chase is preparing what he calls one of the most important presentations of his career: a
~20 minute pitch to Lone Star College's **Vice President of Instruction**, plus a public version
he will promote on **LinkedIn**. Instead of PowerPoint he wants a **Wikipedia-like HTML site
that contains multiple presentations** ("tracks"): click Next through a talk, but anyone can
browse any page, and jargon (agents, context ladders, Claude Code) opens short definitions.

**Phase:** the site skeleton is built and the layout is chosen (**Stage**, option 2), restyled to
Lone Star College brand, and tuned for laptop/1080p projection. All content is still
**placeholder**. Next phase is real content: his data, conference findings, and screen recordings.

## The pitch (agreed framing, from discussion)

- **Ask ladder, smallest first:** (1) one legal/IT review of a defined AI tool set instead of a
  variance per tool (he got Cursor via a variance; wants Claude Code; Netlify, Supabase unknown);
  (2) a **faculty fellowship with course release** for a one-year pilot (both mechanisms exist at
  LSC); (3) pilot deliverables: **College Algebra Skills Hub**, a small cross-discipline faculty
  cohort, a student AI-tools trial; (4) vision: a permanent AI role/center, decided on results.
  Close with "What would it take to start this pilot, and who else needs to see it?"
- **Legal is the real barrier.** Split tools by risk (building / publishing / student data under
  FERPA) so most of the work is low-risk. Bring precedent: which peer colleges (esp. community
  colleges, ideally Texas) have Anthropic/OpenAI agreements.
- **Copilot:** the college likely has Microsoft 365 Copilot (chat, not a coding agent). Do not
  claim "Copilot can't code": GitHub Copilot is a real coding assistant and a fair fallback.
- **Talk order:** Gauss-Jordan tutorial (origin, has data) → guided homework apps (logic,
  transformations, GJ guided practice; small n, at most 28/section, say so plainly as the case for
  a pilot) → **side-by-side vs Pearson** (his app: 17 checkpoints in one problem vs Pearson's one
  answer box and "incorrect, try again"; easy to paste into ChatGPT) → peer colleges from the
  conference → five years (possibilities, not predictions; cost of waiting) → Copilot / legal tiers
  → Skills Hub → the ask.
- Show "better than Pearson/ALEKS" through the side-by-side, not as a bare claim.

## Chase's desired feel

- Stage layout: "really cool", keynote-like, slides that slide in; one link people can explore.
- Builds that animate in ("press a button and it shows the data... another graph... comes in
  nicely with transitions").
- He will **record videos** of himself using the apps and Pearson; no live demos.
- Wanted Lone Star look and logos. He said the blue felt "too blue" once but then only asked to
  remove the letterbox frame; the color question is unresolved (see Open questions).
- Not presenting with dwell, so dwell-sized targets are not needed for this site.

## Accepted decisions

- **Stage (`v2-stage.html`) is the chosen layout.** The other four were for comparison only.
- **Navigation:** clicker/keys: **up arrow and Page Up = next, down arrow and Page Down = back**
  (his presenter mouse; set via `upIsNext: true` in Stage only), right/left arrows too, Space next,
  N notes, F fullscreen. Big **edge arrows** mid-left/mid-right (faded, red on hover), shown only
  while presenting. Bottom HUD: **Home**, Library, **Restart presentation**, counter. Clicker test
  panel was removed at his request (it worked).
- **Glossary terms** open on hover and on click (click pins until X/Escape). Never close on outside
  click.
- **No letterbox frame:** the slide fills the whole window in one color.
- **Sizing:** base font `clamp(14px, min(.95cqw, 1.75cqh), 22px)` (~18px at 1080p, ~14px laptop);
  videos capped ~46% of screen height, side-by-side videos ~34%.
- **Brand (from lonestar.edu style guides):** Blue `#003768` (PMS 540) background, Red `#b30838`
  (PMS 201) accents (progress, Next, ladder numbers, title rule; never tinted), Tan `#f1c585`
  kickers, Light Blue `#c7eafb` secondary text/charts. Fonts Futura → Arial / Arial Black.
  White logos only on solid blue: stacked on title slide, extreme-horizontal top-right of slides.
  Logo don'ts: no shadow, stretch, outline, over images, tan or red.
- Logos saved locally in `assets/` (works offline).

## Rejected directions (do not rediscover)

- PowerPoint / single linear deck.
- Field Guide, Studio, Story, Atlas layouts (built, not chosen).
- Centered fixed 16:9 frame: clipped text ("300+") and showed a second-color strip.
- Original font size `min(1.55cqw, 2.75cqh)`: far too large; he had to scroll on a big monitor.
- Next/Back at the bottom-right corner of the HUD.
- Duplicate element ids inside per-slide markup (broke jsdom tests in Atlas); use classes/data attrs.

## Current implementation state

Folder: `agent docs/scratch/presentation-skeletons/` (indexed in `agent docs/INDEX.md`).
- `shared/content.js`: all pages, two tracks (`vp` 10 stops with speaker notes, `public` 4 stops),
  glossary. Markup: `[[term]]`, `[[term|label]]`, `[[@pageId|label]]`. `sample: true` shows a
  "Placeholder numbers" tag. Video blocks without `src` render a labeled slot.
- `shared/engine.js`: routing (`#t=track&s=stop&b=build`, `#p=page`), builds, block renderers
  (lead, text, callout, quote, video, stat, stats, bars, compare, table, ladder, cards, glossary),
  media stack, glossary popovers, keys. Shared by all variants.
- `shared/base.css`: build/transition mechanics and neutral block styles.
- `v2-stage.html` (~205 lines): the chosen layout with LSC brand, edge arrows, HUD, Library overlay.
- `assets/lonestar-vertical-white.svg`, `assets/lonestar-extreme-horizontal-white.svg`.
- `choose.html`, `v1/v3/v4/v5-*.html`: comparison variants, now unused.
- Verification: headless jsdom scripts (scratchpad, not in repo) stepped the full VP track, keys,
  hover/click popovers, Home/Restart, edge arrows: **no errors**. jsdom cannot check layout:
  whether every slide fits without scrolling on his laptop is **unverified**; he said "that's better".
- jsdom used from `School Scrips/Factoring Guided Practice/node_modules/jsdom`, loading pages via
  `JSDOM.fromURL` on 8765 (fromFile breaks `history.replaceState`).

## Open questions and constraints

- **Firefox new-window question (pending answer):** his default browser is Firefox; chat links
  open as a tab in an existing window. Offered: he unchecks Settings → General → Tabs "Open links
  in tabs instead of new windows", or the agent adds
  `user_pref("browser.link.open_newwindow.override.external", 2);` to his profile `user.js` (only
  with his explicit yes; persistent config change).
- **Color:** keep Lone Star Blue background, or darker navy shade with blue as accent? Unasked.
- **Logo on public/LinkedIn version:** the brand guide does not cover faculty/personal pages and
  requires approval for anything uncovered. Get Marketing & Communications OK or ship the public
  track without the logo.
- Before the meeting Chase should find out: which Copilot LSC provides; whether the Cursor variance
  can be renewed or serve as a model.
- Conference transcripts exist somewhere on his machine (he has more to watch); not yet located.
- Promote Stage to its own clean site folder (drop the four unused variants) when real content
  starts. Hosting for the public link (Netlify needs his explicit deploy request) is undecided.
- Rules: no em dashes anywhere; ask before putting anything on his screen; no Netlify deploy
  unless he says so in that message.

## Exact next step

Ask Chase for the real material for the first stop that has data: the **Gauss-Jordan tutorial
results** (where the data lives, or the numbers) and whether a recording exists yet. Then replace
the `gj-tutorial` placeholders in `shared/content.js` and add `src` to its video block.

## Read first

1. This file.
2. `agent docs/scratch/presentation-skeletons/shared/content.js` (content model) and
   `v2-stage.html`.
3. `agent docs/rules/html-delivery.md` (links are `http://127.0.0.1:8765/...`, never file paths).
