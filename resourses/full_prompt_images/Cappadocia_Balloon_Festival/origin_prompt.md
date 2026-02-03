Prompt:
“Create the iconic Cappadocia hot air balloon scene at dawn.

Output a single HTML file that runs in a blank Chrome tab with no bundler. If you use Three.js, add an import map (before the module script) mapping "three" and "three/addons/" to the same pinned version, and import only via those names. Never reuse identifiers in the same scope — use descriptive variable names.

LANDSCAPE
Turkish fairy chimney rock formations - tall cone-shaped rocks with caps, carved cave dwellings visible, valley terrain. Warm sandstone and terracotta colors.

BALLOONS
80-100 hot air balloons in flight at various altitudes.

Requirements:
- All balloons must be visibly airborne and either rising or floating
- Each balloon envelope must be a different color/pattern from its basket
- Baskets should be brown wicker color, clearly distinct from the colorful envelope above
- Burner flames firing intermittently with orange glow
- Balloons at genuinely varied heights - some just lifted off, some very high

Sunrise light catching the balloon fabric. The scale of so many balloons against the unusual rock landscape.

CONTROLS
- Time of day slider (pre-dawn → sunrise → morning)
- Wind direction and speed (balloons drift accordingly)
- Balloon count slider
- "Ride along" camera (inside one basket, looking out at other balloons and landscape)
- Free orbit camera with reset to classic valley viewpoint

TECHNICAL
- Use InstancedMesh for balloons
- Target ≥55 FPS - adapt balloon count or detail if needed
- Clamp devicePixelRatio ≤ 2”