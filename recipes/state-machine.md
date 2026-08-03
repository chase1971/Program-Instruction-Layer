# State Machine Pattern

> **You might say:** "manage the states", "it gets stuck between modes", "it never leaves dragging"
> **What it is:** Discrete states with explicit transitions, so an interaction can always be reasoned about and reset.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/modules/dwell/backend/dwell_mode2.py` — Mode2State.IDLE / COUNTDOWN / DRAGGING / WAITING_FOR_MODE_SWITCH
- `electron-toolbar/modules/dwell/backend/dwell_globals.py — `mode2_state` lives here`

---

## Overview

A pattern for managing complex behavior through discrete states and transitions. Used extensively in the dwell module for drag operations.

## Pattern Description

A state machine organizes behavior into:
- **States**: Distinct modes of operation
- **Transitions**: Conditions that move between states
- **Actions**: Behavior executed in each state
- **Guards**: Conditions that must be met for transitions

## Basic Structure

```python
class StateMachine:
    def __init__(self):
        self.state = "INITIAL"
        self.state_handlers = {
            "INITIAL": self._handle_initial,
            "ACTIVE": self._handle_active,
            "PAUSED": self._handle_paused
        }
    
    def process(self, input_data):
        """Process input in current state"""
        handler = self.state_handlers.get(self.state)
        if handler:
            handler(input_data)
    
    def transition(self, new_state):
        """Transition to new state"""
        # Exit current state
        self._exit_state(self.state)
        
        # Enter new state
        self.state = new_state
        self._enter_state(new_state)
    
    def _enter_state(self, state):
        """Called when entering a state"""
        pass
    
    def _exit_state(self, state):
        """Called when exiting a state"""
        pass
```

## Dwell Drag State Machine

### States

1. **IDLE**: Waiting for activation
2. **COUNTDOWN**: Showing countdown before action
3. **DRAGGING**: Active drag operation
4. **COOLDOWN**: Post-action waiting period
5. **WAITING_FOR_MODE_SWITCH**: Transition state

### State Handler Pattern

```python
def process_state_machine(current_position, current_time):
    """Main state machine processor"""
    if state == "IDLE":
        handle_idle(current_position, current_time)
    elif state == "COUNTDOWN":
        handle_countdown(current_position)
    elif state == "DRAGGING":
        handle_dragging(current_position, current_time)
    elif state == "COOLDOWN":
        handle_cooldown(current_position, current_time)
    elif state == "WAITING_FOR_MODE_SWITCH":
        handle_waiting(current_position, current_time)
```

### Transition Conditions

```python
# IDLE -> COUNTDOWN
if mouse_stationary and debounce_time_met:
    transition("COUNTDOWN")

# COUNTDOWN -> DRAGGING
if countdown_complete and mouse_not_moved:
    transition("DRAGGING")

# DRAGGING -> COOLDOWN
if mouse_stopped and release_countdown_complete:
    transition("COOLDOWN")

# COOLDOWN -> IDLE
if cooldown_time_met and movement_met and mouse_stopped:
    transition("IDLE")
```

## State Data

Each state may have associated data:

```python
class StateData:
    def __init__(self):
        # IDLE state data
        self.last_idle_position = None
        self.countdown_debounce_start = None
        
        # COUNTDOWN state data
        self.countdown_start_position = None
        self.countdown_step = 0
        
        # DRAGGING state data
        self.drag_start_position = None
        self.has_moved_since_drag_start = False
        self.stop_start_time = None
        self.last_drag_position = None
        
        # COOLDOWN state data
        self.drag_end_position = None
        self.cooldown_end_time = None
        
        # WAITING state data
        self.grace_period_active = False
        self.grace_stationary_start = None
```

## State Entry/Exit

### Entry Actions

Actions performed when entering a state:

```python
def enter_idle():
    """Enter IDLE state"""
    reset_countdown_debounce()
    clear_drag_data()

def enter_countdown():
    """Enter COUNTDOWN state"""
    countdown_start_position = pyautogui.position()
    start_countdown_display()

def enter_dragging():
    """Enter DRAGGING state"""
    drag_start_position = pyautogui.position()
    pyautogui.mouseDown()
    show_drag_indicator()
```

### Exit Actions

Actions performed when leaving a state:

```python
def exit_countdown():
    """Exit COUNTDOWN state"""
    cancel_countdown_display()
    clear_countdown_data()

def exit_dragging():
    """Exit DRAGGING state"""
    pyautogui.mouseUp()
    hide_drag_indicator()
    record_drag_end_position()
```

## Guard Conditions

Conditions that must be met for transitions:

```python
def can_transition_to_countdown():
    """Check if can transition to COUNTDOWN"""
    return (
        state == "IDLE" and
        mouse_stationary and
        debounce_time_met and
        not paused and
        not lock_paused
    )

def can_transition_to_dragging():
    """Check if can transition to DRAGGING"""
    return (
        state == "COUNTDOWN" and
        countdown_complete and
        mouse_not_moved and
        not paused
    )
```

## State Validation

Validate state transitions:

```python
def transition(new_state):
    """Transition with validation"""
    valid_transitions = {
        "IDLE": ["COUNTDOWN"],
        "COUNTDOWN": ["IDLE", "DRAGGING"],
        "DRAGGING": ["COOLDOWN", "WAITING_FOR_MODE_SWITCH"],
        "COOLDOWN": ["IDLE"],
        "WAITING_FOR_MODE_SWITCH": ["IDLE"]
    }
    
    if new_state not in valid_transitions.get(self.state, []):
        print(f"Invalid transition: {self.state} -> {new_state}")
        return False
    
    self._exit_state(self.state)
    self.state = new_state
    self._enter_state(new_state)
    return True
```

## Complete Template

```python
class StateMachine:
    def __init__(self):
        self.state = "INITIAL"
        self.state_data = {}
        self.handlers = {
            "INITIAL": self._handle_initial,
            "ACTIVE": self._handle_active,
            "PAUSED": self._handle_paused
        }
        self.valid_transitions = {
            "INITIAL": ["ACTIVE"],
            "ACTIVE": ["PAUSED", "INITIAL"],
            "PAUSED": ["ACTIVE", "INITIAL"]
        }
    
    def process(self, input_data):
        """Process input in current state"""
        handler = self.handlers.get(self.state)
        if handler:
            handler(input_data)
    
    def transition(self, new_state, data=None):
        """Transition to new state with validation"""
        if new_state not in self.valid_transitions.get(self.state, []):
            print(f"Invalid transition: {self.state} -> {new_state}")
            return False
        
        # Exit current state
        self._exit_state(self.state)
        
        # Transition
        old_state = self.state
        self.state = new_state
        
        # Store state data
        if data:
            self.state_data[new_state] = data
        
        # Enter new state
        self._enter_state(new_state, old_state)
        return True
    
    def _enter_state(self, state, previous_state):
        """Called when entering a state"""
        print(f"Entering state: {state} (from {previous_state})")
        # Implement state entry logic
    
    def _exit_state(self, state):
        """Called when exiting a state"""
        print(f"Exiting state: {state}")
        # Implement state exit logic
    
    def _handle_initial(self, data):
        """Handle INITIAL state"""
        # Check transition conditions
        if should_activate(data):
            self.transition("ACTIVE")
    
    def _handle_active(self, data):
        """Handle ACTIVE state"""
        # Process active state logic
        if should_pause(data):
            self.transition("PAUSED")
    
    def _handle_paused(self, data):
        """Handle PAUSED state"""
        # Process paused state logic
        if should_resume(data):
            self.transition("ACTIVE")
```

## Benefits

1. **Clear Logic Flow**: Easy to understand state transitions
2. **Maintainable**: Each state is isolated
3. **Debuggable**: Can log state transitions
4. **Testable**: Each state can be tested independently
5. **Extensible**: Easy to add new states

## Related Patterns

- See `dwell-drag.md` for complete drag state machine
- See `dwell-click.md` for click pattern
- See `dwell-countdown.md` for countdown system
