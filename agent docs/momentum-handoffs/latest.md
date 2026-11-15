# Momentum handoff — VP Stage: Final Thoughts + Lone Star next

**Written:** 2026-11-14  
**App / area:** `AI presentations` (VP stage track)  
**Phase:** Final Thoughts stretch is in place through Bowen care + a closing Lone Star slide. Graphic attempts for that closing slide were rejected and removed. Sharing-the-deck-as-a-URL was discussed but not built.

---

## Objective and current phase

Chase is finishing the Lone Star College VP of Instruction Stage deck after AAC&U. Classroom examples, productivity, Building This Presentation, Starred Panels, and Final Thoughts (Bowen) are largely done. Last work in this chat was the closing slide **My Thoughts on What Lone Star Should Do** (`final-lone-star-next`), then engine default so bullet points appear all at once, then failed graphic attempts that Chase told us to strip out.

**Where we stopped:** Graphics removed from `final-lone-star-next`. Slide is text-only (four short overview bullets + full wording in notes). No commit/push.

---

## Chase's desired feel

- **Overview bullets** are short scan lines. **Down-arrow notes** hold the full speakable sentences.
- **No agent voice** anywhere on screen. His wording, his stakes.
- **No random decorative graphics.** He rejected AI-generated square illustrations and also rejected a hand-made floating SVG of book / neural net / silhouettes. Do not invent another graphic for this slide unless he asks with a clear reference or meaning.
- **Speakable notes** stay complete sentences he can say aloud (existing AGENTS talk-notes rule).
- Gallup care slide: use the **poll's exact wording** on the Stage question; keep Bowen's oral paraphrase in notes only.

---

## Accepted decisions

1. **Final Thoughts track:** divider → Bowen bio → 72% AI companion (question then answer) → AI professor avatars + HBS Foundry → 27% care (question then answer, then closing bullets) → **My Thoughts on What Lone Star Should Do** → sources page stays in References (`final-bowen-sources`).
2. **Gallup-Purdue 2014:** Stage title uses strongly agreed that their professors cared about them as a person. Answer **27%**. Bowen said it more like "one professor who cared"; notes explain both.
3. **Lone Star next overview (current):**
   - More faculty awareness of why we need to be prepared, and of what other colleges are already doing.
   - Faculty will need to be trained to bring AI into the classroom, not just a policy that says what is allowed.
   - A timeline with dates for where we want to be.
   - A D2L community AI group so people using AI in interesting ways can find each other and learn together.
4. **Course release / wanting to be more involved:** overview line removed; lives in **notes only**. Task-force disclaimer also notes-only (not under the title, not as first bullet).
5. **Bullet builds:** `engine.js` `points` now show **all bullets at once** by default. Opt back into one-by-one with `stepped: true`. **Stats** that step one-by-one stay as they are.
6. **Title spacing:** `.slide-title + .cols { margin-top: .85em; }` in `v2-stage.html` when there is no summary under the title.
7. **Starred Panels** presenter page: `aacu-buckets-present.html` (not the editing review tools). Earlier: Misc renamed **AI and Campus Productivity**; VP slides other-apps / hub-first-build / the-ask removed from track.

---

## Rejected directions (do not rediscover)

- **Decorative graphics on Lone Star next:** generated square/portrait scenes (timeline icons, teacher-student path + neural net compositions) and a transparent SVG of floating symbols. Chase: "random pictures," get rid of all of them. Leave the slide text-only until he asks for a specific visual.
- Do not put the task-force disclaimer back under the title or as overview bullet 1 (duplication he hated).
- Do not put course-release back on the overview.
- Do not re-add VP slides 54–56 style endings (other-apps, hub-first-build, the-ask) unless he asks.
- Em dashes: never.
- Do not launch Stage/GUI without asking.

---

## Current implementation state

**Repo:** `AI presentations` (own git root). Dirty vs `origin/main`; nothing committed this chat for the handoff.

**Key files:**
- `site/shared/content-final.js` — Final Thoughts pages including `final-lone-star-next` (**no image block**)
- `site/shared/content.js` — VP `stops` end with `final-lone-star-next` (index **58**)
- `site/shared/notes.js` — notes through `final-lone-star-next`; talk-note registration end page is `final-lone-star-next`
- `site/shared/engine.js` — points default all-at-once
- `site/v2-stage.html` — title→cols spacing; question-slide / prior Stage UX
- `AGENTS.md` — Final thoughts keyword row mentions Lone Star next
- Media kept for Bowen: `site/media/bowen-ai-professors.png`
- Media removed for Lone Star next: `lone-star-next.jpg` / `.svg` deleted

**Also uncommitted from earlier in the broader Stage pass (same repo):** productivity / classroom / Building This Presentation / buckets-present / notes / artifact churn. Treat as part of the live VP deck work, not as separate failed experiments.

**Stage links (recompute `s` if stops change):**
- Lone Star next: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=58&b=0`
- Bowen care: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=57&b=0`
- Stage root: `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=0&b=0`

**Sharing as a public URL (discussed, not done):** `127.0.0.1:8765` is local-only. Full `site/` can host on Netlify/Cloudflare (~46 MB MP4s are fine). Caveat: Starred Panels stars live in *his* localStorage. Claude artifact path in README is stale relative to current Stage. He had not chosen lasting host vs temporary tunnel yet.

---

## Open questions and constraints

- Does he want a real hosted link next, and if so Netlify/Cloudflare vs a short-lived tunnel?
- Any further polish on Lone Star next wording, or leave text-only as-is?
- When he says put on GitHub / end of session: commit `AI presentations` (and Programs root if agent-docs handoff files belong there).

**Rules that still bind:** never display without permission; no Netlify portal deploy from this; file-size caps; talk-notes speakable; after Stage edits always link with recomputed `s`.

---

## Exact next step

Open `final-lone-star-next` on Stage and confirm the four overview bullets + notes feel right with **no graphic**. From there, either polish that slide's wording if he asks, or pick up the deferred **shareable website link** question (host `site/` vs tunnel) if he wants that instead.

**Read first:** `AI presentations/AGENTS.md` (Final thoughts + talk-notes + after-Stage-change link rule), then `site/shared/content-final.js` and the `final-lone-star-next` / `final-bowen-*` keys in `notes.js`.
