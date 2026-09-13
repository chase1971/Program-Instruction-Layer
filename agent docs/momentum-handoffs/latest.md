# Momentum handoff — Matrix portal polish shipped

**Written:** 2026-09-13 (Sunday, evening)

---

## Objective and current phase

Matrix Gauss-Jordan pilot polish: landscape phone UX, Teacher Console admin preview tools, save-status copy, instructor skip-gates default, Matrix Grades refresh. **Current phase:** portal deploy **#17** live; Macro App TC changes remain **local uncommitted**.

---

## Resolved — CHASE1 empty grades

**Not a bug.** Chase confirmed he was in **Teacher Console preview** (preview version). Preview runs do not write grades to Supabase — expected. Real student links (`/?s=CODE` without preview embed) record normally (verified: phone Part 1 completion showed in grades).

---

## Deployed to production (Netlify deploy #17)

- Red header save status: `retrying` ("Trying again…") vs `blocked` (close other sessions, reopen)
- Instructor phone link with no `previewSkipGated` param **defaults to skip gates**
- TC preview still sends explicit `previewSkipGated=0|1` when toggling
- Fullscreen button, landscape touch check, tutorial copy tweaks (bundled with prior local work)

**Live:** https://mathappsclass.netlify.app · bundle `index-BRzyLe4p.js`

---

## Macro App — local only (restart Macro App to pick up)

- Teacher Console **Refresh grades** on Matrix Grades tab + auto-refresh on tab switch
- Admin preview tools (skip gated toggle, reset progress)
- `portalPreviewUrl.ts` always sets `previewSkipGated=0|1`

---

## Not committed

Per Chase — no git commits this session. Dirty repos: `student-portal`, `Macro App`, agent docs handoffs.

---

## Copy-ready fresh-task prompt

Continue Matrix M1324 pilot from deploy #17. Macro App TC changes need a Macro App restart (or commit when Chase asks). For real grade testing use the student link, not TC preview embed.
