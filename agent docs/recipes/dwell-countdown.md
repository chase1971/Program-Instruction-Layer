# Dwell Countdown System

> **You might say:** "count down before it does the thing", "give me a warning before it fires"
> **What it is:** A reusable countdown display before a timed action, cancellable by movement.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/modules/dwell/backend/dwell_mode2.py`
- `electron-toolbar/modules/dwell/backend/dwell_globals.py`
- `electron-toolbar/modules/dwell/backend/dwell_constants.py`

---

## Overview

A reusable countdown display system that shows visual feedback during timed operations. Used for drag start and drag release countdowns in the dwell module.

## Pattern Description

The countdown system displays a sequence of numbers (typically "2", "1") followed by an action text, providing clear visual feedback before executing an action.

## Implementation Structure

### Countdown Manager

```python
class CountdownManager:
    def __init__(self, display_callback, cancel_callback):
        self.display = display_callback
        self.cancel = cancel_callback
        self.active = False
        self.cancel_id = None
        self.start_position = None
    
    def start_countdown(self, steps, step_delays, final_action):
        """Start a countdown sequence"""
        if self.active:
            return
        
        self.active = True
        self.start_position = pyautogui.position()
        self._show_step(0, steps, step_delays, final_action)
    
    def _show_step(self, step_index, steps, delays, final_action):
        """Show a countdown step"""
        if not self.active:
            return
        
        # Check if position changed (cancel condition)
        if pyautogui.position() != self.start_position:
            self.cancel()
            return
        
        if step_index < len(steps):
            # Show step
            self.display(steps[step_index])
            
            # Schedule next step
            self.cancel_id = after(delays[step_index], 
                lambda: self._show_step(step_index + 1, steps, delays, final_action))
        else:
            # All steps complete - execute action
            final_action()
            self.active = False
    
    def cancel(self):
        """Cancel active countdown"""
        if self.cancel_id:
            after_cancel(self.cancel_id)
            self.cancel_id = None
        self.active = False
        self.start_position = None
```

## Countdown Types

### 1. Drag Start Countdown

Sequence: "2" → "1" → "Drag" (then press mouse)

```python
def show_drag_start_countdown():
    steps = ["2", "1", "Drag"]
    delays = [200, 200, 0]  # milliseconds
    
    def final_action():
        pyautogui.mouseDown()
        state = "DRAGGING"
    
    countdown_manager.start_countdown(steps, delays, final_action)
```

### 2. Drag Release Countdown

Sequence: "2" → "1" → "Release" (then release mouse)

```python
def show_release_countdown():
    # Calculate step timing based on release time
    release_time = DRAG_RELEASE_TIME
    step_time = max(release_time / 4.0, 0.15)  # Minimum 0.15s per step
    
    steps = ["2", "1", "Release"]
    delays = [step_time * 1000, step_time * 1000, 0]  # Convert to ms
    
    def final_action():
        pyautogui.mouseUp()
        state = "COOLDOWN"
    
    countdown_manager.start_countdown(steps, delays, final_action)
```

## Visual Display

### Positioning

Position indicator near cursor:

```python
def position_indicator(x, y):
    """Position countdown indicator near cursor"""
    indicator.geometry(f"+{x+10}+{y-20}")  # Offset from cursor
    indicator.deiconify()
    indicator.attributes("-topmost", True)
```

### Styling

Different styles for different steps:

```python
def show_countdown_number(number: str):
    """Show countdown number in red"""
    indicator.config(
        text=number,
        bg="red",
        fg="white",
        font=("Arial", 24, "bold")
    )

def show_action_text(text: str):
    """Show action text in green"""
    indicator.config(
        text=text,
        bg="green",
        fg="white",
        font=("Arial", 18, "bold")
    )
```

## Cancellation Conditions

### Movement Cancellation

Cancel if cursor moves during countdown:

```python
def check_movement():
    """Check if cursor moved from start position"""
    current = pyautogui.position()
    if current != countdown_start_position:
        cancel_countdown()
        return True
    return False
```

### State Cancellation

Cancel if system state changes:

```python
def should_continue_countdown():
    """Check if countdown should continue"""
    return (
        system_running and
        not system_paused and
        mode == expected_mode and
        state == expected_state
    )
```

## Timing Calculations

### Fixed Timing

For consistent countdowns:

```python
COUNTDOWN_STEP_1_MS = ...  # see electron-toolbar/modules/dwell/backend/dwell_constants.py
COUNTDOWN_STEP_2_MS = ...  # see electron-toolbar/modules/dwell/backend/dwell_constants.py
TOTAL_COUNTDOWN = sum of the two steps above
```

### Dynamic Timing

For variable countdowns based on settings:

```python
def calculate_step_time(total_time, num_steps, min_step_time=0.15):
    """Calculate time per step"""
    step_time = total_time / num_steps
    return max(step_time, min_step_time)  # Enforce minimum
```

## Complete Template

```python
class CountdownSystem:
    def __init__(self):
        self.active = False
        self.start_position = None
        self.cancel_timer = None
        self.display_window = None
    
    def start(self, sequence, delays, on_complete, cancel_on_move=True):
        """Start countdown sequence"""
        if self.active:
            self.cancel()
        
        self.active = True
        self.start_position = pyautogui.position()
        self._execute_sequence(sequence, delays, on_complete, cancel_on_move, 0)
    
    def _execute_sequence(self, sequence, delays, on_complete, cancel_on_move, index):
        """Execute countdown sequence step by step"""
        if not self.active:
            return
        
        # Check cancellation conditions
        if cancel_on_move and pyautogui.position() != self.start_position:
            self.cancel()
            return
        
        if not self._should_continue():
            self.cancel()
            return
        
        if index < len(sequence):
            # Show current step
            self._display(sequence[index])
            
            # Schedule next step
            delay = delays[index] if index < len(delays) else 0
            self.cancel_timer = after(delay, 
                lambda: self._execute_sequence(sequence, delays, on_complete, cancel_on_move, index + 1))
        else:
            # Sequence complete
            on_complete()
            self.active = False
    
    def _display(self, text):
        """Display countdown text"""
        x, y = pyautogui.position()
        self.display_window.position(x + 10, y - 20)
        self.display_window.show(text)
    
    def _should_continue(self):
        """Check if countdown should continue"""
        # Implement state checks
        return True
    
    def cancel(self):
        """Cancel active countdown"""
        if self.cancel_timer:
            after_cancel(self.cancel_timer)
            self.cancel_timer = None
        self.active = False
        self.start_position = None
        if self.display_window:
            self.display_window.hide()
```

## Use Cases

### 1. Action Confirmation

Show countdown before executing important action:

```python
countdown.start(
    sequence=["3", "2", "1", "Execute"],
    delays=[1000, 1000, 1000, 0],
    on_complete=lambda: execute_important_action()
)
```

### 2. Safety Delays

Add delay before potentially destructive actions:

```python
countdown.start(
    sequence=["Warning", "2", "1", "Delete"],
    delays=[500, 1000, 1000, 0],
    on_complete=lambda: delete_file()
)
```

### 3. Mode Transitions

Countdown before switching modes:

```python
countdown.start(
    sequence=["2", "1", "Drag Mode"],
    delays=[200, 200, 0],
    on_complete=lambda: enter_drag_mode()
)
```

## Related Patterns

- See `dwell-drag.md` for drag state machine
- See `dwell-click.md` for click pattern
- See `state-machine.md` for state management
