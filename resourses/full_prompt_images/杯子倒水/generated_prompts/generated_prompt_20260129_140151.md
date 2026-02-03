# Role: Expert Creative Coder & Front-End Developer

Please generate a high-quality, comprehensive web-based simulation based on the "Cup Pouring Water" physics project. The solution must be implemented entirely in **Vanilla JavaScript** using the **HTML5 Canvas API**.

## Project Overview
Develop a 2D fluid simulation engine that visualizes liquid (represented by a particle system) being poured from a tilting cup under the influence of gravity. The simulation should be self-contained, performant, and visually smooth.

## Technical Specifications

### 1. File Structure & Environment
*   **Single File Requirement:** All code (HTML structure, CSS styling, and JavaScript logic) must be contained within a single `index.html` file.
*   **No External Dependencies:** Do not use external physics engines (like Matter.js) or graphics libraries (like Pixi.js). The physics and rendering logic must be written from scratch.
*   **Browser Compatibility:** The code must run directly in modern browsers (Chrome, Firefox, Edge, Safari).

### 2. Canvas & Display
*   **Resolution:** Initialize the canvas with a logical resolution of **1920x1080**.
*   **Styling:** Use CSS to ensure the canvas fits within the user's viewport (e.g., `max-width: 100%; height: auto;`) while maintaining aspect ratio.
*   **Visual Style:**
    *   **Background:** Clean white (`#FFFFFF`).
    *   **Cup:** Black lines (`#000000`), line width approx 3-5px.
    *   **Liquid:** Blue particles (`#3498DB` or similar), approx 4px radius.

### 3. Object-Oriented Architecture
Organize the JavaScript code using modern ES6+ Class syntax.
*   **`Particle` Class:** Handles position `(x, y)`, velocity `(vx, vy)`, radius, color, and physics updates.
*   **`Cup` Class:** Handles geometry definition (vertices), rotation logic, and rendering.
*   **`Simulation` Class:** Manages the main game loop (`requestAnimationFrame`), event handling, and orchestrating interactions between particles and the cup.

## Physics Engine Implementation

### 4. The Particle System (Fluid)
*   **Quantity:** Instantiate approximately **400-500 particles**.
*   **Initialization:** Spawn particles gradually slightly above the cup's initial position so they fall naturally into the container.
*   **Gravity:** Apply a constant downward force to `vy` every frame (e.g., `gravity = 0.15`).
*   **Euler Integration:** Update positions explicitly:
    ```javascript
    velocity += gravity;
    position += velocity;
    ```
*   **Particle Repulsion (Fluid Behavior):** To prevent particles from collapsing into a single point and to simulate volume:
    *   Check distances between particle pairs.
    *   If `distance < radius * 2`, apply a small repulsive force vector to separate them.
    *   *Optimization:* Use spatial partitioning (like a grid) or simply limit checks to neighbors if performance drops, though brute force is acceptable for 400 particles.

### 5. The Cup & Rotation
*   **Geometry:** Define the cup as a set of connected line segments (Polyline). Shape: A "U" shape or a trapezoid with an open top.
*   **State:** The cup starts upright in the horizontal center of the screen.
*   **Animation Sequence:**
    1.  **Fill Phase:** Cup remains stationary while particles spawn and settle.
    2.  **Pour Phase:** After a set time (or when particles settle), the cup begins to rotate.
    3.  **Rotation:** Rotate the cup around its **center of mass** (centroid). The angle should transition smoothly from 0 radians to approximately 2.3 radians (~135 degrees) to ensure all water pours out.

### 6. Collision Detection (Crucial)
*   **Cup-Particle Collision:**
    *   Since the cup rotates, you cannot use simple bounding boxes.
    *   You must mathematically transform the cup's static vertices based on the current rotation angle to get their "world space" coordinates.
    *   Implement **Line Segment vs. Circle** collision detection.
    *   If a particle crosses a cup wall, push it back along the normal vector of that wall.
    *   Apply a **restitution coefficient** (bounce) of ~0.5 to simulate energy loss (water isn't perfectly bouncy).
    *   Include a friction factor when particles slide along the cup walls.
*   **Screen Boundaries:**
    *   Particles should bounce off the floor (bottom of canvas).
    *   Particles can flow off the left/right sides (optional) or bounce off side walls.

## Visuals & Interaction

### 7. Animation Loop
*   Use `requestAnimationFrame` for a smooth 60fps experience.
*   The rendering order must be:
    1.  Clear Canvas.
    2.  Update Physics (Gravity -> Repulsion -> Collision -> Movement).
    3.  Draw Cup.
    4.  Draw Particles.

### 8. User Controls
Add a simple UI overlay in the top-left corner:
*   **"Reset" Button:** Restarts the simulation, resetting the cup angle and respawning particles.
*   **Status Text:** (Optional) Display "Status: Filling" or "Status: Pouring".

## Code Requirements Summary
1.  **Comments:** Provide clear, English comments explaining the vector math (especially the rotation formula and collision reflection vectors).
2.  **Robustness:** Ensure particles do not tunnel (leak) through the corners of the cup.
3.  **Completeness:** The output must be a fully functional HTML string ready to copy-paste.

---
**Please generate the full source code within a code block.**
