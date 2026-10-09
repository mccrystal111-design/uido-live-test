# UiDo Global Golf-Course Database

## Purpose

UiDo owns the canonical golf-course model.

External systems — GolfCourseAPI, OpenStreetMap, club websites, aerial imagery, LiDAR, launch-monitor/course datasets and other providers — are evidence sources. They may propose facts or geometry, but they do not define UiDo's canonical course.

**Core rule: External data can propose. UiDo decides.**

## Architecture

1. **Sources** — external providers and customer reports
2. **Acquisition** — fetch, normalize, snapshot and fingerprint source evidence
3. **Evidence** — immutable source observations with provenance
4. **Reconciliation** — compare evidence, detect conflicts and calculate attribute-level confidence
5. **Canonical model** — UiDo-owned versioned course data
6. **Verification** — human/automated review of conflicts and customer reports
7. **Publishing** — publish immutable course versions
8. **Delivery** — generate course packages consumed by the app/offline cache

The player-facing app must consume a published UiDo course version, not call an external course API as its source of truth.

## Repository model

The first implementation is deliberately Git-backed so that the model is inspectable, reviewable and reversible before introducing PostgreSQL/PostGIS.

Suggested layout:

```
database/
  README.md
  schema/
    course.schema.json
    feature.schema.json
    provenance.schema.json
    issue.schema.json
  courses/
    GB/
      ENG/
        overstone-park/
          course.json
          versions/
            v1/
              course.json
              holes.json
              tees.json
              features.geojson
              provenance.json
```

The canonical data format should remain portable to PostgreSQL/PostGIS later.

## Versioning rules

- A published course version is immutable.
- Corrections create a new course version.
- Previous versions remain available for audit and rollback.
- Geometry changes are versioned with the course version.
- Source observations are never overwritten; a new snapshot is added.
- Confidence is attached to individual attributes/features, not just to a course.

## Verification lifecycle

`REPORTED → TRIAGED → INVESTIGATING → EVIDENCE_COLLECTED → VERIFIED → CANONICAL_UPDATE → PUBLISHED`

A report may instead be rejected with a reason and retained as an audit record.

## First test

Overstone Park and Poult Wood are the first canonical-model fixtures. We should prove the model can represent both courses cleanly before changing the existing acquisition pipeline.
