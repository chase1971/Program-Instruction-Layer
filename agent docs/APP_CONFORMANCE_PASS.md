# App conformance pass — bring one repo up to the current standard

> **Rung 5 — on demand, one app at a time.** Not always-on.
> **Companion:** `INSTRUCTION_LAYER_AUDIT.md` audits the **whole workspace** for
> duplicates and contradictions. **This** file checks **one app** against the
> current Programs-root standard. Different jobs — do not merge them.
>
> **Trigger:** *"Run the conformance pass on `<app>`"* / *"modernize `<app>`'s agent
> docs"* / *"does `<app>` match the current standard?"*

---

## Two phases — analyse first, change nothing

> **"Run the conformance pass on Matrix app."**

That is the whole instruction. What follows is the agent's job, not his.

### Phase 1 — Report only. **Fix nothing.**

Read the app, run the checks, and describe **what is there now and what is wrong
with it**. Do not edit a single file — not even an obvious one-line fix, not even
a missing `CLAUDE.md`. The report *is* the deliverable.

The point is that Chase sees the shape of the app before anything changes. A pass
that arrives with edits already made denies him that, and turns review into
auditing someone else's work.

### Phase 2 — Fix, one item at a time, as he calls them

He reads the findings and picks. Work through them in the order **he** chooses,
confirming as you go. Some findings he will decline — a doc that looks stale to an
agent may describe something he still uses. That is a valid outcome, not a failure.

**One app per pass.** Finish it, report, and ask before starting another. A pass
over four apps produces a report nobody reads and changes nobody can review.

---

## Out of scope — do not touch

| Skip | Why |
|---|---|
| `School Scrips/Calendar 2.0` | **Frozen** (`.cursor/rules/45-frozen-apps.mdc`) unless Chase names it |
| `Deprecated apps/**` | Retired — no conformance expected |
| Vendored trees (`calendar-vendor`, `assignment-assistant-engine`, `my-calendar`) | Copies of other repos. Fix the **origin**, not the copy |
| **Application source code** | This pass changes *instruction* files. Exception: § C, where code is **read** to verify a doc's claim — read, never edit |
| `docs/sessions/SESSIONS.md` | History. Never "correct" a past entry |

---

## The standard, as of 2026-08-01

Six checks. Run in this order — each is cheaper than the one after it.

### A · Discoverability — can an agent find the rules at all?

- [ ] **`CLAUDE.md` exists at the app root.** Without it, **Claude Code cannot see
      any `.mdc` file in this repo** — it never auto-loads them. This is the single
      highest-impact gap and several apps still fail it.
- [ ] **Every `.cursor/rules/*.mdc` has a row** in that `CLAUDE.md` rules table,
      saying *when it applies* — not just its name.
- [ ] Each `.mdc` has an explicit **`alwaysApply:`** value. Missing = no rung at all.
- [ ] Globs are checked against **real filenames in this repo** (see § C).
- [ ] The app appears in `APP_LOCATIONS.md` with its aliases.

### B · Single source — is any value written twice?

- [ ] Run `node scripts/check-docs.js` from the Programs root; read the
      **bare values** count.
- [ ] No timing, threshold, or size appears in **both** a rule and a content doc.
      Rules name the **constant**; the value lives in code or the topic's
      source-of-truth doc. (`AGENTS.md` § One content home, many pointers.)
- [ ] Rules point at an **exemplar file path** rather than describing a pattern in
      prose. Prose drifts silently; a moved path breaks visibly.
- [ ] No app-local restatement of a tree-wide rule — dwell timing, file-size cap,
      modal sizing all have one home outside this repo.

### C · Doc vs code — highest yield, do not skip

The robot cannot see any of this. For each rule in the app, verify its claims:

- [ ] **Values, directions, and behaviors match the code.** Open the file and check.
- [ ] **Named exemplars still exist** and are still the best example.
- [ ] **Code snippets would actually work** if followed literally.
- [ ] **Documented mechanisms are implemented** — grep for them.
- [ ] **Globs match real files.** List the repo's filenames against each `globs:`
      pattern; a near-miss like `*-overlay.html` vs `overlay.html` silently
      disables the rule.

> **The code is the truth.** Fix the doc. If the *code* looks wrong, surface it to
> Chase — never silently change working behavior.

### D · Enforcement — does anything actually block?

- [ ] File-size checker present **and wired**. Check **both** mechanisms:
      `.git/hooks/pre-commit` **and** `git config core.hooksPath` (husky redirects
      there — a repo can look unwired and be fully enforced).
- [ ] **Hook and checker are tracked in git.** Untracked enforcement does not
      follow the repo to another machine — it silently protects one computer.
- [ ] `.gitignore` covers build output, caches, and vendored deps so searches do
      not return duplicated source.

### E · Rung placement

- [ ] Long prose is **not** sitting in an always-on rule. Demote to a rung-5 doc and
      leave a pointer.
- [ ] Anything a lint rule or test already enforces is **deleted** from prose —
      graduating a rung requires removing the lower copy.
- [ ] A rule that must fire reliably is not parked in a doc nothing links to.

### F · Retirement

- [ ] Docs describing removed features, finished migrations, or abandoned plans →
      archive to `Archived markdowns/` or tombstone with
      `> Superseded by … — kept for history.`
- [ ] Orphans from `check-docs.js` belonging to this app → link, merge, or archive.
- [ ] Vendored copies carry a **header naming their origin**, so a copy stays
      traceable rather than orphaned.

---

## Phase 1 report — what it looks like now

Lead with **two or three sentences in plain language**: what this app is, how its
instruction layer is currently put together, and whether it is broadly healthy or
broadly stale. Chase should be able to stop reading there and still know where he
stands.

Then the findings — **no grep dumps, no walls of output**:

| # | Check | What's there now | Why it's a problem | Effort |
|---|---|---|---|---|
| 1 | A · Discoverability | No `CLAUDE.md`; 3 `.mdc` rules exist | Claude Code cannot see any of them — the rules never fire for half your tooling | S |
| 2 | C · Doc vs code | Rule cites `useFoo` helper; deleted in March | An agent following it writes against something that isn't there | S |
| 3 | F · Retirement | 2 docs describe a panel that was removed | Reads as current guidance; would be followed | M |

Rules for the table:

- **Ordered by impact**, worst first — not by which check found them.
- **"Why it's a problem" must name a consequence.** *"Doesn't follow the standard"*
  is not a consequence. *"An agent will rebuild this because it can't find the
  existing one"* is.
- **Effort**: S = minutes · M = a focused sitting · L = needs its own session.
- **Say when something is fine.** *"§ D enforcement: hook wired via husky, tracked,
  nothing to do"* is worth a line. A report that is all problems hides the fact that
  most of the app is healthy.

Close with:

1. `check-docs.js` summary for this app's files
2. **What you would do first if it were your call, and why**
3. Anything you could not determine without asking him

**Then stop.** Do not begin fixing.

---

## Rules for the agent running this pass

1. **Phase 1 changes nothing.** No edits, no new files, no commits — however
   obvious the fix looks. If you find yourself writing a file during Phase 1, stop.
2. **Read before concluding.** Confirm the gap exists *in this repo*. Do not infer
   it from another app's shape — that is how a report becomes fiction.
3. **Extend, don't duplicate** (Phase 2). If the app already has an index or a
   contract, improve it. A second one is the failure this system exists to prevent.
4. **Deletions and archives are always proposals**, even in Phase 2, even when he
   has approved the item generally. List what would go, then wait.
5. **Do not edit application source**, run builds, run tests, or launch GUIs. Code
   is read-only here — you open it only to check whether a doc is telling the truth.
6. **One app.** Stop and report before starting another.
7. **"It looks stale" is a question, not a verdict.** Chase knows what he still
   uses. Report the observation; let him rule on it.

---

*Last template update: 2026-08-01 — created from the standards established that day.*
