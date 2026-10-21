# Build mode: put a planned box in the app

> **You might say:** "put this text box in the app", "I've made some changes, reload it",
> "put it in the app", "implement this box", "make the ghost real"
> **What it is:** AI reads the app's `buildLayout.json`, consumes each `planned` rect as a
> real element with the same `id`, and flips `status` to `implemented`. Moves and resizes
> are already source. AI is only for this flip.

**Exemplar files. Read these before writing code:**

- Layout file (source): `School Scrips/student-portal/src/features/build-playground/buildLayout.json`
- Types + load: `buildLayoutTypes.ts`, `loadBuildLayout.ts`
- Consume rect as `%`, never leftover pixel CSS: `rectPctStyle.ts`
- Render implemented only: `BuildPlaygroundView.tsx` (`implementedElements` + `data-build-element-id`)
- Architecture: `School Scrips/Macro App/docs/plans/BUILD_MODE_LAYOUT_EDITOR_PLAN.md`

If the first message in the chat is a **visual complaint about Build** (wrong phone slot,
navy/empty canvas, orientation, notch, extra scroll), fix that path instead. Do not start
this recipe on a dead canvas. Shared chrome and playground CSS live in
`TeacherConsolePreviewPhoneChrome.tsx` and `build-playground.css`.

---

## Mental model

The layout file is the one copy of positions. Build writes it when Chase adds, moves, or
resizes. Vite reload then updates Build and Preview together.

| Status | What the app draws | What Build draws |
|---|---|---|
| `planned` | nothing | ghost + handles |
| `implemented` | real element at `rect` | selection chrome only |

Chase does not need AI to move an implemented box. If he only moved things, say that and
stop.

---

## Do this, in order

1. **Read the live file** on disk: that app's `buildLayout.json`. For the proof that is
   `student-portal/src/features/build-playground/buildLayout.json`. It is Chase's testing
   file. Never empty it, never reset `revision`, never restore a seed.
2. **Find `planned` entries.** Use the ones he named, or every `planned` row if he said
   "put this in the app" after placing boxes. If there are none, say so and stop. Do not
   invent boxes.
3. **Consume `rect` directly.** Same `id`, same `rect` (`xPct` / `yPct` / `wPct` / `hPct`).
   Place with `rectPctStyle` (or the same `%` `left` / `top` / `width` / `height`). Do not
   translate into `px`, a second coordinate system, or "about where it was."
4. **Flip `status` to `implemented`.** Keep `role` and `placeholder` unless he gave new
   copy. Leave `revision` as Build wrote it.
5. **Run headless tests.** From `student-portal`:
   `npx vitest run src/features/build-playground`
   Update `loadBuildLayout.test.ts` if it still expects zero `implemented` rows. That
   assertion was the Phase 2 empty seed, not a rule. Portal `tsc --noEmit` has unrelated
   failures. Ignore those. Do not launch Macro. Do not open a browser.
6. **Hand Chase a flat reload-and-expect statement.** Then stop.

On the proof playground, `BuildPlaygroundView` already maps every `implemented` element
through `rectPctStyle`. Flipping `status` **is** the consume step. Do not add a second
hardcoded box, a second feature folder, or a new portal tile.

`BuildPlaygroundView` loads the file in `useMemo(..., [])`, so a file edit may not paint
until he Reloads. That is why the handoff is reload, not "it should already be there."

---

## Handoff (statement, never a prompt)

Reload Build. The ghost body should be gone and the real text should sit where you placed
it. Preview should show the same text in the same place.

Do not ask him to run it. Do not offer to open a window. Do not deploy.

---

## Do not

| Do not | Why |
|---|---|
| Create a second testing app, tile, or desktop window | The playground **is** the white testing page |
| Restore or empty `buildLayout.json` | It is his live file (moves, revision, `text-1`) |
| Give Build its own bezel, holder scale, or a `--build` class that hides the landscape spacer | Shared chrome is `TeacherConsolePreviewPhoneChrome`. Preview and Build must share the phone slot |
| Rewire `useBuildStageScale` | Leftover. Unused after shared chrome |
| Write through `POST /__layout/build/...` for this flip | That route is for Build overlay writes. Edit the source file |
| Silent-fail a missing write, or "fix" a down docs server by skipping it | Overlay writes must stay visible failures. This recipe is not an overlay write |
| `npm run deploy:prod` / Netlify | Proof is Preview only (`127.0.0.1:5340`) |
| Open Macro, a browser, or any GUI unless he asked in **this** message | Permission is per run |
| Restyle the playground navy, or restyle ghosts | Canvas is white. Ghosts stay the overlay dashed boxes. Implemented text is dark on white (`.build-playground-text`) |

---

## Later apps (only if that app already has the Build contract)

Same file shape, same `id`, same `rectPctStyle` consume, same status flip. Scaffold a new
app with the contract only when he asks to start that app. Do not migrate Factoring here.
Do not treat "build a white testing app" as a new product.

---

## Related

- Plan and phases: `School Scrips/Macro App/docs/plans/BUILD_MODE_LAYOUT_EDITOR_PLAN.md`
- New portal product (not this): [portal-app-standalone-not-bundled.md](./portal-app-standalone-not-bundled.md)
- Display permission: `agent docs/rules/never-display-without-permission.md`
