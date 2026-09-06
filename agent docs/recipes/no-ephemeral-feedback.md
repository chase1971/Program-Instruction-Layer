# No ephemeral feedback UI

> **You might say:** "don't add confirmation text", "no copied to clipboard message",
> "stop adding little feedback messages", "don't show toast unless I ask"
> **What it is:** Never add transient success/confirmation copy to the UI unless Chase
> explicitly asks for it.

**Exemplar files — read these before writing new code:**

- `School Scrips/Macro App/renderer/src/components/teacher-console/screens/ConsoleExitTicketsScreen.tsx` — Copy formatting: clipboard only, no on-screen notice
- `School Scrips/Macro App/renderer/src/utils/clipboard/copyTextToClipboard.ts` — silent copy helper

---

## Why it exists

Chase uses dwell click and speech-to-text. Ephemeral messages ("Formatting copied",
"Saved!", green notice bars) appear in unpredictable spots, steal layout space, and
become permanent clutter he did not ask for — then he has to remember to ask agents to
remove them.

## The rule

**Do not add UI that confirms a successful action** unless Chase explicitly requests
that feedback for that action.

This includes:

- "Copied to clipboard" / "Formatting copied" lines
- Success toasts, banners, or inline notices after a button click
- Replacing or crowding a button area with temporary status text
- "Helpful" one-line hints that appear only after an action

**Still OK without asking:**

- **Errors** when something failed (parse errors, publish failed, network error) — those
  block the task and must be visible
- **Loading/disabled button state** on the button itself (`Publishing…`, `Saving…`) —
  that is control state, not a separate message
- **Static labels** Chase asked for (field labels, section headings)

## Non-negotiables

| Do | Prevents |
|---|---|
| Copy/write silently; button stays as-is | Random green text under buttons |
| Put errors in a stable, expected place | Success noise mixed with real errors |
| Ask once if feedback is genuinely needed | Agents guessing "users want confirmation" |

## Anti-patterns

- Adding `setNotice('Copied!')` after clipboard actions
- Toast libraries for one-off "success" without a request
- Inline `<p className="success">` that appears after every click
- Replacing button labels with status text instead of using `disabled` + label change on the same button
