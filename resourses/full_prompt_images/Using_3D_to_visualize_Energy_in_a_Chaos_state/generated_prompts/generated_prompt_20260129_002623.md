Create a standalone `index.html` file containing a 3D web visualization labeled "Chaos Energy Containment." The project uses **Three.js** to render a sci-fi scene of unstable energy.

### Visual & Functional Requirements

**1. Scene Atmosphere:**
*   **Background:** Deep void with a heavy, dark red fog/ambient glow, simulating a dangerous environment.
*   **Post-Processing:** Use `EffectComposer` with `UnrealBloomPass` to create an intense glow/neon effect for all geometries.

**2. Central Core (The Containment Target):**
*   **Geometry:** A complex, wireframe geodesic sphere (Icosahedron) in the center.
*   **Material:** Bright white/pale orange emissive wireframe.
*   **Animation:** Rapid, erratic rotation on multiple axes. Slight scaling pulsation.

**3. Chaotic Energy Rays (The "Chaos"):**
*   **Appearance:** Dozens of jagged, lightning-like lines radiating outward from the center sphere.
*   **Colors:** A mix of Cyan/Teal (`#00FFFF`) and Fiery Orange (`#FF4500`).
*   **Animation:** The vertices of these lines must jitter or displace randomly every frame to simulate electricity or unstable plasma. They should look like they are "cracking" the space around the core.

**4. Floating Debris:**
*   **Elements:** Small square particles or tetrahedrons scattered in the background.
*   **Animation:** Slow orbit or drift, influenced by the core's "gravity."

**5. UI Overlay (HUD):**
*   **Style:** CSS overlay, absolute positioning, sci-fi aesthetic.
*   **Content:** A red bordered box in the top-left corner.
*   **Text:** Monospace font (e.g., Courier New). Text: "STATUS: CRITICAL" (blinking) and "UNSTABLE CONTAINMENT FIELD".
*   **Color:** Red text and borders.

**6. Interaction:**
*   **Camera:** Implement `OrbitControls` (auto-rotate disabled by default) but allow user mouse interaction to rotate around the anomaly.
*   **Mouse Move:** Subtle parallax effect where the camera slightly pans based on cursor position.

### Technical Implementation

*   **Libraries:** Use CDN links for Three.js (r128 or compatible) and the necessary Post-Processing scripts (EffectComposer, RenderPass, ShaderPass, UnrealBloomPass).
*   **Performance:** Use `BufferGeometry` for the lightning lines to handle rapid vertex updates efficiently.
*   **File Structure:** Combine HTML, CSS, and JavaScript into a single file.
    *   `<style>` for the HUD and full-screen canvas reset.
    *   `<script>` containing the Three.js logic.

### Prompt for Code Generation

Generate the `index.html` code now. Ensure the code is complete, bug-free, and handles window resizing. The visual output must match the "Critical Energy" aesthetic described above.
