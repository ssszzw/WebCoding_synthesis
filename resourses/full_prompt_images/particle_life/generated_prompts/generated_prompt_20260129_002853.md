Create a standalone `index.html` file containing a comprehensive "Particle Life" simulation called "Autolife".

### Project Overview
Build a zero-player simulation where thousands of colored particles interact based on procedural attraction/repulsion rules, forming complex, organic structures.

### Technical Implementation
*   **Core Logic:** Implement the "Particle Life" algorithm.
    *   **Particles:** ~1000-2000 instances. Properties: x, y, vx, vy, color.
    *   **Colors:** 4 distinct types (e.g., Red, Green, Blue, Yellow).
    *   **Physics:**
        *   Particles exert forces on neighbors within a dynamic `Radius`.
        *   **Rule Matrix:** A 4x4 matrix defining attraction/repulsion forces between color pairs (e.g., Red attracts Green, Green repels Blue). Values range from -1 (repel) to 1 (attract).
        *   **Movement:** Euler integration. Velocity update with `Friction` factor.
        *   **Boundaries:** Toroidal wrapping (particles leaving right side enter left).
*   **Performance:** Optimize the interaction loop.

### Visual Effects
*   **Canvas:** Full-screen, responsive HTML5 Canvas.
*   **Background:** Deep dark blue/black (`#020205`).
*   **Trails:** Implement a motion trail effect by filling the canvas with semi-transparent black (`rgba(0,0,0, 1 - trail_value)`) before drawing frames.
*   **Particles:** Render as small, bright glowing circles or rectangles (2-3px).

### UI & Interaction
Implement a floating, glassmorphism-style control panel (top-left):
*   **Header:** Title "Autolife", subtitle "Zero-player particle life."
*   **Controls:**
    *   **Buttons:**
        *   "Pause/Play": Toggles simulation.
        *   "Remix Rules": Randomizes the attraction/repulsion matrix to generate new behaviors (cells, gliders, worms).
        *   "Re-scatter": Randomizes particle positions.
    *   **Sliders (with labels and live values):**
        *   `Radius`: Interaction distance (0-100).
        *   `Trails`: Visual decay rate (0.0-1.0).
        *   `Friction`: Velocity damping (0.0-1.0).
    *   **Active Colors:** Visual row of the 4 active particle colors.
*   **Overlay:** Bottom-right text showing FPS and Particle Count.

### Code Constraints
*   Merge all HTML, CSS, and JavaScript into a single `index.html` file.
*   Use modern ES6+ JavaScript (classes, const/let).
*   Ensure the UI looks identical to the provided reference (dark theme, blue accents, rounded corners).
