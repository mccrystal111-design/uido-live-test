# AGNOSTIC45 — isolated visual QA protocol

## Purpose and authority

This is an isolated inspection tool for AGNOSTIC45 candidate pages. It runs automatically for selected candidate/QA changes on `main`, with manual dispatch retained as a fallback. It renders the selected commit locally in headless Chromium, captures screenshots and SVG/browser diagnostics, and packages evidence for review.

**It does not deploy, publish, promote, commit, or overwrite any course page.** The approved base remains governed by `overstone/AG45v1-BASE-STATUS.md`; a candidate becomes a new base only after Kieron explicitly approves it.

## Normal change loop

1. **Request:** Kieron specifies the change to the approved AG45 base.
2. **Implement:** make the change in a distinct candidate/review HTML file. Preserve the approved canonical HTML and existing camera, route-fit, projection, and geometry logic unless the request explicitly changes them.
3. **Commit verification:** inspect the diff and commit SHA; confirm the approved base file was not changed unintentionally.
4. **Automated QA:** a push to the candidate HTML, QA script, or workflow on `main` starts the visual QA workflow with default target, hole, and viewport matrix. For a custom target or matrix, open Actions → **AGNOSTIC45 Visual QA (Manual)** → Run workflow and provide the inputs.
5. **Evidence inspection:** review every PNG and `diagnostics.json` from the `ag45-visual-qa-N` artifact. Inspect the SVG `viewBox`, visible bounds, clipping paths, rendered geometry count/classes, layout element bounds, HTTP failures, console warnings/errors and uncaught exceptions.
6. **Assistant review:** compare the actual rendered result and SVG structure with the requested change and the preserved base. Report concrete pass/fail findings; don't call a change visually verified based only on a green workflow.
7. **Handover:** provide Kieron a candidate live HTML URL for final review, explicitly distinguishing committed source from verified Pages deployment.
8. **Final authority:** Kieron decides whether the candidate is accepted. Only after explicit approval may the project mark it as the new base.

## Workflow boundaries

- Triggers: `push` to `main` for the candidate HTML, QA script, or workflow file; `workflow_dispatch` for custom manual runs. No pull-request, schedule, or deployment trigger.
- Browser: Microsoft's Playwright Python container with Chromium.
- Candidate source: the checked-out commit is served on localhost; tests do not rely on a potentially stale GitHub Pages deployment.
- Inputs: candidate repository-relative HTML path, comma-separated hole numbers, viewport matrix, and a short statement of the intended change.
- Evidence: per-case PNG screenshots, raw rendered SVG dumps under `visual-qa/phone-bars/svg-dumps/`, `diagnostics.json`, and `review-checklist.md`, uploaded even when checks fail.
- Automated checks: page response, document overflow, required phone-bar elements, 8% top/bottom bar geometry, 60%/40% rail split, 84% course viewport, flush bar boundaries, SVG presence/render size/geometry, failed requests, console/page errors, and renderer geometry root where available.
- Human checks: expected visual change, camera/course framing, geometry correctness, SVG clip/viewBox integrity, no unexpected distortion/cropping, bar/rail boundaries where present, and phone usability.
- Results: **PASS** = requested change appears correct in code and visuals; **REVIEW** = ambiguous or needs human decision; **FAIL** = reproducible regression or requested change not implemented.
- No automatic reruns. Run only when the change is ready for inspection and the user has asked for the QA pass.

## Inputs

- `target_html`: repository-relative candidate HTML file. Must exist at the selected commit and cannot contain `..`.
- `holes`: comma-separated integers from 1 to 18.
- `viewports`: comma-separated `WIDTHxHEIGHT`, default `390x844,360x640,768x1024,1440x900`.
- `requested_change`: plain-language description stored in the artifact so the evidence is tied to the intended visual change.

## Important limitations

Automated geometry counts and browser checks cannot decide whether a course rendering is visually correct. SVG path counts may legitimately change as a feature is added or removed. Compare the actual screenshots and the SVG structure against the requested change; treat a difference as a regression only when it violates the agreed geometry/layout contract. GitHub Pages publication and cache freshness must be verified separately before handing over a live URL.
