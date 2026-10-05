# UiDo Decision Log

| ID | Date | Decision | Rationale / scope | Status |
|---|---|---|---|---|
| DEC-001 | 2026-10-02 | GitHub control pack is durable project-management source of truth | Versioned alongside code and survives chat resets | Accepted |
| DEC-002 | 2026-10-02 | Figma is visual design source of truth; GitHub is implementation/source control | Separates approved design from reference art and code | Accepted |
| DEC-003 | 2026-10-02 | Configured GitHub Actions may run on their normal triggers; use manual dispatch/reruns when useful and avoid unnecessary duplicates | Automation is permitted; workflow triggers must be fit for purpose and live-product side effects isolated from development/QA | Accepted |
| DEC-004 | 2026-10-02 | Real-Golfer Trigger Principle | Product triggers map to real golfer actions, relevant real-world conditions/events or justified support processes; isolate development/QA | Accepted |
| DEC-005 | 2026-10-02 | Supplied concept board is visual direction, not production artwork | Preserve theme while correcting geometry in editable vectors | Accepted |
| DEC-006 | 2026-10-02 | AGNOSTIC45 extends the proven base rather than rebuilding | Geometry-driven par-4/5 base, without labels/profile/UI overlays | Accepted |
| DEC-007 | 2026-10-02 | Start with GitHub Projects for glanceable dashboard | Avoid extra tool until native views are assessed | Proposed |
| DEC-008 | 2026-10-02 | Stats order: Handicap, Performance, Scoring, Driving, Approach, Short Game | Official + Practice handicap; 9-hole handling aligned with WHS | Accepted |
| DEC-009 | 2026-10-05 | Wind tile flow: selecting a wind direction immediately advances to the Lie tile | Wind is a single selection step; there is no separate Continue action after direction selection. The playground may represent the Wind tile visually, while live wind data/interaction can be implemented later. | Accepted |
| DEC-010 | 2026-10-05 | Yardage screen long-press opens screen help | A long press on the yardage ring should open a concise help overlay explaining the screen's abbreviations, values and controls (including F/M/B, GSB, FWB, bunker distances, yellow selected/primary yardage, and bottom-ring controls such as Wind/Lie). Keep the normal ring visually clean; implementation is separate from this layout review. | Accepted |
| DEC-011 | 2026-10-05 | The yardage playground represents the finished golfer-facing HTML page, not an annotated design/inspection canvas | Visible production UI must contain only purposeful golfer-facing information or controls. Design/editor annotations such as `TOP RING`, `BOTTOM RING`, coordinate grids, selection boxes, inspectors and other authoring aids must remain outside the rendered/exported UI. Ring geometry may remain an implementation/layout construct but must not become user-facing concepts. Placeholder values are permitted only as test data for live/data-driven fields; production fields must be bound to real data. | Accepted |

## Trigger design requirements
Document initiating actor/event, golfer need, preconditions/permissions, connectivity/offline behaviour, idempotency/retries, failure/cancellation, test isolation, and evidence for each live trigger.
