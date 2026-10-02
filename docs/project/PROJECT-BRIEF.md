# UiDo — Project Brief
Last reviewed: 2026-10-02

## What UiDo is
UiDo is a golf decision engine and virtual caddie: it helps a golfer decide what to do next using course geometry, location and conditions, player-specific information, shot context, and performance history. Its purpose is to support clearer decisions on the course and useful reflection afterwards—not to add distraction.

Brand/product idea: “U + Intelligence = Decision Optimised.” The product should feel focused, purposeful and quiet. Process over outcome; useful guidance over noise.

## Product principles
- **Real-Golfer Trigger Principle:** every live-product workflow should map to a genuine golfer action, a relevant real-world event/condition, or a justified support process. Development, deployment and QA activity must be isolated from live-user side effects.
- **Source before assumption:** inspect current code, data, workflow results and design references before changing or declaring something complete.
- **Extend the proven base:** especially for AGNOSTIC45, extend the existing geometry-driven renderer; do not rebuild it without evidence and an explicit reason.
- **Evidence-based status:** a green workflow proves that run passed, not that the whole product is correct. Separate implemented, tested, visually checked and product-approved.
- **Human product ownership:** Kieron owns product scope, priorities, design/visual approval and product trade-offs. ChatGPT can implement agreed work and make reversible implementation choices within those constraints.
- **Normal automation is allowed:** configured GitHub Actions can run on their normal push/schedule/dispatch triggers. Use manual dispatches or reruns when useful; avoid unnecessary duplicate runs.
- **Offline-first awareness:** golf-course use may have limited connectivity. Evaluate offline packages, local device sensors, sync, data access and failure behaviour when designing architecture.

## Current brand direction
Warm ivory, forest green, golden-yellow circular mark, restrained topographic/course imagery, premium understated golf identity. A known green reference is #3F4B3B; Montserrat and Bodoni Moda have been explored. Treat these as references, not final tokens, until checked against the original concept and approved. Do not reinterpret supplied reference art when the task is faithful tracing or conversion.

## Product areas
- **On-course hole view:** course orientation and geometry, player/GPS position, front/middle/back green distances, bunker distances, wind/lie context, a clear viewfinder and compact supporting information.
- **AGNOSTIC45 renderer:** geometry-driven base for par-4 and par-5 holes. Core features include tee, fairway, rough, green, bunkers, water and paths. Keep player profile, labels and UI overlays out of the base renderer.
- **Course acquisition and model:** preserve source geometry and provenance; register/refine geometry against imagery with errors and transformations recorded. Establish canonical hole-by-hole geometry before extending renderer behaviour.
- **Stats:** Handicap (Official + Practice), Performance, Scoring, Driving, Approach and Short Game. Handicap work includes clear explanation/edit/connect and 9-hole handling aligned with WHS/GHIN rules; verify governing rules before specifying calculations.
- **Data and sync:** Supabase is available for consideration. Decide responsibilities from actual data packets, access/security, retention, offline and sync needs rather than assuming all data belongs there.

## Technical/project home
- Repository: https://github.com/mccrystal111-design/uido-live-test
- Live project dashboard: https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html
- Figma: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI
- Project-control entry point: docs/project/README.md
- Current status and next action: docs/project/CURRENT-STATE.md
- Work register: docs/project/ACTION-REGISTER.md
- Decisions: docs/project/DECISION-LOG.md
- Handover: docs/project/SESSION-HANDOVER.md

## Working protocol for any new chat
1. Read this brief, then CURRENT-STATE.md, ACTION-REGISTER.md, DEPENDENCIES.md, DECISION-LOG.md and SESSION-HANDOVER.md as relevant.
2. Inspect the current repository branch/files and relevant commit/PR/workflow evidence before coding. The repo is the implementation source of truth; docs summarize it and must be reconciled when stale.
3. Identify the single next unblocked action and its acceptance criteria. Avoid reopening completed work without new evidence.
4. Make focused changes; test what can be tested; record exactly what was and wasn't verified.
5. Update relevant issue(s), current state, changelog and handover when work changes status.
6. Do not claim a change, test, deployment or visual review happened unless there is evidence.
7. Do not trigger a workflow merely because it exists. Let configured triggers run normally; use manual triggers only when useful. Never let QA/development triggers affect real golfers.
8. Ask Kieron only for genuine product decisions, visual approvals, access limitations or blockers that cannot be resolved from source evidence.

## Important distinction
This brief is the stable orientation layer, not a substitute for live evidence. The dashboard is a navigation/status surface; source code, issue records, commit diffs, workflow results and approved design references determine what is actually true.
