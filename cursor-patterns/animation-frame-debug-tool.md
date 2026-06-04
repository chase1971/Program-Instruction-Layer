# Animation Frame-by-Frame Debug Tool

> **Pattern for debugging overlay positioning and animations with pixel-perfect control**

## Overview

A React-based debugging tool for visualizing and fine-tuning animation states frame-by-frame. Especially useful for positioning overlays that need to align perfectly with underlying UI elements.

**Used in:**
- Fractions App: Sum overlay positioning (Parts 1, 2, 3)

**Key Features:**
- Manual step-through of animation states
- Real-time position adjustment with pixel precision
- Visual state display (what's showing, what's hidden)
- +1/-1 pixel nudge buttons
- Direct value input fields
- Position readout for communicating final values

---

## Problem This Solves

When animations involve overlays that morph or transition into other elements, you often can't tell if they're perfectly aligned until you see them side-by-side. Small pixel offsets cause "jerky" transitions where content appears to shift slightly.

**Without this tool:**
- Hard to see exact positioning during fast animations
- No way to measure pixel differences
- Trial-and-error with manual code changes
- Takes many compile cycles to get it right

**With this tool:**
- Freeze animation at any frame
- Toggle between frames to see differences
- Adjust position in real-time
- Get exact pixel values to update code

---

## Implementation

### Step 1: Add Debug State

Add a debug state that overrides your normal animation state when active:

```typescript
// In your main component
const [debugAnimState, setDebugAnimState] = useState<{
  overlayText: string | null;
  overlayNum: number | null;
  showOverlay: boolean;
  answerNum: number | null;
  popping: string[];
  stayZoomed: string[];
} | null>(null);
```

**Key principle:** When `debugAnimState !== null`, use it instead of the real animation state.

### Step 2: Modify Animation State Logic

Update your rendering logic to check debug state first:

```typescript
// Before (normal operation):
const answerNumSlot: NumberSlotState = {
  value: activePart === 1 ? part1.state.animState.answerNum : null,
  hidden: part1.state.animState.overlayText !== null,
  // ... other properties
};

// After (with debug override):
const answerNumSlot: NumberSlotState = {
  value: debugAnimState !== null ? debugAnimState.answerNum :
         activePart === 1 ? part1.state.animState.answerNum : null,
  hidden: debugAnimState !== null ? (debugAnimState.overlayText !== null) :
          part1.state.animState.overlayText !== null,
  // ... other properties
};
```

### Step 3: Add Position Control Hook

Use or create a position hook that exposes `setPosition`:

```typescript
const sumOverlay = useDraggablePosition(INITIAL_POSITION, containerRef);
// Provides: sumOverlay.position (current), sumOverlay.setPosition (updater)
```

### Step 4: Create Debug Panel UI

Add a debug control panel (example from Fractions App):

```tsx
{FRAME_BY_FRAME_DEBUG && (
  <div className="mt-2 bg-red-50 border-2 border-red-300 rounded-xl p-2 w-full max-w-[500px]">
    <div className="text-xs font-semibold text-red-800 mb-1">Frame-by-Frame Debug</div>
    
    {/* Show current state */}
    <div className="text-xs text-red-700 mb-2">
      Debug Mode: {debugAnimState !== null ? 'ON' : 'OFF'}
    </div>
    <div className="text-xs text-red-700 mb-2">
      <strong>Overlay Position:</strong> left: {sumOverlay.position.left}, top: {sumOverlay.position.top}
    </div>
    
    {/* Frame control buttons */}
    <div className="flex gap-1 flex-wrap">
      <button
        onClick={() => {
          setDebugAnimState({
            overlayText: '1 + 15',
            overlayNum: null,
            showOverlay: true,
            answerNum: null,
            popping: ['leftNum', 'rightNum'],
            stayZoomed: ['leftNum', 'rightNum'],
          });
        }}
        className="px-2 py-1 rounded bg-orange-600 text-white text-xs"
      >
        1. Show Overlay
      </button>
      <button
        onClick={() => {
          setDebugAnimState({
            overlayText: '1 + 15',
            overlayNum: 16,
            showOverlay: false,
            answerNum: null,
            popping: [],
            stayZoomed: [],
          });
        }}
        className="px-2 py-1 rounded bg-orange-600 text-xs"
      >
        2. Morph
      </button>
      <button
        onClick={() => {
          setDebugAnimState({
            overlayText: null,
            overlayNum: null,
            showOverlay: false,
            answerNum: 16,
            popping: [],
            stayZoomed: [],
          });
        }}
        className="px-2 py-1 rounded bg-orange-600 text-xs"
      >
        3. Final State
      </button>
    </div>
    
    {/* Position adjustment controls */}
    <div className="text-xs font-semibold text-red-800 mt-2">Adjust Position:</div>
    <div className="flex gap-2 items-center">
      <div className="flex flex-col gap-1">
        <div className="flex gap-1 items-center">
          <span className="text-xs text-red-800 w-12">Left:</span>
          <button
            onClick={() => sumOverlay.setPosition({ 
              ...sumOverlay.position, 
              left: sumOverlay.position.left - 1 
            })}
            className="px-1 py-0.5 rounded bg-blue-600 text-white text-xs"
          >
            -1
          </button>
          <input
            type="number"
            value={sumOverlay.position.left}
            onChange={(e) => sumOverlay.setPosition({ 
              ...sumOverlay.position, 
              left: parseInt(e.target.value) || 0 
            })}
            className="w-16 px-1 py-0.5 border rounded text-xs"
          />
          <button
            onClick={() => sumOverlay.setPosition({ 
              ...sumOverlay.position, 
              left: sumOverlay.position.left + 1 
            })}
            className="px-1 py-0.5 rounded bg-blue-600 text-white text-xs"
          >
            +1
          </button>
        </div>
        <div className="flex gap-1 items-center">
          <span className="text-xs text-red-800 w-12">Top:</span>
          <button
            onClick={() => sumOverlay.setPosition({ 
              ...sumOverlay.position, 
              top: sumOverlay.position.top - 1 
            })}
            className="px-1 py-0.5 rounded bg-blue-600 text-white text-xs"
          >
            -1
          </button>
          <input
            type="number"
            value={sumOverlay.position.top}
            onChange={(e) => sumOverlay.setPosition({ 
              ...sumOverlay.position, 
              top: parseInt(e.target.value) || 0 
            })}
            className="w-16 px-1 py-0.5 border rounded text-xs"
          />
          <button
            onClick={() => sumOverlay.setPosition({ 
              ...sumOverlay.position, 
              top: sumOverlay.position.top + 1 
            })}
            className="px-1 py-0.5 rounded bg-blue-600 text-white text-xs"
          >
            +1
          </button>
        </div>
      </div>
    </div>
    
    {/* Reset button */}
    <button
      onClick={() => {
        setDebugAnimState(null);
        // Reset to initial state
      }}
      className="mt-2 px-2 py-1 rounded bg-red-600 text-white text-xs"
    >
      Reset & Exit Debug
    </button>
  </div>
)}
```

### Step 5: Add Debug Toggle Flag

Add a constant at the top of your file to easily enable/disable:

```typescript
/** When true, show frame-by-frame animation debug controls. Set false when done. */
const FRAME_BY_FRAME_DEBUG = true;
```

---

## Usage Workflow

### Step 1: Enable Debug Mode

Set the debug flag to `true`:

```typescript
const FRAME_BY_FRAME_DEBUG = true;
```

### Step 2: Navigate to Animation

Load your app and navigate to the screen with the animation you want to debug.

### Step 3: Step Through Frames

Use the frame control buttons to step through the animation:

1. Click "1. Show Overlay" - See the overlay in its initial state
2. Click "2. Morph" - See the transition state
3. Click "3. Final State" - See where the content ends up

Toggle between frames to spot positioning differences.

### Step 4: Adjust Position

If frames don't align:

1. Go to the frame that looks wrong
2. Use the +1/-1 buttons to nudge the position
3. Or type exact values in the input fields
4. Toggle between frames to verify alignment

### Step 5: Note Final Values

When the position is perfect, note the values shown in the debug panel:

```
Overlay Position: left: 115, top: 118
```

### Step 6: Update Constants

Update your position constant in the code:

```typescript
const SUM_OVERLAY_INITIAL_POSITION = { left: 115, top: 118 };
```

### Step 7: Disable Debug Mode

Turn off the debug flag:

```typescript
const FRAME_BY_FRAME_DEBUG = false;
```

---

## Key Design Decisions

### 1. Debug State Overrides Real State

**Why:** Allows you to freeze and manipulate state without interfering with the actual animation logic.

**How:** Check `debugAnimState !== null` first, then fall back to real state:

```typescript
value: debugAnimState !== null ? debugAnimState.value : realState.value
```

### 2. Position Hook with Setters

**Why:** Need to adjust position dynamically without recompiling.

**How:** Use a hook that returns both current position and a setter:

```typescript
const overlay = usePosition(initialPos);
overlay.position.left; // Current value
overlay.setPosition({ left: 120, top: 100 }); // Update
```

### 3. Pixel Nudge Buttons

**Why:** Hard to see small differences (1-2px), so need precise control.

**How:** Simple increment/decrement buttons:

```typescript
onClick={() => setPosition({ ...pos, left: pos.left - 1 })}
```

### 4. Real-time Visual Feedback

**Why:** Need to see changes immediately without page refresh.

**How:** All adjustments update React state, triggering immediate re-render.

### 5. State Display Panel

**Why:** Need to verify what's showing/hidden without inspecting code.

**How:** Display current values from debug state:

```tsx
<div>OverlayText: "{debugAnimState.overlayText}"</div>
<div>ShowOverlay: {debugAnimState.showOverlay ? 'Yes' : 'No'}</div>
```

---

## Variations

### For Draggable Overlays

If you already have draggable overlays for positioning, the debug tool complements them:

- **Draggable:** Use for rough positioning
- **Debug Tool:** Use for final pixel-perfect alignment

### For Multi-Element Animations

If your animation involves multiple moving parts:

1. Add more frame buttons for each significant state
2. Add position controls for each element
3. Display all element positions in the debug panel

### For Color/Opacity Transitions

The same pattern works for any animation property:

```typescript
const [debugAnimState, setDebugAnimState] = useState<{
  opacity: number;
  color: string;
  scale: number;
} | null>(null);
```

Then add sliders or input fields for each property.

---

## Real-World Example: Fractions App

**Problem:** Sum overlay "1 + 15" needs to morph into "16" in the answer slot. The "16" was shifting 2-3 pixels when transitioning, causing a jerky appearance.

**Solution:**

1. Added debug panel with 3 frames:
   - Frame 1: Show "1 + 15" overlay
   - Frame 2: Morph to "16" (still in overlay)
   - Frame 3: Move to answer slot

2. Toggled between Frame 2 and Frame 3 to see the shift

3. Used +1/-1 buttons to adjust overlay position

4. Found perfect position: `left: 115, top: 118` (was `left: 119, top: 114`)

5. Updated constant and disabled debug mode

**Result:** Seamless transition with no visible shift.

---

## Tips & Best Practices

### 1. Screenshot Frames for Comparison

Take screenshots of each frame and overlay them in an image editor to see pixel differences.

### 2. Use Browser DevTools

Right-click the overlay and "Inspect Element" to see actual pixel positions in the DOM.

### 3. Test at Target Resolution

Always test at the resolution your app will run at. Positions can vary based on screen size if your container is responsive.

### 4. Document Final Values

Add comments near the position constant explaining how it was determined:

```typescript
/** 
 * Position: left: 115, top: 118
 * Determined using frame-by-frame debug tool at 390px container width.
 * Aligns overlay "16" with answer numerator slot.
 */
const SUM_OVERLAY_INITIAL_POSITION = { left: 115, top: 118 };
```

### 5. Version Control the Debug Code

Keep the debug panel code in your repo (just disabled). You'll likely need to adjust positions again if you:
- Change font sizes
- Modify container sizes
- Add padding/margins
- Change the content

---

## Checklist for Implementation

- [ ] Add debug state variable
- [ ] Add debug override logic to all affected render paths
- [ ] Create position control hook (or use existing draggable hook)
- [ ] Add debug panel UI with frame buttons
- [ ] Add position adjustment controls (+1/-1 and input fields)
- [ ] Add state display to show what's visible/hidden
- [ ] Add toggle flag constant
- [ ] Test each frame button
- [ ] Test position adjustments
- [ ] Document the tool's location in your codebase

---

## Common Issues

### Issue: Buttons Don't Work

**Cause:** Trying to mutate state directly instead of using setState.

**Fix:** Always use setState:

```typescript
// Bad
debugAnimState.value = 16;

// Good
setDebugAnimState({ ...debugAnimState, value: 16 });
```

### Issue: Position Reverts After Adjustment

**Cause:** Position is controlled by a constant, not the hook's state.

**Fix:** Make sure the overlay uses the hook's position:

```typescript
// Bad
left: CONSTANT_POSITION.left

// Good
left: overlay.position.left
```

### Issue: Can't See Small Differences

**Cause:** Content is moving too fast during transition.

**Fix:** That's exactly what this tool solves! Use frame buttons to freeze at each state.

---

## Future Enhancements

Ideas for extending this pattern:

1. **Animation Speed Control:** Add a slider to slow down animations
2. **Multi-Element Tracking:** Show positions of all animated elements simultaneously
3. **Onion Skinning:** Overlay multiple frames with transparency to see motion paths
4. **Position History:** Track all position adjustments to see what you tried
5. **Export/Import:** Save/load position configurations as JSON
6. **Comparison Mode:** Split-screen showing before/after side-by-side

---

*Created: 2026-02-14*  
*Status: Production-ready*  
*Used in: Fractions App (Part 1, 2, 3 sum overlays)*
