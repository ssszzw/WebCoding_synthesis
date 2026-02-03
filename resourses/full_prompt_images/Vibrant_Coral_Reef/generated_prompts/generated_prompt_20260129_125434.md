# Role: Expert Creative Coder / 3D Web Developer

## Project: Vibrant_Coral_Reef (Single File WebGL Simulation)

You are tasked with creating a highly optimized, visually stunning 3D underwater simulation using **Three.js**. The entire project must be contained within a **single `index.html` file** containing HTML, CSS, and JavaScript.

### 1. File Structure & Library Imports
*   **Single File Constraint:** All logic, styling, and markup must exist in one file. No external CSS or JS files allowed.
*   **Module System:** Use ES Modules.
*   **Import Map:** You must include an `<script type="importmap">` block before your main script.
    *   Map `"three"` to a pinned, recent version (e.g., `https://unpkg.com/three@0.160.0/build/three.module.js`).
    *   Map `"three/addons/"` to the corresponding examples folder (e.g., `https://unpkg.com/three@0.160.0/examples/jsm/`).
    *   **Strict Rule:** Import only via these mapped names. Do not use absolute URLs in the main script.
*   **Code Quality:**
    *   **Naming Convention:** Never reuse identifiers in the same scope. Use descriptive, verbose variable names (e.g., `fishSchoolGeometry` instead of `geom`).
    *   **Structure:** Organize code into clear logical blocks: Setup, Environment Generation, Marine Life Systems, Animation Loop, and UI Handling.

### 2. Scene & Environment (Visuals)
Create an immersive underwater atmosphere focusing on clarity, brightness, and color.

*   **Lighting & Atmosphere:**
    *   **Fog:** Use `THREE.FogExp2` with a deep teal/blue color to simulate depth and distance.
    *   **Lighting:** Strong DirectionalLight (Sun) with shadows enabled. AmbientLight to ensure no completely black shadows.
    *   **Caustics:** Implement a custom shader or a projected texture animation on the sea floor to simulate light dancing through waves.
    *   **Particles:** A particle system simulating rising bubbles and floating "marine snow" (particulate matter) to add depth.
    *   **Background:** A gradient skydome or cube color matching the fog to create a seamless horizon.

*   **Coral Landscape (Procedural Generation):**
    *   **Terrain:** Use `PlaneGeometry` with displaced vertices (Perlin noise or random height variations) to create a seabed with dunes, rocky outcrops, and flat sandy patches.
    *   **Materials:** Procedural materials. Sand should have a grainy look; Rocks should be rough.
    *   **Coral Flora:**
        *   **Staghorn:** Branching geometries.
        *   **Brain Coral:** Hemisphere geometries with bump maps.
        *   **Soft Coral:** Vertical geometries that sway using a simple vertex shader (wind/water current simulation).
        *   **Anemones:** Clusters of small tube geometries.
        *   **Placement:** Scatter these procedurally but densely in "reef clusters," leaving open sandy "highways" for movement.

### 3. Marine Life System (The Stars)
This is the core of the experience. Performance is paramount.

*   **Geometry & Materials:**
    *   Use simple, low-poly geometries for fish (merged primitives) to maintain high FPS.
    *   Use vibrant colors. Differentiate species by color and scale.
    *   **Animation Technique:** **Do not** use Skeletal Animation (Bones). Instead, use a custom **Vertex ShaderMaterial** to bend the fish geometries along the Z-axis (sine wave based on time) to simulate swimming/tail-wagging. This is crucial for performance.

*   **Species & Behaviors:**
    1.  **Schooling Fish (Yellow Tangs):**
        *   **Implementation:** `THREE.InstancedMesh`. This is mandatory.
        *   **Behavior:** Implement the **Boids Algorithm** (Separation, Alignment, Cohesion). They must move as a fluid group, avoiding obstacles and the camera.
    2.  **Grazers (Parrotfish):**
        *   Move slowly near coral surfaces. Occasional "pecking" rotation.
    3.  **Residents (Clownfish):**
        *   Tethered to specific Anemone locations. They hover and dart within a small radius of their home.
    4.  **Wanderers (Angelfish / Butterflyfish):**
        *   Distinct striped patterns (using simple texture generation or vertex colors). Move in pairs or solitary.
    5.  **The Giants:**
        *   **Napoleon Wrasse:** Large scale, slow movement, distinct green/blue coloration.
        *   **Reef Sharks:** 1-2 instances. Faster movement, patrolling the perimeter or upper water column.
        *   **Manta Ray:** 1 instance. Moves using a slow, wide sine-wave vertex animation for wings. Glides overhead.

### 4. Technical & Performance Requirements
*   **Target:** Stable ≥55 FPS on average hardware.
*   **Optimization:**
    *   Use `THREE.BufferGeometry` for everything.
    *   Merge static geometries (coral/rocks) where possible to reduce draw calls.
    *   Use `InstancedMesh` for the Yellow Tang schools and bubble particles.
    *   Limit shadow map resolution to what is necessary (e.g., 2048x2048).

### 5. Interaction & UI (Controls)
*   **Camera:**
    *   Use `OrbitControls`.
    *   Limit polar angles so the camera doesn't go below the seabed.
    *   Enable damping for smooth movement.
*   **GUI:**
    *   Create a clean, semi-transparent HTML overlay (top-right corner).
    *   **Slider:** "Fish Density" (Range: Medium to Very High). This dynamically updates the `count` property of the InstancedMesh or visibility of fish arrays.
    *   **Button:** "Reset View". Smoothly interpolates the camera back to a cinematic starting position.

### 6. Implementation Summary
Write the complete code. The logic should follow:
1.  Initialize Three.js scene, camera, renderer.
2.  Generate textures/materials programmatically (canvas API or shaders).
3.  Build the static environment (Sand, Rocks, Coral).
4.  Initialize fish systems (Boids logic, Shader materials for swimming).
5.  Set up the animation loop (Delta time calculation, Update positions, Render).
6.  Attach Event Listeners (Resize, UI interactions).

**Output the full Markdown code block containing the single HTML file.**
