Create a fully functional, single-file 2D vertical endless runner game named "Cute Roadrunner" using HTML, CSS, and JavaScript.

**Overall Description**
A minimalist, cute top-down arcade game where a pink character runs along a vertically scrolling path, dodging blue blocks and collecting coins. The aesthetic should be clean, bright, and pastel-colored.

**Visual Style & Assets (Canvas API)**
*   **Background:** White with vertical gray dashed lines creating a 3-lane road effect. Lines scroll down to simulate forward movement.
*   **Player:** A cute pink rounded rectangle with simple black eyes and a yellow flame/tuft on top. Must have a soft oval shadow underneath.
*   **Obstacles:** Cyan/Ice-blue rounded squares with a diagonal white reflection (glossy look). Includes shadow.
*   **Collectibles:** Gold coins that spin or float.
*   **UI:** Modern, rounded white panels with soft drop shadows at the top corners.
    *   Top Left: Gold Trophy Icon + "SCORE" + Current number.
    *   Top Right: "BEST" + High score number.

**Gameplay Mechanics**
*   **Controls:** Mouse movement or Touch drag to move the player left/right smoothly. Alternatively, use Arrow Keys. Player stays fixed vertically near the bottom.
*   **Core Loop:**
    *   Obstacles and Coins spawn at the top and move down.
    *   Game speed gradually increases.
    *   **Collision:** Hitting a blue block ends the game. Collecting a coin adds points.
*   **Persistence:** Save high score to `localStorage`.

**Technical Requirements**
*   **Single File:** Combine HTML, CSS, and JS into one `index.html`.
*   **Rendering:** Use HTML5 `<canvas>` for high performance.
*   **Responsiveness:** Canvas should fill the browser window or maintain a mobile-friendly aspect ratio centered on screen.
*   **Animations:** Smooth movement updates via `requestAnimationFrame`. Simple particle effect or pop animation when collecting coins.

**Output:** Provide the complete `index.html` code ready to run.
