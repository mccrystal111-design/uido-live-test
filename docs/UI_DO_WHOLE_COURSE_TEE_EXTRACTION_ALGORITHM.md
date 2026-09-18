# UiDo Whole-Course Tee Extraction Algorithm — Source of Truth

## Purpose
Build a whole-course tee-box inference system that starts with known green data and satellite imagery, independently proposes teeing areas for every hole, plots the provisional course, then validates the model by looking for conflicts and inconsistencies.

This is an extraction problem, not a coordinate-placement problem.

## Source hierarchy
1. SOURCE — satellite/aerial imagery, green F/M/B data, tee-specific API yardage, course metadata.
2. DERIVED — approach bearings, search regions, candidate tee geometry, fairway paths, confidence/evidence, conflicts.
3. VERIFIED — independently captured GPS or mapped tee geometry, used only after extraction for validation.

Verified GPS must never be read by the candidate-generation stage.

## Inputs
- Course boundary/area or known course extent.
- Hole number and par.
- Green Front, Middle and Back for each hole when available.
- Tee-specific API yardage for each hole.
- Satellite imagery.
- Optional course metadata.
- Verified GPS only in a separate validation layer.

## Whole-course workflow

### 1. Anchor every hole on its known green
For each hole, preserve supplied F/M/B exactly.

- M is the distance reference.
- M → F establishes the approach direction.
- B is retained as green geometry but is not required for tee-search direction.
- Known green coordinates locate the search area; they do not determine the tee.

### 2. Establish the tee search envelope
For the selected tee set:

- Expected playing distance = API yardage.
- Start with a configurable distance tolerance, initially ±20 yd.
- Search behind the green relative to the reverse M → F direction.
- Do not use a fixed angular cone as a hard rule.
- Allow lateral displacement, doglegs and unusual tee layouts.

The distance envelope is a search constraint, not evidence that a point is a tee.

### 3. Generate visual tee candidates
Within each hole's search envelope, inspect satellite imagery for tee-complex characteristics:

- closely maintained/short-mown surface;
- distinct boundary from rough;
- rectangular, elongated or otherwise deliberate teeing shape;
- plausible tee-complex size;
- orientation consistent with the local playing direction;
- multiple adjacent teeing areas;
- connection to a plausible fairway start;
- access/path context where visible.

Contextual clues may include:

- bunkers;
- water;
- woodland/trees;
- paths;
- buildings/maintenance areas;
- flag/flagstick visibility;
- flag shadows or other shadows.

No single clue is mandatory. A nearby bunker is not a disqualifier and the absence of a bunker is not proof of a tee.

### 4. Trace the playing corridor
For each candidate:

TEE → FAIRWAY → TURN/DOGLEG → APPROACH → F/M → GREEN

The fairway is allowed to curve. A straight tee-to-green line is not required.

A candidate that looks like a tee but cannot plausibly connect to the correct fairway/approach should be downgraded.

### 5. Candidate evidence
Keep evidence separate so failures can be diagnosed.

Suggested evidence fields:
- distanceAgreement
- visualTeeGeometry
- teeOrientation
- fairwayConnection
- approachConsistency
- teeSetConsistency
- contextualEvidence
- competingCandidates

Do not collapse these into an unexplained single score.

### 6. Select provisional teeing areas
For each hole, retain:
- best candidate;
- alternative candidates when close;
- centre GPS;
- polygon/bounding geometry where available;
- evidence;
- confidence state: HIGH / MEDIUM / REVIEW.

Multiple tee areas may be associated with one hole.

## Whole-course conflict pass

After all holes have provisional geometry, validate the course as a connected system.

### Spatial conflicts
- Candidate tee overlaps another hole's tee area unexpectedly.
- Candidate is implausibly close to another green.
- Two holes claim the same physical tee complex without a shared-tee explanation.

### Routing conflicts
- Tee cannot connect to a plausible fairway.
- Fairway route does not converge on the assigned green.
- Proposed route contradicts the green approach direction.
- A route crosses another hole in an implausible way.

### Yardage conflicts
- Candidate straight-line distance is far outside the API-derived search envelope.
- Candidate distance is plausible only under an implausible route.
- Different tee-set candidates do not preserve the expected relative ordering.

### Visual conflicts
- Candidate appears to be woodland, bunker, water, building, path or other non-tee surface.
- Candidate lacks any plausible maintained tee geometry.
- Satellite evidence strongly supports another nearby candidate.

## Conflict resolution
Do not silently move a candidate to make the model fit.

If conflicts exist:
1. retain the original candidate;
2. generate alternatives if available;
3. record the conflict;
4. re-evaluate the connected hole model;
5. mark the hole REVIEW if ambiguity remains.

## Whole-course output
Produce one geographic model containing:

- all known greens;
- all provisional tee candidates;
- inferred hole corridors/fairway paths where available;
- candidate polygons;
- confidence/evidence;
- conflict markers.

The primary visual test should show the complete course in one view so a human can immediately inspect whether the model makes sense.

## Validation
Only after extraction:
- compare predicted tee GPS with independently captured GPS or mapped tee geometry;
- calculate position error;
- retain validation separately from extraction output.

A successful test is therefore:

KNOWN GREENS + API YARDAGES + SATELLITE
→ INDEPENDENT TEE EXTRACTION
→ WHOLE-COURSE MODEL
→ CONFLICT CHECK
→ HUMAN VISUAL CHECK
→ OPTIONAL VERIFIED-GPS COMPARISON

## Prototype implementation rule
The geographic/search engine and the visual classifier must be separate modules.

The visual classifier can initially be a heuristic prototype. It must not pretend to have detected visual tee geometry if no imagery classification has actually occurred.

Later, the classifier can be replaced by a proper satellite segmentation/CV model without changing the geographic reasoning or conflict-validation layer.

## Current test data
Overstone Park:
- 18 known greens from course_green_data.json.
- Yellow tee API yardages from the supplied Overstone API data.
- No field-test GPS is used by the extraction engine.

The first whole-course test should deliberately expose the algorithm's provisional candidates and conflicts rather than hiding uncertainty.
