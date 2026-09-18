# UiDo Course Pixel Model

## Purpose

The UiDo Course Extractor should not be treated as a tee-box detector. Tee detection is one feature-extraction task inside a broader process that converts aerial/satellite imagery into a structured geographic course model.

The target pipeline is:

SATELLITE IMAGERY
→ PIXEL / REGION CLASSIFICATION
→ GEOGRAPHIC OBJECTS
→ HOLE / COURSE TOPOLOGY
→ UI DO RENDERER

## Source hierarchy

### SOURCE
- Satellite/aerial imagery
- Course/API data
- Known green F/M/B coordinates
- Tee-specific API yardage
- Existing mapped coordinates where supplied

### DERIVED
- Pixel/region class
- Feature masks
- Polygon boundaries
- Feature centroids
- Tee candidates
- Fairway corridors
- Hole routing
- Confidence/evidence
- Conflict markers

### VERIFIED
- Independently captured GPS
- Independently mapped tee/fairway geometry
- Other ground-truth measurements

Verified data must only validate extraction unless explicitly promoted into a new source dataset. It must not silently construct a test claiming independent discovery.

## Initial feature vocabulary

Every image region should be assignable to one of:

- GREEN
- TEE
- FAIRWAY
- ROUGH
- BUNKER
- WATER
- WOODLAND
- PATH
- STRUCTURE
- OOB
- UNKNOWN

UNKNOWN is valid and should be preserved where imagery does not support a confident classification.

## Pixel-to-object process

Pixel classification is not the final geographic model.

1. Acquire a fixed satellite image with a known geographic bounding box.
2. Classify pixels/regions using visual evidence.
3. Apply spatial smoothing so isolated misclassified pixels do not become features.
4. Group neighbouring same-class pixels into connected regions.
5. Remove regions that fail minimum/maximum geographic plausibility checks.
6. Convert retained regions into polygons.
7. Simplify polygon boundaries without materially changing the feature.
8. Preserve confidence and evidence for every polygon.
9. Build relationships between polygons to create hole topology.

The system should retain the raw classification layer separately from the cleaned vector layer so errors can be diagnosed.

## Tee extraction

TEE is detected from the classified image and contextual geometry.

Evidence may include:
- maintained turf signature
- distinct boundary
- deliberate rectangular/elongated geometry
- plausible teeing-area scale
- orientation
- relationship to fairway
- multiple teeing areas
- path/access context
- surrounding features

No single clue is mandatory.

The known green and API yardage define a search constraint; they do not identify the tee.

## Fairway extraction

FAIRWAY regions should be detected independently of the tee.

The hole model may then connect:
TEE → FAIRWAY → DOGLEG / ROUTING → APPROACH → GREEN

A straight tee-to-green line must not be required.

## Green extraction

Known F/M/B points can anchor or validate the green polygon. If a supplied green polygon is unavailable, the visual classifier may generate a green candidate, but this is a separate confidence state.

F/M/B coordinates remain source data and should not be overwritten by the renderer.

## Hazard and context extraction

BUNKER, WATER, WOODLAND, PATH and STRUCTURE are geographic classes, not merely visual decoration.

They can subsequently inform:
- hole routing
- conflict detection
- strategy
- no-go areas
- carry calculations
- visual rendering

Nearby bunkers or absence of bunkers are contextual evidence only, never absolute tee rules.

## Geographic course model

The extracted course should ultimately resemble:

course
  holes[]
    green
      polygon
      F/M/B
    tees[]
      polygon
      centre
      tee_set
      confidence
    fairways[]
      polygon
    hazards[]
      type
      polygon
    context[]
      type
      polygon
    routing
      centreline
      segments
    conflicts[]

The renderer should consume this model rather than re-interpreting satellite imagery.

## Yardage-book generation

The extracted geographic model can drive a separate UiDo visual renderer.

Rendering stages:

1. Take feature polygons from the course model.
2. Apply UiDo colour/style mapping.
3. Simplify geometry for phone/watch readability.
4. Render green, fairway, rough, hazards, woodland, paths and OOB as clean vector shapes.
5. Add F/M/B, yardages and other UiDo overlays.
6. Add strategy/SmartShot layers only after base geometry is stable.

The satellite image is therefore a source document, not the final artwork.

## Important design principle

Do not aim for a literal photographic pixel-for-pixel reproduction.

Aim for a geographically faithful **pixel/region classification first**, followed by a clean vector representation. This produces a smaller, editable, deterministic course model that can be rendered consistently across phone, watch and yardage-book views.

## Validation

For the Hole 2 prototype:

- Green F/M/B: source
- Yellow API yardage: source
- Satellite image: source
- Tee GPS: verification only
- Extracted tee: must be generated without access to tee GPS
- Comparison against tee GPS: final validation step

Success is not simply that a marker lands near the known tee. The system must show which visual/geometric evidence produced the candidate.
