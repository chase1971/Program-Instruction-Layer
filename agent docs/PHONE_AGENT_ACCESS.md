# Running an agent on this PC from Chase's phone

> **Rung 5 — on demand.** No always-on half; nothing about this fires unless Chase asks about
> phone access or the machine stops showing up.
>
> **What it covers:** the "My Machines" Cloud Agent worker that lets Chase send a task from
> his phone and have it execute on the desktop. Read it when he says *"do this from my
> phone"*, *"my PC isn't showing up"*, or *"push it so I can pull at work"*.

---

## How Chase uses it

On his phone, **cursor.com/agents** → the **cloud / remote machines** button (next to *start
from scratch*, which is the cloud-VM path and is **not** this) → pick **desktop** → type the
task. It runs here, on the real working tree, with his real credentials.

This is not remote desktop and not file sync. A small program sits on this PC waiting for a
message; when one arrives, an agent does the work locally.

Registered workspace roots (a task can only touch these):

| Root |
|---|
| `Programs` |
| `School Scrips/Macro App` |
| `School Scrips/App Dashboard` |
| `electron-toolbar` |

Add a root by editing `$workerDirs` in `scripts/cursor-worker-start.ps1`, then restart it.

## What's installed

| Piece | Job |
|---|---|
| `scripts/Start Cursor Worker.vbs` | starts the worker with no console window |
| `scripts/cursor-worker-start.ps1` | picks a working runtime, then supervises and restarts |
| Startup shortcut `Cursor Worker.lnk` | runs the `.vbs` at login |

The `.lnk` lives in `shell:startup`. If it's gone, recreate it pointing `wscript.exe` at the
`.vbs`.

## Two things the bare CLI gets wrong

**Idle release.** `agent worker start` defaults to `--idle-release-timeout 3600`: after an
hour idle the worker exits and the machine silently vanishes from the phone's picker —
exactly when Chase would reach for it. The script passes `0`.

**Runtime mismatch (build `2026.09.02-c22c1a3`).** The package ships Node 24, but its bundled
`better_sqlite3.node` is a **stale prebuilt dated 2026-06-15** — compiled for Node 22 and
never rebuilt when the pipeline bumped to 24. The worker dies starting its exec-daemon:

```powershell
$v = "$env:LOCALAPPDATA\cursor-agent\versions\<version>"
& "$v\node.exe" "$v\index.js" worker start --name abi-test --data-dir "$env:TEMP\abi-test"
# Error starting exec-daemon: ... better_sqlite3.node
# compiled against ... NODE_MODULE_VERSION 127. This version requires 137.
```

**Test it this way, not with a standalone `require` probe.** Two traps: `node_sqlite3.node`
sits at the top of the version dir and loads fine under Node 24, so it's easy to test the
wrong file; and grepping `index.js` for `better-sqlite3` finds nothing because the reference
lives in the chunk files (`9249.index.js`, `9277.index.js`).

**Scope is narrow** — this is why the bug can survive in a shipped build. Normal CLI commands
work fine under the bundled runtime (`index.js --version` exits 0); only the worker's
exec-daemon path breaks. Prebuilt binaries are per-platform, so other OSes may be unaffected.

The launcher falls back to system Node (22.x) when the runtime can't start the worker. **This
self-heals** — once a corrected build ships, the probe passes and it returns to the bundled
runtime. Don't hand-pin a Node version.

## When the machine isn't in the phone's picker

1. Is it alive? Two processes, one `powershell.exe` supervisor and one `node.exe` worker:

   ```powershell
   Get-CimInstance Win32_Process -Filter "Name='node.exe' OR Name='powershell.exe'" |
     Where-Object { $_.CommandLine -match 'worker start --name desktop|cursor-worker-start' } |
     Select-Object ProcessId, Name
   ```

2. **More than one pair means duplicates** — they fight over the data directory and the log.
   Kill them all, then run the `.vbs` once.

3. Launcher log: `%LOCALAPPDATA%\cursor-agent\worker-launcher.log`. The supervisor holds it
   open exclusively while running, so a read can fail with a sharing error — that failure is
   itself a sign it's alive.

4. Deeper: `node <version>\index.js worker debug` prints auth, routing, and visibility
   preflight.

Signed in as Chase's personal account, so no Enterprise plan or service account is involved —
`--pool` and everything about it is a different feature and irrelevant here.

## Deliberately not done

**Scheduled auto-commit-and-push.** Proposed as a way to solve "I forgot to push before
leaving"; Chase rejected it as unnecessary. Don't re-propose it.
