# AG45v1 — Phone Bars Layout Review

**Status:** Working review copy; not approved as a new base  
**Base preserved:** `overstone/agnosticbase45-hole9-geometry-review.html`  
**Review HTML:** `overstone/ag45v1-phone-bars-review.html`  
**Preview URL:** https://mccrystal111-design.github.io/uido-live-test/overstone/ag45v1-phone-bars-review.html?hole=9

## Layout target

- Top notification bar spans the full screen width and is 8% of the phone screen height.
- Right-hand area retains the 60%/40% horizontal split, starts directly below the top bar, and continues to the bottom edge.
- Bottom bar is 8% of screen height and spans from the left edge to the right-hand area's left edge.
- The three bars meet directly, with no intentional gaps.
- The course viewport occupies the remaining central 84% height.
- The viewport height and SVG viewBox are adjusted together. The existing route projection, camera fit, and geometry selection logic remain in the separate review copy.

## Protected base

The approved AG45v1 HTML is unchanged. This is a separate review copy. Do not promote it to the canonical base without explicit user approval.

## Manual Playwright visual QA

Workflow: [AGNOSTIC45 Phone Bars Visual QA](https://github.com/mccrystal111-design/uido-live-test/actions/workflows/visual-qa-agnostic45.yml)

1. Open the workflow link and select **Run workflow**.
2. Leave **Use workflow from** on the intended branch (normally `main`).
3. Default holes: `9`. Default viewports: `390x844,360x640,768x1024,1440x900`.
4. Start the workflow manually. It is intentionally configured for `workflow_dispatch` only; commits do not trigger it automatically.
5. Open the completed run and download the `ag45v1-phone-bars-visual-qa` artifact.
6. Inspect every screenshot in `visual-qa/phone-bars/`, then review `diagnostics.json`.

The browser run checks the three bar boundaries, the 8% bar heights, viewport boundaries, page overflow, SVG clipping/playline, rendered geometry, HTTP status, console warnings/errors, and JavaScript exceptions across each hole/viewport combination. These checks are diagnostic, not a substitute for visually inspecting the screenshots: confirm the course is correctly framed, the route is not unexpectedly cropped or distorted, the side panel and bars are flush, and the central viewing area is usable at phone sizes.

## Verification status

The workflow has been updated to target this review copy and capture the viewport matrix. **It has not been run**, and GitHub Pages deployment/live rendering and screenshot appearance have not yet been verified. No GitHub Actions run was started by this change.


## Isolated QA contract

The manual workflow is defined in [AGNOSTIC45 Visual QA (Manual)](../.github/workflows/visual-qa-agnostic45.yml). The step-by-step approval and evidence protocol is [AG45 Visual QA Protocol](AG45-VISUAL-QA-PROTOCOL.md). The workflow tests a candidate from the selected commit on localhost, captures screenshots and SVG/browser diagnostics, and never deploys or promotes a candidate. Run it only when a requested change is ready for review; do not trigger it automatically on commits.
