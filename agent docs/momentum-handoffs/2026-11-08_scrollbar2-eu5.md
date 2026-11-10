# Momentum handoff: Scroll Bar 2.0 (electron-toolbar), EU5 scrolling and size sliders

**Written:** 2026-11-08. Valid for today's continuation only.
**Topic file, not `latest.md`.** `latest.md` currently holds a live, unrelated handoff (AI
presentation second half), so this one is named by topic. In the fresh task Chase should say
"read the Scroll Bar 2.0 momentum handoff" (file `agent docs/momentum-handoffs/2026-11-08_scrollbar2-eu5.md`).
**Nothing is committed or pushed.** Nothing was ever launched; all verification is headless.

## Objective and current phase

Chase plays Europa Universalis 5 with a head mouse and dwell click. The old Tkinter F13 scroll
bar did not scroll in EU5, but the joystick scroll zones did. He wants one scroll bar that works
the way the joystick works, with the old bar's look. Phase: **built, green headless, waiting on
Chase's live test.** He has not yet seen it run.

(Original idea, a mod so EU5 scrollbar track clicks jump to the click position: answered as not
possible through a normal content mod. Dropped.)

## Chase's desired feel

- "I want the scroll bar to do what the joystick does." Same mechanism, F13 visuals.
- Everything that used the old scroll now uses 2.0 and behaves as before. Old module frozen.
- Sizing: "100% means whatever it currently is" and "0% essentially turned off", because a
  floor above zero "limits the range". No artificial minimums. Applies to the bar scale and
  the speed number size.
- He reviews live only. Never launch a window for him; hand him a flat test statement.

## Accepted decisions

- Scroll Bar 2.0 lives at `electron-toolbar/modules/scroll/scrollbar2/` (README, ARCHITECTURE,
  TESTING, AGENTS, tests). Manager code in `electron-app/src/window-managers/scrollbar2-*.js`.
- Mechanism cloned from the joystick: click-through Electron windows, 10 ms main-process
  `getCursorScreenPoint` poll, 50 ms arm delay, persistent Python child `scrollbar2_wheel.py`
  looping `pyautogui.scroll`, with a `--parent-pid` watchdog.
- Delivery `--mode`: default and europa (`pyautogui.scroll`), unity (page up / down keys),
  game_wheel (SendInput single notch). Scroll profiles (Default, Europa, Endless Legend 2,
  Caves of Qud) still choose the mode.
- Wiring: F13 toggles, F14 moves, toolbar Toggle Scroll button and Overlay Folder tile drive 2.0,
  both suspend managers cover it. Old `scroll` module frozen (`modules/scroll/backend/FROZEN.md`),
  nothing deleted; other apps still import helpers from it. Scroll zones and scroll profiles are
  separate and not frozen.
- Size sliders in Settings > Scroll Bar (and overlay-creator settings): both 0 to 100 in 1% steps,
  default 100, apply live via `scrollbar2-manager.refreshAppearance()`. 100% = bar 150 x 260 px,
  number 13 px. 0% = 1 px sliver and 0 px font. Clamps live in
  `electron-app/src/services/visual-clamps.js` (extracted so `profile-visual-overrides.js` stays
  near 703 lines).

## Rejected directions

- Patching the old Tkinter bar: never worked in EU5, root cause unproven. Do not go back.
- Any size floor (old 18 px strip, 8 pt font, `MIN_CONFIG_HEIGHT`): removed on purpose.
- `||` defaults for sizes: a saved 0 would read as 100. Use `??` and `>= 0`, `params.has(...)`.
- `os.kill(pid, 0)` on Windows: it terminates the target. Use `OpenProcess`/`WaitForSingleObject`.
- Calling the europa nudge in `scroll_wheel_delivery.py` a fix: it was an unverified guess, now frozen code.

## Current implementation state

- 23 node tests (`node --test modules/scroll/scrollbar2/tests/scrollbar2.test.cjs`) and 11 Python
  tests (`python -m unittest discover -s modules/scroll/scrollbar2/tests -p "test_*.py"`) pass,
  run from `electron-toolbar/`. On Node 22 / Windows name the test file explicitly.
- **Collision risk:** another agent edited the same files at the same time to restore Shift+F13
  duplicate bars (`scrollbar2-instance.js`, `SCALE.DUPLICATE`, `DUPLICATE_SPEED`, `SIGNALS.DUPLICATE`,
  `HOTKEYS.DUPLICATE`; duplicates draw at `scale * 0.5`). The `SESSIONS.md` entry says Shift+F13
  was retired; that is now out of date. Re-read files before editing, use small StrReplace edits.
  I did not verify whether `shift+f13` is back in `coordinator/module_registry.py`.
- `main.js` is 698 lines: extract before adding anything. `settings.html` (about 2.1k) and
  `overlay-settings.html` (about 805) were already over the cap; I only changed text and attributes.
- Unrelated dirty paths in the same repo (joystick files, `apps/eu5-setup-checklist/`, scripts-panel)
  belong to other work. Do not sweep them in.
- Untested: whether Windows draws a window at 1 px at 0%. The hover area stays the bar plus 30 px padding.

## Open questions and constraints

- Root cause of the old bar failing in EU5 is unproven; success is judged only by Chase live.
- No GUI launches without asking. No commits or pushes unless Chase says pull / put on GitHub.
- No em dashes. Small buttons. No ephemeral "saved" feedback.

## Exact next step

Wait for Chase's live-test report per `modules/scroll/scrollbar2/TESTING.md`. If he reports a
problem, fix 2.0 (not the frozen module), starting by re-reading `scrollbar2-manager.js` and
`scrollbar2-instance.js` because the other agent may have changed them. The test to hand him: restart
the toolbar, F13 to show the bar, scroll in EU5, then Settings > Scroll Bar, drag both sliders to 50%,
10%, 0%, back to 100%, restart with one at 0% and confirm it stays 0%.
