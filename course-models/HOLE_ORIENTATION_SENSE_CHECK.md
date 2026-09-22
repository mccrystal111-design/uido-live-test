# UiDo Hole Orientation & OpenYardage Sense Check

## Purpose

Use the player's current GPS position on/near the tee as the local origin, rotate the selected hole into its **direction of travel**, and perform a deterministic golf-useful sense check against OpenYardage's OSM-derived measurements.

This is a validation layer, not a replacement for UiDo course geometry.

## Local hole frame

For the selected hole:

1. Identify the tee/starting position from the UiDo course model.
2. Identify the playing direction from the hole routing geometry.
3. Establish a local coordinate frame:
   - **Y = forward along the direction of travel**
   - **X = lateral to the player's left/right**
   - origin = player's current GPS position when available; otherwise selected tee reference point.
4. Rotate/project all course geometry into this local frame.
5. Keep the original WGS84/projected coordinates unchanged. The local frame is a derived view/analysis representation only.

The important distinction is that the hole is **rotated to the direction of play**, not north-up. This makes the geometry directly useful for shot decisions and comparison.

## OpenYardage sense check

OpenYardage is used as an independent geometric reference because its published methodology is also based on OpenStreetMap. It states that hole length follows the line of play, with the hole projected onto that line and arc length counted from the tee; hazard carry distances are measured from the tee to the near and far edges. It also publishes green front/middle/back distances and green depth on supported courses.

For each hole UiDo should compare:

- tee → green middle distance
- tee → green front distance
- tee → green back distance
- green depth
- hazard near-edge carry
- hazard far-edge carry
- hazard lateral side (L/R)
- overall line-of-play geometry
- optional elevation change when LiDAR is available

## Acceptance philosophy

This is a **sense check**, not a survey comparison.

The question is:

> "Does UiDo's geospatial model produce golf distances and geometry that are broadly consistent with an independent OSM-derived yardage calculation when viewed from the tee in the direction of travel?"

Small differences are expected because:
- tee selection may differ;
- OpenYardage and UiDo may choose different line-of-play representations;
- green F/M/B are derived points rather than survey targets;
- GPS itself has finite positional accuracy.

Large discrepancies should trigger QA rather than automatic geometry changes.

## Diagnostic output

For each hole produce a compact diagnostic such as:

- local bearing / direction of travel
- tee-to-green M distance
- UiDo vs reference delta
- F/M/B depth
- each hazard's UiDo near/far distance vs reference
- left/right classification
- warning when a delta exceeds the configured tolerance

The diagnostic must never silently alter source geometry.

## Runtime role

The same local-frame calculation can later drive the player-facing hole view:

**GPS position → selected hole → direction of travel → local hole frame → SmartPoint / SmartShot context**

The player therefore sees the hole oriented naturally from where they are standing, while the underlying course model remains geospatially anchored.

## Reference

OpenYardage's Overstone Park Golf Club page documents its OSM-derived methodology and publishes hole lengths, green depths, elevation and hazard carry distances. Data on the page is stated as of 2026-09-04.

This reference is used for validation only. UiDo does not copy OpenYardage implementation or proprietary data.
