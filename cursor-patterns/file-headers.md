# File Headers Standard

> **Purpose:** Standardized file headers guide AI behavior and prevent breaking changes
>
> **When to Use:** All new TypeScript/JavaScript files, Python modules, and major components

---

## Why File Headers Matter

File headers are the FIRST thing AI reads when opening a file. They:
- **Prevent breaking changes** by documenting invariants
- **Guide refactoring** by marking safe vs. fragile areas
- **Speed up onboarding** for new developers or AI sessions
- **Document dependencies** and why they exist
- **Track verification dates** for maintenance

---

## Standard Header Format (TypeScript/JavaScript)

### For Utilities, Services, and Hooks

```typescript
/*
===============================================================================
FILE: [filename].ts

MODULE ROLE:
[One sentence describing what this file does]

WHY THIS FILE EXISTS:
[Context - when/why was this created? What problem does it solve?]

PUBLIC API (STABLE):
- [exportedFunction](params): ReturnType - [Description]
- [exportedClass] - [Description]

INTERNAL COMPONENTS:
- [internalHelper] - [Purpose]
- [privateFunction] - [Purpose]
(Or write "NONE" if no internal components)

INPUTS / OUTPUTS:
- Inputs: [What this file accepts - parameters, props, data]
- Outputs: [What this file returns - values, side effects]

SIDE EFFECTS:
- [API calls, localStorage writes, console logs, etc.]
(Or write "NONE" for pure functions)

DEPENDENCIES (WHY THEY EXIST):
- react → [UI state management]
- lodash/debounce → [Prevents excessive API calls]
- [package] → [reason for dependency]

INVARIANTS (MUST REMAIN TRUE):
- [Critical assumptions that must never change]
- [e.g., "Function must be called after component mount"]
- [e.g., "State updates are async - never read immediately after set"]

SAFE TO MODIFY:
- [What can be changed without breaking things]
- [e.g., "Timing values (currently 500ms)"]
- [e.g., "Styling and CSS classes"]

FRAGILE / HIGH-RISK AREAS:
- [What should NOT be changed without careful review]
- [e.g., "Timer management with useRef - ensure cleanup"]
- [e.g., "Race condition handling - order matters"]

CALL FLOW (HIGH LEVEL):
[Brief description of how this file is used]
Example: "Component → hook → service → API"

LAST VERIFIED:
- Behavior verified: [YYYY-MM-DD]
- Header reviewed: [YYYY-MM-DD]
===============================================================================
*/
```

### For React Components

```typescript
/**
 * FILE HEADER
 * 
 * FILE: [path relative to src/]
 * 
 * PURPOSE:
 * [What this component renders and its role in the app]
 * 
 * LAST VERIFIED:
 * - Behavior verified: [YYYY-MM-DD]
 * - Header reviewed: [YYYY-MM-DD]
 * 
 * SAFE TO MODIFY:
 * - [List of safe changes]
 * - [e.g., "Button styling and layout"]
 * - [e.g., "Text content and labels"]
 * 
 * FRAGILE / HIGH-RISK AREAS:
 * - [Warning about risky areas]
 * - [e.g., "Positioning logic uses getBoundingClientRect()"]
 * - [e.g., "Portal rendering order affects z-index"]
 */
```

---

## Standard Header Format (Python)

```python
"""
===============================================================================
MODULE: [module_name]

PURPOSE:
[What this module does]

WHY THIS EXISTS:
[Context - problem being solved]

PUBLIC API:
- function_name(params) -> return_type: [Description]
- ClassName: [Description]

INTERNAL HELPERS:
- _private_helper(): [Purpose]
(Or "NONE")

DEPENDENCIES:
- pandas → [Data manipulation]
- requests → [HTTP calls to external API]

SIDE EFFECTS:
- Writes to database
- Creates files in temp directory
(Or "NONE" for pure functions)

SAFE TO MODIFY:
- Timeout values
- Retry attempts
- Log messages

FRAGILE:
- Thread-safe state management (uses locks)
- Database connection pooling

LAST VERIFIED: [YYYY-MM-DD]
===============================================================================
"""
```

---

## When to Update Headers

### "LAST VERIFIED" Date

Update when:
- ✅ You modify the file's behavior
- ✅ You test that the file still works as expected
- ✅ You review the header and confirm it's still accurate
- ❌ Don't update for typo fixes or comment changes

### "SAFE TO MODIFY" Section

Add items when:
- You identify parts of the code that can change without risk
- You extract magic numbers to constants
- You make styling or timing adjustable

### "FRAGILE / HIGH-RISK AREAS" Section

Add warnings when:
- You discover edge cases or race conditions
- You use complex APIs (timers, positioning, state)
- You find bugs that required careful fixes
- Changes could break dependent code

---

## Examples from Real Projects

### Example 1: Custom Hook (useDrawerHover.ts)

```typescript
/*
===============================================================================
FILE: useDrawerHover.ts

MODULE ROLE:
Custom React hook for managing drawer hover interactions with delay timers,
cooldown periods, and accessibility-friendly dwell-mouse support.

WHY THIS FILE EXISTS:
Extracted during 2026-01-10 Phase 3 refactoring to reduce Sidebar.tsx from
1,123 lines. This complex hover logic with multiple timers was tangled with
the sidebar's main component code.

PUBLIC API (STABLE):
- useDrawerHover(OPEN_DELAY, CLOSE_DELAY, COOLDOWN, LOCK_DURATION)
  Returns: { openActionPanel, drawerPosition, scheduleOpen, cancelOpen, ... }

INTERNAL COMPONENTS:
- openTimerRef - useRef for tracking scheduled open timeout
- closeTimerRef - useRef for tracking scheduled close timeout

INPUTS / OUTPUTS:
- Input: Delay configurations (milliseconds)
- Output: State and control functions for drawer behavior

SIDE EFFECTS:
- Creates/clears setTimeout timers
- Console logging for debugging drawer lock behavior
- Updates state that triggers React re-renders

DEPENDENCIES (WHY THEY EXIST):
- react → Custom hook using useState, useRef, useCallback

INVARIANTS (MUST REMAIN TRUE):
- Timers must be cleaned up to prevent memory leaks
- Lock period must complete before allowing close (accessibility)
- Only one timer of each type (open/close) should exist at a time

SAFE TO MODIFY:
- Default delay values (currently 500ms each)
- Console log messages
- Timer duration calculations

FRAGILE / HIGH-RISK AREAS:
- Timer cleanup logic - ensure all refs are cleared properly
- Lock period enforcement - critical for dwell-mouse accessibility
- Race conditions between open/close timers

CALL FLOW (HIGH LEVEL):
Sidebar → useDrawerHover hook → manages timers → returns state/functions

LAST VERIFIED:
- Behavior verified: 2026-01-10
- Header reviewed: 2026-01-10
===============================================================================
*/
```

### Example 2: Service Layer (exportService.ts)

```typescript
/**
 * ============================================================================
 * MODULE: Export Service
 * ============================================================================
 *
 * ROLE: Centralized export logic for calendar data to Excel format
 *
 * WHY THIS EXISTS:
 * Export logic was duplicated between App.tsx and Sidebar.tsx (212 lines).
 * This service provides a single source of truth for export operations,
 * including file-open error detection and retry logic.
 *
 * PUBLIC API:
 * - exportCalendar() - Main export orchestration
 * - retryExport() - Retry export with stored parameters
 * - PendingExport interface - Type for pending export state
 *
 * LAST VERIFIED: 2026-01-11
 * ============================================================================
 */
```

### Example 3: Component (Sidebar.tsx)

```typescript
/**
 * FILE HEADER
 * 
 * FILE: src/components/Sidebar.tsx
 * 
 * PURPOSE:
 * Main sidebar component displaying class list, controls, and class management.
 * Includes drawer-based rename/delete functionality with hover delays.
 * 
 * LAST VERIFIED:
 * - Behavior verified: 2026-01-20
 * - Header reviewed: 2026-01-20
 * 
 * SAFE TO MODIFY:
 * - Drawer delay timings (currently 0.5 seconds)
 * - Drawer styling and positioning
 * - Button styling and layout
 * 
 * FRAGILE / HIGH-RISK AREAS:
 * - Drawer positioning uses `getBoundingClientRect()` and `createPortal`
 *   Changes to positioning logic may break drawer placement
 * - Timer management with `useRef` - ensure proper cleanup in `useEffect` return
 * - Hover logic depends on `onMouseEnter`/`onMouseLeave` timing
 *   Changes may cause flickering
 */
```

---

## Common Mistakes

### ❌ Too Vague
```typescript
/*
FILE: utils.ts
PURPOSE: Helper functions
*/
```

### ✅ Specific and Useful
```typescript
/*
===============================================================================
FILE: semesterDateCalculations.ts

MODULE ROLE:
Utility functions for calculating academic calendar dates (first class day,
spring break, finals week) based on semester name and schedule.

WHY THIS FILE EXISTS:
Extracted during refactoring to eliminate duplicate date logic across
TemplateConversionDialog.tsx and ImportCalendarsModal.tsx.
...
*/
```

### ❌ No Context About Risk
```typescript
/*
FILE: dragHandler.ts
PURPOSE: Handles drag operations
*/
```

### ✅ Clear Risk Warning
```typescript
/*
...
FRAGILE / HIGH-RISK AREAS:
- Drag state machine - transitions must follow IDLE → DRAGGING → COOLDOWN
  Skipping cooldown causes double-trigger bugs
- Position calculations assume single monitor setup
  Multi-monitor requires offset adjustments
*/
```

---

## Template Checklist

When creating a file header, ensure you have:

- [ ] **MODULE ROLE**: One sentence, clear purpose
- [ ] **WHY THIS EXISTS**: Context for creation/extraction
- [ ] **PUBLIC API**: List all exported functions/classes
- [ ] **INPUTS/OUTPUTS**: What goes in, what comes out
- [ ] **SIDE EFFECTS**: API calls, storage, logs, or "NONE"
- [ ] **DEPENDENCIES**: List with reasons, not just names
- [ ] **SAFE TO MODIFY**: Guide future changes
- [ ] **FRAGILE AREAS**: Warn about risky code
- [ ] **LAST VERIFIED**: Date stamp for maintenance

---

## Benefits of Good Headers

**For AI:**
- Reads header FIRST before modifying code
- Knows which areas are safe to change
- Understands dependencies and why they exist
- Avoids breaking invariants

**For Developers:**
- Quick understanding without reading all code
- Confidence when refactoring
- Clear maintenance history
- Prevents "this was written for a reason I don't understand" syndrome

**For Teams:**
- Consistent documentation format
- Easy code reviews
- Onboarding new members faster
- Less time explaining "why does this exist?"

---

## Related Patterns

- [Refactoring Checklist](./refactoring-checklist.md) - Phase 1 includes file header requirements
- [Coding Standards](./CODING_STANDARDS.md) - Overall code quality guidelines
- [Anti-Patterns](./anti-patterns.md) - What NOT to do

---

**Last Updated:** 2026-01-12
