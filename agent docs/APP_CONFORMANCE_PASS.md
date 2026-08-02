# App conformance pass — bring one repo up to the current standard

> **Rung 5 — on demand, one app at a time.** Not always-on.
> **Companion:** `INSTRUCTION_LAYER_AUDIT.md` audits the **whole workspace** for
> duplicates and contradictions. **This** file checks **one app** against the
> current Programs-root standard. Different jobs — do not merge them.
>
> **Trigger:** *"Run the conformance pass on `<app>`"* / *"modernize `<app>`'s agent
> docs"* / *"does `<app>` match the current standard?"*

---

## What Chase says

> **"Run the conformance pass on Matrix app."**

That is the whole instruction. Everything below is the agent's job, not his.

**One app per pass.** A pass over four apps produces a report nobody reads and
changes nobody can review. Finish one, report, then ask whether to continue.

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

## Report back — short table, no grep dumps

| Check | Finding | Action taken / proposed | Needs Chase? |
|---|---|---|---|
| A · Discoverability | e.g. no `CLAUDE.md`; 3 rules invisible | Created index with all rules | N |
| C · Doc vs code | e.g. rule cites a deleted helper | Repointed at current path | N |
| F · Retirement | e.g. 2 docs describe a removed panel | **Proposed** archive | **Y** |

Close with:

1. `check-docs.js` summary **before → after**
2. Anything **proposed but not done** (deletions and archives always need approval)
3. One sentence: *is this app now conformant, or what remains*

---

## Rules for the agent running this pass

1. **Read before writing.** Confirm a gap exists in this repo — do not assume from
   another app's shape.
2. **Extend, don't duplicate.** If the app already has an index or contract, improve
   it. A second one is the failure this whole system exists to prevent.
3. **Never delete without listing it in the report.** Prefer merge + tombstone.
4. **Do not edit application source**, run builds, run tests, or launch GUIs.
5. **Do not commit** unless Chase asks — this pass can be report-only.
6. **One app.** Stop and report before starting another.

---

*Last template update: 2026-08-01 — created from the standards established that day.*
