# Momentum handoff — VP deck: classroom examples done, productivity section added, Lone Star guidelines compared to Brazelton

**Written:** 2026-11-13  
**App / area:** `AI presentations` (VP stage track)  
**Phase:** Classroom examples (5) and a new "AI and Campus Productivity" section (2) are built. Two new slides after Brazelton compare Lone Star's AI guidelines to his six indicators. Chase has not seen any of it on the stage.

---

## Objective and current phase

Chase is building the VP of Instruction presentation after the AAC&U conference, to convince the VP to expand Lone Star's AI work by showing how much thought and work other institutions put in, plus cool class examples. This task finished the classroom examples, built the productivity section, reordered the track, and added a "how do we compare" pair of slides.

**VP track order now (recompute from `tracks` stops after any edit, never guess `s=`):** `aacu-conference` 22, `campus-readiness` 23, `campus-maturity` 24, `campus-maturity-indicators` 25, `campus-lsc-guidelines` 26, `campus-uri` 27, `campus-three-pathways` 28, `campus-networked` 29, `campus-14day` 30, `campus-aligning-values` 31, `campus-coherence` 32, `ai-frameworks` 33, `fw-*` 34 to 40, `classroom-examples` 41 (divider), `class-barking-tree` 42, `class-misuse-literacy` 43, `class-pixels-parameters` 44, `class-players-designers` 45, `class-ai-interprets` 46, `productivity-examples` 47 (divider), `prod-asu-modernize` 48, `prod-reclaim` 49, `future-ideas` 50.

Each slide has an overview (stage), a long detail page behind the top up arrow, and talk notes in `notes.js`. Medium trims for the summary-trim page already existed for these panels (`design`, `kio`, `when-ai-interprets`).

## Chase's desired feel (critical)

- **Overview bullets read like Chase speaking out loud.** One or two complete sentences, no lead-in labels, no fragments, no unexplained names. Rule lives in `AI presentations/AGENTS.md`. **One exception he asked for:** the Brazelton indicators slide and the Lone Star matchup slide use `Default:`, `Reach:` and so on, because he said "it's fine to use just the lenses and then a colon."
- **Slide text is his voice.** Interpretation of his own goes in `notes.js`, never attributed to speakers, never agent-voiced caveats on screen. I slipped an agent-style caveat onto a detail page once and removed it.
- **He checks the transcript.** He catches claims the transcript does not support (the "complaints from both directions" line was wrong: both complaints were opposition to AI; her sentence is garbled and she never describes a complaint that AI was NOT used).
- **Wording he asked for:** soccer player (not football player) in When AI Interprets; "favored" not "privileged"; no "department" explanation for Kio (just "had about 32 students in two courses"); Florida A&M for Kio and Texas A&M for the guest lecturer (affiliation came from Chase, not the transcript).
- **Classroom examples point:** students using AI to do things they likely could not do without it, across fields. Productivity point: staff and faculty using AI to build tools, save money, and get time back.
- **Lone Star matchup goal (his words):** show we have some of this but it is not very comprehensive. He expects thin classroom/reach coverage and thin support (four Udemy learning paths seems like not much).
- Never put anything on his screen without asking (he approved opening the browser pane once, for the student handbook; it is closed). No em dashes. No Netlify deploys.

## Accepted decisions

| Decision | Why |
|---|---|
| Classroom examples now come AFTER the classroom frameworks (`fw-*`), then the productivity section, then `future-ideas` | He built them out of order and wanted frameworks first |
| New section "AI and Campus Productivity" with ASU (Optimizing and Modernizing) and Brazelton (Reclaim Your Time) | His grouping name |
| ASU slide point is cost: lower revenue school, degree tracking tools too expensive, so Academic Affairs built its own | He asked for the cost angle. Staff built tools, faculty author audit rules, students are users (do not say students built them) |
| Reclaim slide includes other schools' examples from the chat (Drescher, Tuma) | He asked for what other schools do. Brazelton's ADHD and autism disclosure is notes only, off the slide |
| Brazelton overview: the six-indicator bullet was cut; indicators now live on their own slide (25) with his title kept | His request. The six-indicator bullet on the DETAIL page was kept |
| Lone Star matchup last bullet ("starting point, not a grade") removed | His request |
| Owner bullet says neither the 2025-26 faculty handbook nor the 2026-27 student handbook mentions AI | Both checked, see below |

## Rejected directions / do not rediscover

- "Complaints from both directions" framing for Kio (see above).
- Calling Kio's students "sustainability students" as a field. She teaches in a department of sustainability and the built environment; the games taught course content (not building design); sample games were irrigation and water use.
- Claiming students built the ASU tools; naming a staff headcount (transcript garbles it).
- Agent-voice caveats on any slide or detail page.

## Current implementation state

**Repos:** `AI presentations` (primary), `Programs/` root (handoff, scorecard). **Nothing committed or pushed.**

**Files (all under `AI presentations/site/shared/` unless noted):**
- `content-classroom.js` (216 lines): divider + Texas Tech, Lyon, Pixels to Parameters, Players to Designers, When AI Interprets, with details. Backgrounds `campus-6/7/8/9/2/3`.
- `content-productivity.js` (new, 99 lines): divider (`campus-4`), ASU (`campus-5`), Reclaim (`campus-1`), details in section `ref-productivity`. Script tag added to all six stage and notes HTML files.
- `content-campus.js` (308 lines): added `campus-maturity-indicators` and `campus-lsc-guidelines`.
- `content.js` (596 lines, watch the 800 cap): stops reordered, `ref-productivity` section added.
- `notes.js` (289 lines): notes for every new slide; classroom divider and `ai-frameworks` notes updated for the new order.
- `AI presentations/AGENTS.md`: routing row now names `content-classroom.js` and `content-productivity.js`.

**Verified:** `node --check` on all edited JS, headless stop-order and page-id resolution, no em dashes. **Not looked at on the stage.**

## Lone Star guidelines findings (facts to rely on)

Sources: lonestar.edu/AI-Guidelines ("Initial Guidelines for the Use of Generative AI"), its three Technology Services subpages, the Faculty Handbook 2025-2026 PDF (Chase's download), the 2026-2027 Student Handbook online viewer, and the Policy Manual V.D, V.E, V.F.
- Guidelines page: six sections (protect confidential data, check with Technology Services before buying tools, review content before publishing, follow academic policies, phishing, training with four Udemy paths). No date, owner or review schedule shown in the text extraction.
- Tool list: Copilot in testing, Adobe Firefly for students in select courses, ChatGPT and Claude.ai "not approved for internal usage."
- No page says what an instructor may assign, require or allow, and none has syllabus language. Only line: faculty should clarify their own expectations; students should ask instructors.
- Faculty handbook: no AI wording at all. Student handbook: all 104 section pages read in the browser pane, no AI wording (the viewer's own search is broken, returns 0 for every term). Policy Manual V.D lists cheating, fabricating, plagiarizing without defining them; V.E.1.3 could be read to reach AI but that is interpretation.
- My own read (notes only): early to developing on Brazelton's scale; syllabus template and division-requested syllabus items are an existing place for an AI statement.

## Open questions and constraints

- **Udemy learning paths:** `lonestar.udemy.com/learning-paths/8356553/` returns 403 for headless fetch (sign-in). Only titles known: Introduction to GenAI for All Employees, Organizational Wide Understanding, Emerging Technical Acumen, Productivity and Role-Based Skills, Transformational Leadership. If a path covers teaching, soften the Support bullet on `campus-lsc-guidelines`. Chase can paste the outline or sign in at the browser pane.
- **Footer date and owner:** the "no date, no owner" claims came from text extraction; Chase should confirm on the live page.
- **Student affairs claim** ("no page is written for student affairs") is based on pages read, not an explicit statement.
- Older Campus Readiness detail pages still have label openers ("Structure:", "Design rule:"); he said he would return to them. Campus Readiness slides have no `bg` photo (offered, not answered).
- Real photos not sourced; slides reuse generic `media/campus-1..9.jpg`.
- One classroom example he called too long was skipped (not named; ask if he wants it).
- Ambiguity in the transcripts: AskStinger spelled several ways (ASU); "5MA staff members" unclear (ASU); Brazelton "57 and 50" denominator unclear (earlier slide).

## Exact next step

Ask Chase (one question) whether he has looked at the stage yet and what he wants next. Likely: (a) finish the Lone Star comparison once he sees the Udemy paths, (b) look at the new slides on the stage and give feedback, or (c) go back to the Campus Readiness label cleanup. Do not launch the stage; hand him a link and a flat statement of what to expect.

**Read first:** `AI presentations/AGENTS.md` (spoken-bullets section and Everything-on-screen-is-Chase's-voice) → `site/shared/content-campus.js` (`campus-maturity-indicators`, `campus-lsc-guidelines`) → matching `notes.js` keys. Source transcripts are in `C:\Users\chase\My Drive\AACU\` (docx) and `...\unwatched\` (md).

---

## Handy links (local)

- Brazelton maturity: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=24&b=0` · indicators `s=25` · Lone Star match `s=26`
- Classroom divider `s=41` · Productivity divider `s=47` · ASU `s=48` · Reclaim `s=49`
- Summary trim: `http://127.0.0.1:8765/ai-presentations/aacu-summary-trim.html`
