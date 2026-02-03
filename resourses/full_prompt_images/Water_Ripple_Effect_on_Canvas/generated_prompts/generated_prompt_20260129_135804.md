# Web Development Prompt: Realistic Interactive Water Ripple Simulation

**Role:** Expert Frontend Developer / Creative Coder
**Task:** Create a high-performance, realistic water ripple simulation using HTML5 Canvas inside a single file.

**Project Name:** Water_Ripple_Effect_on_Canvas

### 1. Project Overview
Develop a full-screen, interactive web page that simulates a realistic water surface. The simulation should use a physics-based algorithm to calculate wave propagation, resulting in natural-looking ripples that refract light, spread outward, interfere with one another, and gradually dampen over time.

### 2. Functional & Technical Requirements

**A. HTML Structure:**
*   A single `index.html` file containing all HTML, CSS, and JavaScript.
*   A `<canvas>` element that covers the entire browser viewport.
*   No external libraries (jQuery, Three.js, etc.) allowed; use vanilla JavaScript only.

**B. CSS Styling:**
*   Remove default browser margins/padding (`body { margin: 0; overflow: hidden; }`).
*   Ensure the canvas is responsive and resizes correctly if the browser window changes dimensions.
*   Set a dark or neutral background color for the body to act as a fallback.

**C. JavaScript Implementation Details:**

*   **Algorithm:** Implement the "2D Wave Equation" (often called the Double Buffering algorithm). You will need:
    *   Two data arrays (buffers): `buffer1` (current state) and `buffer2` (previous state) to store the "height" of the water at every pixel (or downsampled grid).
    *   A damping factor (e.g., 0.96 to 0.99) to ensure ripples fade out gradually.
*   **Rendering (The Visuals):**
    *   Instead of drawing simple circle strokes, use **Pixel Manipulation** (`ctx.getImageData` / `ctx.putImageData`).
    *   **Background:** Generate a procedural background image programmatically (e.g., a tiled stone texture, a grid, or colorful text) and draw it to the canvas once. This background is necessary to demonstrate the refraction effect.
    *   **Refraction:** In the render loop, calculate the displacement of pixels based on the wave height data. Shift the pixel coordinates of the background image to simulate light bending through water.
*   **Performance:**
    *   Use `requestAnimationFrame` for a smooth 60FPS loop.
    *   Consider downsampling the ripple logic (e.g., calculating physics on a grid half the size of the canvas) to maintain high performance on larger screens.

### 3. Interaction & Animation

*   **Mouse Interaction:**
    *   **Click:** When the user clicks, disturb the water buffer at that coordinate to create a strong ripple.
    *   **Drag (MouseMove):** As the mouse moves across the canvas, create a trail of smaller ripples.
*   **Automatic Ripples (Idle State):**
    *   To make the scene feel alive, randomly generate "raindrops" (random ripples) at random coordinates every few seconds.

### 4. Code Structure Requirement
Please provide the complete solution in the following format. Ensure the script is placed at the end of the body or wrapped in a `DOMContentLoaded` event listener.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Realistic Water Ripple Effect</title>
    <style>
        /* CSS content here */
    </style>
</head>
<body>
    <!-- Canvas Element here -->
    
    <script>
        /* JavaScript logic here */
    </script>
</body>
</html>
```
