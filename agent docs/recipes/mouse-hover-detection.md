# Mouse Hover Detection Pattern

> **You might say:** "detect when the cursor is over a region", "polling vs events", "the hover never fires"
> **What it is:** Deciding between polling and DOM events for hover, and hit-testing cursor position against regions.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/modules/scroll/backend/scroll_module.py` — _poll_scroll`, `_start_polling
- `electron-toolbar/modules/volume_module.py`
- `electron-toolbar/electron-app/src/window-helpers.js`

---

## Overview

A pattern for detecting when the mouse cursor is over specific regions of an overlay window and triggering actions based on hover state.

## Pattern Description

This pattern enables click-through overlays that become interactive when the cursor hovers over specific regions (like buttons or controls).

## Implementation Approaches

### 1. Polling-Based Detection (Python/Tkinter)

Continuously poll mouse position and check if it's within bounds:

```python
def _poll_mouse(self):
    if not self.window:
        return
    
    mx, my = pyautogui.position()
    wx = self.window.winfo_rootx()
    wy = self.window.winfo_rooty()
    ww = self.window.winfo_width()
    wh = self.window.winfo_height()
    
    # Check if cursor is over button region
    button_x = wx + BUTTON_OFFSET_X
    button_y = wy + BUTTON_OFFSET_Y
    button_w = BUTTON_WIDTH
    button_h = BUTTON_HEIGHT
    
    if (button_x <= mx <= button_x + button_w and 
        button_y <= my <= button_y + button_h):
        # Cursor is over button
        if not self.button_hovered:
            self._on_button_enter()
            self.button_hovered = True
    else:
        # Cursor left button
        if self.button_hovered:
            self._on_button_leave()
            self.button_hovered = False
    
    # Schedule next poll
    self.window.after(POLL_INTERVAL_MS, self._poll_mouse)
```

### 2. Event-Based Detection (Electron/HTML)

Use native mouse events on interactive elements:

```javascript
button.addEventListener('mouseenter', () => {
    // Tell main process to enable mouse events
    ipcRenderer.send('mouse-on-button', true);
    // Trigger action
    onButtonHover();
});

button.addEventListener('mouseleave', () => {
    // Tell main process to re-enable click-through
    ipcRenderer.send('mouse-on-button', false);
    // Cleanup
    onButtonLeave();
});
```

### 3. Hybrid Approach (Click-Through Windows)

For click-through windows that need to become interactive on hover:

**Electron:**
```javascript
// Window starts click-through
win.setIgnoreMouseEvents(true, { forward: true });

// On hover detection, disable click-through
ipcMain.on('mouse-on-button', (event, isOnButton) => {
    win.setIgnoreMouseEvents(!isOnButton, { forward: true });
});
```

**Python/Tkinter:**
```python
# Window is click-through by default
make_click_through(window)

# On hover, temporarily disable click-through
def _on_button_enter():
    # Remove transparent flag to allow interaction
    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style &= ~WS_EX_TRANSPARENT  # Remove transparent
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
```

## Region Detection Patterns

### Rectangular Regions

```python
def is_cursor_in_region(mx, my, region_x, region_y, region_w, region_h):
    return (region_x <= mx <= region_x + region_w and
            region_y <= my <= region_y + region_h)
```

### Circular Regions

```python
def is_cursor_in_circle(mx, my, center_x, center_y, radius):
    dx = mx - center_x
    dy = my - center_y
    distance = math.sqrt(dx**2 + dy**2)
    return distance <= radius
```

### Multiple Regions

```python
def detect_region(mx, my, regions):
    """Check which region cursor is in"""
    for region_name, (x, y, w, h) in regions.items():
        if is_cursor_in_region(mx, my, x, y, w, h):
            return region_name
    return None
```

## State Management

Track hover state to avoid redundant actions:

```python
class HoverState:
    def __init__(self):
        self.current_region = None
        self.last_region = None
    
    def update(self, mx, my):
        self.last_region = self.current_region
        self.current_region = detect_region(mx, my)
        
        # Only trigger on change
        if self.current_region != self.last_region:
            if self.last_region:
                self._on_leave(self.last_region)
            if self.current_region:
                self._on_enter(self.current_region)
```

## Action Triggers

### Immediate Actions

Trigger immediately when entering region:

```python
def _on_enter(region):
    if region == "button_up":
        keyboard.press('w')
    elif region == "button_down":
        keyboard.press('s')
```

### Continuous Actions

Trigger repeatedly while in region:

```python
def _poll_actions(self):
    region = detect_current_region()
    
    if region and region != self.last_region:
        # Direction change - immediate action
        self._trigger_action(region)
        self.last_action_time = time.time()
    
    if region:
        # Continuous action
        now = time.time()
        if now - self.last_action_time >= ACTION_INTERVAL:
            self._trigger_action(region)
            self.last_action_time = now
    
    self.last_region = region
    self.window.after(POLL_INTERVAL, self._poll_actions)
```

## Performance Optimization

### Throttling

Limit how often detection runs:

```python
POLL_INTERVAL_MS = ...  # see electron-toolbar/modules/dwell/backend/dwell_constants.py — SLEEP_MAIN_LOOP
```

### Early Exit

Skip detection if window not visible:

```python
def _poll_mouse(self):
    if not self.window or not self.window.winfo_exists():
        return
    if not self.window.winfo_viewable():
        return
    # ... detection logic
```

### Bounding Box Check

Quick check before detailed region detection:

```python
# Quick check: is cursor anywhere near window?
wx, wy = window.winfo_rootx(), window.winfo_rooty()
ww, wh = window.winfo_width(), window.winfo_height()
padding = 100  # Detection padding

if not (wx - padding <= mx <= wx + ww + padding and
        wy - padding <= my <= wy + wh + padding):
    return  # Cursor nowhere near, skip detailed detection
```

## Common Use Cases

### 1. Directional Controls (WASD/Arrows)

```python
regions = {
    'up': (center_x - 32, center_y - 40, 64, 40),
    'down': (center_x - 32, center_y, 64, 40),
    'left': (center_x - 40, center_y - 32, 40, 64),
    'right': (center_x, center_y - 32, 40, 64)
}
```

### 2. Scroll Zones

```python
# Top half = scroll up, bottom half = scroll down
if rel_y < height // 2:
    direction = "up"
else:
    direction = "down"
```

### 3. Button Hover States

```python
if cursor_in_button:
    button.config(bg=HOVER_COLOR)
    if not was_hovered:
        trigger_hover_action()
else:
    button.config(bg=NORMAL_COLOR)
```

## Related Patterns

- See `hover-to-lock-drag.md` for drag interaction
- See `scroll-calculation.md` for scroll-specific detection
