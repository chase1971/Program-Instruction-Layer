# Anti-Patterns to Avoid

> Common mistakes to avoid. If you see yourself doing any of these, stop and reconsider.

---

## State Management Anti-Patterns

### ❌ Scattered Global State
```python
# BAD - globals scattered throughout file
global mode
global paused
global last_position

def some_function():
    global mode
    mode = 2
```

**Why it's bad**: Hard to track state changes, race conditions, difficult to test.

**Do this instead**:
```python
# GOOD - consolidated state class
class ModuleState:
    def __init__(self):
        self._lock = threading.Lock()
        self._mode = 1
        self._paused = False
    
    @property
    def mode(self):
        with self._lock:
            return self._mode

state = ModuleState()
```

---

### ❌ File-Based IPC (Inter-Process Communication)
```python
# BAD - using files to communicate between processes
if os.path.exists("show_scroll.txt"):
    os.remove("show_scroll.txt")
    show_scroll()
```

**Why it's bad**: Race conditions, polling waste, no guaranteed delivery, hard to debug.

**Do this instead**:
```python
# GOOD - socket-based signals
from shared.signals import signals

signals.listen("show_scroll", on_show_scroll)
signals.broadcast("show_scroll")
```

---

## Error Handling Anti-Patterns

### ❌ Bare Except Clauses
```python
# BAD - catches everything including KeyboardInterrupt
try:
    risky_operation()
except:
    pass
```

**Why it's bad**: Hides real errors, catches system exits, makes debugging impossible.

**Do this instead**:
```python
# GOOD - specific exception handling
try:
    risky_operation()
except SpecificError as e:
    print(f"[MODULE] Operation failed: {e}")
    return default_value
except Exception as e:
    print(f"[MODULE] Unexpected error: {e}")
    raise  # Re-raise unexpected errors
```

---

### ❌ Silent Failures
```python
# BAD - error happens, nobody knows
try:
    result = parse_config()
except Exception:
    result = {}  # Silently use empty config
```

**Why it's bad**: Bugs go unnoticed, behavior is unpredictable.

**Do this instead**:
```python
# GOOD - log the error, then handle gracefully
try:
    result = parse_config()
except Exception as e:
    print(f"[CONFIG] Failed to parse config: {e}, using defaults")
    result = get_default_config()
```

---

## Code Organization Anti-Patterns

### ❌ God Files (1000+ lines)
```
module.py (2500 lines) - does everything
```

**Why it's bad**: Hard to navigate, hard to test, merge conflicts, cognitive overload.

**Do this instead**:
```
module/
├── module.py           # Main logic (300 lines)
├── module_constants.py # All constants
├── module_state.py     # State management
├── module_helpers.py   # Utility functions
└── module_ui.py        # UI-specific code
```

---

### ❌ Magic Numbers
```python
# BAD - what do these numbers mean?
if len(items) > 47:
    time.sleep(0.5)
    x = screen_width - 150 - 35
```

**Why it's bad**: Unmaintainable, hard to understand, easy to break.

**Do this instead**:
```python
# GOOD - named constants with meaning
MAX_ITEMS_PER_BATCH = 47
RATE_LIMIT_DELAY = 0.5
WINDOW_WIDTH = 150
SOUND_MODULE_OFFSET = 35

if len(items) > MAX_ITEMS_PER_BATCH:
    time.sleep(RATE_LIMIT_DELAY)
    x = screen_width - WINDOW_WIDTH - SOUND_MODULE_OFFSET
```

---

### ❌ Inconsistent Module Structure
```
# BAD - every module organized differently
dwell/
├── main.pyw
├── helpers.py
scroll/
├── scroll_module.pyw
├── utils/
arrow/
├── ArrowModule.py
├── arrow-helpers.js
```

**Why it's bad**: Cognitive overhead switching between modules, no predictable structure.

**Do this instead**:
```
# GOOD - consistent structure everywhere
module_name/
├── module_name.py        # Main logic
├── module_constants.py   # Constants
├── module_state.py       # State class (if needed)
└── module_helpers.py     # Helpers (if needed)
```

---

## Threading Anti-Patterns

### ❌ Unprotected Shared State
```python
# BAD - race condition waiting to happen
class State:
    def __init__(self):
        self.mode = 1
        self.paused = False

# Thread 1: state.mode = 2
# Thread 2: if state.mode == 1:  # Race!
```

**Why it's bad**: Unpredictable behavior, hard-to-reproduce bugs.

**Do this instead**:
```python
# GOOD - protected with locks
class State:
    def __init__(self):
        self._lock = threading.Lock()
        self._mode = 1
    
    @property
    def mode(self):
        with self._lock:
            return self._mode
    
    @mode.setter
    def mode(self, value):
        with self._lock:
            self._mode = value
```

---

### ❌ GUI Operations from Background Threads
```python
# BAD - Tkinter operations from non-main thread
def background_task():
    # This will crash or behave unpredictably
    label.config(text="Updated")
    window.withdraw()
```

**Why it's bad**: Tkinter is not thread-safe, causes crashes or visual glitches.

**Do this instead**:
```python
# GOOD - schedule on main thread
def background_task():
    # Schedule GUI operation on main thread
    master.after(0, lambda: label.config(text="Updated"))
    master.after(0, window.withdraw)
```

---

## Communication Anti-Patterns

### ❌ Hardcoded Paths
```python
# BAD - breaks on different machines
config_path = "C:\\Users\\chase\\Documents\\config.json"
```

**Why it's bad**: Won't work on other machines, won't survive folder moves.

**Do this instead**:
```python
# GOOD - relative to script location
from pathlib import Path
config_path = Path(__file__).parent / "config.json"
```

---

### ❌ Polling Too Frequently
```python
# BAD - burns CPU for no reason
while True:
    check_something()
    time.sleep(0.001)  # 1000 checks per second!
```

**Why it's bad**: Wastes CPU, drains battery, no benefit.

**Do this instead**:
```python
# GOOD - reasonable polling interval
POLL_INTERVAL = 0.01  # 100 checks per second (usually enough)

while True:
    check_something()
    time.sleep(POLL_INTERVAL)
```

---

## Summary Table

| Anti-Pattern | Problem | Solution |
|-------------|---------|----------|
| Scattered globals | Race conditions, untestable | Use state class |
| File-based IPC | Race conditions, wasteful | Use socket signals |
| Bare except | Hides errors | Catch specific exceptions |
| Silent failures | Bugs go unnoticed | Log then handle |
| God files | Unmaintainable | Split into modules |
| Magic numbers | Unclear, fragile | Named constants |
| Inconsistent structure | Cognitive overhead | Follow module template |
| Unprotected state | Race conditions | Use locks |
| GUI from threads | Crashes | Schedule with `after()` |
| Hardcoded paths | Not portable | Use relative paths |
| Polling too fast | Wastes CPU | Reasonable intervals |
