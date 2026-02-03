# Web Development Prompt: 3D Wireframe Cube with Canvas 2D

**Role:** Expert Frontend Developer
**Task:** Create a single-file HTML solution (`index.html`) containing HTML, CSS, and JavaScript to render a rotating 3D wireframe cube using **only the HTML5 Canvas 2D Context**.

### 1. Project Overview
Create a visually striking "Optical Illusion" style 3D cube. The cube should be rendered as a wireframe (skeleton) that rotates continuously in 3D space. The rendering must rely entirely on mathematical projection (projecting 3D coordinates onto a 2D plane) without using WebGL, Three.js, or any external libraries.

### 2. Technical Implementation Requirements
*   **Structure:**
    *   Define the cube using a set of 8 Vertices (x, y, z coordinates).
    *   Define the cube using a set of 12 Edges (connecting specific indices of the vertices array).
*   **Mathematical Logic:**
    *   Implement a "Perspective Projection" algorithm to convert 3D $(x, y, z)$ points into 2D $(x, y)$ canvas coordinates.
    *   Formula reference: `scale = focal_length / (focal_length + z)`.
    *   Apply rotation matrices for the X, Y, and Z axes to the vertices before projection to simulate 3D rotation.
*   **Rendering Loop:**
    *   Use `requestAnimationFrame` for smooth, 60fps animation.
    *   Clear the canvas on every frame before redrawing.
    *   Draw lines connecting the projected vertices based on the Edge definitions.

### 3. Visual & Aesthetic Details
*   **Layout:** The canvas must occupy 100% of the browser window width and height. Remove any scrollbars.
*   **Styling:**
    *   **Background:** A dark, radial gradient (e.g., `#1a1a1a` to `#000000`) to give a sense of depth and focus.
    *   **Cube Lines:** Use a bright, contrasting color (e.g., Cyan `#00f3ff` or White) with a slight `shadowBlur` (glow effect) to make it look modern and sleek.
    *   **Vertices:** Draw small filled circles (dots) at each corner (vertex) of the cube to accentuate the geometry.

### 4. Interactive Features
*   **Mouse Interaction:**
    *   The cube should rotate automatically by default.
    *   Map the user's mouse position (`mousemove`) to influence the rotation speed and angle. For example, moving the mouse to the left/right controls the Y-axis rotation speed, and up/down controls the X-axis rotation speed.
*   **Responsiveness:**
    *   Implement a window `resize` event listener to adjust the canvas dimensions and re-center the cube coordinates dynamically if the browser window changes size.

### 5. Output Format
*   Provide the complete source code in a single code block.
*   The code must be contained within a single `index.html` file.
*   Include `<style>`, `<html>`, `<body>`, and `<script>` tags properly.
*   Ensure the code is bug-free and ready to run immediately in a browser.
