# Add a Line, Change a Sign Pattern

**Use Case:** Animate the mathematical rule "when subtracting a negative, change the subtraction to addition and the negative to positive"

Visual representation of: `a - (-b) → a + b`

---

## Overview

This pattern implements a multi-phase animation sequence that visually demonstrates the algebraic rule for subtracting negative numbers. It shows:

1. Operator (middle minus) pops/zooms to 1.5x
2. Operator changes from minus to plus (while staying popped)
3. Right fraction's negative sign pops/zooms to 1.5x (operator still popped)
4. Right fraction's negative sign changes from minus to plus (both signs still popped)
5. Both signs depop/fade simultaneously:
   - Operator zooms back to normal size (1.0x)
   - Right sign + parentheses fade out completely
   - Fraction itself (numerator/denominator) remains fully visible

---

## State Interface

```typescript
interface AddLineChangeSignState {
  // Operator state
  operatorPlus: boolean;        // true = +, false = -
  popOperator: boolean;         // Pop animation on operator
  depopOperator: boolean;       // Depop animation on operator
  
  // Right fraction negative sign state
  rightFractionNegative: boolean;    // Show negative sign on right fraction
  popRightNegative: boolean;         // Pop animation on right negative sign
  rightNegativeIsPlus: boolean;      // Change minus to plus (while popped)
  fadeRightNegative: boolean;        // Fade out sign and parentheses
}
```

---

## Animation Sequence

```typescript
// Example: 6 - (-5/7) → 6 + 5/7

async function runAddLineChangeSignAnimation() {
  // Phase 1: Pop operator minus to 1.5x (400ms)
  setState(s => ({ ...s, popOperator: true }));
  await wait(400);
  
  // Phase 2: Wait (500ms)
  await wait(500);
  
  // Phase 3: Change minus to plus while popped
  setState(s => ({ ...s, operatorPlus: true }));
  
  // Phase 4: Wait (500ms)
  await wait(500);
  
  // Phase 5: Pop right negative minus to 1.5x (400ms)
  // Note: Operator is STILL popped at this point
  setState(s => ({ ...s, popRightNegative: true }));
  await wait(400);
  
  // Phase 6: Wait (500ms)
  await wait(500);
  
  // Phase 7: Change right negative minus to plus while popped
  setState(s => ({ ...s, rightNegativeIsPlus: true }));
  
  // Phase 8: Wait with both plus signs popped (500ms)
  await wait(500);
  
  // Phase 9: BOTH depop/fade simultaneously
  // - Operator depops back to 1x
  // - Right plus + parentheses fade out (fraction 5/7 stays visible)
  setState(s => ({ 
    ...s, 
    depopOperator: true, 
    fadeRightNegative: true 
  }));
  
  // Phase 10: Wait for animations to complete (800ms)
  await wait(800);
  
  // Phase 11: Finalize state
  setState(s => ({
    ...s,
    operatorPlus: true,
    popOperator: false,
    depopOperator: false,
    rightFractionNegative: false,
    popRightNegative: false,
    rightNegativeIsPlus: false,
    fadeRightNegative: false,
  }));
}
```

---

## Component Implementation

### Props for FractionEquation Component

```typescript
export interface FractionEquationProps {
  // ... other props ...
  
  // Operator
  operator?: '+' | '-';
  popOperator?: boolean;      // Pop (zoom) the operator
  depopOperator?: boolean;    // Depop (zoom back) the operator
  
  // Right fraction negative sign
  rightNegative?: boolean;
  popRightNegative?: boolean;       // Pop (zoom) the right fraction's negative sign
  rightNegativeIsPlus?: boolean;    // Change right negative minus to plus (while popped)
  fadeRightNegative?: boolean;      // Fade out the right fraction's negative sign and parentheses
}
```

### Operator Rendering

```tsx
{/* Operator */}
<button
  type="button"
  onClick={onOperatorClick}
  disabled={isOperatorDisabled}
  className={operatorButtonClass}
  aria-label={operator === '-' ? 'Operator: minus' : 'Operator: plus'}
>
  <span 
    style={{
      transform: popOperator && !depopOperator ? 'scale(1.5)' : 'scale(1)',
      transition: (popOperator || depopOperator) ? 'transform 0.4s ease-out' : 'none',
    }}
  >
    {operatorSymbol}
  </span>
</button>
```

**Key Points:**
- NO CSS animation classes on depop - just smooth transition
- Transition applies on BOTH pop and depop for smooth motion
- Transform changes from `scale(1.5)` to `scale(1)` when depopping

### Right Fraction Negative Sign Rendering

```tsx
const renderFraction = (
  // ... params ...
  negIsPlus: boolean = false,
  fadeNeg: boolean = false
) => {
  const withNegative = negative ? (
    <div className="inline-flex items-stretch gap-0.5">
      {/* Left parenthesis */}
      <span 
        className="self-stretch flex shrink-0" 
        style={{ 
          width: '0.45em',
          opacity: fadeNeg ? 0 : 1,
          transition: fadeNeg ? 'opacity 0.5s ease-out' : 'none',
        }} 
        aria-hidden
      >
        <svg viewBox="0 0 20 100" preserveAspectRatio="none" className="h-full w-full">
          <path d="M 20 0 C 0 0 0 100 20 100" fill="none" stroke="currentColor" strokeWidth={2} />
        </svg>
      </span>
      
      {/* Minus/Plus sign */}
      <span 
        style={{ 
          width: '1.5rem', 
          marginLeft: '-0.2rem', 
          marginRight: '-0.2rem',
          opacity: hideNeg || fadeNeg ? 0 : 1,
          transform: popNeg && !fadeNeg ? 'scale(1.5)' : 'scale(1)',
          transition: fadeNeg ? 'opacity 0.5s ease-out' : (popNeg ? 'transform 0.4s ease-out' : 'none'),
        }}
      >
        {negIsPlus ? '+' : '−'}
      </span>
      
      {/* Fraction content - NOT affected by fade */}
      {fractionContent}
      
      {/* Right parenthesis */}
      <span 
        className="self-stretch flex shrink-0" 
        style={{ 
          width: '0.45em',
          opacity: fadeNeg ? 0 : 1,
          transition: fadeNeg ? 'opacity 0.5s ease-out' : 'none',
        }} 
        aria-hidden
      >
        <svg viewBox="0 0 20 100" preserveAspectRatio="none" className="h-full w-full">
          <path d="M 0 0 C 20 0 20 100 0 100" fill="none" stroke="currentColor" strokeWidth={2} />
        </svg>
      </span>
    </div>
  ) : fractionContent;
  
  return withNegative;
};
```

**Key Points:**
- Sign changes from `−` to `+` based on `negIsPlus` prop
- Fade affects: left parenthesis, sign, right parenthesis
- Fade does NOT affect: fraction content (numerator/denominator)
- Each element has independent opacity control
- Transform (pop) only affects the sign, not the parentheses

---

## Timing Breakdown

| Phase | Duration | State Changes | Visual Effect |
|-------|----------|---------------|---------------|
| 1 | 400ms | `popOperator: true` | Operator zooms to 1.5x |
| 2 | 500ms | *(none)* | Pause for emphasis |
| 3 | 0ms | `operatorPlus: true` | Minus changes to plus |
| 4 | 500ms | *(none)* | Pause to see the change |
| 5 | 400ms | `popRightNegative: true` | Right sign zooms to 1.5x |
| 6 | 500ms | *(none)* | Pause for emphasis |
| 7 | 0ms | `rightNegativeIsPlus: true` | Minus changes to plus |
| 8 | 500ms | *(none)* | Pause with both plus signs |
| 9 | 0ms | `depopOperator: true`<br/>`fadeRightNegative: true` | Both start animating back |
| 10 | 800ms | *(none)* | Wait for animations to finish |
| 11 | 0ms | Reset all animation flags | Clean final state |

**Total Duration:** ~3.7 seconds

---

## Used In

- **Fractions App**: Part 2 Tutorial, Step 8 → Step 9
  - Problem: `6 - (-5/7)` becomes `6 + 5/7`
  - File: `Part2TutorialComponent.tsx`

---

## Common Pitfalls

### ❌ Using CSS animation classes on depop
```typescript
// WRONG - causes unwanted pulse
<span className={depopOperator ? 'animate-tutorial-zoom' : ''}>
```

### ✅ Use inline transitions only
```typescript
// CORRECT - smooth transition back to scale 1
<span style={{
  transform: popOperator && !depopOperator ? 'scale(1.5)' : 'scale(1)',
  transition: (popOperator || depopOperator) ? 'transform 0.4s ease-out' : 'none',
}}>
```

### ❌ Fading the entire fraction wrapper
```typescript
// WRONG - fades the fraction content too
<div style={{ opacity: fadeNeg ? 0 : 1 }}>
  <span>parenthesis</span>
  <span>sign</span>
  {fractionContent}
</div>
```

### ✅ Fade only the sign elements
```typescript
// CORRECT - fraction stays visible
<div>
  <span style={{ opacity: fadeNeg ? 0 : 1 }}>parenthesis</span>
  <span style={{ opacity: fadeNeg ? 0 : 1 }}>sign</span>
  {fractionContent} {/* No fade applied */}
</div>
```

---

## Educational Purpose

This animation teaches students the algebraic rule:

**"When you subtract a negative number, it's the same as adding a positive number"**

The visual sequence helps students understand:
1. The operator changes (subtraction → addition)
2. The sign of the number changes (negative → positive)
3. Both changes happen together to maintain mathematical equivalence

This is a fundamental concept in algebra and fraction operations.
