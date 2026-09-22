# Momentum handoff — GP post-survey + page error button

**Written:** 2026-09-20 (Sunday, ~7:19 PM)

---

## 1. Objective and current phase

**Active thread:** Gauss-Jordan **Guided Practice** student portal — (A) **one-time post-completion survey** after first guided problem, (B) **page error report button** on non-modal screens, (C) **Teacher Console readouts** for both. Same-day bug-fix pass on survey gate, error-button styling, homepage exclusion, label copy, and **admin test bypass** so Chase can re-run the survey.

**Phase:** **Feature + fixes implemented; headless tests green on touched files; not committed; not deployed.** Chase can see the survey again with admin cheats (Skip to end → finish → Do another problem). **Next polish:** last survey step Submit button layout (see §7).

**Do not edit:** `gp_survey_and_error_button_63ac40ce.plan.md` (Chase asked to leave it alone).

---

## 2. Chase's desired feel (use his language)

- **Survey:** Show once after **first guided problem completion** for normal students. Four steps — horizontal No / Maybe / Yes (Q2 adds **I didn't use it**), optional text on Q4. Copy is locked (see §3).
- **Survey testing:** With **admin cheats**, Chase wants to **continuously see the survey** while iterating — even after he already submitted it once. Submit in test mode should **not block** on "Survey already completed."
- **Error button:** Red **! badge** like existing fraction-help triggers, plus **compact label in a small bordered box** (much smaller text). **Not on the homepage.** Label: **"Click or tap if you see an error or mistake on this page."** Whole control is one click target, bottom-right ~50px inset.
- **Skip to end:** Homepage cheat (admin only) to jump workspace to last slot for fast survey testing.
- **No surprise windows** — never launch GUI without asking. Modals never dismiss on backdrop click.

---

## 3. Accepted decisions (do not re-litigate)

| Decision | Why |
|---|---|
| Activity `matrix/guided-practice-survey`, RPCs `gp_post_survey_completed`, `submit_gp_post_survey` | Migration `050_gp_post_survey.sql`; extends `get_practice_bank_status` with `completed_count` |
| Gate: `completed_count === 1 && !surveyAlreadyCompleted` for students | Original one-time spec |
| **Admin test bypass** (`hasAdminCheats()` / `typingCheatsEnabled`): show survey after **every** guided finish; **skip DB submit** on survey complete | Chase testing; avoids duplicate-submit RPC error |
| Page errors: table `gp_page_error_reports`, RPCs `record_gp_page_error`, `list_gp_page_errors` | Migration `051_gp_page_errors.sql` |
| One click per `screen_key`; hide on survey overlay and guided complete modal; **hide on home** | Chase correction |
| `FractionHelpAlertIcon` `variant="error"` (red gradient !) | Matches help-trigger badge style |
| Teacher Console: `GuidedPracticePostSurveyPanel`, `GuidedPracticePageErrorPanel` in `PracticeArchivePanel.tsx` | Import fix: `./` not `../` |
| Migrations **050 + 051 pushed** via `npm run db:push` in student-session-kit (per prior session) | Supabase live |

### Survey copy (locked)

| Step | Prompt | Answers |
|------|--------|---------|
| 1 | When you got something wrong, did the app help you understand your mistake? | No · Maybe · Yes |
| 2 | Were the help buttons useful when you needed them? | No · Maybe · Yes · I didn't use it |
| 3 | Would you use this again to practice before a test? | No · Maybe · Yes |
| 4 | What do you think about the app? Is it helpful? Anything you think I should improve? | Optional text; placeholder: *Optional — even one sentence helps* |

---

## 4. Rejected directions (do not rediscover)

| Rejected | Why |
|---|---|
| Error button on **homepage** | Chase: "doesn't need to be on the homepage" |
| Large unstyled floating red text only (no icon box) | Missing icon sizing CSS on page-error trigger; fixed but layout still being tuned |
| Survey only when `completed_count === 1` for **testers** | CHASE1 had prior completions; survey never showed until admin bypass |
| Blocking re-test when survey already in DB | Admin bypass skips `submit_gp_post_survey` |
| `PracticeArchivePanel` imports from `../GuidedPractice*` | Broke Macro renderer build; use `./` |

---

## 5. Current implementation state

### Student portal (`School Scrips/student-portal`) — dirty, uncommitted

**Survey**
- `GuidedPracticePostSurvey.tsx` — 4-step overlay; `adminTestBypass` skips RPC submit
- `GuidedPracticePostSurveyStep.tsx`, `GuidedPracticePostSurveyTextStep.tsx`
- `guidedPracticePostSurveyCopy.ts`, `guidedPracticePostSurveyService.ts`
- `guidedPracticeSurveyGate.ts` — gate logic + admin bypass
- `GuidedPracticeView.tsx` — wires survey after `finishGuided()` on back-to-menu / another-problem; Skip to end; page error hook

**Page error**
- `GuidedPracticePageErrorButton.tsx` — label constant (final copy above)
- `useGuidedPracticePageErrorButton.ts`, `guidedPracticePageErrorService.ts`, `guidedPracticeScreenKey.ts`
- Mounted on `GuidedPracticeView.tsx` (not home) and `UnguidedPracticeView.tsx`

**Styles**
- `src/styles/guided-practice.css` — `.gp-post-survey__*`, `.gp-page-error-trigger__*`
- Survey Submit uses same class as Next: `.gp-post-survey__next-btn` in `.gp-post-survey__footer` **below** textarea with `margin-top: 0.85rem`

**Tests passing (this session):** `guidedPracticeSurveyGate`, `useGuidedPracticePageErrorButton`, related copy/screen-key tests; portal `npm run build` succeeded earlier in thread.

### Matrix app — dirty (embed + `FractionHelpAlertIcon` error variant, solver callbacks)

### Macro App — dirty (Teacher Console panels + IPC for page errors; `config/d2l-courses.json` machine-local — do not commit)

### student-session-kit — untracked migrations 050, 051 (confirm push state before assuming prod)

---

## 6. Open questions and constraints

- **Submit button layout (Chase's next ask):** On **step 4 only**, shrink Submit to **~half** current size and place **flush with the bottom of the textarea** (not in a separate footer row with gap). Current structure: textarea in `GuidedPracticePostSurveyTextStep`, Submit in sibling `.gp-post-survey__footer` in `GuidedPracticePostSurvey.tsx`. Likely needs a wrapper around text step + submit (CSS grid/flex) or a submit-specific modifier class — **do not change Next button on MCQ steps** unless Chase asks.
- **Production survey behavior** stays one-time; admin bypass is test-only via `typingCheatsEnabled`.
- **No commit/push/deploy** unless Chase asks.
- Read root `AGENTS.md`, `School Scrips/student-portal/AGENTS.md`, `cursor-patterns/CODING_STANDARDS.md` before edits.

---

## 7. Exact next step

1. Read **`GuidedPracticePostSurvey.tsx`** and **`guided-practice.css`** (`.gp-post-survey__textarea`, `.gp-post-survey__footer`, `.gp-post-survey__next-btn`).
2. On the **last survey step only**, make the **Submit** button **half** the current footprint (height/width/padding/font — proportional) and align it **flush with the bottom edge of the text box** (bottom-right typical; remove the 0.85rem footer gap).
3. Keep MCQ **Next →** button unchanged.
4. Verify headlessly (`npm test` / build in student-portal). Hand Chase reload instructions — do not launch portal without permission.

---

## Read first (fresh agent)

1. This file (`agent docs/momentum-handoffs/latest.md`)
2. Root `AGENTS.md` (never display without permission, modal rules, file size)
3. `School Scrips/student-portal/AGENTS.md`
4. `GuidedPracticePostSurvey.tsx`, `GuidedPracticePostSurveyTextStep.tsx`, `src/styles/guided-practice.css` (survey section)

---

## Verification Chase was using

- User **CHASE1** with admin cheats / Skip to end on guided practice home
- Finish problem → **Do another problem** → survey should appear every time in test mode
- Error button visible in guided workspace (not home), red ! + small boxed label
