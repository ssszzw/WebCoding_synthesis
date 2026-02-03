# Role: Expert Creative Coder & WebGL Engineer

**Project:** Voxel_Ancient_Roman_City
**Format:** Single HTML File (Index.html)
**Dependencies:** NONE (No external CDNs, images, or libraries). All logic, shaders, and assets must be procedural and embedded.

---

## 1. Project Objective
Create a sophisticated, procedurally generated **Voxel Art Simulation of Ancient Rome** entirely within a single HTML file using **WebGL 2.0**. The scene serves as an interactive "living diorama" featuring a massive, detailed Colosseum as the centerpiece, surrounded by the Seven Hills, the Tiber River, and a bustling city center. The rendering must be highly optimized using geometry instancing to handle thousands of voxels at 60+ FPS.

## 2. Technical Architecture & Constraints
*   **Single File:** All HTML, CSS, and JavaScript must be contained in one file.
*   **Graphics Engine:** Write a **custom, lightweight WebGL 2.0 boilerplate** from scratch within the `<script>` tag. Do **not** try to embed a massive base64 library like Three.js. Implement only the necessary matrix math (lookAt, perspective, multiply), shader compilation, and buffer management required for voxel rendering.
*   **Rendering Technique:**
    *   Use **Hardware Instancing (`drawElementsInstanced`)**.
    *   Create a single "Cube" geometry.
    *   Pass instance data (Position `vec3`, Color `vec3` or UV `vec2`, Scale `vec3`) via attributes.
    *   **Hidden Surface Removal:** Ideally, implement a simple greedy meshing or simply do not render voxels completely surrounded by others to save performance.
*   **Assets:**
    *   **Textures:** Generate a Texture Atlas programmatically using an off-screen HTML `<canvas>` (e.g., a 4x4 grid of colored pixel patterns for marble, grass, dirt, roof tiles) and bind it as a texture.
    *   **Sound:** Optional, but if included, generate synthesized sound effects using the Web Audio API.

## 3. World Generation & Algorithms
The world must be generated procedurally on init:
1.  **Terrain (Geology):**
    *   Use a simple noise function (e.g., Value Noise or Perlin Noise implementation) to generate elevation maps.
    *   **Seven Hills:** Create rolling elevation changes.
    *   **Tiber River:** Carve a path through the mesh with water voxels (reflective/transparent shader).
    *   **Ground Palette:** Green (grass) on hills, Grey (cobblestone) for roads, Brown (dirt) for the arena.
2.  **City Planning (Logic):**
    *   **Grid System:** The world is a voxel grid (e.g., 128x128x64).
    *   **Zoning:**
        *   *Center:* The Colosseum (Fixed functionality).
        *   *Forum:* Temples with columns and triangular pediments.
        *   *Residential:* Insulae (apartments) stacked 3-5 voxels high with terracotta roofs.
    *   **Collision:** Maintain a simple 2D occupancy map to prevent buildings from overlapping.
    *   **Vegetation:** Scatter "Umbrella Pines" (tall trunks, flat green tops) and "Cypress" (thin, tall) on the hills.

## 4. The Colosseum (Hero Asset)
The Colosseum requires higher fidelity logic:
*   **Shape:** Elliptical generation algorithm.
*   **Structure:** External arches, internal tiered seating (Cavea), and the central arena floor.
*   **Sub-systems:**
    *   **Hypogeum:** An exposed maze structure beneath the arena floor.
    *   **Velarium:** A dynamic mesh of "fabric" voxels that can extend/retract.

## 5. Visual Fidelity & Shaders
*   **Lighting Model:** Implement a custom fragment shader.
    *   **Directional Light:** Controlled by the "Time of Day" system.
    *   **Ambient Occlusion:** Simple vertex-based AO or screen-space approximation if possible, otherwise simulate depth by darkening voxels lower in the Y-axis.
    *   **Atmosphere:** Change the background `clearColor` and fog density based on time (Pink Dawn -> Blue Day -> Orange Sunset -> Dark Blue Night).
*   **Water Shader:** The Tiber River and Naumachia water should oscillate slightly (vertex displacement) and be semi-transparent.

## 6. Interactive "Grand Spectacles" (UI Controls)
Create a minimalist, semi-transparent UI overlay (bottom-left) styled with a "Roman Marble" aesthetic.

**A. Time of Day Slider:**
*   Controls the sun/moon position (`u_lightDir` in shader).
*   **Night Logic:** When the sun sets, toggle an "Emissive" uniform for window voxels (yellow) and street torches (orange) to simulate a lit city.

**B. Event Buttons (State Machine):**
1.  **Naumachia (Naval Battle):**
    *   *Action:* Raise the water level in the Colosseum arena.
    *   *Visuals:* Spawn voxel ships (Triremes).
    *   *FX:* Simple particle system (points) for splashing water.
2.  **Velarium (Awning):**
    *   *Action:* Extend voxel "arms" and "cloth" inward from the Colosseum rim.
    *   *Visuals:* Casts a shadow over the seating area.
3.  **Circus Maximus (Race):**
    *   *Action:* In the distance or on a designated track, animate 4 colored blocks (Chariots) moving rapidly in a loop.
    *   *FX:* Trail particles (dust) behind them.
4.  **Triumphal Procession:**
    *   *Action:* A line of Gold and Red voxels (Legions) moves along the main road (Via Sacra) towards the Forum.
5.  **Festival of Lights:**
    *   *Action:* Force "Night Mode". Spawn floating lanterns (emissive voxels moving upwards) over the river. Launch "Fireworks" (particles exploding outward) above the Colosseum.

## 7. Camera & Controls
*   **God-Mode Camera:**
    *   Implement standard Orbit Controls logic (Mouse Drag to rotate, Right-click to pan, Wheel to zoom).
    *   Ensure the pivot point stays central to the city.

## 8. Implementation Steps (Code Structure)
1.  **CSS:** Reset, full-screen canvas, UI styling (absolute positioning, glassmorphism, Roman font).
2.  **JS Utility:** `Matrix4` class, `ShaderLoader`, `InputHandler`.
3.  **JS Engine:** `Renderer` class handling the WebGL context and Instancing setup.
4.  **JS World:** `VoxelWorld` class handling the data model (3D array).
5.  **JS Generator:** Functions to `generateColosseum()`, `generateTerrain()`, `placeBuilding()`.
6.  **JS Loop:** `requestAnimationFrame` handling time updates, animation state for events, and drawing the scene.

**Final Instruction:**
Write the complete, functional code. Ensure robust error handling (e.g., if a building can't find a spot, skip it). The result must be a visually stunning, high-performance voxel simulation that captures the grandeur of Rome.
