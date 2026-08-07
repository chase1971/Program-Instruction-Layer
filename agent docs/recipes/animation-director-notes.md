# Animation director notes

> **You might say:** "implement the director notes", "the pending animation file"
> **What it is:** Animation Studio director notes — read pending file and implement
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/animation-director-notes.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `**/AnimationStudio*.tsx`
- `**/FrameDirectorNotesPanel.tsx`
- `**/animationDirectorNotes*.ts`
- `**/ANIMATION_DIRECTOR_PENDING.*`
- `**/animation-library/**/spec.json`

---

## Workflow (Chase's model)

1. Chase stops playback on a reference scene and saves a **director note** in Animation Studio.
2. The app writes open notes to **`docs/ANIMATION_DIRECTOR_PENDING.json`** and **`docs/ANIMATION_DIRECTOR_PENDING.md`**.
3. **Cursor reads that file and implements the note** — update storyboard frames, expression layout, link groups, and live app code as needed.
4. **No in-app "Apply" button.** Save note → AI implements. Period.

## When this applies

- User mentions director note, preview note, "do what the note says", Animation Studio feedback while watching playback
- File `docs/ANIMATION_DIRECTOR_PENDING.md` exists with open notes

## Required first step

1. Read **`docs/ANIMATION_DIRECTOR_PENDING.md`** (or `.json` for frame snapshot data).
2. Open the linked animation: **`animation-library/{slug}/spec.json`** or saved catalog entry by `specId`.
3. Use **reference scene number** (`frameNumber`) as the layout/motion exemplar.
4. Implement the note text literally — may require reworking all following frames and the live sandbox widget.

## Division bars

When the note references fraction/division bar alignment:

- Read reference frame's `division-bar` expressions (rectPct, linkGroupId).
- Apply to matching bars on later frames **by index** (first bar under term 1, second under term 2).
- Copy `expressionLinkGroups` from the reference screen when linking is part of the reference.

## After implementing

- Update `animation-library/{slug}/spec.json` and republish if needed
- Mark note `status: "done"` in spec `previewNotes` or clear pending files
- Tell Chase to reload Animation Studio and replay preview
