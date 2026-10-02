# UiDo Master Action Register

Statuses below are planning baselines unless linked evidence confirms completion. The live dashboard is [project-dashboard.html](../../project-dashboard.html). Track work in GitHub issues; do not maintain duplicate status trackers.

| ID | Workstream | Action | Priority | Status | Owner | Dependencies | GitHub issue / acceptance criteria |
|---|---|---|---|---|---|---|---|
| OPS-001 | Project control | Create durable control pack | P0 | Done | ChatGPT | — | Docs committed and linked from repo root |
| OPS-002 | Project control | Inspect repo, commits and workflows; reconcile status | P0 | In progress | ChatGPT | OPS-001 | [Issue #5](https://github.com/mccrystal111-design/uido-live-test/issues/5); deployment and AG45 QA evidence recorded; dashboard-specific browser QA and zero-job workflow failures still need diagnosis |
| OPS-003 | Project control | Create Issues and Project dashboard views | P0 | In progress | ChatGPT + Kieron | OPS-002 | [Issue #6](https://github.com/mccrystal111-design/uido-live-test/issues/6); Today/Next, Board, Roadmap, Blocked and Awaiting Kieron views accessible |
| DES-001 | Design | Place concept PNG unchanged on Figma reference page | P0 | Ready | ChatGPT | Figma file exists | [Issue #7](https://github.com/mccrystal111-design/uido-live-test/issues/7); PNG visible on dedicated page, source unchanged |
| DES-002 | Design | Verify and approve palette from reference | P1 | Backlog | ChatGPT + Kieron | DES-001 | Actual swatches/HEX values documented and approved |
| DES-003 | Design | Refine wordmark typography, spacing and circular mark | P1 | Backlog | ChatGPT | DES-002 | Editable vector inspected at full/small sizes and approved |
| DES-004 | Design | Construct yellow ball/tee and flag icons | P1 | Backlog | ChatGPT | DES-002 | Clean editable vector geometry |
| DES-005 | Design | Export and validate SVG assets | P1 | Backlog | ChatGPT | DES-003, DES-004 | Transparent background, clean paths, rendered at target sizes |
| DES-006 | Design system | Define tokens and reusable components | P1 | Backlog | ChatGPT | DES-002, DES-003 | Figma styles/components documented |
| RND-001 | Renderer | Verify AGNOSTIC45 base and latest manual workflow result | P0 | In progress | ChatGPT + Kieron | OPS-002 | [Issue #8](https://github.com/mccrystal111-design/uido-live-test/issues/8); phone-bars candidate and last successful Playwright run inspected; standalone base needs its own QA evidence |
| RND-002 | Renderer | Confirm canonical hole-by-hole geometry contract | P0 | Backlog | ChatGPT + Kieron | RND-001 | Feature types, coordinate system, direction and provenance documented |
| RND-003 | Renderer | Continue AGNOSTIC45 from proven baseline | P1 | Blocked | ChatGPT | RND-001, RND-002 | Required par-4/5 base features render without UI overlays |
| CRS-001 | Course data | Validate geometry acquisition/refinement pipeline | P1 | Needs verification | ChatGPT + Kieron | OPS-002 | Source geometry, registration/error, refinement and provenance inspectable |
| CRS-002 | Course data | Define canonical course package | P1 | Backlog | ChatGPT + Kieron | CRS-001, RND-002 | Offline-ready package and validation rules documented |
| UI-001 | Live hole UI | Verify implementation against agreed requirements | P1 | Needs verification | ChatGPT + Kieron | RND-001 | GPS, FMB, bunker distances, orientation and panels recorded pass/fail |
| UI-002 | Live hole UI | Fix verified UI gaps | P1 | Backlog | ChatGPT | UI-001 | Each defect has reproduction steps and QA evidence |
| STAT-001 | Stats | Define information architecture and data contracts | P1 | Backlog | ChatGPT + Kieron | OPS-002 | Six agreed sections and handicap handling documented |
| STAT-002 | Stats | Specify 9-hole WHS-aligned Practice Handicap behaviour | P1 | Backlog | ChatGPT + Kieron | STAT-001 | Rules and edge cases documented; assumptions identified |
| DATA-001 | Data/storage | Map data packets and decide Supabase responsibilities | P1 | Ready | ChatGPT + Kieron | OPS-002 | Data, retention, access, offline/sync and security needs documented |
| ARCH-001 | Architecture | Define real-golfer trigger inventory and QA isolation | P0 | Ready | ChatGPT | OPS-002 | Every trigger has actor/event, conditions, permissions, idempotency and test isolation |
| QA-001 | QA | Establish evidence-based release checklist | P1 | Backlog | ChatGPT + Kieron | OPS-002 | Code, workflow, visual, mobile and product behaviour checks separated |
| DOC-001 | Handover | Maintain current state and session handover | P0 | Ongoing | ChatGPT | OPS-001 | Next action remains singular and evidence-backed |

P0 = blocks reliable continuation or establishes a critical rule. P1 = important next-stage work. Done requires acceptance criteria and evidence.