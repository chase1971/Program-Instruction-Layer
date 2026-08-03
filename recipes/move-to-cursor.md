# Move-to-Cursor Pattern

A reusable pattern for moving overlay windows to the cursor position with configurable offsets. This pattern works in both Python (Tkinter) and Electron (JavaScript) environments.

## Overview

The move-to-cursor pattern allows overlay windows to "teleport" to a position relative to the cursor when triggered by a hotkey. This is useful for repositioning overlays that may have been moved off-screen or to a different monitor.

**Key Concept**: Calculate new position as `cursor_position + offset`, then clamp to monitor bounds and apply.

## Python Implementation (Tkinter)

**Reference**: `modules/scroll_module.py` - `move_to_cursor()` function

### Pattern Structure

```python
def move_to_cursor() -> None:
    """Move movable overlays to cursor position"""
    # 1. Check prerequisites
    if not HAS_PYAUTOGUI or not state.instances:
        return
    
    # 2. Get cursor position
    mx, my = pyautogui.position()
    
    # 3. Calculate position with offset
    pos_x = mx + OFFSET_X
    pos_y = my + OFFSET_Y
    
    # 4. For each instance, clamp and move
    for instance in state.instances:
        if not instance.movable:
            continue
        
        # Get dimensions
        aw = instance.arrow_window.winfo_width()
        ah = instance.arrow_window.winfo_height()
        cw = instance.config_window.winfo_width()
        ch = instance.config_window.winfo_height()
        
        # Clamp to monitor
        px, py = clamp_to_monitor(pos_x, pos_y, aw, ah + ch)
        
        # Set position (geometry format: "widthxheight+x+y")
        instance.arrow_window.geometry(f"{aw}x{ah}+{px}+{py}")
        instance.config_window.geometry(f"{cw}x{ch}+{px}+{py + ah}")
```

### Key Components

1. **Cursor Position**: `pyautogui.position()` returns `(x, y)` tuple
2. **Offset Constants**: Defined in `scroll_constants.py`
   - `OFFSET_X = 60` (positions overlay to the right of cursor)
   - `OFFSET_Y = -ARROW_HEIGHT // 2` (centers vertically on cursor)
3. **Window Movement**: `window.geometry("widthxheight+x+y")` sets position
4. **Clamping**: `clamp_to_monitor()` ensures window stays within monitor bounds

### Constants

```python
# From scroll_constants.py
OFFSET_X = 60
OFFSET_Y = -ARROW_HEIGHT // 2  # Centers vertically
```

## Electron Implementation (JavaScript)

**Reference**: `electron-toolbar/src/main.js` - `moveArrowToCursor()` function

### Pattern Structure

```javascript
function moveArrowToCursor() {
    // 1. Check prerequisites
    if (!arrowOverlayWindow) {
        return;
    }
    
    if (arrowOverlayWindow.isDestroyed()) {
        arrowOverlayWindow = null;
        return;
    }
    
    // 2. Ensure window is visible (Electron requirement)
    if (!arrowOverlayWindow.isVisible()) {
        arrowOverlayWindow.show();
    }
    
    try {
        // 3. Get cursor position
        const point = screen.getCursorScreenPoint();
        const mx = point.x;
        const my = point.y;
        
        // 4. Get window dimensions
        const bounds = arrowOverlayWindow.getBounds();
        const aw = bounds.width;
        const ah = bounds.height;
        
        // 5. Calculate position with offset (same as Python)
        const OFFSET_X = 60;
        const OFFSET_Y = -ah / 2;  // Same as -ARROW_HEIGHT // 2
        
        const pos_x = mx + OFFSET_X;
        const pos_y = my + OFFSET_Y;
        
        // 6. Clamp to monitor
        const clamped = clampToMonitor(pos_x, pos_y, aw, ah);
        
        // 7. Move window (use setBounds for reliability)
        arrowOverlayWindow.setBounds({
            x: Math.round(clamped.x),
            y: Math.round(clamped.y),
            width: aw,
            height: ah
        });
        
        // 8. Save position (optional, for persistence)
        store.set('arrow_overlay_bounds', { 
            x: Math.round(clamped.x), 
            y: Math.round(clamped.y), 
            width: aw, 
            height: ah 
        });
    } catch (error) {
        console.log(`[ARROW] ERROR: ${error.message}`);
        if (error.message.includes('destroyed')) {
            arrowOverlayWindow = null;
        }
    }
}
```

### Key Differences from Python

1. **Cursor Position API**:
   - Python: `pyautogui.position()` → `(x, y)` tuple
   - Electron: `screen.getCursorScreenPoint()` → `{x, y}` object
   - Access: `point.x` and `point.y` (not tuple unpacking)

2. **Window Dimensions**:
   - Python: `window.winfo_width()` and `window.winfo_height()` (separate calls)
   - Electron: `window.getBounds()` → `{x, y, width, height}` object
   - Access: `bounds.width` and `bounds.height`

3. **Window Movement**:
   - Python: `window.geometry("widthxheight+x+y")` (string format)
   - Electron: `window.setBounds({x, y, width, height})` (object)
   - **Important**: Use `setBounds()` instead of `setPosition()` for reliability

4. **Visibility Check**:
   - Python: No visibility check needed (Tkinter handles it)
   - Electron: **Must check `isVisible()`** - `setBounds()` may not work on hidden windows
   - Solution: Call `window.show()` if not visible

5. **Error Handling**:
   - Python: Simple return on error
   - Electron: Must check `isDestroyed()` and handle exceptions
   - Must clear window reference if destroyed

6. **Coordinate Rounding**:
   - Python: Tkinter handles integer coordinates automatically
   - Electron: **Must round coordinates** - `Math.round()` prevents floating-point issues

7. **Clamp Function**:
   - Python: Returns `(x, y)` tuple
   - Electron: Returns `{x, y}` object
   - Access: `clamped.x` and `clamped.y`

## Signal Integration

Both implementations are triggered via the signal system:

### Python (main.py)
```python
ADDITIONAL_HOTKEYS = {
    "f14": "move_scroll",  # Scroll module
    "f23": "move_arrow",   # Arrow module (Electron)
}
```

### Electron (main.js)
```javascript
function handleSignal(signalName, data) {
    switch (signalName) {
        case 'move_arrow':
            moveArrowToCursor();
            break;
    }
}
```

## Critical Implementation Notes

### Electron-Specific Requirements

1. **Always check visibility**: `setBounds()` may silently fail on hidden windows
   ```javascript
   if (!arrowOverlayWindow.isVisible()) {
       arrowOverlayWindow.show();
   }
   ```

2. **Use setBounds, not setPosition**: `setBounds()` is more reliable for moving windows
   ```javascript
   // Good
   arrowOverlayWindow.setBounds({ x, y, width, height });
   
   // Less reliable
   arrowOverlayWindow.setPosition(x, y);
   ```

3. **Round coordinates**: Prevents floating-point positioning issues
   ```javascript
   x: Math.round(clamped.x),
   y: Math.round(clamped.y)
   ```

4. **Check for destroyed windows**: Electron windows can be destroyed
   ```javascript
   if (arrowOverlayWindow.isDestroyed()) {
       arrowOverlayWindow = null;
       return;
   }
   ```

5. **Handle exceptions**: Electron APIs can throw errors
   ```javascript
   try {
       // Move window
   } catch (error) {
       // Handle error, clear reference if needed
   }
   ```

### Python-Specific Notes

1. **Simple and direct**: Tkinter's `geometry()` is straightforward
2. **No visibility check needed**: Works on hidden windows
3. **Multiple instances**: Can move multiple windows in a loop
4. **Tuple unpacking**: Natural Python pattern for coordinates

## Offset Calculation

Both implementations use the same offset pattern:

```python
# Python
OFFSET_X = 60
OFFSET_Y = -ARROW_HEIGHT // 2  # Centers vertically
```

```javascript
// Electron
const OFFSET_X = 60;
const OFFSET_Y = -ah / 2;  // Centers vertically
```

**Result**: Overlay appears 60 pixels to the right of cursor, vertically centered.

## Clamp-to-Monitor Function

Both use similar clamping logic:

### Python
```python
def clamp_to_monitor(x, y, width, height):
    # Find monitor containing point
    # Clamp to monitor bounds
    return (clamped_x, clamped_y)
```

### Electron
```javascript
function clampToMonitor(x, y, width, height) {
    // Find display containing point
    // Clamp to display bounds
    return { x: clampedX, y: clampedY };
}
```

**Key Difference**: Python returns tuple `(x, y)`, Electron returns object `{x, y}`.

## Template: Electron Move-to-Cursor

```javascript
function moveOverlayToCursor() {
    // Prerequisites
    if (!overlayWindow) return;
    if (overlayWindow.isDestroyed()) {
        overlayWindow = null;
        return;
    }
    
    // Ensure visible
    if (!overlayWindow.isVisible()) {
        overlayWindow.show();
    }
    
    try {
        // Get cursor
        const point = screen.getCursorScreenPoint();
        const mx = point.x;
        const my = point.y;
        
        // Get dimensions
        const bounds = overlayWindow.getBounds();
        const aw = bounds.width;
        const ah = bounds.height;
        
        // Calculate with offset
        const OFFSET_X = 60;
        const OFFSET_Y = -ah / 2;
        const pos_x = mx + OFFSET_X;
        const pos_y = my + OFFSET_Y;
        
        // Clamp
        const clamped = clampToMonitor(pos_x, pos_y, aw, ah);
        
        // Move
        overlayWindow.setBounds({
            x: Math.round(clamped.x),
            y: Math.round(clamped.y),
            width: aw,
            height: ah
        });
    } catch (error) {
        console.error('[MODULE] Move error:', error);
        if (error.message.includes('destroyed')) {
            overlayWindow = null;
        }
    }
}
```

## Template: Python Move-to-Cursor

```python
def move_to_cursor() -> None:
    """Move overlay to cursor position"""
    if not HAS_PYAUTOGUI or not state.instances:
        return
    
    mx, my = pyautogui.position()
    pos_x = mx + OFFSET_X
    pos_y = my + OFFSET_Y
    
    for instance in state.instances:
        if not instance.movable:
            continue
        
        aw = instance.window.winfo_width()
        ah = instance.window.winfo_height()
        
        px, py = clamp_to_monitor(pos_x, pos_y, aw, ah)
        instance.window.geometry(f"{aw}x{ah}+{px}+{py}")
```

## Use Cases

- **Scroll Module**: F14 hotkey moves scroll overlay to cursor
- **Arrow Module**: F23 hotkey moves arrow overlay to cursor
- **Any Overlay**: Can be applied to any overlay window system

## Key Takeaways

1. **Same calculation logic**: Both use `cursor + offset` pattern
2. **Different APIs**: Python uses Tkinter, Electron uses BrowserWindow
3. **Electron requires more checks**: Visibility, destroyed state, error handling
4. **Electron needs rounding**: Floating-point coordinates can cause issues
5. **Both need clamping**: Monitor bounds must be respected
6. **Simple is better**: Minimal state checks, just move the window

## References

- **Python Implementation**: `modules/scroll_module.py:814-837`
- **Electron Implementation**: `electron-toolbar/src/main.js:531-605`
- **Clamp Function**: `electron-toolbar/src/window-helpers.js:99-118`
- **Signal Integration**: `main.py:83` (F23 hotkey)
