# UiDo — Current State

Updated: 2026-10-05. Tool/access register is linked from the session-start instructions; dashboard deployment and Playwright verification are complete.

## Project control
- Mandatory tool map: [TOOL-AND-ACCESS-REGISTER.md](TOOL-AND-ACCESS-REGISTER.md). It records confirmed routes and current access gaps; verify needed tools at the start of each session.
- Live dashboard source: [project-dashboard.html](../../project-dashboard.html).
- Published URL: https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html. The Pages workflow explicitly copies `project-dashboard.html` into `_site`; deployment [run #36982434145](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982434145) succeeded. Dashboard-specific Playwright/Chromium QA [run #36982461137](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137) passed at 390×844 and 1440×900: HTTP 200, title/heading correct, live counts loaded (6 open issues, 2 open PRs), no browser console/page errors, no failed HTTP responses and no horizontal overflow. [Screenshots/report artifact](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137/artifacts/11216560509).
- Dashboard fetches public GitHub issues, open pull requests and recent workflow runs directly from the GitHub REST API; refreshes every five minutes and on demand. It is read-only and does not start/rerun workflows.
- Figma file: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI .
- Added editable Figma page **02 — Project Dashboard** with a 66-child dashboard concept frame. This is the visual design, not a live Figma data connection.
- GitHub connector access was verified by reading and committing repository docs. Figma connector responded to an identity/workspace query. Supabase connector returned no accessible projects on 2026-10-02. No direct interactive browser-control integration is exposed in this chat session, but repository-hosted Playwright/Chromium QA is available through `.github/workflows/visual-qa-agnostic45.yml` and `.github/workflows/project-dashboard-browser-qa.yml`.
- Created GitHub issues: [OPS-002](https://github.com/mccrystal111-design/uido-live-test/issues/5), [OPS-003](https://github.com/mccrystal111-design/uido-live-test/issues/6), [DES-001](https://github.com/mccrystal111-design/uido-live-test/issues/7), [RND-001](https://github.com/mccrystal111-design/uido-live-test/issues/8).
- GitHub Project (the native Projects board with saved views) has not been created; connected GitHub tools available in this session do not expose a create/configure Project action. OPS-003 tracks this setup and owner-UI steps if needed.

## Open pull requests reviewed on 2026-10-02
- [PR #3 — Define UiDo canonical global course database architecture](https://github.com/mccrystal111-design/uido-live-test/pull/3): open draft targeting `main`; adds course/feature/provenance/issue schemas and Git-backed versioning. Its feature geometry schema currently describes GeoJSON but does not yet constrain geometry structure; treat as a proposal, not an approved geometry contract. Mergeability/check status was not established.
- [PR #1 — Test EA machine acquisition path](https://github.com/mccrystal111-design/uido-live-test/pull/1): open draft targeting `main`; adds a direct EA survey-tile endpoint probe to the Overstone acquisition test. Mergeability/check status was not established.
- Neither PR was merged or changed during this reconciliation.

## Product and technical baseline
- Brand direction: warm ivory, forest green, golden-yellow circular mark, restrained topographic/course imagery and premium understated golf identity. Existing preferences include #3F4B3B, Montserrat and Bodoni Moda; verify actual palette from the concept before approval.
- AGNOSTIC45 goal: extend the proven geometry-driven base renderer for par-4/par-5 holes, supporting tee, fairway, rough, green, bunkers, water and paths, with no labels/player profile/UI overlays in the base.
- Course geometry: canonical hole-by-hole geometry and provenance should be agreed before extending renderer work.
- Live hole UI previously covered GPS/player position, front/middle/back green yardages, bunker distances, orientation, viewfinder and right-side info panels. Verify implementation before reopening defects.
- **Shot/GPS field test:** standalone additive page `overstone/shot-capture-gps-test.html` now supports value selection for Yardage, UiDo Caddie, Wind, Lie, Club, Strike, Trajectory, Start, Shape, Score and Putts, plus HIT SHOT snapshots. Events carry UTC timestamps, shot/hole context and phone GPS coordinates/accuracy; JSON export includes an ordered event log and shot summaries. A mini Overstone wireframe plots captured points. Latest implementation: [9b54d56](https://github.com/mccrystal111-design/uido-live-test/commit/9b54d56bb9fa200771887f87b1af30986ecd9764). Intended test URL: https://mccrystal111-design.github.io/uido-live-test/overstone/shot-capture-gps-test.html. Device testing and live Pages publication have not been verified; no field data captured.
- Stats sections: Handicap (Official + Practice, explanation/edit/connect and 9-hole WHS-aligned handling), Performance, Scoring, Driving, Approach, Short Game.
- Supabase is under consideration for data packets; define data and offline/sync needs before deciding storage architecture.
- Real-Golfer Trigger Principle applies to all product workflows.
- Workflow automation is permitted where configured triggers reflect legitimate development, QA, deployment or support processes. Do not manually dispatch/rerun a workflow unless it is needed; allow normal push-triggered deployment to run.

## Workflow evidence checked on 2026-10-02
- Latest relevant AGNOSTIC45 phone-bars QA: [run #36925474787](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36925474787), completed successfully on source commit `fc51a6d624bf00e2c290bce7cc40f004e2d76bd6`. The job ran Playwright + Chromium, checked the phone-bars/geometry layout at configured viewports and uploaded artifact `ag45-visual-qa-74` with screenshots and diagnostics. This is automated evidence, not human visual approval and not a test of the dashboard.
- AG45 candidate page currently exists at `overstone/ag45v1-phone-bars-review.html` (blob `f9ed5b1113cb5823c1c52b4b2c3bad5bea26cf40`); the standalone unbranded base source `overstone/ui-hole-renderer-agnostic45-ui-base.html` exists (blob `4abe22707f0d000b0cbb3567c22639719ac16c47`). The QA run tested the phone-bars review page, not the standalone base page.
- Latest dashboard-copy Pages deploy [run #36982434145](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982434145) passed at commit `84140b87432507706ad159e3f2a936d93ef72053`. Dashboard Playwright QA [run #36982461137](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137) passed at commit `9bc63015d319a79b0dc7f946137081d54cde5415`.
- Documentation commits caused several push-event workflow runs to fail with zero jobs (e.g. [#36982036792](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982036792)); GitHub's jobs endpoint returns an empty list, so the failure cause is not yet established. No reruns were started. Avoid claiming these are course-build failures until the trigger/check-suite explanation is confirmed.

## Yardage field-mirror playground — 2026-10-05
- `ring-playground.html` is now a two-sided yardage authoring surface: finished UI on the left, same-position semantic field targets on the right, and a separate Field Library for drag/drop binding.
- The mirror is geometry-linked to the finished UI. Semantic fields are deliberately unbound at load; test values are separate from layout geometry.
- Export is now semantic field/layout JSON plus a screenshot of the finished UI canvas only.
- Live renderer `overstone/yardage-lie-prototype.html` remains untouched.
- Implementation commits: [02e22e6](https://github.com/mccrystal111-design/uido-live-test/commit/02e22e65b8db03cd03268675bc0faaa111840614) and QA workflow [917eea9](https://github.com/mccrystal111-design/uido-live-test/commit/917eea938cdaec1aac06e81b2e230468ba24c7a1).
- QA status: **needs verification**. The prior run on the pre-mirror version failed because its selector expected the old `#loadYardage` control; the later run was cancelled after the source was updated. No manual rerun was started.

## Figma + Yardage v4 + Hawk/V5 work — 2026-10-05

### Figma source recreation
- Figma file: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI
- Approved source frame: UiDo Yardage — Source Recreation, node 8:24, 360×780, on 02 — Product UI.
- This frame is the visual source of truth for the yardage UI. The approved design was recreated as a fresh HTML baseline rather than patched from the earlier v3 layout.
- Use Figma design context/geometry as authoritative and verify the actual rendered page at 360×780 before visual approval.
- Do not redesign the approved yardage composition unless explicitly requested.

### Yardage v4 — retained as test baseline
- File: overstone/yardage-v4.html
- v4 is the fresh Figma-derived yardage build and is now the visual test baseline.
- The user has confirmed that v4 is visually correct.
- v4 uses the live yardage/GPS engine derived from earlier work, but it is not the new Hawk product build.
- Do not modify v4 as part of Hawk/V5 development unless explicitly requested. Treat it as a reference/test baseline.
- Latest v4 live-position change: commit a0e015018b0f16161b3e022b927d99ddfa1873db; player position no longer falls back to the tee when live GPS is unavailable. Post-change deployment/render verification was not established, so do not claim that specific revision has been visually verified.

### Hawk / V5 discovery — Q&A only so far
- Hawk is a new app/product experience being defined separately from v4.
- Discovery is currently in Q&A mode. No Hawk build should begin until the Q&A is complete and the accumulated decisions are agreed.
- Current agreed behaviour includes:
  - Start screen: Start Round, Scores, Stats; equal-sized controls, with Start Round distinguished by colour.
  - Start Round opens a brief setup: Course, Tees, scoring format.
  - GPS acquisition begins when the app/page loads.
  - Start Round opens the yardage page on Hole 1.
  - Hole progression occurs after Score + Putts are completed, not automatically from GPS.
  - The current hole remains active unless the player manually uses Jump to Hole.
  - Tapping the hole header (for example HOLE 1 · PAR 4 (4)) opens an 18-hole selector.
  - Hole selector is a 6×3 grid with buttons labelled only 1–18.
  - Selecting a hole closes the selector and opens that hole.
  - GPS continues updating while playing; when the player has stopped and GPS accuracy is better than 4m, hold the position. Resume live updates when movement starts again.
- The Q&A memory is maintained as one cumulative, copyable plain-text line after each answer. This is a project-agnostic discovery protocol, now documented in NEW-CHAT-STARTER.md.
- The eventual final Q&A memory must be persisted in the appropriate project source-of-truth document before Hawk/V5 implementation begins.

## Next actions
- **OPS-002** remains open for separate reconciliation; this session has deliberately moved to another workstream.
- **DATA-001** is now in progress: draft the provider-neutral [Course Packet Specification](../architecture/COURSE-PACKET-SPEC.md) was committed at [53144a8](https://github.com/mccrystal111-design/uido-live-test/commit/53144a8d5bdfb9a410f3142d85f822c2f70df046). Next: compare it with actual Overstone course-builder output and PR #3's proposed schemas, then agree the canonical geometry contract before implementing a builder/validator or choosing storage.

## Unverified
- Final two-sided field-mirror playground behavior has not yet received a green Chromium workflow run; verify the new drag/drop, geometry mirroring and export behavior before treating it as stable.
- The standalone base passed automated geometry QA, but the canonical hole-by-hole geometry contract still needs agreement before renderer extension.
- The original concept PNG has not yet been placed unchanged on a dedicated Figma reference page.
- No timeline dates have been agreed. Do not claim tests or visual QA passed without linked evidence.


## Clean-build canonical database checkpoint — 2026-10-05
- Supabase project uido-production is live in eu-west-2 and now contains the first UiDo-owned Overstone course revision: v1-osm-source.
- Live import verified: 18 course holes, 159 physical source features, 159 feature-provenance links. Revision remains draft because satellite registration/refinement and hole-feature association are not yet verified.
- GitHub canonical evidence is persisted at course-models/source-normalized/overstone-source-normalized-v0.1.json and course-models/canonical/overstone-park-v1.json; the live import record is database/seeds/20261005_overstone_canonical_v1.sql.
- The canonical database preserves OSM source geometry and the existing Overstone F/M/B green anchors. No satellite transform has been invented.
- Supabase security review still reports two public tables without RLS and five RLS-enabled tables without policies. These are foundation/security work, not a reason to alter the course import.
