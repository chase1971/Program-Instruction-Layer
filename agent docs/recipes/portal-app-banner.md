# Portal app banner — every app's top bar looks the same

> **You might say:** "build an app", "add an app to the portal", "the banner needs to be there",
> "all these apps need the banner", "back to home and exit", "fullscreen button", "title at the top"
> **What it is:** The navy `portal-quiz__header` bar across the top of **every** student-portal
> app screen. **Building a portal app, or adding a screen to one, always includes this banner.**
> Never ship a screen with its own home-made header instead.

**Exemplar — read before writing a header:**

- `School Scrips/student-portal/src/features/logic-homework/LogicHomeworkView.tsx` → the
  `showGates` branch (Logic Gates Extra Credit): all four pieces in one place.
- Buttons: `src/app/components/PortalNavigationBackButtons.tsx` · labels:
  `src/config/portalNavigationLabels.ts` · fullscreen:
  `src/features/matrix-tutorial/MatrixTutorialFullscreenButton.tsx`
- CSS (already handles centering — add nothing): `src/styles/portal-base.css` §
  `.portal-quiz__header`, `.portal-quiz__header-title`, `.portal-quiz__header-exit`

---

## The shape

```tsx
<header className="portal-quiz__header">
  <div className="portal-quiz__header-start">
    <PortalQuizAppHomeBackButton onClick={backToAppHome} />   {/* ← Back to home */}
    <MatrixTutorialFullscreenButton />                         {/* Android fullscreen */}
  </div>
  <h2 className="portal-quiz__header-title">{TITLE}</h2>      {/* centered */}
  <PortalQuizHeaderExitButton onClick={() => navigatePortalRoute('home')} />  {/* Exit, far right */}
</header>
```

| Piece | Rule |
|---|---|
| Left: **Back to home** | Returns to the app's own home/menu, not the portal. On the app's home screen itself, use `PortalQuizPillMainMenuBackButton` (Exit) there instead. |
| Left: **fullscreen** | Always present beside the back button. |
| Center: **title** | `portal-quiz__header-title`, visible and centered. No goal sentences or instructions in the banner. Title string lives in the feature's `*Activity.ts` constants. |
| Right: **Exit** | Always back to the portal tile screen. |

## Embedding a sibling app's screen (`@logic/`, `@matrix/`, …)

The sibling app's own header must not show inside the portal. Give the embedded component a
`hideHeader` prop (exemplar: `logic-app/src/app/components/gates/GateSandbox.tsx`) and render
the portal banner around it. The standalone app keeps its own header.

## Exceptions

- **Logic Homework problems** (the truth-table activity) predate this and have Exit inside the
  embed. Chase assigned it as-is: **do not change it** unless he names it.
- Mid-assignment status (saving / error) goes in the center slot via
  `PortalQuizHeaderCenter` — exemplar `transformations/TransformationsActivityHeader.tsx`.
