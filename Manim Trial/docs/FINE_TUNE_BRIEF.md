# Fine-tune brief (builder side, stages 1 and 2)

> **You might say:** *"hand it to the fine-tuner"* · *"write the fine-tune brief"* · *"fine-tune <Scene>"*
>
> The builder (cheap model) writes the brief; the premium fine-tuner reads only the brief and
> [FINE_TUNER.md](FINE_TUNER.md). Why: [FINE_TUNE_PIPELINE.md](FINE_TUNE_PIPELINE.md).

## Before writing it

1. The clip renders as a draft and the numeric audit fixes are applied
   ([LAYOUT_GUARDRAILS.md](LAYOUT_GUARDRAILS.md), steps 2 to 4).
2. **One bounded visual pass** (if the model can read images): generate the contact sheet,
   check it against the list below, make **one batch** of corrections, re-render, regenerate
   the sheet. Do not start a second cheap repair loop.
   - Do arrows start at the axes' intended origin?
   - Are gauge fills inside their tracks and aligned with the gauge?
   - Is anything overlapping, clipped, or too small to read?
   - Did any expected label or object disappear between beats?
3. Same limits as the fine-tuner: never delete or hide an element to clear an overlap; leave
   math, captions and timing alone; do not edit the audit, layout helpers or tests.

A clean numeric audit does not prove the visual corrections worked. Write down what you are
unsure of.

## The brief

Path: `Manim Trial/media/fine-tune/<SceneClass>_brief.md` (under `media/`, not tracked; create
the folder if missing). Under 40 lines. Fill every field:

```
Scene: <module>.py  class <SceneClass>
Teaches: <one or two sentences, what the clip is explaining>
Draft render: done, strict audit status: <clean | n findings>
Audit report: Manim Trial/media/audit/<SceneClass>_audit.json
Contact sheet: Manim Trial/media/audit/<module>_contact.jpg
Cheap visual pass: <completed | skipped: reason>; <corrections made, or none>
Known problems: <marks the builder could not resolve, in its own words>
Motion concerns: <suspected issues | not assessed beyond sampled frames>
Off limits: math values, captions, timing, deleting elements
Round cap: 3
```

## Handing off

The fine-tuner agent is `manim-fine-tuner` in every tool (same name, so Cursor uses its own
file when it also sees the Claude and Codex ones).

| Tool | Hand-off |
|---|---|
| Cursor | Builder chat: `/manim-fine-tuner brief is at <path>`. Fallback: a fresh premium chat, "fine-tune <Scene>, brief is at <path>". |
| Claude Code | Ask for the `manim-fine-tuner` subagent with the brief path, or a fresh Opus session given the brief. |
| Codex | Ask Codex to spawn the `manim-fine-tuner` agent with the brief path, or a fresh session given the brief. |

After it returns: the builder reads its report, then owns the final render, `build_page.py` and
portal wiring as usual. Later edits (stage 4) re-run with `MANIM_AUDIT_STRICT=1`; a nonzero exit
means the layout regressed.

**Benchmark runs:** note the start and end time of the whole run and run no other Cursor chats
in parallel (see "Cursor usage data" in the pipeline doc).
