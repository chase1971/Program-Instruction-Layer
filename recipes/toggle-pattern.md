# Toggle Pattern

## Overview

A pattern for reliably toggling overlay windows on and off, with proper state tracking, cooldown management, and race condition prevention. Used across all overlay modules (toolbar, arrow, scroll).

## Pattern Description

The toggle pattern ensures:
1. Explicit visibility state tracking (not relying on `isVisible()`)
2. Cooldown to prevent rapid toggling
3. State set BEFORE show/hide operations (prevents race conditions)
4. Event listeners to keep state in sync
5. Proper cleanup when hiding

## Problem: Why This Pattern Exists

### Issues with Simple Toggle

**Problem 1: Unreliable `isVisible()`**
```javascript
// BAD - isVisible() can be unreliable for click-through windows
if (window.isVisible()) {
    window.hide();
} else {
    window.show();
}
```

**Problem 2: Race Conditions**
```javascript
// BAD - State set after operation can cause issues
window.hide();
visible = false;  // Too late - another toggle might have fired
```

**Problem 3: Rapid Toggling**
```javascript
// BAD - No cooldown allows accidental double-toggles
// User presses hotkey twice quickly → window shows then immediately hides
```

**Problem 4: Auto-Re-showing**
```javascript
// BAD - setInterval or event handlers can re-show hidden windows
setInterval(() => {
    window.setAlwaysOnTop(true);  // Might trigger show event
}, 2000);
```

## Implementation Structure

### Basic Toggle with State Tracking

```javascript
// State tracking
let overlayVisible = false;
let overlayWindow = null;

// Cooldown management
const COOLDOWNS = {
    OVERLAY_TOGGLE: 300  // ms
};
let lastToggleTime = 0;

function toggleOverlay() {
    // Check cooldown
    const now = Date.now();
    if (now - lastToggleTime < COOLDOWNS.OVERLAY_TOGGLE) {
        const remaining = COOLDOWNS.OVERLAY_TOGGLE - (now - lastToggleTime);
        console.log(`Toggle ignored (cooldown: ${remaining}ms remaining)`);
        return;
    }
    lastToggleTime = now;
    
    console.log('Toggle called, current state:', overlayVisible);
    
    // If visible, hide it
    if (overlayWindow && overlayVisible) {
        overlayVisible = false;  // Set state BEFORE hiding
        overlayWindow.hide();
        console.log('Overlay hidden');
    } else if (overlayWindow) {
        // Window exists but hidden, show it
        overlayVisible = true;  // Set state BEFORE showing
        overlayWindow.show();
        console.log('Overlay shown');
    } else {
        // Window doesn't exist, create it
        overlayWindow = createOverlay();
        overlayVisible = true;
        console.log('Overlay created and shown');
    }
}
```

### Event Listeners for State Sync

```javascript
function createOverlay() {
    const win = new BrowserWindow({ /* ... */ });
    
    // Track visibility changes
    win.on('show', () => {
        overlayVisible = true;
        console.log('Window shown (event)');
    });
    
    win.on('hide', () => {
        overlayVisible = false;
        console.log('Window hidden (event)');
    });
    
    win.on('closed', () => {
        overlayWindow = null;
        overlayVisible = false;
    });
    
    return win;
}
```

## Complete Template

### JavaScript/Electron

```javascript
class ToggleableOverlay {
    constructor() {
        this.window = null;
        this.visible = false;
        this.lastToggleTime = 0;
        this.COOLDOWN_MS = 300;
    }
    
    toggle() {
        // Check cooldown
        const now = Date.now();
        if (now - this.lastToggleTime < this.COOLDOWN_MS) {
            const remaining = this.COOLDOWN_MS - (now - this.lastToggleTime);
            console.log(`Toggle ignored (cooldown: ${remaining}ms remaining)`);
            return;
        }
        this.lastToggleTime = now;
        
        console.log('Toggle called, current state:', this.visible);
        
        // If visible, hide it
        if (this.window && this.visible) {
            this.visible = false;  // Set state BEFORE hiding
            this.window.hide();
            console.log('Overlay hidden');
        } else if (this.window) {
            // Window exists but hidden, show it
            this.visible = true;  // Set state BEFORE showing
            this.window.show();
            console.log('Overlay shown');
        } else {
            // Window doesn't exist, create it
            this.window = this.createWindow();
            this.visible = true;
            console.log('Overlay created and shown');
        }
    }
    
    createWindow() {
        const win = new BrowserWindow({ /* ... */ });
        
        // Track visibility changes
        win.on('show', () => {
            this.visible = true;
            console.log('Window shown (event)');
        });
        
        win.on('hide', () => {
            this.visible = false;
            console.log('Window hidden (event)');
        });
        
        win.on('closed', () => {
            this.window = null;
            this.visible = false;
        });
        
        return win;
    }
}
```

### Python/Tkinter

```python
import time
from typing import Optional

class ToggleableOverlay:
    def __init__(self):
        self.window: Optional[tk.Toplevel] = None
        self.visible: bool = False
        self.last_toggle_time: float = 0.0
        self.COOLDOWN_MS: int = 300
    
    def toggle(self) -> None:
        # Check cooldown
        now_ms = time.time() * 1000
        if now_ms - self.last_toggle_time < self.COOLDOWN_MS:
            remaining = int(self.COOLDOWN_MS - (now_ms - self.last_toggle_time))
            print(f"Toggle ignored (cooldown: {remaining}ms remaining)")
            return
        
        self.last_toggle_time = now_ms
        
        print(f"Toggle called, current state: visible={self.visible}")
        
        # If visible, hide it
        if self.window and self.visible:
            self.visible = False  # Set state BEFORE hiding
            self.hide_overlay()
        elif self.window:
            # Window exists but hidden, show it
            self.visible = True  # Set state BEFORE showing
            self.show_overlay()
        else:
            # Window doesn't exist, create it
            self.window = self.create_window()
            self.visible = True
            print("Overlay created and shown")
    
    def show_overlay(self) -> None:
        if self.visible and self.window:
            print("Already visible")
            return
        
        self.visible = True  # Set state BEFORE showing
        if self.window:
            self.window.deiconify()
        else:
            self.window = self.create_window()
        print("Overlay shown")
    
    def hide_overlay(self) -> None:
        self.visible = False  # Set state BEFORE hiding
        if self.window:
            self.window.withdraw()
        print("Overlay hidden")
    
    def create_window(self) -> tk.Toplevel:
        win = tk.Toplevel()
        # ... configure window ...
        return win
```

## Key Principles

### 1. Explicit State Tracking

**Don't rely on `isVisible()`:**
```javascript
// BAD
if (window.isVisible()) {
    window.hide();
}

// GOOD
if (visible) {
    visible = false;
    window.hide();
}
```

### 2. Set State Before Operations

**Prevent race conditions:**
```javascript
// BAD - State set after operation
window.hide();
visible = false;  // Another toggle might have fired

// GOOD - State set before operation
visible = false;
window.hide();
```

### 3. Cooldown Protection

**Prevent rapid toggling:**
```javascript
const COOLDOWN_MS = 300;  // 300ms minimum between toggles
let lastToggleTime = 0;

function toggle() {
    const now = Date.now();
    if (now - lastToggleTime < COOLDOWN_MS) {
        return;  // Ignore rapid toggles
    }
    lastToggleTime = now;
    // ... toggle logic ...
}
```

### 4. Event Listener Sync

**Keep state in sync with window events:**
```javascript
win.on('show', () => {
    visible = true;  // Sync state when window shows
});

win.on('hide', () => {
    visible = false;  // Sync state when window hides
});
```

### 5. Avoid Redundant Operations

**Don't call setup functions on every show:**
```javascript
// BAD - Re-setup on every show
function toggle() {
    if (visible) {
        window.hide();
    } else {
        window.show();
        setupAlwaysOnTop(window);  // Redundant - already set up
    }
}

// GOOD - Setup once, just show/hide
function toggle() {
    if (visible) {
        visible = false;
        window.hide();
    } else {
        visible = true;
        window.show();  // Setup already done
    }
}
```

## Common Pitfalls

### Pitfall 1: setInterval Re-showing Windows

**Problem:**
```javascript
setInterval(() => {
    window.setAlwaysOnTop(true);
    window.moveTop();  // Might trigger show event
}, 2000);
```

**Solution:**
```javascript
setInterval(() => {
    if (window && !window.isDestroyed() && window.isVisible()) {
        // Only reassert if actually visible
        window.setAlwaysOnTop(true);
        window.moveTop();
    }
}, 2000);
```

### Pitfall 2: Multiple Signal Handlers

**Problem:**
```javascript
// Signal received multiple times
ipcMain.on('toggle', () => toggle());
// Also registered elsewhere
signals.on('toggle', () => toggle());
```

**Solution:**
```javascript
// Use cooldown to prevent duplicate toggles
function toggle() {
    if (now - lastToggleTime < COOLDOWN_MS) {
        return;  // Ignore duplicate signals
    }
    // ... toggle logic ...
}
```

### Pitfall 3: State Out of Sync

**Problem:**
```javascript
// Window hidden externally, but state not updated
window.hide();  // Called from somewhere else
// visible is still true
```

**Solution:**
```javascript
// Use event listeners to sync state
window.on('hide', () => {
    visible = false;  // Always sync on hide
});
```

## Variations

### Single Window Toggle

```javascript
let window = null;
let visible = false;

function toggle() {
    if (visible) {
        visible = false;
        window.hide();
    } else {
        visible = true;
        if (window) {
            window.show();
        } else {
            window = createWindow();
        }
    }
}
```

### Multiple Windows Toggle

```javascript
let windows = [];
let visible = false;

function toggle() {
    if (visible) {
        visible = false;
        windows.forEach(win => win.hide());
    } else {
        visible = true;
        windows.forEach(win => win.show());
    }
}
```

### State-Based Toggle (Python)

```python
class State:
    def __init__(self):
        self.visible = False
        self.instances = []

def toggle():
    if state.visible and state.instances:
        hide_overlay()
    else:
        show_overlay()
```

## Timing Considerations

### Cooldown Duration

- **Short (100-200ms)**: Allows faster toggling, may still allow accidental double-toggles
- **Medium (300-500ms)**: Good balance (recommended)
- **Long (500ms+)**: Prevents rapid toggling, may feel unresponsive

### State Update Timing

Always set state **BEFORE** the operation:
```javascript
// Correct order
visible = false;  // 1. Set state
window.hide();    // 2. Perform operation
```

## Use Cases

1. **Overlay Windows**: Toolbar, arrow overlay, scroll overlay
2. **Modal Dialogs**: Show/hide dialogs
3. **Side Panels**: Toggle side panels in applications
4. **Notification Windows**: Show/hide notifications

## Related Patterns

- See `click-through-windows.md` for window interaction
- See `window-positioning.md` for window management
- See `state-machine.md` for complex state management
