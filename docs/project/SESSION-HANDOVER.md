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
OPS-002: inspect actual repository source, recent commits and relevant workflow runs, then reconcile statuses against evidence. Tool/access register has been created and is now part of mandatory session startup. Dashboard Pages fix is committed; normal push-triggered deployment succeeded in run [#36979995902](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36979995902). Current AGNOSTIC45 status remains unverified. Live dashboard rendering also remains unverified in a real browser.

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
- Playwright/Chromium: no direct browser-control integration was exposed in the current session. Do not claim a Playwright run until an executable runtime or browser service is verified.
- Real-Golfer Trigger Principle applies to all live-product workflows.
- Workflow triggers may run normally when configured; use manual dispatch/reruns only when needed. Preserve human approval for product and visual decisions.

## End-of-session protocol
Update action status and evidence, CURRENT-STATE with one next action, decisions and verified changes, and this handover. State blockers and any required human action. Do not claim tests passed without evidence. Update the tool/access register whenever a tool, access route, permission or procedure changes.
