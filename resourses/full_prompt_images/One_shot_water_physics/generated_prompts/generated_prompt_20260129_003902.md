Create a fully interactive 3D water physics simulation in a single `index.html` file.

**Core Requirements:**
*   **Technology**: Use **Three.js** (loaded via CDN) for rendering. Use basic Euler integration or a lightweight physics setup for gravity/buoyancy.
*   **Structure**: Combine HTML, CSS, and JavaScript into one self-contained file.

**Visual & Scene Setup:**
1.  **Environment**: Soft blue sky background with a large, stylized sun/moon sphere in the distance.
2.  **Water Surface**:
    *   Large, highly subdivided plane geometry (e.g., 100x100 segments).
    *   Material: Light azure blue, high gloss/specular highlights, slight transparency.
    *   Shader/Animation: Dynamic vertex manipulation to simulate gentle idle waves and reactive ripples.
3.  **Lighting**: Ambient light plus a directional light to create specular reflections on the water waves.

**Physics & Interaction:**
1.  **Lemon Spawning**:
    *   **Input**: On mouse click (raycast to water plane).
    *   **Object**: Spawn a yellow, prolate spheroid (lemon shape) at the clicked X/Z position above the water.
    *   **Dynamics**: Object falls with gravity, hits the water surface, and floats/bobs with buoyancy.
2.  **Wave Interaction**:
    *   When a lemon hits the water ($y \approx 0$), trigger a radial ripple effect at that impact point.
    *   Propagate the ripple outward using a wave equation modifying the mesh vertices.

**UI Overlay:**
*   Create a clean, floating card in the top-left corner.
*   **Style**: Dark semi-transparent background (`rgba(0,0,0,0.7)`), rounded corners, white text, sans-serif font.
*   **Content**:
    *   Title: "Hydro Physics Lab" (Bold).
    *   Subtitle: "Fully interactive fluid simulation."
    *   Call to Action: "Click to drop a Lemon! 🍋" (Blue/accent color).

**Implementation Details:**
*   Ensure the render loop updates both physics (lemon positions, wave heights) and rendering.
*   Handle window resize events.
*   No external assets (images/textures); generate visual styles procedurally or via code.
