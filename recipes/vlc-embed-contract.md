# VLC embed contract

> **You might say:** "embed VLC", "the video rectangle", "VlcStage"
> **What it is:** VLC Win32 embed — PID matching, VlcStage owns the video rectangle
> **Source:** converted from `Video Player/.cursor/rules/vlc-embed-contract.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `Video Player/electron/vlc/**`
- `Video Player/src/app/components/VlcStage.tsx`

---

## Win32 / VLC

- All VLC reparenting and Win32 calls live in `electron/vlc/` only — do not scatter FFI elsewhere.
- Match VLC's window by **PID** (`GetWindowThreadProcessId`), **never** by Qt window class string (changes across Qt5 → Qt6).

## Renderer

- `VlcStage` is the **only** component that owns the on-screen rectangle where VLC mounts. Move/resize the video region via `VlcStage` layout — no competing positioning logic in main or other components.

## State

- Watched list, resume positions, settings: JSON in `%APPDATA%\video-player\data\` — do not introduce a database.
- Resume/seek uses VLC HTTP interface (`--extraintf=http`, port 9885) via `httpClient.js` and `playbackMonitor.js`.
