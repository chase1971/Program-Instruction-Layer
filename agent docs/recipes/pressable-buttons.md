# Pressable buttons: they must look like buttons

> **You might say:** "the buttons don't act like buttons", "no 3D effect", "it doesn't look
> like I clicked it", "it's just a blue field", "make it look pressable", "raised button",
> "which one is selected", "I can't tell if it clicked", "buttons need a click animation",
> "did that save?"
> **What it is:** Every clickable button looks raised, lifts on hover, sinks when pressed,
> and a chosen toggle **stays pushed in**. Flat boxes and plain colored rectangles are not
> acceptable as buttons.

**Exemplar files: read these before writing new CSS. The numbers live there, not here.**

- `School Scrips/Macro App/renderer/src/styles/teacher-console-side-panel-buttons.css`: the
  full pattern, including the pushed-in toggle and the flat disabled state. Copy this one.
- `School Scrips/Macro App/renderer/src/styles/buttons-status.css`: `.da-btn--secondary`,
  `--primary`, `--danger`, the app-wide raised buttons it was modeled on.
- In use: `Macro App/renderer/src/components/side-panels/teacher-console/TeacherConsolePortalPreviewControls.tsx`
  (Live/Preview, Sign in as, Phone shape).

---

## Why it exists

Chase clicks with a head-mounted gyro mouse and dwell. He can't feel a click, so the
**screen is the only confirmation** that one landed. A flat white box, or a button that just
turns blue, gives him nothing to see. And a dwell click is so quick that a momentary
`:active` flash is often invisible, so **the lasting state has to carry the message.**

Found 2026-09-13 on the Teacher Console side panel: the app's raised buttons had been
overridden flat by `teacher-console.css`.

## The four states

| State | Looks like | How |
|---|---|---|
| **Resting** | Raised: light top-to-bottom gradient, thin border, a solid **bottom ledge** plus a soft drop shadow | `box-shadow: inset top highlight, 0 Npx 0 <ledge color>, soft blur` |
| **Hover** | Lifts slightly; border takes the accent color | `translateY(-1px)`, taller ledge |
| **Pressed (`:active`)** | Sinks level with the page; ledge gone, inner shadow | `translateY(<ledge height>)`, inset shadow, zero ledge |
| **Chosen toggle** (`--active`, `aria-pressed="true"`) | Accent color **and stays pushed in**, same as pressed | Same transform + inset shadow as `:active`, permanently |
| **Disabled** | Faded and **flat**: no ledge, no motion | `opacity`, `box-shadow: none`, `transform: none` |

Toggle groups (a pair like Portrait/Landscape) are how Chase confirms a click: the one he
picked stays down and the others stay up.

## Non-negotiables

| Do | Prevents |
|---|---|
| Give every button a bottom ledge at rest | "It's just a colored field" |
| Make the chosen toggle **stay** pushed in, not just change color | Chase can't tell whether his dwell click landed |
| Leave room for the ledge (`margin-bottom` ≈ ledge height) in stacked buttons | Ledges touching the next row or a divider |
| Flatten disabled buttons completely | A dead button that looks clickable |
| Style the chosen toggle's `:hover` too (same pushed-in look) | The chosen one popping back up when the pointer rests on it, which a gyro mouse does constantly |
| Put new button CSS in a small, feature-scoped file | Growing an already over-cap stylesheet |
| Also set `aria-pressed` on toggle buttons | The pushed-in state being only visual |

## Anti-patterns

- A later, more specific rule that flattens `.da-btn` (`background: #fff; border: 1px solid`)
  for one screen. This is exactly how the Teacher Console lost its 3D buttons.
- Selected state shown only by a color swap on a flat box.
- Relying on `:active` alone as click feedback.
- Adding "Clicked!" or success text to prove a click landed. Use the button state instead;
  see [no-ephemeral-feedback.md](./no-ephemeral-feedback.md).
- A hover-only effect that carries meaning (Chase's pointer hovers everything it passes).

## Dwell-proof press animation (every app, every button)

CSS `:active` never paints on a dwell click (mouse-down and mouse-up land in one frame), so
**every app also installs one global click animation** that plays its full duration however
short the press was. Added 2026-10-23 after Layout preview / Save / Reset in the portal looked
like flat text and Chase could not tell whether Save did anything.

- **The one implementation:** `School Scrips/Matrix app/src/app/utils/buttonClickFeedback.ts`
  (`installButtonClickFeedback()`; owns the duration constant). Idempotent, so an app embedded
  in the portal does not double up. Skips disabled buttons. Uses the individual `scale`
  property so it never clobbers a button's own `transform`.
- **Install it with one line at the app entry file** (`main.tsx`). Exemplars:
  `student-portal/src/main.tsx` (imports it via `@matrix/`) and `Matrix app/src/main.tsx`.
- **Wired so far:** student portal and Matrix app. Any other app: add the one-line install
  the next time you touch it.
- **Never write per-button press animations**, and never build a second mechanism.
- Every button must also **look pressable at rest** (border or fill, bottom shadow, pointer
  cursor). Exemplar: `.gp-check-layout-banner__btn` in `student-portal/src/styles/guided-practice.css`.

## Scope

Every app Chase drives, including the instructor controls in the student portal. Plain
student-facing portal buttons get the global animation but not the full raised-ledge styling.
