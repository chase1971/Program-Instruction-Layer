# Momentum handoff — 11.2 homework recording on gj-homework slide

**Written:** 2026-11-11  
**Continue in:** fresh task (any tool / model)

> **Not in `latest.md`.** That slot still holds today's **AACU Day 1 extract panels** handoff
> (`2026-11-11_aacu-day1-extract-panels.md`). Do not overwrite it for this topic. Read **this file**.

---

## Objective and current phase

Chase is filling the **AI presentations** VP deck with real app walkthrough videos. Logic homework
is already on **Other Math Apps** as a looping wall clip. This chat finished the **page before
that in the VP track**: **Guided Practice as Homework** (`gj-homework`) with **one full 11.2
guided-practice problem**.

Phase: **re-recorded with human UI**. Chase asked for typing and selecting instead of
`adminGiveAnswer` auto-fill. Recorder now drives the real keypad/buttons with a visible cursor.
Clip is ~110s (was ~23s). Still on VP stop 18.

---

## Chase's desired feel

- Same automation pattern as the Logic homework recorder: **headless Playwright**, drive the real
  app, ffmpeg to MP4, drop into `AI presentations/site/media/`.
- For 11.2: **one full problem**, not a montage. Looks like real homework (11.2 chrome), not a
  half-started mid-column state.
- Presentation link must be a **clickable `http://127.0.0.1:8765/...` URL**, not a `C:\` path.
- Head-mouse / no surprise GUIs: recorders stay **headless**.

---

## Accepted decisions

- **Slide:** VP track stop **`s=18`** → page id `gj-homework`, title "Guided Practice as Homework".
  Correct open link:
  `http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=18&b=0`
- **Video on slide:** `AI presentations/site/media/gj-homework-demo.mp4` wired in
  `site/shared/gj-evidence.js` (`src`, `rate: 2`, `autoplay`).
- **Portal record mount:** `?record-gp=1` → `RecordGpApp` → `GuidedPracticeRecordView` with
  `window.__gpRecord` (`done` / `canGive` / `giveAnswer` / `snapshot`). Uses first 2×2 bank
  problem via `FRAME_GALLERY_TWO_VAR_IDS[0]`, `prependSystemSetup`, `adminGiveAnswer` loop.
- **Recorder:** `School Scrips/student-portal/scripts/record-gp-homework.mjs` ·
  `npm run record:gp-homework`. Viewport **812×460** (portal landscape chrome). Playwright added
  as portal devDependency. Windows vite teardown uses `taskkill /T /F`.
- **Logic exemplar (already shipped earlier this session):**
  `School Scrips/logic-app/scripts/record-logic-homework.mjs` →
  `AI presentations/site/media/app-logic-homework.mp4` on Other Math Apps wall.
- **Deck extract:** Gauss-Jordan evidence pages live in `site/shared/gj-evidence.js` (loaded after
  `content.js`); `content.js` was reduced so it stays under the soft extract line.

---

## Rejected directions

- **Do not** use `DECK.pages` array index in `#s=` — that is the track **stop** index. Page index
  46 for `gj-homework` is wrong; VP stop is **18**.
- **Do not** record portal homework at large desktop viewports (1280×800) with a guessed crop —
  content sits phone-landscape and the first crop was a useless corner. Use **812×460**, full frame.
- **Do not** open a visible browser or portal window to "check" the recording without asking.
- **Do not** overwrite `momentum-handoffs/latest.md` while the AACU Day 1 panels handoff is still
  the active `latest` for that other thread.

---

## Current implementation state

**student-portal (uncommitted):**

- `src/config/recordGpLink.ts`
- `src/app/RecordGpApp.tsx`
- `src/features/frame-gallery/GuidedPracticeRecordView.tsx`
- `src/main.tsx` (mount order: record-gp → practice → App)
- `scripts/record-gp-homework.mjs`
- `package.json` / `package-lock.json` (playwright + `record:gp-homework`)
- `media/recordings/gp-homework-demo.mp4` (+ frame scratch under `media/recordings/gp-frames/` if still present)

**AI presentations (uncommitted, mixed with other parallel work):**

- `site/media/gj-homework-demo.mp4` (and `app-logic-homework.mp4`, other media from parallel agents)
- `site/shared/gj-evidence.js` — homework video block filled
- `site/shared/notes.js` — gj-homework note updated to play the recording
- Plus many unrelated dirty files (AACU review pages, colleges, sessions, etc.) — **do not** assume
  those belong to this recording task.

**Verified:** Human-UI re-record completed; ffprobe ~110s, 812×460; frames show keypad presses,
cell-by-cell matrix fill, operation picks, and row-op typing with cursor. Deck MP4 replaced.
Still `rate: 2` on the slide (playback ~55s).

**Not done:** Chase has not confirmed the new pacing. No commit/push.

---

## Open questions and constraints

- Whether ~23s at `rate: 2` is enough detail, or he wants slower `GP_RECORD_STEP_MS` / longer hold.
- Whether Other Math Apps should get more wall clips next (Transformations, etc.) — he has not asked
  since this homework clip.
- Netlify deploy is **never** unless he says so in the same message.
- Parallel AACU handoff remains in `latest.md` — keep topics separate.

---

## Read first

1. This file (`agent docs/momentum-handoffs/2026-11-11_gj-homework-recording.md`)
2. `AI presentations/AGENTS.md` (deck voice rules)
3. `School Scrips/student-portal/scripts/record-gp-homework.mjs` + Logic exemplar
   `School Scrips/logic-app/scripts/record-logic-homework.mjs`

---

## Exact next step

Wait for Chase’s reaction to the human-typing clip (speed up `rate` / KEY_MS, trim length, or
approve). Open
`http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=18&b=0`
only if he asks. Do not touch the AACU `latest.md` handoff unless he is continuing that topic.
