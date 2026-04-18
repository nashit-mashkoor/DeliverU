# DeliverU Landing Design Philosophy

This document defines the visual system for the DeliverU landing page. It is a tech-futurist, dark-base aesthetic anchored in signal, routing, and urban network metaphors. All front-end additions should align with this system to keep the experience cohesive.

## Core Intent

- Tone: nocturnal, signal-driven, precise, kinetic
- Visual metaphor: networked routes, glowing nodes, shared loops, ambient data flow
- Differentiator: the "route ribbon" motif threading through sections to unify the narrative

## Typography System

Use a distinct display font for headlines and a restrained, readable body font for long copy.

- Display: Oxanium (geometric, technical)
- Body: Sora (modern, stable)

Usage rules:
- Headline (hero): Oxanium, large scale, tight line height, subtle tracking
- Section titles: Oxanium, medium-large scale
- Labels and chips: uppercase, high letter-spacing, small size, muted color
- Body copy: Sora, moderate line height, balanced contrast

## Color System

Dark base with electric accents and soft glow. Avoid purple-on-white or flat gray cards.

Core variables (local to landing page CSS):
- --paper: base background
- --paper-deep: deeper background layer
- --surface: card surfaces, slightly translucent
- --surface-strong: deeper surface for high-contrast sections
- --ink: primary text color
- --accent: primary electric accent (cyan)
- --accent-deep: hover/deeper cyan
- --signal: secondary accent (magenta)
- --outline: subtle electric border
- --soft-shadow / --hard-shadow: depth and lift

Color rules:
- Use accent for primary CTA and key emphasis in headers.
- Use signal sparingly for standout cards or nodes.
- Keep surface contrast subtle; rely on glow and outline for depth.

## Motion System

Motion communicates signal flow and momentum, not playful bounce.

- Page-load: staggered fade-up reveals for sections
- Ambient: slow drift on the route ribbon
- Micro: CTA hover lift, card hover lift, glow intensifies on hover

Accessibility:
- Respect prefers-reduced-motion by removing ambient animations and transitions.

## Layout & Composition

- Asymmetry is intentional; avoid centered, overly balanced blocks.
- Overlap and depth: hero card and ribbon should feel layered.
- Use generous negative space; avoid overcrowding.
- The route ribbon is a visual through-line; it should appear behind primary sections.

## Component Recipes

Buttons:
- Primary: electric fill with dark text, glow and lift on hover
- Secondary: translucent dark surface with cyan outline
- Ghost: transparent with cyan border and soft hover

Cards:
- Dark translucent surfaces with thin cyan outlines
- Optional dashed borders for data chips and signal cards
- Subtle glow or shadow for depth

Chips / Badges:
- Uppercase text, high tracking, rounded pill shapes
- Low-saturation background with cyan border

Route Ribbon:
- Wide diagonal band with gradient shift and 3-4 glowing nodes
- Slow drift animation to suggest flow

## Do / Don’t

Do:
- Maintain the dark-base with electric accents
- Use glow and depth instead of flat surfaces
- Keep typography and spacing consistent with the system

Don’t:
- Introduce light UI patterns or white backgrounds
- Use generic system fonts or default buttons
- Add dense gradients or purple-on-white themes
