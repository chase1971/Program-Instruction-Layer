# Continuous Key Press Pattern

## Overview

A pattern for maintaining continuous key press events through polling, ensuring keys stay pressed for applications that require repeated key events or may release keys unexpectedly.

## Pattern Description

Some applications (especially games) require:
1. Continuous key press events, not just a single press
2. Verification that keys are still pressed
3. Re-pressing if keys were released unexpectedly

This pattern uses polling to continuously send key press events while a key should be held.

## Implementation Structure

### Basic Polling

```javascript
let keyPressInterval = null;
const KEY_PRESS_INTERVAL = 50; // ms

function startKeyPress(key) {
    // Press key immediately
    sendKeyPress(key);
    
    // Start polling
    keyPressInterval = setInterval(() => {
        sendKeyPress(key);
    }, KEY_PRESS_INTERVAL);
}

function stopKeyPress() {
    if (keyPressInterval) {
        clearInterval(keyPressInterval);
        keyPressInterval = null;
    }
    sendKeyRelease(key);
}
```

### With State Management

```javascript
class ContinuousKeyPress {
    constructor(sendKeyPress, sendKeyRelease) {
        this.sendKeyPress = sendKeyPress;
        this.sendKeyRelease = sendKeyRelease;
        this.activeKey = null;
        this.pollInterval = null;
        this.POLL_INTERVAL = 50; // ms
    }
    
    start(key) {
        // Release previous key if different
        if (this.activeKey && this.activeKey !== key) {
            this.stop();
        }
        
        // Press new key
        this.activeKey = key;
        this.sendKeyPress(key);
        
        // Start polling
        this.pollInterval = setInterval(() => {
            if (this.activeKey === key) {
                this.sendKeyPress(key);
            } else {
                this.stop();
            }
        }, this.POLL_INTERVAL);
    }
    
    stop() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
        
        if (this.activeKey) {
            this.sendKeyRelease(this.activeKey);
            this.activeKey = null;
        }
    }
    
    switchKey(newKey) {
        if (this.activeKey === newKey) {
            return; // Already pressing this key
        }
        
        this.stop();
        this.start(newKey);
    }
}
```

## Cross-Process Implementation

### Electron Renderer → Main Process

```javascript
// Renderer (arrow-overlay.html)
const { ipcRenderer } = require('electron');

let keyPressInterval = null;
const KEY_PRESS_INTERVAL = 50;

button.addEventListener('mouseenter', () => {
    const key = button.dataset.key;
    
    // Press immediately
    ipcRenderer.send('arrow-key-press', key);
    
    // Start polling
    keyPressInterval = setInterval(() => {
        ipcRenderer.send('arrow-key-press', key);
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

### Python Verification

```python
import keyboard

current_arrow_key = None

def on_arrow_key_press(data):
    global current_arrow_key
    key = data['key'].lower()
    
    # If already pressing this key, verify it's still pressed
    if current_arrow_key == key:
        if not keyboard.is_pressed(key):
            # Key was released somehow, re-press it
            print(f"Key {key} was released, re-pressing")
            keyboard.press(key)
        return
    
    # Release previous key if different
    if current_arrow_key and current_arrow_key != key:
        keyboard.release(current_arrow_key)
    
    # Press new key
    current_arrow_key = key
    keyboard.press(key)
    
    # Verify it's actually pressed
    if keyboard.is_pressed(key):
        print(f"Key {key} confirmed pressed")
    else:
        print(f"WARNING: Key {key} may not be held properly")
```

## Timing Considerations

### Polling Interval

Choose based on application needs:

- **Fast (25ms)**: Very responsive, higher CPU usage
  - Good for: Fast-paced games, real-time applications
- **Medium (50ms)**: Good balance (recommended)
  - Good for: Most games, general applications
- **Slow (100ms)**: Lower CPU, may miss some events
  - Good for: Slow applications, accessibility tools

### Verification Frequency

How often to verify key is still pressed:

```python
VERIFY_INTERVAL = 5  # Verify every 5th poll

poll_count = 0

def poll_key_press(key):
    global poll_count
    poll_count += 1
    
    # Send press event
    send_key_press(key)
    
    # Periodically verify
    if poll_count % VERIFY_INTERVAL == 0:
        if not keyboard.is_pressed(key):
            # Key was released, re-press
            keyboard.press(key)
```

## Multiple Keys

### Sequential Keys (One at a Time)

```javascript
let activeKey = null;

function pressKey(key) {
    // Release previous key
    if (activeKey && activeKey !== key) {
        releaseKey(activeKey);
    }
    
    // Press new key
    activeKey = key;
    startPolling(key);
}
```

### Simultaneous Keys

```javascript
let activeKeys = new Set();

function pressKey(key) {
    activeKeys.add(key);
    sendKeyPress(key);
    startPolling(key);
}

function releaseKey(key) {
    activeKeys.delete(key);
    sendKeyRelease(key);
    stopPolling(key);
}

// Poll all active keys
setInterval(() => {
    activeKeys.forEach(key => {
        sendKeyPress(key);
    });
}, POLL_INTERVAL);
```

## Error Handling

### Key Release Detection

```python
def verify_key_pressed(key):
    """Verify key is still pressed, re-press if needed"""
    if not keyboard.is_pressed(key):
        print(f"Key {key} was released unexpectedly, re-pressing")
        try:
            keyboard.press(key)
            if keyboard.is_pressed(key):
                print(f"Key {key} re-pressed successfully")
            else:
                print(f"WARNING: Failed to re-press {key}")
        except Exception as e:
            print(f"Error re-pressing {key}: {e}")
            import traceback
            traceback.print_exc()
```

### Cleanup on Exit

```javascript
// Clean up on window close
window.on('closed', () => {
    // Stop all polling
    if (keyPressInterval) {
        clearInterval(keyPressInterval);
        keyPressInterval = null;
    }
    
    // Release all keys
    if (activeKey) {
        ipcRenderer.send('arrow-key-release', activeKey);
        activeKey = null;
    }
});
```

```python
# Python cleanup
def cleanup():
    global current_arrow_key
    if current_arrow_key:
        keyboard.release(current_arrow_key)
        current_arrow_key = None
```

## Complete Template

### JavaScript/Electron

```javascript
class ContinuousKeyPressManager {
    constructor(ipcRenderer) {
        this.ipc = ipcRenderer;
        this.activeKey = null;
        this.pollInterval = null;
        this.POLL_INTERVAL = 50; // ms
    }
    
    start(key) {
        // Release previous key if different
        if (this.activeKey && this.activeKey !== key) {
            this.stop();
        }
        
        // Press new key
        this.activeKey = key;
        this.ipc.send('arrow-key-press', key);
        
        // Start polling
        this.startPolling(key);
    }
    
    stop() {
        this.stopPolling();
        
        if (this.activeKey) {
            this.ipc.send('arrow-key-release', this.activeKey);
            this.activeKey = null;
        }
    }
    
    startPolling(key) {
        this.stopPolling(); // Clear any existing
        
        this.pollInterval = setInterval(() => {
            if (this.activeKey === key) {
                this.ipc.send('arrow-key-press', key);
            } else {
                this.stopPolling();
            }
        }, this.POLL_INTERVAL);
    }
    
    stopPolling() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }
    
    releaseAll() {
        this.stop();
    }
}
```

### Python

```python
import keyboard
import time

class ContinuousKeyPressHandler:
    def __init__(self):
        self.current_key = None
        self.last_verify_time = 0
        self.VERIFY_INTERVAL = 0.25  # seconds
    
    def on_key_press(self, data):
        key = data['key'].lower()
        
        # If already pressing this key, verify it's still pressed
        if self.current_key == key:
            if not keyboard.is_pressed(key):
                # Key was released, re-press it
                keyboard.press(key)
            return
        
        # Release previous key if different
        if self.current_key and self.current_key != key:
            keyboard.release(self.current_key)
        
        # Press new key
        self.current_key = key
        keyboard.press(key)
        
        # Verify it's actually pressed
        if not keyboard.is_pressed(key):
            print(f"WARNING: Key {key} may not be held properly")
    
    def on_key_release(self, data):
        key = data['key'].lower()
        if self.current_key == key:
            keyboard.release(key)
            self.current_key = None
    
    def verify_key(self):
        """Periodically verify key is still pressed"""
        if not self.current_key:
            return
        
        current_time = time.time()
        if current_time - self.last_verify_time >= self.VERIFY_INTERVAL:
            if not keyboard.is_pressed(self.current_key):
                # Key was released, re-press it
                keyboard.press(self.current_key)
            self.last_verify_time = current_time
    
    def release_all(self):
        if self.current_key:
            keyboard.release(self.current_key)
            self.current_key = None
```

## Use Cases

1. **Game Controls**: WASD movement that must stay pressed
2. **Accessibility**: Continuous input for users who can't hold keys
3. **Touch Interfaces**: Simulating key holds from touch events
4. **Remote Control**: Maintaining key state over network

## Related Patterns

- See `hover-to-key-press.md` for hover-based activation
- See `click-through-windows.md` for overlay interaction
