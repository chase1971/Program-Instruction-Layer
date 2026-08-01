# Accessibility Patterns

> **Purpose:** React-side patterns for dwell-mouse interaction, keyboard navigation, and screen readers.
>
> ## ⚠️ Timing values in this file are illustrative, not shipped
>
> The 500 ms figures below match **no running implementation**. For real timing —
> and for the fact that the toolbar fires an OS-level click at **250 ms** on top of
> whatever your component does — read:
>
> ### → **`cursor-patterns/dwell-and-head-mouse.md`** (source of truth)
>
> ## The `useDrawerHover` hook below does not exist
>
> It is reference code, never implemented. **Do not import it.** Before building a
> hover/dwell interaction, use an existing mechanism:
>
> | You need… | Use | Exemplar |
> |---|---|---|
> | Latch-to-drag (move/resize) | `useDwellRectEdit`, `useDwellAttachDrag` | Math App Studio |
> | Shared latch geometry / hit-test | `utils/dwellStationary.ts` | Math App Studio |
> | Delayed tooltip | `useGradebookDelayedHover` | Macro App gradebook |
> | Overlay region hover (vanilla JS) | `createOverlayHoverPoll` | electron-toolbar |
>
> **The exemplar rule to model new app rules on:**
> `School Scrips/Math App Studio/.cursor/rules/studio-dwell-mechanics.mdc`

---

## Dwell Mouse Support

### What is Dwell Mouse?

Dwell mouse (also called "hover click" or "eye-gaze") allows users to interact with computers by hovering the cursor over targets for a set duration instead of clicking. This is essential for users with limited hand mobility who may use:
- Eye-tracking systems
- Head-tracking devices
- Single-switch scanning systems

### Core Pattern: Lock Period

**Problem:** Hover-based UI elements may close immediately when the cursor moves away, making them unusable for dwell-mouse users.

**Solution:** Implement a lock period after opening to prevent immediate closure.

```typescript
// Lock duration to prevent immediate closing (for dwell mouse accessibility)
const PANEL_OPEN_LOCK_DURATION = 500; // milliseconds

let panelOpenLockRef: React.MutableRefObject<number | null>;

// When panel opens
const handleOpen = () => {
  setIsOpen(true);
  panelOpenLockRef.current = Date.now() + PANEL_OPEN_LOCK_DURATION;
  console.log('[Accessibility] Panel locked for dwell mouse support until', panelOpenLockRef.current);
};

// When attempting to close
const handleClose = () => {
  const now = Date.now();
  const lockEnd = panelOpenLockRef.current;
  
  // Check if still in lock period
  if (lockEnd && now < lockEnd) {
    const timeRemaining = lockEnd - now;
    console.log(`[Accessibility] Panel locked for ${timeRemaining}ms more (dwell mouse support)`);
    return; // Cannot close yet - locked for accessibility
  }
  
  setIsOpen(false);
  panelOpenLockRef.current = null;
};
```

**Why This Works:**
- Gives dwell-mouse users 500ms to move cursor to the opened element
- Prevents accidental closures from cursor wobble
- Allows intentional hover-off after lock expires

---

## Hover Delay Pattern

### Problem

Immediate hover triggers can cause accidental activations for:
- Eye-tracking users (unintentional fixation)
- Tremor users (cursor passing over elements)
- Touchpad users (cursor lag)

### Solution: Delayed Hover Activation

```typescript
// Hover delay before opening (prevents accidental triggers)
const HOVER_OPEN_DELAY = 500; // milliseconds
const HOVER_CLOSE_DELAY = 500; // milliseconds

let openTimerRef: NodeJS.Timeout | null = null;
let closeTimerRef: NodeJS.Timeout | null = null;

const scheduleOpen = (target: string) => {
  // Cancel any pending close
  if (closeTimerRef) {
    clearTimeout(closeTimerRef);
    closeTimerRef = null;
  }
  
  // Schedule open after delay
  openTimerRef = setTimeout(() => {
    setOpenTarget(target);
    openTimerRef = null;
  }, HOVER_OPEN_DELAY);
};

const cancelOpen = () => {
  if (openTimerRef) {
    clearTimeout(openTimerRef);
    openTimerRef = null;
  }
};

const scheduleClose = () => {
  // Cancel any pending open
  if (openTimerRef) {
    clearTimeout(openTimerRef);
    openTimerRef = null;
  }
  
  // Schedule close after delay
  closeTimerRef = setTimeout(() => {
    setOpenTarget(null);
    closeTimerRef = null;
  }, HOVER_CLOSE_DELAY);
};

const cancelClose = () => {
  if (closeTimerRef) {
    clearTimeout(closeTimerRef);
    closeTimerRef = null;
  }
};

// Usage in component
<div
  onMouseEnter={() => scheduleOpen('menu')}
  onMouseLeave={() => {
    cancelOpen();
    scheduleClose();
  }}
>
  Hover over me
</div>
```

**Benefits:**
- Prevents accidental triggers from cursor passing through
- Requires intentional hover (500ms is noticeable)
- Gives user time to cancel if unintended

---

## Complete Dwell-Accessible Drawer Pattern

### Use Case
Sidebar with class list where hovering on arrow opens action drawer (rename/delete/export).

### Full Implementation

```typescript
/**
 * Custom hook for dwell-accessible drawer
 */
export function useDrawerHover(
  openDelay: number = 500,
  closeDelay: number = 500,
  cooldownDuration: number = 500,
  lockDuration: number = 500
) {
  const [openActionPanel, setOpenActionPanel] = useState<string | null>(null);
  const [drawerPosition, setDrawerPosition] = useState<Position | null>(null);
  
  const openTimerRef = useRef<NodeJS.Timeout | null>(null);
  const closeTimerRef = useRef<NodeJS.Timeout | null>(null);
  const drawerOpenTimeRef = useRef<number | null>(null);
  const panelOpenLockRef = useRef<number | null>(null);
  
  // Schedule open after delay
  const scheduleOpen = useCallback((className: string) => {
    if (closeTimerRef.current) {
      clearTimeout(closeTimerRef.current);
      closeTimerRef.current = null;
    }
    
    openTimerRef.current = setTimeout(() => {
      setOpenActionPanel(className);
      drawerOpenTimeRef.current = Date.now();
      panelOpenLockRef.current = Date.now() + lockDuration;
      openTimerRef.current = null;
    }, openDelay);
  }, [openDelay, lockDuration]);
  
  // Cancel pending open
  const cancelOpen = useCallback(() => {
    if (openTimerRef.current) {
      clearTimeout(openTimerRef.current);
      openTimerRef.current = null;
    }
  }, []);
  
  // Schedule close after delay (respects lock period)
  const scheduleClose = useCallback(() => {
    if (openTimerRef.current) {
      clearTimeout(openTimerRef.current);
      openTimerRef.current = null;
    }
    
    closeTimerRef.current = setTimeout(() => {
      const now = Date.now();
      const lockEnd = panelOpenLockRef.current;
      
      // Check if still in lock period
      if (lockEnd && now < lockEnd) {
        console.log('[Accessibility] Close blocked - panel locked for dwell mouse');
        // Reschedule close check after lock expires
        setTimeout(() => scheduleClose(), lockEnd - now);
        return;
      }
      
      setOpenActionPanel(null);
      closeTimerRef.current = null;
    }, closeDelay);
  }, [closeDelay]);
  
  // Cancel pending close
  const cancelClose = useCallback(() => {
    if (closeTimerRef.current) {
      clearTimeout(closeTimerRef.current);
      closeTimerRef.current = null;
    }
  }, []);
  
  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (openTimerRef.current) clearTimeout(openTimerRef.current);
      if (closeTimerRef.current) clearTimeout(closeTimerRef.current);
    };
  }, []);
  
  return {
    openActionPanel,
    drawerPosition,
    drawerOpenTimeRef,
    panelOpenLockRef,
    scheduleOpen,
    cancelOpen,
    scheduleClose,
    cancelClose,
    setOpenActionPanel,
    setDrawerPosition
  };
}
```

### Usage in Component

```typescript
const Sidebar = () => {
  const {
    openActionPanel,
    drawerPosition,
    scheduleOpen,
    cancelOpen,
    scheduleClose,
    cancelClose
  } = useDrawerHover(500, 500, 500, 500);
  
  return (
    <div>
      {classes.map((className) => (
        <div key={className}>
          {/* Main button */}
          <button onClick={() => selectClass(className)}>
            {className}
            
            {/* Drawer handle - hover area */}
            <div
              data-drawer-handle
              onMouseEnter={(e) => {
                e.stopPropagation();
                cancelClose(); // Cancel any pending close
                scheduleOpen(className); // Schedule open with delay
              }}
              onMouseLeave={(e) => {
                cancelOpen(); // Cancel pending open
                const relatedTarget = e.relatedTarget as HTMLElement;
                
                // Only close if not moving to drawer panel
                if (!relatedTarget?.closest('[data-drawer-panel]')) {
                  scheduleClose();
                }
              }}
            >
              <ChevronRight />
            </div>
          </button>
          
          {/* Drawer panel */}
          {openActionPanel === className && (
            <div
              data-drawer-panel
              onMouseEnter={() => {
                cancelClose(); // Keep open when hovering drawer
              }}
              onMouseLeave={() => {
                scheduleClose(); // Close when leaving drawer
              }}
              style={{
                position: 'fixed',
                top: drawerPosition?.top,
                left: drawerPosition?.left
              }}
            >
              <button onClick={() => handleRename(className)}>Rename</button>
              <button onClick={() => handleDelete(className)}>Delete</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
```

---

## Timing Guidelines

### Recommended Values

| Interaction | Duration | Reasoning |
|-------------|----------|-----------|
| Hover open delay | 500ms | Prevents accidental triggers, feels intentional |
| Hover close delay | 500ms | Gives time to move to opened element |
| Lock period | 500ms | Allows dwell-mouse cursor adjustment |
| Cooldown | 500ms | Prevents rapid re-triggering |

### Adjustable Timing

Make timing values configurable for user preference:

```typescript
// Allow users to adjust in settings
const TIMING_PRESETS = {
  fast: { open: 300, close: 300, lock: 300 },
  normal: { open: 500, close: 500, lock: 500 },
  slow: { open: 800, close: 800, lock: 800 }
};
```

---

## Debugging Accessibility Features

### Console Logging Pattern

Always include console logs for accessibility-related timing:

```typescript
console.log('[Accessibility] Panel opened, locked until', lockEnd);
console.log('[Accessibility] Close blocked - panel locked for dwell mouse');
console.log('[Accessibility] Lock period expired, allowing close');
```

**Why:**
- Helps debug timing issues
- Confirms accessibility features are working
- Provides insight when user reports issues
- Can be filtered in production (`if (DEBUG_MODE)`)

### Visual Debugging

Add visual indicators for development:

```typescript
// Show lock state visually during development
{IS_DEV && isLocked && (
  <div className="absolute top-0 right-0 bg-yellow-500 text-xs px-2 py-1">
    LOCKED (Accessibility)
  </div>
)}
```

---

## Keyboard Navigation

### Focus Management

Ensure hover-based UI is also keyboard accessible:

```typescript
<div
  tabIndex={0}
  onMouseEnter={() => scheduleOpen()}
  onFocus={() => setOpen(true)} // Keyboard users get immediate open
  onBlur={() => setOpen(false)}
>
  Hover or tab to open
</div>
```

### Escape Key Support

Always allow ESC to close:

```typescript
useEffect(() => {
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && isOpen) {
      setOpen(false);
    }
  };
  
  document.addEventListener('keydown', handleEscape);
  return () => document.removeEventListener('keydown', handleEscape);
}, [isOpen]);
```

---

## Screen Reader Support

### ARIA Labels

```typescript
<div
  role="button"
  aria-label="Show class actions"
  aria-expanded={isOpen}
  aria-haspopup="menu"
  onMouseEnter={scheduleOpen}
>
  <ChevronRight aria-hidden="true" />
</div>
```

### Live Regions for Dynamic Content

```typescript
<div aria-live="polite" aria-atomic="true">
  {message && <p>{message}</p>}
</div>
```

---

## Testing Accessibility

### Manual Testing Checklist

- [ ] Can open menu by hovering for 500ms
- [ ] Can move cursor to opened menu without it closing
- [ ] Menu stays open for at least 500ms after opening
- [ ] Can close menu by moving cursor away for 500ms
- [ ] Can open menu with keyboard (Tab + Enter)
- [ ] Can navigate menu items with arrow keys
- [ ] Can close menu with Escape key
- [ ] Screen reader announces menu state

### Automated Testing

```typescript
describe('Dwell-accessible drawer', () => {
  it('should not open immediately on hover', async () => {
    const { getByTestId } = render(<Sidebar />);
    const handle = getByTestId('drawer-handle');
    
    fireEvent.mouseEnter(handle);
    
    // Should not be open immediately
    expect(queryByTestId('drawer-panel')).not.toBeInTheDocument();
    
    // Should open after delay
    await waitFor(() => {
      expect(getByTestId('drawer-panel')).toBeInTheDocument();
    }, { timeout: 600 });
  });
  
  it('should stay open during lock period', async () => {
    const { getByTestId } = render(<Sidebar />);
    
    // Open drawer
    fireEvent.mouseEnter(getByTestId('drawer-handle'));
    await waitFor(() => getByTestId('drawer-panel'));
    
    // Try to close immediately
    fireEvent.mouseLeave(getByTestId('drawer-handle'));
    
    // Should still be open (locked)
    await new Promise(resolve => setTimeout(resolve, 200));
    expect(getByTestId('drawer-panel')).toBeInTheDocument();
  });
});
```

---

## Common Mistakes

### ❌ No Lock Period
```typescript
// WRONG - Closes immediately
onMouseLeave={() => setOpen(false)}
```

### ✅ With Lock Period
```typescript
// CORRECT - Respects lock period
onMouseLeave={() => {
  if (Date.now() < lockEndTime) return;
  setOpen(false);
}}
```

### ❌ No Hover Delay
```typescript
// WRONG - Opens on any hover (accidental triggers)
onMouseEnter={() => setOpen(true)}
```

### ✅ With Hover Delay
```typescript
// CORRECT - Requires intentional hover
onMouseEnter={() => {
  timer = setTimeout(() => setOpen(true), 500);
}}
```

### ❌ No Cleanup
```typescript
// WRONG - Memory leak
useEffect(() => {
  timer = setTimeout(...);
}, []);
```

### ✅ Proper Cleanup
```typescript
// CORRECT - Cleanup on unmount
useEffect(() => {
  const timer = setTimeout(...);
  return () => clearTimeout(timer);
}, []);
```

---

## Modals and dialogs

### No overlay / backdrop dismiss (hard rule)

**Never** attach `onClick={onClose}` (or `onCancel`, etc.) to a modal overlay/backdrop. The user closes modals only through explicit buttons: OK, Cancel, Close, Done.

Dwell-mouse and head-mouse users cannot keep the cursor perfectly still. A wobble onto the dimmed backdrop must not cancel Setup courses, clear-courses wizards, or any multi-step flow.

```tsx
// ✅ Overlay is inert — matches ModalContainer.tsx
<div className="courses-modal-overlay" role="presentation">
  <div className="courses-modal" role="dialog" aria-modal="true" …>
    <button type="button" onClick={onClose}>Close</button>
  </div>
</div>

// ❌ Accidental dismiss
<div className="courses-modal-overlay" onClick={onClose}>
```

Full pattern: `cursor-patterns/modal-pattern.md` § No overlay / backdrop dismiss.

---

## Related Patterns

**Source of truth for dwell timing and the cross-layer coupling:**
- [Dwell & Head-Mouse](./dwell-and-head-mouse.md)

**Interaction patterns** — these live in the toolbar repo, not here
(`electron-toolbar/electron-app/patterns/`, indexed by its `README.md`):
- [Hover-to-Lock Drag](../electron-toolbar/electron-app/patterns/hover-to-lock-drag.md) — drag with hover-based activation
- [Dwell Activation](../electron-toolbar/electron-app/patterns/dwell-activation.md) — button activation by hover duration
- [Dwell Click](../electron-toolbar/electron-app/patterns/dwell-click.md) · [Dwell Drag](../electron-toolbar/electron-app/patterns/dwell-drag.md) · [Dwell Countdown](../electron-toolbar/electron-app/patterns/dwell-countdown.md)
- [Toggle Pattern](../electron-toolbar/electron-app/patterns/toggle-pattern.md) — state management for toggles
- [Mouse Hover Detection](../electron-toolbar/electron-app/patterns/mouse-hover-detection.md) — polling vs event detection

---

## Resources

- [WebAIM - Motor Disabilities](https://webaim.org/articles/motor/)
- [WCAG 2.1 - Pointer Gestures](https://www.w3.org/WAI/WCAG21/Understanding/pointer-gestures.html)
- [Inclusive Design Principles](https://inclusivedesignprinciples.org/)

---

**Last Updated:** 2026-01-12
