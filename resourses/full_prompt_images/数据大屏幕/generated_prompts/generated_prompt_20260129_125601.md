# Role
Expert Frontend Developer & Data Visualization Specialist.

# Task
Create a single-file "2024 National Day Golden Week Tourism Data Smart Screen".
**Output:** One `index.html` file containing HTML, CSS, and JS. No external libraries (e.g., no ECharts, no D3). Use native Canvas API or SVG for charts.

# Visual & Layout Specifications
*   **Theme:** "Future Tech/Cyberpunk". Deep blue background (`#020617`), neon cyan/blue accents (`#00f2ff`, `#0ea5e9`), semi-transparent glass morphism panels.
*   **Typography:** Sans-serif, digital/monospace numbers. High contrast.
*   **Layout:** CSS Grid dashboard.
    1.  **Header:** Centered title "2024年国庆黄金周旅游数据智慧大屏", date range, background glow.
    2.  **Top Row:**
        *   **Left (Metrics):** 4 Cards. "Domestic Trips" (7.65亿), "Revenue" (7008.17亿), "Outbound" (10.3亿), "Per Capita" (2.03万).
        *   **Right (Map):** Stylized China map (SVG/Canvas). Dark silhouette, pulsing neon dots for hotspots (Beijing, Shanghai, Chengdu, etc.).
    3.  **Middle Row (Charts):** 3x2 Grid or Flex row.
        *   *Top 5 Provinces:* Vertical Bar Chart.
        *   *Transport Mode:* Stacked Bar or Icon chart.
        *   *Consumption Mix:* Donut Chart.
        *   *Hotel Occupancy:* Area/Line Chart (Curve).
        *   *Ticket Sales:* Horizontal Bar Chart.
        *   *Catering Growth:* Histogram.
    4.  **Bottom Row (Insights):** Text-based summary cards + "Regional Highlights" (Big number "9 Provinces").

# Technical Implementation
*   **Structure:** Semantic HTML5.
*   **Styling (CSS):**
    *   Flexbox/Grid for layout.
    *   `box-shadow` and `border-image` for glowing tech borders.
    *   `@keyframes` for pulse, scanlines, and fade-ins.
    *   Responsive scaling (using `rem` or `vh/vw`).
*   **Logic (JS):**
    *   **Data Object:** Store all 2024 metrics in a JSON-like structure.
    *   **Chart Engine:** Write a lightweight class to render Bars, Lines, and Donuts using HTML `<canvas>` or generating SVG strings dynamically.
    *   **Animations:**
        *   `CountUp`: Number rolling effect on load.
        *   `Grow`: Bars/Lines animate from zero.
        *   `Loop`: Subtle breathing glow on borders/map points.
    *   **Interactivity:** Hover effects on charts (show tooltips), hover effects on map points.

# Data Content (Simulated for 2024)
*   **Headline:** 7.65 Billion Person-Trips (Domestic).
*   **Revenue:** 7008.17 Billion RMB.
*   **Trend:** "Night Tourism" +25%, "Cultural Spots" +40%.
*   **Top Cities:** Chongqing, Beijing, Hangzhou, Chengdu, Changsha.

# Code Constraints
*   **Single File:** All CSS in `<style>`, all JS in `<script>`.
*   **Performance:** Use `requestAnimationFrame` for animations.
*   **Compatibility:** Modern Chrome/Edge/Firefox. No images—use CSS shapes or SVG data URIs.
