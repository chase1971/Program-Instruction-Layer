# Click-Through Windows Pattern

> **You might say:** "the overlay eats my clicks", "click-through window", "only the buttons should be clickable"
> **What it is:** Overlay windows that ignore the mouse except over interactive regions.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/electron-app/src/window-helpers.js`
- `electron-toolbar/electron-app/src/ipc-handlers/toolbar-handlers.js`
- `electron-toolbar/electron-app/src/ipc-handlers/arrow-handlers.js`

---

## Overview

A pattern for creating overlay windows that ignore mouse events by default, but become interactive when the cursor hovers over specific UI elements. This allows overlays to be non-intrusive while still providing interactive controls.

## Pattern Description

Click-through windows:
1. Start with `setIgnoreMouseEvents(true)` - all mouse events pass through
2. Detect when cursor enters interactive regions
3. Temporarily disable click-through for that window
4. Re-enable click-through when cursor leaves interactive regions

## Implementation Structure

### Electron Implementation

#### Window Creation

```javascript
const win = new BrowserWindow({
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    resizable: false,
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: false
    }
});

// Start with click-through enabled
win.setIgnoreMouseEvents(true, { forward: true });
```

#### Dynamic Click-Through Management

```javascript
// Main process (main.js)
ipcMain.on('arrow-mouse-on-button', (event, isOnButton) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (win) {
        // When mouse is over a button, disable click-through (enable interaction)
        // When mouse leaves button, re-enable click-through
        win.setIgnoreMouseEvents(!isOnButton, { forward: true });
    }
});
```

#### Renderer Notifications

```javascript
// Renderer (arrow-overlay.html)
const buttons = document.querySelectorAll('.wasd-button');

buttons.forEach(button => {
    button.addEventListener('mouseenter', () => {
        // Tell main process we're on a button
        ipcRenderer.send('arrow-mouse-on-button', true);
    });
    
    button.addEventListener('mouseleave', () => {
        // Tell main process we left the button
        ipcRenderer.send('arrow-mouse-on-button', false);
    });
});
```

### Python/Tkinter Implementation

#### Windows API Setup

```python
import ctypes
from ctypes import wintypes

# Windows constants
GWL_EXSTYLE = -20
WS_EX_NOACTIVATE = 0x08000000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

def make_click_through(window):
    """Make a Tkinter window click-through on Windows"""
    if os.name != "nt":
        return
    
    try:
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style |= (WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW | 
                  WS_EX_LAYERED | WS_EX_TRANSPARENT)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    except OSError as e:
        print(f"Click-through setup failed: {e}")

def make_interactive(window):
    """Make a Tkinter window interactive (disable click-through)"""
    if os.name != "nt":
        return
    
    try:
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style &= ~WS_EX_TRANSPARENT  # Remove transparent flag
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    except OSError as e:
        print(f"Interactive setup failed: {e}")
```

#### Dynamic Toggle

```python
def on_mouse_enter_button(event):
    """Mouse entered button - enable interaction"""
    make_interactive(window)

def on_mouse_leave_button(event):
    """Mouse left button - enable click-through"""
    make_click_through(window)

# Bind events
button.bind('<Enter>', on_mouse_enter_button)
button.bind('<Leave>', on_mouse_leave_button)
```

## Forward Option

The `forward` option in Electron's `setIgnoreMouseEvents`:

```javascript
win.setIgnoreMouseEvents(true, { forward: true });
```

- **`forward: true`**: Mouse events are forwarded to the window behind
- **`forward: false`**: Mouse events are ignored completely

Use `forward: true` for overlays that should allow interaction with underlying applications.

## Multiple Interactive Regions

### Managing Multiple Buttons

```javascript
let interactiveRegions = new Set();

function updateClickThrough(win) {
    // If any region is active, disable click-through
    const shouldBeInteractive = interactiveRegions.size > 0;
    win.setIgnoreMouseEvents(!shouldBeInteractive, { forward: true });
}

// Button 1
button1.addEventListener('mouseenter', () => {
    interactiveRegions.add('button1');
    updateClickThrough(win);
});

button1.addEventListener('mouseleave', () => {
    interactiveRegions.delete('button1');
    updateClickThrough(win);
});

// Button 2
button2.addEventListener('mouseenter', () => {
    interactiveRegions.add('button2');
    updateClickThrough(win);
});

button2.addEventListener('mouseleave', () => {
    interactiveRegions.delete('button2');
    updateClickThrough(win);
});
```

### Drag Handle

```javascript
const dragHandle = document.getElementById('dragHandle');

dragHandle.addEventListener('mouseenter', () => {
    interactiveRegions.add('dragHandle');
    updateClickThrough(win);
});

dragHandle.addEventListener('mouseleave', () => {
    interactiveRegions.delete('dragHandle');
    updateClickThrough(win);
});
```

## Complete Template

### Electron

```javascript
class ClickThroughManager {
    constructor(window) {
        this.window = window;
        this.interactiveRegions = new Set();
        
        // Start with click-through
        this.window.setIgnoreMouseEvents(true, { forward: true });
    }
    
    addInteractiveRegion(regionId, element) {
        element.addEventListener('mouseenter', () => {
            this.interactiveRegions.add(regionId);
            this.updateClickThrough();
        });
        
        element.addEventListener('mouseleave', () => {
            this.interactiveRegions.delete(regionId);
            this.updateClickThrough();
        });
    }
    
    updateClickThrough() {
        const shouldBeInteractive = this.interactiveRegions.size > 0;
        this.window.setIgnoreMouseEvents(!shouldBeInteractive, { forward: true });
    }
    
    forceInteractive(interactive) {
        this.window.setIgnoreMouseEvents(!interactive, { forward: true });
    }
}

// Usage
const win = new BrowserWindow({ /* ... */ });
const clickThroughManager = new ClickThroughManager(win);

// Add interactive regions
clickThroughManager.addInteractiveRegion('button1', button1);
clickThroughManager.addInteractiveRegion('button2', button2);
clickThroughManager.addInteractiveRegion('dragHandle', dragHandle);
```

### Python/Tkinter

```python
class ClickThroughManager:
    def __init__(self, window):
        self.window = window
        self.interactive_regions = set()
        self.make_click_through()
    
    def make_click_through(self):
        """Enable click-through"""
        if os.name != "nt":
            return
        
        try:
            hwnd = ctypes.windll.user32.GetParent(self.window.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style |= WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except OSError:
            pass
    
    def make_interactive(self):
        """Disable click-through"""
        if os.name != "nt":
            return
        
        try:
            hwnd = ctypes.windll.user32.GetParent(self.window.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style &= ~WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except OSError:
            pass
    
    def add_interactive_region(self, region_id, widget):
        """Add a widget that should enable interaction"""
        def on_enter(event):
            self.interactive_regions.add(region_id)
            self.update_click_through()
        
        def on_leave(event):
            self.interactive_regions.discard(region_id)
            self.update_click_through()
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def update_click_through(self):
        """Update click-through based on active regions"""
        if len(self.interactive_regions) > 0:
            self.make_interactive()
        else:
            self.make_click_through()
```

## Edge Cases

### Rapid Mouse Movement

Mouse may leave region before event fires. Use small delays:

```javascript
let leaveTimeout = null;

button.addEventListener('mouseenter', () => {
    if (leaveTimeout) {
        clearTimeout(leaveTimeout);
        leaveTimeout = null;
    }
    enableInteraction();
});

button.addEventListener('mouseleave', () => {
    leaveTimeout = setTimeout(() => {
        disableInteraction();
    }, 50); // Small delay
});
```

### Nested Elements

Child elements should inherit interaction:

```javascript
// Parent container
container.addEventListener('mouseenter', () => {
    enableInteraction();
});

// Child buttons don't need separate handlers
// They inherit from parent
```

## Platform Differences

### Windows

Uses Windows API (`SetWindowLongW`) with `WS_EX_TRANSPARENT` flag.

### macOS

Electron handles click-through automatically. Tkinter requires different approach.

### Linux

May require X11 extensions. Electron handles automatically.

## Use Cases

1. **Overlay Controls**: Non-intrusive UI that becomes interactive on hover
2. **Game Overlays**: Controls that don't interfere with gameplay
3. **Accessibility Tools**: Assistive interfaces that don't block interaction
4. **Monitoring Displays**: Status overlays that can be clicked through

## Related Patterns

- See `hover-to-key-press.md` for hover-based key simulation
- See `hover-to-lock-drag.md` for drag interactions
- See `mouse-hover-detection.md` for hover detection
