# UiDo Canonical Schema v0.1

This schema defines the boundary between evidence and canonical course data.

## Core entities

### Course
Identity and stable location for a golf facility.

- `course_id`
- `canonical_name`
- `club_name`
- `address`
- `country_code`
- `timezone`
- `location`
- `status`
- `created_at`
- `updated_at`

### CourseSourceId
Maps UiDo's course identity to an external provider identity.

- `course_id`
- `source_id`
- `external_course_id`
- `external_url`
- `first_seen`
- `last_seen`

This mapping does not make the external source canonical.

### CourseVersion
An immutable published or working snapshot.

- `course_version_id`
- `course_id`
- `version_number`
- `status`
- `effective_from`
- `effective_to`
- `parent_version_id`
- `change_reason`
- `created_at`
- `created_by`

### Hole
A hole belonging to exactly one course version.

- `hole_id`
- `course_version_id`
- `hole_number`
- `par`
- `stroke_index`
- `name`
- `status`

### Tee
A tee set for a course version.

- `tee_id`
- `course_version_id`
- `name`
- `colour`
- `gender`
- `course_rating`
- `slope_rating`
- `par`

### TeeHole
Per-tee, per-hole playing data.

- `tee_id`
- `hole_id`
- `yardage`
- `par`
- `stroke_index`

### Feature
Spatial course information.

- `feature_id`
- `hole_id`
- `feature_type`
- `geometry`
- `geometry_version`
- `confidence`
- `verification_status`

Feature types initially include:

- teeing_area
- fairway
- rough
- bunker
- water
- trees
- out_of_bounds
- green
- green_front
- green_back
- target
- carry_area
- layup_area

## Evidence entities

### Source
Describes an evidence provider and its licence/terms.

### SourceSnapshot
Immutable capture of a provider response or source artifact.

### Evidence
A normalized observation extracted from a source snapshot.

An evidence record should contain:

- `evidence_id`
- `source_snapshot_id`
- `entity_type`
- `entity_id` when a canonical match exists
- `attribute`
- `value`
- `geometry` when applicable
- `observed_at`
- `ingested_at`
- `confidence`
- `provenance`

## Issues and verification

### Issue
A customer report or internal discrepancy.

Issue types:

- HOLE_CHANGED
- TEE_CHANGED
- YARDAGE_WRONG
- PAR_WRONG
- SI_WRONG
- GREEN_CHANGED
- BUNKER_CHANGED
- WATER_CHANGED
- FAIRWAY_CHANGED
- OB_CHANGED
- COURSE_CLOSED
- COURSE_RENAMED
- COURSE_RECONFIGURED
- OTHER

### Verification
Records the investigation and decision.

Minimum fields:

- `verification_id`
- `issue_id`
- `evidence_ids`
- `decision`
- `reason`
- `verified_by`
- `verified_at`

## Change

A canonical change should identify:

- what changed
- old value/geometry
- new value/geometry
- evidence supporting the change
- issue that triggered it, if any
- author
- timestamp

## Attribute-level confidence

Do not use one global course confidence score.

Example:

- Hole 7 par: 0.99
- Hole 7 yardage: 0.97
- Hole 7 fairway geometry: 0.91
- Hole 7 green geometry: 0.84
- Hole 7 bunker geometry: 0.68

This allows UiDo to know exactly where further evidence or verification is needed.

## Geometry provenance

For each canonical geometry, retain:

1. canonical geometry
2. contributing source geometries
3. transformation/registration applied
4. evidence timestamp
5. verification state
6. confidence
7. change history

The original OSM geometry, for example, must remain recoverable even after imagery-based refinement.
