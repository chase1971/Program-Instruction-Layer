# Overlay Exclusion Zones Pattern

> ⚠️ **STATUS: DESIGN SKETCH — NOT IMPLEMENTED (verified 2026-07-31).**
> The dwell backend contains no exclusion-zone code: there is no `exclusion` or
> `tabletop` reference anywhere in `modules/dwell/backend/*.py`. The
> "Used in: Dwell module (excludes tabletop overlays)" claim in
> `README.md` is stale.
>
> **If you need dwell suppressed over a region or app, do not build from this
> file.** Add a **new pause reason** modeled on `dwell_scroll_zone_pause.py` —
> that is the mechanism the dwell backend actually uses (see also
> `dwell_typing_pause.py` and the pause-reason audit in `dwell_pause_audit.py`).
> Keeping one pause mechanism matters: leaving a zone must only unpause when
> *that* reason caused the pause, which the existing pattern already handles.

## Overview

A pattern for preventing dwell/hover actions from triggering when the cursor is over overlay UI elements like drag handles, close buttons, or other interactive controls. This ensures that interacting with overlay controls doesn't accidentally trigger the overlay's main functionality.

## Problem

When you have overlays that respond to hover/dwell (like dwell-click or dwell-drag), the overlay's own UI elements (drag handles, close buttons, mode toggles) can accidentally trigger those actions. For example:
- Hovering over a drag handle to reposition an overlay triggers a dwell-click
- Moving cursor over a close button starts a drag countdown

## Solution

Define exclusion zones based on overlay positions and dimensions. Before triggering any dwell action, check if the cursor is within an exclusion zone.

## Implementation Structure

### 1. Define Overlay Dimensions (Constants)

```python
# In *_constants.py
WINDOW_WIDTH = 280   # Overlay width in pixels
WINDOW_HEIGHT = 70   # Overlay height in pixels
```

### 2. Store Overlay Positions (JSON)

```python
# Position file path
POSITION_FILE = Path(__file__).parent / "overlay_position.json"

# Save position when overlay moves
def save_position(x: int, y: int) -> None:
    with open(POSITION_FILE, 'w') as f:
        json.dump({"x": x, "y": y}, f)

# Position file format:
# {"x": -1444, "y": 1120}
```

### 3. Exclusion Zone Check Function

```python
import json
from pathlib import Path
from typing import Tuple

# Overlay dimensions (from constants)
OVERLAY_WIDTH = 280
OVERLAY_HEIGHT = 70

def is_over_exclusion_zone(pos: Tuple[int, int]) -> bool:
    """
    Check if position is over any overlay that should be excluded.
    
    Args:
        pos: (x, y) tuple of cursor position
        
    Returns:
        True if cursor is over an exclusion zone (don't trigger action)
        False if cursor is safe to trigger action
    """
    try:
        module_dir = Path(__file__).parent
        
        # List all overlay position files to check
        position_files = [
            module_dir / "overlay1_position.json",
            module_dir / "overlay2_position.json",
            # Add more as needed
        ]
        
        for pos_file in position_files:
            if pos_file.exists():
                try:
                    with open(pos_file, 'r') as f:
                        overlay_pos = json.load(f)
                    
                    ox = overlay_pos.get("x", 0)
                    oy = overlay_pos.get("y", 0)
                    
                    # Check if cursor is within overlay bounds
                    if (ox <= pos[0] <= ox + OVERLAY_WIDTH and
                        oy <= pos[1] <= oy + OVERLAY_HEIGHT):
                        return True
                        
                except (json.JSONDecodeError, KeyError):
                    pass
        
        return False
        
    except Exception:
        return False  # Fail safe - allow action if check fails
```

### 4. Integration Points

Add the check before triggering any dwell action:

```python
# Mode 1 (Click) - before starting dwell timer
def handle_dwell_click(current_position):
    # Skip if over exclusion zone
    if is_over_exclusion_zone(current_position):
        return
    
    # ... rest of dwell click logic

# Mode 2 (Drag) - before starting countdown
def handle_drag_countdown(current_position):
    # Skip if over exclusion zone
    if is_over_exclusion_zone(current_position):
        return
    
    # ... rest of countdown logic
```

## Complete Example

From `dwell_module.py`:

```python
# Constants for overlay dimensions
TABLETOP_WINDOW_WIDTH = 280
TABLETOP_WINDOW_HEIGHT = 70

def is_over_tabletop_overlay(pos: Tuple[int, int]) -> bool:
    """Check if position is over a tabletop overlay (drag or right)."""
    try:
        module_dir = Path(__file__).parent
        position_files = [
            module_dir / "tabletop_drag_position.json",
            module_dir / "tabletop_right_position.json"
        ]
        
        for pos_file in position_files:
            if pos_file.exists():
                try:
                    with open(pos_file, 'r') as f:
                        overlay_pos = json.load(f)
                    
                    ox = overlay_pos.get("x", 0)
                    oy = overlay_pos.get("y", 0)
                    
                    if (ox <= pos[0] <= ox + TABLETOP_WINDOW_WIDTH and
                        oy <= pos[1] <= oy + TABLETOP_WINDOW_HEIGHT):
                        return True
                except (json.JSONDecodeError, KeyError):
                    pass
        
        return False
    except Exception:
        return False


def _handle_mode1(current_position, current_time):
    """Handle Mode 1 (click) logic"""
    # ... other checks ...
    
    # Skip if over tabletop overlay
    if is_over_tabletop_overlay(current_position):
        time.sleep(SLEEP_MAIN_LOOP)
        return
    
    # ... rest of click logic


def _handle_mode2_idle(current_position, current_time):
    """Handle IDLE state in Mode 2"""
    # ... other checks ...
    
    # Skip if over tabletop overlay
    if is_over_tabletop_overlay(current_position):
        time.sleep(SLEEP_MODE2_LOOP)
        return
    
    # ... rest of idle logic
```

## When to Use

Use this pattern when:
- You have hover/dwell-based actions
- You have overlay windows with interactive UI elements
- The overlay's UI elements shouldn't trigger the dwell actions

## Key Design Decisions

1. **Read from JSON files**: Positions are persisted, so reading from files works even across module restarts
2. **Fail-safe behavior**: If the check fails, return False (allow action) to avoid blocking functionality
3. **Check at action trigger point**: Don't check continuously, only when about to trigger an action
4. **Use overlay bounds, not just center**: Full rectangle check ensures entire overlay is excluded

## Variations

### Exclude Only Specific Regions (Drag Handle Only)

```python
DRAG_HANDLE_WIDTH = 40  # Only exclude the drag handle area

def is_over_drag_handle(pos, overlay_pos):
    # Drag handle is on the right side of overlay
    handle_x = overlay_pos["x"] + OVERLAY_WIDTH - DRAG_HANDLE_WIDTH
    return (handle_x <= pos[0] <= overlay_pos["x"] + OVERLAY_WIDTH and
            overlay_pos["y"] <= pos[1] <= overlay_pos["y"] + OVERLAY_HEIGHT)
```

### Dynamic Exclusion (Overlay Visibility)

```python
# Only exclude if overlay is currently visible
exclusion_zones_active = {
    "drag_overlay": False,
    "right_overlay": False
}

def is_over_active_exclusion_zone(pos):
    for zone_name, is_active in exclusion_zones_active.items():
        if is_active and is_in_zone(pos, zone_name):
            return True
    return False
```

## Related Patterns

- See `click-through-windows.md` for making overlays click-through
- See `dwell-activation.md` for dwell-based activation
- See `window-positioning.md` for overlay position management
