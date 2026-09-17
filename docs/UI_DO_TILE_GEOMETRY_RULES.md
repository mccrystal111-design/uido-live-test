# UiDo Tile Geometry Rules

## Master coordinate system

The UiDo tile uses a resolution-independent **1000 × 1000 master canvas**.

- Origin: **X=0, Y=0** at the top-left.
- Centre: **X=500, Y=500**.
- Coordinates are specified in master units, not device pixels.
- Implementations scale the master coordinates proportionally to the target device.

## Perimeter and ring

- Tile canvas: **100%**.
- Minimum perimeter safety margin: **5%** on every side (**50 master units**).
- Outer UiDo ring: **90%** of the tile canvas.
- The ring is the visual frame; it is not an arbitrary content boundary.
- Content should use the available interior space efficiently while avoiding visual collision with the ring.

## Grid

- Fine construction grid: **25 units**.
- Major construction grid: **100 units**.
- Grid is a construction/positioning layer and is not part of the production skin.

## Positioning

All key visual elements should be specified by explicit master coordinates where practical.

Example:

`Score icon centre: X=500, Y=190`

This coordinate is then scaled consistently for phone, Wear OS and Apple Watch implementations.

## Interaction

Visible artwork and touch targets are separate concepts. Touch targets may extend beyond the visible icon artwork to maintain reliable interaction on small screens.

## Master help control

The question-mark help control is a master UI element and should retain its defined position and visual treatment across tiles unless a deliberate system-level change is approved.

On watch interfaces, help is activated by a deliberate **2-second hold** to avoid accidental interruption during play.
