# UiDo Course Pipeline

## Purpose

UiDo captures course information from several independent sources. This document defines the hand-off architecture so those sources are assembled once into a canonical course packet and downstream stages consume that packet instead of recapturing data.

## Pipeline

1. **Course Discovery**
   - GolfCourseAPI supplies course identity and metadata.
   - UiDo registry stores the normalised course record and acquisition requirements.
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
