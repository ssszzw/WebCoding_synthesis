# 3D Voxel Floating Island Scene Generator

## Objective
Create a single-file HTML application (`index.html`) that renders a beautiful 3D voxel art scene using Three.js. The scene must depict a floating island with a cherry blossom (Sakura) tree, matching the aesthetic of the provided reference image.

## Visual & Design Requirements
*   **Style:** Voxel art (cubes). Soft, pastel color palette. Low-poly aesthetic.
*   **Central Subject:** A floating landmass with a large pink tree.
    *   **Tree:** voluminous canopy of pink and rose-colored voxels; twisted dark brown trunk.
    *   **Island:** Top layer of green grass voxels; uneven, tapered bottom layer of grey/brown rock voxels.
    *   **Waterfall:** A stream of light blue/white voxels cascading from the island edge, breaking into scattered blocks near the bottom.
*   **Atmosphere:**
    *   **Background:** Solid pastel peach/cream color (e.g., `#FBEFE9`).
    *   **Lighting:** Soft ambient light + directional light casting soft shadows. Use Fog to blend distant elements into the background.
    *   **Particles:** Small floating pink voxels simulating falling petals and pollen.

## Technical Implementation
*   **Libraries:** Load `Three.js` and `OrbitControls` via CDN (unpkg or cdnjs).
*   **Geometry:** Use `BoxGeometry` for all elements. Optimize performance using `InstancedMesh` for the thousands of cubes (leaves, dirt, stone).
*   **Procedural Generation:**
    *   Generate the island shape using a noise function or pseudo-random radius algorithm to create a natural, tapered underside.
    *   Generate the tree canopy as a sphere or semi-random cloud of blocks around the branch ends.
*   **Animation:**
    *   **Levitation:** The entire island should bob slowly up and down (sine wave).
    *   **Particles:** Petals slowly drift downward and fade/respawn.
    *   **Camera:** Slow auto-rotation around the scene.

## User Interaction
*   **Controls:** Mouse interaction to rotate, zoom, and pan (OrbitControls).
*   **Responsiveness:** Canvas must resize automatically with the browser window.

## Output Structure
*   Provide **one single `index.html` file** containing all HTML structure, CSS styling, and JavaScript logic.
*   Do not rely on external image assets; use VertexColors or basic materials.
*   Ensure the code is bug-free and renders immediately upon opening.
