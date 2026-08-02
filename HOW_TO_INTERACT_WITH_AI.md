# How To Interact With AI

> The operating manual for my AI coding setup — what exists, how each tool finds
> it, and what to do when.
>
> **For me:** so I don't have to remember how this works.
> **For AI:** read this before changing anything about the instruction layer.
> **For someone else:** send them `agent docs/AGENT_SETUP_FOR_PEER_REVIEW.md` instead —
> this file is internal detail, that one is the outward-facing summary.
>
> **Last updated:** 2026-08-01 — rewritten from scratch.

---

## The one thing to understand first

**Cursor and Claude Code do not read the same files.**

| | Cursor | Claude Code |
|---|---|---|
| `.cursor/rules/*.mdc` | ✅ auto-loads | ❌ **never** |
| `AGENTS.md` | via user rule | ✅ always |
| Nearest `CLAUDE.md` | — | ✅ auto-loads |
| Any `.md` | only if pointed at | only if pointed at |

Everything below follows from this. A rule written into one format fires for one
tool. A rule written into **both** drifts apart. So:

> ### Content lives in exactly ONE file. Everything else points at it.

| File | Role | May contain |
|---|---|---|
| `cursor-patterns/<topic>.md` | **The content.** Single source of truth | Everything — values, tables, reasons |
| `.cursor/rules/*.mdc` | Cursor's glob trigger | Behavior + pointer. **No numbers** |
| `AGENTS.md` / `CLAUDE.md` | Claude Code's entry point | Pointer + ≤2-line summary. **No numbers** |

**Never put a threshold, duration, or size in two files.** One accessibility timing
had been copied into six files before this rule existed. `check-docs.js` now blocks
regressions.

---

## The capture ladder

When a lesson is worth keeping, push it as high up this ladder as it will go.
Higher = fires more reliably.

| Rung | Form | Fires |
|---|---|---|
| **1** | Structurally impossible — code shape, single owner, API that can't be misused | Always |
| **2** | Lint rule or test | Every commit |
| **3** | Glob-scoped `.mdc` | When a matching file is open (Cursor only) |
| **4** | Always-on rule (`AGENTS.md`) | Every session |
| **5** | On-demand doc | Only when something points at it |

**Graduating requires deleting the lower copy.** Prose that lint already enforces
is noise.

### Trigger phrases → the `capture` skill

| I say | It means |
|---|---|
| "remember: …" / "capture that" | Put it on the ladder now |
| "always / never …" | A durable rule, not a task instruction |
| **"that's the third time" / "again"** | **The current rung is too low — graduate it** |

I never write these files or decide where they go. I say one sentence; the skill
greps for existing coverage, picks the rung, writes it, deletes what it replaces,
and updates the index.

---

## Two-tier verification: a robot and an audit

**Tier 1 — the robot.** `node scripts/check-docs.js`
Deterministic, runs at every session end, costs nothing. Five checks:
dead links · orphaned docs · byte-identical duplicates · rule files not indexed
anywhere · **bare timing values in rule files**.

Bare-value check has an escape hatch for durations that genuinely *are* the content:
`<!-- value-ok: reason -->` on the line.

**Tier 2 — the audit.** `agent docs/INSTRUCTION_LAYER_AUDIT.md`
AI judgment, I trigger it every few months. Catches what a script can't: same topic
in two homes, contradictory guidance, rules on the wrong rung, and — **§ 2g, highest
yield** — documentation that contradicts the code it describes.

> **The code is the truth.** Fix the doc. If the *code* looks wrong, surface it —
> never silently "fix" working behavior.

---

## Search — read this before concluding something doesn't exist

**`/.ignore` at the Programs root controls what searches can see. Do not delete it.**

The root `.gitignore` is a strict allowlist (`/*`) scoped to the meta-backup repo.
On its own that makes *every* app tree invisible to a tree-wide `Grep` — searches
return **zero hits for code that definitely exists**. `/.ignore` re-includes the
active app trees and keeps `Deprecated apps/` and frozen `Calendar 2.0` out.

| Tool | Respects ignore files? |
|---|---|
| **Grep** (content) | ✅ — prefer it |
| **Glob** (filenames) | ❌ — scope it with `path:` to one app |
| Bash `find` / `ls` | ❌ — don't use these to locate files |

Build outputs, caches and vendored deps duplicate real source (~178 such
directories). If a search returns installer or `__pycache__` copies, the owning
repo's `.gitignore` has a gap — **fix the `.gitignore`, don't work around it.**

> If a tree-wide search comes back empty, **suspect the filter before concluding the
> code is missing.**

---

## Enforcement that actually blocks

| Hook | Runs |
|---|---|
| `.husky/pre-commit` | ESLint on staged files → **800-line hard cap** → credential scan |
| `.husky/pre-push` | `npm run ci:local` — lint, tests, build, Python |

`--no-verify` skips these. On **commit** that also skips the secret scan, which is
the FERPA guard — so when in a hurry, bypass the **push**, not the commit.

File-size cap is a **smell detector, not a law**. The better test: *can I say what
this file does in one sentence, without "and"?* Pressure valves exist —
`SPLIT_TRACKED_ALLOWLIST` for legacy files, `WARN_OVERRIDES` to stop a split file
regrowing.

---

## Accessibility — the constraint that shapes architecture

I drive every app with a **gyro head-mounted mouse + dwell click**. Hovering
something clicks it. There is no "just click it" fallback and no "hold perfectly
still" either.

Two rules subsume most of the rest:

1. **Every hover affordance must also have a click path.**
2. **Assume every hovered element gets clicked** — design so that click is harmless
   or is the intended action.

**Source of truth: `cursor-patterns/dwell-and-head-mouse.md`.** Every timing value
lives there and nowhere else. Never copy a number out of it into another doc.

---

## Code reuse across ~38 repos

This is **not** a monorepo.

| Situation | Method |
|---|---|
| Same repo | `import` / `require` |
| Different repo | **Copy it in**, naming the source in the file header |

Never a path that climbs out of a repo root — `electron-builder` packages only the
app directory, so an external reference ships a crash with no build error.

Known cost: **vendored copies drift.** One component currently exists at 2,140 and
1,865 lines in two trees. The header pointer is what makes a copy traceable rather
than orphaned.

**Before building any new mechanism, search first** (see § Search). Creating a second
implementation of an existing concept is a stop-and-ask, not a judgment call.

---

## The map

| File | What it is |
|---|---|
| `AGENTS.md` | Always-on entry point. Rules, ladder, pointers |
| `CLAUDE.md` | Thin — imports `AGENTS.md` |
| `APP_LOCATIONS.md` | Which app lives where. Read before searching folders |
| `cursor-patterns/` | The content library — `CODING_STANDARDS.md`, `dwell-and-head-mouse.md`, `INIT_NEW_APP.md` |
| `.cursor/rules/*.mdc` | Cursor glob triggers (root + per-app) |
| `<app>/CLAUDE.md` | Per-app index — what it is, which rules apply, on-demand docs |
| `<app>/docs/*_INTEGRATION.md` | Subsystem deep-dives — mental model, symptom→fix, what burned us |
| `<app>/docs/sessions/SESSIONS.md` | Session log |
| `agent docs/INSTRUCTION_LAYER_AUDIT.md` | Workspace-wide periodic audit (rung 5, on demand) |
| `agent docs/APP_CONFORMANCE_PASS.md` | Bring **one app** up to the current standard |
| `agent docs/AGENT_SETUP_FOR_PEER_REVIEW.md` | Outward-facing summary for other developers |
| `scripts/check-docs.js` | The robot |

---

## What to say when

| I want… | I say |
|---|---|
| A rule remembered | "remember: …" — invokes `capture` |
| A rule that keeps getting missed | "that's the third time" — forces it up a rung |
| Periodic instruction cleanup (whole tree) | "run the audit doc" |
| Modernize one app's agent docs | "run the conformance pass on `<app>`" |
| Session wrap-up | "end of session protocol" — logs, commits, pushes all dirty repos |
| State on resuming | "where did we leave off" |
| A new app | "initialize a new app" — follows `cursor-patterns/INIT_NEW_APP.md` |

**Ask before you assume:** when scope or approach is genuinely ambiguous, ask **one**
focused question and wait. Not five. Not none.

---

## Cost notes

Prompt caching means the conversation prefix is cheap to re-read; **what the AI
writes is what costs**. Consequences:

- Long focused sessions beat many short ones — restarting throws away a warm cache.
- Trimming rule files is nearly worthless (~2–3% of context, cached after the first
  message). **Converting a solved problem into a script, and its answer into a
  written record, is worth roughly 10×.**
- The cheapest possible answer is one already written down — zero tool calls.

---

## Frozen apps

`School Scrips/Calendar 2.0` is **frozen** — no scans, edits, or git sync unless I
name it explicitly. It's excluded from tree-wide search via `/.ignore`, and its rules
are deliberately left unindexed. See `.cursor/rules/45-frozen-apps.mdc`.
