# Figma-to-Browser Visual QA Standard

**Status:** Process specification  
**Applies to:** All kite and UiDo browser-rendered product screens, prototypes, and reusable UI components  
**Purpose:** Ensure implemented pages faithfully reproduce approved Figma designs, especially critical geometry such as rings, yardage values, bunker indicators, spacing, and control alignment.

## 1. Core principle

Figma is the approved visual source of truth. Code must be checked against the approved Figma frame; it must not be judged only by the developer's interpretation or by whether it looks plausible in isolation.

A page is not visually approved until:
1. The exact approved Figma frame and version are identified.
2. The implementation is rendered in a real browser at a matching viewport.
3. The render is compared against the reference using both geometry checks and visual inspection.
4. Differences are corrected and the page is rendered and checked again.
5. The evidence and any accepted exceptions are recorded.

Do not report that a page matches Figma unless the comparison has actually been performed.

## 2. Reference package

For each screen, retain:
- Figma file URL, page/frame name and exact node ID.
- Approved frame dimensions and intended device/viewport.
- Exported reference image from that exact frame.
- Geometry manifest for critical layers (section 4).
- Dynamic-content exclusions and approved deviations.
- Reference export revision/date.

Do not use a visually similar frame, an old screenshot, or a prior implementation when a newer frame has been approved. Do not edit master/reference frames to make them agree with code. If the design changes, update the reference package deliberately and record the change.

## 3. Standard QA sequence

### Step 1 — Identify the target

Record the Figma file, page, frame name and node ID; reference image and revision; viewport width/height and device scale factor; screen state to render; and which values are fixed versus dynamic.

If the target is ambiguous, stop and resolve it before implementation.

### Step 2 — Inspect Figma layers and measurements

Use actual Figma layer properties and hierarchy wherever available. Capture:
- X/Y position relative to the frame.
- Width and height.
- Centre point where alignment matters.
- Stroke width/alignment, fill colour, opacity and corner radius.
- Typography: font family, weight, size, line height, letter spacing and text alignment.
- Shadows and other effects.
- Parent/child relationships, constraints and layout behaviour.

Do not estimate from a screenshot if properties can be retrieved directly. Figma coordinates and browser CSS boxes are not always directly equivalent: strokes, font metrics, transforms, shadows and device-pixel rounding can affect visible pixels. Use layer measurements as constraints, then validate the visible browser result.

### Step 3 — Implement from the specification

- Prefer shared, reusable components for recurring UI elements.
- Keep critical geometry and styling explicit and understandable.
- Avoid unexplained offsets and repeated one-off overrides.
- Preserve the intended hierarchy and alignment relationships.
- Separate dynamic data from fixed layout.
- Do not alter the reference to fit the implementation.

For a ring with a changing yardage, the ring geometry should be independently stable and the number aligned by a defined centre/baseline rule, not a hand-tuned position that works for only one string.

### Step 4 — Render the actual page

Use the repository's Playwright/Chromium infrastructure to render the implementation in a real browser.

The generic rendering process must support any configured HTML page, not just AG45 or a particular prototype. It should be manually invokable and must not trigger existing GitHub Actions or deployments unintentionally.

For each test:
- Serve the intended page and assets from a predictable local URL.
- Use the reference viewport dimensions and documented device scale factor.
- Wait for fonts, images, SVGs and other essential assets to load.
- Set deterministic screen state and test data.
- Capture viewport and, where useful, full-page screenshots.
- Record console errors, uncaught page errors, failed requests and horizontal overflow.
- Record actual DOM bounds for elements with stable QA selectors.
- Save outputs as CI artefacts or in the agreed QA output location.

A successful browser launch is not proof of visual correctness. It only establishes that a render was produced.

### Step 5 — Compare geometry

For critical elements, compare browser measurements against the geometry manifest. Add stable data-qa attributes to elements that must be measured; avoid brittle selectors based on incidental DOM nesting.

At minimum, measure:
- Main ring: position, diameter, centre and stroke.
- Yardage value: bounding box, visual centre/baseline and alignment to the ring.
- Front/middle/back yardages: relative position and spacing.
- Bunker indicators: diameter, centre, spacing and relation to the main ring and surrounding content.
- Header and bottom controls: position, size, spacing and edge insets.
- Other elements explicitly marked critical in the screen manifest.

Suggested starting tolerances for a 360 × 780 CSS-pixel viewport (calibrate against actual browser/Figma exports):

| Property | Suggested initial tolerance |
|---|---:|
| Critical element X/Y position | ±1 CSS px |
| Critical element width/height | ±1 CSS px |
| Centre-to-centre alignment | ±1 CSS px |
| Non-critical spacing | ±2 CSS px |
| Colour | Exact token/value where defined; otherwise inspect rendered difference |
| Typography and shadows | Automated checks plus visual review |

These are starting points, not a claim that all browsers or Figma exports will be pixel-identical. Document adjusted tolerances and why. Do not loosen tolerances merely to make a failing page pass.

### Step 6 — Compare images

For the same viewport and state, generate:
1. The Figma reference.
2. The Chromium screenshot.
3. A semi-transparent overlay.
4. A difference image highlighting changed pixels.

Inspect the overlay for doubled edges, shifted centres, changed dimensions and inconsistent spacing. Inspect the difference image for typography, antialiasing, stroke, shadow, colour and icon differences.

A single global pixel-difference score is insufficient. Small font antialiasing differences can inflate it, while a small but important ring shift can be hidden in a mostly matching screen. Report geometry failures separately from pixel-difference metrics.

### Step 7 — Handle dynamic content correctly

Dynamic content is allowed to differ in value, not layout. Examples include yardages, GPS coordinates, wind readings, player names, scores and changing statistics.

- Use deterministic test fixtures where possible.
- Compare stable geometry and alignment independently from the value.
- Mask only the glyph/pixel area that genuinely changes, or normalise text for image comparison.
- Continue checking the containing component, ring, padding, alignment and surrounding layout.
- Test representative strings where width can change (for example 9, 99 and 199).

Never mask an entire ring, card, row or screen area because a value inside it changes. Record every mask and its reason.

### Step 8 — Fix, rerender and verify

For each failure:
1. Identify the exact mismatch and affected Figma layer/component.
2. Make the smallest targeted change.
3. Rerun the same viewport and state.
4. Recreate the screenshot, overlay, difference image and geometry report.
5. Check that the fix resolves the original issue without introducing new ones.

Do not stop after the first screenshot or after a CSS change that has not been rerendered.

### Step 9 — Record the result

Each QA run should report:
- Target frame and revision.
- Page URL/path and test state.
- Viewport and browser/device scale factor.
- Pass/fail for each critical geometry assertion.
- Browser errors, failed requests and overflow findings.
- Screenshot, overlay and difference-image artefacts.
- Dynamic masks and accepted deviations.
- Outstanding defects and the person/decision responsible for accepting exceptions.

## 4. Geometry manifest

Keep critical geometry in a small machine-readable manifest per screen (JSON or another repository-standard format). The manifest should reference exact Figma node IDs and define expected values, measurement strategy and tolerance.

Illustrative template only — values must be extracted from the approved frame, not copied from this example:

    {
      "screen": "Kite — Yardage — Tee Shot",
      "figma": {
        "fileKey": "6peEDBx1XNqpZ3UAeUlHyI",
        "nodeId": "REPLACE_WITH_APPROVED_FRAME_NODE_ID",
        "referenceImage": "REPLACE_WITH_REFERENCE_IMAGE_PATH"
      },
      "viewport": {
        "width": 360,
        "height": 780,
        "deviceScaleFactor": 1
      },
      "criticalElements": [
        {
          "name": "main-yardage-ring",
          "figmaNodeId": "REPLACE_WITH_LAYER_NODE_ID",
          "selector": "[data-qa='main-yardage-ring']",
          "properties": ["x", "y", "width", "height", "centerX", "centerY"],
          "toleranceCssPx": 1
        },
        {
          "name": "main-yardage-value",
          "figmaNodeId": "REPLACE_WITH_LAYER_NODE_ID",
          "selector": "[data-qa='main-yardage-value']",
          "properties": ["centerX", "centerY"],
          "toleranceCssPx": 1,
          "dynamicText": true
        }
      ],
      "dynamicMasks": []
    }

This is a template, not a completed or verified manifest. Do not invent Figma node IDs or measurements. Where a Figma element has no corresponding DOM element, use visible-geometry comparison or add a reliable QA hook to the implementation.

## 5. Generic Playwright/Chromium runner

The shared browser QA layer must be separate from page-specific tests.

### Generic checks (reusable for any page)
- Open the configured local page.
- Set viewport and device scale factor.
- Wait for essential assets/fonts.
- Capture screenshots.
- Collect console and uncaught page errors.
- Collect failed network requests and relevant HTTP failures.
- Detect horizontal overflow.
- Record selected DOM element bounds.
- Emit a structured report and save artefacts.

### Page-specific checks (configured per screen)
- Figma frame/reference image and geometry manifest.
- Required selectors and expected dimensions/positions.
- Expected UI state and deterministic fixture data.
- Dynamic content and masks.
- Page-specific functional assertions.

Keep existing AG45-specific workflows and assertions intact. Do not rename a specialised test as generic or remove its protections. Build the generic runner as an additive capability, then migrate or reuse it deliberately where appropriate.

The manual QA workflow must not run on its own workflow-file push. Use an explicit manual trigger unless a separate, approved CI trigger is agreed. Do not dispatch or rerun workflows without explicit permission.

## 6. Screen acceptance criteria

A screen can be marked **visually accepted** only when:
- The exact approved Figma reference is identified.
- The browser render uses the matching viewport and intended state.
- All designated critical geometry checks pass within documented tolerances.
- Overlay and difference images have been inspected.
- Dynamic content is handled without masking fixed geometry.
- No unexplained visual defects remain.
- Deliberate differences are documented and explicitly accepted.
- Evidence is retained so another person can review the result.

Use these statuses:
- **Not rendered** — no real browser screenshot exists.
- **Rendered, not compared** — screenshot exists, but no reference comparison has been completed.
- **Comparison failed** — one or more critical checks fail or visual defects remain.
- **Conditional** — a documented, explicitly accepted exception remains.
- **Visually accepted** — all required checks and review are complete.

Do not use “pixel-perfect” as a blanket claim. State what was measured, what was visually reviewed and what differences remain.

## 7. First implementation milestone

Prove the process on one high-value screen before applying it everywhere:

1. Confirm the exact approved Kite Tee Shot Figma frame and export it as the reference.
2. Extract real frame and critical layer measurements.
3. Create a geometry manifest with real Figma node IDs.
4. Add stable data-qa hooks to the corresponding HTML elements.
5. Use the generic Chromium runner to render at 360 × 780.
6. Produce and inspect the overlay, difference image and geometry report.
7. Correct ring, yardage and bunker alignment until critical checks pass.
8. Record actual results and only then expand to Approach, Scorecard and End Round.

## 8. Non-negotiable QA rule

**Identify the exact visual target → identify exact Figma layers → make the smallest change → render → compare visually against the target → inspect proportions, shape, spacing, colour and layering → fix anything wrong → render again → only then report.**

The final question for every screen is:

**If the Figma render were placed beside the browser render, would we be comfortable saying they match?**

If that comparison has not been performed, the honest status is “not yet verified”.
