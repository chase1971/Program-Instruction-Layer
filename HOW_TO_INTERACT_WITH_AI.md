# How To Interact With AI

> A complete map of how my AI coding setup works — every file, what it does,
> how the AI finds it, and how to use it day-to-day.
>
> **For me:** so I don't forget how this works.
> **For AI:** if I ask you to change the system, read this first to see the
> whole picture.
>
> **Last updated:** 2026-05-19

---

## The Big Picture (in one paragraph)

I have a layered guidance system. At the top is a **master coding-standards
file** that applies to all my apps. A **Cursor User Rule** (set in Cursor's
settings) and a **`CLAUDE.md`** at the Programs root both point AI at that
master file. Recipes for common tasks (initializing a new app, ending a session)
live in separate files that the AI reads when triggered. Memory files capture
my personal preferences (accessibility, style). Each app then has its own
short `CLAUDE.md` and `guidelines/Guidelines.md` for app-specific quirks. The
result: open Cursor or Claude Code in any folder, and the AI already knows
my standards, my accessibility needs, and my conventions — without me having
to repeat them.

---

## The Map: Where Everything Lives

```
C:\Users\chase\Documents\Programs\
│
├── CLAUDE.md                              ← Auto-loaded by Claude Code for
│                                            every session in this tree.
│                                            Points to standards + recipes.
│
├── HOW_TO_INTERACT_WITH_AI.md             ← THIS FILE. The system overview.
│
├── cursor-patterns\                       ← Where the rules and recipes live.
│   ├── CODING_STANDARDS.md                ★ Master file. THE rules.
│   ├── INIT_NEW_APP.md                    ★ Recipe for new apps.
│   ├── README.md                          ← Index of this folder.
│   ├── refactoring-checklist.md           ← Deep dive (referenced when
│   ├── react-patterns.md                    refactoring or building specific
│   ├── modal-pattern.md                     things).
│   ├── file-size-enforcement.md
│   ├── file-headers.md
│   ├── anti-patterns.md
│   ├── accessibility-patterns.md
│   ├── logging-standards.md
│   ├── FILE_SIZE_QUICK_REFERENCE.md
│   ├── modal-scrolling-fix.md
│   ├── animation-frame-debug-tool.md
│   └── add-a-line-change-a-sign.md
│
├── Archived markdowns\                    ← Old/stale docs. Not loaded by AI.
│   ├── cursor-patterns\                     History only.
│   └── electron-toolbar\
│
├── School Scrips\                         ← My apps live here.
│   └── [app-name]\
│       ├── CLAUDE.md                      ← Per-app AI orientation.
│       ├── README.md                      ← For humans.
│       ├── guidelines\Guidelines.md       ← App-specific rules.
│       └── docs\sessions\SESSIONS.md      ← Running log of work done.
│
└── electron-toolbar\                      ← Special: dwell-mouse overlay tool.
    └── (similar structure)


C:\Users\chase\.claude\projects\C--Users-chase-Documents-Programs\memory\
                                          ← My personal preferences (auto-loaded
                                            by Claude Code).
├── MEMORY.md                              ← Index.
├── user_accessibility.md                  ← How I use the computer.
├── feedback_ask_first.md                  ← Ask before assuming.
└── feedback_prefer_exemplars.md           ← Don't write new pattern docs.
```

---

## How AI Tools Find All This

There are two AI environments I use, and they discover things differently.

### Cursor (my main tool)

Cursor does NOT walk up directories. It only reads:
1. The **User Rule** I set in Cursor Settings → Rules → User Rules
2. `.cursor/rules/*.mdc` files in the current project root
3. `.cursorrules` (legacy single-file format) in the current project root

So my User Rule is what gets Cursor wired into the system. It tells Cursor:
- Where the master standards file lives
- Where the new-app recipe lives
- About my accessibility needs
- Trigger phrases for end-of-session, etc.

**If I update my User Rule, every Cursor session in every project gets the
update immediately.** No need to copy files into each app.

### Claude Code

Claude Code auto-loads any file named `CLAUDE.md` by walking up the directory
tree from wherever I started the session. So:

- `C:\Users\chase\Documents\Programs\CLAUDE.md` loads for every session inside
  `Programs/` or any subfolder.
- A per-app `CLAUDE.md` (like `factoring-app/CLAUDE.md`) loads on top of that
  for sessions inside the app.
- `~/.claude/CLAUDE.md` (user-global) would load for every session anywhere,
  but I'm not using that file currently.

Claude Code also auto-loads my **memory files** at
`C:\Users\chase\.claude\projects\C--Users-chase-Documents-Programs\memory\`.
These contain my preferences (accessibility, ask-first, exemplars-only).

---

## The Files In Detail

### `C:\Users\chase\Documents\Programs\CLAUDE.md`

The entry point for Claude Code sessions. Short (~60 lines). Contains:
- A pointer to `cursor-patterns/CODING_STANDARDS.md` as the master file
- "Ask before you assume" rule
- The 6 most-violated rules (quick reminder)
- Pointer to `INIT_NEW_APP.md` for new apps
- The end-of-session protocol
- A map of what apps live in the tree

This file is short on purpose — it's a router, not the rules themselves.

### Cursor User Rule (in Cursor Settings)

Cursor's equivalent of `CLAUDE.md`. Contains:
- Accessibility context (head-mouse, dwell, VoiceAttack, speech-to-text)
- Ask before you assume
- Coding standards pointer
- Priority order
- Never-do list
- Requires-confirmation list
- Refactoring → refactoring-checklist.md
- Server-start guidance (Windows/PowerShell specifics)
- Reusable consistency (use exemplars, not new pattern docs)
- Starting a new app → INIT_NEW_APP.md
- End-of-session protocol

The full text lives only in Cursor Settings — not in any file here. To back
it up, copy it from Cursor Settings to a safe spot manually.

### `cursor-patterns\CODING_STANDARDS.md` (★ master)

The actual coding rules. ~600 lines. Includes:
- Development phases (rough draft / polish / final build)
- File size enforcement (800 max, 700 extract, 500+50 ask)
- App.tsx as orchestrator (under 100 lines)
- File and module organization
- Core principles (DRY, SRP, KISS, fail fast)
- Naming conventions (Python and TS)
- React patterns (hooks, services, state extraction)
- Modal sizing (`max-w-md`, never `max-w-3xl`)
- File headers (template + when to use)
- Input validation, API response shape
- Error handling, logging
- Anti-patterns
- Final build checklist (9/10 quality bar)
- When to break the rules

Other files in `cursor-patterns/` are deep dives referenced from here.

### `cursor-patterns\INIT_NEW_APP.md` (★ new app recipe)

The AI follows this when I say "initialize a new app" or similar. It:
1. Asks 3 clarifying questions (name, variant, location)
2. Confirms the plan before creating files
3. Scaffolds the folder structure for the chosen variant
4. Writes a `CLAUDE.md`, `Guidelines.md`, README, configs, session log
5. Asks before running `npm install`
6. Reports what was created and how to run it

Supports 4 variants:
- **`educational-math`** — React/Vite/Tailwind math teaching tools (Logic,
  Transformations, Factoring, Matrix, Fractions, Probability)
- **`functional-tool`** — utility apps, may be full-stack with Python backend
  (Makeup Exam, D2L Platform, D2L Macro)
- **`electron-overlay`** — Python + Electron with dwell-mouse accessibility
  (electron-toolbar)
- **`custom`** — describe the stack

### Memory files

Located at `C:\Users\chase\.claude\projects\C--Users-chase-Documents-Programs\memory\`.
Auto-loaded by Claude Code for every session in this tree.

| File | Contains |
|---|---|
| `MEMORY.md` | Index pointing at the others |
| `user_accessibility.md` | Head-mounted mouse, dwell, VoiceAttack, speech-to-text input. Implications for UI design and prompt interpretation. |
| `feedback_ask_first.md` | Ask ONE focused question before starting when scope/approach is ambiguous. |
| `feedback_prefer_exemplars.md` | Don't write new pattern markdowns. Default to "model on [existing file]." |

**Cursor doesn't read these directly** — but the equivalent info is in my
Cursor User Rule, so both environments end up with the same knowledge.

### Per-app `CLAUDE.md`

Short (~30-50 lines). Each app has its own. Contains:
- What the app is (1-2 sentences)
- Variant (educational-math, etc.)
- Pointer to master standards
- App-specific rules (color scheme, libraries, layout quirks)
- Sister apps to reference as exemplars
- Note about session logging

Loaded automatically by Claude Code when working in that app's folder.
For Cursor, this is read because the User Rule tells Cursor to "read CLAUDE.md
in this directory if present."

### Per-app `guidelines\Guidelines.md`

Longer than the per-app `CLAUDE.md`. App-specific design rules — color
palette, button styles, animation timings, math libraries, etc. The
per-app `CLAUDE.md` references this for the deeper details.

### Per-app `docs\sessions\SESSIONS.md`

Running log of every coding session. Newest entry at top. 5-section format:

```
## YYYY-MM-DD — Brief title
**Files changed:** [files with line deltas]
**What worked:** [what got done]
**Current state:** Green / Broken / Mid-refactor — [one line]
**File size flag:** [files now >500 lines, else "None"]
**Next session:** [concrete next action]
```

Written at end of every session by the AI when I say "end of session protocol."

---

## What's Encoded About Me

Across the Cursor User Rule, the memory files, and `Programs/CLAUDE.md`, the
AI knows:

### Accessibility

- I can't type — speech-to-text for ALL prompts. Expect transcription errors.
- I use a head-mounted gyroscopic mouse + dwell-clicking + VoiceAttack hotkeys.
- UI for me: big targets, no hover-only menus, no required typing.
- If a request seems garbled or contains weird tech terms, ASK before acting.
- If intent is obvious despite a typo, just proceed and silently correct.

### Work style

- **Ask before assume.** When scope/approach is ambiguous, ask ONE focused
  question. Don't barrel ahead.
- **Don't ask too much.** Trivial decisions, clear requests, and obvious
  follow-ups don't need confirmation.
- **Preserve existing behavior.** Don't refactor unrelated code while fixing
  a bug. Don't "improve" things I didn't ask about.
- **Prefer exemplars over pattern markdowns.** For consistency, point at
  existing code, don't write new pattern docs.

### The 6 most-violated coding rules

1. Check file size before editing. 800 hard cap.
2. App.tsx is an orchestrator (under 100 lines).
3. Modals use `max-w-md`. Never `max-w-3xl` or larger.
4. API calls go through a service layer. No inline `fetch()`.
5. Component over 300 lines or 5+ useState → extract to a custom hook.
6. Preserve existing behavior.

---

## Workflows

### Starting a new app

```
ME:  "Initialize a new educational-math app called geometry-explorer for
      teaching angle relationships."

AI:  [Asks any missing details — usually just location]
     "Confirm: create at School Scrips/geometry-explorer/ as
      educational-math variant. Yes/edit?"

ME:  "Yes."

AI:  [Scaffolds everything per INIT_NEW_APP.md]
     "Created. Run: cd 'School Scrips/geometry-explorer/' && npm install && npm run dev"
```

The AI follows `cursor-patterns/INIT_NEW_APP.md` — folder structure, configs,
CLAUDE.md, Guidelines.md, session log skeleton, all with the right variant
defaults.

### Day-to-day coding

I just start a session in the app folder and start working. The AI already
knows:
- The master standards (via User Rule)
- My accessibility needs (via User Rule + memory)
- The app's specific quirks (via the app's CLAUDE.md and Guidelines.md)
- The current state (it can read the latest SESSIONS.md entry)

If I say "build me a new modal for X," the AI:
- Checks file size before editing existing files
- Uses `max-w-md` automatically
- Puts the modal in `components/modals/`
- Asks before extracting if a file is already over 500 lines

### Ending a session

```
ME:  "Perform the end of session protocol."

AI:  [Asks if I want to run the build first if relevant]
     [Checks git status briefly]
     [Appends entry to docs/sessions/SESSIONS.md in the 5-section format]
     [Leaves TODO comments in code if mid-edit]
     "Logged. Sidebar at 968 lines is next session's target. Nothing broken."
```

### Picking up next session

```
ME:  "Where did we leave off?"

AI:  [Reads latest SESSIONS.md entry]
     "Yesterday: extracted DeleteConfirmDialog from Sidebar (1118→968 lines).
      All green. Next: extract rename drawer from Sidebar."

ME:  "OK, do that next."
```

### Making changes to the system itself

If I want to update the rules — new style guide entry, new variant for the
init recipe, new accessibility detail — I either:

1. Tell Cursor/Claude Code directly. Examples:
   - "Add a rule to CODING_STANDARDS.md that ..."
   - "Add a new variant to INIT_NEW_APP.md called ..."
   - "Update my accessibility memory to say ..."
2. The AI reads this file (`HOW_TO_INTERACT_WITH_AI.md`) for context if needed.
3. The AI edits the right file.

For Cursor User Rule changes specifically, the AI can only suggest text — I
have to paste it into Cursor Settings myself.

---

## Trigger Phrases (Quick Reference)

These are the magic words that trigger built-in behaviors:

| Say... | AI does... | Defined in |
|---|---|---|
| "Initialize a new app called X" | Reads INIT_NEW_APP.md, asks variant questions, scaffolds | Programs/CLAUDE.md + Cursor User Rule |
| "Bootstrap a new app" | Same as above | Same |
| "Set up a new project" | Same as above | Same |
| "Perform the end of session protocol" | Writes SESSIONS.md entry, checks state | Programs/CLAUDE.md + Cursor User Rule |
| "Wrap the session" / "End the session" | Same as above | Same |
| "Where did we leave off?" / "What's the state?" | Reads latest SESSIONS.md entry | Programs/CLAUDE.md + Cursor User Rule |
| "Refactor X" / "Clean up X" | Follows refactoring-checklist.md | Programs/CLAUDE.md + Cursor User Rule |
| "Final build" / "Make it 9/10" | Applies the final-build checklist | CODING_STANDARDS.md |

---

## Maintenance

### Adding a new rule to the coding standards
1. Edit `cursor-patterns/CODING_STANDARDS.md`
2. If it's a major rule, also add it to the "6 most violated rules" list in
   `Programs/CLAUDE.md` and the Cursor User Rule.

### Adding a new variant to the init recipe
1. Edit `cursor-patterns/INIT_NEW_APP.md`
2. Add a section under "Variants" with folder structure + template content.
3. Add the variant name to the list in `Programs/CLAUDE.md`'s "Starting a New
   App" section and the Cursor User Rule.

### Adding a personal preference (something about how I work)
1. Add a feedback memory file at `C:\Users\chase\.claude\projects\C--Users-chase-Documents-Programs\memory\feedback_X.md`
2. Add an index line to `memory/MEMORY.md`
3. Add the equivalent rule to the Cursor User Rule (since Cursor doesn't read
   memory files directly).

### Archiving stale docs
Move them to `C:\Users\chase\Documents\Programs\Archived markdowns\` with a
brief note in the archive's README about what was moved and why.

### When SESSIONS.md gets too long
Once an app's `SESSIONS.md` crosses ~500 lines, split:
- Keep last 3 months in `SESSIONS.md`
- Move older entries to `docs/sessions/archive/SESSIONS_YYYY-Q#.md`

---

## Troubleshooting

### AI ignores a rule
1. **Check the User Rule is up to date.** Open Cursor Settings → Rules → User
   Rules. Confirm the relevant section is there.
2. **For Claude Code:** check that `Programs/CLAUDE.md` references the file.
3. **For app-specific issues:** check the app's `CLAUDE.md` and
   `guidelines/Guidelines.md` — app rules supplement master rules.
4. **As a last resort:** mention the file by name in the prompt:
   "Check CODING_STANDARDS.md first."

### AI is asking too much (over-clarifying)
The "Ask Before You Assume" rule has a "don't ask if..." section. If AI is
asking about trivial things, remind it: "This is a clear request — just do it.
Don't ask about every small choice."

### AI is asking too little (barreling ahead)
Tell it explicitly: "Slow down. Ask me first before you start." Then strengthen
the "Ask Before You Assume" wording in the User Rule and CLAUDE.md.

### Init recipe gets variant wrong
If `INIT_NEW_APP.md` keeps picking the wrong variant, edit the variant
descriptions to be more specific. Or just be more specific in the initial
prompt: "educational-math variant" rather than letting AI infer.

### SESSIONS.md entries are bloated
If the AI is writing wall-of-text session entries, edit the end-of-session
protocol section to emphasize "5 sections, ~10 lines total, latest at top."

---

## What This System Doesn't Do

Being honest about gaps:

- **No automatic enforcement.** AI can violate rules; the rules exist to
  reduce the likelihood, not eliminate it. I still need to catch violations.
- **No version control of the rules.** If I change CODING_STANDARDS.md and
  break something, no rollback unless I'm using git for the cursor-patterns
  folder.
- **Cursor User Rule isn't synced to a file.** It only lives in Cursor's
  settings. If Cursor is reinstalled or settings get wiped, the User Rule is
  gone. I should periodically copy it out to a backup file.
- **Memory files only work for Claude Code.** Cursor doesn't read them. I
  duplicate the important parts into the Cursor User Rule manually.
- **AI tools change.** The discovery rules (where Claude Code looks, what
  Cursor reads) may change as the tools update. If something breaks
  mysteriously, check the tool's current docs first.

---

## TL;DR

- **Master rules:** `cursor-patterns/CODING_STANDARDS.md`
- **Cursor entry point:** Cursor Settings → Rules → User Rules
- **Claude Code entry point:** `Programs/CLAUDE.md`
- **New app:** say "initialize a new app called X." AI follows `INIT_NEW_APP.md`.
- **End session:** say "perform the end of session protocol." AI writes
  `SESSIONS.md` entry.
- **Next session:** say "where did we leave off?" AI reads `SESSIONS.md`.
- **Memory of my preferences:** Auto-loaded by Claude Code from
  `~/.claude/projects/.../memory/`. Duplicated in Cursor User Rule for Cursor.

If I forget how anything works, this file is the single place to look.
