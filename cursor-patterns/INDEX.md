# cursor-patterns/

> **Standards** — the shape all code must have. Read before writing code.
>
> Looking for **how to build a specific interaction** (drag, dwell, overlay,
> modal, canvas element, animation)? That is **`Programs/recipes/`** —
> see [recipes/INDEX.md](../recipes/INDEX.md). Different job, different folder.

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

## Match what Chase said

> Reached here from [agent docs/INDEX.md](../agent%20docs/INDEX.md). Match a row, read
> **that one file**. If nothing matches, grep — then add the row.

| You might say | Read this |
|---|---|
| "is this file too long" · how big can a file get · 800 lines · split it | [CODING_STANDARDS.md](./CODING_STANDARDS.md) § File Size Enforcement |
| "App.tsx is doing too much" · orchestrator · it should just wire things up | [CODING_STANDARDS.md](./CODING_STANDARDS.md) § App.tsx as Orchestrator |
| "make it look like the other modals" · modal width · modal sizing | [CODING_STANDARDS.md](./CODING_STANDARDS.md) § Standard Modal Sizing |
| "extract a hook" · too many useStates · service layer · no inline fetch · state extraction | [react-patterns.md](./react-patterns.md) |
| what do I name this · naming · casing conventions | [CODING_STANDARDS.md](./CODING_STANDARDS.md) § Naming |
| "put a header on it" · file header format | [file-headers.md](./file-headers.md) |
| "refactor this" · "clean it up" · "make it 9/10" | [refactoring-checklist.md](./refactoring-checklist.md) |
| what not to do · common mistakes · god file · bare except · silent failure | [anti-patterns.md](./anti-patterns.md) |
| "the button is too small to click" · dwell-friendly UI · hover-only won't work | [accessibility-patterns.md](./accessibility-patterns.md) |
| **any dwell / hover / drag timing value** — never copy one from anywhere else | [dwell-and-head-mouse.md](./dwell-and-head-mouse.md) |
| "initialize a new app" · scaffold a project · start something new | [INIT_NEW_APP.md](./INIT_NEW_APP.md) |
| the window opened on the wrong monitor · display scaling · the Display button | [electron-per-monitor-display-scaling.md](./electron-per-monitor-display-scaling.md) |
| hidden `.bat` launcher · no visible cmd window · spawn from Electron | [CODING_STANDARDS.md § Windows: Hidden Launchers](./CODING_STANDARDS.md#windows-hidden-launchers-bat--node-spawn) |
| "am I done" · final build checklist · ready to ship | [CODING_STANDARDS.md](./CODING_STANDARDS.md) § Final Build Checklist |
| apps.json registry · dev ports · Toolbar Shift+F5 | `School Scrips/App Dashboard/docs/LAUNCHER.md` |

**Moved to [`Programs/recipes/`](../recipes/INDEX.md)** (2026-08-02):
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
