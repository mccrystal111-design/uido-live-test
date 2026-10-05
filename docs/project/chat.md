# UiDo — Chat Error Capture / Visual QA Handover

## Purpose

This file exists to stop future chats repeating the visual translation errors that occurred during the Yardage v3 build.

**The visual source is authoritative. The assistant must not reinterpret it by eye and then repeatedly patch the HTML.**

Working chain:

**Figma visual definition → exact structured geometry → HTML implementation → rendered screenshot → visual/coordinate QA → live link**

Do not skip the rendered QA stage.

---

## Critical error captured from Yardage v3

### The coordinate-system mistake

Figma `get_design_context` reports positions **relative to the full 360×780 Figma frame**.

HTML elements placed inside `.top-ring` or `.bottom-ring` are positioned **relative to that ring**, not the full page.

Therefore every Figma coordinate must be explicitly converted before implementation.

For an element inside the top ring:

- Figma frame origin: `x=0, y=0`
- Top ring origin: `x=25, y=44`
- HTML child position must be:

```
child_left = figma_x - ring_x
child_top  = figma_y - ring_y
```

### Exact example that exposed the error

Figma:

- horizontal separator: `x=146, width=67, y=174`
- top ring: `x=25, y=44`

Correct HTML:

```
left = 146 - 25 = 121px
top  = 174 - 44 = 130px
```

The incorrect implementation used `left:146px`, producing an actual screen position of:

```
25 + 146 = 171px
```

So the line was 25px too far right.

The vertical separators had the same class of error on Y:

Figma:

```
y = 140
height = 120
```

Top ring:

```
y = 44
```

Correct HTML:

```
top = 140 - 44 = 96px
```

The implementation initially used `top:140px`, placing the lines 44px too low.

### Rule

**Never copy an absolute Figma frame coordinate directly into a child element inside a positioned HTML container.**

Build a small coordinate table first and show:

| Element | Figma X | Figma Y | Parent X | Parent Y | HTML left | HTML top |
|---|---:|---:|---:|---:|---:|---:|
| Top horizontal separator | 146 | 174 | 25 | 44 | 121 | 130 |
| Bottom horizontal separator | 146 | 233 | 25 | 44 | 121 | 189 |
| Left vertical separator | 128 | 140 | 25 | 44 | 103 | 96 |
| Right vertical separator | 231 | 140 | 25 | 44 | 206 | 96 |

Use this method for **every** positioned child, not only separators.

---

## Visual QA failure that must not repeat

A rendered screenshot was produced and inspected, but the inspection was effectively a visual sanity check rather than a true coordinate/pixel comparison.

The result looked plausible enough to pass an eyeball check even though the separators were systematically displaced.

### Therefore:

1. Render the actual HTML at the exact target viewport.
2. Inspect the rendered screenshot.
3. Compare against the Figma reference at the same dimensions.
4. Check important geometry numerically where possible.
5. Do not call visual QA complete just because the GitHub Action is green.
6. Do not send the live URL until the rendered artifact has actually been inspected.
7. If a geometry mismatch is found, identify the coordinate-system/reference-origin error before changing CSS.
8. Prefer one exact correction over a chain of visual patches.

**Green automation ≠ visually correct UI.**

---

## Figma source rules

The current authoritative product UI source is the Figma file:

**UiDo — Brand & Product Design System**

File key:

`6peEDBx1XNqpZ3UAeUlHyI`

Current Yardage source frame:

**UiDo Yardage — Source Recreation**

Node:

`8:24`

Frame:

`360 × 780`

Use the Figma design-to-code workflow and `get_design_context` for structured geometry.

The screenshot is a **QA reference**, not an implementation asset.

Do not recreate the design by visually guessing from the screenshot when structured Figma geometry is available.

---

## Current Yardage v3 reference

HTML:

`overstone/yardage-v3.html`

Current public URL:

`https://mccrystal111-design.github.io/uido-live-test/overstone/yardage-v3.html`

Visual QA workflow:

`.github/workflows/yardage-v3-visual-qa.yml`

Relevant completed v3 geometry correction:

`87db9aa236a034901ae03c1e474680f20b77320f`

The v3 build is the closest implementation so far. Do not rebuild it unnecessarily.

---

## Current settled visual geometry

Figma frame:

- Width: 360
- Height: 780
- Ivory background: `#f4f1e6`

Top outer ring:

- x: 25
- y: 44
- width: 309.6
- height: 309.6

Bottom outer ring:

- x: 25.2
- y: 425.94
- width: 309.6
- height: 309.6

Important yardage positions are defined by the Figma source. Preserve them rather than reinterpreting them.

### Do not casually change

- horizontal separator position
- ring geometry
- yardage hierarchy
- bunker layout
- page dots
- WIND control
- overall spacing
- ivory/green/yellow visual language

The user has explicitly been happy with the current design apart from identified geometry errors.

---

## Do not invent requirements

Experimental playground fields are **not automatically product requirements**.

In particular, do not infer that the final WIND control requires:

- compass heading
- wind speed in mph
- a wind gauge
- extra GPS controls

unless the current Figma/source definition explicitly specifies them.

The current Figma Yardage design shows a simple **WIND** control.

Likewise, do not replace the current BALL ICON text with a different graphic unless explicitly requested.

---

## UI/data relationship

For this development stage, the UI and the data are intentionally developed together.

Do not introduce an elaborate authoring abstraction merely to separate UI from data.

The goal is to remove **assistant interpretation**, not to add another translation layer.

---

## Failure modes to watch for

### 1. Absolute vs relative coordinates

Most important known failure.

Always calculate the parent-origin conversion.

### 2. “Looks close” QA

A 20–50px systematic error can still look plausible in isolation.

Use actual coordinates and overlays/diffs where possible.

### 3. Desktop scaling

The target is a 360×780 phone composition.

Do not judge only from a desktop browser view.

### 4. Screenshot-only implementation

Do not use a Figma screenshot as the implementation asset.

Use structured Figma geometry and existing local assets.

### 5. Blind patching

If the output is visually wrong, do not keep nudging arbitrary CSS values.

First identify:

- reference coordinate system
- parent coordinate system
- actual rendered coordinate
- required correction

Then make the smallest justified change.

### 6. Automated QA false confidence

A successful Playwright run proves that the page rendered and the test completed.

It does **not** prove that every visible element matches the visual source.

### 7. Sending a link too early

Never send the user a “ready” URL before inspecting the actual rendered artifact.

---

## Required QA checklist for future visual builds

### Before coding

- [ ] Load the Figma design-to-code skill
- [ ] Get structured Figma design context
- [ ] Confirm frame dimensions
- [ ] Record parent/container origins
- [ ] Convert absolute Figma coordinates to local HTML coordinates
- [ ] Inspect existing assets before creating replacements
- [ ] Do not invent unspecified requirements

### After coding

- [ ] Render at the exact target viewport
- [ ] Capture the actual rendered page
- [ ] Inspect the screenshot
- [ ] Compare key coordinates with Figma
- [ ] Check rings
- [ ] Check text anchors
- [ ] Check yardages
- [ ] Check bunker values
- [ ] Check vertical separators
- [ ] Check horizontal separators
- [ ] Check WIND control
- [ ] Check page dots
- [ ] Check bottom BALL ICON position
- [ ] Check for clipping/overflow
- [ ] Check for accidental scaling or desktop-layout behaviour

### Before giving the user the URL

- [ ] Relevant visual QA workflow is green
- [ ] Rendered screenshot/artifact has been inspected
- [ ] Any geometry mismatch has been resolved
- [ ] No unrelated workflow failures are being treated as evidence against the page
- [ ] Only then provide the live URL

---

## Working principle

**Do not ask the user to keep correcting things that can be measured from the source.**

If Figma says an element is at a specific coordinate, implement that coordinate correctly.

If the rendered screenshot disagrees, diagnose the transformation between source coordinates and rendered coordinates.

Do not guess.

**Source → measured implementation → rendered evidence → correction.**

That is the error-capture process this file is intended to preserve.
