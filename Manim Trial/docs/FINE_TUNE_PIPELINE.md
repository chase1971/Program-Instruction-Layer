# Fine-tune pipeline: cheap builder, premium fixer

> **You might say:** *"fine-tune the animation"* · *"hand it to the fine-tuner"* · *"cheap build, premium fix"* ·
> *"fix the collisions with the premium model"* · *"benchmark the animation workflow"*
>
> **Status: docs built 2026-10-21, never run.** The builder's side is
> [FINE_TUNE_BRIEF.md](FINE_TUNE_BRIEF.md), the fine-tuner's side is [FINE_TUNER.md](FINE_TUNER.md),
> and a `manim-fine-tuner` agent stub exists for each tool (Platform notes). No clip has gone
> through it and no benchmark has been run. **UNVERIFIED** marks what the first run must confirm.

---

## Goal

Make math animations (about a minute each) cheaper in **premium-model allowance** at the same
speed and quality. Premium tokens are the metric that matters. Total tokens are secondary.

Chase often does not know exactly what he wants until he sees the clip, so revisions are
normal. The pipeline has to make a revision round cheap, not just the first build.

## The pipeline

| Stage | Who | Context | Job |
|---|---|---|---|
| 1. Build | **cheap model**, Chase's normal session | whatever the session has | Write the whole clip and its functionality. Draft render. Fix errors until it renders. |
| 2. Audit and visual pass | **cheap model with image support**, same session | same | Apply the numeric audit fixes once, then inspect the updated contact sheet and make one batch of visual corrections. Follow the bounded pass below. |
| 3. Fine-tune | **premium model**, **fresh context** | only the brief (below) | Look at the contact sheet, fix collisions and positioning, stop. |
| 4. Revise | **cheap model** | normal | Later changes (wording, new beats). Layout is already settled. |

No isolation or delegation is needed for stages 1, 2, 4. Only stage 3 needs a clean context.
Stage 3 can be a subagent called from the builder, or a separate premium session Chase opens.
**Build the brief file first** (works in every tool); a subagent is a convenience on top.

### Cheap visual review (stage 2)

One bounded pass: checklist, one batch of corrections, no second cheap loop. The procedure and
checklist live in [FINE_TUNE_BRIEF.md](FINE_TUNE_BRIEF.md). The premium model still reviews the
sheet independently, even if the cheap model reports no problems.

**Hypothesis, not a measured saving:** this bounded pass may catch obvious defects before
premium review. Include its image, token and time overhead in the benchmark.

### What the fine-tuner is for (first version)

**Narrow on purpose:** look at frames, find things colliding or out of place, reposition or
rescale so everything is visible. Nothing else. Chase wants to find out whether that alone is
enough. Widen the job later only if a trial shows a real need (motion, construction).

**Do not conclude from the 2026-09-26 trial that cheap models can't build these.** That clip may
have failed partly because Chase was still deciding what he wanted. See
[CHEAP_MODEL_TRIAL.md](CHEAP_MODEL_TRIAL.md). It does record that the audit let a cheap model clear
every layout finding, and that placement bugs were structural (see "Protecting the fix").

## Why this should save tokens

Every turn re-sends the whole conversation. Cost grows with the **square** of the number of
render-look-edit rounds, because round N re-reads rounds 1 to N-1, including every frame image.
Cached re-reads are billed cheaper but still count.

The fine-tuner **avoids paying premium rates for**:
1. the output tokens of writing the clip,
2. the reading the builder did to start (style recipe, guardrails, a sibling clip),
3. the build conversation (errors, failed renders, Chase's back-and-forth).

The fine-tuner **still pays for**: one read of the finished file (about 4 to 6k tokens), the
frame-checking rounds, and the always-on instructions every agent loads (about 6 to 8k tokens;
root `AGENTS.md` is 18 KB).

**Unknown, do not guess:** what share of past animation cost was before the first render versus
the check loop. If the loop is most of it, savings are smaller. Measure first (see Baseline).

### Keeping rounds few

Fix everything visible in one edit, round cap 3, crops after the first round. The rules live in
[FINE_TUNER.md](FINE_TUNER.md) because the fine-tuner is the one that follows them.

## The brief and the fine-tuner's spec

- **Brief** (the only thing the fine-tuner is told): template and procedure in
  [FINE_TUNE_BRIEF.md](FINE_TUNE_BRIEF.md). Written to `Manim Trial/media/fine-tune/`, untracked.
  A smaller, scene-specific cousin of `agent docs/MOMENTUM_HANDOFF.md`; it does not replace it.
- **Fine-tuner spec**: [FINE_TUNER.md](FINE_TUNER.md). Kept separate from this file so the
  premium model reads about 60 lines, not this whole plan.

## Protecting the fix (stage 4 and the builder)

Cheap edits after the fine-tune can undo it. Mitigations that already exist in the repo:
- Build objects from one `view` (origin plus scale) and animate with `rebuild(mob, lambda alpha: ...)`,
  so nothing is positioned after it is built. This removed three placement bug causes in the
  2026-09-27 re-cut (see the end of `CHEAP_MODEL_TRIAL.md`).
- Run `MANIM_AUDIT_STRICT=1` after any later edit; a nonzero exit means layout regressed.
- The builder should use that `view` pattern from the start, so stage 3 has less to fix.

## Platform notes

The shared spec ([FINE_TUNER.md](FINE_TUNER.md)) is tool independent. Per-tool files are
**stubs** named `manim-fine-tuner` that point there and add only the model. Do not copy this content into them. Root `AGENTS.md` and each
tool's existing hooks (`.claude/`, `.codex/`, `.cursor/` all call `scripts/scorecard-hook-tally.js`)
are the existing shared mechanism; keep using them and do not add `.cursor/rules/*.mdc`
(retired 2026-08-02).

| | Cursor (**primary**) | Claude Code | Codex |
|---|---|---|---|
| Why | Most-paid plan. Chase estimates the cheap model gives about 9 times the usage of the premium one (his figure, unmeasured here). | Where most animation work has been done so far. | Occasional use. |
| Builder model | cheap Cursor model (`composer-2.5-fast` was the one trialled) | Sonnet-class | cheap Codex model |
| Fine-tuner stub | `.cursor/agents/manim-fine-tuner.md`, `model: claude-opus-5-5[effort=medium]`. Format per [Cursor subagents docs](https://cursor.com/docs/subagents.md) (checked 2026-10-21). **UNVERIFIED:** that exact model ID; the docs only show the bracket syntax. First run: the subagent's task card must name Opus | `.claude/agents/manim-fine-tuner.md`, `model: opus` | `.codex/agents/manim-fine-tuner.toml` ([Codex subagents docs](https://developers.openai.com/codex/subagents)). No `model` pinned, so it inherits the parent's; pin one when a premium Codex model is chosen |
| Invoke | `/manim-fine-tuner brief is at <path>` | ask for the subagent by name | ask Codex to spawn it by name |
| Always works | Chase opens a premium chat and says "fine-tune <Scene>, brief is at <path>" | same | same |
| Usage visibility | Dashboard usage CSV only (see "Cursor usage data" below). The agent cannot see its own usage, and `scripts/cursor-token-scan.py` now returns zeros (checked 2026-10-21) | Transcripts under `~/.claude/projects/` have per-message token counts (input, cached, output, model) | **UNVERIFIED** |

Known limits to state rather than hide:
- Delegation, model routing and context isolation are **not identical** across the three tools. If a
  tool cannot route a subagent to a chosen model, the fallback is the manual premium session.
- Subagents probably still load root `AGENTS.md` (about 4.6k tokens). Accepted: it is cached and small.
- Cursor also reads `.claude/agents/` and `.codex/agents/`; on a name clash its own `.cursor/`
  file wins, which is why all three stubs share one name.
- Reported tokens are not subscription allowance. Cursor and Claude bill allowance differently.

### Cursor usage data

Cursor no longer writes token counts to its local `state.vscdb`; every recent chat reads zero.
The source is the dashboard export (`usage-events-<date>.csv`), one row per request with columns
`Date, Model, Input (w/ Cache Write), Input (w/o Cache Write), Cache Read, Output Tokens,
Total Tokens, Cost`. `Cost` reads `Included` on Chase's plan, so it gives no dollar figure.

There is **no chat ID column**, so a run is attributed by time window and model:
- During a benchmark run, **no other Cursor chats run in parallel**, or their rows mix in.
- Record the run's start and end time; after the run, download the CSV and sum rows in that
  window by model.
- Parent and fine-tuner subagent separate cleanly only because they use different models.

## Baseline and benchmark

**Baseline first, no new building:** scan past Manim Claude transcripts and total fresh input,
cached reads, output and image counts, split at the first render. This says whether the check loop
really is the expensive part. Cursor baseline from the dashboard CSV, by time window, only for
past sessions that ran without parallel chats.

**Then a comparison on the same task, same completion criteria, from the same project state
(separate copies of `Manim Trial`, not a shared tree; a git worktree lacks `.venv`, MiKTeX and `media/`):**

| Arm | Workflow |
|---|---|
| A | Premium model does everything in one session (Chase's current habit). |
| B | Cheap build, numeric audit plus bounded cheap visual review, premium fine-tune in a fresh context (this pipeline). |

Optional arm C: same as A but with a fresh premium session for the check loop only, to separate
"isolation helps" from "cheap builder helps".

Record per run, **only what a platform reports** (leave blank otherwise, never estimate):
premium tokens, cheap tokens, input, output, cached input, parent versus subagent, agent calls,
fine-tune rounds, minutes to an acceptable clip, strict-audit result, final render status.
Where nothing is reported, enter numbers by hand from the provider dashboard.
In the run notes, record whether the cheap visual pass ran, what it corrected, and what the
premium review still found. Include the cheap visual pass in total usage and elapsed time.

Store as a CSV (one row per run) at `Manim Trial/benchmarks/runs.csv` plus a note column.
Do not build a new tracking system: extend `agent docs/session-scorecards.jsonl` conventions if a
field fits, and keep this file separate if it does not.

**Quality is judged by Chase** in the app, using the same rubric for both arms: nothing overlaps,
everything is readable, the teaching order is intact. One run per arm is an anecdote; run at least
three clips per arm and say so in the report. **Do not claim savings the numbers don't show.**

Report: premium-token difference (primary), total-token difference, fine-tune rounds, minutes,
and whether Chase judged the two clips equivalent.

**Weight before comparing.** Cache reads dominate raw totals (one Sonnet request in the
2026-10-21 export: about 230k fresh input, 6.1M cache read) and bill at a fraction of fresh
input. Compare each arm as tokens times the model's published per-token price for input, cache
write, cache read and output, not as `Total Tokens`. The same applies to the "cost grows with the
square of rounds" argument above: most re-read tokens are cached, so measure, do not assume.

## Open questions

1. Does a layout-only fine-tuner produce a clip Chase accepts, or does it also need to fix motion
   and construction? (The first trial answers this.)
2. Subagent versus manual premium session on each platform, and whether each stub's model
   pin actually takes effect (the UNVERIFIED cells above).
3. How much of past cost sits before versus after the first render (the baseline answers this).
4. Whether the numeric audit and bounded visual review at stage 2 remove enough findings to
   reduce premium work without adding excessive cheap-model usage or regressions.

## Build order

1. Baseline scan (read-only). **Not done.**
2. This spec reviewed and corrected by other agents. **Done 2026-10-21** (Cursor usage data, cost weighting).
3. Brief template, fine-tuner spec, and the Cursor, Claude and Codex stubs. **Done 2026-10-21.**
4. One real clip through arm B, then the three-clip comparison.
5. If the subagent stubs misbehave (wrong model, too much context), fall back to the manual
   premium session; keep the stubs only if they prove worth it.

**Built:** `Manim Trial/docs/FINE_TUNE_BRIEF.md`, `Manim Trial/docs/FINE_TUNER.md`,
`.cursor/agents/manim-fine-tuner.md`, `.claude/agents/manim-fine-tuner.md`,
`.codex/agents/manim-fine-tuner.toml`. **Created on first use:** `Manim Trial/media/fine-tune/`
(briefs), `Manim Trial/benchmarks/runs.csv`.
