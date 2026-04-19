```markdown
# Design System Document: The Living Laboratory

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Living Laboratory."** 

This system bridges the raw, organic vitality of the soil with the clinical, high-precision world of Artificial Intelligence. Unlike standard agricultural software that feels utilitarian and cluttered, this system adopts an **Editorial High-End** aesthetic. We reject the "dashboard" look in favor of a "breathing" interactive experience.

To break the "template" feel, we utilize:
*   **Intentional Asymmetry:** Content is not always centered; it follows a sophisticated rhythmic flow inspired by premium editorial journals.
*   **Breathing Spaces:** Whitespace is not "empty"; it is a functional element that allows complex AI data to feel manageable and calm.
*   **Sequential Reveal:** Information is choreographed to fade in smoothly, preventing cognitive overload and mimicking the natural growth of a plant.

---

## 2. Colors & Surface Philosophy

The palette is rooted in ecological depth and technical precision. We use **Material Design 3** naming conventions but apply them with an editorial eye.

### Tonal Hierarchy
*   **Primary (`#0d631b`):** Represents the core ecological authority. Used for high-impact brand moments and primary actions.
*   **Secondary (`#005db7`):** The "Intelligence" layer. Used for data-heavy sections, AI insights, and technical feedback.
*   **Tertiary (`#734e00`):** The "Harvest" accent. Used sparingly for highlights, alerts, or vital notifications.
*   **Surface Foundation (`#efffdb`):** A soft, organic off-white that feels warmer and more premium than pure digital white.

### The "No-Line" Rule
**Explicit Instruction:** You are prohibited from using 1px solid borders to define sections. 
Boundaries must be created through:
1.  **Tonal Shifts:** Placing a `surface-container-low` (#e7fad2) card against a `surface` (#efffdb) background.
2.  **Negative Space:** Using the spacing scale to separate concepts.
3.  **Soft Shadows:** Extremely diffused, low-opacity ambient shadows.

### Glassmorphism & Textures
For floating panels (e.g., AI Diagnostic overlays), use the **Glassmorphism Rule**:
*   **Background:** `surface` at 70% opacity.
*   **Effect:** `backdrop-filter: blur(20px)`.
*   **Signature Texture:** Use subtle linear gradients for CTAs, transitioning from `primary` (#0d631b) to `primary_container` (#2e7d32). This adds "soul" and prevents the flat, "cheap" look of single-hex buttons.

---

## 3. Typography: The Editorial Voice

We utilize a high-contrast hierarchy to signal authority.

*   **The Display Scale (Space Grotesk):** Reserved for hero headers and impactful data points. It is bold, precise, and tech-forward. 
*   **The Body Scale (Inter/Roboto):** Optimized for high readability. Agriculture requires clarity; we use `body-lg` (1rem) as our standard to ensure accessibility in the field.
*   **Bilingual Balance:** When pairing 'Source Han Sans' (CN) and 'Roboto' (EN), ensure the Chinese characters have slightly increased line-height (1.6x) to match the visual weight of the Latin script.

| Role | Font Family | Size | Weight | Intent |
| :--- | :--- | :--- | :--- | :--- |
| **Display-LG** | Space Grotesk | 3.5rem | Bold | Hero Statements |
| **Headline-MD** | Space Grotesk | 1.75rem | Medium | Section Entrances |
| **Title-LG** | Inter | 1.375rem | Semi-Bold | Card/Module Headers |
| **Body-LG** | Inter | 1rem | Regular | Deep-read content |
| **Label-MD** | Inter | 0.75rem | Medium | Technical Metadata |

---

## 4. Elevation & Depth: Tonal Layering

Traditional drop shadows are too "digital." We achieve depth through **Physical Stacking**.

*   **The Layering Principle:** Treat the UI as layers of fine paper. 
    *   Base: `surface`
    *   Mid: `surface-container-low`
    *   Top (Active): `surface-container-highest`
*   **Ambient Shadows:** If an element must "float" (like a diagnostic modal), use a shadow color tinted with the brand green: `rgba(18, 31, 7, 0.06)` with a blur of `40px`. 
*   **The "Ghost Border":** For high-density data tables where separation is critical, use `outline_variant` (#bfcaba) at **15% opacity**. Never 100%.

---

## 5. Signature Components

### Buttons (The "Call to Action")
*   **Style:** Large, pill-shaped (`radius-full`).
*   **Primary:** Gradient from `primary` to `primary_container`. White text.
*   **Hover:** A subtle expansion of the gradient and a `4px` lift using an ambient shadow.
*   **Motion:** Use a damping effect (0.4s, cubic-bezier(0.25, 1, 0.5, 1)).

### Diagnostic Cards
*   **Style:** No borders. Background: `surface_container_low`. 
*   **Corner Radius:** `xl` (1.5rem) to evoke a friendly, modern tech feel.
*   **Interaction:** On hover, the background shifts to `surface_container_high`. Do not use a border change.

### The "Pulse" Indicator (AI Action)
*   For active AI processes, use a soft, breathing glow using the `secondary` (#005db7) color. A circular element that scales from 1.0 to 1.1 with a `20px` blur.

### Form Inputs
*   **Style:** "Understated Elegance." A filled style using `surface_variant` with a bottom-only indicator of 2px using `primary`. 
*   **Focus:** The bottom indicator expands slightly, and the background subtly brightens to `surface_bright`.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use sequential fade-in animations for all page loads (0.1s delay between elements).
*   **Do** allow images of crops and nature to bleed to the edges of containers.
*   **Do** use "Sticky" navigation that feels light and unobtrusive (Glassmorphic).
*   **Do** keep icons rounded (8px) and linear to match the tech-minimalist aesthetic.

### Don't:
*   **Don't** use standard "Select-all" checkboxes; use modern selection chips for a tactile feel.
*   **Don't** use pure black (#000000); use `on_surface` (#121f07) for better tonal harmony.
*   **Don't** use divider lines. If the content feels cluttered, increase the whitespace or shift the background tone.
*   **Don't** use "snappy" or "linear" animations. Everything must have a "damping" quality—smooth, organic, and weighted.

---
*Director's Final Note: Design for the farmer's eyes and the scientist's mind. Every pixel should feel intentional, every transition should feel like a breath.*```