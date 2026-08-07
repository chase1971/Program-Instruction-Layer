# Toolbar System Pattern

> **You might say:** "build a toolbar", "add a button to the toolbar", "the toolbar will not come back"
> **What it is:** A full overlay toolbar: click-through window, dwell-activated buttons, auto-hide, reposition mode, multi-monitor.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/electron-app/src/window-managers/toolbar-manager.js — `createAllToolbars`, `startAutoHideTimer``
- `electron-toolbar/electron-app/src/toolbar.html — `dwellTimer`, `activateButton` (~lines 346-403)`
- `electron-toolbar/electron-app/src/main-constants.js — `COOLDOWNS`, `AUTO_HIDE_CONFIG``

---

## Overview

A reusable toolbar system that provides hover-based button activation with dwell time, progress feedback, and click-through window support. Designed for non-intrusive overlay interfaces.

## Pattern Description

The toolbar system:
1. Creates click-through overlay windows (one per monitor)
2. Provides buttons with hover-based dwell activation
3. Shows visual progress during dwell time
4. Sends actions via IPC to main process
5. Supports reposition mode for moving the toolbar

## Architecture

### Components

1. **HTML/CSS/JS (toolbar.html)**: Renderer process, handles UI and dwell activation
2. **Main Process (main.js)**: Creates windows, handles IPC, manages state
3. **Signal System**: Communicates with Python backend

### Window Structure

```
Toolbar Window (Electron BrowserWindow)
├── Click-through by default
├── Interactive on button hover
├── Always on top
└── Transparent background
```

## Adding Buttons

### HTML Structure

Add buttons to `toolbar.html`:

```html
<div class="button-row">
    <!-- New button -->
    <div class="toolbar-button" data-action="my_action" data-tooltip="My Action">
        <span>🔘</span>  <!-- Icon or text -->
        <svg class="progress-ring">
            <circle cx="18" cy="18" r="15"></circle>
        </svg>
    </div>
</div>
```

### Required Elements

1. **Container**: `.toolbar-button` class
2. **Action**: `data-action` attribute (used for IPC)
3. **Icon**: Content inside button (emoji, text, or SVG)
4. **Progress Ring**: SVG circle for dwell progress visualization

### Button Structure

```html
<div class="toolbar-button" data-action="action_name" data-tooltip="Tooltip Text">
    <!-- Icon/Content -->
    <span>→</span>
    
    <!-- Progress ring (required for dwell activation) -->
    <svg class="progress-ring">
        <circle cx="18" cy="18" r="15"></circle>
    </svg>
</div>
```

### Blank/Spacer Buttons

For spacing without functionality:

```html
<div class="toolbar-button blank"></div>
```

## Dwell Activation System

### How It Works

1. **Hover Detection**: Mouse enters button area
2. **Dwell Timer**: Starts counting down (default 600ms)
3. **Progress Ring**: Visual feedback shows progress
4. **Activation**: After dwell time, action is triggered
5. **Cooldown**: Prevents rapid re-activation (default 800ms)

### Dwell Flow

```
Mouse Enter
  └─> Start Dwell Timer (600ms)
      └─> Update Progress Ring
          └─> Timer Complete
              └─> Send Action via IPC
                  └─> Cooldown (800ms)
```

### Configuration

In `toolbar.html`:

```javascript
const DWELL_TIME = /* see electron-toolbar/modules/dwell/backend/dwell_constants.py — DWELL_TIME */;
const COOLDOWN_TIME = 800;   // ms between activations
```

## Hover Interaction

### Mouse Events

Buttons automatically handle:

```javascript
button.addEventListener('mouseenter', () => {
    // Enable interaction (disable click-through)
    ipcRenderer.send('mouse-on-button', true);
    
    // Start dwell activation
    startDwell(button);
});

button.addEventListener('mouseleave', () => {
    // Disable interaction (enable click-through)
    ipcRenderer.send('mouse-on-button', false);
    
    // Cancel dwell activation
    cancelDwell();
});
```

### Click-Through Management

The toolbar window:
- Starts with `setIgnoreMouseEvents(true, { forward: true })`
- Becomes interactive when hovering over buttons
- Returns to click-through when mouse leaves

```javascript
// Main process (main.js)
ipcMain.on('mouse-on-button', (event, isOnButton) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (win) {
        // Toggle click-through based on hover
        win.setIgnoreMouseEvents(!isOnButton, { forward: true });
    }
});
```

## Visual Feedback

### Button States

1. **Default**: Semi-transparent background
2. **Hover**: Slightly brighter, scale up
3. **Activating**: Green tint, progress ring animating
4. **Activated**: Bright green flash (200ms)

### CSS Classes

```css
.toolbar-button              /* Default state */
.toolbar-button:hover        /* Hover state */
.toolbar-button.activating   /* Dwell in progress */
.toolbar-button.activated    /* Just activated */
.toolbar-button.blank        /* Spacer button */
```

### Progress Ring

The progress ring shows dwell progress:

```javascript
// Update progress ring
const circle = button.querySelector('.progress-ring circle');
const progress = elapsed / DWELL_TIME;
// 95 is full circle, 0 is complete
circle.style.strokeDashoffset = 95 - (progress * 95);
```

## Action Handling

### Renderer → Main Process

```javascript
// toolbar.html
function activateButton(button) {
    const action = button.dataset.action;
    ipcRenderer.send('button-action', action);
}
```

### Main Process Handler

```javascript
// main.js
ipcMain.on('button-action', (event, action) => {
    console.log('[IPC] Button action:', action);
    
    // Handle locally if needed
    if (action === 'toggle_arrow') {
        toggleArrowOverlay();
    }
    
    // Send to Python signal server
    sendSignal(action);
});
```

### Python Signal Handler

```python
# main.py
def on_toggle_arrow(data):
    # Handle arrow toggle
    pass

signals.listen("toggle_arrow", on_toggle_arrow)
```

## Complete Button Example

### HTML

```html
<div class="button-row">
    <div class="toolbar-button" data-action="my_custom_action" data-tooltip="Custom Action">
        <span>⭐</span>
        <svg class="progress-ring">
            <circle cx="18" cy="18" r="15"></circle>
        </svg>
    </div>
</div>
```

### Main Process Handler

```javascript
// main.js
ipcMain.on('button-action', (event, action) => {
    switch (action) {
        case 'my_custom_action':
            // Handle custom action
            console.log('Custom action triggered');
            // Send to Python if needed
            sendSignal('my_custom_action');
            break;
    }
});
```

### Python Handler (Optional)

```python
# main.py
def on_my_custom_action(data):
    print("Custom action received from toolbar")
    # Do something

signals.listen("my_custom_action", on_my_custom_action)
```

## Reposition Mode

### Enabling

Reposition mode allows dragging the toolbar:

```javascript
// Toggle via signal
sendSignal('toggle_reposition_mode');

// Or via hotkey (Ctrl+F10)
globalShortcut.register('Ctrl+F10', () => {
    toggleRepositionMode();
});
```

### How It Works

1. Disables click-through temporarily
2. Enables window dragging
3. Shows visual feedback ("DRAG TO MOVE")
4. Saves position when moved
5. Re-enables click-through when disabled

```javascript
function toggleRepositionMode() {
    repositionMode = !repositionMode;
    
    toolbarWindows.forEach(win => {
        if (repositionMode) {
            // Enable mouse events for dragging
            win.setIgnoreMouseEvents(false);
        } else {
            // Back to click-through
            win.setIgnoreMouseEvents(true, { forward: true });
        }
        // Update renderer visual state
        win.webContents.send('reposition-mode', repositionMode);
    });
}
```

## Multi-Monitor Support

### Automatic Creation

Toolbars are created for each monitor:

```javascript
function createAllToolbars() {
    const displays = screen.getAllDisplays();
    
    displays.forEach((display, index) => {
        const win = createToolbarWindow(display, index);
        toolbarWindows.push(win);
    });
}
```

### Position Storage

Each toolbar's position is saved separately:

```javascript
// Save position
store.set(`toolbar_${index}_bounds`, bounds);

// Load position
const savedBounds = store.get(`toolbar_${index}_bounds`);
```

## Configuration

### Window Defaults

```javascript
const TOOLBAR_DEFAULTS = {
    WIDTH: 200,
    HEIGHT: 120,
    OFFSET_X: 100,  // From right edge
    OFFSET_Y: 300   // From bottom edge
};
```

### Dwell Settings

```javascript
const DWELL_TIME = /* see electron-toolbar/modules/dwell/backend/dwell_constants.py — DWELL_TIME */;
const COOLDOWN_TIME = 800;   // ms - time between activations
```

### Cooldowns

```javascript
const COOLDOWNS = {
    REPOSITION_TOGGLE: 300,  // ms
    TOOLBAR_TOGGLE: 300      // ms
};
```

## Button Layout

### Rows

Buttons are organized in rows:

```html
<div class="toolbar-container">
    <!-- Top row -->
    <div class="button-row">
        <div class="toolbar-button" data-action="action1">...</div>
        <div class="toolbar-button" data-action="action2">...</div>
    </div>
    
    <!-- Bottom row -->
    <div class="button-row">
        <div class="toolbar-button" data-action="action3">...</div>
        <div class="toolbar-button" data-action="action4">...</div>
    </div>
</div>
```

### Spacing

- Gap between buttons: `6px`
- Gap between rows: `6px`
- Padding around container: `10px`

## Styling Customization

### Button Colors

```css
.toolbar-button {
    background: rgba(68, 68, 68, 0.5);
    border: 2px solid rgba(136, 136, 136, 0.5);
}

.toolbar-button:hover {
    background: rgba(102, 102, 102, 0.5);
    border-color: rgba(170, 170, 170, 0.5);
}

.toolbar-button.activating {
    background: rgba(100, 140, 100, 0.5);
    border-color: rgba(150, 200, 150, 0.5);
}

.toolbar-button.activated {
    background: rgba(80, 160, 80, 0.5);
    border-color: rgba(120, 220, 120, 0.5);
}
```

### Progress Ring

```css
.progress-ring circle {
    stroke: #4CAF50;        /* Green */
    stroke-width: 2;
    stroke-dasharray: 95;   /* Full circle */
    stroke-dashoffset: 95;   /* Start hidden */
}
```

## Auto-Hide and Collapsible Toolbar

### Overview

The toolbar supports auto-hide functionality with a collapsible design:
- **Collapsed State**: Only a small arrow indicator is visible on the right edge
- **Expanded State**: Full toolbar with all buttons visible
- **Auto-Collapse**: Toolbar automatically collapses after inactivity timeout

### Arrow Indicator

A small arrow indicator (◀) remains visible on the right edge when collapsed:

```html
<div class="arrow-indicator" id="arrowIndicator"></div>
```

**Behavior**:
- Always visible (even when toolbar is collapsed)
- Hover: Expands toolbar if collapsed
- Click: Toggles toolbar expansion state
- Visual feedback: Arrow rotates 180° when expanded

### Expansion State Management

**Critical**: Track expansion state separately from visibility state.

```javascript
// Main process (main.js)
let toolbarVisible = false;   // Window visibility
let toolbarExpanded = false;  // Toolbar expansion (separate state!)

// Renderer (toolbar.html)
let toolbarExpanded = false;  // Local expansion state
```

**State Synchronization**:
- Renderer sends `toolbar-expanded` IPC message on state change
- Main process syncs state via IPC handler
- Auto-hide timer checks BOTH `toolbarVisible` AND `toolbarExpanded`

### Auto-Hide Configuration

```javascript
// Main process (main.js)
const AUTO_HIDE_CONFIG = {
    INACTIVITY_TIMEOUT: 5000,   // 5 seconds in milliseconds
    CHECK_INTERVAL: 1000        // Check every second
};
```

### Implementation Pattern

**Main Process**:
```javascript
// Track expansion state
let toolbarExpanded = false;

// Auto-hide timer
function startAutoHideTimer() {
    autoHideTimer = setInterval(() => {
        if (toolbarVisible && toolbarExpanded) {
            const timeSinceLastInteraction = Date.now() - lastToolbarInteractionTime;
            
            if (timeSinceLastInteraction >= AUTO_HIDE_CONFIG.INACTIVITY_TIMEOUT) {
                toolbarExpanded = false;  // Set state BEFORE collapsing
                toolbarWindows.forEach(win => {
                    if (!win.isDestroyed()) {
                        win.webContents.send('collapse-toolbar');
                    }
                });
            }
        }
    }, AUTO_HIDE_CONFIG.CHECK_INTERVAL);
}

// Sync expansion state
ipcMain.on('toolbar-expanded', (event, expanded) => {
    toolbarExpanded = expanded;  // Sync state
    resetToolbarInteractionTimer();
});
```

**Renderer**:
```javascript
// Expansion functions
function expandToolbar() {
    if (toolbarExpanded) return;
    toolbarExpanded = true;
    container.classList.add('expanded');
    arrowIndicator.classList.add('expanded');
    ipcRenderer.send('toolbar-expanded', true);
    ipcRenderer.send('toolbar-interaction');
}

function collapseToolbar() {
    if (!toolbarExpanded) return;
    toolbarExpanded = false;
    container.classList.remove('expanded');
    arrowIndicator.classList.remove('expanded');
    ipcRenderer.send('toolbar-expanded', false);
}

// Handle collapse from main process
ipcRenderer.on('collapse-toolbar', () => {
    collapseToolbar();
});
```

### Interaction Tracking

Reset timer on ALL interactions:
- Arrow hover/click
- Button hover
- Button clicks
- Button activations

```javascript
// Track all interactions
ipcRenderer.send('toolbar-interaction');

// Main process resets timer
ipcMain.on('toolbar-interaction', () => {
    resetToolbarInteractionTimer();
});
```

### CSS for Collapsible Toolbar

```css
/* Arrow indicator - always visible */
.arrow-indicator {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 12px;
    height: 40px;
    z-index: 10;
}

.arrow-indicator::before {
    content: '◀';
    transition: transform 0.3s ease;
}

.arrow-indicator.expanded::before {
    transform: rotate(180deg);
}

/* Toolbar container - slides in/out */
.toolbar-container {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translate(100%, -50%); /* Hidden by default */
    transition: transform 0.3s ease;
}

.toolbar-container.expanded {
    transform: translate(0, -50%); /* Visible when expanded */
}
```

### Key Principles

1. **Separate States**: Track `toolbarVisible` (window) and `toolbarExpanded` (toolbar) separately
2. **State Sync**: Always sync expansion state via IPC between renderer and main process
3. **Set State First**: Set `toolbarExpanded = false` BEFORE sending collapse command
4. **Timer Check**: Auto-hide timer must check BOTH visibility AND expansion states
5. **Reset on Interaction**: Reset interaction timer on ALL user interactions

## Best Practices

### Button Actions

1. Use descriptive `data-action` names (snake_case)
2. Keep actions simple and focused
3. Handle actions in main process first, then forward to Python if needed

### Icons

1. Use emoji for simple icons (✅, ❌, →, ⇈)
2. Use Unicode symbols for directional controls
3. Keep icons small and visible at 30x30px

### Layout

1. Group related buttons in same row
2. Use blank buttons for spacing
3. Limit to 2-3 rows for compactness

### Performance

1. Dwell time should be 400-800ms (not too fast, not too slow)
2. Cooldown prevents accidental double-activation
3. Progress ring updates at 60fps (16ms intervals)

### Auto-Hide

1. Inactivity timeout: 5-10 seconds (configurable)
2. Check interval: 1 second (balance between responsiveness and performance)
3. Always track expansion state separately from visibility
4. Reset timer on all interactions (hover, click, activation)

## Related Patterns

- See `click-through-windows.md` for window interaction
- See `dwell-click.md` for dwell activation pattern
- See `hover-to-key-press.md` for hover-based actions
- See `toggle-pattern.md` for toggle functionality
