# Window Positioning Pattern

> **You might say:** "it opened off-screen", "wrong monitor", "keep it on the screen I am using"
> **What it is:** Clamp overlay windows to monitor bounds and handle multi-monitor setups.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/electron-app/src/window-helpers.js — `clampToMonitor``
- `electron-toolbar/electron-app/src/window-managers/alt-manager.js`
- `electron-toolbar/modules/scroll/backend/scroll_module.py — `clamp_to_monitor` (Python side)`

---

## Overview

A pattern for keeping overlay windows within monitor bounds and handling multi-monitor setups.

## Pattern Description

When positioning or moving overlay windows, they must be clamped to stay within the visible area of the monitor they're on. This prevents windows from being positioned off-screen or spanning multiple monitors incorrectly.

## Implementation

### Monitor Detection

Find which monitor contains a point:

```python
def find_monitor_for_point(x, y):
    monitors = screeninfo_get_monitors()
    for monitor in monitors:
        if (monitor.x <= x <= monitor.x + monitor.width and
            monitor.y <= y <= monitor.y + monitor.height):
            return monitor
    return monitors[0]  # Fallback to first monitor
```

### Clamping to Monitor

```python
def clamp_to_monitor(x, y, width, height):
    """Clamp window position to stay within monitor bounds"""
    monitors = screeninfo_get_monitors()
    
    # Find monitor containing the point
    target = None
    for monitor in monitors:
        if (monitor.x <= x <= monitor.x + monitor.width and
            monitor.y <= y <= monitor.y + monitor.height):
            target = monitor
            break
    
    if not target:
        target = monitors[0]  # Fallback
    
    # Clamp coordinates
    clamped_x = max(
        target.x,
        min(x, target.x + target.width - width)
    )
    clamped_y = max(
        target.y,
        min(y, target.y + target.height - height)
    )
    
    return clamped_x, clamped_y
```

### Electron Implementation

```javascript
function clampToMonitor(x, y, width, height) {
    const displays = screen.getAllDisplays();
    
    for (const display of displays) {
        if (display.bounds.x <= x && x <= display.bounds.x + display.bounds.width &&
            display.bounds.y <= y && y <= display.bounds.y + display.bounds.height) {
            const clampedX = Math.max(
                display.bounds.x,
                Math.min(x, display.bounds.x + display.bounds.width - width)
            );
            const clampedY = Math.max(
                display.bounds.y,
                Math.min(y, display.bounds.y + display.bounds.height - height)
            );
            return { x: clampedX, y: clampedY };
        }
    }
    
    return { x, y };  // Fallback
}
```

## Use Cases

### 1. Initial Positioning

When creating a window, clamp default position:

```python
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
default_x = (screen_w - WINDOW_WIDTH) // 2
default_y = (screen_h - WINDOW_HEIGHT) // 2

x, y = clamp_to_monitor(default_x, default_y, WINDOW_WIDTH, WINDOW_HEIGHT)
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
```

### 2. Drag Movement

When dragging, clamp new position:

```python
def on_drag(new_x, new_y):
    x, y = clamp_to_monitor(new_x, new_y, window_width, window_height)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
```

### 3. Cursor Following

When following cursor, clamp ghost position:

```python
def follow_cursor():
    cx, cy = pyautogui.position()
    new_x = cx - offset_x
    new_y = cy - offset_y
    new_x, new_y = clamp_to_monitor(new_x, new_y, width, height)
    ghost_window.setPosition(new_x, new_y)
```

## Multi-Monitor Considerations

### Primary vs All Monitors

```python
# Get primary display
primary = screen.getPrimaryDisplay()

# Get all displays
displays = screen.getAllDisplays()
```

### Monitor Selection

When positioning at cursor:

```python
def position_at_cursor():
    mx, my = pyautogui.position()
    
    # Find which monitor cursor is on
    for display in displays:
        if (display.bounds.x <= mx <= display.bounds.x + display.bounds.width and
            display.bounds.y <= my <= display.bounds.y + display.bounds.height):
            # Position relative to this monitor
            x = display.bounds.x + (display.bounds.width - WINDOW_WIDTH) // 2
            y = display.bounds.y + (display.bounds.height - WINDOW_HEIGHT) // 2
            break
```

### Duplicate Display Handling

Some systems report duplicate displays. Filter them:

```python
def get_unique_monitors():
    """Filter out duplicate displays"""
    seen = set()
    unique = []
    for monitor in monitors:
        key = (monitor.x, monitor.y, monitor.width, monitor.height)
        if key not in seen:
            seen.add(key)
            unique.append(monitor)
    return unique
```

## Edge Cases

### Window Larger Than Monitor

```python
def clamp_to_monitor(x, y, width, height):
    # If window is larger than monitor, center it
    if width > monitor.width:
        x = monitor.x + (monitor.width - width) // 2
    if height > monitor.height:
        y = monitor.y + (monitor.height - height) // 2
    
    # Then clamp normally
    x = max(monitor.x, min(x, monitor.x + monitor.width - width))
    y = max(monitor.y, min(y, monitor.y + monitor.height - height))
```

### Negative Coordinates

Some systems allow negative coordinates (extended desktop):

```python
# Handle negative coordinates
if x < 0:
    # Find leftmost monitor
    leftmost = min(monitors, key=lambda m: m.x)
    if x < leftmost.x:
        x = leftmost.x
```

## Related Patterns

- See `hover-to-lock-drag.md` for drag positioning usage
- See `window-helpers.js` for reusable implementation
