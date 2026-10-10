# UiDo Session Handover

Updated: 2026-10-10

## First read
1. [Project control pack](README.md)
2. [Tool & access register](TOOL-AND-ACCESS-REGISTER.md)
3. CURRENT-STATE.md
4. ACTION-REGISTER.md
5. DEPENDENCIES.md
6. DECISION-LOG.md

## Immediate next action

**CORE-001 / issue #9: arrange a genuinely isolated Supabase QA environment and a published course fixture, then validate the live Auth → profile → round → hole → shot path.** The browser contract is green in [run 38080864650](https://github.com/mccrystal111-design/uido-live-test/actions/runs/38080864650), and the draft RLS migration passed against ephemeral PostgreSQL in [run 37915117865](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37915117865). The browser test also exposed and fixed a real startup ReferenceError in `hawk.html`. These tests use mocks/isolated PostgreSQL and do **not** prove live Supabase persistence. Only `uido-production` is currently available and the Overstone revision is still draft; do not insert synthetic customer/round/shot records into production or apply the draft migration there.

Once isolated live persistence is unblocked, resume **DATA-001 / CRS-002**: reconcile the pinned-fixture adapter with the live-acquisition / generic builder path and finish offline packet-loader integration and promotion gates. Read section 11 of [COURSE-PACKET-SPEC.md](../architecture/COURSE-PACKET-SPEC.md#11-real-overstone-fixture-review--2026-10-09) and [issue #10](https://github.com/mccrystal111-design/uido-live-test/issues/10). Do not publish the existing course draft until measured registration and verified physical-feature/hole associations are resolved.

## Previous immediate next action

**Kieron's requested field test: radial tile + GPS capture at the ball.** Open the standalone [Shot Capture + GPS test](../../overstone/shot-capture-gps-test.html) or intended published URL https://mccrystal111-design.github.io/uido-live-test/overstone/shot-capture-gps-test.html on the phone. Allow location access, wait for a fix, tap a radial tile, select its value, and tap **HIT SHOT** to save that shot's decision snapshot. Use **Score** and **Putts** for hole-level values, then **Export JSON**. Compare captured phone coordinates/timestamps/accuracy with the Garmin watch and review the plotted points against the Overstone wireframe. The page is additive and does not alter the existing hole renderer. It stores events in browser local storage until export or clear. **No on-course/device test has yet been performed, and live Pages publication could not be verified from this session.** If the URL is not live yet, check the normal Pages deployment; do not manually rerun Actions without a reason.

- Latest full decision-capture implementation: [9b54d56](https://github.com/mccrystal111-design/uido-live-test/commit/9b54d56bb9fa200771887f87b1af30986ecd9764). Categories include Yardage, UiDo Caddie, Wind, Lie, Club, Strike, Trajectory, Start, Shape, Score and Putts. Export includes raw events and shot snapshots with GPS metadata. The category vocabulary is a field-test starting point, not yet a canonical product contract.
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

## Latest work — Figma, Yardage v4 and Hawk/V5 — 2026-10-05

- **Figma:** Approved yardage source is UiDo Yardage — Source Recreation, node 8:24, 360×780, on 02 — Product UI in the UiDo — Brand & Product Design System file.
- **Yardage v4:** overstone/yardage-v4.html is the fresh Figma-derived visual baseline. Kieron confirmed the visual result is correct. Keep v4 as a test/reference baseline; do not alter it for Hawk/V5 unless explicitly requested.
- **Hawk/V5:** this is a separate new product experience currently in Q&A discovery only. Do not start implementation until discovery is complete and the cumulative decisions are agreed.
- Current Hawk decisions: Start Round / Scores / Stats on the start screen; equal-sized controls with Start Round distinguished by colour; brief setup with Course + Tees + scoring format; GPS starts at app load; Start Round opens Hole 1 yardage; Score + Putts advances the hole; tapping the hole header opens a 6×3 selector containing only 1–18; selecting a hole closes the selector and opens that hole; GPS updates continuously, holds a stopped position when accuracy is better than 4m, and resumes live updates when movement restarts.
- Q&A discovery uses the new project-agnostic cumulative-memory protocol in NEW-CHAT-STARTER.md. Keep one cumulative copyable memory line after every answer and ask one question at a time.

## End-of-session protocol
Update action status and evidence, CURRENT-STATE with one next action, decisions and verified changes, and this handover. State blockers and any required human action. Do not claim tests passed without evidence. Update the tool/access register whenever a tool, access route, permission or procedure changes.


## 2026-10-05 clean-build checkpoint
- Continued directly from the canonical-build handoff; no prototype or renderer patching was used.
- Verified GitHub repo access and Supabase uido-production access.
- Persisted Overstone source-normalized evidence and canonical v1 model in GitHub.
- Imported Overstone v1 source evidence into Supabase as a draft canonical revision: 18 holes, 159 physical features, 159 provenance links.
- Next unblocked build action: reconcile the canonical geometry contract against the real Overstone model, then complete measured satellite registration/refinement rather than publishing the draft.


## 2026-10-09 execution checkpoint

- **Ring Playground Browser QA passed** at 390×844 and 1440×900: semantic binding, layout stability when values change, UI movement mirrored to the same geometry, JSON export, PNG export, no console/page/HTTP errors and no horizontal overflow. Evidence: [run 37912037681](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37912037681). This is functional browser QA, not Figma pixel-level visual approval.
- Fixed the literal JavaScript line-break corruption in `hawk.html` and the CSV newline escape. **Core Prototype Static QA passed**: [run 37911801415](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37911801415).
- Core end-to-end persistence remains unverified. The only accessible Supabase project is `uido-production`; the profile/round/hole/shot tables are empty, and the only course revision is draft. The prototype allows optional free-text course/version IDs although the schema requires UUID foreign keys. Production was not written to.
- Yardage field-mirror QA passed in Chromium at 390×844 and 1440×900: 18 UI objects matched 18 mirror targets, 16 field cards were present, semantic `green.middle` binding worked, changing the test value did not change geometry, dragging the UI moved the mirror, and JSON + PNG exports passed. No browser console/page errors or HTTP failures. [Run 37912037681](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37912037681); the tested HTML and workflow blobs match current main exactly.
- Inspected the committed Overstone source-normalized and canonical fixtures against live Supabase. The pinned adapter reproduces the 159-feature / 18-hole draft, including all 54 green F/M/B anchors. [Fixture/schema/gate QA run 37913598055](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37913598055) passed with six unit tests. A read-only coordinate comparison found no F/M/B differences over 5 cm between `course_green_data.json` and live Supabase. Course-level validation still flags satellite registration and hole-feature association; the pinned versus live-acquisition build path and offline package manifest remain unresolved. Findings are in section 11 of the course-packet spec and [issue #10](https://github.com/mccrystal111-design/uido-live-test/issues/10).
- A new P0 blocker is tracked as [CORE-001 / issue #9](https://github.com/mccrystal111-design/uido-live-test/issues/9). No GitHub Actions were manually rerun; the QA runs above were normal repository-triggered runs.

Next after promotion/packet-manifest implementation: resume measured satellite registration/refinement and explicit physical-feature/hole association. Preserve the approved Yardage and AGNOSTIC45 baselines.
