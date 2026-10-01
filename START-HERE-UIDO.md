# UiDo — Start Here (Cross-Chat Handover)

**Purpose:** This is the first file to read when continuing UiDo work in a new ChatGPT conversation. Treat the repository as the durable source of truth; do not make Kieron repeat decisions already recorded here or in the linked project documents.

**Last updated:** 2026-10-01  
**Repository:** https://github.com/mccrystal111-design/uido-live-test  
**Default branch:** `main`

## Instructions for the next ChatGPT conversation

1. **Read this file first**, then inspect the current `main` branch and the relevant source files before making claims or edits. Do not rely on an old chat summary as proof of the current repository state.
2. Work directly in the existing GitHub repository using available GitHub tools. **Do not hand off to Work mode**; Kieron has asked to continue in the normal ChatGPT conversation.
3. Kieron wants to act as a **product user**, not as the person operating development or QA workflows. Automate the repository/QA steps wherever the connected tools actually allow it. Do not ask him to repeat manual technical steps when they can be performed directly.
4. Be transparent about tool limits. Never claim a workflow ran, a commit deployed, an artifact was inspected, or a preview was verified unless the available evidence confirms it. If a workflow cannot be started with the available tools, say exactly what is blocked and continue with other useful work.
5. **Extend the proven base; do not rebuild it.** Make requested changes in a separate candidate/review copy. Do not overwrite or promote the approved baseline without Kieron's explicit approval.
6. After each requested UI change: inspect current code; make the smallest appropriate edit; commit it; verify the resulting commit and workflow run; inspect screenshots and diagnostics where available; report the evidence and unresolved issues; provide the relevant preview URL. Kieron makes the final visual/product approval.
7. Do not automatically deploy or promote a candidate just because checks pass. A passing automated check is evidence, not user approval.
8. Preserve course geometry and camera/projection logic when working on layout. Do not move course geometry to compensate for screen-layout issues; keep layout and geometry/camera concerns separate.

## Current AGNOSTIC45 state

### Approved baseline — protected
- Status document: [`overstone/AG45v1-BASE-STATUS.md`](overstone/AG45v1-BASE-STATUS.md)
- Canonical HTML: `overstone/agnosticbase45-hole9-geometry-review.html`
- Approval recorded: **2026-10-01**
- Approved source commit recorded in the status file: `abf82bf297c439810e2d0a8ae1cac8e75283c91b`
- Preview: https://mccrystal111-design.github.io/uido-live-test/overstone/agnosticbase45-hole9-geometry-review.html?hole=9

The approved AG45v1 base is geometry-driven for a Par 4/Par 5 and contains no unapproved UiDo branding or player-profile/UI overlays. Preserve the established camera, view-window, route-fit, geometry-fit, and projection calculations unless a specific change is agreed.

### Current phone-bars candidate — not approved as a new base
- Candidate HTML: `overstone/ag45v1-phone-bars-review.html`
- Review notes: [`overstone/AG45v1-PHONE-BARS-REVIEW.md`](overstone/AG45v1-PHONE-BARS-REVIEW.md)
- Preview: https://mccrystal111-design.github.io/uido-live-test/overstone/ag45v1-phone-bars-review.html?hole=9
- QA protocol: [`overstone/AG45-VISUAL-QA-PROTOCOL.md`](overstone/AG45-VISUAL-QA-PROTOCOL.md)
- QA script: `scripts/ag45_visual_qa.py`
- Workflow: [AGNOSTIC45 Visual QA](.github/workflows/visual-qa-agnostic45.yml) — https://github.com/mccrystal111-design/uido-live-test/actions/workflows/visual-qa-agnostic45.yml

Phone-bars design target:
- Top bar: full width, 8% of viewport height.
- Right-hand panel/rail: 60%/40% horizontal split, begins below the top bar and continues to the bottom edge.
- Bottom bar: 8% of viewport height, from the left edge to the start of the right-hand rail.
- Bars meet without intentional gaps.
- Course viewport uses the remaining central 84% height.
- Adjust viewport height and SVG viewBox together; keep camera/projection and geometry selection separate.

### QA automation status
- **Automatic push trigger proven:** a push to the QA workflow file started the AG45 visual QA workflow.
- **Push-event defaults repaired:** the workflow now supplies defaults when `workflow_dispatch` inputs are absent.
- **Playwright dependency repaired:** the job installs the matching Python package `playwright==1.52.0` into the official browser container.
- **End-to-end run succeeded:** run [36906252066](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36906252066) rendered Hole 9 at all four default viewports, completed browser/SVG diagnostics with no fatal cases, and uploaded screenshots/diagnostics.
- **Phone-bars layout restored in the candidate:** the review HTML now contains the top bar, course viewport, right rail and bottom bar; the approved canonical HTML was not edited.
- **Layout-geometry QA passed:** run [36906688848](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36906688848) completed successfully on candidate commit `78cad854d177eb64dea1d56357db8a2a95584caa`. All four viewport cases passed every automated check, including top-bar height, course viewport height, right-rail split, bottom-bar dimensions, and gap-free joins; no console errors, page errors, failed HTTP requests, or fatal cases were recorded. Its screenshot/diagnostics artifact is `ag45-visual-qa-56`.
- The workflow remains local-only: it does not deploy or promote the candidate. Live GitHub Pages state must be checked separately.
- Manual `workflow_dispatch` remains available as a fallback; if a future tool cannot start a run, be transparent rather than claiming one was launched.

The intended QA viewport matrix is `390x844,360x640,768x1024,1440x900`; the default target is the phone-bars candidate and default hole is `9`. Automated diagnostics cover page/layout bounds, bar dimensions, overflow, SVG details, HTTP status, browser console and JavaScript errors. Human screenshot inspection remains necessary.

## Source-of-truth and approval rules

- GitHub `main` and the specific project status/review documents are the durable record. Verify the current head and file contents at the start of a new chat.
- Keep approved base, working candidate, QA evidence, and deployment state distinct.
- A source commit is not proof of GitHub Pages deployment. Verify the live URL separately.
- Keep changes narrow, reversible, and committed with descriptive messages.
- If the repo contradicts this handover, inspect the actual files and update this handover to reflect the verified state; do not blindly follow stale notes.

## First task on resuming

Check the current `main` HEAD, read this handover plus the base status, phone-bars review, QA protocol, workflow and QA script. Then verify the live preview/deployment separately, review the phone-bars layout with Kieron, and continue the next front-end task in the candidate only. Keep the approved base protected.
