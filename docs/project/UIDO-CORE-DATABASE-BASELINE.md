# UiDo Core User Database — Baseline

Updated: 2026-10-09

## Architecture

UiDo Core is the complete customer/data model. Kite is the current customer-facing product brand. A customer has one permanent Supabase Auth identity; product/UI layers decide what to expose from Core. The legacy `hawk.html` file is a prototype harness, not a separate brand.

## Live Supabase customer-data model

- `uido_profiles` — Auth-linked core customer identity/profile; now includes home course, lifecycle status and retention timestamps.
- `uido_user_preferences` — mutable app preferences such as units, default tee and notifications.
- `uido_handicap_records` — historical handicap records by provider, including UiDo Practice Handicap and future WHS/GHIN integrations.
- `uido_equipment` — equipment history.
- `uido_clubs` — club inventory and carry-distance history.
- `uido_rounds` — permanent Round IDs, course/course-version linkage, tee selection, round/session type, timestamps, start GPS, course-selection method and device context.
- `uido_round_holes` — hole-by-hole score/putt records.
- `uido_shots` — full available UiDo shot flow, GPS, club, lie, wind, trajectory, shape, outcome, Free Aim/decision data, source data and UiDo interpretation.
- `uido_external_records` — provider-neutral storage for future Garmin, TrackMan, WHS, GHIN and other integrations, preserving original payloads separately from UiDo interpretation.

All customer-owned tables have RLS enabled and owner policies based on `auth.uid()`.

## Design principles

1. Capture rich Core data; simplify only at the product/UI layer.
2. Preserve historical data rather than overwriting it when equipment, handicaps, preferences or course versions change.
3. Preserve original third-party source data and store UiDo interpretation separately.
4. Give every round a permanent Round ID and retain the course version used.
5. Practice activity is first-class data, but is distinct from scored/official rounds.
6. Keep mutable preferences separate from historical player activity.
7. Design external integrations to be provider-neutral and extensible.
8. Do not constrain Core around one product screen or feature subset.

## Git-backed schema

The current schema snapshot is at:
`database/schema/uido-core-user-data-v1.sql`

The live database was applied directly and independently verified after creation. A formal Supabase migration file should be generated through the project's migration tooling when the schema is ready to be promoted into migration history.

## Known open items

- Exact Core schema-versioning strategy remains open.
- WHS/GHIN API integration details remain to be implemented.
- Offline storage/sync is a product capability to define later.
- The approximately five-year retired-customer recovery period followed by anonymization remains subject to final legal/privacy implementation.

## Security note

The Supabase security advisor still reports the existing PostGIS-managed `public.spatial_ref_sys` RLS finding, plus PostGIS-related infrastructure warnings. This was not introduced by the Core user-data build and should not be "fixed" by applying blanket RLS without appropriate policies.
