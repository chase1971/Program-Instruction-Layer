# Momentum handoff — TC phone preview polish + Gauss-Jordan practice

**Written:** 2026-09-16 (Wednesday, ~4:00 PM)

---

## 1. Objective and current phase

Two threads in one session:

**A. Gauss-Jordan guided practice (Matrix app + student portal)** — largely **done**.
**B. Teacher Console landscape phone preview** — **browser width works**; **frame alignment
and color match** need one more pass.

**Phase now:** TC preview **phone-frame bezel** — Chase confirmed **top clipping is fixed**.
Still needs **1px left nudge**, **1px bottom up**, and **navy color match** between portal
header and Macro App phone frame.

---

## 2. Chase's desired feel

### Gauss-Jordan (done — do not redo unless asked)
- Row-entry calculator: live digits in pulsing cell before Next/Enter; ⌫ live; Next/Enter commits
- Entry cells: `shrink-0` + `text-lg` (not smaller font — flex squeeze was the clip bug)
- Step 4 row builder polish, taller keys, 5-col keypad — done earlier this session

### TC preview vs real iPhone
- Preview must show **same horizontal space** as phone: notch clearance + empty right margin
- **Embedded BrowserView width** must actually change when constants change (Chase measured
  with a ruler — bezel-only edits did nothing)
- Landscape viewport is **932×360** (812 real chrome + **120px** extra width; was 150, then
  −30px per Chase)
- **Notch pill** must not overlap home app icons — white panel shifted right (~50px inset)
- **Navy header** stays full-width flush left; only white content panel inset
- Phone **frame ring** must not clip flat at top/bottom — **top is now OK per Chase**
- Frame **hairline cracks**: nudge frame — side **in another 1px**, bottom **up 1px**
- **Border colors must match**: portal navy vs TC phone frame navy look different today

---

## 3. Accepted decisions

| Decision | Why |
|---|---|
| `STUDENT_PORTAL_PREVIEW_LANDSCAPE_WIDTH_EXTRA_PX = 120` | Chase tuned from 150 → 120 (−30px) |
| Viewport sizing via `--student-portal-preview-viewport-width/height` on `.browser-holder` | Only way to actually resize Electron BrowserView |
| `studentPortalPreviewFrameChromeWindow` adds inset + ring to outer holder | Ring shadow needs layout space or top/bottom clip |
| Dedicated `.teacher-console-live-preview__phone-frame` wrapper | Rectangular BrowserView inset inside curved bezel |
| TC preview home: `portal-content-wrap` gets `--portal-notch-inset` (50px) | Quiz banner still flush (`padding-left: 0` on focus+quiz) |
| `transform: translate(1px, 1px)` on phone-frame | Closed some hairline gaps; top now acceptable |

---

## 4. Rejected directions — do not redo

- **Smaller font on entry cells** — wrong; flex squeeze without `shrink-0` was root cause
- **Bezel/padding-only width changes** — BrowserView stayed 812px; Chase verified with ruler
- **Zero all notch inset in TC preview** — made preview not match phone right-side gap
- **Negative margin quiz banner breakout** — clipped Back button (`overflow: hidden` on panel)
- **`max-width: 100%` on preview holder** — clamped width changes to column width

---

## 5. Current implementation state (uncommitted)

### Matrix app
- `src/app/components/builders/MatrixEntryGrid.tsx` — `activeCellPreview`, `shrink-0`
- `src/app/components/guided-practice/GuidedPracticeSolver.tsx` — passes live preview string

### Student portal
- `src/styles/portal-compact-layout.css` — TC preview home notch inset; quiz banner flush
- `src/services/previewNotch.ts` — comments
- `src/styles/matrix-embed.css` — reverted smaller-font override

### Macro App renderer
- `src/utils/studentProgress/studentPortalChromeWindow.ts` — +120px landscape width,
  frame inset 14px, ring 11px in frame calc
- `src/utils/studentProgress/studentPortalChromeWindow.test.ts` — viewport + frame tests
- `src/components/teacher-console/TeacherConsolePortalPreviewEmbed.tsx` — phone-frame wrapper,
  viewport + frame CSS vars
- `src/styles/teacher-console.css` — phone-frame, holder ring padding, `translate(1px, 1px)`
- `src/styles/teacher-console-neumorphic.css` — ring shadow on phone-frame
- `src/styles/teacher-console-workspaces.css` — max-width none, overflow visible
- `src/styles/teacher-console-dashboard.css` — viewport vars on dashboard preview

### Verification
- Matrix app `npm test -- --run` — 38 passed (earlier this session)
- Macro App `studentPortalChromeWindow.test.ts` — 2 passed

---

## 6. Color mismatch — likely root cause (proposal, not yet applied)

| Surface | Color |
|---|---|
| Student portal `--portal-navy` | **`#002d5b`** (`portal-base.css`) |
| TC phone frame + ring | **`#1e3a5f`** (`teacher-console.css`, neumorphic ring shadow) |

Next agent should align frame background + box-shadow ring to **`#002d5b`** (or sample from
live portal header in preview and match exactly). Also check Macro App `--da-primary` — may
be `#1e3a5f` and wrong for this context.

---

## 7. Exact next step (one concrete action)

In **`Macro App/renderer/src/styles/teacher-console.css`** (and matching ring in
**`teacher-console-neumorphic.css`**):

1. Change phone-frame nudge from `translate(1px, 1px)` → **`translate(2px, 0)`**
   (side in +1px more; bottom up 1px — top stays fixed per Chase).
2. Replace frame/ring **`#1e3a5f`** with portal navy **`#002d5b`** everywhere on phone-frame
   (background + box-shadow ring color).

Restart Macro App; refresh portal preview. Chase verifies with ruler/eye — no need to launch
GUI for the agent unless asking first per AGENTS.md.

---

## 8. Open questions and constraints

- **Do not commit/push** unless Chase asks
- **Do not launch GUI** without asking (dwell/voice accessibility)
- **Calendar 2.0** frozen — do not touch
- **Windows PowerShell** — no `&&`
- If preview still wrong after color/nudge: trace `getEmbeddedBrowserBounds` → holder rect;
  phone emulation uses `width: 0` (follows real bounds — not the blocker)

---

## Read first (fresh task)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. `School Scrips/Matrix app/AGENTS.md` — only if touching guided practice
3. `School Scrips/student-portal/AGENTS.md` — if touching portal preview layout/notch
4. For frame work:
   - `Macro App/renderer/src/styles/teacher-console.css` (phone-frame, translate)
   - `Macro App/renderer/src/styles/teacher-console-neumorphic.css` (ring shadow)
   - `School Scrips/student-portal/src/styles/portal-base.css` (`--portal-navy: #002d5b`)
   - `Macro App/renderer/src/utils/studentProgress/studentPortalChromeWindow.ts` (sizes)
