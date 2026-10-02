# UiDo — Current State

Updated: 2026-10-02. Dashboard source and Pages deployment fix are committed; live publication is being verified.

## Project control
- Live dashboard source: [project-dashboard.html](../../project-dashboard.html).
- Published URL: https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html. The Pages workflow now explicitly copies `project-dashboard.html` into `_site`; deployment/access verification is pending.
- Dashboard fetches public GitHub issues, open pull requests and recent workflow runs directly from the GitHub REST API; refreshes every five minutes and on demand. It is read-only and does not start/rerun workflows.
- Figma file: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI .
- Added editable Figma page **02 — Project Dashboard** with a 66-child dashboard concept frame. This is the visual design, not a live Figma data connection.
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

## Next action
**OPS-002** — inspect actual repository source, recent commits and relevant workflow runs, then reconcile the control pack against evidence. The workflow file change is committed and its normal push-triggered Pages deployment is expected; no manual dispatch/rerun was requested.

## Unverified
- The public GitHub Pages dashboard URL has not been confirmed accessible.
- Latest AGNOSTIC45 run status and current source baseline have not been verified in this setup.
- The original concept PNG has not yet been placed unchanged on a dedicated Figma reference page.
- No timeline dates have been agreed. Do not claim tests or visual QA passed without linked evidence.