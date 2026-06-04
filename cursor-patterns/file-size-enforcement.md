# File Size Enforcement Rules

> **Purpose:** Prevent file bloat - the #1 most violated rule in AI-assisted coding
>
> **When to Use:** Add to `.cursorrules` in every project
>
> **Priority:** CRITICAL - This rule is violated more than any other

---

## 🚨 The Problem

AI assistants naturally want to:
- ✅ Be helpful and complete
- ✅ Give you working code immediately
- ✅ Add features inline for convenience

This leads to:
- ❌ Files growing to 1000+ lines
- ❌ Monolithic components that are hard to maintain
- ❌ Code that should be extracted staying inline
- ❌ Violation of the 800-line limit

**Solution:** Force AI to check size BEFORE coding, not after.

---

## 📋 Complete Rule Text (Copy to .cursorrules)

```markdown
────────────────────────────────
🚨 FILE SIZE ENFORCEMENT (CRITICAL)
────────────────────────────────

**THIS IS THE MOST VIOLATED RULE. FOLLOW IT STRICTLY.**

BEFORE adding ANY code to ANY file, AI MUST:

1. **CHECK FILE SIZE FIRST**
   - Read the target file
   - Report current line count: "File X is currently Y lines"
   - If file size is unknown, estimate based on file read

2. **EVALUATE IMPACT BEFORE CODING**
   - Estimate how many lines will be added
   - Calculate final size: "Adding ~Z lines → file will be ~(Y+Z) lines"
   - Check against limits below

3. **MANDATORY APPROVAL REQUIRED IF:**
   - File is > 500 lines AND adding > 50 lines
   - File would exceed 800 lines (HARD LIMIT)
   - Adding a modal/dialog/form (> 100 lines typically)
   - Adding a major feature (> 150 lines typically)
   
   **STOP. DO NOT CODE. ASK USER:**
   "File X is Y lines. Adding this would make it ~Z lines. Should I:
   a) Extract to separate component/file?
   b) Proceed with inline addition?
   c) Something else?"

4. **MANDATORY EXTRACTION REQUIRED IF:**
   - File is > 700 lines (extract immediately, no questions)
   - Addition is > 100 lines (extract, no questions)
   - Adding reusable component (modal, form, wizard)
   - File would exceed 800 lines (extract, no questions)

   **STOP. DO NOT CODE. PROPOSE EXTRACTION:**
   "File X is Y lines. This addition requires extraction to maintain file size limits.
   Proposed: Create [new file path] with [description].
   Proceed with extraction?"

5. **FILE SIZE LIMITS (HARD RULES):**
   - **Max 800 lines** - NO EXCEPTIONS
   - **Warning at 500 lines** - Ask before adding > 50 lines
   - **Extract at 700 lines** - No new additions without extraction
   - **React Components:** Extract state to hook if > 300 lines with 5+ useState

6. **VIOLATION CONSEQUENCES:**
   If AI adds code that:
   - Makes file exceed 800 lines without asking → USER WILL REJECT
   - Adds 100+ lines inline without proposing extraction → USER WILL REJECT
   - Adds modal/dialog inline when file is > 500 lines → USER WILL REJECT
   - Ignores this section entirely → USER WILL REJECT

   **When user says "This violates file size rules":**
   - Apologize immediately
   - Acknowledge the violation
   - Extract to separate file with proper header (file-headers.md)
   - Update imports
   - Report: "Extracted X lines to [new file]. File Y is now Z lines."

7. **EXTRACTION PATTERNS:**
   - Modal/Dialog → `components/modals/[Name]Modal.tsx` (see [Modal Pattern](./modal-pattern.md) for sizing guidelines)
   - Form → `components/forms/[Name]Form.tsx` or `components/[Name]Form.tsx`
   - Complex UI block → `components/shared/[Name].tsx`
   - State logic → `hooks/use[Name].ts`
   - Business logic → `services/[name]Service.ts`
   - Pure utilities → `utils/[name]Utils.ts`
   
   **⚠️ MODAL SIZING:** When creating modals, always use `max-w-md` (448px), NOT `max-w-3xl` or larger. See [Modal Pattern](./modal-pattern.md) for details.

8. **SESSION CHECK-IN (Every 30 minutes):**
   If working for > 30 minutes, proactively report:
   - "Session check: Files modified this session:"
   - List each file with current line count
   - Flag any files > 700 lines or that grew by > 200 lines
   - Propose extractions if needed

**REMEMBER:**
- File size rules apply to EVERY code addition
- "Just this once" is NOT an exception
- "It's only 20 lines" still counts if file is at 780 lines
- Better to ask and extract than violate and get rejected
- User will catch violations - don't make them catch you
```

---

## 🎯 Quick Reference Card

### Before Adding Code

```
1. Read file → Get line count
2. Estimate addition size
3. Calculate: current + addition = final size
4. Check limits:
   - > 800 lines? → STOP, extract required
   - > 700 lines? → STOP, extract required
   - > 500 lines + > 50 lines? → ASK user
   - > 100 lines addition? → STOP, extract required
5. If approved, code. If not, propose extraction.
```

### Extraction Triggers

| Condition | Action |
|-----------|--------|
| File > 700 lines | Extract immediately |
| Addition > 100 lines | Extract immediately |
| File would exceed 800 lines | Extract immediately |
| Adding modal/dialog/form | Extract (typically > 100 lines) |
| File > 500 lines + adding > 50 lines | Ask user first |

### When User Rejects

```
1. "I apologize - I violated the file size rule."
2. "File X was Y lines, I added Z lines → now (Y+Z) lines."
3. "Extracting to [new file path]..."
4. "Extraction complete. File X is now Y lines."
```

---

## 💬 Example Interactions

### ✅ Good AI Behavior

```
User: "Add a delete confirmation dialog"

AI: "Checking Sidebar.tsx... Currently 1118 lines.
     Adding a delete confirmation dialog would add ~150 lines.
     This would make the file ~1268 lines, exceeding the 800-line limit.
     
     Proposed: Extract to components/modals/DeleteConfirmDialog.tsx
     Proceed with extraction?"
```

### ❌ Bad AI Behavior (What We're Preventing)

```
User: "Add a delete confirmation dialog"

AI: [Immediately adds 150 lines inline to Sidebar.tsx]
    "Done! Added delete confirmation dialog."
    
    // Sidebar.tsx: 1118 → 1268 lines 🚨 VIOLATION
```

### ✅ Good Recovery After Violation

```
User: "This violates file size rules"

AI: "I apologize - I violated the file size rule.
     Sidebar.tsx was 1118 lines, I added 150 lines → now 1268 lines.
     
     Extracting delete confirmation dialog to:
     components/modals/DeleteConfirmDialog.tsx
     
     [Extracts code, updates imports]
     
     Extraction complete. Sidebar.tsx is now 1118 lines.
     DeleteConfirmDialog.tsx created with 150 lines."
```

---

## 🔧 Integration with Other Rules

### Works With:

- **File Headers** (`file-headers.md`) - New extracted files need headers
- **React Patterns** (`react-patterns.md`) - Extraction patterns match
- **Refactoring Checklist** (`refactoring-checklist.md`) - Phase 1 includes file size checks
- **Coding Standards** (`coding-standards.md`) - File length guidelines align

### Enforcement Hierarchy:

1. **File Size Enforcement** (this rule) - Check FIRST
2. **Architecture Rules** - Where to extract (hooks/, services/, etc.)
3. **Pattern Files** - How to structure extracted code
4. **Coding Standards** - Code quality within extracted files

---

## 📊 Success Metrics

**Before This Rule:**
- Files regularly exceeded 1000 lines
- Modals added inline to large components
- No size checking before additions
- User had to catch violations

**After This Rule:**
- AI checks size before every addition
- Proposes extraction proactively
- Files stay under 800 lines
- User approves extractions, not violations

---

## 🎓 Teaching AI to Follow This

### Explicit Triggers (Use These Phrases)

```
"Add X. Keep file under 800 lines."
"Add X. Check file size first."
"Add X. Extract if needed to maintain file size."
"Add X. Don't bloat the file."
```

### Session Reminders

Every 30 minutes:
```
"Quick check: Any files getting too large?"
"List files modified with current line counts."
"Should anything be extracted?"
```

### After Violations

```
"This violates file size rules. Extract it."
"File is too large. Fix it."
"Don't add inline - extract to separate file."
```

---

## 🔄 Maintenance

**When to Update This Rule:**

1. If file size limits change (e.g., 800 → 1000)
2. If extraction patterns change (new folder structure)
3. If new file types need size limits (e.g., test files)
4. If violations persist despite rule (strengthen language)

**How to Know It's Working:**

- ✅ AI asks before adding to large files
- ✅ AI proposes extractions proactively
- ✅ Files stay under limits
- ✅ User approves extractions, not violations

---

**Last Updated:** 2026-01-12  
**Status:** Active enforcement rule
