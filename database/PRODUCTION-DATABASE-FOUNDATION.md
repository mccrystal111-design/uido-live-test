# UiDo Production Database Foundation

Date: 2026-10-05

Supabase project: `uido-production`  
Region: `eu-west-2` (London)

## Canonical domain

The production database foundation separates:

- course identity
- immutable course revisions
- hole/routing data
- tee sets and hole tee positions
- physical course features
- source records and source snapshots
- feature-level provenance

Spatial data uses PostGIS and WGS84/EPSG:4326 at the database boundary. Internal calculations remain metric; UI conversion to yards/feet happens at the application boundary.

## Tables established

- `profiles`
- `courses`
- `course_versions`
- `course_holes`
- `tee_sets`
- `hole_tees`
- `course_features`
- `course_sources`
- `course_source_snapshots`
- `feature_provenance`
- `course_version_sources`

## Design rules

1. A course has stable identity; corrections create a new course version.
2. A course version is immutable once published.
3. Physical geometry is stored independently of hole relationships so shared features do not have to be cloned.
4. Source provenance is retained; canonical geometry never silently replaces evidence.
5. Kite consumes canonical course data; UiDo Core owns customer activity and the canonical course database.
6. Rendering remains a separate consumer of the same course model.
7. Round/player data remains separate from course data.
8. Supabase stores the live canonical/indexed database; delivery packets remain a separate versioned boundary.
9. Overstone is the first production fixture and must pass canonical validation before publication.

## Current status

Database foundation: **in progress**

Overstone canonical import: **not yet published**

User authentication/profile policies: **live; owner-only profile access is configured**

Course publication read policies: **live; clients can read active courses and published versions only**

Round/shot persistence policy hardening: **draft migration prepared, not applied**

Course packet delivery: **QA packet generator and manifest exist; actual app offline-loader integration remains open**

## Important

The existing Overstone builder already produces a provider-neutral model with 18 holes, routing, tees, fairways, green F/M/B points, hazards, provenance and source-preservation rules. The production import must consume that model rather than rebuild course geometry backwards from Hawk.


## Round/shot integrity checkpoint — 2026-10-09

The live database currently contains one Overstone course version, `v1-osm-source`, with status `draft`; there are no published course versions. There are also zero UiDo customer profiles, rounds, round-hole rows or shot rows. No live round/shot persistence test has been performed.

Read-only policy inspection found that course reads are limited to active courses and published versions, but the current round insert policy checks only `auth.uid() = user_id`. That leaves a direct-client data-integrity gap: the policy does not itself require a matching published course version, and shot policies do not verify that referenced rounds/holes belong to the same user/round.

A candidate hardening migration is available at `database/migrations/20261009_round_persistence_integrity.sql`. **It is draft-only and has not been applied to production.** It tightens round creation to active courses + published versions, validates tee-set/version and hole/version relationships, and checks shot ownership/round-hole consistency. Apply it only after review and tests in an isolated QA Supabase project.

The legacy `hawk.html` prototype now identifies its data source as Kite and preflights course/version/tee-set context before attempting a round insert. The browser contract test uses a mocked Supabase client and must not be treated as evidence of live database persistence. Live validation remains blocked until an isolated QA project and a published test course version are available.
