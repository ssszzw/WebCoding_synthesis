**Role:** Senior Front-End Developer / Creative Coder

**Task:** Create a self-contained HTML file implementing a physics-based "Gravity Hexagon" animation.

**Project Overview:**
A physics simulation featuring a ball bouncing inside a continuously rotating neon hexagon. The simulation must simulate gravity, friction, collision detection, and user interaction.

**Visual & UI Requirements:**
1.  **Canvas:** Full-screen, deep black background.
2.  **Hexagon:**
    -   Centered, large radius.
    -   Style: Bright Cyan/Teal stroke with a neon glow effect (CSS `shadowBlur` or filter).
    -   Animation: Continuous smooth rotation.
3.  **Ball:**
    -   Solid Red/Pink circle.
    -   Trapped inside the hexagon boundaries.
4.  **UI Overlay:**
    -   Top-left container.
    -   Title: "Gravity Hexagon" (Cyan, bold).
    -   Subtitle: "Click to boost the ball" (White, smaller).
    -   Font: Sans-serif/Monospace.

**Physics & Technical Implementation:**
1.  **Core Logic:** Use HTML5 `<canvas>` and vanilla JavaScript.
2.  **Motion Physics:**
    -   **Gravity:** Constant downward force applied to the ball's velocity.
    -   **Friction/Damping:** Slight velocity loss upon wall collision and movement (air resistance).
    -   **Rotation:** Hexagon vertices must be calculated dynamically based on current rotation angle.
3.  **Collision Detection:**
    -   Implement strict collision logic between the circle (ball) and line segments (hexagon walls).
    -   Calculate wall normal vectors to reflect the ball's velocity vector correctly upon impact.
    -   Add rotational velocity transfer (the spinning wall imparts force to the ball).
4.  **Interaction:**
    -   **Click/Tap:** Applies an immediate velocity boost (impulse) to the ball, launching it upwards or towards the center.
5.  **Game Loop:** Use `requestAnimationFrame` for smooth 60fps rendering.

**Output Requirement:**
Provide a single `index.html` file containing all HTML structure, CSS styling, and JavaScript logic. No external libraries or assets. Ensure the code is bug-free and renders immediately in a modern browser.
