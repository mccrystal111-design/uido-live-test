# UiDo Session Handover

Updated: 2026-10-02

## First read
1. [Project control pack](README.md)
2. [Tool & access register](TOOL-AND-ACCESS-REGISTER.md)
3. CURRENT-STATE.md
4. ACTION-REGISTER.md
5. DEPENDENCIES.md
6. DECISION-LOG.md

## Immediate next action

**Kieron's requested field test: radial tile + GPS capture at the ball.** Open the standalone [Shot Capture + GPS test](../../overstone/shot-capture-gps-test.html) or intended published URL https://mccrystal111-design.github.io/uido-live-test/overstone/shot-capture-gps-test.html on the phone. Allow location access, wait for a fix, tap radial tiles and **HIT SHOT** at the ball, then use **Export JSON**. Compare captured phone coordinates/timestamps/accuracy with the Garmin watch and review the plotted points against the Overstone wireframe. The page is additive and does not alter the existing hole renderer. It stores events in browser local storage until export or clear. **No on-course/device test has yet been performed, and live Pages publication could not be verified from this session.** If the URL is not live yet, check the normal Pages deployment; do not manually rerun Actions without a reason.

- Implementation commit: [1a15b63](https://github.com/mccrystal111-design/uido-live-test/commit/1a15b63db29478e6c9cb88677bec34ce27f2d82a). The event JSON includes schema/version, event/session IDs, course and hole, event type, tile ID/label, UTC event time, shot number where applicable, GPS coordinates, accuracy and other available location metadata.
- **OPS-002 is being handled separately**; do not duplicate that investigation. Earlier runs #36982036792 and #36982882178 returned zero jobs through the available connector; cause remains unverified and neither was rerun. Dashboard Playwright QA [#36982461137](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137), Pages deployment [#36982434145](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982434145), AG45 phone-bars QA [#36925474787](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36925474787), and standalone base QA [#36982883414](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982883414) are prior verified evidence, not tests of this new field-test page.
- After the field test, resume **DATA-001**: inspect real Overstone/Poult Wood builder output against [Course Packet Specification v0.1](../architecture/COURSE-PACKET-SPEC.md), then define fixture acceptance tests before changing acquisition, storage or renderer code.
- Dashboard direct browser confirmation and the zero-job workflow diagnosis remain separate open items; do not claim this new page has passed QA until it is tested on-device or by a dedicated browser run.

## Project links
- Repo: https://github.com/mccrystal111-design/uido-live-test
- [Live dashboard page](../../project-dashboard.html) — intended published URL: https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html (deployment run succeeded; direct browser confirmation remains outstanding).
- Figma: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI
- Figma dashboard design page: 02 — Project Dashboard.
- Tool/access register: [TOOL-AND-ACCESS-REGISTER.md](TOOL-AND-ACCESS-REGISTER.md)
- Issues: [OPS-002 #5](https://github.com/mccrystal111-design/uido-live-test/issues/5), [OPS-003 #6](https://github.com/mccrystal111-design/uido-live-test/issues/6), [DES-001 #7](https://github.com/mccrystal111-design/uido-live-test/issues/7), [RND-001 #8](https://github.com/mccrystal111-design/uido-live-test/issues/8).

## Work completed in this session
- Created draft v0.1 of the provider-neutral course packet contract at `docs/architecture/COURSE-PACKET-SPEC.md`. It defines package layout, manifest/checksum requirements, course/hole model, coordinate/unit rules, provenance, validation gates, compatibility, offline/cache behavior, storage boundaries, acceptance tests and unresolved decisions.
- Explicitly left the archive format, storage provider/Supabase split, local coordinate generation and geometry cardinality open; no implementation or storage choice is claimed.
- DATA-001 moved from Ready to In progress. The draft has not been tested against a real packet yet and is not an approved geometry contract.

## Work completed in this session
- Created and refined [Course Packet Specification v0.1](../architecture/COURSE-PACKET-SPEC.md), including a comparison with PR #3's actual head-branch schemas.
- PR #3's feature schema currently accepts any object for `geometry`; it does not enforce GeoJSON structure, geometry-to-feature compatibility, coordinate semantics or cardinality. Provenance also needs feature-level links and a defined place for registration/error metrics. Treat these as fixture-driven schema gaps, not a blanket rejection of the draft.
- The next data-workstream step is still to locate and inspect the actual current Overstone and Poult Wood builder outputs, then create a fixture and validator plan. No builder code was changed and no fixture tests were run.
- OPS-002 remains delegated/separate; do not repeat its workflow investigation in this workstream.

## Active context
- Concept PNG supplied on 2026-10-02; place unchanged on dedicated Figma reference page.
- Design: warm ivory, forest green, golden-yellow circular mark, restrained topographic/course imagery. Correct errors; don't reinterpret via image generation.
- AGNOSTIC45: extend proven geometry-driven par-4/5 base; tee, fairway, rough, green, bunkers, water, paths; no labels/profile/UI overlays.
- Course geometry: establish canonical hole-by-hole source and provenance before renderer extension.
- Live hole UI: verify GPS, F/M/B yardages, bunker distances, orientation, viewfinder and right-side panels.
- Stats: Handicap (Official + Practice, edit/connect, explanation and 9-hole WHS-aligned handling), Performance, Scoring, Driving, Approach, Short Game.
- Supabase: classify data and offline/sync/security needs before deciding its responsibilities. The connector returned no accessible projects on 2026-10-02, so confirm intended project/account before implementation.
- Playwright/Chromium: no direct interactive browser-control tool is exposed in the chat session, but repository-hosted GitHub Actions Playwright routes are available. AG45 QA run #36925474787 passed. Dashboard-specific QA workflow was added in commit `9bc63015d319a79b0dc7f946137081d54cde5415`; run [#36982461137](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137) passed at 390×844 and 1440×900, confirming HTTP 200, live data, no browser errors/failed responses and no horizontal overflow. [Artifact](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137/artifacts/11216560509).
- Real-Golfer Trigger Principle applies to all live-product workflows.
- Workflow triggers may run normally when configured; use manual dispatch/reruns only when needed. Preserve human approval for product and visual decisions.

## End-of-session protocol
Update action status and evidence, CURRENT-STATE with one next action, decisions and verified changes, and this handover. State blockers and any required human action. Do not claim tests passed without evidence. Update the tool/access register whenever a tool, access route, permission or procedure changes.
