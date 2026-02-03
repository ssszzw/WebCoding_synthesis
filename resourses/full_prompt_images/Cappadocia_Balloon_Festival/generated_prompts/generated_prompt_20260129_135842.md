# Web Development Prompt: Interactive Cappadocia Balloon Festival

**Role:** Expert Creative Technologist / Three.js Developer
**Task:** Create a photorealistic, interactive 3D WebGL scene of the Cappadocia Hot Air Balloon Festival at dawn within a single HTML file.

---

### 1. Project Setup & Architecture
*   **File Structure:** Output a single `index.html` file containing HTML, CSS, and JavaScript. No external assets (images/models) or bundlers.
*   **Library Management:**
    *   Use an **Import Map** positioned before the main module script.
    *   Map `three` and `three/addons/` to a pinned CDN version (e.g., `https://unpkg.com/three@0.160.0/build/three.module.js`).
    *   Import specific modules via the map names (e.g., `import * as THREE from 'three';`).
*   **Code Quality:**
    *   Use strict ES6+ syntax.
    *   **Variable Naming:** Never reuse identifiers in the same scope (e.g., do not redeclare `material` five times; use `balloonMaterial`, `terrainMaterial`, etc.).
    *   **Structure:** Separate logic for `SceneInit`, `TerrainGenerator`, `BalloonManager`, and `InputHandler`.

### 2. Visual Style & Environment ("The Cappadocia Vibe")
*   **Atmosphere:**
    *   **Lighting:** Implement a dynamic lighting system based on a "Time of Day" parameter.
        *   *Pre-Dawn:* Deep blues/purples, minimal ambient light, heavy fog.
        *   *Sunrise:* Golden hour directional light, warm ambient light, long shadows.
        *   *Morning:* Bright, clear daylight, harsh shadows.
    *   **Sky:** Create a custom gradient background (using a large Sphere or Shader) that transitions colors smoothly based on the time slider.
    *   **Fog:** Use `THREE.FogExp2` to create depth. The fog color must blend seamlessly with the horizon color of the sky gradient.
*   **Terrain (Procedural Generation):**
    *   **Base:** A large `PlaneGeometry` with vertices displaced by a noise algorithm (simplex or perlin) to create rolling valleys.
    *   **Fairy Chimneys:** Procedurally generate the iconic rock formations.
        *   Use merged geometries (Cylinders for bases, Cones for caps) to form the "hoodoos".
        *   Scatter these clusters randomly but logically across the terrain.
    *   **Texture/Color:** Use vertex colors or procedural noise shaders to simulate sandstone, limestone, and terracotta textures. No external image textures.

### 3. The Balloons (Hero Objects)
*   **Construction:**
    *   **Envelope:** Use a modified `SphereGeometry` or `CapsuleGeometry` (tapered at the bottom).
    *   **Basket:** A small brown `CylinderGeometry` or `BoxGeometry` suspended below.
    *   **Connection:** Visually imply ropes/cables (can be simple lines or thin cylinders).
*   **Instancing (Technical Requirement):**
    *   Use `THREE.InstancedMesh` for the envelopes and baskets to handle 100+ balloons efficiently.
    *   **Variety:** Assign a unique random color/pattern to each balloon instance instance color attribute. Ensure high contrast between the colorful envelope and the brown basket.
*   **Burner Effect:**
    *   Place a `PointLight` and a small billboard sprite (or emissive mesh) inside the mouth of the balloon.
    *   Logic: The burner triggers intermittently (random intervals), casting an orange glow on the inside of the balloon fabric and increasing the balloon's upward velocity slightly.

### 4. Animation & Physics Simulation
*   **Movement Logic:**
    *   **Vertical:** Balloons must start at different states: some grounded, some lifting off, some at high altitude. Apply a sinusoidal "hovering" motion to airborne balloons.
    *   **Horizontal (Wind):** All balloons must drift based on a global `Wind Vector`.
    *   **Orientation:** Balloons should tilt slightly in the direction of the wind/movement.
*   **Lifecycle:** If a balloon drifts too far (out of bounds), reset it to a start position upwind to create an infinite loop of balloons crossing the valley.

### 5. Interaction & Controls (UI)
*   Implement **Lil-GUI** (imported via addons) with the following controls:
    *   **Time of Day (0.0 - 1.0):** Controls sun position, sky gradient colors, fog density, and ambient light intensity.
    *   **Wind Speed:** Modifies the drift velocity of the instances.
    *   **Wind Direction:** Rotates the drift vector (0-360 degrees).
    *   **Balloon Count:** A slider (re-initializes the InstancedMesh buffers upon change).
    *   **Camera Mode:** A dropdown or toggle:
        *   *Orbit:* Standard `OrbitControls` allowing the user to pan/zoom around the valley.
        *   *Ride Along:* Attaches the camera to a specific balloon (e.g., Balloon index #0). The camera should sit "in the basket," bobbing with the balloon, looking out at the horizon.

### 6. Performance & Rendering
*   **Target:** Maintain ≥60 FPS.
*   **Optimization:**
    *   Clamp `renderer.setPixelRatio` to a maximum of 2.
    *   Enable ShadowMap, but optimize shadow bias and map size (don't use 4k shadow maps).
    *   Use a single `requestAnimationFrame` loop.
    *   Ensure window resize events update the camera aspect ratio and renderer size.

### 7. Implementation Constraints
*   **HTML/CSS:**
    *   `body { margin: 0; overflow: hidden; }`
    *   Canvas must fill the screen.
    *   Loading overlay: visible until the scene is fully generated, then fades out.
*   **Code Structure:**
    *   Start with the Import Map.
    *   Follow with CSS styles.
    *   End with the `<script type="module">`.
    *   Inside the script, initialize the scene, generate geometry, setup GUI, and start the loop.

**Final Output Requirement:** Produce the complete, raw code block ready to be saved as `index.html`.
