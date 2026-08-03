# Hover-to-Lock Drag Pattern

> **You might say:** "drag handle on an overlay", "hover the handle then it follows", "ghost overlay"
> **What it is:** Hover a handle to lock drag, ghost overlay follows the cursor, snaps when the cursor stops.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/modules/scroll/backend/scroll_module.py` — DragHandler`, `_start_polling
- `electron-toolbar/modules/scroll/backend/scroll_placement_ui.py`
- `electron-toolbar/electron-app/src/window-managers/arrow-manager.js`

---

## Overview

A reusable drag interaction pattern that allows users to move overlay windows by hovering over a drag handle, then having a ghost overlay follow the cursor until it stops moving.

## Pattern Description

Instead of requiring click-and-drag, this pattern:
1. User hovers over drag handle for a set duration (e.g., 0.5 seconds)
2. Drag mode "locks" and a ghost overlay appears
3. Ghost follows cursor position
4. When cursor stops moving for a set time (e.g., 0.25 seconds), the actual window snaps to ghost position
5. Cooldown period prevents accidental re-locking

## Implementation Structure

### State Variables

```python
class DragHandler:
    # Lock state
    locked: bool = False
    hover_start: Optional[float] = None
    hover_timer: Optional[str] = None
    cooldown_end: Optional[float] = None
    
    # Ghost window
    ghost_window: Optional[tk.Toplevel] = None
    
    # Cursor tracking
    offset_x: Optional[int] = None  # Cursor offset from window
    offset_y: Optional[int] = None
    last_cursor: Optional[Tuple[int, int]] = None
    last_move_time: Optional[float] = None
    has_moved: bool = False
    first_stop: bool = False  # Track first stop vs second stop
```

### Constants

```python
HOVER_LOCK_TIME = ...      # Seconds to hover before lock
IDLE_SNAP_TIME = ...       # Seconds idle before snap
DRAG_COOLDOWN_TIME = ...   # Cooldown after snap
CURSOR_FOLLOW_INTERVAL = ...  # ghost follow update rate
```

### Event Flow

1. **Mouse Enter** (`_on_enter`):
   - Start hover timer
   - Change drag handle color to hover state
   - Timer set for `HOVER_LOCK_TIME`

2. **Mouse Leave** (`_on_leave`):
   - Cancel hover timer if not locked
   - Reset handle color if not locked

3. **Hover Lock** (`_check_hover_lock`):
   - After `HOVER_LOCK_TIME`, set `locked = True`
   - Create ghost overlay window
   - Change handle color to active/locked state
   - Start cursor following loop

4. **Cursor Following** (`_follow_cursor`):
   - Calculate offset on first call (cursor position - window position)
   - Update ghost position: `new_pos = cursor - offset`
   - Clamp to monitor bounds
   - Track cursor movement:
     - If cursor moved: reset idle timer
     - If cursor stopped and `has_moved == True`:
       - First stop: set `first_stop = True`, reset timer
       - Second stop: trigger snap

5. **Snap to Ghost** (`_snap_to_ghost`):
   - Move actual window to ghost position
   - Destroy ghost window
   - Reset all state
   - Set cooldown period
   - Reset handle color

### Ghost Window Creation

The ghost window is a semi-transparent copy that:
- Matches the size of the original window
- Has reduced opacity (e.g., 0.6)
- Is click-through
- Follows cursor smoothly
- Provides visual feedback of where window will snap

### Code Template

```python
class DragHandler:
    def __init__(self, window, drag_handle):
        self.window = window
        self.drag_handle = drag_handle
        self.locked = False
        self.hover_timer = None
        self.ghost_window = None
        # ... other state
        
        drag_handle.bind("<Enter>", self._on_enter)
        drag_handle.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        if self.cooldown_end and time.time() < self.cooldown_end:
            return
        self.drag_handle.config(bg=HOVER_COLOR)
        self.hover_start = time.time()
        self.hover_timer = self.window.after(
            int(HOVER_LOCK_TIME * 1000), 
            self._check_hover_lock
        )
    
    def _check_hover_lock(self):
        if time.time() - self.hover_start >= HOVER_LOCK_TIME:
            self.locked = True
            self._create_ghost()
            self.drag_handle.config(bg=ACTIVE_COLOR)
            self._follow_cursor()
    
    def _follow_cursor(self):
        if not self.locked:
            return
        
        cx, cy = pyautogui.position()
        
        # Calculate offset on first call
        if self.offset_x is None:
            wx, wy = self.window.winfo_x(), self.window.winfo_y()
            self.offset_x = cx - wx
            self.offset_y = cy - wy
        
        # Update ghost position
        new_x = cx - self.offset_x
        new_y = cy - self.offset_y
        new_x, new_y = clamp_to_monitor(new_x, new_y)
        self.ghost_window.setPosition(new_x, new_y)
        
        # Check for cursor stop
        if self.last_cursor:
            cursor_moved = (cx != self.last_cursor[0] or cy != self.last_cursor[1])
            if cursor_moved:
                self.has_moved = True
                self.last_move_time = time.time()
                self.first_stop = False
            elif self.has_moved and self.last_move_time:
                idle = time.time() - self.last_move_time
                if idle >= IDLE_SNAP_TIME:
                    if not self.first_stop:
                        self.first_stop = True
                        self.last_move_time = time.time()
                    else:
                        self._snap_to_ghost()
                        return
        
        self.last_cursor = (cx, cy)
        self.window.after(CURSOR_FOLLOW_INTERVAL, self._follow_cursor)
```

## Usage Examples

### Python/Tkinter (Scroll Module)

```python
drag_handler = DragHandler(instance, drag_handle_widget)
# Automatically handles all drag interactions
```

### Electron/JavaScript — **poll, do not listen**

> 🔴 **This is the mistake this recipe exists to prevent.** An earlier version of this
> doc showed `dragHandle.addEventListener('mouseenter', …)`. **That silently never
> fires.** Live overlays are created click-through (`setIgnoreMouseEvents` — see
> `recipes/click-through-windows.md`), so the OS never delivers mouse events to the
> window and no DOM hover event is ever raised. Following it produces a handle that
> looks correct and does nothing.

The working approach polls the cursor position against the handle's rect from the
**main process**, the same way `scroll_module.py` does on the Python side:

```javascript
// main process — poll, because the overlay window is click-through
const POLL_MS = /* see cursor-patterns/dwell-and-head-mouse.md */;

setInterval(() => {
    const { x, y } = screen.getCursorScreenPoint();
    const over = pointInRect({ x, y }, handleRectOnScreen());

    if (over && !hoverStart) hoverStart = Date.now();
    if (!over) { hoverStart = null; return; }

    if (Date.now() - hoverStart >= HOVER_LOCK_MS) lockDrag();
}, POLL_MS);
```

**Do not restate the timing values here** — `POLL_MS` and `HOVER_LOCK_MS` live in
`cursor-patterns/dwell-and-head-mouse.md` and
`electron-toolbar/modules/dwell/backend/dwell_constants.py`.

Exception: if the window is **not** click-through (a normal focusable window), DOM
events work fine. Check how the window was created before choosing.

## Key Design Decisions

1. **Two-Stop Detection**: Requires cursor to stop twice before snapping
   - Prevents accidental snaps during slow movement
   - First stop resets timer, second stop triggers snap

2. **Cooldown Period**: Prevents immediate re-locking after snap
   - Gives user time to adjust if needed
   - Prevents accidental drag activation

3. **Offset Calculation**: Calculated on first follow call
   - Preserves relative position between cursor and window
   - Makes dragging feel natural

4. **Ghost Overlay**: Visual feedback of final position
   - User can see where window will move
   - Semi-transparent so it doesn't obstruct view

## Variations

- **Manual Drag Fallback**: Can also support click-and-drag for users who prefer it
- **Different Lock Times**: Can adjust `HOVER_LOCK_TIME` for different use cases
- **Multiple Ghosts**: For windows with multiple parts (like scroll module's arrow + config windows)

## Related Patterns

- See `mouse-hover-detection.md` for hover detection patterns
- See `window-positioning.md` for monitor clamping logic
