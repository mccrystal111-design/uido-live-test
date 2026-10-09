# UiDo — Current State

Updated: 2026-10-09.

## UiDo Core User Database — 2026-10-09

The first UiDo Core customer-data foundation is now live in Supabase project uido-production.

Core architecture:
- One permanent Supabase Auth identity follows a customer across Kite experiences and future product surfaces.
- Core stores the complete customer/data model; Kite is the current customer-facing brand. The legacy `hawk.html` file is a prototype harness, not a separate product brand.
- Customer-owned data is protected with RLS policies based on auth.uid().

Live customer tables:
- uido_profiles
- uido_user_preferences
- uido_handicap_records
- uido_equipment
- uido_clubs
- uido_rounds
- uido_round_holes
- uido_shots
- uido_external_records

The model supports:
- historical player data
- WHS/GHIN/UiDo handicap sources
- equipment and club/carry history
- multiple rounds/sessions per day
- permanent Round IDs
- course + Course Version linkage
- tee selection and rating/slope context
- practice sessions
- round-start GPS and course-selection method
- device context
- full available shot-flow data
- Free Aim decision data
- original third-party source payloads plus separate UiDo interpretation
- future provider integrations such as Garmin and TrackMan

Git-backed references:
- docs/project/UIDO-CORE-DATABASE-BASELINE.md
- docs/project/Q&A-UIDO-USER-DATABASE-CORE.md
- database/schema/uido-core-user-data-v1.sql

Schema-versioning strategy remains open. Offline/sync and WHS/GHIN API implementation remain future work.

No GitHub Actions were manually rerun for this database build.

## Project control

Use docs/project/NEW-CHAT-STARTER.md as the new-chat orientation point and read the Core database baseline/Q&A before further Core database work.
## Execution checkpoint — 2026-10-09

### Yardage field-mirror playground — browser QA passed

The existing `ring-playground.html` has been tested in Chromium at **390×844** and **1440×900**. The successful run verified:
- 18 finished-UI objects and 18 mirror targets at both viewports.
- Semantic binding for `green.middle`.
- Changing the test value from 367 to 401 leaves layout geometry unchanged.
- Moving the bound UI element updates the mirror target to matching layout percentages.
- JSON field/layout export and finished-UI PNG export both download; the JSON uses the `uido-yardage-field-layout-v1` schema.
- No browser console errors, page errors or HTTP failures; no horizontal overflow.

Evidence: [Ring Playground Browser QA run](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37912037681). This is functional browser QA, not a visual-design approval or pixel-level Figma review.

The playground code also fixes the font-size inspector mapping. The QA test now measures the target after scrolling it into view, avoiding the earlier false drag failure caused by stale viewport coordinates.

### Core persistence prototype — syntax fixed, end-to-end path not yet proven

`hawk.html` is a **legacy prototype filename**, not a decision to restore Hawk as a separate customer-facing brand. Kite remains the current product brand.

- The inline script previously contained literal backslash-n sequences in JavaScript code, which broke parsing of the auth and persistence logic. The line breaks and CSV export newline escape have been corrected.
- A dedicated static workflow now extracts the inline JavaScript and runs `node --check`. It passed: [Core Prototype Static QA](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37911801415).
- The code contains Supabase Auth/profile, round, round-hole and shot persistence operations, but the live database path has **not** been demonstrated end to end.

Verified production state:
- Only the `uido-production` Supabase project is visible through the current connection; no separate QA project is available in the current access.
- `uido_profiles`, `uido_rounds`, `uido_round_holes` and `uido_shots` each currently contain zero rows.
- The Overstone revision `v1-osm-source` is still `draft`; public read policies expose course versions/holes/features/tees only when the version is `published`.
- `uido_rounds.course_id` and `course_version_id` are required UUID foreign keys, while the prototype presents these fields as optional free text. This UI/schema contract must be reconciled before a reliable round can be created.

Do not insert synthetic customer/round/shot records into production. Track the blocked end-to-end test in [CORE-001, issue #9](https://github.com/mccrystal111-design/uido-live-test/issues/9).

### Overstone course packet — real fixture inspected, draft retained

The committed source-normalized and canonical files and live Supabase revision were compared. A new deterministic adapter reproduces the 159-feature / 18-route canonical draft from the pinned fixture, and [fixture acceptance QA passed](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37912622803). Course-level validation remains incomplete due to satellite registration and hole-feature association. The separate live-acquisition / generic builder path still emits a different output shape, and the runtime package's green F/M/B anchor boundary must be reconciled. The course-packet spec records the evidence and gates.

See [Course Packet Specification, real fixture review](../architecture/COURSE-PACKET-SPEC.md#11-real-overstone-fixture-review--2026-10-09). Do not publish or regenerate over the existing draft until the producer/input/contract mismatch is resolved.

### Next action

**DATA-001 / CRS-002:** reconcile the pinned-fixture adapter with the live-acquisition / generic builder path and settle the runtime package boundary for green F/M/B anchors ([issue #10](https://github.com/mccrystal111-design/uido-live-test/issues/10)). Preserve the existing Yardage and AGNOSTIC45 baselines. Core end-to-end validation remains blocked until an isolated QA environment and a published course fixture are available.
