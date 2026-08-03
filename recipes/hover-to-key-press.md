# Hover-to-Key-Press Pattern

## Overview

A pattern for triggering keyboard key presses by hovering over UI elements. Used in the arrow module to simulate WASD key presses when hovering over directional buttons.

## Pattern Description

The hover-to-key-press pattern:
1. Detects when cursor enters a button region
2. Sends key press signal to keyboard simulation system
3. Continuously polls to maintain key press (for apps needing continuous events)
4. Releases key when cursor leaves button

## Implementation Structure

### Basic Hover Detection

```javascript
// HTML/Electron Renderer
buttons.forEach(button => {
    const key = button.dataset.key;
    
    button.addEventListener('mouseenter', () => {
        // Enable mouse events (disable click-through)
        ipcRenderer.send('arrow-mouse-on-button', true);
        
        // Press key
        ipcRenderer.send('arrow-key-press', key);
        button.classList.add('active');
    });
    
    button.addEventListener('mouseleave', () => {
        // Disable mouse events (enable click-through)
        ipcRenderer.send('arrow-mouse-on-button', false);
        
        // Release key
        ipcRenderer.send('arrow-key-release', key);
        button.classList.remove('active');
    });
});
```

### Continuous Key Press Polling

Some applications require continuous key press events. Polling ensures the key stays pressed:

```javascript
let keyPressInterval = null;
const KEY_PRESS_INTERVAL = 50; // ms

button.addEventListener('mouseenter', () => {
    const key = button.dataset.key;
    
    // Press key immediately
    ipcRenderer.send('arrow-key-press', key);
    
    // Start polling to keep key pressed
    keyPressInterval = setInterval(() => {
        if (activeKey === key) {
            ipcRenderer.send('arrow-key-press', key);
        } else {
            clearInterval(keyPressInterval);
            keyPressInterval = null;
        }
    }, KEY_PRESS_INTERVAL);
});

button.addEventListener('mouseleave', () => {
    // Stop polling
    if (keyPressInterval) {
        clearInterval(keyPressInterval);
        keyPressInterval = null;
    }
    
    // Release key
    ipcRenderer.send('arrow-key-release', key);
});
```

## Cross-Process Communication

### Electron Renderer → Main Process

```javascript
// Renderer (arrow-overlay.html)
ipcRenderer.send('arrow-key-press', 'w');
ipcRenderer.send('arrow-key-release', 'w');
```

### Main Process → Python Signal Server

```javascript
// Main process (main.js)
ipcMain.on('arrow-key-press', (event, key) => {
    sendSignal('arrow_key_press', { key: key });
});

ipcMain.on('arrow-key-release', (event, key) => {
    sendSignal('arrow_key_release', { key: key });
});
```

### Python Signal Handler → Keyboard Simulation

```python
# Python (main.py)
import keyboard

current_arrow_key = None

def on_arrow_key_press(data):
    global current_arrow_key
    key = data['key'].lower()
    
    # Release previous key if different
    if current_arrow_key and current_arrow_key != key:
        keyboard.release(current_arrow_key)
    
    # Press new key
    current_arrow_key = key
    keyboard.press(key)

def on_arrow_key_release(data):
    global current_arrow_key
    key = data['key'].lower()
    
    if current_arrow_key == key:
        keyboard.release(key)
        current_arrow_key = None

# Register handlers
signals.listen("arrow_key_press", on_arrow_key_press)
signals.listen("arrow_key_release", on_arrow_key_release)
```

## Key State Management

### Preventing Key Conflicts

Only one key should be pressed at a time:

```python
def on_arrow_key_press(data):
    global current_arrow_key
    key = data['key'].lower()
    
    # If already pressing this key, verify it's still pressed
    if current_arrow_key == key:
        if not keyboard.is_pressed(key):
            # Key was released somehow, re-press it
            keyboard.press(key)
        return
    
    # Release previous key if different
    if current_arrow_key and current_arrow_key != key:
        keyboard.release(current_arrow_key)
    
    # Press new key
    current_arrow_key = key
    keyboard.press(key)
```

### Force Release All Keys

Emergency release when overlay is hidden:

```python
def on_arrow_key_release_all(data):
    global current_arrow_key
    if current_arrow_key:
        keyboard.release(current_arrow_key)
        current_arrow_key = None
```

```javascript
// Electron main process
arrowOverlayWindow.on('closed', () => {
    sendSignal('arrow_key_release_all');
});
```

## Click-Through Window Management

### Enable Interaction on Hover

Window starts click-through, becomes interactive when hovering over buttons:

```javascript
// Main process (main.js)
// Create window with click-through
win.setIgnoreMouseEvents(true, { forward: true });

// Enable interaction when hovering over button
ipcMain.on('arrow-mouse-on-button', (event, isOnButton) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (win) {
        // Disable click-through when on button (enable interaction)
        // Enable click-through when not on button
        win.setIgnoreMouseEvents(!isOnButton, { forward: true });
    }
});
```

### Renderer Notifies Main Process

```javascript
// Renderer (arrow-overlay.html)
button.addEventListener('mouseenter', () => {
    // Tell main process we're on a button
    ipcRenderer.send('arrow-mouse-on-button', true);
});

button.addEventListener('mouseleave', () => {
    // Tell main process we left the button
    ipcRenderer.send('arrow-mouse-on-button', false);
});
```

## Visual Feedback

### Active State Styling

```css
.wasd-button {
    background: linear-gradient(to bottom, #64748b, #334155);
    transition: all 0.15s ease;
}

.wasd-button:hover,
.wasd-button.active {
    background: linear-gradient(to bottom, #94a3b8, #475569);
    box-shadow: 0 10px 15px -3px rgba(100, 116, 139, 0.5);
}
```

```javascript
// Add active class on hover
button.addEventListener('mouseenter', () => {
    button.classList.add('active');
});

button.addEventListener('mouseleave', () => {
    button.classList.remove('active');
});
```

## Complete Template

### Electron Renderer

```javascript
class HoverKeyPress {
    constructor(buttons, ipcRenderer) {
        this.buttons = buttons;
        this.ipc = ipcRenderer;
        this.activeKey = null;
        this.keyPressInterval = null;
        this.KEY_PRESS_INTERVAL = 50; // ms
    }
    
    setup() {
        this.buttons.forEach(button => {
            const key = button.dataset.key;
            
            button.addEventListener('mouseenter', () => {
                this.onButtonEnter(button, key);
            });
            
            button.addEventListener('mouseleave', () => {
                this.onButtonLeave(button, key);
            });
        });
    }
    
    onButtonEnter(button, key) {
        // Enable interaction
        this.ipc.send('arrow-mouse-on-button', true);
        
        // Release previous key if different
        if (this.activeKey && this.activeKey !== key) {
            this.ipc.send('arrow-key-release', this.activeKey);
        }
        
        // Press new key
        this.activeKey = key;
        button.classList.add('active');
        this.ipc.send('arrow-key-press', key);
        
        // Start polling
        this.startPolling(key);
    }
    
    onButtonLeave(button, key) {
        // Disable interaction
        this.ipc.send('arrow-mouse-on-button', false);
        
        // Stop polling
        this.stopPolling();
        
        // Release key
        if (this.activeKey === key) {
            button.classList.remove('active');
            this.ipc.send('arrow-key-release', key);
            this.activeKey = null;
        }
    }
    
    startPolling(key) {
        this.stopPolling(); // Clear any existing
        
        this.keyPressInterval = setInterval(() => {
            if (this.activeKey === key) {
                this.ipc.send('arrow-key-press', key);
            } else {
                this.stopPolling();
            }
        }, this.KEY_PRESS_INTERVAL);
    }
    
    stopPolling() {
        if (this.keyPressInterval) {
            clearInterval(this.keyPressInterval);
            this.keyPressInterval = null;
        }
    }
    
    releaseAll() {
        this.stopPolling();
        if (this.activeKey) {
            this.ipc.send('arrow-key-release', this.activeKey);
            this.activeKey = null;
        }
    }
}
```

### Python Keyboard Handler

```python
class ArrowKeyHandler:
    def __init__(self):
        self.current_key = None
    
    def on_key_press(self, data):
        key = data['key'].lower()
        
        # Verify current key is still pressed
        if self.current_key == key:
            if not keyboard.is_pressed(key):
                keyboard.press(key)
            return
        
        # Release previous key
        if self.current_key and self.current_key != key:
            keyboard.release(self.current_key)
        
        # Press new key
        self.current_key = key
        keyboard.press(key)
    
    def on_key_release(self, data):
        key = data['key'].lower()
        if self.current_key == key:
            keyboard.release(key)
            self.current_key = None
    
    def release_all(self):
        if self.current_key:
            keyboard.release(self.current_key)
            self.current_key = None
```

## Timing Considerations

### Polling Interval

- **Fast (25ms)**: Very responsive, higher CPU usage
- **Medium (50ms)**: Good balance (recommended)
- **Slow (100ms)**: Lower CPU, may miss some events

### Key Press Verification

Some applications may release keys unexpectedly. Verify and re-press:

```python
if current_arrow_key == key:
    if not keyboard.is_pressed(key):
        # Key was released, re-press it
        keyboard.press(key)
```

## Use Cases

1. **Game Controls**: WASD movement via hover
2. **Accessibility**: Alternative input methods
3. **Touch Interfaces**: Hover-based keyboard simulation
4. **Overlay Controls**: Non-intrusive UI controls

## Related Patterns

- See `click-through-windows.md` for window interaction management
- See `hover-to-lock-drag.md` for drag pattern
- See `mouse-hover-detection.md` for hover detection
