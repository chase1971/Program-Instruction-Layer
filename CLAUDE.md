@AGENTS.md

## Claude Code

This repo uses `@AGENTS.md` as the shared baseline, so Cursor, Claude Code, and Codex
read the same text. App-specific guidance lives in each app's `AGENTS.md` — a keyword
table routing what Chase says to the one doc to read — imported by that app's
three-line `CLAUDE.md`.

**How to build something we've built before:** `recipes/README.md`.

`.cursor/rules/*.mdc` were retired 2026-08-02; do not create new ones.
