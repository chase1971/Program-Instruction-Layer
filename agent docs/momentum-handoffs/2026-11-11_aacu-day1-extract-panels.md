# Momentum handoff — AACU Day 1 extract panels (approve/disapprove)

**Written:** 2026-11-11  
**Continue in:** fresh task (any tool / model)

---

## Objective and current phase

Chase is building the **AI presentations** pitch deck (Lone Star VP of Instruction) from AAC&U 2026 conference sessions. Transcripts are captured. Next phase is **not** more Zoom downloading: it is **extracting candidate presentation panels from Day 1 transcripts**, each with **thumbs up / thumbs down**, so Chase can approve or reject before anything is consolidated into the real Stage deck.

Phase right now: handoff boundary. Capture pipeline for Days 1–3 unwatched Zoom recordings is done. Chase just watched **AI Communities of Practice** and discussed what is usable from a discussion-format session. He asked for more panels with approve/disapprove UI, then immediately asked for this handoff **before** building those panels.

---

## Chase's desired feel

- He wants a **review queue**, not a finished deck dump. Panels first → he thumbs → then consolidate the ones he likes.
- Even when a session looks irrelevant, **still make a summary panel**. He will decide. Do not pre-filter away "weak" sessions.
- Capture rules already set: auto-captures stay in `AACU\unwatched\` so he knows he has not watched them; watched stay in `AACU\` root; **do not mark checklist HAVE** for auto-captures; mute Zoom players when capturing (he watches other video at the same time).
- On Communities of Practice: it is "more like just a discussion," but the "what is holding you back / restrictions on experimenting with AI" thread resonated with what he is going through. Prefer **usable extract** (claims, questions, tensions) over a flat recap.

---

## Accepted decisions

- **Unwatched folder:** `C:\Users\chase\My Drive\AACU\unwatched\` for auto-captured transcripts. Watched remain in `C:\Users\chase\My Drive\AACU\`.
- **Checklist:** `electron-toolbar/apps/aacu-transcript-checklist/` — HAVE only for ones he watched / deliberately saved. Do not flip HAVE for batch captures.
- **Agent Browser** (CDP 9227) + script `Agent Browser/scripts/capture-aacu-unwatched.mjs` (`--day 2` / `--day 3`) for muted Zoom transcript pulls via Zoom Events transcript API.
- **Opening Plenary:** dropped from presentation needs earlier (summary-only / not a priority).
- **Communities of Practice use:** faculty-conditions / third-space framing and diagnostic questions are fair game; **not** a student-facing college exemplar card like ASKED or course chatbots.
- **Next build shape (Chase's words):** add more panels to the presentation area, each with thumbs up / thumbs down; he evaluates; later consolidate liked ones. Next agent starts with **Day 1**.

---

## Rejected directions

- Do not treat every AACU session as a "college card" peer-example. Discussion / CoP sessions may only yield framing or diagnostic questions.
- Do not mark HAVE for transcripts he has not watched.
- Do not put agent voice, draft caveats, or "I could not verify" into on-screen deck text (`AI presentations/AGENTS.md`).
- Do not open/launch the Stage deck or Agent Browser GUI without asking (never-display rule).
- Do not Netlify-deploy or GitHub-push as part of this handoff.
- Do not skip summarizing a Day 1 session because it "does not look relevant."

---

## Current implementation state

### Transcripts

**Day 1 checklist** (`aacu_transcript_checklist.py`):

| Session | Status |
|---|---|
| AI Communities of Practice — Caparas / Dodge | Watched; file in AACU root |
| Coordinating AI Strategy Across URI | Unwatched capture in `unwatched\` |
| From Experimentation to Framework — de Castro | HAVE (watched) |
| From Logistics to Meaning-Making — Booker | **Not on Zoom** (empty search) |
| From Textbooks to Chatbots — Landon | HAVE |
| Has Claude Heard Any Good Ones — Huskey | HAVE |
| From Players to Designers — Kio (UF) / Falade (Texas A&M) | HAVE |
| Our Co-Evolution with AI — Hughes | HAVE |
| Building an AI-Ready Faculty — Metzler | HAVE (was summary concern earlier; file exists) |
| Governing AI / Smoother Sailing / Cognitive Pyramid / AI Policing / When AI Interprets / AI Misuse | Unwatched captures in `unwatched\` |

**Unwatched folder** has ~36 `.md` files (Day 1 + 2 + 3 Zoom pulls). Day 2 saved 11; Day 3 saved 18; many checklist titles simply are not on Zoom.

**Communities of Practice extract already discussed (do not rediscover from scratch):**

- Claim: top-down AI PD creates resistance; CoP / third space prioritizes psychological safety over deliverables.
- California Learning Lab CoP: ~8 months, twice monthly, peer-led, CCC/CSU/UC, cross-functional, funded.
- Stealable questions: silos that limit/support AI experimentation; ways proving yourself as an academic limits exploring AI; if free of campus politics, what pedagogical/professional risk would you take.
- Named tensions: private AI use vs public silence; faculty vs admin role freedom; committee ≠ CoP; grief ("time to grieve our discipline").
- Fit: faculty-conditions slide section, not a peer-college swap card.

### presentation site

- App: `AI presentations/` (own git repo). Stage: `site/v2-stage.html`. Content: `site/shared/content.js` (**already ~715 lines — over 700 extract threshold; extract before adding large new blocks**). Engine: `site/shared/engine.js`. Related: `colleges.js`, `sessions.js`, `notes.js`.
- Existing AACU summaries also live in School documents / `sessions.js` generation path; do not invent a second parallel inventory without checking what exists.
- Docs server: open Stage only after asking. Prefer headless checks or hand Chase a path/URL statement.

### tooling from this chat

- `Agent Browser/scripts/capture-aacu-unwatched.mjs` — batch CDP capture, muted, writes `unwatched\`, reports `_dayN-capture-report.json`.
- Address bar Paste/Go already on Agent Browser from earlier in the conversation.
- INDEX row for AACU checklist + unwatched path is updated.

### verification

- Day 2/3 batch scripts completed (ok + not-found counts). Players muted after runs.
- No thumbs-up/down panel UI built yet (explicitly deferred to the next task after this handoff).

---

## Open questions and constraints

- Exact UI home for approve/disapprove panels: Chase said "add some more panels to the presentation" with thumbs up/down. Prefer extending the existing Stage / a review mode inside `AI presentations` rather than a one-off HTML island, **unless** file-size / orchestrator rules force a separate review page. Ask one question only if placement is genuinely ambiguous after reading `AI presentations/AGENTS.md` + current Stage patterns.
- Persistence of thumbs: needs a dwell-safe control (no backdrop-dismiss modals; small buttons OK per head-mouse density recipe). Store approve/reject state so consolidate can filter. Prefer existing patterns (localStorage / APPDATA / simple JSON) — grep before inventing.
- Day 1 "Logistics" has no transcript; make a short "not on Zoom" stub panel so the queue is complete, or omit with a note in chat — Chase still wants coverage of Day 1.
- Kio college = University of Florida (confirmed earlier); D'Amico = Alamo Colleges District. Some deck/college cards may still need those updates if touched.
- Never display without permission. PowerShell: no `&&`.

---

## Exact next step

**Start Day 1 only:** for every Day 1 checklist session, read the transcript (root or `unwatched\`), write a **candidate presentation panel** (summary + any slide-usable claims, college names, frameworks, numbers, tensions — even if thin), and wire **thumbs up / thumbs down** on each panel so Chase can approve or reject. Do not consolidate into the final VP track yet. Do not batch Day 2/3 extracts until Day 1 review UI works and Chase has a path to click through it (ask before launching any GUI).

**Read first:** this file; `AI presentations/AGENTS.md`; `AI presentations/README.md`; Day 1 sources under `C:\Users\chase\My Drive\AACU\` and `...\unwatched\`; checklist order in `electron-toolbar/apps/aacu-transcript-checklist/aacu_transcript_checklist.py` day1 tasks.

---

## Repos touched this stretch (for later pull / wrap)

- `Programs/` root (agent docs INDEX, momentum handoffs, session tracking)
- `Agent Browser` (capture script)
- `electron-toolbar` (AACU checklist app; earlier in conversation)
- `AI presentations` (next agent will edit; may be dirty from prior nights)
)
