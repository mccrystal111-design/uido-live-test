# UiDo Decision Log

| ID | Date | Decision | Rationale / scope | Status |
|---|---|---|---|---|
| DEC-001 | 2026-10-02 | GitHub control pack is durable project-management source of truth | Versioned alongside code and survives chat resets | Accepted |
| DEC-002 | 2026-10-02 | Figma is visual design source of truth; GitHub is implementation/source control | Separates approved design from reference art and code | Accepted |
| DEC-003 | 2026-10-02 | Kieron manually triggers GitHub Actions; ChatGPT must not auto-rerun | Explicit operating boundary | Accepted |
| DEC-004 | 2026-10-02 | Real-Golfer Trigger Principle | Product triggers map to real golfer actions, relevant real-world conditions/events or justified support processes; isolate development/QA | Accepted |
| DEC-005 | 2026-10-02 | Supplied concept board is visual direction, not production artwork | Preserve theme while correcting geometry in editable vectors | Accepted |
| DEC-006 | 2026-10-02 | AGNOSTIC45 extends the proven base rather than rebuilding | Geometry-driven par-4/5 base, without labels/profile/UI overlays | Accepted |
| DEC-007 | 2026-10-02 | Start with GitHub Projects for glanceable dashboard | Avoid extra tool until native views are assessed | Proposed |
| DEC-008 | 2026-10-02 | Stats order: Handicap, Performance, Scoring, Driving, Approach, Short Game | Official + Practice handicap; 9-hole handling aligned with WHS | Accepted |

## Trigger design requirements
Document initiating actor/event, golfer need, preconditions/permissions, connectivity/offline behaviour, idempotency/retries, failure/cancellation, test isolation, and evidence for each live trigger.
