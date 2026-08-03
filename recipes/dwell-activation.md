# Dwell Activation Pattern

> **You might say:** "hover a button to fire it", "toolbar button activation", "it fires before I mean it to"
> **What it is:** Hover-for-a-duration to trigger an action, with progress feedback and a cooldown.

**Exemplar files — read these before writing new code:**

- `electron-toolbar/electron-app/src/toolbar.html — `dwellTimer`, `activateButton` (~lines 346-403)`
- `electron-toolbar/electron-app/src/window-managers/toolbar-manager.js`

---

## Overview

A pattern for triggering actions by hovering over UI elements for a set duration (dwell time). Provides visual progress feedback and prevents accidental activation.

## Pattern Description

Dwell activation:
1. Detects when cursor enters an element
2. Starts a timer (dwell time)
3. Shows visual progress feedback
4. Triggers action when timer completes
5. Enforces cooldown to prevent rapid re-activation

## Implementation Structure

### Basic Dwell System

```javascript
const DWELL_TIME = /* see electron-toolbar/modules/dwell/backend/dwell_constants.py — DWELL_TIME */;
const COOLDOWN_TIME = /* see electron-toolbar/modules/dwell/backend/dwell_constants.py — TOGGLE_COOLDOWN */;

let dwellTimer = null;
let dwellStartTime = null;
let lastActivationTime = 0;
let currentElement = null;

function startDwell(element) {
    const now = Date.now();
    
    // Check cooldown
    if (now - lastActivationTime < COOLDOWN_TIME) {
        return; // Still in cooldown
    }
    
    // Cancel any existing dwell
    cancelDwell();
    
    // Start new dwell
    currentElement = element;
    dwellStartTime = now;
    element.classList.add('activating');
    
    // Set activation timer
    dwellTimer = setTimeout(() => {
        activateElement(element);
    }, DWELL_TIME);
}

function cancelDwell() {
    if (dwellTimer) {
        clearTimeout(dwellTimer);
        dwellTimer = null;
    }
    if (currentElement) {
        currentElement.classList.remove('activating');
        currentElement = null;
    }
    dwellStartTime = null;
}

function activateElement(element) {
    const now = Date.now();
    
    // Final cooldown check
    if (now - lastActivationTime < COOLDOWN_TIME) {
        cancelDwell();
        return;
    }
    
    // Cancel dwell
    cancelDwell();
    
    // Trigger action
    const action = element.dataset.action;
    triggerAction(action);
    
    // Record activation time
    lastActivationTime = now;
}
```

## Progress Feedback

### Progress Ring (SVG Circle)

```html
<svg class="progress-ring">
    <circle cx="18" cy="18" r="15"></circle>
</svg>
```

```css
.progress-ring {
    position: absolute;
    width: 36px;
    height: 36px;
    pointer-events: none;
}

.progress-ring circle {
    fill: none;
    stroke: #4CAF50;
    stroke-width: 2;
    stroke-linecap: round;
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
    stroke-dasharray: 95;      /* Full circle */
    stroke-dashoffset: 95;     /* Start hidden */
    transition: stroke-dashoffset 0.05s linear;
}
```

### Progress Update

```javascript
let progressInterval = null;

function startDwell(element) {
    // ... setup ...
    
    const circle = element.querySelector('.progress-ring circle');
    
    // Update progress every frame
    progressInterval = setInterval(() => {
        const elapsed = Date.now() - dwellStartTime;
        const progress = Math.min(elapsed / DWELL_TIME, 1);
        
        // Update stroke offset (95 is full circle)
        circle.style.strokeDashoffset = 95 - (progress * 95);
    }, 16); // ~60fps
}

function cancelDwell() {
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    
    if (currentElement) {
        const circle = currentElement.querySelector('.progress-ring circle');
        if (circle) {
            circle.style.strokeDashoffset = '95'; // Reset
        }
    }
}
```

## Visual States

### CSS Classes

```css
.element {
    /* Default state */
    background: rgba(68, 68, 68, 0.5);
    transition: all 0.15s ease;
}

.element:hover {
    /* Hover state */
    background: rgba(102, 102, 102, 0.5);
    transform: scale(1.05);
}

.element.activating {
    /* Dwell in progress */
    background: rgba(100, 140, 100, 0.5);
    border-color: rgba(150, 200, 150, 0.5);
}

.element.activated {
    /* Just activated (brief flash) */
    background: rgba(80, 160, 80, 0.5);
    border-color: rgba(120, 220, 120, 0.5);
}
```

### State Management

```javascript
function activateElement(element) {
    // Remove activating state
    element.classList.remove('activating');
    
    // Add activated state (brief flash)
    element.classList.add('activated');
    
    // Trigger action
    triggerAction(element.dataset.action);
    
    // Remove activated state after flash
    setTimeout(() => {
        element.classList.remove('activated');
    }, 200);
}
```

## Event Handling

### Mouse Events

```javascript
elements.forEach(element => {
    element.addEventListener('mouseenter', () => {
        // Enable interaction
        enableInteraction();
        
        // Start dwell
        startDwell(element);
    });
    
    element.addEventListener('mouseleave', () => {
        // Disable interaction
        disableInteraction();
        
        // Cancel dwell
        cancelDwell();
    });
    
    // Optional: Click as backup
    element.addEventListener('click', () => {
        if (Date.now() - lastActivationTime >= COOLDOWN_TIME) {
            activateElement(element);
        }
    });
});
```

## Cooldown System

### Purpose

Prevents rapid re-activation that could cause:
- Accidental double-triggers
- System overload
- User confusion

### Implementation

```javascript
const COOLDOWN_TIME = /* see electron-toolbar/modules/dwell/backend/dwell_constants.py — TOGGLE_COOLDOWN */;
let lastActivationTime = 0;

function canActivate() {
    const now = Date.now();
    return (now - lastActivationTime) >= COOLDOWN_TIME;
}

function activateElement(element) {
    if (!canActivate()) {
        console.log('Cooldown active, canceling activation');
        cancelDwell();
        return;
    }
    
    // ... activate ...
    
    // Record activation time
    lastActivationTime = Date.now();
}
```

### Cooldown Check Points

1. **Before starting dwell**: Prevents starting if recently activated
2. **Before activation**: Final check before triggering action

```javascript
function startDwell(element) {
    // Check cooldown before starting
    if (!canActivate()) {
        return;
    }
    // ... start dwell ...
}

function activateElement(element) {
    // Final cooldown check
    if (!canActivate()) {
        cancelDwell();
        return;
    }
    // ... activate ...
}
```

## Complete Template

```javascript
class DwellActivation {
    constructor(options = {}) {
        this.dwellTime = options.dwellTime || 600;      // ms
        this.cooldownTime = options.cooldownTime || 800; // ms
        this.updateInterval = options.updateInterval || 16; // ms
        
        this.dwellTimer = null;
        this.progressInterval = null;
        this.dwellStartTime = null;
        this.lastActivationTime = 0;
        this.currentElement = null;
    }
    
    setup(elements) {
        elements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                this.startDwell(element);
            });
            
            element.addEventListener('mouseleave', () => {
                this.cancelDwell();
            });
        });
    }
    
    startDwell(element) {
        const now = Date.now();
        
        // Check cooldown
        if (now - this.lastActivationTime < this.cooldownTime) {
            return;
        }
        
        // Don't restart if same element
        if (this.currentElement === element && this.dwellTimer) {
            return;
        }
        
        // Cancel existing
        this.cancelDwell();
        
        // Start new
        this.currentElement = element;
        this.dwellStartTime = now;
        element.classList.add('activating');
        
        // Start progress update
        this.startProgress(element);
        
        // Set activation timer
        this.dwellTimer = setTimeout(() => {
            this.activateElement(element);
        }, this.dwellTime);
    }
    
    cancelDwell() {
        if (this.dwellTimer) {
            clearTimeout(this.dwellTimer);
            this.dwellTimer = null;
        }
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
        if (this.currentElement) {
            this.currentElement.classList.remove('activating');
            this.resetProgress(this.currentElement);
            this.currentElement = null;
        }
        this.dwellStartTime = null;
    }
    
    startProgress(element) {
        const circle = element.querySelector('.progress-ring circle');
        if (!circle) return;
        
        circle.style.strokeDashoffset = '95'; // Reset
        
        this.progressInterval = setInterval(() => {
            const elapsed = Date.now() - this.dwellStartTime;
            const progress = Math.min(elapsed / this.dwellTime, 1);
            circle.style.strokeDashoffset = 95 - (progress * 95);
        }, this.updateInterval);
    }
    
    resetProgress(element) {
        const circle = element.querySelector('.progress-ring circle');
        if (circle) {
            circle.style.strokeDashoffset = '95';
        }
    }
    
    activateElement(element) {
        const now = Date.now();
        
        // Final cooldown check
        if (now - this.lastActivationTime < this.cooldownTime) {
            this.cancelDwell();
            return;
        }
        
        // Cancel dwell
        this.cancelDwell();
        
        // Visual feedback
        element.classList.remove('activating');
        element.classList.add('activated');
        this.resetProgress(element);
        
        // Trigger action
        const action = element.dataset.action;
        this.onActivate(action, element);
        
        // Record activation
        this.lastActivationTime = now;
        
        // Clear activated state
        setTimeout(() => {
            element.classList.remove('activated');
        }, 200);
    }
    
    onActivate(action, element) {
        // Override this method
        console.log('Activated:', action);
    }
}

// Usage
const dwell = new DwellActivation({
    dwellTime: 600,
    cooldownTime: 800
});

dwell.onActivate = (action, element) => {
    // Handle activation
    console.log('Action:', action);
};

dwell.setup(document.querySelectorAll('.dwell-element'));
```

## Timing Considerations

### Dwell Time

- **Fast (300-400ms)**: Quick activation, may cause accidental triggers
- **Medium (500-700ms)**: Good balance (recommended)
- **Slow (800-1000ms)**: Deliberate activation, may feel sluggish

### Cooldown Time

- **Short (400-600ms)**: Allows rapid actions, may cause double-triggers
- **Medium (700-900ms)**: Good balance (recommended)
- **Long (1000ms+)**: Prevents rapid actions, may feel unresponsive

### Update Interval

- **60fps (16ms)**: Smooth animation, higher CPU
- **30fps (33ms)**: Good balance
- **15fps (66ms)**: Lower CPU, less smooth

## Use Cases

1. **Toolbar Buttons**: Hover to activate controls
2. **Accessibility**: Alternative to clicking
3. **Touch Interfaces**: Dwell instead of tap
4. **Overlay Controls**: Non-intrusive activation

## Related Patterns

- See `toolbar-system.md` for complete toolbar implementation
- See `dwell-click.md` for click-based dwell
- See `click-through-windows.md` for window interaction
