# Momentum handoff: pixel-office explainer animations (Macro App office, documentation office, docs vs no docs)

**Written:** 2026-11-05. Valid for today's continuation only.
**Nothing is committed or pushed.** No Netlify deploy. All pages are headless-verified (Edge via Playwright screenshots), not viewed live by Chase except through the links below.

## Objective and current phase

Chase is starting to make presentations about how he develops with AI. He wants **animated pixel-art "office" scenes (robots at desks, like a Facebook post he saw)** as a way to explain concepts to people: how his documentation is structured, and why AI fails without it (more tokens, god files, rewrites, duplicates, context overflow). The scenes do not need to connect to anything real. They only need to act the way an agent acts. Phase: three finished pages; he loved the last one and asked for small additions, which are done. Next is more scenes or polish, per his lead.

## Chase's desired feel
- "I love this." Realistic agent behavior: the robot walks to the files, reads them, and **thinks out loud in speech bubbles that justify each step** ("what are the rules I have to follow").
- A **fake token counter** is fine for now (could be real later by running a task and counting).
- Show the **bad version** as escalating real failure modes: wandering, god file, rewrites you did not ask for, duplicates, context full, and what happens after.
- He is a teacher; audience is people who might want to learn this setup.
- Flat panels labeled as "rooms" were **rejected**. It must look like the screenshot: brick wall with string lights, desks with monitors, robots at desks, plants, coffee machine, meeting table.
- He chose the **robot** sprite (one of five options) and the **assembly line (conveyor belt)** layout for the Macro App.

## Accepted decisions
- Robot sprite, 12x16 pixels, recolored per group. The agent robot is gold (`#ffd84a`); the root AGENTS desk is red so it does not match the agent.
- Macro App scene: assembly-line layout (D2L and Pearson wall screens, workshops, control room with Teacher Console, conveyor, Student Portal with Supabase server racks). The Student Portal is drawn as its own space.
- Documentation scene: one good-docs office where a gold agent walks root `AGENTS.md`, `INDEX.md`, recipes, an app's keyword-table `AGENTS.md`, one doc from a `docs/` cabinet, then `SESSIONS.md`.
- Docs vs no docs: **split screen, same four tasks at the same time**, stacked top (with docs) and bottom (no docs), with token bars as the race. Tabs: Side by side, With docs, No docs. Task jump buttons, Pause, Restart, Speed 1x/2x.
- A **commentary box in the lower right** of each office: per-step remarks, token cost remarks, and a red ERROR explanation matching the red badges.
- After context is full the bad agent: compacts (bar drops, rules lost), then **deploys to production unasked**, then Chase has to start a new chat. Ends in FAILED.
- Token numbers, routes, and thoughts are illustrations (labeled so on the pages).

## Rejected directions
- Panel-style floor plans (the first `macro-app-floorplans.html`, deleted).
- Five-plan comparison page is superseded; Chase picked plan 5.
- Not asked: connecting this to live Claude Code. Explained only: hooks give one-way events with no API needed; talking to agents would need a local server calling `claude -p`. Parked, not built.

## Current implementation state
All in `agent docs/scratch/` (served at `http://127.0.0.1:8765/scratch/<file>`), each a **self-contained HTML file** with inline JS. Edit the HTML directly. The build scripts lived in the old session scratchpad and may be gone; do not rely on them.

| File | What it is |
|---|---|
| `pixel-agents.html` | Five agent sprite designs (robot chosen) |
| `macro-app-offices.html` | Five Macro App office layouts. Its top half is the shared engine (`R`, `bricks`, `floor`, `carpet`, `partition`, `monitor`, `robot`, `Plan`, `sceneBg`, `sceneFg`) that the later pages copy |
| `documentation-office.html` | Good-docs office, one agent, thought bubbles, fake token counter and bar |
| `docs-vs-no-docs.html` | The split-screen race (latest and best) |

Published once as a **private** Claude artifact: `https://claude.ai/artifact/7ctUctmg2F2uZUtrnngETu` ("Macro App Office", assembly line only). Chase has **not** asked to publish the documentation pages. Say "publish it" is the offered phrase.

Engine notes for `docs-vs-no-docs.html`: pixel canvas 640x236 per side; HTML labels, bubbles, and the commentary panel are overlays positioned in percent and sized in `cqw`; routes are `GOOD` and `BAD` arrays of `S(x, y, thought, highlight, readsFile, tokens, {fx, prob, note})`; `fx` events (pile, dupe, rewrite, collapse, compact, deploy) drive the scene; `prob` strings become red badges; loop is about 164 s with `starts[]` per task. Sim clock `sim` drives everything so Pause works.

## Open questions and constraints
- "Split these up as separate taps": I read it as tabs for the two offices. Not confirmed; ask if he meant something else (for example separate pages per task).
- Windows head-mouse user: **never put anything on his screen unprompted** (root `AGENTS.md`). I verified via headless Playwright with `channel: 'msedge'`. Links go to him as `http://127.0.0.1:8765/...` only. Server `scripts/serve-programs-docs.js` must be running on 8765.
- No em dashes anywhere in written text.
- Publishing is outward-facing: only on his word.

## Exact next step
Ask Chase what he wants next, with these likely candidates: publish `docs-vs-no-docs.html` as a Claude link; build another "what goes wrong" scene; or use the real thing (run one task with and without docs and replace the fake token numbers). Do not start building without his pick.
