# UiDo — Current State

Updated: 2026-10-02. Dashboard source and Pages deployment fix are committed; the normal Pages deployment completed successfully (run #36979995902). Tool/access register added and linked from the session-start instructions.

## Project control
- Mandatory tool map: [TOOL-AND-ACCESS-REGISTER.md](TOOL-AND-ACCESS-REGISTER.md). It records confirmed routes and current access gaps; verify needed tools at the start of each session.
- Live dashboard source: [project-dashboard.html](../../project-dashboard.html).
- Published URL: https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html. The Pages workflow explicitly copies `project-dashboard.html` into `_site`; deployment run succeeded. Direct live browser rendering remains unverified.
- Dashboard fetches public GitHub issues, open pull requests and recent workflow runs directly from the GitHub REST API; refreshes every five minutes and on demand. It is read-only and does not start/rerun workflows.
- Figma file: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI .
- Added editable Figma page **02 — Project Dashboard** with a 66-child dashboard concept frame. This is the visual design, not a live Figma data connection.
- GitHub connector access was verified by reading and committing repository docs. Figma connector responded to an identity/workspace query. Supabase connector returned no accessible projects on 2026-10-02. No direct browser-control integration is exposed in this chat session, but repository-hosted Playwright/Chromium QA is available through `.github/workflows/visual-qa-agnostic45.yml`.
- Created GitHub issues: [OPS-002](https://github.com/mccrystal111-design/uido-live-test/issues/5), [OPS-003](https://github.com/mccrystal111-design/uido-live-test/issues/6), [DES-001](https://github.com/mccrystal111-design/uido-live-test/issues/7), [RND-001](https://github.com/mccrystal111-design/uido-live-test/issues/8).
- GitHub Project (the native Projects board with saved views) has not been created; connected GitHub tools available in this session do not expose a create/configure Project action. OPS-003 tracks this setup and owner-UI steps if needed.

## Product and technical baseline
- Brand direction: warm ivory, forest green, golden-yellow circular mark, restrained topographic/course imagery and premium understated golf identity. Existing preferences include #3F4B3B, Montserrat and Bodoni Moda; verify actual palette from the concept before approval.
- AGNOSTIC45 goal: extend the proven geometry-driven base renderer for par-4/par-5 holes, supporting tee, fairway, rough, green, bunkers, water and paths, with no labels/player profile/UI overlays in the base.
- Course geometry: canonical hole-by-hole geometry and provenance should be agreed before extending renderer work.
- Live hole UI previously covered GPS/player position, front/middle/back green yardages, bunker distances, orientation, viewfinder and right-side info panels. Verify implementation before reopening defects.
- Stats sections: Handicap (Official + Practice, explanation/edit/connect and 9-hole WHS-aligned handling), Performance, Scoring, Driving, Approach, Short Game.
- Supabase is under consideration for data packets; define data and offline/sync needs before deciding storage architecture.
- Real-Golfer Trigger Principle applies to all product workflows.
- Workflow automation is permitted where configured triggers reflect legitimate development, QA, deployment or support processes. Do not manually dispatch/rerun a workflow unless it is needed; allow normal push-triggered deployment to run.

## Workflow evidence checked on 2026-10-02
- Latest relevant AGNOSTIC45 Visual QA run found: [run #36925474787](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36925474787), completed successfully on source commit `fc51a6d624bf00e2c290bce7cc40f004e2d76bd6`. The job ran Playwright + Chromium, checked the phone-bars/geometry layout at configured viewports and uploaded artifact `ag45-visual-qa-74` with screenshots and diagnostics. This is automated evidence, not human visual approval and not a test of the dashboard.
- AG45 candidate page currently exists at `overstone/ag45v1-phone-bars-review.html` (blob `f9ed5b1113cb5823c1c52b4b2c3bad5bea26cf40`); the standalone unbranded base source `overstone/ui-hole-renderer-agnostic45-ui-base.html` exists (blob `4abe22707f0d000b0cbb3567c22639719ac16c47`). The QA run tested the phone-bars review page, not the standalone base page.
- Latest Pages deploy [run #36979995902](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36979995902) passed all deploy steps at commit `436f612f8acff69cab1f96eb80c576145147add4`.
- Documentation commits caused several push-event workflow runs to fail with zero jobs (e.g. [#36982036792](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982036792)); GitHub's jobs endpoint returns an empty list, so the failure cause is not yet established. No reruns were started. Avoid claiming these are course-build failures until the trigger/check-suite explanation is confirmed.

## Next action
**OPS-002** — dashboard still needs a dashboard-specific browser check; investigate why the legacy/workflow-dispatch-only workflow records show push-event failures with zero jobs. Then complete control-pack reconciliation before advancing RND-002 geometry contract.

## Unverified
- The public GitHub Pages dashboard URL has not been confirmed accessible in a real browser.
- Latest AGNOSTIC45 run status and current source baseline have not been verified in this setup.
- The original concept PNG has not yet been placed unchanged on a dedicated Figma reference page.
- No timeline dates have been agreed. Do not claim tests or visual QA passed without linked evidence.
