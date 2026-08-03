# Scroll Calculation Pattern

> **You might say:** "scroll faster near the edge", "region to scroll speed", "it scrolls the wrong way"
> **What it is:** Map cursor position within an overlay region to a scroll direction and speed, with detection padding.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/modules/scroll/backend/scroll_module.py — `_poll_scroll`, `DragHandler``
- `electron-toolbar/modules/scroll/backend/scroll_profiles.py`

---

## Overview

A pattern for detecting mouse position relative to an overlay and triggering continuous scrolling based on which region the cursor is in.

## Pattern Description

The scroll overlay divides the arrow window into two regions:
- **Top half**: Scroll up
- **Bottom half**: Scroll down

When the cursor hovers over the overlay, it continuously scrolls in the detected direction at a configurable speed.

## Implementation Structure

### Detection Area

The overlay has a detection zone that may extend beyond the visual bounds:

```python
# Get window bounds
ax = window.winfo_rootx()  # Absolute X position
ay = window.winfo_rooty()  # Absolute Y position
aw = window.winfo_width()  # Window width
ah = window.winfo_height() # Window height

# Detection area (with padding for easier activation)
in_x = (ax - DETECTION_PADDING_X) <= mx <= (ax + aw + DETECTION_PADDING_X)
in_y = ay <= my <= ay + ah
```

### Direction Calculation

```python
if in_x and in_y:
    # Calculate relative Y position within window
    rel_y = my - ay
    
    # Determine direction based on which half
    direction = "up" if rel_y < (ah // 2) else "down"
```

### Continuous Scrolling

The scroll action is triggered:
1. **Immediately** when direction changes
2. **Repeatedly** at intervals while cursor remains in region

```python
# Check for direction change
if direction != self.last_direction:
    self.last_direction = direction
    self.last_scroll_time = time.time() * 1000
    # Immediate scroll
    pyautogui.scroll(scroll_amount if direction == "up" else -scroll_amount)

# Continuous scrolling at intervals
now = time.time() * 1000
if now - self.last_scroll_time >= SCROLL_DELAY_MS:
    pyautogui.scroll(scroll_amount if direction == "up" else -scroll_amount)
    self.last_scroll_time = now
```

### Polling Loop

The detection runs in a polling loop:

```python
def _poll_scroll(self):
    if not self.window or not window.winfo_exists():
        return
    
    mx, my = pyautogui.position()
    
    # Detection logic
    if cursor_in_overlay(mx, my):
        direction = calculate_direction(mx, my)
        trigger_scroll(direction)
    
    # Schedule next poll
    self.window.after(POLL_INTERVAL_MS, self._poll_scroll)
```

## Key Components

### 1. Detection Padding

Allows easier activation by extending detection zone:

```python
DETECTION_PADDING_X = ...  # see electron-toolbar/modules/scroll/backend/
```

This makes it easier to trigger scrolling without precise cursor placement.

### 2. Scroll Amount

Configurable scroll speed:

```python
SCROLL_OPTIONS = [20, 40, 60, 90]  # Pixels per scroll
DEFAULT_SCROLL_AMOUNT = ...  # see electron-toolbar/modules/scroll/backend/
```

### 3. Scroll Delay

Time between scroll events:

```python
SCROLL_DELAY_MS = ...  # see electron-toolbar/modules/scroll/backend/
```

Lower values = faster continuous scrolling.

### 4. Poll Interval

How often to check cursor position:

```python
POLL_INTERVAL_MS = ...  # see electron-toolbar/modules/scroll/backend/
```

## Complete Code Template

```python
class ScrollInstance:
    def __init__(self):
        self.last_direction = None
        self.last_scroll_time = 0
        self.scroll_amount = DEFAULT_SCROLL_AMOUNT
        self._start_polling()
    
    def _poll_scroll(self):
        if not self.window:
            return
        
        mx, my = pyautogui.position()
        ax = self.window.winfo_rootx()
        ay = self.window.winfo_rooty()
        aw = self.window.winfo_width()
        ah = self.window.winfo_height()
        
        # Check if cursor is in detection area
        in_x = (ax - DETECTION_PADDING_X) <= mx <= (ax + aw + DETECTION_PADDING_X)
        in_y = ay <= my <= ay + ah
        
        if in_x and in_y:
            # Calculate direction
            rel_y = my - ay
            direction = "up" if rel_y < (ah // 2) else "down"
            
            # Direction change - immediate scroll
            if direction != self.last_direction:
                self.last_direction = direction
                self.last_scroll_time = time.time() * 1000
                self._do_scroll(direction)
            
            # Continuous scroll
            now = time.time() * 1000
            if now - self.last_scroll_time >= SCROLL_DELAY_MS:
                self._do_scroll(direction)
                self.last_scroll_time = now
        else:
            # Cursor left overlay
            if self.last_direction:
                self.last_direction = None
        
        # Schedule next poll
        self.window.after(POLL_INTERVAL_MS, self._poll_scroll)
    
    def _do_scroll(self, direction):
        amount = self.scroll_amount if direction == "up" else -self.scroll_amount
        pyautogui.scroll(amount)
```

## Variations

### Multi-Direction

Can extend to 4 directions (up/down/left/right):

```python
rel_x = mx - ax
rel_y = my - ay

if rel_y < (ah // 3):
    direction = "up"
elif rel_y > (ah * 2 // 3):
    direction = "down"
elif rel_x < (aw // 2):
    direction = "left"
else:
    direction = "right"
```

### Radial Zones

For circular overlays, use distance from center:

```python
center_x = ax + aw // 2
center_y = ay + ah // 2
dx = mx - center_x
dy = my - center_y
angle = math.atan2(dy, dx)
direction = angle_to_direction(angle)
```

### Speed Zones

Different speeds based on distance from center:

```python
distance = math.sqrt(dx**2 + dy**2)
max_distance = math.sqrt((aw//2)**2 + (ah//2)**2)
speed_factor = distance / max_distance
scroll_amount = int(BASE_SCROLL * speed_factor)
```

## Performance Considerations

1. **Poll Interval**: Balance between responsiveness and CPU usage
   - Too frequent: High CPU usage
   - Too infrequent: Laggy response
   - 50ms is a good default

2. **Scroll Delay**: Controls scroll rate
   - Lower = faster scrolling but more events
   - Higher = smoother but slower

3. **Detection Padding**: Makes activation easier but increases detection area

## Related Patterns

- See `hover-to-lock-drag.md` for drag positioning
- See `mouse-hover-detection.md` for general hover patterns
