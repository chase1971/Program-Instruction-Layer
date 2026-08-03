---
name: Per-student Graphing analysis export
overview: Enhance the Graphing Transformations "Save Analysis" to write an Excel file with a summary sheet, a detail sheet, and one sheet per student containing seen/missed counts, percentages for S4 parameters (A/B/C/D), and S4 step breakdown (transformation, XY column, operation). Use the full G1 payload to compute "saw X, missed Y, Z%" per student.
todos: []
isProject: false
---

# Per-Student Graphing Analysis Export

## What the code already has

The G1 completion code stores full per-problem, per-step data:

- **Payload shape** ([session_codec.py](C:\Users\chase\Documents\Programs\School Scripts\transformations-app\scripts\session_codec.py) `validate_graph_session_log` / `compute_graph_stats`): `log["ps"]` = 6 problems; each problem has `s1`, `s2`, `s3` (0/1) and `t4` = list of entries. Each `t4` entry has `p` in ("A","B","C","D") and `**tr`, `xy`, `op`** (0 = wrong, 1 = correct) for transformation choice, XY column question, and operation question.
- **Aggregate stats** already include `s4WrongByStep`: `tr`, `xy`, `op` (and `s4WrongByParam`: A,B,C,D). So the code has XY and operation; the current CSV detail table simply **does not write** `s4_tr`, `s4_xy`, `s4_op` per row (summary does aggregate them).

So we have everything needed to add:

- Per-student **S4 step** counts (transformation, XY, operation) and percentages.
- Per-student **S4 parameter** “seen / missed / %” from the raw payload (count `t4` entries by `p`, count wrong when any of `tr`/`xy`/`op` is 0).

## Scope (Graphing only)

- **In scope:** Graphing Transformations “Save Analysis” → multi-sheet Excel with per-student sheets and richer metrics.
- **Out of scope:** Identifying Transformations report stays as-is (single CSV); no Excel there unless you ask later.

## 1. Add per-student detail from the payload

When building the G1 report we already have `result = decode_graph_session(code)` which returns `result["payload"]` (full log). For each CSV row we will:

- Keep storing **first name and last name** from the Forms CSV (columns 1 and 2) so we can label sheets and rows.
- From the payload, compute per-student:
  - **S4 parameter** (A/B/C/D): for each param, count “seen” = number of `t4` entries with `p == param`, “missed” = number of those where `tr==0 or xy==0 or op==0`; then **% missed** = (missed/seen)*100 when seen > 0.
  - **S4 steps**: total S4 “slots” = total number of `t4` entries across 6 problems; for each step type (`tr`, `xy`, `op`) we already have counts in `st["s4WrongByStep"]`. So we can report “Transformation choice: X missed out of Y (Z%)”, same for XY column and operation.

Add a helper that takes `payload` (the decoded G1 log) and returns a small dict, e.g.:

- `s4_seen_A/B/C/D`, `s4_missed_A/B/C/D`, `s4_pct_A/B/C/D`
- `s4_total_slots` (total t4 entries)
- `s4_tr`, `s4_xy`, `s4_op` (wrong counts; we already have these in stats)
- Optionally per-problem summary (e.g. which function types they missed) for the student sheet.

Use this in `build_report_from_csv_g1` so each `detail_rows` entry (and any new “per_student” structure) includes these fields. Also add **first_name**, **last_name** (and keep **row_index**) to each detail row so we can label sheets.

## 2. Add S4 step columns to current detail table

In [build_report_from_csv_g1](C:\Users\chase\Documents\Programs\School Scripts\transformations-app\scripts\session_codec.py) (around 596–611), each `detail_rows` item currently does **not** include `s4_tr`, `s4_xy`, `s4_op`. Add them from `st["s4WrongByStep"]` so the existing “Detail” view/CSV includes transformation, XY, and operation counts per student.

## 3. Output format: Excel with multiple sheets

CSV does not support multiple tabs; Excel does. So:

- **Option A (recommended):** When the user clicks “Save Analysis as CSV” for Graphing, offer two behaviors, or replace with “Save Analysis as Excel” that writes a **.xlsx** file with:
  - **Sheet 1 – Summary:** Same as current summary block (total rows, valid count, wrong by stage, S4 by step, S4 by param, wrong by function type).
  - **Sheet 2 – Detail:** Current detail table plus columns for **S4 transformation (tr), S4 XY, S4 operation**, and optionally “seen/missed/%” for A,B,C,D so the single table has the percentages too.
  - **Sheet 3+ – One per student:** e.g. “Student 1 – First Last” (or “Row 2 – First Last” if name missing). Each student sheet contains:
    - Student identifier (name, row from CSV).
    - **Stages 1–3:** e.g. “S1 wrong: X/6”, “S2 wrong: X/6”, “S3 wrong: X/6”.
    - **Stage 4 – by parameter:** Table with columns like Parameter, Seen, Missed, % Missed (A, B, C, D).
    - **Stage 4 – by step:** Transformation choice: X missed out of Y (Z%); XY column: …; Operation: ….
    - Optionally: which function types they missed (quadratic/absolute/cubic/sqrt) for each problem.
- **Option B:** Keep “Save Analysis as CSV” as-is (single CSV with summary + detail, with the new S4_tr/xy/op and seen/missed/% columns in the detail table), and add a **second** button “Save Analysis as Excel” that produces the multi-sheet .xlsx above.

Recommendation: **Option B** so existing “Save as CSV” still works and gains the extra columns; new “Save as Excel” gives the tabs and per-student sheets.

## 4. Dependency

Writing .xlsx with multiple sheets requires a library. Use **openpyxl** (standard choice, no Excel needed). Add it for the scripts environment:

- Add a `requirements.txt` in [scripts](C:\Users\chase\Documents\Programs\School Scripts\transformations-app\scripts) (or project root) with `openpyxl`, and document that “Save as Excel” needs `pip install openpyxl` if not already installed.
- In [session_codec.py](C:\Users\chase\Documents\Programs\School Scripts\transformations-app\scripts\session_codec.py), import openpyxl only when writing Excel (or at top with try/except and disable “Save as Excel” if missing).

## 5. Implementation order

1. **Payload helper** – From a decoded G1 `payload`, compute per-student `s4_seen_`*, `s4_missed_`*, `s4_pct_*`, `s4_total_slots`, and use existing `s4WrongByStep` for tr/xy/op.
2. **Detail rows** – In `build_report_from_csv_g1`, add first_name, last_name (from CSV row), s4_tr, s4_xy, s4_op, and the new seen/missed/% fields to each detail row; ensure `write_report_csv_g1` writes the new columns so the single CSV is still useful.
3. **Excel export** – New function `write_report_xlsx_g1(summary, detail_rows, student_sheets_data, out_path)`. `student_sheets_data` = list of dicts (one per student) with name, row_index, and the per-student breakdown (stages, S4 by param with seen/missed/%, S4 by step with counts and %). Build Summary sheet, Detail sheet, then one sheet per student (name sheet “First Last” or “Row N” if no name). Use openpyxl; catch ImportError and show a message to install openpyxl if the button is used.
4. **GUI** – In the Graphing tab, add a “Save Analysis as Excel” button that calls the new writer; keep “Save Analysis as CSV” as-is (with the enhanced detail columns).

## 6. Edge cases

- **Seen = 0** for a parameter (e.g. no A questions in that problem set): show “0 seen” and avoid division; show “—” or 0% for % missed.
- **Sheet names:** Excel has a 31-character limit; trim long names to “First L…” or “Row 2 – First Last”.
- **Invalid characters** in sheet names (e.g. `\ / * ? : [ ]`): replace with space or underscore so openpyxl doesn’t error.

## Summary

- The **code already has** XY and operation in the payload and in aggregate stats; we just don’t currently put `s4_tr`, `s4_xy`, `s4_op` (or seen/missed/%) into the per-row detail. Adding that and a payload-based helper gives “how many they saw” and “% missing” per student for S4 parameters and for the three S4 steps (transformation, XY column, operation).
- **Save Analysis as CSV** continues to write one CSV with summary + detail, with new columns for S4 steps and for seen/missed/% per param.
- **Save Analysis as Excel** (new) writes one .xlsx with a Summary sheet, a Detail sheet, and one tab per student with the detailed breakdown you asked for, using openpyxl.

