# Project: Interactive Seasonal Central Park Aerial View (Three.js)

**Objective:**
Develop a sophisticated, interactive 3D aerial visualization of Central Park in Manhattan using Three.js. The scene must simulate a seamless transformation between the four seasons, rendered within a single, self-contained HTML file. The application must optimize for performance (≥55 FPS) while maintaining high visual fidelity through custom shaders and instanced geometry.

---

### 1. Technical Architecture & Constraints
*   **Single File Output:** All code (HTML structure, CSS styling, JavaScript logic, and shader code) must be contained within a single `index.html` file. No external assets (images/models) requiring download; use procedural generation or Base64 data URIs if absolutely necessary (prefer procedural).
*   **Library Management:**
    *   Use an **Import Map** defined before the module script.
    *   Map `three` and `three/addons/` to a pinned CDN version (e.g., `https://unpkg.com/three@0.160.0/build/three.module.js`).
    *   Import only via these mapped names.
*   **Code Quality:**
    *   **Strict Variable Naming:** Never reuse identifiers in the same scope. Use descriptive, verbose variable names (e.g., use `cherryBlossomMaterial` instead of `mat1`, `reservoirGeometry` instead of `geo`).
    *   **Modularity:** Structure the code into logical functions or classes within the main script (e.g., `class SeasonalManager`, `function generateCityGrid()`).

### 2. Scene Composition & Visual Style

#### A. The View
*   **Perspective:** Aerial/Orbit view focusing on the rectangular "void" of nature amidst the dense Manhattan grid.
*   **Camera:** Implement an `OrbitCamera` that allows free rotation and zooming, but clamps polar angles to prevent going below ground level.

#### B. The Terrain (Central Park)
*   **Ground:** A textured plane representing grass and paths.
*   **Water Bodies:** specifically **The Reservoir** (large oval) and **The Lake**.
    *   *Shader Logic:* Water must reflect the sky. In Winter, the water roughness and color must shift to simulate a frozen/icy surface.
*   **Landmarks:** Create simplified but recognizable geometric representations for:
    *   **Bethesda Fountain:** Circular plaza structure.
    *   **The Mall:** Straight, wide tree-lined promenade.
    *   **Bow Bridge:** A subtle arch over the water.

#### C. The City (Surrounding Context)
*   **Grid System:** Procedurally generate a grid of building blocks surrounding the park rectangle.
*   **Building Appearance:**
    *   Grey/Concrete aesthetic to contrast with the park.
    *   **Window Logic:** Buildings must have a shader-based emissive property. As the "Time of Day" slider approaches night, or when the Season is "Winter" (late afternoon feel), windows should randomly light up (yellow/warm white).

### 3. The Seasonal System (Core Feature)
Implement a unified "Season Factor" (float 0.0 to 4.0) controlled by a UI slider. The transition must be handled via **GLSL Shaders** on the materials for smooth interpolation, not just swapping textures.

*   **0.0 - 1.0 (Spring):**
    *   *Trees:* Instanced meshes bloom with pink/white clusters (Cherry Blossoms) mixed with fresh light green.
    *   *Ground:* Vibrant, fresh green grass.
*   **1.0 - 2.0 (Summer):**
    *   *Trees:* Transition to deep, full canopy green. Foliage density appears highest.
    *   *Water:* Active fountains (simple particle systems).
*   **2.0 - 3.0 (Autumn):**
    *   *Trees:* Colors morph to Gold, Orange, Red, and Brown.
    *   *Effect:* A simple particle system showing falling leaves when in this range.
*   **3.0 - 4.0 (Winter):**
    *   *Trees:* Foliage opacity decreases to reveal bare grey branches (or geometry switches to bare branches).
    *   *Ground:* Shader creates a white noise/snow overlay on the grass and paths.
    *   *Water:* Transitions to white/blue-ish ice with high roughness.

### 4. Technical Implementation Details

#### A. Vegetation (Optimization)
*   **InstancedMesh:** You **must** use `THREE.InstancedMesh` for the thousands of trees required to fill the park.
*   **Custom ShaderMaterial:** The tree instances must use a custom shader that accepts a `uSeason` uniform. The shader calculates the color of the leaves based on the season value.
    *   *Vertex Shader:* Add slight wind movement (sine wave) that freezes in Winter.

#### B. Lighting & Atmosphere
*   **Time of Day:** A separate slider affecting:
    *   Sun position (DirectionalLight).
    *   Ambient light intensity and color (warm at noon, blue at night).
    *   Fog density and color.
*   **Shadows:** Enable soft shadows for the directional light.

### 5. User Interface (UI)
Create a minimalist overlay in the top-right corner using semantic HTML/CSS (absolute positioning).

*   **Controls:**
    *   **Season Slider:** Range input (Spring -> Summer -> Autumn -> Winter). Labels clearly visible.
    *   **Time of Day:** Range input (Dawn -> Noon -> Dusk -> Night).
*   **Navigation Buttons:**
    *   [Zoom to Reservoir]
    *   [Zoom to Bethesda Terrace]
    *   [Reset View]
*   **Stats:** Add a simple FPS counter in the corner (or use `stats.js` via CDN if compatible with import map logic).

### 6. Executable Instructions
1.  Initialize the Three.js scene, renderer, and camera.
2.  Create the `createPark()` function to generate the terrain and water.
3.  Create the `createCity()` function for the procedural buildings.
4.  Create the `createVegetation()` function using `InstancedMesh` with custom shaders for color interpolation.
5.  Implement the animation loop with logic to update uniforms based on UI inputs.
6.  Ensure responsive resizing logic is included.
7.  **Final Output:** Return only the valid HTML string code block.
