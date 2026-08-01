# React-Specific Patterns

> **Purpose:** Patterns for React/TypeScript applications including hooks, state management, and component organization
>
> **When to Use:** All React projects, especially those using TypeScript

---

## Custom Hooks Pattern

### When to Extract a Custom Hook

Create a custom hook when you have:

| Condition | Example | Action |
|-----------|---------|--------|
| **3+ related useState calls** | `useState` for modal, loading, error states | Extract to `useModalState` |
| **State used across components** | Authentication state needed everywhere | Extract to `useAuth` |
| **Complex initialization** | Fetch data, calculate defaults, setup listeners | Extract to `useDataInit` |
| **State + computed values** | State with derived calculations | Extract to custom hook |
| **State + helper functions** | State with actions that modify it | Extract to custom hook |

### Hook Naming Convention

```typescript
// Pattern: use + PascalCase + descriptive name

// ✅ State management hooks
useModalState.ts          // Manages modal visibility state
useCalendarData.ts        // Manages calendar content state
useClassManagement.ts     // Manages class operations

// ✅ Handler orchestrators (coordinate multiple services)
useAddClassHandlers.ts    // Orchestrates add class workflow
useImportHandlers.ts      // Orchestrates import workflow
useTemplateHandlers.ts    // Orchestrates template operations

// ✅ Effect hooks (encapsulate side effects)
useAppEffects.ts          // Window listeners, server checks
useSemesterEffects.ts     // Semester change side effects
```

### Custom Hook Structure Template

```typescript
/*
===============================================================================
FILE: use[Name].ts

MODULE ROLE:
[What state/logic does this hook manage?]

WHY THIS FILE EXISTS:
Extracted to reduce [ComponentName] complexity / Reused across [Component1, Component2]

PUBLIC API (STABLE):
- use[Name](): [Name]State - Returns state and actions

LAST VERIFIED: [YYYY-MM-DD]
===============================================================================
*/

import { useState, useCallback } from 'react';

// Export interface for type safety
export interface [Name]State {
  // State values (read-only from consumer perspective)
  value: string;
  isLoading: boolean;
  error: string | null;
  
  // Actions (functions that modify state)
  setValue: (val: string) => void;
  setLoading: (loading: boolean) => void;
  clearError: () => void;
  
  // Computed values (if needed)
  hasError: boolean;
  
  // Helper functions
  reset: () => void;
}

/**
 * Custom hook to manage [description]
 * 
 * Consolidates [number] state variables and [number] functions
 * 
 * @returns State and actions for [feature]
 */
export function use[Name](): [Name]State {
  const [value, setValue] = useState('');
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Use useCallback for functions to prevent unnecessary re-renders
  const clearError = useCallback(() => {
    setError(null);
  }, []);
  
  const reset = useCallback(() => {
    setValue('');
    setLoading(false);
    setError(null);
  }, []);
  
  // Computed values
  const hasError = error !== null;
  
  return {
    // State
    value,
    isLoading,
    error,
    
    // Actions
    setValue,
    setLoading,
    clearError,
    
    // Computed
    hasError,
    
    // Helpers
    reset
  };
}
```

---

## Service Layer Pattern

### Why Service Layer?

All API calls MUST go through a service layer for:
- **Centralized error handling**
- **Consistent request/response patterns**
- **Easier testing** (mock the service, not fetch)
- **Type safety** for API contracts
- **Reusability** across components

### Service File Structure

```typescript
/*
===============================================================================
FILE: [name]Service.ts

MODULE ROLE:
Service layer for [feature] API calls

PUBLIC API (STABLE):
- fetch[Resource](): Promise<[Resource][]>
- save[Resource](data): Promise<ApiResponse>
- delete[Resource](id): Promise<ApiResponse>

SIDE EFFECTS:
- Makes HTTP requests to backend API
- May update localStorage for caching

LAST VERIFIED: [YYYY-MM-DD]
===============================================================================
*/

// API Response type (consistent across all services)
export interface ApiResponse<T = any> {
  success: boolean;
  error?: string;
  data?: T;
  logs?: string[];
}

// Resource-specific types
export interface MyResource {
  id: string;
  name: string;
  // ... other fields
}

/**
 * Fetch all resources from API
 */
export async function fetchResources(): Promise<ApiResponse<MyResource[]>> {
  try {
    const response = await fetch('/api/resources');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('[Service] Fetch failed:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

/**
 * Save resource to API
 */
export async function saveResource(resource: MyResource): Promise<ApiResponse> {
  try {
    const response = await fetch('/api/resources', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(resource)
    });
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('[Service] Save failed:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to save'
    };
  }
}
```

### Using Services in Components

```typescript
// ❌ WRONG - Direct fetch in component
const MyComponent = () => {
  const handleSave = async () => {
    const response = await fetch('/api/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    if (!result.success) {
      setError(result.error);
    }
  };
  
  return <button onClick={handleSave}>Save</button>;
};

// ✅ CORRECT - Use service layer
import { saveResource } from '../services/resourceService';

const MyComponent = () => {
  const handleSave = async () => {
    const result = await saveResource(data);
    if (!result.success) {
      setError(result.error);
    }
  };
  
  return <button onClick={handleSave}>Save</button>;
};
```

---

## State Management Extraction

### When to Extract State

Extract state to custom hook if **ANY** of these are true:

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Component size | > 300 lines | Extract state to hook |
| useState calls | 5+ in one component | Extract to hook |
| State duplication | Used in 2+ components | Extract to shared hook |
| Complex state + complex UI | Both present | Extract state to hook |

### Before/After Example

```typescript
// ❌ BEFORE: Component with too much state (450 lines)
export default function MyComponent() {
  // 12 useState calls
  const [value1, setValue1] = useState('');
  const [value2, setValue2] = useState(false);
  const [value3, setValue3] = useState<string[]>([]);
  const [value4, setValue4] = useState<Record<string, any>>({});
  const [value5, setValue5] = useState(0);
  const [value6, setValue6] = useState<Date | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [modal1Open, setModal1Open] = useState(false);
  const [modal2Open, setModal2Open] = useState(false);
  const [modal3Open, setModal3Open] = useState(false);
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  
  // 20+ helper functions
  const handleAction1 = () => { /* ... */ };
  const handleAction2 = () => { /* ... */ };
  // ... etc
  
  // 350 more lines of JSX and logic
  return (
    <div>{/* massive UI */}</div>
  );
}

// ✅ AFTER: Extracted to hook (now 150 lines each)
// hooks/useMyComponentState.ts
export function useMyComponentState() {
  const [value1, setValue1] = useState('');
  // ... all 12 state variables
  
  const handleAction1 = useCallback(() => { /* ... */ }, []);
  // ... all helper functions
  
  return {
    // Organized state
    values: { value1, value2, value3, value4, value5, value6 },
    ui: { loading, error },
    modals: { modal1Open, modal2Open, modal3Open },
    selected: { selectedItem },
    
    // Actions
    setValue1,
    // ... other setters
    
    // Helpers
    handleAction1,
    handleAction2
  };
}

// Component now just handles UI (150 lines)
export default function MyComponent() {
  const {
    values,
    ui,
    modals,
    selected,
    setValue1,
    handleAction1,
    handleAction2
  } = useMyComponentState();
  
  // Just UI rendering
  return (
    <div>{/* clean UI code */}</div>
  );
}
```

---

## Import Organization

### Standard Import Order

```typescript
// 1. React core (always first)
import React, { useState, useEffect, useRef, useCallback } from 'react';

// 2. Third-party UI libraries (alphabetical)
import { Button } from '@radix-ui/react-button';
import { Dialog } from '@radix-ui/react-dialog';
import { Moon, Sun, Settings } from 'lucide-react';

// 3. Internal utilities (from furthest to closest)
import { API_BASE_URL } from '../config';
import { logger } from '../utils/logger';
import { soundEffects } from '../utils/sounds';

// 4. Internal services (alphabetical)
import { saveCalendarData } from '../services/calendarService';
import { exportData } from '../services/exportService';

// 5. Internal hooks (alphabetical)
import { useAppState } from '../hooks/useAppState';
import { useModalState } from '../hooks/useModalState';

// 6. Internal components (alphabetical)
import { Calendar } from './Calendar';
import { Sidebar } from './Sidebar';

// 7. Types (if not inline with imports)
import type { CalendarMode, SemesterInfo } from '../types/calendar';

// 8. Styles (always last)
import './MyComponent.css';
```

---

## Component Organization Pattern

### File Structure

```
src/
├── api/              # Backend communication (service layer)
│   └── calendar.ts
├── components/
│   ├── modals/       # Modal dialogs
│   ├── wizards/      # Multi-step wizards
│   ├── shared/       # Reusable UI components
│   └── portals/      # Portal layer components
├── data/             # Static data, constants, themes
├── handlers/         # Handler orchestrators (complex workflows)
│   └── useAddClassHandlers.ts
├── hooks/            # Custom React hooks (state management)
│   └── useModalState.ts
├── services/         # Business logic, API calls
│   └── classOperations.ts
├── types/            # TypeScript type definitions
│   └── calendar.ts
├── utils/            # Pure utility functions
│   └── dateUtils.ts
└── main.tsx          # Entry point
```

### When to Create New Files

```typescript
// Question: Should I create a new file?

// Is it a modal/dialog?
//   → Yes: components/modals/MyModal.tsx
//   → No: Continue

// Is it state management?
//   → Yes: hooks/useMyState.ts
//   → No: Continue

// Is it a pure function (no hooks/state)?
//   → Yes: utils/myUtils.ts
//   → No: Continue

// Is it API/business logic?
//   → Yes: services/myService.ts
//   → No: Continue

// Is it a multi-step wizard?
//   → Yes: components/wizards/MyWizard.tsx
//   → No: Keep in current component
```

---

## Common Anti-Patterns

### ❌ Inline API Calls
```typescript
// WRONG
const MyComponent = () => {
  const handleClick = async () => {
    await fetch('/api/data', { method: 'POST', ... });
  };
};
```

### ✅ Service Layer
```typescript
// CORRECT
import { saveData } from '../services/dataService';

const MyComponent = () => {
  const handleClick = async () => {
    await saveData(myData);
  };
};
```

### ❌ Too Much State in Component
```typescript
// WRONG - 10+ useState in component
const MyComponent = () => {
  const [state1, setState1] = useState();
  const [state2, setState2] = useState();
  // ... 8 more
};
```

### ✅ Extracted to Hook
```typescript
// CORRECT
const MyComponent = () => {
  const { state, actions } = useMyComponentState();
};
```

### ❌ Prop Drilling
```typescript
// WRONG - passing props through 3+ levels
<Parent>
  <Child value={x} onChange={y}>
    <GrandChild value={x} onChange={y}>
      <GreatGrandChild value={x} onChange={y} />
    </GrandChild>
  </Child>
</Parent>
```

### ✅ Context or Custom Hook
```typescript
// CORRECT - Context for global state
const MyContext = createContext();

// Or custom hook for shared logic
const { value, onChange } = useSharedState();
```

---

## Testing Patterns

### Testing Custom Hooks

```typescript
// hooks/__tests__/useModalState.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useModalState } from '../useModalState';

describe('useModalState', () => {
  it('should initialize with all modals closed', () => {
    const { result } = renderHook(() => useModalState());
    
    expect(result.current.settingsOpen).toBe(false);
    expect(result.current.editOpen).toBe(false);
  });
  
  it('should open and close modals', () => {
    const { result } = renderHook(() => useModalState());
    
    act(() => {
      result.current.setSettingsOpen(true);
    });
    
    expect(result.current.settingsOpen).toBe(true);
    
    act(() => {
      result.current.closeAllModals();
    });
    
    expect(result.current.settingsOpen).toBe(false);
  });
});
```

### Testing Services

```typescript
// services/__tests__/dataService.test.ts
import { saveData } from '../dataService';

// Mock fetch
global.fetch = jest.fn();

describe('dataService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('should return success on successful save', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true })
    });
    
    const result = await saveData({ id: '1', name: 'Test' });
    
    expect(result.success).toBe(true);
    expect(fetch).toHaveBeenCalledWith('/api/data', expect.any(Object));
  });
  
  it('should handle errors gracefully', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));
    
    const result = await saveData({ id: '1', name: 'Test' });
    
    expect(result.success).toBe(false);
    expect(result.error).toContain('Network error');
  });
});
```

---

## Modal/Dialog Pattern

### Critical: Modal Sizing

**⚠️ COMMON MISTAKE:** Modals often span the entire screen width when created.

**✅ FIX:** Always use `max-w-md` (448px) for standard modals, `max-w-lg` (512px) for wide modals.

```tsx
// ✅ CORRECT - Standard modal size
<div className="w-full max-w-md max-h-[85vh] rounded-lg border shadow-xl">
  {/* Modal content */}
</div>

// ❌ WRONG - Spans full width
<div className="w-full max-w-4xl">  {/* Too wide! */}
<div className="w-full">  {/* No constraint! */}
```

**See:** [Modal Pattern](./modal-pattern.md) for complete modal guidelines.

---

## Related Patterns

- [File Headers](./file-headers.md) - Standardized documentation
- [Coding Standards](./CODING_STANDARDS.md) - General code quality
- [Refactoring Checklist](./refactoring-checklist.md) - When to refactor
- [Modal Pattern](./modal-pattern.md) - Modal/dialog sizing and structure

---

**Last Updated:** 2026-01-12
