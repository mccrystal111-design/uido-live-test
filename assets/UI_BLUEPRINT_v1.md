# UiDo UI Blueprint v1.0

**Status: LOCKED**

This document is the source of truth for UiDo UI component dimensions and visual rules. Do not infer dimensions, spacing, positioning, or component styling from older screenshots, prototypes, or previous images unless this blueprint is explicitly updated.

## Brand
- UI font: Space Grotesk
- Primary yellow: #FFD600
- UiDo green: #0E3D2B
- Green highlight: #1F8B46
- White: #F9FAF9
- Charcoal: #121212

## Buttons
### Primary Button
- Width: 320px maximum on standard mobile layout
- Height: 56px
- Corner radius: 28px
- Text: Space Grotesk 16px / 600
- Icon: 20px
- Horizontal padding: 24px
- Purpose: primary action
- Normal: UiDo yellow background, dark text
- Pressed: same geometry with visually reduced brightness
- Disabled: muted grey with 40% content opacity

### Secondary Button
- Width: 320px maximum on standard mobile layout
- Height: 56px
- Corner radius: 28px
- Text: Space Grotesk 16px / 600
- Icon: 20px
- Horizontal padding: 24px
- Purpose: secondary action
- Normal: transparent/dark surface with green outline and light text

### Tertiary Button
- Width: 320px maximum on standard mobile layout
- Height: 56px
- Corner radius: 28px
- Text: Space Grotesk 16px / 600
- Icon: 20px
- Horizontal padding: 24px
- Purpose: low-emphasis action
- Normal: transparent/dark surface with light outline and light text

### Icon Button
- 56px × 56px
- Corner radius: 16px
- Icon: 24px
- Minimum touch target: 44px; preferred target 56px

## Selection / Toggle
- Selection controls use a clear selected state.
- Selected state uses UiDo green highlight where appropriate.
- Geometry must remain consistent between states.

## Cards / Panels
- Corner radius: 16px
- Padding: 20px
- Border: 1px
- Default dark panel background: #1A1A1A

## Spacing
Use an 8px base grid:
- 4px: tight
- 8px: XS
- 16px: S
- 24px: M
- 32px: L
- 48px: XL

## Mobile Layout
- Standard left/right margin: 20px
- Header zone: 100px reference height
- Bottom action zone: 120px reference height
- Content area: flexible
- Screen padding follows the 8px grid where practical.

## Design Principles
1. Clear and consistent
2. Optimised for outdoor use
3. Minimal taps, maximum clarity
4. Premium, modern and focused
5. Every element supports better decisions

## Implementation Rule
The blueprint defines component geometry and visual behaviour. Individual approved screens define component placement. Code implements both. Never use an old screenshot as an implicit layout specification.
