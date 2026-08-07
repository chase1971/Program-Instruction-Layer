# Coding Standards — Master File

> **This is the canonical coding-standards file for all of Chase's projects.**
>
> **AI assistants:** Read this BEFORE writing or modifying any code in the
> `C:\Users\chase\Documents\Programs\` tree. The `CLAUDE.md` at the Programs
> root auto-loads and points you here.
>
> **Last updated:** 2026-06-02 (rev 2 — rule §9 Document the Lesson)

---

## How To Use This File

This is the single source of truth. The other files in `cursor-patterns/` are
deep-dives on specific patterns — this file references them when relevant.

**Reading order for a new session:**
1. This file (top to bottom — it's organized by importance)
2. The app's own `CLAUDE.md` or `guidelines/Guidelines.md` (app-specific rules)
3. Specific pattern files only when needed (e.g. `modal-pattern.md` if you're
   building a modal)

---

## Quick Reference Card — The 9 Most Important Rules

1. **CHECK FILE SIZE BEFORE EDITING.** Files have a hard 800-line limit. Files
   over 700 lines require extraction before adding anything new. See
   [File Size Enforcement](#file-size-enforcement-critical).

2. **The entry file orchestrates, never implements** — `App.tsx` (React), `main.py`
   (Python), `index.js` (Node), whatever it's called for the stack. Target under 100 lines.
   See [Entry File as Orchestrator](#entry-file-as-orchestrator).

3. **Modals use `max-w-md`. Never `max-w-3xl` or larger.** See
   [Modal Pattern](#modal-pattern).

4. **All API calls go through a service layer.** No inline `fetch()` in
   components. See [Service Layer](#service-layer).

5. **State over 5 useState calls or component over 300 lines → extract to a
   custom hook.** See [State Extraction](#state-extraction).

6. **Preserve existing behavior.** Don't refactor things you weren't asked to
   touch. Don't add "just in case" features.

7. **Electron apps include Display scaling.** Title-bar **Display** button,
   `#app-scale-frame`, slider + Fit-to-window. (Per-monitor auto-memory is
   optional, not required — build only if asked.) See
   [Electron Shell: Display Scaling](#electron-shell-display-scaling).

8. **Grep before adding any new mechanism.** Before creating a new hook,
   utility, service, IPC channel, log helper, state store, partition,
   registry, or any system another part of the code might already do:
   search the codebase (and sister apps) for what it would replace. If
   something exists, extend it. If you add a new one anyway, your response
   MUST name what you chose not to reuse and why. See [Grep Before Adding](#grep-before-adding-critical).

9. **Document the lesson when you finish a focused refactor or hotfix.**
   Write a `docs/<subsystem>_INTEGRATION.md` next to the affected code,
   modeled on `School Scrips/Macro App/docs/BROWSER_TAB_INTEGRATION.md`.
   The reasons code exists must live in the repo, not in your head. See
   [Document the Lesson](#document-the-lesson-critical).

---

## Electron Shell: Display Scaling

**Applies to:** Every app with an Electron desktop shell (`electron/` + React or HTML renderer).

**Spec:** `cursor-patterns/electron-per-monitor-display-scaling.md`

**Exemplar:** `School Scrips/Calendar 2.0`

**Minimum deliverables (required):**

- `displayZoom.ts` — transform scale on `#app-scale-frame`, not `zoom` on `#root`
- `DisplayScaleModal` + **Display** button in title bar (slider 35–100%, Fit, Done)
- A remembered scale in `localStorage` (one global value — not per-monitor by default)
- `initPerMonitorDisplayZoom()` in entry file **before** `createRoot`
- If the app embeds a **BrowserView** under modals: **`freezeForModal({ snapshot: false })`** — PNG snapshots look frozen when Display scale changes

**Optional, build only if Chase asks:** per-monitor auto-memory — `{appSlug}-display-by-monitor`
persistence keyed by monitor id, plus `electron/main.js` + `preload.js` IPC
(`get-active-monitor-info`, `active-display-changed`) to detect and auto-restore a distinct
scale per monitor. Downgraded from required 2026-08-07 — even in Macro App, the exemplar for
this half, it wasn't reliably saving the manual re-adjustment it's meant to save.

New Electron apps: follow `INIT_NEW_APP.md` **Step 4b** for the required part. Do not ship a
new Electron shell without the manual Display button unless Chase opts out explicitly.

---

## Windows: Hidden Launchers (.bat + Node spawn)

**Applies to:** School Scrips apps, App Dashboard, Electron Toolbar hotkey/script launches, and any Windows `.bat` that starts dev servers or Electron.

**Exemplar `.bat`:** `School Scrips/logic-app/launch.bat` (one-liner delegating to the shared dispatcher).

**Full registry + port contract:** `School Scrips/App Dashboard/docs/LAUNCHER.md`.

Chase must **not** see stray `cmd.exe` windows that stay open or kill the app when closed. Use the patterns below — they are **not interchangeable**.

### 1. Per-app `.bat` (double-click or terminal)

**Do not** put npm/electron logic in the app folder. Register the app in `apps.json`, then create a **three-line** launcher:

```bat
@echo off
REM <App name> launcher (<kind> kind). Config: apps.json id "<id>".
call "%~dp0..\App Dashboard\scripts\launch-app-invoke.bat" <id>
exit /b %errorlevel%
```

That chain runs `launch-app.ps1`, which dispatches by `kind` (`chrome-vite`, `electron-vite`, `python-electron`). Hidden dev servers are started inside **`scripts/launch-common.ps1`** → `Start-SchoolDevServerLogged`:

- `Start-Process cmd.exe /c "npm run … >> log 2>&1" -WindowStyle Hidden` (default)
- Output → `%LOCALAPPDATA%\SchoolLaunch\logs\<id>.log` (truncated each launch)

**Never** use `cmd /k` in production launchers — `/k` keeps the window open.

### 2. Node `child_process.spawn` from Electron (Dashboard or Toolbar)

When an Electron host launches `npm run electron:dev` directly (Dashboard **Launch** button, Toolbar **Shift+F5** for `electron-vite`):

| Option | Value | Why |
|--------|-------|-----|
| `stdio` | `['ignore', 'pipe', 'pipe']` | Redirected stdio → **no visible console** |
| `windowsHide` | `false` for `electron-vite` | `true` (= `CREATE_NO_WINDOW`) can **block the Electron window** |
| `detached` | `false` | `detached: true` + visible cmd → orphan window; **closing it kills the app** |
| `shell` | `false` | Run `cmd.exe /d /s /c "npm run …"` on Windows (never spawn `npm.cmd` with `shell: false`) |

**Exemplars:** `App Dashboard/electron/processManager.ts` → `spawnNpmScript(..., windowsHide: false)`; `electron-toolbar/electron-app/src/school-app-spawn.js` → `spawnNpmDev`.

For **`chrome-vite`** / **`python-electron`** from Toolbar (no in-process npm spawn), use hidden **`launch-app.ps1`** (`-WindowStyle Hidden` on the outer PowerShell, `stdio: 'ignore'`, `windowsHide: true` on that wrapper only).

### 3. App Dashboard’s own `launch.bat` (orchestrator)

Dashboard root launchers are special: they run **`node scripts\dev.mjs`** via `start` (see `launch.bat`, `launch-from-toolbar.bat`). Toolbar variant uses `start /min` for the Node console; Electron still opens visibly. Do **not** wrap this in hidden PowerShell `Start-Process` — that broke paths with spaces and hid Electron.

### Critical distinction (Windows)

| Mechanism | Effect |
|-----------|--------|
| PowerShell `Start-Process -WindowStyle Hidden` | Hides **cmd**; safe for npm when output is redirected to a log file |
| Node `windowsHide: true` | Sets **`CREATE_NO_WINDOW`** on the spawned process — OK for taskkill/Python; **avoid on electron-vite parent cmd** |
| Node `detached: true` + visible cmd | **Anti-pattern** — user sees a console; closing it terminates the child tree |

### Debug environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `SCHOOL_LAUNCH_SHOW_DEV_WINDOW` | unset (hidden) | `1`/`true` = visible `cmd /k`; `min` = minimized |
| `SCHOOL_LAUNCH_SUCCESS_DELAY_SEC` | `5` | Pause after successful `launch-app.ps1`; use `0` from hotkeys |
| `SCHOOL_LAUNCH_EXIT_CMD_ON_SUCCESS` | unset | `1` = close hosting cmd tab after success |
| `SCHOOL_LAUNCH_VERBOSE` | unset | `1` = extra probe logging |

### Checklist — new School Scrips app

1. Add row to `App Dashboard/apps.json` (`id`, `kind`, `cwd`, ports, etc.).
2. Add one-liner `launch.bat` (template above).
3. Run `npm run audit:launch-registry` from App Dashboard.
4. If Toolbar should expose it: `TOOLBAR_TO_APPSJSON` in `electron-toolbar/electron-app/src/school-launchers.js`.
5. Tail logs: `Get-Content -Wait "$env:LOCALAPPDATA\SchoolLaunch\logs\<id>.log"`.

---

## Development Phases

Code quality requirements differ by phase. Don't add 9/10 polish to rough-draft
code, and don't ship rough-draft code as final.

| Phase | Focus | Skip For Now |
|-------|-------|--------------|
| **Rough Draft** | Working code, decent structure | Tests, full docs, env config |
| **Polish** | Edge cases, error messages, cleanup | Tests (if not changing behavior) |
| **Final Build** | Tests, docs, env config, error boundaries | Nothing |

### Rough Draft (Getting It Working)
- Follow DRY, Single Responsibility, naming conventions
- Type hints on function signatures
- Extract constants (no magic numbers)
- Basic error handling
- Input validation at API boundaries
- Consistent API response shapes
- **Skip:** Full test coverage, full docstrings, env vars, deep edge cases

### Polish (Almost Done)
- Handle edge cases found during development
- Improve error messages with context
- Clean up shortcuts taken in rough draft
- All API calls through service layer
- Extract magic strings to constants

### Final Build (Ready to Ship)
See [Final Build Checklist](#final-build-checklist).

---

## File Size Enforcement (CRITICAL)

**This is the most violated rule. Follow it strictly.**

### Hard Limits

| Limit | Action |
|-------|--------|
| **800 lines** | HARD MAX — NO EXCEPTIONS |
| **700 lines** | Extract immediately, no questions |
| **500 lines + adding 50+ lines** | Ask the user before adding |
| **100+ line addition** | Extract immediately |

### Before Adding ANY Code

```
1. Read the target file
2. Report the current line count: "File X is currently Y lines"
3. Estimate addition size
4. Calculate final size: "Adding ~Z lines → file will be ~(Y+Z) lines"
5. Check against limits → STOP if needed
6. Ask user or extract BEFORE coding
```

### Mandatory Approval Required If:
- File is > 500 lines AND adding > 50 lines
- File would exceed 800 lines
- Adding a modal/dialog/form (typically > 100 lines)
- Adding a major feature (> 150 lines)

**STOP. DO NOT CODE. ASK:**
> "File X is Y lines. Adding this would make it ~Z lines. Should I:
> (a) Extract to a separate component/file, or (b) Proceed inline?"

### Mandatory Extraction Required If:
- File is > 700 lines
- Addition is > 100 lines
- Adding a reusable component (modal, form, wizard)
- File would exceed 800 lines

**STOP. DO NOT CODE. PROPOSE:**
> "File X is Y lines. This addition requires extraction. Proposed:
> Create [new file path] with [description]. Proceed?"

### Where to Extract

| Adding | Goes To |
|--------|---------|
| Modal/Dialog | `components/modals/[Name]Modal.tsx` (use `max-w-md`) |
| Form | `components/forms/[Name]Form.tsx` |
| Complex UI block | `components/shared/[Name].tsx` |
| State logic | `hooks/use[Name].ts` |
| Business logic | `services/[name]Service.ts` |
| Pure utilities | `utils/[name]Utils.ts` |
| Constants | `[name]Constants.ts` or `*_constants.py` |

### After a Violation

If the user catches a violation:
1. Apologize and acknowledge: "File X was Y lines, I added Z → now (Y+Z) lines."
2. Extract immediately to the right destination
3. Add a proper file header to the new file
4. Update imports
5. Report: "Extracted X lines to [path]. File Y is now Z lines."

### Enforcement Rule (AI Sessions)

If you are asked to edit a file that is **already over 800 lines**, you MUST
refactor it first before making the requested change — this is not optional.
If the refactor is larger than the session allows, stop and surface it:

> "File X is already Y lines (over the 800-line cap). I need to extract
> [seam] before adding anything new. This refactor will take [estimated scope].
> Should I do that first, or would you like to handle it separately?"

Do NOT silently add to an over-cap file. The cap rule exists because AI
sessions are the main way files grow past it.

---

## Grep Before Adding (CRITICAL)

**The single biggest source of "things stopped fitting together" in this tree.**

Each fix or feature is locally cheaper to solve by *adding a new mechanism*
than by reading the existing one well enough to extend it. Over months, this
produces parallel solutions to the same problem — three URL resolvers, two
logging hooks, four activation paths, dead-code hooks left in place because
the new one was easier to write than to delete the old one. The codebase
slowly becomes a museum of "what we tried." Symptoms the user feels:
"introducing new things keeps breaking unrelated things," "diagnosing
anything is harder than it used to be," and the dreaded "this doesn't fit
into the system."

### The Rule

Before creating ANY of the following, grep the codebase (and the sister apps
listed in the app's `CLAUDE.md`) for what it would replace:

- A new custom hook
- A new utility function or `utils/` file
- A new service or service method
- A new IPC channel or preload surface
- A new log helper, log channel, or log buffer
- A new state store, context, or persistence key
- A new partition, slot, registry, or routing map
- A new "manager," "orchestrator," "controller," "session," or "coordinator"
- A new pattern for solving a problem the app already solves somewhere

**This rule also applies to small repeated shapes, not just large mechanisms.**
The third copy of any `try { localStorage.setItem } catch {}`, any
`def _log(message): print(message, flush=True)`, or any
`function resolveX() { /* same 20-line probe */ }` is the moment to write
the shared helper — not the moment to shrug and copy-paste once more. Small
skeletons diverge silently: when the algorithm changes, one copy gets updated
and three don't. The symptom is "grades land in the wrong folder with no error."

### The Grep Checklist (60 seconds)

```
1. The verb / domain noun:    grep "warmup" / "slot" / "logger" / "fetch courses"
2. The scope prefix:          grep for the bracketed log tag, e.g. "[Browser"
3. The hook name pattern:     ls hooks/use*<Topic>*.ts
4. The IPC channel namespace: grep for the channel root, e.g. "browserView:"
5. The sibling file:          read the file next to where you'd add it
```

If anything turns up, READ IT before deciding to add new. The existing one
may already do 80% of what you need.

### If You Decide To Add Anyway

State it in your response, plainly:

> "I considered extending [existing file/function] but chose to add
> [new file/function] because [specific reason — different shape, different
> lifecycle, different consumer, etc.]. The two will need to be reconciled
> later if [condition]."

This is not bureaucracy. It is the only signal the user has that the
duplication was a choice and not an oversight. Without it, every parallel
mechanism looks identical to the user — a thing nobody noticed was already
there.

### What Counts as "Extending"

- Adding a parameter or option to an existing function — yes
- Adding a new exported function in the same file with shared helpers — yes
- Adding a new case to an existing switch / registry / map — yes
- Adding a new branch inside an existing hook that exposes the new behavior — yes
- Copying the existing function and modifying it — **no, this is parallel**
- Creating a new file that imports nothing from the existing one — **no, this is parallel**

### Examples Of What Parallel Mechanisms Look Like

These are abstract — the specific instances live in app `docs/`:

- Two hooks subscribed to the same IPC channel, producing two log buffers.
- Three functions that resolve the "config for X" — one in a registry, one
  in a util, one inlined in a hook — all returning the same shape, none
  calling each other.
- A `useFooWarmup` hook that no file imports, sitting next to a
  `useFooLoader` hook that does the same job.
- Two markdown docs describing the same subsystem with different mental models.
- Four code paths that all call `activateThing(id)`, none of them aware of
  the others, racing on first paint.

If you spot one of these *adjacent* to your change, flag it for the user.
Don't fix it inline (that violates "Preserve existing behavior") but
mention it so they can decide.

### Why This Sits Beside File Size

File size catches *one file* growing past readability. This rule catches
the *codebase* growing past coherence. They are the same failure mode at
different scopes.

---

## Document the Lesson (CRITICAL)

**The failure mode this prevents:** AI removes code that "looks
redundant," the code was a fix for a bug nobody documented, the bug
returns, AI eventually re-derives the same fix. The cycle costs you the
user's time on every refactor pass.

**The rule:** When a session retires multiple band-aids, fixes a class
of bugs, or restructures a subsystem, write a
`docs/<subsystem>_INTEGRATION.md` next to the affected code. The
reasons code exists must live in the repo, not in your head.

### The Exemplar

**`School Scrips/Macro App/docs/BROWSER_TAB_INTEGRATION.md`** is the
canonical example. Read it before writing your own. Its shape is what
"good" looks like — not its specific content.

### Required sections

A doc that fulfills this rule must include all five:

1. **One-page mental model.** ASCII or mermaid showing the layers and
   how they connect. Reader should grok the subsystem in 30 seconds.
2. **Symptom → root-cause → fix-location table.** One row per bug class
   the refactor fixed. Names the file and the function. Future AI
   reading any of those files sees the symptom that would return if the
   fix is removed.
3. **Anti-patterns ("what burned us") section.** Numbered list of
   things that look correct but break the system, with the bug each
   one previously caused. This is the section that stops re-derivation.
4. **Key-files index.** Table mapping concern → file path, so AI edits
   stay within boundaries.
5. **Reusable method.** A Phase 0–N checklist for the *next* instance
   of the same problem class (e.g. "next browser-tab feature," "next
   automation surface"). Generalizes the lesson.

Optional but valuable: a "minimal template" snippet showing how to
copy-paste the structure for the next similar feature.

### When the rule fires

Write the doc when **any** of these are true:

- You retired 3+ guard refs / band-aids in one session.
- You fixed a deadlock, race, or "intermittent" bug whose root cause
  was non-obvious.
- You restructured a subsystem (collapsed parallel mechanisms, added a
  single source of truth, split a god-file into named owners).
- The session log entry would naturally include phrases like "we
  finally figured out why" or "had to redo this several times."

If your session log already explains *why* certain code now exists, the
doc is just that explanation reorganized for the next reader.

### Where the doc lives

- Subsystem-scoped: `<app>/docs/<SUBSYSTEM>_INTEGRATION.md` (Macro App
  exemplar pattern).
- Cross-cutting (e.g. "embedded browser modals"): same place, broader
  name.
- Not in `docs/plans/` — plans describe future work; integration docs
  capture executed lessons.

### What this is NOT

- Not a session log. SESSIONS.md tells you *what* was done.
  INTEGRATION.md tells you *why* the resulting code is shaped this way.
- Not a tutorial. Reader is assumed to be an AI or developer about to
  touch the subsystem.
- Not generated at every commit. Fire the rule for *focused* refactors
  and hotfixes, not for ordinary feature work.

### Why this sits beside Grep Before Adding

§8 prevents you from creating parallel mechanisms because you didn't
know the existing one was there. §9 prevents the next person from
deleting your mechanism because they didn't know *why* it was there.
They are the two halves of "the codebase remembers what we learned."

---

## Entry File as Orchestrator

**The entry file is an orchestrator, never an implementer** — whatever it's called for the
stack in use: `App.tsx` (React), `main.py` (Python), `index.js` (Node). Target: under 100
lines, ideally under 50.

### Entry File Responsibilities
- Wire the pieces together and hand off to them
- Own top-level state/mode if nothing else owns it (React: which view is active; Python:
  which subcommand or mode was requested)
- That's it.

### Correct App.tsx (React)
```typescript
import MainMenu from '@/app/components/MainMenu';
import Tutorial from '@/app/components/Tutorial';

export default function App() {
  const [view, setView] = useState<'menu' | 'tutorial'>('menu');

  return (
    <div className="h-screen w-screen overflow-hidden">
      {view === 'menu' && <MainMenu onStart={() => setView('tutorial')} />}
      {view === 'tutorial' && <Tutorial onBack={() => setView('menu')} />}
    </div>
  );
}
```

### Correct main.py (Python)
```python
from module_a import run_module_a
from module_b import run_module_b
from cli_args import parse_args

def main():
    args = parse_args()
    if args.mode == "a":
        run_module_a(args)
    else:
        run_module_b(args)

if __name__ == "__main__":
    main()
```

### What Does NOT Belong in the Entry File
- The actual work of any module — delegate to it
- Business logic (calculations, validations, transformations)
- Detailed UI components (buttons, forms, cards) — React specifically
- API calls or data fetching
- Anything that could be extracted into its own file or function

### When the Entry File Grows Too Large
1. Identify logical sections (menu, tutorial, module A, module B, etc.)
2. Extract each to its own component / function / module
3. Import and call or render from the entry file
4. Pass necessary props / arguments

---

## File and Module Organization

### React/TypeScript App Layout

```
src/
├── app/
│   ├── App.tsx                 # Orchestrator only
│   └── components/
│       ├── modals/             # Modal dialogs
│       ├── wizards/            # Multi-step wizards
│       ├── shared/             # Reusable UI components
│       └── [Feature].tsx       # Feature-specific components
├── hooks/                      # Custom React hooks (state)
├── services/                   # API calls, business logic
├── utils/                      # Pure utility functions (no hooks)
├── types/                      # TypeScript type definitions
├── styles/                     # Global CSS
└── main.tsx                    # Entry point
```

### Python Module Layout

Each module should have a consistent structure:

```
module_name/
├── module_name.py        # Main logic
├── module_constants.py   # All constants / magic numbers
├── module_state.py       # State class with locking (if needed)
└── module_helpers.py     # Utility functions (if needed)
```

### Should I Create a New File?

```
Is it a modal/dialog?       → Yes: components/modals/MyModal.tsx
Is it state management?     → Yes: hooks/useMyState.ts
Is it a pure function?      → Yes: utils/myUtils.ts
Is it API/business logic?   → Yes: services/myService.ts
Is it a multi-step wizard?  → Yes: components/wizards/MyWizard.tsx
None of the above           → Keep in current component
```

### Proactive File Splitting

When adding a new component or handler to an existing file:
- Check the current line count first
- If the file is already over 300 lines, extract the new addition as its own
  file instead of appending
- Named inline functions (e.g., `function ScoreBar()`, `function ExplanationModal()`)
  are the primary signal — each is a candidate for its own file
- Any function/component with its own props interface that could be imported
  *should* be imported

---

## Core Principles

### 1. DRY — Don't Repeat Yourself
- If you write similar code twice, extract it into a function
- Before writing new code, check if something similar already exists. For
  hooks, utilities, services, IPC channels, log helpers, or any
  *mechanism* (not just a line of code), this is mandatory — see
  [Grep Before Adding](#grep-before-adding-critical).

### 2. Single Responsibility
- Each function does ONE thing
- Each module has ONE purpose
- If a function needs "and" to describe it, split it

### 3. Keep It Simple
- Prefer simple over clever
- Don't add features that weren't requested
- Don't add "just in case" flexibility

### 4. Fail Fast
- Validate inputs at the start of functions
- Return early for edge cases
- Don't nest deeply — use guard clauses

```python
# BAD - deeply nested
def process(data):
    if data:
        if data.is_valid:
            if data.has_items:
                return result
    return None

# GOOD - guard clauses
def process(data):
    if not data:
        return None
    if not data.is_valid:
        return None
    if not data.has_items:
        return None
    return result
```

### 5. Preserve Existing Behavior
- Don't refactor unrelated code
- Don't rename things outside scope
- Don't "improve" things you weren't asked to improve

---

## Naming Conventions

### Python
```python
class MyClassName:          # PascalCase for classes
    CONSTANT_VALUE = 100    # UPPER_SNAKE_CASE for constants
    _private_var = None     # Leading underscore for private

    def my_function_name(self, param_name: str) -> bool:  # snake_case
        local_variable = "value"
```

### JavaScript/TypeScript
```typescript
class MyClassName {}           // PascalCase for classes
const CONSTANT_VALUE = 100;    // UPPER_SNAKE_CASE for constants
let myVariableName = "";       // camelCase for variables
function myFunctionName() {}   // camelCase for functions
```

### Files
- Python: `snake_case.py`
- TypeScript components: `PascalCase.tsx`
- TypeScript utilities: `camelCase.ts`
- Constants files: `*Constants.ts` or `*_constants.py`

### State and Handlers (React)
- State: `[name]`, setter: `set[Name]`
- Handlers: `handle[Action]`
- Boolean states: `is[State]`, `show[Thing]`, `has[Thing]`
- Custom hooks: `use[Name]`

---

## Function Guidelines

- **Max length:** 50 lines (split if longer)
- **Acceptable:** 30-50 lines for complex linear logic
- **Hard limit:** 100 lines — no exceptions
- **Parameters:** 1-3 ideal, 5 max (use config object/dataclass if more)

---

## React Patterns

### When to Extract a Custom Hook

| Condition | Action |
|-----------|--------|
| 3+ related useState calls | Extract to custom hook |
| State used across components | Extract to shared hook |
| Complex initialization | Extract to custom hook |
| State + computed values | Extract to custom hook |
| Component > 300 lines | Extract state to hook |
| 5+ useState in one component | Extract to hook |

### Hook Naming

```typescript
// State management hooks
useModalState.ts          // Manages modal visibility
useCalendarData.ts        // Manages calendar content
useClassManagement.ts     // Manages class operations

// Handler orchestrators
useAddClassHandlers.ts    // Orchestrates workflow
useImportHandlers.ts

// Effect hooks
useAppEffects.ts          // Window listeners, server checks
```

### State Extraction Example

```tsx
// BEFORE: 450-line component with 12 useState calls
export default function MyComponent() {
  const [value1, setValue1] = useState('');
  const [value2, setValue2] = useState(false);
  // ... 10 more
  // 350 more lines of JSX and logic
}

// AFTER: hooks/useMyComponentState.ts
export function useMyComponentState() {
  const [value1, setValue1] = useState('');
  // ... all state and handlers

  return {
    values: { value1, value2, ... },
    ui: { loading, error },
    modals: { modal1Open, ... },
    setValue1,
    handleAction1,
  };
}

// Component now just renders UI (150 lines)
export default function MyComponent() {
  const { values, ui, modals, setValue1, handleAction1 } = useMyComponentState();
  return (/* clean UI */);
}
```

### Service Layer

All API calls go through a service layer for centralized error handling,
testing, type safety, and reusability.

```typescript
// ❌ WRONG — direct fetch in component
const handleSave = async () => {
  const response = await fetch('/api/save', { method: 'POST', ... });
};

// ✅ CORRECT — service layer
import { saveResource } from '../services/resourceService';

const handleSave = async () => {
  const result = await saveResource(data);
  if (!result.success) setError(result.error);
};
```

#### Service File Template

```typescript
export interface ApiResponse<T = any> {
  success: boolean;
  error?: string;
  data?: T;
  logs?: string[];
}

export async function fetchResources(): Promise<ApiResponse<MyResource[]>> {
  try {
    const response = await fetch('/api/resources');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return { success: true, data: await response.json() };
  } catch (error) {
    console.error('[Service] Fetch failed:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}
```

### Import Order

```typescript
// 1. React core
import React, { useState, useEffect, useRef } from 'react';

// 2. Third-party UI libraries (alphabetical)
import { Button } from '@radix-ui/react-button';
import { Moon, Sun } from 'lucide-react';

// 3. Internal utilities
import { API_BASE_URL } from '../config';
import { logger } from '../utils/logger';

// 4. Internal services
import { saveData } from '../services/dataService';

// 5. Internal hooks
import { useModalState } from '../hooks/useModalState';

// 6. Internal components
import { Sidebar } from './Sidebar';

// 7. Types
import type { CalendarMode } from '../types/calendar';

// 8. Styles (always last)
import './MyComponent.css';
```

### Python Import Order

```python
# Standard library
import os
import sys
from typing import Optional, List, Dict

# Third-party
import pyautogui
from screeninfo import get_monitors

# Local
from shared.signals import signals
from module_constants import TIMEOUT
```

---

## Modal Pattern

**⚠️ COMMON MISTAKE:** Modals that span the entire screen because of
`w-full` without a `max-w-*`, or `max-w-3xl` / `max-w-4xl` / `max-w-6xl`.

### Standard Modal Sizing

| Modal Type | Max Width | Use Case |
|------------|-----------|----------|
| Confirmation | `max-w-md` (448px) | Yes/No dialogs |
| Form | `max-w-md` (448px) | Single-column forms |
| Wizard | `max-w-lg` (512px) | Multi-step wizards |
| Complex wizard | `max-w-xl` (576px) | Rare — only if necessary |

**NEVER:** `max-w-2xl`, `max-w-3xl`, `max-w-4xl`, `max-w-6xl`, or `w-full`
without a max-width.

**Always:** `max-h-[85vh]` for height; `overflow-y-auto` on content area.

**Never dismiss on overlay click.** Do not put `onClick={onClose}` on the
backdrop. The user must use an explicit button (OK, Cancel, Close). Required
for dwell-mouse accessibility. See `cursor-patterns/modal-pattern.md`.

### Correct Modal

```tsx
<ModalPortal>
  <div className="fixed inset-0 z-50 flex items-center justify-center">
    <div
      className="w-full max-w-md max-h-[85vh] rounded-lg border shadow-xl overflow-hidden flex flex-col"
      onClick={(e) => e.stopPropagation()}
    >
      <div className="flex items-center justify-between p-4 border-b">
        <h2>Modal Title</h2>
        <button onClick={onClose}><X /></button>
      </div>
      <div className="flex-1 overflow-y-auto p-6">
        {/* content */}
      </div>
    </div>
  </div>
</ModalPortal>
```

Always use `ModalPortal` to ensure proper z-index stacking.

See `modal-pattern.md` for the full template.

---

## File Headers

File headers are the FIRST thing AI reads when opening a file. They prevent
breaking changes, document invariants, and speed up onboarding.

### When to Add a Header
- All new TypeScript/JavaScript files
- All Python modules
- Any extracted file (refactoring output)

### Standard Header (TypeScript)

```typescript
/*
===============================================================================
FILE: useDrawerHover.ts

MODULE ROLE:
Custom React hook managing drawer hover with delay timers and cooldown.

WHY THIS FILE EXISTS:
Extracted from Sidebar.tsx during refactoring to reduce file size.
Hover logic with multiple timers was tangled with sidebar UI code.

PUBLIC API (STABLE):
- useDrawerHover(OPEN_DELAY, CLOSE_DELAY, COOLDOWN, LOCK_DURATION)
  Returns: { openActionPanel, drawerPosition, scheduleOpen, cancelOpen, ... }

INPUTS / OUTPUTS:
- Input: Delay configurations (milliseconds)
- Output: State and control functions for drawer behavior

SIDE EFFECTS:
- Creates/clears setTimeout timers
- Updates state triggering re-renders

INVARIANTS (MUST REMAIN TRUE):
- Timers must be cleaned up to prevent memory leaks
- Lock period must complete before allowing close (accessibility)
- Only one timer of each type should exist at a time

SAFE TO MODIFY:
- Default delay values (currently 500ms)
- Timer duration calculations

FRAGILE / HIGH-RISK AREAS:
- Timer cleanup logic — ensure all refs are cleared
- Lock period enforcement — critical for dwell-mouse accessibility

LAST VERIFIED: 2026-01-10
===============================================================================
*/
```

### Short Header (Components)

```typescript
/**
 * FILE: src/components/Sidebar.tsx
 *
 * PURPOSE: Main sidebar with class list and management drawer.
 *
 * SAFE TO MODIFY: Drawer timings, styling.
 * FRAGILE: Drawer positioning uses getBoundingClientRect() + createPortal.
 *
 * LAST VERIFIED: 2026-01-20
 */
```

See `file-headers.md` for the Python template and full examples.

---

## Input Validation

Always validate at system boundaries (API endpoints, public functions, CLI args,
file/config loaders, user input). Don't validate inside trusted internal code.

### What to Check
1. **Existence:** Is the required field present?
2. **Type:** Is it the expected type?
3. **Format:** Does it match expected patterns?
4. **Range:** Is it within acceptable bounds?

### Python Example

```python
def process_class(drive: str, class_name: str) -> dict:
    if not class_name or not isinstance(class_name, str):
        return {"success": False, "error": "Class name is required"}
    if not class_name.strip():
        return {"success": False, "error": "Class name cannot be empty"}
    if drive and not re.match(r'^[A-Za-z]$', drive):
        return {"success": False, "error": "Drive must be a single letter"}
    # ... proceed
```

### Validation Response

```python
# Good - clear, actionable
return {"success": False, "error": "Class name is required"}

# Bad - generic
return {"success": False, "error": "Invalid input"}

# Bad - exposes internals
return {"success": False, "error": "TypeError: cannot read property 'trim' of undefined"}
```

---

## API Response Shape

All API endpoints return the same shape:

```typescript
interface ApiResponse<T = any> {
  success: boolean;
  error?: string;      // Only when success=false
  data?: T;            // Only when success=true
  logs?: string[];     // Optional progress/debug messages
}
```

### Response Helper Pattern

```javascript
function apiResponse(res, { success, error = null, ...data }) {
  res.json({ success, error: success ? null : error, ...data });
}

app.post('/api/something', (req, res) => {
  if (!valid) return apiResponse(res, { success: false, error: 'Invalid' });
  apiResponse(res, { success: true, items: results });
});
```

---

## Error Handling

### Do

```python
try:
    result = risky_operation()
except SpecificError as e:
    print(f"[MODULE] Operation failed: {e}")
    return default_value
```

### Don't

```python
try:
    result = risky_operation()
except:  # BAD — catches KeyboardInterrupt too
    pass  # BAD — silently ignores
```

### Silent Failures Are Bugs

```python
# BAD — error happens, nobody knows
try:
    result = parse_config()
except Exception:
    result = {}

# GOOD — log, then handle
try:
    result = parse_config()
except Exception as e:
    print(f"[CONFIG] Failed to parse: {e}, using defaults")
    result = get_default_config()
```

---

## Logging

### Levels

- **INFO:** State changes, important events (startup, shutdown, mode changes)
- **DEBUG:** Detailed flow for troubleshooting
- **WARNING:** Unexpected but handled
- **ERROR:** Failures needing attention

### Format

```python
print(f"[MODULE_NAME] Event description: {relevant_data}")

# Examples:
print("[DWELL] Mode switched to Mode 2")
print(f"[SCROLL] Position updated: x={x}, y={y}")
print(f"[SIGNAL] Error connecting: {e}")
```

### Don't
- Log in tight loops
- Log sensitive data
- Use bare `print()` without module prefix

---

## Anti-Patterns to Avoid

### Code Organization
- **God files (1000+ lines)** → Split into modules
- **Magic numbers** (`if x > 47:`) → Named constants
- **Inconsistent module structure** → Follow the module template

### State Management
- **Scattered global state** → Use a state class with locking
- **Unprotected shared state** → Add threading locks
- **Prop drilling 3+ levels** → Context or custom hook

### Error Handling
- **Bare `except:`** → Catch specific exceptions
- **Silent failures** → Log then handle

### Communication
- **File-based IPC** (polling text files) → Socket-based signals
- **Hardcoded paths** → Use `Path(__file__).parent` or env vars
- **Polling too fast** (1000/sec) → Reasonable intervals (100/sec)

### React Specific
- **Direct fetch in components** → Service layer
- **15 useState in one component** → Extract to custom hook
- **`max-w-3xl` modals** → `max-w-md`
- **Modals without ModalPortal** → Use the portal

See `anti-patterns.md` for full examples.

---

## Secrets & Configuration

### Never Commit
- API keys, tokens, passwords
- Private keys, certificates
- Connection strings with credentials
- `.env` files with real values

### Use Environment Variables

```python
import os
API_KEY = os.environ.get("API_KEY")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
```

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
```

### .gitignore Essentials

```
.env
.env.local
*.pem
*_secret*
credentials.json
node_modules/
__pycache__/
*.pyc
dist/
build/
```

---

## Final Build Checklist (9/10 Quality)

> Use this when the user says "final build", "ready to ship", or "make it 9/10".
> Skip during rough draft and polish phases.

### 1. Tests
- [ ] Complex logic with multiple branches has tests
- [ ] Public API functions have tests
- [ ] Edge cases discovered during dev have tests
- [ ] Bug fixes have regression tests (write the test FIRST)

### 2. Environment Configuration
- [ ] No hardcoded URLs (`localhost:5000`, etc.)
- [ ] No absolute paths (`C:\`, `/Users/`)
- [ ] All config via environment variables
- [ ] `.env.example` committed; `.env` in `.gitignore`

### 3. State Management (React)
- [ ] No component > 300 lines with 5+ useState
- [ ] State extracted to custom hooks where needed

### 4. CLI Refactoring (Python)
- [ ] No `main()` over 100 lines
- [ ] CLI logic extracted to testable functions
- [ ] `main()` is < 50 lines and only orchestrates

### 5. Documentation
- [ ] Docstrings on complex functions
- [ ] JSDoc on service functions
- [ ] README has install + env setup
- [ ] File headers on all major files

### 6. Error Handling
- [ ] ErrorBoundary wraps main app (React)
- [ ] Error messages explain what went wrong AND how to fix
- [ ] No exposed internals in error messages

### 7. API Consistency
- [ ] All API calls through service layer
- [ ] All endpoints return `{ success, error?, data? }`

### 8. Quality Pass
- [ ] No TypeScript/ESLint errors
- [ ] No unused imports or variables
- [ ] No `console.log` debug statements left in
- [ ] No commented-out code (git has history)

---

## When to Break the Rules

These are guidelines, not laws. Acceptable deviations:

| Rule | When to Break It |
|------|------------------|
| Functions < 50 lines | An 80-line function with clear linear flow beats 4 fragmented helpers |
| Extract duplicate code | If two blocks are evolving independently, duplication may be clearer |
| Constants file | A single magic number used once with a clear comment doesn't need extraction |
| Extract state to hook | A cohesive 350-line component unlikely to be reused may be fine |
| Full test coverage | Prototype/experimental code may not need tests |

### The Test: Readability

Ask: *"If I come back to this in 6 months, will I understand it faster with or
without this rule applied?"*

- If breaking the rule makes it **clearer**, break it
- If following the rule is **mechanical with no benefit**, skip it
- If unsure, **follow the rule** — it exists for a reason

When breaking a rule intentionally, leave a brief comment:

```python
# Note: Keeping as one function — the linear flow is clearer than splitting
def process_submission():
    ...
```

---

## Related Pattern Files

Deep-dives on specific topics. Read these only when relevant to current work.

| File | When to Read |
|------|--------------|
| `INIT_NEW_APP.md` | Scaffolding a new app — variants, folder structure, file templates |
| `react-patterns.md` | Building hooks, services, components |
| `modal-pattern.md` | Building a modal/dialog/wizard |
| `file-headers.md` | Header templates and examples |
| `refactoring-checklist.md` | When the user asks to refactor or clean up |
| `anti-patterns.md` | Full anti-pattern catalog with examples |
| `accessibility-patterns.md` | Hover delays, dwell-mouse support, screen readers |
| `dwell-and-head-mouse.md` | **Source of truth** for any dwell/hover/drag timing value |
| `electron-per-monitor-display-scaling.md` | **Required** Electron shell: Display button, per-monitor scale |
| `School Scrips/App Dashboard/docs/LAUNCHER.md` | Registry, ports, hidden `.bat` chain, Toolbar hotkey |

File size enforcement is covered in full above in this same file — no separate deep-dive needed.

---

## Workflow Contract (For Meaningful Changes)

1. **Plan** — State which files will be modified and why. Check file sizes first.
2. **Implement** — Follow the standards above. Preserve existing behavior.
3. **Verify** — Test functionality. Check for console errors.
4. **Writeback** — If the app has `docs/sessions/SESSIONS.md`, append a dated
   entry. Note any new patterns discovered.

---

**Your goal:** Leave the codebase cleaner, clearer, and more coherent than you
found it. Don't add scope. Don't refactor what wasn't asked for. Don't violate
file size limits. If unsure, ask.
