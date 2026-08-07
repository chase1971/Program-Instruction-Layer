# Dwell Drag Pattern

> **You might say:** "drag by dwelling", "dwell mode 2", "the drag state machine", "it will not let go"
> **What it is:** Drag via hover: countdown to grab, drag, countdown to release. Full state machine.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/modules/dwell/backend/dwell_mode2.py — `Mode2State` transitions`
- `electron-toolbar/modules/dwell/backend/dwell_globals.py — `mode2_state``
- `electron-toolbar/modules/dwell/backend/dwell_constants.py`

---

## Overview

A state machine-based pattern for triggering drag operations through hover interactions. Uses countdown timers and state transitions to provide controlled drag start and release.

## Pattern Description

The dwell drag pattern uses a state machine with multiple states:
1. **IDLE**: Waiting for cursor to become stationary
2. **COUNTDOWN**: Showing "2, 1" countdown before drag
3. **DRAGGING**: Mouse is held down, dragging
4. **COOLDOWN**: Post-drag cooldown period
5. **WAITING_FOR_MODE_SWITCH**: Transition state

## State Machine

### State Transitions

```
IDLE
  └─> (cursor stationary + debounce) ─> COUNTDOWN
         └─> (mouse moved) ─> IDLE (reset)

COUNTDOWN
  └─> (countdown complete) ─> DRAGGING
  └─> (mouse moved) ─> IDLE (cancel)

DRAGGING
  └─> (mouse stopped + time elapsed) ─> COUNTDOWN (release)
  └─> (release countdown complete) ─> COOLDOWN
  └─> (jiggle detected) ─> WAITING_FOR_MODE_SWITCH

COOLDOWN
  └─> (time + movement met) ─> IDLE

WAITING_FOR_MODE_SWITCH
  └─> (mouse stationary) ─> IDLE (mode switch)
```

### State Definitions

#### IDLE State

Waiting for cursor to become stationary:

```python
def handle_idle(current_position, current_time):
    # Check if mouse moved
    if last_idle_position is None or current_position != last_idle_position:
        last_idle_position = current_position
        countdown_debounce_start = None
        return
    
    # Mouse stationary - check debounce
    if countdown_debounce_start is None:
        countdown_debounce_start = current_time
    elif current_time - countdown_debounce_start >= COUNTDOWN_DEBOUNCE_TIME:
        # Start countdown
        state = "COUNTDOWN"
        start_countdown()
```

#### COUNTDOWN State

Showing countdown before drag:

```python
def handle_countdown(current_position):
    # Check if mouse moved (cancels countdown)
    if current_position != countdown_start_position:
        cancel_countdown()
        state = "IDLE"
        return
    
    # Show countdown steps
    if step == 2:
        show_countdown("2")
        schedule_next_step(step=1, delay=200ms)
    elif step == 1:
        show_countdown("1")
        schedule_next_step(step="drag", delay=200ms)
    elif step == "drag":
        show_text("Drag")
        start_dragging()
        state = "DRAGGING"
```

#### DRAGGING State

Mouse is held down:

```python
def handle_dragging(current_position, current_time):
    # Track movement
    if current_position != drag_start_position:
        has_moved_since_drag_start = True
    
    # Monitor for stop
    if current_position == last_position:
        # Mouse stopped
        stop_duration = current_time - stop_start_time
        
        if stop_duration >= DRAG_STOP_CONFIRM_TIME:
            # Start release countdown
            if not release_countdown_active:
                start_release_countdown()
    else:
        # Mouse moved - cancel release countdown
        cancel_release_countdown()
        stop_start_time = current_time
        last_position = current_position
    
    # Check release countdown
    if release_countdown_complete:
        release_mouse()
        state = "COOLDOWN"
```

#### COOLDOWN State

Post-drag cooldown:

```python
def handle_cooldown(current_position, current_time):
    # Check time requirement
    time_met = current_time >= cooldown_end_time
    
    # Check movement requirement
    if drag_end_position:
        movement = distance(current_position, drag_end_position)
        movement_met = movement >= MOVEMENT_THRESHOLD
    
    # Check if mouse stopped
    if current_position == last_idle_position:
        # Both requirements met and mouse stopped
        if time_met and movement_met:
            state = "IDLE"
    else:
        last_idle_position = current_position
```

## Implementation Template

```python
class DwellDragHandler:
    def __init__(self):
        self.state = "IDLE"
        self.countdown_start_position = None
        self.drag_start_position = None
        self.drag_end_position = None
        self.last_idle_position = None
        self.cooldown_end_time = None
        self.has_moved_since_drag_start = False
    
    def process(self, current_position, current_time):
        """Main state machine processor"""
        if self.state == "IDLE":
            self._handle_idle(current_position, current_time)
        elif self.state == "COUNTDOWN":
            self._handle_countdown(current_position)
        elif self.state == "DRAGGING":
            self._handle_dragging(current_position, current_time)
        elif self.state == "COOLDOWN":
            self._handle_cooldown(current_position, current_time)
    
    def _handle_idle(self, position, time):
        """IDLE: Wait for cursor to stop"""
        if self.last_idle_position is None or position != self.last_idle_position:
            self.last_idle_position = position
            self.countdown_debounce_start = None
        else:
            if self.countdown_debounce_start is None:
                self.countdown_debounce_start = time
            elif time - self.countdown_debounce_start >= COUNTDOWN_DEBOUNCE_TIME:
                self.state = "COUNTDOWN"
                self.countdown_start_position = position
                self.start_countdown()
    
    def _handle_countdown(self, position):
        """COUNTDOWN: Show countdown before drag"""
        if position != self.countdown_start_position:
            self.cancel_countdown()
            self.state = "IDLE"
            return
        
        # Countdown logic (handled by countdown manager)
        # When complete, transitions to DRAGGING
    
    def _handle_dragging(self, position, time):
        """DRAGGING: Monitor for release"""
        # Track movement
        if not self.has_moved_since_drag_start:
            if position != self.drag_start_position:
                self.has_moved_since_drag_start = True
        
        # Monitor stop
        if position == self.last_drag_position:
            stop_duration = time - self.stop_start_time
            if stop_duration >= DRAG_STOP_CONFIRM_TIME:
                if not self.release_countdown_active:
                    self.start_release_countdown()
        else:
            self.cancel_release_countdown()
            self.stop_start_time = time
            self.last_drag_position = position
        
        # Check release
        if self.release_countdown_complete:
            pyautogui.mouseUp()
            self.state = "COOLDOWN"
            self.drag_end_position = position
            self.cooldown_end_time = time + COOLDOWN_DURATION
    
    def _handle_cooldown(self, position, time):
        """COOLDOWN: Post-drag waiting period"""
        time_met = time >= self.cooldown_end_time
        movement_met = False
        
        if self.drag_end_position:
            movement = distance(position, self.drag_end_position)
            movement_met = movement >= MOVEMENT_THRESHOLD
        
        if position == self.last_idle_position:
            if time_met and movement_met:
                self.state = "IDLE"
        else:
            self.last_idle_position = position
```

## Countdown System

### Drag Start Countdown

Shows "2", "1", then "Drag":

```python
def start_drag_countdown():
    countdown_start_position = pyautogui.position()
    
    # Step 1: Show "2"
    show_countdown("2")
    after(200ms, lambda: show_countdown("1"))
    
    # Step 2: Show "1"
    after(200ms, lambda: start_drag())
    
    # Step 3: Show "Drag" and press mouse
    show_text("Drag")
    pyautogui.mouseDown()
```

### Release Countdown

Shows "2", "1", then "Release" when mouse stops:

```python
def start_release_countdown():
    # Calculate step timing based on release time
    step_time = max(DRAG_RELEASE_TIME / 4.0, 0.15)
    
    # Step 1: Show "2"
    show_countdown("2")
    after(step_time, lambda: show_countdown("1"))
    
    # Step 2: Show "1"
    after(step_time, lambda: release_mouse())
    
    # Step 3: Show "Release" and release mouse
    show_text("Release")
    pyautogui.mouseUp()
```

## Key Features

### 1. Debounce Before Countdown

Prevents accidental activation from brief stops:

```python
COUNTDOWN_DEBOUNCE_TIME = ...  # see electron-toolbar/modules/dwell/backend/dwell_constants.py

# Mouse must be stationary for this long before countdown starts
if time_stationary >= COUNTDOWN_DEBOUNCE_TIME:
    start_countdown()
```

### 2. Movement Requirement for Release

Requires mouse to have moved before allowing release:

```python
if not has_moved_since_drag_start:
    # Don't allow release countdown
    return

# Only start release countdown if mouse has moved
if has_moved_since_drag_start and mouse_stopped:
    start_release_countdown()
```

### 3. Grace Period

Prevents immediate release after drag start:

```python
DRAG_RELEASE_GRACE_TIME = ...  # see electron-toolbar/modules/dwell/backend/dwell_constants.py

drag_release_grace_end = time.time() + DRAG_RELEASE_GRACE_TIME

# Don't allow release countdown during grace period
if time.time() < drag_release_grace_end:
    return  # Still in grace period
```

### 4. Cooldown Requirements

Both time and movement must be met:

```python
# Time requirement
time_met = current_time >= cooldown_end_time

# Movement requirement
movement = distance(current_position, drag_end_position)
movement_met = movement >= MOVEMENT_THRESHOLD

# Both must be true
if time_met and movement_met and mouse_stopped:
    exit_cooldown()
```

## Visual Feedback

### Countdown Display

```python
def show_countdown(number: str):
    """Show countdown number in red"""
    indicator.config(text=number, bg="red", fg="white")
    indicator.position_near_cursor()

def show_drag_text():
    """Show 'Drag' in green"""
    indicator.config(text="Drag", bg="green", fg="white")

def show_release_text():
    """Show 'Release' in green"""
    indicator.config(text="Release", bg="green", fg="white")
```

## Constants

```python
COUNTDOWN_DEBOUNCE_TIME = ...      # Wait before starting countdown
COUNTDOWN_STEP_1_MS = ...          # Time for "2"
COUNTDOWN_STEP_2_MS = ...          # Time for "1"
DRAG_RELEASE_TIME = ...            # Time to hold before release countdown
DRAG_STOP_CONFIRM_TIME = ...       # Time stopped before release countdown
DRAG_RELEASE_GRACE_TIME = ...      # Grace period after drag start
MODE2_COOLDOWN_DURATION = ...      # Cooldown after release
MOVEMENT_THRESHOLD = ...           # Pixels moved to exit cooldown
```

## Related Patterns

- See `dwell-click.md` for click pattern
- See `dwell-countdown.md` for countdown system details
- See `state-machine.md` for general state machine pattern
