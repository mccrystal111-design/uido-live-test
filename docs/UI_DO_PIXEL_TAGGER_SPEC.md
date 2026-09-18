# UiDo Pixel Tagger — Priority Specification

## Priority

The pixel tagger is the first technical priority of the UiDo Course Extraction Engine.

Do not build additional tee-specific inference around an unproven tagger. The tagger must first turn fixed aerial imagery into a classified geographic representation.

## Objective

Input:
- fixed satellite/aerial image
- exact geographic bounding box
- optional source course data for anchoring/validation

Output:
- a classification for every pixel or image cell
- confidence for each classification
- a geographic transform from image coordinates to latitude/longitude
- grouped regions/polygons derived from classifications

Initial classes:
1. GREEN
2. TEE
3. FAIRWAY
4. ROUGH
5. BUNKER
6. WATER
7. WOODLAND
8. PATH
9. STRUCTURE
10. OOB
11. UNKNOWN

## Principle

Classify first. Interpret second.

The tagger must not use the known tee GPS to improve its classification. Verified field GPS is a validation layer only.

Known green F/M/B and API yardage may be supplied to downstream inference, but the raw pixel tagger should remain as independent as practical.

## Processing stages

### 1. Acquire imagery
Use one fixed image with a known geographic extent rather than analysing a live slippy-map display.

### 2. Normalise
- record image dimensions
- preserve native pixels
- record bounding box
- establish pixel-to-geographic transform
- optionally normalise illumination/colour carefully without destroying useful turf differences

### 3. Initial classification
For every pixel/image cell, estimate:
- class
- confidence
- supporting visual features

The first prototype may use deterministic visual heuristics. It must clearly identify itself as a prototype and must not claim semantic accuracy that has not been tested.

### 4. Spatial refinement
Use neighbouring pixels/regions to remove isolated noise while preserving genuine boundaries.

### 5. Region formation
Group connected pixels of the same class into regions.

For each region store:
- polygon
- area
- perimeter
- centroid
- shape descriptors
- class confidence
- source image coordinates
- geographic coordinates

### 6. Geographic plausibility
Reject or downgrade impossible regions using conservative constraints.

Examples:
- extremely tiny isolated regions
- impossible feature sizes
- obvious image artefacts

Do not impose golf-specific assumptions too early.

### 7. Course interpretation
Only after the pixel/region layer exists:
- identify green polygons
- identify fairway corridors
- trace playing corridors
- locate tee complexes
- associate hazards
- build hole topology

### 8. Rendering
The renderer consumes the geographic model, not the raw satellite image.

The same model can produce:
- premium UiDo yardage-book view
- phone hole view
- watch view
- strategy/SmartShot overlays

## Pixel output model

Conceptual structure:

pixel/cell:
  x
  y
  latitude
  longitude
  class
  confidence

region:
  class
  polygon
  area
  centroid
  confidence
  evidence

course:
  holes[]
  features[]
  conflicts[]

## Prototype success criteria

The first successful prototype does NOT need perfect classification.

It must demonstrate that:
1. a fixed satellite image can be ingested;
2. pixels/cells can be classified;
3. classifications can be visualised as a colour mask;
4. neighbouring classifications can form coherent regions;
5. regions can be converted back to geographic coordinates;
6. the raw mask and geographic regions agree spatially.

Only then should tee/fairway inference be judged.

## UiDo rendering palette

Initial semantic mapping:

GREEN → UiDo green
TEE → UiDo tee/grass treatment
FAIRWAY → lighter maintained turf
ROUGH → muted natural green
BUNKER → sand/stone
WATER → water treatment
WOODLAND → deep natural green
PATH → stone
STRUCTURE → neutral structure
OOB → boundary treatment
UNKNOWN → satellite/neutral fallback

Exact visual values remain renderer-controlled and should not be hard-coded into extraction logic.

## Validation protocol

Hole 2 is the laboratory.

Extraction input:
- satellite image
- geographic extent
- supplied green F/M/B only where required by downstream interpretation
- Yellow API yardage for downstream validation

Not permitted in extraction:
- actual field-test tee GPS
- field-test tee marker coordinates
- manually placed tee candidate

Validation:
- compare extracted regions/candidates with the independently captured GPS after extraction is complete.

## Long-term target

The final system should be capable of producing a geographically faithful vector course model from imagery, then rendering that model into the UiDo visual language.

The goal is not a photographic copy. It is a structured, editable and geographically meaningful representation of the actual course.
