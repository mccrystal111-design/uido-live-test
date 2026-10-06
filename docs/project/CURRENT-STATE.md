# UiDo — Current State

Updated: 2026-10-06.

## UiDo Core User Database — 2026-10-06

The first UiDo Core customer-data foundation is now live in Supabase project uido-production.

Core architecture:
- One permanent Supabase Auth identity follows a customer through Hawk and full UiDo.
- Core stores the complete customer/data model; Hawk is a simplified product variant.
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
## Hawk → Core integration — 2026-10-06

Hawk is now connected to the UiDo Core customer-data foundation at the first round/shot persistence layer.

- Starting a Hawk round creates a permanent `uido_rounds` record.
- The round stores the authenticated customer, course/course-version/tee IDs when supplied, round type, course-selection method, start time, start GPS when available, and device/app context.
- Entering a hole creates the corresponding `uido_round_holes` record on demand.
- Score changes sync to the Core round-hole record.
- Record Shot syncs the shot to `uido_shots`, including GPS when available, timestamp, Hawk source identity, raw local shot data and device/app context.
- LocalStorage remains as a local cache; it is not the Core source of truth once a Core round is active.
- No GitHub Actions were manually rerun.

Next implementation checkpoint: validate the live Hawk → Supabase round/shot path, then build the Hawk front page on top of the real Core-backed customer/session model.
