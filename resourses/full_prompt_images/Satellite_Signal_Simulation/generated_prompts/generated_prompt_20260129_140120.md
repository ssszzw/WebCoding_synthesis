# Role
You are an expert Frontend Developer and Creative Coder specializing in HTML5 Canvas, physics simulations, and interactive UI design.

# Task
Create a sophisticated, self-contained **Satellite Signal Simulation** web application. The application must simulate a satellite orbiting Earth, communicating with multiple ground stations. It requires realistic physics approximations for orbits and signal propagation, accompanied by a futuristic, data-rich user interface.

# Implementation Specifications

Please generate a single `index.html` file containing all HTML, CSS, and JavaScript. The code must be production-ready, error-free, and render immediately in a modern browser without external dependencies or assets.

## 1. Visual Design & Layout (HTML/CSS)
*   **Theme:** Sci-fi / Aerospace monitoring dashboard. Dark background (`#0b0d17`) with procedural starfield.
*   **Layout:**
    *   **Main Viewport:** A large central Canvas element occupying 70-80% of the screen for the visual simulation.
    *   **Control Panel (Left/Right Sidebar):** A semi-transparent "glassmorphism" panel containing simulation controls.
    *   **Data Log (Bottom or Sidebar):** A scrolling terminal-like log displaying transmission events in real-time.
*   **Styling:**
    *   Use monospace fonts (e.g., 'Courier New', 'Consolas') for data.
    *   Neon color palette: Cyan for active signals, Green for successful reception, Red for signal loss/interference, Amber for satellite path.
    *   Smooth transitions for UI hover states.

## 2. Core Simulation Logic (JavaScript)
*   **The Earth:** Placed at the center of the canvas. It should have a visual atmosphere (glowing gradient).
*   **The Satellite:**
    *   Follows an elliptical orbit around the Earth.
    *   **Orbital Mechanics:** Use simplified Keplerian physics (gravity point attraction) or a parametric ellipse equation to update position ($x, y$) based on time ($t$).
    *   Rotates to face the Earth (optional but adds realism).
*   **Ground Stations:**
    *   Place 3-4 static stations at fixed coordinates on the surface of the "Earth" circle.
    *   Each station has a unique ID (e.g., "GS-Alpha", "GS-Bravo").
    *   State: Idle, Receiving, Offline.
*   **Signal Propagation:**
    *   **Transmission:** The satellite emits a signal pulse every $X$ milliseconds (configurable).
    *   **Travel:** Signals are not instant. They must travel at a finite speed across the canvas pixels.
    *   **Distance Calculation:** Calculate Euclidean distance between Satellite and Station in real-time.
    *   **Signal Strength:** Implement a simplified Inverse Square Law ($Strength = P / Distance^2$).
    *   **Latency:** Display the calculated time it took for the signal to travel.
    *   **Interference/Loss:**
        *   Introduce a randomized "Atmospheric Noise" factor.
        *   If the satellite moves behind the Earth relative to a station (Line of Sight blockage), the signal must be lost immediately.
        *   Small random chance (e.g., 5%) of packet loss even with line of sight.

## 3. Visualization Details (Canvas API)
*   **Orbit Path:** Draw a faint trail or a dashed line showing the satellite's full orbital trajectory.
*   **Signal Visuals:**
    *   Represent signals as moving pulse waves (concentric arcs or glowing particles) traveling from Satellite to Stations.
    *   **Color Coding:**
        *   High Strength: Bright Green/White.
        *   Medium Strength: Yellow.
        *   Low Strength/Distorted: Red/Flickering.
*   **Telemetry Overlay:** Draw small text floating near the satellite showing current velocity or altitude.

## 4. Interaction & UI Features
*   **Dashboard Controls:**
    *   **Orbit Speed:** Slider to speed up or slow down time.
    *   **Transmission Rate:** Slider to change how often signals are sent.
    *   **Toggle Orbit:** Switch between Circular and Elliptical orbit paths.
*   **Real-time Data Logs:**
    *   When a station receives a signal, append a log entry: `[Timestamp] STATION_ID: Signal Rx | -45dBm | 124ms Latency`.
    *   If a signal is lost, log: `[Timestamp] Signal Lost: Obstruction/Interference`.
*   **Interactive Canvas:**
    *   Hovering over a Ground Station highlights it and shows a tooltip with its coordinates and total packets received.

## 5. Technical Constraints
*   **Single File:** All CSS (in `<style>`) and JS (in `<script>`) must be embedded within the `<html>` structure.
*   **Performance:** Use `requestAnimationFrame` for the simulation loop to ensure 60FPS.
*   **Responsiveness:** The canvas should resize correctly if the browser window is resized.
*   **No External Images:** Draw Earth, Satellite, and Icons using Canvas primitive shapes (`arc`, `rect`, `moveTo`, `lineTo`) only.

# Code Output
Please provide the complete code block below.
