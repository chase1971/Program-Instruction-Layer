# Momentum handoff: AI presentation site, Gauss-Jordan section built with real data

**Written:** 2026-11-07 (second handoff today; replaces the morning "Stage layout" one). Valid for
today's continuation only.
**Nothing is committed or pushed.** No Netlify. Docs server on `http://127.0.0.1:8765/`.

## Objective and current phase

Chase is preparing a ~20 minute pitch to Lone Star College's **Vice President of Instruction**
(plus a public LinkedIn version) as a Wikipedia-like HTML site with presentation tracks, built in
the **Stage** layout. Pitch framing, ask ladder, and brand rules are unchanged from the morning
handoff (summarized under Constraints below).

**Phase:** the **Gauss-Jordan (GJ) evidence section is built with real data** (VP stops 2 to 10).
Next is real content for the rest: the guided-practice **homework** app (Precalculus, data due after
Wednesday), the static vs dynamic side-by-side recordings, the **Skills Hub** pitch (Chase has one,
not yet sent), peer colleges, legal tiers, the ask.

## Chase's desired feel (his words where they matter)

- Each point **slides in** on its own press and **stays**. Stats/charts must **all stay on screen**
  ("I don't like how you replace the previous one"). Use `board` pages for data.
- **No horizontal bars where label length shifts the bar.** He prefers rings/donuts or aligned bars;
  plain big numbers are fine for single percentages.
- **Framing of the GJ tutorial:** an *experiment in whether an app can teach on its own*, for
  self-directed learning. **Not** a missed-class catch-up tool (he rejected that as the lead). It is
  a **supplement, not a replacement**: his theory is that struggling with it before the lesson makes
  the lesson click. Don't call it "flipped".
- Be honest about limits: no comparison class; confidence gain includes his lesson; exam-score
  improvement is an unverified impression (speaker notes only, if asked).
- Comparisons with publisher platforms (Pearson) use **neutral headers, never red**. Publisher
  comparison belongs on the customization slide and the later static vs dynamic slide, **not** on
  the slides describing the tutorial itself.
- **No student names** anywhere; describe his data views rather than showing his screenshots.
- Presenting tools for himself: text size control and slide-skip buttons (built).

## Accepted decisions (current GJ section, VP track order)

1. `welcome` (still placeholder numbers)
2. `gj-why` "Learning from an app": experiment framing, 4 points.
3. `gj-setup` "The app was their introduction": topic, only row ops taught, worksheet copying,
   new problem on the back with no help/feedback, **6 classes: 4 Finite Math spring 2026, then 1
   Finite Math + 1 Precalculus fall 2026**. (Worksheet quote removed at his request.)
4. `gj-tutorial` "Inside the tutorial": video slot + 7 points (3 parts and can go back; part 3
   students answer; every click saved; **You lost me** button, added late, little data; autosolve
   summary; saves place; records under a code, no names). No mechanics of row reduction.
5. `gj-results` (board 2): 117 students; 81% never seen it (93/115); donut 71% (42 correct / 41
   correct method, small slips / 34 not successful).
6. `gj-before-class` "Learning before the lesson": supplement-not-replacement theory, 4 points.
7. `gj-ready` (board 3): rings 44% → 87% somewhat/very confident (78 responses); 87% easier to
   follow (68/78); 82% would use more apps (89/108); 3 student quotes (#31, #24, #34); closing line
   on no comparison class + assign guided tutorials before class + pilot link.
8. `gj-adapt` "Customizable and flexible apps" (board 2): feedback → "What I changed" pairs
   (more-in-depth-explanations quote → short tutorials; **pause/replay has no quote yet**; keyboard
   quote from in-app feedback → keyboard entry); AI-makes-change-easy callout; table Publisher
   platforms vs Apps I build (who it fits / fixing a problem / student feedback).
9. `gj-data` "What the apps tell me" (board 2): anonymized one-student miss chips and whole-class
   misses-by-skill bars (practice-set numbers from his screenshots), callout on three views.
10. `gj-homework` "Guided practice as homework": **placeholder** (Precalc, ~20 students, pending).
11. `side-by-side` "Static homework or dynamic guided practice" (board 1): two video slots, neutral
    headers, points; the old "17 vs 1" stat removed.
Then `homework-apps` and later stops are still placeholders.

Public track: welcome, gj-why, gj-tutorial, gj-results, gj-adapt, side-by-side, homework-apps.

## Rejected directions (do not rediscover)

- Titles: "They learned it from the app", "Fixed between classes, not between editions",
  "Homework that teaches, next to homework that grades".
- Missed-class framing as the purpose; "flipped instruction" label.
- Media stack that swaps one stat for the next; horizontal bars with per-row label widths.
- Red/colored publisher vs app headers; publisher lines inside the tutorial slide.
- Explaining row-reduction mechanics on the tutorial slide.
- Using his dashboard screenshots directly (they show student names).
- Invented claims (e.g. "without grading a paper by hand"); keep to what Chase said or the data.

## Current implementation state

Folder `agent docs/scratch/presentation-skeletons/` (all uncommitted):
- `shared/content.js` (~355 lines): pages, tracks, glossary (added `gauss-jordan`).
- `shared/engine.js` (~300): new blocks `points` (stepped slide-in), `donut`, `rings`, `fixes`
  (quote then fix, two builds per item), `chips`; block options `wide`, `span`, `rows`;
  `nextSlide`/`prevSlide`; count-up clamp fix (no negative flash).
- `shared/base.css` (~150): points, donut/rings, fixes, chips; bars now one shared grid so all bars
  start at the same x.
- `v2-stage.html` (~245): `board: true|n` pages (grid, everything stays), text size control
  top-left (A−/%/A+, plus/minus keys, 70% to 160%, localStorage `stage-zoom`), HUD buttons
  "‹‹ Slide" / "Slide ››", neutral compare headers.
- Source data: `C:\Users\chase\My Drive\M1324\GaussJordan_App_Experiment_Report.docx`,
  `GaussJordan_Combined_Raw_Data(3).xlsx` (follow-up comments on sheet "Follow-Up Responses"),
  worksheet `Unit 1\Matrix App Problem.docx` (matrices are WMF, not convertible).

**Verification:** jsdom scripts in the scratchpad (not repo) step the whole VP track, all builds,
no errors. Layout checked with **headless Edge screenshots** (no window): copy `v2-stage.html` to
a temp `zz-shot.html` with injected CSS `transition/animation:none` and a `requestAnimationFrame`
override so builds are fully drawn, screenshot at 1920x1080 and 1366x768, then delete the copy.
All GJ slides fit at both sizes. Real-browser look is Chase's to judge.

## Open questions and constraints

- **Pause/replay feedback quote:** not in the 35 written comments; Chase thinks a student said the
  animations were too quick (maybe email). Add it to `gj-adapt` item 2 `said` when found.
- **Homework section:** Precalc guided-practice homework results after Wednesday (~20 students);
  fill `gj-homework`, then the side-by-side recordings.
- **Skills Hub pitch:** Chase has it; the report's Skills Hub section is consistent.
- Byline: the report is signed Damon McDaniel; slides carry no author name. Ask before adding one.
- Still open from the morning: Firefox new-window setting; background color question; logo on the
  public version needs LSC Marketing OK.
- Pitch constraints: ask ladder (legal/IT review of one tool set → fellowship with course release
  → pilot: Skills Hub, cohort, student trial → permanent role); legal is the real barrier; do not
  claim Copilot cannot code.
- Rules: no em dashes; ask before putting anything on his screen (use headless screenshots); no
  Netlify deploy unless he says so in that message.

## Exact next step

Ask Chase which to do next: the **Skills Hub** pitch (he has text ready) or the **homework** section
(after Wednesday's data). Start with whichever material he provides.

## Read first

1. This file.
2. `agent docs/scratch/presentation-skeletons/shared/content.js`, then `v2-stage.html`.
3. `agent docs/rules/html-delivery.md` (links are `http://127.0.0.1:8765/...`).
