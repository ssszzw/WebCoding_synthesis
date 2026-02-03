# Three.js 3D Particle Galaxy Prompt

Create a single-file HTML application rendering a 3D particle galaxy using Three.js.

### Visual Effects
*   **Background:** Deep black void.
*   **Central Galaxy:** A dense spiral structure composed of thousands of small, glowing pink/red particles arranging in logarithmic spirals.
*   **Nebula/Environment:** Surrounding the center, place large, semi-transparent, low-opacity spheres (bokeh effect) in muted greenish-grey tones to simulate depth and nebulas.
*   **Stars:** Scattered blue point particles filling the distant background.
*   **Style:** Sci-fi, abstract, high contrast. Use additive blending for particle glow.

### Animation & Interaction
*   **Motion:** The entire galaxy system should slowly rotate on the Y-axis.
*   **Controls:** Implement `OrbitControls` to allow:
    *   Mouse drag to rotate camera.
    *   Mouse wheel to zoom in/out.
*   **Responsiveness:** Canvas must resize automatically with the window.

### UI Overlay
*   **Position:** Fixed top-left corner.
*   **Title:** "3D Particle Galaxy" in bright Cyan/Teal (sans-serif, bold).
*   **Instructions:** "使用鼠标拖拽旋转视角，滚轮缩放" in smaller grey text below the title.

### Technical Implementation
*   **Library:** Use Three.js (via CDN) and OrbitControls (via CDN).
*   **Geometry:** Use `BufferGeometry` for particles to ensure performance with high counts (e.g., 5000+ points).
*   **Materials:** Use `PointsMaterial` with custom colors and opacity.
*   **Structure:** All code (HTML structure, CSS styling, Three.js logic) must be contained within a single `index.html` file.
