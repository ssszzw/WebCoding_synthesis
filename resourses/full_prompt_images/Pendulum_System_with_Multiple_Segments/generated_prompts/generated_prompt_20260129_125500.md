# Web Development Prompt: Realistic Multi-Segment Pendulum Simulation

**Role:** Expert Frontend Developer & Physics Simulation Specialist
**Project Name:** Pendulum_System_with_Multiple_Segments
**Objective:** Create a highly realistic, interactive, and visually stunning Double/Triple (N-Segment) Pendulum simulation using the HTML5 Canvas API.

## 1. Overall Description
Develop a single-page web application that simulates the chaotic motion of a multi-segment pendulum. The system should accurately render physics based on Lagrangian mechanics, visualizing how small changes in initial conditions lead to vastly different outcomes (Chaos Theory). The aesthetic should be modern, minimalist, and "scientific," utilizing a dark theme with neon accents to highlight the motion and trajectory traces.

## 2. Technical Implementation
*   **Tech Stack:** Pure HTML5, CSS3, and Vanilla JavaScript (ES6+). No external libraries.
*   **Physics Engine:**
    *   Implement a generalized **N-Pendulum** logic (supporting at least 2 to 4 segments).
    *   Use **Runge-Kutta 4th Order (RK4)** integration method for numerical stability and precision. Do not use simple Euler integration, as it loses energy too quickly or becomes unstable.
    *   Calculate angular acceleration, velocity, and position for each joint in real-time.
*   **Performance:** Use `requestAnimationFrame` for a smooth 60fps+ rendering loop. Off-screen canvas or efficient array management should be considered for drawing the motion trails to prevent performance drops.

## 3. Visual Effects & Animation
*   **Canvas:** Full-screen responsive canvas that resizes with the browser window.
*   **The Pendulum:**
    *   **Rods:** Thin, crisp white or light gray lines connecting the masses.
    *   **Bobs (Masses):** Circular nodes where the radius scales slightly based on the configured mass.
*   **Motion Trails (The "Chaos" Visualizer):**
    *   The last bob (the tail) must leave a colored trail to visualize the path.
    *   The trail color should change dynamically (e.g., cycling through HSL spectrum) based on velocity or time.
    *   Implement a "fading" effect where older parts of the trail slowly disappear or darken over time, rather than persisting forever.
*   **Theme:** Dark background (`#0f0f15` or similar) to make the neon trails pop.

## 4. Interactive Features (UI/UX)
Create a semi-transparent, floating control panel (top-right or top-left) containing the following controls:

*   **System Configuration:**
    *   **Segment Count:** A slider or input to switch between Double (2), Triple (3), or Quad (4) pendulums dynamically.
    *   **Gravity:** Slider to adjust gravity ($g$), allowing for slow-motion (low gravity) or high-energy (high gravity) simulation.
    *   **Friction/Damping:** Slider to adjust air resistance (0 = perpetual motion, 1 = comes to a stop quickly).
*   **Segment Properties:**
    *   **Length:** A global slider to scale the length of the rods.
    *   **Mass:** A global slider to adjust the mass of the bobs.
*   **Action Buttons:**
    *   **Restart/Randomize:** Resets the simulation with random initial angles.
    *   **Clear Trail:** Removes the drawing history without resetting the physics.
    *   **Pause/Resume:** Toggles the animation loop.
*   **Mouse Interaction:** Allow the user to click and drag the first or second bob to set a new starting position manually (optional but highly desired).

## 5. Output Requirement
**CRITICAL:** Please combine all source code into a single `index.html` file.
*   **HTML:** Structure for the canvas and the UI overlay.
*   **CSS:** Embedded inside `<style>` tags. Ensure the UI is stylish, using a translucent glass-morphism effect, and the font is legible (sans-serif).
*   **JavaScript:** Embedded inside `<script>` tags. Ensure code is modular, well-commented, and handles the math logic cleanly.

**Deliver the complete, runnable code block now.**
