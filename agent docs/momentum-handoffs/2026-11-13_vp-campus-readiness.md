# Momentum handoff — VP deck campus readiness + frameworks

**Written:** 2026-11-13  
**App / area:** `AI presentations` (VP stage track)  
**Phase:** Classroom frameworks stretch finished for now; Campus Readiness stretch started (URI + Three Pathways). More Campus & admin panels likely from summary-trim ★★★★ / ★★★.

---

## Objective and current phase

Chase is rebuilding the VP presentation after `aacu-conference` into two conference stretches:

1. **Campus Readiness** (institutional effort: strategy, faculty prep, tool training, titled teams)
2. **AI Frameworks** (named classroom checklists / scales)

Track order now: `aacu-conference` → `campus-readiness` → `campus-uri` → `campus-three-pathways` → `ai-frameworks` → classroom `fw-*` → `future-ideas`.

Classroom frameworks locked for this pass: TAKE AI.M, A.S.K.E.D., Five Pillars, Cognitive Pyramid, Flipping the Pyramid, Teaching with AI (FGCU), Six Essential Pedagogical Moves. **SIAC stays on the frameworks review page only** (not VP stage).

Campus readiness done so far: **URI Coordinating AI Strategy**, **Three Pathways, One Foundation** (Indiana Wesleyan).

---

## Chase's desired feel

### Classroom frameworks
- Overview = short/medium steps + graphic; detail via top ↑; return via bottom ↓.
- Notes hold the real talk track, denser than overview.
- Breadth matters: some slides (Six Moves) can be name-list only on overview if he will not speak long.
- Field pills gold; kind tags light blue (e.g. AI Tutor). Multi-Discipline when it applies across fields.

### Campus readiness (critical for next agent)
- **Point of the stretch:** show how much thought and work campuses put into AI. Not jargon feature lists.
- Story shape: **challenge → steps → what they put in place → results / still live**.
- Medium length on overview / summary-trim Short column: denser than 3-bullet short, shorter than full long review.
- Longer write-up on detail page (↑) and in notes.
- Exact speaker lines when he asks (URI: Sue Adams institutional-change quote).
- Concrete prep Chase can compare to Lone Star (tool training, titled roles, institutes with real Brightspace builds).

Rule doc: `AI presentations/docs/campus-readiness-story.md` (keyed from `AI presentations/AGENTS.md`).

---

## Accepted decisions

| Decision | Why |
|---|---|
| Section title **Campus Readiness**, not Governance | He wants faculty/campus prep framing, not “government” |
| Campus stretch **before** AI Frameworks | Institutional effort first, then classroom frameworks |
| SIAC: review page only, not VP track | Thin student acronym; already on SUNY college card |
| Six Moves: on VP track as breadth, six names on overview | Demonstrate range; full text in detail/notes |
| Flipping the Pyramid: upside-down shape; Creating at bottom tip; Remembering wide top | Literal flip of traditional Bloom categories |
| Flipping field: Multi-Discipline | Applies across fields, not Faculty Development |
| URI: exact Sue Adams lines; include tool training (Copilot/LibreChat/roadshows); drop grading-hypocrisy bullet from overview; keep structures/trust close | Matches what he remembered and what Lone Star lacks |
| “Ad hoc experimentation” = uneven local tool use, not a named pilot catalog | Transcript/report never inventory specific early experiments |
| Three Pathways: prep story with titled Lab + Institute results | Good demo of preparing faculty, not webinars only |
| Summary-trim Short drafts for these panels expanded to medium story shape | Short was too short for talk |

---

## Rejected directions / do not rediscover

- Do not put SIAC on the VP track unless Chase asks again.
- Do not treat Frameworks page as the home for URI / campus-admin panels (those are Campus & admin / summary-trim).
- Do not write campus slides as abstract governance feature lists (“federated,” “data tiers”) without the change path.
- Do not put the student “professor bans AI but grades with AI” complaint back on the URI overview.
- Do not invent what URI’s early ad hoc experiments were; sources do not name them.
- Do not launch the stage / GUI without asking.
- Do not deploy Netlify.
- No em dashes. Slide voice is Chase’s presentation voice only.
- Do not guess VP track `s=` indices; recompute from `tracks` stops after edits (campus inserts shift framework indices).

---

## Current implementation state

**Repos:** `AI presentations` (primary), `Programs/` root (agent docs / handoff / scorecard).

**Key files:**
- `site/shared/content-campus.js` — `campus-readiness`, `campus-uri` (+ detail), `campus-three-pathways` (+ detail)
- `site/shared/content-frameworks.js` — all `fw-*` overview + detail
- `site/shared/content.js` — VP stops order; `ai-frameworks` divider
- `site/shared/notes.js` — talk expansions
- `site/shared/panel-summary-trims.js` — medium drafts for `uri-coordinating`, `three-pathways`
- `site/shared/panel-frameworks.js` — review catalog (SIAC still here)
- `docs/campus-readiness-story.md` — extraction / slide story rule
- Stage HTML variants load `content-campus.js` after `content-frameworks.js`

**Approx VP indices (re-check):** campus-readiness ~23, campus-uri ~24, campus-three-pathways ~25, ai-frameworks ~26.

**Verification:** Headless page-id / track checks during build. Chase opens stage himself. No commit/push this handoff.

---

## Open questions and constraints

- Which Campus & admin panel is next from summary-trim ★★★★ / ★★★ (Admin / Govern as he directs)?
- Tag vocabulary for frameworks still open-ended beyond AI Tutor.
- Watch `content-frameworks.js` (~267 lines) and `content-campus.js` (~87) growth; keep satellites, not dump into `content.js`.
- Six Moves full move text by role still lives in their published CC document if he pulls it later.

---

## Exact next step

Continue **Campus Readiness**: open `aacu-summary-trim.html` Campus & admin / Govern ★★★★ and ★★★ list, ask Chase which panel is next if unclear, then add the same way as URI / Three Pathways: medium overview in `content-campus.js`, long detail ↑, notes, medium `panel-summary-trims.js` draft, VP stop after `campus-three-pathways` and before `ai-frameworks`. Follow `docs/campus-readiness-story.md`.

**Read first:** `AI presentations/AGENTS.md` (Campus readiness story row) → `docs/campus-readiness-story.md` → `site/shared/content-campus.js` + matching `notes.js` keys.

---

## Handy links (local)

- Campus Readiness divider: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=23&b=0`
- URI: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=24&b=0`
- Three Pathways: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=25&b=0`
- Summary trim: `http://127.0.0.1:8765/ai-presentations/aacu-summary-trim.html`
- Frameworks review: `http://127.0.0.1:8765/ai-presentations/aacu-frameworks.html`
