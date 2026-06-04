# Refactoring Checklist

> Use this checklist when the user says "refactor", "clean up", "improve code quality", or similar.

## When to Use This

Trigger phrases:
- "Refactor this"
- "Clean up the code"
- "Check code quality"
- "Is there anything that needs refactoring?"
- "Review the code"

## Which Checklist to Use

| User Says | Use |
|-----------|-----|
| "Refactor", "Clean up", "Polish" | **Phases 0-4** (Standard refactoring) |
| "Final build", "Ready to ship", "Make it 9/10" | **Phase 6: Final Build** |
| "Prepare for production" | **Phases 0-4 + Phase 6** |

---

## Phase 0: Before Starting (Always Do First)

### Establish Baseline
- [ ] Run existing tests (note which pass/fail)
- [ ] Note current behavior (does it work?)
- [ ] Identify scope - what are we changing vs. NOT touching?

### Safety
- [ ] Create a branch or checkpoint (git commit before changes)
- [ ] Identify risky changes that could break things

### Scope Definition
```markdown
## Refactoring Scope
**In scope**: [files/functions to change]
**Out of scope**: [files/functions to NOT touch]
**Risk areas**: [changes that could break things]
```

---

## Phase 1: Quick Wins (Always Do)

### Dead Code Removal
- [ ] Delete unused imports
- [ ] Delete unused functions
- [ ] Delete unused variables
- [ ] Delete commented-out code (git has history)
- [ ] Delete empty files

### File Headers (Required for New Files)
- [ ] All new `.ts`/`.tsx` files must include standardized file headers
- [ ] Headers should follow project's CODING_STANDARDS.md format
- [ ] Headers must include: MODULE ROLE, WHY THIS FILE EXISTS, PUBLIC API, LAST VERIFIED date
- [ ] Check existing files for missing headers and add them if needed
- [ ] Headers help AI and developers quickly understand file purpose and structure

### Secrets Check
- [ ] No API keys hardcoded in source files
- [ ] No passwords or tokens in code
- [ ] No connection strings with credentials
- [ ] Secrets use environment variables or gitignored config files
- [ ] `.gitignore` includes `.env`, `*.pem`, `credentials.json`, etc.

### Magic Numbers → Constants
```python
# Before
if len(items) > 100:
    time.sleep(0.5)

# After
MAX_ITEMS = 100
RATE_LIMIT_DELAY = 0.5

if len(items) > MAX_ITEMS:
    time.sleep(RATE_LIMIT_DELAY)
```

### Naming Improvements
- [ ] Rename vague variables (`x`, `data`, `temp`, `result`)
- [ ] Rename functions that don't describe what they do
- [ ] Fix inconsistent naming (mixing `camelCase` and `snake_case`)

### Error Handling Consistency
- [ ] Fix mixed try/except styles (make consistent across module)
- [ ] Replace bare `except:` with specific exceptions
- [ ] Ensure error messages include context (not just "Error")

---

## Phase 2: Structure (Do If Time Permits)

### Split Large Files
For each file over 500 lines:
- [ ] Can constants be extracted to `*_constants.py`?
- [ ] Can state management be extracted to `*_state.py`?
- [ ] Can helper functions be extracted to `*_helpers.py`?
- [ ] Can the file be split by responsibility?

**Target**: 200-400 lines per file. **Max**: 800 lines.

### Extract Duplicates
Look for:
- [ ] Same code block appearing 2+ times → Extract to function
- [ ] Similar code with small variations → Extract with parameters
- [ ] Same pattern across files → Extract to shared module

### Simplify Functions
For each function over 30 lines:
- [ ] Can it be split into smaller functions?
- [ ] Are there deeply nested blocks that could use guard clauses?
- [ ] Is there a loop that could be its own function?

### Watch for Circular Imports
When splitting files, check:
- [ ] Does module A import from B, and B import from A? → Circular import
- [ ] Fix by: moving shared code to a third module, or using late imports

### Test Coverage
- [ ] Do existing tests still pass after changes?
- [ ] Did refactoring break any functionality?
- [ ] Are there new functions that need tests?

### Parameter Reduction
For functions with 4+ parameters:
```python
# Before
def create_window(x, y, width, height, title, color, alpha, topmost):

# After
@dataclass
class WindowConfig:
    x: int
    y: int
    width: int
    height: int
    title: str = "Window"
    color: str = "#333333"
    alpha: float = 1.0
    topmost: bool = True

def create_window(config: WindowConfig):
```

### Input Validation at Boundaries
Check that inputs are validated at system boundaries:
- [ ] API endpoints validate request body before processing
- [ ] Public functions validate parameters before use
- [ ] CLI scripts validate arguments before execution
- [ ] File/config loaders validate data after reading

### API Response Consistency
If the code has API endpoints:
- [ ] All endpoints return the same response shape (`{ success, error, data }`)
- [ ] Use a response helper function instead of raw `res.json()`
- [ ] Error responses always include `success: false` and `error` message
- [ ] Success responses always include `success: true`

```javascript
// Check: Is there a helper like this?
function apiResponse(res, { success, error = null, ...data }) {
  res.json({ success, error: success ? null : error, ...data });
}

// All endpoints should use it
apiResponse(res, { success: true, items: results });
apiResponse(res, { success: false, error: 'Something went wrong' });
```

```python
# Before - trusts input blindly
def process_class(drive, class_name):
    result = run_script(drive, class_name)  # What if class_name is None?

# After - validates at boundary
def process_class(drive: str, class_name: str) -> dict:
    if not class_name or not isinstance(class_name, str):
        return {"success": False, "error": "Class name is required"}
    if not class_name.strip():
        return {"success": False, "error": "Class name cannot be empty"}

    result = run_script(drive, class_name)
```

```javascript
// Before - trusts input blindly
app.post('/api/process', (req, res) => {
  const { className } = req.body;
  runScript(className);  // What if className is undefined?
});

// After - validates at boundary
app.post('/api/process', (req, res) => {
  const { className } = req.body;
  if (!className || typeof className !== 'string') {
    return res.json({ success: false, error: 'Class name is required' });
  }
  runScript(className);
});
```

---

## Phase 3: Patterns (Do If Significant)

### Check Against Existing Patterns
- [ ] Is there a pattern in `cursor-patterns/` that should be used?
- [ ] Is the code doing something a pattern already solves?
- [ ] Should this code become a new pattern?

### State Management
- [ ] Is state scattered across globals? → Consolidate into state class
- [ ] Are there race conditions? → Add threading locks
- [ ] Is state hard to track? → Consider state machine pattern

### Module Architecture Consistency
- [ ] Does each module have a `*_constants.py` file?
- [ ] Do modules with state use a state class (not raw globals)?
- [ ] Do modules use `shared/signals.py` for communication?
- [ ] Do modules follow the same structure/pattern?
- [ ] Is file-based IPC replaced with socket-based signals?

### Error Handling
- [ ] Are errors silently caught? → Log or handle properly
- [ ] Are bare `except:` clauses used? → Catch specific exceptions
- [ ] Are errors propagated correctly?

### Performance Check
- [ ] Did changes introduce new loops or repeated operations?
- [ ] Are there new blocking calls that could slow things down?
- [ ] Is there unnecessary work being done repeatedly?

---

## Phase 4: Documentation (Do If Needed)

### Missing Documentation
- [ ] Public functions without docstrings
- [ ] Complex logic without comments
- [ ] Non-obvious "why" decisions unexplained

### Outdated Documentation
- [ ] Comments that don't match code
- [ ] Docstrings with wrong parameter names
- [ ] README that doesn't reflect current state

### Breaking Changes
- [ ] Did any function signatures change? (parameters added/removed)
- [ ] Did any function names change?
- [ ] Document breaking changes for other code that calls these functions

---

## Phase 5: Verification (Always Do Last)

### Definition of "Done"
- [ ] All existing tests pass
- [ ] No new linting errors
- [ ] Code runs without errors
- [ ] Original functionality still works
- [ ] Type hints complete on changed functions
- [ ] Edge cases handled
- [ ] Error messages are helpful (include context)

---

## Refactoring Report Template

After refactoring, provide this summary:

```markdown
## Refactoring Summary

### Changes Made
- Removed X unused imports/functions
- Extracted Y duplicate code blocks into shared functions
- Renamed Z variables for clarity
- Simplified N functions using guard clauses

### Code Quality Before/After
- Functions over 50 lines: X → Y
- Duplicate code blocks: X → Y
- Magic numbers: X → Y
- Missing type hints: X → Y

### Remaining Tech Debt
- [List anything not fixed and why]

### New Patterns Created
- [If any code was generalized into a pattern]
```

---

## Quick Reference: What to Look For

| Category | Look For | Fix |
|----------|----------|-----|
| **Dead Code** | Unused imports, functions, variables | Delete |
| **Duplication** | Same code 2+ times | Extract function |
| **Complexity** | Functions > 50 lines | Split |
| **File Size** | Files > 800 lines | Split into multiple files |
| **Nesting** | 4+ indent levels | Guard clauses |
| **Magic Values** | Hardcoded numbers/strings | Extract to `*_constants.py` |
| **Raw Globals** | `global var` for state | Use state class with locking |
| **File IPC** | Polling text files | Use socket-based signals |
| **Naming** | Vague names (`x`, `data`, `tmp`) | Descriptive names |
| **Types** | Missing type hints | Add hints |
| **Errors** | Bare `except:`, silent failures | Specific handling |
| **Docs** | Missing docstrings | Add them |
| **Inconsistency** | Modules structured differently | Follow module template |
| **No Validation** | API/functions trust input blindly | Add validation at boundaries |
| **Hardcoded Secrets** | API keys, passwords in source | Move to env vars/config |
| **Inconsistent API** | Different response shapes per endpoint | Use response helper |
| **No Fallback** | External service with no backup plan | Add graceful degradation |

---

## Phase 6: Final Build (9/10 Quality)

> **When to use**: User says "final build", "ready to ship", "make it 9/10", or "prepare for production".
>
> This phase is separate from regular refactoring. Skip during rough draft and polish phases.

### Pre-Flight Check
- [ ] All standard refactoring (Phases 1-4) is complete
- [ ] Code is functional and tested manually
- [ ] No known bugs or broken features

---

### 6.1 Testing

#### Identify What Needs Tests
- [ ] List all complex functions with multiple branches
- [ ] List all public API functions other modules call
- [ ] List any edge cases discovered during development
- [ ] List any bugs that were fixed (each needs a regression test)

**Priority testing targets (if present):**
- Name matching / fuzzy matching logic
- Data parsing (CSV, JSON, file formats)
- Grade calculation / scoring logic
- File path resolution across platforms
- Any function with 3+ if/else branches

#### Create Test Files
```
# For each module with complex logic:
module_name/
├── module_name.py
└── test_module_name.py

# For TypeScript/React:
src/
├── services/
│   └── myService.ts
tests/
├── services/
│   └── myService.test.ts
```

#### Write Minimum Tests
For each complex function:
- [ ] Test the happy path (normal input → expected output)
- [ ] Test edge cases (empty input, null, boundary values)
- [ ] Test error cases (invalid input → graceful failure)

```python
# Example: Name matching function needs these tests
def test_match_exact_name(): ...
def test_match_hyphenated_name(): ...
def test_match_multi_word_name(): ...
def test_no_match_returns_none(): ...
def test_empty_roster_returns_none(): ...
```

#### Verify Tests Pass
- [ ] All new tests pass
- [ ] All existing tests still pass
- [ ] No tests are skipped or commented out

---

### 6.2 Environment Configuration

#### Find Hardcoded Values
Search for:
- [ ] `localhost:` URLs
- [ ] Absolute file paths (`C:\`, `/Users/`)
- [ ] API keys or tokens (should already be gone, but double-check)
- [ ] Port numbers

#### Extract to Config
```python
# Before
API_URL = "http://localhost:5000"
ROSTERS_PATH = "C:\\Rosters etc"

# After
import os
API_URL = os.environ.get("API_URL", "http://localhost:5000")
ROSTERS_PATH = os.environ.get("ROSTERS_PATH", "C:\\Rosters etc")
```

```typescript
// Before
const API_BASE_URL = 'http://localhost:5000/api';

// After
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
```

#### Create Environment Files
- [ ] Create `.env.example` (committed) with all required variables
- [ ] Ensure `.env` is in `.gitignore`
- [ ] Document any required environment variables in README

---

### 6.3 State Management (React)

#### Check Component Size
For each component over 300 lines:
- [ ] Count useState/useReducer calls
- [ ] If > 5 state variables, extract to custom hook

#### Extract State to Hook
```tsx
// Before: Option2.tsx has 15 useState calls and 500+ lines

// After: Create useQuizProcessor.ts
export function useQuizProcessor() {
  // All state and handlers here
  return { state, actions };
}

// Option2.tsx now just renders UI
function Option2() {
  const { state, actions } = useQuizProcessor();
  return (/* UI only */);
}
```

---

### 6.4 CLI Function Refactoring (Python)

#### Check CLI main() Length
For each Python CLI script (files ending in `_cli.py`):
- [ ] If `main()` is over 100 lines, extract logic into separate functions

#### Extract to Testable Functions
```python
# Before: main() does everything
def main():
    # 300+ lines of logic
    pass

# After: main() orchestrates, functions do work  
def find_files(folder: str) -> List[Path]:
    """Find files to process."""
    ...

def process_file(path: Path) -> Result:
    """Process a single file."""
    ...

def main():
    args = parse_args()
    files = find_files(args.folder)
    results = [process_file(f) for f in files]
    write_output(results)
```

#### Verification
- [ ] Each extracted function has a clear single responsibility
- [ ] Functions can be imported and tested independently
- [ ] main() is under 50 lines and only orchestrates

---

### 6.5 Documentation

#### Add Docstrings to Complex Functions
For each function identified in 6.1:
- [ ] Add docstring with description
- [ ] Document parameters and return value
- [ ] Add example if behavior is non-obvious

#### Add JSDoc to Service Functions
- [ ] Document all exported functions
- [ ] Include @param, @returns, @example

#### Update README
- [ ] Installation instructions are accurate
- [ ] Environment variables are documented
- [ ] Basic usage examples included

---

### 6.6 Error Handling

#### Add Error Boundaries (React)
- [ ] Create ErrorBoundary component
- [ ] Wrap main app component
- [ ] Add fallback UI for crashes

#### Improve Error Messages
For each error message:
- [ ] Does it explain what went wrong?
- [ ] Does it suggest how to fix it?
- [ ] Does it avoid exposing internals?

```python
# Bad
return {"error": "Failed"}

# Good
return {"error": "Could not find class folder. Check that the class name matches a folder in Rosters etc."}
```

---

### 6.7 API Consistency

#### Centralize All API Calls
- [ ] Search for direct `fetch()` calls outside service layer
- [ ] Move all API calls to service file
- [ ] Ensure all calls use the `apiCall()` helper

#### Verify Response Shape
- [ ] All endpoints return `{ success, error?, data? }`
- [ ] All error responses include helpful message
- [ ] All success responses include relevant data

---

### 6.8 Final Verification

#### Run Full Test Suite
```bash
# Python
pytest

# JavaScript/TypeScript
npm test
```

#### Manual Smoke Test
- [ ] App starts without errors
- [ ] Main workflow completes successfully
- [ ] Error cases show helpful messages
- [ ] No console errors in browser

#### Code Quality Check
- [ ] No TypeScript/ESLint errors
- [ ] No Python linting errors
- [ ] No unused imports or variables

---

### Final Build Report Template

After completing Phase 6, provide this summary:

```markdown
## Final Build Report

### Tests Added
- [ ] `test_module_name.py` - X tests for name matching
- [ ] `service.test.ts` - X tests for API service

### Environment Configuration
- [ ] Extracted X hardcoded values to environment variables
- [ ] Created `.env.example` with X variables

### State Management
- [ ] Extracted state from `ComponentName` to `useHookName`
- [ ] Reduced component from X lines to Y lines

### Documentation Added
- [ ] Docstrings on X functions
- [ ] JSDoc on X service functions
- [ ] Updated README with environment setup

### Error Handling
- [ ] Added ErrorBoundary component
- [ ] Improved X error messages

### API Consistency
- [ ] Moved X inline fetch calls to service layer
- [ ] All Y endpoints use consistent response shape

### Quality Score
Before: X/10
After: 9/10

### Remaining Items (if any)
- [List anything deferred and why]
```
