# DeliverU Frontend Design System

This document defines the shared visual language for DeliverU. The refreshed direction is **Neon Control Room**: dark, technical, and operationally precise. The landing page and authenticated app should feel like one continuous product surface.

## Core Intent

- Tone: focused, kinetic, system-level confidence
- Visual metaphor: route telemetry, control panels, synchronized loops
- Memorable signature: animated telemetry sweep crossing route graph components
- Principle: one bold motif executed consistently beats many unrelated effects

## Typography

- Display: `Audiowide`
- Body/UI: `Exo 2`

Usage:
- Headlines: uppercase display style with tight line-height and moderate tracking
- Kicker labels: micro uppercase with high tracking and restrained contrast
- Body copy: readable technical tone, 1.65-1.8 line-height
- Numeric emphasis: display font for key metrics and telemetry values

## Color and Tokens

Global tokens live in `frontend/src/styles/theme.css`. Landing-specific tokens are scoped in `frontend/src/pages/Landing.css`.

Core palette:
- Base: deep navy-black layers (`--color-bg`, `--color-bg-deep`)
- Primary: electric cyan (`--color-primary`)
- Secondary accent: cool signal blue (`--color-signal`)
- Utility accent: amber (`--color-accent`) for hotspots and active nodes

Guidelines:
- Keep primary emphasis on cyan; amber is a sparse highlight, not a dominant fill
- Use translucent surfaces with subtle internal highlights for depth
- Build hierarchy through contrast + spacing, not heavy saturation everywhere

## Motion System

Motion communicates flow and system response.

- Entrance: staged reveal-up animation per major section
- Ambient: telemetry sweep and ticker movement only
- Interaction: controlled lift on cards/buttons and border/glow intensification
- Accessibility: `prefers-reduced-motion` must disable non-essential animation

Avoid playful bounce or excessive micro-interactions.

## Layout and Composition

- Strong asymmetry in hero (copy left, operations panel right)
- Structured sections with clear rhythm and spacing between content bands
- Panel-first composition: bordered, translucent modules over atmospheric background
- Maintain negative space around headings to preserve scanability

## Component Recipes

### Navigation
- Compact operational header with micro-label links
- Brand uses a simple geometric mark and display lettering

### Buttons
- Primary: bright cyan gradient with dark text and subtle inset depth
- Secondary/Ghost: dark translucent surface with cyan border
- All buttons use uppercase micro-copy with consistent tracking

### Data Cards
- Thin cyan borders with low-opacity dark fills
- Numeric value in display type, supporting label in compact uppercase
- Hover state lifts card by 2-4px with controlled shadow growth

### Operations Panel
- Includes route graph with active nodes and telemetry sweep animation
- Uses stacked status rows for immediate state scanning

## Landing Page Structure

`frontend/src/pages/Landing.jsx` should follow this sequence:
1. Hero + control panel
2. Telemetry ticker
3. Operations matrix metrics
4. Workflow timeline
5. Reliability signal cards
6. Final call to action

This order creates a clear narrative from promise -> evidence -> activation.

## App Surface Alignment

Authenticated pages (`Layout`, `Dashboard`, `Items`, `Auth`) should continue using shared tokens and preserve:
- dark translucent containers
- cyan border language
- uppercase utility labels
- restrained glow depth

If introducing new components, derive styles from existing tokens first.

## Do / Don't

Do:
- Keep visual density intentional and modular
- Reuse tokenized spacing, border, and shadow values
- Prioritize clear hierarchy for fast scanning

Don't:
- Introduce light-theme sections into the default experience
- Mix unrelated visual styles in the same page
- Revert to generic system fonts or default component kits
