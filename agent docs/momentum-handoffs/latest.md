# Momentum handoff — Logic Gates Extra Credit wall clip

**Written:** 2026-11-11  
**Continue in:** fresh task (any tool / model)

> Earlier today, other handoffs stay dated (do not overwrite them for those threads):
> - GJ homework deck: `agent docs/momentum-handoffs/2026-11-11_gj-homework-deck.md`
> - GJ homework recording: `agent docs/momentum-handoffs/2026-11-11_gj-homework-recording.md`
> - AACU Day 1 panels: `agent docs/momentum-handoffs/2026-11-11_aacu-day1-extract-panels.md`
>
> This slot is the **Logic Gates Extra Credit recording + Other Math Apps wall** continuation.

---

## Objective and current phase

Chase wanted a **human-feeling** Logic Gates Extra Credit (XOR) walkthrough video for the
VP **Other Math Apps** wall: truth table first, then placing / dragging / wiring the circuit
from AND, OR, NOT (not a flash-complete cheat).

Phase: **done for review.** Gates-only wall clip is cropped, entire video at **2x** baked into
the file (~17.6s, 820×360), homework clip removed from that slide. Chase asked for the
momentum handoff after approving whole-clip 2x (no split).

Open: [Other Math Apps](http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=19&b=0)
(`#s=` is the **track stop**, not `DECK.pages` index).

---

## Chase's desired feel

- Table can be quick; circuit must look like a person: palette clicks, drag gates into place,
  draw wires. Not teleport-complete.
- Desktop gates smaller without hurting phone hit targets.
- A / B letters and OUTPUT label smaller after size pass.
- Wall: gates clip only (homework starts the same way, so drop it). Whole clip 2x, no
  table/circuit split.
- Reviews on **local** stage / portal first. Live Netlify will not show unpushed size work.
- No surprise GUIs. Links only as `http://127.0.0.1:8765/...`. Flat handoffs, not
  "want me to…".

---

## Accepted decisions

- **Record stack (logic-app):** `?record-gates=1` → `window.__logicGatesRecord`;
  `scripts/record-logic-gates.mjs`; `npm run record:gates`; `docs/RECORD_GATES.md`.
  Bridge + data attrs on Port / GateShape / IOTerminal. Table-first in record mode;
  cheat / bypass can jump to circuit for Chase, but the **recording** stays table→circuit.
- **XOR shape:** (A∨B) ∧ ¬(A∧B) with AND, OR, NOT (two ANDs, one OR, one NOT).
- **Desktop vs phone sizes:** geometry `TOUCH_SCALE = 1`, `TERMINAL_BOX_SCALE = 1`.
  Phone restores size via `PHONE_VIEW_BOOST = 1.3 * 1.3` in `gateCanvasViewScale` when
  `(hover: none)` or `(pointer: coarse)`. Do **not** use a DESKTOP_VIEW_SCALE on short
  browser windows: portal canvases are often under 820×460, so that path never fired.
- **Label fonts:** `IOTerminal` `INPUT_LETTER_FONT = 24`, `OUTPUT_LABEL_FONT = 17`.
- **Portal cheat:** `LogicHomeworkView` uses `hasAdminCheats()` so Chase can open on circuit
  when allowed.
- **Wall:** `content.js` `other-math-apps` — single clip
  `[["media/app-logic-gates.mp4", 2.28]]`, `h: 26`, wall `rate: 1` (speed is **in the file**,
  do not also set wall rate 2). Notes: whole clip at 2x.
- **ffmpeg in `record:gates`:** `crop=820:360:150:40,setpts=0.5*PTS`, then copy to
  `AI presentations/site/media/app-logic-gates.mp4`.
- **Current deliverable file:** ~17.6s, 820×360, from full-speed source
  `logic-gates-2026-11-12T00-47-23-907Z.mp4` (35.08s) with crop+2x. Also copied to
  `logic-app/media/recordings/logic-gates-extra-credit-demo.mp4` and
  `agent docs/scratch/logic-gates-extra-credit-demo.mp4`.

---

## Rejected directions

- **DESKTOP_VIEW_SCALE** on canvas fit for "desktop shrink" — never applied on typical portal
  widths; shrink base geometry + phone boost instead.
- Judging size on **mathappsclass.netlify.app** after local-only edits — looks unchanged until
  deploy / local portal (`:5340/?s=CHASE1`).
- Keeping **app-logic-homework** beside gates on Other Math Apps — Chase dropped it; starts
  the same way as gates.
- Speeding **only** the circuit half (trim at ~12s / concat) — he then asked for whole-clip 2x,
  no split. Do not bring the split filter back.
- Wiring via flaky SVG mouse-capture alone — record script uses bridge `connect` / `armWire`
  plus human drag visuals.
- Netlify production deploy for this work — not asked; do not ship.

---

## Current implementation state

**Repos (dirty, uncommitted / unpushed):**

| Repo | Notable |
|---|---|
| `School Scrips/logic-app` | Record stack, gate sizing, IOTerminal fonts, GateSandbox bridge, `record-logic-gates.mjs` with crop+2x |
| `AI presentations` | `app-logic-gates.mp4` (untracked media), `content.js` gates-only wall, `notes.js` |
| `School Scrips/student-portal` | `LogicHomeworkView` admin cheat bypass for gates |
| `Programs/` root | This handoff; scratch demo mp4/html |

**Verified:** ffprobe on wall file → 820×360, duration 17.6s. Stage link above for Chase.

**Not done / not requested:** Netlify deploy; deleting unused `app-logic-homework.mp4` from
media; re-recording from a new Playwright run (current wall file is retime of last good
capture).

---

## Open questions and constraints

- Chase may still want wall `h`, crop, or speed tweaks after looking at the 2x whole clip.
- Never launch GUIs / browsers without per-run permission.
- Never `deploy:prod` / Netlify unless he says so in that message.
- Modal backdrop dismiss is forbidden tree-wide; not touched here.
- Sister pull: session-guided uses `Repos touched:` below.

---

## Exact next step

Open [Other Math Apps](http://127.0.0.1:8765/ai-presentations/v2-stage.html#t=vp&s=19&b=0)
only if Chase asks you to launch something; otherwise wait for his reaction to the gates-only
2x wall clip (pacing, crop, size) and apply only what he names.

**Read first:** `School Scrips/logic-app/docs/RECORD_GATES.md`,
`AI presentations/site/shared/content.js` (`other-math-apps`),
`School Scrips/logic-app/src/app/components/gates/gateTypes.ts` (TOUCH / PHONE_VIEW_BOOST).
