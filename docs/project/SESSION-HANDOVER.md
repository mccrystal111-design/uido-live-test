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
OPS-002 remains the priority. Dashboard Playwright evidence and AGNOSTIC45 base QA are confirmed. I rechecked jobs for runs #36982036792 and #36982882178; both return zero jobs. The connected GitHub tool surface in this session does not expose workflow-run metadata/listing, and public web opening of the run pages is unavailable, so the event/workflow/conclusion details needed to explain these records cannot be retrieved here. Do not rerun them blindly. Next: inspect the run detail pages in GitHub Actions (run #36982882178 and #36982036792) to capture workflow name, event, conclusion and check-suite annotations; then use that evidence to disposition the failures. No owner decision is needed unless GitHub itself reports an access/permission restriction. Tool/access register has been created and is now part of mandatory session startup. Dashboard copy no longer tells the user to run Actions manually; deployment [#36982434145](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982434145) succeeded after the copy correction. Dashboard-specific Playwright run [#36982461137](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137) passed at 390×844 and 1440×900; artifact [screenshots/report](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137/artifacts/11216560509). It confirmed HTTP 200, expected page content, live GitHub data, no browser console/page errors, no failed HTTP responses and no horizontal overflow. AG45 phone-bars QA [#36925474787](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36925474787) and standalone base QA [#36982883414](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982883414) both passed. Base QA artifact: [screenshots and diagnostics](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982883414/artifacts/11216462231).

## Project links
- Repo: https://github.com/mccrystal111-design/uido-live-test
- [Live dashboard page](../../project-dashboard.html) — intended published URL: https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html (deployment run succeeded; direct browser confirmation remains outstanding).
- Figma: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI
- Figma dashboard design page: 02 — Project Dashboard.
- Tool/access register: [TOOL-AND-ACCESS-REGISTER.md](TOOL-AND-ACCESS-REGISTER.md)
- Issues: [OPS-002 #5](https://github.com/mccrystal111-design/uido-live-test/issues/5), [OPS-003 #6](https://github.com/mccrystal111-design/uido-live-test/issues/6), [DES-001 #7](https://github.com/mccrystal111-design/uido-live-test/issues/7), [RND-001 #8](https://github.com/mccrystal111-design/uido-live-test/issues/8).

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
