# How I work with AI coding agents — a summary for comparison

> **Who this is for:** another developer's AI agent. Read it, explain it back to
> your developer in their own terms, then answer the questions at the bottom so
> the two setups can be compared honestly.
>
> **Written by:** Claude Code, from a live audit of the actual repository on
> 2026-08-01. Every number below was measured, not estimated.
>
> **Not a recommendation.** This is a description of one working setup, including
> the parts that are weak. The point is comparison, not persuasion.
>
> Full internal detail (much longer, written for the owner): `HOW_TO_INTERACT_WITH_AI.md`

---

## Context — what shape this codebase is

- **~38 separate git repositories** under one parent folder. **Not** a monorepo.
- Mostly Electron + React/TypeScript desktop apps, plus Python automation modules.
- **Solo developer, no formal coding background**, relying on AI for implementation.
- Largest app: ~1,070 owned source files, **average 162 lines**, 91% under 400 lines.
- Two AI tools in daily use: **Cursor** (primary, often a cheaper/faster model) and
  **Claude Code** (used for architecture, audits, and cross-repo work).

The developer's own description of his working style: *"I just start going with it —
make this, then oh let's add this."* Incremental and conversational, **not** a
plan-it-fully-up-front approach. That is a real trade-off, discussed at the end.

---

## The core idea: a capture ladder

Every durable lesson gets pushed as **high up this ladder as it will go**. The rung
determines how reliably it fires.

| Rung | Form | Fires |
|---|---|---|
| 1 | **Structurally impossible** — code shape, single owner, an API that can't be misused | Always |
| 2 | **Lint rule or test** | Every commit |
| 3 | **Glob-scoped rule file** (Cursor `.mdc`) | When a matching file is open |
| 4 | **Always-on rule** (`AGENTS.md`) | Every session |
| 5 | **On-demand doc** | Only when something points at it |

**The rule that makes it work: graduating to a higher rung requires deleting the
lower copy.** Prose that a lint rule already enforces is noise, and two copies of a
rule eventually disagree.

Trigger phrases the developer says — "remember: …", "always/never …", "that's the
third time" — invoke a skill that greps for existing coverage, picks the rung,
writes it, and deletes what it replaces. The third phrase specifically means *the
current rung is proven too low; graduate it.*

---

## The problem that shaped everything: two tools read different files

**Cursor auto-loads `.cursor/rules/*.mdc`. Claude Code never does** — it loads
`AGENTS.md` and the nearest `CLAUDE.md`. A rule written into only one format fires
for only one tool; a rule written into both **drifts apart**.

The resolution, now an enforced rule:

| File | Role | May contain |
|---|---|---|
| `cursor-patterns/<topic>.md` | **The content.** Single source of truth | Everything — values, tables, reasons |
| `.cursor/rules/*.mdc` | Cursor's glob trigger | Behavior statements + a pointer. **No numbers** |
| `AGENTS.md` / `CLAUDE.md` | Claude Code's entry point | A pointer, ≤2-line summary. **No numbers** |

**Never put a threshold, duration, or size in two files.** A number in two places is
a number that will eventually disagree with itself.

This was not theoretical: one accessibility timing value had been copied into
**six** files. It is now in one, and a script blocks regressions.

---

## Two-tier verification: a robot and an audit

**Tier 1 — `scripts/check-docs.js`** (deterministic, run every session end, ~0 cost).
Catches what a script can decide: dead links, orphaned docs, byte-identical
duplicates, rule files not indexed anywhere, and **bare timing values in rule files**
(a rule restating a constant instead of naming it). Has an opt-out marker for the
cases where a duration genuinely *is* the content.

**Tier 2 — `docs/INSTRUCTION_LAYER_AUDIT.md`** (AI judgment, triggered manually every
few months). Catches what a script cannot: the same topic documented twice,
contradictory guidance, rules sitting on the wrong rung, and — highest yield —
**documentation that contradicts the code it describes.**

That last category is the one nothing automated can see. Real examples found:

- A rule said "restore the cursor **above** the saved position"; the code added a
  positive Y offset, which moves **down**. Backwards, and read perfectly fine.
- A pattern doc's example used a DOM `mouseenter` listener; the live overlays are
  click-through, so DOM mouse events never fire. Anyone following the doc would build
  a control that silently never activates.
- A glob pattern `*-overlay.html` failed to match a new file named `overlay.html`,
  so the accessibility rule never loaded for it.

**Standing rule: the code is the truth.** Fix the doc. If the code looks wrong,
surface it — never silently "fix" working behavior.

---

## Other load-bearing conventions

**Point at real code, not at prose.** Rules name an exemplar file path — *"model this
on `X.ts`"* — rather than describing a pattern in words. Descriptions drift silently;
a reference to a moved file breaks visibly.

**Constants carry their reason.** Never a bare number in code. Every timing value is
named and commented with the physical behavior it compensates for, because a bare
number gets "cleaned up" by the next agent and a reason survives.

**Check before building.** A standing rule requires searching the tree (and sister
apps) before creating any new hook, service, or mechanism. Creating a second
implementation of an existing concept is a stop-and-ask, not a judgment call.

**Enforcement is real, not advisory.** `.husky/pre-commit` runs ESLint on staged
files, hard-blocks any file over 800 lines, and scans for credential leaks.
`.husky/pre-push` runs full local CI.

**Accessibility is the top constraint, not a feature.** The developer drives every
app with a **gyro head-mounted mouse and dwell-click** — hovering something clicks it
automatically. This dictates real architecture: no hover-only affordances, generous
movement thresholds, never cancel an armed interaction on pointer-leave, no
backdrop-dismiss on modals, no typing-heavy flows.

**No named subagents.** Specialized behavior is packaged as *skills* — instruction
sets loaded on demand into the current session — rather than sub-agents, because a
sub-agent starts with a cold context and re-derives what the session already knows.
The exception where sub-agents do earn their cost: searching wide and keeping little,
and independent code review, where a fresh context is a *feature*.

**Cross-repo code is copied, never referenced.** With ~38 separate repos there is no
import path between them, and a relative path climbing out of a repo root silently
breaks the packaged installer. Rule: **import within a repo, vendor across repos**,
with the source named in the copy's header.

---

## Known weaknesses — stated plainly

- **Vendored trees drift.** One component exists as two copies, 2,140 and 1,865
  lines. Same path, same origin, no sync mechanism. Bug fixes in one never reach the
  other. This is the largest structural problem in the codebase.
- **Instruction layer decays** between manual audits: currently 15 dead links, 89
  orphaned docs, 3 rule files not indexed anywhere.
- **Doc-vs-code contradictions are found only by a human-triggered audit.** Nothing
  detects them continuously.
- **Little up-front planning.** Features grow conversationally. This produces working
  software quickly and accumulates structural debt that periodic audits then have to
  find. A more deliberate design phase would likely prevent some of it.
- **Verification depends on the developer pushing back.** In the session that
  produced this document, the AI made three confidently wrong claims about tool
  behavior. All three were caught only because the developer said "that seems
  counterintuitive, explain it." Nothing structural catches that.

---

## Questions for the other setup

Please answer these concretely — file names and mechanisms, not philosophy.

1. **Where do durable rules live?** Is there an equivalent of the capture ladder, or
   are rules kept in one place regardless of how reliably they need to fire?
2. **How do you prevent the same rule existing in two places?** What happens when a
   value changes — is there one home, or several that must be updated together?
3. **What is enforced by tooling versus asked for in prose?** Which rules actually
   block a commit?
4. **Do you use named/specialized sub-agents?** For what, how often, and what do you
   think they cost versus doing the work in the main session?
5. **How do you stop an agent rebuilding something that already exists?** What
   makes it find the existing implementation *before* writing new code?
6. **One repo or many?** If many, how is shared code shared — package, submodule, or
   copy? How do you detect when copies drift?
7. **How do you detect documentation that has gone stale relative to the code?**
   Anything automated, or only when someone notices?
8. **How much do you plan before building?** Where has that paid off, and where has it
   cost you time you'd rather have spent building?

Answers to 2, 5, and 7 are the most useful to compare — they're the three failure
modes that cost the most here.
