# Momentum handoff — Macro App portal-link emails (Email tab + Outlook send drafts)

Written: 2026-10-04 (America/Chicago)
Workspace: `C:\Users\chase\Documents\Programs` — primary app **`School Scrips/Macro App`**
Phase: Portal-link Outlook **draft** flow works; **send-all-drafts** automation was broken (wrong
clicks). Browser exploration fixed the OWA path; CDP code updated. Email tab side panel got
**collapsible Students** (no inner scroll) and **Email tools** with the same send button as Manage
class. **Not yet verified** end-to-end from the in-app “Send drafts in Outlook” button after the
CDP rewrite.

## Read first

1. Root `AGENTS.md` — no GUI/browser without per-run permission; handoff ≠ commit/push.
2. `School Scrips/Macro App/AGENTS.md` — keyword row for Macro App / Teacher Console / Email tab.
3. **`modules/outlook/outlook_send_drafts_cdp.py`** — send loop (Drafts folder → open draft →
   Continue editing → Send → wait for count/fingerprint change).
4. **`renderer/src/components/side-panels/EmailSidePanel.tsx`** +
   **`renderer/src/components/side-panels/email/EmailSidePanelPortalLinkTools.tsx`** — Email tab
   portal tools + collapsible Students (`storageKey`: `email-tab-students-open`).
5. **`renderer/src/hooks/teacher-console/usePortalLinkEmailCompose.ts`** — draft report
   localStorage, `getDraftReportForCourseMap`, compose/send bridge.
6. **`renderer/src/hooks/shell/useMacroAppStudentProgressShell.ts`** — `loadPortalCodeMaps` when
   `student-progress` **or** `d2l-email` so portal maps load on Email tab.

## What Chase wants

- **Draft** portal-link emails per student (M2412 / pre-calc roster) into Outlook Drafts — done before this stretch.
- **Send** those drafts without an agent: one button, CDP automation on the **Email tab** Outlook
  embed (CDP **9224**).
- Email tab side panel: **Students** collapses to a single toggle (no Select all / names / Copy when
  collapsed). When expanded, **all names visible** — **no nested scroll** on the list; the whole
  panel card scrolls if needed.
- **Send drafts** lives on **Email tab → Email tools** (and still on **Teacher Console → Manage
  class → Roster actions**). Portal-link section can stay collapsible; that was secondary.

## Feel and accessibility

- Dwell clicking — big targets, modals **no backdrop dismiss**.
- Handoffs are statements, not “want me to test?” — but **ask before** launching Macro App GUI or
  driving Outlook on screen unless Chase already said yes for that run.

## Accepted decisions

| Decision | Why |
|---|---|
| Persist draft/send report in `localStorage` (`macro-app-portal-link-email-draft-reports-v1`) | Email tab unmounts TC panel; Chase needs a durable box under roster / Email tools. |
| Email tab course = `findPortalMapForCourse(selectedCourse, maps, folderIndex)` | Gradebook tab ≠ Email tab class picker. |
| Separate template selection on Email tab via `usePortalLinkEmailTemplateSelection(portalCourseCode, …)` | TC hook `courseCode` follows Manage-class map only. |
| Send automation: **Drafts tree → list option → Continue editing (if needed) → Send** | OWA reading pane does not show Send until compose opens; after send, **next draft opens in compose** — do not wait for Send to disappear. |
| Success detection: matching **draft count drops** or **compose fingerprint** changes | Send stays visible for the next message. |

## Rejected / do not rediscover

- **Inner scroll** on `email-student-picker__list` — Chase cannot use a scroll rail; removed `overflow-y: auto` and flex shrink chain.
- Collapsing **only** portal-link emails when Chase asked to collapse **Students** — Students collapsible is the important one.
- Assuming **`button[aria-label="Send"]`** exists without opening compose — fails on reading-pane draft view.
- **`is_compose_open()`** via `input[aria-label="Subject"]` alone — OWA uses `[placeholder="Add a subject"]` textbox; send path uses Send visibility + fingerprint instead.

## Current implementation state (uncommitted Macro App)

**Backend / automation**

- `modules/outlook/outlook_send_drafts_cdp.py` — rewritten send flow (see above).
- `modules/outlook/outlook_compose_processor.py` — `send-portal-link-drafts` command.
- `electron-app/d2l-bridge-timeouts.js` — timeout for send command.

**Renderer**

- Email tab: `EmailSidePanelPortalLinkTools.tsx` (new), `AppSidePanel.tsx` wiring, CSS in
  `renderer/src/styles/index.css`.
- TC: `PortalLinkEmailDraftReportBox`, `PortalLinkEmailSendConfirmModal`, roster + side panel props;
  `getPortalLinkEmailDraftReport(studentProgress.selectedCourseMap)` for Manage class report.
- `PortalLinkEmailComposeSection` — `showSendButton={false}` on Email tab collapsible; send in tools only.
- `usePortalLinkEmailCompose.ts` — `getDraftReportForCourseMap`, `getEmailTemplatesForCourse` export.

**Verification already done**

- Unit tests: `portalLinkEmailDraftReport.test.ts`, `portalCourseMatch.test.ts` (passed earlier).
- **Playwright MCP** on live Outlook tab: Drafts → Continue editing → Send × **2** (Corbin Shaskin,
  Adrian Velasquez). Drafts count **26 → 24** for portal-link set (approx.).
- Headless: `python scripts/send-portal-link-drafts.py --dry-run` → `onDraftsFolder: true`,
  `sendButtonVisible: true`, `remaining: 12` (subject-filtered count at that moment).

**Not done**

- In-app **Send drafts in Outlook (N)** after CDP rewrite (Chase has not confirmed).
- Git commit/push (explicitly out of scope for handoff).

## Open questions / constraints

- Remaining portal drafts (~24 before manual sends; dry-run showed 12 matching filter — confirm
  subject filter matches template: default needle **"your math app portal link"**).
- If send fails from app: run `--dry-run` first; check Email tab is active and Outlook signed in on
  slot `d2l-email`.
- **Frozen:** Calendar 2.0 — do not touch.

## Exact next step

With Macro App running and Email tab on Outlook Drafts, have Chase trigger **Send drafts in Outlook**
once (or run `python scripts/send-portal-link-drafts.py --count 2` headlessly as a smoke test if CDP
9224 is up). If it fails, read the returned `log` / `failed` arrays from the Python result and align
CDP selectors with the Playwright flow (`getByLabel('Send', { exact: true })`, **Continue editing**,
Drafts `treeitem`).

This handoff is a continuation boundary only — no GitHub or end-of-session actions were performed.
