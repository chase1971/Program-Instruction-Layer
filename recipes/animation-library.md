# Animation library

> **You might say:** "reuse an animation", "animation template", "port an animation"
> **What it is:** Animation library — reusable code templates in @canvas-kit (discover, adapt, port), plus legacy snapshot library
> **Source:** converted from `School Scrips/Math App Studio/.cursor/rules/animation-library.mdc` on 2026-08-02 (was a Cursor glob rule that almost never fired).

**Exemplar files — read these before writing new code:**

- `**/canvas-kit/src/animations/**`
- `**/ANIMATION_TEMPLATE_PENDING.*`
- `**/AnimationTemplate*.tsx`
- `**/animation-library/**`
- `**/AnimationStudio*.tsx`
- `**/animationGuide*.ts`
- `**/animationPlaybackPlan.ts`

---

Two systems exist. **Code templates are the current, preferred model.** The
snapshot storyboard library below is **legacy** (kept working until explicitly
retired).

## When this applies

User mentions: "use our library {id} animation", division animation, a reusable
animation for a math problem, adapt/port an animation template, animation
template feedback, or edits under `canvas-kit/src/animations/`.

---

## Code templates (preferred)

A template is **pure code**: a param schema + an ordered list of **beats**
(labeled moments an element enters/changes, each with a hold time) + a `render`
that draws the visual state at a beat index. Smoothness comes from CSS keyframe
entrances (`canvas-kit/src/animations/animation-templates.css`) that fire as
each element mounts. **Beats = the "frames"** shown in the Studio's Edit mode —
an editing lens, never the source of truth.

### Discovery (source of truth — do not maintain a duplicate index)

1. **`School Scrips/canvas-kit/src/animations/index.ts`** — the
   `animationTemplateRegistry` lists every built-in template. This file is the
   index; there is no `index.json` for code templates.
2. Each template lives in **`canvas-kit/src/animations/templates/{id}/`**:
   - `{Name}Template.tsx` — `render` + `beats` + the `AnimationTemplate` object
   - `{id}Beats.ts` — the reveal sequence (beat labels + hold times + which
     elements are visible at each beat)
   - `{id}Params.ts` — the param schema (`*_PARAM_FIELDS`) with defaults + a
     `to{Name}Params` resolver
3. Template shape is defined in **`canvas-kit/src/animations/types.ts`**
   (`AnimationTemplate`, `AnimationBeatMeta`, `AnimationTemplateParamField`).

Current templates: **`division`** (params: `term1`, `term2`, `gcf`,
`quotient1`, `quotient2`, `rightSide`).

### Adapt a template to a specific problem (params only — do NOT fork)

Templates are parameterized so the same code serves every problem. To reuse one:
override its param defaults; never copy-paste the render into a new template for
a one-off problem.

```ts
import { animationTemplateRegistry, useAnimationTimeline } from '@canvas-kit';

const template = animationTemplateRegistry.get('division')!;
const timeline = useAnimationTimeline(template, {
  loop: true,
  params: { term1: '6a^4', term2: '9a^2', gcf: '3a^2', quotient1: '2a^2', quotient2: '3', rightSide: '= 0' },
});
```

Add a genuinely new *kind* of motion (not a new problem) → author a new template
folder under `templates/{id}/` following the division exemplar, then register it
in `index.ts`. Grep the registry first; extend before adding.

### Port a template into a math app

1. `import { animationTemplateRegistry, useAnimationTimeline } from '@canvas-kit';`
2. `import '@canvas-kit/animations/animation-templates.css';` (once) for the
   entrance keyframes.
3. Drive it: `const t = useAnimationTimeline(template, { loop, autoPlay, params });`
4. Render: `template.render({ beatIndex: t.beatIndex, params: t.params })`.
5. Playback controls if needed: `t.play() / t.pause() / t.restart() / t.seek(n)`.

Leave the old bespoke animation in the target app untouched unless Chase asks to
replace it — the plan is to port the refined template in deliberately.

### Template feedback handoff (Studio → Cursor → rebuild)

Chase leaves notes on a template in the Studio (a general note in Preview, or a
per-beat note in Edit). The app writes them to
**`docs/ANIMATION_TEMPLATE_PENDING.md`** (+ `.json`). When that file has open
notes:

1. **Read `docs/ANIMATION_TEMPLATE_PENDING.md` first.**
2. Edit the template code under `canvas-kit/src/animations/templates/{id}/`
   (beats / render / params) so each note holds for its beat **and everything
   after it** (a note on beat N applies from N onward).
3. No in-app "Apply" button. Save note → AI edits template code → HMR/reload →
   Chase replays. Clear the pending file once addressed.

---

## Legacy: snapshot storyboard library

> Kept working until explicitly retired. Prefer code templates for anything new.

- Discovery: **`animation-library/index.json`** → `animation-library/{id}/guide.md` + `spec.json`.
- Reference by id (e.g. `slide-into-chain`) instead of re-deriving; the spec is architecture.
- Generate mode: follow `animation-library/GENERATION_TEMPLATE.md` — write `spec.json` + `guide.md`, update `index.json`.
- Director notes for snapshots: see **`animation-director-notes.mdc`** and `docs/ANIMATION_DIRECTOR_PENDING.md`.
- Implementation: storyboard frames are **key poses**, not slideshow playback; final frame = target layout; use `@canvas-kit` `renderKatexHtml` + exemplar SQ CSS.
