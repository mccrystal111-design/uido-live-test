# UiDo UI Blueprint v1.0

**Status: LOCKED**

This document is the source of truth for UiDo interface geometry and visual tokens. Do not infer layout, button dimensions, spacing, or component styling from older screenshots or prototypes.

## 1. Brand / visual foundation

- Primary logo: `assets/uido-logo-primary-exact.png`
- App logo: `assets/uido-logo-primary-transparent.png`
- Interface font: Space Grotesk
- Font weights: 300, 400, 500, 600, 700
- Design intent: clear, consistent, modern, intuitive, optimised for outdoor use, premium and focused.

## 2. Colour palette

| Token | Value | Use |
|---|---|---|
| UiDo Yellow | `#FFD600` | Primary / CTA |
| UiDo Green | `#0E3D2B` | Background |
| Green Light | `#1F8B46` | Highlights / selected |
| White | `#F9FAF9` | Text / icons |
| Charcoal | `#121212` | Panels / text |

## 3. Typography

Space Grotesk is used throughout the interface.

| Weight | Value |
|---|---:|
| Light | 300 |
| Regular | 400 |
| Medium | 500 |
| SemiBold | 600 |
| Bold | 700 |

## 4. Button styles

### Primary button
- Width: 320px
- Height: 56px
- Radius: 28px
- Text: 16px / 600
- Icon: 20px
- Horizontal padding: 24px
- Primary fill: UiDo Yellow
- Primary text: Charcoal

### Secondary button
- Width: 320px
- Height: 56px
- Radius: 28px
- Text: 16px / 600
- Icon: 20px
- Horizontal padding: 24px
- Outline: Green Light
- Text/icon: White

### Tertiary button
- Width: 320px
- Height: 56px
- Radius: 28px
- Text: 16px / 600
- Icon: 20px
- Horizontal padding: 24px
- Outline: White/neutral
- Text/icon: White

### Icon button
- Width: 56px
- Height: 56px
- Radius: 16px
- Icon: 24px
- Padding: 16px
- Minimum touch target: 44px; 56px preferred

### Disabled button
- Same geometry as its parent button style
- Opacity: 40%

## 5. Button states

- Normal: standard component styling
- Pressed: visually reduced/highlighted state without changing geometry
- Disabled: 40% opacity

## 6. Toggle / selection

### Three-way selection
- Front / Middle / Back
- Selected state: Green Light
- Unselected state: transparent/dark panel with neutral outline

### Two-way selection
- Auto / Manual
- Selected state: Green Light
- Unselected state: transparent/dark panel with neutral outline

## 7. Icon language

Core icon examples:
- Flag
- Wind
- Elevation
- Lie
- Aim / SmartPoint

Icons should remain simple, high-contrast and immediately legible outdoors.

## 8. Mobile screen layout

- Standard horizontal margin: 20px left/right
- Header: 100px
- Content area: flexible height
- Action area: 120px
- Minimum touch target: 44px
- Preferred touch target: 56px
- Screen padding / top-bottom reference: 20px

## 9. Spacing system

Use an 8px grid.

- 4px — tight
- 8px — XS
- 16px — S
- 24px — M
- 32px — L
- 48px — XL

## 10. Card / panel style

- Radius: 16px
- Padding: 20px
- Border: 1px
- Background: `#1A1A1A`

## 11. Design principles

1. Clear and consistent
2. Optimised for outdoor use
3. Minimal taps, maximum clarity
4. Premium, modern and focused
5. Every element supports better decisions

## Source-of-truth rule

The locked blueprint above takes precedence over previous screenshots, old prototype layouts, or inferred dimensions. Approved screen designs may specify where these components are placed, but must not silently redefine the component geometry or visual tokens.

Exact supplied image assets must be used unchanged unless the user explicitly approves a new asset.
