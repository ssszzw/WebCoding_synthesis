# Web-based Pixel Art Editor Prompt

Create a single-file `index.html` containing a fully functional Pixel Art Editor with the following specifications.

### 1. Visual Style & Layout
*   **Theme:** Dark blue gradient background (`#2c3e50` to `#34495e`). Modern, flat UI.
*   **Header:** Title "🎨 像素画板 (支持回放/GIF)" centered at the top, white text.
*   **Toolbar:**
    *   Located above the canvas.
    *   Container: Dark, semi-transparent background, rounded corners, padding.
    *   **Elements:**
        1.  Color Picker: Square swatch showing current color (default black).
        2.  "Undo (Ctrl+Z)" Button: Blue style.
        3.  "Clear" Button: Danger/Gray style.
        4.  Divider (vertical line).
        5.  "Playback" Button: Icon + Text.
        6.  "Export GIF" Button: Icon + Text.
*   **Canvas Area:**
    *   Centered square canvas.
    *   Background: Checkerboard pattern (light gray/white squares) to represent transparency.
    *   Grid size: Default 32x32 pixels.
    *   Rendering: Crisp edges (`image-rendering: pixelated`).

### 2. Core Functionality
*   **Drawing Engine:**
    *   HTML5 Canvas API.
    *   Mouse interaction: Click or drag to paint pixels.
    *   Dynamic cursor highlighting the target pixel.
*   **State Management:**
    *   Record every pixel change (coordinate + color) into a history stack.
    *   **Undo:** Revert last action using the history stack. Support `Ctrl+Z` shortcut.
    *   **Clear:** Reset canvas and history.

### 3. Advanced Features
*   **Playback Mode:**
    *   Button click triggers a function to clear the canvas and redraw the history stack sequentially with a small delay (e.g., 50-100ms) between steps to animate the creation process.
*   **GIF Export:**
    *   Button click converts the drawing history into an animated GIF.
    *   Include a CDN link for a GIF generation library (e.g., `gif.js` or `gifshot`) within the HTML.
    *   The GIF should animate the drawing process (similar to Playback) or export the final frame if preferred, but "Playback" implies the GIF shows the process.
    *   Trigger browser download upon completion.

### 4. Technical Requirements
*   **Structure:** Single `index.html` file.
*   **CSS:** Internal `<style>` block. Flexbox for layout. Responsive design.
*   **JS:** Internal `<script>` block. No external local dependencies (use CDNs if needed).
*   **Performance:** Optimized canvas rendering. Handle array manipulation for history efficiently.

### 5. Implementation Steps
1.  **Setup HTML:** Container, Canvas, Toolbar controls.
2.  **CSS Styling:** Apply the dark blue theme, button styles (hover effects, transitions), and checkerboard canvas background using CSS `linear-gradient`.
3.  **JS Logic:**
    *   Initialize grid and context.
    *   Event listeners: `mousedown`, `mousemove`, `mouseup` for drawing.
    *   `addToHistory(x, y, color)` function.
    *   `undo()` function popping from history array.
    *   `playback()` function using `setInterval` or `requestAnimationFrame` to iterate through history.
    *   `exportGIF()` integration using the external library to capture frames and download.
