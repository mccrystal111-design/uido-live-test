# UiDo — Project Source of Truth

**Last updated:** 2026-09-21  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

This is the first file a fresh UiDo session should read. It records authoritative data, completed work, current blockers, exact next step, and what must not be rebuilt.

## Current state

**Course data foundation: READY.** Overstone's authoritative OSM capture is recovered and identity-locked; deterministic normalisation and the provider-neutral course model exist. Public EA source resolution is complete. **EA aerial acquisition is now proven end-to-end. LiDAR acquisition, raster post-render and the final provider-neutral course package remain outstanding.**

**Do not start another visual prototype.** The immediate priority is the public-source data/model pipeline and course-package build.

## Authoritative Overstone source

### Raw OSM — authoritative

Do not ask the user to re-upload the OSM capture.

- Library: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
- Library file id: `file_00000000e32481f4a00f707344416e79`
- SHA-256: `e1eebf606f5e2767cfdf2af3951f7e2f50660b5b6b75ff2567af5c755a01b16e`
- GitHub identity lock: `course-models/OVERSTONE_OSM_SOURCE_LOCK.json`
- GitHub manifest: `course-models/OVERSTONE_SOURCE_MANIFEST.json`

Source counts: 18 holes, 18 pins, 20 greens, 30 tees, 17 fairways, 31 bunkers, 23 rough, 17 paths, 2 water hazards, 1 driving range; 177 features total. Only `golf=hole` features carry explicit `ref=1..18`; other feature classes must be associated spatially/derived, never by feature order. fileciteturn239file1

### Normalised source — authoritative derived artifact

- Library: `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json`
- Library file id: `file_0000000052948210969af327286d4488`
- Schema: `uido.course.source-normalized.v0.1`
- SHA-256: `876eb808a978f577057747f71cca759d4032ed5cc776c3bf036eb126ce6b28e9`
- Status: **complete**; source geometry unchanged; no invented hole assignments. Library report confirms 177 features and 141 non-explicit-hole features. fileciteturn239file4

## Course model state

### GitHub canonical model

- `course-models/overstone-park-v0.1.json`
- Schema: `uido.course.v0.1`
- Contains all 18 green F/M/B anchors.
- Registration transform/metrics remain null until measured control points are used.

### Library discrepancy — preserve, do not overwrite

Library contains `/UiDo/UiDo_Overstone_Course_Model_v0.4.json`, a newer generated model with source-preserving geometry, derived hole associations and registration/refinement gates. It is **not promoted as the GitHub canonical model**. Reconcile/version the promotion explicitly; do not delete, recreate or silently replace v0.1.

## EA public-source state

### Catalogue resolution — COMPLETE

Exact Overstone EA coverage is resolved in EPSG:27700.

**Aerial:** 2013, 0.25 m, product `vertical_aerial_photography_tiles_night_time`. Required source ECWs are:
- SP8064 — `P00055683`
- SP8065 — `P00055670`
- SP8164 — `P00055697`
- SP8165 — `P00055618`

**LiDAR:** 1 m survey `P_10738`, flown 2020-01-29 and 2020-03-06; required tiles SP8060 and SP8065, with DSM, DTM, FZ DSM, intensity, LAZ and VOM records already resolved in the repository manifests.

Course footprint: EPSG:27700 E 480137.49–481451.93 / N 264803.28–266016.15.

### Automated aerial acquisition — PROVEN

`.github/workflows/build-overstone-ea.yml` is the active manual acquisition runner. It discovers the EA product/tiles from the fixed Overstone footprint, downloads the EA survey ZIPs, validates ZIP/raster contents, retries failures, records URLs/byte counts/SHA-256 and uploads an artifact.

**Successful proof:** workflow run `35545736650` / commit `75d4c9d9ee5e74de395483c2e1b4c3d6a291b5b2`. Both download steps succeeded and the artifact `overstone-ea-aerial-capture` was created. Artifact id `10616132263`, size 24,883,030 bytes, SHA-256 `90efebca7e9a2980256a1c95389052978e137d01da7b544ec7cd4fe53be22208`, expiry 2026-10-04.

The artifact contains the two required download blocks SP8060/SP8065 and all four required Overstone ECWs (`P00055683`, `P00055670`, `P00055697`, `P00055618`). The acquisition manifest records schema `uido.course.ea-acquisition.v0.2`, product/year/resolution and source hashes. **Do not call aerial acquisition unproven anymore.**

The earlier 12-second failure was a pre-fix product-id assumption. It is retained only as history and is not evidence of EA unavailability.

### Post-render — IMPLEMENTED, NOT YET PROVEN

Commit `44b3fdbbccaf90d2399a7250017f63f536cd945d` adds a compact Overstone render stage after acquisition. It attempts to enable ECW/GDAL, build a VRT over the fixed course footprint, and output approximately 0.5 m/pixel WebP/JPEG overview imagery plus a render manifest.

No successful post-render run/artifact has yet been recorded. **Do not claim phone-ready rendering is proven until the next workflow run is inspected.**

### LiDAR — NOT YET ACQUIRED

Catalogue records are resolved, but no successful automated LiDAR acquisition artifact is recorded. The next LiDAR work must reuse the resolved SP8060/SP8065 records and the existing acquisition architecture; do not rediscover the source manually.

### Production architecture

Phone/watch clients should **not** download raw EA/OSM/LiDAR. Central UiDo acquisition/processing should build a compact provider-neutral course package, then the client downloads that package for offline/on-course use.

`course footprint -> provider adapter -> source catalogue -> source download -> raw archive -> processing/render -> UiDo course package -> API/CDN -> phone/watch`

Manual EA portal downloads are development fallback only, not production-approved.

## Registration / refinement state

Measured OSM-to-raster registration is still a separate stage. `course-models/OVERSTONE_REGISTRATION_CONTROL_POINTS.json` is the control-point template. Do not invent/reuse a transform or use validation GPS as candidate-generation geometry. After fixed raster acquisition, obtain real measured control points, run `register_affine.py`, and record residuals/RMS/max error.

Established refinement remains two-pass: whole-course maintained-surface discovery, then hole-specific refinement constrained by source ROIs. Preserve feature provenance/confidence. LiDAR is intended for terrain/elevation, vegetation/tree structure, height/visibility context and ambiguous geometry refinement.

## UI / product state

The Library remains the source of truth for the current UI: premium golf instrument aesthetic, light/dark system, persistent navigation icon language and the GPS/Yardage/Wind/Lie/Start Line/Shape/Strike live shot flow. The agreed round flow deliberately keeps SmartShot strategy out until the engine is ready. Do not redesign from memory. fileciteturn237file0 fileciteturn237file4

The current UI implementation blueprint explicitly locks shared theme tokens, icon component, tile shell, tile migration, radial navigation and phone/watch continuity before independent tile redesign. fileciteturn237file9

## Outstanding work

1. Prove the new post-render stage on the successful aerial acquisition path.
2. Inspect render output size, runtime, visual extent and georeferencing; determine whether a compact offline course image/tile package is practical for phone download.
3. Build/prove automated EA LiDAR acquisition for SP8060/SP8065.
4. Establish measured OSM-to-raster control points and registration metrics.
5. Build the provider-neutral UiDo course package and review/verification layer.
6. Reconcile Library v0.4 against GitHub v0.1 deliberately before promoting a new canonical model version.

## EXACT NEXT STEP

**Run `.github/workflows/build-overstone-ea.yml` again using the existing Overstone Park / 2013 / 0.25 m defaults, then inspect the new post-render step and artifact.** The acquisition portion is already proven; this run is specifically to prove the compact render stage. Do not change the source data or manually download EA files.

If the render fails, capture the exact GDAL/ECW error and fix only that stage. If it succeeds, measure the resulting package size/runtime and use that evidence to design the first offline UiDo course-package format.

## DO NOT REBUILD

1. **Do not ask for `export (1).geojson` again.** The authoritative OSM capture is recovered and persisted.
2. Do not recreate the normalised source; it is complete and persisted.
3. Do not recreate the course model from screenshots or memory.
4. Do not replace source geometry with derived geometry or silently overwrite verified/source features.
5. Do not invent an OSM-to-raster transform or reuse an unmeasured one.
6. Do not use validation GPS as candidate-generation geometry.
7. Do not generate PNGs merely to demonstrate progress.
8. Do not treat screenshots/diagnostics as the source of truth when underlying data exists.
9. Do not ask the user to repeat information already recorded here, in source manifests/locks, the course model or the Library.
10. If a GitHub artifact appears missing, check its recorded Library/conversation sources and GitHub artifact history before declaring it lost.
11. Do not silently promote Library v0.4 over GitHub v0.1; reconcile and version the promotion explicitly.
12. Do not treat EA catalogue connectivity as equivalent to acquisition — **aerial acquisition is now proven; LiDAR remains unproven**.
13. Do not treat the pre-fix EA failure as a current blocker.
14. Do not replace the working EA aerial runner with manual portal steps.
15. Do not declare the post-render or phone-ready course package complete until an actual successful render artifact has been inspected.

## Change discipline

Whenever meaningful UiDo work changes project state, update this document. If GitHub and Library disagree, inspect both authoritative artifacts, record the discrepancy explicitly, and resolve it deliberately. Never guess or silently overwrite source data.
