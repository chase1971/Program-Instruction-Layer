# Math explanation animation recipe

Use this recipe when generating a new Manim animation for Chase's math apps.

## Teaching movement

- Treat the original equation as written work. Put it on one baseline and keep it visible while the next line develops.
- Work downward, like handwriting on paper. Do not make the solution float upward into place.
- Preserve the normal baseline of `+`, `=`, and parentheses. Do not make operators look like separate fractions unless division is the actual point.
- When a new line is complete, make it the final position before building around it. Do not move it again just to add a factor, parentheses, or `= 0`.
- Use deliberate, smooth motion with short pauses after each mathematical idea.

## GCF and division pattern

1. Show the full equation, already written, including `= 0` when relevant.
2. Draw fraction bars directly beneath the terms being divided.
3. Put the same GCF below each bar.
4. Move each quotient downward into its final position.
5. Say that the terms are divided by the same common factor.
6. Merge duplicate GCF labels into one factor and put it in front of the expression that remains.
7. Form parentheses around the quotient expression without moving the quotient.
8. Add `= 0` last when the equation is factored.
9. If solving by the zero-product property, lift the factored equation into the original equation's position, separate the factors diagonally, and create one equation per factor.
10. Solve each equation with the same visible operation style: show the operation beneath both sides, then reveal the simplified result.

## Language

Prefer plain classroom language:

- “Divide each term by the same common factor.”
- “Put the GCF you factored out in front of what is left.”
- “When we factor a GCF, we put it in front like this.”

Avoid “multiply back” unless the lesson specifically teaches checking by multiplication.

## Visual style

- Dark navy background, large high-contrast math, muted instructional captions.
- Gold for the GCF, light blue for the remaining factors, white for operators and structure.
- Keep the equation readable on a phone held horizontally.
- Use MathTex for formulas; do not render equations as ordinary text.
- Produce a reviewable MP4 first. Interactive student manipulation belongs in the web app, not in the rendered clip.

## Prompt template

> Create a Manim mathematical explanation animation using the attached “Math explanation animation recipe.” Teach [CONCEPT] with [EQUATION]. Keep the original equation written on one baseline. Develop the work downward like handwriting. Preserve the final position of each completed expression; build new factors, parentheses, and equality signs around it. Use fraction bars and visible operations where they clarify the algebra. Use deliberate pauses and plain classroom captions. Use the navy, gold, blue, and white visual language from the recipe. Render a phone-readable MP4. Do not invent extra algebraic steps; ask only if the intended mathematical sequence is ambiguous.
