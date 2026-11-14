# Momentum handoff — VP deck classroom frameworks

**Written:** 2026-11-13  
**App / area:** `AI presentations` (VP stage track)  
**Phase:** Building classroom-framework slides after the AACU conference intro; four frameworks done; more may follow.

---

## Objective and current phase

Chase is rebuilding the VP presentation stretch after `aacu-conference`: divider **AI Frameworks**, then one overview slide per classroom framework (graphic, credit, field/tag pills, short step list, top ↑ detail / bottom ↓ back), with **full talkable expansions in `notes.js`** so he can speak the how-it-works without reading the detail page aloud.

Done in this chain: **TAKE AI.M**, **A.S.K.E.D.**, **Five Pillars of Logic**, **AI Cognitive Pyramid**. Colleges are off the VP track while this stretch is built.

---

## Chase's desired feel

- Same intro pattern every time: short summary of what it is / when it fits, then spell the steps; notes hold the real talk track.
- Graphics: flat blue/teal, faceless, metaphor that matches the framework. No marijuana / cannabis imagery (hard rule from A.S.K.E.D. art).
- Voice on slides is Chase's presentation voice only (no agent commentary). No em dashes.
- Expanded versions always land in **speaker notes** for every framework, denser than the overview bullets.
- Pills are building toward later filter/search: field of study vs kind tags, different colors as you go.

---

## Accepted decisions

| Decision | Why |
|---|---|
| Overview = short steps + image; detail page via top-edge ↑; return via bottom-edge ↓ | Matches TAKE AI.M / A.S.K.E.D. pattern Chase locked in |
| Framework pages live in `site/shared/content-frameworks.js` (satellite push onto `DECK.pages`) | `content.js` was near the 700 extract line; track stops stay in `content.js` |
| `field` / `fields` = gold `.field-pill`; `tags` = light-blue `.tag-pill` | Chase: field of study gold; kinds like AI Tutor another color for future search |
| Five Pillars: `field: "Nursing"`, `tags: ["AI Tutor"]` | Explicitly a tutoring bot, not only a nursing field card |
| Cognitive Pyramid = mainly **faculty assignment design** (who does the cognitive work; solo / support / delegate); students get told the mode, but the pyramid is not a student acronym like A.S.K.E.D. | Chase asked; answered from Inara Scott session material |
| Notes carry full write-ups; detail pages mirror them; overview can be slightly expanded lines (Cognitive Pyramid) when bare names are too thin | Chase: expand slide a bit, notes even more |

---

## Rejected directions / do not rediscover

- Do **not** center TAKE AI.M on the shaft / diameter demo; intent is commit-first design judgment (rescue-device style tradeoffs).
- A.S.K.E.D. graphic: decision / Sign–Veto / conflicting advisors — **no** cannabis leaves.
- Do not put agent process text on slides or stop-notes (`note: ""` unless Chase dictates).
- Do not launch the deck / GUI without asking.
- Do not merge field-of-study and kind into one gold pill list; keep `tags` separate.
- Do not treat Cognitive Pyramid as “student learns five pillar names” — it is teacher planning first.

---

## Current implementation state

**Repos:** `AI presentations` (primary), `Programs/` root (agent docs / handoff / scorecard).

**Key files:**
- `AI presentations/site/shared/content-frameworks.js` — all `fw-*` overview + detail pages
- `AI presentations/site/shared/content.js` — `ai-frameworks` divider; VP track stops include `fw-take-aim` → `fw-asked` → `fw-five-pillars` → `fw-cognitive-pyramid` before `future-ideas`
- `AI presentations/site/shared/notes.js` — full expansions per overview id (+ `*-detail` pointer lines)
- `AI presentations/site/shared/panel-frameworks.js` — review cards aligned (expanded parts, no colon shorthand where Chase asked)
- `AI presentations/site/v2-stage.html` — `pageHead` renders field pills + tag pills; edge ↑/↓ for detail
- Media: `site/media/fw-take-aim-board.jpg`, `fw-asked-decision.jpg`, `fw-five-pillars.jpg`, `fw-cognitive-pyramid.jpg`
- Scripts: `content-frameworks.js` loaded after `content.js` on stage + notes (+ other stage variants)

**Verification:** Headless page-id / track index checks earlier; Chase opens stage himself. No commit/push this handoff.

**Approx track indices (0-based on VP stops):** five-pillars ~26, cognitive-pyramid ~27 — re-check if stops change.

---

## Open questions and constraints

- Which classroom framework is next? Chase has been naming them one at a time (next after Cognitive Pyramid not chosen in this chat).
- Tag vocabulary for later search is open-ended; only **AI Tutor** exists so far. Add `tags: [...]` as kinds appear.
- `content-frameworks.js` will grow; watch line count before it needs a second split.
- Never deploy Netlify / never surprise-launch the stage.

---

## Exact next step

When Chase names the next classroom framework (or asks to tweak an existing one), add it the same way: expand `panel-frameworks.js` + overview/detail in `content-frameworks.js`, rich `notes.js` block, graphic into `site/media/`, VP track stop after `fw-cognitive-pyramid`, gold `field` + light-blue `tags` as needed. If he only says “continue frameworks,” ask **one** question: which framework is next from the classroom list on `aacu-frameworks.html` / `panel-frameworks.js`.

**Read first:** `AI presentations/AGENTS.md` (stage + pills row), then `site/shared/content-frameworks.js` and the matching `notes.js` keys for the last four `fw-*` slides.

---

## Handy links (local)

- Stage: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=27&b=0` (Cognitive Pyramid; adjust `s` if track shifts)
- Frameworks review: `http://127.0.0.1:8765/ai-presentations/aacu-frameworks.html`
- Notes page: `http://127.0.0.1:8765/ai-presentations/notes.html`
