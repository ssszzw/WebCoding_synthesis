Please help me write a single-file HTML AR gesture shooting game.

1. Core gameplay:

- Gesture: Recognize a “pistol” hand gesture (index finger aiming, thumb pulling the trigger to shoot).

- Enemies: Flying discs spawn randomly around the edges of the screen and fly toward the center. Keep 4 on screen at all times; when one is shattered, immediately spawn a replacement.

- Experience: Include magnetic aim assist (crosshair snaps/attracts to discs), a laser aiming line, hit impact sound effects, and floating “HIT/MISS” text VFX.

2. Critical anti-crash requirements (must implement):

- Use Three.js and MediaPipe Hands.
- Hard version lock: MediaPipe resources must be loaded from unpkg and pinned to version 0.4.1646424915 to prevent WASM version mismatches that cause crashes.
- Crash-safe loading: Add a full-screen Loading overlay; you must wait until the model finishes downloading before entering the game. The gesture-recognition loop must be wrapped in try-catch for protection.
- Performance: Limit the AI detection frequency, while keeping rendering running at a full 60 FPS.