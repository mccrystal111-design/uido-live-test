# UiDo Dependencies and Delivery Sequence

## Critical dependencies
1. Project control → tool/access register → repository reconciliation → dashboard.
2. Reference PNG → palette approval → logo/icon vectors → SVG validation → design tokens/components → screen design → implementation comparison.
3. Renderer baseline verification → canonical geometry contract → AGNOSTIC45 base → live-hole UI integration/QA.
4. Course source geometry/provenance → registration/refinement validation → canonical course package → offline/render integration.
5. Stats information architecture → data contracts → handicap/9-hole rules → implementation and QA.
6. Data/storage requirements → data model and offline/sync needs → Supabase decision and implementation.
7. Trigger inventory → product event/condition contracts → isolated tests → production activation.

## Rules
- Do not refine renderer geometry against an unverified geometry contract.
- Do not finalise UI styling before tokens and assets are approved.
- Do not implement handicap calculations from assumptions; document WHS/GHIN rules and unsupported competition-specific handling.
- Do not choose Supabase for every data type before classifying access, retention, sync and offline needs.
- Never activate a live trigger because a development workflow or test ran.
- Let configured Actions triggers run normally; use manual dispatch/reruns only when useful and avoid unnecessary duplicates.
- Verify tool access and permissions before planning work that depends on them; the Tool & Access Register records known routes and gaps.
- Dates remain unset until scope, dependencies and available time are reviewed.

## Logical critical paths
OPS-002 → OPS-003
DES-001 → DES-002 → DES-003/DES-004 → DES-005/DES-006
RND-001 → RND-002 → RND-003 → UI-001/UI-002
CRS-001 → CRS-002
STAT-001 → STAT-002
ARCH-001 → QA-001
