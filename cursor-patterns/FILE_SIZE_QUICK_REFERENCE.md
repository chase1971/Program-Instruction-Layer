# File Size Enforcement - Quick Reference

> **One-page cheat sheet for AI and developers**

---

## ⚡ Before Adding ANY Code

```
1. Read file → Get line count
2. Estimate addition size  
3. Calculate: current + addition = final
4. Check limits → STOP if needed
5. Ask user or extract
```

---

## 🚨 Hard Limits

| Limit | Action |
|-------|--------|
| **800 lines** | HARD MAX - NO EXCEPTIONS |
| **700 lines** | Extract immediately |
| **500 lines + 50+ addition** | Ask user first |
| **100+ line addition** | Extract immediately |

---

## ✅ What to Do

### File > 700 lines
→ **STOP. Extract. No questions.**

### File > 500 lines + adding > 50 lines
→ **STOP. Ask user:**
"File X is Y lines. Adding Z lines → (Y+Z) lines. Extract or proceed?"

### Adding > 100 lines
→ **STOP. Extract. No questions.**

### Adding modal/dialog/form
→ **STOP. Extract. (Usually > 100 lines)**

---

## 📁 Where to Extract

- Modal/Dialog → `components/modals/[Name]Modal.tsx` (⚠️ Use `max-w-md`, NOT `max-w-3xl` - see [Modal Pattern](./modal-pattern.md))
- Form → `components/forms/[Name]Form.tsx`
- State logic → `hooks/use[Name].ts`
- Business logic → `services/[name]Service.ts`
- Utilities → `utils/[name]Utils.ts`

---

## ❌ When User Rejects

1. Apologize
2. Acknowledge violation
3. Extract immediately
4. Report: "Extracted X lines. File Y is now Z lines."

---

## 🔄 Session Check (Every 30 min)

"Session check: Files modified:"
- List files with line counts
- Flag files > 700 lines
- Flag files that grew > 200 lines
- Propose extractions

---

## 💬 Magic Phrases (Use These)

**User says:**
- "Add X. Keep file under 800 lines."
- "Add X. Check file size first."
- "Add X. Extract if needed."

**AI must:**
- Check size FIRST
- Calculate impact
- Ask or extract BEFORE coding

---

**Remember:** Better to ask and extract than violate and get rejected.
