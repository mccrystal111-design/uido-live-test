# UiDo Course Model v0.1

Provider-neutral course geometry model for phone, watch, yardage-book and renderer consumers.

## Layer contract
- **source**: supplied geometry/data. Never mutate it during extraction.
- **derived**: geometry inferred from imagery/topology. Must include evidence and confidence.
- **verified**: independently measured/mapped ground truth used for validation unless explicitly promoted into a new source dataset.
- **conflict**: two sources disagree; preserve both references and do not silently choose one.

## Registration contract
The course model may contain a registration transform between source geographic geometry and an imagery coordinate frame. The transform is optional and must remain null until measured. Store parameters and error metrics together. Never warp the satellite image to make a source fit.

## Feature contract
Every geometry-bearing feature should carry: id, type, geometry, provenance, confidence, evidence, source_refs, and status. Unknown is valid.

## Hole contract
Each hole contains green F/M/B, zero or more tees, fairways, hazards, context, routing and conflicts. Multiple tee polygons are expected. Missing secondary features must remain missing rather than being invented.

## Current Overstone state
The first committed model contains the 18 supplied green F/M/B anchors only. OSM/satellite registration is explicitly pending recovery of the source artifacts and measured transform. This is intentional: it prevents the model from claiming geometry that is not currently reproducible from repository data.
