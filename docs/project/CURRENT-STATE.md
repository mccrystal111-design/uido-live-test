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

