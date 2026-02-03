Create a standalone `index.html` file containing a Three.js procedurally generated voxel art scene titled "Autumn Walk".

### Visual Style & Atmosphere
- **Aesthetic:** Voxel art (Minecraft-style). All geometry consists of simple cubes.
- **Palette:** Autumn colors. Leaves in varying shades of red, orange, and gold. Dark brown tree trunks. Green blocky ground.
- **Lighting/Sky:** Warm, hazy orange background (`#ffaa55` approx) with matching exponential fog to hide the horizon. Soft ambient light and directional sunlight casting shadows.

### Scene Components
- **Terrain:** Infinite procedural ground plane made of green voxels.
- **Vegetation:** Voxel trees generated randomly.
  - Trunks: Vertical stack of brown blocks.
  - Foliage: Clustered arrangement of colored blocks (red/orange/yellow) atop trunks.
- **Particles:** Falling autumn leaves (small flat squares) that drift down with slight rotation and wind sway, resetting position upon hitting the ground.

### Technical Implementation
- **Library:** Use `three.min.js` via CDN (e.g., cdnjs).
- **Optimization:** Use `THREE.InstancedMesh` for rendering ground blocks, tree parts, and leaves to ensure 60FPS performance.
- **Generation Logic:** As the camera moves, generate new chunks/rows of terrain and trees ahead, and remove those far behind (infinite illusion).

### Interaction & Animation
- **Camera:** First-person perspective at eye level.
- **Movement:**
  - **Auto-Walk:** Clicking "Start Walk" moves the camera forward automatically at a steady pace.
  - **Manual:** WASD keys to override movement. Mouse to look around (FirstPerson/PointerLock controls).
- **UI Overlay:**
  - Top Left: Title "Autumn Walk" and subtitle "An infinite procedural voxel forest".
  - Bottom Left: Instructions "MOUSE to look around", "WASD to move".
  - Bottom Right: "START WALK" button with a play icon.

### File Structure
- **Single File:** Merge all HTML structure, CSS styling, and JavaScript logic into one valid `index.html`. No external texture or model dependencies.
