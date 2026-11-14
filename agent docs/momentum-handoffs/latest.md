# Momentum handoff — VP deck: campus notes pass (URI, Indiana Wesleyan, Boise)

**Written:** 2026-11-13  
**App / area:** `AI presentations` (VP stage track)  
**Phase:** Campus Readiness talk-notes pass through Boise (`campus-networked`). URI and Three Pathways (Indiana Wesleyan) notes/slides refined earlier in this chat. Boise overview summary + overview bullets + notes rewritten. Next stop in the pass: `campus-14day` (Touro).

---

## Objective and current phase

Chase is building the VP of Instruction presentation after AAC&U. Campus readiness slides already exist; this stretch is making each stop speakable: overview bullets in his voice, and especially **talk notes he can glance at and say out loud** without decoding fragments.

**Where we stopped:** Boise State (`campus-networked`) notes were just rewritten as speakable sentences. Chase approved the *shape* of that writing for notes going forward. He has not asked to continue into Touro yet.

**VP track order (recompute from `tracks` stops after any edit, never guess `s=`):**  
`aacu-conference` 22 · `campus-readiness` 23 · `campus-maturity` 24 · `campus-maturity-indicators` 25 · `campus-lsc-guidelines` 26 · `campus-other-campuses` 27 · `campus-uri` 28 · `campus-three-pathways` 29 · `campus-networked` 30 · `campus-14day` 31 · `campus-aligning-values` 32 · `campus-coherence` 33 · then frameworks / classroom / productivity / `future-ideas`.

Handy stage links (local server assumed):  
- Three Pathways: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=29&b=0`  
- Boise: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=30&b=0`  
- Next (Touro 14 Day): `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=31&b=0`

---

## Chase's desired feel (critical — notes)

**Talk notes must be sentences he would speak aloud** that make the campus move understandable. That is the main correction of this chat.

Do:
- Complete sentences in his presentation voice.
- Explain what the thing *is* and what people *did*, so a glance makes the story clear.
- Expand jargon into what it means in the same sentence (policy guidance, briefs, LMS live-build, etc.).
- Keep notes short enough to scan; cut staffing counts, name laundry lists, and numbers he said he does not care about unless he asks.

Do not:
- Label-colon dumps (`Hackathons: …`, `Homegrown Boise State AI: …`).
- Stage directions (`bring this up`, `skip unless asked`, `talk point:`, `gist:`, `optional if you want`).
- Meta about the session (`they opened the presentation with…`). Say the campus situation, not how the AAC&U panel was structured.
- Cryptic summary phrases that only make sense after reading the transcript (`turned a seven-day time log into an AI analysis partner`, `de-identified log` without saying strip the name and paste into AI).
- Agent-voiced asides, verification hedges on the slide, or notes that explain the notes to Chase.

**Slide text** stays his voice too (existing `AGENTS.md` spoken-bullets rule). Summary under the title = campus situation / what they built, not “opened with a SWOT.”

**Transcript fidelity:** when he asks what someone meant, go back to the AACU transcript under `C:\Users\chase\My Drive\AACU\unwatched\` and answer plainly, then put the clear version in notes. Do not invent beyond the source.

**Head-mouse:** never open stage/GUI without asking. Hand him `http://127.0.0.1:8765/...` links. No em dashes. No Netlify.

---

## Accepted decisions (this stretch)

| Decision | Why |
|---|---|
| URI ATL workshop titles + faculty consultation live in **notes only** | He named A.I. and Writing, AI in the Classroom, Navigating AI…, consultation; not more slide lists |
| Indiana Wesleyan question-shift on slide/notes = old assignments easy for a chatbot, what do I do | Tiffany’s wording is “weren’t designed with AI in mind”; Chase’s clearer practical meaning |
| Course Refresh talk point = technologist beside faculty building live into Brightspace | What he wants to bring up; not turn-taking |
| AI literacy vs resilient = use AI on purpose vs redesign so a chatbot cannot finish alone | Verified in transcript |
| Soft Lone Star parallel: Timothy Mousel / D2L session mentioned in Three Pathways notes | Live-in-LMS help has happened at LSC; he is unsure if it was activities |
| Hackathons ≠ fix-one-assignment workshop; that is just-in-time / Institute hour | Tiffany: half-day for one program goal (e.g. set AI level from their scale) |
| Boise overview summary/bullets: situation + builds, not “they opened with…” | Meta about panel structure does not belong on the slide |
| Boise notes: speakable rewrite; drop nursing/grant unless he asks later | He named what he cares about: split, informal→committee, non-binding briefs, Institute purpose, homegrown LLM + FERPA/HR |
| Briefs = suggestions on contentious topics (tutoring, detection, grading, proctoring), not binding policy | “No formal policy stakes” = nobody had to follow them; something written so meetings could move on |

---

## Rejected directions / do not rediscover

- Wall-of-text notes with student counts, every speaker role, and “herself + one FT + one PT.”
- Reading the question-shift as “how do I put AI in all my assignments.”
- Calling hackathons drop-in assignment help workshops.
- Explaining jargon *to* Chase in the notes (“Crosswalks (plain English): …”) instead of writing the speakable sentence.
- Keeping “next topics: course materials, agentic AI” when the transcript only named titles with no content.
- Putting “bring this up / skip nursing” style directions in notes.
- Treating detail-page cryptic example blurbs as enough; when he uses an example, spell the assignment redesign in plain language (Daphne spiritual-formation time log is the exemplar).

---

## Current implementation state

**Repo:** `AI presentations` (also Programs root for agent docs / handoff). Nothing committed/pushed this chat.

**Touched this stretch:**
- `AI presentations/site/shared/notes.js` — `campus-uri` ATL lines earlier; `campus-three-pathways` rewritten several times then stabilized; `campus-networked` just rewritten speakable.
- `AI presentations/site/shared/content-campus.js` — Three Pathways question-shift + example bullets; Boise overview `summary` + overview `blocks` (briefs replaced nursing/grant on overview).
- `AI presentations/site/shared/panel-summary-trims.js` — matching question-shift / Boise summary lines.
- URI PDF detail and earlier URI slide work from prior turns in same day still in tree.

**Sources:**  
`C:\Users\chase\My Drive\AACU\unwatched\Three Pathways One Foundation.md`  
`C:\Users\chase\My Drive\AACU\unwatched\Utilizing a Networked Approach.md`

**File size:** `notes.js` ~365 lines; `content-campus.js` ~325. Under caps.

**Verification:** content edits only; stage not opened this stretch. Chase views stage himself.

**Still open from older campus work:** Brazelton self-assessment webform TODO (red) in maturity-indicators notes, if still present.

---

## Open questions and constraints

- Capture the speakable-notes rule into `AI presentations/AGENTS.md` (gap logged on scorecard this session). Do that early in the fresh task if continuing notes work.
- Chase may still want Boise detail page (`campus-networked-detail`) aligned to the same speakable / non-meta standard; overview was the focus.
- Do not launch GUI / stage without asking.
- Mid-session: no commit/push unless he says pull / put on GitHub / end of session.

---

## Exact next step

1. If continuing the campus notes pass: open Touro `campus-14day` at `s=31`, read current overview + `notes.js` + `C:\Users\chase\My Drive\AACU\unwatched\` 14 Day transcript/summary, then rewrite notes (and fix overview phrasing if it is session-meta or cryptic) as **speakable aloud sentences only**, matching the Boise notes voice.
2. Before editing notes elsewhere, add a short keyword row / section in `AI presentations/AGENTS.md` for talk notes: speakable sentences, no stage directions, no label-colon dumps.

**Read first:** `AI presentations/AGENTS.md` (spoken-bullets + talk notes) → `site/shared/notes.js` keys `campus-networked` (exemplar) and `campus-14day` → matching `content-campus.js` pages → AACU unwatched transcript for that panel.

---

## Repos touched

- `AI presentations`
- `Programs/` root (`agent docs/momentum-handoffs/`, session tracking)
