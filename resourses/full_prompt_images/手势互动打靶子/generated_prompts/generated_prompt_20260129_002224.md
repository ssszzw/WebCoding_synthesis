# Role
Expert Web Game Developer (Three.js & Computer Vision focus).

# Objective
Create a single-file `index.html` AR gesture shooting game using Three.js and MediaPipe Hands. The game must track the user's hand to control a crosshair and destroy flying targets.

# Technical Specifications (Critical)
1.  **Dependencies:**
    *   Three.js (CDN).
    *   MediaPipe Hands: **Strictly pin** to version `0.4.1646424915` via unpkg to prevent WASM crashes.
    *   Camera Utils: MediaPipe Camera Utils.
2.  **Architecture:**
    *   **Single File:** All HTML, CSS, and JS must be within one file.
    *   **Loading Safety:** Implement a full-screen "Loading AI Model..." overlay. Do not start the game loop until MediaPipe is fully initialized.
    *   **Performance:** Decouple rendering (60fps) from AI detection (throttle to ~30fps or 50-100ms intervals).
    *   **Error Handling:** Wrap gesture recognition in `try-catch` blocks.

# Visual & Gameplay Requirements

### 1. Visual Style
*   **Perspective:** First-person view. Background is black (or subtle dark gradient).
*   **PIP:** Display the raw webcam feed in a small picture-in-picture box (bottom-right) for debugging/feedback.
*   **UI Elements:**
    *   **Crosshair:** Cyan/White circular reticle with a center dot.
    *   **Laser:** Semi-transparent line connecting the bottom-center of the screen to the crosshair.
    *   **Score:** Simple score counter in top corner.

### 2. Core Mechanics
*   **Gesture Control:**
    *   **Aiming:** Map the Index Finger Tip (Landmark 8) x/y coordinates to the screen cursor.
    *   **Firing:** Detect a "Pistol" gesture. "Fire" event triggers when the Thumb Tip (Landmark 4) moves quickly closer to the Index MCP (Landmark 5) or creates a distinct "trigger" motion.
*   **Target System:**
    *   **Enemies:** 3D Disc/Coin geometries (Cyan/White neon style).
    *   **Spawning:** Random locations at screen edges.
    *   **Movement:** Fly towards the screen center (0,0,0).
    *   **Logic:** Maintain exactly 4 targets onscreen. Immediate respawn upon hit.
*   **Aim Assist:** "Magnetic" cursor effect. If the reticle is near a target, slightly snap the crosshair position to the target center.

### 3. Feedback & VFX
*   **Hit Impact:**
    *   Target shatters or scales down rapidly to zero.
    *   Particle explosion effect (Three.js Points).
*   **Floating Text:** Show "HIT! +100" (Yellow/Gold font) at the impact location, floating upward and fading out.
*   **Audio:** Synthesize sound effects using `window.AudioContext` (no external assets):
    *   High-pitch "pew" for shooting.
    *   Crunchy noise for hits.

# Code Structure Implementation
Generate the complete `index.html` containing:
1.  **CSS:** Reset, full-screen canvas, loading overlay styles, UI positioning.
2.  **HTML Structure:** Canvas container, video element (hidden), loading div.
3.  **JS Logic:**
    *   `init()`: Setup Three.js scene, camera, renderer.
    *   `loadMediaPipe()`: precise version loading and configuration.
    *   `gameLoop()`: Animation frame for rendering.
    *   `detectHands()`: Throttled AI processing.
    *   `TargetManager`: Class to handle spawning, movement, and collision.
    *   `AudioManager`: Simple oscillator-based SFX.

**Output the full, executable code now.**
