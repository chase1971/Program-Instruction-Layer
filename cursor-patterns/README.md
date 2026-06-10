# cursor-patterns/

> Reusable coding standards and patterns for all of Chase's projects.

---

## Start Here

**[CODING_STANDARDS.md](./CODING_STANDARDS.md)** — the master file. Single source
of truth for file size limits, App.tsx orchestrator rule, modal sizing, React
patterns, anti-patterns, and the final-build checklist. Read this first.

**[INIT_NEW_APP.md](./INIT_NEW_APP.md)** — recipe for scaffolding a new app
(educational-math / functional-tool / electron-overlay variants). AI follows
this when you say "initialize a new app." **Electron apps:** Step 4b + **[electron-per-monitor-display-scaling.md](./electron-per-monitor-display-scaling.md)** (required).

---

## Deep-Dive References

These files are referenced from `CODING_STANDARDS.md` when more detail is
needed. You don't read these front-to-back — you jump in when relevant.

| File | When to read |
|---|---|
| [file-size-enforcement.md](./file-size-enforcement.md) | Full reference for the 800-line rule and extraction triggers |
| [FILE_SIZE_QUICK_REFERENCE.md](./FILE_SIZE_QUICK_REFERENCE.md) | One-page cheat sheet for size limits |
| [react-patterns.md](./react-patterns.md) | Building hooks, services, components, state extraction |
| [modal-pattern.md](./modal-pattern.md) | Building any modal/dialog/wizard (`max-w-md`!) |
| [modal-scrolling-fix.md](./modal-scrolling-fix.md) | When modal content needs to scroll properly |
| [file-headers.md](./file-headers.md) | Standardized header format for new files |
| [refactoring-checklist.md](./refactoring-checklist.md) | When the user says "refactor", "clean up", or "make it 9/10" |
| [anti-patterns.md](./anti-patterns.md) | Common mistakes catalog |
| [accessibility-patterns.md](./accessibility-patterns.md) | Building dwell-friendly UIs (Chase uses dwell-mouse) |
| [electron-per-monitor-display-scaling.md](./electron-per-monitor-display-scaling.md) | **Required** for every Electron shell: Display button, per-monitor scale, exemplar Calendar 2.0 |
| [CODING_STANDARDS.md § Windows: Hidden Launchers](./CODING_STANDARDS.md#windows-hidden-launchers-bat--node-spawn) | `.bat` one-liners, no visible cmd, Node spawn from Electron |
| `School Scrips/App Dashboard/docs/LAUNCHER.md` | apps.json registry, ports, Toolbar Shift+F5 |
| [logging-standards.md](./logging-standards.md) | Logging conventions and levels |
| [animation-frame-debug-tool.md](./animation-frame-debug-tool.md) | React dev tool for pixel-perfect overlay debugging |
| [add-a-line-change-a-sign.md](./add-a-line-change-a-sign.md) | Educational math animation pattern (negatives, subtraction) |

---

## How AI Sessions Find This

- **Claude Code:** Auto-loads `C:\Users\chase\Documents\Programs\CLAUDE.md`,
  which points here.
- **Cursor (Programs workspace):** `.cursor/rules/00-programs-entrypoint.mdc`
  (`alwaysApply: true`) — entrypoint + index of every file in this folder.
  File-specific rules: `10-file-size-before-edit.mdc`, `20-modal-pattern.mdc`.
- **Cursor (User Rules):** Settings → Rules → User Rules still supplements
  accessibility and session protocol; canonical code standards remain
  `CODING_STANDARDS.md`.
- **Per-app:** `[app]/.cursor/rules/` and `[app]/CLAUDE.md` when working inside
  an app (e.g. Macro App: `macro-modals.mdc`, `embedded-browser-modals.mdc`).

---

## Archived Files

Older/specialized files were moved to
`C:\Users\chase\Documents\Programs\Archived markdowns\cursor-patterns\`.
Mostly dwell-mouse/electron-overlay implementation patterns that aren't
relevant outside the electron-toolbar app.
