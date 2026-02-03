# Web Development Prompt: Solar System Animation

**Role:** Expert Frontend Developer / Creative Coder
**Project:** Solar_System_Animation
**Objective:** Create a visually stunning, interactive 2D simulation of the Solar System using HTML5 Canvas. The entire project must be contained within a single `index.html` file.

## 1. Project Overview
Develop a simulation of the 8 planets orbiting the Sun. The view should be a top-down 2D perspective. The simulation must accurately represent the relative order of planets and vary their orbital speeds and radii (simplified for visual clarity, not 1:1 astronomical scale). The goal is to create an educational and aesthetic experience.

## 2. Technical Implementation Requirements
*   **File Structure:** All code (HTML structure, CSS styling, and JavaScript logic) must be combined into one single file named `index.html`.
*   **Core Technology:** Use the **HTML5 Canvas API** for rendering the solar system to ensure high performance and smooth 60fps animation.
*   **Responsiveness:** The canvas should automatically resize to fill the entire browser window (`window.innerWidth`, `window.innerHeight`).
*   **No External Dependencies:** Do not use external images, libraries (like Three.js or jQuery), or CSS frameworks. All graphics must be drawn programmatically.

## 3. Visual & Aesthetic Details
*   **Background:** A deep space theme (dark black/blue gradient) populated with a generated starfield. Stars should have varying sizes and opacity to create depth.
*   **The Sun:** Located at the center of the screen. It should emit a glowing effect (using radial gradients or shadow blurring) and be yellow/orange in color.
*   **The Planets:**
    *   Render Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.
    *   **Colors:** Assign distinct colors to each planet (e.g., Earth = Blue, Mars = Red, Jupiter = Beige/Striped effect if possible).
    *   **Sizes:** Planets should have different sizes (e.g., Jupiter significantly larger than Earth), though scaled down to fit the screen.
    *   **Saturn's Rings:** Specifically draw a ring system around Saturn to distinguish it.
*   **Orbits:** Draw faint, circular lines (stroke) representing the orbital path of each planet so the user can see the tracks.

## 4. Animation & Physics
*   **Orbital Mechanics:**
    *   Planets must orbit the Sun counter-clockwise.
    *   **Speed:** Inner planets (e.g., Mercury) must orbit faster than outer planets (e.g., Neptune).
    *   **Animation Loop:** Use `requestAnimationFrame` for smooth rendering.
*   **Star Twinkle:** (Optional) Add a subtle twinkling effect to the background stars.

## 5. Interaction Features
Implement a minimal UI overlay (positioned at the top-left or bottom-left) with the following controls:
1.  **Speed Control:** A range slider (`<input type="range">`) to adjust the simulation speed (e.g., from 0.1x to 5x speed).
2.  **Mouse Interaction (Hover):** When the user hovers their mouse cursor over a planet:
    *   The planet should highlight (e.g., increase brightness or stroke).
    *   A tooltip or label should appear near the planet displaying its name (e.g., "Mars").

## 6. Code Structure Guidelines
Please organize the code within the single file as follows:
1.  **HTML:** Container for the Canvas and UI controls.
2.  **CSS (`<style>`):** Reset default margins, set body to `overflow: hidden`, style the UI overlay to be semi-transparent and modern.
3.  **JavaScript (`<script>`):**
    *   Configuration object (planets data: radius, color, distance, speed).
    *   `Star` class/function for background generation.
    *   `Planet` class/function with `draw()` and `update()` methods.
    *   Main `animate()` loop.
    *   Event listeners for resizing, mouse movement (hit detection), and UI controls.

**Deliverable:** A complete, copy-paste ready `index.html` file containing the full solution.
