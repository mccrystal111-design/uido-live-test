# UiDo Session Handover

Updated: 2026-10-02

## First read
1. CURRENT-STATE.md
2. ACTION-REGISTER.md
3. DEPENDENCIES.md
4. DECISION-LOG.md

## Immediate next action
OPS-002: inspect actual repository source, recent commits and relevant workflow runs, then reconcile statuses against evidence. Dashboard Pages fix is committed; verify the normal push-triggered deployment. Current AGNOSTIC45 status remains unverified.

## Project links
- Repo: https://github.com/mccrystal111-design/uido-live-test
- [Live dashboard page](../../project-dashboard.html) — intended published URL: https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html (publication not verified yet).
- Figma: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI
- Figma dashboard design page: 02 — Project Dashboard.
- Issues: [OPS-002 #5](https://github.com/mccrystal111-design/uido-live-test/issues/5), [OPS-003 #6](https://github.com/mccrystal111-design/uido-live-test/issues/6), [DES-001 #7](https://github.com/mccrystal111-design/uido-live-test/issues/7), [RND-001 #8](https://github.com/mccrystal111-design/uido-live-test/issues/8).

## Active context
- Concept PNG supplied on 2026-10-02; place unchanged on dedicated Figma reference page.
- Design: warm ivory, forest green, golden-yellow circular mark, restrained topographic/course imagery. Correct errors; don't reinterpret via image generation.
- AGNOSTIC45: extend proven geometry-driven par-4/5 base; tee, fairway, rough, green, bunkers, water, paths; no labels/profile/UI overlays.
- Course geometry: establish canonical hole-by-hole source and provenance before renderer extension.
- Live hole UI: verify GPS, F/M/B yardages, bunker distances, orientation, viewfinder and right-side panels.
- Stats: Handicap (Official + Practice, edit/connect, explanation and 9-hole WHS-aligned handling), Performance, Scoring, Driving, Approach, Short Game.
- Supabase: classify data and offline/sync/security needs before deciding its responsibilities.
- Real-Golfer Trigger Principle applies to all live-product workflows.
- Workflow triggers may run normally when configured; use manual dispatch/reruns only when needed. Preserve human approval for product and visual decisions.

## End-of-session protocol
Update action status and evidence, CURRENT-STATE with one next action, decisions and verified changes, and this handover. State blockers and any required human action. Do not claim tests passed without evidence.