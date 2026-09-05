# APP_LOCATIONS.md — Where things live

> **AI: read this file before searching the tree.** Resolve app names and aliases here first.
> Only `Glob`/`Grep` the filesystem when this index does not list the target or you need a specific file inside an app.

**Workspace root:** `C:\Users\chase\Documents\Programs\`

Most school/teaching apps live under **`School Scrips\`**. That folder is **not** a separate
workspace — it is inside Programs.

> ### The folder names differ between Chase's two machines
>
> **On the desktop — this file's canonical spelling — it is `School Scrips`: *Scrips*, no T.**
> It was a typo years ago and it stuck. On the laptop the same folder is spelled correctly,
> `School Scripts`, and a few apps inside it differ too (`Macro-App` vs `Macro App`,
> `seating-chart` vs `Seating-Chart`).
>
> **Leave it alone.** Renaming it would touch launchers, `apps.json`, `.bat` files, vendored
> paths, and every doc in the tree — not worth the breakage. This is a known, accepted split.
>
> **What that means for you:** every path in this file is the **desktop** spelling. If a path
> from here doesn't exist, you are on the laptop — **list the parent folder and use what's
> actually there.** Do not conclude the app is missing, do not create the misspelled folder,
> and do not "fix" a path in this file to the laptop's spelling. Paths written into code or
> config must never hardcode either spelling.

---

## Quick lookup (active apps)

| You say… | Canonical folder | GitHub | Notes |
|----------|------------------|--------|-------|
| **Macro App**, macro | `School Scrips\Macro App` | chase1971/Macro-App | Main Electron hub; embeds calendar + Assignment Assistant |
| **Assignment Assistant**, AA, D2L Platform | `School Scrips\Macro App\assignment-assistant-engine` | *(vendored in Macro App)* | **Living source of truth** for AA UI/engine inside Macro App |
| **D2L-Assignment-Platform**, platform repo | `Deprecated apps\D2L-Assignment-Platform` | chase1971/D2L-Assignment-Platform | **Moved to Deprecated apps** (2026-07-21). Frozen reference — see `FROZEN.md` |
| **App Dashboard**, School OS | `School Scrips\App Dashboard` | chase1971/App-Dashboard | Launcher registry (`apps.json`), dev proxy, `.bat` launchers |
| **Factoring** | `School Scrips\factoring-app` | chase1971/factoring-app | Chrome + Vite math app |
| **Solving Quadratics** | `School Scrips\Solving Quadratics App` | chase1971/Solving-Quadratics-App | Chrome + Vite math app; multiple quadratic-solving tutorials (apps.json id `solving-quadratics`, port 5330) |
| **Fractions** | `School Scrips\Fractions-App` | chase1971/Fractions-App | |
| **Logic** | `School Scrips\logic-app` | chase1971/logic-app | |
| **Matrix** | `School Scrips\Matrix app` | chase1971/Matrix-app | |
| **Probability** | `School Scrips\Probability App` | chase1971/Probability-App | |
| **Statistics** | `School Scrips\Statistics app` | chase1971/Statistics-app | |
| **Transformations** | `School Scrips\transformations-app` | chase1971/transformations-app | Guided practice app; **code reader GUI:** `scripts\session_codec.py` (Launcher Panel: Transformations Code Reader) |
| **Student Portal**, the dashboard students go to, the website with all the apps on it | `School Scrips\student-portal` | *(create repo)* | Public Netlify landing page — tile grid linking out to each math app. Live: **https://mathappsclass.netlify.app**. Tile list: `src\config\apps.ts`. No login/backend yet |
| **student-session-kit** | `School Scrips\student-session-kit` | *(create repo)* | Shared Supabase client for math app session submission + Macro App review |
| **Math App Studio** | `School Scrips\Math App Studio` | chase1971/annotation-studio | Electron embed + visual design/pin layer for math apps (launcher id `annotation-studio`) |
| **School documents**, school docs | `School Scrips\School documents` | chase1971/School-Documents | Miscellaneous teaching HTML/docs (exam maps, Pearson comparisons); not app code. **Tell AI to save new school HTML here.** |
| **Makeup Exam** | `School Scrips\makeup-exam-standalone` | chase1971/makeup-exam-standalone | Python + Electron |
| **Extra Credit** (v2) | `School Scrips\Extra credit extractor v2` | chase1971/Extra-credit-extractor-v2 | |
| **Seating Chart** | `School Scripts\seating-chart` | chase1971/Seating-Chart | Electron; reads Macro rosters |
| **Electron toolbar**, toolbar | `electron-toolbar` | chase1971/electron-toolbar | Python + Electron overlay; dwell-mouse host. **"Put in electron toolbar" = Launcher Panel grid (📚), not App Dashboard, not main strip buttons** — see `electron-toolbar/docs/LAUNCHER_PANEL.md` |
| **Overlay maker**, overlay picker, overlay setups | `electron-toolbar\overlay-creator\` | *(part of electron-toolbar)* | **Overlay Folder** — see **`overlay-creator\AGENTS.md`**. Saved setups use edit-mode title bar (Unassigned vs group name); Active grid always shows individual overlay tiles. Pointer policy + behavior modes in registry/presets. Integration: `overlay-creator\index.js`. |
| **Video Player**, video player | `Video Player` | *(local git)* | **`C:\Users\chase\Documents\Programs\Video Player\`** — Electron + embedded VLC; random episode picker + resume. **Not inside electron-toolbar** — toolbar only launches it (`Shift+F19`, Launcher Panel tile `video-player` → `Video Player\launch.bat`). Data: `%APPDATA%\video-player\data\`. Docs: `Video Player\CLAUDE.md`, `docs\VLC_EMBEDDING.md`. |
| **Agent Browser**, agent browser | `Agent Browser` | *(local)* | **`C:\Users\chase\Documents\Programs\Agent Browser\`** — Personal Electron + embedded Chromium for agent experiments. CDP **9227**. **Cursor MCP:** `Programs/.cursor/mcp.json` → server `agent-browser` (Playwright MCP + CDP). Launch: Launcher Panel tile `agent-browser` (monitor-aware) or **Shift+F20** (primary monitor). Not connected to Macro App. Docs: `Agent Browser\CLAUDE.md`. |
| **Hearthstone Overlay 3.0**, HS Overlay 3.0, go face, hearthstone overlay | `Hearthstone Overlay 3.0` | *(local)* | **`C:\Users\chase\Documents\Programs\Hearthstone Overlay 3.0\`** — Electron + Python log service. Launch: `launch.bat` or toolbar Launcher Panel tile **`hearthstone-overlay-3`**. Go Face / combat robot: `electron/play-actions.js`, `electron/robot-worker.js`, `electron/go-face-window.js`. Session log: `docs/sessions/SESSIONS.md`. Daily driver (2.0 is legacy Tk overlay). |
| **Quasimorph Tracker**, QM Tracker | `Quasimorph Tracker` | *(local)* | Electron + React companion dashboard for Quasimorph; reads `QM_FactionDump` JSON. Launcher Panel tile `quasimorph-tracker` -> `launch.bat`. |
| **Guildrun Stats**, Guild Run Tracker, Guild Run, guildrun-stats, guildrun | `Guildrun Stats` | *(local)* | Python. HTML run sheet built from Guildrun save files. View: `http://127.0.0.1:8765/scratch/guildrun-stats.html`, past runs `.../guildrun-runs.html`. **Keyword routing: `Guildrun Stats/AGENTS.md`**; mechanics: `Guildrun Stats/README.md`. |
| **CourseAgent** | `CourseAgent` | ccarlozzi/CourseAgent | |
| **Programs patterns / standards / recipes** | `agent docs\recipes\` | *(Programs root repo)* | `CODING_STANDARDS.md`, `INIT_NEW_APP.md`, and every interaction recipe live here |

Full paths: prepend `C:\Users\chase\Documents\Programs\` to every relative path above.

---

## Frozen apps — do not scan, edit, or pair-check unless Chase explicitly asks

| You say… | Folder | GitHub | Status |
|----------|--------|--------|--------|
| **Calendar 2.0**, calendar | `School Scrips\Calendar 2.0` | chase1971/Calendar-2.0 | **FROZEN** (2026-07-29). See `FROZEN.md`. Skip in multi-repo git scans. Read-only exemplar for other apps OK. |

---

## Sister-app pairs (check both when either changes)

| Pair | Why |
|------|-----|
| **Macro App** ↔ **assignment-assistant-engine** | Engine folder inside Macro App is the live AA copy |

**Not auto-paired (frozen or deprecated):** Calendar 2.0, D2L-Assignment-Platform — only when Chase explicitly asks.

---

## Legacy / duplicate folders — do not use unless explicitly asked

All superseded copies below live under **`Deprecated apps\`** (safe to delete that whole folder when done). See `Deprecated apps\README.md`.

| Folder | Status |
|--------|--------|
| `Deprecated apps\Calendar` | **Old** calendar (v1). Use **Calendar 2.0** instead. |
| `Deprecated apps\D2L Macro App` | No git repo; stale duplicate name. Use **Macro App**. |
| `Deprecated apps\D2L-Assignment-Assistant` | Standalone AA repo; superseded for daily work by Macro App vendored engine |
| `Deprecated apps\d2l-assignment-assistant-app` | Upstream fork (swaroop-sapkota); snapshot/reference only |
| `Deprecated apps\D2L-Macro` | Separate repo; not the main Macro App |
| `Deprecated apps\Extra credit extractor` | v1; use **Extra credit extractor v2** |
| `Deprecated apps\Old Apps` | Archive |
| `Deprecated apps\Makeup-Exam-Platform` | No git; use **makeup-exam-standalone** |
| `Deprecated apps\D2L-Assignment-Platform` | Frozen reference; live AA is in Macro App |
| `Deprecated apps\Hearthstone Overlay 2.0` | **Legacy** Tk overlay. Daily work → **Hearthstone Overlay 3.0** |
| `Deprecated apps\Targeting overlay` | Predecessor to HS 3.0 targeting |
| `Deprecated apps\voicy-extracted` | Extracted Voicy app for inspection |
| `Archived markdowns\` | Historical docs only — not current guidance |

---

## Other projects under Programs (non–School Scrips)

| Folder | GitHub | Purpose |
|--------|--------|---------|
| `android-auto-scroll` | chase1971/android-auto-scroll | |
| `spire-overlay` | chase1971/spire-overlay | Slay the Spire overlay |
| `sts2-dwell-targeting` | chase1971/Dwell-Targeting | STS2 dwell targeting |
| `Video Player` | *(local git)* | See **Quick lookup** — not in App Dashboard; toolbar Launcher Panel + Shift+F19 |
| `Agent Browser` | *(local)* | See **Quick lookup** — personal Electron + embedded Chromium; CDP **9227**; toolbar Launcher Panel + Shift+F20; not in App Dashboard |
| `poe-stats-overlay` | | Path of Exile overlay |
| `Monitor Configuration App` | | Display/monitor tooling |
| `generic scripts` | | One-off scripts |
| `program discovery` | | Program inventory GUI/scripts |

---

## Other workspaces (outside Programs)

| Workspace | Path | Notes |
|-----------|------|-------|
| **ToME**, Tome, T-Engine | `C:\Users\chase\Desktop\t-engine4-windows-1.7.6` | Tales of Maj'Eyal/T-Engine desktop install. Addons go in `game\addons\*.teaa`; user data lives in `C:\Users\chase\T-Engine\4.0\tome\`. |
| **Quasimorph mods**, Quasimorph, QM_StickyTooltips | `C:\Users\chase\Desktop\games\Quasimorph-GoldBerg\mod-dev` | Local Harmony mod source outside Programs; build each mod from `QM_*\src`; post-build deploys to Quasimorph `LocalUserPresets`. |
| **Rosters etc** | `C:\Users\chase\My Drive\Rosters etc` | Course rosters, attendance, calendars, email templates — Google Drive |
| **D2L Assignment Assistant** | `C:\Users\chase\Documents\D2L Assignment Assistant` | Separate Cursor workspace folder (may be empty or symlink — prefer Macro App for AA code) |

---

## Machine-readable launch registry

**`School Scrips\App Dashboard\apps.json`** — canonical `cwd` paths and dev ports for every toolbar-launched app.
Use when you need exact launch paths or proxy ports, not just “which folder is this app.”

---

## Git layout reminder

Each app above with a GitHub row is its **own git repo** (sibling repos, not a monorepo).
Committing Macro App does **not** commit sibling repos (e.g. frozen Calendar 2.0).
Programs root (`C:\Users\chase\Documents\Programs\.git`) — **`chase1971/Program-Instruction-Layer`**
(instruction layer: `AGENTS.md`, `HOW_TO_INTERACT_WITH_AI.md`, `agent docs/recipes/`, `agent docs/rules/` — not app source).

---

## Maintenance

When you **initialize a new app** or rename a folder, add a row to **Quick lookup** and (if toolbar-launched) an entry in `App Dashboard\apps.json`.
