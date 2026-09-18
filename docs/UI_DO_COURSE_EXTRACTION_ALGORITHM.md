# UiDo Course Extraction Algorithm — Source of Truth

## Purpose
Define the deterministic process UiDo uses to infer course geometry from satellite imagery and available course data. This document governs test runners and later production extraction.

## Source hierarchy
1. **Source data:** satellite/aerial imagery, API hole/tee yardage, existing mapped coordinates.
2. **Derived data:** bearings, distance bands, search corridors, candidate geometry and confidence.
3. **Verified data:** independently captured GPS or mapped tee/fairway geometry used only to validate or improve the algorithm.

Verified coordinates must never be used to construct a test that claims to have independently found the feature.

## Inputs
- Hole identifier and par.
- Green Front, Middle and Back coordinates when available.
- Tee-specific API playing yardage.
- Satellite imagery in a geographic coordinate system.
- Optional course metadata.
- Optional verified GPS for validation only.

## Stage 1 — Lock the green
- Preserve the supplied F/M/B coordinates exactly.
- Do not move, rotate, reinterpret or redraw the green markers.
- Middle (M) is the reference point for tee-distance inference.
- Front (F) defines the approach direction.
- Back (B) is retained as green data but is **not** used to define the tee search direction.

## Stage 2 — Establish approach direction
Calculate the geographic bearing from **M → F**.
Extend that vector beyond F to represent the approach/playing direction.
The reverse of M → F points into the tee-search side of the hole.

Do not use a line from B → M to define the approach corridor.

## Stage 3 — Establish distance search
For the selected tee colour, take the API hole yardage as the expected playing distance.

Because API playing yardage is not guaranteed to equal straight-line M → tee distance:
- use a configurable tolerance band;
- initial prototype default: **±20 yd**;
- therefore a 154 yd hole searches approximately **134–174 yd** from M.

The band is a search region, not proof of a tee location.

## Stage 4 — Generate candidate tee region
Search geographically behind M relative to the M → F approach direction.

The initial candidate region may use an angular corridor around the reverse approach bearing, but angular limits are **not a hard requirement**. They must be validated against real holes and widened/adapted where tee geometry requires it.

A candidate must satisfy the distance test before it can be considered.

## Stage 5 — Identify tee-box candidates from imagery
Within the geographic search region, inspect satellite imagery for areas consistent with a golf tee complex:
- distinct maintained rectangular/elongated playing surface;
- appropriate scale for a teeing area;
- relationship to the beginning of a fairway;
- sensible orientation relative to the hole;
- multiple tee areas may exist for different tee colours.

The algorithm must identify the geographic area from imagery; it must not simply place a marker at a predetermined or previously captured GPS coordinate.

## Stage 6 — Fairway sense-check
For each candidate tee:
1. Determine the likely playing direction from the tee into the fairway.
2. Trace the visible fairway from the candidate.
3. Allow the fairway to curve or dogleg.
4. Check that the traced fairway ultimately connects with the known approach direction near the green.

For a straight par 3 this may reduce to:
**TEE → FAIRWAY → APPROACH → M/F**

For a dogleg:
**TEE → FAIRWAY → TURN → APPROACH → M/F**

A straight tee-to-green line is therefore not mandatory.

## Stage 7 — Candidate confidence
Evaluate candidates using separate evidence, not a single arbitrary score:
- API distance agreement;
- position within search region;
- tee-box visual geometry;
- tee orientation;
- fairway connection;
- consistency with approach direction;
- consistency across available tee yardages.

The output should retain the evidence and candidate location so failures can be diagnosed.

## Stage 8 — Validation
After an independent candidate is produced, compare it with verified GPS or mapped tee geometry.

Report:
- predicted tee position/area;
- verified position/area;
- distance error;
- directional error;
- which stage accepted/rejected the candidate.

Verified data is validation only.

## Rules for test runners
- Satellite imagery must remain geographically fixed.
- Do not rotate, stretch or transform the source satellite layer to make geometry fit.
- F/M/B markers must use their exact source coordinates.
- Tests must distinguish source, derived and verified layers.
- A visual test should not silently alter the algorithm.
- Any parameter change must be explicit and recorded.

## Current prototype parameters
- API yardage tolerance: ±20 yd.
- Approach reference: M → F.
- Tee-search direction: reverse of M → F.
- Angular corridor: provisional only; do not treat ±20° as locked.
- Satellite: geographic north-up unless a display-only viewport rotation is explicitly requested.
