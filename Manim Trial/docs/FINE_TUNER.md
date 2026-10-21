# Fine-tuner instructions (stage 3)

> The premium fine-tuner reads **this file and the brief, nothing else** unless it hits a problem.
> Do not read the docs tree. Why this exists and how it is measured:
> [FINE_TUNE_PIPELINE.md](FINE_TUNE_PIPELINE.md). How the brief is written: [FINE_TUNE_BRIEF.md](FINE_TUNE_BRIEF.md).

**Job, narrow on purpose:** look at the frames, find things colliding or out of place,
reposition or rescale so everything is visible. Nothing else.

All commands run from `Manim Trial/` in PowerShell. No window, preview or player opens.

## Does

1. Read the brief, the scene file, the audit JSON and the contact sheet it names.
2. Move or rescale elements to fix collisions and unreadable placement. Use `fit_into` and the
   named regions `DIAGRAM`, `WORK`, `GAUGE`, `CENTER` from `scene_layout.py`. Keep related
   objects built from one `view` (origin plus scale) and animate with `rebuild(mob, lambda alpha: ...)`,
   so nothing is positioned after it is built.
3. Draft render without strict mode first, so every mark's problems print in one pass:

       $env:PATH = (Join-Path $env:LOCALAPPDATA 'Programs/MiKTeX/miktex/bin/x64') + ';' + $env:PATH
       & '.\.venv\Scripts\python.exe' -m manim -ql --disable_caching <module>.py <SceneClass>

   Read the `[audit]` block (small) before generating any image.
4. Regenerate the sheet and look again:

       & '.\.venv\Scripts\python.exe' contact_sheet.py <module>

5. When the sheet reads well, confirm with `$env:MANIM_AUDIT_STRICT = '1'` and the same render
   command. A nonzero exit means a mark is still not clean.

## Keeping rounds few

Every round re-reads everything before it, including images, so rounds are the cost.

1. Fix **everything visible in the sheet in one edit**, then one re-render, one new sheet.
2. **Round cap: 3.** Stop and report what is left. A problem that survives 3 rounds is
   probably structural; say so.
3. Rounds after the first look at **crops** of the broken marks, not the full sheet.

## Never does

- change math values, caption text or timing;
- **delete or hide an element to resolve an overlap** (the audit reports an absent element as
  clean, so this is a silent regression; relocate it instead);
- edit `scene_audit.py`, `scene_layout.py` or the test files;
- run the final 1080 render, `build_page.py`, or portal wiring (the builder owns "done");
- open a window, preview or player;
- use em dashes in any on-screen text it touches.

A contact sheet shows sampled frames, not movement. Do not claim motion is verified; list
suspected motion problems separately. Problems that need broader changes get reported, not
rewritten.

## Returns (under 10 lines)

Marks changed and how, marks still unresolved and why, rounds used, final strict-audit result.
No narration of the process.
