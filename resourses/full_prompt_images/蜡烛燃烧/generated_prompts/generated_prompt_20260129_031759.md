### Project: 10-Second Melting Candle Animation

**Goal:**
Create a single, standalone HTML file that renders a realistic burning candle which melts completely over a duration of 10 seconds.

**Visual & Design Requirements:**
*   **Environment:** Dark, void-like background (black or very dark blue) to emphasize the light source.
*   **Candle Body:**
    *   White or cream-colored cylindrical shape.
    *   Rounded base and top edge.
    *   Subtle CSS shading/gradients to suggest 3D volume (cylindrical form).
    *   Visible black wick at the top center.
*   **Flame:**
    *   Multi-colored gradient (white/blue base, yellow core, orange/red tip).
    *   Dynamic shape that changes frame-by-frame.
    *   Outer glow effect to simulate light emission.

**Animation & Logic:**
1.  **Flame Physics:** Use HTML5 Canvas or complex CSS keyframes to create a "flickering" effect. The flame should move realistically (turbulence/wind simulation), not just a static pulse.
2.  **Melting Mechanic:**
    *   Upon load, the candle body height must smoothly decrease from 100% to 0% over exactly 10 seconds.
    *   The flame and wick must stay attached to the top of the candle body as it lowers.
    *   (Optional) Small wax drip particles or pooling effect at the base.
3.  **Termination:** Once the 10 seconds elapse and the candle is gone, the flame should extinguish (fade out).

**Technical Constraints:**
*   **Single File:** All HTML structure, CSS styling, and JavaScript logic must be contained within `index.html`.
*   **No Dependencies:** Do not use external libraries (no Three.js, no jQuery, no external images). Use native Canvas API or CSS3.
*   **Performance:** Animation should run smoothly at 60fps.

**Output Code Structure:**
Please provide the complete source code containing:
*   `<!DOCTYPE html>` declaration.
*   `<style>` block for layout, candle shape, and background.
*   `<script>` block for the flame rendering loop and melting countdown logic.
*   Correct logic to sync the flame's Y-position with the shrinking candle div/rect.
