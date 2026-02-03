# Application Development Prompt: Interactive Firework Particle System

Please generate a single, self-contained `index.html` file including HTML, CSS, and JavaScript to create a web-based interactive firework and particle simulation.

### 1. Overall Concept
A full-screen interactive canvas animation featuring a dark, deep-space themed background with floating geometric shapes. The core functionality involves a high-performance particle system where the user's mouse creates trails, clicks create explosions, and a UI panel controls physics and visual parameters.

### 2. Visual Style & Layout
*   **Background:** Deep blue/purple gradient (e.g., `#0f0c29` to `#24243e`). Scattered faint stars and large, semi-transparent slowly floating geometric shapes (triangles, squares, circles) to add depth.
*   **Particles:** Glowing, vibrant colors. Use additive blending (`globalCompositeOperation = 'lighter'`) for a neon firework effect.
*   **UI Design:** "Glassmorphism" style. Translucent dark backgrounds with blur (`backdrop-filter`), rounded corners, white text, and neon accent colors (pink/purple gradients) for buttons.

### 3. Functional Modules

#### A. Control Panel (Top Left)
A floating window titled "🎨 Control Panel" containing:
*   **Sliders:**
    *   "Particle Count": Adjusts emission rate.
    *   "Particle Speed": Adjusts velocity magnitude.
*   **Toggles (Checkboxes/Switches):**
    *   "Gravity": Toggles vertical acceleration.
    *   "Line Effect": Draws thin lines between particles close to each other (network effect).
    *   "Rainbow Mode": Cycles particle colors vs fixed colors.
*   **Buttons:**
    *   "Clear Canvas": Immediately removes all particles.
    *   "Firework Show": Triggers an automated random firework loop.

#### B. Info Panel (Bottom Right)
A floating static window displaying:
*   **Instructions:**
    *   "🖱️ Move mouse to create particles"
    *   "🚀 Click to explode"
    *   "⌨️ Spacebar to Pause/Resume"
*   **Stats:** Real-time counter: "Particle Count: [N]".

#### C. Canvas Layer
*   Full-screen HTML5 Canvas covering the viewport.
*   Handles all particle rendering and animation loops.

### 4. Technical & Animation Logic

*   **Particle Class:**
    *   Properties: `x, y, vx, vy, life, color, size`.
    *   Update: Apply velocity, friction (decay), gravity (if enabled). Shrink size over time.
    *   Draw: Circle or spark shape. If "Line Effect" is on, calculate distance to neighbors and draw lines if `< threshold`.
*   **Interactions:**
    *   `mousemove`: Spawn a stream of particles at cursor position.
    *   `mousedown`: Spawn a "burst" (radial explosion) of many particles.
    *   `keydown (Space)`: Toggle animation pause state.
*   **Auto Mode:** Timer-based random explosions at random coordinates.
*   **Optimization:** Remove particles when `life <= 0`. Use `requestAnimationFrame` for the loop.

### 5. Implementation Requirements
*   **Single File:** All CSS (inside `<style>`) and JS (inside `<script>`) must be embedded in the HTML.
*   **Responsiveness:** Canvas must resize automatically with the browser window.
*   **No External Assets:** Use CSS drawing or Canvas API for all shapes/icons. Do not link to external images or libraries.
