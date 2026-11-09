# Momentum handoff: Final Exam Review bank (Pearson unit exams)

**Written:** 2026-11-06. Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify. Docs server assumed on `http://127.0.0.1:8765/`.

## Objective and current phase

Chase is building a **Final Exam Review bank** HTML map that holds every pool alternate from Calculus I Exams 1–4, so he can later click problems into a final review and then a final exam. Phase: **Exam 1 and Exam 2 editor harvests are done and visible on the map.** Exams 3 and 4 are empty tabs. Exam 4 unit map work from earlier in this chat (review harvest, by-skill, pools, section counts, re-pool proposal) is separate and already usable.

## Chase's desired feel
- He wants **all pool alternates**, not print (print only shows one draw per pool).
- Traditional Pearson editor, not the modern Beta copy UI: "you'd be able to do it a lot faster with the traditional way."
- Copy-dialog annoyance: wait ~2–3s until the "Send grades…" checkbox appears before Continue.
- Live exams with student attempts are locked for Add/Remove Content. Workflow: **Copy** the exam → traditional Continue → Add/Remove Content → harvest the copy.
- He asked to copy Exams 1 and 2 (skip Exam 3 copy until needed; he thought no one had started Exam 3). Finish one exam harvest, show him the page, then continue.
- Pearson designing is "annoying" (uneven multi-part problems, thin alternate banks). Earlier Exam 4 advice was about pool balance and part counts; that map already has work badges.

## Accepted decisions
- **Editor harvest** (`PEARSON_EXAM_POOL_HARVEST.md`): Edit/copy → Add/Remove Content → click first My Selections ID → `PlayerAddAndRemove.aspx` → Work as student → Next loop → raw JSON → post-process.
- Final bank page: `final-exam-review-map.html` with Exam 1–4 tabs; expand pools/problems. Add-to-final-review UI not built yet.
- Exam 1: harvested from traditional **Exam 1 (Copy)** — **39 Q / 25 pools**. Pool orders fixed from `harvest/_exam1-ids.json` (Question Details), not the broken My Selections table scrape.
- Exam 2: harvested from **Exam 2 (Copy)** — **34 Q / 20 pools**. Pool orders from My Selections text dump (`harvest/_exam2-myselections.txt`); regex must allow `\d+(?:\.\d+)+` (three-part IDs). Question Details CLI failed while editor was open (AM grid hidden).
- Pearson quirk on Exam 2: **`3.7.20` appears in both pool 11 and pool 12** (same ID twice in My Selections).
- Traditional copy path only for future exams. Do not use modern Beta assignment creation for harvest.

## Rejected directions
- Print harvest alone for pooled exams (25 slots vs 39 IDs on Exam 1). Kept as `exam1-exam-print-harvest.json` but not the bank source of truth.
- Harvesting the live locked Exam 1 editor (students already started).
- Modern copy UI / clicking IDs there (did not open `PlayerAddAndRemove`).
- Treating Question Details failure as a blocker when My Selections text is available.

## Current implementation state

**Open for Chase:** [http://127.0.0.1:8765/final-exam-review-map.html](http://127.0.0.1:8765/final-exam-review-map.html) — Exam 1 and Exam 2 tabs ready.

| Artifact | Role |
|---|---|
| `School Scrips/School documents/final-exam-review-map.html` (+ `-app.js`, `-data.js`) | Final bank UI |
| `exam1-exam-harvest.json`, `exam1-exam-data.js` | Exam 1 cleaned harvest |
| `exam2-exam-harvest.json`, `exam2-exam-data.js` | Exam 2 cleaned harvest |
| `harvest/exam1-editor-preview-raw.json`, `exam2-editor-preview-raw.json` | Raw Next-loop MCP output |
| `harvest/write_exam1_editor_harvest.py`, `write_exam2_editor_harvest.py` | Post-process (reuse `write_exam3_editor_harvest` helpers) |
| `harvest/write_final_exam_review_data.py` | Regenerates map data from harvest JSONs |
| `harvest/fix_exam2_pools.py` | Re-parse My Selections text → fix poolOrder |
| `index.html` | Final Review Bank card (Exams 1–2 ready) |

**Also this session (Exam 4 unit map, still local):** re-pooled `exam4-review-map-state.json` (backup `exam4-review-map-state.before-repool.json`), part-count badges (`exam4-problem-load.js`), section summary, skill groups, pools UI. Chase loaded re-pool via **Load from repo**.

**Pearson leftovers:** `Exam 1 (Copy)` and `Exam 2 (Copy)` still exist in Assignment Manager. Delete when harvests for remaining exams are done (or when Chase says).

**Uncommitted:** all of the above under `School Scrips/School documents` (own git repo). No push.

## Open questions and constraints
- Exam 3: try live editor first (may be unlocked). If locked, traditional copy like 1–2.
- Exam 4: same; live Exam 4 may already have attempts.
- Final map still needs: add-to-final-review / pool building (like Exam 4 map), LaTeX polish pass if stems are rough, delete Pearson copies.
- Never display GUI without asking. Never deploy Netlify unless he says so in that message.
- Macro App MCP `macro-app` for Pearson; recipe copy-paste blocks; step fails → ask Chase.
- Context was already heavy when Exam 2 finished; keep Exam 3/4 harvests in the fresh task.

## Exact next step

1. Confirm Macro App Pearson is on Assignment Manager (or Chase has Exam 3 copy on Add/Remove Content).
2. If Exam 3 is unlocked: Edit → traditional → Add/Remove Content → full Next-loop harvest (same as Exam 1/2).
3. If locked: Copy Exam 3 → **traditional** Continue (wait for Send-grades checkbox) → harvest the copy.
4. Save raw to `harvest/exam3-editor-preview-raw.json` (or reuse existing Exam 3 harvest only after confirming it matches current Pearson; Chase said Exam 2/3 may be stale). Prefer a fresh harvest if unsure.
5. Wire into `write_final_exam_review_data.py` SOURCES + regenerate; show Exam 3 tab on the Final Review map.
6. Then Exam 4 the same way.

## Read first
- `School Scrips/Macro App/docs/Automations/PEARSON_EXAM_POOL_HARVEST.md`
- `School Scrips/School documents/harvest/HARVEST.md` (Exam 4 print notes; editor path is the pool doc)
- Exemplars: `harvest/write_exam1_editor_harvest.py`, `harvest/write_exam2_editor_harvest.py`, `harvest/fix_exam2_pools.py`
