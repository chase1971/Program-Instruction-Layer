# cursor-patterns/

> **Standards** — the shape all code must have. Read before writing code.
>
> Looking for **how to build a specific interaction** (drag, dwell, overlay,
> modal, canvas element, animation)? That is **`Programs/recipes/`** —
> see [recipes/README.md](../recipes/README.md). Different job, different folder.

---

## Standards vs recipes vs values

| Kind | Home | Example |
|---|---|---|
| **Standard** — shape all code must have | **this folder** | `CODING_STANDARDS.md`, `file-headers.md` |
| **Recipe** — how to build one interaction | `Programs/recipes/` | `dwell-drag.md`, `modal-shell.md` |
| **Values** — timings, thresholds, sizes | `dwell-and-head-mouse.md` (here) + `dwell_constants.py` | never restated elsewhere |
| **Integration doc** — why one app's subsystem is like this | that app's `docs/` | `EMBEDDED_BROWSER_AND_MODALS.md` |

---

## Start Here

**[CODING_STANDARDS.md](./CODING_STANDARDS.md)** — the master file. Single source
of truth for file size limits, App.tsx orchestrator rule, modal sizing, React
patterns, anti-patterns, and the final-build checklist. Read this first.

**[INIT_NEW_APP.md](./INIT_NEW_APP.md)** — recipe for scaffolding a new app
(educational-math / functional-tool / electron-overlay variants). AI follows
this when you say "initialize a new app." **Electron apps:** Step 4b + **[electron-per-monitor-display-scaling.md](./electron-per-monitor-display-scaling.md)** (required).

**[dwell-and-head-mouse.md](./dwell-and-head-mouse.md)** — **the source of truth
for every dwell / hover / drag timing value in the tree.** Read before touching
any threshold. Never copy a number out of it into another file.

---

## Deep-Dive References

These files are referenced from `CODING_STANDARDS.md` when more detail is
needed. You don't read these front-to-back — you jump in when relevant.

| File | When to read |
|---|---|
| [react-patterns.md](./react-patterns.md) | Building hooks, services, components, state extraction |
| [file-headers.md](./file-headers.md) | Standardized header format for new files |
| [refactoring-checklist.md](./refactoring-checklist.md) | When the user says "refactor", "clean up", or "make it 9/10" |
| [anti-patterns.md](./anti-patterns.md) | Common mistakes catalog |
| [accessibility-patterns.md](./accessibility-patterns.md) | Building dwell-friendly UIs (Chase uses dwell-mouse) |
| [electron-per-monitor-display-scaling.md](./electron-per-monitor-display-scaling.md) | **Required** for every Electron shell: Display button, per-monitor scale, exemplar Calendar 2.0 |
| [CODING_STANDARDS.md § Windows: Hidden Launchers](./CODING_STANDARDS.md#windows-hidden-launchers-bat--node-spawn) | `.bat` one-liners, no visible cmd, Node spawn from Electron |
| `School Scrips/App Dashboard/docs/LAUNCHER.md` | apps.json registry, ports, Toolbar Shift+F5 |

**Moved to [`Programs/recipes/`](../recipes/README.md)** (2026-08-02):
`modal-pattern.md` → `recipes/modal-shell.md`.

**Archived** (superseded or stale — see `Archived markdowns/cursor-patterns/`):
`file-size-enforcement.md`, `FILE_SIZE_QUICK_REFERENCE.md` (lint + pre-commit),
`logging-standards.md`, `animation-frame-debug-tool.md`, `add-a-line-change-a-sign.md`,
`modal-scrolling-fix.md` (merged into the modal recipe).

---

## How AI Sessions Find This

Every tool lands on the same text, because `AGENTS.md` holds the content and
`CLAUDE.md` is a three-line import of it.

| Tool | Entry point |
|---|---|
| **Claude Code** | Nearest `CLAUDE.md` → `@AGENTS.md` |
| **Cursor** | `AGENTS.md` (root, and the app's) |
| **Codex / others** | `AGENTS.md` |

Per-app guidance lives in `<app>/AGENTS.md`, which routes by **what Chase says**,
not by which file is open. `.cursor/rules/*.mdc` glob contracts were retired in
2026-08 — they only fired when a matching file happened to be open in an editor
tab, which is not how Chase works.

---

## Archived Files

Older/specialized files were moved to
`C:\Users\chase\Documents\Programs\Archived markdowns\cursor-patterns\`.
Mostly dwell-mouse/electron-overlay implementation patterns that aren't
relevant outside the electron-toolbar app.
