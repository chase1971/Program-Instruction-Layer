# Accessibility patterns — moved

> **Rung 5 — on demand.** Most of this file's original content — hover-delay patterns,
> lock-period code samples, a `useDrawerHover` hook that was never implemented, keyboard-
> navigation and screen-reader guidance, illustrative-only timing values, and external
> resource links — was removed 2026-08-07 at Chase's direction. It was generic
> web-accessibility boilerplate written for keyboard-only and screen-reader users, neither of
> which describes his setup (head-mounted gyro mouse + dwell-click + VoiceAttack), and none of
> it was governing anything in practice.

## What's actually needed, and where it lives

| You need... | Read |
|---|---|
| Dwell/hover/drag timing, overlay behavior, "how do I build a drag handle" | **[dwell-and-head-mouse.md](./dwell-and-head-mouse.md)** — the real source of truth |
| A dwell-click drag / toggle / countdown recipe | `Programs/recipes/` — `dwell-click.md`, `dwell-drag.md`, `hover-to-lock-drag.md`, `dwell-activation.md`, `dwell-countdown.md`, `toggle-pattern.md`, `mouse-hover-detection.md` |
| Modal backdrop-dismiss rule | [CODING_STANDARDS.md](./CODING_STANDARDS.md) § Modal Pattern — **never dismiss on backdrop click**, confirmed still wanted for every modal |

Do not maintain this file — update `dwell-and-head-mouse.md` or the relevant recipe instead.

**Last updated:** 2026-08-07 — gutted at Chase's direction; kept only the parts he confirmed matter.
