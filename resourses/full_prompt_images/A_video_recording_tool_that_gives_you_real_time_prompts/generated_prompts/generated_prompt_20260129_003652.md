# Role
You are an expert Frontend Developer and UI/UX Designer. Create a functional, single-file prototype of a "Real-time AI Video Journaling Tool" named "Sparks".

# Project Overview
Build a web-based video recorder where an AI "Host" displays dynamic prompts over the user's camera feed to guide their speech.

# Visual & UI Specifications
*   **Layout:** Clean, centered single-column layout. White background.
*   **Header:**
    *   Logo: Rounded square icon with pink-purple gradient and camera glyph.
    *   Title: "Sparks" in a bold, elegant serif font (e.g., Merriweather/Playfair).
    *   Subtitle: "CREATIVE VIDEO JOURNAL" in small, tracked-out sans-serif caps.
*   **Video Container:** Large, rounded rectangle (approx. aspect ratio 4:3 or 16:9) with soft drop shadow.
*   **Overlays (Z-Index High):**
    *   **Top Right:** "Recording" pill with blinking red dot and MM:SS timer.
    *   **Center:** "Glassmorphism" Prompt Card.
        *   Style: Translucent white background, `backdrop-filter: blur`, rounded corners, thin white border.
        *   Badge: Purple pill shape at top: "((•)) LIVE INTERVIEW".
        *   Text: Large, centered Serif font. Initial state: "Connecting to host...". Subsequent states: AI questions.
    *   **Bottom:** Control Bar.
        *   Left/Right: Mute and Camera toggle icons (outline style).
        *   Center: Large Record/Stop button. Active state: Red square inside a circle with a translucent red ripple/ring animation.

# Functional Specifications
1.  **Webcam Integration:** Use `navigator.mediaDevices.getUserMedia` to stream video to a `<video>` element. Handle permission errors gracefully.
2.  **Recording Logic:**
    *   Clicking the center button starts/stops the "recording" state.
    *   Start: Timer begins counting, "Live Interview" badge appears, prompts begin cycling.
    *   Stop: Timer resets, interface returns to idle.
3.  **AI Prompt Simulation:**
    *   Create an array of interview questions (e.g., "What was the highlight of your day?", "What are you grateful for?").
    *   When recording starts, show "Connecting to host..." for 2 seconds.
    *   Then, cycle through questions every 5-8 seconds with a smooth fade transition.
4.  **Animations:**
    *   Blinking red recording dot.
    *   Pulse/Ripple effect around the main record button.
    *   Smooth fade-in/out for prompt text changes.

# Technical Requirements
*   **Single File:** Combine HTML5, CSS3, and JavaScript into one `index.html`.
*   **Libraries:** Use Tailwind CSS (via CDN) for styling and Vue.js 3 (via CDN) for reactive logic. Use FontAwesome (via CDN) for icons.
*   **Fonts:** Import Google Fonts for the serif (e.g., 'Playfair Display') and sans-serif (e.g., 'Inter').
*   **Responsiveness:** Ensure the video container scales correctly within the viewport.

# Implementation Plan
Generate the complete code. Ensure the video feed actually works in a modern browser.
