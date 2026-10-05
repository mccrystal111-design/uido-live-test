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
5. Hawk consumes canonical course data. It does not own the course database.
6. Rendering remains a separate consumer of the same course model.
7. Round/player data remains separate from course data.
8. Supabase stores the live canonical/indexed database; delivery packets remain a separate versioned boundary.
9. Overstone is the first production fixture and must pass canonical validation before publication.

## Current status

Database foundation: **in progress**

Overstone canonical import: **not yet published**

User authentication/profile policies: **next foundation slice**

RLS publication policies: **next foundation slice**

Course packet storage/delivery: **not yet selected**

## Important

The existing Overstone builder already produces a provider-neutral model with 18 holes, routing, tees, fairways, green F/M/B points, hazards, provenance and source-preservation rules. The production import must consume that model rather than rebuild course geometry backwards from Hawk.
