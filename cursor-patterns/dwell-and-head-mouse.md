# Dwell & Head-Mouse — drag handles and overlays

> Building a drag handle or a hover/dwell interaction on an overlay? **Don't invent a new
> mechanism — copy how the electron-toolbar's existing overlays already do it.** That's the
> whole rule. Timing (how fast it latches, how long it takes to release) is controlled through
> the toolbar's own settings, not a value to invent or copy into new code.

## Where the real overlays live

| What | Path |
|---|---|
| OS-level dwell click engine | `electron-toolbar/modules/dwell/backend/` |
| Overlay hover/dwell factory — the actual drag-handle mechanism | `electron-toolbar/electron-app/src/overlay-hover-poll.js` |
| Existing toolbar interaction patterns | `electron-toolbar/electron-app/patterns/` (indexed by its own `README.md`) |
| Exemplar recipe to model a new one on | `recipes/studio-dwell-latch.md` |

## Modal rule

No backdrop dismiss — see `CODING_STANDARDS.md` § Modal Pattern.

**Last updated:** 2026-08-07 — cut from 175 lines to this at Chase's direction. The prior
version's timing tables, "four implementations" comparison, cross-layer-coupling essay, and
non-negotiable-behaviors list were AI-generated detail nobody was using; the one thing that
mattered — where the real overlay code lives — is above.
