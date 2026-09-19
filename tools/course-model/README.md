# UiDo Course Model Builder

Deterministic source-normalisation stage for the UiDo course pipeline.

Pipeline: OSM/course source data -> normalise -> UiDo course model -> satellite refinement -> LiDAR enrichment -> verification/fusion -> renderers.

The builder does not fit OSM to satellite imagery, use verified GPS to create candidates, move source geometry to make it look right, invent missing geometry, or generate PNG diagnostics.

It preserves source geometry, normalises common OSM golf tags, associates explicitly tagged features with holes where possible, retains unassigned features, and attaches provenance/evidence.

Inputs: --osm GeoJSON, --greens course_green_data.json, --out generated course model JSON.

Example: python tools/course-model/build_overstone_model.py --osm export.geojson --greens course_green_data.json --out course-models/overstone-park-v0.1.json

## Registration tool

`register_affine.py` fits a measured affine transform from OSM longitude/latitude to satellite pixel coordinates and reports per-control-point residuals plus RMS/max error. It requires real measured control points; validation GPS must not be used as a shortcut.
