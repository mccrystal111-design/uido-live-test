# Figma Editing & Visual QA Handover — kite

**Purpose:** This document is a handover for a separate ChatGPT conversation working directly on the kite Figma file while another conversation works on browser rendering and visual QA. It defines how to inspect and edit Figma safely, and what evidence must be provided to the QA workflow.

**Figma file:** https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI  
**File key:** `6peEDBx1XNqpZ3UAeUlHyI`  
**GitHub repository:** https://github.com/mccrystal111-design/uido-live-test  
**Related process:** [Figma-to-Browser Visual QA Standard](./FIGMA-TO-BROWSER-VISUAL-QA.md)

## 1. Parallel-work boundary

Two workstreams may proceed in parallel, but their responsibilities must stay distinct.

### Figma workstream
- Inspect the approved design and its layer structure.
- Confirm which frame is the current visual target.
- Export reference screenshots and capture exact node IDs and measurements.
- Maintain the approved design and its reference package.
- Document design changes that affect browser implementation.

### Browser/code QA workstream
- Build or adapt the generic Chromium/Playwright runner.
- Render configured HTML pages and collect diagnostics.
- Compare rendered screenshots and DOM geometry against supplied Figma references.
- Report discrepancies with evidence.
- Do not edit the Figma source design unless explicitly asked.

### Coordination contract
- Agree the exact target frame and revision before comparison.
- Never edit the same source artefact at the same time without coordinating.
- Treat Figma as the design source of truth, not the browser implementation.
- If a mismatch is found, first classify it: implementation defect, stale reference, or intentional design change.
- Do not change the design merely to make a failed implementation pass.
- Record the owner of any decision that changes the approved design.

## 2. Figma file map and protected areas

Known file: `6peEDBx1XNqpZ3UAeUlHyI`

Pages and known node IDs:
- `01 — Brand Foundations` — `0:1` — approved; **do not modify**.
- `02 — Product UI` — `6:2`.
- `02 — Kite Brand` — `35:3`.
- `03 — Kite Palette` — `38:2`.
- `04 — Kite Symbol` — `41:2`.
- `05 — Kite Logo Concept` — `43:26`.

Known product frames:
- Front screen construction V1: `93:2`.
- Start Round V1: `124:25`.
- Current copied yardage working frame — Tee Shot: `219:91`.
- Current copied yardage working frame — Par 3 / Approach: `219:166`.
- End Hole: `229:8`.
- End Round: `229:75`.
- Scorecard V1: `261:30`.
- End Round V1: `261:125`.

These are remembered locations, not a guarantee that the current file has not changed. Verify frame names and IDs in the live file before making edits. Do not resurrect deleted experiments `138:2`, `140:2` or `142:66`. Preserve original/master yardage designs; edit only the current working copies that the user identifies.

## 3. Rules for editing Figma

1. **Inspect before editing.** Open the exact target frame and inspect its hierarchy, dimensions and nearby variants.
2. **Identify exact layers.** Prefer the layer's actual node ID over a guessed name or visual location.
3. **Make the smallest change.** Do not rebuild a whole frame to fix one element.
4. **Preserve approved design decisions.** Do not adjust the Brand Foundations page or unrelated screens.
5. **Do not invent design values.** Read actual values from Figma; mark anything unknown for confirmation.
6. **Keep reusable components reusable.** Where an element is already a component/instance, do not detach it unless there is a clear reason.
7. **Protect masters.** Make changes on a user-approved working copy, not on a master/reference frame.
8. **Render after changes.** Capture the edited Figma frame and inspect proportions, shape, spacing, colour, typography and layering.
9. **Report exact changes.** Name the frame, layer(s), properties changed and the resulting node ID(s).
10. **Be candid.** If the screenshot could not be captured or inspected, say so; do not claim visual QA passed.

## 4. Reference package required for browser QA

For every screen that needs to be implemented or compared, provide:

- Figma URL with exact node ID.
- Page and frame name.
- Exported PNG at the frame's actual dimensions.
- Frame width and height.
- Viewport assumptions and device scale factor.
- Exact node IDs for critical layers.
- A geometry table for critical elements.
- Typography, stroke, fill, radius and effect values where important.
- Dynamic text/value areas that may change at runtime.
- Any intentional differences between Figma and the browser version.

### Critical yardage screen elements

For Tee Shot and Approach screens, prioritise:
- Main red yardage ring: position, size, centre and stroke.
- Main yardage value: visible centre/baseline and alignment to the ring.
- Front/middle/back yardage values and their relative positions.
- Bunker rings: positions, dimensions, spacing and relationship to other elements.
- Header and hole/par/n nett-par content.
- Bottom controls: icon silhouette, backing shape, shadow and spacing.
- Frame insets and safe space at the top and bottom.

For scorecard screens, prioritise:
- Header and score summary geometry.
- Column positions and row heights.
- Front nine/back nine totals and overall total alignment.
- Card padding, dividers, text baselines and stat chart sizes.
- Scrollable content boundaries and bottom controls.

Do not copy values from this list; it is a checklist of what to measure.

## 5. Geometry handoff format

Send a compact table or JSON manifest to the browser QA workstream. Each critical element should include:
- Human-readable element name.
- Figma node ID.
- X/Y, width/height and centre coordinates where relevant.
- Stroke/fill/radius and typography values where relevant.
- Intended browser selector (for example, a `data-qa` attribute).
- Tolerance and reason for it.
- Whether text/value is dynamic.

Do not invent selectors and then assume the code already contains them. The code workstream must add and verify stable QA hooks.

Example row (placeholder only):

| Element | Figma node ID | Expected geometry | Browser selector | Dynamic? |
|---|---|---|---|---|
| Main yardage ring | Replace with real ID | x/y/w/h/centre from Figma | `[data-qa="main-yardage-ring"]` | No |
| Main yardage value | Replace with real ID | centred within ring | `[data-qa="main-yardage-value"]` | Yes |

## 6. Handling dynamic values

The number may change; its layout must not drift.

- Keep the ring and other static geometry independently measurable.
- Record how the number should be centred (geometric centre, baseline or other defined rule).
- Use representative values with different character widths, such as `9`, `99` and `199`.
- Do not ask QA to mask the whole ring or its surroundings.
- If a reference export uses a particular sample number, note it. The QA comparison can mask/normalise only the changing glyph area while separately checking text alignment and ring geometry.

## 7. Review loop

For each proposed design/code comparison:

1. Confirm the Figma target has not changed.
2. Export the reference from the exact frame.
3. Render the current implementation in Chromium at the same viewport.
4. Inspect the side-by-side, overlay and difference image.
5. Check geometry report for critical layer bounds.
6. Classify each mismatch as:
   - implementation defect;
   - stale or incorrect reference;
   - Figma design defect/ambiguity;
   - expected dynamic-content difference;
   - approved intentional difference.
7. Fix the correct source of the discrepancy.
8. Export/render again and recheck.
9. Record evidence and status.

A screenshot of Figma alone is not proof that the browser matches it. A successful browser render alone is not proof either.

## 8. Current status and next actions

This document is a working handover/process specification. It does not claim that a generic runner has already been implemented or that any Kite page has passed browser-to-Figma comparison.

### Figma workstream next actions
- Verify the current live Figma frames and node IDs.
- Confirm the exact Tee Shot frame to use as the first reference.
- Export its reference PNG at native dimensions.
- Extract real measurements for the main ring, main yardage, bunker indicators and bottom controls.
- Deliver the reference package and geometry manifest to the browser QA workstream.
- Avoid changing the target design while that comparison is underway unless a design defect is confirmed and the change is agreed.

### Browser QA workstream next actions
- Implement the generic, manually invoked Playwright/Chromium runner as a separate additive capability.
- Consume the Figma reference package and geometry manifest.
- Produce screenshots, overlay, difference image and geometry report.
- Do not trigger or rerun GitHub Actions without explicit permission.

## 9. Required honesty in reporting

Use one of these statuses:
- **Reference not prepared**
- **Reference prepared**
- **Browser render not available**
- **Rendered, not compared**
- **Comparison failed**
- **Conditional — documented exception**
- **Visually accepted**

Only use **Visually accepted** when the actual browser render has been compared against the exact approved reference, critical geometry passes, visual differences have been reviewed, and remaining deviations are explicitly accepted.

**QA rule:** Identify the exact visual target → identify exact Figma layers → make the smallest change → render → compare visually against the target → inspect proportions, shape, spacing, colour and layering → fix anything wrong → render again → only then report.
