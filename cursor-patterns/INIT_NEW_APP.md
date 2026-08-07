# Initialize New App — AI Recipe

> **For AI:** When Chase says any of:
> - "Initialize a new app called [name]"
> - "Bootstrap a new [variant] app called [name]"
> - "Set up [name] using the init template"
> - "Start a new app"
>
> Follow this recipe step-by-step. Do NOT skip the clarification questions.

---

## The Recipe (Follow In Order)

### Step 1: Ask 3 Clarifying Questions

Don't start creating anything yet. Ask:

1. **App name and one-line purpose.** Example: "factoring-app — interactive polynomial factoring tutorial."
2. **Variant** — one of:
   - **`educational-math`** — React/Vite/Tailwind teaching tool (like Logic, Transformations, Factoring, Matrix, Probability, Fractions)
   - **`functional-tool`** — utility app, may be full-stack or have a Python backend (like Makeup Exam, D2L Platform, Macro)
   - **`electron-overlay`** — Python + Electron overlay with dwell-mouse accessibility (like electron-toolbar)
   - **`custom`** — describe the stack
3. **Where to create it.** Default: `C:\Users\chase\Documents\Programs\School Scrips\[app-name]\` for school apps, `C:\Users\chase\Documents\Programs\[app-name]\` for tools.

### Step 2: Confirm The Plan

Before creating ANYTHING, summarize back:

> "I'll create `[path]` as a `[variant]` app. Stack: [stack]. Files: CLAUDE.md, README.md, guidelines/Guidelines.md, docs/sessions/SESSIONS.md, .cursorrules, .gitignore, [variant-specific configs]. Proceed?"

Wait for "yes" before doing anything.

### Step 3: Create Folder Structure

Use the variant-specific structure from the [Variants](#variants) section below.

### Step 4: Write Files

Use the templates from the [File Templates](#file-templates) section. Fill in the
`[bracketed]` placeholders with the actual app name, variant, purpose, etc.

### Step 4b: Electron shell — Display scaling (REQUIRED; per-monitor memory is optional)

If the app includes an **Electron** desktop shell (`electron/main.js` or `electron-app/`
+ a React/Vite or HTML renderer), you **must** implement the manual Display scale button
**before** calling the app "done" for first scaffold. Automatic **per-monitor** memory
(detecting which monitor and auto-restoring a distinct remembered scale) is **optional** —
build it only if Chase asks. See `electron-per-monitor-display-scaling.md`'s 2026-08-07 note
for why: even Macro App's version of it wasn't reliably saving him a re-adjustment.

1. Read **`cursor-patterns/electron-per-monitor-display-scaling.md`** (full spec + checklist).
2. **Exemplar:** copy/adapt from `School Scrips/Calendar 2.0` (see file table in that doc).
3. Set `STORAGE_KEY` in `displayZoom.ts` to `{appSlug}-display-scale` (one global value —
   only use `{appSlug}-display-by-monitor` if building the optional per-monitor Phase 3).
4. Add a title-bar **Display** button opening a slider modal (35–100%, Fit to window, Done; no backdrop dismiss).
5. Wire `initPerMonitorDisplayZoom()` + `initManualZoom()` in `main.tsx` before `createRoot`.
6. **Optional (skip unless asked):** add IPC in main/preload (`get-active-monitor-info`, `active-display-changed`) for per-monitor auto-memory.
7. Mention in the app’s `CLAUDE.md` and `guidelines/Guidelines.md` that Display scaling is standard for this app.

**Do not** use CSS `zoom` on `#root` or auto-scale on load. **Do** use `#app-scale-frame` + `transform: scale`.

**Embedded BrowserView:** If the app hides the browser and shows a **snapshot image** under modals, use **`freezeForModal({ snapshot: false })`** (and default snapshot to off). Otherwise Display rescaling looks like the browser is not updating. See the “Embedded browser + modal freeze snapshots” section in `electron-per-monitor-display-scaling.md`.

Skip the whole step only if Chase explicitly says the app is not Electron or opts out of Display scaling.

### Step 4c: Embedded browser — pin Electron to Macro App (REQUIRED)

If the new app embeds a native browser (`WebContentsView`, Macro-style bounds IPC, CDP
remote debugging for automation), **before** writing `package.json` or `browser-view.js`:

1. Read **`School Scrips/Macro App/package.json`** → copy the **`electron`** devDependency version (currently **`^42.2.0`**).
2. Put **that same version** in the new app’s `package.json`. Do **not** copy Electron from Video Player, Calendar 2.0, or electron-toolbar — those apps use **28.x** and do not use `WebContentsView`.
3. Exemplar for browser code: **`School Scrips/Macro App/electron-app/`** (not Video Player).
4. In the new app’s `CLAUDE.md`, state the pinned Electron version and that embedded-browser apps must stay aligned with Macro App’s generation.

**Why:** `WebContentsView`, `contentView.addChildView`, and `navigationHistory` require **Electron 30+**. Mixing Macro browser code with Electron 28 crashes at runtime (`navigationHistory` undefined, `setBounds is not a function`).

**Programs reality:** Electron versions are **not** unified repo-wide (28 / 33 / 42 coexist). Only apps that **share Macro’s embedded browser** must match Macro’s pin. Simple shells without embedded browser may stay on an older sister app’s version until a deliberate upgrade.

Skip this step only if the app has no embedded browser.

### Step 5: Install Dependencies (ASK FIRST)

Don't run `npm install` automatically. Ask:

> "Run `npm install` now to install dependencies? (Or want me to leave that for you?)"

### Step 6: Report

Tell Chase:
- What got created (full path)
- What variant
- What to run next (`npm run dev`, port number, etc.)
- Where the AI orientation is (`[app]/CLAUDE.md`)
- Reminder: master coding standards at `cursor-patterns/CODING_STANDARDS.md`
- If Electron: confirm Display scaling (Step 4b) was included or deferred with Chase’s OK
- If embedded browser: confirm Electron version matches Macro App (Step 4c)

---

## Variants

### Variant: `educational-math`

**Stack:** React 18 + Vite + TypeScript + Tailwind CSS + Radix UI

**Defining traits:**
- Mobile-first, landscape orientation
- Tutorial overlay pattern (draggable windows, step-by-step)
- Blue educational color theme
- Interactive math visualizations
- Sister apps to reference: `Logic app`, `transformations-app`, `factoring-app`, `Fractions-App`, `Matrix app`, `Probability App`

**Folder structure:**
```
[app-name]/
├── src/
│   ├── app/
│   │   ├── App.tsx                   # ORCHESTRATOR ONLY (<100 lines)
│   │   └── components/
│   │       ├── MainMenu.tsx
│   │       ├── modals/
│   │       └── ui/
│   ├── hooks/                        # Custom state hooks
│   ├── services/                     # API/business logic (if needed)
│   ├── utils/                        # Pure functions
│   │   └── mathHelpers.ts            # Math utilities
│   ├── types/                        # TypeScript definitions
│   ├── styles/
│   │   └── index.css
│   └── main.tsx                      # Entry point
├── docs/
│   └── sessions/
│       └── SESSIONS.md
├── guidelines/
│   └── Guidelines.md
├── public/
├── CLAUDE.md
├── README.md
├── .cursorrules
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── postcss.config.js
```

**Default Vite port:** Auto-assigned (Vite will pick 5173 or next available).

---

### Variant: `functional-tool`

**Stack:** varies. Ask Chase whether it's:
- React frontend only
- React frontend + Express/Node backend
- React frontend + Python (Flask/FastAPI) backend
- Pure Python CLI
- Electron desktop app

**Defining traits:**
- More backend logic than UI
- Often integrates with external systems (D2L, CSVs, PDFs)
- Sister apps to reference: `makeup-exam-standalone`, `D2L-Assignment-Platform`, `D2L-Macro`

**Folder structure (React + Python backend):**
```
[app-name]/
├── src/                              # Frontend (React)
│   ├── app/
│   │   ├── App.tsx
│   │   └── components/
│   ├── hooks/
│   ├── services/                     # Calls backend API
│   ├── utils/
│   └── main.tsx
├── backend/                          # Python backend
│   ├── api/                          # Flask/FastAPI routes
│   ├── services/                     # Business logic
│   ├── utils/
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
├── docs/
│   └── sessions/
│       └── SESSIONS.md
├── guidelines/
│   └── Guidelines.md
├── CLAUDE.md
├── README.md
├── .cursorrules
├── .gitignore
├── package.json
├── tsconfig.json
└── vite.config.ts
```

If pure Python or Electron, adapt accordingly — ask before scaffolding.

**Electron desktop app:** use the React + `electron/` layout (see Calendar 2.0), include
`electron/`, `src/electron.css`, and complete **Step 4b** (Display scaling) on first scaffold.

---

### Variant: `electron-overlay`

**Stack:** Python (overlay logic) + Electron (window management) + HTML/JS frontend

**Defining traits:**
- Dwell-mouse accessibility is a CORE requirement
- Always-on-top overlay windows
- Click-through where appropriate
- IPC signals between Python and Electron (no file-based polling)
- Sister app to reference: `electron-toolbar` (see `electron-toolbar/ARCHITECTURE_PATTERNS.md` and `electron-toolbar/OVERLAY_MODULE_PATTERN.md`)
- **Electron shell:** per-monitor **Display** scaling is still required for any renderer window Chase resizes on multiple monitors — see **Step 4b** and `cursor-patterns/electron-per-monitor-display-scaling.md` (port from Calendar 2.0 if the overlay uses React/HTML in Electron).

**Folder structure:**
```
[app-name]/
├── modules/                          # Each overlay module is its own folder
│   └── [module_name]/
│       ├── [module_name].py
│       ├── [module_name]_constants.py
│       ├── [module_name]_state.py    # Thread-safe state with locks
│       └── [module_name].html        # Overlay UI (if HTML-based)
├── shared/
│   └── signals.py                    # Socket-based IPC
├── electron-app/
│   ├── main.js
│   └── preload.js
├── docs/
│   └── sessions/
│       └── SESSIONS.md
├── CLAUDE.md
├── README.md
├── ARCHITECTURE_PATTERNS.md          # Module pattern catalog
├── .cursorrules
├── .gitignore
├── main.py
├── package.json
└── requirements.txt
```

---

## File Templates

Fill in `[bracketed]` placeholders. Don't include the brackets in the actual file.

### `CLAUDE.md` (universal — adapt content per variant)

```markdown
# CLAUDE.md — [App Name]

> Auto-loaded by Claude Code in this directory. Cursor: covered by User Rule.

## What This App Is

[1-2 sentences. Example: "React/Vite educational app for teaching students
to identify geometric transformations interactively. Mobile-first landscape."]

## Variant

[educational-math | functional-tool | electron-overlay | custom]

## Read First

Master coding standards:
`C:\Users\chase\Documents\Programs\cursor-patterns\CODING_STANDARDS.md`

## App-Specific Rules

[App-specific things — examples below per variant]

## Sister Apps (Look Here For Patterns)

[Variant-specific list of sister apps]

## Session Log

Append a short entry to `docs/sessions/SESSIONS.md` at session end. Format:
date, files changed, what worked, file-size flags, next session note.
```

**Variant-specific "App-Specific Rules" snippets:**

For `educational-math`:
```
- Stack: React 18 + Vite + TypeScript + Tailwind + Radix UI
- Mobile-first, LANDSCAPE orientation. Show rotation prompt on portrait.
- Blue educational theme (see guidelines/Guidelines.md for palette).
- Tutorial system: draggable overlay window with step-by-step progression.
- All transformation/math math goes in `src/utils/mathHelpers.ts`.
- Button style: "Layered depth" 3D — see Guidelines.md for exact gradient.
- App.tsx is an orchestrator — feature components live in src/app/components/.
```

For `functional-tool`:
```
- Stack: [confirm with Chase — React+Python? React+Express? Pure Python CLI? Electron?]
- API responses ALWAYS use { success, error?, data?, logs? } shape.
- All API calls through service layer (no inline fetch).
- Validate input at API/CLI/function boundaries.
- File path handling: use pathlib (Python) or path.join (Node). Never hardcode "C:\".
- If Electron: per-monitor Display scaling is required — cursor-patterns/electron-per-monitor-display-scaling.md; exemplar Calendar 2.0.
```

For `electron-overlay`:
```
- ACCESSIBILITY-CRITICAL: this app is operated via head-mounted gyroscopic mouse
  with dwell-clicking. UI must have big targets, no hover-only menus.
- Each module is its own folder with: module.py, module_constants.py,
  module_state.py (with locks), and optional module.html.
- IPC: use shared/signals.py (socket-based). NEVER file-polling.
- Python state classes always use threading.Lock(). No raw globals.
- Tkinter operations only on main thread. Use master.after(0, ...) from threads.
- Electron renderer windows: implement per-monitor Display scaling (Step 4b / electron-per-monitor-display-scaling.md).
```

---

### `README.md` (universal)

```markdown
# [App Name]

[1-paragraph description for humans.]

## Stack

- [Framework]
- [Build tool]
- [Other key libraries]

## Setup

\`\`\`bash
npm install
npm run dev
\`\`\`

Dev server: http://localhost:[port]

## Project Structure

See `CLAUDE.md` for the AI orientation and folder layout.

## Development Guidelines

App-specific rules: `guidelines/Guidelines.md`
Global coding standards: `C:\Users\chase\Documents\Programs\cursor-patterns\CODING_STANDARDS.md`

## Build

\`\`\`bash
npm run build
\`\`\`
Output: `dist/`
```

---

### `guidelines/Guidelines.md` for `educational-math`

```markdown
# [App Name] Guidelines

## Design Principles

- **Educational focus:** clear visualizations, step-by-step learning, immediate feedback.
- **Consistency with sister apps:** match Logic, Transformations, Factoring, Matrix.
- **Mobile-first landscape:** safe-area insets, touch-friendly buttons.

## Architecture

**App.tsx is an orchestrator, never an implementer.** Target < 100 lines.

```
src/
├── app/
│   ├── App.tsx                    # Orchestrator
│   └── components/
│       └── [Feature].tsx          # Feature components
├── hooks/                         # State management
├── utils/
│   └── mathHelpers.ts             # All math operations
└── styles/
```

## Color Scheme

- Primary: Blue (educational theme)
- Background: blue-50, white
- Borders: blue-200, gray-300
- Text: blue-900, gray-900
- Highlights: blue-100
- Error: red tones
- Success: green tones

## Button Style — Layered Depth (3D #10)

Primary action buttons:
- Background: `linear-gradient(180deg, #3b82f6 0%, #2563eb 100%)`
- Shadow: `0 1px 0 0 rgba(255,255,255,0.2), 0 2px 0 0 rgba(0,0,0,0.05), 0 4px 0 0 #1e40af, 0 6px 12px -2px rgba(0,0,0,0.2), inset 0 1px 0 0 rgba(255,255,255,0.25)`
- Press: translateY(2px) + flatten shadow

## Animation Timing

- Instant: 0s
- Quick: 0.2s
- Fast: 0.3s
- Normal: 0.5s
- Slow: 0.8s
- Transformation animations: 1-2s

## Tutorial System

- Draggable overlay window
- Step-by-step progression
- "Next" button appears after step action complete
- Exit button always visible
- Pattern reference: Matrix app, Transformations app

## File Size Limits

- Max 800 lines (hard limit)
- Warning at 500 lines
- See `cursor-patterns/CODING_STANDARDS.md` for full rules

## Testing Checklist

Before committing:
- [ ] App runs without console errors
- [ ] All buttons/interactions work
- [ ] Landscape orientation prompt works on mobile
- [ ] Animations smooth
- [ ] Math calculations accurate
```

---

### `guidelines/Guidelines.md` for `functional-tool`

```markdown
# [App Name] Guidelines

## Purpose

[What this tool does in 1 paragraph]

## Architecture

[Describe: frontend stack, backend stack, how they communicate]

## Key Modules

- `[module]`: [what it does]
- `[module]`: [what it does]

## External Integrations

- [System name]: [what we read/write]

## Electron shell (if this app uses Electron)

- Per-monitor **Display** scaling is required on first scaffold.
- Spec: `cursor-patterns/electron-per-monitor-display-scaling.md`
- Exemplar: `School Scrips/Calendar 2.0`
- Title bar **Display** button; slider modal; no backdrop dismiss on Display modal.

## API Response Shape

All endpoints return:
\`\`\`typescript
{ success: boolean, error?: string, data?: any, logs?: string[] }
\`\`\`

## File Size Limits

See `cursor-patterns/CODING_STANDARDS.md` (max 800 lines).

## Testing Strategy

[What gets tested, what doesn't, how to run tests]
```

---

### `guidelines/Guidelines.md` for `electron-overlay`

```markdown
# [App Name] Guidelines

## Accessibility Requirement (Non-Negotiable)

This app is operated by head-mounted gyroscopic mouse + dwell-click. Every UI
must have:
- Large click targets (min 44px, prefer 60px+)
- No hover-only menus or tooltips
- No required typing
- Dwell-friendly buttons (no fast-vanishing UI)

## Module Pattern

Each overlay module is its own folder:
\`\`\`
modules/[name]/
├── [name].py              # Main logic
├── [name]_constants.py    # ALL constants (no magic numbers)
├── [name]_state.py        # Thread-safe state (threading.Lock)
└── [name].html            # Overlay UI (optional)
\`\`\`

## IPC

Use `shared/signals.py` for cross-module communication. Socket-based.
**Never use file-polling.**

## Threading

- Tkinter operations only on main thread. Use `master.after(0, lambda: ...)` from background threads.
- Shared state always behind a lock.
- No raw globals — use a state class with locked accessors.

## Reference

Pattern catalog: `[app]/ARCHITECTURE_PATTERNS.md`
Overlay pattern: `[app]/OVERLAY_MODULE_PATTERN.md` (if applicable)
Master standards: `cursor-patterns/CODING_STANDARDS.md`
```

---

### `docs/sessions/SESSIONS.md` (universal)

```markdown
# Sessions Log — [App Name]

Latest entries at top. Keep each entry to ~10 lines.

**Format:**
- **Files changed:** bullet list with line-count deltas if relevant
- **What worked:** what was accomplished
- **File size flag:** any files now > 500 lines, or growth > 200 lines
- **Next session:** what to pick up

---

## [YYYY-MM-DD] — Initial scaffold

**Files changed:** Project initialized via cursor-patterns/INIT_NEW_APP.md.

**What worked:** Folder structure, configs, guidelines, and AI orientation files created.

**File size flag:** None.

**Next session:** Implement [first feature].

---
```

---

### `.cursorrules` (universal, one-liner)

```markdown
---
alwaysApply: true
---

Read CLAUDE.md in this directory and follow it.
Master coding standards: C:\Users\chase\Documents\Programs\cursor-patterns\CODING_STANDARDS.md
```

---

### `.gitignore` (universal)

```gitignore
# Dependencies
node_modules/
__pycache__/
*.pyc
venv/

# Build
dist/
build/
*.tsbuildinfo

# Environment
.env
.env.local
*.pem
credentials.json
config.local.json

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

---

### `package.json` for `educational-math`

```json
{
  "name": "[app-name-kebab]",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react-swc": "^3.7.1",
    "typescript": "^5.6.3",
    "vite": "^5.4.10",
    "tailwindcss": "^3.4.14",
    "postcss": "^8.4.47",
    "autoprefixer": "^10.4.20"
  }
}
```

Note: do NOT lock to exact versions; let Chase update as needed.

---

### `vite.config.ts` (educational-math)

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

---

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"]
}
```

---

### `tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
};
```

---

### `postcss.config.js`

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

---

### `index.html` (educational-math)

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
    <title>[App Name]</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

### `src/main.tsx` (educational-math)

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app/App';
import './styles/index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

### `src/app/App.tsx` (educational-math — minimal orchestrator)

```typescript
import { useState } from 'react';
import MainMenu from './components/MainMenu';

export default function App() {
  const [view, setView] = useState<'menu'>('menu');

  return (
    <div className="h-screen w-screen overflow-hidden bg-blue-50">
      {view === 'menu' && <MainMenu />}
    </div>
  );
}
```

---

### `src/app/components/MainMenu.tsx` (educational-math — placeholder)

```typescript
export default function MainMenu() {
  return (
    <div className="flex h-full items-center justify-center">
      <h1 className="text-4xl font-bold text-blue-900">[App Name]</h1>
    </div>
  );
}
```

---

### `src/styles/index.css` (educational-math)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

html, body, #root {
  height: 100%;
  margin: 0;
  padding: 0;
}
```

---

## After Init — What to Tell Chase

```
✅ Initialized [app-name] at [full path]
   Variant: [variant]
   Files created: [N]

To start:
  cd "[path]"
  npm install        # (or run `pip install -r backend/requirements.txt` if Python)
  npm run dev

The dev server will print the URL (usually http://localhost:5173 or next).

AI orientation: [app-name]/CLAUDE.md
App rules: [app-name]/guidelines/Guidelines.md
Master standards: cursor-patterns/CODING_STANDARDS.md

Append session entries to: [app-name]/docs/sessions/SESSIONS.md
```

---

## Notes For AI

- **Don't skip Step 1.** Even if Chase sounds eager, ask the 3 questions first. The variant decision matters and the path matters.
- **Don't auto-run npm install.** Ask first. Chase may want to inspect the package.json before installing.
- **Don't initialize git.** Chase manages git separately.
- **Don't create a remote, don't open a browser, don't write tests yet.** This is scaffolding only — first feature comes in the next session.
- **If the user names a variant you don't recognize**, default to asking what stack they want and adapt one of the three above.
- **Educational-math apps should reference sister apps in their CLAUDE.md.** That's how Chase keeps them consistent.
- **Functional-tool variant has the most uncertainty.** Always confirm the stack before scaffolding.
- **Embedded browser in a new Electron app:** Step 4c — pin `electron` to Macro App’s version; never mix Macro `WebContentsView` code with Video Player / Calendar 2.0’s Electron 28 scaffold.
