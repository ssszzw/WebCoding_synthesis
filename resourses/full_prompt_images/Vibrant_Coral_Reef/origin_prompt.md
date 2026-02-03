Prompt:
“Create a vibrant coral reef teeming with marine life.

Output a single HTML file that runs in a blank Chrome tab with no bundler. If you use Three.js, add an import map (before the module script) mapping "three" and "three/addons/" to the same pinned version, and import only via those names. Never reuse identifiers in the same scope — use descriptive variable names.

SCENE
An explosion of color and life. The focus is equally on FISH and coral.

Coral landscape:
- Varied terrain with coral formations, sandy patches, rocky outcrops
- Coral types: branching staghorn, brain coral, soft flowing coral, anemones
- Depth variation with shallow and deeper zones

Fish (the stars):
- Large schools of yellow tangs moving together using flocking behavior
- Parrotfish grazing on coral
- Clownfish in anemones
- Angelfish and butterflyfish with distinct patterns
- A large Napoleon wrasse
- One or two reef sharks patrolling
- Manta ray gliding through occasionally

Fish should be constantly moving and reacting to each other. High variety is essential.

Environment:
- Caustic light patterns dancing on the sand
- Bubble streams rising
- Bright, clear tropical water with good visibility

CONTROLS
- Free orbit/pan/zoom camera
- Fish population density slider (medium to very high)
- Reset camera to overview position

TECHNICAL
- Use BufferGeometry and InstancedMesh for fish schools
- Target ≥55 FPS
- Keep water clear and bright throughout”