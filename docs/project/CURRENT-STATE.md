# UiDo — Current State

Updated: 2026-10-02. This is a partial snapshot from project context; verify live repository and workflow state before technical changes.

## Where we are
- Project control pack is being established; it must be reconciled against actual repository files and workflow runs.
- Figma file: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI . Initial editable foundations page exists. The chosen concept PNG is not yet embedded.
- Brand direction: warm ivory, forest green, golden-yellow circular mark, restrained topographic/course imagery and premium understated golf identity. Existing preferences include #3F4B3B, Montserrat and Bodoni Moda; verify actual palette from the concept before approval.
- AGNOSTIC45 goal: extend the proven geometry-driven base renderer for par-4/par-5 holes, supporting tee, fairway, rough, green, bunkers, water and paths, with no labels/player profile/UI overlays in the base.
- Course geometry: canonical hole-by-hole geometry and provenance should be agreed before extending renderer work.
- Live hole UI previously covered GPS/player position, front/middle/back green yardages, bunker distances, orientation, viewfinder and right-side info panels. Verify implementation before reopening defects.
- Stats sections: Handicap (Official + Practice, explanation/edit/connect and 9-hole WHS-aligned handling), Performance, Scoring, Driving, Approach, Short Game.
- Supabase is under consideration for data packets; define data and offline/sync needs before deciding storage architecture.
- Real-Golfer Trigger Principle applies to all product workflows.
- Kieron manually starts GitHub Actions; never automatically rerun them.

## Next action
OPS-002 — Inspect actual repository files, recent commits and relevant workflow runs, then reconcile this snapshot against evidence.

After reconciliation: create actionable GitHub Issues and Project views; then continue DES-001, placing the concept PNG unchanged on a dedicated Figma reference page.

## Unverified
Latest AGNOSTIC45 run status is not verified in this setup. No timeline dates have been agreed. Do not claim tests or visual QA passed without linked evidence.
