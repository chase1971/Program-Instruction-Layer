# Program-Instruction-Layer

Meta-backup repo for the **Programs instruction layer** — the rules, docs, and scripts that apply across every app under `C:\Users\chase\Documents\Programs\`.

## What lives here

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Always-on agent baseline (loaded every Cursor session) |
| `agent docs/` | Scorecards, audits, peer-review docs, session HTML logs |
| `scripts/` | `check-docs.js`, scorecard pipeline, doc server |
| `recipes/` | Shared UI/interaction patterns (dwell, toolbar, modals) |
| `cursor-patterns/` | Coding standards and init recipes |
| `.cursor/` | Cursor hooks (scorecard auto-tally) |

Individual apps (Macro App, electron-toolbar, math apps, etc.) have **their own git repos** as siblings under Programs. This repo tracks only the cross-app instruction layer — not app source code.

## Sync

```powershell
cd "C:\Users\chase\Documents\Programs"
git pull --ff-only
git push
```

See `AGENTS.md` § Git for multi-repo end-of-session protocol.
