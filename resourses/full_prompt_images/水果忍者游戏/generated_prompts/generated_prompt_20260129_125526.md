# Fruit Ninja Game Creation Prompt

Please generate a complete, playable "Fruit Ninja" style web game contained within a single `index.html` file.

### 1. Overall Description
Create a minimalist, browser-based arcade game using HTML5 Canvas and Vanilla JavaScript. The game should replicate the visual style of the reference image: a calming gradient background with simple 2D geometric fruits. The player creates a "blade" trail with their mouse to slice flying fruits while avoiding bombs.

### 2. Visual Style & Assets
*   **Background:** A vertical linear gradient moving from Teal/Sky Blue (top) to Lime Green (bottom).
*   **Fruits:** Represented as colored circles (Red, Orange, Yellow, Green, Purple).
    *   Must have a white, off-center circular highlight to simulate a 3D spherical look (as seen in the image).
*   **Blade Trail:** A white line that follows the cursor, tapering off or fading out to create a "swoosh" effect.
*   **UI:** Minimalist score counter in the top corner (white text). "Game Over" overlay with a restart button.

### 3. Core Mechanics & Interaction
*   **Controls:** Mouse drag (or touch) to slice. The blade is active only while the mouse button is held down.
*   **Spawning:** Fruits launch from the bottom of the screen with varying upward velocities and slight rotation.
*   **Physics:** Apply gravity so fruits rise and then fall in parabolic arcs.
*   **Collision:** Detect intersection between the mouse path (blade line) and the fruit circles.
*   **Game Loop:** Use `requestAnimationFrame` for smooth rendering.

### 4. Animations & Effects
*   **Slicing Effect:** When a fruit is hit:
    1.  The fruit disappears.
    2.  Spawn two semi-circles (halves) that rotate and fall away.
    3.  Spawn small colored particle "splashes" that fade out.
*   **Blade Animation:** The trail should smoothly connect the last few mouse positions and vanish quickly when movement stops.

### 5. Technical Requirements
*   **Single File:** All HTML structure, CSS styling, and JavaScript logic must be inside one `index.html` file.
*   **Responsive:** The canvas should resize to fit the browser window.
*   **Logic:**
    *   Maintain arrays for `fruits`, `particles`, and `bladePoints`.
    *   Implement a cleanup function to remove off-screen entities.
    *   Simple state management (Menu, Playing, Game Over).

**Output:** Provide the full, executable code block for `index.html`.
