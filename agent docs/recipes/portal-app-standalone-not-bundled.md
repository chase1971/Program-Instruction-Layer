# Portal apps are separate — never bundle into an existing app

> **You might say:** "make a new app for this course", "it's a separate app", "don't combine it with matrix",
> "this has nothing to do with the other apps", "stop putting things together"
> **What it is:** Product rule — each portal app Chase names is its **own** app (activity, feature, TC row).
> It is **not** a submodule of Matrix, Transformations, or "whatever we already ship for that course."

**Exemplar files — read these before wiring:**

- **Separate apps (copy this shape):** `student-portal/src/features/transformations/` + `transformations/*` activity ids;
  exit tickets (one activity per ticket, own TC row)
- **Pipeline checklist (all six places):** `School Scrips/student-session-kit/docs/STUDENT_PROGRESS_PIPELINE.md` § Adding a new app today
- **Catalog (split products):** `Macro App/renderer/src/utils/teacher-console/teacherConsoleBuiltInCatalog.ts`
  — `builtInLogicHomeworkActivities` vs `builtInMatrixCourseActivities`
- **Portal tile gate:** `student-portal/src/config/portalAccess.ts` — `hasLogicHomeworkAccess` + `sectionGate: 'logic'`
  in `portalHomeApps.ts` (not `matrix`)

---

## Why this exists

Speech-to-text and shorthand ("logic for M1324", "another matrix app") push agents to **extend**
an existing course bundle: same Teacher Console switcher list, same portal section gate, same
feature folder patterns. Chase's model is **one named app at a time** — new activity, new route,
new TC enable/responses row — with **no implied relationship** to apps already on the portal.

Bundling silently removes the teacher path (wrong catalog course, hidden switcher, "no way to activate").

---

## The rule

When Chase says **new app** (for any course):

1. **New Supabase activity** (`activities.id`) — not an extra screen inside another activity's id.
2. **New `student-portal/src/features/<name>/`** — not "add a panel to matrix-tutorial" unless he
   explicitly asked to extend that product.
3. **New home tile + route** — own entry in `portalHomeApps.ts` (or classwork path), own hash in
   `usePortalRoute.ts`, own branch in `App.tsx`.
4. **New Teacher Console catalog row** for the **course that owns the app** in
   `builtInActivitiesForCourse` — not "append to M1324 because matrix is there" unless he said
   this app **is** part of that product.
5. **Access, responses, and roster** follow **`logic/problems`-style activity id** end to end —
   one id for `student_app_access`, submits, and TC `activityId`.

Matrix Part 3 as an **embedded repo** is still one app: separate activity id and portal host,
not "more matrix tutorial steps."

---

## Non-negotiables (each prevents a real bug)

| Do not | Bug it causes |
|--------|----------------|
| Add the new app only inside an existing feature folder | No isolated deploy, access, or grades; TC can't target it |
| Reuse another app's activity id for a second product | Activate/responses/submit fight over one row |
| Put the app only in Preview/instructor bypass | "Works for me" but no student tile or TC Activate |
| Assume **course code ⇒ one switcher bucket** | Teacher Console shows no app / wrong course (e.g. logic only on M1324 list) |
| Merge checklist steps into "we'll piggyback on X" | Migration missing, `PROGRESS_ROSTER_APPS` missing — saves vanish from TC |

---

## Anti-patterns

- "It's for M1324 so it goes with Matrix Tutorial in the catalog."
- "Same section gate as matrix" without Chase choosing that coupling.
- One `MarginTeleport` / instructor shortcut treated as the **student** path (teleports ≠ roster Activate).
- Skipping Macro App because "portal is enough" — **Activate all** and **Responses** live in TC/Roster.

---

## When bundling *is* OK

Only when Chase **explicitly** asks: e.g. "add a third part to matrix tutorial", "another clip in
Conics", "new exit ticket." Then extend **that named product**, still with a **distinct activity id**
when grades/access must be separate (Transformations Part 1 vs Part 2 pattern).

---

## Related

- Full wiring list: `STUDENT_PROGRESS_PIPELINE.md` § Adding a new app today
- Access gates: [portal-assignment-gate.md](./portal-assignment-gate.md)
- student-portal `AGENTS.md` — keyword row for "add an app to the portal"
