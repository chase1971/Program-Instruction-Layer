# Never put anything on Chase's screen without asking

> **Rung 5 — on demand.** The always-on summary is root `AGENTS.md` § Never put anything on Chase's screen; this
> file is the detail behind it. Read it when that section is not enough.
> **What it covers:** Never run anything that puts pixels on Chase's screens, or changes his display config, without explicit per-run permission. Detail behind AGENTS.md § Never put anything on Chase's screen.
>
> *Was `.cursor/rules/05-never-display-without-permission.mdc` until 2026-08-02. Moved because `.cursor/rules/*.mdc`
> only load when a matching file is open in a Cursor editor tab — which is not how Chase works.
> AGENTS.md links this file by path instead, so every tool can reach it.*

---

Chase drives the cursor with a **head-mounted gyroscopic mouse and dwell-click**.
A window that appears unannounced steals focus and pointer context, and a display
change can leave him unable to see or click anything — including the button that
would undo it. Treat "something appeared on screen" as a **destructive side effect**.

## The rule

**Do not execute anything that renders on his monitors, or alters his displays,
unless he gave permission for that specific run in the current conversation.**

Permission is **per run, not per session**. "Yes, launch it" once is not standing
consent for the next launch.

## Needs explicit permission first

| Action | Examples |
|---|---|
| Launching a GUI app | `python main_app.py`, `launch.bat`, Electron/Tkinter/PyQt apps |
| Any window, dialog, or overlay | confirm dialogs, message boxes, splash screens, toasts |
| Smoke-testing UI code | "just checking the dialog renders" — **this still counts** |
| Opening a browser | `start http://localhost:5173`, `npm run dev` then navigating |
| Changing display config | `SetDisplayConfig`, `DisplaySwitch.exe`, resolution/topology/monitor on-off |
| Anything topmost or full-screen | overlays, screensavers, kiosk modes |

## Fine without asking

Headless and read-only work: `py_compile` / import checks, unit tests that create
no window, **read-only** display queries (`QueryDisplayConfig`, EDID reads),
linters, type checkers, `git`, file reads, and starting a **server** as long as you
do not open a browser at it.

## What to do instead

Write the code, verify it as far as you can headlessly, then **hand the test to
Chase**:

```
Ready to test. Run:  .\launch.bat
Expect: two prompts, one per screen, counting down from 15s.
Tell me what the log says.
```

Never substitute running it yourself. If you cannot verify without a visible
window, say so plainly and stop — an unverified change he can test beats a
verified one that hijacked his screens.

If a visible test is genuinely the only path forward, **ask first** and state what
will appear, on which screen, and how it goes away.

## Why this exists

An agent ran a Tkinter smoke test that opened confirm dialogs on both of Chase's
monitors with no warning, to verify a dialog it had just written. The code was
fine; running it was not the agent's call to make.
