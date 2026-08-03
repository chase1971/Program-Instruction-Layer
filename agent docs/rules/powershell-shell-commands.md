# Windows PowerShell Shell Commands

> **Rung 5 — on demand.** The always-on summary is root `AGENTS.md` § Windows PowerShell 5.x; this
> file is the detail behind it. Read it when that section is not enough.
> **What it covers:** Windows PowerShell shell syntax — no && chaining; use ; or parallel tool calls. Summary lives in AGENTS.md § Windows PowerShell.
>
> *Was `.cursor/rules/30-powershell-shell-commands.mdc` until 2026-08-02. Moved because `.cursor/rules/*.mdc`
> only load when a matching file is open in a Cursor editor tab — which is not how Chase works.
> AGENTS.md links this file by path instead, so every tool can reach it.*

---

Chase's shell is **Windows PowerShell 5.x** (not PowerShell 7+). Models default to **bash / PS7** syntax — **`&&` and `||` are invalid here** and fail with "The token '&&' is not a valid statement separator." This rule must stay always-on; agents do not reliably learn from one correction.

## Never

```powershell
cd "C:\...\Programs" && git status && git diff
```

## Do instead

**Preferred:** parallel Shell calls with `working_directory` (no inline `cd`):

```
git status    # working_directory: C:\Users\chase\Documents\Programs
git diff --stat
```

**One invocation:** semicolon only — `Set-Location "..."; git status; git diff`

**Run B only if A succeeded:** separate tool calls; check exit code — no `&&`.

## Also

- No `curl` — use `Invoke-WebRequest -Uri "..." -UseBasicParsing`
