---
name: capture
description: Capture a lesson, rule, or correction into the Programs instruction layer at the right level of the capture ladder. Use when Chase says "remember:", "capture that", "that was the third time", "make sure you always/never...", or otherwise states a durable rule he wants to stop repeating. Not for one-off task instructions.
---

# Capture a lesson into the instruction layer

Chase said something he does not want to repeat again. Your job is to put it
where it will **fire automatically next time** — and to remove any weaker copy it
replaces.

He should not have to write files or decide placement. He says one sentence; you
do the rest. Typing is expensive for him — **ask at most one question, and only if
the rung is genuinely ambiguous.**

---

## Step 1 — Grep before you write

Search for where this rule already lives. Check, in order:

1. `AGENTS.md` (root)
2. **`recipes/INDEX.md`** — is there already a recipe for this?
3. `<app>/AGENTS.md` keyword table
4. `cursor-patterns/*.md` and `agent docs/rules/*.md`
5. Existing lint configs (`.eslintrc.cjs`) and `scripts/check-*.js`

**`.cursor/rules/*.mdc` no longer exist** (retired 2026-08-02) — do not create one.

**If it already exists somewhere: extend that, do not add a second copy.** If it
exists but keeps getting violated, that is the signal to **graduate it** (Step 3).

---

## Step 2 — Pick the rung

The capture ladder, strongest first. Push it as high as it will go.

| Rung | Form | Choose when |
|---|---|---|
| **1** | Structurally impossible — one owner, an API that can't be misused | The rule is about *who may do X*. Exemplar: only `usePersistedState.ts` may touch `localStorage` |
| **2** | Lint rule or test | The violation is mechanically detectable in code |
| **3a** | **A recipe in `recipes/` + its index row** | It is *how to build something* — an interaction, a component, a flow. **Default for patterns** |
| **3b** | **A keyword row in `<app>/AGENTS.md`** pointing at one doc | It applies to one app, and Chase would ask for it in plain speech |
| **4** | Always-on rule (root `AGENTS.md`) | It applies everywhere, is short, and must fire when Chase is *not* thinking about it. **Costs tokens every session** |
| **5** | On-demand doc nothing routes to | Deep background that can't be compressed, and no keyword fits |

**Rung 3 is the default.** It used to mean a glob-scoped `.mdc`; that trigger
depended on a matching file being open in a Cursor editor tab, which is not how
Chase works, so it never fired. A recipe or keyword row fires on **what he says** —
which is always present.

**Rung 4 is expensive.** It is re-read in every session, including the ones where
it is irrelevant. Only put something there if it must fire at a moment Chase is not
thinking about it — screen permission, git sync, shell syntax. *"He might forget the
recipe exists"* is **not** sufficient: he retrieves recipes by asking for them, and
that is a design he has chosen deliberately. Do not propose always-on injection to
make a lookup folder "fire automatically."

### Repetition forces graduation

If Chase signals this is a repeat — *"that was the third time"*, *"I've told you
this before"*, *"again"* — the current rung is **proven too low**. Move it up at
least one rung. Do not simply reword it in place.

---

## Step 3 — Write it in the five-ingredient shape

Model on `recipes/studio-dwell-latch.md` — the exemplar in this tree. Every rule needs:

1. **Why it exists**, in one sentence. A rule without a reason reads as a
   preference, and preferences get overridden.
2. **The single implementation, named** — this hook, at this path. Not "use a hook."
3. **An exemplar file to copy.** Point at working code; prose drifts, paths don't.
4. **Non-negotiables, each with the bug it prevents.** This is what stops a future
   session deleting code that looks redundant.
5. **An anti-pattern list** — the failure modes stated as failures.

For a **constant**, never write a bare number. Name it and record what it
compensates for, the way `electron-toolbar/modules/dwell/backend/dwell_constants.py`
does. A recipe never restates a value — it points at the file that owns it.

A recipe opens with this header:

```markdown
# <Title>

> **You might say:** "<the words Chase would use>", "<another phrasing>"
> **What it is:** <one line>

**Exemplar files — read these before writing new code:**

- `<real path>`
- `<real path>`

---
```

The **You might say** line is the trigger. Write it in *his* words, not the
technical name — that line is what a future agent matches against.

---

## Step 4 — Delete the lower copy

**Graduating means removing what it replaced.** Prose that a lint rule now
enforces is noise, and two copies drift apart. If the lesson moved from a doc to a
rule, cut the paragraph from the doc and leave a pointer if the doc still has other
reasons to exist.

If a whole file is superseded, tombstone it — a few lines pointing at the live
version — rather than deleting, so links don't dangle.

---

## Step 5 — Make it reachable

A rule nothing points at is functionally deleted. Update whichever applies:

- **New recipe** → add a row to the matching table in `recipes/INDEX.md`, with a
  status mark. **A recipe no table names is invisible.**
- **New app-specific doc** → add a keyword row to that app's `AGENTS.md`, in the
  words Chase would use
- **New root rule** → add it to the right section of root `AGENTS.md`; if it needs
  detail, put the detail in `agent docs/rules/` and link it from that section
- **New `cursor-patterns/` standard** → add it to `cursor-patterns/INDEX.md`
- **New app with no `AGENTS.md` yet** → create one plus a three-line `CLAUDE.md`
  that does `@AGENTS.md` (see `cursor-patterns/INIT_NEW_APP.md`)

**Both tools read the same file.** `AGENTS.md` holds the content; `CLAUDE.md` imports
it. Never write the same guidance into both.

---

## Step 6 — Report back, briefly

One or two lines:

> Captured as a glob rule at `<path>` (fires on `*.tsx`). Removed the paragraph it
> replaced in `<other path>`. Indexed in `<app>/CLAUDE.md`.

Do not narrate the ladder reasoning unless the choice was close.

---

## What NOT to capture

- **One-off task instructions.** "Use blue for this button" is not a rule.
- **Anything the repo already records** — code structure, git history, past fixes.
- **Vague preferences with no failure mode.** If you cannot name the bug it
  prevents, it is not ready. Ask what went wrong, and capture *that*.

If Chase asks to remember something in these categories, say so in one sentence and
ask what the underlying rule is.
