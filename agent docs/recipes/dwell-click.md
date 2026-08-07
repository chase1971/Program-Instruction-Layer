# Dwell Click Pattern

> **You might say:** "click by holding still", "dwell mode 1", "it clicks when I do not want it to"
> **What it is:** Trigger a click by keeping the cursor stationary for a duration, with progress feedback and movement cancel.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/modules/dwell/backend/dwell_module.py`
- `electron-toolbar/modules/dwell/backend/dwell_constants.py` — every timing, named
- `electron-toolbar/modules/dwell/backend/dwell_persisted_settings.json` — the overrides that actually run

---

## Overview

A pattern for triggering mouse clicks by keeping the cursor stationary at a position for a set duration (dwell time). Provides visual progress feedback and can be cancelled by movement.

## Pattern Description

The dwell click pattern:
1. Detects when cursor stops moving
2. Starts a timer and shows progress
3. If cursor remains stationary for the full dwell time, triggers a click
4. If cursor moves during dwell, cancels and resets

## Implementation Structure

### Basic Dwell Loop

```python
def dwell_click_loop():
    current_position = pyautogui.position()
    current_time = time.time()
    
    # Skip if same position as last click (prevent double-clicks)
    if current_position == last_click_position:
        return
    
    # Start dwell timer
    start_time = time.time()
    dwell_position = current_position
    
    # Wait for dwell time while checking for movement
    while time.time() - start_time < DWELL_TIME:
        new_position = pyautogui.position()
        
        # Cancel if mouse moved
        if new_position != dwell_position:
            break
        
        # Update progress indicator
        elapsed = time.time() - start_time
        progress = elapsed / DWELL_TIME
        update_progress_indicator(progress)
        
        time.sleep(0.01)  # Small sleep to avoid CPU spinning
    else:
        # Dwell complete - trigger click
        pyautogui.mouseDown()
        time.sleep(0.02)
        pyautogui.mouseUp()
        last_click_position = current_position
        reset_progress_indicator()
```

### Key Components

#### 1. Position Tracking

Track last click position to prevent double-clicks:

```python
last_click_position = None

# Before starting dwell
if current_position == last_click_position:
    return  # Skip - already clicked here

# After successful click
last_click_position = current_position
```

#### 2. Progress Feedback

Show visual progress during dwell:

```python
def update_progress_indicator(progress: float):
    """Update progress bar/circle (0.0 to 1.0)"""
    # Example: Update progress ring
    progress_ring.set_progress(progress)
    
    # Or update overlay opacity
    overlay.set_opacity(0.3 + (progress * 0.7))
```

#### 3. Movement Detection

Continuously check if cursor moved:

```python
dwell_position = current_position

while time.time() - start_time < DWELL_TIME:
    new_position = pyautogui.position()
    
    # Check for movement
    if new_position != dwell_position:
        # Cancel dwell
        reset_progress_indicator()
        break
    
    # Continue dwell
    update_progress(elapsed / DWELL_TIME)
```

#### 4. Click Execution

Execute click after successful dwell:

```python
# Mouse down
pyautogui.mouseDown()

# Brief delay (allows some systems to register)
time.sleep(0.02)

# Mouse up
pyautogui.mouseUp()
```

## Complete Template

```python
class DwellClickHandler:
    def __init__(self, dwell_time: float = 1.0):
        self.dwell_time = dwell_time
        self.last_click_position = None
        self.dwell_start_time = None
        self.dwell_position = None
    
    def process(self):
        """Main processing loop"""
        current_position = pyautogui.position()
        current_time = time.time()
        
        # Skip if same position as last click
        if current_position == self.last_click_position:
            return
        
        # Check if cursor is stationary
        if self.dwell_position is None:
            # Start new dwell
            self.dwell_start_time = current_time
            self.dwell_position = current_position
        elif current_position != self.dwell_position:
            # Cursor moved - reset
            self.dwell_position = None
            self.dwell_start_time = None
            self.update_progress(0.0)
        else:
            # Cursor stationary - check if dwell complete
            elapsed = current_time - self.dwell_start_time
            if elapsed >= self.dwell_time:
                # Dwell complete - click
                self.trigger_click(current_position)
                self.dwell_position = None
                self.dwell_start_time = None
            else:
                # Update progress
                progress = elapsed / self.dwell_time
                self.update_progress(progress)
    
    def trigger_click(self, position):
        """Execute click at position"""
        pyautogui.mouseDown()
        time.sleep(0.02)
        pyautogui.mouseUp()
        self.last_click_position = position
    
    def update_progress(self, progress: float):
        """Update visual progress indicator"""
        # Implement progress display
        pass
```

## Variations

### 1. With Grace Period

Allow brief movement without canceling:

```python
GRACE_MOVEMENT_THRESHOLD = ...  # see electron-toolbar/modules/dwell/backend/dwell_constants.py — JIGGLE_COOLDOWN_MOVEMENT_THRESHOLD

movement = distance(current_position, dwell_position)
if movement > GRACE_MOVEMENT_THRESHOLD:
    # Significant movement - cancel
    cancel_dwell()
else:
    # Small movement - continue
    continue_dwell()
```

### 2. With Jiggle Detection

Cancel on rapid movement (jiggle):

```python
def check_jiggle(recent_positions):
    """Detect rapid back-and-forth movement"""
    if len(recent_positions) < 3:
        return False
    
    # Check for oscillation pattern
    movements = [distance(p1, p2) for p1, p2 in zip(recent_positions[:-1], recent_positions[1:])]
    total_movement = sum(movements)
    net_movement = distance(recent_positions[0], recent_positions[-1])
    
    # High total movement but low net = jiggle
    return total_movement > JIGGLE_THRESHOLD and net_movement < JIGGLE_NET_THRESHOLD
```

### 3. With Pause Detection

Pause dwell during certain conditions:

```python
if is_paused():
    # Don't process dwell
    return

if check_jiggle_trigger():
    pause_system()
    return
```

### 4. Progress Visualization

Different ways to show progress:

**Progress Ring:**
```python
# Circular progress indicator
stroke_dashoffset = CIRCUMFERENCE - (progress * CIRCUMFERENCE)
progress_ring.set_dashoffset(stroke_dashoffset)
```

**Opacity:**
```python
# Fade in as progress increases
opacity = 0.3 + (progress * 0.7)
overlay.set_opacity(opacity)
```

**Color Gradient:**
```python
# Change color as progress increases
if progress < 0.5:
    color = interpolate(RED, YELLOW, progress * 2)
else:
    color = interpolate(YELLOW, GREEN, (progress - 0.5) * 2)
```

## Timing Considerations

### Dwell Time

Typical values:
- **Fast**: 0.5 - 0.8 seconds
- **Medium**: 1.0 - 1.5 seconds
- **Slow**: 2.0 - 3.0 seconds

### Update Frequency

How often to check position:
- **High frequency**: 10ms (smooth but CPU intensive)
- **Medium frequency**: 20ms (good balance)
- **Low frequency**: 50ms (less responsive)

### Click Delay

Delay between mouseDown and mouseUp:
- **Immediate**: 0ms (may not register on some systems)
- **Recommended**: 10-20ms
- **Safe**: 50ms (ensures registration)

## State Management

Track dwell state to prevent issues:

```python
class DwellState:
    def __init__(self):
        self.dwell_active = False
        self.dwell_start_time = None
        self.dwell_position = None
        self.last_click_position = None
        self.progress = 0.0
    
    def start_dwell(self, position):
        self.dwell_active = True
        self.dwell_start_time = time.time()
        self.dwell_position = position
        self.progress = 0.0
    
    def cancel_dwell(self):
        self.dwell_active = False
        self.dwell_start_time = None
        self.dwell_position = None
        self.progress = 0.0
    
    def complete_dwell(self):
        self.last_click_position = self.dwell_position
        self.cancel_dwell()
```

## Related Patterns

- See `dwell-drag.md` for drag pattern
- See `dwell-countdown.md` for countdown system
- See `mouse-hover-detection.md` for position tracking
