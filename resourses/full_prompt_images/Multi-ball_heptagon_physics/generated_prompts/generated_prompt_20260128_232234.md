# Web-based Spinning Heptagon Physics Simulation

Please write a single, self-contained `index.html` file that implements a physics simulation using HTML5 Canvas and vanilla JavaScript.

### 1. Visual Style & Layout
*   **Background:** Solid dark gray or black (`#1a1a1a` or similar).
*   **Container (Heptagon):** A large, regular 7-sided polygon centered on the screen.
    *   **Style:** Neon cyan/light-blue outline (`#00FFFF`) with a slight glow effect (`shadowBlur`).
    *   **Animation:** The heptagon must rotate continuously clockwise.
*   **Balls:** 20 circular objects inside the heptagon.
    *   **Appearance:** Each ball must have a unique, vibrant fill color, a white border (stroke), and a white number (1-20) centered inside.
*   **UI Overlay:** A semi-transparent black box in the top-left corner displaying:
    *   Title: "Heptagon Physics" (Bold, White).
    *   Stats: "Balls: 20", "Gravity: On", "Wall Friction: On" (Smaller, light gray text).

### 2. Physics Engine Requirements
*   **Gravity:** Constant downward force acting on all balls.
*   **Collision Detection:**
    *   **Ball-to-Ball:** Elastic collisions where balls bounce off each other without overlapping.
    *   **Ball-to-Wall:** Balls must bounce off the rotating walls of the heptagon.
        *   *Critical:* The collision calculation must account for the rotation of the wall to impart correct angular momentum/bounce direction to the balls (balls should be "scooped" or hit by the moving wall).
*   **Motion:** Implement velocity, acceleration, and friction/damping to prevent infinite energy buildup.
*   **Constraint:** Balls must remain strictly inside the heptagon shape.

### 3. Technical Implementation
*   **Structure:** Merge HTML, CSS, and JavaScript into one file.
*   **Rendering:** Use the HTML5 `<canvas>` API for high-performance rendering.
*   **Loop:** Use `requestAnimationFrame` for the game loop.
*   **Responsiveness:** The canvas should fit the window size, but the simulation area can be fixed or responsive.

### 4. Code Output
Provide the complete source code within a single `index.html` file, ready to run in a browser. Ensure the math for the rotating polygon collision is accurate so balls do not tunnel through walls.
