# Studio ↔ AI — one source of truth at a time

> **You might say:** "Studio and AI are fighting over screens.json", "design handoff"
> **What it is:** Bidirectional source-of-truth between Studio and AI canvas edits
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/studio-design-propagation.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `**/screens.json`
- `**/prototype.json`
- `School Scrips/Math App Studio/**`
- `School Scrips/Solving Quadratics App/**`

---

## The handoff model (Chase's workflow)

| Phase | Source of truth | Who reads | Who writes |
|-------|-----------------|------------|------------|
| **Starting an AI task** | Math App Studio (`screens.json` on disk) | AI reads Studio + git diff | — |
| **AI completes the task** | AI's result on disk | Studio reloads automatically | AI writes `screens.json` (+ live app code) |

There must never be two competing versions. After AI finishes, **Studio must show exactly what is on disk**.

## Before editing `screens.json` or live design code

1. **Archive** the current spec:
   - PowerShell: `School Scrips/Math App Studio/scripts/archive-design-spec.ps1 -DesignDir "<app>/src/design"`
   - Or copy to `src/design/backups/screens-pre-ai-<timestamp>.json`
2. **`git diff`** the design file — small rect moves count.
3. Read Studio state as truth; propagate templates to siblings when obvious (step 1 → steps 2/3, etc.).

Archives live in `src/design/backups/` — Chase can restore any `pre-ai-*` file manually.

## After editing `screens.json`

- Write the file directly (AI result is truth).
- If Math App Studio is open, it **watches the file** and reloads almost immediately.
- Studio autosave will **not** overwrite a newer disk file.
- Run `scripts/check-design-spec.ps1` as the **final step** of any session that touched a spec; resolve error-level findings before declaring done.
- **After AI was source of truth** (AI wrote `screens.json` directly): run `scripts/ai-handoff-complete.ps1 -DesignDir "<app>/src/design"`. This pins the current spec as the handoff baseline and clears stale "Export for AI" diffs in Studio (otherwise Studio compares against the old pre-export pin and flags every new element).

## Design history (Phase 1)

- Journal: `src/design/history/journal.jsonl` + `snapshots/` (gitignored, per-machine).
- Pinned checkpoints: `src/design/history/pinned/` (**committed**).
- Playbook: `Math App Studio/docs/DESIGN_HISTORY.md`.
- List history: `scripts/list-design-history.ps1 -DesignDir "<app>/src/design"`.
- Restore: `scripts/restore-design-snapshot.ps1 -DesignDir "..." -SnapshotId "<id>"`.
- Export: click **Export for AI** in Studio sidebar, or `scripts/handoff-to-ai.ps1 -DesignDir "<app>/src/design"`.
- **Journal before restore; pin before edit.** Consult `journal.jsonl` before any restore; archive/pre-ai pin before any AI spec edit.

## One write path

Any code that writes `screens.json` / `prototype.json` must go through `saveCanvasSpec` in `electron/canvas-spec.js` — never a raw `writeFile`.

## Visible boxes and structure (Phase 3 rules — apply when authoring)

1. **Every visible box is defined in the spec.** Popups/dialogs are modals in `screens.json`; code opens by id, never hardcodes position/copy.
2. **Structure for editability.** Grouped/evenly spaced buttons use `buttonArrays` + link groups, not loose siblings.
3. **Triggered events are AI-authored** (`triggerNote` + `eventGroupId` when Phase 3 lands) — Chase inspects via tabs, does not build them in Studio.

## Design packages (tutorial banks, practice sets)

Problems that share a layout shell belong in a **design package** — metadata only, not a navigable screen.

**On each problem screen:**
- `packageId` — stable id, e.g. `gcf-tutorial`, `factoring-practice`
- `packagePath` — `["<packageId>", "<segmentId>", "<problem-leaf>"]` e.g. `["gcf-tutorial","part-1","problem-1"]`
- `problemIndex` — 1-based order within the segment
- `title` — human label, e.g. `GCF Tutorial — Problem 1`

**Top-level `designPackages` registry** (in `screens.json`):
```json
"designPackages": {
  "gcf-tutorial": {
    "id": "gcf-tutorial",
    "title": "GCF Tutorial",
    "kind": "tutorial",
    "segments": { "part-1": { "id": "part-1", "title": "Finding the GCF" } }
  }
}
```

**When adding a new problem in an existing package:** clone layout from the template problem in that package; new `screen.id`; unique equation/copy/triggers; same `packageId`; new `packagePath` leaf + `problemIndex`; register segment in `designPackages` if new.

**When adding a new package:** create `designPackages` entry + first problem screen tagged as above. Exemplar: Solving Quadratics `gcf-tutorial` / `screen-1783803390569-790`.

**Cross-screen layout linking (future):** optional `packageLinkGroupId` on buttons/modals — same id within a package will propagate resize across problems when Studio support lands. Prefer matching rects + naming convention until then.

**Export/handoff** includes `## Design packages` tree — consult it before bulk edits ("all GCF problems", "part 2 only" → filter by `packagePath`).

## What AI may add without asking

- Missing navigation (Back, Exit) so the user is not trapped.
- Wiring needed for buttons/actions already in the design.
- Propagating a template layout across tutorial steps / repeated blocks.
- **Multiple-choice or evenly spaced button groups** → use `buttonArrays` (e.g. 2×2 grid), not loose separate buttons. Match existing grid pattern: `buttonArrays` entry + `arrayGroupId` + `linkGroupId` on each cell. Exemplar: Launch Menu `btnarray-1783739493938-601` or GCF `btnarray-gcf-mcq`.

## What AI must not do unasked

- Arbitrary resize/reposition of elements Chase already placed in Studio.
- "Improving" layout that diverges from the current `screens.json`.
- Changing step-specific copy when propagating structure.
- **Studio display/rendering bugs** → fix renderer/canvas-kit only. Never touch `screens.json` rects or add load-time repair that overwrites user placement.
- **`blankCanvasRepair`** → fill missing/broken data only (empty arrays, broken refs). Never normalize rects, sizes, or link-group positions the user set.

## Still ask when

- Two valid templates (which step is the reference?).
- Chat contradicts the on-disk design.
