# UiDo Course Pipeline

## Purpose

UiDo captures course information from several independent sources. This document defines the hand-off architecture so those sources are assembled once into a canonical course packet and downstream stages consume that packet instead of recapturing data.

## Pipeline

1. **Course Discovery**
   - `tools/course-discovery/search_golfcourseapi.py` queries GolfCourseAPI using the `GOLFCOURSEAPI_API_KEY` secret.
   - `.github/workflows/discover-course.yml` provides the GitHub Actions search front door.
   - `.github/workflows/register-course.yml` registers a selected provider course and commits the normalised registry record.
   - Registration captures the complete GolfCourseAPI detail response under `course-models/provider-data/golfcourseapi/` and builds the canonical UiDo scorecard/tee packet under `course-models/scorecards/`.
   - Registration is cache-first: an existing provider snapshot is reused without another GolfCourseAPI call. A fresh provider pull requires the explicit `refresh_provider` workflow input.
   - `tools/course-discovery/validate_scorecard_packet.py` validates 18-hole structure, hole numbering, tee totals and provider provenance before a registration run can commit.
   - UiDo registry stores a stable UiDo identity, provider identity, location metadata and lifecycle state.
   - Discovery/registration does not invent a physical boundary or silently acquire geometry.
2. **Course Acquisition**
   - OSM golf data.
   - OSM fairway multipolygon relations.
   - EA vertical aerial imagery where available.
   - EA National LiDAR DTM and DSM.
3. **Course Packet QA**
   - Validate the standard packet structure and 18-hole target references.
4. **Downstream processing**
   - Wireframe.
   - Terrain/feature processing.
   - Course model.
   - Later UiDo course-loader packaging.

## Hand-off rule

The **course packet is the source hand-off between stages**.

A downstream stage must consume the packet produced by acquisition. It must not silently return to Overpass, EA, or another source to recapture the same input.

This gives us deterministic debugging:

source capture -> packet -> processing -> output

rather than:

source capture -> processing -> fresh source capture -> output

## Course discovery / registration

GolfCourseAPI is the discovery/index provider, not the physical geometry authority. The provider ID is retained for provenance, while UiDo assigns a deterministic permanent course identity. A newly registered course starts at lifecycle state `registered`; it becomes `acquisition-ready` only after the physical acquisition inputs are resolved.

## GitHub workflow structure

- `.github/workflows/build-course-ea.yml`
  - Reusable acquisition stage.
  - Still supports standalone manual execution.
- `.github/workflows/build-course.yml`
  - Master orchestration workflow.
  - Calls acquisition.
  - Downloads the acquisition artifact.
  - validates the packet contract.
  - republishes the validated packet as `uido-course-packet-<course-id>`.

Future downstream stages should be added as separate reusable workflows called by the master pipeline.

## Iteration rule

Acquisition and processing are versioned independently.

If wireframe logic changes:
- reuse the existing course packet;
- rerun wireframe;
- do not recapture source data unless the source itself is intentionally refreshed.

If acquisition changes:
- create a new packet;
- retain the old packet for comparison where practical.

## Project hand-over

`PROJECT_STATUS.md` is the persistent human-readable hand-over document. It must record:
- current pipeline stage;
- last verified run/artifact;
- current blocker;
- exact next action;
- anything that must not be rebuilt.

The repository, packet manifests and workflow outputs are the technical memory. Chat history is context, not the source of truth.


## Canonical model stages — 2026-10-09

Both stages use `uido.course.canonical.v2`, but they have distinct provenance labels and must not overwrite one another silently:

- **`source_only_draft`** — reproducible output from a pinned source-normalized fixture. Physical features retain stable source IDs and provenance at course scope; hole records contain routing plus green F/M/B anchors. Physical-feature/hole association and satellite registration may remain unresolved. This is the current committed Overstone draft.
- **`enriched_candidate`** — output from the acquisition/intermediate-model path. It may carry per-feature association evidence from nearest-hole/nearest-green heuristics. That evidence is useful for review but is not verified association. The canonical builder must keep `validation.course_complete=false` until registration and associations are explicitly verified and green anchors/routes are complete.

`.github/workflows/validate-canonical-v2.yml` is a **manual live-acquisition candidate workflow**: it fetches fresh Overpass data to exercise the candidate path. It is not a downstream consumer of the pinned source fixture and must not overwrite the source-only draft or publish a course. Deterministic acceptance tests use committed fixtures and do not call external providers.

Promotion to a publishable course revision is a separate, explicit step after geometry validation, measured satellite registration, association review, packet generation and RLS/package QA all pass.
